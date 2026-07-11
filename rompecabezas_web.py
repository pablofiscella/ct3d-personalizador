#!/usr/bin/env python3
"""rompecabezas_web.py — Rompecabezas INTERACTIVO (producto digital vivo).

El producto ES un link (/armar/<token>): una web app táctil donde el chico ARMA
rompecabezas de las escenas de su temática, arrastrando piezas con encastres
reales hasta completar la imagen. Espejo de actividades_web.py (mismo contrato):

  - carpeta por token en rompecabezas_web/<token>/ (gitignored, runtime)
  - manifest.json = existe/está listo; imágenes del tema copiadas (autocontenido)
  - visor = rompecabezas_player.html + rompecabezas_player.js (plantillas del
    repo, se sirven en cada request → una mejora del player llega a TODOS los
    links ya vendidos) + data.json por token (la personalización viva)

El MISMO principio del motor: las formas de las piezas las genera el código —
se REUSA la receta de knobs Bézier del rompecabezas imprimible
(rompecabezas._bordes_grilla: bulbo más ancho que su cuello, jitter
determinístico por seed) y se exportan como polilíneas en data.json; el player
solo las dibuja. Las imágenes salen del arte YA REVISADO del tema (fondo IA
dedicado «rompecabezas» + escenas del libro). La banda de edad decide los
niveles (cantidad de piezas), igual que en actividades_web."""
import glob
import json
import math
import os
import re
import secrets
import time
import zlib

from PIL import Image, ImageDraw

import fondos_ia

BASEDIR = os.path.dirname(os.path.abspath(__file__))
ROMPE_DIR = os.path.join(BASEDIR, "rompecabezas_web")
TEMAS = os.path.join(BASEDIR, "temas")
TEMPLATE_HTML = os.path.join(BASEDIR, "rompecabezas_player.html")
TEMPLATE_JS = os.path.join(BASEDIR, "rompecabezas_player.js")
VIGENCIA_DIAS = 7300         # igual que audiolibro/actividades: respalda "Mis compras"
_TOKEN_RE = r"[A-Za-z0-9_-]{8,32}"

MAX_PUZZLES = 6

# Niveles (cantidad de piezas): los MISMOS para toda compra (Pablo 11-jul-2026:
# el producto no pide edad — el chico elige de 4 a ~50 piezas, como el demo).
# El tope real es 48/49 según la proporción de la foto: son los conteos ≤50
# con piezas CUADRADAS (6x8 / 7x7); 50 exacto solo factoriza 5x10, piezas 2:1.
TARGETS = [4, 6, 12, 20, 30, 48]


def _paleta(tema):
    import actividades_web
    return actividades_web._paleta(tema)


# ── Imágenes del tema (arte ya revisado; NUNCA se genera IA acá) ──

def _imagenes_tema(tema):
    """Paths candidatos, en orden: el fondo IA dedicado del rompecabezas
    imprimible + escenas del libro (espaciadas parejo para variar ambientes).
    Solo arte que vive en el repo (committeado tras revisión humana)."""
    out = []
    p = fondos_ia.fondo_path(tema, "rompecabezas")
    if os.path.isfile(p):
        out.append(p)
    escenas = sorted(
        glob.glob(os.path.join(TEMAS, tema, "overrides", "libro", "*.png")),
        key=lambda q: int(re.sub(r"\D", "", os.path.basename(q)) or 0))
    escenas = [q for q in escenas
               if re.fullmatch(r"\d+\.png", os.path.basename(q))]
    faltan = MAX_PUZZLES - len(out)
    if escenas and faltan > 0:
        n = min(faltan, len(escenas))
        paso = len(escenas) / n
        out += [escenas[int(i * paso)] for i in range(n)]
    return out


def _formato(im):
    """(W, H) destino según la proporción del arte: vertical 3:4, apaisado 4:3
    o cuadrado. Nunca se estira (fondos_ia.cover recorta centrado)."""
    r = im.height / im.width
    if r >= 1.25:
        return 900, 1200
    if r <= 0.8:
        return 1200, 900
    return 1000, 1000


def _grilla(target, w, h):
    """(cols, filas) con piezas lo más cuadradas posible para la proporción
    w:h de la imagen (cols, filas >= 2). Los niveles chicos exigen el conteo
    EXACTO (factorizan bien); el tope (~50) admite conteos vecinos ±3 porque
    50 exacto solo factoriza 5x10 (piezas 2:1) — así una foto 3:4 corta 6x8=48
    y una cuadrada 7x7=49, siempre piezas cuadradas. El player muestra el
    conteo REAL (cols*filas)."""
    mejor = None
    conteos = range(target - 3, target + 4) if target >= 40 else (target,)
    for n in conteos:
        for c in range(2, n + 1):
            if n % c:
                continue
            f = n // c
            if f < 2:
                continue
            d = (abs(math.log((w / c) / (h / f))), abs(n - target))
            if mejor is None or d < mejor[0]:
                mejor = (d, c, f)
    return mejor[1], mejor[2]


