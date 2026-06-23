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
    asc, desc = font.getmetrics()
    cap = asc * 0.70                       # alto aprox. de mayúscula (centro visual)
    pad = 16
    H = int(asc + desc) + pad * 2
    ty = H / 2 - asc + cap / 2             # ubica el CENTRO VISUAL de la letra en H/2
    for i, ch in enumerate(text):
        w = widths[i]; ca = w / radius
        a = ang + step * ca / 2
        x = cx + radius * math.cos(a); y = cy + radius * math.sin(a)
        ci = Image.new("RGBA", (int(w) + pad * 2, H), (0, 0, 0, 0))
        dci = ImageDraw.Draw(ci)
        dci.text((pad + 2, ty + 3), ch, font=font, fill=(255, 255, 255, 130))  # lip claro = grabado incrustado
        dci.text((pad, ty), ch, font=font, fill=color)
        rot = ci.rotate(rotf(a), expand=True, resample=Image.BICUBIC)   # centro visual = centro de la img
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


# ---------------------------------------------------------------------------
# Iconos (línea monocromo, ideales para grabado). Fútbol GENÉRICO (no escudos de clubes).
# ---------------------------------------------------------------------------
def _i_corazon(d, cx, cy, s, c, w):
    p = []
    for i in range(0, 361, 5):
        t = math.radians(i); x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        p.append((cx + x * s / 16, cy - y * s / 16))
    d.line(p + [p[0]], fill=c, width=w, joint="curve")

def _i_estrella(d, cx, cy, s, c, w):
    p = [(cx + (s if k % 2 == 0 else s * 0.45) * math.cos(-math.pi / 2 + k * math.pi / 5),
          cy + (s if k % 2 == 0 else s * 0.45) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
    d.line(p + [p[0]], fill=c, width=w, joint="curve")

def _i_pelota(d, cx, cy, s, c, w):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=c, width=w)
    pent = [(cx + s * 0.34 * math.cos(-math.pi / 2 + k * 2 * math.pi / 5),
             cy + s * 0.34 * math.sin(-math.pi / 2 + k * 2 * math.pi / 5)) for k in range(5)]
    d.line(pent + [pent[0]], fill=c, width=w, joint="curve")
    for px, py in pent:
        a = math.atan2(py - cy, px - cx)
        d.line([(px, py), (cx + s * 0.92 * math.cos(a), cy + s * 0.92 * math.sin(a))], fill=c, width=w)

def _i_escudo(d, cx, cy, s, c, w):
    p = [(cx - s * 0.8, cy - s), (cx + s * 0.8, cy - s), (cx + s * 0.8, cy + s * 0.15),
         (cx, cy + s), (cx - s * 0.8, cy + s * 0.15)]
    d.line(p + [p[0]], fill=c, width=w, joint="curve")

def _i_camiseta(d, cx, cy, s, c, w):
    p = [(cx - s * 0.32, cy - s * 0.62), (cx - s * 0.72, cy - s * 0.4), (cx - s * 0.95, cy - s * 0.12),
         (cx - s * 0.62, cy + s * 0.08), (cx - s * 0.5, cy + s), (cx + s * 0.5, cy + s),
         (cx + s * 0.62, cy + s * 0.08), (cx + s * 0.95, cy - s * 0.12), (cx + s * 0.72, cy - s * 0.4),
         (cx + s * 0.32, cy - s * 0.62)]
    d.line(p, fill=c, width=w, joint="curve")
    d.arc([cx - s * 0.32, cy - s * 0.78, cx + s * 0.32, cy - s * 0.46], 0, 180, fill=c, width=w)

def _i_infinito(d, cx, cy, s, c, w):
    d.ellipse([cx - s, cy - s * 0.5, cx, cy + s * 0.5], outline=c, width=w)
    d.ellipse([cx, cy - s * 0.5, cx + s, cy + s * 0.5], outline=c, width=w)

def _i_flor(d, cx, cy, s, c, w):
    for k in range(6):
        a = k * math.pi / 3; px = cx + s * 0.52 * math.cos(a); py = cy + s * 0.52 * math.sin(a)
        d.ellipse([px - s * 0.4, py - s * 0.4, px + s * 0.4, py + s * 0.4], outline=c, width=w)
    d.ellipse([cx - s * 0.22, cy - s * 0.22, cx + s * 0.22, cy + s * 0.22], outline=c, width=w)

def _i_corona(d, cx, cy, s, c, w):
    p = [(cx - s, cy + s * 0.55), (cx - s, cy - s * 0.3), (cx - s * 0.5, cy + s * 0.12), (cx, cy - s * 0.6),
         (cx + s * 0.5, cy + s * 0.12), (cx + s, cy - s * 0.3), (cx + s, cy + s * 0.55)]
    d.line(p + [p[0]], fill=c, width=w, joint="curve")

def _i_nota(d, cx, cy, s, c, w):
    d.ellipse([cx - s * 0.75, cy + s * 0.15, cx - s * 0.1, cy + s * 0.7], outline=c, width=w)
    d.line([(cx - s * 0.1, cy + s * 0.45), (cx - s * 0.1, cy - s * 0.8)], fill=c, width=w)
    d.line([(cx - s * 0.1, cy - s * 0.8), (cx + s * 0.6, cy - s * 0.5)], fill=c, width=w)

ICONOS = {"corazon": _i_corazon, "estrella": _i_estrella, "pelota": _i_pelota, "escudo": _i_escudo,
          "camiseta": _i_camiseta, "infinito": _i_infinito, "flor": _i_flor, "corona": _i_corona,
          "nota": _i_nota}


def _dibujar_icono(base, nombre, cx, cy, s):
    fn = ICONOS.get(nombre)
    if not fn:
        return
    d = ImageDraw.Draw(base)
    w = max(4, int(s * 0.10))
    fn(d, cx + 2, cy + 3, s, (255, 255, 255), w)   # lip claro (grabado)
    fn(d, cx, cy, s, GRABADO, w)


def render(texto="", mate_id="demo", font="Poppins-Medium.ttf", size_frac=0.052,
           spacing=8, foto=None, r=None, max_px=1000, texto_abajo="", abajo_flip=False, icono=""):
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
    if icono:
        _dibujar_icono(base, icono, cx, cy, int(W * 0.13))   # centrado sobre la madera
    if max_px and W > max_px:
        base.thumbnail((max_px, max_px), Image.LANCZOS)
    return base


if __name__ == "__main__":
    img = render("Pablo", "demo")
    out = os.path.join(_PROY, "salida", "mate_test.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out); print("->", out)
