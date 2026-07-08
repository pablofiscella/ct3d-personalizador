"""Orquesta la generación de todas las piezas de un tema hacia ia_draft/."""
import concurrent.futures
import glob
import os

from PIL import Image, ImageChops, ImageDraw, ImageFilter

import quitar_fondo
from . import catalogo
from . import cajita as ia_cajita
from .validate import validar_png

# Piezas que son un único círculo: se recortan a una máscara circular por código,
# así nada queda fuera del círculo (el prompt solo no lo garantiza).
_MASCARA_CIRCULAR = {"topper", "base_torta"}

# Piezas que se imprimen y cortan por contorno: fondo transparente + borde blanco,
# silueta sólida sin huecos (el software de print&cut corta offset del borde).
_DIE_CUT = {"stickers", "topper_palito"}   # figuras die-cut (borde + recorte); el resto rectangular/circular

# Piezas de diseño COMPLETO que deben tener SIEMPRE fondo opaco (llenan el rectángulo).
# gpt-image-2 a veces devuelve el fondo transparente aunque se le pida con color -> se
# aplana sobre blanco por código para GARANTIZAR que no queden "sin fondo".
_FONDO_SOLIDO = {"separadores", "etiqueta_botella", "tarjetas_agradecimiento", "wrappers_cupcakes"}


def _aplanar_blanco(im):
    """Compone la imagen sobre un fondo BLANCO opaco: rellena las zonas transparentes que
    OpenAI deja aunque se le pida fondo de color. Garantiza que la pieza tenga fondo."""
    im = im.convert("RGBA")
    base = Image.new("RGBA", im.size, (255, 255, 255, 255))
    base.alpha_composite(im)
    return base


def _rellenar_huecos(mask):
    """Rellena huecos internos (transparentes encerrados) de una máscara binaria L."""
    w, h = mask.size
    work = Image.new("L", (w + 2, h + 2), 0)
    work.paste(mask, (1, 1))
    ImageDraw.floodfill(work, (0, 0), 128)                # exterior alcanzable -> 128
    work = work.crop((1, 1, w + 1, h + 1))
    return work.point(lambda p: 0 if p == 128 else 255)   # sólido = forma + huecos


def _borde_sticker(im, frac=0.02):
    """Die-cut: silueta SÓLIDA (cierra gaps finos y rellena huecos internos) + borde blanco.
    TODA la morfología se hace en baja resolución (MaxFilter a full-res con kernel grande es
    lentísimo); la máscara final se escala a resolución completa. El arte va crudo encima."""
    im = im.convert("RGBA")
    w, h = im.size
    a = im.getchannel("A").point(lambda p: 255 if p > 10 else 0)
    esc = min(1.0, 384.0 / max(w, h))
    sw, sh = max(8, int(w * esc)), max(8, int(h * esc))
    ks = min(2 * max(2, int(min(sw, sh) * frac * 1.5)) + 1, 21)   # cerrar gaps
    kb = min(2 * max(2, int(min(sw, sh) * frac)) + 1, 21)         # borde
    sm = a.resize((sw, sh)).point(lambda p: 255 if p > 128 else 0)
    sm = sm.filter(ImageFilter.MaxFilter(ks))             # cerrar gaps finos
    sm = _rellenar_huecos(sm)                             # rellenar huecos encerrados
    sm = sm.filter(ImageFilter.MinFilter(ks))             # restaurar (close morfológico)
    sm = sm.filter(ImageFilter.MaxFilter(kb))             # + borde blanco
    borde = sm.resize((w, h)).point(lambda p: 255 if p > 128 else 0)
    base = Image.composite(Image.new("RGBA", (w, h), (255, 255, 255, 255)),
                           Image.new("RGBA", (w, h), (0, 0, 0, 0)), borde)
    base.alpha_composite(im)                              # arte crudo encima; huecos quedan blancos
    bb = base.getbbox()
    return base.crop(bb) if bb else base


