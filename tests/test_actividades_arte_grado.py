"""Arte ESCOLAR por grado (actividades_arte/g<N>/): el elenco dibujado en el estilo de la
portada de cada grado reemplaza a los stickers del tema de cumpleaños.

Lo que se verifica: (a) sin arte del grado, el token sale EXACTAMENTE como siempre (los
p*.png del tema) — la garantía de no-regresión para los links ya vendidos; (b) con arte del
grado, el token usa ese elenco; (c) arte incompleto (1 sola imagen) cae al tema, no deja un
token con menos personajes de los que el player necesita."""
import os
import shutil
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import actividades_web as aw  # noqa: E402

TEMA = "safari"
EDAD_5TO = "10"          # edad 10 → 5° grado
GRADO = int(EDAD_5TO) - 5


@pytest.fixture
def arte_dir():
    """Crea/limpia actividades_arte/g<N>/ sin pisar arte real si existiera."""
    d = os.path.join(aw.BASEDIR, "actividades_arte", "g%d" % GRADO)
    backup = d + ".bak-test"
    existia = os.path.isdir(d)
    if existia:
        shutil.move(d, backup)
    os.makedirs(d, exist_ok=True)
    yield d
    shutil.rmtree(d, ignore_errors=True)
    if existia:
        shutil.move(backup, d)


def _sticker(path, color):
    im = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    im.paste(color, (60, 60, 240, 240))
    im.save(path)


def _crear(token, edad=EDAD_5TO):
    d = os.path.join(aw.ACT_DIR, token)
    shutil.rmtree(d, ignore_errors=True)
    aw.crear({"nombre": "Test", "edad": edad}, TEMA, token=token)
    return d


def test_sin_arte_de_grado_usa_el_tema(arte_dir):
    """Sin arte del grado (dir vacío) el token sale como siempre: stickers p*.png del tema."""
    shutil.rmtree(arte_dir, ignore_errors=True)      # ni siquiera existe el dir
    tok = "test-arte-sin-aabb"
    d = _crear(tok)
    try:
        import json
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        assert dj["personajes"], "el token quedó sin personajes"
        assert all(p.startswith("p") for p in dj["personajes"]), dj["personajes"]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_con_arte_de_grado_lo_usa(arte_dir):
    """Con arte del grado, el token usa ESE elenco (s*.png) y los archivos llegan al token."""
    for i, col in enumerate([(200, 30, 30), (30, 200, 30), (30, 30, 200), (200, 200, 30)]):
        _sticker(os.path.join(arte_dir, "s%02d.png" % i), col)
    tok = "test-arte-con-aabb"
    d = _crear(tok)
    try:
        import json
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        assert dj["personajes"] == ["s00.png", "s01.png", "s02.png", "s03.png"], dj["personajes"]
        assert dj["sombras"] == dj["personajes"]
        for fn in dj["personajes"]:
            assert os.path.exists(os.path.join(d, fn)), "falta %s en el token" % fn
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_arte_incompleto_cae_al_tema(arte_dir):
    """Con UNA sola imagen (arte a medio generar) NO se usa: el player necesita variedad."""
    _sticker(os.path.join(arte_dir, "s00.png"), (200, 30, 30))
    tok = "test-arte-media-aabb"
    d = _crear(tok)
    try:
        import json
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        assert all(p.startswith("p") for p in dj["personajes"]), dj["personajes"]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_otro_grado_no_se_contamina(arte_dir):
    """El arte de 5° no se le aplica a un token de otra edad (grado distinto)."""
    for i, col in enumerate([(200, 30, 30), (30, 200, 30), (30, 30, 200)]):
        _sticker(os.path.join(arte_dir, "s%02d.png" % i), col)
    tok = "test-arte-otro-aabb"
    d = _crear(tok, edad="7")          # 2° grado, sin arte propio
    try:
        import json
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        assert all(p.startswith("p") for p in dj["personajes"]), dj["personajes"]
    finally:
        shutil.rmtree(d, ignore_errors=True)
