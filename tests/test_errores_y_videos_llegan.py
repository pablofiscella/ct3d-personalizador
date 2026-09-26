# -*- coding: utf-8 -*-
"""Lo que pasa en el celular de la familia llega al servidor (25-sep-2026).

INF-22: si el cuaderno se rompía en el navegador de una familia —uno viejo, el de Facebook,
un deploy con un error— nadie se enteraba: en el embudo quedaba como «entró y no jugó». Ahora
un manejador en el HTML del cuaderno (antes de player.js) manda cada error de JavaScript a
`/act/<token>/error-js`, que lo anota con tope y SIN datos personales: ni el token (abre el
cuaderno de un chico), ni la IP, ni el nombre.

PRO-19: los videos interactivos no dejaban rastro para el padre ni la maestra. Ahora el
cuaderno manda «visto» y «terminado» por el mismo canal de telemetría que los juegos.
"""
import hashlib
import json
import os
import shutil
import sys
import threading
from http.server import ThreadingHTTPServer

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)
import actividades_web as aw  # noqa: E402

sin_navegador = pytest.mark.skipif(
    __import__("importlib").util.find_spec("playwright") is None,
    reason="no hay playwright instalado")

TOK = "errores-prueba-3"
CLAVE = "ct3d_act::/act/" + TOK


