#!/usr/bin/env python3
"""
Motor de personalizacion — Kit Safari "Un Anito Salvaje" (CT3D)
---------------------------------------------------------------
Toma una PLANTILLA (mapa de capas de arte + campos de texto con coordenadas)
y los DATOS del cliente, y produce la pieza personalizada lista para imprimir.

- Render server-side con Pillow (calidad imprenta 300 DPI).
- El mismo SPEC (coordenadas en fracciones) lo va a reusar el preview en vivo
  del front-end, asi la posicion en pantalla y en el PDF coinciden exacto.

Uso:
    python3 generador.py            # render de ejemplo (datos demo)
"""
import os, copy, json
from PIL import Image, ImageDraw, ImageFont

BASEDIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = "/root/ct3d-personalizador/recortes"   # arte ya recortado (fondo limpio)
FONTS  = "/root/ct3d-personalizador/fonts"
OUT    = "/root/ct3d-personalizador/salida"

# ---- Paleta de marca ----
CREAM = (244, 239, 230)
BROWN = (111, 78, 55)
TERRA = (200, 103, 78)
OLIVE = (107, 122, 79)

DPI = 300
# 5 x 7 pulgadas a 300 DPI
W, H = 1500, 2100

# ----------------------------------------------------------------------------
# Las piezas (specs) se cargan desde la TEMÁTICA por defecto (temas/<id>/tema.json):
# cada spec trae sus campos de texto, su imagen de fondo por edad y su layout.
# El motor es genérico; la temática vive en disco (multi-temática).
# ----------------------------------------------------------------------------
import temas
TEMA_DEFAULT = "safari"
_tema = temas.cargar_tema(TEMA_DEFAULT)
SPECS = _tema["specs"]
SPECS["cartel"] = SPECS["afiche"]   # el afiche es el cartel de bienvenida
SPEC = SPECS["invitacion"]

# cache de specs por temática (la default ya está cargada)
_specs_cache = {TEMA_DEFAULT: SPECS}
def specs_de(tema):
    """Devuelve los specs de una temática (cargándola si hace falta)."""
    if not tema or not temas.existe(tema):
        tema = TEMA_DEFAULT
    if tema not in _specs_cache:
        s = temas.cargar_tema(tema)["specs"]
        if "afiche" in s:
            s["cartel"] = s["afiche"]
        _specs_cache[tema] = s
    return _specs_cache[tema]

# ---- helpers de imagen ----
def crop_alpha(im):
    bb = im.getbbox()
    return im.crop(bb) if bb else im