def _bordes_json(cols, filas, seed):
    """Bordes interiores de la grilla como polilíneas en coords unitarias
    (cada borde va de (0,0) a (1,0); el player lo mapea a su celda). Reusa la
    receta EXACTA del imprimible (knob Bézier con traba real y jitter)."""
    from rompecabezas import _bordes_grilla
    horiz, vert = _bordes_grilla(cols, filas, seed)

    def _pl(edge):
        return [[round(x, 3), round(y, 3)] for x, y in edge[::2]]

    return {"h": [[_pl(e) for e in fila] for fila in horiz],
            "v": [[_pl(e) for e in col] for col in vert]}


# ── Estado del token (mismo contrato que actividades_web/audiolibro) ──

def _marca_gen(token):
    return os.path.join(ROMPE_DIR, token, ".generando")


def _marca_error(token):
    return os.path.join(ROMPE_DIR, token, ".error")


def marcar_generando(token):
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return
    os.makedirs(os.path.join(ROMPE_DIR, token), exist_ok=True)
    with open(_marca_gen(token), "w") as f:
        f.write("1")


def marcar_error(token, motivo=""):
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return
    os.makedirs(os.path.join(ROMPE_DIR, token), exist_ok=True)
    try:
        os.remove(_marca_gen(token))
    except OSError:
        pass
    try:
        with open(_marca_error(token), "w", encoding="utf-8") as f:
            f.write(str(motivo)[:500])
    except OSError:
        pass


def estado(token):
    """'listo' / 'generando' / 'error' / None (token inexistente)."""
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return None
    d = os.path.join(ROMPE_DIR, token)
    if os.path.isfile(os.path.join(d, "manifest.json")):
        return "listo"
    if os.path.isfile(_marca_gen(token)):
        return "generando"
    if os.path.isfile(_marca_error(token)):
        return "error"
    return None


