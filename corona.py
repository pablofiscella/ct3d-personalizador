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


def _personajes(tema, n=2):
    try:
        import cuaderno
        return cuaderno.personajes_decorativos(tema, n)
    except Exception:
        return []


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


def _fondo_ia(tema, pieza):
    try:
        import corona_ia
        return corona_ia.cargar_fondo(tema, pieza)
    except Exception:
        return None


def gorro(data, tema="safari"):
    """Gorro cónico de cumpleaños para armar: un sector (abanico) que se recorta y
    se enrolla en cono. El abanico abre HACIA ABAJO y todo el texto va centrado y
    apilado sobre él (antes abría a la derecha y el texto caía sobre el fondo).
    Si el tema tiene un fondo generado con IA (corona_ia), se usa como arte del
    abanico en vez del color liso; si no, cae al relleno procedural de siempre."""
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or ""
    edad = str(data.get("edad") or "").strip()

    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)

    cx, apex_y = Wp / 2, 200
    r = 620
    half = math.radians(55)
    base = math.radians(90)                      # el abanico apunta hacia abajo
    pts = [(cx, apex_y)]
    for i in range(81):
        a = base - half + i * 2 * half / 80
        pts.append((cx + r * math.cos(a), apex_y + r * math.sin(a)))

    fondo = _fondo_ia(tema, "gorro")
    if fondo is not None:
        mask = Image.new("L", (Wp, Hp), 0)
        ImageDraw.Draw(mask).polygon(pts, fill=255)
        art = fondo.resize((Wp, Hp), Image.LANCZOS)
        im.paste(art, (0, 0), mask)
    else:
        dr.polygon(pts, fill=acc + (255,))
    dr.arc([cx - r, apex_y - r, cx + r, apex_y + r],
           math.degrees(base - half), math.degrees(base + half), fill=acc, width=5)
    for s in (-1, 1):                             # bordes = líneas de doblez suaves
        ex = cx + r * math.cos(base + s * half)
        ey = apex_y + r * math.sin(base + s * half)
        dr.line([(cx, apex_y), (ex, ey)], fill=_tint(acc, 0.4), width=2)

    # stroke oscuro en el texto: con fondo IA (no siempre uniforme como el color
    # liso de antes) el blanco solo puede perder legibilidad en zonas claras.
    _tx = dict(stroke_width=4, stroke_fill=(0, 0, 0, 190))
    if edad:
        efs = 150
        while _font(efs).getbbox(edad)[2] > 260 and efs > 70:
            efs -= 4
        dr.text((cx, apex_y + 130), edad, font=_font(efs), fill=(255, 255, 255), anchor="mm", **_tx)
    dr.text((cx, apex_y + 268), "CUMPLEAÑOS", font=_font(46), fill=(255, 255, 255), anchor="mm", **_tx)
    if nombre:
        fs = 76
        while _font(fs).getbbox(nombre)[2] > 520 and fs > 28:
            fs -= 3
        dr.text((cx, apex_y + 344), nombre, font=_font(fs), fill=(255, 255, 255), anchor="mm", **_tx)

    personajes = _personajes(tema, 1)
    if personajes:
        _paste_h(im, personajes[0], cx, apex_y + r - 90, 175)

    _draw_instrucciones(dr, cx, apex_y + r + 130, acc)

    dr.text((cx, Hp - 40), "casatridimensional.com.ar", font=_font(18, False), fill=(180, 180, 180), anchor="mm")
    return im


def corona(data, tema="safari"):
    """Corona de rey/reina para armar. Tira con picos, solapas para pegar.
    Si el tema tiene un fondo generado con IA (corona_ia), se usa como arte de
    los picos + la banda en vez del color liso; si no, cae al color de siempre."""
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or ""

    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    y0 = 160
    h_banda = 220
    w_corona = Wp - 200
    x0 = (Wp - w_corona) / 2
    banda_box = [x0 - 10, y0 + h_banda - 30, Wp - x0 + 10, y0 + h_banda + 30]

    picos = []
    for i in range(7):
        px = x0 + w_corona * (i / 6)
        pico_h = 160 + ((i * 37) % 3) * 30
        picos.append((px, pico_h,
                      [(px - 40, y0 + h_banda), (px, y0 - pico_h + h_banda), (px + 40, y0 + h_banda)]))

    fondo = _fondo_ia(tema, "corona")
    if fondo is not None:
        mask = Image.new("L", (Wp, Hp), 0)
        mdr = ImageDraw.Draw(mask)
        for _px, _ph, pts in picos:
            mdr.polygon(pts, fill=255)
        mdr.rounded_rectangle(banda_box, 20, fill=255)
        art = fondo.resize((Wp, Hp), Image.LANCZOS)
        im.paste(art, (0, 0), mask)
        for _px, _ph, pts in picos:
            dr.polygon(pts, outline=_tint(acc, 0.2), width=3)
    else:
        for _px, _ph, pts in picos:
            dr.polygon(pts, fill=acc, outline=_tint(acc, 0.2), width=3)
        dr.rounded_rectangle(banda_box, 20, fill=_tint(acc, 0.6))

    for px, pico_h, _pts in picos:
        dr.ellipse([px - 18, y0 - pico_h + h_banda - 15, px + 18, y0 - pico_h + h_banda + 15],
                   fill=(255, 255, 255), outline=acc, width=2)

    if nombre:
        fs = 56
        while _font(fs).getbbox(nombre)[2] > w_corona - 80 and fs > 24:
            fs -= 3
        dr.text((Wp / 2, y0 + h_banda), nombre, font=_font(fs), fill=(255, 255, 255),
                 stroke_width=4, stroke_fill=(0, 0, 0, 190), anchor="mm")

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

    personajes = _personajes(tema, 2)
    if personajes:
        spots = [(Wp * 0.3, Hp - 280), (Wp * 0.7, Hp - 280)] if len(personajes) > 1 else [(Wp / 2, Hp - 280)]
        for p, (sx, sy) in zip(personajes, spots):
            _paste_h(im, p, sx, sy, 300)

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
