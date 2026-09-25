# -*- coding: utf-8 -*-
"""La sala de prueba pública no hereda ni guarda el progreso de otros visitantes.

POR QUÉ EXISTE (25-sep-2026, auditoría EXP-02/PRO-01/MOT-01/SEG-04/MOT-13). Los cuadernos
`muestra-kydo-1..7` son la sala de /kydo/probar, el «mirarlo ustedes» del correo a 2.693
escuelas y las demos de la portada: UN cuaderno por grado para todo el mundo. Cada familia
nueva abría el cuaderno con el nombre y las estrellas del visitante anterior, sin «¿Quién
juega?» ni nivelación, y los nombres de chicos quedaban públicos en /act/muestra-kydo-N/progreso.
Y el nombre del perfil se pintaba sin escapar en el panel para grandes: `<img onerror=…>` se
ejecutaba.

Lo que cuidan estos tests:
  · el player no LEE ni ESCRIBE progreso en el servidor para un cuaderno muestra-*;
  · el servidor tampoco (segunda barrera: un player viejo en caché, o alguien con curl);
  · un cuaderno de verdad sigue recuperando y guardando como siempre;
  · el nombre se escapa en el panel y se sanea al guardarlo.
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

node = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


def _fuente(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _node(js):
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip())


_ARNES_MUESTRA = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
const f = src.match(/function cuadernoEsMuestraPublica\(\)[\s\S]*?\n\}/);
if (!f) { console.error("no encontré cuadernoEsMuestraPublica"); process.exit(1); }
const res = {};
for (const ruta of %s) {
  global.location = { pathname: ruta };
  eval(f[0]);
  res[ruta] = cuadernoEsMuestraPublica();
}
console.log(JSON.stringify(res));
"""


@node
def test_reconoce_la_sala_y_no_los_cuadernos_de_verdad():
    rutas = ["/act/muestra-kydo-4/", "/act/muestra-kydo-1", "/act/muestra-otra/x",
             "/act/E-f5k2DEAsCSsTqQ/", "/act/revision-4to/", "/act/Uxs13dkGbXKpocSB/",
             "/act/nomuestra-1/"]
    r = _node(_ARNES_MUESTRA % (json.dumps(PLAYER), json.dumps(rutas)))
    assert r["/act/muestra-kydo-4/"] and r["/act/muestra-kydo-1"] and r["/act/muestra-otra/x"]
    assert not any(r[x] for x in ("/act/E-f5k2DEAsCSsTqQ/", "/act/revision-4to/",
                                  "/act/Uxs13dkGbXKpocSB/", "/act/nomuestra-1/"))


_ARNES_RECUPERA = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
const f = src.match(/function cuadernoEsMuestraPublica\(\)[\s\S]*?\n\}/);
const m = src.match(/async function recuperarProgresoDelServidor\(\)[\s\S]*?\n\}/);
global.location = { pathname: %s };
eval(f[0]);
global.senoEsMuestra = () => false;
const Store = { data: { profiles: {}, activeProfile: null }, save() {} };
let pedidos = 0;
global.fetch = async () => { pedidos++; return { ok: true, json: async () => (
  { profiles: { "Otro chico": { ts: 1, estado: { stars: { sopa: 3 }, nd: {}, av: 1, dominio: {} } } } }) }; };
eval(m[0]);
(async () => {
  await recuperarProgresoDelServidor();
  console.log(JSON.stringify({ activo: Store.data.activeProfile, pedidos }));
})();
"""


@node
def test_la_sala_no_trae_el_progreso_de_otro_visitante():
    r = _node(_ARNES_RECUPERA % (json.dumps(PLAYER), json.dumps("/act/muestra-kydo-3/")))
    assert r["activo"] is None, "la sala saludó con el nombre de otro visitante"
    assert r["pedidos"] == 0, "la sala le pidió al servidor el progreso compartido"


@node
def test_un_cuaderno_de_verdad_sigue_recuperando():
    r = _node(_ARNES_RECUPERA % (json.dumps(PLAYER), json.dumps("/act/E-f5k2DEAsCSsTqQ/")))
    assert r["activo"] == "Otro chico"


def test_el_player_no_envia_progreso_de_la_sala():
    src = _fuente(PLAYER)
    i = src.index("function _enviarProgreso()")
    cuerpo = src[i:src.index("\n}", i)]
    assert "cuadernoEsMuestraPublica()" in cuerpo


def test_el_nombre_se_escapa_en_el_panel_para_grandes():
    src = _fuente(PLAYER)
    i = src.index("function panelPadres()")
    assert "escHtml(Store.data.activeProfile" in src[i:i + 300]


@node
def test_escHtml_neutraliza_codigo():
    js = r"""
const src = require("fs").readFileSync(%s, "utf8");
eval(src.match(/function escHtml\(s\)[\s\S]*?\n\}/)[0]);
console.log(JSON.stringify(escHtml('<img src=x onerror="a()">&\'')));
""" % json.dumps(PLAYER)
    out = _node(js)
    assert "<" not in out and ">" not in out and '"' not in out


# ─────────── el servidor del motor ───────────

class _FakeHandler:
    """Lo mínimo para llamar a los métodos de progreso del handler real sin levantar un
    servidor: guarda la respuesta en vez de escribirla al socket."""
    def __init__(self, cuerpo=b"{}"):
        self._cuerpo = cuerpo
        self.resp = None

    def _body(self):
        return self._cuerpo

    def _json(self, code, data):
        self.resp = (code, data)


def _handler_con(servicio, cuerpo=b"{}"):
    h = _FakeHandler(cuerpo)
    H = servicio.Handler if hasattr(servicio, "Handler") else None
    assert H is not None, "no encontré la clase Handler en servicio.py"
    h._es_muestra_publica = H._es_muestra_publica          # staticmethod: sin atar
    for nombre in ("_act_progreso_get", "_act_progreso_set"):
        setattr(h, nombre, getattr(H, nombre).__get__(h))
    return h


@pytest.fixture
def motor(tmp_path, monkeypatch):
    import actividades_web as aw
    monkeypatch.setattr(aw, "ACT_DIR", str(tmp_path))
    for tok in ("muestra-kydo-4", "TOKENDEVERDAD1234"):
        d = tmp_path / tok
        d.mkdir()
        (d / "progreso.json").write_text(json.dumps(
            {"profiles": {"Chico": {"ts": 1, "resumen": {}, "dominados": []}}}), encoding="utf-8")
    import servicio
    return servicio, tmp_path


def test_el_servidor_no_devuelve_el_progreso_de_la_sala(motor):
    servicio, _ = motor
    h = _handler_con(servicio)
    h._act_progreso_get("muestra-kydo-4")
    assert h.resp == (200, {"profiles": {}})
    h._act_progreso_get("TOKENDEVERDAD1234")
    assert "Chico" in h.resp[1]["profiles"], "un cuaderno de verdad dejó de devolver su progreso"


def test_el_servidor_no_guarda_progreso_en_la_sala(motor):
    servicio, tmp = motor
    antes = (tmp / "muestra-kydo-4" / "progreso.json").read_text(encoding="utf-8")
    h = _handler_con(servicio, json.dumps({"perfil": "Intruso"}).encode())
    h._act_progreso_set("muestra-kydo-4")
    assert h.resp[0] == 200 and h.resp[1].get("guardado") is False
    assert (tmp / "muestra-kydo-4" / "progreso.json").read_text(encoding="utf-8") == antes
