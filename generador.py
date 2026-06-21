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
    """Iconitos de línea (calendario / reloj / pin) para fecha/hora/lugar."""
    w = max(2, int(s * 0.075))
    half = s / 2
    l, t, r, b = cx - half, cy - half, cx + half, cy + half
    if kind == "calendar":
        d.rounded_rectangle([l, t + s * 0.12, r, b], radius=s * 0.12, outline=color, width=w)
        d.line([l, t + s * 0.34, r, t + s * 0.34], fill=color, width=w)
        d.line([l + s * 0.27, t, l + s * 0.27, t + s * 0.22], fill=color, width=w)
        d.line([r - s * 0.27, t, r - s * 0.27, t + s * 0.22], fill=color, width=w)
    elif kind == "clock":
        d.ellipse([l, t, r, b], outline=color, width=w)
        d.line([cx, cy, cx, cy - s * 0.30], fill=color, width=w)
        d.line([cx, cy, cx + s * 0.22, cy + s * 0.04], fill=color, width=w)
    elif kind == "pin":
        cr = s * 0.32
        ct = t + cr
        d.ellipse([cx - cr, t, cx + cr, t + 2 * cr], outline=color, width=w)
        d.line([cx - cr * 0.78, ct + cr * 0.5, cx, b], fill=color, width=w)
        d.line([cx + cr * 0.78, ct + cr * 0.5, cx, b], fill=color, width=w)
        d.ellipse([cx - cr * 0.28, ct - cr * 0.28, cx + cr * 0.28, ct + cr * 0.28], fill=color)

def draw_text(draw, field, data, W, H):
    text = field["tpl"].format(**data)
    if not text.strip():
        return
    maxw_px = int(W * field.get("maxw", 0.9))
    f = fit_font(draw, text, field["font"], field["size"], maxw_px, field.get("wght"))
    x, y = int(W * field["x"]), int(H * field["y"])
    icon = field.get("icon")
    if icon and field["anchor"] == "mm":
        tw = draw.textlength(text, font=f)
        isz = field["size"] * 0.95
        gap = isz * 0.42
        start = x - (isz + gap + tw) / 2
        draw_icon(draw, icon, start + isz / 2, y, isz, field["color"])
        draw.text((start + isz + gap, y), text, font=f, fill=field["color"], anchor="lm")
    else:
        draw.text((x, y), text, font=f, fill=field["color"], anchor=field["anchor"])

def draw_icon_group(draw, fields, data, W, H):
    """Renderiza fecha/hora/lugar con los iconos alineados en columna y el
    texto arrancando todo a la misma x (bloque centrado según la línea más larga)."""
    rows, maxtw = [], 0
    for f in fields:
        text = f["tpl"].format(**data)
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
        draw_icon(draw, f["icon"], icon_cx, y, isz, f["color"])
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
    samples = {"nombre": "Tomás", "fecha": "Sábado 12 de julio", "hora": "16:00 hs",
               "lugar": "Salón Los Robles", "direccion": "Av. Siempreviva 742", "rsvp": "11-5555-5555"}
    fams = {"DancingScript-VF.ttf": "DancingScript", "Poppins-Medium.ttf": "Poppins",
            "Fredoka-VF.ttf": "Fredoka"}
    out = []
    for f in _effective_texts(spec):
        out.append({"id": f["id"], "x": f["x"], "y": f["y"], "size": f["size"],
                    "maxw": f.get("maxw", 0.9), "anchor": f["anchor"],
                    "family": fams.get(f["font"], "sans-serif"), "wght": f.get("wght", 500),
                    "color": "#%02x%02x%02x" % tuple(f["color"]), "sample": samples.get(f["id"], "")})
    return {"size": spec["size"], "fields": out, "pieza": pieza, "tema": tema,
            "piezas": list(specs_de(tema).keys())}

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
    if scale != 1.0:                        # escala los tamaños de fuente junto con el canvas
        for f in texts:
            f["size"] = f["size"] * scale
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
