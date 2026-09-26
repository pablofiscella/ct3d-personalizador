# -*- coding: utf-8 -*-
"""El cuaderno tiene que pesar poco en un celular con datos (25-sep-2026).

Auditoría MOT-03 / EXP-13 / PRO-14: medido con Chromium, CPU ×4 y 4G lento, el cuaderno de
4.º bajaba 2,1 MB y tardaba 12-13 s en sacar «Preparando tus juegos…». Lo que más pesaba y
se podía sacar SIN tocar un solo token vendido:

  - los 8 personajes en PNG (~1,2 MB), que el arranque espera todos;
  - el catálogo curricular de los siete grados (~1 MB sin comprimir) cuando cada cuaderno
    usa uno.

Medido después del cambio, mismo perfil: 0,9 MB y 6,2-6,3 s.

Todo se resuelve al SERVIR (`actividades_web.archivo`), así que los tests arman un token
de mentira en una carpeta temporal y le piden los archivos como se los pide el navegador.
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import urllib.request
from http.server import ThreadingHTTPServer

import pytest
from PIL import Image

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)
import actividades_web as aw  # noqa: E402

TOKEN = "prueba-peso-4to"
CUR = os.path.join(_BASE, "actividades_curriculum.js")


def _ids_del_grado(g):
    src = open(CUR, encoding="utf-8").read()
    return re.findall(r"^/\* %d° · .*? — ([a-z0-9_]+)" % g, src, re.M)


@pytest.fixture
def token(tmp_path, monkeypatch):
    """Un cuaderno de 4.º con dos personajes, una actividad curricular de 4.º y una nativa."""
    monkeypatch.setattr(aw, "ACT_DIR", str(tmp_path))
    d = tmp_path / TOKEN
    d.mkdir()
    (d / "manifest.json").write_text(json.dumps({"titulo": "Cuaderno"}))
    # Los personajes de verdad del arte de 4.º (están en el repo), achicados como los deja
    # `_arte_de_grado` al armar un token: un dibujo inventado comprime distinto.
    for i in range(2):
        with Image.open(os.path.join(_BASE, "actividades_arte", "g4", "s%02d.png" % i)) as im:
            im = im.convert("RGBA")
            im.thumbnail((420, 420), Image.LANCZOS)
            im.save(d / ("s%02d.png" % i), optimize=True)
    menu = [{"id": "memotest"}, {"id": _ids_del_grado(4)[0]}]
    (d / "data.json").write_text(json.dumps({
        "edad": "9", "menu": menu, "personajes": ["s00.png", "s01.png"],
        "sombras": ["s00.png", "s01.png"], "escena": "escena.jpg"}))
    return d


# ── personajes ────────────────────────────────────────────────────────────────────────

def test_el_data_json_pide_los_personajes_en_webp(token):
    body, ct = aw.archivo(TOKEN, "data.json")
    dj = json.loads(body)
    assert dj["personajes"] == ["s00.webp", "s01.webp"]
    assert dj["sombras"] == ["s00.webp", "s01.webp"]
    assert dj["escena"] == "escena.jpg", "sólo se tocan los personajes"
    # el archivo en disco NO se toca: es de la compra
    assert json.loads((token / "data.json").read_text())["personajes"] == ["s00.png", "s01.png"]


def test_el_webp_es_webp_y_pesa_menos(token):
    body, ct = aw.archivo(TOKEN, "s00.webp", acepta_webp=True)
    assert ct == "image/webp"
    assert body[:4] == b"RIFF" and body[8:12] == b"WEBP"
    assert len(body) < os.path.getsize(token / "s00.png")
    assert len(body) < os.path.getsize(token / "s00.png") / 2, "tiene que bajar a menos de la mitad"
    im = Image.open(io.BytesIO(body))
    assert im.size == Image.open(token / "s00.png").size
    assert im.mode == "RGBA", "la transparencia tiene que quedar"


def test_al_navegador_que_no_entiende_webp_se_le_da_el_png(token):
    """Safari de iOS 13 o anterior no anuncia `image/webp`: recibe los mismos bytes de
    siempre, con su tipo. El navegador mira los bytes, no la extensión de la URL."""
    body, ct = aw.archivo(TOKEN, "s01.webp", acepta_webp=False)
    assert ct == "image/png"
    assert body == (token / "s01.png").read_bytes()


def test_el_png_de_siempre_se_sigue_sirviendo(token):
    """Un HTML o un data.json viejo en la caché del navegador todavía pide `s00.png`."""
    body, ct = aw.archivo(TOKEN, "s00.png")
    assert ct == "image/png" and body == (token / "s00.png").read_bytes()


def test_un_personaje_que_no_existe_no_se_inventa(token):
    assert aw.archivo(TOKEN, "s07.webp", acepta_webp=True) is None
    assert aw.archivo(TOKEN, "../s00.webp", acepta_webp=True) is None


# ── catálogo curricular ─────────────────────────────────────────────────────────────

def _cur(token_):
    body, ct = aw.archivo(TOKEN, "actividades_curriculum.js")
    assert ct.startswith("text/javascript")
    return body.decode("utf-8")


def _grados_en(js):
    return set(int(g) for g in re.findall(r"^/\* (\d)° · ", js, re.M))


def test_el_catalogo_trae_solo_el_grado_del_cuaderno(token):
    js = _cur(token)
    completo = open(CUR, encoding="utf-8").read()
    assert _grados_en(js) == {4}
    assert len(js) < len(completo) / 4, "el catálogo de 4.º tiene que ser una parte chica"
    assert "const CAJA_IMPORTA" in js, "la cabecera compartida no se puede perder"
    for i in _ids_del_grado(4):
        assert "GAMES.%s = " % i in js
    assert "GAMES.%s = " % _ids_del_grado(5)[0] not in js


def test_las_extras_de_otro_grado_suman_su_grado(token):
    """La escuela o el padre pueden sumar actividades de otro grado («Más allá»)."""
    extra = _ids_del_grado(5)[0]
    (token / "extras.json").write_text(json.dumps({"items": [{"id": extra, "grado": 5}]}))
    js = _cur(token)
    assert _grados_en(js) == {4, 5}
    assert "GAMES.%s = " % extra in js


def test_la_url_del_catalogo_cambia_si_cambian_los_grados(token):
    """El catálogo se cachea un día: si la escuela suma un grado, la URL tiene que ser otra
    para que el navegador no se quede con el que no tiene la actividad nueva."""
    orig = aw._es_escolar
    aw._es_escolar = lambda t, reg=None: True
    try:
        antes = re.search(r'actividades_curriculum\.js\?v=([^"]+)"', aw.html(TOKEN)).group(1)
        (token / "extras.json").write_text(json.dumps(
            {"items": [{"id": _ids_del_grado(5)[0], "grado": 5}]}))
        despues = re.search(r'actividades_curriculum\.js\?v=([^"]+)"', aw.html(TOKEN)).group(1)
    finally:
        aw._es_escolar = orig
    assert antes != despues
    assert antes.endswith(".4") and despues.endswith(".45")


@pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")
def test_el_catalogo_partido_corre_y_el_duelo_tiene_su_grado(token, tmp_path):
    """Lo que más miedo da: que el recorte deje una variable nombrada y sin declarar (el
    pozo del duelo nombra los bancos) y el archivo entero tire ReferenceError."""
    arch = tmp_path / "cur4.js"
    arch.write_text(_cur(token), encoding="utf-8")
    prog = r"""
