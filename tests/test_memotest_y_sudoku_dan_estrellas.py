# -*- coding: utf-8 -*-
"""El memotest y el sudoku tienen que poder dar 3 estrellas. Si no, no hay diploma.

POR QUÉ EXISTE (25-sep-2026, auditoría, hallazgo PRO-13)
──────────────────────────────────────────────────────────
`todoCompleto()` pide 3★ en TODAS las tarjetas del menú para dar «🏆 Ver mi diploma», y el
memotest está en los siete grados. Pero el memotest:

- llamaba a `ctx.casi()` en cada pareja errada y NUNCA a `ctx.bien()`, y
- terminaba con `ctx.win()` sin estrellas.

`win()` sin estrellas calcula la precisión de PRIMER intento, y con cero `bien` esa precisión
es 0/n → 1★. Siempre. El chico que armaba todas las parejas se llevaba una estrella, y el
diploma —lo único que se le puede mostrar al padre— era imposible en los siete grados. La
telemetría lo confirmaba: 0 de 32 primeros intentos «bien» en todos los cuadernos, que el
informe leía como «contenido difícil». Era una señal falsa.

LA REGLA NUEVA DEL MEMOTEST: errar una pareja es parte del juego —las cartas empiezan boca
abajo y hay que darlas vuelta para verlas—, así que no se mide por «acertó al primer
intento» sino por cuántas parejas erró RESPECTO de cuántas había:

    errores ≤ parejas      → 3★   (juega recordando: una memoria perfecta erra ~0,6 por pareja)
    errores ≤ 2 × parejas  → 2★
    más                    → 1★   (dar vuelta al azar: con 6 parejas llega a 3★ el 2 % de las veces)

Los números salen de simular 4.000 partidas con memoria perfecta, con olvido y al azar; están
en el comentario de `_estrellasMemotest`.

EL SUDOKU tenía el mismo agujero con otra forma: nunca anotaba un acierto, así que un solo
choque en toda la partida lo dejaba en 1★ (0 aciertos sobre 1 primer intento), y sólo el que
no chocaba NUNCA sacaba 3★ — nunca 2★. Ahí la regla general del motor (precisión de primer
intento ≥ 90 % → 3★, ≥ 70 % → 2★) SÍ tiene sentido: cada casillero se deduce, no se adivina.
Lo que faltaba era anotar los aciertos. Se anotan en silencio (`ctx.anotar`), sin cartel de
«¡Muy bien!»: el sudoku acepta cualquier ficha que no choque aunque no sea la de la solución,
y festejar sólo las correctas le soplaría al chico cuál es cuál.

Los juegos se EJECUTAN con node (con un DOM de juguete), no se leen como texto.
"""
import json
import os
import shutil
import subprocess
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

PLAYER = os.path.join(_BASE, "actividades_player.js")

sin_node = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


def _src():
    return open(PLAYER, encoding="utf-8").read()


def _juego(nombre):
    s = _src()
    i = s.index("GAMES.%s = {" % nombre)
    return s[i:s.index("\n};", i) + 3]


def _funcion(nombre):
    """El texto de una función de nivel superior del player, o "" si no está. Que falte no
    rompe el arnés: así, contra el player VIEJO, los tests fallan por lo que el juego HACE
    (1★) y no por un `substring not found`."""
    s = _src()
    i = s.find("function %s(" % nombre)
    return s[i:s.index("\n}", i) + 2] if i >= 0 else ""


# La cuenta que tenía `win()` adentro antes de sacarla a `_estrellasDeLaPartida`: se usa
# sólo si el player no trae la función (o sea, corriendo contra el código viejo).
_REGLA_VIEJA = """
function _estrellasDeLaPartida(ok, tot, fallos) {
  if (tot > 0) { const acc = ok / tot; return acc >= 0.9 ? 3 : (acc >= 0.7 ? 2 : 1); }
  return fallos === 0 ? 3 : (fallos <= 2 ? 2 : 1);
}
"""


