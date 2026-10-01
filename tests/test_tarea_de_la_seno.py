# -*- coding: utf-8 -*-
"""La TAREA DE LA SEÑO en el cuaderno del chico (01-oct-2026).

Pablo aprobó la maqueta el 01-oct-2026: la maestra elige desde su panel de Kydo qué tiene
que practicar el curso y para cuándo, y el chico lo ve ARRIBA de «Misión de hoy» en una
tarjeta «📌 Tarea de la seño — para el lunes · 1 de 3», con lo hecho tildado.

Acá se cuida la mitad del motor:

1. **Se sanea contra el menú real del token** (como el orden): un id que el cuaderno no
   tiene no llega al player, y `n` —cuántas consignas hacen falta para darla por hecha— sale
   de las rondas de ESE juego en ESE cuaderno.
2. **Nunca en un kit de cumpleaños de Casatridimensional**, ni en la muestra pública.
3. **Sólo la escribe Kydo**, por loopback o con la API key: con el link del chico solo no se
   le cambia la tarea a nadie.
4. **El player la pinta arriba de la misión, la tilda y la deja vencer sola.**
"""
import json
import os
import shutil
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)
import actividades_web as aw  # noqa: E402

PLAYER = os.path.join(_BASE, "actividades_player.js")
TOK = "tarea-seno-prueba-4"
TOK_CUMPLE = "tarea-seno-cumple-4"

sin_navegador = pytest.mark.skipif(
    __import__("importlib").util.find_spec("playwright") is None,
    reason="no hay playwright instalado")
sin_node = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


def _cuaderno(act, tok, escolar, edad="9"):
    d = act / tok
    d.mkdir(parents=True)
    dj = aw._armar_data("safari", "Ana", edad, 1, escolar)
    pers = []
    for i in range(8):
        shutil.copy(os.path.join(_BASE, "actividades_arte", "g3", "s%02d.png" % i), d)
        pers.append("s%02d.png" % i)
    # `escolar_on` lo pone `crear()`, no `_armar_data`: es la marca de un cuaderno de Kydo.
    dj.update(personajes=pers, sombras=pers, escolar_on=escolar, adaptativo_on=escolar)
    (d / "data.json").write_text(json.dumps(dj, ensure_ascii=False), encoding="utf-8")
    (d / "manifest.json").write_text(json.dumps({"titulo": "Cuaderno de prueba",
                                                 "escolar_on": escolar}))
    return dj


@pytest.fixture
def act(tmp_path, monkeypatch):
    a = tmp_path / "act"
    a.mkdir()
    monkeypatch.setattr(aw, "ACT_DIR", str(a))
    return a


def _menu_ids(dj):
    return [m["id"] for m in dj["menu"] if isinstance(m, dict)]


def _data(act, tok):
    return json.loads((act / tok / "data.json").read_text(encoding="utf-8"))


# ── 1. se sanea contra el menú real ──────────────────────────────────────────────────

def test_la_tarea_se_sanea_contra_el_menu_y_lleva_las_rondas(act):
    dj = _cuaderno(act, TOK, True)
    por_id = {m["id"]: m for m in dj["menu"] if isinstance(m, dict)}
    ids = [i for i in _menu_ids(dj) if i != "rompecabezas"][:2]
    r = aw.tarea_seno_guardar(TOK, {"id": "7", "hasta": "2026-10-06", "creada": 1759330000,
                                    "items": [{"id": ids[0]}, "no_existe", ids[1], ids[0]]})
    assert r["ok"], r
    t = _data(act, TOK)["tarea_seno"]
    assert [x["id"] for x in t["items"]] == ids, "pasó un id que el cuaderno no tiene"
    for x in t["items"]:
        assert x["n"] == aw._rondas_de(por_id[x["id"]])
    assert t["hasta"] == "2026-10-06" and t["id"] == "7" and t["creada"] == 1759330000


def test_una_tarea_sin_actividades_validas_no_se_guarda(act):
    _cuaderno(act, TOK, True)
    r = aw.tarea_seno_guardar(TOK, {"id": "1", "hasta": "2026-10-06", "items": ["nada"]})
    assert not r["ok"]
    assert "tarea_seno" not in _data(act, TOK)


def test_una_fecha_rota_no_se_guarda(act):
    dj = _cuaderno(act, TOK, True)
    r = aw.tarea_seno_guardar(TOK, {"id": "1", "hasta": "el lunes",
                                    "items": _menu_ids(dj)[:1]})
    assert not r["ok"]


