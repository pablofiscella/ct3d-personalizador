#!/usr/bin/env python3
"""actividades_web.py — Cuaderno de actividades INTERACTIVO (producto digital vivo).

El producto ES un link (/act/<token>): una web app táctil donde el chico juega
las mismas actividades del cuaderno imprimible (colorear, memotest, sopa de
letras, laberinto, contar, sumas…) con corrección automática, estrellas y
festejo. Espejo de audiolibro.py:

  - carpeta por token en actividades/<token>/ (gitignored, runtime)
  - manifest.json = existe/está listo; assets del tema copiados (autocontenido)
  - visor = actividades_player.html + actividades_player.js (plantillas del
    repo, se sirven en cada request → una mejora del player llega a TODOS los
    links ya vendidos) + data.json por token (la personalización viva)

El MISMO principio del motor: el código genera y VERIFICA (laberinto con
salida por BFS, sopa con todas las palabras colocadas, sudoku de solución
única — reusa los generadores determinísticos de cuaderno.py); el arte del
tema (stickers recortados, páginas para colorear IA, fondo de escena) se copia
al token. La banda de edad decide el menú de juegos, igual que _construir."""
import os, re, json, glob, math, time, zlib, random, secrets
from html import escape as _esc

from PIL import Image, ImageDraw, ImageFont, ImageFilter

import piezas

BASEDIR = os.path.dirname(os.path.abspath(__file__))
ACT_DIR = os.path.join(BASEDIR, "actividades")
TEMPLATE_HTML = os.path.join(BASEDIR, "actividades_player.html")
TEMPLATE_JS = os.path.join(BASEDIR, "actividades_player.js")
VIGENCIA_DIAS = 7300         # igual que el audiolibro: respalda "Mis compras"
_TOKEN_RE = r"[A-Za-z0-9_-]{8,32}"

# ── Paletas por tema (elegidas a mano: cálidas, contraste AA en textos, un
#    acento fuerte + uno secundario; "espacio" es la única oscura a propósito) ──
PALETAS = {
    "safari":       {"bg": "#FBF3E4", "card": "#FFFFFF", "ink": "#4A3728", "ac": "#E07B2E", "ac2": "#57A05A", "soft": "#F5E3C4", "star": "#F2A93B"},
    "futbol":       {"bg": "#EFF6EF", "card": "#FFFFFF", "ink": "#1F3A2E", "ac": "#2E9E4F", "ac2": "#2563B6", "soft": "#DCEEDD", "star": "#F2A93B"},
    "princesas":    {"bg": "#FCF1F6", "card": "#FFFFFF", "ink": "#4C2A3D", "ac": "#D9569A", "ac2": "#8E5FC8", "soft": "#F8DCE9", "star": "#E8A426"},
    "monstruos":    {"bg": "#F3F0FA", "card": "#FFFFFF", "ink": "#31284A", "ac": "#7C5CD6", "ac2": "#2FA96A", "soft": "#E4DCF6", "star": "#F2A93B"},
    "superheroes":  {"bg": "#EFF4FC", "card": "#FFFFFF", "ink": "#1E2A4A", "ac": "#D63B34", "ac2": "#2563B6", "soft": "#DBE6F8", "star": "#F2A93B"},
    "superhéroes":  {"bg": "#EFF4FC", "card": "#FFFFFF", "ink": "#1E2A4A", "ac": "#D63B34", "ac2": "#2563B6", "soft": "#DBE6F8", "star": "#F2A93B"},
    "construccion": {"bg": "#FBF5E3", "card": "#FFFFFF", "ink": "#3E3222", "ac": "#DE9204", "ac2": "#4A6FA5", "soft": "#F6E9C1", "star": "#E07B2E"},
    "circo":        {"bg": "#FBF1E8", "card": "#FFFFFF", "ink": "#47262A", "ac": "#CE4747", "ac2": "#25938A", "soft": "#F7DECE", "star": "#F2A93B"},
    "bomberos":     {"bg": "#FBF0EB", "card": "#FFFFFF", "ink": "#3C2320", "ac": "#CE3E28", "ac2": "#DE9204", "soft": "#F7DACF", "star": "#F2A93B"},
    "campamento":   {"bg": "#F2F6EC", "card": "#FFFFFF", "ink": "#2F3B26", "ac": "#5F8B3B", "ac2": "#A06C3C", "soft": "#E1ECD4", "star": "#F2A93B"},
    "artistas":     {"bg": "#FBF4ED", "card": "#FFFFFF", "ink": "#3A2E3C", "ac": "#DB6844", "ac2": "#2E96A8", "soft": "#F6E1D2", "star": "#E8A426"},
    "aviadores":    {"bg": "#EDF5FB", "card": "#FFFFFF", "ink": "#243447", "ac": "#3577B4", "ac2": "#D96A5F", "soft": "#D8E8F6", "star": "#F2A93B"},
    "un-espacio-de-locura":
                    {"bg": "#171C42", "card": "#232A63", "ink": "#F2F4FF", "ac": "#8E7DFF", "ac2": "#43D6C5", "soft": "#2B3170", "star": "#FFD166"},
}
_PALETA_DEFAULT = {"bg": "#FBF4EA", "card": "#FFFFFF", "ink": "#44372E", "ac": "#E0713C", "ac2": "#4E9C7E", "soft": "#F5E4CE", "star": "#F2A93B"}


