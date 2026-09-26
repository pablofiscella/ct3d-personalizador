# -*- coding: utf-8 -*-
"""Los primeros minutos del chico y el motivo para volver (auditoría de Kydo, 25-sep-2026).

POR QUÉ EXISTE. De los 8 cuadernos reales ninguno se jugó en dos días distintos; la
nivelación cortó sesiones en 2 de 4 casos (arrancaba por lo difícil, 4-5 juegos seguidos,
sin ← y terminando en un menú de 65 a 105 tarjetas); lo jugado en la sala de prueba se perdía
al guardarla; y la sala ofrecía guardar por reloj, en la mitad de una partida. Ids:
PRO-04, MOT-10, PRO-05, EMB-02, EXP-11, PRO-09, PRO-03, EXP-18, PRO-10.

Lo que cuidan estos tests (todos corren el JS del archivo que se sirve, recortado con node):
  1. la nivelación: corta, el primero fácil, salteable en cada paso y sin bloquear el menú;
  2. entrar directo a jugar lo que conviene, no a un menú de 70 tarjetas;
  3. la sala: el cuaderno avisa cuando el chico TERMINA un juego, y sólo desde la sala;
  4. lo jugado en la sala pasa al cuaderno nuevo desde el navegador, sin traer lo de otro;
  5. la misión de hoy, el «1 de 2 días» y la racha desde el día 1;
  6. el link propio del chico: el motor devuelve el mismo permiso, nunca uno nuevo;
  7. el duelo, a la vista donde el chico festeja.
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
HTML = os.path.join(BASE, "actividades_player.html")

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


def _fuente(path=PLAYER):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _node(js):
    r = subprocess.run(["node", "-e", js], cwd=BASE, capture_output=True, text=True, timeout=90)
    assert r.returncode == 0, r.stderr[-3000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


# Recorta una función de nivel superior del player (desde `function nombre(` hasta la primera
# llave que cierra en la columna 0). Así se prueba el código que se sirve, no una copia.
_RECORTAR = r"""
const fs = require("fs");
const SRC = fs.readFileSync("actividades_player.js", "utf8");
function recortar(nombre) {
  const re = new RegExp("\\n(async )?function " + nombre + "\\(");
  const m = re.exec(SRC);
  if (!m) throw new Error("no encontré la función " + nombre);
  const finLinea = SRC.indexOf("\n", m.index + 1);
  const linea = SRC.slice(m.index + 1, finLinea);
  if (/\}\s*$/.test(linea)) return linea;          // función de una sola línea
  const j = SRC.indexOf("\n}\n", m.index + 1);
  return SRC.slice(m.index + 1, j + 2);
}
function recortarObjeto(inicio, fin) {
  const i = SRC.indexOf(inicio);
  if (i < 0) throw new Error("no encontré " + inicio);
  const j = SRC.indexOf(fin, i);
  return SRC.slice(i, j + fin.length);
}
"""


# ── 1. la nivelación ───────────────────────────────────────────────────────────────────

def _plan(edad):
    return _node("""
      const {Adapt, SABERES_MOTOR} = require('./motor_adaptativo.js');
      global.D = {edad: %d, adaptativo_on: true};
      global.Store = {ubicado: () => false, ubicados: () => [], sello: () => 'practicando',
                      repasoPendiente: () => false, stars: () => 0};
      const g = %d - 5; const ids = new Set();
      for (const sid in SABERES_MOTOR) { const s = SABERES_MOTOR[sid];
        if (s.grado <= g) s.juegos.forEach((j) => ids.add(j)); }
      const plan = Adapt.planSondeo([...ids]);
      // la profundidad mínima de la materia del primero, para comparar
      const prof = (sid, v) => { if (v.has(sid)) return 0; v.add(sid); const s = SABERES_MOTOR[sid];
        return (!s || !s.prereqs.length) ? 0 : 1 + Math.max(...s.prereqs.map((p) => prof(p, v))); };
      let minCat = Infinity;
      for (const sid in SABERES_MOTOR) { const s = SABERES_MOTOR[sid];
        if (s.grado !== g || !plan.length) continue;
        const j = s.juegos.find((x) => ids.has(x));
        if (j && Adapt.categoria(j) === plan[0].cat) minCat = Math.min(minCat, prof(sid, new Set())); }
      console.log(JSON.stringify({plan: plan.map((p) => ({sid: p.sid, cat: p.cat, d: p.d, facil: !!p.facil})),
                                  minCat: minCat}));
    """ % (edad, edad))


@pytest.mark.parametrize("edad", [6, 7, 8, 9, 10, 11, 12])
def test_la_nivelacion_es_corta_y_arranca_facil(edad):
    """PRO-04: en 3.º el primer juego era poema_3 (25 % de acierto a la primera) y el chico
    real se fue a los 20 segundos. Y de 4.º a 7.º eran 4-5 juegos antes de ver el cuaderno."""
    r = _plan(edad)
    plan = r["plan"]
    if not plan:
        pytest.skip("sin plan para este grado")
    assert len(plan) <= 3, "la nivelación volvió a ser larga: %d juegos" % len(plan)
    assert plan[0]["facil"], "el primer juego no está marcado como el fácil"
    assert plan[0]["d"] == r["minCat"], \
        "el primer juego no es el más fácil de su materia (%s, d=%s)" % (plan[0]["sid"], plan[0]["d"])
    assert not any(p["facil"] for p in plan[1:]), "sólo el primero es el de arranque"
    assert len({p["cat"] for p in plan}) == len(plan), "repite materia"


_ARNES_SONDEO = _RECORTAR + r"""
eval(recortarObjeto("const Sondeo = {", "\n};\n").replace("const Sondeo", "global.Sondeo"));
global.Adapt = { saberYPrereqs: (sid) => new Set([sid, sid + "-prev"]) };
const marcados = { ubicados: [], sondeo: null };
global.Store = { marcarUbicados: (a) => { marcados.ubicados.push(...a); },
                 marcarSondeo: (s) => { marcados.sondeo = { saltado: !!s }; } };
