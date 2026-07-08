"""Cuaderno de actividades por TEMA + EDAD, generado y VERIFICADO por código.

Filosofía (lo que lo hace confiable): todo lo que tiene "respuesta correcta" lo
genera un algoritmo determinístico y se verifica antes de entregar (laberinto con
salida garantizada por BFS; sopa de letras con todas las palabras realmente
colocadas y rebuscadas). La IA / el arte solo aportan lo creativo: los monstruos
del tema (extraídos de los stickers) y el line-art para colorear.

Actividades: portada · laberinto · sopa de letras · unir los puntos · contar ·
colorear, + página de SOLUCIONARIO. El set y la dificultad dependen de la edad.

API: generar_cuaderno(tema, edad, out_dir) -> path del PDF.
"""
import os, math, random, glob, json
from collections import deque
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
NAVY = (29, 25, 79); VIOLET = (107, 91, 210); INK = (40, 38, 55); CREAM = (246, 242, 236)
COLS = [(224, 85, 107), (63, 167, 214), (232, 155, 44), (95, 184, 122), (139, 91, 210), (38, 140, 90)]
PALABRAS = ["CUMPLE", "FIESTA", "GLOBO", "TORTA", "REGALO", "JUGAR", "DULCE", "AMIGOS"]
# La lista visible se muestra con Ñ y tildes; en la GRILLA la Ñ se conserva
# (sopa en castellano) y las tildes se quitan (convención de las sopas de letras).
PALABRAS2 = ["SORPRESA", "CORONA", "CANCIÓN", "BAILAR", "FELIZ", "JUEGOS", "PIÑATA", "RISA"]


def _sin_tilde(w):
    return w.translate(str.maketrans("ÁÉÍÓÚÜ", "AEIOUU"))


def _edad_label(edad):
    e = str(edad).strip()
    return "1 añito" if e == "1" else "%s años" % e
BRAND = "CASATRIDIMENSIONAL"

def _tema_nombre(tema):
    """Nombre corto del tema para el encabezado (lo que va donde antes decía 'Monstruos').
    Lee tema.json::nombre y corta lo de antes del guión ('Circo — Gran Función' -> 'Circo').
    Fallback: el id del tema capitalizado."""
    try:
        n = json.load(open(os.path.join(TEMAS, tema, "tema.json"), encoding="utf-8")).get("nombre", "")
    except Exception:
        n = ""
    n = (n.split("—")[0].split("-")[0].strip()) if n else ""
    return n or tema.replace("_", " ").capitalize()

def _font(sz, bold=True):
    for p in glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True):
        try:
            f = ImageFont.truetype(p, sz)
            try: f.set_variation_by_axes([700 if bold else 500])
            except Exception: pass
            return f
        except Exception: pass
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)

# ───────────────────────── arte: monstruos del tema ─────────────────────────
def _extraer_monstruos(tema):
    """Recorta cada personaje del tema desde la hoja de stickers, por COMPONENTE DE ALPHA: los
    stickers nuevos vienen separados por un gap transparente, así que cada componente conexo del
    canal alpha = un personaje (con su bordecito). Mucho más simple/robusto que separar por color.
    Lee ia_draft/ (nuevo) o extras/. Cachea en temas/<tema>/actividades_mon/c*.png — se
    AUTOINVALIDA si la hoja de stickers es más nueva que el cache (si no, regenerar los
    stickers con IA no cambiaba nada acá: corona/rompecabezas/cápsula/etc. seguían
    mostrando los personajes viejos para siempre)."""
    cache = os.path.join(TEMAS, tema, "actividades_mon")
    # extras/ (APROBADO por Pablo) antes que ia_draft/ (borrador sin revisar) —
    # el orden inverso hacía que las piezas usaran arte no aprobado aunque
    # existiera la versión aprobada.
    sheet = next((p for p in (os.path.join(TEMAS, tema, "extras", "stickers_1.png"),
                              os.path.join(TEMAS, tema, "ia_draft", "stickers_1.png"))
                  if os.path.isfile(p)), None)
    if os.path.isdir(cache):
        ya = sorted(glob.glob(f"{cache}/c*.png"))
        if ya and (not sheet or os.path.getmtime(sheet) <= os.path.getmtime(cache)):
            return ya
        if ya:   # sheet más nueva que el cache: descartarlo y re-extraer
            import shutil
            shutil.rmtree(cache, ignore_errors=True)
    if not sheet:
        return []
    im = Image.open(sheet).convert("RGBA"); W, H = im.size
    esc = min(1.0, 320.0 / max(W, H)); sw, sh = max(8, int(W * esc)), max(8, int(H * esc))
    sm = im.getchannel("A").resize((sw, sh)).point(lambda p: 255 if p > 100 else 0)
    px = sm.load(); lab = [[0] * sw for _ in range(sh)]; boxes = []; cur = 0
    for y in range(sh):
        for x in range(sw):
            if px[x, y] == 255 and not lab[y][x]:
                cur += 1; q = deque([(x, y)]); lab[y][x] = cur
                mnx = mxx = x; mny = mxy = y; n = 0
                while q:
                    cx, cy = q.popleft(); n += 1
                    mnx = min(mnx, cx); mxx = max(mxx, cx); mny = min(mny, cy); mxy = max(mxy, cy)
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < sw and 0 <= ny < sh and not lab[ny][nx] and px[nx, ny] == 255:
                                lab[ny][nx] = cur; q.append((nx, ny))
                if n > 30: boxes.append((mnx, mny, mxx, mxy, n))
    if not boxes:
        os.makedirs(cache, exist_ok=True); return []
    # descartar fragmentos sueltos (salpicaduras/motas de pintura que la IA mete pese al
    # prompt): un componente mucho más chico que la mediana NO es un personaje y al ampliarlo
    # (p.ej. en la página de colorear) queda una mancha. Umbral relativo = robusto entre temas.
    ns = sorted(b[4] for b in boxes); med = ns[len(ns) // 2]
    boxes = [b for b in boxes if b[4] >= 0.22 * med]
    boxes.sort(key=lambda b: (round(b[1] / 16), b[0]))   # orden de lectura
    sx, sy = W / sw, H / sh
    os.makedirs(cache, exist_ok=True); out = []
    for i, (x0, y0, x1, y1, _n) in enumerate(boxes):
        bb = (max(0, int(x0 * sx) - 4), max(0, int(y0 * sy) - 4),
              min(W, int((x1 + 1) * sx) + 4), min(H, int((y1 + 1) * sy) + 4))
        p = f"{cache}/c{i:03d}.png"; im.crop(bb).save(p); out.append(p)
    return out

def _ahash(im, lado=8):
    """Hash perceptual promedio (aHash) de un recorte, para detectar figuras
    repetidas: el mismo monito aparece varias veces en la hoja de stickers y
    elegir por tamaño sacaba 2-3 copias casi idénticas en la misma pieza."""
    g = im.convert("L").resize((lado, lado), Image.LANCZOS)
    px = list(g.getdata())
    prom = sum(px) / len(px)
    return sum(1 << i for i, v in enumerate(px) if v >= prom)


def _hamming(a, b):
    return bin(a ^ b).count("1")


def _es_personaje_vision(tema, paths):
    """Clasifica los recortes del tema con UNA llamada de visión (grilla numerada)
    y devuelve {basename: tipo} SOLO para los que son personajes ('nena', 'mono',
    'león'...), cacheado en actividades_mon/clasif.json. Bugs reales que motiva:
    (1) elegir por tamaño pegaba una MESA y un FRASCO como 'personajes' en
    certificado/cápsula/rompecabezas/corona de artistas; (2) salían 2-3 monitos
    casi idénticos en la misma pieza (el tipo permite elegir personajes DISTINTOS).
    Best-effort: sin API key o ante cualquier error devuelve None (el caller no
    filtra, comportamiento histórico)."""
    import base64 as _b64
    import io as _io
    import json as _json
    import urllib.request as _rq
    if not paths:
        return None
    cache_dir = os.path.dirname(paths[0])
    cache_p = os.path.join(cache_dir, "clasif.json")
    nombres = [os.path.basename(p) for p in paths]
    # el CACHÉ va antes que la key: un tema ya clasificado filtra bien aunque el
    # proceso actual no tenga OPENAI_API_KEY (tests, CLI, workers) — si no, esos
    # procesos caían al modo sin filtro y volvían la mesa/las hojas de palmera.
    try:
        c = json.load(open(cache_p))
        if c.get("archivos") == nombres and isinstance(c.get("tipos"), dict):
            return c["tipos"]
    except Exception:
        pass
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        # grilla de contacto numerada (una sola imagen = una sola llamada). El
        # número va GRANDE adentro de la celda y cada celda lleva borde — con el
        # número chiquito abajo el modelo atribuía etiquetas a la celda vecina
        # (etiquetó un frasco como "nene" en artistas).
        cols = 6
        filas = (len(paths) + cols - 1) // cols
        celda = 200
        grid = Image.new("RGB", (cols * celda, filas * celda), (255, 255, 255))
        from PIL import ImageDraw as _ID
        gdr = _ID.Draw(grid)
        fnt = _font(34)
        for i, p in enumerate(paths):
            im = Image.open(p).convert("RGBA")
            im.thumbnail((celda - 46, celda - 46))
            x = (i % cols) * celda
            y = (i // cols) * celda
            gdr.rectangle([x, y, x + celda - 1, y + celda - 1], outline=(190, 190, 190), width=2)
            grid.paste(im, (x + 40, y + 40), im)
            gdr.text((x + 6, y + 4), str(i), fill=(200, 30, 30), font=fnt,
                     stroke_width=2, stroke_fill=(255, 255, 255))
        buf = _io.BytesIO()
        grid.save(buf, "PNG")
        body = _json.dumps({
            "model": os.environ.get("OPENAI_QA_MODEL", "gpt-4o-mini"),
            "max_tokens": 500,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text":
                 "Cada celda numerada es un sticker recortado de un kit infantil. "
                 "Respondé UNA línea por CADA celda, en el formato 'numero: tipo'. "
                 "Si la celda muestra UN SOLO personaje (una persona, animal o "
                 "criatura CON CARA, entera y sola), tipo = una palabra corta en "
                 "minúscula que lo identifique (ej. 'nena', 'nene', 'mono', "
                 "'león', 'monstruo verde'). Si muestra un objeto sin cara "
                 "(mueble, frasco, herramienta, manguera, planta, flor, comida, "
                 "pelota, globo, estrella) o 2+ personajes juntos, tipo = "
                 "exactamente 'no'. Respondé TODAS las celdas, sin texto extra."},
                {"type": "image_url", "image_url": {"url":
                 "data:image/png;base64," + _b64.b64encode(buf.getvalue()).decode(),
                 "detail": "high"}}]}]}).encode()
        req = _rq.Request("https://api.openai.com/v1/chat/completions", data=body,
                          method="POST", headers={"Authorization": "Bearer " + api_key,
                                                  "Content-Type": "application/json"})
        with _rq.urlopen(req, timeout=45) as r:
            out = _json.loads(r.read())
        resp = out["choices"][0]["message"]["content"] or ""
        import re as _re
        tipos = {}
        for m in _re.finditer(r"(\d+)\s*[:\-]\s*([^\n,;]+)", resp):
            i = int(m.group(1))
            t = m.group(2).strip().lower()[:40]
            if i < len(paths) and t and t != "no":
                tipos[nombres[i]] = t
        if not tipos:
            return None
        with open(cache_p, "w") as f:
            json.dump({"archivos": nombres, "tipos": tipos}, f, ensure_ascii=False)
        return tipos
    except Exception:
        return None