# El DOM de juguete y un ctx que anota como el de verdad: el primer resultado de cada ronda
# es el «primer intento», `ronda()` lo rearma. Es la misma cuenta que `registrar()` en
# `Shell.ctx`; las estrellas las calcula la función REAL del player.
_ARNES = r"""
const mk = (tag, cls, html) => {
  const n = { tag, children: [], style: {}, innerHTML: html || "", _l: {},
    classList: { s: new Set((cls || "").split(" ").filter(Boolean)),
      add(c) { this.s.add(c); }, remove(...cs) { cs.forEach((c) => this.s.delete(c)); },
      contains(c) { return this.s.has(c); } },
    appendChild(c) { this.children.push(c); return c; },
    addEventListener(t, f) { this._l[t] = f; },
    click() { return this._l.click ? this._l.click() : undefined; },
    getBoundingClientRect() { return { top: 0 }; } };
  Object.defineProperty(n, "innerHTML", { get() { return this._h; },
    set(v) { this._h = v; if (v === "") this.children = []; } });
  n.innerHTML = html || "";
  return n;
};
const el = mk;
const GAMES = {};
const requestAnimationFrame = () => {};
const innerHeight = 800;
const espera = async () => {};
const Sfx = new Proxy({}, { get: () => () => {} });
const sample = (a, n) => a.slice(0, n);
const shuffle = (a) => a;          // mazo en orden: la carta i hace pareja con la i+pares
const rint = (a) => a;
let P = ["a.png", "b.png", "c.png", "d.png", "e.png", "f.png", "g.png", "h.png"];
let D = {};

function hacerCtx(cfg) {
  const log = [];
  let resp = false, pOk = 0, pTot = 0, fallos = 0;
  const anotar = (ok) => { if (!resp) { pTot++; if (ok) pOk++; } resp = true; };
  const ctx = {
    cfg: cfg || {}, nivelDif: 0, bonusDominio: 0, juego: mk("div"), log,
    consigna() {}, rondas() {},
    ronda(i) { resp = false; log.push("ronda" + i); },
    bien() { anotar(true); log.push("bien"); },
    anotar(ok) { anotar(ok); log.push("anotar:" + ok); },
    casi() { anotar(false); fallos++; log.push("casi"); },
    win(e) {
      ctx.estrellas = e !== undefined ? e : _estrellasDeLaPartida(pOk, pTot, fallos);
      ctx.explicita = e !== undefined;
      log.push("win");
    },
  };
  return ctx;
}
"""


def _node(cuerpo):
    js = "\n".join([_ARNES, _funcion("_estrellasDeLaPartida") or _REGLA_VIEJA,
                    _funcion("_estrellasMemotest"), _juego("memotest"), _juego("sudoku"),
                    "(async () => {", cuerpo, "})().catch((e) => { console.error(e); process.exit(1); });"])
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-1500:]
    return json.loads(r.stdout.strip().splitlines()[-1])


# ── memotest ─────────────────────────────────────────────────────────────────────

# Jugar el memotest con `pares` parejas errando `errores` veces. Con el mazo en orden la
# carta i hace pareja con la i+pares; se yerra abriendo la 0 con la 1.
_JUGAR_MEMO = r"""
async function jugarMemo(pares, errores) {
  const ctx = hacerCtx({ pares });
  GAMES.memotest.crear(ctx);
  const grid = ctx.juego.children[0].children[0];
  const c = grid.children;
  for (let k = 0; k < errores; k++) { await c[0].click(); await c[1].click(); }
  for (let i = 0; i < pares; i++) { await c[i].click(); await c[i + pares].click(); }
  return { e: ctx.estrellas, explicita: ctx.explicita, log: ctx.log };
}
"""


