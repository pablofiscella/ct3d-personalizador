# -*- coding: utf-8 -*-
"""Pedir ayuda no puede valer lo mismo que resolverlo.

Pablo, 31-jul-2026, probando 4.º: *"en «suma con cifras» puse ayuda y completó el número.
Puse ayuda, ayuda, ayuda hasta completar el número y me dijo excelente"*.

Tenía razón y era DOBLE:

1. **La ayuda de la suma COMPLETABA la cifra.** El botón llamaba a `resolverColumna()` con
   el dígito correcto, o sea exactamente lo mismo que acertar: escribía el número y pasaba a
   la columna siguiente. Se podía terminar la cuenta entera sin sumar nada. Su hermana, la
   resta en columnas, ya lo hacía bien: EXPLICA la columna y el chico tiene que tocar la
   cifra. Ahora las dos hacen lo mismo.

2. **Usarla puntuaba igual.** Ninguna de las dos anotaba que se había pedido ayuda, así que
   el chico terminaba con 3★ — y 3★ es lo que marca DOMINIO y le sube el nivel de dificultad
   para la próxima. El motor adaptativo se convencía de que domina algo que no hizo y le
   endurecía la actividad. Es justo lo que el propio `ctx.win` dice que quiere evitar: *"las
   estrellas miden DOMINIO real, no «completé»"*.

EL FESTEJO DE COMPLETAR SE MANTIENE. Pedir ayuda es legítimo y no se castiga con una
pantalla triste: lo único que cambia es cuántas estrellas.

VERIFICADO EN EL NAVEGADOR, no leyendo el código: apretando Ayuda 70 veces seguidas los
casilleros quedan vacíos y las estrellas en 0.
"""
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

PLAYER = os.path.join(_BASE, "actividades_player.js")

COLUMNAS = ("suma_columnas", "resta_columnas")


def _src():
    return open(PLAYER, encoding="utf-8").read()


def _juego(nombre):
    s = _src()
    i = s.index("GAMES.%s = {" % nombre)
    return s[i:s.index("\n};", i)]


# ── 1. la ayuda explica, no completa ─────────────────────────────────────────────

def test_la_ayuda_de_la_suma_ya_no_completa_la_cifra():
    """EL bug. Si esto vuelve, se puede terminar la cuenta sin sumar nada."""
    c = _juego("suma_columnas")
    assert "btnAyuda.addEventListener(\"click\", () => resolverColumna(" not in c, \
        "la ayuda volvió a escribir la cifra correcta"
    assert 'btnAyuda.addEventListener("click", mostrarAyuda)' in c


@pytest.mark.parametrize("juego", COLUMNAS)
def test_las_dos_ayudan_igual(juego):
    """La suma y la resta son la misma mecánica: que una explique y la otra resuelva era una
    diferencia que sólo se notaba jugando."""
    c = _juego(juego)
    assert "const mostrarAyuda" in c, "%s no tiene una ayuda que explique" % juego
    i = c.index("const mostrarAyuda")
    cuerpo = c[i:i + 1400]
    assert "reproducirConsigna(txt)" in cuerpo, "%s: la ayuda no se dice en voz alta" % juego
    assert "resolverColumna" not in cuerpo, "%s: la ayuda todavía resuelve" % juego


def test_la_ayuda_de_la_suma_explica_el_acarreo():
    """No alcanza con no resolver: tiene que ENSEÑAR. El acarreo es justo lo que el chico no
    ve, y es de lo que trata la actividad."""
    c = _juego("suma_columnas")
    i = c.index("const mostrarAyuda")
    cuerpo = c[i:i + 1400]
    assert "te llevás 1" in cuerpo, "la ayuda no explica qué pasa cuando pasa de 10"


# ── 2. usarla no da dominio ──────────────────────────────────────────────────────

@pytest.mark.parametrize("juego", COLUMNAS)
def test_se_anota_que_se_uso_la_ayuda(juego):
    c = _juego(juego)
    assert "let rondasConAyuda = 0" in c, "%s no cuenta las ayudas" % juego
    assert "ayudaEnEstaRonda = true; rondasConAyuda++" in c, \
        "%s: la ayuda no queda anotada" % juego
    assert "ctx.win(_estrellasConAyuda(rondasConAyuda, rondas))" in c, \
        "%s: las estrellas no miran si hubo ayuda" % juego


@pytest.mark.parametrize("juego", COLUMNAS)
def test_se_cuenta_una_vez_por_ronda_y_no_por_toque(juego):
    """Si contara los TOQUES, apretar dos veces en la misma columna valdría el doble; lo que
    importa es en cuántas cuentas necesitó ayuda."""
    c = _juego(juego)
    assert "let ayudaEnEstaRonda = false" in c
    assert "if (!ayudaEnEstaRonda)" in c


@pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")
def test_con_ayuda_nunca_llega_a_tres_estrellas():
    """3★ es lo que marca dominio y sube el nivel: con ayuda no se puede llegar. La función
    se corre de verdad, no se lee."""
    js = ('const fs=require("fs");const src=fs.readFileSync(%s,"utf8");'
          'eval(src.match(/function _estrellasConAyuda[\\s\\S]*?\\n\\}/)[0]);'
          'console.log(JSON.stringify([0,1,2,3,4,5,6].map(a=>_estrellasConAyuda(a,6))));'
          % json.dumps(PLAYER))
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-800:]
    got = json.loads(r.stdout.strip())
    assert got[0] is None, "sin ayuda tiene que puntuar como siempre"
    assert all(v is not None and v <= 2 for v in got[1:]), \
        "con ayuda se sigue pudiendo sacar 3 estrellas: %s" % got
    assert got[4] == 1 and got[1] == 2, \
        "pedir ayuda en MÁS de la mitad de las cuentas tiene que valer menos: %s" % got


def test_sin_ayuda_no_cambia_nada():
    """No-regresión: el que la resuelve solo puntúa exactamente como antes. `undefined` deja
    que `ctx.win` use su cálculo de precisión de siempre."""
    c = _src()
    i = c.index("function _estrellasConAyuda")
    cuerpo = c[i:i + 400]
    assert "if (!rondasConAyuda) return undefined;" in cuerpo


def test_el_festejo_de_completar_se_mantiene():
    """Pedir ayuda es legítimo. Lo que baja son las estrellas, no el festejo: `ctx.win` se
    sigue llamando, así que el chico igual llega a la pantalla de "¡lo lograste!"."""
    for juego in COLUMNAS:
        assert "ctx.win(" in _juego(juego), "%s dejó de festejar" % juego
        assert "ctx.bien()" in _juego(juego)
