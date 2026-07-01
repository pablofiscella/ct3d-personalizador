"""Gorro / Corona de cumpleaños para armar (craft recortable).
Template A4 con solapas para imprimir, recortar, doblar y pegar.
Dos estilos: gorro cónico (party hat) y corona de rey/reina."""
import os, math, json, glob
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
CREAM = (253, 250, 242)


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


def _draw_instrucciones(dr, x, y, col):
    dr.text((x, y), "Instrucciones:", font=_font(28, False), fill=col, anchor="mm")
    pasos = ["1. Recortá por la línea de corte", "2. Doblá por la línea punteada",
             "3. Pegá las solapas con adhesivo"]
    for i, txt in enumerate(pasos):
        dr.text((x, y + 50 + i * 36), txt, font=_font(22, False), fill=_tint(col, 0.3), anchor="mm")


def _draw_instrucciones_en(im, dr, x, y, col):
    _draw_instrucciones(dr, x, y, col)


def gorro(data, tema="safari"):
    """Gorro cónico de cumpleaños para armar. Ocupa media hoja A4."""
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or ""

    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    cx, cy = Wp / 2, 120
    r = 520
    ang = math.radians(60)
    pts = []
    for i in range(61):
        a = -ang + i * 2 * ang / 60
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    dr.polygon([(cx, cy)] + pts, outline=(180, 180, 180), width=3, fill=acc + (180,))

    dr.arc([cx - r, cy - r, cx + r, cy + r], -60, 60, fill=acc, width=4)

    solapas = []
    for side in (-1, 1):
        sx = cx + r * math.cos(side * ang)
        sy = cy + r * math.sin(side * ang)
        sl = 40
        solapas.append((sx, sy, sx + side * sl, sy))
    for x1, y1, x2, y2 in solapas:
        dr.line([x1, y1, x2, y2], fill=acc, width=3)

    if nombre:
        nr = 220
        n_ang = math.radians(45)
        n_cx = cx + nr * math.cos(n_ang)
        n_cy = cy + nr * math.sin(n_ang)
        fs = 62
        while _font(fs).getbbox(nombre)[2] > 400 and fs > 24:
            fs -= 3
        dr.text((n_cx, n_cy), nombre, font=_font(fs), fill=(255, 255, 255), anchor="mm")

    dr.text((cx, cy + 100), "CUMPLEAÑOS", font=_font(50), fill=(255, 255, 255) if acc else acc, anchor="mm")
    edad = str(data.get("edad") or "").strip()
    if edad:
        efs = 130
        while _font(efs).getbbox(edad)[2] > 300 and efs > 60:
            efs -= 4
        dr.text((cx + 110, cy - 40), edad, font=_font(efs), fill=(255, 255, 255) if acc else acc, anchor="mm")

    _draw_instrucciones_en(im, dr, Wp / 2, 700, acc)

    dr.text((Wp / 2, Hp - 40), "casatridimensional.com.ar", font=_font(18, False), fill=(180, 180, 180), anchor="mm")
    return im


def corona(data, tema="safari"):
    """Corona de rey/reina para armar. Tira con picos, solapas para pegar."""
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or ""

    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    y0 = 160
    h_banda = 220
    w_corona = Wp - 200
    x0 = (Wp - w_corona) / 2

    for i in range(7):
        px = x0 + w_corona * (i / 6)
        pico_h = 160 + ((i * 37) % 3) * 30
        pts = [(px - 40, y0 + h_banda), (px, y0 - pico_h + h_banda), (px + 40, y0 + h_banda)]
        dr.polygon(pts, fill=acc, outline=_tint(acc, 0.2), width=3)
        dr.ellipse([px - 18, y0 - pico_h + h_banda - 15, px + 18, y0 - pico_h + h_banda + 15],
                   fill=(255, 255, 255), outline=acc, width=2)

    dr.rounded_rectangle([x0 - 10, y0 + h_banda - 30, Wp - x0 + 10, y0 + h_banda + 30],
                         20, fill=_tint(acc, 0.6))

    if nombre:
        fs = 56
        while _font(fs).getbbox(nombre)[2] > w_corona - 80 and fs > 24:
            fs -= 3
        dr.text((Wp / 2, y0 + h_banda), nombre, font=_font(fs), fill=(255, 255, 255), anchor="mm")

    for side in (-1, 1):
        sx = Wp / 2 + side * (w_corona / 2 + 30)
        dr.line([sx, y0 + h_banda + 30, sx + side * 30, y0 + h_banda + 30],
                fill=acc, width=3)

    dr.line([x0 - 10, y0 + h_banda + 60, Wp - x0 + 10, y0 + h_banda + 60],
            fill=(180, 180, 180), width=2,)
    for x in range(int(x0 - 10), int(Wp - x0 + 10), 15):
        dr.line([x, y0 + h_banda + 60, x + 7, y0 + h_banda + 60], fill=(180, 180, 180), width=2)

    dr.text((x0 - 10, y0 + h_banda + 75), "← Doblar", font=_font(18, False), fill=(150, 150, 150))
    dr.text((Wp - x0 + 10, y0 + h_banda + 75), "Doblar →", font=_font(18, False), fill=(150, 150, 150), anchor="ra")

    _draw_instrucciones_en(im, dr, Wp / 2, y0 + h_banda + 180, acc)

    dr.text((Wp / 2, Hp - 40), "casatridimensional.com.ar", font=_font(18, False), fill=(180, 180, 180), anchor="mm")
    return im


def piezas(data, tema="safari"):
    """Ambos estilos: gorro + corona en 2 páginas."""
    return [("1_gorro", lambda d: gorro(d, tema), True),
            ("2_corona", lambda d: corona(d, tema), True)]


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Mateo"
    edad = sys.argv[3] if len(sys.argv) > 3 else "5"
    out = sys.argv[4] if len(sys.argv) > 4 else "/tmp/corona"
    gorro({"nombre": nombre, "edad": edad}, tema).convert("RGB").save(f"{out}_gorro.png")
    corona({"nombre": nombre, "edad": edad}, tema).convert("RGB").save(f"{out}_corona.png")
    print(f"OK -> {out}_gorro.png + {out}_corona.png")
