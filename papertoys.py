"""Paper Toys / Figuras 3D para armar — cubo temático (dado de la fiesta).

REDISEÑO 7-jul-2026 (skill armar-kit §11 — la versión anterior NO ARMABA: la
"red" era una fila de 4 caras + 2 caras contiguas abajo que se superponían al
plegar, con gaps entre caras, sin solapas reales y con cara vacía si el nombre
tenía <6 letras):
- Red en CRUZ válida de cubo (tira vertical de 4 caras + 2 laterales pegadas a
  la segunda), caras CONTIGUAS (sin gaps: los dobleces son aristas compartidas).
- 7 pestañas trapezoidales de ~9mm con chanfles a 45°, UNA por arista abierta,
  NUMERADAS en orden de pegado (skill: la base se pega última para poder meter
  los dedos).
- Líneas: corte = sólida gris; doblez = guiones.
- El arte CONTINÚA a través de las aristas (mismo fondo de color corrido).
  SIN letras ni nombre (Pablo 8-jul-2026): las 6 caras llevan personajes del
  tema — full imagen.
- 300dpi real (A4 = 2480x3508): caras de 6cm — cubo terminado de 6cm.
"""
import os, math, json, glob
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
_PXMM = 2480 / 210.0
Wp, Hp = 2480, 3508
CREAM = (253, 250, 242)
INK = (60, 50, 45)
CORTE = (140, 140, 140)


def _mm(v):
    return v * _PXMM


def _font(sz, bold=True):
    for p in glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True):
        try:
            f = ImageFont.truetype(p, sz)
            try: f.set_variation_by_axes([700 if bold else 500])
            except Exception: pass
            return f
        except Exception: pass
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)


def _accent(tema):
    try:
        d = json.load(open(os.path.join(TEMAS, tema, "tema.json")))
        h = (d.get("kit") or {}).get("accent") or "#6B5BD2"
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except Exception:
        return (107, 91, 210)


def _tint(c, p):
    return tuple(int(v + (255 - v) * p) for v in c[:3])


def _personajes(tema, n=2):
    try:
        import cuaderno
        return cuaderno.personajes_decorativos(tema, n)
    except Exception:
        return []


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


def _pestania(dr, x0, y0, x1, y1, hacia, prof, num, acc):
    """Pestaña trapezoidal con chanfles a 45° sobre la arista (x0,y0)-(x1,y1).
    `hacia` = (dx,dy) unitario hacia AFUERA de la red. Numerada (orden de pegado)."""
    ux, uy = x1 - x0, y1 - y0
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    ch = min(prof, L * 0.28)             # chanfle 45°: corre el borde exterior
    px0 = (x0 + ux * ch + hacia[0] * prof, y0 + uy * ch + hacia[1] * prof)
    px1 = (x1 - ux * ch + hacia[0] * prof, y1 - uy * ch + hacia[1] * prof)
    dr.polygon([(x0, y0), px0, px1, (x1, y1)],
               fill=_tint(acc, 0.88), outline=CORTE, width=4)
    cx, cy = (px0[0] + px1[0]) / 2 - hacia[0] * prof * 0.32, (px0[1] + px1[1]) / 2 - hacia[1] * prof * 0.32
    dr.text((cx, cy), str(num), font=_font(int(prof * 0.55)), fill=_tint(INK, 0.25), anchor="mm")


def _doblez(dr, x0, y0, x1, y1):
    """Línea de doblez punteada."""
    L = math.hypot(x1 - x0, y1 - y0)
    n = max(2, int(L / _mm(4)))
    for i in range(n):
        t0, t1 = i / n, i / n + 0.55 / n
        dr.line([x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0,
                 x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1], fill=(120, 110, 100), width=4)


