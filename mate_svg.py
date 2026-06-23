#!/usr/bin/env python3
"""Export SVG vectorial del grabado del mate, para abrir en LightBurn.

El texto se convierte a CONTORNOS (paths) con fonttools → no depende de tener la
fuente instalada en LightBurn. Misma geometría que el preview raster (mate.py), a
ESCALA REAL en mm. Los iconos se emiten como polilíneas vectoriales.
"""
import math, os
from functools import lru_cache

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
W = 1000                      # lienzo de referencia (igual que el preview)
MATE_DIAM_FRAC = 0.86         # diámetro del mate (virola externa) = 0.86*W en el preview


@lru_cache(maxsize=8)
def _ttfont(fname):
    from fontTools.ttLib import TTFont
    return TTFont(os.path.join(FONTS, os.path.basename(fname)))


def _glyph(fname, ch):
    from fontTools.pens.svgPathPen import SVGPathPen
    f = _ttfont(fname)
    upm = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    gid = cmap.get(ord(ch))
    gs = f.getGlyphSet()
    cap = 0
    try: cap = f["OS/2"].sCapHeight or 0
    except Exception: cap = 0
    if not cap: cap = int(upm * 0.7)
    if gid is None or gid not in gs:
        return "", upm * 0.5, upm, cap
    pen = SVGPathPen(gs)
    gs[gid].draw(pen)
    return pen.getCommands(), gs[gid].width, upm, cap


def _arc_paths(text, cx, cy, radius, fs, fname, pos="arriba", flip=False, spacing_px=8):
    if not text:
        return []
    chars = [(ch,) + _glyph(fname, ch) for ch in text]   # (ch, d, adv, upm, cap)
    widths = [(c[3] and (c[2] / c[3]) * fs) or 0 for c in chars]   # adv en px
    total = sum(widths) + spacing_px * (len(text) - 1)
    arc = total / radius
    if pos == "arriba":
        ang = -math.pi / 2 - arc / 2; step = 1; rotf = lambda a: math.degrees(a) + 90
    elif flip:                                   # abajo, mirando arriba (continúa el aro)
        ang = math.pi / 2 - arc / 2; step = 1; rotf = lambda a: math.degrees(a) + 90
    else:                                         # abajo, mirando abajo (legible)
        ang = math.pi / 2 + arc / 2; step = -1; rotf = lambda a: math.degrees(a) - 90
    out = []
    for i, (ch, d, adv, upm, cap) in enumerate(chars):
        wpx = widths[i]; ca = wpx / radius
        a = ang + step * ca / 2
        x = cx + radius * math.cos(a); y = cy + radius * math.sin(a)
        if d:
            s = fs / upm
            tr = ("translate(%.2f,%.2f) rotate(%.2f) scale(%.5f,%.5f) translate(%.1f,%.1f)"
                  % (x, y, rotf(a), s, -s, -adv / 2, -cap / 2))
            out.append('<path d="%s" transform="%s"/>' % (d, tr))
        ang += step * (ca + spacing_px / radius)
    return out