def _seleccionar_recortes(tema, n=2, variedad_estricta=False, incluir_objetos=False):
    """PATHS de los mejores recortes del tema (misma selección que
    personajes_decorativos). La usa también el CUADERNO: usar los recortes
    crudos rompía la matemática de contar/sumas (columnas de stickers apiladas
    contadas como UN personaje — skill §19, bug 1)."""
    return _personajes_paths(tema, n, variedad_estricta, incluir_objetos)


def personajes_decorativos(tema, n=2, variedad_estricta=False, incluir_objetos=False):
    out = []
    for p in _personajes_paths(tema, n, variedad_estricta, incluir_objetos):
        try:
            out.append(Image.open(p).convert("RGBA"))
        except Exception:
            pass
    return out


def _personajes_paths(tema, n=2, variedad_estricta=False, incluir_objetos=False):
    """n personajes reales del tema (recortados de la hoja de stickers) para decorar otros
    productos (rompecabezas, calendario, corona, cápsula, certificado, papertoys…). Reusa
    _extraer_monstruos; SIN fallback genérico — si el tema no tiene stickers, lista vacía
    (nunca mezcla personajes de un tema con otro). Selección: figuras grandes y densas,
    filtradas por un clasificador de visión personaje-vs-objeto (cacheado — sin él, la
    mesa y el frasco de artistas salían de 'personajes'), y DEDUPLICADAS por hash
    perceptual (la misma figura aparece varias veces en la hoja y salían 2-3 monitos
    idénticos en una pieza).

    variedad_estricta=True: SOLO un personaje por tipo (puede devolver menos de n).
    Lo usa el juego de la memoria — con la segunda pasada, dos leones apenas
    distintos salían como pares DIFERENTES y el juego era injugable.

    incluir_objetos=True: si con los personajes no alcanza, completa con los
    OBJETOS del tema (coronas, castillos, varitas… los recortes que la visión
    NO etiquetó como personaje pero pasan los filtros de calidad). Lo usa la
    memoria: en temas de un solo tipo de personaje (princesas) las cartas
    quedaban en 1 princesa + relleno genérico — feedback Pablo 8-jul-2026."""
    try:
        paths = _extraer_monstruos(tema) or []
    except Exception:
        return []
    if not paths:
        return []
    # Puntúa cada figura por área + DENSIDAD (píxeles opacos / recuadro). Un personaje
    # limpio llena bien su recuadro; un recorte MEZCLADO (varios stickers pegados con
    # huecos transparentes en medio) tiene densidad baja → se descarta, así las piezas
    # no salen con amasijos. También se filtran objetos chicos (hojas/íconos) y tiras.
    cand = []
    for p in paths:
        try:
            im = Image.open(p).convert("RGBA")
            w, h = im.size
            area = w * h
            if area < 6000:
                continue
            opacos = sum(im.getchannel("A").histogram()[41:])
            if opacos / area < 0.35:
                continue
            # aspecto: descartar tiras HORIZONTALES (stickers pegados lado a lado)
            # y COLUMNAS apiladas — pero un personaje parado es legítimamente ALTO
            # (una princesa de vestido largo da ~1.7-2.2; el corte simétrico en 1.9
            # las borraba). La columna apilada se delata por DENSIDAD baja (huecos
            # transparentes entre sticker y sticker): alto + ralo = apilado.
            asp_v = h / max(1, w)
            if w >= h and w / max(1, h) > 1.9:
                continue
            if asp_v > 2.6 or (asp_v > 1.9 and opacos / area < 0.55):
                continue
            cand.append((area, p, _ahash(im)))
        except Exception:
            pass
    if not cand:
        return []
    cand_todos = list(cand)              # con objetos incluidos (para incluir_objetos)
    tipos = _es_personaje_vision(tema, paths)
    if tipos:
        # el modelo a veces lista objetos igual (con tipo "objeto"/"globo"/"flor"…)
        # aunque el prompt se lo prohíbe — lista negra sobre la etiqueta.
        no_pers = {"objeto", "objetos", "globo", "globos", "flor", "flores",
                   "estrella", "pelota", "planta", "mesa", "frasco", "nube",
                   "hoja", "corazon", "corazón", "torta", "regalo", "arbol",
                   "árbol", "pincel", "paleta", "casa", "auto", "bandera"}
        tipos = {k: v for k, v in tipos.items() if v not in no_pers}
        con_cara = [c for c in cand if os.path.basename(c[1]) in tipos]
        if con_cara:                     # si el filtro dejó algo, usarlo; si no, no filtrar
            cand = con_cara
    cand.sort(key=lambda t: -t[0])
    # Variedad: primero un personaje de cada TIPO distinto (nena, mono, león...);
    # si hacen falta más, recién ahí repite tipo (el más grande no usado). El hash
    # perceptual queda de red de seguridad para copias casi idénticas sin visión.
    out, tipos_usados, hashes, usados = [], set(), [], set()
    def _pasada(exigir_tipo_nuevo):
        for _area, p, h in cand:
            if len(out) >= n:
                return
            if p in usados or any(_hamming(h, hu) <= 5 for hu in hashes):
                continue
            t = tipos.get(os.path.basename(p)) if tipos else None
            if exigir_tipo_nuevo and t is not None and t in tipos_usados:
                continue
            out.append(p)
            usados.add(p)
            hashes.append(h)
            if t is not None:
                tipos_usados.add(t)
    _pasada(exigir_tipo_nuevo=True)
    if not variedad_estricta:
        _pasada(exigir_tipo_nuevo=False)
    if incluir_objetos and len(out) < n and tipos:
        # completar con objetos del tema (recortes de calidad sin etiqueta de
        # personaje), deduplicados contra lo ya elegido
        objetos = sorted((c for c in cand_todos
                          if os.path.basename(c[1]) not in tipos), key=lambda t: -t[0])
        for _area, p, h in objetos:
            if len(out) >= n:
                break
            if p in usados or any(_hamming(h, hu) <= 5 for hu in hashes):
                continue
            out.append(p)
            usados.add(p)
            hashes.append(h)
    return out

def _lineart(path):
    """Personaje → line-art (contorno negro sobre blanco) para colorear, por DETECCIÓN DE
    BORDES en vez de umbral de luminancia: el umbral rellenaba de negro a los personajes de
    color oscuro. Combina el borde de la silueta (canal alpha) con el detalle interno
    (luminancia), engrosa un poco y lo invierte a líneas negras sobre blanco."""
    s = Image.open(path).convert("RGBA")
    a = s.getchannel("A").point(lambda v: 255 if v > 128 else 0)
    edges_a = a.filter(ImageFilter.FIND_EDGES)                       # borde de la silueta
    bg = Image.new("RGBA", s.size, (255, 255, 255, 255)); bg.alpha_composite(s)
    edges_g = bg.convert("L").filter(ImageFilter.FIND_EDGES)         # detalle interno
    comb = ImageChops.lighter(edges_a, edges_g).point(lambda v: 255 if v > 55 else 0)
    comb = comb.filter(ImageFilter.MaxFilter(3))                     # engrosar el trazo
    return comb.point(lambda v: 0 if v > 0 else 255)                # líneas negras sobre blanco

def _contorno(path):
    """Solo el CONTORNO (silueta) del personaje, línea negra fina sobre blanco. Para 'dibujá
    la otra mitad': una forma limpia para espejar (el line-art interno completo ensucia)."""
    s = Image.open(path).convert("RGBA")
    a = s.getchannel("A").point(lambda v: 255 if v > 128 else 0)
    edge = a.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))
    return edge.point(lambda v: 0 if v > 40 else 255)

def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))

def _sin_halo(im):
    """Saca el aro blanco del die-cut conservando las partes blancas del personaje (guantes).
    Los personajes tienen CONTORNO OSCURO; el aro es el blanco que queda POR FUERA de ese
    contorno. Floodfill desde las esquinas (exterior) avanzando por blanco/transparente hasta
    chocar el contorno oscuro: lo alcanzado = aro -> se quita del alpha. Los guantes, que están
    DENTRO del contorno oscuro, no se alcanzan y quedan intactos. Para la portada (crema)."""
    im = im.convert("RGBA"); W, H = im.size
    a = im.getchannel("A")
    r, g, bl = im.convert("RGB").split()
    mn = ImageChops.darker(ImageChops.darker(r, g), bl)        # canal mínimo = qué tan blanco
    near_white = mn.point(lambda v: 255 if v > 205 else 0)
    transp = a.point(lambda v: 255 if v < 40 else 0)
    passable = ImageChops.lighter(near_white, transp)          # 255 = exterior o aro blanco
    work = passable.copy()
    for seed in ((0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)):
        if work.getpixel(seed) == 255:
            ImageDraw.floodfill(work, seed, 128)               # marca lo alcanzable desde afuera
    reached = work.point(lambda v: 255 if v == 128 else 0)
    quitar = ImageChops.multiply(reached, near_white)          # aro blanco alcanzable (no los guantes)
    out = im.copy(); out.putalpha(ImageChops.subtract(a, quitar)); bb = out.getbbox()
    return out.crop(bb) if bb else out

# ───────────────────────── generadores verificados ─────────────────────────
def _maze(W, H, seed):
    r = random.Random(seed)
    w = [[{'N', 'S', 'E', 'W'} for _ in range(H)] for _ in range(W)]
    v = [[False] * H for _ in range(W)]; st = [(0, 0)]; v[0][0] = 1
    d = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}; o = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    while st:
        x, y = st[-1]
        nb = [(k, x + a, y + b) for k, (a, b) in d.items() if 0 <= x + a < W and 0 <= y + b < H and not v[x + a][y + b]]
        if not nb: st.pop(); continue
        k, nx, ny = r.choice(nb); w[x][y].discard(k); w[nx][ny].discard(o[k]); v[nx][ny] = 1; st.append((nx, ny))
    return w

def _maze_path(w, W, H):
    """Devuelve el camino solución (lista de celdas) o None."""
    d = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    prev = {(0, 0): None}; q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        if (x, y) == (W - 1, H - 1):
            path = []; cur = (x, y)
            while cur is not None: path.append(cur); cur = prev[cur]
            return path[::-1]
        for k, (a, b) in d.items():
            if k not in w[x][y] and 0 <= x + a < W and 0 <= y + b < H and (x + a, y + b) not in prev:
                prev[(x + a, y + b)] = (x, y); q.append((x + a, y + b))
    return None

# ── laberinto circular (theta maze): anillos × sectores, perfecto (siempre tiene salida)
def _theta_maze(rings, S, rnd, se):
    RAD = [[True] * S for _ in range(rings)]   # pared radial en el ángulo s*paso del anillo r
    CIRC = [[True] * S for _ in range(rings)]  # pared circular entre el anillo r y r+1 en el sector s
    HUB = [True] * S                           # pared entre el centro y (0, s)
    def neighbors(node):
        if node == 'C':
            return [((0, s), ('H', s)) for s in range(S)]
        r, s = node
        res = [((r, (s + 1) % S), ('R', r, (s + 1) % S)), ((r, (s - 1) % S), ('R', r, s))]
        res.append(('C' if r == 0 else (r - 1, s), ('H', s) if r == 0 else ('C', r - 1, s)))
        if r < rings - 1:
            res.append(((r + 1, s), ('C', r, s)))
        return res
    def remove(w):
        if w[0] == 'H': HUB[w[1]] = False
        elif w[0] == 'R': RAD[w[1]][w[2]] = False
        else: CIRC[w[1]][w[2]] = False
    visited = {'C'}; stack = ['C']
    while stack:
        nb = [(n, w) for n, w in neighbors(stack[-1]) if n not in visited]
        if not nb: stack.pop(); continue
        n, w = rnd.choice(nb); remove(w); visited.add(n); stack.append(n)
    CIRC[rings - 1][se] = False                 # abrir la salida al exterior
    return RAD, CIRC, HUB