@sin_node
@pytest.mark.parametrize("pares,errores,esperadas", [
    (6, 0, 3), (6, 4, 3), (6, 6, 3),          # jugando con memoria: 3★
    (6, 7, 2), (6, 12, 2),                    # le costó: 2★
    (6, 13, 1), (6, 30, 1),                   # dar vuelta al azar: 1★
    (3, 3, 3), (3, 4, 2), (8, 8, 3), (8, 17, 1),
])
def test_el_memotest_da_estrellas_por_errores_respecto_de_las_parejas(pares, errores, esperadas):
    r = _node(_JUGAR_MEMO + "console.log(JSON.stringify(await jugarMemo(%d, %d)));"
              % (pares, errores))
    assert r["explicita"], "el memotest volvió a terminar con ctx.win() sin estrellas"
    assert r["e"] == esperadas, (
        "memotest de %d parejas con %d errores dio %s★ (se esperaban %d)"
        % (pares, errores, r["e"], esperadas))


@sin_node
def test_armar_el_memotest_jugando_bien_llega_a_tres_estrellas():
    """EL bug: con el código viejo esto daba 1★ en cualquier partida con un error, que es
    cualquier partida real, y el diploma quedaba imposible."""
    r = _node(_JUGAR_MEMO + "console.log(JSON.stringify(await jugarMemo(6, 3)));")
    assert r["e"] == 3


@sin_node
def test_el_memotest_anota_cada_pareja_como_acierto_en_su_ronda():
    """La telemetría tenía 0 aciertos porque nunca se llamaba a `bien`. Tiene que llamarse
    ANTES de pasar de ronda: si no, el acierto se anota en la ronda de la pareja siguiente
    y se come su primer intento."""
    r = _node(_JUGAR_MEMO + "console.log(JSON.stringify(await jugarMemo(3, 1)));")
    log = r["log"]
    assert log.count("bien") == 3, log
    assert log.count("casi") == 1, log
    for i in (1, 2, 3):
        j = log.index("ronda%d" % i)
        assert log[j - 1] == "bien", "la pareja %d no se anotó antes de pasar de ronda: %s" % (i, log)


@sin_node
def test_las_estrellas_del_memotest_no_bajan_con_mas_parejas():
    """La dificultad adaptativa SUMA parejas cuando el chico domina (`+ ctx.nivelDif`). Si la
    regla no escalara con las parejas, subir de nivel lo castigaría."""
    got = _node("console.log(JSON.stringify([3,6,8,10,12].map((n) => _estrellasMemotest(n, n))));")
    assert got == [3, 3, 3, 3, 3], got


# ── sudoku ───────────────────────────────────────────────────────────────────────

_SOL = [[0, 1, 2, 3], [2, 3, 0, 1], [1, 0, 3, 2], [3, 2, 1, 0]]
# 10 casilleros vacíos. (0,0) admite un 1 que no choca con nada y no es el de la solución.
_PUZ = [[None, None, 2, 3], [2, 3, None, None], [None, None, None, 2], [3, None, None, None]]

_JUGAR_SUDOKU = r"""
D.sudokus = [{ sol: %s, puz: %s }];
async function jugarSudoku(plan) {
  const ctx = hacerCtx({});
  GAMES.sudoku.crear(ctx);
  const tab = ctx.juego.children[1], grid = tab.children[0], pick = ctx.juego.children[2];
  const celda = (r, c) => grid.children[r * 4 + c];
  const sol = D.sudokus[0].sol, puz = D.sudokus[0].puz;
  for (const [r, c, v, levantar] of plan) {
    await celda(r, c).click();
    await pick.children[v].click();
    if (levantar) await celda(r, c).click();           // tocar una puesta la levanta
    // un choque deja el casillero elegido: el chico pone ahí la que va, y así cada choque
    // cae en SU ronda (dos choques en la misma ronda son un solo primer intento)
    else if (v !== sol[r][c]) await pick.children[sol[r][c]].click();
  }
  for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) {
    if (puz[r][c] !== null) continue;
    if (plan.some(([pr, pc, pv, lev]) => pr === r && pc === c && !lev)) continue;
    await celda(r, c).click(); await pick.children[sol[r][c]].click();
  }
  return { e: ctx.estrellas, log: ctx.log };
}
""" % (json.dumps(_SOL), json.dumps(_PUZ))


