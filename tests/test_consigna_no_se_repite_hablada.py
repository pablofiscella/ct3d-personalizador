# -*- coding: utf-8 -*-
"""La voz no dice dos veces seguidas la misma consigna.

29-jul-2026. Pablo, jugando el cuaderno: *"nodos, que dice «pensá cómo está armada
internet», y en cada pregunta lo repite hablando"*. Y después: *"pasa en varios"*.

QUÉ PASABA. Los motores de banco vuelven a poner la consigna en pantalla en cada ronda
—es correcto: el texto tiene que seguir visible— pero `ctx.consigna()` además la
REPRODUCE. En una trivia de 14 preguntas, Valeria decía la misma frase catorce veces.
Medido: **253 de las 325 actividades del catálogo** (trivia, paramétrica, ordenar y
manipular) más 13 juegos propios del player. `juegoClasificar` ya estaba a salvo porque
usaba `consignaVariada`; los otros tres motores, no.

DÓNDE SE ARREGLÓ Y POR QUÉ AHÍ. En `ctx.consigna()`, no en cada motor. Son 76 juegos más
el catálogo entero, y un juego nuevo volvería a traer el problema sin que nadie se
acuerde de la regla. Poniéndolo en el único lugar por el que pasan todos, el arreglo
alcanza también a los que todavía no existen.

QUÉ NO CAMBIA. La consigna sigue apareciendo SIEMPRE en pantalla: lo que se calla es la
repetición hablada. Y si el texto cambia —`consignaVariada`, o un juego que la reescribe
por ronda— vuelve a sonar, que es justo cuando hace falta.
"""
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER = os.path.join(_BASE, "actividades_player.js")

pytestmark = pytest.mark.skipif(shutil.which("node") is None,
                                reason="node no está instalado")


def _src():
    with open(PLAYER, encoding="utf-8") as f:
        return f.read()


def _correr(js):
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-2000:]
    return r.stdout.strip()


def test_la_misma_consigna_suena_una_sola_vez():
    """EL test. Se ejecuta el método `consigna` REAL del player, no una copia."""
    js = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
const m = src.match(/consigna\(txt, pistaSrc\) \{[\s\S]*?\n      \},/);
if (!m) { console.error("no encontré el método consigna()"); process.exit(1); }
let dicho = [];
const $ = () => ({ style: {}, set innerHTML(v) {}, set src(v) {} });
const reproducirConsigna = (t) => { dicho.push(t); };
const self = { _ultConsigna: null };
const ctx = eval("({" + m[0] + "})");
ctx.consigna("Pensá cómo está armada internet.");
ctx.consigna("Pensá cómo está armada internet.");
ctx.consigna("Pensá cómo está armada internet.");
const repetida = dicho.length;
ctx.consigna("¿Y este?");
ctx.consigna("Pensá cómo está armada internet.");
console.log(JSON.stringify({ repetida: repetida, total: dicho.length, dicho: dicho }));
""" % json.dumps(PLAYER)
    r = json.loads(_correr(js))
    assert r["repetida"] == 1, \
        "tres rondas con la misma consigna sonaron %d veces" % r["repetida"]
    assert r["total"] == 3, "al cambiar el texto tiene que volver a sonar"
    assert r["dicho"][1] == "¿Y este?"


def test_la_consigna_siempre_se_escribe_en_pantalla():
    """Callar la voz no puede callar el texto: el chico que no escucha lo lee."""
    src = _src()
    cuerpo = re.search(r"consigna\(txt, pistaSrc\) \{[\s\S]*?\n      \},", src).group(0)
    escribe = cuerpo.index("consignaTexto")
    guarda = cuerpo.index("_ultConsigna")
    assert escribe < guarda, \
        "el texto tiene que escribirse ANTES de decidir si suena, y siempre"


def test_se_resetea_al_entrar_a_un_juego():
    """Volver a abrir la actividad SÍ tiene que decir la consigna otra vez."""
    src = _src()
    abrir = src[src.index("  abrir(id) {"):]
    abrir = abrir[:abrir.index("\n  },")]
    assert "_ultConsigna = null" in abrir, \
        "sin resetear, la consigna no vuelve a sonar al reentrar al juego"


def test_los_motores_de_banco_siguen_poniendo_la_consigna():
    """No se arregló borrando la consigna de los motores: eso la sacaría de pantalla."""
    src = _src()
    for motor in ("juegoTriviaTexto", "juegoTriviaBanco", "juegoParametrico"):
        i = src.index("function %s(" % motor)
        cuerpo = src[i:i + 3000]
        assert "ctx.consigna(" in cuerpo or "consignaVariada(" in cuerpo, \
            "%s dejó de poner la consigna en pantalla" % motor