def _paleta(tema):
    return dict(PALETAS.get(tema, _PALETA_DEFAULT))


def _banda(edad):
    """Banda de edad → menú y dificultad (mismo criterio que cuaderno._construir)."""
    try:
        e = int(str(edad).strip() or 5)
    except (TypeError, ValueError):
        e = 5
    return "mini" if e <= 3 else ("media" if e <= 5 else "grande")


# ── Menú por banda (orden = recorrido sugerido; cfg = perillas de dificultad).
#    Curado con la investigación 10-jul-2026: contar-tocando, patrón y memotest
#    son los de mayor valor educativo; sopa/sudoku recién para lectores. ──
def _menu(banda, edad):
    try:
        e = int(str(edad).strip() or 5)
    except (TypeError, ValueError):
        e = 5
    if banda == "mini":
        return [
            {"id": "contar",    "titulo": "¿Cuántos hay?",    "icono": "🖐️", "cfg": {"max": 3, "rondas": 5}},
            {"id": "colorear",  "titulo": "¡A pintar!",       "icono": "🎨", "cfg": {}},
            {"id": "memotest",  "titulo": "Memotest",         "icono": "🧠", "cfg": {"pares": 3}},
            {"id": "sombra",    "titulo": "Sombras",          "icono": "👤", "cfg": {"pares": 3, "rondas": 2}},
            {"id": "diferente", "titulo": "El distinto",      "icono": "🔍", "cfg": {"opciones": 3, "rondas": 5}},
            {"id": "tamano",    "titulo": "El más grande",    "icono": "📏", "cfg": {"rondas": 5}},
            {"id": "patron",    "titulo": "Seguí el patrón",  "icono": "🔁", "cfg": {"nivel": 1, "rondas": 5}},
        ]
    if banda == "media":
        m = [
            {"id": "contar",    "titulo": "¿Cuántos hay?",    "icono": "🖐️", "cfg": {"max": 6, "rondas": 5}},
            {"id": "colorear",  "titulo": "¡A pintar!",       "icono": "🎨", "cfg": {}},
            {"id": "memotest",  "titulo": "Memotest",         "icono": "🧠", "cfg": {"pares": 6}},
            {"id": "laberinto", "titulo": "El laberinto",     "icono": "🌀", "cfg": {"desde": 0}},
            {"id": "sombra",    "titulo": "Sombras",          "icono": "👤", "cfg": {"pares": 4, "rondas": 2}},
            {"id": "puntos",    "titulo": "Uní los puntos",   "icono": "✨", "cfg": {"figuras": ["estrella"]}},
            {"id": "patron",    "titulo": "Seguí el patrón",  "icono": "🔁", "cfg": {"nivel": 2, "rondas": 5}},
            {"id": "mas_menos", "titulo": "¿Dónde hay más?",  "icono": "⚖️", "cfg": {"max": 6, "rondas": 5}},
            {"id": "diferente", "titulo": "El distinto",      "icono": "🔍", "cfg": {"opciones": 4, "rondas": 5}},
            {"id": "tamano",    "titulo": "El más grande",    "icono": "📏", "cfg": {"rondas": 5}},
        ]
        if e >= 5:
            m.append({"id": "sumas", "titulo": "Sumas", "icono": "➕", "cfg": {"max": 5, "rondas": 5}})
        return m
    return [
        {"id": "memotest",  "titulo": "Memotest",         "icono": "🧠", "cfg": {"pares": 8}},
        {"id": "laberinto", "titulo": "El laberinto",     "icono": "🌀", "cfg": {"desde": 0}},
        {"id": "sopa",      "titulo": "Sopa de letras",   "icono": "🔤", "cfg": {}},
        {"id": "sudoku",    "titulo": "Sudoku",           "icono": "🧩", "cfg": {}},
        {"id": "sumas",     "titulo": "Sumas",            "icono": "➕", "cfg": {"max": 10, "rondas": 6}},
        {"id": "restas",    "titulo": "Restas",           "icono": "➖", "cfg": {"max": 10, "rondas": 6}},
        {"id": "serie",     "titulo": "La serie",         "icono": "🔢", "cfg": {"rondas": 6}},
        {"id": "patron",    "titulo": "Seguí el patrón",  "icono": "🔁", "cfg": {"nivel": 3, "rondas": 6}},
        {"id": "puntos",    "titulo": "Uní los puntos",   "icono": "✨", "cfg": {"figuras": ["estrella", "corazon"]}},
        {"id": "contar",    "titulo": "¿Cuántos hay?",    "icono": "🖐️", "cfg": {"max": 9, "rondas": 5}},
        {"id": "colorear",  "titulo": "¡A pintar!",       "icono": "🎨", "cfg": {}},
        {"id": "mas_menos", "titulo": "¿Dónde hay más?",  "icono": "⚖️", "cfg": {"max": 9, "rondas": 5}},
    ]


