#!/usr/bin/env python3
"""Saca el texto en español QUEMADO en el arte de monstruos, para poder venderlo en inglés.

POR QUÉ
───────
19-ago-2026. `idioma.py` hace que el motor escriba en inglés, pero eso sólo alcanza para el
texto que el motor DIBUJA. El inventario (`herramientas/texto_quemado.py`) encontró 12 de 282
PNG con español metido en los píxeles, y los 12 son de **monstruos**: es la única temática
con arte por edad para esas piezas, y ese lote vino con los rótulos escritos.

    topper_2..5            «TOPPER PARA TORTA» · «TOPPER REDONDO» · «TOPPERS PARA CUPCAKES»
                           y «¡FELIZ CUMPLE!» ×2 sobre cinta azul
    etiqueta_botella_2..5  «¡FELIZ CUMPLE!» sobre cinta azul
    cajita_sorpresa_2..5   «CAJITA SORPRESA» sobre banda verde

DOS CLASES DE TEXTO, DOS TRATOS DISTINTOS
─────────────────────────────────────────
1. **Rótulos de la hoja** («CAJITA SORPRESA», «TOPPER PARA TORTA»…). No se imprimen en la
   decoración: están AFUERA del troquel, indicándole al comprador qué es cada cosa. Se
   borran y no se pierde nada — lo que es cada pieza ya lo dice el nombre del archivo.
2. **«¡FELIZ CUMPLE!» sobre la cinta**. Eso SÍ es decoración: va impreso en el topper de la
   torta y en la etiqueta de la botella. Se repinta la cinta y se escribe encima.

SE DETECTA, NO SE ADIVINA
─────────────────────────
La primera versión traía las zonas escritas a mano en fracciones del ancho y el alto. Salió
mal y se vio de una: los parches cayeron al lado de las cintas, que quedaron intactas con su
«¡FELIZ CUMPLE!», y encima aparecieron recuadros blancos en medio del dibujo. Cuatro
variantes de edad del mismo diseño NO están en el mismo lugar.

Ahora se buscan por color y forma, y el color se MIDIÓ del archivo en vez de suponerlo —
que es la otra cosa que salió mal. El segundo intento buscaba los rótulos en «verde
oscuro» y marcaba 46 a 76 zonas por hoja, todas falsas: los rótulos no son verdes, son
**marrón (98, 68, 28)**. O sea que el detector no encontraba ni uno de los suyos mientras
marcaba decenas de monstruos, y aun así «devolvía resultados». Hay que mirar QUÉ marca, no
cuántas marcas hay.

  · **cinta** = mancha AZUL ancha y baja (una cinta es apaisada; un monstruo azul es
    redondo, y ahí se cae solo por la proporción). El texto es el blanco de adentro de la
    SILUETA — por el rectángulo no sirve: las esquinas de una cinta son fondo blanco.
  · **rótulo** = marrón plano rodeado de blanco, en los márgenes de la hoja.
  · **banda** = el rectángulo liso, ancho y bajo de la cajita, pegado al borde de arriba.

Con eso da exacto: 1 banda en la cajita, 2 cintas en la etiqueta, 8 rótulos + 2 cintas en el
topper. Verificado después con el mismo lector de `texto_quemado.py`: 0 español restante.

NO PISA NADA: AGREGA
────────────────────
El resultado se guarda **al lado** del original, como `topper_5.en.png`, y el original no se
toca nunca. `productos._arte_del_idioma` usa el `.en.png` sólo cuando el comprador pidió
inglés.

Se hace así, y no reemplazando, por una razón concreta: **los once kits en español están
vendiendo en Mercado Libre desde el 17-ago**. Un arte que dijera «HAPPY BIRTHDAY» encima del
original arreglaría Etsy rompiendo lo único que hoy factura. Y de paso, `--aplicar` deja de
ser una acción destructiva: si el resultado no gusta, se borran los `.en.png` y listo.

    python3 herramientas/despintar.py             # vista previa en salida/despintado/
    python3 herramientas/despintar.py --marcar    # vista previa MARCANDO lo que detectó
    python3 herramientas/despintar.py --aplicar   # instala los .en.png junto al arte
"""
import os

