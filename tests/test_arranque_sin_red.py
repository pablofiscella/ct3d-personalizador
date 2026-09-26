# -*- coding: utf-8 -*-
"""Si el arranque no llega, el cuaderno lo DICE y deja probar de nuevo.

POR QUÉ EXISTE (25-sep-2026, auditoría, hallazgo MOT-04)
──────────────────────────────────────────────────────────
`boot()` hacía `fetch("data.json")` y `r.json()` sin mirar nada, y el player, el catálogo
curricular y el motor se cargan como tres `<script>` sueltos. Probado con Chromium bloqueando
cada uno:

- si `data.json` no llega → «Preparando tus juegos…» para siempre, «Failed to fetch» en una
  consola que nadie mira;
- si `player.js` no llega → «GAMES is not defined» y la misma pantalla congelada.

Sin reintento, sin botón, sin una palabra. Con la conexión intermitente del celular de
muchas familias, un corte justo en el arranque dejaba al chico frente a una pantalla muerta y
al padre sin saber si era el cuaderno o su señal. Es la primera impresión del producto.

QUÉ SE PIDE AHORA
─────────────────
- `data.json` se reintenta solo, corto (tres intentos en unos tres segundos): un corte de un
  segundo no se tiene que notar.
- Si igual no llega —o llega una página de error en vez del JSON, que es lo que devuelve
  Cloudflare con el servidor caído—, se muestra un mensaje que entiende un chico y un adulto,
  y un botón «Probar de nuevo» que, cuando la red vuelve, arranca el cuaderno de verdad.
- Si lo que no llega es un script, el mismo mensaje: ahí `boot()` ni existe, así que el aviso
  vive en el HTML.

Se prueba en un navegador de verdad, cortando la red con `page.route` (no hay servidor: los
archivos se sirven desde una carpeta temporal armada con `actividades_web.crear`, que no llama
a ninguna IA).
"""
import json
import os
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

sin_navegador = pytest.mark.skipif(
    __import__("importlib").util.find_spec("playwright") is None,
    reason="no hay playwright instalado")

TOK = "test-arranque-sinred1"
URL = "http://cuaderno.test/act/%s/" % TOK

_CT = {".json": "application/json", ".js": "text/javascript", ".png": "image/png",
       ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".ttf": "font/ttf",
       ".html": "text/html; charset=utf-8"}


@pytest.fixture(scope="module")
def carpeta(tmp_path_factory):
    """La carpeta del token tal como la sirve el motor: el HTML con sus marcas resueltas, los
    scripts del REPO y el data.json + arte de una generación real (en tmp)."""
    import actividades_web as aw
    raiz = tmp_path_factory.mktemp("act")
    mp = pytest.MonkeyPatch()
    mp.setattr(aw, "ACT_DIR", str(raiz))
    try:
        aw.crear({"nombre": "Sofía", "edad": "8"}, "safari", token=TOK)
    finally:
        mp.undo()
    d = raiz / TOK
    html = open(aw.TEMPLATE_HTML, encoding="utf-8").read()
    html = (html.replace("{{TITULO}}", "Cuaderno").replace("{{MARCA}}", "Kydo")
                .replace("{{FAVICON}}", "favicon_kydo.svg").replace("{{SENO}}", "null")
                .replace("{{V}}", "t"))
    (d / "index.html").write_text(html, encoding="utf-8")
    for nombre, src in (("player.js", aw.TEMPLATE_JS), ("motor_adaptativo.js", aw.TEMPLATE_MOTOR),
                        ("actividades_curriculum.js", aw.TEMPLATE_CURRICULUM),
                        ("duelo.js", aw.TEMPLATE_DUELO)):
        (d / nombre).write_bytes(open(src, "rb").read())
    return d


class _Red:
    """Sirve la carpeta y deja cortar archivos a pedido. `pedidos` cuenta cuántas veces se
    pidió cada uno, para ver el reintento."""

    def __init__(self, carpeta):
        self.carpeta = carpeta
        self.cortar = {}        # nombre → "abort" | "502" | n (cortar las primeras n veces)
        self.pedidos = {}

    def __call__(self, route):
        path = route.request.url.split("?", 1)[0]
        nombre = path.rsplit("/", 1)[-1] or "index.html"
        self.pedidos[nombre] = self.pedidos.get(nombre, 0) + 1
        modo = self.cortar.get(nombre)
        if isinstance(modo, int):
            if self.pedidos[nombre] <= modo:
                return route.abort("internetdisconnected")
        elif modo == "abort":
            return route.abort("internetdisconnected")
        elif modo == "sintaxis":
            # lo que ve un navegador viejo: el archivo LLEGA, pero no lo entiende
            return route.fulfill(status=200, content_type="text/javascript",
                                 body="var boot = function () { return 1 @@ 2; };")
        elif modo == "502":
            return route.fulfill(status=502, content_type="text/html",
                                 body="<html><body>Bad gateway</body></html>")
        p = self.carpeta / nombre
        if not p.is_file():
            return route.fulfill(status=404, body="")
        return route.fulfill(status=200, body=p.read_bytes(),
                             content_type=_CT.get(p.suffix, "application/octet-stream"))


