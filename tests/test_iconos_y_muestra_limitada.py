# -*- coding: utf-8 -*-
"""Dos arreglos de Kydo aprobados por Pablo el 01-oct-2026.

1. ÍCONOS QUE NO SE DIBUJAN. Pablo, en el panel de la tarea de la seño: *"fijate tablas ninja
   no tiene icono"*. 🥷 (Emoji 13) y 🟰 (Emoji 14) salen como un cuadradito vacío en Windows 10
   —que llega a Emoji 12— y en celulares viejos. El guardián del 04-sep-2026
   (`test_iconos_se_dibujan_en_todos_lados.py`) miraba sólo el bloque U+1FA70–1FAFF, y estos
   dos viven en otros bloques: pasaron. Acá se mira por VERSIÓN de emoji. Y como el ícono queda
   congelado en el `data.json` de cada cuaderno ya entregado, también se prueba que se traduzca
   al mostrar (player y desglose).

2. LA MUESTRA PÚBLICA TAMBIÉN VENCE. El límite de 30 minutos vivía sólo en la sala de
   /kydo/probar; abriendo `muestra-kydo-N/` directo el cuaderno se usaba entero y para siempre.
   Ahora el propio cuaderno cuenta, salvo adentro de un marco (manda la sala), en `?muestra=`
   (una actividad pública a propósito) y en el modo seño (que pasa a ser vista previa).
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

node = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")

#: Códigos de emoji de Emoji 13.0 en adelante (sacado de la tabla de emoji de Unicode). Más el
#: bloque entero U+1FA70–1FAFF, que el guardián del 04-sep ya trataba como no seguro (trae
#: Emoji 12 que tampoco está en celulares viejos).
EMOJI_13_O_MAS = (
    (0x26A7, 0x26A7), (0x1F6D6, 0x1F6D9), (0x1F6DC, 0x1F6DF), (0x1F6FB, 0x1F6FC),
    (0x1F7F0, 0x1F7F0), (0x1F90C, 0x1F90C), (0x1F972, 0x1F972), (0x1F977, 0x1F979),
    (0x1F9A3, 0x1F9A4), (0x1F9AB, 0x1F9AD), (0x1F9CB, 0x1F9CC), (0x1FA70, 0x1FAFF))


def _no_se_dibujan(texto):
    return ["%s U+%04X" % (c, ord(c)) for c in (texto or "")
            if any(a <= ord(c) <= b for a, b in EMOJI_13_O_MAS)]


def _fuente(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _node(js):
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def _funcion_js(src, firma):
    m = re.search(re.escape(firma) + r"[\s\S]*?\n\}", src)
    assert m, "no encontré %s en el player" % firma
    return m.group(0)


# ─────────────────────────────── 1. los íconos ───────────────────────────────

def test_ningun_icono_del_catalogo_es_de_emoji_13_o_posterior():
    import actividades_curriculum as ac
    malos = ["%s (%s.º): %s" % (a.get("titulo"), a.get("grado"), _no_se_dibujan(a.get("icono")))
             for a in ac.CATALOGO if _no_se_dibujan(a.get("icono"))]
    src = _fuente(os.path.join(BASE, "actividades_web.py"))
    for m in re.finditer(r'"titulo":\s*"([^"]*)",\s*"icono":\s*"([^"]*)"', src):
        if _no_se_dibujan(m.group(2)):
            malos.append("%s (actividades_web.py): %s" % (m.group(1), _no_se_dibujan(m.group(2))))
    assert not malos, "íconos que Windows 10 dibuja como un cuadradito:\n  " + "\n  ".join(malos)


def test_tablas_ninja_y_despeja_la_x_tienen_icono_nuevo():
    src = _fuente(os.path.join(BASE, "actividades_web.py"))
    assert src.count('"titulo": "Tablas ninja", "icono": "🥋"') == 4
    assert '"titulo": "Despejá la x", "icono": "↔️"' in src


def test_el_mapa_cubre_los_dos_de_hoy_y_sus_reemplazos_se_dibujan():
    import emoji_compat as ec
    assert ec.EMOJI_COMPAT["🥷"] == "🥋"
    assert ec.EMOJI_COMPAT["🟰"] == "↔️"
    for viejo, nuevo in ec.EMOJI_COMPAT.items():
        assert _no_se_dibujan(viejo), "%r no hace falta en el mapa: ya se dibuja" % viejo
        assert not _no_se_dibujan(nuevo), "el reemplazo de %r tampoco se dibuja" % viejo
    # las secuencias antes que sus partes
    assert ec.compat("❤️‍🩹 y 🩹") == "⚕️ y ⚕️"
    assert ec.compat("🥷 Tablas") == "🥋 Tablas"
    assert ec.compat("") == "" and ec.compat(None) == ""


def test_el_desglose_que_lee_la_app_sale_traducido():
    """El panel del curso y la tarea de la seño (app de Kydo) leen el desglose: el ícono que
    trae un `data.json` viejo tiene que salir ya cambiado."""
    import desglose
    t = desglose._tarjeta({"id": "tablas_ninja", "titulo": "Tablas ninja", "icono": "🥷"},
                          {}, {}, 4)
    assert t["icono"] == "🥋"


@pytest.fixture
def tokens(tmp_path, monkeypatch):
    import actividades_web as aw
    monkeypatch.setattr(aw, "ACT_DIR", str(tmp_path))
    aw.crear({"nombre": "Muestra", "edad": "9", "escolar_on": True}, "safari",
             token="muestra-kydo-4")
    aw.crear({"nombre": "Sofi", "edad": "9", "escolar_on": True}, "safari", token="escolar-de-verdad")
    aw.crear({"nombre": "Sofi", "edad": "7"}, "safari", token="cumple-de-verdad")
    return aw


def _ventana(page, nombre):
    m = re.search(r"window\." + nombre + r" = (.*?);", page)
    assert m, "no está window.%s en el visor" % nombre
    return json.loads(m.group(1))


def test_el_visor_le_pasa_el_mapa_al_player(tokens):
    for tok in ("muestra-kydo-4", "escolar-de-verdad", "cumple-de-verdad"):
        page = tokens.html(tok)
        assert "{{EMOJI_COMPAT}}" not in page and "{{MUESTRA_LIMITE}}" not in page
        assert _ventana(page, "EMOJI_COMPAT")["🥷"] == "🥋"


@node
def test_el_player_traduce_el_icono_congelado_en_el_data_json():
    src = _fuente(PLAYER)
    js = """
