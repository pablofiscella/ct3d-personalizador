# -*- coding: utf-8 -*-
"""La sopa de letras entra ENTERA en su tarjeta, en cualquier ventana (28-sep-2026).

Reporte desde una PC con Windows y Chrome, en la muestra pública de 4.º grado: *«se ve la mitad
de la cuadrícula»*. Pablo lo probó en modo «responsive» y lo veía bien — y tenía razón: en los
anchos de celular no pasa.

Pasaba en las ventanas ANCHAS Y BAJAS, que son de las más comunes en Windows: una notebook de
1366x768, o una PC de 1920x1080 con la escala de pantalla al 150 %. El lado de la grilla salía del
ALTO de la ventana y la letra salía del ANCHO (`clamp(15px, 3.4vw, 24px)`): grilla de 212 px con
letras de 24 px. Diez letras no entraban, cada `1fr` se estiraba hasta el ancho de su letra, la
grilla se salía y la tarjeta (`.tablero {overflow:hidden}`) cortaba las dos columnas de la
derecha: 20 de 100 celdas invisibles. Si las palabras que faltaban caían ahí, no había forma de
terminar — el reporte llegó en la ronda 5.

Ahora las columnas son `minmax(0, 1fr)`, la letra sale de la celda, y en esas ventanas las
palabras van al costado (idea de Pablo) para que la grilla use todo el alto.

Se prueba en un navegador de verdad: es un problema de diseño y sólo se ve midiendo.
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

TOK = "sopa-prueba-4"
CLAVE = "ct3d_act::/act/" + TOK
_PERFIL = ("localStorage.getItem(%r) || localStorage.setItem(%r, JSON.stringify("
           "{activeProfile: 'Ana', profiles: {Ana: {stars: {}}}}));") % (CLAVE, CLAVE)

# Ventanas útiles reales de Chrome maximizado (pantalla menos las barras del navegador).
NOTEBOOK = (1366, 657)          # 1366x768, la notebook más común
ESCALA_150 = (1280, 585)        # 1920x1080 con la escala de Windows al 150 %
PC_GRANDE = (1920, 969)         # 1920x1080 al 100 %: acá siempre se vio bien
CELULAR = (390, 740)            # acá también


@pytest.fixture(scope="module")
def cuaderno(tmp_path_factory):
    import servicio
    tmp = tmp_path_factory.mktemp("sopa")
    viejo = aw.ACT_DIR
    aw.ACT_DIR = str(tmp)
    d = tmp / TOK
    d.mkdir()
    dj = aw._armar_data("safari", "Ana", "9", 1, True)    # 4.º grado, como la muestra
    assert {s["n"] for s in dj["sopas"]} == {10}, "el caso del reporte es una sopa de 10x10"
    pers = []
    for i in range(8):
        shutil.copy(os.path.join(_BASE, "actividades_arte", "g4", "s%02d.png" % i), d)
        pers.append("s%02d.png" % i)
    dj.update(personajes=pers, sombras=pers)
    (d / "data.json").write_text(json.dumps(dj, ensure_ascii=False), encoding="utf-8")
    (d / "manifest.json").write_text(json.dumps({"titulo": "Cuaderno de prueba"}))
    srv = ThreadingHTTPServer(("127.0.0.1", 0), servicio.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield "http://127.0.0.1:%d/act/%s/" % (srv.server_address[1], TOK)
    srv.shutdown()
    srv.server_close()
    aw.ACT_DIR = viejo


_MEDIR = """() => {
  const grid = document.querySelector('#sopa');
  const tr = grid.closest('.tablero').getBoundingClientRect();
  const celdas = [...grid.querySelectorAll('.celda')];
  const chips = [...document.querySelectorAll('#sopaPalabras .palabra')];
  return {
    celdas: celdas.length,
    cortadas: celdas.filter(c => { const r = c.getBoundingClientRect();
      return r.right > tr.right + 0.5 || r.left < tr.left - 0.5 || r.bottom > tr.bottom + 0.5; }).length,
    letras_anchas: celdas.filter(c => c.scrollWidth > c.clientWidth).length,
    palabras_fuera: chips.filter(c => c.getBoundingClientRect().bottom > innerHeight + 0.5).length,
    al_costado: document.querySelector('#sopaWrap').classList.contains('alCostado'),
    letra: getComputedStyle(celdas[0]).fontSize,
    celda: celdas[0].getBoundingClientRect().width,
  };
}"""


def _sopa(url, ancho, alto):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav = p.chromium.launch()
        ctx = nav.new_context(viewport={"width": ancho, "height": alto})
        ctx.add_init_script(_PERFIL)
        pag = ctx.new_page()
        errores = []
        pag.on("pageerror", lambda e: errores.append(str(e)))
        pag.goto(url, wait_until="domcontentloaded", timeout=60000)
        pag.wait_for_function("() => !document.getElementById('cargando')", timeout=60000)
        pag.evaluate("() => Shell.abrir('sopa')")
        pag.wait_for_function("() => document.querySelectorAll('#sopa .celda').length > 0")
        pag.wait_for_timeout(400)            # el ajuste corre en el cuadro siguiente
        m = pag.evaluate(_MEDIR)
        nav.close()
    assert not errores, errores
    return m


@pytest.mark.parametrize("ancho,alto", [NOTEBOOK, ESCALA_150, PC_GRANDE, CELULAR],
                         ids=["notebook-1366x768", "windows-escala-150", "pc-1920", "celular"])
def test_la_grilla_entra_entera_y_las_palabras_se_ven(cuaderno, ancho, alto):
    m = _sopa(cuaderno, ancho, alto)
    assert m["celdas"] == 100
    assert m["cortadas"] == 0, "la tarjeta tapa %d celdas de la grilla" % m["cortadas"]
    assert m["letras_anchas"] == 0, "hay %d letras que no entran en su celda" % m["letras_anchas"]
    assert m["palabras_fuera"] == 0, "%d palabras quedan debajo del borde" % m["palabras_fuera"]


def test_en_la_notebook_las_palabras_van_al_costado_y_la_grilla_crece(cuaderno):
    m = _sopa(cuaderno, *NOTEBOOK)
    assert m["al_costado"]
    assert m["celda"] >= 30, "la celda quedó en %.0f px: la grilla no aprovechó el alto" % m["celda"]


def test_donde_ya_se_veia_bien_queda_igual(cuaderno):
    """El arreglo no le cambia nada a quien no tenía el problema."""
    pc = _sopa(cuaderno, *PC_GRANDE)
    assert not pc["al_costado"] and pc["letra"] == "24px"
    cel = _sopa(cuaderno, *CELULAR)
    assert not cel["al_costado"] and cel["letra"] == "15px"