def test_none_le_saca_la_tarea(act):
    dj = _cuaderno(act, TOK, True)
    aw.tarea_seno_guardar(TOK, {"id": "1", "hasta": "2026-10-06", "items": _menu_ids(dj)[:1]})
    assert aw.tarea_seno_leer(TOK)
    assert aw.tarea_seno_guardar(TOK, None)["ok"]
    assert aw.tarea_seno_leer(TOK) is None


def test_la_rondas_por_defecto_son_cinco_como_en_el_player():
    assert aw._rondas_de({"id": "x"}) == 5
    assert aw._rondas_de({"id": "x", "cfg": {"rondas": 10}}) == 10
    assert aw._rondas_de({"id": "x", "cfg": {"rondas": "basura"}}) == 5


# ── 2. nunca en un cumpleaños ─────────────────────────────────────────────────────────

def test_un_kit_de_cumpleanos_no_recibe_tarea(act):
    """Casatridimensional comparte este motor y este data.json: un kit de cumpleaños no
    tiene seño, y una tarea ahí sería la marca escolar adentro del otro negocio."""
    dj = _cuaderno(act, TOK_CUMPLE, False)
    r = aw.tarea_seno_guardar(TOK_CUMPLE, {"id": "1", "hasta": "2026-10-06",
                                           "items": _menu_ids(dj)[:2]})
    assert not r["ok"]
    assert "tarea_seno" not in _data(act, TOK_CUMPLE)


# ── 3. sólo la escribe Kydo, por loopback ────────────────────────────────────────────