global.window = { EMOJI_COMPAT: {"🥷": "🥋", "🟰": "↔️", "❤️‍🩹": "⚕️", "🩹": "⚕️"} };
const _ICONO_POR_BANDERA = {}; const _ES_BANDERA = /[\\u{1F1E6}-\\u{1F1FF}]/u;
%s
%s
console.log(JSON.stringify([_iconoSeguro({id: "tablas_ninja", icono: "🥷"}),
  _iconoSeguro({id: "ecuaciones_simples", icono: "🟰"}), _iconoSeguro({icono: "❤️‍🩹"}),
  _iconoSeguro({icono: "🧮"})]));
""" % (_funcion_js(src, "function _iconoCompat("), _funcion_js(src, "function _iconoSeguro("))
    assert _node(js) == ["🥋", "↔️", "⚕️", "🧮"]


# ───────────────────────────── 2. la muestra vence ─────────────────────────────

def test_solo_la_muestra_recibe_el_limite_y_por_config(tokens, monkeypatch):
    monkeypatch.delenv("CT3D_MUESTRA_LIMITE_MIN", raising=False)
    c = _ventana(tokens.html("muestra-kydo-4"), "MUESTRA_LIMITE")
    assert c["min"] == 30 and c["dias"] == 30
    assert c["guardar"].endswith("/kydo/probar")
    # los cuadernos de verdad no cambian en nada
    assert _ventana(tokens.html("escolar-de-verdad"), "MUESTRA_LIMITE") is None
    assert _ventana(tokens.html("cumple-de-verdad"), "MUESTRA_LIMITE") is None
    monkeypatch.setenv("CT3D_MUESTRA_LIMITE_MIN", "45")
    assert _ventana(tokens.html("muestra-kydo-4"), "MUESTRA_LIMITE")["min"] == 45
    monkeypatch.setenv("CT3D_MUESTRA_LIMITE_MIN", "0")       # 0 lo apaga
    assert _ventana(tokens.html("muestra-kydo-4"), "MUESTRA_LIMITE") is None


def test_en_el_espejo_el_boton_no_manda_a_produccion(tokens, monkeypatch):
    monkeypatch.setenv("CT3D_ENTORNO", "dev")
    assert _ventana(tokens.html("muestra-kydo-4"), "MUESTRA_LIMITE")["guardar"] == \
        "https://dev.kydo.com.ar/kydo/probar"


@node
def test_el_reloj_es_el_de_la_sala_y_no_se_reinicia_al_recargar():
    src = _fuente(PLAYER)
    js = """%s