# --- iconos como polilíneas (mismas formas que mate.py, en vectores) ---
def _icon_polys(nombre, cx, cy, s):
    P = []
    def L(pts, close=True):
        if close: pts = pts + [pts[0]]
        P.append('<polyline points="%s" fill="none"/>' %
                 " ".join("%.1f,%.1f" % (px, py) for px, py in pts))
    def C(x, y, rr):
        P.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none"/>' % (x, y, rr))
    if nombre == "corazon":
        pts = []
        for i in range(0, 361, 5):
            t = math.radians(i); x = 16 * math.sin(t) ** 3
            yy = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
            pts.append((cx + x * s / 16, cy - yy * s / 16))
        L(pts)
    elif nombre == "estrella":
        L([(cx + (s if k % 2 == 0 else s*0.45) * math.cos(-math.pi/2 + k*math.pi/5),
            cy + (s if k % 2 == 0 else s*0.45) * math.sin(-math.pi/2 + k*math.pi/5)) for k in range(10)])
    elif nombre == "pelota":
        C(cx, cy, s)
        pent = [(cx + s*0.34*math.cos(-math.pi/2 + k*2*math.pi/5),
                 cy + s*0.34*math.sin(-math.pi/2 + k*2*math.pi/5)) for k in range(5)]
        L(pent)
        for px, py in pent:
            a = math.atan2(py - cy, px - cx)
            L([(px, py), (cx + s*0.92*math.cos(a), cy + s*0.92*math.sin(a))], close=False)
    elif nombre == "escudo":
        L([(cx-s*0.8, cy-s), (cx+s*0.8, cy-s), (cx+s*0.8, cy+s*0.15), (cx, cy+s), (cx-s*0.8, cy+s*0.15)])
    elif nombre == "corona":
        L([(cx-s, cy+s*0.55), (cx-s, cy-s*0.3), (cx-s*0.5, cy+s*0.12), (cx, cy-s*0.6),
           (cx+s*0.5, cy+s*0.12), (cx+s, cy-s*0.3), (cx+s, cy+s*0.55)])
    elif nombre == "infinito":
        C(cx - s*0.5, cy, s*0.5); C(cx + s*0.5, cy, s*0.5)
    elif nombre == "flor":
        for k in range(6):
            a = k*math.pi/3; C(cx + s*0.52*math.cos(a), cy + s*0.52*math.sin(a), s*0.4)
        C(cx, cy, s*0.22)
    # camiseta/nota: se omiten en v1 del SVG (se pueden sumar)
    return P


def export_svg(texto="", mate_id="demo", font="Poppins-Medium.ttf", size_frac=0.052,
               r=None, spacing_px=8, texto_abajo="", abajo_flip=False, icono="",
               iconos=None, diam_mm=75.0):
    """Devuelve el SVG (str) del grabado, a escala real (mm). diam_mm = diámetro de la virola."""
    import mate
    _, cfg = mate.cargar(mate_id)
    r_texto = cfg["r_texto"]
    if r is not None:
        try: r_texto = max(0.28, min(0.45, float(r)))
        except Exception: pass
    cx = cy = W / 2
    radius = W * r_texto
    fs = W * size_frac
    paths = []
    paths += _arc_paths(texto, cx, cy, radius, fs, font, "arriba", False, spacing_px)
    paths += _arc_paths(texto_abajo, cx, cy, radius, fs, font, "abajo", abajo_flip, spacing_px)
    icon_polys = []
    if iconos:
        for ic in iconos:
            nm = ic.get("n")
            ang = math.radians(float(ic.get("ang", 0)))
            s = max(0.02, min(0.12, float(ic.get("size", 0.045)))) * W
            ix = cx + radius * math.sin(ang); iy = cy - radius * math.cos(ang)
            icon_polys += _icon_polys(nm, ix, iy, s)
    elif icono:
        icon_polys = _icon_polys(icono, cx, cy, W * 0.13)
    # escala física: el mate (0.86*W px) = diam_mm
    mm_per_px = float(diam_mm) / (MATE_DIAM_FRAC * W)
    svg_mm = W * mm_per_px
    head = ('<svg xmlns="http://www.w3.org/2000/svg" width="%.1fmm" height="%.1fmm" '
            'viewBox="0 0 %d %d">' % (svg_mm, svg_mm, W, W))
    # texto/iconos: relleno negro (grabado por fill en LightBurn)
    body = '<g fill="#000000">' + "".join(paths) + "</g>"
    icons = '<g fill="none" stroke="#000000" stroke-width="%.1f">%s</g>' % (max(3, fs * 0.10), "".join(icon_polys))
    # círculo guía de la virola (hairline rojo = ponelo en "no output" en LightBurn, o borralo)
    guide = ('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#ff0000" stroke-width="0.5"/>'
             % (cx, cy, int(W * 0.43)))
    return head + guide + icons + body + "</svg>"


if __name__ == "__main__":
    s = export_svg("Catalina", texto_abajo="Feliz Cumple", icono="estrella")
    open(os.path.join(os.path.dirname(__file__), "salida", "mate_test.svg"), "w").write(s)
    print("ok", len(s), "bytes")
