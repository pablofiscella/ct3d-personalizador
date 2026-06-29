"""Arma por CÓDIGO la red imprimible de una cajita cúbica: 6 caras + solapas para pegar
+ líneas de doblez. La IA solo aporta el arte decorativo de las caras (principio "OpenAI
solo ilustra"): la geometría que hace que la caja CIERRE bien la garantiza el código, no
el prompt (los modelos de imagen no saben hacer moldes plegables correctos)."""
import math

from PIL import Image, ImageDraw

# Cruz de cubo (3 columnas x 4 filas). Frente al centro, todo conectado -> cierra.
#     [Tapa]
# [Izq][Frente][Der]
#     [Atras]
#     [Base]
_CARAS = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (3, 1)]
# bordes de cada celda: nombre -> (vecino dr,dc, normal hacia afuera nx,ny)
_BORDES = {"top": (-1, 0, 0, -1), "bot": (1, 0, 0, 1), "left": (0, -1, -1, 0), "right": (0, 1, 1, 0)}
# Rotación del arte por cara para que quede DERECHO al plegar el cubo (la red plana las
# muestra giradas): izquierda -90°, derecha +90°, atrás 180°; tapa/frente/base derechas.
_ROT_CARA = {(1, 0): -90, (1, 2): 90, (2, 1): 180}


def _hex(c):
    c = (c or "#4A4A4A").lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _dash(d, x0, y0, x1, y1, fill, width=3, dash=22, gap=14):
    L = math.hypot(x1 - x0, y1 - y0)
    if L == 0:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    t = 0.0
    while t < L:
        e = min(t + dash, L)
        d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * e, y0 + uy * e)], fill=fill, width=width)
        t += dash + gap


def _edge_xy(box, lado_k):
    x0, y0, x1, y1 = box
    return {"top": (x0, y0, x1, y0), "bot": (x0, y1, x1, y1),
            "left": (x0, y0, x0, y1), "right": (x1, y0, x1, y1)}[lado_k]


def armar_cajita(art, paleta, lado=560):
    """art: ilustración decorativa (PIL.Image). Devuelve la red de la cajita (RGBA)."""
    art = art.convert("RGBA")
    ink = _hex((paleta or {}).get("ink", "#4A4A4A")) + (255,)
    C = int(lado)
    tab = max(8, int(C * 0.22))
    pad = tab + max(6, C // 40)
    W, H = pad * 2 + 3 * C, pad * 2 + 4 * C
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    cara = art.resize((C, C), Image.LANCZOS)
    ocup = set(_CARAS)

    def box(r, c):
        x, y = pad + c * C, pad + r * C
        return [x, y, x + C, y + C]

    # 1) decorar cada cara; las laterales/posterior se rotan para que queden derechas al cubo
    for (r, c) in _CARAS:
        x0, y0, _, _ = box(r, c)
        ang = _ROT_CARA.get((r, c), 0)
        out.alpha_composite(cara.rotate(ang, expand=False) if ang else cara, (x0, y0))

    # 2) solapas (en cada borde LIBRE) + líneas de doblez/corte
    for (r, c) in _CARAS:
        b = box(r, c)
        for k, (dr, dc, nx, ny) in _BORDES.items():
            ex0, ey0, ex1, ey1 = _edge_xy(b, k)
            if (r + dr, c + dc) in ocup:
                _dash(d, ex0, ey0, ex1, ey1, ink)          # doblez entre dos caras
                continue
            # borde libre -> solapa trapezoidal hacia afuera + corte sólido
            ax, ay = ex0 + (ex1 - ex0) * 0.14, ey0 + (ey1 - ey0) * 0.14
            bx, by = ex1 - (ex1 - ex0) * 0.14, ey1 - (ey1 - ey0) * 0.14
            cx0, cy0 = ax + nx * tab + (ex1 - ex0) * 0.12, ay + ny * tab + (ey1 - ey0) * 0.12
            cx1, cy1 = bx + nx * tab - (ex1 - ex0) * 0.12, by + ny * tab - (ey1 - ey0) * 0.12
            d.polygon([(ax, ay), (cx0, cy0), (cx1, cy1), (bx, by)], fill=(255, 255, 255, 255))
            d.line([(ax, ay), (cx0, cy0)], fill=ink, width=2)
            d.line([(cx0, cy0), (cx1, cy1)], fill=ink, width=2)
            d.line([(cx1, cy1), (bx, by)], fill=ink, width=2)
            _dash(d, ex0, ey0, ex1, ey1, ink)              # doblez de la solapa
    return out