const T = 1800000000;
console.log(JSON.stringify([
  _relojDeMuestra(null, T, 30),                 // primera vez: arranca ahora
  _relojDeMuestra(String(T - 600), T, 30),      // recargó a los 10 min: le quedan 20
  _relojDeMuestra(String(T - 1800), T, 30),     // justo 30: vencida
  _relojDeMuestra(String(T - 99999), T, 30),    // hace días: vencida
  _relojDeMuestra(String(T + 500), T, 30),      // del futuro: arranca ahora
  _relojDeMuestra("basura", T, 30)]));
""" % _funcion_js(src, "function _relojDeMuestra(")
    r = _node(js)
    T = 1800000000
    assert r[0] == {"desde": T, "restan": 1800}
    assert r[1] == {"desde": T - 600, "restan": 1200}
    assert r[2]["restan"] == 0 and r[3]["restan"] == 0
    assert r[4] == {"desde": T, "restan": 1800}
    assert r[5] == {"desde": T, "restan": 1800}


_ARNES_CORTE = r"""
const src = require("fs").readFileSync(%s, "utf8");
const pick = (f) => { const m = src.match(new RegExp(f.replace(/[()]/g, "\\$&") + "[\\s\\S]*?\\n\\}"));
                      if (!m) { console.error("falta " + f); process.exit(1); } return m[0]; };
