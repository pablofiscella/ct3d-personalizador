"""Tests del cuaderno de actividades interactivo (actividades_web.py).

Mismo criterio que el resto del motor: lo que tiene respuesta correcta se
VERIFICA por código — laberinto transitable, sopa con las palabras realmente
en la grilla, sudoku válido y único, puntos normalizados."""
import json
import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import actividades_web as aw  # noqa: E402

TEMA = "safari"
_TOK = "test-act-aabbccdd"


@pytest.fixture(scope="module")
def token():
    d = os.path.join(aw.ACT_DIR, _TOK)
    shutil.rmtree(d, ignore_errors=True)
    aw.crear({"nombre": "Sofía", "edad": "7"}, TEMA, token=_TOK)
    yield _TOK
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture(scope="module")
def data(token):
    return json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"),
                          encoding="utf-8"))


def test_crear_genera_todo(token, data):
    d = os.path.join(aw.ACT_DIR, token)
    for fn in ("data.json", "manifest.json", "portada.jpg"):
        assert os.path.isfile(os.path.join(d, fn)), fn
    assert aw.estado(token) == "listo"
    assert len(data["personajes"]) >= 4
    assert len(data["sombras"]) == len(data["personajes"])
    for fn in data["personajes"] + data["sombras"] + data["colorear"]:
        assert os.path.isfile(os.path.join(d, fn)), fn


def test_bandas_de_edad():
    assert aw._banda("2") == "mini" and aw._banda("3") == "mini"
    assert aw._banda("4") == "media" and aw._banda("5") == "media"
    assert aw._banda("6") == "grande" and aw._banda("9") == "grande"
    assert aw._banda("") == "media"          # sin edad -> media (defecto)
    ids_mini = {m["id"] for m in aw._menu("mini", 3)}
    assert "sopa" not in ids_mini and "sudoku" not in ids_mini
    ids_grande = {m["id"] for m in aw._menu("grande", 7)}
    assert {"sopa", "sudoku", "sumas", "restas"} <= ids_grande


def test_laberintos_transitables(data):
    BIT = {"E": 4, "W": 8, "N": 1, "S": 2}
    for lab in data["laberintos"]:
        n, celdas, cam = lab["n"], lab["celdas"], lab["camino"]
        assert cam[0] == [0, 0] and cam[-1] == [n - 1, n - 1]
        for (x, y), (nx, ny) in zip(cam, cam[1:]):
            dx, dy = nx - x, ny - y
            dir_ = {(1, 0): "E", (-1, 0): "W", (0, 1): "S", (0, -1): "N"}[(dx, dy)]
            assert not celdas[y][x] & BIT[dir_], "pared en el camino"


def test_sopas_verificadas(data):
    assert data["sopas"], "banda grande sin sopas"
    for s in data["sopas"]:
        assert len(s["palabras"]) >= 4
        for w, cs in s["sol"].items():
            assert "".join(s["filas"][y][x] for x, y in cs) == w


def test_sudokus_validos(data):
    for su in data["sudokus"]:
        sol, puz = su["sol"], su["puz"]
        for i in range(4):
            assert sorted(sol[i]) == [0, 1, 2, 3]                    # filas
            assert sorted(f[i] for f in sol) == [0, 1, 2, 3]         # columnas
        for r0 in (0, 2):
            for c0 in (0, 2):                                        # cajas 2x2
                caja = [sol[r][c] for r in (r0, r0 + 1) for c in (c0, c0 + 1)]
                assert sorted(caja) == [0, 1, 2, 3]
        assert any(v is None for f in puz for v in f)
        for r in range(4):
            for c in range(4):
                assert puz[r][c] in (None, sol[r][c])


def test_figuras_normalizadas(data):
    for pts in data["figuras"].values():
        assert len(pts) >= 8
        assert all(0 <= x <= 1 and 0 <= y <= 1 for x, y in pts)


def test_tokens_invalidos():
    assert aw.estado("no-existe-xx") is None
    assert aw.estado("../../etc") is None
    assert aw.html("no-existe-xx") is None
    assert aw.archivo("no-existe-xx", "data.json") is None


def test_archivo_whitelist(token):
    assert aw.archivo(token, "manifest.json") is None      # no expuesto
    assert aw.archivo(token, "../secreto.txt") is None
    assert aw.archivo(token, "data.json")[1].startswith("application/json")
    js = aw.archivo(token, "player.js")                     # sale del REPO
    assert js and b"GAMES" in js[0]
    assert aw.archivo(token, "f1.ttf")[1] == "font/ttf"
    assert aw.archivo(token, "p00.png")[1] == "image/png"


def test_html_personalizado(token):
    page = aw.html(token)
    assert "Las actividades de Sofía" in page
    assert "player.js?v=" in page


def test_paletas_completas():
    claves = set(aw._PALETA_DEFAULT)
    for tema, pal in aw.PALETAS.items():
        assert set(pal) == claves, tema


# ─────────────────────────────────────────────────────────────────────────
# Diploma de logro (14-jul-2026): Pablo — "cuando algún peque haga todo el
# cuaderno de actividades interactivo sin errores que le agregue el
# certificado de esa actividad para que lo pueda imprimir como un logro".
# Se renderiza EN VIVO (no se pre-genera con el resto de los assets del
# token) porque depende de algo que solo se sabe DESPUÉS de jugar.
def test_certificado_logro_token_valido(token, data):
    im = aw.certificado_logro(token)
    assert im is not None
    import certificado
    assert im.size == (certificado.WpH, certificado.HpH)


def test_certificado_logro_token_invalido():
    assert aw.certificado_logro("no-existe-xx") is None
    assert aw.certificado_logro("../../etc") is None
    assert aw.certificado_logro("") is None