def _theta_path(RAD, CIRC, HUB, rings, S, se):
    def opens(node):
        if node == 'C':
            return [(0, s) for s in range(S) if not HUB[s]]
        r, s = node; res = []
        if not RAD[r][(s + 1) % S]: res.append((r, (s + 1) % S))
        if not RAD[r][s]: res.append((r, (s - 1) % S))
        if r == 0:
            if not HUB[s]: res.append('C')
        elif not CIRC[r - 1][s]: res.append((r - 1, s))
        if r < rings - 1 and not CIRC[r][s]: res.append((r + 1, s))
        return res
    prev = {'C': None}; q = deque(['C']); goal = (rings - 1, se)
    while q:
        n = q.popleft()
        if n == goal:
            p = []; cur = n
            while cur is not None: p.append(cur); cur = prev[cur]
            return p[::-1]
        for m in opens(n):
            if m not in prev: prev[m] = n; q.append(m)
    return None

# ── sudoku 4×4 de figuras: solución única garantizada por conteo
def _sudoku_ok(g, r, c, v):
    if any(g[r][i] == v or g[i][c] == v for i in range(4)): return False
    br, bc = (r // 2) * 2, (c // 2) * 2
    return all(g[i][j] != v for i in range(br, br + 2) for j in range(bc, bc + 2))

def _sudoku_count(g, limit=2):
    for r in range(4):
        for c in range(4):
            if g[r][c] is None:
                n = 0
                for v in range(4):
                    if _sudoku_ok(g, r, c, v):
                        g[r][c] = v; n += _sudoku_count(g, limit); g[r][c] = None
                        if n >= limit: break
                return n
    return 1

def _sudoku_make(rnd):
    g = [[0, 1, 2, 3], [2, 3, 0, 1], [1, 0, 3, 2], [3, 2, 1, 0]]
    perm = list(range(4)); rnd.shuffle(perm)
    g = [[perm[v] for v in row] for row in g]
    for _ in range(8):                          # transformaciones que preservan validez
        op = rnd.randrange(5)
        if op == 0: g[0], g[1] = g[1], g[0]
        elif op == 1: g[2], g[3] = g[3], g[2]
        elif op == 2: g[0:2], g[2:4] = g[2:4], g[0:2]
        elif op == 3:
            for row in g: row[0], row[1] = row[1], row[0]
        else:
            for row in g: row[0:2], row[2:4] = row[2:4], row[0:2]
    sol = [row[:] for row in g]
    puz = [row[:] for row in g]
    cells = [(r, c) for r in range(4) for c in range(4)]; rnd.shuffle(cells)
    quitadas = 0
    for r, c in cells:
        if quitadas >= 8: break
        saved = puz[r][c]; puz[r][c] = None
        if _sudoku_count([row[:] for row in puz]) != 1:
            puz[r][c] = saved
        else:
            quitadas += 1
    return sol, puz

_DIRS = [(1, 0), (0, 1), (1, 1), (-1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1)]
def _wordsearch(words, N, seed):
    r = random.Random(seed); g = [[None] * N for _ in range(N)]; sol = {}
    for w in sorted(words, key=len, reverse=True):
        for _ in range(500):
            dx, dy = r.choice(_DIRS); x = r.randrange(N); y = r.randrange(N)
            if not (0 <= x + dx * (len(w) - 1) < N and 0 <= y + dy * (len(w) - 1) < N): continue
            cs = [(x + dx * i, y + dy * i) for i in range(len(w))]
            if any(g[a][b] not in (None, w[i]) for i, (a, b) in enumerate(cs)): continue
            for i, (a, b) in enumerate(cs): g[a][b] = w[i]
            sol[w] = cs; break
        else:
            return None, None
    for x in range(N):
        for y in range(N):
            if g[x][y] is None: g[x][y] = r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return g, sol

def _ws_has(g, w):
    N = len(g)
    for x in range(N):
        for y in range(N):
            for dx, dy in _DIRS:
                if 0 <= x + dx * (len(w) - 1) < N and 0 <= y + dy * (len(w) - 1) < N and \
                   all(g[x + dx * i][y + dy * i] == w[i] for i in range(len(w))):
                    return True
    return False

# ───────────────────────── piezas de página ─────────────────────────
def _page():
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255)); return im, ImageDraw.Draw(im)
BANNER_H = 92
def _banner(dr, etiqueta):
    """Banner FINO superior: marca CASATRIDIMENSIONAL a la izquierda y la etiqueta
    ('Actividad N · 6 años' o 'Soluciones') a la derecha, con un filete violeta."""
    dr.rectangle([0, 0, Wp, BANNER_H], fill=NAVY)
    dr.text((60, BANNER_H / 2), BRAND, font=_font(30), fill="white", anchor="lm")
    dr.text((Wp - 60, BANNER_H / 2), etiqueta, font=_font(26, False), fill=(205, 200, 230), anchor="rm")
    dr.rectangle([0, BANNER_H, Wp, BANNER_H + 4], fill=VIOLET)
def _foot(dr):
    dr.text((Wp / 2, Hp - 40), "casatridimensional.com.ar", font=_font(20, False), fill=(150, 150, 160), anchor="mm")

def _cake(dr, ccx, ccy, sgn):
    dr.rounded_rectangle([ccx - sgn * .55, ccy - sgn * .05, ccx + sgn * .55, ccy + sgn * .5], sgn * .12, fill=COLS[2])
    dr.rounded_rectangle([ccx - sgn * .55, ccy - sgn * .22, ccx + sgn * .55, ccy + sgn * .12], sgn * .12, fill=COLS[0])
    dr.line([ccx, ccy - sgn * .22, ccx, ccy - sgn * .5], fill=COLS[1], width=3)
    dr.ellipse([ccx - sgn * .12, ccy - sgn * .66, ccx + sgn * .12, ccy - sgn * .42], fill=COLS[5])

