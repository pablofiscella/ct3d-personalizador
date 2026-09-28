# -*- coding: utf-8 -*-
"""El reporte del 🚩 lleva la ventana, la escala y una captura de la pantalla (28-sep-2026).

POR QUÉ
───────
El primer reporte que llegó —«se ve la mitad de la cuadrícula», sopa de letras de 4.º, desde
una PC con Windows— sólo se veía en ventanas anchas y bajas. Pablo lo abrió y lo veía bien, y
hubo que reproducirlo probando tamaños a ciegas. Pablo: *"estaría bueno que si alguien reporta
pueda hacer un screen de la pantalla para ver si justo está ahí"*.

QUÉ SE VIGILA
─────────────
- que la captura se guarde APARTE, dentro del cuaderno, y que el reporte la nombre;
- que llegue al aviso de Pablo como un link FIRMADO, y que sin firma o vencido no se vea: la
  captura puede mostrar el nombre del chico y las muestras públicas las abre cualquiera;
- que el endpoint, que es público y escribe en disco, no acepte cualquier cosa;
- y, con un navegador de verdad, que la captura efectivamente se saque: si la librería no
  carga o falla, el reporte sale igual pero sin imagen, y eso no se vería en ningún otro test.
"""
import base64
import io
import json
import os
import shutil
import sys
import threading
import time
from http.server import ThreadingHTTPServer

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import actividades_web as aw  # noqa: E402
import servicio  # noqa: E402

TOKEN = "tok-test-captura"


def _jpeg(ancho=40, alto=30):
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", (ancho, alto), (200, 80, 40)).save(buf, "JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


@pytest.fixture
def token():
    d = os.path.join(aw.ACT_DIR, TOKEN)
    os.makedirs(d, exist_ok=True)
    yield TOKEN
    shutil.rmtree(d, ignore_errors=True)


class _Falso(servicio.Handler):
    """El handler REAL, sin levantar el server (mismo molde que test_reportar_error)."""

    def __init__(self, body=b"", largo=None):
        self.headers = {"Content-Length": str(len(body) if largo is None else largo),
                        "User-Agent": "Chrome/153"}
        self.rfile = io.BytesIO(body)
        self.wfile = io.BytesIO()
        self.salida = {}
        self.codigo = None
        self.encabezados = {}

    def _json(self, code, obj):
        self.salida = {"code": code, "obj": obj}

    def send_response(self, c):
        self.codigo = c

    def send_header(self, k, v):
        self.encabezados[k] = v

    def end_headers(self):
        pass

    def log_error(self, *a):
        pass


def _postear(cuerpo, largo=None, avisos=None):
    body = json.dumps(cuerpo).encode()
    h = _Falso(body, largo)
    import notificaciones
    orig = notificaciones.notif_emit
    if avisos is not None:
        notificaciones.notif_emit = lambda *a, **k: avisos.append(k)
    try:
        h._act_reporte(TOKEN)
    finally:
        notificaciones.notif_emit = orig
    return h.salida


def _reportes():
    p = os.path.join(aw.ACT_DIR, TOKEN, "reportes.jsonl")
    return [json.loads(l) for l in open(p, encoding="utf-8")] if os.path.isfile(p) else []


def _capturas():
    d = os.path.join(aw.ACT_DIR, TOKEN, "reportes")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


# ── lo que hace el servidor ─────────────────────────────────────────────────────────────

def test_la_captura_se_guarda_aparte_y_el_reporte_la_nombra(token):
    r = _postear({"motivo": "roto", "juego": "sopa", "ventana": "1366x657",
                  "pantalla": "1366x768", "escala": "1", "captura": _jpeg()})
    assert r["code"] == 200
    rep = _reportes()[-1]
    assert rep["ventana"] == "1366x657" and rep["pantalla"] == "1366x768" and rep["escala"] == "1"
    assert rep["captura"] and _capturas() == [rep["captura"]]
    with open(os.path.join(aw.ACT_DIR, TOKEN, "reportes", rep["captura"]), "rb") as f:
        assert f.read(3) == b"\xff\xd8\xff"


def test_el_aviso_lleva_la_ventana_y_el_link_firmado_de_la_captura(token):
    avisos = []
    _postear({"motivo": "otro", "juego": "sopa", "titulo": "Sopa de letras",
              "ventana": "1280x585", "escala": "1.5", "captura": _jpeg()}, avisos=avisos)
    assert avisos, "no avisó"
    k = avisos[-1]
    for texto in (k["detalle"], k["wa_texto"]):
        assert "Ventana 1280x585 · escala 1.5" in texto
        assert "/act-captura/%s/" % TOKEN in texto and "&s=" in texto


def test_lo_que_no_es_un_jpeg_no_se_guarda_pero_el_reporte_si(token):
    png = "data:image/jpeg;base64," + base64.b64encode(b"\x89PNG\r\n\x1a\nfalso").decode()
    for mala in (png, "data:image/png;base64,AAAA", "no es una imagen", 12345,
                 "data:image/jpeg;base64,%%%no-es-base64%%%"):
        r = _postear({"motivo": "roto", "captura": mala})
        assert r["code"] == 200
    assert len(_reportes()) == 5
    assert all(rep["captura"] == "" for rep in _reportes())
    assert _capturas() == []