global.pararVoz = () => {};
const llamadas = [];
Sondeo._siguiente = function () { llamadas.push("siguiente"); this.activo = true; };
Sondeo._terminar = function () { llamadas.push("terminar"); };
Sondeo.plan = [{ sid: "A", juego: "a" }, { sid: "B", juego: "b" }, { sid: "C", juego: "c" }];
Sondeo.idx = 0; Sondeo.aciertos = []; Sondeo.activo = true;
"""


def test_si_le_va_mal_en_dos_seguidos_la_nivelacion_termina():
    """Seguir con el tercero sólo lo haría sentir peor: es lo que pasó en 1.º (2 de 8 en el
    último y no jugó nada más)."""
    r = _node(_ARNES_SONDEO + r"""
      Sondeo.resultado("a", 0.33);
      Sondeo.resultado("b", 0.5);
      console.log(JSON.stringify(llamadas));
    """)
    assert r == ["siguiente", "terminar"], "después de dos malos siguió con el tercero: %s" % r


def test_saltear_un_paso_no_cuenta_como_error_ni_como_acierto():
    r = _node(_ARNES_SONDEO + r"""
      Sondeo.resultado("a", 0.2);
      Sondeo.saltearPaso();                 // saltea el segundo
      Sondeo.resultado("c", 1);
      console.log(JSON.stringify({ llamadas, aciertos: Sondeo.aciertos }));
    """)
    assert r["llamadas"] == ["siguiente", "siguiente", "siguiente"], \
        "saltear un juego cortó la nivelación o la contó como error: %s" % r
    assert r["aciertos"][1]["precision"] is None


def test_el_boton_de_atras_corta_la_nivelacion_sin_perder_lo_ubicado():
    """MOT-10: el ← estaba oculto y no había salida hasta terminar. Ahora se puede ir al menú
    en cualquier paso, y lo que ya resolvió bien queda ubicado."""
    r = _node(_ARNES_SONDEO + r"""
      Sondeo.resultado("a", 1);             // el primero, bien
      Sondeo.cortar();                      // y se va por el ←
      console.log(JSON.stringify({ marcados, activo: Sondeo.activo }));
    """)
    assert r["activo"] is False
    assert r["marcados"]["sondeo"] == {"saltado": True}, "no quedó registrada como salteada"
    assert set(r["marcados"]["ubicados"]) == {"A", "A-prev"}, "se perdió lo que ya había ubicado"


def test_el_atras_y_el_saltear_estan_a_la_vista_en_cada_paso():
    s = _fuente()
    i = s.index("  _siguiente() {")
    cuerpo = s[i:s.index("\n  },", i)]
    assert '$("#btnAtras").classList.add("ver")' in cuerpo, "el ← sigue oculto en la nivelación"
    assert "sondeoSaltear" in cuerpo, "no hay «Saltear este juego» en cada paso"
    j = s.index("function volverMenu() {")
    assert "Sondeo.cortar()" in s[j:s.index("\n}\n", j)], "el ← no corta la nivelación"


def test_la_nivelacion_termina_con_festejo_y_lleva_a_jugar():
    """PRO-04 y PRO-05: terminaba en un cartel de texto y un botón al menú de 70 tarjetas."""
    s = _fuente()
    i = s.index("  _terminar() {")
    cuerpo = s[i:s.index("\n  },", i)]
    assert "Confeti.tirar(" in cuerpo and "Sfx.fanfarria()" in cuerpo, "terminar no se festeja"
    assert "¡Ya sé por dónde empezar!" in cuerpo
    assert "entrarAJugar()" in cuerpo, "el botón grande del final no lleva a jugar"
    k = s.index("  iniciar() {")
    assert "entrarAJugar()" in s[k:s.index("\n  },", k)], "«Saltear y jugar» no lleva a jugar"


def test_en_primero_la_nivelacion_va_en_mayuscula():
    html = _fuente(HTML)
    for sel in ("body.g1 .sondeo,", "body.g1 .sondeo button,", "body.g1 .sondeo-paso,"):
        assert sel in html, "falta %s en la regla de 1.º" % sel


# ── 2. entrar directo a jugar ──────────────────────────────────────────────────────────

_ARNES_SEGUIR = _RECORTAR + r"""
global.location = { pathname: "/act/TOKENNUEVO123/" };
eval(recortar("_hoyStr"));
eval(recortarObjeto("const Store = {", "\n};\n").replace("const Store", "global.Store"));
global.localStorage = { getItem: () => null, setItem: () => {} };
Store.data = { profiles: { Sofi: { stars: {} } }, activeProfile: "Sofi" };
Store.save = () => {};
for (const n of ["_elegirMision", "_idsDelMenu", "_misionDeHoy", "_misionCumplida",
                 "_paraSellarManana", "_idParaSeguir", "entrarAJugar"]) eval(recortar(n));
