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
    Lee ia_draft/ (nuevo) o extras/. Cachea en temas/<tema>/actividades_mon/c*.png."""
    cache = os.path.join(TEMAS, tema, "actividades_mon")
    if os.path.isdir(cache):
        ya = sorted(glob.glob(f"{cache}/c*.png"))
        if ya: return ya
    sheet = next((p for p in (os.path.join(TEMAS, tema, "ia_draft", "stickers_1.png"),
                              os.path.join(TEMAS, tema, "extras", "stickers_1.png"))
                  if os.path.isfile(p)), None)
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
    comb = ImageChops.lighter(edges_a, edges_g).point(lambda v: 255 if v > 38 else 0)
    comb = comb.filter(ImageFilter.MaxFilter(3))                     # engrosar el trazo
    return comb.point(lambda v: 0 if v > 0 else 255)                # líneas negras sobre blanco

def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))

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
def _header(dr, edad, nombre="Cumpleaños"):
    dr.rectangle([0, 0, Wp, 150], fill=NAVY)
    dr.text((60, 42), "Cuaderno de Actividades", font=_font(46), fill="white")
    dr.text((62, 100), "%s · %s años" % (nombre, edad), font=_font(26, False), fill=(200, 195, 225))
    dr.rounded_rectangle([Wp - 230, 40, Wp - 60, 110], 35, fill=VIOLET)
    dr.text((Wp - 145, 75), str(edad), font=_font(40), fill="white", anchor="mm")
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

def _portada(mons, edad, nombre="Cumpleaños"):
    im, dr = _page(); dr.rectangle([0, 0, Wp, Hp], fill=CREAM)
    dr.rounded_rectangle([55, 55, Wp - 55, Hp - 55], 40, outline=VIOLET, width=8)
    dr.text((Wp / 2, 290), "Cuaderno de", font=_font(70), fill=NAVY, anchor="mm")
    dr.text((Wp / 2, 390), "Actividades", font=_font(92), fill=VIOLET, anchor="mm")
    etiqueta = "%s · %s años" % (nombre, edad)
    ew = max(460, _font(40).getlength(etiqueta) + 80)
    dr.rounded_rectangle([Wp / 2 - ew / 2, 470, Wp / 2 + ew / 2, 560], 45, fill=COLS[1])
    dr.text((Wp / 2, 515), etiqueta, font=_font(40), fill="white", anchor="mm")
    pos = [(300, 820, 300), (950, 800, 300), (625, 1080, 360), (330, 1360, 300), (930, 1360, 300), (625, 1500, 240)]
    for (x, y, h), p in zip(pos, mons):
        _paste_h(im, Image.open(p).convert("RGBA"), x, y, h)
    _foot(dr); return im

def _sec(dr, y, n, titulo, instr):
    dr.text((60, y), "%d) %s" % (n, titulo), font=_font(34), fill=VIOLET); y += 48
    dr.text((60, y), instr, font=_font(24, False), fill=INK); return y + 44

def _arrow(dr, x0, y0, x1, y1, color=NAVY, w=8):
    dr.line([x0, y0, x1, y1], fill=color, width=w)
    ang = math.atan2(y1 - y0, x1 - x0); L = 26
    for a in (ang + 2.5, ang - 2.5):
        dr.line([x1, y1, x1 - L * math.cos(a), y1 - L * math.sin(a)], fill=color, width=w)

def _goal_torta(dr, cx, cy, s):
    for dx, col in ((-s * 0.95, COLS[1]), (s * 0.95, COLS[3])):       # globos a los lados
        dr.ellipse([cx + dx - s * 0.34, cy - s * 1.0, cx + dx + s * 0.34, cy - s * 0.2], fill=col)
        dr.line([cx + dx, cy - s * 0.2, cx + dx, cy + s * 0.25], fill=NAVY, width=3)
    _cake(dr, cx, cy, s)

def _draw_maze(im, dr, w, MW, MH, y, mons, sol=False):
    cell = 60; mx = (Wp - MW * cell) // 2; lw = 4
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
        _paste_h(im, Image.open(mons[3 % len(mons)]).convert("RGBA"), mx - 175, y + 150, 200)
        _arrow(dr, mx - 70, y + 115, mx - 6, y + cell / 2 + 4)
    gx = mx + MW * cell + 150; gy = y + (MH - 1) * cell + cell / 2    # meta (torta) en la salida + flecha
    _arrow(dr, mx + MW * cell + 8, gy, gx - 78, gy)
    _goal_torta(dr, gx, gy, 70)
    return y + MH * cell
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

def _draw_ws(dr, g, sol, y, mostrar_sol=False):
    """Sopa CENTRADA: la grilla centrada horizontal y la lista de palabras debajo."""
    N = len(g); gs = 50; gx = (Wp - N * gs) // 2; fg = _font(30)
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
    for row in range((len(PALABRAS) + per - 1) // per):
        grp = PALABRAS[row * per:(row + 1) * per]
        txt = "   ".join("• " + w.capitalize() for w in grp)
        dr.text((Wp / 2, yy), txt, font=fw, fill=INK, anchor="mm"); yy += 38
    return yy

# ───────────────────────── sombra ─────────────────────────
def _shadow(path):
    m = Image.open(path).convert("RGBA")
    s = Image.new("RGBA", m.size, (74, 68, 96, 255)); s.putalpha(m.split()[3]); return s

# ───────────────────────── builder con paginado automático ─────────────────────────
TOP = 180; BOT = Hp - 90

class _Book:
    def __init__(self, edad, mons, seed, nombre="Cumpleaños"):
        self.edad = edad; self.mons = mons; self.rnd = random.Random(seed); self.nombre = nombre
        self.pages = []; self.im = None; self.dr = None; self.y = 0; self.secn = 0; self.sol = {}
    def _flush(self):
        if self.im is not None: _foot(self.dr); self.pages.append(self.im)
    def _newpage(self):
        self._flush(); self.im, self.dr = _page(); _header(self.dr, self.edad, self.nombre); self.y = TOP
    def ensure(self, h):
        if self.im is None or self.y + h > BOT: self._newpage()
    def sec(self, titulo, instr, h):
        self.ensure(h + 100); self.secn += 1; self.y = _sec(self.dr, self.y, self.secn, titulo, instr)
    def mon(self, i):
        return self.mons[i % len(self.mons)] if self.mons else None
    def finish(self):
        self._flush()

def _IM(p): return Image.open(p).convert("RGBA")

# ───────────────────────── actividades ─────────────────────────
def _a_laberinto(b, n):
    for s in range(1, 60):
        w = _maze(n, n, s)
        if _maze_path(w, n, n): break
    assert _maze_path(w, n, n)
    b.sec("El laberinto del cumple", "¡Ayudá al personaje a llegar a la torta de cumpleaños!", n * 60 + 30)
    b.y = _draw_maze(b.im, b.dr, w, n, n, b.y, b.mons) + 30
    b.sol["maze"] = (w, n, n)

def _a_laberinto_circular(b, rings=4):
    S = 12; se = b.rnd.randrange(0, 6)                # salida en la mitad inferior (queda en página)
    RAD, CIRC, HUB = _theta_maze(rings, S, b.rnd, se)
    path = _theta_path(RAD, CIRC, HUB, rings, S, se)
    assert path                                       # laberinto perfecto → siempre hay salida
    R0 = 66; dt = 74; Rmax = R0 + rings * dt
    b.sec("Laberinto circular", "Salí desde el centro hasta afuera siguiendo los caminos.", 2 * Rmax + 150)
    cx = Wp / 2; cy = b.y + Rmax + 20
    _draw_theta(b.im, b.dr, RAD, CIRC, HUB, rings, S, se, cx, cy, R0, dt, b.mons)
    b.y = cy + Rmax + 70
    b.sol["cmaze"] = (RAD, CIRC, HUB, rings, S, se, path)

def _a_sopa(b):
    for s in range(5, 95):
        g, sol = _wordsearch(PALABRAS, 12, s)
        if g and all(_ws_has(g, x) for x in PALABRAS): break
    assert g and all(_ws_has(g, x) for x in PALABRAS)
    b.sec("Sopa de letras", "Encontrá las 8 palabras escondidas.", 12 * 50 + 170)
    b.y = _draw_ws(b.dr, g, sol, b.y) + 20
    b.sol["ws"] = (g, sol)

def _a_puntos(b, nd):
    b.sec("Uní los puntos", "Uní del 1 al %d y descubrí la figura." % nd, 460)
    cx, cy, R = Wp / 2, b.y + 205, 190
    for i, (px, py) in enumerate(_star_pts(cx, cy, R)[:nd]):
        b.dr.ellipse([px - 9, py - 9, px + 9, py + 9], fill=NAVY)
        b.dr.text((px + 14, py - 16), str(i + 1), font=_font(28), fill=COLS[i % len(COLS)])
    b.y = cy + R + 30

def _a_contar(b, na, nb):
    b.sec("Contá", "¿Cuántos hay de cada uno? Escribí el número.", 430)
    y = b.y; b.dr.rounded_rectangle([60, y, Wp - 60, y + 250], 20, outline=(220, 215, 225), width=3)
    spots = []
    def free():
        for _ in range(400):
            x = b.rnd.randint(150, Wp - 160); yy = b.rnd.randint(y + 55, y + 205)
            if all((x - a) ** 2 + (yy - c) ** 2 > 150 ** 2 for a, c in spots): spots.append((x, yy)); return x, yy
        return b.rnd.randint(150, Wp - 160), b.rnd.randint(y + 55, y + 205)
    mA, mB = b.mon(1), b.mon(5)
    for _ in range(na):
        x, yy = free();  (mA and _paste_h(b.im, _IM(mA), x, yy, 105))
    for _ in range(nb):
        x, yy = free();  (mB and _paste_h(b.im, _IM(mB), x, yy, 105))
    yb = y + 300
    if mA: _paste_h(b.im, _IM(mA), 130, yb, 85)
    b.dr.text((190, yb), "Amarillos:", font=_font(30), fill=INK, anchor="lm")
    b.dr.rounded_rectangle([470, yb - 30, 535, yb + 30], 8, outline=NAVY, width=3)
    if mB: _paste_h(b.im, _IM(mB), 130, yb + 90, 85)
    b.dr.text((190, yb + 90), "Rojos:", font=_font(30), fill=INK, anchor="lm")
    b.dr.rounded_rectangle([470, yb + 60, 535, yb + 120], 8, outline=NAVY, width=3)
    b.y = yb + 150; b.sol["count"] = (na, nb)

def _a_sombra(b, k):
    if not b.mons: return
    b.sec("Uní con su sombra", "Uní cada personaje con su sombra.", k * 150 + 20)
    idx = list(range(min(len(b.mons), 7))); b.rnd.shuffle(idx); idx = idx[:k]
    right = idx[:]; b.rnd.shuffle(right)
    y0 = b.y + 20; step = 150; lx = 330; rx = Wp - 330
    for row, i in enumerate(idx):
        yy = y0 + row * step
        _paste_h(b.im, _IM(b.mons[i]), lx, yy, 120)
        b.dr.ellipse([lx + 132, yy - 8, lx + 148, yy + 8], fill=NAVY)
    for row, i in enumerate(right):
        yy = y0 + row * step
        _paste_h(b.im, _shadow(b.mons[i]), rx, yy, 120)
        b.dr.ellipse([rx - 148, yy - 8, rx - 132, yy + 8], fill=NAVY)
    b.y = y0 + k * step + 10

def _a_diferente(b, rows):
    if not b.mons: return
    b.sec("¿Cuál es diferente?", "Marcá con un círculo el que no es igual.", rows * 135 + 20)
    pool = list(range(min(len(b.mons), 7)))
    for r in range(rows):
        base, diff = b.rnd.sample(pool, 2); m = 5; odd = b.rnd.randrange(m)
        yy = b.y + r * 135 + 55
        for c in range(m):
            _paste_h(b.im, _IM(b.mons[diff if c == odd else base]), 180 + c * 190, yy, 105)
    b.y = b.y + rows * 135 + 20

def _a_patron(b, rows):
    if not b.mons: return
    b.sec("Continuá el patrón", "Pintá o dibujá el que sigue en cada fila.", rows * 140 + 20)
    pool = list(range(min(len(b.mons), 7)))
    for r in range(rows):
        pat = b.rnd.sample(pool, b.rnd.choice([2, 2, 3])); yy = b.y + r * 140 + 60; total = 6
        for c in range(total):
            x = 160 + c * 165
            if c < total - 2:
                _paste_h(b.im, _IM(b.mons[pat[c % len(pat)]]), x, yy, 100)
            else:
                b.dr.rounded_rectangle([x - 52, yy - 52, x + 52, yy + 52], 12, outline=NAVY, width=3)
    b.y = b.y + rows * 140 + 20

def _a_sumas(b, rows):
    if not b.mons: return
    b.sec("Sumas con personajes", "Contá y escribí el resultado.", rows * 150 + 20)
    res = []
    for r in range(rows):
        a = b.rnd.randint(1, 4); bb = b.rnd.randint(1, 4); yy = b.y + r * 150 + 65; x = 110
        for _ in range(a): _paste_h(b.im, _IM(b.mon(1)), x, yy, 70); x += 74
        b.dr.text((x + 6, yy), "+", font=_font(48), fill=INK, anchor="lm"); x += 66
        for _ in range(bb): _paste_h(b.im, _IM(b.mon(5)), x, yy, 70); x += 74
        b.dr.text((x + 6, yy), "=", font=_font(48), fill=INK, anchor="lm"); x += 66
        b.dr.rounded_rectangle([x, yy - 42, x + 84, yy + 42], 10, outline=NAVY, width=3)
        res.append(a + bb)
    b.y = b.y + rows * 150 + 20; b.sol["sumas"] = res

def _a_sudoku(b):
    """Sudoku 4×4 de figuras: cada fila/columna/cuadro lleva un monstruo de cada tipo.
    Solución única garantizada (se verifica por conteo). El chico escribe el número."""
    if not b.mons or len(b.mons) < 4: return
    sol, puz = _sudoku_make(b.rnd)
    imgs = [_IM(b.mons[i]) for i in range(4)]
    b.sec("Sudoku de personajes", "Cada figura es un número. Completá los casilleros vacíos: en cada fila, columna y cuadro va uno de cada.", 1010)
    # leyenda figura = número
    ly = b.y; lx = 90
    for i in range(4):
        _paste_h(b.im, imgs[i], lx, ly + 42, 80)
        b.dr.text((lx + 52, ly + 42), "= %d" % (i + 1), font=_font(34), fill=INK, anchor="lm")
        lx += 270
    # grilla 4×4
    cell = 150; gx = (Wp - 4 * cell) // 2; gy = ly + 120
    for r in range(4):
        for c in range(4):
            x0, y0 = gx + c * cell, gy + r * cell
            b.dr.rectangle([x0, y0, x0 + cell, y0 + cell], outline=(150, 145, 160), width=2)
            if puz[r][c] is not None:
                _paste_h(b.im, imgs[puz[r][c]], x0 + cell / 2, y0 + cell / 2, cell - 36)
    for k in range(0, 5, 2):                          # líneas gruesas de los cuadros 2×2
        b.dr.line([gx + k * cell, gy, gx + k * cell, gy + 4 * cell], fill=NAVY, width=6)
        b.dr.line([gx, gy + k * cell, gx + 4 * cell, gy + k * cell], fill=NAVY, width=6)
    b.y = gy + 4 * cell + 30
    b.sol["sudoku"] = (sol, [b.mons[i] for i in range(4)])

def _a_buscar(b, n):
    """Encontrá los escondidos (iSpy): escena con muchos personajes; buscar X de cada
    tipo. Aprovecha los stickers recortados del tema. Verificable: contamos lo puesto."""
    if not b.mons: return
    b.sec("Encontrá los escondidos", "Buscá en el dibujo y marcá con un círculo:", 600)
    pool = list(range(min(len(b.mons), 7))); imgs = [_IM(b.mons[i]) for i in pool]
    y0 = b.y; boxh = 470
    b.dr.rounded_rectangle([60, y0, Wp - 60, y0 + boxh], 18, fill=(250, 248, 244), outline=(220, 215, 225), width=3)
    placed = {}; spots = []
    for _ in range(n):
        ti = b.rnd.randrange(len(pool)); sz = b.rnd.randint(78, 118)
        x = y = 0
        for _t in range(40):
            x = b.rnd.randint(110, Wp - 110); y = b.rnd.randint(y0 + 50, y0 + boxh - 50)
            if all((x - a) ** 2 + (y - c) ** 2 > 62 ** 2 for a, c in spots): break
        spots.append((x, y))
        m = imgs[ti].rotate(b.rnd.randint(-22, 22), expand=True, resample=Image.BICUBIC)
        _paste_h(b.im, m, x, y, sz); placed[ti] = placed.get(ti, 0) + 1
    targets = [t for t in placed if placed[t] >= 2][:3] or list(placed.keys())[:2]
    b.y = y0 + boxh + 18; tx = 110
    for t in targets:
        _paste_h(b.im, imgs[t], tx + 42, b.y + 38, 80)
        b.dr.text((tx + 92, b.y + 38), "× %d" % placed[t], font=_font(36), fill=INK, anchor="lm")
        tx += 250
    b.y += 110
    b.sol["buscar"] = [placed[t] for t in targets]

def _colorear_img(tema):
    """Página para colorear DIBUJADA por OpenAI (aprobada en extras/ o aún en ia_draft/).
    Aplica un umbral idempotente como garantía de B/N. Devuelve None si el tema todavía no
    tiene una generada -> el cuaderno cae al line art derivado del personaje (fallback)."""
    p = next((q for q in (os.path.join(TEMAS, tema, "extras", "colorear.png"),
                          os.path.join(TEMAS, tema, "ia_draft", "colorear.png"))
              if os.path.isfile(q)), None)
    if not p:
        return None
    im = Image.open(p).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    return bg.convert("L").point(lambda v: 0 if v < 165 else 255).convert("RGBA")

def _a_colorear(b, tema):
    b.ensure(1040); b.sec("Pintá el dibujo", "Coloreá como más te guste.", 60)
    la = _colorear_img(tema)                  # 1º: la página dibujada por OpenAI (la que te gusta)
    if la is None and b.mons:                 # fallback: line art del personaje MÁS ALTO (no un manchón ancho)
        src = max(b.mons, key=lambda p: Image.open(p).size[1])
        la = _lineart(src).convert("RGBA")
    if la is not None:
        h = 980; w = int(la.width * h / la.height)
        if w > Wp - 160:                      # clamp por si la pieza es muy ancha
            w = Wp - 160; h = int(la.height * w / la.width)
        la = la.resize((w, h), Image.LANCZOS)
        b.im.alpha_composite(la, (int(Wp / 2 - w / 2), b.y + 10))
    b.y = BOT

def _solucionario(b):
    if not any(k in b.sol for k in ("maze", "cmaze", "ws", "sumas", "sudoku")): return
    pages = []
    im, dr = _page(); _header(dr, b.edad, b.nombre)
    dr.text((60, 200), "Solucionario", font=_font(40), fill=COLS[0]); y = 280
    def newpage():
        nonlocal im, dr, y
        _foot(dr); pages.append(im); im, dr = _page(); _header(dr, b.edad, b.nombre); y = 220
    def need(h):
        if y + h > BOT: newpage()
    if "maze" in b.sol:
        w, MW, MH = b.sol["maze"]; need(MH * 60 + 70)
        dr.text((60, y), "Laberinto:", font=_font(28), fill=VIOLET); y += 44
        y = _draw_maze(im, dr, w, MW, MH, y, b.mons, sol=True) + 36
    if "cmaze" in b.sol:
        RAD, CIRC, HUB, rings, S, se, path = b.sol["cmaze"]
        R0 = 40; dt = 46; Rmax = R0 + rings * dt; need(2 * Rmax + 80)
        dr.text((60, y), "Laberinto circular:", font=_font(28), fill=VIOLET); y += 50
        cx = Wp / 2; cy = y + Rmax
        _draw_theta(im, dr, RAD, CIRC, HUB, rings, S, se, cx, cy, R0, dt, b.mons, sol=True, path=path)
        y = cy + Rmax + 36
    if "ws" in b.sol:
        g, sol = b.sol["ws"]; need(len(g) * 50 + 90)
        dr.text((60, y), "Sopa de letras:", font=_font(28), fill=VIOLET); y += 44
        y = _draw_ws(dr, g, sol, y, mostrar_sol=True) + 20
    if "sudoku" in b.sol:
        sgrid, _mp = b.sol["sudoku"]; cell = 80; need(4 * cell + 80)
        dr.text((60, y), "Sudoku (números):", font=_font(28), fill=VIOLET); y += 50
        gx = (Wp - 4 * cell) // 2
        for r in range(4):
            for c in range(4):
                x0, y0 = gx + c * cell, y + r * cell
                dr.rectangle([x0, y0, x0 + cell, y0 + cell], outline=(150, 145, 160), width=2)
                dr.text((x0 + cell / 2, y0 + cell / 2), str(sgrid[r][c] + 1), font=_font(40), fill=NAVY, anchor="mm")
        for k in range(0, 5, 2):
            dr.line([gx + k * cell, y, gx + k * cell, y + 4 * cell], fill=NAVY, width=5)
            dr.line([gx, y + k * cell, gx + 4 * cell, y + k * cell], fill=NAVY, width=5)
        y += 4 * cell + 30
    lines = []
    if "count" in b.sol: lines.append("Contar — Amarillos: %d · Rojos: %d" % b.sol["count"])
    if "sumas" in b.sol: lines.append("Sumas: " + ", ".join(str(x) for x in b.sol["sumas"]))
    lines.append("(Sombra, ¿cuál es diferente? y patrón se revisan a simple vista.)")
    need(34 * len(lines) + 40)
    for ln in lines:
        dr.text((60, y), ln, font=_font(23), fill=INK); y += 34
    _foot(dr); pages.append(im); b.pages.extend(pages)

# ───────────────────────── plan por edad ─────────────────────────
def _plan(edad):
    e = int(edad) if str(edad).isdigit() else 6
    if e <= 3: return dict(maze=0, cmaze=0, sopa=False, dots=6, count=(3, 2), sombra=3, diferente=2, patron=0, sumas=0, sudoku=False, buscar=10)
    if e <= 5: return dict(maze=7, cmaze=0, sopa=False, dots=8, count=(5, 3), sombra=4, diferente=3, patron=3, sumas=0, sudoku=False, buscar=14)
    return dict(maze=9, cmaze=4, sopa=True, dots=10, count=(5, 3), sombra=4, diferente=3, patron=3, sumas=3, sudoku=True, buscar=18)

# ───────────────────────── armado ─────────────────────────
def paginas(tema, edad, seed=1, con_solucionario=True):
    """Devuelve la lista de páginas (PIL.Image) del cuaderno, ya verificadas.
    Es lo que consume el motor del kit para empaquetar el ZIP del producto."""
    mons = _extraer_monstruos(tema); plan = _plan(edad); nombre = _tema_nombre(tema)
    b = _Book(edad, mons, seed, nombre)
    b.pages.append(_portada(mons, edad, nombre))
    if plan["maze"]: _a_laberinto(b, plan["maze"])
    if plan.get("cmaze"): _a_laberinto_circular(b, plan["cmaze"])
    if plan["sopa"]: _a_sopa(b)
    _a_puntos(b, plan["dots"])
    _a_contar(b, *plan["count"])
    if plan.get("buscar"): _a_buscar(b, plan["buscar"])
    if plan["sombra"]: _a_sombra(b, plan["sombra"])
    if plan["diferente"]: _a_diferente(b, plan["diferente"])
    if plan["patron"]: _a_patron(b, plan["patron"])
    if plan["sumas"]: _a_sumas(b, plan["sumas"])
    if plan.get("sudoku"): _a_sudoku(b)
    _a_colorear(b, tema)
    b.finish()
    if con_solucionario:
        _solucionario(b)
    return b.pages

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
        rgb[0].save(pdf, save_all=True, append_images=rgb[1:]); out = pdf
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
    pgs = [p.convert("RGB") for p in paginas(tema, str(edad), seed)]
    os.makedirs(cd, exist_ok=True)
    for i, p in enumerate(pgs):
        p.save(os.path.join(cd, "b%02d.png" % i))
    return pgs

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
    plan = _plan(edad); tiene_sol = bool(plan["maze"] or plan["sopa"])
    out = []
    for i in range(len(base)):
        if tiene_sol and i == len(base) - 1:           # última = solucionario → no mostrar
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
