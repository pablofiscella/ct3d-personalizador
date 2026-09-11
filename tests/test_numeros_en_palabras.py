"""Números en palabras (2.º y 3.º): leer y escribir números, en los dos sentidos.

Pablo, 11-sep-2026: *"pasar un número a texto y al revés. Por ejemplo 880 y que aparezcan
palabras como ochocientos, novecientos, setenta, etc"*. La actividad enseña justo lo que un
chico escribe mal si nadie lo corrige —80080 por ochocientos ochenta—, así que lo primero es
que el cuaderno no se equivoque NUNCA al escribir un número: se corre el JS del player con
node (el archivo que se sirve, no una copia en Python) y se compara, número por número,
contra una implementación escrita aparte y contra una tabla escrita a mano.

Después, que las trampas sean trampas de verdad: ninguna ficha que sobra puede ser parte de
la respuesta, y el error central del tema tiene que estar entre las opciones.
"""
import json
import os
import re
import subprocess
import sys

import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
import actividades_web as aw  # noqa: E402

PLAYER = os.path.join(BASE, "actividades_player.js")

# Carga en node sólo lo que el juego necesita: el azar, las palabras de la voz y su lógica.
PRELUDIO = r"""
const fs = require('fs');
const src = fs.readFileSync('actividades_player.js', 'utf8');
const corte = (desde, hasta) => {
  const i = src.indexOf(desde), j = src.indexOf(hasta, i);
  if (i < 0 || j < 0) throw new Error('no está en el player: ' + desde);
  return src.slice(i, j).replace(/^const /gm, 'var ');
};
eval(corte('const rint = ', 'const espera = '));
eval(corte('const _UNI = ', 'const _SIGNOS = '));
eval(corte('function _npPalabras', 'GAMES.numeros_palabras = {'));
"""


def _node(js):
    r = subprocess.run(["node", "-e", PRELUDIO + js], cwd=BASE,
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


# ── la referencia, escrita aparte ───────────────────────────────────────────────
UNI = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
       "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete",
       "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidós", "veintitrés",
       "veinticuatro", "veinticinco", "veintiséis", "veintisiete", "veintiocho", "veintinueve"]
DEC = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta",
       8: "ochenta", 9: "noventa"}
CEN = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos",
       6: "seiscientos", 7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def en_palabras(n):
    """Escrita aparte y a propósito distinta del player (por divmod, de arriba abajo): si
    las dos coinciden en los 9.999 números, no es porque una copió a la otra."""
    miles, resto = divmod(n, 1000)
    partes = []
    if miles == 1:
        partes.append("mil")
    elif miles:
        partes += [UNI[miles], "mil"]
    cientos, dos = divmod(resto, 100)
    if resto == 100:
        partes.append("cien")
    elif cientos:
        partes.append(CEN[cientos])
    if 0 < dos < 30:
        partes.append(UNI[dos])
    elif dos:
        decenas, unidades = divmod(dos, 10)
        partes.append(DEC[decenas])
        if unidades:
            partes += ["y", UNI[unidades]]
    return " ".join(partes)


# Los que un adulto revisaría a ojo: irregulares, cien/ciento, el cero, el mil.
A_MANO = {
    100: "cien", 101: "ciento uno", 116: "ciento dieciséis", 121: "ciento veintiuno",
    500: "quinientos", 555: "quinientos cincuenta y cinco", 700: "setecientos",
    777: "setecientos setenta y siete", 805: "ochocientos cinco", 880: "ochocientos ochenta",
    888: "ochocientos ochenta y ocho", 900: "novecientos", 999: "novecientos noventa y nueve",
    1000: "mil", 1001: "mil uno", 1016: "mil dieciséis", 1100: "mil cien",
    1200: "mil doscientos", 2022: "dos mil veintidós", 3005: "tres mil cinco",
    3450: "tres mil cuatrocientos cincuenta", 6060: "seis mil sesenta",
    7777: "siete mil setecientos setenta y siete", 9999: "nueve mil novecientos noventa y nueve",
}


def test_la_referencia_coincide_con_la_tabla_escrita_a_mano():
    """Si la referencia está mal, el test de los 9.999 no prueba nada."""
    for n, w in A_MANO.items():
        assert en_palabras(n) == w, "la referencia escribe mal el %d" % n


def test_el_player_escribe_bien_los_que_se_revisan_a_ojo():
    ns = sorted(A_MANO)
    got = _node("console.log(JSON.stringify(%s.map((n) => _npPalabras(n).join(' '))));"
                % json.dumps(ns))
    for n, w in zip(ns, got):
        assert w == A_MANO[n], "%d se escribe «%s», no «%s»" % (n, A_MANO[n], w)