# ── Puzzles verificados (reusan los generadores determinísticos de cuaderno.py) ──

def _lab_json(n, seed):
    """Laberinto n×n como bitmask de paredes por celda (N=1 S=2 E=4 W=8),
    filas row-major + camino solución (BFS — garantiza salida)."""
    from cuaderno import _maze, _maze_path
    w = _maze(n, n, seed)
    camino = _maze_path(w, n, n)
    bit = {"N": 1, "S": 2, "E": 4, "W": 8}
    celdas = [[sum(bit[k] for k in w[x][y]) for x in range(n)] for y in range(n)]
    celdas[0][0] &= ~bit["W"]          # entrada abierta (igual que _draw_maze)
    celdas[n - 1][n - 1] &= ~bit["E"]  # salida abierta
    return {"n": n, "celdas": celdas, "camino": [list(c) for c in camino]}


def _sopa_json(palabras, N, seed):
    """Sopa N×N: todas las palabras colocadas y verificadas (o None si no entran).
    En la grilla van sin tilde (la Ñ se conserva); 'lindas' = como se muestran."""
    from cuaderno import _wordsearch, _sin_tilde
    ws, lindas = [], []
    for p in palabras:
        p = str(p).strip().upper()
        if 3 <= len(p) <= N and p not in lindas:
            lindas.append(p)
            ws.append(_sin_tilde(p))
    g = sol = None
    for s in range(seed, seed + 60):
        g, sol = _wordsearch(ws, N, s)
        if g:
            break
    if not g:
        return None
    filas = ["".join(g[x][y] for x in range(N)) for y in range(N)]
    return {"n": N, "filas": filas, "palabras": ws, "lindas": lindas,
            "sol": {w: [[x, y] for x, y in cs] for w, cs in sol.items()}}


def _sudoku_json(seed):
    """Sudoku 4×4 de solución ÚNICA (verificado por conteo en cuaderno.py)."""
    from cuaderno import _sudoku_make
    sol, puz = _sudoku_make(random.Random(seed))
    return {"sol": sol, "puz": puz}


