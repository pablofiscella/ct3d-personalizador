"""Kit de Baby Shower imprimible — 6 piezas personalizadas, 4 sub-temáticas pastel.

Igual que cuaderno.py / rutina.py: 100% procedural con Pillow, sin assets externos.
Tiene su propio set de sub-temáticas (nubes, osito, arcoíris, safari bebé) definidas
en código (paleta + motivos dibujados). Si más adelante hay arte real, se puede
swappear por el sistema de extras/ del kit.

Piezas (las 6 del spec): invitación · juego "No digas bebé" · predicciones de los
invitados · etiquetas souvenir · banderines · tarjeta para abrir a los 18.

API:
    pieza(key, data, tema) -> PIL.Image    (tema = sub-temática)
    PIEZAS  -> [(key, label), ...]
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
FONTDIR = os.path.join(KIT, "fonts")
Wp, Hp = 1240, 1754


def _f(fname, sz, wght=None):
    f = ImageFont.truetype(os.path.join(FONTDIR, fname), sz)
    if wght is not None:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f

def _script(sz):  return _f("Pacifico-Regular.ttf", sz)
def _hand(sz):    return _f("DancingScript-VF.ttf", sz, 700)
def _body(sz, bold=False): return _f("Poppins-SemiBold.ttf" if bold else "Poppins-Regular.ttf", sz)


def _tint(c, p):
    """p>0 mezcla hacia blanco; p<0 hacia negro."""
    if p >= 0: return tuple(int(v + (255 - v) * p) for v in c[:3])
    return tuple(int(v * (1 + p)) for v in c[:3])


# ───────────────────────────── sub-temáticas ─────────────────────────────
SUBTEMAS = {
    "nubes": dict(
        nombre="Nubes y Estrellas", bg=(234, 244, 251), frame=(159, 200, 234),
        c1=(125, 185, 246), c2=(247, 215, 116), c3=(246, 166, 193), ink=(66, 80, 110),
        motifs=["cloud", "star", "dot", "moon"]),
    "osito": dict(
        nombre="Osito del Bosque", bg=(241, 239, 227), frame=(195, 176, 145),
        c1=(176, 137, 104), c2=(169, 196, 127), c3=(232, 200, 160), ink=(91, 74, 58),
        motifs=["bear", "leaf", "dot", "star"]),
    "arcoiris": dict(
        nombre="Arcoíris", bg=(255, 247, 241), frame=(243, 185, 198),
        c1=(246, 132, 155), c2=(125, 192, 232), c3=(247, 200, 115), ink=(90, 74, 92),
        motifs=["rainbow", "cloud", "heart", "dot"]),
    "safari_bebe": dict(
        nombre="Safari Bebé", bg=(251, 244, 226), frame=(217, 192, 138),
        c1=(224, 168, 92), c2=(143, 179, 107), c3=(201, 138, 94), ink=(90, 75, 51),
        motifs=["sun", "paw", "leaf", "dot"]),
}
ORDEN = ["nubes", "osito", "arcoiris", "safari_bebe"]

def _sub(tema):
    return SUBTEMAS.get((tema or "").lower().replace("-", "_"), SUBTEMAS["nubes"])


# ───────────────────────────── motivos (Pillow) ─────────────────────────────
def _m_star(dr, im, s, cx, cy, r, col):
    pts = [(cx + (r if i % 2 == 0 else r * .45) * math.cos(-math.pi / 2 + i * math.pi / 5),
            cy + (r if i % 2 == 0 else r * .45) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
    dr.polygon(pts, fill=col)

def _m_dot(dr, im, s, cx, cy, r, col):
    dr.ellipse([cx - r * .5, cy - r * .5, cx + r * .5, cy + r * .5], fill=col)

def _m_cloud(dr, im, s, cx, cy, r, col):
    dr.ellipse([cx - r, cy - r * .35, cx + r, cy + r * .5], fill=col)
    dr.ellipse([cx - r * .7, cy - r * .8, cx + r * .05, cy + r * .2], fill=col)
    dr.ellipse([cx - r * .1, cy - r, cx + r * .75, cy + r * .15], fill=col)

def _m_heart(dr, im, s, cx, cy, r, col):
    dr.ellipse([cx - r, cy - r * .7, cx, cy + r * .15], fill=col)
    dr.ellipse([cx, cy - r * .7, cx + r, cy + r * .15], fill=col)
    dr.polygon([(cx - r * .92, cy - r * .12), (cx + r * .92, cy - r * .12), (cx, cy + r)], fill=col)

def _m_rainbow(dr, im, s, cx, cy, r, col):
    cols = [s["c1"], s["c3"], s["c2"], _tint(s["c1"], .35)]
    for i, c in enumerate(cols):
        rr = r - i * (r * .19)
        dr.arc([cx - rr, cy - rr, cx + rr, cy + rr], 180, 360, fill=c, width=max(5, int(r * .15)))

def _m_moon(dr, im, s, cx, cy, r, col):
    dr.ellipse([cx - r * .55, cy - r * .55, cx + r * .55, cy + r * .55], fill=col)
    dr.ellipse([cx - r * .15, cy - r * .68, cx + r * .75, cy + r * .42], fill=s["bg"])

def _m_sun(dr, im, s, cx, cy, r, col):
    for i in range(12):
        a = i * math.pi / 6
        dr.line([cx + r * .55 * math.cos(a), cy + r * .55 * math.sin(a),
                 cx + r * .85 * math.cos(a), cy + r * .85 * math.sin(a)], fill=col, width=max(4, int(r * .1)))
    dr.ellipse([cx - r * .45, cy - r * .45, cx + r * .45, cy + r * .45], fill=col)

def _m_leaf(dr, im, s, cx, cy, r, col):
    dr.pieslice([cx - r, cy - r, cx + r, cy + r], 90, 200, fill=col)
    dr.pieslice([cx - r, cy - r, cx + r, cy + r], 20, 130, fill=_tint(col, .18))

def _m_paw(dr, im, s, cx, cy, r, col):
    dr.ellipse([cx - r * .42, cy - r * .05, cx + r * .42, cy + r * .6], fill=col)
    for dx in (-.5, -.18, .18, .5):
        dr.ellipse([cx + r * dx - r * .14, cy - r * .5, cx + r * dx + r * .14, cy - r * .18], fill=col)

def _m_bear(dr, im, s, cx, cy, r, col):
    snout = _tint(col, .5); eye = _tint(col, -.45)
    dr.ellipse([cx - r * .82, cy - r, cx - r * .3, cy - r * .48], fill=col)
    dr.ellipse([cx + r * .3, cy - r, cx + r * .82, cy - r * .48], fill=col)
    dr.ellipse([cx - r * .82, cy - r * .72, cx + r * .82, cy + r * .82], fill=col)
    dr.ellipse([cx - r * .42, cy + r * .02, cx + r * .42, cy + r * .72], fill=snout)
    dr.ellipse([cx - r * .13, cy + r * .12, cx + r * .13, cy + r * .36], fill=eye)
    dr.ellipse([cx - r * .4, cy - r * .3, cx - r * .2, cy - r * .08], fill=eye)
    dr.ellipse([cx + r * .2, cy - r * .3, cx + r * .4, cy - r * .08], fill=eye)

_MOTIF = {"star": _m_star, "dot": _m_dot, "cloud": _m_cloud, "heart": _m_heart,
          "rainbow": _m_rainbow, "moon": _m_moon, "sun": _m_sun, "leaf": _m_leaf,
          "paw": _m_paw, "bear": _m_bear}


def _decor(im, dr, s, seed, zonas=None):
    """Esparce motivos de la sub-temática en los bordes (sin tapar el centro)."""
    rnd = random.Random(seed)
    pal = [s["c1"], s["c2"], s["c3"], _tint(s["c1"], .4)]
    if zonas is None:   # banda superior + márgenes laterales (sin banda inferior: deja libre el texto)
        zonas = [(110, Wp - 110, 110, 285, 8),
                 (60, 165, 320, Hp - 170, 5), (Wp - 165, Wp - 60, 320, Hp - 170, 5)]
    for x0, x1, y0, y1, n in zonas:
        for _ in range(n):
            x = rnd.randint(x0, x1); y = rnd.randint(y0, y1)
            name = rnd.choice(s["motifs"]); r = rnd.randint(26, 52)
            col = _tint(rnd.choice(pal), 0.12)
            _MOTIF[name](dr, im, s, x, y, r, col)


# ───────────────────────────── base + texto ─────────────────────────────
def _base(s, marco=True, seed=1, zonas=None):
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=s["bg"])
    _decor(im, dr, s, seed, zonas)
    if marco:
        dr.rounded_rectangle([48, 48, Wp - 48, Hp - 48], 46, outline=s["frame"], width=7)
        dr.rounded_rectangle([76, 76, Wp - 76, Hp - 76], 34, outline=_tint(s["frame"], .45), width=3)
    return im, dr

_TOP = [(110, Wp - 110, 110, 285, 10)]   # decoración solo arriba (piezas con texto a todo lo ancho)

def _fit(text, fontfn, maxw, start, minsz=24):
    sz = start
    while fontfn(sz).getbbox(text)[2] > maxw and sz > minsz:
        sz -= 2
    return fontfn(sz)

def _wrap(text, font, maxw):
    out = []
    for para in text.split("\n"):
        words = para.split(); line = ""
        for w in words:
            t = (line + " " + w).strip()
            if font.getbbox(t)[2] <= maxw: line = t
            else:
                if line: out.append(line)
                line = w
        out.append(line)
    return out

def _parrafo(dr, text, font, fill, cx, y, maxw, lh, anchor="mm"):
    for ln in _wrap(text, font, maxw):
        dr.text((cx, y), ln, font=font, fill=fill, anchor=anchor); y += lh
    return y

def _g(d, *keys):
    for k in keys:
        v = (d or {}).get(k)
        if v not in (None, ""): return str(v).strip()
    return ""


def _titulo_grande(dr, s, y, texto="Baby Shower"):
    f = _fit(texto, _script, Wp - 320, 110, 60)
    dr.text((Wp / 2, y), texto, font=f, fill=s["c1"], anchor="mm")
    return y


# ───────────────────────────── piezas ─────────────────────────────
def _p_invitacion(d, s):
    im, dr = _base(s, seed=11)
    bebe = _g(d, "nombre")
    _titulo_grande(dr, s, 360)
    sub = ("Esperando a %s" % bebe) if bebe else "Estamos esperando a nuestro bebé"
    dr.text((Wp / 2, 470), sub, font=_fit(sub, _hand, Wp - 320, 76, 44), fill=s["ink"], anchor="mm")
    dr.line([Wp / 2 - 220, 540, Wp / 2 + 220, 540], fill=_tint(s["frame"], .2), width=3)
    _m_heart(dr, im, s, Wp / 2, 540, 22, s["c3"])

    dr.text((Wp / 2, 640), "Te invitamos a celebrar con nosotros", font=_body(34), fill=s["ink"], anchor="mm")
    pad = _g(d, "mama"); pap = _g(d, "papa")
    if pad or pap:
        quien = " y ".join([x for x in (pad, pap) if x])
        dr.text((Wp / 2, 700), "de parte de %s" % quien, font=_hand(46), fill=s["c1"], anchor="mm")

    y = 820
    filas = [("Cuándo", _g(d, "fecha") or "—"), ("Hora", _g(d, "hora") or "—"),
             ("Dónde", _g(d, "lugar") or "—")]
    if _g(d, "direccion"): filas.append(("Dirección", _g(d, "direccion")))
    for et, val in filas:
        dr.text((Wp / 2, y), et.upper(), font=_body(26, True), fill=s["c1"], anchor="mm"); y += 44
        dr.text((Wp / 2, y), val, font=_fit(val, lambda z: _body(z, True), Wp - 320, 46, 30), fill=s["ink"], anchor="mm")
        y += 96
    dr.text((Wp / 2, Hp - 250), "¡Te esperamos!", font=_hand(64), fill=s["c1"], anchor="mm")
    return im

def _p_no_digas(d, s):
    im, dr = _base(s, seed=22, zonas=_TOP)
    dr.text((Wp / 2, 300), "El juego del broche", font=_hand(56), fill=s["ink"], anchor="mm")
    _titulo_grande(dr, s, 410, "No digas «bebé»")
    dr.rounded_rectangle([120, 540, Wp - 120, 1430], 34, fill=(255, 255, 255), outline=s["frame"], width=4)
    reglas = [
        "Al llegar, cada invitada recibe un broche y se lo prende.",
        "Durante toda la fiesta, ¡nadie puede decir la palabra «bebé»!",
        "Si alguien te escucha decirla, te quita tu broche.",
        "Podés robar los broches de quienes se descuiden.",
        "Quien junte más broches al final… ¡se lleva el premio!",
    ]
    n = len(reglas); top = 600; bot = 1380; slot = (bot - top) / n
    tcx = (270 + (Wp - 160)) / 2; maxw = (Wp - 160) - 270 - 10
    for i, r in enumerate(reglas):
        yc = top + slot * i + slot / 2
        dr.ellipse([175, yc - 30, 235, yc + 30], fill=s["c1"])
        dr.text((205, yc), str(i + 1), font=_body(34, True), fill="white", anchor="mm")
        lines = _wrap(r, _body(32), maxw); ly = yc - (len(lines) - 1) * 46 / 2
        for ln in lines:
            dr.text((tcx, ly), ln, font=_body(32), fill=s["ink"], anchor="mm"); ly += 46
    dr.text((Wp / 2, 1525), "¡Mucha suerte y a cuidar la boquita!", font=_hand(48), fill=s["c1"], anchor="mm")
    bebe = _g(d, "nombre")
    if bebe:
        dr.text((Wp / 2, 1600), "Baby Shower de %s" % bebe, font=_body(28, True), fill=s["ink"], anchor="mm")
    return im

def _p_predicciones(d, s):
    im, dr = _base(s, seed=33, zonas=_TOP)
    bebe = _g(d, "nombre")
    dr.text((Wp / 2, 300), "Predicciones para", font=_hand(50), fill=s["ink"], anchor="mm")
    _titulo_grande(dr, s, 400, bebe or "el bebé")
    campos = ["Fecha de nacimiento", "Hora", "Peso", "¿Se parece a mamá o a papá?",
              "Color de ojos", "¿Nene o nena?", "Nombre que sugiero"]
    y = 540
    for c in campos:
        dr.text((150, y), c, font=_body(30, True), fill=s["c1"], anchor="lm")
        dr.line([150, y + 44, Wp - 150, y + 44], fill=_tint(s["ink"], .55), width=2)
        y += 110
    dr.text((150, y), "Un consejo para los papás", font=_body(30, True), fill=s["c1"], anchor="lm"); y += 70
    for _ in range(2):
        dr.line([150, y, Wp - 150, y], fill=_tint(s["ink"], .55), width=2); y += 72
    dr.text((150, Hp - 200), "De parte de:", font=_body(30, True), fill=s["c1"], anchor="lm")
    dr.line([400, Hp - 188, Wp - 150, Hp - 188], fill=_tint(s["ink"], .55), width=2)
    return im

def _p_etiquetas(d, s):
    im, dr = _base(s, marco=False, seed=44,
                   zonas=[(70, 150, 70, Hp - 70, 4), (Wp - 150, Wp - 70, 70, Hp - 70, 4)])
    bebe = _g(d, "nombre")
    cols, rows = 3, 3; mx, my = 150, 150
    cw = (Wp - 2 * mx) / cols; ch = (Hp - 2 * my) / rows; rad = min(cw, ch) / 2 - 16
    for r in range(rows):
        for c in range(cols):
            cx = mx + cw * (c + .5); cy = my + ch * (r + .5)
            for k in range(0, 360, 18):                      # borde festoneado (cortar)
                a = math.radians(k)
                dr.ellipse([cx + rad * math.cos(a) - 9, cy + rad * math.sin(a) - 9,
                            cx + rad * math.cos(a) + 9, cy + rad * math.sin(a) + 9], fill=s["c3"])
            dr.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(255, 255, 255), outline=s["frame"], width=3)
            _MOTIF[s["motifs"][0]](dr, im, s, cx, cy - rad * .42, rad * .34, s["c1"])
            dr.text((cx, cy + rad * .12), "¡Gracias", font=_hand(40), fill=s["ink"], anchor="mm")
            dr.text((cx, cy + rad * .42), "por venir!", font=_hand(40), fill=s["ink"], anchor="mm")
            if bebe:
                dr.text((cx, cy + rad * .72), bebe, font=_body(22, True), fill=s["c1"], anchor="mm")
    return im

def _p_banderines(d, s):
    im, dr = _base(s, marco=False, seed=55, zonas=[(110, Wp - 110, 60, 215, 7)])
    palabra = (_g(d, "nombre") or "BIENVENIDO").upper()[:12]
    pal = [s["c1"], s["c2"], s["c3"]]
    gap = 22; margin = 70; avail = Wp - 2 * margin; per_row = 6
    filas = [palabra[i:i + per_row] for i in range(0, len(palabra), per_row)] or [palabra]
    nmax = max(len(f) for f in filas)
    fw = min(225, (avail - (nmax - 1) * gap) / nmax); fh = fw * 1.25
    total_h = len(filas) * (fh + 150); y0 = (Hp - total_h) / 2 + 40
    for fi, fila in enumerate(filas):
        nf = len(fila); span = nf * fw + (nf - 1) * gap
        x0 = (Wp - span) / 2; ytop = y0 + fi * (fh + 150)
        dr.line([x0 - 10, ytop - 8, x0 + span + 10, ytop - 8], fill=_tint(s["ink"], .3), width=5)
        for i, ch in enumerate(fila):
            x = x0 + i * (fw + gap); col = pal[(fi * per_row + i) % 3]
            dr.polygon([(x, ytop), (x + fw, ytop), (x + fw / 2, ytop + fh)], fill=col, outline=_tint(col, -.18))
            dr.ellipse([x + fw / 2 - 11, ytop - 24, x + fw / 2 + 11, ytop - 2], fill=_tint(s["ink"], .3))  # ojal
            dr.text((x + fw / 2, ytop + fh * .4), ch, font=_body(int(fw * .6), True), fill="white", anchor="mm")
    dr.text((Wp / 2, Hp - 110), "Recortá los banderines y unilos con un hilo o cinta",
            font=_body(26), fill=s["ink"], anchor="mm")
    return im

def _p_carta18(d, s):
    im, dr = _base(s, seed=66, zonas=_TOP)
    bebe = _g(d, "nombre")
    _m_star(dr, im, s, Wp / 2, 300, 46, s["c2"])
    dr.text((Wp / 2, 410), "Para %s" % (bebe or "vos"), font=_fit("Para %s" % (bebe or "vos"), _script, Wp - 320, 90, 56), fill=s["c1"], anchor="mm")
    dr.text((Wp / 2, 510), "para abrir cuando cumplas 18 años", font=_hand(50), fill=s["ink"], anchor="mm")
    dr.text((Wp / 2, 600), "Un mensaje de quienes te esperaban con tanto amor:", font=_body(28), fill=s["ink"], anchor="mm")
    y = 700
    while y < Hp - 320:
        dr.line([160, y, Wp - 160, y], fill=_tint(s["ink"], .55), width=2); y += 78
    dr.text((160, Hp - 230), "De:", font=_body(30, True), fill=s["c1"], anchor="lm")
    dr.line([260, Hp - 218, 720, Hp - 218], fill=_tint(s["ink"], .55), width=2)
    dr.text((770, Hp - 230), "Fecha:", font=_body(30, True), fill=s["c1"], anchor="lm")
    dr.line([920, Hp - 218, Wp - 160, Hp - 218], fill=_tint(s["ink"], .55), width=2)
    return im


PIEZAS = [
    ("invitacion", "Invitación"),
    ("no_digas_bebe", "Juego: No digas «bebé»"),
    ("predicciones", "Predicciones de los invitados"),
    ("etiquetas", "Etiquetas souvenir"),
    ("banderines", "Banderines"),
    ("carta_18", "Tarjeta para los 18"),
]
_FN = {"invitacion": _p_invitacion, "no_digas_bebe": _p_no_digas, "predicciones": _p_predicciones,
       "etiquetas": _p_etiquetas, "banderines": _p_banderines, "carta_18": _p_carta18}


def pieza(key, data, tema="nubes"):
    return _FN.get(key, _p_invitacion)(data or {}, _sub(tema))


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "nubes"
    d = {"nombre": "Benja", "fecha": "Sábado 12 de julio", "hora": "16:00",
         "lugar": "Salón Las Nubes", "direccion": "Av. Siempreviva 742", "mama": "Caro", "papa": "Lucas"}
    for k, _l in PIEZAS:
        pieza(k, d, tema).convert("RGB").save("/tmp/bs_%s_%s.png" % (tema, k))
    print("OK", tema, [k for k, _ in PIEZAS])