def place(base, im, anchor, x, y, w_frac, W, H):
    """Pega im sobre base. anchor: 2 chars (h: l/m/r, v: t/m/b). x,y,w en fracciones."""
    im = crop_alpha(im.convert("RGBA"))
    target_w = int(W * w_frac)
    s = target_w / im.width
    im = im.resize((target_w, max(1, int(im.height * s))), Image.LANCZOS)
    px, py = int(W * x), int(H * y)
    h, v = anchor[0], anchor[1]
    ox = {"l": 0, "m": im.width // 2, "r": im.width}[h]
    oy = {"t": 0, "m": im.height // 2, "b": im.height}[v]
    base.alpha_composite(im, (px - ox, py - oy))

# ---- helpers de fuente ----
_font_cache = {}
# Poppins es estática: el grosor se logra cambiando de archivo
_POPPINS = {400: "Poppins-Regular.ttf", 500: "Poppins-Medium.ttf",
            600: "Poppins-SemiBold.ttf", 700: "Poppins-Bold.ttf"}

# Catálogo de tipografías que el cliente puede elegir (mini-editor). Cada entrada
# existe como .ttf en FONTS y se carga igual en el canvas (CSS family) y en
# Pillow (file). `kind`: display = títulos/nombre, body = datos.
FONTS_CATALOG = [
    {"file": "DancingScript-VF.ttf", "family": "DancingScript", "label": "Manuscrita", "kind": "display"},
    {"file": "Pacifico-Regular.ttf", "family": "Pacifico",      "label": "Cursiva",    "kind": "display"},
    {"file": "Fredoka-VF.ttf",       "family": "Fredoka",       "label": "Redondeada", "kind": "display"},
    {"file": "Baloo2-VF.ttf",        "family": "Baloo2",        "label": "Globo",      "kind": "display"},
    {"file": "Poppins-Medium.ttf",   "family": "Poppins",       "label": "Limpia",     "kind": "body"},
    {"file": "Nunito-VF.ttf",        "family": "Nunito",        "label": "Suave",      "kind": "body"},
    {"file": "LuckiestGuy.ttf",      "family": "LuckiestGuy",   "label": "Cartel",     "kind": "display"},
    {"file": "BreeSerif-Regular.ttf","family": "BreeSerif",     "label": "Cuento",     "kind": "display"},
    {"file": "Rye-Regular.ttf",      "family": "Rye",          "label": "Circo",      "kind": "display"},
    {"file": "Quicksand-VF.ttf",     "family": "Quicksand",    "label": "Redonda",    "kind": "body"},
    {"file": "Bungee-Regular.ttf",   "family": "Bungee",       "label": "Obra",       "kind": "display"},
    {"file": "Montserrat-VF.ttf",    "family": "Montserrat",   "label": "Moderna",    "kind": "body"},
    {"file": "Bangers-Regular.ttf",  "family": "Bangers",      "label": "Comic",      "kind": "display"},
]
_FONT_FILES = {f["file"] for f in FONTS_CATALOG}
_FILE_TO_FAMILY = {f["file"]: f["family"] for f in FONTS_CATALOG}

def _resolve_font_file(fname, wght):
    if fname.startswith("Poppins") and wght:
        nearest = min(_POPPINS, key=lambda k: abs(k - wght))
        return _POPPINS[nearest]
    return fname

def get_font(fname, size, wght=None, wdth=None):
    key = (fname, size, wght, wdth)
    if key in _font_cache:
        return _font_cache[key]
    fname = _resolve_font_file(fname, wght)
    f = ImageFont.truetype(os.path.join(FONTS, fname), size)
    try:
        axes = f.get_variation_axes()
        if axes:
            vals = []
            for a in axes:
                nm = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
                nl = nm.lower()
                if nl == "weight":
                    vals.append(wght if wght is not None else a["default"])
                elif nl == "width":
                    vals.append(wdth if wdth is not None else a["default"])
                else:
                    vals.append(a["default"])
            f.set_variation_by_axes(vals)
    except Exception:
        pass
    _font_cache[key] = f
    return f

def fit_font(draw, text, fname, size, maxw_px, wght=None):
    """Achica la fuente hasta que el texto entre en maxw_px (auto-ajuste)."""
    s = size
    while s > 10:
        f = get_font(fname, s, wght)
        w = draw.textlength(text, font=f)
        if w <= maxw_px:
            return f
        s -= 2
    return get_font(fname, s, wght)

def draw_icon(d, kind, cx, cy, s, color):
    """Iconitos de línea para fecha/hora/lugar, con variantes de forma.
    fecha: calendar / calendar2 · hora: clock / clock2 · lugar: pin / pin2."""
    w = max(2, int(s * 0.075))
    half = s / 2
    l, t, r, b = cx - half, cy - half, cx + half, cy + half
    if kind == "calendar":
        d.rounded_rectangle([l, t + s * 0.12, r, b], radius=s * 0.12, outline=color, width=w)
        d.line([l, t + s * 0.34, r, t + s * 0.34], fill=color, width=w)
        d.line([l + s * 0.27, t, l + s * 0.27, t + s * 0.22], fill=color, width=w)
        d.line([r - s * 0.27, t, r - s * 0.27, t + s * 0.22], fill=color, width=w)
    elif kind == "calendar2":   # calendario con cabecera llena (estilo "día")
        d.rounded_rectangle([l, t + s * 0.12, r, b], radius=s * 0.12, outline=color, width=w)
        d.rounded_rectangle([l, t + s * 0.12, r, t + s * 0.40], radius=s * 0.12, fill=color)
        d.line([l + s * 0.27, t, l + s * 0.27, t + s * 0.20], fill=color, width=w)
        d.line([r - s * 0.27, t, r - s * 0.27, t + s * 0.20], fill=color, width=w)
    elif kind == "clock":
        d.ellipse([l, t, r, b], outline=color, width=w)
        d.line([cx, cy, cx, cy - s * 0.30], fill=color, width=w)
        d.line([cx, cy, cx + s * 0.22, cy + s * 0.04], fill=color, width=w)
    elif kind == "clock2":      # despertador (campanitas + patitas)
        cr = s * 0.36
        d.ellipse([cx - cr, cy - cr * 0.78, cx + cr, cy + cr * 1.0], outline=color, width=w)
        d.line([cx, cy + cr * 0.1, cx, cy - cr * 0.45], fill=color, width=w)
        d.line([cx, cy + cr * 0.1, cx + cr * 0.4, cy + cr * 0.1], fill=color, width=w)
        d.arc([cx - cr - s * 0.16, t - s * 0.04, cx - cr * 0.2, t + s * 0.30], 200, 320, fill=color, width=w)
        d.arc([cx + cr * 0.2, t - s * 0.04, cx + cr + s * 0.16, t + s * 0.30], 220, 340, fill=color, width=w)
        d.line([cx - cr * 0.7, cy + cr * 0.95, cx - cr, b], fill=color, width=w)
        d.line([cx + cr * 0.7, cy + cr * 0.95, cx + cr, b], fill=color, width=w)
    elif kind == "pin":
        cr = s * 0.32
        ct = t + cr
        d.ellipse([cx - cr, t, cx + cr, t + 2 * cr], outline=color, width=w)
        d.line([cx - cr * 0.78, ct + cr * 0.5, cx, b], fill=color, width=w)
        d.line([cx + cr * 0.78, ct + cr * 0.5, cx, b], fill=color, width=w)
        d.ellipse([cx - cr * 0.28, ct - cr * 0.28, cx + cr * 0.28, ct + cr * 0.28], fill=color)
    elif kind == "pin2":        # casita (techo + cuerpo)
        d.line([l + s * 0.06, cy - s * 0.02, cx, t + s * 0.04], fill=color, width=w)
        d.line([cx, t + s * 0.04, r - s * 0.06, cy - s * 0.02], fill=color, width=w)
        d.rectangle([l + s * 0.16, cy - s * 0.02, r - s * 0.16, b - s * 0.06], outline=color, width=w)
        d.rectangle([cx - s * 0.07, cy + s * 0.12, cx + s * 0.07, b - s * 0.06], outline=color, width=w)

_ICON_KINDS = {"calendar", "calendar2", "clock", "clock2", "pin", "pin2"}
# catálogo para el editor del cliente (qué iconos ofrecer por dato)
ICONS_CATALOG = [
    {"kind": "calendar",  "para": "fecha", "label": "Calendario"},
    {"kind": "calendar2", "para": "fecha", "label": "Día"},
    {"kind": "clock",     "para": "hora",  "label": "Reloj"},
    {"kind": "clock2",    "para": "hora",  "label": "Despertador"},
    {"kind": "pin",       "para": "lugar", "label": "Ubicación"},
    {"kind": "pin2",      "para": "lugar", "label": "Casita"},
]
def _hex_rgb(h):
    try:
        h = str(h).lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except Exception:
        return None

def _field_text(field, data):
    """Texto a dibujar: el custom del cliente (_text) tiene prioridad sobre el tpl."""
    t = field.get("_text")
    if t is None:
        t = field["tpl"].format(**data)
    # plural inteligente de la edad: "1 año" / "5 años"
    if "{edad}" in field.get("tpl", "") and str(data.get("edad", "")).strip() == "1":
        t = t.replace(" años", " año")
    return t

_CREAM = (248, 245, 239)
def _hex2rgb(c):
    c = str(c).lstrip("#")
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

def draw_slime(draw, cx, cy, tw, th, hexcolor, alpha=0.5):
    """Mancha de slime semitransparente detrás del nombre (verde mezclado sobre el crema,
    con bumps orgánicos y goteras). Pensada para los temas de monstruos."""
    import math
    g = _hex2rgb(hexcolor)
    col = tuple(int(g[i] * alpha + _CREAM[i] * (1 - alpha)) for i in range(3))
    rw = tw * 0.58 + th * 0.55          # semi-ancho
    rh = th * 0.85                       # semi-alto
    draw.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=col)
    nb = 11                              # bumps alrededor (aspecto orgánico)
    for i in range(nb):
        a = 2 * math.pi * i / nb + 0.4
        bx = cx + rw * 0.93 * math.cos(a)
        by = cy + rh * 0.93 * math.sin(a)
        br = th * (0.30 + 0.14 * ((i * 41) % 7) / 7.0)
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=col)
    for dx, dy, dr in [(-rw*0.45, rh*1.05, th*0.26), (rw*0.05, rh*1.35, th*0.20),
                        (rw*0.5, rh*1.0, th*0.22), (-rw*0.05, rh*0.95, th*0.3)]:
        draw.ellipse([cx+dx-dr, cy+dy-dr, cx+dx+dr, cy+dy+dr], fill=col)   # goteras