def _figura_pts(figura, nd):
    """Contorno ordenado (unir los puntos) en coords normalizadas 0..1."""
    pts = []
    if figura == "estrella":
        nd = nd if nd % 2 == 0 else nd + 1
        for i in range(nd):
            a = -math.pi / 2 + i * 2 * math.pi / nd
            r = 0.46 if i % 2 == 0 else 0.20
            pts.append((0.5 + r * math.cos(a), 0.52 + r * math.sin(a)))
    else:  # corazón (paramétrico clásico, arranca arriba al medio)
        for i in range(nd):
            t = math.pi / 2 + i * 2 * math.pi / nd
            x = 16 * math.sin(t) ** 3
            y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pts.append((0.5 + x * 0.028, 0.47 - y * 0.028))
    return [[round(x, 4), round(y, 4)] for x, y in pts]


# ── Estado del token (mismo contrato que audiolibro.py) ──

def _marca_gen(token):
    return os.path.join(ACT_DIR, token, ".generando")


def _marca_error(token):
    return os.path.join(ACT_DIR, token, ".error")


def marcar_generando(token):
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return
    os.makedirs(os.path.join(ACT_DIR, token), exist_ok=True)
    with open(_marca_gen(token), "w") as f:
        f.write("1")


def marcar_error(token, motivo=""):
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return
    os.makedirs(os.path.join(ACT_DIR, token), exist_ok=True)
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
    d = os.path.join(ACT_DIR, token)
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
    p = os.path.join(ACT_DIR, token, "manifest.json")
    if not os.path.isfile(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


# ── Generación ──

def _miniatura_cmp(im):
    """Miniatura RGB 24×24 del contenido (para comparar recortes entre sí)."""
    from PIL import ImageOps
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    m = bg.convert("RGB").resize((24, 24), Image.LANCZOS)
    return m, ImageOps.mirror(m)


def _dif_pixel(m1, m2par):
    """Diferencia media RGB entre miniaturas (considera el espejo)."""
    m2, m2esp = m2par
    def dif(a, b):
        pa, pb = list(a.getdata()), list(b.getdata())
        return sum(abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])
                   for x, y in zip(pa, pb)) / (len(pa) * 3)
    return min(dif(m1, m2), dif(m1, m2esp))


def _matiz_sat(im):
    """(matiz circular medio en grados, saturación media) de los píxeles
    opacos y no-blancos. Para distinguir 'flor amarilla vs flor roja' (misma
    etiqueta, matiz lejos) de 'león vs león' (matiz igual)."""
    import colorsys
    m = im.copy()
    m.thumbnail((64, 64))
    hx = hy = n = 0.0
    sats = []
    for r, g, b, a in m.getdata():
        if a < 60 or (r > 225 and g > 225 and b > 225):
            continue
        h, sat, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        if sat > 0.12 and v > 0.15:
            hx += math.cos(h * 2 * math.pi)
            hy += math.sin(h * 2 * math.pi)
            sats.append(sat)
            n += 1
    if not n:
        return None, 0.0
    return math.degrees(math.atan2(hy, hx)) % 360, sum(sats) / len(sats)


def _dist_matiz(a, b):
    if a is None or b is None:
        return 0.0           # sin color confiable → no separa (decide el resto)
    d = abs(a - b) % 360
    return min(d, 360 - d)


def _etiquetas_tema(tema):
    """Etiquetas del clasificador de visión (clasif.json, cacheado por el
    cuaderno): {'c001.png': 'león', …}. Vacío si el tema no tiene."""
    try:
        t = json.load(open(os.path.join(BASEDIR, "temas", tema,
                                        "actividades_mon", "clasif.json"),
                           encoding="utf-8")).get("tipos") or {}
        return {str(k).lower(): str(v).strip().lower() for k, v in t.items()}
    except Exception:
        return {}


def _silueta_cmp(im, S=28):
    """Silueta binaria S×S (+espejo) para comparar formas."""
    from PIL import ImageOps
    a = im.getchannel("A").point(lambda v: 255 if v > 40 else 0).resize((S, S))
    return a, ImageOps.mirror(a)


def _iou_silueta(a, bpar):
    """IoU de siluetas (máx con el espejo): 'león vs león' da ~0.81; figuras
    de forma distinta (hoja vs flor) quedan por debajo de ~0.75."""
    def iou(x, y):
        px, py = list(x.getdata()), list(y.getdata())
        inter = sum(1 for u, v in zip(px, py) if u and v)
        union = sum(1 for u, v in zip(px, py) if u or v)
        return inter / max(1, union)
    return max(iou(a, bpar[0]), iou(a, bpar[1]))


