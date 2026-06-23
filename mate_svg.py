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


# --- iconos en SVG, reusando la geometría de mate._icon_shapes (relleno o contorno) ---
def _icon_polys(nombre, cx, cy, s, relleno=True, rot=0):
    import mate
    out = []
    sw = max(2.5, s * 0.09)
    for kind, data, skip in mate._icon_shapes(nombre, cx, cy, s):
        if relleno and skip:
            continue
        if kind == "poly":
            pts = " ".join("%.1f,%.1f" % (px, py) for px, py in data)
            if relleno:
                out.append('<polygon points="%s" fill="#000000"/>' % pts)
            else:
                out.append('<polyline points="%s %.1f,%.1f" fill="none" stroke="#000000" stroke-width="%.1f"/>'
                           % (pts, data[0][0], data[0][1], sw))
        elif kind == "circle":
            x, y, r = data
            if relleno:
                out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#000000"/>' % (x, y, r))
            else:
                out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000000" stroke-width="%.1f"/>'
                           % (x, y, r, sw))
        else:  # line
            pts = " ".join("%.1f,%.1f" % (px, py) for px, py in data)
            out.append('<polyline points="%s" fill="none" stroke="#000000" stroke-width="%.1f"/>' % (pts, sw))
    if rot:
        return ['<g transform="rotate(%.1f %.1f %.1f)">%s</g>' % (rot, cx, cy, "".join(out))]
    return out


def export_svg(texto="", mate_id="demo", font="Poppins-Medium.ttf", size_frac=0.052,
               r=None, spacing_px=8, texto_abajo="", abajo_flip=False, icono="",
               iconos=None, diam_mm=None):
    """Devuelve el SVG (str) del grabado, a escala real (mm). diam_mm = diámetro externo;
    si no se pasa, se toma de la config del mate (admin)."""
    import mate
    _, cfg = mate.cargar(mate_id)
    if diam_mm is None:
        diam_mm = cfg.get("diam_mm", 109.0)
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
            rot = float(ic.get("ang", 0)) if ic.get("seguir") else float(ic.get("rot", 0) or 0)
            icon_polys += _icon_polys(nm, ix, iy, s, relleno=ic.get("relleno", True), rot=rot)
    elif icono:
        icon_polys = _icon_polys(icono, cx, cy, W * 0.13)
    # escala física: el mate (0.86*W px) = diam_mm
    mm_per_px = float(diam_mm) / (MATE_DIAM_FRAC * W)
    svg_mm = W * mm_per_px
    head = ('<svg xmlns="http://www.w3.org/2000/svg" width="%.1fmm" height="%.1fmm" '
            'viewBox="0 0 %d %d">' % (svg_mm, svg_mm, W, W))
    # texto/iconos: relleno negro (grabado por fill en LightBurn)
    body = '<g fill="#000000">' + "".join(paths) + "</g>"
    icons = "".join(icon_polys)   # cada elemento ya trae su fill/stroke (relleno o contorno)
    # círculo guía de la virola (hairline rojo = ponelo en "no output" en LightBurn, o borralo)
    guide = ('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#ff0000" stroke-width="0.5"/>'
             % (cx, cy, int(W * 0.43)))
    return head + guide + icons + body + "</svg>"


if __name__ == "__main__":
    s = export_svg("Catalina", texto_abajo="Feliz Cumple", icono="estrella")
    open(os.path.join(os.path.dirname(__file__), "salida", "mate_test.svg"), "w").write(s)
    print("ok", len(s), "bytes")