@pytest.fixture
def motor(act, monkeypatch, tmp_path):
    import servicio
    srv = ThreadingHTTPServer(("127.0.0.1", 0), servicio.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield "http://127.0.0.1:%d" % srv.server_address[1]
    srv.shutdown()
    srv.server_close()


def _post(url, body, headers=None):
    h = {"Content-Type": "application/json"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST", headers=h)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def test_kydo_la_deja_por_loopback(act, motor):
    dj = _cuaderno(act, TOK, True)
    st, r = _post(motor + "/act/%s/tarea" % TOK,
                  {"tarea": {"id": "3", "hasta": "2026-10-06", "items": _menu_ids(dj)[:3]}})
    assert st == 200 and r["ok"], r
    assert len(_data(act, TOK)["tarea_seno"]["items"]) == 3


def test_desde_afuera_no_se_escribe_una_tarea(act, motor):
    """Un pedido que viene por el túnel trae los headers de Cloudflare: aunque salga de
    loopback, es un navegador de afuera con el link del chico."""
    dj = _cuaderno(act, TOK, True)
    st, _r = _post(motor + "/act/%s/tarea" % TOK,
                   {"tarea": {"id": "3", "hasta": "2026-10-06", "items": _menu_ids(dj)[:3]}},
                   {"CF-Connecting-IP": "203.0.113.9"})
    assert st == 403
    assert "tarea_seno" not in _data(act, TOK)


def test_la_muestra_publica_no_tiene_tarea(act, motor):
    dj = _cuaderno(act, "muestra-kydo-4", True)
    st, _r = _post(motor + "/act/muestra-kydo-4/tarea",
                   {"tarea": {"id": "3", "hasta": "2026-10-06", "items": _menu_ids(dj)[:3]}})
    assert st == 403
    assert "tarea_seno" not in _data(act, "muestra-kydo-4")


def test_la_tarea_sobrevive_a_regenerar_el_token(act):
    """Es trabajo de la maestra, como el orden: re-armar el cuaderno no puede borrarlo."""
    aw.crear({"nombre": "Sofía", "edad": "9", "escolar_on": True}, "safari", token=TOK)
    ids = _menu_ids(_data(act, TOK))[:2]
    aw.tarea_seno_guardar(TOK, {"id": "9", "hasta": "2026-10-06", "items": ids})
    aw.crear({"nombre": "Sofía", "edad": "9", "escolar_on": True}, "safari", token=TOK)
    t = _data(act, TOK).get("tarea_seno") or {}
    assert [x["id"] for x in t.get("items", [])] == ids


# ── 4. el player ──────────────────────────────────────────────────────────────────────

def _fuente():
    with open(PLAYER, encoding="utf-8") as f:
        return f.read()


@sin_node
def test_cuando_vence_dice_el_dia():
    """El 1-oct-2026 es jueves: el lunes siguiente es el 5."""
    js = """
      const fs = require('fs');
      const src = fs.readFileSync('actividades_player.js', 'utf8');
      const i = src.indexOf('function _tareaCuando');
      const j = src.indexOf('let _tareaCSSPuesto', i);
      eval(src.slice(i, j));
      console.log(JSON.stringify([
        _tareaCuando('2026-10-05', '2026-10-01'), _tareaCuando('2026-10-02', '2026-10-01'),
        _tareaCuando('2026-10-01', '2026-10-01'), _tareaCuando('2026-10-13', '2026-10-01')]));
    """
    r = subprocess.run(["node", "-e", js], cwd=_BASE, capture_output=True, text=True,
                       timeout=60)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout) == ["para el lunes", "para mañana", "para hoy", "para el 13/10"]


def test_la_tarea_se_pinta_arriba_de_la_mision():
    s = _fuente()
    i = s.index("_pintarTarea(stage, visibles);             // la tarea de la seño")
    j = s.index("if (!SENO_ON) _pintarMision(stage, visibles);")
    assert i < j


def test_la_tarea_esta_gateada_a_escolar_y_no_a_la_muestra():
    s = _fuente()
    cuerpo = s[s.index("function _tareaVigente"):s.index("function _tareaConsignas")]
    for cond in ("D.escolar_on", "cuadernoEsMuestraPublica()", "senoEsMuestra()", "SENO_ON",
                 "String(t.hasta) < (hoy || _hoyStr())"):
        assert cond in cuerpo, "falta el freno %s" % cond


@pytest.fixture
def servido(act):
    import servicio
    srv = ThreadingHTTPServer(("127.0.0.1", 0), servicio.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield "http://127.0.0.1:%d/act/" % srv.server_address[1]
    srv.shutdown()
    srv.server_close()


def _abrir_y_leer(base, tok, perfil_previo=None):
    from playwright.sync_api import sync_playwright
    url = base + tok + "/"
    with sync_playwright() as p:
        nav = p.chromium.launch()
        ctx = nav.new_context(viewport={"width": 390, "height": 844})
        prev = perfil_previo or {"stars": {}}
        ctx.add_init_script("localStorage.setItem(%r, JSON.stringify({activeProfile: 'Ana',"
                            " profiles: {Ana: %s}}));" % ("ct3d_act::/act/" + tok,
                                                          json.dumps(prev)))
        pag = ctx.new_page()
        pag.goto(url, wait_until="domcontentloaded", timeout=60000)
        pag.wait_for_function("() => !document.getElementById('cargando')", timeout=60000)
        pag.wait_for_timeout(600)
        r = pag.evaluate("""() => {
          const t = document.getElementById('tareaSeno');
          const m = document.getElementById('misionHoy');
          return {hay: !!t, texto: t ? t.innerText : '',
                  hechas: t ? t.querySelectorAll('.tarea-item.hecha').length : 0,
                  antes: !!(t && m && (t.compareDocumentPosition(m) & 4))};
        }""")
        nav.close()
    return r


@sin_navegador
def test_el_chico_ve_la_tarea_con_lo_hecho_tildado(act, servido):
    dj = _cuaderno(act, TOK, True)
    ids = [m["id"] for m in dj["menu"] if isinstance(m, dict)
           and m.get("id") not in ("rompecabezas", "duelo")][:3]
    aw.tarea_seno_guardar(TOK, {"id": "5", "hasta": "2099-12-31", "creada": 1759330000,
                                "items": ids})
    r = _abrir_y_leer(servido, TOK, {"stars": {}, "tareas": {"5": [ids[0]]}})
    assert r["hay"], "no se pintó la tarea"
    assert "Tarea de la seño" in r["texto"] and "1 de 3" in r["texto"]
    assert r["hechas"] == 1


@sin_navegador
def test_una_tarea_vencida_no_se_pinta(act, servido):
    dj = _cuaderno(act, TOK, True)
    aw.tarea_seno_guardar(TOK, {"id": "5", "hasta": "2020-01-01", "items": _menu_ids(dj)[:2]})
    assert not _abrir_y_leer(servido, TOK)["hay"]


@sin_navegador
def test_un_cumpleanos_no_muestra_nada_aunque_el_data_json_la_traiga(act, servido):
    """Segunda cerradura: aunque alguien escribiera la tarea a mano en un kit de
    cumpleaños, el player no la pinta sin `escolar_on`."""
    dj = _cuaderno(act, TOK_CUMPLE, False)
    dj["tarea_seno"] = {"id": "5", "hasta": "2099-12-31", "creada": 0,
                        "items": [{"id": i, "n": 5} for i in _menu_ids(dj)[:2]]}
    (act / TOK_CUMPLE / "data.json").write_text(json.dumps(dj), encoding="utf-8")
    r = _abrir_y_leer(servido, TOK_CUMPLE)
    assert not r["hay"]