def _es_duplicado(cand, elegidos):
    """¿`cand` se confunde con alguno ya elegido? Calibrado 10-jul-2026 con los
    dups REALES del memotest (2 leones diff-píxel 38, 2 monsteras 31 — la
    métrica de píxeles sola NO alcanza; feedback Pablo). El clasif.json
    etiqueta solo una parte de los recortes, así que hay tres casos:
    - ambos ETIQUETADOS: misma etiqueta y matiz cerca (<40°) → dup (león vs
      león); matiz lejos → se quedan (flor amarilla vs flor roja)
    - alguno SIN etiqueta: matiz cerca (<25°) + píxel <40 + MISMA FORMA
      (IoU silueta >0.75) → dup (atrapa al león sin etiquetar y a las dos
      monsteras; deja pasar hoja-vs-flor, que difieren en forma)
    - píxel <24 → dup siempre (casi-idénticos)"""
    for e in elegidos:
        dp = _dif_pixel(cand["mini"][0], e["mini"])
        if dp < 24:
            return True
        dm = _dist_matiz(cand["matiz"], e["matiz"])
        if cand["etiqueta"] and e["etiqueta"]:
            if cand["etiqueta"] == e["etiqueta"] and dm < 40:
                return True
        elif dm < 25 and dp < 40 \
                and _iou_silueta(cand["sil"][0], e["sil"]) > 0.75:
            return True
    return False


def _personajes(tema, d):
    """Copia al token los mejores recortes del tema, LIMPIOS (sin el aro
    blanco del die-cut — acá no son stickers; feedback Pablo 10-jul-2026, vía
    cuaderno._recorte_limpio/piezas.quitar_halo): variedad estricta (sin
    casi-duplicados — la regla que salvó al memotest del papel), sin tiras
    compuestas, dedup extra por contenido (dos hojas casi iguales confunden).
    Devuelve filenames (hasta 8); como van sin aro, la silueta de sombras se
    hace en el player con el mismo archivo (brightness 0)."""
    from cuaderno import _seleccionar_recortes, _recorte_limpio
    paths = _seleccionar_recortes(tema, 16, variedad_estricta=True, incluir_objetos=True)
    if len(paths) < 4:
        paths = _seleccionar_recortes(tema, 16, incluir_objetos=True)
    etiquetas = _etiquetas_tema(tema)
    buenos, elegidos = [], []
    for p in paths:
        try:
            im = _recorte_limpio(p)
        except Exception:
            continue
        im = im.crop(im.getbbox() or (0, 0, im.width, im.height))
        if not piezas.un_solo_blob(im):
            continue
        matiz, _sat = _matiz_sat(im)
        cand = {"mini": _miniatura_cmp(im), "matiz": matiz,
                "sil": _silueta_cmp(im),
                "etiqueta": etiquetas.get(os.path.basename(p).lower(), "")}
        if _es_duplicado(cand, elegidos):
            continue
        elegidos.append(cand)
        buenos.append(im)
        if len(buenos) >= 8:
            break
    if len(buenos) < 2:
        raise RuntimeError("el tema %r no tiene stickers para las actividades" % tema)
    out = []
    for i, im in enumerate(buenos):
        im.thumbnail((420, 420), Image.LANCZOS)
        fn = "p%02d.png" % i
        im.save(os.path.join(d, fn), optimize=True)
        out.append(fn)
    return out, list(out)      # sombras = los mismos archivos (ya sin aro)


def _colorear(tema, d):
    from cuaderno import _colorear_imgs
    out = []
    for i, im in enumerate(_colorear_imgs(tema)[:3]):
        im = im.convert("L")
        im.thumbnail((1100, 1100), Image.LANCZOS)
        fn = "colorear_%d.png" % i
        im.save(os.path.join(d, fn), optimize=True)
        out.append(fn)
    return out


def _escena(tema, d):
    try:
        import fondos_ia
        f = fondos_ia.cargar_fondo(tema, "escena")
    except Exception:
        f = None
    if f is None:
        return None
    f = f.convert("RGB")
    f.thumbnail((1600, 1600), Image.LANCZOS)
    f.save(os.path.join(d, "escena.jpg"), quality=82)
    return "escena.jpg"