def _leaf(draw, x, y, s, ang, color):
    """Hojita: rombo/lente apuntado, rotado un ángulo (rad), + nervadura."""
    import math
    pts = [(0, 0), (s*0.5, -s*0.32), (s, 0), (s*0.5, s*0.32)]
    ca, sa = math.cos(ang), math.sin(ang)
    rot = [(x + px*ca - py*sa, y + px*sa + py*ca) for px, py in pts]
    draw.polygon(rot, fill=color)

def draw_woodsign(draw, cx, cy, tw, th, fill="#D9B98E", border="#8B5E3C",
                  grain="#C8A372", leaf="#4E7D43"):
    """Cartel de madera detrás del nombre: tablón redondeado con borde, vetas y
    hojitas en las esquinas superiores. Estética bosque/campamento (reutilizable)."""
    px = th * 0.7; py = th * 0.5
    l, t, r, b = cx - tw/2 - px, cy - th/2 - py, cx + tw/2 + px, cy + th/2 + py
    rad = th * 0.32; bw = max(3, int(th * 0.07))
    draw.rounded_rectangle([l, t, r, b], radius=rad, fill=fill, outline=border, width=bw)
    gw = max(1, int(th * 0.025))
    for i in range(1, 4):                         # vetas horizontales sutiles
        gy = t + (b - t) * i / 4.0
        draw.line([l + rad*0.6, gy, r - rad*0.6, gy], fill=grain, width=gw)
    ls = th * 0.55                                # hojitas en las 2 esquinas de arriba
    _leaf(draw, l + rad*0.2, t + rad*0.1, ls, -2.5, leaf)
    _leaf(draw, l + rad*0.2, t + rad*0.1, ls*0.8, -1.9, leaf)
    _leaf(draw, r - rad*0.2, t + rad*0.1, ls, -0.6, leaf)
    _leaf(draw, r - rad*0.2, t + rad*0.1, ls*0.8, -1.2, leaf)

