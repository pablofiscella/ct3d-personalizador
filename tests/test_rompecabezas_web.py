"""Tests del rompecabezas interactivo (rompecabezas_web.py).

Mismo criterio que el resto del motor: lo que tiene respuesta correcta se
VERIFICA por código — acá, que las piezas exportadas a data.json cierren y
PARTICIONEN exactamente la imagen (los bordes compartidos entre piezas vecinas
son la misma polilínea, así que la suma de áreas debe dar el área total)."""
import json
import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import rompecabezas_web as rw  # noqa: E402

TEMA = "safari"
_TOK = "test-rompe-aabbccdd"
ESC = 0.9      # escala del knob (rompecabezas._dibujar_cortes / player)


@pytest.fixture(scope="module")
def token():
    d = os.path.join(rw.ROMPE_DIR, _TOK)
    shutil.rmtree(d, ignore_errors=True)
    rw.crear({"nombre": "Sofía", "edad": "5"}, TEMA, token=_TOK)
    yield _TOK
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture(scope="module")
def data(token):
    return json.load(open(os.path.join(rw.ROMPE_DIR, token, "data.json"),
                          encoding="utf-8"))


def test_crear_genera_todo(token, data):
    d = os.path.join(rw.ROMPE_DIR, token)
    for fn in ("data.json", "manifest.json", "portada.jpg"):
        assert os.path.isfile(os.path.join(d, fn)), fn
    assert rw.estado(token) == "listo"
    assert 1 <= len(data["puzzles"]) <= rw.MAX_PUZZLES
    for p in data["puzzles"]:
        assert os.path.isfile(os.path.join(d, p["img"])), p["img"]
        assert os.path.isfile(os.path.join(d, p["thumb"])), p["thumb"]


def test_imagenes_coinciden_con_data(token, data):
    from PIL import Image
    d = os.path.join(rw.ROMPE_DIR, token)
    for p in data["puzzles"]:
        with Image.open(os.path.join(d, p["img"])) as im:
            assert im.size == (p["w"], p["h"])


def test_bandas_de_edad():
    assert rw.NIVELES_BANDA[rw._banda("2")] == [4, 6, 12, 20, 30, 48]
    assert rw.NIVELES_BANDA[rw._banda("5")] == [6, 12, 20, 30, 48]
    assert rw.NIVELES_BANDA[rw._banda("8")] == [12, 20, 30, 48]
    # TODAS las bandas llegan al tope ~50 (pedido de Pablo 11-jul-2026)
    assert all(n[-1] == 48 for n in rw.NIVELES_BANDA.values())


def test_grillas_y_bordes(data):
    for p in data["puzzles"]:
        assert set(p["grillas"]) == {str(t) for t in data["targets"]}
        for t, clave in p["grillas"].items():
            cols, filas = map(int, clave.split("x"))
            if int(t) >= 40:
                # el tope admite conteos vecinos (6x8=48 / 7x7=49): 50 exacto
                # solo factoriza 5x10, piezas 2:1
                assert abs(cols * filas - int(t)) <= 3
            else:
                assert cols * filas == int(t)
            b = data["bordes"][clave]
            assert len(b["h"]) == filas - 1
            assert all(len(fila) == cols for fila in b["h"])
            assert len(b["v"]) == cols - 1
            assert all(len(col) == filas for col in b["v"])


def test_bordes_bien_formados(data):
    """Cada borde va de (0,0) a (1,0) con el knob acotado (traba real, nunca
    invade más de media celda vecina)."""
    for clave, b in data["bordes"].items():
        for grupo in (b["h"], b["v"]):
            for fila in grupo:
                for e in fila:
                    assert len(e) >= 10
                    assert abs(e[0][0]) < 1e-6 and abs(e[0][1]) < 1e-6
                    assert abs(e[-1][0] - 1) < 1e-6 and abs(e[-1][1]) < 1e-6
                    assert max(abs(y) for _, y in e) < 0.55