def _etiquetar(fg):
    """Connected-Component Labeling (BFS): devuelve (label[y][x], n_figuras). 0 = fondo."""
    from collections import deque
    w, h = fg.size
    px = fg.load()
    label = [[0] * w for _ in range(h)]
    n = 0
    for y in range(h):
        for x in range(w):
            if px[x, y] > 128 and label[y][x] == 0:
                n += 1
                label[y][x] = n
                q = deque([(x, y)])
                while q:
                    cx, cy = q.popleft()
                    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                        if 0 <= nx < w and 0 <= ny < h and px[nx, ny] > 128 and label[ny][nx] == 0:
                            label[ny][nx] = n
                            q.append((nx, ny))
    return label, n


def _cerrar(mask, frac=0.015):
    """Close morfológico en baja resolución (rápido) reescalado a full-res: reconecta una figura
    PARTIDA por una franja transparente fina SIN unir vecinos bien separados (kernel chico)."""
    w, h = mask.size
    esc = min(1.0, 384.0 / max(w, h))
    sw, sh = max(8, int(w * esc)), max(8, int(h * esc))
    ks = min(2 * max(2, int(min(sw, sh) * frac)) + 1, 15)
    sm = mask.resize((sw, sh)).point(lambda p: 255 if p > 128 else 0)
    sm = sm.filter(ImageFilter.MaxFilter(ks)).filter(ImageFilter.MinFilter(ks))
    return sm.resize((w, h)).point(lambda p: 255 if p > 128 else 0)


def _stickers_individuales(im):
    """Extrae cada sticker (componente conexa) a RESOLUCIÓN COMPLETA con floodfill: conserva el
    detalle fino (brazos/colas/patas) Y aísla la figura del vecino aunque caiga en el mismo
    rectángulo (la máscara es solo lo conexo, no el rectángulo). Devuelve (lista RGBA, n)."""
    im = im.convert("RGBA")
    W, H = im.size
    abin = _rellenar_huecos(im.getchannel("A").point(lambda p: 255 if p > 10 else 0))
    # link = silueta con gaps finos cerrados: se usa SOLO para agrupar (que una figura partida
    # por una franja transparente no quede en dos mitades); el recorte final sigue el alpha crudo.
    link = _cerrar(abin)
    # etiquetado en baja resolución: rápido, solo para ubicar cada figura (bbox + semilla)
    esc = min(1.0, 320.0 / max(W, H))
    sw, sh = max(8, int(W * esc)), max(8, int(H * esc))
    sm = link.resize((sw, sh)).point(lambda p: 255 if p > 128 else 0)
    label, n = _etiquetar(sm)
    boxes = {}
    for y in range(sh):
        row = label[y]
        for x in range(sw):
            k = row[x]
            if not k:
                continue
            b = boxes.get(k)
            if b is None:
                boxes[k] = [x, y, x, y]
            else:
                b[0] = min(b[0], x); b[1] = min(b[1], y)
                b[2] = max(b[2], x); b[3] = max(b[3], y)
    work = link.copy()
    wpx = work.load()
    sx, sy = W / sw, H / sh
    pad = int(0.04 * min(W, H))
    mindim = max(8, int(0.05 * min(W, H)))
    stickers = []
    for b in boxes.values():
        x0 = max(0, int(b[0] * sx) - pad); y0 = max(0, int(b[1] * sy) - pad)
        x1 = min(W, int((b[2] + 1) * sx) + pad); y1 = min(H, int((b[3] + 1) * sy) + pad)
        seed = None                                      # un pixel fg de esta figura
        for yy in range(y0, y1, 2):
            for xx in range(x0, x1, 2):
                if wpx[xx, yy] == 255:
                    seed = (xx, yy); break
            if seed:
                break
        if not seed:
            continue
        ImageDraw.floodfill(work, seed, 128)             # rellena SOLO la figura conexa (full res)
        region = work.crop((x0, y0, x1, y1))
        comp = region.point(lambda p: 255 if p == 128 else 0)   # máscara exacta (excluye vecinos)
        comp = ImageChops.multiply(comp, abin.crop((x0, y0, x1, y1)))   # recorte = alpha crudo (detalle)
        work.paste(region.point(lambda p: 0 if p == 128 else p), (x0, y0))   # marcar visitado
        bb = comp.getbbox()
        if not bb or max(bb[2] - bb[0], bb[3] - bb[1]) < mindim:
            continue
        comp = comp.crop(bb)
        fig = im.crop((x0 + bb[0], y0 + bb[1], x0 + bb[2], y0 + bb[3]))
        cut = Image.new("RGBA", fig.size, (0, 0, 0, 0))
        cut.paste(fig, (0, 0), comp)                     # solo esta figura, con TODO su detalle
        stickers.append(cut)                             # SIN borde: el borde uniforme va al final
    return stickers, n