def _star(draw, cx, cy, r, color):
    import math
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = -math.pi/2 + i * math.pi/5
        pts.append((cx + rr*math.cos(a), cy + rr*math.sin(a)))
    draw.polygon(pts, fill=color)

def draw_circoplaca(draw, cx, cy, tw, th, fill="#D9624C", border="#F4C95D",
                    star="#F4C95D", shadow="#7A3B2E"):
    """Placa central tipo cartel de circo: rojo vintage, doble borde dorado,
    estrellas a los lados y sombra suave. Detrás del nombre (reutilizable)."""
    px = th * 0.75; py = th * 0.5
    l, t, r, b = cx - tw/2 - px, cy - th/2 - py, cx + tw/2 + px, cy + th/2 + py
    rad = th * 0.3; bw = max(4, int(th * 0.09))
    off = int(th * 0.07)
    draw.rounded_rectangle([l+off, t+off, r+off, b+off], radius=rad, fill=shadow)   # sombra
    draw.rounded_rectangle([l, t, r, b], radius=rad, fill=fill, outline=border, width=bw)
    iw = max(2, int(th*0.03)); ins = bw + th*0.10                                   # borde interno fino
    draw.rounded_rectangle([l+ins, t+ins, r-ins, b-ins], radius=rad*0.7, outline=border, width=iw)
    sr = th * 0.34                                                                  # estrellas a los lados
    for sy in (t + (b-t)*0.5,):
        _star(draw, l - sr*0.2, sy, sr, star)
        _star(draw, r + sr*0.2, sy, sr, star)

def _bolt(draw, x, y, r, color="#888888", dark="#2F2F2F"):
    draw.ellipse([x-r, y-r, x+r, y+r], fill=color, outline=dark, width=max(2, int(r*0.28)))
    draw.line([x-r*0.5, y, x+r*0.5, y], fill=dark, width=max(2, int(r*0.28)))   # ranura

