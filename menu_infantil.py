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
        ("🥤", "Entrada", "Picada divertida\nPapas fritas y palitos"),
        ("🍕", "Plato principal", "Pizza o hamburguesa\ncon papas"),
        ("🎂", "Postre", "Torta de cumpleaños\n¡con velitas!"),
        ("🧃", "Bebida", "Jugo o gaseosa"),
    ]
    y = 310
    for emoji, titulo, desc in items:
        dr.rounded_rectangle([100, y, Wp - 100, y + 170], 25, fill=(255, 255, 255), outline=_tint(acc, 0.5), width=3)
        dr.text((160, y + 50), emoji, font=_font(50), fill=acc, anchor="mm")
        dr.text((280, y + 40), titulo, font=_font(36), fill=acc, anchor="lm")
        dl = desc.split("\n")
        for i, line in enumerate(dl):
            dr.text((280, y + 85 + i * 32), line, font=_font(26, False), fill=INK, anchor="lm")
        y += 190

    dr.text((Wp / 2, Hp - 120), "✂ Coloreá la pizza y la torta", font=_font(24, False), fill=_tint(INK, 0.3), anchor="mm")
    dr.text((Wp / 2, Hp - 60), "casatridimensional.com.ar", font=_font(20, False), fill=(180, 180, 180), anchor="mm")
    return im


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Ciro"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/menu.png"
    generar_menu({"nombre": nombre, "edad": "5"}, tema).convert("RGB").save(out)
    print("OK ->", out)
