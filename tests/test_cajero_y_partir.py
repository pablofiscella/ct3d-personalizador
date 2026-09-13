"""«El cajero» y «Partí el número» (2.º), las dos de lo visto en mudi.com.ar.

Pablo, 12-sep-2026: *"quiero que construyas algunas"*. Las dos enseñan que la cifra dice
CUÁNTOS de su lugar hay: con billetes (el cajero) y con el número partido (300 + 40 + 7).

Lo que tiene respuesta correcta se VERIFICA por código, recorriendo los 900 números de tres
cifras y no un par de ejemplos. Las funciones se corren con node, recortadas del player que se
sirve: si alguien las cambia, se prueba lo que de verdad le llega al chico.
"""
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
PLAYER = os.path.join(BASE, "actividades_player.js")

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


def _fuente():
    with open(PLAYER, encoding="utf-8") as f:
        return f.read()


def _node(expr):
    """Evalúa `expr` con las funciones del player cargadas, y devuelve el JSON que imprime."""
    js = r"""
      const fs = require('fs');
      const src = fs.readFileSync('actividades_player.js', 'utf8');
      const tramo = (desde, hasta) => {
        const i = src.indexOf(desde), j = src.indexOf(hasta, i);
        if (i < 0 || j < 0) throw new Error('no encontré ' + desde);
        return src.slice(i, j);
      };
      global.rint = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
      eval(tramo('function _npPalabras', 'GAMES.numeros_palabras = {'));
      eval(tramo('function _cduPartes', 'GAMES.cajero_cdu = {'));
      eval(tramo('function _descTrampas', 'GAMES.descomponer = {'));
      console.log(JSON.stringify((() => { %s })()));
    """ % expr
    r = subprocess.run(["node", "-e", js], cwd=BASE, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout.strip())


# ── partir en centenas, decenas y unidades ───────────────────────────────────────
def test_las_partes_son_centenas_decenas_y_unidades_y_el_cero_no_es_un_pedazo():
    r = _node("return [347, 407, 340, 500, 105, 999].map(_cduPartes);")
    assert r == [[300, 40, 7], [400, 7], [300, 40], [500], [100, 5], [900, 90, 9]]


def test_juntar_las_partes_da_el_numero_en_los_900():
    """La propiedad que el juego enseña, para todos los números de tres cifras."""
    malos = _node("""
      const out = [];
      for (let n = 100; n <= 999; n++) {
        const s = _cduPartes(n).reduce((a, b) => a + b, 0);
        if (s !== n) out.push(n);
      }
      return out;""")
    assert not malos, "las partes no suman el número: %s" % malos[:10]


def test_el_sorteo_nunca_da_un_numero_que_no_se_pueda_armar():
    """Con billetes de 100, 10 y 1 y hasta 9 por lugar, el 1000 no se arma: si saliera, el chico
    quedaría trabado en una ronda imposible."""
    r = _node("""
      let fuera = 0, conCero = 0;
      for (let i = 0; i < 3000; i++) {
        const n = _cduSortear(i % 2);
        if (n < 100 || n > 999) fuera++;
        if (Math.floor((n % 100) / 10) === 0 && n % 10 !== 0) conCero++;
      }
      return {fuera, conCero};""")
    assert r["fuera"] == 0, "el sorteo dio %d números imposibles" % r["fuera"]
    assert r["conCero"] > 200, "casi no salen ceros en el medio, que es lo que más cuesta"


# ── el cajero ────────────────────────────────────────────────────────────────────
def test_el_cajero_reconoce_las_cifras_dadas_vuelta():
    m = _node("return _cajPorQue(347, {100: 7, 10: 4, 1: 3});")
    assert m.startswith("Pusiste las cifras dadas vuelta"), m
    assert "3 billetes de $100" in m, m


def test_el_cajero_reconoce_el_cero_del_medio():
    m = _node("return _cajPorQue(407, {100: 4, 10: 7, 1: 0});")
    assert "0 en las decenas" in m and "ningún billete de $10" in m, m


def test_el_cajero_nombra_el_lugar_que_no_coincide():
    m = _node("return _cajPorQue(347, {100: 3, 10: 3, 1: 7});")
    assert m.startswith("Mirá las decenas"), m
    assert "tiene 4" in m and "3 billetes de $10" in m, m


def test_el_cajero_sabe_explicar_CUALQUIER_error_posible():
    """Cada combinación de billetes que no da el número tiene que devolver una explicación, sin
    reventar: si una sola tira error, el chico se queda sin respuesta en la pantalla."""
    r = _node("""
      let sinTexto = 0, sinRegla = 0, total = 0;
      for (const n of [347, 407, 340, 105, 999, 100, 610]) {
        for (let c = 0; c <= 9; c++) for (let d = 0; d <= 9; d++) for (let u = 0; u <= 9; u++) {
          if (c * 100 + d * 10 + u === n) continue;
          total++;
          const m = _cajPorQue(n, {100: c, 10: d, 1: u});
          if (!m) sinTexto++;
          else if (m.indexOf(': ') <= 0) sinRegla++;
        }
      }
      return {sinTexto, sinRegla, total};""")
    assert r["total"] > 6000
    assert r["sinTexto"] == 0, "hay errores sin explicación"
    assert r["sinRegla"] == 0, "hay explicaciones sin «regla: detalle» (no se muestran en dos tiempos)"