global.SENO_ON = false;
global.P = [1, 2, 3];
global.GAMES = {};
const ESTADO = {};
global.Adapt = {
  categoria: (id) => (id === "duelo" || id.startsWith("x_")) ? "logica" : "lengua",
  estadoActividad: (id) => ESTADO[id] || "disponible",
  peso: (id) => ({ repaso: 0, recomendado: 1, disponible: 2, dominado: 3, reforzar: 4 })[ESTADO[id] || "disponible"],
  proximaRecomendada: (ids) => ids.find((id) => ESTADO[id] === "recomendado") || null,
};
function menu(ids) {
  global.D = { adaptativo_on: true, escolar_on: true, menu: ids.map((id) => ({ id: id, titulo: id })) };
  ids.forEach((id) => { GAMES[id] = { crear() {} }; });
}
"""


def test_la_primera_vez_entra_directo_a_la_actividad_que_conviene():
    """PRO-05: de cada 10 que tocaban el cuaderno, 1 llegaba a 5 minutos, y el menú de 7.º
    mide 14.000 px. Ahora el final de la nivelación abre la actividad de «Seguí por acá»."""
    r = _node(_ARNES_SEGUIR + r"""
      menu(["a", "b", "c", "duelo"]);
      ESTADO.b = "recomendado";
      let abierta = null, menuPintado = false;
      global.Shell = { abrir: (id) => { abierta = id; } };
      global.pintarMenu = () => { menuPintado = true; };
      entrarAJugar();
      console.log(JSON.stringify({ abierta, menuPintado }));
    """)
    assert r == {"abierta": "b", "menuPintado": False}, r


# ── 3. la sala se entera de que el chico terminó un juego ──────────────────────────────

_ARNES_SALA = _RECORTAR + r"""
eval(recortar("cuadernoEsMuestraPublica"));
eval(recortar("_avisarALaSala"));
function probar(ruta, enMarco) {
  const enviados = [];
  const padre = { postMessage: (m, o) => enviados.push([m, o]) };
  global.location = { pathname: ruta };
  global.window = {};
  window.parent = enMarco ? padre : window;
  _avisarALaSala("termino", { estrellas: 3 });
  return enviados;
}
console.log(JSON.stringify({
  sala: probar("/act/muestra-kydo-3/", true),
  sala_sin_marco: probar("/act/muestra-kydo-3/", false),
  comprado_en_marco: probar("/act/E-f5k2DEAsCSsTqQ/", true),
}));
"""


def test_el_cuaderno_le_avisa_a_la_sala_solo_desde_la_sala():
    """EMB-02: la sala ofrecía guardarlo por reloj, en la mitad de una partida. Ahora el
    cuaderno avisa al terminar un juego; un cuaderno comprado no le habla a nadie."""
    r = _node(_ARNES_SALA)
    assert r["sala"] == [[{"tipo": "kydo-sala", "evento": "termino", "estrellas": 3}, "*"]]
    assert r["sala_sin_marco"] == [], "abierta sola, la muestra no tiene a quién avisar"
    assert r["comprado_en_marco"] == [], "un cuaderno comprado no puede avisarle a nadie"


def test_el_aviso_sale_al_ganar_y_no_en_la_nivelacion():
    s = _fuente()
    i = s.index("if (typeof Sondeo !== \"undefined\" && Sondeo.activo) {\n          Sondeo.resultado(")
    j = s.index('_avisarALaSala("termino"')
    k = s.index("festejar(e, evtDom")
    assert i < k < j, "el aviso a la sala tiene que salir después del festejo y nunca en la nivelación"
    assert '_avisarALaSala("hola")' in s, "sin el saludo la sala no apaga su reloj"


# ── 4. lo jugado en la sala pasa al cuaderno nuevo ─────────────────────────────────────

_ARNES_TRASPASO = _RECORTAR + r"""
eval(recortar("_hoyStr"));
eval(recortar("_tieneProgreso"));
eval(recortar("cuadernoEsMuestraPublica"));
eval(recortar("gradoDelChico"));
eval(SRC.match(/const SALA_TRASPASO_DIAS = \d+;/)[0].replace("const ", "global."));
eval(recortar("_perfilDeLaSala"));
eval(recortar("_traerLoDeLaSala"));
global.NOMBRE_INVITADO = "Invitado";
global.senoEsMuestra = () => false;
function hoyMenos(n) { return _hoyStr(new Date(Date.now() - n * 86400000)); }
function correr(caso) {
  const guardado = {};
  global.localStorage = { getItem: (k) => (k in caso.ls ? JSON.stringify(caso.ls[k]) : null) };
  global.location = { pathname: caso.ruta || "/act/TOKENNUEVO123/" };
  global.D = Object.assign({ escolar_on: true, edad: "8" }, caso.D || {});
  global.Store = { data: { profiles: caso.perfiles || {}, activeProfile: null },
                   save() { guardado.ok = true; } };
  const trajo = _traerLoDeLaSala();
  return { trajo, activo: Store.data.activeProfile, perfiles: Object.keys(Store.data.profiles),
           estrellas: (Store.data.profiles.Juli || {}).stars || null,
           sondeo: !!((Store.data.profiles.Juli || {}).sondeo) };
}
const sala = (dias, extra) => ({ activeProfile: "Juli", profiles: { Juli: Object.assign(
  { stars: { poema_3: 2, suma_columnas: 3 }, dias: dias, sondeo: { ts: Date.now() - 3600e3 } },
  extra || {}) } });
