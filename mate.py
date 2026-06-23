#!/usr/bin/env python3
"""Editor de MATES con grabado láser (vista desde arriba).

El cliente escribe un texto (y opcionalmente una foto) y ve cómo quedaría GRABADO
sobre la virola del mate. Es un producto FÍSICO: esto NO genera un PDF — la
personalización (texto/foto + posición) viaja en el pedido para que Pablo lo grabe
con el láser. El preview es para vender.

- Si existe una foto real del mate en `temas/mate/<id>/foto.png` (+ config.json con
  el radio de la virola), se usa esa. Si no, un mate sintético de muestra.
- El texto se dibuja CURVADO siguiendo la virola, en estilo grabado.
- La foto opcional se reduce a chiquita y se muestra en grabado (alto contraste).
"""
import os, json, math
from PIL import Image, ImageDraw, ImageFont, ImageOps

_PROY = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(_PROY, "fonts")
MATES_DIR = os.path.join(_PROY, "temas", "mate")

GRABADO = (74, 70, 66)        # color del grabado (gris cálido oscuro)
SILVER = (236, 238, 240)
GRAY_BG = (190, 194, 198)


_FONTS_OK = {"Poppins-SemiBold.ttf", "Poppins-Medium.ttf", "Fredoka-VF.ttf",
             "Baloo2-VF.ttf", "DancingScript-VF.ttf", "Pacifico-Regular.ttf"}

def _font(fname, size):
    fname = os.path.basename(fname or "")          # anti path-traversal
    if fname not in _FONTS_OK:
        fname = "Poppins-SemiBold.ttf"
    return ImageFont.truetype(os.path.join(FONTS, fname), int(size))


# ---------------------------------------------------------------------------
# Base del mate (foto real subida, o sintético de muestra)
# ---------------------------------------------------------------------------
def _sintetico(W=1100):
    """Mate de muestra (vista de arriba): fondo gris, virola plateada, madera suave."""
    base = Image.new("RGB", (W, W), GRAY_BG)
    d = ImageDraw.Draw(base)
    cx = cy = W // 2
    rv = int(W * 0.43)   # radio externo virola
    rw = int(W * 0.33)   # radio madera (interno)
    d.ellipse([cx - rv, cy - rv, cx + rv, cy + rv], fill=SILVER, outline=(120, 120, 124), width=4)
    # madera: relleno radial suave (sin moaré)
    for r in range(rw, 0, -1):
        t = 1 - r / rw
        col = (int(168 - 30 * t), int(122 - 22 * t), int(80 - 16 * t))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.ellipse([cx - rw, cy - rw, cx + rw, cy + rw], outline=(120, 95, 60), width=3)
    return base


def cargar(mate_id="demo"):
    """Devuelve (imagen_base, cfg). cfg trae el radio de la virola (fracción de W).
    Usa la foto real si está subida; si no, el mate sintético."""
    d = os.path.join(MATES_DIR, mate_id)
    foto = os.path.join(d, "foto.png")
    if os.path.isfile(foto):
        img = Image.open(foto).convert("RGB")
        # cuadrar
        s = min(img.size)
        img = ImageOps.fit(img, (s, s), Image.LANCZOS)
        cfg = {"r_texto": 0.39, "r_foto": 0.0}
        try:
            cfg.update(json.load(open(os.path.join(d, "config.json"))))
        except Exception:
            pass
        return img, cfg
    return _sintetico(), {"r_texto": 0.378, "r_foto": 0.0}


