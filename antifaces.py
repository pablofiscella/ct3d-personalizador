"""Antifaces y Photo Booth Props — máscaras, bigotes, lentes, coronas en palito.
Para imprimir, recortar, pegar en palitos y sacarse fotos.
100% procedural con Pillow."""
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


def antifaz_mariposa(data, tema="safari"):
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip()
    im = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    cx, cy = Wp / 2, Hp / 2
    w, h = 400, 180
    for side in (-1, 1):
        ox = cx + side * 220
        dr.ellipse([ox - w / 2, cy - h / 2, ox + w / 2, cy + h / 2], fill=acc, outline=_tint(acc, 0.2), width=6)
        dr.ellipse([ox - w / 3, cy - h / 3, ox + w / 3, cy + h / 3], fill=(255, 255, 255), outline=_tint(acc, 0.2), width=3)
    dr.ellipse([cx - 25, cy - 12, cx + 25, cy + 12], fill=acc)
    for side in (-1, 1):
        dr.line([cx + side * 25, cy, cx + side * 60, cy - 20], fill=acc, width=5)
        dr.line([cx + side * 25, cy, cx + side * 60, cy + 20], fill=acc, width=5)
    fs = 36
    while _font(fs).getbbox(nombre)[2] > 400 and fs > 18:
        fs -= 2
    dr.text((cx, cy + h / 2 + 60), nombre, font=_font(fs), fill=acc, anchor="mm")
    dr.text((cx, cy + h / 2 + 100), "Recortá y pegá en un palito", font=_font(20, False), fill=_tint(INK, 0.3), anchor="mm")
    return im


def bigotes(data, tema="safari"):
    acc = _accent(tema)
    im = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    for i in range(6):
        cx = (i % 3) * 400 + 220
        cy = (i // 3) * 500 + 300
        w, h = 160, 50
        dr.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=acc)
        for side in (-1, 1):
            pts = [(cx + side * w * 0.45, cy - h * 0.3),
                   (cx + side * w * 1.8, cy - h * 1.2),
                   (cx + side * w * 1.6, cy - h * 0.45),
                   (cx + side * w * 0.45, cy - h * 0.05)]
            dr.polygon(pts, fill=acc)
        dr.line([cx - w * 0.7, cy + h * 0.4, cx + w * 0.7, cy + h * 0.4], fill=acc, width=4)
    return im


def lentes_fiesta(data, tema="safari"):
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip()
    im = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    for i in range(3):
        cx = i * 400 + 300
        cy = 400
        for side in (-1, 1):
            r = 100
            dr.ellipse([cx + side * 130 - r, cy - r, cx + side * 130 + r, cy + r],
                       outline=acc, width=12)
        dr.arc([cx - 130, cy - 130, cx + 130, cy + 130], -30, 210, fill=acc, width=12)
        dr.line([cx - 130, cy + 100, cx - 130, cy + 450], fill=acc, width=8)
        dr.line([cx + 130, cy + 100, cx + 130, cy + 450], fill=acc, width=8)
        dr.line([cx - 280, cy + 80, cx - 130, cy + 80], fill=acc, width=10)
        dr.line([cx + 280, cy + 80, cx + 130, cy + 80], fill=acc, width=10)
        dr.text((cx, cy + 470), nombre if i == 1 else "", font=_font(28), fill=acc, anchor="mm")
    return im


def piezas(data, tema="safari"):
    return [("1_antifaz", lambda d: antifaz_mariposa(d, tema), True),
            ("2_bigotes", lambda d: bigotes(d, tema), True),
            ("3_lentes", lambda d: lentes_fiesta(d, tema), True)]


if __name__ == "__main__":
    tema = "safari"
    d = {"nombre": "Luna", "edad": "4"}
    antifaz_mariposa(d, tema).save("/tmp/antifaz.png")
    bigotes(d, tema).save("/tmp/bigotes.png")
    lentes_fiesta(d, tema).save("/tmp/lentes.png")
    print("OK")
