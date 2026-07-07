"""Juego de la memoria personalizado — cartas con el personaje del tema + nombre.
12 pares (24 cartas) para imprimir, recortar y jugar.

Las imágenes de las cartas son los personajes REALES del tema (mismo mecanismo que
el cuaderno de actividades: recorte por componente de alpha de la hoja de stickers).
Si el tema no tiene stickers generados todavía, cae a íconos geométricos por código
(nunca mezcla temas: no hay fallback a animalitos genéricos en un tema que no lo es)."""
import os, json, glob, math, random
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
CREAM = (253, 250, 242)
INK = (60, 50, 45)

random.seed(42)


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


def _fit_into(img, mw, mh):
    r = min(mw / img.width, mh / img.height)
    return img.resize((max(1, int(img.width * r)), max(1, int(img.height * r))), Image.LANCZOS)


def _dibujar_forma(forma, size, color):
    """Ícono geométrico simple (fallback cuando el tema no tiene stickers extraíbles)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    m = size * 0.14
    cx = cy = size / 2
    if forma == "circulo":
        dr.ellipse([m, m, size - m, size - m], fill=color)
    elif forma == "cuadrado":
        dr.rounded_rectangle([m, m, size - m, size - m], size * 0.15, fill=color)
    elif forma == "triangulo":
        dr.polygon([(cx, m), (size - m, size - m), (m, size - m)], fill=color)
    elif forma == "diamante":
        dr.polygon([(cx, m), (size - m, cy), (cx, size - m), (m, cy)], fill=color)
    elif forma == "estrella":
        ro, ri = (size - 2 * m) / 2, (size - 2 * m) / 2 * 0.42
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            r = ro if i % 2 == 0 else ri
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        dr.polygon(pts, fill=color)
    elif forma == "corazon":
        r = (size - 2 * m) / 4
        dr.ellipse([cx - 2 * r, cy - 2 * r, cx, cy], fill=color)
        dr.ellipse([cx, cy - 2 * r, cx + 2 * r, cy], fill=color)
        dr.polygon([(cx - 2 * r, cy - r * 0.6), (cx + 2 * r, cy - r * 0.6), (cx, size - m)], fill=color)
    return im


def _personajes(tema, n=12):
    """n imágenes RGBA distintas para las cartas: personajes reales del tema si hay
    (extraídos de la hoja de stickers), completando con íconos geométricos si faltan."""
    imgs = []
    try:
        import cuaderno
        paths = cuaderno._extraer_monstruos(tema) or []
        paso = max(1, len(paths) // n)
        for p in paths[::paso][:n]:
            try:
                imgs.append(Image.open(p).convert("RGBA"))
            except Exception:
                pass
    except Exception:
        pass
    if len(imgs) < n:
        acc = _accent(tema)
        formas = ["circulo", "cuadrado", "triangulo", "estrella", "diamante", "corazon"]
        combos = [(f, c) for c in (acc, _tint(acc, 0.45)) for f in formas]
        for f, c in combos[:max(0, n - len(imgs))]:
            imgs.append(_dibujar_forma(f, 300, c))
    return imgs[:n]


def carta(im, dr, cx, cy, w, h, img, idx, acc, volteada=True):
    """Dibuja una carta del memory. volteada=True -> dorso oculto; False -> cara con imagen."""
    if volteada:
        dr.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                             14, fill=acc, outline=_tint(acc, 0.2), width=4)
        dr.rounded_rectangle([cx - w / 2 + 10, cy - h / 2 + 10, cx + w / 2 - 10, cy + h / 2 - 10],
                             10, fill=_tint(acc, 0.7))
        dr.text((cx, cy - 10), "?", font=_font(60), fill="white", anchor="mm")
    else:
        dr.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                             14, fill=(255, 255, 255), outline=_tint(acc, 0.3), width=3)
        if img is not None:
            fit = _fit_into(img, w - 26, h - 46)
            im.alpha_composite(fit, (int(cx - fit.width / 2), int(cy - h / 2 + 10)))
        dr.text((cx, cy + h / 2 - 16), str(idx + 1), font=_font(16, False), fill=_tint(INK, 0.35), anchor="mm")


def generar_memoria(data, tema="safari"):
    """Hoja A4 con 24 cartas (12 pares) para recortar y jugar."""
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip() or "MI MEMORIA"

    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    dr.text((Wp / 2, 70), "JUEGO DE LA MEMORIA", font=_font(44), fill=acc, anchor="mm")
    dr.text((Wp / 2, 120), nombre, font=_font(28, False), fill=_tint(INK, 0.3), anchor="mm")

    cols, rows = 6, 4
    n_pares = (cols * rows) // 2   # 12 pares = 24 cartas: llena la grilla exacto
    base_imgs = _personajes(tema, n_pares)
    cartas_data = []
    for i, img in enumerate(base_imgs):
        cartas_data.append((i, img))
        cartas_data.append((i, img))
    random.shuffle(cartas_data)

    cw, ch = 170, 210
    gap_x, gap_y = 30, 30
    total_w = cols * cw + (cols - 1) * gap_x
    x0 = (Wp - total_w) / 2 + cw / 2
    y0 = 190 + ch / 2

    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            if idx >= len(cartas_data):
                break
            par_idx, img = cartas_data[idx]
            cx = x0 + c * (cw + gap_x)
            cy = y0 + r * (ch + gap_y)
            carta(im, dr, cx, cy, cw, ch, img, par_idx, acc, volteada=False)

    y_info = y0 + rows * (ch + gap_y) - gap_y / 2 + 40
    dr.text((Wp / 2, y_info), "Recortá las cartas, dales vuelta y encontrá los pares",
            font=_font(24, False), fill=INK, anchor="mm")
    dr.text((Wp / 2, Hp - 40), "casatridimensional.com.ar", font=_font(18, False), fill=(180, 180, 180), anchor="mm")
    return im


def dorso_memoria(data, tema="safari"):
    """Hoja A4 con los dorsos de las cartas (para imprimir al dorso)."""
    acc = _accent(tema)
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    cols, rows = 6, 4
    cw, ch = 170, 210
    gap_x, gap_y = 30, 30
    total_w = cols * cw + (cols - 1) * gap_x
    x0 = (Wp - total_w) / 2 + cw / 2
    y0 = 100 + ch / 2

    for r in range(rows):
        for c in range(cols):
            cx = x0 + c * (cw + gap_x)
            cy = y0 + r * (ch + gap_y)
            carta(im, dr, cx, cy, cw, ch, None, 0, acc, volteada=True)

    dr.text((Wp / 2, Hp - 40), "Dorso — %s" % str(data.get("nombre") or ""),
            font=_font(18, False), fill=_tint(INK, 0.3), anchor="mm")
    return im


def piezas(data, tema="safari"):
    return [("1_cartas_memoria", lambda d: generar_memoria(d, tema), True),
            ("2_dorso", lambda d: dorso_memoria(d, tema), True)]


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Benicio"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/memoria"
    d = {"nombre": nombre, "edad": "5"}
    generar_memoria(d, tema).convert("RGB").save(f"{out}_cartas.png")
    dorso_memoria(d, tema).convert("RGB").save(f"{out}_dorso.png")
    print(f"OK -> {out}_cartas.png + {out}_dorso.png")