def test_una_ventana_o_escala_con_forma_rara_se_descarta(token):
    """Lo manda el navegador de cualquiera y termina en el WhatsApp de Pablo."""
    _postear({"motivo": "otro", "ventana": "https://evil.ru/x", "pantalla": "<b>1</b>",
              "escala": "1.5 visitá bit.do"})
    rep = _reportes()[-1]
    assert rep["ventana"] == "" and rep["pantalla"] == "" and rep["escala"] == ""


def test_un_cuerpo_gigante_se_rechaza_sin_leerlo(token):
    r = _postear({"motivo": "otro"}, largo=5 * 1024 * 1024)
    assert r["code"] == 413
    assert _reportes() == []


def test_la_captura_se_ve_solo_con_el_link_firmado_y_vigente(token):
    _postear({"motivo": "roto", "captura": _jpeg()})
    arch = _reportes()[-1]["captura"]
    link = servicio.captura_link(TOKEN, arch)
    q = link.split("?", 1)[1]

    def pedir(query, arch_=arch):
        h = _Falso()
        h._act_captura(TOKEN, arch_, query)
        return h.codigo or h.salida.get("code")

    assert pedir(q) == 200
    assert pedir("") == 404                                   # sin firma
    assert pedir(q.replace("&s=", "&s=0")) == 404              # firma trucha
    otro = _capturas()[0].replace(".jpg", "") + "0.jpg"
    assert pedir(q, otro) == 404                              # la firma es de OTRO archivo
    vencido = servicio.captura_link(TOKEN, arch, now=time.time() - 40 * 86400).split("?", 1)[1]
    assert pedir(vencido) == 404


def test_la_captura_no_se_sirve_por_la_ruta_publica_del_cuaderno(token):
    _postear({"motivo": "roto", "captura": _jpeg()})
    arch = _reportes()[-1]["captura"]
    assert aw.archivo(TOKEN, arch) is None
    assert aw.archivo(TOKEN, "reportes.jsonl") is None


# ── y que el player de verdad la saque ─────────────────────────────────────────────────

@pytest.mark.skipif(__import__("importlib").util.find_spec("playwright") is None,
                    reason="no hay playwright instalado")
def test_el_player_saca_la_captura_y_la_manda_con_la_ventana(tmp_path, monkeypatch):
    monkeypatch.setattr(aw, "ACT_DIR", str(tmp_path))
    tok = "captura-prueba-4"
    d = tmp_path / tok
    d.mkdir()
    dj = aw._armar_data("safari", "Ana", "9", 1, True)
    pers = []
    for i in range(8):
        shutil.copy(os.path.join(_BASE, "actividades_arte", "g4", "s%02d.png" % i), d)
        pers.append("s%02d.png" % i)
    dj.update(personajes=pers, sombras=pers)
    (d / "data.json").write_text(json.dumps(dj, ensure_ascii=False), encoding="utf-8")
    (d / "manifest.json").write_text(json.dumps({"titulo": "Cuaderno de prueba"}))
    clave = "ct3d_act::/act/" + tok
    perfil = ("localStorage.getItem(%r) || localStorage.setItem(%r, JSON.stringify("
              "{activeProfile: 'Ana', profiles: {Ana: {stars: {}}}}));") % (clave, clave)
    srv = ThreadingHTTPServer(("127.0.0.1", 0), servicio.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = "http://127.0.0.1:%d/act/%s/" % (srv.server_address[1], tok)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            nav = p.chromium.launch()
            ctx = nav.new_context(viewport={"width": 1280, "height": 585})
            ctx.add_init_script(perfil)
            pag = ctx.new_page()
            errores = []
            pag.on("pageerror", lambda e: errores.append(str(e)))
            pag.goto(url, wait_until="domcontentloaded", timeout=60000)
            pag.wait_for_function("() => !document.getElementById('cargando')", timeout=60000)
            pag.evaluate("() => Shell.abrir('sopa')")
            pag.wait_for_function("() => document.querySelectorAll('#sopa .celda').length > 0")
            pag.click("#btnReportar")
            pag.click(".rep-op >> nth=4")                      # «Otra cosa»
            pag.click(".rep-btn:has-text('Enviar')")
            pag.wait_for_selector("text=¡Gracias!", timeout=15000)
            nav.close()
        assert not errores, errores
        reps = [json.loads(l) for l in open(d / "reportes.jsonl", encoding="utf-8")]
        rep = reps[-1]
        assert rep["ventana"] == "1280x585", rep
        assert rep["captura"], "el player mandó el reporte SIN captura"
        from PIL import Image
        im = Image.open(d / "reportes" / rep["captura"])
        assert im.format == "JPEG" and im.size[0] == 1280, im.size
    finally:
        srv.shutdown()
        srv.server_close()