def draw_obrasign(draw, cx, cy, tw, th, fill="#F2B632", border="#2F2F2F", bolt="#9A9A9A"):
    """Cartel de obra amarillo: borde negro grueso y tornillos en las 4 esquinas.
    Estética construcción/maquinaria (reutilizable)."""
    px = th * 0.7; py = th * 0.5
    l, t, r, b = cx - tw/2 - px, cy - th/2 - py, cx + tw/2 + px, cy + th/2 + py
    rad = th * 0.16; bw = max(5, int(th * 0.11))
    draw.rounded_rectangle([l, t, r, b], radius=rad, fill=fill, outline=border, width=bw)
    br = th * 0.16; ins = bw + br
    for bx, by in [(l+ins, t+ins), (r-ins, t+ins), (l+ins, b-ins), (r-ins, b-ins)]:
        _bolt(draw, bx, by, br, bolt, border)

def draw_splatter(draw, cx, cy, tw, th, colors):
    """Salpicaduras de pintura alrededor del nombre (tema artistas)."""
    spots = [(-0.62,-0.55,0.22),(0.58,-0.5,0.3),(-0.45,0.62,0.26),(0.5,0.64,0.2),
             (-0.72,0.12,0.16),(0.74,0.08,0.24),(-0.3,-0.72,0.14),(0.28,-0.66,0.18),
             (0.0,0.8,0.16),(-0.58,-0.2,0.12),(0.66,-0.18,0.13),(0.15,0.72,0.1),
             (-0.2,0.68,0.12),(0.4,-0.62,0.1),(-0.5,0.36,0.1),(0.56,0.36,0.14)]
    rw = tw/2 + th*0.55; rh = th*1.1
    for i,(fx,fy,fr) in enumerate(spots):
        col = colors[i % len(colors)]
        dx = cx + fx*rw; dy = cy + fy*rh; r = fr*th
        draw.ellipse([dx-r,dy-r,dx+r,dy+r], fill=col)
        r2 = r*0.4; ox = r*1.5*(1 if i%2 else -1)
        draw.ellipse([dx+ox-r2,dy-r2,dx+ox+r2,dy+r2], fill=col)

def _draw_multicolor(draw, x, y, text, font, colors, anchor, sw, sf):
    """Cada letra en un color distinto (pinceladas). Avanza char por char."""
    tw = draw.textlength(text, font=font)
    h, v = anchor[0], anchor[1]
    cur = x - tw/2 if h == "m" else (x if h == "l" else x - tw)
    ci = 0
    for ch in text:
        cw = draw.textlength(ch, font=font)
        if ch.strip():
            col = colors[ci % len(colors)]; ci += 1
            draw.text((cur, y), ch, font=font, fill=col, anchor="l"+v,
                      stroke_width=sw, stroke_fill=sf)
        cur += cw

def _bolt_shape(cx, cy, s):
    pts = [(0.18,-1.0),(-0.38,0.08),(0.02,0.08),(-0.28,1.0),(0.4,-0.12),(0.0,-0.12),(0.28,-1.0)]
    return [(cx+px*s, cy+py*s) for px,py in pts]

def draw_heroshield(draw, cx, cy, tw, th, fill="#3B82F6", border="#F6C445",
                    bolt="#F6C445", shadow="#1E3A6E"):
    """Insignia hexagonal tipo escudo de héroe: azul, borde dorado, sombra y
    rayos a los costados. Detrás del nombre (tema superhéroes)."""
    padx = th * 0.8; pady = th * 0.5
    Wd = tw + 2*padx; Hd = th + 2*pady; notch = Hd * 0.5
    def hexpts(ox, oy):
        return [(cx-Wd/2+ox, cy+oy), (cx-Wd/2+notch+ox, cy-Hd/2+oy),
                (cx+Wd/2-notch+ox, cy-Hd/2+oy), (cx+Wd/2+ox, cy+oy),
                (cx+Wd/2-notch+ox, cy+Hd/2+oy), (cx-Wd/2+notch+ox, cy+Hd/2+oy)]
    off = int(th * 0.08); bw = max(5, int(th * 0.1))
    draw.polygon(hexpts(off, off), fill=shadow)                 # sombra
    draw.polygon(hexpts(0, 0), fill=fill, outline=border, width=bw)
    bs = th * 0.55                                              # rayos a los costados
    draw.polygon(_bolt_shape(cx - Wd/2 - bs*0.7, cy, bs), fill=bolt)
    draw.polygon(_bolt_shape(cx + Wd/2 + bs*0.7, cy, bs), fill=bolt)

