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

# ───────────────────────── plan por edad ─────────────────────────
def _plan(edad):
    e = int(edad) if str(edad).isdigit() else 6
    if e <= 3:  return {"maze": 0, "sopa": False, "dots": 6, "count": (3, 2)}
    if e <= 5:  return {"maze": 7, "sopa": False, "dots": 8, "count": (5, 3)}
    return {"maze": 9, "sopa": True, "dots": 10, "count": (5, 3)}

# ───────────────────────── armado ─────────────────────────
def generar_cuaderno(tema, edad, out_dir, seed=1):
    os.makedirs(out_dir, exist_ok=True)
    mons = _extraer_monstruos(tema)
    plan = _plan(edad)
    pages = [_portada(mons, edad)]
    sol_items = {}   # para el solucionario

    # — página de laberinto (+ sopa si corresponde) —
    if plan["maze"]:
        im, dr = _page(); _header(dr, edad)
        MW = MH = plan["maze"]
        for s in range(seed, seed + 60):
            w = _maze(MW, MH, s)
            if _maze_path(w, MW, MH): break
        assert _maze_path(w, MW, MH), "laberinto sin solución"
        y = _sec(dr, 200, 1, "El laberinto", "Ayudá al monstruo a llegar a la torta.")
        y = _draw_maze(im, dr, w, MW, MH, y, mons) + 50
        if plan["sopa"]:
            for s in range(seed + 5, seed + 90):
                g, sol = _wordsearch(PALABRAS, 12, s)
                if g and all(_ws_has(g, x) for x in PALABRAS): break
            assert g and all(_ws_has(g, x) for x in PALABRAS), "sopa incompleta"
            y = _sec(dr, y, 2, "Sopa de letras", "Encontrá las 8 palabras escondidas.")
            _draw_ws(dr, g, sol, y)
            sol_items["maze"] = (w, MW, MH); sol_items["ws"] = (g, sol)
        else:
            sol_items["maze"] = (w, MW, MH)
        _foot(dr); pages.append(im)

    # — página unir puntos + contar —
    im, dr = _page(); _header(dr, edad)
    nd = plan["dots"]
    y = _sec(dr, 200, 3, "Uní los puntos", "Uní del 1 al %d y descubrí la figura." % nd)
    cx, cy, R = Wp / 2, y + 240, 210
    pts = _star_pts(cx, cy, R)[:nd]
    for i, (px, py) in enumerate(pts):
        dr.ellipse([px - 9, py - 9, px + 9, py + 9], fill=NAVY)
        dr.text((px + 14, py - 16), str(i + 1), font=_font(28), fill=COLS[i % len(COLS)])
    y = cy + R + 50
    na, nb = plan["count"]
    y = _sec(dr, y, 4, "Contá", "¿Cuántos hay de cada uno? Escribí el número.") + 16
    dr.rounded_rectangle([60, y, Wp - 60, y + 300], 20, outline=(220, 215, 225), width=3)
    rnd = random.Random(seed + 3); spots = []
    def free():
        for _ in range(400):
            x = rnd.randint(150, Wp - 160); yy = rnd.randint(y + 70, y + 250)
            if all((x - a) ** 2 + (yy - b) ** 2 > 165 ** 2 for a, b in spots): spots.append((x, yy)); return x, yy
        return rnd.randint(150, Wp - 160), rnd.randint(y + 70, y + 250)
    mA = mons[1 % len(mons)] if mons else None; mB = mons[5 % len(mons)] if mons else None
    for _ in range(na):
        x, yy = free()
        if mA: _paste_h(im, Image.open(mA).convert("RGBA"), x, yy, 115)
    for _ in range(nb):
        x, yy = free()
        if mB: _paste_h(im, Image.open(mB).convert("RGBA"), x, yy, 115)
    yb = y + 360
    if mA: _paste_h(im, Image.open(mA).convert("RGBA"), 130, yb, 95)
    dr.text((195, yb), "Amarillos:", font=_font(30), fill=INK, anchor="lm")
    dr.rounded_rectangle([470, yb - 32, 540, yb + 32], 8, outline=NAVY, width=3)
    if mB: _paste_h(im, Image.open(mB).convert("RGBA"), 130, yb + 95, 95)
    dr.text((195, yb + 95), "Rojos:", font=_font(30), fill=INK, anchor="lm")
    dr.rounded_rectangle([470, yb + 63, 540, yb + 127], 8, outline=NAVY, width=3)
    sol_items["count"] = (na, nb)
    _foot(dr); pages.append(im)

    # — página colorear —
    im, dr = _page(); _header(dr, edad)
    _sec(dr, 200, 5, "Pintá el monstruo", "Coloreá como más te guste.")
    if mons:
        la = _lineart(mons[3 % len(mons)]).convert("RGBA")
        h = 950; w = int(la.width * h / la.height); la = la.resize((w, h), Image.LANCZOS)
        im.alpha_composite(la, (int(Wp / 2 - w / 2), 360))
    _foot(dr); pages.append(im)

    # — solucionario —
    im, dr = _page(); _header(dr, edad)
    dr.text((60, 200), "Solucionario", font=_font(40), fill=COLS[0])
    y = 280
    if "maze" in sol_items:
        w, MW, MH = sol_items["maze"]
        dr.text((60, y), "Laberinto:", font=_font(28), fill=VIOLET); y += 44
        y = _draw_maze(im, dr, w, MW, MH, y, mons, sol=True) + 40
    if "ws" in sol_items:
        g, sol = sol_items["ws"]
        dr.text((60, y), "Sopa de letras:", font=_font(28), fill=VIOLET); y += 44
        _draw_ws(dr, g, sol, y, mostrar_sol=True)
    na, nb = sol_items["count"]
    dr.text((60, Hp - 140), "Contar — Amarillos: %d   Rojos: %d" % (na, nb), font=_font(26), fill=INK)
    _foot(dr); pages.append(im)

    rgb = [p.convert("RGB") for p in pages]
    # PNGs (siempre; es lo que entrega el motor del kit en el ZIP)
    paths = []
    for i, p in enumerate(rgb):
        pp = os.path.join(out_dir, f"pg{i}.png"); p.save(pp); paths.append(pp)
    # PDF opcional (depende de que el PIL tenga JPEG)
    out = paths
    try:
        pdf = os.path.join(out_dir, f"cuaderno_{tema}_{edad}.pdf")
        rgb[0].save(pdf, save_all=True, append_images=rgb[1:]); out = pdf
    except Exception as e:
        out = paths
    return out, len(pages)


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "monstruos"
    edad = sys.argv[2] if len(sys.argv) > 2 else "6"
    pdf, n = generar_cuaderno(tema, edad, "/root/.claude/jobs/2ed32d0f/tmp/act/out")
    print("OK", pdf, n, "páginas")
