# -*- coding: utf-8 -*-
"""El progreso del chico sobrevive al navegador.

Pablo, 30-jul-2026, después de que publicáramos el cuaderno en `mi.kydo.com.ar`:
*"me parece que cada vez que se sube un cambio se pierde el historial, porque en el
cuaderno de 7.º me pidió varias veces el nombre"*.

No era el deploy: **el `localStorage` es por DOMINIO**. La clave (`ct3d_act::/act/<token>`)
era la misma, pero el navegador guarda un cajón distinto por cada sitio, así que al mover
el cuaderno de dominio el progreso quedó del otro lado, invisible.

Y eso destapó algo más grande, que pasa sin ningún deploy de por medio: el progreso vive
SÓLO en el dispositivo. El chico que pasa de la tablet al celular, o al que le limpian el
navegador, empieza de cero. El servidor ya guardaba un snapshot por chico —lo usa el
tablero del padre— pero **nadie lo leía de vuelta**.

QUÉ SE GUARDA Y QUÉ NO. Estrellas, nivel por actividad, avatar y sellos de dominio. NO los
ítems ya acertados (`io`): son una optimización interna y multiplicarían el tamaño por 60.

LA REGLA QUE NO SE PUEDE AFLOJAR: sólo se restaura si el navegador está VACÍO. Si ya hay
un perfil local, el local manda — puede tener partidas que el snapshot todavía no vio,
porque se manda best-effort. Restaurar encima sería pisar lo nuevo con lo viejo.
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
SERVICIO = os.path.join(_BASE, "servicio.py")

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


def _fuente(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _correr(js):
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip())


_ARNES = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
const m = src.match(/async function recuperarProgresoDelServidor\(\)[\s\S]*?\n\}/);
if (!m) { console.error("no encontré la función"); process.exit(1); }
const RESP = %s;
const Store = { data: %s, save() {} };
global.fetch = async () => ({ ok: %s, json: async () => RESP });
eval(m[0]);
(async () => {
  await recuperarProgresoDelServidor();
  console.log(JSON.stringify({ activo: Store.data.activeProfile, perfiles: Store.data.profiles }));
})();
"""


def _restaurar(respuesta, local=None, ok=True):
    return _correr(_ARNES % (json.dumps(PLAYER), json.dumps(respuesta),
                             json.dumps(local or {"sound": True, "activeProfile": None, "profiles": {}}),
                             "true" if ok else "false"))


SNAP = {"profiles": {"Sofía": {"ts": 1785000000000, "estado": {
    "stars": {"sopa": 3, "memotest": 2}, "nd": {"sopa": 1}, "av": 4,
    "dominio": {"sopa": {"dias": ["2026-07-01", "2026-07-02"], "sello": "dominado", "repasarEn": 0}}}}}}


def test_un_navegador_vacio_recupera_el_progreso():
    """EL caso: cambió de dispositivo, o el cuaderno cambió de dominio."""
    r = _restaurar(SNAP)
    assert r["activo"] == "Sofía", "no recuperó el nombre del chico"
    p = r["perfiles"]["Sofía"]
    assert p["stars"] == {"sopa": 3, "memotest": 2}
    assert p["av"] == 4, "se perdió el avatar que había elegido"
    assert p["dominio"]["sopa"]["sello"] == "dominado", "se perdió lo que ya dominaba"
    assert p["rest"] == 1, "tiene que quedar marcado que vino del servidor"


def test_no_pisa_el_progreso_que_ya_esta_en_el_aparato():
    """La regla que no se afloja: lo local puede tener partidas que el snapshot no vio."""
    local = {"sound": True, "activeProfile": "Juan",
             "profiles": {"Juan": {"stars": {"sopa": 1}}}}
    r = _restaurar(SNAP, local=local)
    assert r["activo"] == "Juan"
    assert list(r["perfiles"]) == ["Juan"], "restauró encima de un perfil que ya jugaba"
    assert r["perfiles"]["Juan"]["stars"] == {"sopa": 1}


def test_elige_el_perfil_que_jugo_ultimo():
    """Si el cuaderno lo usaron dos hermanos, vuelve el último que jugó."""
    snap = {"profiles": {
        "Vieja": {"ts": 1, "estado": {"stars": {"sopa": 1}}},
        "Nueva": {"ts": 999, "estado": {"stars": {"sopa": 3}}}}}
    assert _restaurar(snap)["activo"] == "Nueva"


def test_un_snapshot_viejo_sin_estado_no_rompe_nada():
    """Los links ya entregados mandan el snapshot SIN `estado`: no hay qué restaurar,
    pero tampoco puede quedar un perfil vacío que tape la pantalla de elegir nombre."""
    snap = {"profiles": {"Ana": {"ts": 5, "resumen": {}, "dominados": []}}}
    r = _restaurar(snap)
    assert r["activo"] is None and r["perfiles"] == {}


def test_sin_red_se_juega_igual():
    """Nunca puede dejar al chico sin cuaderno por un fetch que falló."""
    r = _restaurar(SNAP, ok=False)
    assert r["activo"] is None and r["perfiles"] == {}


def test_el_player_manda_el_estado():
    """Sin esto no hay nada que recuperar: el snapshot vuelve a ser sólo un resumen."""
    src = _fuente(PLAYER)
    i = src.index("function _enviarProgreso()")
    cuerpo = src[i:src.index("\n}", i)]
    assert "estado: estado" in cuerpo, "el snapshot dejó de llevar el estado"
    for campo in ("stars", "nd", "av", "dominio"):
        assert campo in cuerpo, "falta %s en el estado" % campo
    # ojo con buscar "io:" a secas: matchea adentro de "dominio:"
    assert "p.io" not in cuerpo, "no se manda `io`: pesa 60 veces más y no es progreso visible"


def test_el_servidor_acepta_y_sanea_el_estado():
    """El endpoint tiene lista blanca: un campo que no esté nombrado se pierde en silencio."""
    src = _fuente(SERVICIO)
    i = src.index("estado = {}")
    cuerpo = src[i:src.index('p = os.path.join(d, "progreso.json")', i)]
    assert '"stars"' in cuerpo and '"nd"' in cuerpo and '"dominio"' in cuerpo
    assert "practicando" in cuerpo, "el sello tiene que validarse contra una lista cerrada"
    assert "[:300]" in cuerpo, "sin tope, un cliente puede inflar el archivo"


def test_no_borra_el_estado_cuando_juega_un_player_viejo():
    """Un link ya entregado manda el snapshot SIN `estado`. Si eso pisara lo guardado, el
    chico perdería lo recuperable justo por abrir el cuaderno desde el aparato viejo."""
    src = _fuente(SERVICIO)
    i = src.index("nuevo = {")
    cuerpo = src[i:i + 900]
    assert 'anterior.get("estado")' in cuerpo, \
        "el estado guardado se pisa con vacío cuando el player no lo manda"