# Decoraciones temáticas detrás del nombre (marco): el cliente las puede apagar
# desde el editor (override "marco": false) y se quitan todas de ese campo.
DECOR_KEYS = ("slime", "woodsign", "circoplaca", "obrasign", "heroshield",
              "splatter", "band")


def draw_text(draw, field, data, W, H):
    text = _field_text(field, data)
    if not text.strip():
        return
    maxw_px = int(W * field.get("maxw", 0.9))
    f = fit_font(draw, text, field["font"], field["size"], maxw_px, field.get("wght"))
    x, y = int(W * field["x"]), int(H * field["y"])
    anchor = field["anchor"]; h, v = anchor[0], anchor[1]
    sw = int(field.get("stroke", 0)); sf = field.get("stroke_color")
    icon = field.get("icon")
    if icon:                                   # icono + texto, según alineación (l/m/r)
        tw = draw.textlength(text, font=f)
        isz = field["size"] * 0.95
        gap = isz * 0.42
        block = isz + gap + tw
        start = x - block / 2 if h == "m" else (x if h == "l" else x - block)
        draw_icon(draw, icon, start + isz / 2, y, isz, field.get("icon_color") or field["color"])
        draw.text((start + isz + gap, y), text, font=f, fill=field["color"], anchor="l" + v,
                  stroke_width=sw, stroke_fill=sf)
    else:
        tw = draw.textlength(text, font=f)
        try: th = f.size
        except Exception: th = field["size"]
        if field.get("woodsign"):              # cartel de madera detrás (bosque/campamento)
            draw_woodsign(draw, x, y, tw, th)
        if field.get("circoplaca"):            # placa de circo (roja, borde dorado, estrellas)
            draw_circoplaca(draw, x, y, tw, th)
        if field.get("obrasign"):              # cartel de obra (amarillo, borde negro, tornillos)
            draw_obrasign(draw, x, y, tw, th)
        if field.get("heroshield"):            # insignia hexagonal de héroe (azul, borde dorado, rayos)
            draw_heroshield(draw, x, y, tw, th)
        if field.get("band"):                  # franja redondeada detrás (estilo cartel/emergencia)
            px0 = th * 0.55; py0 = th * 0.34
            draw.rounded_rectangle([x - tw/2 - px0, y - th/2 - py0, x + tw/2 + px0, y + th/2 + py0],
                                   radius=th * 0.45, fill=field["band"])
        if field.get("slime"):
            draw_slime(draw, x, y, tw, th, field["slime"])
        if field.get("splatter"):              # salpicaduras de pintura (artistas)
            draw_splatter(draw, x, y, tw, th, field["splatter"])
        if field.get("shadow"):                # sombra de color, desplazada
            dx = field["size"] * 0.045; dy = field["size"] * 0.06
            draw.text((x + dx, y + dy), text, font=f, fill=field["shadow"], anchor=anchor,
                      stroke_width=sw, stroke_fill=field["shadow"])
        mc = field.get("multicolor")
        if mc:                                 # cada letra un color (pinceladas)
            _draw_multicolor(draw, x, y, text, f, mc, anchor, sw, sf)
        else:
            draw.text((x, y), text, font=f, fill=field["color"], anchor=anchor,
                      stroke_width=sw, stroke_fill=sf)

def draw_icon_group(draw, fields, data, W, H):
    """Renderiza fecha/hora/lugar con los iconos alineados en columna y el
    texto arrancando todo a la misma x (bloque centrado según la línea más larga)."""
    rows, maxtw = [], 0
    for f in fields:
        text = _field_text(f, data)
        if not text.strip():
            continue
        font = fit_font(draw, text, f["font"], f["size"], int(W * f.get("maxw", 0.9)), f.get("wght"))
        tw = draw.textlength(text, font=font)
        rows.append((f, text, font))
        maxtw = max(maxtw, tw)
    if not rows:
        return
    isz = fields[0]["size"] * 0.95
    gap = isz * 0.42
    left = W * 0.5 - (isz + gap + maxtw) / 2
    icon_cx = left + isz / 2
    text_x = left + isz + gap
    for f, text, font in rows:
        y = int(H * f["y"])
        draw_icon(draw, f["icon"], icon_cx, y, isz, f.get("icon_color") or f["color"])
        draw.text((text_x, y), text, font=font, fill=f["color"], anchor="lm")

