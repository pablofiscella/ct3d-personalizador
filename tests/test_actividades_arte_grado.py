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
def arte_dir(tmp_path, monkeypatch):
    """Carpeta de arte del grado, en un tmp: `ARTE_DIR` se apunta ahí para que el test
    NUNCA toque el arte real del repo (ver test_actividades_tematica_grado.py)."""
    monkeypatch.setattr(aw, "ARTE_DIR", str(tmp_path))
    d = tmp_path / ("g%d" % GRADO)
    d.mkdir()
    return str(d)


def _sticker(path, color):
    im = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    im.paste(color, (60, 60, 240, 240))
    im.save(path)


def _crear(token, edad=EDAD_5TO):
    d = os.path.join(aw.ACT_DIR, token)
    shutil.rmtree(d, ignore_errors=True)
    aw.crear({"nombre": "Test", "edad": edad, "escolar_on": True}, TEMA, token=token)
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


def test_header_dice_el_mundo_del_grado(arte_dir):
    """Con arte del grado, el header muestra el mundo de la portada (no 'Safari')."""
    for i in range(4):
        _sticker(os.path.join(arte_dir, "s%02d.png" % i), (10, 90, 200))
    tok = "test-arte-mundo-aabb"
    d = _crear(tok)
    try:
        import json
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        assert dj["tema_nombre"] == aw.MUNDO_GRADO[GRADO], dj["tema_nombre"]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_sin_arte_el_header_sigue_siendo_el_tema(arte_dir):
    """Sin arte del grado, el header NO promete un mundo que el cuaderno no muestra."""
    shutil.rmtree(arte_dir, ignore_errors=True)
    tok = "test-arte-mundo2-aabb"
    d = _crear(tok)
    try:
        import json
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        assert dj["tema_nombre"] != aw.MUNDO_GRADO[GRADO], dj["tema_nombre"]
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
    """El arte de 5° NO se le aplica a un token de otro grado: cada grado usa SU carpeta.

    Se verifica por CONTENIDO (no por nombre): las piezas de 5° acá son de un color único,
    y ninguna del token de otro grado puede tener ese color."""
    marca = (177, 13, 201)                       # color que no aparece en ningún arte real
    for i in range(4):
        _sticker(os.path.join(arte_dir, "s%02d.png" % i), marca)
    tok = "test-arte-otro-aabb"
    d = _crear(tok, edad="7")                    # 2° grado (su propio arte, o el tema)
    try:
        import json
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        for fn in dj["personajes"]:
            im = Image.open(os.path.join(d, fn)).convert("RGBA")
            colores = {p[:3] for p in im.getdata() if p[3] > 200}
            assert marca not in colores, "%s trae arte de 5° en un token de 2°" % fn
    finally:
        shutil.rmtree(d, ignore_errors=True)
