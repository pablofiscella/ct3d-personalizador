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
import os, math, random, glob
from collections import deque
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
NAVY = (29, 25, 79); VIOLET = (107, 91, 210); INK = (40, 38, 55); CREAM = (246, 242, 236)
COLS = [(224, 85, 107), (63, 167, 214), (232, 155, 44), (95, 184, 122), (139, 91, 210), (38, 140, 90)]
PALABRAS = ["MONSTRUO", "FIESTA", "GLOBO", "TORTA", "REGALO", "JUGAR", "DULCE", "AMIGOS"]

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
    """Recorta los monstruos individuales de temas/<tema>/extras/stickers_1.png
    (los separa por color, ya que los halos blancos se tocan). Cachea en
    temas/<tema>/actividades_mon/c*.png. Devuelve lista de paths (vacía si no hay)."""
    cache = os.path.join(TEMAS, tema, "actividades_mon")
    if os.path.isdir(cache):
        ya = sorted(glob.glob(f"{cache}/c*.png"))
        if ya: return ya
    sheet = os.path.join(TEMAS, tema, "extras", "stickers_1.png")
    if not os.path.isfile(sheet):
        return []
    im = Image.open(sheet).convert("RGBA"); W, H = im.size
    rgb = im.convert("RGB").load()
    lab = [[0] * H for _ in range(W)]; comps = []; cur = 0
    sat = lambda x, y: (lambda r, g, b: max(r, g, b) - min(r, g, b))(*rgb[x, y]) > 45
    for x in range(W):
        for y in range(H):
            if sat(x, y) and not lab[x][y]:
                cur += 1; q = deque([(x, y)]); lab[x][y] = cur
                mnx = mxx = x; mny = mxy = y; n = 0
                while q:
                    cx, cy = q.popleft(); n += 1
                    mnx = min(mnx, cx); mxx = max(mxx, cx); mny = min(mny, cy); mxy = max(mxy, cy)
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < W and 0 <= ny < H and not lab[nx][ny] and sat(nx, ny):
                                lab[nx][ny] = cur; q.append((nx, ny))
                if n > 2500: comps.append((mnx, mny, mxx, mxy, cur))
    comps.sort(key=lambda c: (round(c[1] / 120), c[0]))
    os.makedirs(cache, exist_ok=True); out = []
    for i, (x0, y0, x1, y1, cid) in enumerate(comps):
        bm = Image.new("L", (W, H), 0); bp = bm.load()
        for x in range(max(0, x0 - 30), min(W, x1 + 30)):
            for y in range(max(0, y0 - 30), min(H, y1 + 30)):
                if lab[x][y] == cid: bp[x, y] = 255
        bm = bm.filter(ImageFilter.MaxFilter(29)).filter(ImageFilter.GaussianBlur(2))  # incluir borde blanco
        cut = im.copy(); cut.putalpha(bm)
        c = cut.crop((max(0, x0 - 30), max(0, y0 - 30), min(W, x1 + 30), min(H, y1 + 30)))
        p = f"{cache}/c{i}.png"; c.save(p); out.append(p)
    return out

def _lineart(path, thr=75):
    """Monstruo → line-art cerrado para colorear (umbral + engrose leve que cierra
    los contornos abiertos de arriba)."""
    s = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", s.size, (255, 255, 255, 255)); bg.alpha_composite(s)
    la = bg.convert("L").point(lambda v: 0 if v < thr else 255)
    return la.filter(ImageFilter.MinFilter(3))

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
def _header(dr, edad):
    dr.rectangle([0, 0, Wp, 150], fill=NAVY)
    dr.text((60, 42), "Cuaderno de Actividades", font=_font(46), fill="white")
    dr.text((62, 100), "Monstruos · %s años" % edad, font=_font(26, False), fill=(200, 195, 225))
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

def _portada(mons, edad):
    im, dr = _page(); dr.rectangle([0, 0, Wp, Hp], fill=CREAM)
    dr.rounded_rectangle([55, 55, Wp - 55, Hp - 55], 40, outline=VIOLET, width=8)
    dr.text((Wp / 2, 290), "Cuaderno de", font=_font(70), fill=NAVY, anchor="mm")
    dr.text((Wp / 2, 390), "Actividades", font=_font(92), fill=VIOLET, anchor="mm")
    dr.rounded_rectangle([Wp / 2 - 230, 470, Wp / 2 + 230, 560], 45, fill=COLS[1])
    dr.text((Wp / 2, 515), "Monstruos · %s años" % edad, font=_font(40), fill="white", anchor="mm")
    pos = [(300, 820, 300), (950, 800, 300), (625, 1080, 360), (330, 1360, 300), (930, 1360, 300), (625, 1500, 240)]
    for (x, y, h), p in zip(pos, mons):
        _paste_h(im, Image.open(p).convert("RGBA"), x, y, h)
    _foot(dr); return im

def _sec(dr, y, n, titulo, instr):
    dr.text((60, y), "%d) %s" % (n, titulo), font=_font(34), fill=VIOLET); y += 48
    dr.text((60, y), instr, font=_font(24, False), fill=INK); return y + 44

