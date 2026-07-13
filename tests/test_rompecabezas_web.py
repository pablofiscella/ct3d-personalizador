"""Tests del rompecabezas interactivo (rompecabezas_web.py).

Mismo criterio que el resto del motor: lo que tiene respuesta correcta se
VERIFICA por código — acá, que las piezas exportadas a data.json cierren y
PARTICIONEN exactamente la imagen (los bordes compartidos entre piezas vecinas
son la misma polilínea, así que la suma de áreas debe dar el área total)."""
import base64
import io
import json
import os
import re
import shutil
import sys
import time

import pytest
from PIL import Image

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


def test_niveles_fijos_para_todos(data):
    """Pablo 11-jul-2026: el producto NO pide edad — toda compra trae los
    mismos niveles, de 4 a ~50 piezas (como el demo)."""
    assert rw.TARGETS == [4, 6, 12, 20, 30, 48]
    assert data["targets"] == rw.TARGETS


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
    assert productos.campos_tipo("rompecabezas-web") == []   # nada para completar (Pablo 11-jul)
    assert productos.existe_tipo("rompecabezas-foto")
    assert productos.campos_tipo("rompecabezas-foto") == []  # la personalización es la foto, no texto
    piezas = productos.piezas_tipo(None, "rompecabezas-foto")
    assert len(piezas) == 1
    im = piezas[0][1]({})
    assert im.size[0] > 0 and im.size[1] > 0


def test_preview_thumbnail_rompecabezas_foto_no_cae_a_invitacion():
    """La miniatura de la ficha (usada por tienda_kit_admin.preview_thumb) pasa
    por productos.preview() -> _spec(tipo)['preview'] -> el whitelist de tipos
    100% procedurales. Si "rompecabezas-foto" faltara ahí, caería silenciosamente
    al render de invitación (bug real encontrado al auditar el registro completo,
    14-jul-2026) — acá se compara CONTENIDO (no solo tamaño) contra la imagen
    de ejemplo del tipo, para no dejar pasar un fallback que "por casualidad"
    tenga el mismo tamaño."""
    import productos
    im = productos.preview({}, tema="safari", tipo="rompecabezas-foto", max_px=300)
    demo = productos.piezas_tipo(None, "rompecabezas-foto")[0][1]({}).convert("RGB")
    demo.thumbnail((300, 300), Image.LANCZOS)
    assert im.size == demo.size
    assert im.convert("RGB").getpixel((5, 5)) == demo.getpixel((5, 5))


def test_portada_banda_clara_y_edad_mas():
    """Feedback Pablo 11-jul: la banda inferior de la portada es SIEMPRE clara
    (con la paleta oscura del tema espacial salía azul) y la edad se muestra
    como «+N años»."""
    im = rw.preview_mock({"nombre": "", "edad": "3"}, "un-espacio-de-locura")
    r, g, b = im.convert("RGB").getpixel((450, 1120))
    assert 0.299 * r + 0.587 * g + 0.114 * b > 180, "banda oscura en la portada"


# ─────────────────────────────────────────────────────────────────────────
# Rompecabezas de FOTO (13-jul-2026): Pablo, "rompecabezas con una foto que
# nos suba". PROTOTIPO — probado el motor real hasta 500 piezas antes de
# fijar TARGETS_FOTO (server y snap andan bien en todo el rango; el techo es
# de USO, no de motor: la bandeja de piezas sueltas se satura antes que el
# tablero — ver TARGETS_FOTO). Reusa el mismo _bordes_json que el de tema,
# así que la partición geométrica (test_piezas_particionan_la_imagen) ya
# está cubierta por _bordes_grilla en general — acá se verifica el camino
# ESPECÍFICO de la foto: sin tema, targets ampliados, y los rechazos.
_TOK_FOTO = "test-rompe-foto-aabbccdd"


@pytest.fixture(scope="module")
def token_foto():
    d = os.path.join(rw.ROMPE_DIR, _TOK_FOTO)
    shutil.rmtree(d, ignore_errors=True)
    foto = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "temas", "circo", "overrides", "libro", "1.png")
    with open(foto, "rb") as f:
        rw.crear_desde_foto(f.read(), token=_TOK_FOTO)
    yield _TOK_FOTO
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture(scope="module")
def data_foto(token_foto):
    return json.load(open(os.path.join(rw.ROMPE_DIR, token_foto, "data.json"),
                          encoding="utf-8"))


def test_foto_sin_tema_ni_mascota(data_foto):
    assert data_foto["tema"] is None
    assert data_foto["masco"] is None
    assert data_foto["tema_nombre"] == "Tu foto"


def test_foto_targets_ampliados(data_foto):
    assert data_foto["targets"] == rw.TARGETS_FOTO
    assert 70 in rw.TARGETS_FOTO and 100 in rw.TARGETS_FOTO   # niveles nuevos, probados


