# -*- coding: utf-8 -*-
"""«Leé el transportador» (5.º) dibujaba el ángulo. Faltaba la función que lo genera.

Pablo, 03-ago-2026: *"Leé el transportador 5to grado no hay dibujo de ángulo y hay
opciones para responder"*.

Las opciones SON del diseño —la actividad ataca la confusión de leer la escala
equivocada, el clásico "¿40 o 140?", y para eso ofrece las dos lecturas—. Lo que estaba
roto era el dibujo: `GAMES.transportador` llamaba a `_generarAnguloTransportador(...)` y
esa función **no existía en ningún archivo del motor**. La primera línea útil del juego
tiraba `ReferenceError`, así que la consigna alcanzaba a mostrarse —se pide antes— y de
ahí en adelante no se dibujaba nada.

Se revisó el player entero buscando otras funciones llamadas y nunca definidas: era la
única. El test de abajo deja esa barrida corriendo sola.

EL CONTRATO, leído de cómo se usa (`const th = ...`; `usados.push(th)`; `180 - th`):
devuelve un NÚMERO —no `{grados, tipo}` como `_generarAngulo`, que es la de 4.º—,
múltiplo de 10 para que la lectura sea exacta, y nunca 90: ahí las dos escalas coinciden
y no hay nada que confundir, que es justamente lo que la actividad enseña.
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

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


def _angulos(bonus=0, usados=(), n=2000):
    """Corre la función REAL del player n veces y devuelve lo que salió."""
    js = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
function rint(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
const m = src.match(/function _generarAnguloTransportador[\s\S]*?\n\}/);
if (!m) throw new Error("_generarAnguloTransportador no existe en el player");
eval(m[0]);
const out = [];
for (let i = 0; i < %d; i++) out.push(_generarAnguloTransportador(%d, %s));
process.stdout.write(JSON.stringify(out));
""" % (json.dumps(PLAYER), n, bonus, json.dumps(list(usados)))
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[:600]
    return json.loads(r.stdout)


def test_la_funcion_existe():
    """EL test. Sin ella el juego tira ReferenceError y no dibuja nada."""
    src = open(PLAYER, encoding="utf-8").read()
    assert "function _generarAnguloTransportador" in src, \
        "la función que genera el ángulo del transportador no está definida"


def test_devuelve_un_numero_y_no_un_objeto():
    """`_generarAngulo` (4.º) devuelve `{grados, tipo}`; ésta se usa como número crudo
    (`180 - th`). Devolver un objeto daría "180 - [object Object]" = NaN y un SVG vacío,
    que es el mismo síntoma que se está arreglando pero más difícil de ver."""
    assert all(isinstance(g, int) for g in _angulos(n=50))


def test_siempre_multiplo_de_10():
    """La lectura tiene que ser EXACTA sobre las marcas del transportador: con 37° no hay
    nada que leer, y las tres opciones dejarían de tener sentido."""
    assert all(g % 10 == 0 for g in _angulos(n=3000))


def test_nunca_devuelve_90():
    """En 90 las dos escalas coinciden: no hay ninguna confusión que enseñar, que es
    justo el punto de esta actividad."""
    assert 90 not in _angulos(n=3000)


def test_siempre_dentro_del_transportador():
    """El SVG dibuja de 0 a 180. Fuera de ahí el lado móvil se sale del semicírculo."""
    assert all(10 <= g <= 170 for g in _angulos(n=3000))


def test_la_otra_lectura_tambien_es_valida():
    """La opción "equivocada" que ofrece el juego es `180 - th`: si cayera fuera del
    transportador o coincidiera con la correcta, la actividad perdería su razón de ser."""
    for g in set(_angulos(n=1000)):
        otra = 180 - g
        assert 10 <= otra <= 170 and otra != g, g


def test_con_mas_dominio_los_angulos_se_acercan_a_90():
    """La dificultad de leer un transportador NO está en el número: está en elegir la
    escala. Con 40° vs 140° el chico zafa mirando la forma ("se ve agudo, entonces 40");
    con 80 vs 100 no le queda otra que leer. Por eso a más dominio, más cerca de 90."""
    lejos = max(abs(g - 90) for g in _angulos(bonus=0, n=2000))
    cerca = max(abs(g - 90) for g in _angulos(bonus=3, n=2000))
    assert cerca < lejos, "el dominio no cambia la dificultad (%d vs %d)" % (cerca, lejos)


def test_no_repite_dentro_de_la_partida():
    """Ocho rondas con el mismo ángulo dejan de enseñar a la segunda."""
    usados = [10, 20, 30, 40, 50]
    assert not set(_angulos(bonus=0, usados=usados, n=500)) & set(usados)


def test_si_se_agotan_los_angulos_igual_devuelve_uno():
    """Una partida más larga que la banda de dificultad no puede quedarse sin ángulo y
    colgar el juego: repetir es peor que trabarse, pero mucho menos peor."""
    todos = [g for g in range(10, 180, 10) if g != 90]
    salidas = _angulos(bonus=0, usados=todos, n=50)
    assert salidas and all(g in todos for g in salidas)


# ── la barrida: ninguna otra función llamada y nunca definida ───────────────────────────

def test_ninguna_funcion_del_player_queda_sin_definir():
    """Es lo que faltaba para encontrar ESTE bug sin que lo reporte Pablo jugando.

    Se mira sólo el prefijo `_` —los ayudantes del módulo, que es donde vivía el
    faltante— porque el resto de las llamadas son métodos de objeto (`ctx.bien()`),
    parámetros y funciones del navegador, y distinguirlos con una regex daría más ruido
    que señal."""
    src = open(PLAYER, encoding="utf-8").read()
    limpio = re.sub(r"/\*[\s\S]*?\*/", " ", src)
    limpio = re.sub(r"(^|[^:])//[^\n]*", r"\1 ", limpio)
    definidas = set(re.findall(r"function\s+(_[A-Za-z0-9_$]+)", limpio))
    definidas |= set(re.findall(r"(?:const|let|var)\s+(_[A-Za-z0-9_$]+)\s*=", limpio))
    # método corto de objeto: `_ctx() {`, `_nota(f, t0) {`. Son ocho en el player y se
    # llaman como `this._ctx()`; sin esta forma, el test los daba por inexistentes.
    definidas |= set(re.findall(r"^\s*(_[A-Za-z0-9_$]+)\s*\([^)]*\)\s*\{", limpio, re.M))
    llamadas = set(re.findall(r"(?<![.\w$])(_[A-Za-z0-9_$]+)\s*\(", limpio))
    faltan = sorted(llamadas - definidas)
    assert not faltan, "el player llama a funciones que no existen: %s" % faltan