const K3 = "ct3d_act::/act/muestra-kydo-3";
console.log(JSON.stringify({
  normal: correr({ ls: { [K3]: sala([hoyMenos(0)]) } }),
  otro_grado: correr({ ls: { "ct3d_act::/act/muestra-kydo-4": sala([hoyMenos(0)]) } }),
  ya_tiene: correr({ ls: { [K3]: sala([hoyMenos(0)]) }, perfiles: { Tomi: { stars: {} } } }),
  vieja: correr({ ls: { [K3]: sala([hoyMenos(9)], { sondeo: { ts: Date.now() - 9 * 86400e3 } }) } }),
  casatridimensional: correr({ ls: { [K3]: sala([hoyMenos(0)]) }, D: { escolar_on: false } }),
  en_la_sala: correr({ ls: { [K3]: sala([hoyMenos(0)]) }, ruta: "/act/muestra-kydo-3/" }),
  sin_jugar: correr({ ls: { [K3]: { activeProfile: "Juli", profiles: { Juli: { stars: {} } } } } }),
}));
"""


def test_lo_jugado_en_la_sala_pasa_al_cuaderno_nuevo():
    """EXP-11 y PRO-09: el cartel prometía «seguís justo donde estabas» y el cuaderno nuevo
    arrancaba con «¿Quién juega?» y otra nivelación. El chico de 1.º de Tafí Viejo hizo la
    nivelación dos veces en cinco minutos."""
    r = _node(_ARNES_TRASPASO)["normal"]
    assert r["trajo"] and r["activo"] == "Juli", r
    assert r["estrellas"] == {"poema_3": 2, "suma_columnas": 3}
    assert r["sondeo"], "la nivelación de la sala no viajó: la repetiría"


def test_el_traspaso_no_trae_lo_de_otro():
    r = _node(_ARNES_TRASPASO)
    assert not r["otro_grado"]["trajo"], "trajo la sala de otro grado"
    assert not r["ya_tiene"]["trajo"] and r["ya_tiene"]["perfiles"] == ["Tomi"], \
        "pisó un cuaderno que ya tenía chico"
    assert not r["vieja"]["trajo"], "trajo una sala de hace días (puede ser de un hermano)"
    assert not r["sin_jugar"]["trajo"], "trajo un perfil que no jugó nada"


def test_el_traspaso_es_solo_de_kydo_y_nunca_en_la_sala_misma():
    """Un cuaderno de cumpleaños (Casatridimensional) no tiene sala de prueba: no cambia."""
    r = _node(_ARNES_TRASPASO)
    assert not r["casatridimensional"]["trajo"]
    assert not r["en_la_sala"]["trajo"]


def test_el_traspaso_va_despues_del_servidor():
    s = _fuente()
    i = s.index("await recuperarProgresoDelServidor();\n")
    assert "_traerLoDeLaSala()" in s[i:i + 400], \
        "el traspaso tiene que ir DESPUÉS del servidor: si el cuaderno ya tenía a alguien, manda eso"


# ── 5. la misión de hoy, el «1 de 2 días» y la racha ───────────────────────────────────

def test_la_mision_prioriza_repasar_y_sellar_y_deja_afuera_los_extras():
    r = _node(_ARNES_SEGUIR + r"""
      menu(["a", "b", "c", "d", "e", "x_extra", "duelo"]);
      const HOY = "2026-09-25";
      Store.data.profiles.Sofi.dominio = {
        c: { dias: ["2026-09-24"], sello: "practicando", repasarEn: 0 },          // para sellar
        d: { dias: ["2026-09-20", "2026-09-21"], sello: "dominado", repasarEn: 1 }, // repaso
      };
      ESTADO.e = "recomendado"; ESTADO.x_extra = "recomendado";
      const m = _elegirMision(_idsDelMenu(), HOY);
      console.log(JSON.stringify(m));
    """)
    assert r == ["d", "c", "e"], "orden de la misión: repaso, sellar, recomendada: %s" % r


def test_la_mision_queda_fija_en_el_dia_y_se_cumple():
    r = _node(_ARNES_SEGUIR + r"""
      menu(["a", "b", "c", "d"]);
      const antes = _misionDeHoy();
      ESTADO.d = "recomendado";                // el motor cambia de idea en el medio del día
      const despues = _misionDeHoy();
      const cumplida0 = _misionCumplida();
      antes.forEach((id) => Store.marcarGanadaHoy(id));
      console.log(JSON.stringify({ antes, despues, cumplida0, cumplida1: _misionCumplida(),
                                   seguir: _idParaSeguir() }));
    """)
    assert r["antes"] == r["despues"], "la misión cambió en el medio del día"
    assert len(r["antes"]) == 3
    assert r["cumplida0"] is False and r["cumplida1"] is True
    assert r["seguir"] == "d", "con la misión cumplida, «Seguí por acá» vuelve a la recomendada"


def test_uno_de_dos_dias_y_para_sellar():
    r = _node(_ARNES_SEGUIR + r"""
      Store.data.profiles.Sofi.dominio = {
        hoy: { dias: [_hoyStr()], sello: "practicando" },
        ayer: { dias: ["2026-01-01"], sello: "practicando" },
        listo: { dias: ["2026-01-01", "2026-01-02"], sello: "dominado" },
      };
      console.log(JSON.stringify({
        uno: ["hoy", "ayer", "listo", "nada"].map((id) => Store.unoDeDos(id)),
        sellar: ["hoy", "ayer", "listo", "nada"].map((id) => Store.paraSellarHoy(id)),
      }));
    """)
    assert r["uno"] == [True, True, False, False]
    assert r["sellar"] == [False, True, False, False], "sellar HOY es sólo si el 3★ fue otro día"


def test_lo_ganado_hoy_se_reinicia_al_cambiar_el_dia():
    r = _node(_ARNES_SEGUIR + r"""
      Store.marcarGanadaHoy("a", "2026-09-24");
      Store.marcarGanadaHoy("b", "2026-09-25");
      Store.marcarGanadaHoy("b", "2026-09-25");
      console.log(JSON.stringify([Store.ganadasHoy("2026-09-24"), Store.ganadasHoy("2026-09-25")]));
    """)
    assert r == [[], ["b"]]


def test_el_festejo_dice_volve_manana_para_sellarla():
    """PRO-03: el sello pide 3★ en dos días y sólo se festejaba cuando ya había pasado."""
    s = _fuente()
    i = s.index("function festejar(")
    cuerpo = s[i:s.index("\nfunction cerrarFestejo", i)]
    assert "Volvé mañana" in cuerpo and "1 de 2 días" in cuerpo
    assert "D.adaptativo_on" in cuerpo, "el cuaderno de cumpleaños tiene que festejar como siempre"
    assert "Misión de hoy cumplida" in cuerpo
    assert 'id="festejoExtra"' in _fuente(HTML)


def test_la_tarjeta_dice_uno_de_dos_dias():
    s = _fuente()
    assert "Store.unoDeDos(m.id)" in s and "🏅 1 de 2 días" in s


def test_la_racha_se_ve_desde_el_primer_dia():
    """PRO-03: aparecía recién el día 2, y ningún chico real llegó al día 2."""
    s = _fuente()
    i = s.index('_rp = document.getElementById("hdrRacha")')
    assert re.search(r"if \(_racha >= 1\)", s[i - 200:i + 400])
    assert '"Día " + _racha + " de tu racha' in s


# ── 6. el link propio del chico ────────────────────────────────────────────────────────

class _Resp:
    def __init__(self):
        self.code, self.headers, self.cuerpo = None, {}, b""


class _FakeHandler:
    def __init__(self, cookie):
        self._cookie = cookie
        self.r = _Resp()
        self.wfile = self

    def write(self, b):
        self.r.cuerpo += b

    def _read_cookie(self, nombre):
        return self._cookie if nombre == "act_grant" else None

    def send_response(self, code):
        self.r.code = code

    def send_header(self, k, v):
        self.r.headers[k] = v

    def end_headers(self):
        pass

    def _json(self, code, data):
        self.r.code, self.r.cuerpo = code, json.dumps(data).encode()


@pytest.fixture
def motor(tmp_path, monkeypatch):
    import actividades_web as aw
    monkeypatch.setattr(aw, "ACT_DIR", str(tmp_path))
    for tok in ("KYDOGATEADO12345", "CUMPLEPUBLICO123", "muestra-kydo-4"):
        (tmp_path / tok).mkdir()
    gate = {"KYDOGATEADO12345": (True, False), "CUMPLEPUBLICO123": (False, False),
            "muestra-kydo-4": (False, False)}
    monkeypatch.setattr(aw, "estado_gate", lambda t: gate.get(t, (False, False)))
    import servicio
    return servicio, gate


def _pase(servicio, token, cookie):
    h = _FakeHandler(cookie)
    h._es_muestra_publica = servicio.Handler._es_muestra_publica     # staticmethod: sin atar
    servicio.Handler._act_pase_get(h, token)
    return h.r.code, json.loads(h.r.cuerpo or b"{}"), h.r.headers


def test_el_pase_devuelve_el_mismo_permiso_y_nunca_uno_nuevo(motor):
    """EXP-18: copiar la dirección a la tablet del chico daba el candado. El link lleva el
    MISMO permiso que ya abrió el cuaderno en este aparato: vence cuando vence el acceso."""
    servicio, _ = motor
    g = servicio.act_grant_make("KYDOGATEADO12345", ttl=3600)
    code, d, h = _pase(servicio, "KYDOGATEADO12345", g)
    assert code == 200 and d == {"ok": True, "g": g}
    assert h.get("Cache-Control") == "no-store"


def test_el_pase_no_le_contesta_a_quien_no_tiene_permiso(motor):
    servicio, gate = motor
    assert _pase(servicio, "KYDOGATEADO12345", None)[0] == 403
    otro = servicio.act_grant_make("OTROTOKEN", ttl=3600)
    assert _pase(servicio, "KYDOGATEADO12345", otro)[0] == 403, "aceptó el permiso de otro cuaderno"
    vencido = servicio.act_grant_make("KYDOGATEADO12345", ttl=-10)
    assert _pase(servicio, "KYDOGATEADO12345", vencido)[0] == 403, "aceptó un permiso vencido"
    gate["KYDOGATEADO12345"] = (True, True)
    g = servicio.act_grant_make("KYDOGATEADO12345", ttl=3600)
    assert _pase(servicio, "KYDOGATEADO12345", g)[0] == 403, "un cuaderno revocado dio su link"


def test_el_pase_de_un_cuaderno_publico_es_la_direccion_pelada(motor):
    servicio, _ = motor
    assert _pase(servicio, "CUMPLEPUBLICO123", None)[:2] == (200, {"ok": True, "g": None})
    assert _pase(servicio, "muestra-kydo-4", None)[0] == 404, "la muestra es de todos: sin link propio"


def test_el_panel_para_grandes_ofrece_mandarlo_a_la_tablet():
    s = _fuente()
    i = s.index("async function _pasarALaTablet(")
    cuerpo = s[i:s.index("\n}\n", i)]
    assert 'fetch("pase"' in cuerpo and "D.escolar_on" in cuerpo and "cuadernoEsMuestraPublica()" in cuerpo
    assert "wa.me" in cuerpo
    assert "_pasarALaTablet(" in s[s.index("function panelPadres()"):]


# ── 7. el duelo, donde el chico festeja ────────────────────────────────────────────────

def test_el_duelo_se_ofrece_en_el_festejo_y_en_la_mision_cumplida():
    """PRO-10: era la tarjeta 74 de 74, al fondo de Extras, y nadie lo usó."""
    s = _fuente()
    i = s.index("function festejar(")
    assert "_hayDuelo()" in s[i:s.index("\nfunction cerrarFestejo", i)]
    j = s.index("function _pintarMision(")
    assert "_hayDuelo()" in s[j:s.index("\n}\n", j)] and 'Shell.abrir("duelo")' in s[j:s.index("\n}\n", j)]
    assert 'id="btnDuelo"' in _fuente(HTML)
    k = s.index("function _hayDuelo(")
    cuerpo = s[k:s.index("\n}\n", k)]
    assert "D.escolar_on" in cuerpo and "cuadernoEsMuestraPublica()" in cuerpo


def test_el_desafiado_termina_en_la_sala_de_su_grado():
    html = _fuente(os.path.join(BASE, "duelo_publico.html"))
    i = html.index("function cierreHTML(")
    cuerpo = html[i:html.index("\n}\n", i)]
    assert "/kydo/probar?grado=" in cuerpo, "el desafiado sigue terminando en la portada"