def _star_pts(cx, cy, R):
    return [(cx + (R if i % 2 == 0 else R * .45) * math.cos(-math.pi / 2 + i * math.pi / 5),
             cy + (R if i % 2 == 0 else R * .45) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]

def _heart_pts(cx, cy, R, n):
    """n puntos en ORDEN sobre el contorno de un corazón, repartidos por LONGITUD
    DE ARCO (muestrear el parámetro directo amontonaba puntos en el pico y la
    punta — con 30 puntos quedaban pegados y los números ilegibles)."""
    denso = []
    for i in range(720):
        t = math.pi / 2 + 2 * math.pi * i / 720
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        denso.append((cx + x * R / 16, cy + y * R / 16))
    largos = [0.0]
    for a, b2 in zip(denso, denso[1:] + denso[:1]):
        largos.append(largos[-1] + math.hypot(b2[0] - a[0], b2[1] - a[1]))
    total = largos[-1]
    idxs, j = [], 0
    for i in range(n):
        objetivo = total * i / n
        while j < 719 and largos[j + 1] < objetivo:
            j += 1
        idxs.append(j)
    # separación EUCLIDIANA mínima: en el pico del corazón la curva se pliega y
    # dos puntos con igual arco quedan pegados (los números se encimaban)
    # d_min SIEMPRE menor que el espaciado natural (total/n): si lo supera, el
    # ajuste empuja todos los puntos en cascada y el final se apila (bug real)
    d_min = max(36, min(R * 0.22, 0.8 * total / n))
    def _d(a, b3):
        return math.hypot(denso[a][0] - denso[b3][0], denso[a][1] - denso[b3][1])
    for k in range(1, n):
        while idxs[k] < 715 and _d(idxs[k], idxs[k - 1]) < d_min:
            idxs[k] += 4
    # el par que CIERRA el lazo (último ↔ primero) también necesita aire: el
    # ajuste de arriba empujaba al último justo encima del 1
    while len(idxs) > 2 and idxs[-1] > idxs[-2] + 8 and _d(idxs[-1], idxs[0]) < d_min:
        idxs[-1] -= 4
    return [denso[j] for j in idxs]

def _figura_pts(figura, cx, cy, R, n):
    return _heart_pts(cx, cy, R, n) if figura == "corazon" else _star_pts(cx, cy, R)[:n]

def _portada(mons, edad, nombre="Cumpleaños", tema=None):
    """Tapa del cuaderno. Con arte IA del tema (la escena de portada del libro,
    que ya viene compuesta con AIRE arriba para el título) queda como la tapa de
    un libro de verdad — feedback Pablo 9-jul-2026. Fallback: la tapa procedural
    de siempre (crema + personajes)."""
    art = None
    if tema:
        try:
            import libro as _libro
            p = _libro.override_escena_path(tema, 0)
            if os.path.isfile(p):
                art = Image.open(p).convert("RGBA")
        except Exception:
            art = None
    etiqueta = "%s · %s" % (nombre, _edad_label(edad))
    if art is not None:
        import fondos_ia
        im = fondos_ia.cover(art, Wp, Hp)
        dr = ImageDraw.Draw(im)
        # panel translúcido arriba para que el título se lea sobre cualquier arte
        velo = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
        ImageDraw.Draw(velo).rounded_rectangle([100, 130, Wp - 100, 600], 42,
                                               fill=(255, 255, 255, 216))
        im.alpha_composite(velo)
        dr.text((Wp / 2, 260), "Cuaderno de", font=_font(70), fill=NAVY, anchor="mm")
        dr.text((Wp / 2, 360), "Actividades", font=_font(92), fill=VIOLET, anchor="mm")
        ew = max(460, _font(40).getlength(etiqueta) + 80)
        dr.rounded_rectangle([Wp / 2 - ew / 2, 440, Wp / 2 + ew / 2, 530], 45, fill=COLS[1])
        dr.text((Wp / 2, 485), etiqueta, font=_font(40), fill="white", anchor="mm")
        dr.text((Wp / 2, Hp - 40), "casatridimensional.com.ar", font=_font(20, False),
                fill=(150, 150, 160), anchor="mm", stroke_width=4, stroke_fill=(255, 255, 255))
        return im
    # Fondo crema (cálido). Los personajes se pegan SIN el aro blanco del die-cut (_sin_halo),
    # así no se ve contorno en crema y tampoco desaparecen sus partes blancas internas.
    im, dr = _page(); dr.rectangle([0, 0, Wp, Hp], fill=CREAM)
    dr.rounded_rectangle([55, 55, Wp - 55, Hp - 55], 40, outline=VIOLET, width=8)
    dr.text((Wp / 2, 290), "Cuaderno de", font=_font(70), fill=NAVY, anchor="mm")
    dr.text((Wp / 2, 390), "Actividades", font=_font(92), fill=VIOLET, anchor="mm")
    ew = max(460, _font(40).getlength(etiqueta) + 80)
    dr.rounded_rectangle([Wp / 2 - ew / 2, 470, Wp / 2 + ew / 2, 560], 45, fill=COLS[1])
    dr.text((Wp / 2, 515), etiqueta, font=_font(40), fill="white", anchor="mm")
    pos = [(300, 820, 300), (950, 800, 300), (625, 1080, 360), (330, 1360, 300), (930, 1360, 300), (625, 1500, 240)]
    for (x, y, h), p in zip(pos, mons):
        _paste_h(im, _sin_halo(Image.open(p).convert("RGBA")), x, y, h)
    _foot(dr); return im

def _sec(dr, y, titulo, instr):
    dr.text((60, y), titulo, font=_font(38), fill=VIOLET); y += 52
    # la consigna se envuelve para NUNCA salirse del ancho (una consigna larga
    # llegaba hasta el borde de la hoja — guardián tests/test_cuaderno_margenes)
    f = _font(25, False)
    linea = ""
    for w in instr.split():
        t = (linea + " " + w).strip()
        if dr.textlength(t, font=f) <= Wp - 130 or not linea:
            linea = t
        else:
            dr.text((60, y), linea, font=f, fill=INK); y += 34; linea = w
    if linea:
        dr.text((60, y), linea, font=f, fill=INK)
    return y + 48

def _arrow(dr, x0, y0, x1, y1, color=NAVY, w=5):
    # flecha chica y prolija: línea fina + cabeza triangular rellena.
    ang = math.atan2(y1 - y0, x1 - x0); L = 16
    bx, by = x1 - L * 0.85 * math.cos(ang), y1 - L * 0.85 * math.sin(ang)
    dr.line([x0, y0, bx, by], fill=color, width=w)
    dr.polygon([(x1, y1),
                (x1 - L * math.cos(ang - 0.5), y1 - L * math.sin(ang - 0.5)),
                (x1 - L * math.cos(ang + 0.5), y1 - L * math.sin(ang + 0.5))], fill=color)

def _goal_torta(dr, cx, cy, s):
    for dx, col in ((-s * 0.95, COLS[1]), (s * 0.95, COLS[3])):       # globos a los lados
        dr.ellipse([cx + dx - s * 0.34, cy - s * 1.0, cx + dx + s * 0.34, cy - s * 0.2], fill=col)
        dr.line([cx + dx, cy - s * 0.2, cx + dx, cy + s * 0.25], fill=NAVY, width=3)
    _cake(dr, cx, cy, s)

def _draw_maze(im, dr, w, MW, MH, y, mons, sol=False, cell=60):
    mx = (Wp - MW * cell) // 2; lw = max(3, cell // 18)
    w[0][0].discard('W'); w[MW - 1][MH - 1].discard('E')              # abrir entrada (izq) y salida (der)
    for x in range(MW):
        for yy in range(MH):
            cx, cy = mx + x * cell, y + yy * cell; ww = w[x][yy]
            if 'N' in ww: dr.line([cx, cy, cx + cell, cy], fill=NAVY, width=lw)
            if 'W' in ww: dr.line([cx, cy, cx, cy + cell], fill=NAVY, width=lw)
            if x == MW - 1 and 'E' in ww: dr.line([cx + cell, cy, cx + cell, cy + cell], fill=NAVY, width=lw)
            if yy == MH - 1 and 'S' in ww: dr.line([cx, cy + cell, cx + cell, cy + cell], fill=NAVY, width=lw)
    if sol:
        path = _maze_path(w, MW, MH)
        pts = [(mx + px * cell + cell / 2, y + py * cell + cell / 2) for px, py in path]
        dr.line(pts, fill=COLS[0], width=8, joint="curve")
    if mons:                                                          # personaje en la entrada + flecha
        pj = Image.open(mons[3 % len(mons)]).convert("RGBA")
        h = 165
        w = max(1, int(pj.width * h / pj.height))
        if w > 190:                                   # figura ancha: achicar para
            h = max(60, int(190 * pj.height / pj.width))  # que no se salga de la hoja
            w = max(1, int(pj.width * h / pj.height))
        _paste_h(im, pj, max(30 + w // 2, mx - 135), y + 150, h)
        _arrow(dr, mx - 64, y + 115, mx - 6, y + cell / 2 + 4)
    gx = mx + MW * cell + 120; gy = y + (MH - 1) * cell + cell / 2    # meta (torta) en la salida + flecha
    _arrow(dr, mx + MW * cell + 8, gy, gx - 64, gy)
    _goal_torta(dr, gx, gy, 64)
    return y + MH * cell

def _draw_theta(im, dr, RAD, CIRC, HUB, rings, S, se, cx, cy, R0, dt, mons, sol=False, path=None):
    step = 2 * math.pi / S; lw = 5
    def P(rad, ang): return (cx + rad * math.cos(ang), cy + rad * math.sin(ang))
    for r in range(rings):
        for s in range(S):
            if RAD[r][s]:
                a = s * step; dr.line([P(R0 + r * dt, a), P(R0 + (r + 1) * dt, a)], fill=NAVY, width=lw)
    for r in range(rings):
        rad = R0 + (r + 1) * dt
        for s in range(S):
            if CIRC[r][s]:
                dr.arc([cx - rad, cy - rad, cx + rad, cy + rad],
                       math.degrees(s * step), math.degrees((s + 1) * step), fill=NAVY, width=lw)
    for s in range(S):
        if HUB[s]:
            dr.arc([cx - R0, cy - R0, cx + R0, cy + R0],
                   math.degrees(s * step), math.degrees((s + 1) * step), fill=NAVY, width=lw)
    Rmax = R0 + rings * dt; ea = (se + 0.5) * step
    if sol and path:
        pts = [(cx, cy) if n == 'C' else P(R0 + (n[0] + 0.5) * dt, (n[1] + 0.5) * step) for n in path]
        pts.append(P(Rmax + dt * 0.6, ea))
        dr.line(pts, fill=COLS[0], width=7, joint="curve")
    else:
        if mons:
            _paste_h(im, Image.open(mons[0]).convert("RGBA"), cx, cy, R0 * 1.25)
        bx, by = P(Rmax, ea); ax, ay = P(Rmax + dt * 0.55, ea)
        _arrow(dr, bx, by, ax, ay)
        _goal_torta(dr, *P(Rmax + dt * 1.15, ea), 60)
    return cy + Rmax

def _draw_ws(dr, g, sol, y, words, mostrar_sol=False, gs=50):
    """Sopa CENTRADA: la grilla centrada horizontal y la lista de palabras debajo."""
    N = len(g); gx = (Wp - N * gs) // 2; fg = _font(int(gs * 0.6))
    if mostrar_sol:
        for w, cells in sol.items():
            (x0, y0), (x1, y1) = cells[0], cells[-1]
            dr.line([gx + x0 * gs + gs / 2, y + y0 * gs + gs / 2, gx + x1 * gs + gs / 2, y + y1 * gs + gs / 2],
                    fill=COLS[0], width=14)
    for x in range(N):
        for yy in range(N):
            dr.text((gx + x * gs + gs / 2, y + yy * gs + gs / 2), g[x][yy], font=fg, fill=NAVY, anchor="mm")
    yy = y + N * gs + 24
    dr.text((Wp / 2, yy), "Buscá:", font=_font(26), fill=VIOLET, anchor="mm"); yy += 40
    fw = _font(24, False); per = 4
    for row in range((len(words) + per - 1) // per):
        grp = words[row * per:(row + 1) * per]
        txt = "   ".join("• " + w.capitalize() for w in grp)
        dr.text((Wp / 2, yy), txt, font=fw, fill=INK, anchor="mm"); yy += 38
    return yy

# ───────────────────────── sombra ─────────────────────────
def _shadow(path):
    m = Image.open(path).convert("RGBA")
    s = Image.new("RGBA", m.size, (74, 68, 96, 255)); s.putalpha(m.split()[3]); return s

# ───────────────────────── builder: UNA actividad por página ─────────────────────────
TOP = BANNER_H + 78; BOT = Hp - 90

class _Book:
    def __init__(self, edad, mons, seed, nombre="Cumpleaños"):
        self.edad = edad; self.mons = mons; self.rnd = random.Random(seed); self.nombre = nombre
        self.pages = []; self.im = None; self.dr = None; self.y = 0; self.act = 0; self.sol = {}
        self._etq = ""
    def _flush(self):
        if self.im is not None:
            _foot(self.dr)
            # número de página fijo (skill §19: numeración siempre)
            n = len(self.pages) + 1
            self.dr.ellipse([Wp - 96, Hp - 72, Wp - 32, Hp - 8], fill=VIOLET)
            self.dr.text((Wp - 64, Hp - 40), str(n), font=_font(30), fill="white", anchor="mm")
            self.pages.append(self.im)
    def _newpage(self, etiqueta=None):
        self._flush(); self.im, self.dr = _page()
        _banner(self.dr, etiqueta if etiqueta is not None else self._etq); self.y = TOP
    def ensure(self, h):
        if self.im is None or self.y + h > BOT: self._newpage()
    def sec(self, titulo, instr, h=0):
        # cada actividad = su propia página, numerada en el banner.
        self.act += 1
        self._etq = "Actividad %d · %s" % (self.act, _edad_label(self.edad))
        self._newpage()
        self.y = _sec(self.dr, self.y, titulo, instr)
    def mon(self, i):
        return self.mons[i % len(self.mons)] if self.mons else None
    def soladd(self, key, val):                          # acumula soluciones (puede repetirse el tipo)
        self.sol.setdefault(key, []).append(val)
    def finish(self):
        self._flush()

def _IM(p): return Image.open(p).convert("RGBA")

# ───────────────────────── actividades ─────────────────────────
# Cada actividad ocupa TODA la página: las filas se reparten a lo alto del área disponible
# [b.y, BOT] con _slot, y las figuras/grillas se agrandan. _slot empieza en pitch/2 (bien
# debajo del título) -> nunca se pisa el texto.
def _slot(top, rows, i):
    pitch = (BOT - top) / max(1, rows)
    return top + pitch * i + pitch / 2, pitch

def _a_laberinto(b, n):
    seeds = [b.rnd.randrange(1, 10 ** 6) for _ in range(80)]   # semillas variables -> repetible distinto
    for s in seeds:
        w = _maze(n, n, s)
        if _maze_path(w, n, n): break
    assert _maze_path(w, n, n)
    b.sec("El laberinto del cumple", "¡Ayudá al personaje a llegar a la torta de cumpleaños!")
    avail = BOT - b.y
    cell = min(90, (Wp - 470) // n, (avail - 40) // n)        # grande, deja lugar al personaje/torta
    y0 = b.y + max(0, (avail - n * cell) // 2)                # centrado vertical
    _draw_maze(b.im, b.dr, w, n, n, y0, b.mons, cell=cell)
    b.y = BOT
    b.soladd("maze", (w, n, n))

def _a_laberinto_circular(b, rings=4):
    S = 12; se = b.rnd.randrange(0, 6)                # salida en la mitad inferior (queda en página)
    RAD, CIRC, HUB = _theta_maze(rings, S, b.rnd, se)
    path = _theta_path(RAD, CIRC, HUB, rings, S, se)
    assert path                                       # laberinto perfecto → siempre hay salida
    b.sec("Laberinto circular", "Salí desde el centro hasta afuera siguiendo los caminos.")
    avail = BOT - b.y; R0 = 84
    rmax_t = min((Wp - 240) / 2, (avail - 60) / 2)
    dt = max(60, (rmax_t - R0) / (rings + 1))         # +1 deja aire para la flecha/torta de salida
    cx = Wp / 2; cy = b.y + avail / 2
    _draw_theta(b.im, b.dr, RAD, CIRC, HUB, rings, S, se, cx, cy, R0, dt, b.mons)
    b.y = BOT
    b.soladd("cmaze", (RAD, CIRC, HUB, rings, S, se, path))

def _a_sopa(b, words=None):
    words = words or PALABRAS
    grid_words = [_sin_tilde(w) for w in words]    # la grilla sin tildes, la lista con
    base = b.rnd.randrange(1000)
    for s in range(base, base + 120):
        g, sol = _wordsearch(grid_words, 12, s)
        if g and all(_ws_has(g, x) for x in grid_words): break
    assert g and all(_ws_has(g, x) for x in grid_words)
    b.sec("Sopa de letras", "Encontrá las %d palabras escondidas." % len(words))
    N = len(g); gs = 66; blockH = N * gs + 64 + ((len(words) + 3) // 4) * 40 + 30
    top = b.y + max(0, (BOT - b.y - blockH) // 2)             # bloque centrado verticalmente
    _draw_ws(b.dr, g, sol, top, words, gs=gs)
    b.y = BOT
    b.soladd("ws", (g, sol, words))

def _a_puntos(b, nd, figura="estrella"):
    # sin spoiler: la gracia es DESCUBRIR qué figura aparece (skill §19 bug 3)
    b.sec("Uní los puntos", "Uní los puntos en orden, del 1 al %d. ¿Qué figura aparece?" % nd)
    top = b.y; R = min(360, int((BOT - top) * 0.4)); cx, cy = Wp / 2, top + (BOT - top) / 2
    pts = _figura_pts(figura, cx, cy, R, nd); fg = _font(34)
    for i, (px, py) in enumerate(pts):
        # el número va hacia AFUERA de la figura (normal desde el centro): con el
        # criterio del vecino más cercano, en el pliegue del corazón dos rótulos
        # caían en el mismo hueco y se encimaban.
        ux, uy = px - cx, py - cy
        L = math.hypot(ux, uy) or 1.0
        b.dr.ellipse([px - 11, py - 11, px + 11, py + 11], fill=NAVY)
        b.dr.text((px + 40 * ux / L, py + 40 * uy / L), str(i + 1), font=fg,
                  fill=COLS[i % len(COLS)], anchor="mm")
    b.y = BOT

def _a_contar(b, na, nb):
    # a los 2-3 no escriben: la consigna la lee el adulto y el nene señala
    chico = str(b.edad).isdigit() and int(b.edad) <= 3
    consigna = ("¿Cuántos hay? Contalos señalando con el dedo." if chico
                else "¿Cuántos hay de cada uno? Escribí el número.")
    b.sec("Contá", consigna)
    y = b.y; avail = BOT - y; boxh = int(avail * 0.62)
    b.dr.rounded_rectangle([60, y, Wp - 60, y + boxh], 20, outline=(220, 215, 225), width=3)
    spots = []
    def free():
        for _ in range(600):
            x = b.rnd.randint(170, Wp - 180); yy = b.rnd.randint(y + 80, y + boxh - 80)
            if all((x - a) ** 2 + (yy - c) ** 2 > 175 ** 2 for a, c in spots): spots.append((x, yy)); return x, yy
        return b.rnd.randint(170, Wp - 180), b.rnd.randint(y + 80, y + boxh - 80)
    mA, mB = b.mon(1), b.mon(5)
    for _ in range(na):
        x, yy = free();  (mA and _paste_h(b.im, _IM(mA), x, yy, 118))
    for _ in range(nb):
        x, yy = free();  (mB and _paste_h(b.im, _IM(mB), x, yy, 118))
    yb = y + boxh + 95
    if mA: _paste_h(b.im, _IM(mA), 160, yb, 100)
    b.dr.text((235, yb), "¿Cuántos?", font=_font(36), fill=INK, anchor="lm")
    b.dr.rounded_rectangle([540, yb - 40, 626, yb + 40], 10, outline=NAVY, width=3)
    if mB: _paste_h(b.im, _IM(mB), 160, yb + 135, 100)
    b.dr.text((235, yb + 135), "¿Cuántos?", font=_font(36), fill=INK, anchor="lm")
    b.dr.rounded_rectangle([540, yb + 95, 626, yb + 175], 10, outline=NAVY, width=3)
    b.y = BOT; b.soladd("count", (na, nb))

def _a_sombra(b, k):
    if not b.mons: return
    b.sec("Uní con su sombra", "Uní cada personaje con su sombra.")
    idx = list(range(min(len(b.mons), 7))); b.rnd.shuffle(idx); idx = idx[:k]
    right = idx[:]; b.rnd.shuffle(right)
    lx = 330; rx = Wp - 330; sz = min(165, int((BOT - b.y) / k * 0.6))
    for row, i in enumerate(idx):
        yy, _ = _slot(b.y, k, row)
        _paste_h(b.im, _IM(b.mons[i]), lx, yy, sz)
        b.dr.ellipse([lx + sz * 0.6, yy - 9, lx + sz * 0.6 + 18, yy + 9], fill=NAVY)
    for row, i in enumerate(right):
        yy, _ = _slot(b.y, k, row)
        _paste_h(b.im, _shadow(b.mons[i]), rx, yy, sz)
        b.dr.ellipse([rx - sz * 0.6 - 18, yy - 9, rx - sz * 0.6, yy + 9], fill=NAVY)
    b.y = BOT

def _a_diferente(b, rows):
    if not b.mons: return
    b.sec("¿Cuál es diferente?", "Marcá con un círculo el que no es igual.")
    pool = list(range(min(len(b.mons), 7))); sz = min(150, int((BOT - b.y) / rows * 0.55))
    for r in range(rows):
        base, diff = b.rnd.sample(pool, 2); m = 5; odd = b.rnd.randrange(m)
        yy, _ = _slot(b.y, rows, r)
        for c in range(m):
            _paste_h(b.im, _IM(b.mons[diff if c == odd else base]), 180 + c * 190, yy, sz)
    b.y = BOT

def _a_patron(b, rows):
    # Respuesta por OPCIONES (rodear), no "dibujá el que sigue": pedirle a un
    # chico que dibuje una princesa en un casillero era imposible (skill §19).
    if not b.mons or len(b.mons) < 3: return
    b.sec("Continuá el patrón", "Rodeá con un círculo el que sigue en cada fila.")
    pool = list(range(min(len(b.mons), 7)))
    sz0 = min(112, int((BOT - b.y) / rows * 0.45)); res = []
    n_seq = 5; gap = 16; MARG = 80
    for r in range(rows):
        pat = b.rnd.sample(pool, b.rnd.choice([2, 2, 3]))
        yy, _ = _slot(b.y, rows, r)
        correcto = pat[n_seq % len(pat)]
        otros = [p for p in pool if p != correcto]; b.rnd.shuffle(otros)
        ops = [correcto] + otros[:2]; b.rnd.shuffle(ops)
        seq_im = [_IM(b.mons[pat[c % len(pat)]]) for c in range(n_seq)]
        ops_im = [_IM(b.mons[o]) for o in ops]
        # dos pasadas: si con sz0 la fila no entra, se escala TODO para que entre
        def ancho_total(sz):
            box = sz // 2 + 8
            return (sum(_ancho_a(m, sz) + gap for m in seq_im) - gap + gap + 2 * box +
                    46 + 34 + sum(_ancho_a(m, int(sz * 0.92)) + gap for m in ops_im) - gap)
        sz = sz0
        # colchón extra: los redondeos de _paste_h acumulan algunos px por ítem
        while ancho_total(sz) > Wp - 2 * MARG - 56 and sz > 56:
            sz -= 2
        box = sz // 2 + 8
        x = MARG
        for m in seq_im:                             # espaciado por ANCHO real
            w = _ancho_a(m, sz)
            _paste_h(b.im, m, x + w / 2, yy, sz); x += w + gap
        b.dr.rounded_rectangle([x, yy - box, x + 2 * box, yy + box], 12, outline=NAVY, width=3)
        b.dr.text((x + box, yy), "?", font=_font(46), fill=(185, 180, 200), anchor="mm")
        x += 2 * box + 46
        b.dr.line([x, yy - sz * 0.62, x, yy + sz * 0.62], fill=(210, 205, 220), width=3)
        x += 34
        for m in ops_im:
            w = _ancho_a(m, int(sz * 0.92))
            _paste_h(b.im, m, x + w / 2, yy, int(sz * 0.92)); x += w + gap
        res.append(ops.index(correcto) + 1)
    b.y = BOT; b.soladd("patron", res)

def _ancho_a(img, sz):
    """Ancho REAL con el que _paste_h dibuja la imagen a altura sz (la corona es
    ancha y el corazón angosto: espaciar por centros fijos los pegaba/separaba
    desparejo — feedback Pablo)."""
    return max(1, int(img.width * sz / img.height))


def _fila_items(b, img, n, x, yy, sz, gap=14):
    """Pega n copias de img desde el borde izquierdo x, con gap FIJO entre
    bordes. Devuelve el borde derecho de la fila."""
    w = _ancho_a(img, sz)
    for _ in range(n):
        _paste_h(b.im, img, x + w / 2, yy, sz)
        x += w + gap
    return x - gap


def _a_sumas(b, rows):
    if not b.mons: return
    b.sec("Sumas con personajes", "Contá y escribí el resultado.")
    res = []; sz0 = min(84, int((BOT - b.y) / rows * 0.4)); G = 46; MARG = 80
    for r in range(rows):
        a = b.rnd.randint(1, 4); bb = b.rnd.randint(1, 4); yy, _ = _slot(b.y, rows, r)
        bb = max(1, min(bb, 7 - a))    # 4+4 figuras ANCHAS no entran ni escalando
        mA, mB = _IM(b.mon(1)), _IM(b.mon(5))
        # NUNCA pasarse del ancho (regla de Pablo): se calcula el ancho total de
        # la fila con los anchos REALES y se achica sz hasta que entre
        def ancho(sz):
            return (a * _ancho_a(mA, sz) + (a - 1) * 14 + G + 40 + G +
                    bb * _ancho_a(mB, sz) + (bb - 1) * 14 + G + 44 + G + 100)
        sz = sz0
        while ancho(sz) > Wp - 2 * MARG and sz > 40:
            sz -= 2
        x = _fila_items(b, mA, a, MARG, yy, sz)
        b.dr.text((x + G, yy), "+", font=_font(54), fill=INK, anchor="lm")
        x = _fila_items(b, mB, bb, x + G + 40 + G, yy, sz)
        b.dr.text((x + G, yy), "=", font=_font(54), fill=INK, anchor="lm")
        bx = x + G + 44 + G
        b.dr.rounded_rectangle([bx, yy - 52, bx + 100, yy + 52], 10, outline=NAVY, width=3)
        res.append(a + bb)
    b.y = BOT; b.soladd("sumas", res)

def _a_sudoku(b):
    """Sudoku 4×4 de figuras: cada fila/columna/cuadro lleva un monstruo de cada tipo.
    Solución única garantizada (se verifica por conteo). El chico escribe el número."""
    if not b.mons or len(b.mons) < 4: return
    sol, puz = _sudoku_make(b.rnd)
    imgs = [_IM(b.mons[i]) for i in range(4)]

    def _h_max(img, h_tope, w_tope):
        """Altura que respeta AMBOS topes: las figuras anchas (aspecto ~1.9,
        una corona) desbordaban la celda y pisaban los '=' de la leyenda."""
        h = h_tope
        if _ancho_a(img, h) > w_tope:
            h = max(30, int(w_tope * img.height / img.width))
        return h

    b.sec("Sudoku de personajes", "Cada figura es un número. Completá los casilleros vacíos: en cada fila, columna y cuadro va uno de cada.")
    cell = 196; gw = 4 * cell; avail = BOT - b.y
    ly = b.y + max(0, (avail - (gw + 150)) // 2)      # bloque (leyenda + grilla) centrado
    lx = (Wp - 4 * 250) // 2 + 40
    for i in range(4):                                 # leyenda figura = número
        h = _h_max(imgs[i], 88, 150)
        w = _ancho_a(imgs[i], h)
        _paste_h(b.im, imgs[i], lx, ly + 44, h)
        b.dr.text((lx + w / 2 + 14, ly + 44), "= %d" % (i + 1), font=_font(38), fill=INK, anchor="lm")
        lx += 250
    gx = (Wp - gw) // 2; gy = ly + 130
    for r in range(4):
        for c in range(4):
            x0, y0 = gx + c * cell, gy + r * cell
            b.dr.rectangle([x0, y0, x0 + cell, y0 + cell], outline=(150, 145, 160), width=2)
            if puz[r][c] is not None:
                img = imgs[puz[r][c]]
                _paste_h(b.im, img, x0 + cell / 2, y0 + cell / 2,
                         _h_max(img, cell - 46, cell - 26))
    for k in range(0, 5, 2):                          # líneas gruesas de los cuadros 2×2
        b.dr.line([gx + k * cell, gy, gx + k * cell, gy + 4 * cell], fill=NAVY, width=7)
        b.dr.line([gx, gy + k * cell, gx + 4 * cell, gy + k * cell], fill=NAVY, width=7)
    b.y = BOT
    b.soladd("sudoku", sol)

def _a_buscar(b, n):
    """Encontrá los escondidos (iSpy): escena con muchos personajes; buscar X de cada
    tipo. Aprovecha los stickers recortados del tema. Verificable: contamos lo puesto."""
    if not b.mons: return
    b.sec("Encontrá los escondidos", "Buscá en el dibujo y marcá con un círculo:")
    pool = list(range(min(len(b.mons), 7))); imgs = [_IM(b.mons[i]) for i in pool]
    y0 = b.y; boxh = int((BOT - b.y) * 0.78)           # escena grande que llena la página
    b.dr.rounded_rectangle([60, y0, Wp - 60, y0 + boxh], 18, fill=(255, 255, 255), outline=(220, 215, 225), width=3)
    placed = {}; spots = []
    for _ in range(n):
        ti = b.rnd.randrange(len(pool)); sz = b.rnd.randint(95, 132)
        x = y = 0
        for _t in range(60):
            x = b.rnd.randint(120, Wp - 120); y = b.rnd.randint(y0 + 70, y0 + boxh - 70)
            if all((x - a) ** 2 + (y - c) ** 2 > 118 ** 2 for a, c in spots): break
        spots.append((x, y))
        m = imgs[ti].rotate(b.rnd.randint(-22, 22), expand=True, resample=Image.BICUBIC)
        _paste_h(b.im, m, x, y, sz); placed[ti] = placed.get(ti, 0) + 1
    targets = [t for t in placed if placed[t] >= 2][:3] or list(placed.keys())[:2]
    ty = y0 + boxh + 60; tx = 130
    for t in targets:
        _paste_h(b.im, imgs[t], tx + 46, ty, 92)
        b.dr.text((tx + 104, ty), "× %d" % placed[t], font=_font(42), fill=INK, anchor="lm")
        tx += 280
    b.y = BOT
    b.soladd("buscar", [placed[t] for t in targets])

def _colorear_imgs(tema):
    """Páginas para colorear DIBUJADAS por OpenAI (colorear*.png en extras/ o ia_draft/),
    cada una con garantía B/N idempotente. Lista (puede haber varias). Vacía si todavía no
    hay ninguna -> el cuaderno cae al line art derivado del personaje (fallback)."""
    seen, out = set(), []
    for d in ("extras", "ia_draft"):
        for p in sorted(glob.glob(os.path.join(TEMAS, tema, d, "colorear*.png"))):
            n = os.path.basename(p)
            if n in seen:
                continue
            seen.add(n)
            im = Image.open(p).convert("RGBA")
            bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
            out.append(bg.convert("L").point(lambda v: 0 if v < 165 else 255).convert("RGBA"))
    return out

def _a_colorear(b, k=0):
    imgs = getattr(b, "_colorear", [])
    if k >= len(imgs):
        # SIN arte IA la página NO va (skill §19 bug 2): el viejo fallback
        # ampliaba un sticker de 300px a página entera → masa negra pixelada.
        # El botón ⚡ genera las 3 variantes de colorear de cada tema.
        return
    b.sec("Pintá el dibujo", "Coloreá como más te guste.")
    la = imgs[k]
    h = 980; w = int(la.width * h / la.height)
    if w > Wp - 160:
        w = Wp - 160; h = int(la.height * w / la.width)
    la = la.resize((w, h), Image.LANCZOS)
    b.im.alpha_composite(la, (int(Wp / 2 - w / 2), b.y + 10))
    b.y = BOT

# ── actividades nuevas (todas por código, reusan los recortes del tema) ──
def _a_restas(b, rows):
    if not b.mons: return
    b.sec("Restas con personajes", "Tachá los que se van y escribí cuántos quedan.")
    m = _IM(b.mon(2)); res = []; sz0 = min(100, int((BOT - b.y) / rows * 0.4)); G = 46
    MARG = 80
    for r in range(rows):
        a = b.rnd.randint(2, 5); c = b.rnd.randint(1, a - 1); yy, _ = _slot(b.y, rows, r)
        sz = sz0
        while a * _ancho_a(m, sz) + (a - 1) * 14 + G + 44 + G + 100 > Wp - 2 * MARG and sz > 50:
            sz -= 2
        w = _ancho_a(m, sz)
        x = MARG
        for i in range(a):
            _paste_h(b.im, m, x + w / 2, yy, sz)
            if i >= a - c:
                cxx = x + w / 2
                b.dr.line([cxx - w * 0.5, yy - sz * 0.45, cxx + w * 0.5, yy + sz * 0.45],
                          fill=COLS[0], width=7)
            x += w + 14
        x -= 14
        b.dr.text((x + G, yy), "=", font=_font(54), fill=INK, anchor="lm")
        bx = x + G + 44 + G
        b.dr.rounded_rectangle([bx, yy - 52, bx + 100, yy + 52], 10, outline=NAVY, width=3)
        res.append(a - c)
    b.y = BOT; b.soladd("restas", res)

def _a_serie(b, rows):
    b.sec("Completá la serie", "Mirá los números y escribí los que faltan.")
    res = []; rad = 54
    for r in range(rows):
        step = b.rnd.choice([1, 1, 2]); start = b.rnd.randint(1, 6)
        seq = [start + step * i for i in range(7)]
        blanks = sorted(b.rnd.sample(range(2, 7), 2))
        yy, _ = _slot(b.y, rows, r); x0 = 130; gap = 150
        for i, v in enumerate(seq):
            cx = x0 + i * gap
            if i in blanks:
                b.dr.rounded_rectangle([cx - rad, yy - rad, cx + rad, yy + rad], 12, outline=NAVY, width=3)
            else:
                b.dr.ellipse([cx - rad, yy - rad, cx + rad, yy + rad], fill=COLS[i % len(COLS)])
                b.dr.text((cx, yy), str(v), font=_font(48), fill="white", anchor="mm")
        res.append([seq[i] for i in blanks])
    b.y = BOT; b.soladd("serie", res)

def _a_mas_menos(b, rows):
    if not b.mons: return
    b.sec("¿Cuál tiene más?", "Marcá con un círculo el grupo que tiene MÁS.")
    bw = (Wp - 120 - 40) // 2; res = []; pitch = (BOT - b.y) / rows; bh = pitch * 0.8
    for r in range(rows):
        yy = b.y + pitch * r + (pitch - bh) / 2
        counts = [b.rnd.randint(1, 5), b.rnd.randint(1, 5)]
        while counts[0] == counts[1]:
            counts[1] = b.rnd.randint(1, 5)
        m = _IM(b.mon(r + 1))
        for side in (0, 1):
            bx = 60 + side * (bw + 40)
            b.dr.rounded_rectangle([bx, yy, bx + bw, yy + bh], 18, outline=(210, 205, 220), width=3)
            for i in range(counts[side]):
                cx = bx + 110 + (i % 3) * 140; cyy = yy + bh * 0.32 + (i // 3) * (bh * 0.4)
                _paste_h(b.im, m, cx, cyy, 92)
        res.append(0 if counts[0] > counts[1] else 1)
    b.y = BOT; b.soladd("masmenos", res)

def _a_tamano(b, rows):
    if not b.mons: return
    b.sec("Grande y chico", "En cada fila, marcá con un círculo el MÁS GRANDE.")
    res = []
    for r in range(rows):
        m = _IM(b.mon(r + 2)); yy, _ = _slot(b.y, rows, r)
        sizes = [95, 155, 80, 200]; b.rnd.shuffle(sizes)
        for c, h in enumerate(sizes):
            _paste_h(b.im, m, 230 + c * 255, yy, h)
        res.append(sizes.index(max(sizes)))
    b.y = BOT; b.soladd("tamano", res)

def _a_iguales(b, k):
    if not b.mons or len(b.mons) < k: return
    b.sec("Uní los iguales", "Uní cada dibujo con su igual.")
    idx = list(range(min(len(b.mons), 7))); b.rnd.shuffle(idx); idx = idx[:k]
    right = idx[:]; b.rnd.shuffle(right)
    lx = 330; rx = Wp - 330; sz = min(165, int((BOT - b.y) / k * 0.6))
    for row, i in enumerate(idx):
        yy, _ = _slot(b.y, k, row)
        _paste_h(b.im, _IM(b.mons[i]), lx, yy, sz)
        b.dr.ellipse([lx + sz * 0.6, yy - 9, lx + sz * 0.6 + 18, yy + 9], fill=NAVY)
    for row, i in enumerate(right):
        yy, _ = _slot(b.y, k, row)
        _paste_h(b.im, _IM(b.mons[i]), rx, yy, sz)
        b.dr.ellipse([rx - sz * 0.6 - 18, yy - 9, rx - sz * 0.6, yy + 9], fill=NAVY)
    b.y = BOT

def _a_trazos(b, rows):
    b.sec("Repasá las líneas", "Seguí la línea punteada con el lápiz, de izquierda a derecha.")
    estilos = ["recta", "zigzag", "curva", "onda", "lazo"]; b.rnd.shuffle(estilos)
    for r in range(rows):
        yy, pitch = _slot(b.y, rows, r); amp = min(70, pitch * 0.28)
        est = estilos[r % len(estilos)]; x0, x1 = 250, Wp - 230
        pts = []
        for i in range(81):
            t = i / 80; x = x0 + (x1 - x0) * t
            if est == "recta": y = yy
            elif est == "zigzag": y = yy + (amp if int(t * 8) % 2 else -amp)
            elif est == "curva": y = yy - amp * math.sin(t * math.pi)
            elif est == "onda": y = yy - amp * 0.7 * math.sin(t * math.pi * 4)
            else: y = yy - amp * 0.85 * math.sin(t * math.pi * 3)
            pts.append((x, y))
        for i in range(0, len(pts) - 1, 2):
            b.dr.line([pts[i], pts[i + 1]], fill=NAVY, width=7)
        if b.mons:
            _paste_h(b.im, _IM(b.mon(r)), x0 - 80, yy, min(140, int(pitch * 0.6)))
        _goal_torta(b.dr, x1 + 70, yy, 54)
    b.y = BOT

def _tema_palabras(tema):
    """Palabras TEMÁTICAS para la sopa/código (tema.json::palabras) — la sopa con
    vocabulario genérico de cumpleaños violaba la regla 'el tema es estructural'
    (skill §19). Fallback: las genéricas de siempre."""
    try:
        ws = json.load(open(os.path.join(TEMAS, tema, "tema.json"), encoding="utf-8")).get("palabras")
        ws = [str(w).strip().upper() for w in (ws or []) if str(w).strip()]
        return ws[:8] if len(ws) >= 4 else None
    except Exception:
        return None


def _a_codigo(b, palabra):
    """Código secreto: cada figura es una letra — decodificá la palabra del tema.
    Actividad 6+ de los libros pro (Highlights); verificable: la clave ES la palabra."""
    letras = []
    for ch in _sin_tilde(palabra):
        if ch not in letras:
            letras.append(ch)
    if not b.mons or len(b.mons) < len(letras): return
    b.sec("Código secreto", "Cada figura es una letra. Descubrí la palabra escondida.")
    figs = {ch: _IM(b.mons[i]) for i, ch in enumerate(letras)}
    # leyenda figura=letra en 2 filas con la MISMA grilla de columnas (cada fila
    # con su propio paso quedaba desalineada — feedback Pablo) y el "= X" en una
    # posición FIJA de cada columna, sin depender del ancho de la figura
    per = (len(letras) + 1) // 2
    col_w = (Wp - 160) / per
    for idx, ch in enumerate(letras):
        fila, col = divmod(idx, per)
        x0 = 80 + col * col_w
        cy = b.y + 80 + fila * 150
        h = 96
        if _ancho_a(figs[ch], h) > col_w * 0.44:
            h = max(40, int(col_w * 0.44 * figs[ch].height / figs[ch].width))
        _paste_h(b.im, figs[ch], x0 + col_w * 0.26, cy, h)
        b.dr.text((x0 + col_w * 0.54, cy), "= " + ch, font=_font(40), fill=INK, anchor="lm")
    ly = b.y + 80 + 150
    # la palabra codificada: figuras con un casillero debajo de cada una
    seq = [figs[ch] for ch in _sin_tilde(palabra)]
    yy = ly + (BOT - ly) / 2
    sz = 120; gap = 26; MARG = 90
    def ancho(s):
        return sum(max(_ancho_a(m, s), 96) + gap for m in seq) - gap
    while ancho(sz) > Wp - 2 * MARG and sz > 56:
        sz -= 2
    x = (Wp - ancho(sz)) / 2
    for m in seq:
        w = max(_ancho_a(m, sz), 96)
        _paste_h(b.im, m, x + w / 2, yy - 60, sz)
        b.dr.rounded_rectangle([x + w / 2 - 44, yy + 40, x + w / 2 + 44, yy + 128], 10,
                               outline=NAVY, width=3)
        x += w + gap
    b.y = BOT
    b.soladd("codigo", palabra)


def _a_diferencias(b, n_dif=5):
    """Buscá las diferencias: dos escenas iguales, la de abajo con n_dif cambios
    CONTROLADOS (se sabe exactamente qué cambió → solucionario verificable)."""
    if not b.mons or len(b.mons) < 3: return
    n_dif = min(n_dif, 4)          # 5 de 10 era "buscá los iguales": pocas y sutiles
    b.sec("Buscá las diferencias", "Hay %d diferencias entre los dos dibujos. Marcalas en el de abajo." % n_dif)
    pool = list(range(min(len(b.mons), 7)))
    cols_n, rows_n = 6, 2
    slots = [(c, r) for r in range(rows_n) for c in range(cols_n)]
    base = [b.rnd.choice(pool) for _ in slots]
    cambios = b.rnd.sample(range(len(slots)), n_dif)
    alt = list(base)
    for i in cambios:
        alt[i] = b.rnd.choice([p for p in pool if p != base[i]])
    boxh = int((BOT - b.y - 60) / 2)
    for bi, contenido in ((0, base), (1, alt)):
        y0 = b.y + bi * (boxh + 40)
        b.dr.rounded_rectangle([60, y0, Wp - 60, y0 + boxh], 16,
                               outline=(215, 210, 225), width=3)
        for (c, r), ti in zip(slots, contenido):
            cx = 60 + (c + 0.5) * (Wp - 120) / cols_n
            cy = y0 + (r + 0.5) * boxh / rows_n
            img = _IM(b.mons[ti])
            h = min(130, int(boxh / rows_n * 0.62))
            if _ancho_a(img, h) > (Wp - 120) / cols_n - 24:
                h = max(40, int(((Wp - 120) / cols_n - 24) * img.height / img.width))
            _paste_h(b.im, img, cx, cy, h)
    b.y = BOT
    b.soladd("difs", sorted((i % cols_n) + 1 + (i // cols_n) * cols_n for i in cambios))


def _a_otra_mitad(b):
    if not b.mons: return
    b.sec("Dibujá la otra mitad", "Mirá la mitad del dibujo y dibujá la que falta.")
    src = _contorno(max(b.mons, key=lambda p: Image.open(p).size[1])).convert("RGBA")
    h = 760; w = int(src.width * h / src.height); src = src.resize((w, h), Image.LANCZOS)
    half = src.crop((0, 0, w // 2, h)); axis = Wp // 2; top = b.y + 40
    b.im.alpha_composite(half, (axis - w // 2, top))
    for yy in range(top - 10, top + h + 10, 30):
        b.dr.line([axis, yy, axis, yy + 15], fill=(150, 150, 160), width=4)
    b.y = BOT

def _a_tateti(b):
    b.sec("Ta-te-ti", "Jugá con un amigo. Cada uno elige un personaje; gana quien hace tres en línea.")
    if b.mons:
        _paste_h(b.im, _IM(b.mon(0)), 250, b.y + 40, 95)
        b.dr.text((320, b.y + 40), "vs", font=_font(38), fill=INK, anchor="lm")
        _paste_h(b.im, _IM(b.mon(1)), 470, b.y + 40, 95)
    y0 = b.y + 130; g = 330; gap = 90; bx0 = (Wp - (2 * g + gap)) // 2
    for bi in range(4):
        r, c = divmod(bi, 2); ox = bx0 + c * (g + gap); oy = y0 + r * (g + gap)
        for k in (1, 2):
            b.dr.line([ox + k * g / 3, oy, ox + k * g / 3, oy + g], fill=NAVY, width=6)
            b.dr.line([ox, oy + k * g / 3, ox + g, oy + k * g / 3], fill=NAVY, width=6)
    b.y = BOT

def _solucionario(b):
    keys = ("maze", "cmaze", "ws", "sudoku", "sumas", "restas", "serie", "count",
            "masmenos", "tamano", "patron", "codigo", "difs")
    if not any(k in b.sol for k in keys): return
    pages = []; im, dr = _page(); _banner(dr, "Soluciones"); y = TOP
    dr.text((60, y), "Soluciones", font=_font(44), fill=COLS[0]); y += 76
    def newpage():
        nonlocal im, dr, y
        _foot(dr); pages.append(im); im, dr = _page(); _banner(dr, "Soluciones"); y = TOP
    def need(h):
        if y + h > BOT: newpage()
    for (w, MW, MH) in b.sol.get("maze", []):
        need(MH * 60 + 80); dr.text((60, y), "Laberinto:", font=_font(28), fill=VIOLET); y += 44
        y = _draw_maze(im, dr, w, MW, MH, y, b.mons, sol=True) + 36
    for (RAD, CIRC, HUB, rings, S, se, path) in b.sol.get("cmaze", []):
        R0 = 40; dt = 46; Rmax = R0 + rings * dt; need(2 * Rmax + 90)
        dr.text((60, y), "Laberinto circular:", font=_font(28), fill=VIOLET); y += 54
        cx = Wp / 2; cy = y + Rmax
        _draw_theta(im, dr, RAD, CIRC, HUB, rings, S, se, cx, cy, R0, dt, b.mons, sol=True, path=path)
        y = cy + Rmax + 36
    for (g, sol, words) in b.sol.get("ws", []):
        need(len(g) * 50 + 130); dr.text((60, y), "Sopa de letras:", font=_font(28), fill=VIOLET); y += 44
        y = _draw_ws(dr, g, sol, y, words, mostrar_sol=True) + 24
    for sgrid in b.sol.get("sudoku", []):
        cell = 76; need(4 * cell + 90); dr.text((60, y), "Sudoku (números):", font=_font(28), fill=VIOLET); y += 50
        gx = (Wp - 4 * cell) // 2
        for r in range(4):
            for c in range(4):
                x0, y0 = gx + c * cell, y + r * cell
                dr.rectangle([x0, y0, x0 + cell, y0 + cell], outline=(150, 145, 160), width=2)
                dr.text((x0 + cell / 2, y0 + cell / 2), str(sgrid[r][c] + 1), font=_font(38), fill=NAVY, anchor="mm")
        for k in range(0, 5, 2):
            dr.line([gx + k * cell, y, gx + k * cell, y + 4 * cell], fill=NAVY, width=5)
            dr.line([gx, y + k * cell, gx + 4 * cell, y + k * cell], fill=NAVY, width=5)
        y += 4 * cell + 30
    lines = []
    for res in b.sol.get("sumas", []): lines.append("Sumas: " + ", ".join(map(str, res)))
    for res in b.sol.get("restas", []): lines.append("Restas: " + ", ".join(map(str, res)))
    for res in b.sol.get("serie", []):
        lines.append("Serie — faltan: " + "  ".join("/".join(map(str, blk)) for blk in res))
    for (na, nb) in b.sol.get("count", []): lines.append("Contar — Grupo 1: %d · Grupo 2: %d" % (na, nb))
    for res in b.sol.get("masmenos", []):
        lines.append("¿Cuál tiene más?: " + ", ".join("izquierda" if v == 0 else "derecha" for v in res))
    for res in b.sol.get("tamano", []):
        lines.append("El más grande: posición " + ", ".join(str(v + 1) for v in res))
    for res in b.sol.get("patron", []):
        lines.append("Patrón — opción correcta: " + ", ".join(str(v) for v in res))
    for palabra in b.sol.get("codigo", []):
        lines.append("Código secreto: %s" % palabra)
    for pos in b.sol.get("difs", []):
        lines.append("Diferencias — casilleros (1-12, de izq. a der. y de arriba abajo): "
                     + ", ".join(str(v) for v in pos))
    lines.append("(Sombra, intruso, iguales, trazos, otra mitad y colorear se revisan a simple vista.)")
    for ln in lines:
        need(40); dr.text((60, y), ln, font=_font(23), fill=INK); y += 36
    _foot(dr); pages.append(im); b.pages.extend(pages)

# ───────────────────── armado por banda de edad ─────────────────────
def _construir(b, e, palabras=None):
    """Secuencia por banda de edad, RECALIBRADA con los hitos del CDC/Kumon (skill
    §19, fase 2): dificultad progresiva dentro de cada banda, sin páginas
    duplicadas como relleno, sin tareas de sala de 2 a los 6 años ni consignas de
    lectoescritura a los 2-3. `palabras`: vocabulario temático (sopa/código)."""
    ws = palabras or PALABRAS
    if e <= 3:
        # 2-3 años: motricidad + discriminación visual. SIN números escritos,
        # SIN letras, SIN 'unir puntos' con secuencia numérica (CDC).
        _a_colorear(b, 0); _a_trazos(b, 4); _a_sombra(b, 3); _a_iguales(b, 3)
        _a_tamano(b, 3); _a_contar(b, 3, 2); _a_patron(b, 3); _a_mas_menos(b, 3)
        _a_trazos(b, 4); _a_buscar(b, 8); _a_colorear(b, 1); _a_colorear(b, 2)
    elif e <= 5:
        # 4-5 años: fácil → difícil; puntos 1-10 primero y 1-20 al final
        _a_trazos(b, 4); _a_colorear(b, 0); _a_sombra(b, 4); _a_iguales(b, 4)
        _a_puntos(b, 10, "estrella"); _a_contar(b, 5, 3); _a_patron(b, 3)
        _a_tamano(b, 3); _a_mas_menos(b, 3); _a_diferente(b, 3)
        _a_laberinto(b, 7); _a_sudoku(b); _a_buscar(b, 14)
        _a_laberinto(b, 8); _a_puntos(b, 20, "corazon"); _a_tateti(b)
        _a_colorear(b, 1); _a_colorear(b, 2)
    else:
        # 6-7 años: AFUERA las tareas de sala de 2 (iguales, más grande, cuál
        # tiene más); sopa TEMÁTICA; código secreto y diferencias en vez de
        # páginas repetidas; puntos 1-30; segundo laberinto MÁS difícil (11x11).
        _a_colorear(b, 0); _a_laberinto(b, 9); _a_contar(b, 6, 4)
        _a_sombra(b, 4); _a_sopa(b, ws); _a_puntos(b, 30, "corazon")
        _a_sumas(b, 4); _a_patron(b, 3); _a_diferencias(b, 4)
        _a_laberinto_circular(b, 4); _a_colorear(b, 1); _a_restas(b, 4)
        pal_codigo = min([w for w in ws if 5 <= len(w) <= 8] or ws, key=len)
        _a_codigo(b, pal_codigo); _a_sudoku(b); _a_serie(b, 4)
        _a_buscar(b, 18); _a_diferente(b, 3); _a_laberinto(b, 11)
        _a_tateti(b); _a_colorear(b, 2)

# ───────────────────────── armado ─────────────────────────
def _cover_mons(tema, mons):
    """6 personajes para la portada. Por defecto los primeros 6 (orden de lectura). Cada tema
    puede curarlos con tema.json::portada_mons = [índices] (p.ej. para elegir un payaso más
    prolijo). Completa con el resto si la lista es corta."""
    try:
        idx = json.load(open(os.path.join(TEMAS, tema, "tema.json"), encoding="utf-8")).get("portada_mons")
    except Exception:
        idx = None
    if idx:
        sel = [mons[i] for i in idx if 0 <= i < len(mons)]
        resto = [p for p in mons if p not in sel]
        return (sel + resto)[:6]
    return mons[:6]

def _build(tema, edad, seed):
    """Devuelve (paginas_actividades, paginas_solucionario) por separado, para que la galería
    de la tienda pueda excluir el solucionario sin regenerar."""
    # recortes FILTRADOS (skill §19 bug 1): dedup + sin columnas apiladas + visión.
    # Con menos de 4 utilizables se cae a los crudos (mejor algo que nada).
    mons = _seleccionar_recortes(tema, 8, incluir_objetos=True)
    if len(mons) < 4:
        mons = _extraer_monstruos(tema)
    nombre = _tema_nombre(tema)
    b = _Book(edad, mons, seed, nombre); b._colorear = _colorear_imgs(tema)
    portada = _portada(_cover_mons(tema, mons), edad, nombre, tema=tema)
    e = int(edad) if str(edad).isdigit() else 6
    _construir(b, e, palabras=_tema_palabras(tema)); b.finish()
    acts = [portada] + list(b.pages)
    b.pages = []; _solucionario(b)
    return acts, list(b.pages)

def paginas(tema, edad, seed=1, con_solucionario=True):
    """Lista de páginas (PIL.Image) del cuaderno, ya verificadas. Es lo que consume el motor
    del kit para empaquetar el ZIP del producto."""
    acts, sols = _build(tema, edad, seed)
    return acts + sols if con_solucionario else acts

def preview_paths(tema, edad="6"):
    """Páginas del cuaderno cacheadas como PNG (para la galería de la ficha de la
    tienda). Sin solucionario (no spoilea respuestas). Se regenera si no existe."""
    cache = os.path.join(TEMAS, tema, "actividades_preview")
    pngs = sorted(glob.glob(os.path.join(cache, "p*.png")))
    if pngs:
        return pngs
    try:
        pgs = paginas(tema, str(edad), con_solucionario=False)
    except Exception:
        return []
    os.makedirs(cache, exist_ok=True); out = []
    for i, p in enumerate(pgs):
        pp = os.path.join(cache, "p%02d.png" % i); p.convert("RGB").save(pp); out.append(pp)
    return out

def generar_cuaderno(tema, edad, out_dir, seed=1):
    os.makedirs(out_dir, exist_ok=True)
    rgb = [p.convert("RGB") for p in paginas(tema, edad, seed)]
    paths = []
    for i, p in enumerate(rgb):
        pp = os.path.join(out_dir, "pg%d.png" % i); p.save(pp); paths.append(pp)
    out = paths
    try:
        pdf = os.path.join(out_dir, "cuaderno_%s_%s.pdf" % (tema, edad))
        # resolution=150: páginas 1240x1754 = "A4 a 150dpi"; sin declararla el
        # PDF multipágina sale a otro tamaño físico (CLAUDE.md regla #5).
        rgb[0].save(pdf, save_all=True, append_images=rgb[1:], resolution=150); out = pdf
    except Exception:
        out = paths
    return out, len(rgb)


# ───────────── cuaderno canónico + overrides del usuario (panel del kit) ─────────────
# Cada (tema, edad) tiene UN cuaderno canónico cacheado en actividades_cache/<edad>/b*.png.
# Pablo lo cura desde el panel: reemplaza (override pg*.png) o quita (pg*.removed) páginas.
# Todos los compradores reciben esa versión curada (el cuaderno no tiene personalización).
def _cache_dir(tema, edad): return os.path.join(TEMAS, tema, "actividades_cache", str(edad))
def _override_dir(tema, edad): return os.path.join(TEMAS, tema, "actividades_override", str(edad))

def base_paginas(tema, edad, seed=1):
    """Cuaderno canónico (cacheado). Se genera una sola vez por tema+edad."""
    cd = _cache_dir(tema, edad)
    pngs = sorted(glob.glob(os.path.join(cd, "b*.png")))
    if pngs:
        return [Image.open(p).convert("RGB") for p in pngs]
    acts, sols = _build(tema, str(edad), seed)
    pgs = [p.convert("RGB") for p in (acts + sols)]
    os.makedirs(cd, exist_ok=True)
    for i, p in enumerate(pgs):
        p.save(os.path.join(cd, "b%02d.png" % i))
    with open(os.path.join(cd, "nsol.txt"), "w") as f:    # cuántas páginas finales son solucionario
        f.write(str(len(sols)))
    return pgs

def _n_sol(tema, edad):
    try:
        return int(open(os.path.join(_cache_dir(tema, edad), "nsol.txt")).read().strip())
    except Exception:
        return 1

def regenerar_pagina(tema, edad, idx):
    """Genera una VARIANTE NUEVA de la página <idx> (mismo tipo de actividad —el orden del
    menú por banda de edad es fijo—, pero contenido interno distinto: otro laberinto, otra
    sopa de letras, etc.) y la guarda como override. No toca el resto del cuaderno."""
    import random as _random
    base = base_paginas(tema, edad)
    if idx >= len(base):
        return False
    seed = _random.randint(2, 999999)   # el seed 1 es el canónico; cualquier otro da otra variante
    acts, sols = _build(tema, str(edad), seed)
    fresh = [p.convert("RGB") for p in (acts + sols)]
    if idx >= len(fresh):
        return False
    od = _override_dir(tema, edad); os.makedirs(od, exist_ok=True)
    fresh[idx].save(os.path.join(od, "pg%02d.png" % idx))
    rmp = os.path.join(od, "pg%02d.removed" % idx)
    if os.path.exists(rmp):
        os.remove(rmp)
    return True

def pagina_efectiva(tema, edad, idx, base=None):
    """Página final del índice idx: el override del usuario si existe, si no la canónica."""
    ov = os.path.join(_override_dir(tema, edad), "pg%02d.png" % idx)
    if os.path.isfile(ov):
        return Image.open(ov).convert("RGB")
    base = base if base is not None else base_paginas(tema, edad)
    return base[idx] if idx < len(base) else None

def paginas_finales(tema, edad, seed=1):
    """Cuaderno a entregar: canónico + overrides (reemplazos, quitadas, extras)."""
    base = base_paginas(tema, edad, seed); od = _override_dir(tema, edad); out = []
    for i in range(len(base)):
        if os.path.exists(os.path.join(od, "pg%02d.removed" % i)):
            continue
        out.append(pagina_efectiva(tema, edad, i, base))
    for ep in sorted(glob.glob(os.path.join(od, "pg*.png"))):     # páginas extra agregadas
        try: idx = int(os.path.basename(ep)[2:4])
        except ValueError: continue
        if idx >= len(base):
            out.append(Image.open(ep).convert("RGB"))
    return [p for p in out if p is not None]

def estado(tema, edad, seed=1):
    """Estado de cada página para el panel: idx, si está reemplazada o quitada."""
    base = base_paginas(tema, edad, seed); od = _override_dir(tema, edad); items = []
    for i in range(len(base)):
        items.append({"idx": i,
                      "removed": os.path.exists(os.path.join(od, "pg%02d.removed" % i)),
                      "override": os.path.isfile(os.path.join(od, "pg%02d.png" % i)), "extra": False})
    for ep in sorted(glob.glob(os.path.join(od, "pg*.png"))):
        try: idx = int(os.path.basename(ep)[2:4])
        except ValueError: continue
        if idx >= len(base):
            items.append({"idx": idx, "removed": False, "override": True, "extra": True})
    return {"tema": tema, "edad": str(edad), "n": len(base), "paginas": items}

def galeria_indices(tema, edad="6"):
    """Índices de página a mostrar en la galería de la ficha: el cuaderno curado
    (canónico + overrides) SIN la hoja de solucionario (no spoilea respuestas)."""
    base = base_paginas(tema, edad); od = _override_dir(tema, edad)
    cut = len(base) - _n_sol(tema, edad)               # las últimas páginas son el solucionario
    out = []
    for i in range(len(base)):
        if i >= cut:                                   # solucionario → no mostrar en la galería
            continue
        if os.path.exists(os.path.join(od, "pg%02d.removed" % i)):
            continue
        out.append(i)
    for ep in sorted(glob.glob(os.path.join(od, "pg*.png"))):
        try: idx = int(os.path.basename(ep)[2:4])
        except ValueError: continue
        if idx >= len(base):
            out.append(idx)
    return out

def regenerar(tema, edad):
    """Borra el cuaderno canónico cacheado (la próxima vez se genera uno nuevo).
    NO toca los overrides del usuario."""
    import shutil
    for d in (_cache_dir(tema, edad), os.path.join(TEMAS, tema, "actividades_preview")):
        if os.path.isdir(d): shutil.rmtree(d)


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "monstruos"
    edad = sys.argv[2] if len(sys.argv) > 2 else "6"
    o, n = generar_cuaderno(tema, edad, "/root/.claude/jobs/2ed32d0f/tmp/act/out")
    print("OK", n, "páginas")
