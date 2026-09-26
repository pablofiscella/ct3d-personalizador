# -*- coding: utf-8 -*-
"""El cuaderno tiene que arrancar en un iPhone con iOS 15 o anterior (25-sep-2026).

Auditoría MOT-05: `actividades_player.js` tenía dos expresiones regulares escritas LITERALES
con sintaxis que Safari recién entiende desde la 16.4 (marzo de 2023):

  - un lookbehind `(?<![\\d.,])` en `_fraccionesEnPalabras`;
  - `\\p{Extended_Pictographic}` en `_opcionesEnPantalla`.

Un regex literal que el navegador no entiende es error de SINTAXIS: el archivo entero no se
ejecuta y el chico ve «Preparando tus juegos…» para siempre. Todos los navegadores de iPhone
usan el motor de Safari, así que quedaban afuera los 6s, 7 y SE de primera generación (no
pasan de iOS 15) y los que están en 16.0-16.3.

Estos tests no necesitan un iPhone: miran que no vuelva a aparecer esa sintaxis en ningún
JS que sirve el cuaderno, y que la reescritura dice lo mismo que el original.
"""
import json
import os
import re
import shutil
import subprocess

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER = os.path.join(_BASE, "actividades_player.js")
SERVIDOS = ["actividades_player.js", "motor_adaptativo.js", "actividades_duelo.js",
            "actividades_curriculum.js", "video_interactivo_player.js"]

necesita_node = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


def _src(n):
    with open(os.path.join(_BASE, n), encoding="utf-8") as f:
        return f.read()


@pytest.mark.parametrize("nombre", SERVIDOS)
def test_ningun_js_servido_usa_lookbehind(nombre):
    """`(?<=` / `(?<!` sólo anda desde Safari 16.4. Si hace falta, se captura el carácter
    de la izquierda y se devuelve en el reemplazo (ver `_fraccionesEnPalabras`)."""
    m = re.search(r"\(\?<[=!]", _src(nombre))
    assert not m, "%s usa lookbehind cerca de: %r" % (nombre, _src(nombre)[m.start() - 60:m.end() + 40])


@pytest.mark.parametrize("nombre", SERVIDOS)
def test_ningun_js_servido_usa_propiedades_unicode_literales(nombre):
    """`\\p{…}` escrito en un regex literal rompe el archivo en el navegador que no conoce
    la propiedad. Armado con `new RegExp("\\\\p{…}")` dentro de un try, sí se puede."""
    m = re.search(r"(?<!\\)\\p\{", _src(nombre))
    assert not m, "%s tiene \\p{ literal cerca de: %r" % (nombre, _src(nombre)[m.start() - 60:m.end() + 40])


_ARNES = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
eval([/const _UNI = \[[\s\S]*?\];/, /const _DEC = \[[\s\S]*?\];/, /const _CEN = \[[\s\S]*?\];/,
      /function _numeroEnPalabras[\s\S]*?\n\}/, /const _ORDINAL_FRAC = \{[\s\S]*?\};/,
      /function _nombreDenominador[\s\S]*?\n\}/, /function _fraccionesEnPalabras[\s\S]*?\n\}/]
     .map((re) => src.match(re)[0]).join(";\n"));
// La versión de ANTES, con su lookbehind (node sí lo entiende): tienen que decir lo mismo.
function _viejo(txt) {
  return String(txt).replace(/(?<![\d.,])(\d{1,4})\s*\/\s*(\d{1,4})(?!\d|[.,]\d)/g,
    (m0, a, b) => {
      const n = parseInt(a, 10), d = parseInt(b, 10);
      if (!d) return m0;
      if (d === 1) return _numeroEnPalabras(n) + " sobre uno";
      const nombre = _nombreDenominador(d);
      return n === 1 ? "un " + nombre : _numeroEnPalabras(n) + " " + nombre + "s";
    });
}
const casos = JSON.parse(fs.readFileSync(%s, "utf8"));
console.log(JSON.stringify(casos.map((t) => [t, _viejo(t), _fraccionesEnPalabras(t)])));
"""


@necesita_node
def test_las_fracciones_se_dicen_igual_que_antes(tmp_path):
    fijos = ["da 3/6.", "3/4 de la torta", "1/2,5", "12/3", "x1/2", "1.5/2", "5/1",
             "entre 2/3 y 3/4, la mayor", "0/5", "3/0", "(1/2)", "1/2/3", "a 7/10.",
             "2 / 5 y 10/100", "1,2/3", "1/2 1/3 1/4"]
    import random
    rnd = random.Random(25092026)
    piezas = ["1/2", "3/4", "12/5", "7 / 8", " ", ".", ",", "a", "5", "x", "10/3.", "/", "0"]
    azar = ["".join(rnd.choice(piezas) for _ in range(rnd.randint(1, 8))) for _ in range(800)]
    casos = tmp_path / "casos.json"
    casos.write_text(json.dumps(fijos + azar), encoding="utf-8")
    r = subprocess.run(["node", "-e", _ARNES % (json.dumps(PLAYER), json.dumps(str(casos)))],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-1500:]
    distintos = [(t, a, b) for t, a, b in json.loads(r.stdout) if a != b]
    assert not distintos, "la reescritura sin lookbehind cambia lo que se dice: %r" % distintos[:5]


@necesita_node
def test_sin_propiedades_unicode_los_emojis_igual_no_van_a_la_voz():
    """En el navegador que no entiende `\\p{Extended_Pictographic}` se usa el rango de pares
    sustitutos. Se simula haciendo que `RegExp` tire con la marca `u`."""
    js = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
const def = src.match(/var _RE_EMOJI = \(function \(\) \{[\s\S]*?\}\)\(\);/)[0];
const Real = RegExp;
const out = {};
out.nuevo = eval(def + "; _RE_EMOJI");
{
  const RegExp = function (p, f) { if (/u/.test(f || "")) throw new SyntaxError("viejo"); return new Real(p, f); };
  out.viejo = eval(def + "; _RE_EMOJI");
}
const t = ["🌾 Campo", "Ciudad 🏙️", "⭐ estrella", "Sin dibujo"];
console.log(JSON.stringify({
  nuevo: t.map((x) => x.replace(out.nuevo, "").trim()),
  viejo: t.map((x) => x.replace(out.viejo, "").trim()),
  flags: out.viejo.flags }));
""" % json.dumps(PLAYER)
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-1500:]
    o = json.loads(r.stdout)
    esperado = ["Campo", "Ciudad", "estrella", "Sin dibujo"]
    assert o["nuevo"] == esperado
    assert o["viejo"] == esperado, o
    assert "u" not in o["flags"], "el respaldo no puede depender de la marca u"