def _cargar(token):
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return None
    p = os.path.join(ROMPE_DIR, token, "manifest.json")
    if not os.path.isfile(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


# ── Generación ──

def _mascota(tema, d):
    """Un recorte limpio del tema para el avatar del header y el festejo
    (mismo pipeline filtrado que actividades_web). Opcional: sin recortes el
    player cae a un emoji — nunca bloquea la venta."""
    try:
        import piezas
        from cuaderno import _recorte_limpio, _seleccionar_recortes
        for p in _seleccionar_recortes(tema, 6, variedad_estricta=True,
                                       incluir_objetos=True):
            try:
                im = _recorte_limpio(p)
            except Exception:
                continue
            im = im.crop(im.getbbox() or (0, 0, im.width, im.height))
            if not piezas.un_solo_blob(im):
                continue
            im.thumbnail((420, 420), Image.LANCZOS)
            im.save(os.path.join(d, "masco.png"), optimize=True)
            return "masco.png"
    except Exception:
        pass
    return None


def _hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _dibujar_cortes_pil(im, cols, filas, seed, color, ancho):
    """Los cortes del puzzle sobre una imagen PIL (para portada/preview):
    misma receta y mismo mapeo que rompecabezas._dibujar_cortes."""
    from rompecabezas import _bordes_grilla, _dibujar_cortes
    horiz, vert = _bordes_grilla(cols, filas, seed)
    _dibujar_cortes(ImageDraw.Draw(im, "RGBA"), 0, 0, im.width, im.height,
                    cols, filas, horiz, vert, color, ancho)


def _fuente(nombre, px):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(os.path.join(BASEDIR, "fonts", nombre), px)
    except Exception:
        return ImageFont.load_default()


def _luminancia(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def _render_portada(titulo, tema_nombre, pal, img):
    """Portada 900×1200 (la card de Mi biblioteca es 3:4): el arte del primer
    puzzle a sangre con los cortes encima — se lee «rompecabezas» de una — y
    una banda inferior con marca y título.

    Feedback Pablo 11-jul-2026: (1) la edad va FIJA como «+3 años» (el
    producto ya no pide edad: toda compra trae los niveles de 4 a ~50 piezas);
    (2) la banda va SIEMPRE clara — con la paleta oscura del tema espacial
    salía azul y desentonaba con el resto de la grilla de Mi biblioteca."""
    W, H = 900, 1200
    im = fondos_ia.cover(img, W, H).convert("RGB")
    _dibujar_cortes_pil(im, 3, 4, zlib.crc32(b"portada-rompe"),
                        (255, 255, 255, 175), 5)
    dr = ImageDraw.Draw(im, "RGBA")
    card, ink = _hex_rgb(pal["card"]), _hex_rgb(pal["ink"])
    if _luminancia(card) < 150:            # paleta oscura (espacio) → banda clara
        card, ink = (255, 255, 255), (58, 48, 42)
    bh = 250
    dr.rectangle((0, H - bh, W, H), fill=card + (242,))
    dr.rectangle((0, H - bh, W, H - bh + 10), fill=_hex_rgb(pal["ac"]) + (255,))
    f_tit = _fuente("Baloo2-VF.ttf", 64)
    tit = titulo
    while f_tit.getlength(tit) > W - 90 and f_tit.size > 34:
        f_tit = _fuente("Baloo2-VF.ttf", f_tit.size - 4)
    dr.text((W // 2, H - bh + 88), tit, font=f_tit, fill=ink, anchor="mm")
    f_sub = _fuente("Nunito-VF.ttf", 36)
    sub = "%s · +3 años" % tema_nombre
    dr.text((W // 2, H - bh + 158), sub, font=f_sub,
            fill=_hex_rgb(pal["ac2"]), anchor="mm")
    f_marca = _fuente("Nunito-VF.ttf", 27)
    dr.text((W // 2, H - 42), "Rompecabezas interactivo · CASATRIDIMENSIONAL",
            font=f_marca, fill=ink + (150,), anchor="mm")
    return im


def crear(data, tema, token=None):
    """Genera rompecabezas_web/<token>/ completo. Síncrono y rápido (sin
    llamadas IA: cortes procedurales + copiar arte ya existente del tema).
    Devuelve el token."""
    if not (token and re.fullmatch(_TOKEN_RE, token)):
        token = secrets.token_urlsafe(12)
    d = os.path.join(ROMPE_DIR, token)
    os.makedirs(d, exist_ok=True)
    # limpiar assets de una generación anterior (regenerar un token dejaba
    # huérfanos — mismo criterio que actividades_web.crear)
    for fn in os.listdir(d):
        if re.fullmatch(r"[pt]\d\.jpg|masco\.png", fn):
            try:
                os.remove(os.path.join(d, fn))
            except OSError:
                pass
    nombre = (data.get("nombre") or "").strip()
    targets = TARGETS

    paths = _imagenes_tema(tema)
    if not paths:
        raise RuntimeError("el tema %r no tiene arte para el rompecabezas "
                           "(ni fondo dedicado ni escenas del libro)" % tema)

    puzzles, bordes, imgs = [], {}, []
    for i, p in enumerate(paths[:MAX_PUZZLES]):
        im = Image.open(p).convert("RGB")
        w, h = _formato(im)
        im = fondos_ia.cover(im, w, h)
        im.save(os.path.join(d, "p%d.jpg" % i), quality=86)
        th = im.copy()
        th.thumbnail((330, 330), Image.LANCZOS)
        th.save(os.path.join(d, "t%d.jpg" % i), quality=80)
        imgs.append(im)
        grillas = {}
        for t in targets:
            cols, filas = _grilla(t, w, h)
            clave = "%dx%d" % (cols, filas)
            if clave not in bordes:
                seed = zlib.crc32(("%s|%s" % (token, clave)).encode())
                bordes[clave] = _bordes_json(cols, filas, seed)
            grillas[str(t)] = clave
        puzzles.append({"img": "p%d.jpg" % i, "thumb": "t%d.jpg" % i,
                        "w": w, "h": h, "grillas": grillas})

    from cuaderno import _tema_nombre
    titulo = ("Los rompecabezas de %s" % nombre) if nombre \
        else "Rompecabezas %s" % _tema_nombre(tema)
    pal = _paleta(tema)
    dj = {
        "v": 1, "tema": tema, "tema_nombre": _tema_nombre(tema),
        "nombre": nombre, "titulo": titulo,
        "paleta": pal, "targets": targets,
        "masco": _mascota(tema, d),
        "puzzles": puzzles, "bordes": bordes,
    }
    with open(os.path.join(d, "data.json"), "w", encoding="utf-8") as f:
        json.dump(dj, f, ensure_ascii=False)

    _render_portada(titulo, dj["tema_nombre"], pal,
                    imgs[0]).save(os.path.join(d, "portada.jpg"), quality=88)

    with open(os.path.join(d, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"tema": tema, "nombre": nombre, "titulo": titulo,
                   "creado": int(time.time())}, f, ensure_ascii=False)
    try:
        os.remove(_marca_gen(token))
    except OSError:
        pass
    _limpiar_vencidos()
    return token


def _limpiar_vencidos():
    import shutil
    limite = time.time() - VIGENCIA_DIAS * 86400
    try:
        for fn in os.listdir(ROMPE_DIR):
            p = os.path.join(ROMPE_DIR, fn)
            if os.path.isdir(p) and os.path.getmtime(p) < limite:
                shutil.rmtree(p, ignore_errors=True)
    except OSError:
        pass


# ── Servido (visor + assets) ──

def _player_version():
    """Cache-buster: cambia solo cuando se toca el player en el repo."""
    try:
        return str(int(max(os.path.getmtime(TEMPLATE_JS),
                           os.path.getmtime(TEMPLATE_HTML))))
    except OSError:
        return "1"


def html(token):
    """El visor (HTML). Rutas RELATIVAS → servirlo SIEMPRE bajo /armar/<token>/
    (con barra final). None si el token no está listo.

    {{DV}} = mtime del data.json del token: los assets van con Cache-Control
    de 24h y sin esto, al REGENERAR un token el navegador seguía mostrando las
    piezas viejas (le pasó a Pablo probando el fix de knobs 11-jul-2026 —
    mismo cache-buster por asset que usa mandalas_web)."""
    from html import escape as _esc
    reg = _cargar(token)
    if not reg:
        return None
    with open(TEMPLATE_HTML, encoding="utf-8") as f:
        t = f.read()
    try:
        dv = str(int(os.path.getmtime(os.path.join(ROMPE_DIR, token, "data.json"))))
    except OSError:
        dv = "1"
    return (t.replace("{{TITULO}}", _esc(reg.get("titulo") or "Rompecabezas"))
             .replace("{{V}}", _player_version())
             .replace("{{DV}}", dv))


_ASSET_RE = re.compile(
    r"^(data\.json|player\.js|f[12]\.ttf|[pt]\d\.jpg|masco\.png|portada\.jpg)$")
_CT = {".json": "application/json; charset=utf-8",
       ".js": "text/javascript; charset=utf-8",
       ".ttf": "font/ttf", ".png": "image/png", ".jpg": "image/jpeg"}


def archivo(token, nombre):
    """(bytes, content_type) de un asset del token, o None. El player y las
    fuentes salen del REPO (mejoras llegan a links ya vendidos); el resto, de
    la carpeta del token."""
    if not _cargar(token) or not _ASSET_RE.fullmatch(nombre or ""):
        return None
    if nombre == "player.js":
        p = TEMPLATE_JS
    elif nombre == "f1.ttf":
        p = os.path.join(BASEDIR, "fonts", "Baloo2-VF.ttf")
    elif nombre == "f2.ttf":
        p = os.path.join(BASEDIR, "fonts", "Nunito-VF.ttf")
    else:
        p = os.path.join(ROMPE_DIR, token, nombre)
    if not os.path.isfile(p):
        return None
    ct = _CT[os.path.splitext(nombre)[1]]
    with open(p, "rb") as f:
        return f.read(), ct


def n_puzzles(tema):
    return min(MAX_PUZZLES, len(_imagenes_tema(tema)))


def preview_puzzle(tema, idx):
    """Una escena del set con los cortes encima, en tarjeta UNIFORME 3:4
    (contain sobre el crema del tema: no se recorta nada y la galería de la
    ficha queda pareja — Pablo 11-jul-2026: la mezcla de proporciones se veía
    desprolija)."""
    paths = _imagenes_tema(tema)
    img = Image.open(paths[idx]).convert("RGB")
    W, H = 900, 1200
    im = Image.new("RGB", (W, H), _hex_rgb(_paleta(tema)["soft"]))
    esc = min((W - 60) / img.width, (H - 60) / img.height)
    iw, ih = int(img.width * esc), int(img.height * esc)
    img = img.resize((iw, ih), Image.LANCZOS)
    x0, y0 = (W - iw) // 2, (H - ih) // 2
    im.paste(img, (x0, y0))
    from rompecabezas import _bordes_grilla, _dibujar_cortes
    cols, filas = _grilla(12, iw, ih)
    horiz, vert = _bordes_grilla(cols, filas, zlib.crc32(b"portada-rompe"))
    _dibujar_cortes(ImageDraw.Draw(im, "RGBA"), x0, y0, iw, ih, cols, filas,
                    horiz, vert, (255, 255, 255, 175), 5)
    return im


def preview_mock(data, tema):
    """Miniatura para la ficha de la tienda / dash (sin crear token): la portada.
    Sin nombre (el producto no pide datos — Pablo 11-jul-2026)."""
    paths = _imagenes_tema(tema)
    if paths:
        img = Image.open(paths[0]).convert("RGB")
    else:
        img = Image.new("RGB", (900, 1200), _hex_rgb(_paleta(tema)["soft"]))
    from cuaderno import _tema_nombre
    return _render_portada("Rompecabezas %s" % _tema_nombre(tema),
                           _tema_nombre(tema), _paleta(tema), img)