@pytest.fixture
def cuaderno(tmp_path, monkeypatch):
    import servicio
    act = tmp_path / "act"
    d = act / TOK
    d.mkdir(parents=True)
    monkeypatch.setattr(aw, "ACT_DIR", str(act))
    monkeypatch.setattr(servicio, "ERRORES_JS", str(tmp_path / "errores_js.jsonl"))
    servicio._ERRJS_CUENTA.clear()
    dj = aw._armar_data("safari", "Ana", "8", 1, True)
    pers = []
    for i in range(8):
        shutil.copy(os.path.join(_BASE, "actividades_arte", "g3", "s%02d.png" % i), d)
        pers.append("s%02d.png" % i)
    dj.update(personajes=pers, sombras=pers)
    (d / "data.json").write_text(json.dumps(dj, ensure_ascii=False), encoding="utf-8")
    (d / "manifest.json").write_text(json.dumps({"titulo": "Cuaderno de prueba"}))
    srv = ThreadingHTTPServer(("127.0.0.1", 0), servicio.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield {"url": "http://127.0.0.1:%d/act/%s/" % (srv.server_address[1], TOK), "dir": d,
           "errores": tmp_path / "errores_js.jsonl", "tmp": tmp_path}
    srv.shutdown()
    srv.server_close()


def _lineas(p):
    if not os.path.isfile(p):
        return []
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def _abrir(p, url):
    nav = p.chromium.launch()
    ctx = nav.new_context(viewport={"width": 412, "height": 839})
    ctx.add_init_script("localStorage.setItem(%r, JSON.stringify({activeProfile: 'Ana',"
                        " profiles: {Ana: {stars: {}}}}));" % CLAVE)
    return nav, ctx.new_page()


# ── INF-22 ──────────────────────────────────────────────────────────────────────────

@sin_navegador
def test_un_error_de_js_llega_sin_el_token_ni_el_nombre(cuaderno):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav, pag = _abrir(p, cuaderno["url"])
        pag.goto(cuaderno["url"], wait_until="domcontentloaded", timeout=60000)
        pag.wait_for_function("() => !document.getElementById('cargando')", timeout=60000)
        pag.evaluate("() => setTimeout(() => { throw new Error('se rompió en ' + location.href); }, 0)")
        pag.wait_for_timeout(800)
        nav.close()
    lin = _lineas(cuaderno["errores"])
    assert len(lin) == 1, lin
    e = lin[0]
    assert "se rompió en" in e["m"]
    assert e["cuaderno"] == hashlib.sha256(TOK.encode()).hexdigest()[:10]
    assert e["edad"] == "8"
    crudo = open(cuaderno["errores"], encoding="utf-8").read()
    assert TOK not in crudo, "el token abre el cuaderno de un chico: no puede quedar anotado"
    assert "Ana" not in crudo


@sin_navegador
def test_si_player_js_no_se_puede_leer_igual_se_entera(cuaderno, monkeypatch):
    """El caso del iPhone viejo (MOT-05): un error de SINTAXIS en player.js. El manejador
    está en el HTML, antes, así que lo ve."""
    roto = cuaderno["tmp"] / "player_roto.js"
    roto.write_text("const x = ;\n", encoding="utf-8")
    monkeypatch.setattr(aw, "TEMPLATE_JS", str(roto))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav, pag = _abrir(p, cuaderno["url"])
        pag.goto(cuaderno["url"], wait_until="load", timeout=60000)
        pag.wait_for_timeout(1000)
        nav.close()
    lin = _lineas(cuaderno["errores"])
    assert any(e["f"] == "player.js" and "Syntax" in e["m"] for e in lin), lin


@sin_navegador
def test_una_pagina_que_tira_errores_en_loop_no_llena_el_disco(cuaderno):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav, pag = _abrir(p, cuaderno["url"])
        pag.goto(cuaderno["url"], wait_until="domcontentloaded", timeout=60000)
        pag.wait_for_function("() => !document.getElementById('cargando')", timeout=60000)
        pag.evaluate("""() => { for (let i = 0; i < 30; i++)
          setTimeout(() => { throw new Error('error número ' + i); }, 0); }""")
        pag.wait_for_timeout(1000)
        nav.close()
    assert 1 <= len(_lineas(cuaderno["errores"])) <= 5


def test_el_servidor_pone_tope_por_cuaderno_y_rota_el_archivo(cuaderno, monkeypatch):
    import servicio
    assert sum(servicio._error_js_cupo("otro-token-x") for _ in range(50)) == 20
    monkeypatch.setattr(servicio, "ERRORES_JS_TOPE", 300)
    for i in range(20):
        servicio._error_js_anotar({"m": "x" * 50, "i": i})
    assert os.path.getsize(cuaderno["errores"]) < 300 + 200
    assert os.path.isfile(str(cuaderno["errores"]) + ".1")


def test_un_token_que_no_existe_no_anota_nada(cuaderno):
    import urllib.request
    import urllib.error
    base = cuaderno["url"].rsplit("/act/", 1)[0]
    with pytest.raises(urllib.error.HTTPError) as e:
        urllib.request.urlopen(urllib.request.Request(
            base + "/act/no-existe-este-1/error-js", data=b'{"m":"x"}', method="POST"))
    assert e.value.code == 404
    assert not _lineas(cuaderno["errores"])


# ── PRO-19 ──────────────────────────────────────────────────────────────────────────

@sin_navegador
def test_el_video_deja_visto_y_terminado_en_la_telemetria(cuaderno):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav, pag = _abrir(p, cuaderno["url"])
        pag.goto(cuaderno["url"], wait_until="domcontentloaded", timeout=60000)
        pag.wait_for_function("() => !document.getElementById('cargando')", timeout=60000)
        pag.evaluate("""() => {
          VIDEOS_VI = [{ pieza: "sonidos_prueba", titulo: "Sonidos", grado: 3 }];
          abrirVideoInteractivo(VIDEOS_VI[0]);
          window.postMessage({ tipo: "kydo-video-interactivo", datos: { pieza: "sonidos_prueba",
            saber: "x", pasos: [{ primer_intento: true }, { primer_intento: false },
                                { primer_intento: true }] } }, location.origin);
        }""")
        pag.wait_for_timeout(800)
        nav.close()
    tel = [e for e in _lineas(cuaderno["dir"] / "telemetria.jsonl") if e.get("tipo") == "video"]
    assert [e["vi"] for e in tel] == ["visto", "terminado"], tel
    assert all(e["j"] == "vi:sonidos_prueba" for e in tel)
    assert tel[1]["pasos"] == 3 and tel[1]["bien"] == 2
    assert not tel[0]["primer"], "un video no es una respuesta de primer intento"
