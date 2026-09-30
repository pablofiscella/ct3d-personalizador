# -*- coding: utf-8 -*-
"""La muestra de UNA actividad no deja pasar a otra, y el festejo entra en la pantalla (30-sep-2026).

EL AGUJERO. El modo `?muestra=<actividad>` —el de las páginas públicas de ejercicios y el de la
landing— escondía el ← y el menú, pero el festejo ofrecía «▶ Seguir: Vida colonial»: abría la
actividad que recomienda el motor, y de ésa a la siguiente. Desde una página pública se recorría el
grado entero. Pablo: *"tiene un agujero. Si le pongo siguiente sigue con la otra actividad y así
pueden usar todo el cuaderno"*. El candado va en `Shell.abrir`, la única puerta.

EL FESTEJO. Una regla vieja les daba a los botones `flex: 1 1 200px` (para botones en fila) y otra,
más nueva, los puso en columna: el 200px pasó a ser el ALTO. Dos pastillas de 200px al final de
cada actividad, en TODOS los cuadernos. Y centrado sin scroll, en una pantalla baja el cartel se
salía por arriba: 152px en el recuadro de la página pública.

Con navegador de verdad: es comportamiento y diseño, y los dos sólo se ven ejecutándolo.
"""
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

pytestmark = pytest.mark.skipif(
    __import__("importlib").util.find_spec("playwright") is None,
    reason="no hay playwright instalado")

TOK = "muestra-prueba-una"          # «muestra-» como las públicas de verdad


@pytest.fixture(scope="module")
def cuaderno(tmp_path_factory):
    import servicio
    tmp = tmp_path_factory.mktemp("muestra")
    viejo = aw.ACT_DIR
    aw.ACT_DIR = str(tmp)
    d = tmp / TOK
    d.mkdir()
    dj = aw._armar_data("safari", "Ana", "7", 1, True)          # 2.º grado
    pers = []
    for i in range(8):
        shutil.copy(os.path.join(_BASE, "actividades_arte", "g4", "s%02d.png" % i), d)
        pers.append("s%02d.png" % i)
    dj.update(personajes=pers, sombras=pers)
    (d / "data.json").write_text(json.dumps(dj, ensure_ascii=False), encoding="utf-8")
    (d / "manifest.json").write_text(json.dumps({"titulo": "Cuaderno de prueba"}))
    ids = [m["id"] for m in dj["menu"]]
    assert "sumas" in ids and "restas" in ids
    srv = ThreadingHTTPServer(("127.0.0.1", 0), servicio.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield "http://127.0.0.1:%d/act/%s/" % (srv.server_address[1], TOK)
    srv.shutdown()
    srv.server_close()
    aw.ACT_DIR = viejo


def _abrir(url, ancho=390, alto=740):
    from playwright.sync_api import sync_playwright
    p = sync_playwright().start()
    nav = p.chromium.launch()
    pag = nav.new_context(viewport={"width": ancho, "height": alto}).new_page()
    errores = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.goto(url, wait_until="domcontentloaded", timeout=60000)
    pag.wait_for_function("() => !document.getElementById('cargando')", timeout=60000)
    pag.wait_for_timeout(600)
    return p, nav, pag, errores


_FESTEJO = """() => {
  const f = document.getElementById('festejo'), r = f.querySelector('.caja').getBoundingClientRect();
  const vis = (id) => { const b = document.getElementById(id); return !!(b && b.offsetParent); };
  return {
    seguir: vis('btnSeguir'), duelo: vis('btnDuelo'), otra_vez: vis('btnOtraVez'),
    altos: [...f.querySelectorAll('.botones .btn')].filter(b => b.offsetParent)
             .map(b => Math.round(b.getBoundingClientRect().height)),
    arriba: Math.round(r.top),
  };
}"""


def test_en_la_muestra_no_se_puede_pasar_a_otra_actividad(cuaderno):
    p, nav, pag, errores = _abrir(cuaderno + "?muestra=sumas")
    try:
        assert pag.evaluate("() => Shell.actual") == "sumas"
        pag.evaluate("() => festejar(3)")
        pag.wait_for_timeout(400)
        f = pag.evaluate(_FESTEJO)
        assert not f["seguir"], "el festejo ofrece «Seguir» a otra actividad"
        assert not f["duelo"], "el duelo abre otra actividad"
        assert f["otra_vez"]
        # y aunque algo pida otra actividad, la puerta no la abre
        pag.evaluate("() => { cerrarFestejo(); Shell.abrir('restas'); }")
        pag.wait_for_timeout(300)
        assert pag.evaluate("() => Shell.actual") == "sumas"
        assert not errores, errores
    finally:
        nav.close()
        p.stop()


def test_el_cuaderno_de_siempre_sigue_ofreciendo_seguir(cuaderno):
    """El candado es SÓLO de la muestra: el cuaderno de una familia no cambia."""
    p, nav, pag, errores = _abrir(cuaderno)
    try:
        pag.evaluate("() => { Shell.abrir('sumas'); festejar(3); }")
        pag.wait_for_timeout(400)
        assert pag.evaluate(_FESTEJO)["seguir"], "el cuaderno perdió el «Seguir»"
        pag.evaluate("() => { cerrarFestejo(); Shell.abrir('restas'); }")
        pag.wait_for_timeout(300)
        assert pag.evaluate("() => Shell.actual") == "restas"
        assert not errores, errores
    finally:
        nav.close()
        p.stop()


@pytest.mark.parametrize("ancho,alto", [(390, 740), (830, 460), (1280, 800)],
                         ids=["celular", "recuadro-pagina-publica", "pc"])
def test_los_botones_del_festejo_tienen_tamano_de_boton_y_el_cartel_no_se_corta(cuaderno, ancho, alto):
    p, nav, pag, _ = _abrir(cuaderno, ancho, alto)
    try:
        pag.evaluate("() => { Shell.abrir('sumas'); festejar(3); }")
        pag.wait_for_timeout(500)
        f = pag.evaluate(_FESTEJO)
        assert f["altos"] and max(f["altos"]) <= 80, "botones de %s px de alto" % f["altos"]
        assert f["arriba"] >= 0, "el cartel se sale %d px por arriba" % -f["arriba"]
    finally:
        nav.close()
        p.stop()