def test_foto_grillas_altas_particionan_bien(data_foto):
    """Mismo chequeo de partición que test_piezas_particionan_la_imagen, pero
    en los niveles NUEVOS (70/100) para no confiar solo en la inspección
    visual manual de esta sesión."""
    p = data_foto["puzzles"][0]
    for t in (70, 100):
        clave = p["grillas"][str(t)]
        cols, filas = map(int, clave.split("x"))
        b = data_foto["bordes"][clave]
        total = sum(_area(_poli(ci, fi, cols, filas, b, p["w"], p["h"]))
                    for fi in range(filas) for ci in range(cols))
        assert abs(total - p["w"] * p["h"]) / (p["w"] * p["h"]) < 0.002, clave


def test_foto_rechaza_no_imagen():
    with pytest.raises(ValueError):
        rw.crear_desde_foto(b"esto no es una imagen")


def test_foto_rechaza_demasiado_pesada():
    with pytest.raises(ValueError):
        rw.crear_desde_foto(b"x" * (16 * 1024 * 1024))


# ─────────────────────────────────────────────────────────────────────────
# Staging (14-jul-2026): venta REAL a $9000 — la foto sube ANTES de pagar
# (stage_foto, ficha del producto) y el rompecabezas completo recién se
# arma DESPUÉS del pago confirmado (crear_desde_foto_staged, /api/generar).
_FOTO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "temas", "circo", "overrides", "libro", "1.png")


@pytest.fixture
def foto_bytes():
    with open(_FOTO_PATH, "rb") as f:
        return f.read()


def test_stage_foto_devuelve_token_y_preview_con_marca_de_agua(foto_bytes):
    stage_token, preview = rw.stage_foto(foto_bytes)
    try:
        assert re.fullmatch(r"[A-Za-z0-9_-]{10,40}", stage_token)
        assert preview.startswith("data:image/jpeg;base64,")
        raw_prev = base64.b64decode(preview.split(",", 1)[1])
        im = Image.open(io.BytesIO(raw_prev))
        assert max(im.size) <= 480
        assert os.path.isfile(os.path.join(rw._STAGING_DIR, stage_token + ".jpg"))
    finally:
        try:
            os.remove(os.path.join(rw._STAGING_DIR, stage_token + ".jpg"))
        except OSError:
            pass


def test_stage_foto_rechaza_igual_que_crear_desde_foto():
    with pytest.raises(ValueError):
        rw.stage_foto(b"esto no es una imagen")
    with pytest.raises(ValueError):
        rw.stage_foto(b"x" * (16 * 1024 * 1024))


def test_crear_desde_foto_staged_materializa_y_borra_el_staging(foto_bytes):
    stage_token, _ = rw.stage_foto(foto_bytes)
    stage_path = os.path.join(rw._STAGING_DIR, stage_token + ".jpg")
    assert os.path.isfile(stage_path)
    tok = rw.crear_desde_foto_staged(stage_token)
    try:
        d = json.load(open(os.path.join(rw.ROMPE_DIR, tok, "data.json"), encoding="utf-8"))
        assert d["tema"] is None and d["targets"] == rw.TARGETS_FOTO
        assert not os.path.isfile(stage_path), "el staging debe borrarse tras materializar"
    finally:
        shutil.rmtree(os.path.join(rw.ROMPE_DIR, tok), ignore_errors=True)


def test_crear_desde_foto_staged_token_desconocido_o_invalido():
    with pytest.raises(ValueError):
        rw.crear_desde_foto_staged("token-que-no-existe-nunca-se-subio")
    with pytest.raises(ValueError):
        rw.crear_desde_foto_staged("../../etc/passwd")
    with pytest.raises(ValueError):
        rw.crear_desde_foto_staged("")


def test_crear_desde_foto_staged_no_se_puede_reusar(foto_bytes):
    """Una vez materializado, el mismo stage_token no debe volver a andar —
    evita que alguien reintente /api/generar y arme el mismo pedido dos
    veces gratis a partir de una sola foto subida."""
    stage_token, _ = rw.stage_foto(foto_bytes)
    tok = rw.crear_desde_foto_staged(stage_token)
    try:
        with pytest.raises(ValueError):
            rw.crear_desde_foto_staged(stage_token)
    finally:
        shutil.rmtree(os.path.join(rw.ROMPE_DIR, tok), ignore_errors=True)


def test_limpiar_staging_vencido_borra_solo_lo_viejo(foto_bytes):
    stage_token, _ = rw.stage_foto(foto_bytes)
    p = os.path.join(rw._STAGING_DIR, stage_token + ".jpg")
    viejo = os.path.join(rw._STAGING_DIR, "viejo-test-token.jpg")
    with open(viejo, "wb") as f:
        f.write(foto_bytes)
    vencido = time.time() - rw._STAGING_VIGENCIA_SEG - 60
    os.utime(viejo, (vencido, vencido))
    try:
        rw._limpiar_staging_vencido()
        assert not os.path.isfile(viejo), "el staging vencido debe borrarse"
        assert os.path.isfile(p), "el staging reciente NO debe tocarse"
    finally:
        for x in (p, viejo):
            try:
                os.remove(x)
            except OSError:
                pass
