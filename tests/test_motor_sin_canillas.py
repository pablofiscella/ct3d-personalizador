# -*- coding: utf-8 -*-
"""Las tres canillas abiertas del motor que encontró la auditoría del 25-sep-2026.

1. **MOT-09 / SEG-06 — actividades pagas gratis.** `POST /act/<token>/extras` le creía la
   lista `compradas` a cualquiera: con el link del cuaderno y un curl (sin cabecera Origin,
   que `_origin_ok` deja pasar) se sumaba cualquier actividad paga de cualquier grado. Ahora
   `compradas` sólo vale con la credencial de la tienda, igual que /herencia. Y el orden
   público de las muestras (`muestra-kydo-N`) ya no lo reordena cualquiera.
2. **SEG-07 — /tts.** Generaba voz paga de ElevenLabs para cualquier texto, sin tope de
   gasto. Ahora lo NUEVO tiene tope por IP y un presupuesto diario global; lo cacheado sale
   igual que siempre.
3. **SEG-08 — el 🚩.** Cada reporte mandaba un WhatsApp a Pablo, sin límite, aunque el
   archivo estuviera lleno y también desde las muestras públicas.

Lo que NO puede cambiar, y también se prueba acá: un cuaderno ya vendido conserva lo que
pagó aunque el que guarda no traiga credencial, el modo seño sigue guardando borradores
desde el navegador, y el panel de Kydo sigue pudiendo pasarle el orden a cada chico.
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

TEMA = "safari"


@pytest.fixture(autouse=True)
def _cupos_limpios():
    """Los topes viven en memoria del proceso: cada test arranca con los cupos vacíos."""
    servicio._RL.clear()
    yield
    servicio._RL.clear()


class _Salida(Exception):
    pass


def _handler(path="/", body=b"", headers=None):
    """El handler REAL con un pedido de juguete, sin levantar el server."""
    hs = {"Content-Length": str(len(body)), "User-Agent": "Chrome/126"}
    hs.update(headers or {})

    class Falso(servicio.Handler):
        def __init__(self):
            self.headers = hs
            self.path = path
            self.rfile = io.BytesIO(body)
            self.wfile = io.BytesIO()
            self.salida = {}
            self.client_address = ("203.0.113.9", 5555)

        def _json(self, code, obj):
            self.salida = {"code": code, "obj": obj}

        def send_response(self, c):
            self.salida = {"code": c}

        def send_header(self, *a):
            pass

        def end_headers(self):
            pass

        def log_error(self, *a):
            pass

    return Falso()


def _post(metodo, token, cuerpo, headers=None, sufijo=""):
    body = json.dumps(cuerpo).encode()
    h = _handler("/act/%s/%s" % (token, sufijo), body, headers)
    getattr(h, metodo)(token)
    return h.salida


CLAVE = {"X-API-Key": servicio.API_KEY}


# ══ 1. MOT-09 / SEG-06: `compradas` sólo con credencial ═══════════════════════════════

@pytest.fixture
def cuaderno_4to():
    """Un cuaderno de 4.º grado (edad 9) sin nada extra."""
    tok = "test-sin-canillas-extras"
    d = os.path.join(aw.ACT_DIR, tok)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    json.dump({"edad": "9", "menu": []},
              open(os.path.join(d, "data.json"), "w", encoding="utf-8"))
    yield tok
    shutil.rmtree(d, ignore_errors=True)


def _de_7mo():
    cat = aw.catalogo_actividades()
    return {"id": cat[7][0]["id"], "grado": 7}


def test_un_curl_sin_credencial_NO_se_regala_una_actividad_paga(cuaderno_4to):
    """EL AGUJERO. Un cuaderno de 4.º, un POST sin Origin ni clave diciendo «ésta la
    pagué» con una de 7.º: antes entraba como comprada, salteando el tope y el grado."""
    lejana = _de_7mo()
    r = _post("_act_extras_set", cuaderno_4to,
              {"items": [lejana], "compradas": [lejana]}, sufijo="extras")
    assert r["code"] == 200
    assert not any(x.get("origen") == "comprada" for x in r["obj"]["items"]), \
        "el motor le creyó al cliente que la había pagado"
    assert not any(x["id"] == lejana["id"] and x["grado"] == 7 for x in r["obj"]["items"])
    assert r["obj"].get("compradas_ignoradas") is True, \
        "sin la marca, la tienda no se entera de que su lista no valió"
    guardado = aw.extras_leer(cuaderno_4to)["items"]
    assert not any(x.get("origen") == "comprada" for x in guardado)


def test_la_tienda_con_su_clave_sigue_entregando_lo_pagado(cuaderno_4to):
    """El camino legítimo (tienda_pago al acreditarse el pago) no se puede cortar."""
    lejana = _de_7mo()
    r = _post("_act_extras_set", cuaderno_4to,
              {"items": [lejana], "compradas": [lejana]}, headers=CLAVE, sufijo="extras")
    assert r["code"] == 200
    assert [x["origen"] for x in r["obj"]["items"]] == ["comprada"]
    assert "compradas_ignoradas" not in r["obj"]


def test_lo_ya_pagado_no_se_pierde_si_guardan_sin_credencial(cuaderno_4to):
    """CUADERNOS YA VENDIDOS. Lo que entró pagado (con la clave de la tienda) lo recuerda el
    propio motor: si después alguien guarda los extras sin credencial —la pantalla del padre
    mientras la tienda todavía no manda la clave—, la comprada sigue ahí, como comprada."""
    lejana = _de_7mo()
    _post("_act_extras_set", cuaderno_4to,
          {"items": [lejana], "compradas": [lejana]}, headers=CLAVE, sufijo="extras")
    r = _post("_act_extras_set", cuaderno_4to,
              {"items": [lejana], "compradas": []}, sufijo="extras")
    assert [(x["id"], x["grado"], x["origen"]) for x in r["obj"]["items"]] == \
        [(lejana["id"], 7, "comprada")], "el padre pagó y el cuaderno se la sacó"


def test_sin_credencial_lo_gratis_dentro_del_tope_se_sigue_guardando(cuaderno_4to):
    """Lo que el padre puede elegir gratis no necesita clave: el tope lo pone el motor."""
    cat = aw.catalogo_actividades()
    de5 = [{"id": m["id"], "grado": 5} for m in cat[5] if m.get("categoria") == "lengua"]
    r = _post("_act_extras_set", cuaderno_4to, {"items": de5}, sufijo="extras")
    assert r["code"] == 200
    assert len(r["obj"]["items"]) == aw.EXTRAS_TOPE_ADYACENTE
    assert r["obj"]["items"][0]["origen"] == "escuela"


def test_compradas_con_basura_no_rompe(cuaderno_4to):
    """Antes un `grado` no numérico en `compradas` tiraba un 500."""
    r = _post("_act_extras_set", cuaderno_4to,
              {"items": [], "compradas": [{"id": "x", "grado": "siete"}, "nada"]},
              headers=CLAVE, sufijo="extras")
    assert r["code"] == 200


# ── /orden: la muestra pública no la reordena cualquiera ─────────────────────────────

@pytest.fixture(scope="module")
def muestra_y_privado():
    toks = ("muestra-kydo-test-canillas", "test-canillas-orden-privado")
    for t in toks:
        shutil.rmtree(os.path.join(aw.ACT_DIR, t), ignore_errors=True)
        aw.crear({"nombre": "Sofía", "edad": "9", "escolar_on": True}, TEMA, token=t)
    yield toks
    for t in toks:
        shutil.rmtree(os.path.join(aw.ACT_DIR, t), ignore_errors=True)


def _ids(token):
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    return [m["id"] for m in d["menu"]]


def _orden(token):
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    return d.get("orden_seno")


def test_nadie_reordena_la_muestra_publica_sin_credencial(muestra_y_privado):
    """El orden SIN curso de `muestra-kydo-N` es el que ve cada familia que prueba."""
    muestra, _ = muestra_y_privado
    antes = _orden(muestra)
    ids = list(reversed(_ids(muestra)))[:4]
    r = _post("_act_orden_set", muestra, {"ids": ids}, sufijo="orden")
    assert r["code"] == 403
    assert _orden(muestra) == antes, "se reordenó la muestra que ve todo el mundo"
    # un curso que `_curso_sano` descarta cae en el mismo camino: tampoco pasa
    r = _post("_act_orden_set", muestra, {"ids": ids, "curso": "<<no>>"}, sufijo="orden")
    assert r["code"] == 403 and _orden(muestra) == antes


def test_el_modo_seno_sigue_guardando_su_borrador_en_la_muestra(muestra_y_privado):
    """El navegador de la seño guarda con `curso`: eso no se puede cortar."""
    muestra, _ = muestra_y_privado
    ids = _ids(muestra)[:3]
    r = _post("_act_orden_set", muestra, {"ids": ids, "curso": "4A"}, sufijo="orden")
    assert r["code"] == 200 and aw.orden_seno_leer(muestra, "4A") == ids


def test_con_credencial_la_muestra_si_se_ordena(muestra_y_privado):
    muestra, _ = muestra_y_privado
    ids = _ids(muestra)[:2]
    r = _post("_act_orden_set", muestra, {"ids": ids}, headers=CLAVE, sufijo="orden")
    assert r["code"] == 200 and _orden(muestra) == ids


def test_el_panel_de_kydo_sigue_pasandole_el_orden_a_cada_chico(muestra_y_privado):
    """`kydo/web.py` manda el orden a los cuadernos de los alumnos sin clave: un cuaderno
    privado lo sigue aceptando (el que tiene el link es el dueño)."""
    _, privado = muestra_y_privado
    ids = _ids(privado)[:3]
    r = _post("_act_orden_set", privado, {"ids": ids}, sufijo="orden")
    assert r["code"] == 200 and _orden(privado) == ids


# ══ 2. SEG-07: /tts con tope de gasto ═════════════════════════════════════════════════

@pytest.fixture
def tts(tmp_path, monkeypatch):
    """/tts contra un caché vacío en tmp y un ElevenLabs de mentira que cuenta llamadas."""
    import audiolibro
    llamadas = []
    monkeypatch.setattr(aw, "BASEDIR", str(tmp_path))
    monkeypatch.setattr(audiolibro, "_tts_elevenlabs",
                        lambda texto, voice_id=None: llamadas.append(texto) or b"ID3mp3")
    return llamadas


def _tts(texto, ip="198.51.100.7", headers=None):
    hs = {"CF-Connecting-IP": ip}
    hs.update(headers or {})
    h = _handler("/tts?t=x", b"", hs)
    h._tts_dinamico(texto)
    return h.salida.get("code")


def test_tts_no_genera_voz_nueva_pasado_el_tope_diario(tts, monkeypatch):
    """EL AGUJERO. Sin tope, cualquiera vaciaba el saldo de ElevenLabs pidiendo textos
    inventados. Pasado el presupuesto del día: 429 y ElevenLabs ni se entera."""
    monkeypatch.setattr(servicio, "TTS_TOPE_DIARIO", 30)
    avisos = []
    import notificaciones
    monkeypatch.setattr(notificaciones, "notif_emit", lambda *a, **k: avisos.append((a, k)))
    assert _tts("Contá los patitos") == 200                  # 17 caracteres: entra
    assert _tts("Ahora contá las jirafas del safari") == 429  # se pasaría del tope
    assert len(tts) == 1, "se llamó a ElevenLabs pasado el tope"
    assert avisos and avisos[0][0][0] == "health", "Pablo no se entera de que se cortó la voz"
    assert avisos[0][1].get("cooldown_h") and avisos[0][1].get("ref_id"), \
        "sin dedup, el aviso del tope se volvería él mismo una canilla"


def test_tts_lo_cacheado_sale_aunque_se_haya_llegado_al_tope(tts, monkeypatch):
    """Lo ya generado no cuesta nada: los chicos lo siguen escuchando."""
    assert _tts("Muy bien") == 200
    monkeypatch.setattr(servicio, "TTS_TOPE_DIARIO", 0)
    assert _tts("Muy bien") == 200
    assert len(tts) == 1


def test_tts_tope_por_ip_para_la_voz_nueva(tts, monkeypatch):
    monkeypatch.setattr(servicio, "TTS_NUEVOS_IP_HORA", 2)
    assert _tts("uno") == 200 and _tts("dos") == 200
    assert _tts("tres") == 429, "una sola IP puede pedir voz nueva sin freno"
    assert _tts("cuatro", ip="198.51.100.8") == 200, "el tope de una IP frena a las demás"
    assert _tts("uno") == 200, "lo ya cacheado no cuenta contra el tope por IP"
    assert len(tts) == 3


def test_tts_el_gasto_sobrevive_a_un_reinicio(tts, monkeypatch, tmp_path):
    """El contador va a disco: reiniciar el motor no puede regalar otro día de cupo."""
    monkeypatch.setattr(servicio, "TTS_TOPE_DIARIO", 20)
    assert _tts("quince letras!!") == 200
    g = json.load(open(os.path.join(str(tmp_path), "audio_dinamico", "_gasto_tts.json")))
    assert g["caracteres"] >= 15
    servicio._RL.clear()                                   # «reinicio»
    assert _tts("otras quince!!!") == 429


# ══ 3. SEG-08: el 🚩 no es una canilla de WhatsApp ════════════════════════════════════

def _reportar(token, cuerpo=None, ip="192.0.2.44"):
    avisos = []
    import notificaciones
    orig = notificaciones.notif_emit
    notificaciones.notif_emit = lambda *a, **k: avisos.append((a, k))
    try:
        r = _post("_act_reporte", token, cuerpo or {"motivo": "respuesta", "juego": "tablas"},
                  headers={"CF-Connecting-IP": ip}, sufijo="reporte")
    finally:
        notificaciones.notif_emit = orig
    return r, avisos


@pytest.fixture
def tok_reporte():
    toks = ["test-canillas-reporte", "muestra-kydo-test-rep", "demo-test-rep"]
    for t in toks:
        os.makedirs(os.path.join(aw.ACT_DIR, t), exist_ok=True)
    yield toks
    for t in toks:
        shutil.rmtree(os.path.join(aw.ACT_DIR, t), ignore_errors=True)


def test_reporte_con_archivo_lleno_no_avisa(tok_reporte):
    """Antes el aviso salía aunque el archivo estuviera lleno: el tope de 2 MB no frenaba
    nada del lado del teléfono."""
    p = os.path.join(aw.ACT_DIR, tok_reporte[0], "reportes.jsonl")
    with open(p, "w") as f:
        f.write("x" * (2 * 1024 * 1024 + 10))
    r, avisos = _reportar(tok_reporte[0])
    assert r["obj"]["ok"] is False
    assert avisos == [], "avisó un reporte que ni se guardó"


def test_reporte_de_un_cuaderno_vendido_avisa_con_tope_diario(tok_reporte):
    todos = []
    for i in range(servicio.REPORTE_TOPE_AVISOS_TOKEN + 3):
        r, avisos = _reportar(tok_reporte[0], {"motivo": "otro", "juego": "j%d" % i},
                              ip="192.0.2.%d" % (i + 1))
        assert r["code"] == 200 and r["obj"]["ok"] is True, "el reporte se tiene que guardar"
        todos += avisos
    assert len(todos) == servicio.REPORTE_TOPE_AVISOS_TOKEN
    lineas = open(os.path.join(aw.ACT_DIR, tok_reporte[0], "reportes.jsonl")).readlines()
    assert len(lineas) == servicio.REPORTE_TOPE_AVISOS_TOKEN + 3, "se perdió un reporte"


def test_reporte_va_con_dedup(tok_reporte):
    """Sin `ref_id` y `cooldown_h`, el dedup de `notif_emit` no corre nunca."""
    _, avisos = _reportar(tok_reporte[0])
    kw = avisos[0][1]
    assert kw.get("cooldown_h") and tok_reporte[0] in (kw.get("ref_id") or "")


def test_las_muestras_publicas_casi_no_avisan(tok_reporte):
    """`muestra-kydo-N` y `demo-*` los abre cualquiera: sus reportes se guardan, pero
    entre todas avisan como mucho REPORTE_TOPE_AVISOS_MUESTRA por día."""
    todos = []
    for i in range(12):
        tok = tok_reporte[1 + i % 2]
        r, avisos = _reportar(tok, {"motivo": "roto", "juego": "j%d" % i},
                              ip="192.0.2.%d" % (i + 1))
        assert r["obj"]["ok"] is True
        todos += avisos
    assert len(todos) == servicio.REPORTE_TOPE_AVISOS_MUESTRA
    assert servicio.REPORTE_TOPE_AVISOS_MUESTRA <= 3


def test_reporte_tope_por_ip(tok_reporte):
    """Una familia reporta uno, dos, tres errores; diez por hora desde una IP ya no."""
    for _ in range(servicio.REPORTE_TOPE_IP_HORA):
        r, _a = _reportar(tok_reporte[0])
        assert r["code"] == 200
    r, avisos = _reportar(tok_reporte[0])
    assert r["code"] == 429 and avisos == []
    lineas = open(os.path.join(aw.ACT_DIR, tok_reporte[0], "reportes.jsonl")).readlines()
    assert len(lineas) == servicio.REPORTE_TOPE_IP_HORA, "pasado el tope igual escribió"


def test_el_whatsapp_no_lleva_links_del_que_reporta(tok_reporte):
    """El detalle es texto libre y llega al teléfono de Pablo con cara de reporte de una
    familia. En el archivo queda tal cual; en el WhatsApp se desarman los links."""
    r, avisos = _reportar(tok_reporte[0], {
        "motivo": "otro", "juego": "sopa",
        "detalle": "entrá a https://banco-falso.example/login o a pagos-kydo.com.ar/x ya"})
    wa = avisos[0][1]["wa_texto"]
    assert "https://" not in wa and "pagos-kydo.com.ar" not in wa and "[link]" in wa
    rec = json.loads(open(os.path.join(aw.ACT_DIR, tok_reporte[0],
                                       "reportes.jsonl")).readlines()[-1])
    assert "https://banco-falso.example/login" in rec["detalle"]


def test_el_whatsapp_tampoco_lleva_links_de_otros_dominios(tok_reporte):
    """La primera versión desarmaba sólo una lista cerrada de terminaciones (.com, .ar, .ly…):
    `evil.ru/pago` o `bit.do/x` llegaban al WhatsApp como link tocable (25-sep-2026, revisión
    adversarial de SEG-08). Hay miles de dominios de primer nivel; lo que se desarma es la
    forma de dominio, no una lista."""
    r, avisos = _reportar(tok_reporte[0], {
        "motivo": "otro", "juego": "sopa",
        "detalle": "pagá acá evil.ru/pago o bit.do/x o kydo.shop, 3.5 está mal"})
    wa = avisos[0][1]["wa_texto"]
    for link in ("evil.ru", "bit.do", "kydo.shop"):
        assert link not in wa, "llegó un link tocable al WhatsApp: %s" % link
    assert "3.5 está mal" in wa, "se comió un número decimal que no es un link"


def test_el_titulo_del_reporte_tampoco_lleva_links(tok_reporte):
    """`titulo` y `juego` también los manda el navegador —o un curl— y encabezan el aviso
    («🚩 <titulo>»). Desarmar sólo el detalle dejaba el link en la primera línea
    (25-sep-2026)."""
    r, avisos = _reportar(tok_reporte[0], {
        "motivo": "otro", "titulo": "Reclamá tu premio en https://premio-kydo.example/x",
        "juego": "entrá a kydo-premios.shop"})
    kw = avisos[0][1]
    for campo in ("wa_texto", "titulo"):
        assert "https://" not in kw[campo] and "premio-kydo.example" not in kw[campo], campo
    rec = json.loads(open(os.path.join(aw.ACT_DIR, tok_reporte[0],
                                       "reportes.jsonl")).readlines()[-1])
    assert "https://premio-kydo.example/x" in rec["titulo"], "en el archivo va tal cual"
