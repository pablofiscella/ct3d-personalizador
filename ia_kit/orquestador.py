"""Orquesta la generación de todas las piezas de un tema hacia ia_draft/."""
import concurrent.futures
import glob
import os

from PIL import Image, ImageDraw, ImageFilter

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


def _stickers_individuales(im):
    """Extrae cada sticker (componente conexa) del sheet ya sin fondo y le pone su borde
    die-cut COMPLETO por separado (sin vecinos que se lo coman / sin cortes en el borde).
    Devuelve (lista de RGBA recortados, n_figuras)."""
    im = im.convert("RGBA")
    W, H = im.size
    a = im.getchannel("A").point(lambda p: 255 if p > 10 else 0)
    esc = min(1.0, 320.0 / max(W, H))
    sw, sh = max(8, int(W * esc)), max(8, int(H * esc))
    sm0 = a.resize((sw, sh)).point(lambda p: 255 if p > 128 else 0)
    sm0 = _rellenar_huecos(sm0)
    label, n = _etiquetar(sm0)
    pts = {}                                             # pixeles de cada figura (1 pasada)
    for y in range(sh):
        row = label[y]
        for x in range(sw):
            k = row[x]
            if k:
                pts.setdefault(k, []).append((x, y))
    stickers = []
    for plist in pts.values():
        if len(plist) < 6:                               # ruido / motas
            continue
        mk = Image.new("L", (sw, sh), 0)
        ImageDraw.Draw(mk).point(plist, fill=255)
        mkf = mk.resize((W, H)).point(lambda p: 255 if p > 100 else 0)
        bb = mkf.getbbox()
        if not bb:
            continue
        fig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fig.paste(im, (0, 0), mkf)                       # solo el arte de ESTA figura
        stickers.append(_borde_sticker(fig.crop(bb)))    # su borde completo, aislado
    return stickers, n


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
    for i, s in enumerate(stickers):
        r, c = divmod(i, cols)
        maxw, maxh = cw * 0.82, ch * 0.82                # margen claro dentro de la celda
        if s.width > maxw or s.height > maxh:
            f = min(maxw / s.width, maxh / s.height)
            s = s.resize((max(1, int(s.width * f)), max(1, int(s.height * f))), Image.LANCZOS)
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


def contar_faltantes(temas_dir, tema, edades, solo=None):
    """Cuántas piezas FALTAN en el draft (las que ya están no se vuelven a generar)."""
    draft = os.path.join(temas_dir, tema, "ia_draft")
    return sum(1 for p in catalogo.PIEZAS if not (solo and p.key not in solo)
               for edad in _edades_de(p, edades, solo)
               if not os.path.exists(os.path.join(draft, _nombre_pieza(p, edad))))


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

    # solo_faltantes: saltea las piezas que YA están en el draft (para completar una tanda
    # que falló a mitad, sin rehacer ni gastar de más).
    work = [(p, edad) for p in catalogo.PIEZAS
            if not (solo and p.key not in solo)
            for edad in _edades_de(p, edades, solo)
            if not (solo_faltantes and os.path.exists(os.path.join(draft, _nombre_pieza(p, edad))))]

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
                      "número grande de edad: poné el número %d en lugar del %d."
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