def _armar_data(tema, nombre, edad, seed):
    """El data.json del token: paleta + menú + puzzles verificados."""
    from cuaderno import _tema_nombre, _tema_palabras, PALABRAS
    banda = _banda(edad)
    rnd = random.Random(seed)
    palabras = _tema_palabras(tema) or list(PALABRAS)

    sopas, sudokus, laberintos = [], [], []
    if banda == "grande":
        for i in range(4):
            sub = rnd.sample(palabras, min(6, len(palabras)))
            s = _sopa_json(sub, 10, seed + i * 101)
            if s:
                sopas.append(s)
        sudokus = [_sudoku_json(seed + i * 13) for i in range(4)]
    if banda != "mini":
        tams = [6, 7, 8, 9] if banda == "media" else [9, 10, 11, 12]
        laberintos = [_lab_json(n, seed + i * 17) for i, n in enumerate(tams)]

    titulo = ("Las actividades de %s" % nombre) if nombre else "Cuaderno de actividades"
    return {
        "v": 1, "tema": tema, "tema_nombre": _tema_nombre(tema),
        "nombre": nombre, "edad": edad, "banda": banda, "titulo": titulo,
        "paleta": _paleta(tema),
        "menu": _menu(banda, edad),
        "sopas": sopas, "sudokus": sudokus, "laberintos": laberintos,
        "figuras": {"estrella": _figura_pts("estrella", 10),
                    "corazon": _figura_pts("corazon", 14)},
    }


def _fuente(nombre, px):
    try:
        return ImageFont.truetype(os.path.join(BASEDIR, "fonts", nombre), px)
    except Exception:
        return ImageFont.load_default()