# ---------------------------------------------------------------------------
# Render del grabado
# ---------------------------------------------------------------------------
def _curved_text(base, text, cx, cy, radius, font, color, spacing=8, pos="arriba", flip=False):
    """Dibuja `text` curvado sobre la virola.
       pos='arriba' → arco superior, legible.
       pos='abajo'  → arco inferior; flip=False letras mirando para abajo (legible desde afuera),
                      flip=True letras mirando para arriba (continúa el aro, se lee girando el mate)."""
    if not text:
        return
    widths = [font.getlength(ch) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    arc = total / radius
    if pos == "arriba":
        ang = -math.pi / 2 - arc / 2; step = 1; rotf = lambda a: -math.degrees(a) - 90
    elif not flip:                       # abajo, mirando para abajo (legible)
        ang = math.pi / 2 + arc / 2; step = -1; rotf = lambda a: -math.degrees(a) + 90
    else:                                # abajo, mirando para arriba (continúa el aro)
        ang = math.pi / 2 - arc / 2; step = 1; rotf = lambda a: -math.degrees(a) - 90
    for i, ch in enumerate(text):
        w = widths[i]; ca = w / radius
        a = ang + step * ca / 2
        x = cx + radius * math.cos(a); y = cy + radius * math.sin(a)
        pad = 12
        ci = Image.new("RGBA", (int(w) + pad * 2, font.size + pad * 2), (0, 0, 0, 0))
        dci = ImageDraw.Draw(ci)
        dci.text((pad + 2, pad + 3), ch, font=font, fill=(255, 255, 255, 130))  # lip claro = grabado incrustado
        dci.text((pad, pad), ch, font=font, fill=color)
        rot = ci.rotate(rotf(a), expand=True, resample=Image.BICUBIC)
        base.paste(rot, (int(x - rot.width / 2), int(y - rot.height / 2)), rot)
        ang += step * (ca + spacing / radius)


def _grabar_foto(base, foto, cx, cy, diam):
    """Pega una foto chiquita en estilo grabado (gris alto contraste) sobre la virola."""
    f = ImageOps.fit(foto.convert("L"), (diam, diam), Image.LANCZOS)
    f = ImageOps.autocontrast(f, cutoff=2)
    # máscara circular
    mask = Image.new("L", (diam, diam), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, diam, diam], fill=255)
    # tinte hacia el color de grabado (no negro puro)
    tint = ImageOps.colorize(f, black=GRABADO, white=(225, 225, 225))
    base.paste(tint, (int(cx - diam / 2), int(cy - diam / 2)), mask)
    ImageDraw.Draw(base).ellipse([cx - diam / 2, cy - diam / 2, cx + diam / 2, cy + diam / 2],
                                 outline=GRABADO, width=3)


def render(texto="", mate_id="demo", font="Poppins-Medium.ttf", size_frac=0.052,
           spacing=8, foto=None, r=None, max_px=1000, texto_abajo="", abajo_flip=False):
    """Render del mate con el grabado. Devuelve PIL RGB.
       - texto: texto de ARRIBA (curvado, legible).
       - texto_abajo: texto de ABAJO; abajo_flip controla si mira para arriba o para abajo.
       - r: radio del texto (fracción del ancho) para centrarlo en la virola; si no, el del config.
       - foto: PIL.Image opcional → se achica chiquita y se graba sobre la virola.
    """
    base, cfg = cargar(mate_id)
    W = base.width
    cx = cy = W // 2
    r_texto = cfg["r_texto"]
    if r is not None:
        try: r_texto = max(0.28, min(0.45, float(r)))
        except Exception: pass
    # foto chiquita arriba-izquierda de la virola si viene
    if foto is not None:
        rf = cfg.get("r_foto") or cfg["r_texto"]
        fx = cx + W * rf * math.cos(-math.pi / 2 - 0.6)
        fy = cy + W * rf * math.sin(-math.pi / 2 - 0.6)
        _grabar_foto(base, foto, fx, fy, int(W * 0.11))
    fnt = _font(font, int(W * size_frac))
    if texto:
        _curved_text(base, texto, cx, cy, int(W * r_texto), fnt, GRABADO, spacing, pos="arriba")
    if texto_abajo:
        _curved_text(base, texto_abajo, cx, cy, int(W * r_texto), fnt, GRABADO, spacing,
                     pos="abajo", flip=abajo_flip)
    if max_px and W > max_px:
        base.thumbnail((max_px, max_px), Image.LANCZOS)
    return base


if __name__ == "__main__":
    img = render("Pablo", "demo")
    out = os.path.join(_PROY, "salida", "mate_test.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out); print("->", out)
