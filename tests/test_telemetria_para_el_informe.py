# -*- coding: utf-8 -*-
"""Los datos que necesita el INFORME DEL PADRE de Kydo (25-sep-2026, auditoría EXP-06,
PRO-02 y PRO-12).

El padre abría el progreso y veía 0 firmes en todo: las 8 pruebas reales de septiembre,
aunque una había contestado 86 consignas. Lo que el chico hizo estaba guardado —en
`telemetria.jsonl`— pero ninguna pantalla lo leía, y lo que la nivelación averiguó ni
siquiera salía del navegador. Lo que se verifica acá es el lado del MOTOR:

1. **Cada respuesta lleva la hora del SERVIDOR.** La del aparato no sirve: un cuaderno
   creado el 23-sep tenía respuestas «del 21-sep», y el informe contaba un día de más.
2. **Cada respuesta dice QUIÉN y si era la nivelación.** Sin eso dos hermanos se mezclan y
   las consignas del sondeo —difíciles a propósito— parecen «acá se trabó».
3. **La app del padre puede LEER las respuestas**, y un navegador no.
4. **El resultado de la nivelación se guarda en el servidor** y un player viejo no lo borra.
5. **El desglose lo devuelve con nombre**, y separado del dominio.
"""
import io
import json
import os
import shutil
import subprocess
import sys
import time

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import actividades_web as aw  # noqa: E402
import desglose as dg  # noqa: E402
import servicio  # noqa: E402

PLAYER = os.path.join(_BASE, "actividades_player.js")
TOKEN = "tok-test-informe-padre"


@pytest.fixture
def token():
    """Un cuaderno de 4.º mínimo: sólo lo que leen estos endpoints (data.json con edad y
    menú). Armarlo con `aw.crear` genera todo el arte y acá no hace falta."""
    d = os.path.join(aw.ACT_DIR, TOKEN)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    with open(os.path.join(d, "data.json"), "w", encoding="utf-8") as f:
        json.dump({"edad": 9, "menu": [
            {"id": "problemas_mult_div", "titulo": "Problemas de verdad"},
            {"id": "dividir", "titulo": "Dividir"},
        ]}, f)
    yield TOKEN
    shutil.rmtree(d, ignore_errors=True)


def _handler(body=b"", headers=None, ip="127.0.0.1", path="/"):
    """El handler REAL sin levantar el server (mismo arnés que test_reportar_error)."""

    class Falso(servicio.Handler):
        def __init__(self):
            h = {"Content-Length": str(len(body))}
            h.update(headers or {})
            self.headers = h
            self.rfile = io.BytesIO(body)
            self.wfile = io.BytesIO()
            self.client_address = (ip, 12345)
            self.path = path
            self.salida = {}

        def _json(self, code, obj):
            self.salida = {"code": code, "obj": obj}

        def send_response(self, c):
            self.salida.setdefault("code", c)

        def send_header(self, *a):
            pass

        def end_headers(self):
            pass

        def log_error(self, *a):
            pass

    return Falso()


def _postear_respuesta(tok, ev):
    h = _handler(json.dumps(ev).encode())
    h._act_telemetria(tok)
    return h


def _lineas(tok):
    p = os.path.join(aw.ACT_DIR, tok, "telemetria.jsonl")
    return [json.loads(l) for l in open(p, encoding="utf-8")]


# ── 1 y 2. lo que se guarda de cada respuesta ──────────────────────────────────────────

def test_cada_respuesta_lleva_la_hora_del_servidor(token):
    """El reloj del aparato puede estar corrido días: el informe no se puede apoyar en él."""
    antes = int(time.time())
    _postear_respuesta(token, {"j": "dividir", "it": "d#1", "ok": True, "primer": True,
                               "t": 1726000000000})          # un aparato con la fecha vieja
    r = _lineas(token)[-1]
    assert antes <= r["srv"] <= int(time.time()) + 1, "no guardó la hora del servidor"
    assert r["t"] == 1726000000000, "la hora del aparato se sigue guardando tal cual"


def test_cada_respuesta_dice_quien_y_si_era_la_nivelacion(token):
    _postear_respuesta(token, {"j": "dividir", "it": "d#1", "ok": False, "primer": True,
                               "perfil": "Perfil A", "niv": 1})
    r = _lineas(token)[-1]
    assert r["perfil"] == "Perfil A"
    assert r["niv"] is True


def test_un_player_viejo_deja_la_linea_como_antes(token):
    """Los links ya entregados no mandan `perfil` ni `niv`: no tienen que aparecer vacíos."""
    _postear_respuesta(token, {"j": "dividir", "it": "d#1", "ok": True, "primer": True})
    r = _lineas(token)[-1]
    assert "perfil" not in r and "niv" not in r


def test_el_perfil_se_acota(token):
    _postear_respuesta(token, {"j": "x", "perfil": "N" * 500})
    assert len(_lineas(token)[-1]["perfil"]) == 40


