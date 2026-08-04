# -*- coding: utf-8 -*-
"""«Encontré un error acá» — el 🚩 del cuaderno.

Pablo, 03-ago-2026: *"un icono arriba junto con los otros para que nos puedan informar
algo, una especie de formulario para que si encuentran un error nos puedan avisar. Tipo
Waze pero de esto, encontré en tal lugar, etc"*.

LO QUE LO HACE ÚTIL ES QUE EL «DÓNDE» VIAJA SOLO. En Waze uno no escribe la calle: el
teléfono ya sabe dónde está. Acá igual — el reporte lleva la actividad, el grado, la ronda
y la consigna que había en pantalla, y la familia sólo dice QUÉ pasa. Un "está mal" sin el
dónde no se puede accionar, y pedirle a una madre que explique en qué ejercicio estaba es
pedirle que haga el trabajo de soporte.

Y SE AVISA, no sólo se guarda. Un archivo que nadie mira es lo mismo que no tener nada:
pasó el mismo día con el faro del embudo, que juntaba datos desde el 31-jul sin que
ninguna pantalla los mostrara.
"""
import io
import json
import os
import shutil
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import actividades_web as aw  # noqa: E402
import servicio  # noqa: E402

PLAYER = open(os.path.join(_BASE, "actividades_player.js"), encoding="utf-8").read()
HTML = open(os.path.join(_BASE, "actividades_player.html"), encoding="utf-8").read()
TOKEN = "tok-test-reporte"


@pytest.fixture
def token():
    d = os.path.join(aw.ACT_DIR, TOKEN)
    os.makedirs(d, exist_ok=True)
    yield TOKEN
    shutil.rmtree(d, ignore_errors=True)


def _postear(cuerpo, tok=TOKEN, avisos=None):
    """Ejercita el handler REAL sin levantar el server."""
    body = json.dumps(cuerpo).encode() if isinstance(cuerpo, dict) else cuerpo

    class Falso(servicio.Handler):
        def __init__(self):
            self.headers = {"Content-Length": str(len(body)), "User-Agent": "Chrome/126"}
            self.rfile = io.BytesIO(body)
            self.wfile = io.BytesIO()
            self.salida = {}

        def _json(self, code, obj):
            self.salida = {"code": code, "obj": obj}

        def send_response(self, c):
            pass

        def send_header(self, *a):
            pass

        def end_headers(self):
            pass

        # `log_error` de BaseHTTPRequestHandler arma la línea con la IP del cliente, que
        # este handler de juguete no tiene. Se calla acá: lo que el test mide es que el
        # reporte sobreviva al fallo del aviso, no cómo se loguea.
        def log_error(self, *a):
            pass

    h = Falso()
    if avisos is not None:
        import notificaciones
        orig = notificaciones.notif_emit
        notificaciones.notif_emit = lambda *a, **k: avisos.append((a, k))
        try:
            h._act_reporte(tok)
        finally:
            notificaciones.notif_emit = orig
    else:
        h._act_reporte(tok)
    return h.salida


def _leidos():
    p = os.path.join(aw.ACT_DIR, TOKEN, "reportes.jsonl")
    if not os.path.isfile(p):
        return []
    return [json.loads(l) for l in open(p, encoding="utf-8")]


# ── el dónde viaja solo ────────────────────────────────────────────────────────────────

def test_el_reporte_guarda_DONDE_estaba(token):
    """EL punto de la funcionalidad. Sin esto es un buzón de quejas sin dirección."""
    assert _postear({"motivo": "respuesta", "detalle": "dice que 7x8=54",
                     "juego": "tablas_ninja", "titulo": "Tablas ninja",
                     "grado": "4", "ronda": "3",
                     "consigna": "¿Cuánto es 7 × 8?"})["code"] == 200
    r = _leidos()[-1]
    assert r["titulo"] == "Tablas ninja" and r["grado"] == "4" and r["ronda"] == "3"
    assert r["consigna"] == "¿Cuánto es 7 × 8?"
    assert r["detalle"] == "dice que 7x8=54"
    assert r["token"] == TOKEN and r["ts"], "sin token ni fecha no se puede volver al caso"


def test_el_player_manda_el_contexto_sin_preguntarlo(token):
    """El formulario NO le pide la ubicación a la familia: la saca del propio player."""
    assert "function _contextoDelReporte" in PLAYER
    i = PLAYER.index("function _contextoDelReporte")
    cuerpo = PLAYER[i:i + 900]
    for campo in ("juego:", "titulo:", "grado:", "ronda:", "consigna:"):
        assert campo in cuerpo, "el reporte no manda %s" % campo
    assert "consignaTexto" in cuerpo, "no lee la consigna que hay en pantalla"