def _abrir(carpeta, cortar):
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    nav = pw.chromium.launch()
    pag = nav.new_context(viewport={"width": 420, "height": 760}).new_page()
    red = _Red(carpeta)
    red.cortar.update(cortar)
    pag.route("http://cuaderno.test/**", red)
    errores = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.goto(URL, wait_until="domcontentloaded", timeout=30000)
    return pw, nav, pag, red, errores


def _cerrar(pw, nav):
    nav.close()
    pw.stop()


def _arranco(pag):
    """Arrancó = se fue «Preparando tus juegos…» y hay algo para tocar (¿Quién juega? o el menú)."""
    return pag.evaluate("() => !document.getElementById('cargando')")


@sin_navegador
def test_sin_data_json_avisa_y_el_boton_arranca_cuando_vuelve_la_red(carpeta):
    """EL bug: antes esto quedaba en «Preparando tus juegos…» para siempre."""
    pw, nav, pag, red, _ = _abrir(carpeta, {"data.json": "abort"})
    try:
        pag.wait_for_selector("#cargando .carga-fallo", timeout=12000)
        texto = pag.inner_text("#cargando")
        assert "No se pudieron cargar los juegos" in texto, texto
        assert "Probar de nuevo" in texto, texto
        assert red.pedidos.get("data.json") == 3, (
            "data.json no se reintentó antes de rendirse: %s pedidos" % red.pedidos.get("data.json"))
        # vuelve la red → el botón arranca el cuaderno de verdad
        red.cortar.pop("data.json")
        pag.click("#cargando button")
        pag.wait_for_function("() => !document.getElementById('cargando')", timeout=15000)
        assert pag.is_visible("#perfil") or pag.query_selector(".carta"), \
            "el botón sacó el aviso pero el cuaderno no arrancó"
    finally:
        _cerrar(pw, nav)


@sin_navegador
def test_un_corte_corto_no_se_nota(carpeta):
    """Falla el primer pedido y el segundo anda: arranca solo, sin mostrar ningún aviso."""
    pw, nav, pag, red, errores = _abrir(carpeta, {"data.json": 1})
    try:
        pag.wait_for_function("() => !document.getElementById('cargando')", timeout=15000)
        assert red.pedidos.get("data.json") == 2, red.pedidos
        assert not errores, errores[:3]
    finally:
        _cerrar(pw, nav)


@sin_navegador
def test_una_pagina_de_error_en_vez_del_json_tambien_avisa(carpeta):
    """Con el servidor caído Cloudflare contesta 502 con HTML: `r.json()` revienta. Antes
    también quedaba congelado."""
    pw, nav, pag, red, _ = _abrir(carpeta, {"data.json": "502"})
    try:
        pag.wait_for_selector("#cargando .carga-fallo", timeout=12000)
        assert "Probar de nuevo" in pag.inner_text("#cargando")
    finally:
        _cerrar(pw, nav)


@sin_navegador
@pytest.mark.parametrize("script", ["player.js", "actividades_curriculum.js"])
def test_si_no_llega_un_script_tambien_avisa(carpeta, script):
    """Sin player.js no existe `boot()`; sin el catálogo curricular el cuaderno abriría con
    el menú casi vacío. En los dos casos el aviso lo pone el HTML."""
    pw, nav, pag, red, _ = _abrir(carpeta, {script: "abort"})
    try:
        pag.wait_for_selector("#cargando .carga-fallo", timeout=12000)
        pag.wait_for_timeout(1500)
        assert pag.query_selector("#cargando .carga-fallo"), \
            "el aviso apareció y el arranque lo pisó"
        assert "Probar de nuevo" in pag.inner_text("#cargando")
    finally:
        _cerrar(pw, nav)


@sin_navegador
def test_con_la_red_bien_arranca_como_siempre(carpeta):
    pw, nav, pag, red, errores = _abrir(carpeta, {})
    try:
        pag.wait_for_function("() => !document.getElementById('cargando')", timeout=15000)
        assert red.pedidos.get("data.json") == 1, red.pedidos
        assert not errores, errores[:3]
    finally:
        _cerrar(pw, nav)


@sin_navegador
@pytest.mark.parametrize("script", ["player.js", "actividades_curriculum.js"])
def test_si_el_navegador_no_entiende_el_script_no_dice_que_es_la_conexion(carpeta, script):
    """26-sep-2026. Un script que LLEGA pero el navegador rechaza por sintaxis (Safari de iOS
    15 con un regex nuevo, MOT-05) no se arregla reintentando: el aviso tiene que sugerir
    actualizar el navegador o abrir el link en otro, y no «revisá la conexión»."""
    pw, nav, pag, red, _ = _abrir(carpeta, {script: "sintaxis"})
    try:
        pag.wait_for_selector("#cargando .carga-fallo", timeout=12000)
        texto = pag.inner_text("#cargando")
        assert "navegador" in texto and ("Actualizá" in texto or "otro navegador" in texto), texto
        assert "Probar de nuevo" not in texto, "a un navegador viejo le ofrece reintentar"
        assert "conexión" not in texto, texto
        assert pag.query_selector("#cargando button"), "sin el botón para copiar el link"
    finally:
        _cerrar(pw, nav)
