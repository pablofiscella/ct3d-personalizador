"""El player tiene que EJECUTARSE, no sólo decir lo que corresponde.

POR QUÉ EXISTE
──────────────
20-ago-2026. Arreglando un texto que salía en español, quedó así:

    D.targets.forEach((t) => {            // `t` es el nivel…
        ...  ${t("piezasSolo")}  ...      // …y acá se llama a la función `t()`

`t` es el nombre de la función de traducción, global. Usarla como variable de bucle la
tapa: `t("piezasSolo")` intenta llamar a un número y lanza «t is not a function». Efecto
para el usuario: **toca una carta y ve una pantalla en blanco**, sin ningún mensaje.

Se promovió a producción con **2192 tests en verde**, porque los 2192 miran el player
como TEXTO —que las frases estén, que tengan su inglés, que no haya literales sueltos— y
ninguno lo ejecuta. Un error de sintaxis lo hubiera cazado `node --check`; éste no es de
sintaxis: es válido y revienta al correr.

Peor: la misma línea con el mismo error existía desde el día anterior en la rama del modo
demo, o sea que el botón «Probalo gratis» de la tienda estaba roto y nadie se enteró.

QUÉ HACE
────────
Levanta el motor, abre el player en un navegador de verdad, toca una carta y comprueba
que la pantalla siguiente aparezca y que la consola no tenga un solo error. No mira el
juego en detalle: mira que ARRANQUE. Es el único test de este repo que ejecuta el JS.
"""
import json
import os
import shutil
import sys
import threading
import time
from http.server import ThreadingHTTPServer

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sin_navegador = pytest.mark.skipif(
    __import__("importlib").util.find_spec("playwright") is None,
    reason="no hay playwright instalado")


def _data_json_jugable(tema="safari"):
    """Lo mínimo que el player necesita para dibujar el menú y la pantalla de niveles.

    No se genera un rompecabezas de verdad —tarda minuto y medio— porque lo que se prueba
    es que el JAVASCRIPT corra, no que la imagen sea linda."""
    bordes = {}
    grillas = {}
    for t, (c, f) in {"4": (2, 2), "6": (2, 3), "12": (3, 4), "20": (4, 5),
                      "30": (5, 6), "48": (6, 8), "100": (10, 10)}.items():
        clave = "%dx%d" % (c, f)
        grillas[t] = clave
        bordes[clave] = {"v": [], "h": []}
    return {
        "v": 1, "tema": tema, "tema_nombre": "Safari", "nombre": "Emma",
        "titulo": "Emma\u2019s puzzles", "idioma": "en",
        "paleta": {"fondo": "#faf3e0", "tinta": "#5a4230", "acento": "#c8674e"},
        "targets": [4, 6, 12, 20, 30, 48],
        "masco": None,
        "puzzles": [{"img": "p%d.jpg" % i, "thumb": "t%d.jpg" % i,
                     "w": 800, "h": 1000, "grillas": grillas} for i in range(6)],
        "bordes": bordes,
    }


@pytest.fixture
def servidor(monkeypatch, tmp_path):
    import rompecabezas_web as rw
    import servicio

    rompe = tmp_path / "rompe"
    rompe.mkdir()
    monkeypatch.setattr(rw, "ROMPE_DIR", str(rompe))

    tok = "playerandando1"
    d = rompe / tok
    d.mkdir()
    (d / "manifest.json").write_text(json.dumps(
        {"tema": "safari", "nombre": "Emma", "titulo": "x",
         "creado": int(time.time()), "idioma": "en"}))
    (d / "data.json").write_text(json.dumps(_data_json_jugable()))
    for i in range(6):
        for pre in ("p", "t"):
            (d / ("%s%d.jpg" % (pre, i))).write_bytes(b"\xff\xd8\xff\xe0x")

    srv = ThreadingHTTPServer(("127.0.0.1", 0), servicio.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield srv.server_address[1], tok
    srv.shutdown()
    srv.server_close()


@sin_navegador
def test_el_player_ARRANCA_y_responde_al_primer_toque(servidor):
    """EL test. Si el JS revienta, el usuario ve una pantalla en blanco y nada más."""
    from playwright.sync_api import sync_playwright
    puerto, tok = servidor
    url = "http://127.0.0.1:%d/armar/%s/" % (puerto, tok)

    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_context(viewport={"width": 420, "height": 760}).new_page()
        errores = []
        pag.on("pageerror", lambda e: errores.append(str(e)))
        pag.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)

        pag.goto(url, wait_until="networkidle", timeout=45000)
        pag.wait_for_timeout(2000)
        cartas = pag.query_selector_all(".carta")
        assert cartas, "el menú no dibujó ninguna carta: el player no arrancó"
        assert not errores, "el player tiró errores al cargar: %s" % errores[:3]

        # el primer toque: de la lista a los niveles. Acá es donde reventaba.
        pag.click(".carta")
        pag.wait_for_timeout(1500)
        niveles = pag.query_selector_all(".nivelBtn")
        assert not errores, (
            "tocar una carta rompió el player (el usuario ve una pantalla en blanco): %s"
            % errores[:3])
        assert niveles, "no apareció ningún nivel: la pantalla quedó vacía"
        nav.close()


@sin_navegador
def test_lo_que_el_player_escribe_al_arrancar_esta_en_INGLES(servidor):
    """De paso, el idioma medido sobre lo que se ve —no sobre el diccionario—. Es la
    comprobación que ningún test de texto puede hacer: lo que quedó en la pantalla."""
    from playwright.sync_api import sync_playwright
    puerto, tok = servidor
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_context(viewport={"width": 420, "height": 760}).new_page()
        pag.goto("http://127.0.0.1:%d/armar/%s/" % (puerto, tok),
                 wait_until="networkidle", timeout=45000)
        pag.wait_for_timeout(2000)
        visible = pag.inner_text("body")
        assert "Puzzle" in visible, "las cartas no están en inglés: %r" % visible[:120]
        assert "Rompecabezas" not in visible, (
            "el player escribió español en el producto en inglés: %r" % visible[:120])
        pag.click(".carta")
        pag.wait_for_timeout(1200)
        v2 = pag.inner_text("body")
        assert "piezas" not in v2.lower(), "la pantalla de niveles dice «piezas»: %r" % v2[:150]
        assert "pieces" in v2.lower() or "How many" in v2, v2[:150]
        nav.close()