def cubo_personalizado(data, tema="safari"):
    """Cubo temático: red en cruz válida + pestañas numeradas + arte del tema.
    SIN nombre (decisión de Pablo 8-jul-2026: full imagen, sin letras)."""
    acc = _accent(tema)

    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)
    dr.text((60, 55), "CUBO PARA ARMAR · el dado del tema",
            font=_font(44, False), fill=_tint(acc, 0.3))

    lado = _mm(52)                                  # cubo terminado de 5.2cm
    prof = _mm(9)                                   # pestañas ~9mm
    # red en cruz: tira vertical T(arriba) F B K + laterales L R pegados a F
    cx = Wp / 2
    y0 = _mm(24)
    caras = {
        "T": (cx - lado / 2, y0),
        "F": (cx - lado / 2, y0 + lado),
        "B": (cx - lado / 2, y0 + 2 * lado),
        "K": (cx - lado / 2, y0 + 3 * lado),
        "L": (cx - 3 * lado / 2, y0 + lado),
        "R": (cx + lado / 2, y0 + lado),
    }

    # ---- fondo de color CONTINUO en toda la cruz (el arte cruza las aristas) ----
    cruz = [(caras[k][0], caras[k][1], caras[k][0] + lado, caras[k][1] + lado)
            for k in caras]
    fondo = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fondo)
    for x0_, y0_, x1_, y1_ in cruz:
        fd.rectangle([x0_, y0_, x1_, y1_], fill=_tint(acc, 0.72))
    # lunares del tema cruzando TODA la cruz (continuidad entre caras)
    import random
    rnd = random.Random(hash(tema) & 0xffff)
    minx = min(c[0] for c in cruz); maxx = max(c[2] for c in cruz)
    miny = min(c[1] for c in cruz); maxy = max(c[3] for c in cruz)
    mask = Image.new("L", (Wp, Hp), 0)
    md = ImageDraw.Draw(mask)
    for x0_, y0_, x1_, y1_ in cruz:
        md.rectangle([x0_, y0_, x1_, y1_], fill=255)
    lunares = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lunares)
    for _ in range(90):
        x = rnd.uniform(minx, maxx); y = rnd.uniform(miny, maxy)
        r = rnd.uniform(_mm(1.4), _mm(3.4))
        ld.ellipse([x - r, y - r, x + r, y + r],
                   fill=_tint(acc, rnd.choice((0.35, 0.5, 0.9))))
    fondo.alpha_composite(Image.composite(lunares, Image.new("RGBA", lunares.size, (0, 0, 0, 0)), mask))
    im.alpha_composite(fondo)

    # ---- contenido por cara: personajes + objetos del tema en las 6 (sin letras).
    # L y R van GIRADAS 90° (una a cada lado): al plegar la caja quedan de
    # costado, y con el giro el dibujo se ve derecho (feedback Pablo 9-jul-2026).
    pjs = _personajes(tema, 6)
    if len(pjs) < 3:
        try:
            import cuaderno
            pjs = cuaderno.personajes_decorativos(tema, 6, incluir_objetos=True)
        except Exception:
            pass
    orden = ["F", "L", "R", "T", "B", "K"]        # las caras más visibles primero
    rot = {"L": 90, "R": -90}    # +180° vs la 1ª versión (Pablo probó el plegado)
    for i, k in enumerate(orden):
        x, y = caras[k]
        if pjs:
            pj = pjs[i % len(pjs)]
            if rot.get(k):
                pj = pj.rotate(rot[k], expand=True, resample=Image.BICUBIC)
            _paste_h(im, pj, x + lado / 2, y + lado / 2, lado * 0.78)
        else:
            dr.ellipse([x + lado * 0.30, y + lado * 0.30, x + lado * 0.70, y + lado * 0.70],
                       fill=_tint(acc, 0.4))

    # ---- pestañas (7, numeradas en orden de pegado; la base al final) ----
    T, F, B, K, L, R = (caras[k] for k in "TFBKLR")
    dr2 = ImageDraw.Draw(im)
    pest = [
        (L[0], L[1], L[0], L[1] + lado, (-1, 0), 1),                 # L izquierda
        (R[0] + lado, R[1], R[0] + lado, R[1] + lado, (1, 0), 2),    # R derecha
        (T[0], T[1], T[0] + lado, T[1], (0, -1), 3),                 # T arriba
        (T[0], T[1], T[0], T[1] + lado, (-1, 0), 4),                 # T izq
        (T[0] + lado, T[1], T[0] + lado, T[1] + lado, (1, 0), 5),    # T der
        (K[0], K[1], K[0], K[1] + lado, (-1, 0), 6),                 # K izq
        (K[0] + lado, K[1], K[0] + lado, K[1] + lado, (1, 0), 7),    # K der
    ]
    for x0_, y0_, x1_, y1_, hacia, num in pest:
        _pestania(dr2, x0_, y0_, x1_, y1_, hacia, prof, num, acc)

    # ---- líneas: doblez (aristas internas) y corte (contorno exterior) ----
    _doblez(dr2, F[0], F[1], F[0] + lado, F[1])                      # T/F
    _doblez(dr2, B[0], B[1], B[0] + lado, B[1])                      # F/B
    _doblez(dr2, K[0], K[1], K[0] + lado, K[1])                      # B/K
    _doblez(dr2, F[0], F[1], F[0], F[1] + lado)                      # L/F
    _doblez(dr2, R[0], R[1], R[0], R[1] + lado)                      # F/R
    # contorno de corte (perímetro de la cruz, salvo donde hay pestaña: se corta
    # alrededor de la pestaña, ya dibujada con su outline)
    per = [
        (T[0], T[1] + lado, T[0], T[1]), (T[0], T[1], T[0] + lado, T[1]),
        (T[0] + lado, T[1], T[0] + lado, T[1] + lado),
        (R[0], R[1], R[0] + lado, R[1]), (R[0] + lado, R[1], R[0] + lado, R[1] + lado),
        (R[0] + lado, R[1] + lado, R[0], R[1] + lado),
        (B[0] + lado, B[1], B[0] + lado, B[1] + lado),
        (K[0] + lado, K[1], K[0] + lado, K[1] + lado),
        (K[0] + lado, K[1] + lado, K[0], K[1] + lado),
        (K[0], K[1] + lado, K[0], K[1]), (B[0], B[1] + lado, B[0], B[1]),
        (L[0] + lado, L[1] + lado, L[0], L[1] + lado), (L[0], L[1] + lado, L[0], L[1]),
        (L[0], L[1], L[0] + lado, L[1]),
    ]
    for x0_, y0_, x1_, y1_ in per:
        dr2.line([x0_, y0_, x1_, y1_], fill=CORTE, width=4)

    # ---- instrucciones + decoración ----
    y = K[1] + lado + prof + _mm(16)
    pasos = ["1. Recortá TODO el contorno (con las pestañas).",
             "2. Doblá por las líneas punteadas (marcalas antes con una regla).",
             "3. Pegá las pestañas EN ORDEN (1 a 7) — la 6 y 7 al final, son la base.",
             "4. ¡Listo! Un dado del tema para jugar en la fiesta."]
    for t in pasos:
        dr2.text((Wp / 2, y), t, font=_font(38, False), fill=_tint(INK, 0.2), anchor="mm")
        y += _mm(9)

    # sin decoración extra al pie: el cubo ya lleva los personajes en sus caras
    # laterales, y los recortes al pie chocaban con las instrucciones.
    dr2.text((Wp / 2, Hp - 60), "casatridimensional.com.ar", font=_font(36, False),
             fill=(180, 180, 180), anchor="mm")
    return im


def piezas(data, tema="safari"):
    return [("1_cubo", lambda d: cubo_personalizado(d, tema), True)]


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "LUCAS"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/papertoys.png"
    cubo_personalizado({"nombre": nombre}, tema).convert("RGB").save(out)
    print("OK ->", out)
