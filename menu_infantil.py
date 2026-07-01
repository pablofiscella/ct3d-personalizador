"""Menú infantil personalizado — para la mesa del cumple.
Hoja A4 con espacio para colorear + menú + nombre del cumpleañero.
Ideal para restaurantes / salones de fiesta."""
import os, json, glob
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


def _icono(tipo, size, color):
    """Ícono simple dibujado por código (los emoji no siempre tienen glifo en la fuente)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    s = size
    if tipo == "entrada":       # bowl de picada
        dr.pieslice([s * 0.12, s * 0.35, s * 0.88, s * 0.95], 0, 180, fill=color)
        for i in range(4):
            x = s * 0.28 + i * s * 0.13
            dr.rounded_rectangle([x, s * 0.12, x + s * 0.08, s * 0.45], s * 0.03, fill=color)
    elif tipo == "plato":        # porción de pizza
        dr.polygon([(s * 0.5, s * 0.1), (s * 0.87, s * 0.88), (s * 0.13, s * 0.88)], fill=color)
        for dx, dy in ((-0.1, 0.25), (0.12, 0.4), (-0.12, 0.55), (0.06, 0.65)):
            dr.ellipse([s * 0.5 + dx * s - s * 0.05, s * 0.5 + dy * s - s * 0.05,
                       s * 0.5 + dx * s + s * 0.05, s * 0.5 + dy * s + s * 0.05], fill=(255, 255, 255, 200))
    elif tipo == "postre":       # torta con velita
        dr.rounded_rectangle([s * 0.22, s * 0.5, s * 0.78, s * 0.85], s * 0.05, fill=color)
        dr.polygon([(s * 0.22, s * 0.5), (s * 0.5, s * 0.28), (s * 0.78, s * 0.5)], fill=color)
        dr.rounded_rectangle([s * 0.46, s * 0.1, s * 0.54, s * 0.28], s * 0.02, fill=color)
        dr.ellipse([s * 0.44, s * 0.02, s * 0.56, s * 0.12], fill=(255, 190, 60, 255))
    elif tipo == "bebida":       # vaso con sorbete
        dr.polygon([(s * 0.32, s * 0.22), (s * 0.68, s * 0.22), (s * 0.6, s * 0.88), (s * 0.4, s * 0.88)], fill=color)
        dr.rounded_rectangle([s * 0.46, s * 0.02, s * 0.54, s * 0.24], s * 0.02, fill=color)
    return im


def generar_menu(data, tema="safari"):
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip() or "______________"

    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    dr.rounded_rectangle([80, 60, Wp - 80, 250], 30, fill=acc)
    dr.text((Wp / 2, 130), "MENÚ DEL DÍA", font=_font(56), fill="white", anchor="mm")
    dr.text((Wp / 2, 198), "Hoy cumple %s" % nombre, font=_font(32, False), fill=_tint(acc, 0.75), anchor="mm")

    items = [
        ("entrada", "Entrada", "Picada divertida\nPapas fritas y palitos"),
        ("plato", "Plato principal", "Pizza o hamburguesa\ncon papas"),
        ("postre", "Postre", "Torta de cumpleaños\n¡con velitas!"),
        ("bebida", "Bebida", "Jugo o gaseosa"),
    ]
    y = 310
    for tipo, titulo, desc in items:
        dr.rounded_rectangle([100, y, Wp - 100, y + 170], 25, fill=(255, 255, 255), outline=_tint(acc, 0.5), width=3)
        ic = _icono(tipo, 90, acc)
        im.alpha_composite(ic, (115, int(y + 40)))
        dr.text((280, y + 40), titulo, font=_font(36), fill=acc, anchor="lm")
        dl = desc.split("\n")
        for i, line in enumerate(dl):
            dr.text((280, y + 85 + i * 32), line, font=_font(26, False), fill=INK, anchor="lm")
        y += 190

    dr.text((Wp / 2, Hp - 120), "Coloreá la pizza y la torta", font=_font(24, False), fill=_tint(INK, 0.3), anchor="mm")
    dr.text((Wp / 2, Hp - 60), "casatridimensional.com.ar", font=_font(20, False), fill=(180, 180, 180), anchor="mm")
    return im


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Ciro"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/menu.png"
    generar_menu({"nombre": nombre, "edad": "5"}, tema).convert("RGB").save(out)
    print("OK ->", out)