import sys

import numpy as np
import scipy.ndimage as nd
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, "salida", "despintado")
FONTS = os.path.join(RAIZ, "fonts")

TEXTO_CINTA = "HAPPY BIRTHDAY!"

PIEZAS = [("cajita_sorpresa", range(2, 6)),
          ("etiqueta_botella", range(2, 6)),
          ("topper", range(2, 6))]

# Qué buscar en cada pieza. La cajita sólo tiene rótulo; el topper tiene de los dos.
QUE_BUSCAR = {"cajita_sorpresa": ("banda",),
              "etiqueta_botella": ("cinta",),
              "topper": ("rotulo", "cinta")}  # rotulo = marron sobre blanco


# ── detección ────────────────────────────────────────────────────────────────

def _cintas(a):
    """Manchas AZULES anchas y bajas. Devuelve (caja, forma) — la FORMA importa.

    Devolver sólo el rectángulo no alcanzaba: una cinta es un banderín con colas, así que
    las esquinas de su rectángulo son fondo BLANCO, y buscar «lo blanco de adentro del
    rectángulo» daba una caja de texto del ancho de la cinta entera. El blanco hay que
    buscarlo dentro de la SILUETA."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    azul = (b > 90) & (b > r + 45) & (b > g + 30)
    azul = nd.binary_closing(azul, np.ones((5, 5)))
    lab, n = nd.label(azul)
    H, W = azul.shape
    out = []
    for i, sl in enumerate(nd.find_objects(lab), start=1):
        y0, y1 = sl[0].start, sl[0].stop
        x0, x1 = sl[1].start, sl[1].stop
        w, h = x1 - x0, y1 - y0
        if w * h < (W * H) * 0.00015:          # ruido
            continue
        if w < h * 2.2:                        # una cinta es apaisada; un monstruo, redondo
            continue
        if w > W * 0.98:                       # una banda de punta a punta no es una cinta
            continue
        forma = nd.binary_fill_holes(lab[sl] == i)
        out.append(((x0, y0, x1, y1), forma))
    return out


def _texto_blanco_en(a, caja, forma):
    """Las LETRAS: lo casi blanco que cae DENTRO de la silueta de la cinta."""
    x0, y0, x1, y1 = caja
    sub = a[y0:y1, x0:x1, :3]
    blanco = (sub[..., 0] > 195) & (sub[..., 1] > 195) & (sub[..., 2] > 195) & forma
    # los brillos del pliegue son finitos; las letras, gruesas
    blanco = nd.binary_opening(blanco, np.ones((3, 3)))
    if blanco.sum() < 60:
        return None
    blanco = nd.binary_closing(blanco, np.ones((3, 15)))
    ys, xs = np.nonzero(blanco)
    return (x0 + int(xs.min()), y0 + int(ys.min()),
            x0 + int(xs.max()) + 1, y0 + int(ys.max()) + 1)


COLOR_ROTULO = (98, 68, 28)      # el marrón plano de «TOPPER PARA TORTA» y compañía


def _rotulos_marron(a, tol=42):
    """Los rótulos del topper: MARRÓN PLANO sobre blanco, en los márgenes.

    El color se midió del archivo, no se supuso — y eso resolvió el problema. La primera
    versión buscaba «verde oscuro» y encontraba 46 a 76 zonas por hoja, TODAS falsas: los
    rótulos no son verdes, son marrón (98, 68, 28), así que el detector nunca vio ni uno de
    los que venía a buscar mientras marcaba decenas de monstruos. Un detector que no
    encuentra nada de lo suyo y mucho de lo ajeno igual «devuelve resultados»: por eso hay
    que mirar lo que marca, no cuántas marcas hay."""
    H, W = a.shape[:2]
    dif = np.abs(a[..., :3] - np.array(COLOR_ROTULO)).max(axis=-1)
    marron = dif <= tol
    # las letras de un renglón se pegan al dilatar a lo ancho
    ancho = max(9, int(W * 0.004))
    junto = nd.binary_dilation(marron, np.ones((3, ancho)))
    junto = nd.binary_dilation(junto, np.ones((max(3, int(H * 0.004)), 3)))
    lab, n = nd.label(junto)
    out = []
    for i, sl in enumerate(nd.find_objects(lab), start=1):
        y0, y1 = sl[0].start, sl[0].stop
        x0, x1 = sl[1].start, sl[1].stop
        w, h = x1 - x0, y1 - y0
        if w < W * 0.015 or w > W * 0.45:
            continue
        if h > H * 0.10 or w < h:
            continue
        if marron[sl].mean() < 0.08:          # casi vacío: es ruido pegado
            continue
        m = max(8, int(h * 0.5))
        anillo = a[max(0, y0 - m):min(H, y1 + m), max(0, x0 - m):min(W, x1 + m), :3]
        blanco = ((anillo[..., 0] > 225) & (anillo[..., 1] > 225) &
                  (anillo[..., 2] > 225)).mean()
        if blanco < 0.55:                     # tiene que estar en el margen, no sobre dibujo
            continue
        out.append((x0, y0, x1, y1))
    return out


def _banda_rotulo(a):
    """La BANDA de la cajita: un rectángulo liso, ancho y bajo, arriba de todo.

    Acá NO se busca «texto verde oscuro». Esa fue la primera versión y se disparaba 46 a 76
    veces por hoja: los monstruos tienen partes verde oscuro y quedan rodeados de blanco,
    o sea que cumplían la regla igual que un rótulo. Se busca la BANDA, que sí es
    inconfundible: un bloque de color plano de más de un tercio del ancho, bajito, pegado
    al borde de arriba."""
    H, W = a.shape[:2]
    alto_max = int(H * 0.22)
    zona = a[:alto_max, :, :3]
    # «color plano» = poca variación local. Se compara cada píxel con la mediana de la zona.
    r, g, b = zona[..., 0], zona[..., 1], zona[..., 2]
    verde = (g > r + 10) & (g > b + 10) & (g < 190)
    verde = nd.binary_closing(verde, np.ones((7, 7)))
    lab, n = nd.label(verde)
    out = []
    for i, sl in enumerate(nd.find_objects(lab), start=1):
        y0, y1 = sl[0].start, sl[0].stop
        x0, x1 = sl[1].start, sl[1].stop
        w, h = x1 - x0, y1 - y0
        if w < W * 0.30 or h > H * 0.20 or w < h * 3:
            continue
        # Se TAPAN LOS AGUJEROS antes de medir el relleno. Sin eso la banda se rechazaba
        # sola: las letras blancas son agujeros en el verde, y una banda con «CAJITA
        # SORPRESA» escrito encima no llega nunca al 80% de relleno. O sea que el filtro
        # descartaba justo a la que venía a buscar, por la razón misma por la que la
        # buscaba.
        lleno = nd.binary_fill_holes(lab[sl] == i).mean()
        if lleno < 0.80:                       # un rectángulo lleno, no una silueta irregular
            continue
        out.append((x0, y0, x1, y1))
    return out


# ── pintura ──────────────────────────────────────────────────────────────────

def _color_del_borde(a, caja, margen=8):
    x0, y0, x1, y1 = caja
    H, W = a.shape[:2]
    tiras = []
    if y0 - margen >= 0:
        tiras.append(a[max(0, y0 - margen):y0, x0:x1, :3])
    if y1 + margen < H:
        tiras.append(a[y1:min(H, y1 + margen), x0:x1, :3])
    tiras = [t.reshape(-1, 3) for t in tiras if t.size]
    if not tiras:
        return (255, 255, 255)
    return tuple(int(v) for v in np.median(np.concatenate(tiras, axis=0), axis=0))


def _repintar_cinta(im, a, cinta, forma):
    """Deja la cinta lisa, con su borde intacto, y le escribe el texto en inglés encima.

    TRES INTENTOS QUE NO SIRVIERON, Y POR QUÉ
    ─────────────────────────────────────────
    1. **Rectángulo de color plano sobre el texto.** La cinta es un banderín CURVO: el
       rectángulo se desbordaba por los extremos —azul sobre el fondo blanco— y encima
       tapaba el contorno oscuro. Al 100%, que es como se imprime, se veía de lejos.
    2. **Interpolar columna por columna** entre el píxel de cinta de arriba y el de abajo.
       Respetaba la silueta, pero dejaba vetas verticales: el degradé de la cinta no es
       lineal.
    3. **`cv2.inpaint`.** Reconstruía la textura muy bien pero **el texto seguía legible en
       fantasma**, porque las letras tienen una sombra que la máscara no agarraba. Al
       ampliar la máscara para incluirla, el inpaint se comió el borde de la cinta y lo
       dejó punteado. Peor que antes.

    LO QUE SÍ FUNCIONA es dejar de imitar el degradé: se rellena **todo el interior** de la
    silueta con el azul de la cinta, plano, y se respeta el borde erosionando unos píxeles.
    Queda una cinta lisa —un diseño legítimo, no un remiendo— con su forma y su contorno
    originales. Es menos ambicioso y es lo único que aguanta 300 DPI."""
    x0, y0, x1, y1 = cinta
    # La erosión va PROPORCIONAL al alto de la cinta, no en 11 píxeles fijos: con un valor
    # fijo el relleno plano se comía el contorno oscuro y las cintas quedaban como recortes
    # de papel liso. Dejando un anillo del 12% del alto, el borde y el sombreado del pliegue
    # sobreviven y sólo se aplana el centro, que es donde estaba el texto.
    anillo = max(11, int((y1 - y0) * 0.12)) | 1
    dentro = nd.binary_erosion(forma, np.ones((anillo, anillo)))
    if not dentro.any():
        dentro = nd.binary_erosion(forma, np.ones((11, 11)))
    if not dentro.any():
        dentro = forma
    sub = a[y0:y1, x0:x1, :3]
    vals = sub[dentro]
    # se saca lo casi blanco (las letras) para que el azul no salga lavado
    az = vals[vals.sum(axis=1) < 620]
    base = tuple(int(v) for v in np.median(az if len(az) > 50 else vals, axis=0))

    w, h = x1 - x0, y1 - y0
    masc = Image.fromarray((dentro * 255).astype(np.uint8), "L")
    im.paste(Image.new("RGB", (w, h), base), (x0, y0), masc)

    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dc = ImageDraw.Draw(capa)
    ys, xs = np.nonzero(dentro)
    alto = (ys.max() - ys.min()) * 0.62
    f = _fuente(alto)
    while alto > 8 and dc.textlength(TEXTO_CINTA, font=f) > w * 0.80:
        alto -= max(1, alto * 0.06)
        f = _fuente(alto)
    dc.text((w / 2, (ys.min() + ys.max()) / 2), TEXTO_CINTA, font=f,
            fill=(255, 255, 255, 255), anchor="mm")
    # el texto también recortado a la silueta: una letra que se saliera de la cinta se
    # corta sola en vez de quedar flotando sobre el fondo
    im.paste(capa, (x0, y0),
             Image.composite(capa.split()[3], Image.new("L", (w, h), 0), masc))
    return cinta


def _tapar_texto_de_la_cinta(a, cinta, forma, texto):
    """Devuelve el parche que reemplaza las letras: la cinta SIN texto, con su sombreado.

    La primera versión rellenaba con un azul plano (la mediana) y **se veía el remiendo**:
    la cinta tiene un degradé, así que un bloque de color liso deja el rectángulo marcado.
    Se nota al 100%, que es como se imprime.

    Acá, para cada COLUMNA del recuadro del texto, se toman los píxeles de cinta que hay
    justo arriba y justo abajo —los primeros que caen dentro de la silueta— y se interpola
    entre los dos. Así el parche hereda el sombreado propio de esa columna y el borde
    desaparece."""
    cx0, cy0, cx1, cy1 = cinta
    tx0, ty0, tx1, ty1 = texto
    sub = a[cy0:cy1, cx0:cx1, :3].astype(float)
    hforma = forma
    ry0, ry1 = ty0 - cy0, ty1 - cy0
    parche = np.zeros((ry1 - ry0, tx1 - tx0, 3), float)
    for j, x in enumerate(range(tx0 - cx0, tx1 - cx0)):
        col = hforma[:, x]
        arriba = None
        for y in range(ry0 - 1, -1, -1):
            if col[y]:
                arriba = sub[y, x]
                break
        abajo = None
        for y in range(ry1, sub.shape[0]):
            if col[y]:
                abajo = sub[y, x]
                break
        if arriba is None and abajo is None:
            continue
        if arriba is None:
            arriba = abajo
        if abajo is None:
            abajo = arriba
        t = np.linspace(0, 1, ry1 - ry0)[:, None]
        parche[:, j, :] = arriba * (1 - t) + abajo * t
    return np.clip(parche, 0, 255).astype(np.uint8)


def _color_de_la_cinta(a, cinta, texto):
    """El azul de la cinta: mediana de lo NO blanco de adentro.

    Se saca el blanco a propósito — el blanco son las letras, y promediarlas aclararía el
    parche hasta que se note el remiendo."""
    x0, y0, x1, y1 = cinta
    sub = a[y0:y1, x0:x1, :3].reshape(-1, 3)
    if texto:
        tx0, ty0, tx1, ty1 = texto
        alt = a[y0:y1, x0:x1, :3]
        mask = np.ones(alt.shape[:2], bool)
        mask[ty0 - y0:ty1 - y0, tx0 - x0:tx1 - x0] = False
        sub = alt[mask]
    oscuros = sub[sub.sum(axis=1) < 620]
    if len(oscuros) < 30:
        oscuros = sub
    return tuple(int(v) for v in np.median(oscuros, axis=0))


def _fuente(alto):
    # fuente REDONDEADA: el arte usa una gruesa y redonda, y una Poppins recta al lado de
    # los monstruos se nota que es de otra mano.
    for f in ("Fredoka-VF.ttf", "Baloo2-VF.ttf", "Poppins-Bold.ttf"):
        p = os.path.join(FONTS, f)
        if not os.path.exists(p):
            continue
        fnt = ImageFont.truetype(p, max(10, int(alto)))
        # Fredoka es VARIABLE: cargada sin más sale en su peso liviano, y al lado de una
        # tipografía gorda y redonda como la del arte queda un hilito. Hay que pedirle el
        # peso, no alcanza con elegir el archivo.
        try:
            for ejes in (fnt.get_variation_axes() or []):
                pass
            fnt.set_variation_by_axes([700])
        except Exception:
            pass
        return fnt
    return ImageFont.load_default()


def guardar(im, destino, modo_original):
    """Guarda pesando lo menos posible, sin que se note en la impresión.

    Dos cosas que costaron plata en disco y se aprendieron midiendo:
    1. **Se respeta el modo del original.** El arte de monstruos es RGB, sin transparencia,
       y la primera versión lo guardaba en RGBA: un canal alfa entero, inútil, que hacía
       que el «arreglo» pesara MÁS que el archivo que arreglaba (21,1 MB contra 17,5).
    2. **Paleta de 256 colores.** El topper baja de 21,1 MB a 3,8 MB. Comparado al 100% —que
       es como se imprime, a 300 DPI— no se distingue del original: son ilustraciones de
       colores planos, no fotos."""
    if modo_original != "RGBA":
        im = im.convert("RGB")
    if im.width * im.height > 4_000_000:
        # SIN dithering: son ilustraciones de colores planos, y el ruido del Floyd-Steinberg
        # sólo ensucia las zonas lisas. Con dither la hoja quedaba salpicada.
        q = im.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
        # Y se devuelve el BLANCO a blanco. La cuantización dejaba el fondo en (249,247,249):
        # un gris con tinte lila en TODA la hoja, invisible en miniatura y bien visible
        # impreso en A4. Se corrigen sólo los casi-blancos NEUTROS (canales parejos), para
        # no tocar los cremas del arte, que son casi tan claros pero cálidos.
        pal = q.getpalette() or []
        for i in range(0, len(pal), 3):
            r, g, b = pal[i:i + 3]
            if min(r, g, b) >= 244 and (max(r, g, b) - min(r, g, b)) <= 8:
                pal[i:i + 3] = [255, 255, 255]
        q.putpalette(pal)
        q.save(destino, optimize=True)
    else:
        im.save(destino, optimize=True)


def despintar(ruta, marcar=False):
    base = os.path.basename(ruta)
    pieza = base.rsplit("_", 1)[0]
    buscar = QUE_BUSCAR.get(pieza)
    if not buscar:
        return None, [], None
    modo_original = Image.open(ruta).mode
    im = Image.open(ruta).convert("RGBA")
    a = np.asarray(im).astype(int)
    d = ImageDraw.Draw(im)
    hechas = []

    if "rotulo" in buscar:
        for c in _rotulos_marron(a):
            col = _color_del_borde(a, c)
            if marcar:
                d.rectangle(list(c), outline=(255, 0, 255), width=6)
            else:
                x0, y0, x1, y1 = c
                d.rectangle([x0 - 4, y0 - 4, x1 + 4, y1 + 4], fill=col + (255,))
            hechas.append(("rotulo", c))

    if "banda" in buscar:
        for c in _banda_rotulo(a):
            col = _color_del_borde(a, c)
            if marcar:
                d.rectangle(list(c), outline=(255, 0, 0), width=4)
            else:
                x0, y0, x1, y1 = c
                d.rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 3], fill=col + (255,))
            hechas.append(("banda", c))

    if "cinta" in buscar:
        for cinta, forma in _cintas(a):
            t = _texto_blanco_en(a, cinta, forma)
            if t is None:
                continue
            # el texto tiene que ocupar una parte razonable de la cinta; si es un reflejo
            # o un puntito, no es una palabra
            if (t[2] - t[0]) < (cinta[2] - cinta[0]) * 0.25:
                continue
            if marcar:
                d.rectangle(list(cinta), outline=(0, 160, 255), width=4)
                d.rectangle(list(t), outline=(255, 0, 0), width=3)
            else:
                t = _repintar_cinta(im, a, cinta, forma)
                d = ImageDraw.Draw(im)
            hechas.append(("cinta", t))
    return im, hechas, modo_original


def main():
    aplicar = "--aplicar" in sys.argv
    marcar = "--marcar" in sys.argv
    sub = "marcado" if marcar else ""
    dest = os.path.join(DEST, sub) if sub else DEST
    os.makedirs(dest, exist_ok=True)

    n = 0
    for pieza, edades in PIEZAS:
        for e in edades:
            rel = "temas/monstruos/extras/%s_%d.png" % (pieza, e)
            p = os.path.join(RAIZ, rel)
            if not os.path.exists(p):
                continue
            im, hechas, modo = despintar(p, marcar)
            if im is None:
                continue
            q = os.path.join(dest, "%s_%d.png" % (pieza, e))
            guardar(im, q, modo)
            n += 1
            print("%-30s %d zona(s): %s" % (
                os.path.basename(rel), len(hechas),
                ", ".join("%s%s" % (k, v) for k, v in hechas) or "NINGUNA"))
            if aplicar and not marcar:
                # se AGREGA al lado; el original ni se abre para escribir
                destino = p[:-4] + ".en.png"
                guardar(im, destino, modo)
                print("     instalado -> %s" % os.path.relpath(destino, RAIZ))
    print("\n%d archivos -> %s" % (n, os.path.relpath(dest, RAIZ)))
    if aplicar and not marcar:
        print("INSTALADO como .en.png junto al arte. Los originales NO se tocaron:\n"
              "el español sigue exactamente igual, que es lo que vende en Mercado Libre.")
    else:
        print("Vista previa nada más: no se instaló nada.")


if __name__ == "__main__":
    main()
