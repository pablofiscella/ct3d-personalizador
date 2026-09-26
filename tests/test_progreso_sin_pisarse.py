# -*- coding: utf-8 -*-
"""Dos chicos del mismo cuaderno guardando a la vez no se borran (25-sep-2026).

Auditoría MOT-02: `_act_progreso_set` escribía `progreso.json` con `open(p, "w")` +
`json.dump`, sin candado y sin archivo temporal, en un servidor que atiende en paralelo. Si
dos snapshots se cruzaban, el archivo podía quedar truncado o mezclado: la lectura siguiente
lo tomaba como vacío y el POST de después lo reescribía con UN perfil — los hermanos perdían
todo. Y el panel del padre, leyendo justo en ese instante, veía «sin progreso».

Se prueba contra el servidor de verdad, con hilos que mandan snapshots a la vez mientras
otro lee.
"""
import json
import os
import sys
import threading
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)
import actividades_web as aw  # noqa: E402

TOK = "progreso-carrera-1"


@pytest.fixture
def servidor(tmp_path, monkeypatch):
    import servicio
    monkeypatch.setattr(aw, "ACT_DIR", str(tmp_path))
    d = tmp_path / TOK
    d.mkdir()
    (d / "manifest.json").write_text(json.dumps({"titulo": "x"}))
    (d / "data.json").write_text(json.dumps({"edad": "7", "menu": []}))
    srv = ThreadingHTTPServer(("127.0.0.1", 0), servicio.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield "http://127.0.0.1:%d/act/%s/progreso" % (srv.server_address[1], TOK), d
    srv.shutdown()
    srv.server_close()


def _snapshot(perfil, i):
    # un snapshot con peso real: un chico con muchas actividades hechas
    dom = ["actividad_%03d" % k for k in range(120)]
    return json.dumps({"perfil": perfil, "resumen": {"lengua": {"dom": i, "proc": 1,
                       "pend": 3, "total": 20}}, "dominados": dom, "ts": 1000 + i,
                       "estado": {"stars": {x: 3 for x in dom}, "nd": {}, "av": 1,
                                  "dominio": {}}}).encode()


def test_tres_hermanos_a_la_vez_no_se_borran_y_el_panel_nunca_ve_vacio(servidor):
    url, d = servidor
    hermanos = ["Ana", "Beto", "Caro"]
    vacios, errores = [], []
    fin = threading.Event()

    def jugar(perfil):
        for i in range(60):
            try:
                urllib.request.urlopen(urllib.request.Request(
                    url, data=_snapshot(perfil, i), method="POST",
                    headers={"Content-Type": "application/json"}), timeout=10).read()
            except Exception as e:           # noqa: BLE001 — se reporta abajo
                errores.append(repr(e))

    def mirar():
        visto_alguno = False
        while not fin.is_set():
            try:
                r = json.loads(urllib.request.urlopen(url, timeout=10).read())
            except Exception as e:           # noqa: BLE001
                errores.append(repr(e))
                continue
            if r.get("profiles"):
                visto_alguno = True
            elif visto_alguno:
                vacios.append(1)             # ya había progreso y el panel lo vio vacío

    hilos = [threading.Thread(target=jugar, args=(h,)) for h in hermanos]
    panel = threading.Thread(target=mirar)
    panel.start()
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    fin.set()
    panel.join()

    assert not errores, errores[:3]
    final = json.loads((d / "progreso.json").read_text(encoding="utf-8"))
    assert sorted(final["profiles"]) == hermanos, "se perdió un hermano: %s" % sorted(final["profiles"])
    assert all(final["profiles"][h]["resumen"]["lengua"]["dom"] == 59 for h in hermanos)
    assert not vacios, "el panel del padre vio el progreso vacío %d veces" % len(vacios)
    assert not [f for f in os.listdir(d) if f.endswith(".tmp")], "quedaron temporales"


def test_el_tope_de_perfiles_se_sigue_respetando(servidor):
    url, d = servidor
    for i in range(30):
        urllib.request.urlopen(urllib.request.Request(
            url, data=json.dumps({"perfil": "chico%02d" % i, "ts": 1}).encode(),
            method="POST"), timeout=10).read()
    final = json.loads((d / "progreso.json").read_text(encoding="utf-8"))
    assert len(final["profiles"]) == 25