def test_se_puede_enviar_sin_escribir_nada(token):
    """La mayoría no va a redactar. Si el envío dependiera del texto, el reporte no sale."""
    assert _postear({"motivo": "roto"})["code"] == 200
    assert _leidos()[-1]["motivo"] == "roto"
    i = PLAYER.index("function abrirReporte")
    cuerpo = PLAYER[i:i + 3500]
    assert "(opcional)" in cuerpo, "el texto libre no está marcado como opcional"
    assert "enviar.disabled = true" in cuerpo, \
        "se puede enviar sin elegir motivo: llegaría un reporte sin ninguna pista"


# ── que le LLEGUE a Pablo ──────────────────────────────────────────────────────────────

def test_avisa_ademas_de_guardar(token):
    """Guardar solo no alcanza: el faro del embudo juntó datos 3 días sin que nadie los
    viera. El aviso lleva el dónde en el propio texto, para poder actuar sin abrir nada."""
    avisos = []
    _postear({"motivo": "audio", "titulo": "English time", "grado": "7", "ronda": "2",
              "consigna": "¿Cómo se dice «agua» en inglés?"}, avisos=avisos)
    assert avisos, "no se avisó a nadie: el reporte muere en un archivo"
    (args, kw) = avisos[0]
    assert args[0] == "reporte_cuaderno"
    texto = json.dumps([args, kw], ensure_ascii=False)
    assert "English time" in texto and "7" in texto, "el aviso no dice dónde fue"


def test_si_el_aviso_falla_el_reporte_NO_se_pierde(token, monkeypatch):
    """Perder el aviso es molesto; perder el reporte es perder a la persona que se tomó
    el trabajo de escribirlo."""
    import notificaciones

    def revienta(*a, **k):
        raise RuntimeError("la tienda no está")

    monkeypatch.setattr(notificaciones, "notif_emit", revienta)
    assert _postear({"motivo": "otro", "detalle": "algo raro"})["code"] == 200
    assert _leidos()[-1]["detalle"] == "algo raro"


# ── es un endpoint público: no puede ser un agujero ────────────────────────────────────

def test_un_token_que_no_existe_no_escribe_nada(token):
    assert _postear({"motivo": "otro"}, tok="no-existe-este-token")["code"] == 404


def test_un_body_roto_no_rompe(token):
    assert _postear(b"{esto no es json")["code"] == 400


def test_el_motivo_sale_de_una_lista_cerrada(token):
    """Sin lista blanca, el campo es texto libre que después se muestra en un aviso."""
    _postear({"motivo": "<script>alert(1)</script>", "detalle": "x"})
    assert _leidos()[-1]["motivo"] == "otro"


def test_los_campos_tienen_tope(token):
    """El endpoint escribe en disco sin auth. Sin topes, un solo pedido llena el archivo."""
    _postear({"motivo": "otro", "detalle": "A" * 5000, "consigna": "B" * 5000,
              "titulo": "C" * 5000})
    r = _leidos()[-1]
    assert len(r["detalle"]) == 500 and len(r["consigna"]) == 300 and len(r["titulo"]) == 80


# ── el botón, donde se encuentra el error ──────────────────────────────────────────────

def test_el_boton_esta_en_el_header_junto_a_los_otros():
    """Pablo lo pidió *"arriba junto con los otros"*, y es lo correcto: el error se
    encuentra JUGANDO. Si hay que salir a buscar dónde avisar, no se avisa."""
    assert 'id="btnReportar"' in HTML, "no está el botón"
    i, j = HTML.index("<header id=\"hdr\">"), HTML.index("</header>")
    assert i < HTML.index('id="btnReportar"') < j, "el botón quedó fuera del header"
    assert 'abrirReporte()' in PLAYER, "el botón no abre nada"


def test_se_agradece_aunque_el_envio_falle():
    """La familia hizo su parte. Decirle "no se pudo" no le sirve y la deja con la
    sensación de que no la escuchamos; el que tiene que enterarse es el servidor."""
    i = PLAYER.index("function abrirReporte")
    cuerpo = PLAYER[i:i + 3500]
    assert "¡Gracias!" in cuerpo
    k = cuerpo.index("¡Gracias!")
    assert "if (!ok" not in cuerpo[:k], "el agradecimiento está condicionado al envío"