def test_el_juego_del_cajero_no_muestra_el_total_y_tiene_tope_de_9():
    """Las dos decisiones que hacen que se aprenda el lugar y no a sumar de a uno."""
    s = _fuente()
    i = s.index("GAMES.cajero_cdu = {")
    cuerpo = s[i:s.index("function _descTrampas", i)]
    assert "cuenta[v] >= 9" in cuerpo, "se perdió el tope de 9 billetes por lugar"
    assert "total" not in cuerpo.split('listo.addEventListener')[0], (
        "el total que se va juntando aparece en pantalla antes de «Listo»")


# ── partí el número ──────────────────────────────────────────────────────────────
def test_ninguna_ficha_que_sobra_es_un_pedazo_de_la_respuesta():
    """Con dos fichas iguales, una buena y otra marcada como error, la corrección mentiría."""
    r = _node("""
      const out = [];
      for (let n = 100; n <= 999; n++) {
        const partes = _cduPartes(n);
        for (const t of _descTrampas(n)) {
          if (partes.includes(t.v)) out.push([n, t.v]);
          if (t.m.indexOf(': ') <= 0) out.push([n, 'sin regla']);
        }
      }
      return out;""")
    assert not r, "fichas trampa inválidas: %s" % r[:10]


def test_el_cero_que_no_suma_aparece_justo_cuando_hay_un_cero_en_el_medio():
    r = _node("""
      const tiene = (n) => _descTrampas(n).some((t) => t.v === 0);
      return [tiene(407), tiene(347), tiene(340), tiene(500)];""")
    assert r == [True, False, False, False]


def test_juntar_las_partes_trae_el_error_de_pegarlas():
    """300 + 40 + 7 → 300407 es el error clásico, el mismo de «ochocientos ochenta» → 80080."""
    r = _node("return _descOpciones(347).map((o) => o.v);")
    assert 300407 in r and 743 in r and 347 not in r


def test_perder_el_cero_es_una_opcion_cuando_hay_cero_en_el_medio():
    r = _node("return _descOpciones(407).map((o) => o.v);")
    assert 47 in r, r


def test_ninguna_opcion_mala_es_la_respuesta():
    r = _node("""
      const out = [];
      for (let n = 100; n <= 999; n++)
        for (const o of _descOpciones(n)) {
          if (o.v === n) out.push(n);
          if (o.m.indexOf(': ') <= 0) out.push('sin regla ' + n);
        }
      return out;""")
    assert not r, r[:10]


def test_hay_numeros_de_sobra_para_jugar_las_dos_mitades():
    """El juego sortea hasta encontrar un número con al menos 2 fichas trampa (o 2 opciones
    malas). Si quedaran pocos, se repetirían en la partida y mediría memoria."""
    r = _node("""
      let partes = 0, numero = 0;
      for (let n = 100; n <= 999; n++) {
        if (_cduPartes(n).length < 2) continue;
        if (_descTrampas(n).length >= 2) partes++;
        if (_descOpciones(n).length >= 2) numero++;
      }
      return {partes, numero};""")
    assert r["partes"] > 500, r
    assert r["numero"] > 500, r


# ── enganchadas al catálogo y al Diseño Curricular ───────────────────────────────
def test_estan_en_el_catalogo_y_el_juego_existe():
    import actividades_curriculum as ac
    s = _fuente()
    por_id = {a["id"]: a for a in ac.CATALOGO}
    for aid, juego in (("cajero_cdu_2", "cajero_cdu"), ("descomponer_2", "descomponer")):
        a = por_id.get(aid)
        assert a, "%s no está en el catálogo" % aid
        assert a["grado"] == 2 and a["mecanica"] == "reusa" and a["juego"] == juego
        assert ("GAMES.%s = {" % juego) in s, "el juego %s no existe en el player" % juego


def test_cubren_el_tema_de_valor_posicional_de_segundo():
    import actividades_cobertura as c
    m2 = next(t for t in c.temas(2) if t["cod"] == "M2")
    cubre = m2["cubre"] if isinstance(m2["cubre"], list) else [m2["cubre"]]
    assert "cajero_cdu_2" in cubre and "descomponer_2" in cubre, cubre


def test_dice_centenas_decenas_y_unidades_como_en_el_pizarron():
    """Nada de «cienes» ni «dieces»: los nombres del programa (decisión del 31-jul-2026)."""
    s = _fuente()
    i = s.index("/* ── EL CAJERO Y PARTÍ EL NÚMERO")
    bloque = s[i:s.index("/* ── ESTADOS DE LA MATERIA", i)]
    assert not re.search(r"\b(cienes|dieces|unos)\b", bloque), "vocabulario que no es del pizarrón"