def test_el_player_escribe_bien_del_1_al_9999():
    got = _node("const o = []; for (let n = 1; n <= 9999; n++) o.push(_npPalabras(n).join(' '));"
                " console.log(JSON.stringify(o));")
    malos = [(n, w) for n, w in enumerate(got, start=1) if w != en_palabras(n)]
    assert not malos, "el player escribe mal %d números, por ejemplo %s" % (len(malos), malos[:5])


# ── las tiradas ─────────────────────────────────────────────────────────────────
def _tiradas(cifras, bonus, n=400):
    return _node("""
      const out = [];
      for (let i = 0; i < %d; i++) {
        const n = _npSortear(%d, %d);
        out.push({n: n, palabras: _npPalabras(n), trampas: _npTrampas(n, 3),
                  opciones: _npOpciones(n)});
      }
      console.log(JSON.stringify(out));
    """ % (n, cifras, bonus))


GRADOS = [(3, 0), (3, 1), (4, 0), (4, 1)]
PALABRAS = set(UNI[1:]) | set(DEC.values()) | set(CEN.values()) | {"cien", "mil", "y"}
DICHAS_COMO_SUENAN = {"cincocientos", "sietecientos", "nuevecientos",
                      "seisenta", "sietenta", "nueventa"}


@pytest.mark.parametrize("cifras,bonus", GRADOS)
def test_ninguna_ficha_que_sobra_es_parte_de_la_respuesta(cifras, bonus):
    """Con dos fichas iguales —una buena y otra marcada como error—, la corrección miente."""
    for t in _tiradas(cifras, bonus):
        ws = [x["w"] for x in t["trampas"]]
        assert len(ws) >= 2, "el %d trae %d fichas que sobran" % (t["n"], len(ws))
        assert len(set(ws)) == len(ws), "fichas repetidas en el %d: %s" % (t["n"], ws)
        assert not set(ws) & set(t["palabras"]), (
            "en el %d sobra una ficha que es parte de la respuesta: %s" % (t["n"], ws))


@pytest.mark.parametrize("cifras,bonus", GRADOS)
def test_toda_ficha_que_sobra_es_un_error_que_existe(cifras, bonus):
    """Una palabra inventada que no se parece a nada no enseña: se descarta sin pensar.
    Cada ficha que sobra es una palabra de número, una dicha como suena («sietecientos») o
    una de las del mil («un», «tresmil»); y su porqué termina con la respuesta."""
    for t in _tiradas(cifras, bonus):
        frase = " ".join(t["palabras"])
        for x in t["trampas"]:
            w = x["w"]
            assert (w in PALABRAS or w in DICHAS_COMO_SUENAN or w == "un"
                    or re.fullmatch(r"(dos|tres|cuatro|cinco|seis|siete|ocho|nueve)mil", w)), (
                "«%s» (en el %d) no es ningún error conocido" % (w, t["n"]))
            assert x["m"].endswith(": " + frase + "."), (
                "el porqué de «%s» no dice la respuesta al final: %s" % (w, x["m"]))


def test_escribir_como_se_dice_esta_entre_las_opciones():
    """El error del tema (Lerner y Sadovsky): la numeración hablada suma pedazos y el chico
    los escribe uno atrás del otro."""
    casos = {880: "80080", 805: "8005", 1200: "1000200", 3450: "3000450", 3005: "30005"}
    got = _node("console.log(JSON.stringify(%s.map((n) => _npDistractores(n).map((d) => d.v))));"
                % json.dumps(list(casos)))
    for (n, error), vs in zip(casos.items(), got):
        assert error in vs, "al %d le falta el error de escribir como se dice (%s): %s" % (
            n, error, vs)


def test_el_cero_corrido_y_el_cero_que_falta():
    casos = {805: {"850", "85"}, 880: {"808"}, 3040: {"3400", "3004", "340"}}
    got = _node("console.log(JSON.stringify(%s.map((n) => _npDistractores(n).map((d) => d.v))));"
                % json.dumps(list(casos)))
    for (n, esperados), vs in zip(casos.items(), got):
        assert esperados <= set(vs), "al %d le faltan %s: %s" % (n, esperados - set(vs), vs)