const vm = require("vm");
const ctx = { GAMES: {}, juegoTriviaTexto: () => ({}), juegoClasificar: () => ({}),
  juegoOrdenar: () => ({}), juegoParametrico: () => ({}), juegoManipular: () => ({}) };
vm.createContext(ctx);
vm.runInContext(require("fs").readFileSync(%s, "utf8") + "\n;this.__duelo = CUR_DUELO_POR_GRADO;", ctx);
console.log(JSON.stringify({ juegos: Object.keys(ctx.GAMES), duelo: Object.keys(ctx.__duelo),
  preguntas: (ctx.__duelo[4] || []).reduce((a, p) => a + p[1].length, 0) }));
""" % json.dumps(str(arch))
    r = subprocess.run(["node", "-e", prog], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-1500:]
    out = json.loads(r.stdout)
    assert out["duelo"] == ["4"]
    assert out["preguntas"] >= 5, "el duelo de 4.º necesita su pozo de preguntas"
    assert set(_ids_del_grado(4)) <= set(out["juegos"])


def test_si_el_catalogo_cambia_de_forma_se_sirve_entero(token, tmp_path, monkeypatch):
    """Si mañana `gen_curriculum.py` cambia la cabecera, recortar a ciegas rompería todos
    los cuadernos: mejor servirlo entero (pesa más, pero anda)."""
    raro = tmp_path / "cur.js"
    raro.write_text("const CAJA_IMPORTA = new Set([]);\nGAMES.x = {};\n", encoding="utf-8")
    monkeypatch.setattr(aw, "TEMPLATE_CURRICULUM", str(raro))
    body, _ = aw.archivo(TOKEN, "actividades_curriculum.js")
    assert body == raro.read_bytes()


# ── la ruta de verdad ─────────────────────────────────────────────────────────────────

def test_el_servidor_manda_webp_o_png_segun_el_accept_y_no_deja_cachear_en_el_medio(token):
    import servicio
    srv = ThreadingHTTPServer(("127.0.0.1", 0), servicio.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        url = "http://127.0.0.1:%d/act/%s/s00.webp" % (srv.server_address[1], TOKEN)
        chrome = urllib.request.urlopen(urllib.request.Request(
            url, headers={"Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8"}))
        viejo = urllib.request.urlopen(urllib.request.Request(
            url, headers={"Accept": "image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5"}))
        assert chrome.headers["Content-Type"] == "image/webp"
        assert viejo.headers["Content-Type"] == "image/png"
        for r in (chrome, viejo):
            assert "private" in r.headers["Cache-Control"], \
                "Cloudflare no puede guardar una versión y dársela al otro navegador"
            assert "Accept" in (r.headers.get("Vary") or "")
    finally:
        srv.shutdown()