def _sudoku(plan):
    return _node(_JUGAR_SUDOKU + "console.log(JSON.stringify(await jugarSudoku(%s)));"
                 % json.dumps(plan))


@sin_node
def test_el_sudoku_sin_errores_da_tres_estrellas():
    r = _sudoku([])
    assert r["e"] == 3, r
    assert r["log"].count("anotar:true") == 10, r["log"]


@sin_node
def test_un_choque_en_todo_el_sudoku_no_lo_tira_a_una_estrella():
    """EL bug del sudoku: un solo choque en 10 casilleros daba 1★ (0 aciertos anotados sobre
    1 primer intento). Con los aciertos anotados es 9 de 10 → 3★, como en el resto del motor."""
    r = _sudoku([[0, 0, 2, False]])            # el 2 ya está en la fila: choca
    assert r["log"].count("casi") == 1, r["log"]
    assert r["e"] == 3, r


@sin_node
def test_el_sudoku_ahora_puede_dar_dos_estrellas():
    """Antes era 3★ o 1★, sin término medio. Tres choques en 10 → 7 de 10 → 2★."""
    r = _sudoku([[0, 0, 2, False], [0, 1, 3, False], [1, 2, 2, False]])
    assert r["e"] == 2, r


@sin_node
def test_la_ficha_que_no_choca_pero_esta_mal_cuenta_como_error_sin_decirlo():
    """El sudoku acepta un 1 en (0,0): no choca con nada. Pero no es la solución, y hay que
    levantarla para terminar. Para las estrellas cuenta como error; en pantalla no cambia
    nada (no hay `casi`, no hay cartel), porque avisarlo le soplaría la respuesta."""
    r = _sudoku([[0, 0, 1, True]])
    assert "anotar:false" in r["log"], r["log"]
    assert r["log"].count("casi") == 0, r["log"]
    assert "bien" not in r["log"], "el sudoku festeja las fichas: le sopla cuál es la correcta"


def test_el_ctx_anota_sin_festejar():
    """`anotar` es `registrar` pelado: sin sonido, sin cartel, sin marcar lo que tocó."""
    s = _src()
    i = s.index("  ctx(item) {")
    ctx = s[i:s.index("\n  },\n", s.index("win(estrellas)", i))]
    j = ctx.index("anotar(ok)")
    linea = ctx[j:ctx.index("\n", j)]
    assert "registrar(" in linea, linea
    for ruido in ("Sfx", "toast", "marcarLoQueToco"):
        assert ruido not in linea, "ctx.anotar hace ruido (%s): %s" % (ruido, linea)


def test_win_sigue_usando_la_misma_regla_para_los_demas_juegos():
    """Factorizar la cuenta no puede cambiarla: los otros 300 juegos puntúan igual que antes."""
    s = _src()
    i = s.index("win(estrellas) {")
    cuerpo = s[i:i + 2500]
    assert "_estrellasDeLaPartida(self.primerOk, self.primerTotal, self.fallos)" in cuerpo


@sin_node
def test_la_regla_general_no_cambio():
    got = _node("console.log(JSON.stringify(["
                "_estrellasDeLaPartida(9, 10, 1), _estrellasDeLaPartida(7, 10, 3),"
                "_estrellasDeLaPartida(6, 10, 4), _estrellasDeLaPartida(0, 0, 0),"
                "_estrellasDeLaPartida(0, 0, 2), _estrellasDeLaPartida(0, 0, 3)]));")
    assert got == [3, 2, 1, 3, 2, 1], got