# ── 3. la app del padre lee, el navegador no ───────────────────────────────────────────

def _leer(tok, **kw):
    h = _handler(**kw)
    h._act_telemetria_get(tok)
    return h.salida


def test_la_app_del_padre_lee_las_respuestas_por_loopback(token):
    for i in range(3):
        _postear_respuesta(token, {"j": "dividir", "it": "d#%d" % i, "ok": True,
                                   "primer": True})
    r = _leer(token)
    assert r["code"] == 200 and r["obj"]["ok"]
    assert [e["it"] for e in r["obj"]["eventos"]] == ["d#0", "d#1", "d#2"]


def test_un_navegador_no_puede_leerlas(token):
    """Lo que llega por el túnel también sale de loopback, pero trae los headers de
    Cloudflare: eso es un navegador, y no tiene por qué leer esto."""
    _postear_respuesta(token, {"j": "dividir", "it": "d#1", "ok": True, "primer": True})
    assert _leer(token, headers={"CF-Connecting-IP": "200.1.2.3"})["code"] == 403
    assert _leer(token, ip="200.1.2.3")["code"] == 403


def test_con_la_api_key_tambien_se_puede(token, monkeypatch):
    monkeypatch.setattr(servicio, "API_KEY", "clave-de-prueba")
    r = _leer(token, ip="10.0.0.9", headers={"X-API-Key": "clave-de-prueba"})
    assert r["code"] == 200


def test_si_nunca_jugo_devuelve_lista_vacia_no_error(token):
    """«No jugó» es un dato, no una falla: el informe le dice algo distinto al padre."""
    r = _leer(token)
    assert r["code"] == 200 and r["obj"]["eventos"] == []


def test_token_inexistente_da_404():
    assert _leer("no-existe-este-token")["code"] == 404


def test_una_linea_rota_no_tira_el_resto(token):
    p = os.path.join(aw.ACT_DIR, token, "telemetria.jsonl")
    with open(p, "w", encoding="utf-8") as f:
        f.write('{"j": "a"}\n{roto\n\n{"j": "b"}\n')
    assert [e["j"] for e in _leer(token)["obj"]["eventos"]] == ["a", "b"]


def test_devuelve_las_mas_recientes_con_tope(token, monkeypatch):
    monkeypatch.setattr(servicio.Handler, "TELEMETRIA_GET_TOPE", 2)
    p = os.path.join(aw.ACT_DIR, token, "telemetria.jsonl")
    with open(p, "w", encoding="utf-8") as f:
        for j in "abcd":
            f.write(json.dumps({"j": j}) + "\n")
    assert [e["j"] for e in _leer(token)["obj"]["eventos"]] == ["c", "d"]


def test_la_ruta_get_existe_y_va_antes_del_visor():
    """Si cae en el matcher genérico de `/act/<token>/<archivo>`, el GET contesta el visor
    o un 404 y el informe dice «no jugó» a un chico que jugó."""
    src = open(os.path.join(_BASE, "servicio.py"), encoding="utf-8").read()
    i = src.index("return self._act_telemetria_get(")
    j = src.index('m = re.match(r"^/act/([A-Za-z0-9_-]+)(?:/([a-z_0-9.]*))?$", path)')
    assert i < j


# ── 4. la nivelación se guarda en el servidor ──────────────────────────────────────────

def _snapshot(tok, **extra):
    ev = {"perfil": "Perfil A", "resumen": {}, "dominados": [], "ts": 1}
    ev.update(extra)
    h = _handler(json.dumps(ev).encode())
    h._act_progreso_set(tok)


def _progreso(tok):
    return json.load(open(os.path.join(aw.ACT_DIR, tok, "progreso.json"), encoding="utf-8"))


def test_el_resultado_de_la_nivelacion_se_guarda(token):
    _snapshot(token, sondeo={"ts": 1758000000000, "saltado": False},
              ubicado=["MAT-4-PROB", "MAT-4-DIV"])
    p = _progreso(token)["profiles"]["Perfil A"]
    assert p["sondeo"] == {"ts": 1758000000000, "saltado": False}
    assert p["ubicado"] == ["MAT-4-PROB", "MAT-4-DIV"]


def test_un_snapshot_sin_sondeo_no_borra_la_nivelacion(token):
    """Un player viejo, u otro aparato donde el chico todavía no la hizo, manda el snapshot
    sin `sondeo`. Borrarla sería perder lo único que el padre ve de los primeros minutos."""
    _snapshot(token, sondeo={"ts": 5, "saltado": False}, ubicado=["MAT-4-DIV"])
    _snapshot(token)
    p = _progreso(token)["profiles"]["Perfil A"]
    assert p["sondeo"]["ts"] == 5 and p["ubicado"] == ["MAT-4-DIV"]


def test_la_nivelacion_se_sanea(token):
    _snapshot(token, sondeo={"ts": "no-numero", "saltado": "si"},
              ubicado=["X" * 90] + ["MAT-4-DIV"] * 400)
    p = _progreso(token)["profiles"]["Perfil A"]
    assert p["sondeo"] == {"ts": 0, "saltado": True}
    assert len(p["ubicado"]) == 300 and len(p["ubicado"][0]) == 40


