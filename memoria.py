"""Juego de la memoria personalizado — cartas con dibujos + nombre.
12 pares (24 cartas) para imprimir, recortar y jugar.
Cada carta tiene un dibujo decorativo + el nombre del cumpleañero.
Incluye versión temática (usa los stickers del tema) y procedural."""
import os, json, glob, random
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


_ICONOS_MEMORIA = [
    "🎈", "🎂", "🎁", "🎉", "🎊", "🦁",
    "🐘", "🦒", "🐒", "🐯", "⭐", "🌈",
]


def carta(dr, cx, cy, w, h, emoji, label, acc, volteada=True):
    """Dibuja una carta del memory (el dorso si no está volteada)."""
    if volteada:
        dr.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                             14, fill=acc, outline=_tint(acc, 0.2), width=4)
        dr.rounded_rectangle([cx - w / 2 + 10, cy - h / 2 + 10, cx + w / 2 - 10, cy + h / 2 - 10],
                             10, fill=_tint(acc, 0.7))
        dr.text((cx, cy - 10), "?", font=_font(60), fill="white", anchor="mm")
    else:
        dr.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                             14, fill=(255, 255, 255), outline=_tint(acc, 0.3), width=3)
        dr.text((cx, cy - 14), emoji, font=_font(50), anchor="mm")
        dr.text((cx, cy + h / 2 - 36), label, font=_font(20, False), fill=INK, anchor="mm")


def _intentar_cargar_stickers(tema):
    """Intenta cargar stickers del tema para usarlos como imágenes del memory."""
    try:
        import piezas as pz
        if pz.has_recortes(tema):
            anims = pz.animales(tema)
            if anims:
                return [pz.load(a, tema) for a in anims[:6]]
    except Exception:
        pass
    return None


def generar_memoria(data, tema="safari"):
    """Hoja A4 con 24 cartas (12 pares) para recortar y jugar."""
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip() or "MI MEMORIA"

    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    dr.text((Wp / 2, 70), "JUEGO DE LA MEMORIA", font=_font(44), fill=acc, anchor="mm")
    dr.text((Wp / 2, 120), nombre, font=_font(28, False), fill=_tint(INK, 0.3), anchor="mm")

    pares = _ICONOS_MEMORIA[:8]
    labels = []
    for i in range(8):
        labels.append(str(i + 1))
    cartas_data = []
    for i, (emoji, label) in enumerate(zip(pares, labels)):
        cartas_data.append((emoji, label))
        cartas_data.append((emoji, label))
    random.shuffle(cartas_data)

    cols, rows = 6, 4
    cw = 170
    ch = 210
    gap_x = 30
    gap_y = 30
    total_w = cols * cw + (cols - 1) * gap_x
    total_h = rows * ch + (rows - 1) * gap_y
    x0 = (Wp - total_w) / 2 + cw / 2
    y0 = 190 + ch / 2

    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            if idx >= len(cartas_data):
                break
            emoji, label = cartas_data[idx]
            cx = x0 + c * (cw + gap_x)
            cy = y0 + r * (ch + gap_y)
            carta(dr, cx, cy, cw, ch, emoji, label, acc, volteada=False)

    y_info = y0 + rows * (ch + gap_y) - gap_y / 2 + 40
    dr.text((Wp / 2, y_info), "✂ Recortá las cartas, dales vuelta y encontrá los pares",
            font=_font(24, False), fill=INK, anchor="mm")
    dr.text((Wp / 2, Hp - 40), "casatridimensional.com.ar", font=_font(18, False), fill=(180, 180, 180), anchor="mm")
    return im


def dorso_memoria(data, tema="safari"):
    """Hoja A4 con los dorsos de las cartas (para imprimir al dorso)."""
    acc = _accent(tema)
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)

    cols, rows = 6, 4
    cw = 170
    ch = 210
    gap_x = 30
    gap_y = 30
    total_w = cols * cw + (cols - 1) * gap_x
    x0 = (Wp - total_w) / 2 + cw / 2
    y0 = 100 + ch / 2

    for r in range(rows):
        for c in range(cols):
            cx = x0 + c * (cw + gap_x)
            cy = y0 + r * (ch + gap_y)
            carta(dr, cx, cy, cw, ch, "", "", acc, volteada=True)

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
