# -*- coding: utf-8 -*-
"""El panel «para grandes» dice el grado del cuaderno y no promete nada (25-sep-2026).

Auditoría EXP-17 / PRO-17: al llegar una materia al 80 %, el panel decía «¡Ya domina X de
4°!» y ofrecía «Desbloquear X de 5°» ESCRITOS FIJOS, en cualquier grado; el botón respondía
«Te vamos a mandar el acceso… (demo — el flujo de compra se termina de definir)» y no
mandaba nada. Además decía «Esta semana domina N» con el total acumulado y mostraba
«Extras» como si fuera una materia.

Se abre el panel de verdad en un navegador, con el resumen del motor adaptativo fijado a
mano para no tener que jugar cien partidas.
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

TOK = "panel-grandes-2"
CLAVE = "ct3d_act::/act/" + TOK


@pytest.fixture
def url(tmp_path, monkeypatch):
    import servicio
    monkeypatch.setattr(aw, "ACT_DIR", str(tmp_path))
    d = tmp_path / TOK
    d.mkdir()
    dj = aw._armar_data("safari", "Ana", "7", 1, True)
    pers = []
    for i in range(8):
        shutil.copy(os.path.join(_BASE, "actividades_arte", "g2", "s%02d.png" % i), d)
        pers.append("s%02d.png" % i)
    dj.update(personajes=pers, sombras=pers)
    (d / "data.json").write_text(json.dumps(dj, ensure_ascii=False), encoding="utf-8")
    (d / "manifest.json").write_text(json.dumps({"titulo": "Cuaderno de prueba"}))
    srv = ThreadingHTTPServer(("127.0.0.1", 0), servicio.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield "http://127.0.0.1:%d/act/%s/" % (srv.server_address[1], TOK)
    srv.shutdown()
    srv.server_close()


def _panel(url, escolar, edad):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav = p.chromium.launch()
        ctx = nav.new_context(viewport={"width": 412, "height": 839})
        ctx.add_init_script("localStorage.setItem(%r, JSON.stringify({activeProfile: 'Ana',"
                            " profiles: {Ana: {stars: {}}}}));" % CLAVE)
        pag = ctx.new_page()
        errores = []
        pag.on("pageerror", lambda e: errores.append(str(e)))
        pag.goto(url, wait_until="domcontentloaded", timeout=60000)
        pag.wait_for_function("() => !document.getElementById('cargando')", timeout=60000)
        pag.evaluate("""([escolar, edad]) => {
          D.escolar_on = escolar; D.edad = edad;
          Adapt.resumenPorCategoria = () => ({
            matematica: { dom: 9, proc: 0, pend: 1, total: 10 },
            lengua: { dom: 1, proc: 2, pend: 7, total: 10 },
            logica: { dom: 1, proc: 0, pend: 0, total: 1 } });
          panelPadres();
        }""", [escolar, edad])
        texto = pag.evaluate("() => document.getElementById('cerrarPadres').parentElement.innerText")
        botones = pag.evaluate("() => document.querySelectorAll('[data-upsell]').length")
        nav.close()
    assert not errores, errores[:3]
    return texto, botones


def test_en_un_cuaderno_de_2do_dice_2do_y_no_4to(url):
    texto, botones = _panel(url, True, 7)
    assert "¡Ya domina Matemática de 2.º!" in texto, texto[:600]
    assert "4°" not in texto and "5°" not in texto
    assert "lo de 3.º" in texto


def test_no_hay_boton_de_demo_ni_promesa_de_mail(url):
    texto, botones = _panel(url, True, 7)
    assert botones == 0
    assert "demo" not in texto.lower()
    assert "Desbloquear" not in texto


def test_el_total_no_se_llama_esta_semana_y_extras_no_es_materia(url):
    texto, _ = _panel(url, True, 7)
    assert "Esta semana" not in texto
    assert "Hasta hoy Ana domina 10 temas" in texto, "el total es de las materias, sin Extras"
    assert "Extras" not in texto


def test_el_de_cumpleanos_no_inventa_un_grado(url):
    """El cuaderno de Casatridimensional no es de un grado: festeja sin decir «de N.º»."""
    texto, _ = _panel(url, False, 6)
    assert "¡Ya domina Matemática!" in texto
    assert ".º" not in texto
