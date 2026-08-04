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


def _cuerpo_abrir_reporte(sin_comentarios=False):
    """El cuerpo completo de `abrirReporte`, delimitado por la función siguiente.

    Con `sin_comentarios` saca las líneas `//`: un test que busca "background:transparent"
    se cazaba a sí mismo, porque esa cadena vive en el comentario que explica POR QUÉ no
    hay que usarla. Misma trampa que ya apareció hoy dos veces en este repo."""
    import re as _re
    i = PLAYER.index("function abrirReporte")
    j = PLAYER.index("\nfunction gatePadres", i)
    cuerpo = PLAYER[i:j]
    if sin_comentarios:
        cuerpo = _re.sub(r"^\s*//[^\n]*$", "", cuerpo, flags=_re.M)
    return cuerpo


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
    cuerpo = _cuerpo_abrir_reporte()
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
    cuerpo = _cuerpo_abrir_reporte()
    assert "¡Gracias!" in cuerpo
    k = cuerpo.index("¡Gracias!")
    assert "if (!ok" not in cuerpo[:k], "el agradecimiento está condicionado al envío"


# ── los tres defectos que encontró Pablo probándolo (04-ago-2026) ──────────────────────

def test_el_boton_de_cancelar_se_VE():
    """*"Tiene un botón blanco sin nada abajo, no sé qué es"*.

    Era el "Ahora no". Estaba con `background: transparent` inline, y como `.btn-sondeo`
    trae `color:#fff`, quedaba BLANCO SOBRE BLANCO: un rectángulo vacío. La hoja ya tenía
    `.btn-sondeo--ghost` (fondo `--soft`, texto `--ink`) hecho justo para esto."""
    cuerpo = _cuerpo_abrir_reporte(sin_comentarios=True)
    assert "btn-sondeo--ghost" in cuerpo, "el botón de cancelar no usa el estilo con texto visible"
    assert "background:transparent" not in cuerpo.replace(" ", ""), \
        "volvió el fondo transparente: el texto blanco desaparece"


def test_las_opciones_NO_reusan_la_clase_de_los_botones_de_juego():
    """*"Está peor, textos muy grandes y sigue sin entrar"*.

    La primera versión les puso `.op` a las opciones — la clase de los botones de los
    JUEGOS, que son de 38px de letra y 84px de alto. Cada frase se partía en dos renglones
    y el formulario no entraba ni de casualidad.

    Y no alcanzaba con declarar `.rep-op` antes: `.op` vive 130 líneas más abajo y, con la
    misma especificidad, gana la última. Por eso el arreglo no es pelear la especificidad
    sino NO reusar una clase pensada para otra cosa."""
    cuerpo = _cuerpo_abrir_reporte()
    assert '"op rep-op"' not in cuerpo and '"rep-op op"' not in cuerpo, \
        "las opciones volvieron a usar `.op`: letra de 38px y 84px de alto por opción"
    assert '"rep-op"' in cuerpo, "las opciones no tienen su propia clase"


def test_ninguna_regla_del_formulario_pierde_contra_una_posterior():
    """El bug de fondo, medido.

    A igual especificidad gana la regla que viene DESPUÉS en la hoja. `.rep-op` estaba
    declarada 130 líneas ANTES que `.op`, así que `.op` ganaba y las opciones salían con
    38px de letra y 84px de alto.

    Reusar una clase de otra parte NO está mal por sí solo —`.btn-sondeo--ghost` se reusa
    bien, porque vive antes que las reglas del formulario y éstas la ajustan—. Lo que no
    puede pasar es que una clase ajena se declare DESPUÉS: ahí pisa al formulario y el
    síntoma aparece en la pantalla, no en los tests."""
    import re as _re
    usadas = set()
    for grupo in _re.findall(r'el\("[a-z]+", "([a-z0-9- ]+)"', _cuerpo_abrir_reporte()):
        usadas.update(c for c in grupo.split() if c and not c.startswith("comoes"))
    assert usadas, "no se encontró ninguna clase del formulario"
    # dónde arrancan las reglas propias del formulario
    primera_propia = min(HTML.index(".%s" % c) for c in usadas if c.startswith("rep-"))
    for c in sorted(usadas):
        if c.startswith("rep-"):
            assert ".%s" % c in HTML, "la clase `%s` no tiene estilos propios" % c
            continue
        pos = HTML.find(".%s" % c)
        assert pos >= 0 and pos < primera_propia, (
            "el formulario usa `%s`, que se declara DESPUÉS de sus propias reglas: "
            "con la misma especificidad pisa al formulario (es lo que pasó con `.op`)" % c)


def test_el_formulario_ENTRA_sin_scrollear():
    """*"Tiene la barra de scroll porque por poco no entra"*. Un formulario que hay que
    scrollear para llegar al Enviar es un formulario que no se manda.

    Se mide sobre las reglas que lo hacen compacto: sin ellas hereda las de las lecciones
    (opciones de 12px y botones de 54px apilados) y no entra."""
    assert ".comoes--reporte" in HTML, "el formulario no tiene estilos propios"
    for regla in (".rep-op", ".rep-acciones", ".rep-btn"):
        assert regla in HTML, "falta %s: el formulario vuelve a los estilos grandes" % regla
    i = HTML.index(".rep-acciones")
    assert "display: flex" in HTML[i:i + 120], \
        "los dos botones van en FILA; apilados suman 108px por dos palabras"


def test_desde_el_MENU_se_puede_decir_en_que_actividad():
    """*"Si se pudiera ser más específico en la actividad mejor"*.

    Jugando, el player ya sabe dónde está. Pero el 🚩 también se toca desde el menú —que es
    donde uno se acuerda de avisar— y ahí el reporte salía como "el cuaderno", sin
    actividad: justo el dato que lo hace accionable."""
    cuerpo = _cuerpo_abrir_reporte()
    assert "const enUnJuego = !!Shell.actual" in cuerpo
    assert 'document.createElement("select")' in cuerpo, \
        "desde el menú no se puede elegir la actividad"
    assert "(D.menu || []).map" in cuerpo, "la lista no sale del menú del cuaderno"
    # y lo elegido tiene que MANDAR sobre el contexto vacío
    assert "if (sel && sel.value)" in cuerpo, "se arma la lista pero no se usa al enviar"
    assert "ctx.titulo = m.titulo" in cuerpo, "no viaja el título de la actividad elegida"


def test_jugando_NO_pregunta_la_actividad():
    """El control del anterior. Si preguntara siempre, se le estaría pidiendo a la familia
    un dato que el player ya tiene — que es exactamente lo que esta pantalla evita."""
    cuerpo = _cuerpo_abrir_reporte()
    j = cuerpo.index("if (!enUnJuego)")
    k = cuerpo.index('document.createElement("select")')
    assert j < k, "la lista se arma sin mirar si ya está adentro de una actividad"


def test_la_lista_deja_no_saber():
    """Obligar a elegir una de 39 actividades para poder avisar es otra forma de que no
    avisen. La primera opción es "no sé"."""
    cuerpo = _cuerpo_abrir_reporte()
    assert 'value=""' in cuerpo and "No sé" in cuerpo
