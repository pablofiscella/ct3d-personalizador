"""Test guardián de los cortes del rompecabezas (imprimible Y web comparten
_borde_knob/_bordes_grilla).

Bug real 11-jul-2026 (Pablo probando el rompecabezas web): los knobs eran tan
profundos (~45% de la celda) que las curvas de bordes perpendiculares se
CRUZABAN (~12 cruces por puzzle 4x5) — líneas superpuestas y piezas con puntas
visualmente sueltas. Regla: los bordes de la grilla NUNCA se tocan entre sí,
en ninguna proporción de celda que usen los productos (imprimible 0.75-1.33,
web hasta 1.5), y los flips van en damero (2 trabas + 2 huecos por pieza)."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rompecabezas import _bordes_grilla  # noqa: E402

ESC = 0.9      # escala perpendicular del knob (_dibujar_cortes / player web)


def _edges_abs(cols, filas, seed, cw, ch):
    """Todos los bordes interiores en coordenadas absolutas (mismo mapeo que
    rompecabezas._dibujar_cortes y el player web)."""
    horiz, vert = _bordes_grilla(cols, filas, seed)
    out = []
    for fi in range(filas - 1):
        for ci in range(cols):
            out.append([(ci * cw + px * cw, (fi + 1) * ch + py * ch * ESC)
                        for px, py in horiz[fi][ci]])
    for ci in range(cols - 1):
        for fi in range(filas):
            out.append([((ci + 1) * cw + py * cw * ESC, fi * ch + px * ch)
                        for px, py in vert[ci][fi]])
    return out


def _se_cruzan(s1, s2):
    (ax, ay), (bx, by) = s1
    (cx, cy), (dx, dy) = s2
    d1 = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    d2 = (bx - ax) * (dy - ay) - (by - ay) * (dx - ax)
    d3 = (dx - cx) * (ay - cy) - (dy - cy) * (ax - cx)
    d4 = (dx - cx) * (by - cy) - (dy - cy) * (bx - cx)
    return d1 * d2 < 0 and d3 * d4 < 0    # cruce estricto (tocarse en el corner no cuenta)


def _bbox(e):
    xs = [p[0] for p in e]
    ys = [p[1] for p in e]
    return min(xs), min(ys), max(xs), max(ys)


@pytest.mark.parametrize("cw,ch", [(1.0, 1.0), (1.5, 1.0), (1.0, 1.5)])
def test_bordes_no_se_cruzan(cw, ch):
    for seed in range(25):
        edges = _edges_abs(5, 6, seed, cw, ch)
        boxes = [_bbox(e) for e in edges]
        for i in range(len(edges)):
            x0, y0, x1, y1 = boxes[i]
            si = list(zip(edges[i], edges[i][1:]))
            for j in range(i + 1, len(edges)):
                a0, b0, a1, b1 = boxes[j]
                if a0 > x1 or a1 < x0 or b0 > y1 or b1 < y0:
                    continue
                sj = list(zip(edges[j], edges[j][1:]))
                for s1 in si:
                    for s2 in sj:
                        assert not _se_cruzan(s1, s2), \
                            "bordes %d y %d se cruzan (seed %d, celda %sx%s)" % (i, j, seed, cw, ch)


def test_profundidad_acotada():
    """La punta del knob no pasa de ~⅓ del borde (con ESC queda <30% de la
    celda): garantiza que nunca invade el knob de la celda de enfrente."""
    horiz, vert = _bordes_grilla(6, 6, 7)
    for grupo in (horiz, vert):
        for fila in grupo:
            for e in fila:
                assert max(abs(y) for _, y in e) < 0.36


def test_flips_en_damero():
    """Toda pieza interior queda con 2 trabas y 2 huecos (bordes alternados):
    el lado del knob alterna por paridad en ambas direcciones."""
    horiz, vert = _bordes_grilla(5, 5, 3)

    def lado(e):
        tip = max(e, key=lambda p: abs(p[1]))
        return 1 if tip[1] > 0 else -1

    for fi, fila in enumerate(horiz):
        for ci, e in enumerate(fila):
            assert lado(e) == (1 if (fi + ci) % 2 == 0 else -1)
    for ci, col in enumerate(vert):
        for fi, e in enumerate(col):
            assert lado(e) == (1 if (ci + fi) % 2 == 0 else -1)