const casos = %s, res = [];
for (const c of casos) {
  let vencio = 0;
  const store = {}; if (c.desde) store.kydo_muestra_desde = String(c.desde);
  global.localStorage = { getItem: (k) => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = v; } };
  global.location = { pathname: c.ruta };
  const win = { MUESTRA_LIMITE: c.cfg }; win.parent = c.embebida ? {} : win;
  global.window = win;
  const SENO_ON = !!c.seno, MUESTRA_SOLA = c.sola || null;
  let MUESTRA_VENCIDA = false;
  const MUESTRA_RELOJ_KEY = "kydo_muestra_desde";
  const _vencerMuestra = () => { vencio++; MUESTRA_VENCIDA = true; };
  eval(pick("function cuadernoEsMuestraPublica()") + pick("function _relojDeMuestra(") +
       pick("function _muestraEmbebida()") + pick("function _muestraConReloj()") +
       "res.push([" + pick("function _revisarRelojDeMuestra()").replace(/^function _revisarRelojDeMuestra\(\)/, "(function ()") +
       ")(), vencio, store.kydo_muestra_desde || null]);");
}
console.log(JSON.stringify(res));
"""


@node
def test_corta_la_muestra_abierta_directo_y_nada_mas():
    hace_rato = 1000000000          # 2001: vencida hace mucho
    cfg = {"min": 30, "dias": 30, "guardar": "https://kydo.com.ar/kydo/probar"}
    casos = [
        {"ruta": "/act/muestra-kydo-4/", "cfg": cfg, "desde": hace_rato},                    # 0 corta
        {"ruta": "/act/muestra-kydo-4/", "cfg": cfg},                                       # 1 recién llega
        {"ruta": "/act/muestra-kydo-4/", "cfg": cfg, "desde": hace_rato, "embebida": True},  # 2 la sala manda
        {"ruta": "/act/muestra-kydo-4/", "cfg": cfg, "desde": hace_rato, "seno": True},      # 3 modo seño
        {"ruta": "/act/muestra-kydo-4/", "cfg": cfg, "desde": hace_rato, "sola": "angulos"},  # 4 ?muestra=
        {"ruta": "/act/E-f5k2DEAsCSsTqQ/", "cfg": cfg, "desde": hace_rato},                  # 5 de verdad
        {"ruta": "/act/E-f5k2DEAsCSsTqQ/", "cfg": None, "desde": hace_rato},                 # 6 de verdad
        {"ruta": "/act/muestra-kydo-4/", "cfg": None, "desde": hace_rato},                   # 7 apagado
    ]
    r = _node(_ARNES_CORTE % (json.dumps(PLAYER), json.dumps(casos)))
    assert r[0][:2] == [True, 1], "la muestra vencida abierta directo no cortó"
    assert r[1][:2] == [False, 0] and r[1][2], "el reloj tiene que arrancar en la primera visita"
    assert r[2][:2] == [False, 0], "adentro de la sala manda la sala: no va un segundo cartel"
    assert r[2][2] == str(hace_rato), "adentro de la sala el reloj igual corre"
    for i in (3, 4, 5, 6, 7):
        assert r[i][:2] == [False, 0], "caso %d no tenía que cortar" % i


def test_la_unica_puerta_a_un_juego_mira_el_reloj_y_la_vista_previa():
    src = _fuente(PLAYER)
    i = src.index("  abrir(id) {")
    cuerpo = src[i:src.index("  ctx(item) {", i)]
    assert "_revisarRelojDeMuestra()" in cuerpo, "Shell.abrir no mira el reloj de la muestra"
    assert cuerpo.index("_revisarRelojDeMuestra()") < cuerpo.index("GAMES[id].crear"), \
        "el corte tiene que ir ANTES de armar el juego"
    assert "_senoVistaPrevia()" in cuerpo and "SENO_VISTA_RONDAS" in cuerpo
    assert re.search(r"const SENO_VISTA_RONDAS = 1;", src)
    # y se arma al arrancar, después de saber si es seño o `?muestra=`
    b = src.index("async function boot()")
    arranque = src[b:src.index("\n}", b)]
    assert arranque.index("SENO_ON = ") < arranque.index("_armarRelojDeMuestra()")


@node
def test_la_vista_previa_es_solo_para_la_seno_en_la_muestra():
    src = _fuente(PLAYER)
    js = """
const res = [];
for (const [ruta, seno] of [["/act/muestra-kydo-4/", true], ["/act/muestra-kydo-4/", false],
                            ["/act/E-f5k2DEAsCSsTqQ/", true]]) {
  global.location = { pathname: ruta };
  const SENO_ON = seno;
  eval(%s + %s + "res.push(_senoVistaPrevia());");
}
console.log(JSON.stringify(res));
""" % (json.dumps(_funcion_js(src, "function cuadernoEsMuestraPublica()")),
       json.dumps(_funcion_js(src, "function _senoVistaPrevia()")))
    assert _node(js) == [True, False, False]


def test_el_cartel_dice_lo_aprobado_y_sale_del_marco():
    src = _fuente(PLAYER)
    f = _funcion_js(src, "function _vencerMuestra()")
    assert "¿Le gusta? Guardáselo" in f
    assert 'target="_top"' in f, "el botón tiene que salir del cuaderno, no abrir la sala adentro"
    assert "?grado=" in f
    assert "2147483000" in f, "el cartel tiene que tapar todo lo demás"