def _sticker_borde(fig, ancho):
    """Borde blanco de ancho UNIFORME alrededor de la figura (die-cut), a la resolución final
    (después de escalar) para que TODOS los stickers tengan el mismo margen siguiendo el contorno."""
    fig = fig.convert("RGBA")
    m = ancho + 2
    w, h = fig.size
    padded = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    padded.paste(fig, (m, m))
    a = _rellenar_huecos(padded.getchannel("A").point(lambda p: 255 if p > 40 else 0))
    a = a.filter(ImageFilter.MaxFilter(2 * max(1, ancho) + 1))   # dilatación uniforme exacta
    W2, H2 = padded.size
    base = Image.composite(Image.new("RGBA", (W2, H2), (255, 255, 255, 255)),
                           Image.new("RGBA", (W2, H2), (0, 0, 0, 0)), a)
    base.alpha_composite(padded)                         # arte crudo encima
    bb = base.getbbox()
    return base.crop(bb) if bb else base


def _regrid_stickers(stickers, W, H, menos=1):
    """Reacomoda TODOS los stickers en una grilla con 1 columna menos que el empaque ajustado
    (más espacio horizontal) y las filas necesarias para que entren todos, cada uno centrado
    con margen claro en su celda -> contornos completos y separados. Devuelve (imagen, 0)."""
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    N = len(stickers)
    if not N:
        return out, 0
    base = int(N ** 0.5)                                  # grilla ~cuadrada que entra justa
    if base * base < N:
        base += 1
    cols = max(1, base - menos)                           # 1 columna menos -> más aire
    rows = (N + cols - 1) // cols                         # filas para que entren TODOS
    cw, ch = W / cols, H / rows
    ancho = max(2, int(min(W, H) * 0.003))                # margen UNIFORME (fino) para TODOS
    for i, s in enumerate(stickers):
        r, c = divmod(i, cols)
        maxw, maxh = cw * 0.74, ch * 0.74                # dejar lugar para el borde + aire
        if s.width > maxw or s.height > maxh:
            f = min(maxw / s.width, maxh / s.height)
            s = s.resize((max(1, int(s.width * f)), max(1, int(s.height * f))), Image.LANCZOS)
        s = _sticker_borde(s, ancho)                     # borde uniforme DESPUÉS de escalar
        cx, cy = cw * (c + 0.5), ch * (r + 0.5)
        out.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))
    return out, 0


def _plancha_stickers(im):
    """Plancha de stickers: extrae cada figura con su borde die-cut completo y las reacomoda
    en grilla con más espacio (1 fila y 1 columna menos). Devuelve (imagen, pocas_figuras)."""
    im = im.convert("RGBA")
    stickers, n = _stickers_individuales(im)
    out, _descartados = _regrid_stickers(stickers, im.size[0], im.size[1])
    return out, (n < 4)


