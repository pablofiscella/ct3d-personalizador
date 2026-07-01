"""Paper Toys / Figuras 3D para armar — personajes de la temática en papel.
Prismas, cubos y formas geométricas con solapas para recortar, doblar y pegar.
Cada figura despliega en una hoja A4 con instrucciones."""
import os, math, json, glob
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
CREAM = (253, 250, 242)
INK = (60, 50, 45)


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


def cubo_personalizado(data, tema="safari"):
    """Cubo desplegable (6 caras) con letras del nombre + decoración."""
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip().upper() or "JUEGO"
    letras = (nombre + " " * 6)[:6]

    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    dr.text((Wp / 2, 80), "CUBO PARA ARMAR", font=_font(48), fill=acc, anchor="mm")
    dr.text((Wp / 2, 130), nombre, font=_font(30, False), fill=_tint(INK, 0.3), anchor="mm")

    lado = 220
    gap = 30
    x0 = (Wp - 3 * lado - 2 * gap) / 2
    y0 = 220

    for i in range(4):
        cx = x0 + i * (lado + gap) + lado / 2
        cy = y0 + lado / 2
        dr.rounded_rectangle([cx - lado / 2, cy - lado / 2, cx + lado / 2, cy + lado / 2],
                             12, fill=acc, outline=_tint(acc, 0.2), width=4)
        dr.text((cx, cy), letras[i] if i < len(letras) else "?", font=_font(100), fill="white", anchor="mm")
        for side in (-1, 1):
            sl = 40
            dr.line([cx + side * lado / 2, cy, cx + side * (lado / 2 + sl), cy], fill=acc, width=3)
        dr.line([cx, cy + lado / 2, cx, cy + lado / 2 + gap], fill=_tint(INK, 0.3), width=2,)

    for i in range(2):
        cx = x0 + i * (lado + gap) + lado / 2 + (lado + gap)
        cy = y0 + lado + gap + lado / 2
        dr.rounded_rectangle([cx - lado / 2, cy - lado / 2, cx + lado / 2, cy + lado / 2],
                             12, fill=acc, outline=_tint(acc, 0.2), width=4)
        dr.text((cx, cy), letras[4 + i] if 4 + i < len(letras) else "?",
                font=_font(100), fill="white", anchor="mm")
        for side in (-1, 1):
            sl = 40
            dr.line([cx + side * lado / 2, cy, cx + side * (lado / 2 + sl), cy], fill=acc, width=3)

    dr.line([x0 + lado / 2, y0 + lado, x0 + lado / 2, y0 + lado + gap], fill=_tint(INK, 0.3), width=2,)

    instrucciones = [
        "1. Recortá todo el contorno",
        "2. Doblá por las líneas punteadas",
        "3. Pegá las solapas con adhesivo",
        "4. ¡Armaste tu cubo personalizado!",
    ]
    y = y0 + 2 * lado + 2 * gap + 60
    for t in instrucciones:
        dr.text((Wp / 2, y), t, font=_font(26, False), fill=INK, anchor="mm")
        y += 42

    personajes = _personajes(tema, 2)
    if personajes:
        spots = [(Wp * 0.3, Hp - 300), (Wp * 0.7, Hp - 300)] if len(personajes) > 1 else [(Wp / 2, Hp - 300)]
        for p, (sx, sy) in zip(personajes, spots):
            _paste_h(im, p, sx, sy, 340)

    dr.text((Wp / 2, Hp - 40), "casatridimensional.com.ar", font=_font(18, False), fill=(180, 180, 180), anchor="mm")
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