# ── 5. el desglose la devuelve con nombre, aparte del dominio ──────────────────────────

def test_el_desglose_nombra_lo_que_la_nivelacion_dio_por_sabido(token):
    _snapshot(token, sondeo={"ts": 5, "saltado": False},
              ubicado=["MAT-4-PROB", "MAT-4-DIV", "NO-EXISTE"])
    per = dg.desglose(token)["perfiles"]["Perfil A"]
    assert per["sondeo"] == {"ts": 5, "saltado": False}
    nombres = {u["id"]: u["nombre"] for u in per["ubicado"]}
    assert nombres == {"MAT-4-PROB": "Problemas de multiplicación y división",
                       "MAT-4-DIV": "División por una cifra"}, \
        "el saber inexistente se cae y los otros llegan con su nombre legible"
    assert per["dominadas"] == 0, "ubicar no es dominar: no puede sumar a `dominadas`"
    assert not any(m["dominado"] for t in per["tarjetas"] for m in t["mide"])


def test_sin_nivelacion_el_desglose_dice_none():
    """None y no {}: «no la hizo» y «la salteó» son dos cosas distintas para el padre."""
    assert dg._sondeo({}) is None
    assert dg._sondeo({"sondeo": {"ts": 1, "saltado": True}}) == {"ts": 1, "saltado": True}
    assert dg._ubicado({}, 4) == []


def test_la_nivelacion_no_nombra_saberes_de_un_grado_mayor():
    assert dg._ubicado({"ubicado": ["MAT-4-DIV"]}, 3) == []


# ── el player manda todo eso ───────────────────────────────────────────────────────────

pytest_node = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


def _fuente():
    return open(PLAYER, encoding="utf-8").read()


def test_el_player_manda_quien_y_si_es_la_nivelacion():
    src = _fuente()
    i = src.index("Tel.push({")
    ev = src[i:src.index("});", i)]
    assert "perfil:" in ev and "activeProfile" in ev
    assert "niv:" in ev and "Sondeo.activo" in ev


_ARNES_SNAP = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
const m = src.match(/function _enviarProgreso\(\)[\s\S]*?\n\}/);
if (!m) { console.error("no encontré _enviarProgreso"); process.exit(1); }
global.D = { adaptativo_on: true, menu: [] };
global.Adapt = { resumenPorCategoria: () => ({}), _dominados: () => new Set() };
global.senoEsMuestra = () => false;
global.esMasAlla = () => false;
global.nivelDeDificultad = () => 0;
global.Store = { data: { activeProfile: "Perfil A", profiles: { "Perfil A": %s } } };
let enviado = null;
global.navigator = { sendBeacon: (url, blob) => { enviado = blob; return true; } };
eval(m[0]);
_enviarProgreso();
enviado.text().then((t) => console.log(t));
"""


def _snap_del_player(perfil):
    r = subprocess.run(["node", "-e", _ARNES_SNAP % (json.dumps(PLAYER), json.dumps(perfil))],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip())


@pytest_node
def test_el_snapshot_lleva_la_nivelacion():
    s = _snap_del_player({"stars": {}, "sondeo": {"ts": 7, "saltado": False},
                          "ubicado": {"MAT-4-DIV": 1, "MAT-4-MUL": 1}})
    assert s["sondeo"] == {"ts": 7, "saltado": False}
    assert sorted(s["ubicado"]) == ["MAT-4-DIV", "MAT-4-MUL"]


@pytest_node
def test_sin_nivelacion_el_snapshot_no_manda_sondeo():
    """Si mandara `sondeo` vacío, el servidor pisaría la nivelación que hizo en otro aparato."""
    s = _snap_del_player({"stars": {"sopa": 2}})
    assert "sondeo" not in s and "ubicado" not in s


def test_terminar_la_nivelacion_manda_el_snapshot():
    """El snapshot salía sólo al ganar una partida: el chico que hacía la nivelación y se
    iba dejaba el resultado en su navegador."""
    src = _fuente()
    i = src.index("  _terminar() {")
    j = src.index("Store.marcarSondeo(false)", i)
    k = src.index("const n = sabidos.size", j)
    assert "_enviarProgreso()" in src[j:k]


def test_saltear_la_nivelacion_no_crea_el_perfil_en_el_servidor():
    """«Ahora no» sin contestar nada NO puede mandar el snapshot (revisión 25-sep-2026): el
    perfil en `progreso.json` es lo que la tienda lee como «jugó», y el aviso de pausa le
    decía «todo lo que hizo tu peque queda guardado» a quien tocó un botón y se fue."""
    src = _fuente()
    j = src.index("Store.marcarSondeo(true)")
    fin = src.index("\n", j)
    assert "_enviarProgreso" not in src[j:fin]
