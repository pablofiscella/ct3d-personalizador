# -*- coding: utf-8 -*-
"""Dos cosas del cuaderno de 4.º, y las dos son de PRESENTACIÓN.

Pablo, 31-jul-2026, revisando 4.º. Ninguna de las dos era un error de contenido: la
matemática estaba bien. Lo que fallaba era cómo se le muestra al chico, que a esta edad es
la mitad del ejercicio.

1. **La resta pedía papel.** *"La resta con canje tendría que ser como las sumas grandes
   graficadas, porque los números así tendrían que hacerlo en un papel para saber qué valor
   tiene"*. El desbalance estaba en el mismo menú: 4.º mostraba la SUMA en columnas
   (`suma_columnas`) y la resta como una cuenta EN LÍNEA con tres opciones. Y el propio DC
   de ese tema pide el *"algoritmo de resta ANALIZADO"* — que es justo lo que muestra la
   versión en columnas y lo que la de opciones esconde.

   La resta en columnas YA estaba escrita —la usa 3.º— así que se reusa con el rango de
   este grado, en vez de escribir un segundo juego que haga lo mismo. Para eso el catálogo
   estrena la mecánica `reusa`.

2. **La cuenta se iba antes de poder verla.** *"La cuenta paso a paso no se llega a ver
   cómo queda porque se va enseguida a la próxima; debería decir qué número quedó y esperar
   2 segundos"*. Eran las dos cosas: el resultado se escribía pero no se DECÍA, y la pausa
   era de 950 ms — menos de lo que tarda un chico en leer el resultado después de haber
   hecho toda la división paso a paso.
"""
import os
import re
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import actividades_curriculum as cur  # noqa: E402
import actividades_web as aw  # noqa: E402

PLAYER = os.path.join(_BASE, "actividades_player.js")


def _player():
    return open(PLAYER, encoding="utf-8").read()


def _juego(nombre):
    s = _player()
    i = s.index("GAMES.%s = {" % nombre)
    return s[i:s.index("\n};", i)]


def _menu4():
    return {m["id"]: m for m in aw._menu("grande", "9", True) + aw._menu_curricular("9")}


# ── 1. la resta en columnas ──────────────────────────────────────────────────────

def test_la_resta_de_4to_se_ve_en_columnas_como_la_suma():
    """EL pedido. Lo que se compara es lo que el chico ve en el MISMO menú: si la suma se
    grafica y la resta no, la resta le pide papel."""
    a = [x for x in cur.CATALOGO if x["id"] == "resta_canje_4"][0]
    assert a["mecanica"] == "reusa", "la resta de 4.º volvió a ser una cuenta en línea"
    assert a["juego"] == "resta_columnas"
    assert "GAMES.resta_columnas = {" in _player()


def test_el_rango_es_el_que_pide_el_programa_de_4to():
    """El DC de este tema habla de rangos de 10.000 y 100.000: 4 y 5 cifras. Con el default
    del juego (3 y 4) 4.º estaría haciendo la resta de 3.º."""
    m = _menu4()["resta_canje_4"]
    assert m["cfg"]["cifrasMin"] == 4 and m["cfg"]["cifrasMax"] == 5, m["cfg"]
    assert "10.000" in [x for x in cur.CATALOGO if x["id"] == "resta_canje_4"][0]["dc"]


def test_reusar_no_duplica_el_juego():
    """La resta en columnas se escribe UNA vez. Si mañana se arregla un bug del préstamo,
    se arregla para 3.º y para 4.º al mismo tiempo."""
    assert _player().count("GAMES.resta_columnas = {") == 1
    js = open(os.path.join(_BASE, "actividades_curriculum.js"), encoding="utf-8").read()
    assert "GAMES.resta_canje_4 = { crear(ctx) { return GAMES.resta_columnas.crear(ctx); } };" in js