def _poli(ci, fi, cols, filas, b, w, h):
    """El contorno de la pieza (ci,fi) — MISMO mapeo que el player JS."""
    cw, ch = w / cols, h / filas
    pts = []
    if fi == 0:
        pts += [(ci * cw, 0), ((ci + 1) * cw, 0)]
    else:
        pts += [(ci * cw + px * cw, fi * ch + py * ch * ESC) for px, py in b["h"][fi - 1][ci]]
    if ci == cols - 1:
        pts.append((w, (fi + 1) * ch))
    else:
        pts += [((ci + 1) * cw + py * cw * ESC, fi * ch + px * ch) for px, py in b["v"][ci][fi]]
    if fi == filas - 1:
        pts.append((ci * cw, h))
    else:
        pts += [(ci * cw + px * cw, (fi + 1) * ch + py * ch * ESC)
                for px, py in reversed(b["h"][fi][ci])]
    if ci != 0:
        pts += [(ci * cw + py * cw * ESC, fi * ch + px * ch)
                for px, py in reversed(b["v"][ci - 1][fi])]
    return pts


def _area(pts):
    s = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def test_piezas_particionan_la_imagen(data):
    """La suma de áreas de las piezas = área de la imagen (los knobs de bordes
    compartidos se compensan) — garantiza que el player recorta sin huecos ni
    solapamientos."""
    for p in data["puzzles"]:
        for clave in p["grillas"].values():
            cols, filas = map(int, clave.split("x"))
            b = data["bordes"][clave]
            total = sum(_area(_poli(ci, fi, cols, filas, b, p["w"], p["h"]))
                        for fi in range(filas) for ci in range(cols))
            assert abs(total - p["w"] * p["h"]) / (p["w"] * p["h"]) < 0.002, clave


def test_nivel_tope_piezas_cuadradas(data):
    """El tope (~50) elige grillas de piezas CUADRADAS: 6x8=48 en fotos 3:4,
    7x7=49 en cuadradas — nunca 5x10 (piezas 2:1)."""
    import math
    for p in data["puzzles"]:
        clave = p["grillas"][str(data["targets"][-1])]
        cols, filas = map(int, clave.split("x"))
        r = (p["w"] / cols) / (p["h"] / filas)
        assert abs(math.log(r)) < 0.12, clave


def test_bordes_deterministicos_por_token(token, data):
    """Regenerar el MISMO token reproduce las mismas formas (seed = token)."""
    rw.crear({"nombre": "Sofía", "edad": "5"}, TEMA, token=_TOK)
    d2 = json.load(open(os.path.join(rw.ROMPE_DIR, token, "data.json"),
                        encoding="utf-8"))
    assert d2["bordes"] == data["bordes"]


def test_archivo_whitelist(token):
    assert rw.archivo(token, "data.json") is not None
    assert rw.archivo(token, "p0.jpg") is not None
    js = rw.archivo(token, "player.js")
    assert js is not None and b"Casatridimensional" in js[0]
    for malo in ("manifest.json", "../data.json", "kit.zip", "p00.png",
                 "portada.png", "", None):
        assert rw.archivo(token, malo) is None
    assert rw.archivo("token-inexistente-123", "data.json") is None


def test_html_y_tokens_invalidos(token):
    page = rw.html(token)
    assert page and "Sofía" in page and "player.js?v=" in page
    assert rw.html("no-existe-9999") is None
    assert rw.html("../etc") is None
    assert rw.estado("x") is None


def test_preview_mock():
    im = rw.preview_mock({"nombre": "Benja", "edad": "4"}, TEMA)
    assert im.size == (900, 1200)


def test_tipo_registrado_en_productos():
    import productos
    assert productos.existe_tipo("rompecabezas-web")
    assert productos.campos_tipo("rompecabezas-web") == ["nombre", "edad"]