def _palito(im):
    """Agrega un PALITO (dowel de madera) sólido abajo-centro a una figura die-cut, con borde
    blanco, como cake topper para clavar. La IA solo hace la escena; el palito (pieza técnica)
    lo pone el código, así no queda hueco/roto como cuando lo dibuja la IA con líneas finas."""
    im = im.convert("RGBA")
    w, h = im.size
    pw = max(10, int(w * 0.035))                  # palito fino
    pl = max(60, int(h * 0.55))                   # largo del palito
    b = max(5, pw // 2)                            # borde blanco
    out = Image.new("RGBA", (w, h + pl), (0, 0, 0, 0))
    out.alpha_composite(im, (0, 0))
    cx = w // 2
    y0 = h - int(h * 0.06)                         # arranca un poco dentro del cuerpo
    d = ImageDraw.Draw(out)
    d.rounded_rectangle([cx - pw // 2 - b, y0, cx + pw // 2 + b, y0 + pl + b],
                        radius=pw, fill=(255, 255, 255, 255))           # borde blanco
    d.rounded_rectangle([cx - pw // 2, y0, cx + pw // 2, y0 + pl],
                        radius=pw // 2, fill=(201, 160, 106, 255))      # madera
    bb = out.getbbox()
    return out.crop(bb) if bb else out


def _limpiar_colorear(im):
    """Garantiza line art B/N PURO para la página de colorear: aplana sobre blanco, umbral
    (mata cualquier gris/sombra que el modelo cuele) y engrosa apenas el trazo. El modelo
    dibuja la estética; el código asegura el blanco y negro (nunca un blob gris)."""
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    g = bg.convert("L").point(lambda v: 0 if v < 165 else 255)   # B/N puro
    g = g.filter(ImageFilter.MinFilter(3))                       # trazo un poco más grueso
    return g.convert("RGBA")


def _mascara_circular(im):
    im = im.convert("RGBA")
    w, h = im.size
    d = min(w, h)
    x0, y0 = (w - d) // 2, (h - d) // 2
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse([x0, y0, x0 + d - 1, y0 + d - 1], fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    bb = out.getbbox()
    return out.crop(bb) if bb else out

# invitacion es el único slot que va a la raíz temas/<tema>/; el resto va a extras/.


def _refs(tema_dir):
    # Referencias visuales para OpenAI: primero los cutouts de recortes/; si no hay,
    # el arte base del tema (invitación/afiche), que ya muestra los personajes y el estilo.
    paths = sorted(glob.glob(os.path.join(tema_dir, "recortes", "*.png")))
    if not paths:
        paths = (sorted(glob.glob(os.path.join(tema_dir, "invitacion_*.png")))
                 + sorted(glob.glob(os.path.join(tema_dir, "afiche_*.png"))))
    return [open(p, "rb").read() for p in paths[:10]]  # OpenAI admite hasta 16


def _guardar(im, draft_dir, nombre):
    os.makedirs(draft_dir, exist_ok=True)
    im.save(os.path.join(draft_dir, nombre))


def _edades_de(p, edades, solo):
    """Qué edades genera una pieza en el batch (1 sola fuente de verdad para generar/contar).
    invitación (UNA_SOLA) y afiche (REPLICABLE) generan solo la 1ª edad; el resto, todas."""
    if p.por_edad and p.key in catalogo.UNA_SOLA:
        return [edades[0]]
    if p.por_edad and p.key in catalogo.REPLICABLE and not solo:
        return [edades[0]]
    return edades if p.por_edad else [None]


def contar_piezas(edades, solo=None):
    """Cuántas piezas generará generar_tema (para la barra de progreso)."""
    return sum(len(_edades_de(p, edades, solo)) for p in catalogo.PIEZAS
               if not (solo and p.key not in solo))


def _nombre_pieza(p, edad):
    # El nombre de archivo debe matchear lo que productos._piezas_kit levanta.
    if p.key == "invitacion":
        return "invitacion_%d.png" % int(edad)              # -> slot raíz vía aprobar
    if p.key in catalogo.EXTRAS_POR_EDAD:
        e = int(edad) if p.por_edad else 1                  # arte único -> _1 (el motor lo reusa)
        return "%s_%d.png" % (p.key, e)                     # -> extras/
    return "%s.png" % p.key                                 # universal -> extras/


def _pieza_existe(tema_dir, nombre):
    """Una pieza cuenta como generada si está en el DRAFT o ya APROBADA en
    extras/ — mirar solo el draft hacía que un tema con todo el arte aprobado
    (draft vacío tras aprobar) figurara como 'faltan todas' y el incremental
    regenerara el kit entero al pedo (bug real, detectado con artistas)."""
    return (os.path.exists(os.path.join(tema_dir, "ia_draft", nombre)) or
            os.path.exists(os.path.join(tema_dir, "extras", nombre)))


def contar_faltantes(temas_dir, tema, edades, solo=None):
    """Cuántas piezas FALTAN (ni en draft ni aprobadas en extras)."""
    tema_dir = os.path.join(temas_dir, tema)
    return sum(1 for p in catalogo.PIEZAS if not (solo and p.key not in solo)
               for edad in _edades_de(p, edades, solo)
               if not _pieza_existe(tema_dir, _nombre_pieza(p, edad)))


def generar_tema(client, temas_dir, tema, edades, progress=None, solo=None,
                 quitar=quitar_fondo.remove_bg, concurrencia=4, calidad="medium",
                 reusar_maestra=False, solo_faltantes=False):
    tema_dir = os.path.join(temas_dir, tema)
    draft = os.path.join(tema_dir, "ia_draft")
    pal = catalogo.paleta_de(temas_dir, tema)
    refs = _refs(tema_dir)
    if not refs:
        raise RuntimeError(
            "El tema '%s' no tiene imágenes de referencia: subí personajes a "
            "recortes/ o cargá el arte base (invitacion_*/afiche_*)." % tema)
    # imagen maestra de estilo: ancla de consistencia, se manda como ref extra.
    # Se cachea en ia_maestra.png (fuera de ia_draft, no se publica) para reusarla al
    # regenerar una pieza suelta -> regenerar = 1 sola llamada, sin rehacer la maestra.
    cache_maestra = os.path.join(tema_dir, "ia_maestra.png")
    if reusar_maestra and os.path.exists(cache_maestra):
        with open(cache_maestra, "rb") as f:
            maestra = f.read()
    else:
        maestra = client.editar(refs, "Lámina maestra de estilo del tema. " +
                                catalogo.bloque_estilo(pal), catalogo._SQUARE, quality=calidad)
        with open(cache_maestra, "wb") as f:
            f.write(maestra)
    refs_full = refs + [maestra]
    os.makedirs(draft, exist_ok=True)

    # solo_faltantes: saltea las piezas que YA están (en el draft o aprobadas en
    # extras/ — ver _pieza_existe), para completar una tanda sin gastar de más.
    work = [(p, edad) for p in catalogo.PIEZAS
            if not (solo and p.key not in solo)
            for edad in _edades_de(p, edades, solo)
            if not (solo_faltantes and _pieza_existe(tema_dir, _nombre_pieza(p, edad)))]

    def _trabajo(p, edad):
        # corre en un thread; captura sus propios errores y devuelve el evento.
        try:
            aviso = ""
            raw = client.editar(refs_full, catalogo.prompt_de(pal, p, edad), p.size,
                                 quality=calidad)
            im = validar_png(raw, size_esperado=tuple(int(x) for x in p.size.split("x")))
            im = im.convert("RGBA")
            if p.key == "cajita_sorpresa":     # la IA da la decoración; el molde lo arma el código
                im = ia_cajita.armar_cajita(im, pal)
            elif p.key in _MASCARA_CIRCULAR:    # círculo garantizado por código
                im = _mascara_circular(im)
            elif p.key in _DIE_CUT:            # die-cut: transparente + borde blanco, sin huecos
                im = quitar(im, protect=True)
                if p.key == "stickers":       # borde ADAPTATIVO: que no se peguen entre sí
                    im, tocan = _plancha_stickers(im)
                    if tocan:
                        aviso = "algunos stickers se tocan en el arte; conviene regenerar"
                else:
                    im = _borde_sticker(im)
                    if p.key == "topper_palito":  # + palito de madera sólido por código
                        im = _palito(im)
            elif p.key == "colorear":          # line art: el código garantiza B/N puro
                im = _limpiar_colorear(im)
            elif p.key in _FONDO_SOLIDO:       # diseño completo: fondo opaco garantizado
                im = _aplanar_blanco(im)
            elif p.recorte:
                im = quitar(im, protect=True)
                bb = im.getbbox()
                if bb:
                    im = im.crop(bb)
            nombre = _nombre_pieza(p, edad)
            _guardar(im, draft, nombre)
            # OJO: la invitación (UNA_SOLA) queda como UN solo draft (1 tarjeta en el panel);
            # la copia a todas las edades se hace al APROBAR (ia_kit/aprobar.py).
            return {"pieza": p.key, "edad": edad, "ok": True, "error": "", "archivo": nombre,
                    "aviso": aviso}
        except Exception as e:  # una pieza que falla no frena a las demás
            return {"pieza": p.key, "edad": edad, "ok": False, "error": str(e), "archivo": ""}

    generadas, errores = [], []
    # Las piezas se generan en paralelo (gpt-image-2 es lento); el thread principal
    # es el único que emite progreso y acumula -> sin necesidad de locks.
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, concurrencia)) as ex:
        futs = [ex.submit(_trabajo, p, edad) for (p, edad) in work]
        for fut in concurrent.futures.as_completed(futs):
            evt = fut.result()
            if progress:
                progress(evt)
            (generadas if evt["ok"] else errores).append(evt)
    return {"generadas": generadas, "errores": errores}


def replicar_pieza(client, temas_dir, tema, pieza_key, edades, progress=None, calidad="medium"):
    """Replica <pieza>_<edades[0]> a las demás edades cambiando SOLO el número, usando esa
    imagen como referencia (mantiene composición/colores/estilo). Para piezas con número
    por edad (afiche): generás la 1ª, la revisás y replicás el resto."""
    p = next((x for x in catalogo.PIEZAS if x.key == pieza_key), None)
    if p is None:
        raise RuntimeError("pieza desconocida: %s" % pieza_key)
    draft = os.path.join(temas_dir, tema, "ia_draft")
    base_edad = int(edades[0])
    base_path = os.path.join(draft, "%s_%d.png" % (pieza_key, base_edad))
    if not os.path.exists(base_path):
        raise RuntimeError("Generá primero el %s de %d año antes de replicar." % (pieza_key, base_edad))
    with open(base_path, "rb") as f:
        base = f.read()
    size_t = tuple(int(x) for x in p.size.split("x"))
    generadas, errores = [], []
    for edad in edades:
        if int(edad) == base_edad:
            continue
        nombre = "%s_%d.png" % (pieza_key, int(edad))
        try:
            prompt = ("Reproducí esta lámina EXACTAMENTE IGUAL —misma composición, personajes, "
                      "colores, fondo, recuadro y estilo, sin mover ni cambiar nada— EXCEPTO el "
                      "número grande de edad: poné el número %d en lugar del %d. El número nuevo "
                      "con EXACTAMENTE el mismo estilo, tamaño, grosor, color y RELLENO que el "
                      "original: si el número original es de CONTORNO hueco (relleno claro), el "
                      "nuevo también hueco de contorno; NO lo dibujes macizo/relleno de color."
                      % (int(edad), base_edad))
            raw = client.editar([base], prompt, p.size, quality=calidad)
            im = validar_png(raw, size_esperado=size_t).convert("RGBA")
            _guardar(im, draft, nombre)
            ev = {"pieza": pieza_key, "edad": edad, "ok": True, "error": "", "archivo": nombre}
        except Exception as e:
            ev = {"pieza": pieza_key, "edad": edad, "ok": False, "error": str(e), "archivo": ""}
        if progress:
            progress(ev)
        (generadas if ev["ok"] else errores).append(ev)
    return {"generadas": generadas, "errores": errores}


def generar_variantes_colorear(client, temas_dir, tema, n=3, calidad="low",
                               intentos_por_variante=4, progress=None):
    """Genera N variantes DISTINTAS de la página 'colorear' (colorear.png, colorear_2.png, …):
    el cuaderno de actividades usa hasta 3 escenas distintas y si faltan cae a un fallback
    algorítmico (line-art por bordes) que con personajes de IA sombreados da un blob negro
    ilegible — más vale tener las 3. OpenAI a veces RECHAZA la generación por moderación de
    forma aleatoria (la MISMA referencia a veces pasa, a veces no, típico en escenas de acción)
    -> cada variante reintenta sola hasta `intentos_por_variante` veces."""
    tema_dir = os.path.join(temas_dir, tema)
    draft = os.path.join(tema_dir, "ia_draft")
    p = next((x for x in catalogo.PIEZAS if x.key == "colorear"), None)
    if p is None:
        raise RuntimeError("pieza desconocida: colorear")
    pal = catalogo.paleta_de(temas_dir, tema)
    refs = _refs(tema_dir)
    if not refs:
        raise RuntimeError("el tema no tiene recortes/arte base para usar de referencia")
    size_t = tuple(int(x) for x in p.size.split("x"))
    prompt = catalogo.prompt_de(pal, p)
    # Cada variante con una COMPOSICIÓN distinta obligatoria: con el mismo prompt
    # las 3 salían casi idénticas (mismos personajes, mismo encuadre — feedback
    # Pablo 8-jul-2026, princesas) y el cuaderno repetía el dibujo.
    composiciones = [
        " COMPOSICIÓN de esta variante: UN solo personaje del tema bien GRANDE "
        "en primer plano, simple, con 2-3 objetos icónicos del tema alrededor.",
        " COMPOSICIÓN de esta variante: DOS personajes del tema haciendo una "
        "actividad juntos (jugando, bailando, explorando), encuadre medio — "
        "escena DIFERENTE a un retrato grupal estático.",
        " COMPOSICIÓN de esta variante: el LUGAR del tema en plano general "
        "(el escenario completo, bien detallado para colorear) con un personaje "
        "chiquito integrado en la escena.",
    ]
    generadas, errores = [], []
    for i in range(n):
        nombre = "colorear.png" if i == 0 else "colorear_%d.png" % (i + 1)
        prompt_i = prompt + composiciones[i % len(composiciones)]
        ok, ultimo_error, bloqueada = False, "", False
        for intento in range(1, intentos_por_variante + 1):
            try:
                raw = client.editar(refs, prompt_i, p.size, quality=calidad)
                im = validar_png(raw, size_esperado=size_t).convert("RGBA")
                im = _limpiar_colorear(im)
                _guardar(im, draft, nombre)
                ok = True
                break
            except Exception as e:
                ultimo_error = str(e)
                bloqueada = "moderation" in ultimo_error.lower()
                if progress:
                    progress({"pieza": "colorear", "variante": i + 1, "intento": intento,
                              "ok": False, "reintentando": True,
                              "error": ultimo_error, "archivo": ""})
                if not bloqueada:   # error real (no moderación) -> no insistir de más
                    break
        ev = {"pieza": "colorear", "variante": i + 1, "ok": ok,
              "archivo": nombre if ok else "", "error": "" if ok else ultimo_error}
        if progress:
            progress(ev)
        (generadas if ok else errores).append(ev)
    return {"generadas": generadas, "errores": errores}