@pytest.mark.parametrize("cifras,bonus", GRADOS)
def test_las_opciones_de_que_numero_es(cifras, bonus):
    """Tres distintas, la correcta entre ellas, y nunca las dos incorrectas más largas que
    la correcta: si no, se gana eligiendo la más corta, sin entender nada."""
    validas = [t for t in _tiradas(cifras, bonus) if t["opciones"]]
    assert len(validas) >= 150, "sólo %d de 400 números sirven para «¿qué número es?»" % len(
        validas)
    for t in validas:
        o = t["opciones"]
        vs = [o["ok"]] + [d["v"] for d in o["d"]]
        assert o["ok"] == str(t["n"])
        assert len(set(vs)) == 3, "opciones repetidas para el %d: %s" % (t["n"], vs)
        assert any(len(d["v"]) <= len(o["ok"]) for d in o["d"]), (
            "para el %d la correcta es la más corta: %s" % (t["n"], vs))
        assert all(d["m"].endswith(" es %s." % o["ok"]) for d in o["d"]), (
            "algún porqué no dice cuál es el número: %s" % o["d"])


@pytest.mark.parametrize("cifras,lo,hi", [(3, 100, 1000), (4, 100, 9999)])
def test_el_sorteo_respeta_el_rango_y_no_se_repite(cifras, lo, hi):
    for bonus in (0, 1):
        ns = [t["n"] for t in _tiradas(cifras, bonus)]
        fuera = [n for n in ns if not lo <= n <= hi]
        assert not fuera, "números fuera del rango del grado: %s" % fuera[:5]
        assert len(set(ns)) >= 100, "sólo %d números distintos en 400: se memoriza" % len(set(ns))
        if cifras == 4:
            assert sum(n >= 1000 for n in ns) > 250, (
                "3.º tiene que trabajar sobre todo con cuatro cifras")


def test_el_escalon_ganado_trae_mas_ceros_en_el_medio():
    """`ctx.bonusDominio` es la palanca de dificultad (ver test_dificultad_por_dominio): al
    dominar tiene que aparecer más el cero que no se dice, que es lo que más cuesta."""
    p = _node("""
      const prop = (b) => { let k = 0; for (let i = 0; i < 4000; i++)
        if (/0[1-9]/.test(String(_npSortear(4, b)))) k++; return k / 4000; };
      console.log(JSON.stringify([prop(0), prop(1)]));
    """)
    assert p[1] > p[0] + 0.08, "con el escalón ganado no aparecen más ceros en el medio: %s" % p


def test_el_porque_de_una_ficha_que_va_pero_todavia_no():
    got = _node("""console.log(JSON.stringify([
      _npPorQue(888, {w: 'ocho', trampa: null}, 'y'),
      _npPorQue(880, {w: 'ochenta', trampa: null}, 'ochocientos'),
      _npPorQue(838, {w: 'y', trampa: null}, 'treinta')]));""")
    assert "va una «y»" in got[0], got[0]
    assert "orden" in got[1], got[1]
    assert "solamente entre las decenas y las unidades" in got[2], got[2]


# ── el juego en el cuaderno ─────────────────────────────────────────────────────
def test_la_actividad_llega_al_menu_de_segundo_y_de_tercero():
    for edad, id_, cifras in (("7", "numeros_palabras_2", 3), ("8", "numeros_palabras_3", 4)):
        menu = {m["id"]: m for m in aw._menu_curricular(edad)}
        assert id_ in menu, "«Números en palabras» no está en el menú de %s años" % edad
        assert (menu[id_].get("cfg") or {}).get("cifras") == cifras, (
            "el menú de %s años no le pasa su rango al juego" % edad)
    src = open(PLAYER, encoding="utf-8").read()
    assert re.search(r"GAMES\.numeros_palabras\s*=", src), "el juego no existe en el player"


def test_las_opciones_no_se_leen_en_voz_alta():
    """En 1.º-3.º el player lee las opciones después de la consigna (`leerOpciones`). Acá
    eso regala la respuesta: leer 80080 —«ochenta mil ochenta»— dice de oído cuál no es.
    El juego lo pide con `data-no-leer` y el lector lo tiene que respetar."""
    s = open(PLAYER, encoding="utf-8").read()
    i = s.find("function _opcionesEnPantalla")
    assert "[data-no-leer]" in s[i:s.find("\n}", i)], "el lector de opciones no respeta data-no-leer"
    j = s.find("GAMES.numeros_palabras = {")
    juego = s[j:s.find("\n};", j)]
    assert juego.count('setAttribute("data-no-leer"') == 2, (
        "algún tramo del juego deja que se lean sus opciones")


def test_hay_mini_leccion_en_los_dos_grados():
    s = open(PLAYER, encoding="utf-8").read()
    i = s.find("const COMO_ES = {")
    como_es = s[i:s.find("\nconst FRASES_BIEN", i)]
    for id_ in ("numeros_palabras_2", "numeros_palabras_3"):
        assert re.search(r"\n  %s: \{ t:" % id_, como_es), "falta la mini-lección de %s" % id_