def _hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _render_portada(dj, pers_imgs):
    """Portada VERTICAL 1000×1414 (ratio A4 ≈ 826/1169, el de la tarjeta de Mi biblioteca:
    antes era apaisada 1200×900 y `object-fit:cover` le comía los costados). Cover de
    biblioteca + og:image + preview de la tienda."""
    pal = dj["paleta"]
    W, H = 1000, 1414
    im = Image.new("RGB", (W, H), _hex_rgb(pal["bg"]))
    dr = ImageDraw.Draw(im)
    # tarjeta + franja superior con el acento
    dr.rounded_rectangle((40, 40, W - 40, H - 40), radius=48, fill=_hex_rgb(pal["card"]))
    dr.rounded_rectangle((40, 40, W - 40, 300), radius=48, fill=_hex_rgb(pal["ac"]))
    dr.rectangle((40, 230, W - 40, 300), fill=_hex_rgb(pal["ac"]))
    f_marca = _fuente("Nunito-VF.ttf", 34)
    f_tit = _fuente("Baloo2-VF.ttf", 88)
    f_sub = _fuente("Nunito-VF.ttf", 44)
    dr.text((W // 2, 130), "CASATRIDIMENSIONAL", font=f_marca, fill="#FFFFFF", anchor="mm")
    dr.text((W // 2, 220), "Cuaderno interactivo", font=f_sub, fill="#FFFFFF", anchor="mm")
    # título (auto-ajuste al ancho)
    tit = dj["titulo"]
    f = f_tit
    while f.getlength(tit) > W - 200 and f.size > 40:
        f = _fuente("Baloo2-VF.ttf", f.size - 4)
    dr.text((W // 2, 470), tit, font=f, fill=_hex_rgb(pal["ink"]), anchor="mm")
    dr.text((W // 2, 575), "%s · %s años" % (dj["tema_nombre"], dj["edad"] or "?"),
            font=f_sub, fill=_hex_rgb(pal["ac2"]), anchor="mm")
    # personajes (hasta 3, apoyados abajo) — más aire vertical que en la apaisada
    if pers_imgs:
        n = min(3, len(pers_imgs))
        slot = (W - 160) // n
        for i in range(n):
            p = pers_imgs[i].copy()
            p.thumbnail((slot - 30, 560), Image.LANCZOS)
            x = 80 + slot * i + (slot - p.width) // 2
            im.paste(p, (x, H - 110 - p.height), p)
    # estrellitas decorativas
    star = _hex_rgb(pal["star"])
    for cx, cy, r in ((150, 430, 16), (850, 400, 20), (880, 720, 13), (150, 760, 11)):
        dr.regular_polygon((cx, cy, r), 5, rotation=90, fill=star)
    return im


def crear(data, tema, token=None):
    """Genera actividades/<token>/ completo. Síncrono y rápido (sin llamadas IA:
    todo procedural + copiar arte ya existente del tema). Devuelve el token."""
    if not (token and re.fullmatch(_TOKEN_RE, token)):
        token = secrets.token_urlsafe(12)
    d = os.path.join(ACT_DIR, token)
    os.makedirs(d, exist_ok=True)
    # limpiar assets de una generación anterior (regenerar un token dejaba
    # huérfanos: p07.png viejo junto a los p00-p06 nuevos)
    for fn in os.listdir(d):
        if re.fullmatch(r"(?:[ps]\d{2}|colorear_\d)\.png", fn):
            try:
                os.remove(os.path.join(d, fn))
            except OSError:
                pass
    nombre = (data.get("nombre") or "").strip()
    edad = (str(data.get("edad") or "")).strip()
    seed = zlib.crc32(token.encode())

    pers, sombras = _personajes(tema, d)
    cols = _colorear(tema, d)
    esc = _escena(tema, d)
    dj = _armar_data(tema, nombre, edad, seed)
    dj["personajes"] = pers
    dj["sombras"] = sombras
    dj["colorear"] = cols
    dj["escena"] = esc
    with open(os.path.join(d, "data.json"), "w", encoding="utf-8") as f:
        json.dump(dj, f, ensure_ascii=False)

    pers_imgs = [Image.open(os.path.join(d, p)).convert("RGBA") for p in pers[:3]]
    _render_portada(dj, pers_imgs).save(os.path.join(d, "portada.jpg"), quality=88)

    with open(os.path.join(d, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"tema": tema, "nombre": nombre, "edad": edad,
                   "banda": dj["banda"], "titulo": dj["titulo"],
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
        for fn in os.listdir(ACT_DIR):
            p = os.path.join(ACT_DIR, fn)
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
    """El visor (HTML). Rutas RELATIVAS → servirlo SIEMPRE bajo /act/<token>/
    (con barra final). None si el token no está listo."""
    reg = _cargar(token)
    if not reg:
        return None
    with open(TEMPLATE_HTML, encoding="utf-8") as f:
        t = f.read()
    return (t.replace("{{TITULO}}", _esc(reg.get("titulo") or "Actividades"))
             .replace("{{V}}", _player_version()))


_ASSET_RE = re.compile(
    r"^(data\.json|player\.js|f[12]\.ttf|[ps]\d{2}\.png|colorear_\d\.png|escena\.jpg|portada\.jpg)$")
_CT = {".json": "application/json; charset=utf-8", ".js": "text/javascript; charset=utf-8",
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
        p = os.path.join(ACT_DIR, token, nombre)
    if not os.path.isfile(p):
        return None
    ct = _CT[os.path.splitext(nombre)[1]]
    with open(p, "rb") as f:
        return f.read(), ct


def preview_mock(data, tema):
    """Miniatura para la ficha de la tienda / dash (sin crear token): la portada."""
    nombre = (data.get("nombre") or "").strip() or "Sofía"
    edad = (str(data.get("edad") or "")).strip() or "5"
    dj = _armar_data_liviano(tema, nombre, edad)
    pers = []
    try:
        from cuaderno import _seleccionar_recortes
        for p in _seleccionar_recortes(tema, 3, variedad_estricta=True,
                                       incluir_objetos=True)[:3]:
            pers.append(Image.open(p).convert("RGBA"))
    except Exception:
        pass
    return _render_portada(dj, pers)


def _armar_data_liviano(tema, nombre, edad):
    """Solo lo que necesita la portada (sin generar puzzles)."""
    from cuaderno import _tema_nombre
    return {"titulo": "Las actividades de %s" % nombre, "paleta": _paleta(tema),
            "tema_nombre": _tema_nombre(tema), "edad": edad}