# ---- layout editable (editor visual) ----
def _layout_path(spec):
    p = spec.get("layout_file")
    if not p:
        return None
    return p if os.path.isabs(p) else os.path.join(spec.get("_dir", BASEDIR), p)

def _effective_texts(spec):
    """Devuelve los campos de texto con las posiciones/tamaños del editor
    (si existe el archivo de layout), sin tocar los defaults del spec."""
    texts = copy.deepcopy(spec["text"])
    p = _layout_path(spec)
    if p and os.path.exists(p):
        try:
            ov = json.load(open(p, encoding="utf-8"))
            for f in texts:
                o = ov.get(f["id"]) or {}
                for k in ("x", "y", "size", "maxw", "wght"):
                    if k in o:
                        f[k] = o[k]
                fn = o.get("font")
                if fn in _FONT_FILES:                 # tipografía guardada (del catálogo)
                    f["font"] = fn
                if "color" in o:                      # color guardado (hex → rgb)
                    c = _hex_rgb(o["color"])
                    if c: f["color"] = c
                a = o.get("anchor")                   # alineación guardada
                if isinstance(a, str) and len(a) == 2 and a[0] in "lmr" and a[1] in "tmb":
                    f["anchor"] = a
        except Exception:
            pass
    return texts

def bg_path_for(pieza, edad="1", tema=TEMA_DEFAULT):
    """Ruta del fondo de una pieza (resolviendo {edad})."""
    spec = specs_de(tema).get(pieza, SPEC)
    base = spec.get("_dir", BASEDIR)
    p = spec.get("bgimage", "")
    if not p:
        return None
    if "{edad}" in p:
        cand = p.format(edad=str(edad) or "1")
        full = cand if os.path.isabs(cand) else os.path.join(base, cand)
        p = cand if os.path.exists(full) else p.format(edad="1")
    return p if os.path.isabs(p) else os.path.join(base, p)

def layout_file_path(pieza, tema=TEMA_DEFAULT):
    return _layout_path(specs_de(tema).get(pieza, SPEC))

def layout_para_editor(pieza="invitacion", tema=TEMA_DEFAULT):
    """Datos que necesita el editor visual para dibujar y mover cada texto."""
    spec = specs_de(tema).get(pieza, SPEC)
    # ejemplo para mostrar el texto propuesto de cada campo (formateando su tpl)
    ej = {"nombre": "Tomás", "fecha": "Sábado 12 de julio", "hora": "16:00 hs",
          "lugar": "Salón Los Robles", "direccion": "Av. Siempreviva 742",
          "telefono": "11-5555-5555", "edad": "5"}
    def _sample(f):
        try: return f["tpl"].format(**ej)
        except Exception: return ""
    # familia CSS de cada archivo de fuente (cae al catálogo si no está mapeada)
    fams = dict(_FILE_TO_FAMILY)
    fams.setdefault("Poppins-Medium.ttf", "Poppins")
    out = []
    for f in _effective_texts(spec):
        ffile = f["font"]
        marco_kind = next((k for k in DECOR_KEYS if k in f), None)  # tipo de marco o None
        out.append({"id": f["id"], "x": f["x"], "y": f["y"], "size": f["size"],
                    "maxw": f.get("maxw", 0.9), "anchor": f["anchor"],
                    "font": ffile,                      # archivo .ttf actual (para overrides)
                    "family": fams.get(ffile, "sans-serif"), "wght": f.get("wght", 500),
                    "color": "#%02x%02x%02x" % tuple(f["color"]), "sample": _sample(f),
                    "editable": f.get("editable", True), "toggleable": f.get("toggleable", False),
                    "iconable": f.get("iconable", False), "icon": f.get("icon"),
                    "tpl": f.get("tpl", ""),
                    "marco": marco_kind,                # tipo de decoración apagable (o None)
                    "marco_color": f.get("slime") or f.get("band") or f.get("splatter") or "",
                    "default_hidden": f.get("default_hidden", False)})
    return {"size": spec["size"], "fields": out, "pieza": pieza, "tema": tema,
            "piezas": list(specs_de(tema).keys()), "fonts": FONTS_CATALOG, "icons": ICONS_CATALOG}