def test_la_mecanica_nueva_verifica_que_el_juego_exista():
    """Una actividad que reusa un juego inexistente aparecería en el menú y no abriría —
    el peor síntoma, porque no da error. La validación del catálogo lo caza antes."""
    problemas = cur.validar()
    assert not problemas, problemas[:3]
    assert "reusa" in cur.MECANICAS


def test_sigue_cubriendo_el_tema_del_programa():
    """No-regresión curricular: el id no cambió, así que el manifiesto de cobertura sigue
    apuntando a la misma actividad y 4.º no pierde el tema M4."""
    import actividades_cobertura as cob
    m4 = [t for t in cob.DC[4] if t["cod"] == "M4"]
    assert m4 and m4[0]["cubre"] == "resta_canje_4"
    assert "resta_canje_4" in _menu4()


def test_la_suma_de_4to_no_se_toco():
    """Lo que ya estaba bien sigue igual: Pablo la puso de EJEMPLO, no de problema."""
    assert "suma_columnas" in _menu4()
    assert "GAMES.suma_columnas = {" in _player()


# ── 2. la cuenta paso a paso ─────────────────────────────────────────────────────

def test_la_cuenta_dice_el_resultado_antes_de_pasar_a_la_siguiente():
    """*"Debería decir qué número quedó"*. Se escribía, no se decía."""
    c = _juego("cuenta_larga")
    assert "cerrarCuenta" in c, "la cuenta volvió a cerrar sin decir el resultado"
    i = c.index("const cerrarCuenta")
    cuerpo = c[i:i + 700]
    assert "reproducirConsigna(texto)" in cuerpo, "el resultado no se dice en voz alta"


def test_la_espera_deja_terminar_la_voz():
    """Tres intentos hasta acertarle, y el del medio fue un error propio.

    950 ms (original) → 2,6 s → 3,5-6 s → y ahí Pablo cazó lo que el techo rompía: *"dijo
    «no sobró nada, 90 dividido 2 es…» y se quedó sin decir lo que faltaba porque se fue a
    otro ejercicio"*. MEDIDO después: la frase de cierre tarda ~2 s en generarse y ~5 s en
    decirse (6,7 a 7,7 s), así que el techo de 6 s la cortaba justo en el resultado — la
    única parte que importa.

    El techo salió de una preocupación mía por el "silencio" de los primeros segundos, que
    Pablo nunca planteó: lo que pidió las dos veces fue MÁS tiempo. Ahora se espera a que
    termine de hablar; el tope alto existe sólo por si el audio se cuelga."""
    c = _juego("cuenta_larga")
    i = c.index("const cerrarCuenta")
    cuerpo = c[i:i + 700]
    assert "reproducirConsigna(texto)" in cuerpo
    assert "Promise.race" in cuerpo, "sin techo, la espera depende de cuánto tarde la voz"
    assert re.search(r"PISO_CIERRE = 3[0-9]{3}", _juego("cuenta_larga")), \
        "el piso de espera bajó de los 3,5 s que pidió Pablo"
    tope = re.search(r"TOPE_COLGADO = (\d+)", _juego("cuenta_larga"))
    assert tope and int(tope.group(1)) >= 10000, \
        "el tope volvió a ser bajo y va a cortar la voz: la frase tarda hasta 7,7 s"


def test_los_tres_finales_de_la_cuenta_cierran_igual():
    """La división termina de tres maneras (sin resto, con resto, y con la comprobación del
    nivel 2). Las tres tienen que darle tiempo: arreglar sólo una dejaba el problema vivo en
    las otras dos."""
    c = _juego("cuenta_larga")
    assert c.count("cerrarCuenta(") >= 3, "algún final de la cuenta sigue pasando de largo"
    assert "finRonda(); return;" not in c, "quedó un final que no espera"


def test_la_cuenta_paso_a_paso_sigue_en_4to():
    """No se arregló sacándola."""
    assert "cuenta_larga" in _menu4()