def _draw_maze(im, dr, w, MW, MH, y, mons, sol=False):
    cell = 60; mx = (Wp - MW * cell) // 2; lw = 4
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
    if mons: _paste_h(im, Image.open(mons[3 % len(mons)]).convert("RGBA"), mx + cell / 2, y + cell / 2, cell * 1.5)
    ex, ey = mx + (MW - 1) * cell, y + (MH - 1) * cell
    _cake(dr, ex + cell / 2, ey + cell / 2, cell * 0.5)
    return y + MH * cell

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
    def __init__(self, edad, mons, seed):
        self.edad = edad; self.mons = mons; self.rnd = random.Random(seed)
        self.pages = []; self.im = None; self.dr = None; self.y = 0; self.secn = 0; self.sol = {}
    def _flush(self):
        if self.im is not None: _foot(self.dr); self.pages.append(self.im)
    def _newpage(self):
        self._flush(); self.im, self.dr = _page(); _header(self.dr, self.edad); self.y = TOP
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
    b.sec("El laberinto", "Ayudá al monstruo a llegar a la torta.", n * 60 + 20)
    b.y = _draw_maze(b.im, b.dr, w, n, n, b.y, b.mons) + 30
    b.sol["maze"] = (w, n, n)

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
    b.sec("Uní con su sombra", "Uní cada monstruo con su sombra.", k * 150 + 20)
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
    b.sec("Sumas con monstruos", "Contá y escribí el resultado.", rows * 150 + 20)
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

def _a_colorear(b):
    b.ensure(1040); b.sec("Pintá el monstruo", "Coloreá como más te guste.", 60)
    if b.mons:
        la = _lineart(b.mon(3)).convert("RGBA"); h = 900; w = int(la.width * h / la.height)
        la = la.resize((w, h), Image.LANCZOS); b.im.alpha_composite(la, (int(Wp / 2 - w / 2), b.y + 10))
    b.y = BOT

def _solucionario(b):
    if not any(k in b.sol for k in ("maze", "ws", "sumas")): return
    im, dr = _page(); _header(dr, b.edad)
    dr.text((60, 200), "Solucionario", font=_font(40), fill=COLS[0]); y = 280
    if "maze" in b.sol:
        w, MW, MH = b.sol["maze"]; dr.text((60, y), "Laberinto:", font=_font(28), fill=VIOLET); y += 44
        y = _draw_maze(im, dr, w, MW, MH, y, b.mons, sol=True) + 36
    if "ws" in b.sol:
        g, sol = b.sol["ws"]; dr.text((60, y), "Sopa de letras:", font=_font(28), fill=VIOLET); y += 44
        y = _draw_ws(dr, g, sol, y, mostrar_sol=True) + 20
    lines = []
    if "count" in b.sol: lines.append("Contar — Amarillos: %d · Rojos: %d" % b.sol["count"])
    if "sumas" in b.sol: lines.append("Sumas: " + ", ".join(str(x) for x in b.sol["sumas"]))
    lines.append("(Sombra, ¿cuál es diferente? y patrón se revisan a simple vista.)")
    yy = Hp - 70 - 34 * len(lines)
    for ln in lines:
        dr.text((60, yy), ln, font=_font(23), fill=INK); yy += 34
    _foot(dr); b.pages.append(im)

# ───────────────────────── plan por edad ─────────────────────────
def _plan(edad):
    e = int(edad) if str(edad).isdigit() else 6
    if e <= 3: return dict(maze=0, sopa=False, dots=6, count=(3, 2), sombra=3, diferente=2, patron=0, sumas=0)
    if e <= 5: return dict(maze=7, sopa=False, dots=8, count=(5, 3), sombra=4, diferente=3, patron=3, sumas=0)
    return dict(maze=9, sopa=True, dots=10, count=(5, 3), sombra=4, diferente=3, patron=3, sumas=3)

# ───────────────────────── armado ─────────────────────────
def paginas(tema, edad, seed=1):
    """Devuelve la lista de páginas (PIL.Image) del cuaderno, ya verificadas.
    Es lo que consume el motor del kit para empaquetar el ZIP del producto."""
    mons = _extraer_monstruos(tema); plan = _plan(edad)
    b = _Book(edad, mons, seed)
    b.pages.append(_portada(mons, edad))
    if plan["maze"]: _a_laberinto(b, plan["maze"])
    if plan["sopa"]: _a_sopa(b)
    _a_puntos(b, plan["dots"])
    _a_contar(b, *plan["count"])
    if plan["sombra"]: _a_sombra(b, plan["sombra"])
    if plan["diferente"]: _a_diferente(b, plan["diferente"])
    if plan["patron"]: _a_patron(b, plan["patron"])
    if plan["sumas"]: _a_sumas(b, plan["sumas"])
    _a_colorear(b)
    b.finish()
    _solucionario(b)
    return b.pages

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


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "monstruos"
    edad = sys.argv[2] if len(sys.argv) > 2 else "6"
    o, n = generar_cuaderno(tema, edad, "/root/.claude/jobs/2ed32d0f/tmp/act/out")
    print("OK", n, "páginas")
