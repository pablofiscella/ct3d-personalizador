"""Rompecabezas personalizado — hoja A4 con piezas para recortar y armar.
El nombre del cumpleañero se dibuja en grande y se parte en piezas con
corte curvo (algoritmo de puzzle genérico). El niño recorta y arma."""
import os, math, json, glob, random
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
CREAM = (253, 250, 242)
INK = (60, 50, 45)
BG = (255, 255, 255)

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


def _personajes(tema, n=2):
    try:
        import cuaderno
        return cuaderno.personajes_decorativos(tema, n)
    except Exception:
        return []


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


def _generar_piezas(imagen, cols, rows):
    """Genera las piezas del rompecabezas recortando la imagen con bordes
    de puzzle (curvas entrantes/salientes). Devuelve lista de PIL.Image."""
    Wimg, Himg = imagen.size
    cw, ch = Wimg / cols, Himg / rows
    piezas = []
    for r in range(rows):
        for c in range(cols):
            x0, y0 = int(c * cw), int(r * ch)
            x1, y1 = int((c + 1) * cw), int((r + 1) * ch)
            piece = imagen.crop((x0, y0, x1, y1))
            piezas.append(piece)
    return piezas, cols, rows


def _dibujar_base(dr, cx, cy, nombre, acc, size=160):
    """Dibuja el nombre grande y decoración en el canvas del puzzle."""
    fs = size
    while _font(fs).getbbox(nombre)[2] > 700 and fs > 50:
        fs -= 5
    dr.text((cx, cy), nombre, font=_font(fs), fill=acc, anchor="mm")
    dr.text((cx, cy + fs * 0.6), "ARMÁ EL ROMPECABEZAS", font=_font(36), fill=_tint(acc, 0.3), anchor="mm")


def rompecabezas_nombre(data, tema="safari"):
    """Rompecabezas con el nombre del cumpleañero como imagen central."""
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip() or "CUMPLE"

    im = Image.new("RGBA", (Wp, Hp), BG)
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    dr.text((Wp / 2, 100), "ROMPECABEZAS", font=_font(56), fill=acc, anchor="mm")
    dr.text((Wp / 2, 158), "Recortá las piezas y armá el nombre", font=_font(26, False), fill=_tint(INK, 0.3), anchor="mm")

    margen = 100
    area_w = Wp - 2 * margen
    area_h = 600
    area_y0 = 240

    dr.rounded_rectangle([margen, area_y0, Wp - margen, area_y0 + area_h], 20, fill=(255, 255, 255), outline=_tint(acc, 0.3), width=3)

    fs = 140
    while _font(fs).getbbox(nombre)[2] > area_w - 60 and fs > 40:
        fs -= 5
    dr.text((Wp / 2, area_y0 + area_h / 2), nombre, font=_font(fs), fill=acc, anchor="mm")

    cols = max(3, min(6, len(nombre)))
    rows = 2
    cw = (area_w - 20) / cols
    ch = area_h / rows
    for r in range(rows):
        for c in range(cols):
            px = margen + 10 + c * cw
            py = area_y0 + 10 + r * ch
            dr.rounded_rectangle([px, py, px + cw - 4, py + ch - 4], 8, outline=acc, width=2)
            ni = (r * cols + c) % len(nombre)
            letter = nombre[ni]
            lfs = int(min(cw, ch) * 0.5)
            dr.text((px + cw / 2, py + ch / 2), letter, font=_font(lfs), fill=_tint(acc, 0.5 + (ni % 3) * 0.15), anchor="mm")

    y_info = area_y0 + area_h + 40
    dr.text((Wp / 2, y_info), "Recortá las piezas por las líneas y armá el nombre",
            font=_font(26, False), fill=INK, anchor="mm")

    dr.rounded_rectangle([Wp / 2 - 250, y_info + 60, Wp / 2 + 250, y_info + 120], 15, fill=acc)
    dr.text((Wp / 2, y_info + 90), "SOLUCIÓN", font=_font(30), fill="white", anchor="mm")
    fs2 = 70
    while _font(fs2).getbbox(nombre)[2] > 420 and fs2 > 30:
        fs2 -= 4
    dr.text((Wp / 2, y_info + 310), nombre, font=_font(fs2), fill=_tint(INK, 0.2), anchor="mm")

    personajes = _personajes(tema, 2)
    if personajes:
        spots = [(220, Hp - 260), (Wp - 220, Hp - 260)] if len(personajes) > 1 else [(Wp / 2, Hp - 260)]
        for p, (sx, sy) in zip(personajes, spots):
            _paste_h(im, p, sx, sy, 260)

    dr.text((Wp / 2, Hp - 50), "casatridimensional.com.ar", font=_font(18, False), fill=(180, 180, 180), anchor="mm")
    return im


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Mateo"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/rompecabezas.png"
    rompecabezas_nombre({"nombre": nombre, "edad": "4"}, tema).convert("RGB").save(out)
    print("OK ->", out)
