# -*- coding: utf-8 -*-
"""Lo que llega tarde de una partida que ya se dejó no hace nada, y dos pestañas del mismo
cuaderno no se borran el progreso (25-sep-2026).

MOT-06: los juegos dejan `setTimeout` andando (la pausa de 1,15 s antes de `win()` en
«Línea de tiempo», el `render()` de la ronda siguiente) y nadie los cancela al salir. Tocar
← en esa pausa festejaba ENCIMA del menú y guardaba estrellas bajo el juego «null»; salir y
abrir otra actividad dejaba que la consigna vieja pisara la nueva — y el `win()` tardío le
regalaba las estrellas a la actividad NUEVA, porque `Shell.actual` ya era ésa.

MOT-17: `Store.save()` escribía el objeto entero que la pestaña tenía en memoria: la otra
pestaña (o una vieja a la que se vuelve con «atrás») borraba lo ganado acá.

Se prueba en un navegador de verdad con un cuaderno armado en una carpeta temporal: el
player es JS de página y lo que importa es cómo se comporta con timers y con localStorage
reales.
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

TOK = "partidas-prueba-4"
CLAVE = "ct3d_act::/act/" + TOK


@pytest.fixture
def cuaderno(tmp_path, monkeypatch):
    import servicio
    monkeypatch.setattr(aw, "ACT_DIR", str(tmp_path))
    d = tmp_path / TOK
    d.mkdir()
    dj = aw._armar_data("safari", "Ana", "9", 1, True)
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


# Un perfil ya elegido, para que el arranque vaya derecho al menú.
_PERFIL = ("localStorage.getItem(%r) || localStorage.setItem(%r, JSON.stringify("
           "{activeProfile: 'Ana', profiles: {Ana: {stars: {}}}}));") % (CLAVE, CLAVE)

# Un juego de mentira que hace lo que hacen los de verdad: escribe la consigna y deja un
# timer que, más tarde, cambia la consigna y gana.
_JUEGO_CON_TIMER = """() => {
  GAMES.__lento = { crear(ctx) {
    ctx.consigna("la de la partida lenta");
    setTimeout(() => { ctx.consigna("CONSIGNA TARDÍA"); ctx.ronda(5); ctx.win(3); }, 400);
  } };
  D.menu.push({ id: "__lento", titulo: "Lento", icono: "🐢", cfg: {}, nivel: 1 });
}"""


def _abrir(p, url):
    nav = p.chromium.launch()
    ctx = nav.new_context(viewport={"width": 412, "height": 839})
    ctx.add_init_script(_PERFIL)
    pag = ctx.new_page()
    errores = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.goto(url, wait_until="domcontentloaded", timeout=60000)
    pag.wait_for_function("() => !document.getElementById('cargando')", timeout=60000)
    return nav, ctx, pag, errores


def _estrellas(pag):
    return pag.evaluate("() => JSON.parse(localStorage.getItem(%r)).profiles.Ana.stars" % CLAVE)


def test_salir_al_menu_en_la_pausa_no_festeja_ni_guarda_null(cuaderno):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav, _ctx, pag, errores = _abrir(p, cuaderno)
        pag.evaluate(_JUEGO_CON_TIMER)
        pag.evaluate("() => { Shell.abrir('__lento'); volverMenu(); }")
        pag.wait_for_timeout(900)
        stars = _estrellas(pag)
        festejo = pag.evaluate("() => document.getElementById('festejo').classList.contains('ver')")
        nav.close()
    assert "null" not in stars and "__lento" not in stars, stars
    assert not festejo, "el festejo de la partida abandonada salió encima del menú"
    assert not errores, errores[:3]


def test_la_partida_vieja_no_pisa_la_consigna_ni_regala_estrellas_a_la_nueva(cuaderno):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav, _ctx, pag, errores = _abrir(p, cuaderno)
        pag.evaluate(_JUEGO_CON_TIMER)
        pag.evaluate("() => { Shell.abrir('__lento'); Shell.abrir('memotest'); }")
        antes = pag.inner_text("#consignaTexto")
        pag.wait_for_timeout(900)
        despues = pag.inner_text("#consignaTexto")
        stars = _estrellas(pag)
        nav.close()
    assert "TARDÍA" not in despues, "la consigna de la actividad anterior pisó la de memotest"
    assert despues == antes
    assert "memotest" not in stars, "el win() tardío le dio las estrellas a la actividad nueva"
    assert not errores, errores[:3]


def test_la_partida_en_pantalla_sigue_ganando(cuaderno):
    """El freno no puede frenar a la partida que SÍ está en pantalla."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav, _ctx, pag, errores = _abrir(p, cuaderno)
        pag.evaluate(_JUEGO_CON_TIMER)
        pag.evaluate("() => { Shell.abrir('__lento'); }")
        pag.wait_for_timeout(900)
        stars = _estrellas(pag)
        consigna = pag.inner_text("#consignaTexto")
        nav.close()
    assert stars.get("__lento") == 3, stars
    assert "TARDÍA" in consigna
    assert not errores, errores[:3]


def test_dos_pestanas_no_se_borran_las_estrellas(cuaderno):
    """El caso del auditor: A gana en memotest, después B (abierta antes, con la memoria
    vieja) gana en sopa. Tienen que quedar las dos."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav, ctx, a, errores = _abrir(p, cuaderno)
        b = ctx.new_page()
        b.on("pageerror", lambda e: errores.append(str(e)))
        b.goto(cuaderno, wait_until="domcontentloaded", timeout=60000)
        b.wait_for_function("() => !document.getElementById('cargando')", timeout=60000)
        a.evaluate("() => Store.setStars('memotest', 3)")
        # B no se entera por la memoria: se simula que el evento `storage` no llegó
        # (pestaña dormida), que es el peor caso — la fusión tiene que estar en el save.
        b.evaluate("() => { Store.data.profiles.Ana.stars = {}; Store.setStars('sopa', 2); }")
        final = _estrellas(b)
        # y la que sí está despierta recibe lo de la otra en memoria, sin recargar
        a.wait_for_timeout(300)
        en_memoria_a = a.evaluate("() => Store.data.profiles.Ana.stars")
        nav.close()
    assert final.get("memotest") == 3 and final.get("sopa") == 2, final
    assert en_memoria_a.get("sopa") == 2, en_memoria_a
    assert not errores, errores[:3]


def test_un_perfil_renombrado_en_esta_pestana_no_resucita(cuaderno):
    """«Peque» → «Ana»: el perfil viejo se borra a propósito; fusionar no lo trae de vuelta."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav, _ctx, pag, errores = _abrir(p, cuaderno)
        perfiles = pag.evaluate("""() => {
          Store.data.profiles.Peque = { stars: { sopa: 1 } }; Store.save();
          Store.data.profiles.Lola = Store.data.profiles.Peque;
          delete Store.data.profiles.Peque; Store.save();
          return Object.keys(JSON.parse(localStorage.getItem(%r)).profiles).sort();
        }""" % CLAVE)
        nav.close()
    assert perfiles == ["Ana", "Lola"], perfiles
    assert not errores, errores[:3]
