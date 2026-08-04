# -*- coding: utf-8 -*-
"""El cuaderno tiene icono en la pestaña, y es el de SU marca.

Pablo, 03-ago-2026: *"poné en la página el icono de kydo como el icono de la pestaña del
navegador"*, y después *"falta el favicon"*.

El cuaderno no tenía NINGUNO. La landing de Kydo sí —`/static/img/kydo-favicon.svg`, con
200— pero el player lo sirve el MOTOR, que es otro servidor y otro árbol, y ahí nunca se
había puesto: la pestaña salía con el icono en blanco del navegador.

VA POR MARCA, igual que el título. El mismo player sirve las dos líneas —Kydo la escolar y
Casatridimensional la de cumpleaños—, así que un favicon único habría puesto la marca
equivocada en la mitad de los cuadernos. Es la misma regla que ya seguía `{{MARCA}}`.
"""
import os
import sys

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import actividades_web as aw  # noqa: E402


def _html_de(escolar):
    """El HTML del cuaderno con la marca pedida, sin depender de tokens reales (el
    registro vive en el árbol de producción, no en el worktree ni en CI)."""
    orig_cargar, orig_esc = aw._cargar, aw._es_escolar
    aw._cargar = lambda t: {"titulo": "Mis Desafíos — 7.º grado"}
    aw._es_escolar = lambda t, reg=None: escolar
    try:
        return aw.html("token-de-prueba") or ""
    finally:
        aw._cargar, aw._es_escolar = orig_cargar, orig_esc


def test_el_cuaderno_declara_un_favicon():
    """Sin esto la pestaña sale con el icono genérico del navegador — que es lo que veía
    Pablo."""
    h = _html_de(True)
    assert '<link rel="icon"' in h, "el cuaderno no declara ningún favicon"
    assert "{{FAVICON}}" not in h, "quedó el placeholder sin reemplazar"


def test_cada_marca_lleva_el_suyo():
    """Un favicon único pondría la marca equivocada en la mitad de los cuadernos."""
    kydo, ct3d = _html_de(True), _html_de(False)
    assert "favicon_kydo.svg" in kydo and "favicon_ct3d.svg" not in kydo
    assert "favicon_ct3d.svg" in ct3d and "favicon_kydo.svg" not in ct3d
    assert "Kydo" in kydo and "Casatridimensional" in ct3d


def test_los_dos_archivos_existen_y_se_sirven():
    """Declararlo no alcanza: el motor sólo entrega lo que está en su lista blanca, y un
    favicon declarado que da 404 deja la pestaña igual de vacía."""
    orig = aw._cargar
    aw._cargar = lambda t: {"titulo": "x"}
    try:
        for n in ("favicon_kydo.svg", "favicon_ct3d.svg"):
            assert os.path.isfile(os.path.join(_BASE, n)), "falta el archivo %s" % n
            r = aw.archivo("token-de-prueba", n)
            assert r, "el motor no sirve %s (¿está en _ASSET_RE?)" % n
            datos, ct = r
            assert ct == "image/svg+xml", "%s sale con content-type %r" % (n, ct)
            assert datos.lstrip().startswith(b"<svg"), "%s no es un SVG" % n
    finally:
        aw._cargar = orig


def test_no_sirve_cualquier_favicon():
    """La lista blanca es lo que impide que el token se convierta en un servidor de
    archivos. Un nombre que no sea uno de los dos no puede pasar."""
    for malo in ("favicon_otro.svg", "favicon_.svg", "favicon_kydo.png", "../secreto.svg"):
        assert not aw._ASSET_RE.fullmatch(malo), "la lista blanca acepta %r" % malo


def test_el_favicon_lleva_la_version():
    """Son archivos del REPO servidos por token: sin `?v=`, cambiar el icono no le llegaría
    nunca al que ya tiene el cuaderno abierto. Es el mismo agujero que tenía el manifest
    de inglés, y que costó una tarde encontrar."""
    h = _html_de(True)
    i = h.index("favicon_kydo.svg")
    assert h[i:i + 30].startswith("favicon_kydo.svg?v="), \
        "el favicon se pide sin versión: un cambio no llega a los cuadernos ya abiertos"


def test_todo_lo_que_el_motor_sirve_es_ALCANZABLE_por_la_ruta():
    """Dos filtros distintos tienen que coincidir, y no coincidían.

    `_ASSET_RE` dice QUÉ se sirve; la ruta de `servicio.py` dice qué NOMBRES llegan
    siquiera a preguntar. Su charset es `[a-z_0-9.]` — **sin guion medio**. Todos los
    assets del repo usan guion BAJO (`motor_adaptativo.js`, `ingles_manifest.json`,
    `audio_manifest.json`), así que nunca se había notado; el favicon entró con guion medio
    y daba 404 aunque estuviera en la lista blanca y el archivo existiera. Se descubrió
    verificando contra producción, no leyendo el código.

    Este test prueba nombres REALES contra las dos rejas a la vez."""
    import re
    ruta_src = open(os.path.join(_BASE, "servicio.py"), encoding="utf-8").read()
    m = re.search(r'r"\^/act/\(\[A-Za-z0-9_-\]\+\)\(\?:/\(([^)]+)\)\)\?\$"', ruta_src)
    assert m, "cambió la ruta de /act/ en servicio.py: revisá este test"
    charset = re.compile("^%s$" % m.group(1))
    nombres = ["favicon_kydo.svg", "favicon_ct3d.svg", "player.js", "data.json",
               "ingles_manifest.json", "audio_manifest.json", "motor_adaptativo.js",
               "duelo.js", "actividades_curriculum.js", "portada.jpg", "escena.jpg"]
    for n in nombres:
        assert aw._ASSET_RE.fullmatch(n), "%s no está en la lista blanca" % n
        assert charset.match(n), \
            ("%s está en la lista blanca pero la ruta de /act/ no lo deja pasar: "
             "daría 404. Los nombres van con guion BAJO." % n)