# ---- render principal ----
def render(data, spec=None):
    spec = spec or SPEC
    scale = spec.get("render_scale", 1.0)   # renderiza a mayor resolución sin cambiar el layout
    W, H = int(spec["size"][0] * scale), int(spec["size"][1] * scale)
    if spec.get("bgimage"):
        bdir = spec.get("_dir", BASEDIR)
        p = spec["bgimage"]
        if "{edad}" in p:                       # fondo según la edad elegida
            edad = str(data.get("edad", "1")).strip() or "1"
            cand = p.format(edad=edad)
            full = cand if os.path.isabs(cand) else os.path.join(bdir, cand)
            p = cand if os.path.exists(full) else p.format(edad="1")  # fallback a 1
        if not os.path.isabs(p):
            p = os.path.join(bdir, p)
        base = Image.open(p).convert("RGBA")
        if base.size != (W, H):
            base = base.resize((W, H), Image.LANCZOS)
    else:
        base = Image.new("RGBA", (W, H), spec["bg"] + (255,))
    for layer in spec["art"]:
        im = Image.open(os.path.join(ASSETS, layer["file"]))
        place(base, im, layer["anchor"], layer["x"], layer["y"], layer["w"], W, H)
    draw = ImageDraw.Draw(base)
    texts = _effective_texts(spec)
    # campo que "adopta" la posición/config de otro cuando ese otro está vacío
    byid = {f["id"]: f for f in texts}
    for f in texts:
        src = f.get("adopts_if_empty")
        if src and src in byid and not str(data.get(src, "")).strip():
            for k in ("x", "y", "size", "maxw", "wght", "anchor"):
                if k in byid[src]:
                    f[k] = byid[src][k]
    # overrides del cliente (mini-editor):
    #   data["_over"][campo] = {x,y,size,maxw,wght,font,color,icon,hidden,text}
    # se mezclan sobre tu layout. La tipografía/iconos se validan contra el catálogo.
    over = data.get("_over") or {}
    if over:
        for f in texts:
            o = over.get(f["id"]) or {}
            for k in ("x", "y", "size", "maxw", "wght"):
                if k in o:
                    try: f[k] = float(o[k])
                    except (TypeError, ValueError): pass
            fn = o.get("font")
            if fn in _FONT_FILES:          # solo fuentes del catálogo (existen como .ttf)
                f["font"] = fn
            if "color" in o:
                c = _hex_rgb(o["color"])
                if c: f["color"] = c
            if "icon" in o:                # icono junto al dato, o ninguno
                f["icon"] = o["icon"] if o["icon"] in _ICON_KINDS else None
            if "text" in o and isinstance(o["text"], str):
                f["_text"] = o["text"]
            a = o.get("anchor")
            if isinstance(a, str) and len(a) == 2 and a[0] in "lmr" and a[1] in "tmb":
                f["anchor"] = a
            if o.get("hidden"):            # el cliente decidió no incluir este dato
                f["_hidden"] = True
            if o.get("marco") is False:    # el cliente apagó el marco decorativo del nombre
                for dk in DECOR_KEYS:
                    f.pop(dk, None)
    if scale != 1.0:                        # escala los tamaños de fuente junto con el canvas
        for f in texts:
            f["size"] = f["size"] * scale
    texts = [f for f in texts if not f.get("_hidden")]   # ocultos: no se dibujan
    group = [f for f in texts if f.get("icongroup")]
    for field in texts:
        if not field.get("icongroup"):
            draw_text(draw, field, data, W, H)
    if group:
        draw_icon_group(draw, group, data, W, H)
    return base.convert("RGB")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    demo = {
        "nombre": "Tomás",
        "fecha": "Sábado 12 de julio",
        "hora": "16:00 hs",
        "lugar": "Salón Los Robles",
        "telefono": "11-5555-5555",
    }
    img = render(demo)
    png = os.path.join(OUT, "invitacion_demo.png")
    pdf = os.path.join(OUT, "invitacion_demo.pdf")
    img.save(png, "PNG")
    img.save(pdf, "PDF", resolution=DPI)
    print("OK ->", png)
    print("OK ->", pdf, f"({W}x{H}px @ {DPI}dpi = 5x7in)")
