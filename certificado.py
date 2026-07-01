"""Certificado oficial de cumpleañero — diploma A4 imprimible.
Personalizado con nombre + edad + temática. Marco decorativo, medalla, sello."""
import os, math, json, glob
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
CREAM = (253, 250, 242)
GOLD = (212, 175, 55)
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


def _medalla(dr, cx, cy, r, col, gold):
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=gold, outline=col, width=max(3, r//12))
    dr.ellipse([cx - r*0.78, cy - r*0.78, cx + r*0.78, cy + r*0.78], fill=col, outline=gold, width=max(2, r//15))
    pts = [(cx - r*1.2, cy + r*0.7), (cx, cy + r*2.2), (cx + r*1.2, cy + r*0.7)]
    dr.polygon(pts, fill=col, outline=gold, width=max(2, r//14))
    dr.polygon([(cx - r*0.5, cy + r*0.9), (cx, cy + r*1.6), (cx + r*0.5, cy + r*0.9)], fill=gold)


def _sello(dr, cx, cy, r, col):
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=max(3, r//12))
    dr.ellipse([cx - r*0.85, cy - r*0.85, cx + r*0.85, cy + r*0.85], outline=col, width=max(2, r//18))
    for i in range(20):
        a = i * math.pi / 10
        inner_r = r if i % 2 == 0 else r * 0.88
        x1 = cx + r * 0.95 * math.cos(a)
        y1 = cy + r * 0.95 * math.sin(a)
        x2 = cx + inner_r * math.cos(a)
        y2 = cy + inner_r * math.sin(a)
        dr.line([x1, y1, x2, y2], fill=col, width=max(2, r//16))


def _personajes(tema, n=1):
    try:
        import cuaderno
        return cuaderno.personajes_decorativos(tema, n)
    except Exception:
        return []


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


def generar_certificado(data, tema="safari"):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "______________"
    edad = str(data.get("edad") or "").strip() or "_____"
    anyo = str(data.get("anyo") or data.get("fecha", ""))[:4] or "_____"

    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    bx, by = 120, 100
    dr.rounded_rectangle([bx, by, Wp - bx, Hp - by], 60, outline=GOLD, width=6)
    dr.rounded_rectangle([bx + 20, by + 20, Wp - bx - 20, Hp - by - 20], 45, outline=acc, width=3)

    _medalla(dr, Wp/2, 340, 90, acc, GOLD)

    dr.text((Wp/2, 480), "CERTIFICADO", font=_font(80), fill=GOLD, anchor="mm")
    dr.text((Wp/2, 555), "OFICIAL DE CUMPLEAÑOS", font=_font(44, False), fill=INK, anchor="mm")

    dr.text((Wp/2, 680), "Se otorga el presente certificado a", font=_font(32, False), fill=INK, anchor="mm")

    nom_fs = 120
    while _font(nom_fs).getbbox(nombre)[2] > Wp - 300 and nom_fs > 40:
        nom_fs -= 4
    dr.text((Wp/2, 820), nombre, font=_font(nom_fs), fill=acc, anchor="mm")

    dr.text((Wp/2, 940), "por haber cumplido", font=_font(30, False), fill=INK, anchor="mm")

    edad_fs = 90
    while _font(edad_fs).getbbox(edad + " años")[2] > Wp - 350 and edad_fs > 40:
        edad_fs -= 4
    dr.text((Wp/2, 1060), edad + " años", font=_font(edad_fs), fill=acc, anchor="mm")

    dr.text((Wp/2, 1160), "con alegría, amor y mucha diversión.", font=_font(28, False), fill=INK, anchor="mm")

    _sello(dr, Wp*0.75, Hp - 250, 80, GOLD)
    personajes = _personajes(tema, 1)
    if personajes:
        _paste_h(im, personajes[0], Wp * 0.25, Hp - 260, 190)

    dr.line([Wp*0.2, Hp - 180, Wp*0.45, Hp - 180], fill=INK, width=2)
    dr.text((Wp*0.325, Hp - 165), "Firma", font=_font(24, False), fill=(150, 150, 160), anchor="mm")

    dr.text((Wp/2, Hp - 60), "casatridimensional.com.ar", font=_font(20, False), fill=(180, 180, 180), anchor="mm")
    return im


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Valentina"
    edad = sys.argv[3] if len(sys.argv) > 3 else "4"
    out = sys.argv[4] if len(sys.argv) > 4 else "/tmp/certificado.png"
    generar_certificado({"nombre": nombre, "edad": edad}, tema).convert("RGB").save(out)
    print("OK ->", out)
