"""El link deja de ser la llave: la llave es el mail.

POR QUÉ
───────
19-ago-2026. Los productos web se entregan como una URL con token: **el que tiene el
link, entra**. Para Mercado Libre alcanzaba (se lo mandamos a una persona por mensaje),
pero en Etsy el comprador se BAJA el archivo de entrega, y ese archivo se reenvía, se
sube a un grupo o se revende.

Pedido de Pablo, textual: *«Tiene que haber alguna forma asociada al mail. Si se loguea
en casatridimensional tiene acceso y no otros»*.

LO QUE ESTE ARCHIVO CUIDA, EN ORDEN DE IMPORTANCIA
──────────────────────────────────────────────────
1. **Que los links YA VENDIDOS sigan abriendo.** Un candado para todos rompe de golpe
   todo lo que factura hoy. El candado es opt-in: sin dueño anotado, se abre solo.
2. **Que el candado no tenga ventana.** El primer instinto es proteger el HTML; pero el
   producto son el `data.json` y los `p*.jpg`, que se piden aparte. Si sólo se cierra la
   puerta, alcanza con pedir los archivos derecho.
3. **Que Cloudflare no lo desarme.** El borde cachea `.jpg` por extensión, sin regla
   ninguna: con `Cache-Control: public`, la primera visita del dueño deja las imágenes
   servidas para cualquiera, sin volver a pasar por el motor. El candado más prolijo del
   mundo no sirve si el CDN de adelante contesta antes.
4. **Que la firma se valide de verdad**, no que la cookie exista. El resto del motor
   miraba `"ct3d_cliente=" in cookie` — pero eso decidía un banner, no un acceso.
5. **Que el ID token de Google sea PARA NOSOTROS.** Google verifica firma y vencimiento;
   lo único que Google no puede saber es para qué app se emitió. Sin comparar el `aud`,
   un token de cualquier otra app abre la puerta.
6. **Que el mail no se filtre.** Ni al `data.json` (lo lee el navegador), ni a la página
   de login (la ve cualquiera que tenga el link), ni por el endpoint de login.

CÓMO SE PRUEBA
──────────────
Levantando el servidor de verdad y pidiéndole las URLs. Los tests de rutas que ya había
en este repo leen el código fuente y comprueban el ORDEN de las líneas; hoy mismo un
test así se quedó en verde con el código desconectado. Un control de acceso se prueba
pidiéndole al servidor que te deje pasar, y viendo que no te deje.
"""
import http.client
import json
import os
import shutil
import sys
import tempfile
import threading
import time
from http.server import ThreadingHTTPServer

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import acceso  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETO_FALSO = "secreto-de-test-no-real-largo-para-hs256"


# ── el secreto, sin tocar el de producción ───────────────────────────────────

@pytest.fixture
def config_falso(tmp_path, monkeypatch):
    """Un config.json de mentira. Sin esto, los tests leerían el secreto REAL de
    producción — y un test que depende de un secreto de producción es un test que se
    cae en cualquier otra máquina, además de una mala idea."""
    p = tmp_path / "config.json"
    p.write_text(json.dumps({"session_secret": SECRETO_FALSO}))
    monkeypatch.setattr(acceso, "CONFIG_TIENDA", str(p))
    return str(p)


def _cookie_tienda(email, secreto=None, tipo=None):
    """Arma una cookie como la que emite la tienda (tienda_auth_cliente._token)."""
    import datetime as dt
    import hashlib
    import hmac

    import jwt as _jwt
    base = secreto or SECRETO_FALSO
    derivado = hmac.new(base.encode(), b"cliente", hashlib.sha256).hexdigest()
    ahora = dt.datetime.now(dt.timezone.utc)
    payload = {"email": email, "iat": int(ahora.timestamp()),
               "exp": int((ahora + dt.timedelta(days=30)).timestamp())}
    if tipo:
        payload["tipo"] = tipo
    return _jwt.encode(payload, derivado, algorithm="HS256")


# ── 1. el candado es opt-in ──────────────────────────────────────────────────

def test_un_token_SIN_dueño_sigue_abriendo_solo(config_falso):
    """EL test que más importa de este archivo. Todo lo que se vendió hasta hoy son
    links sin dueño; si el candado aplicara a todos, cada cliente de Mercado Libre se
    queda afuera de lo que ya pagó — un incendio, no un bug."""
    ok, dueño = acceso.puede_abrir({"tema": "safari", "nombre": "Emma"}, "")
    assert ok is True
    assert dueño is None


def test_un_token_CON_dueño_no_abre_sin_sesion(config_falso):
    ok, dueño = acceso.puede_abrir({"dueño": "ana@gmail.com"}, "")
    assert ok is False
    assert dueño == "ana@gmail.com"


def test_el_dueño_abre_su_propio_link(config_falso):
    c = "ct3d_acceso=%s" % acceso.sesion_crear("ana@gmail.com")
    ok, _ = acceso.puede_abrir({"dueño": "ana@gmail.com"}, c)
    assert ok is True


def test_otra_persona_logueada_NO_abre_el_link_ajeno(config_falso):
    """El caso que se compra el problema: alguien con cuenta, y con el link — porque se
    lo pasaron. Tener sesión no es tener derecho a ESTE link."""
    c = "ct3d_acceso=%s" % acceso.sesion_crear("otro@gmail.com")
    ok, _ = acceso.puede_abrir({"dueño": "ana@gmail.com"}, c)
    assert ok is False


def test_el_mail_se_compara_normalizado(config_falso):
    """Etsy manda «Ana@Gmail.com» y Google devuelve «ana@gmail.com». Sin normalizar,
    el dueño no puede abrir su propio link y no hay forma de que se dé cuenta por qué."""
    c = "ct3d_acceso=%s" % acceso.sesion_crear("ANA@Gmail.COM")
    ok, _ = acceso.puede_abrir({"dueño": " ana@gmail.com "}, c)
    assert ok is True


# ── 2. la cookie de la tienda se valida de verdad ────────────────────────────

def test_la_cuenta_de_la_tienda_tambien_abre(config_falso):
    """La segunda puerta: quien ya compró en casatridimensional.com.ar tiene la cookie
    del dominio padre, que llega también a kit.* — no tiene que entrar con Google."""
    c = "ct3d_cliente=%s" % _cookie_tienda("ana@gmail.com")
    assert acceso.email_de_la_tienda(c) == "ana@gmail.com"
    ok, _ = acceso.puede_abrir({"dueño": "ana@gmail.com"}, c)
    assert ok is True


def test_una_cookie_firmada_con_OTRO_secreto_no_vale(config_falso):
    """Que la cookie EXISTA no es que sea válida. El resto del motor mira
    `"ct3d_cliente=" in cookie` porque ahí sólo decide mostrar un banner; acá decide un
    acceso, y una cookie que cualquiera puede escribir a mano no decide nada."""
    c = "ct3d_cliente=%s" % _cookie_tienda("ana@gmail.com", secreto="otro-secreto")
    assert acceso.email_de_la_tienda(c) is None
    ok, _ = acceso.puede_abrir({"dueño": "ana@gmail.com"}, c)
    assert ok is False


def test_una_cookie_inventada_no_vale(config_falso):
    assert acceso.email_de_la_tienda("ct3d_cliente=ana@gmail.com") is None
    assert acceso.email_de_la_tienda("ct3d_cliente=") is None
    assert acceso.email_de_la_tienda("") is None


def test_el_token_de_RESET_de_contraseña_no_es_una_sesion(config_falso):
    """El backend emite tokens con `tipo=reset` para «olvidé mi contraseña». Ese token
    llega por mail y sirve para UNA cosa; si valiera como sesión, quien intercepte ese
    mail entra a todo. El backend hace esta distinción y acá se respeta igual."""
    c = "ct3d_cliente=%s" % _cookie_tienda("ana@gmail.com", tipo="reset")
    assert acceso.email_de_la_tienda(c) is None


def test_la_derivacion_del_secreto_es_la_MISMA_que_la_del_backend():
    """El código está COPIADO del backend a propósito (regla de Pablo: los sistemas no
    comparten código). El riesgo de copiar es que allá cambie y acá no: si eso pasa, la
    cookie de un cliente real deja de validar y nadie se entera hasta que un comprador
    no puede entrar. Este test lee el archivo real y compara."""
    p = "/opt/ct3d/backend/tienda_auth_cliente.py"
    if not os.path.isfile(p):
        pytest.skip("el backend no está en esta máquina")
    fuente = open(p, encoding="utf-8").read()
    assert 'hmac.new(base.encode(), b"cliente", hashlib.sha256).hexdigest()' in fuente, (
        "el backend cambió cómo deriva el secreto de la sesión de cliente. `acceso.py` "
        "tiene la copia vieja y va a rechazar cookies buenas: actualizá los dos.")
    assert acceso.COOKIE_TIENDA in fuente


# ── 3. Google ────────────────────────────────────────────────────────────────

def _respuesta_google(**campos):
    d = {"aud": acceso.GOOGLE_CLIENT_ID, "iss": "https://accounts.google.com",
         "email": "ana@gmail.com", "email_verified": "true",
         "exp": str(int(time.time()) + 600)}
    d.update(campos)
    return lambda url: json.dumps(d).encode()


def test_google_devuelve_el_mail_verificado():
    assert acceso.email_de_google("token.de.google",
                                  _abrir=_respuesta_google()) == "ana@gmail.com"


def test_un_id_token_emitido_para_OTRA_app_no_entra():
    """Lo único que Google no puede chequear por nosotros. Cualquiera puede conseguir un
    ID token válido —de su propia app— y mandarlo acá: sin comparar el `aud`, ese token
    entra, porque la firma de Google es legítima. Es el error clásico de este flujo."""
    assert acceso.email_de_google("t", _abrir=_respuesta_google(
        aud="999-otra-app.apps.googleusercontent.com")) is None


def test_un_mail_sin_verificar_no_entra():
    """Google deja tener una cuenta con un mail no verificado. Si entrara, alguien se
    hace una cuenta con el mail del comprador y le abre el link."""
    assert acceso.email_de_google("t",
                                  _abrir=_respuesta_google(email_verified="false")) is None


def test_un_id_token_vencido_no_entra():
    assert acceso.email_de_google("t", _abrir=_respuesta_google(
        exp=str(int(time.time()) - 10))) is None


def test_un_emisor_que_no_es_google_no_entra():
    assert acceso.email_de_google("t",
                                  _abrir=_respuesta_google(iss="https://malo.com")) is None


def test_si_google_no_contesta_no_entra():
    """Falla CERRADO. Que se caiga la red no puede ser una forma de saltear la puerta."""
    def revienta(url):
        raise OSError("sin red")
    assert acceso.email_de_google("t", _abrir=revienta) is None


def test_basura_como_token_no_entra():
    assert acceso.email_de_google("", _abrir=_respuesta_google()) is None
    assert acceso.email_de_google(None, _abrir=_respuesta_google()) is None
    assert acceso.email_de_google("x" * 9000, _abrir=_respuesta_google()) is None


# ── 4. la página de login no filtra ni redirige a cualquier lado ─────────────

def test_la_pagina_de_login_NO_muestra_el_mail_entero(config_falso):
    """La ve cualquiera que tenga el link — incluido quien no debería tenerlo. Decir
    «este link es de ana.gonzalez@gmail.com» le regala el mail del comprador a quien
    entró de prepo. La pista alcanza para que el dueño se reconozca."""
    html = acceso.pagina_login("/armar/tok/", "es", "anabelen@gmail.com")
    assert "anabelen@gmail.com" not in html
    assert "@gmail.com" in html          # el dominio sí, para que se reconozca
    assert html.count("a•") == 1    # la inicial y los puntitos


def test_la_pista_no_delata_CUANTAS_letras_tiene_el_mail():
    """Los puntitos son un número fijo, no uno por letra.

    Con un puntito por letra, `pablofiscella@gmail.com` salía
    «p••••••••••••@gmail.com»: (a) no entraba en la caja y se partía a mitad de
    «gmail.com» —se vio en la captura de la página, no en el código— y (b) le contaba el
    largo del mail del comprador a cualquiera que tuviera el link. Lo segundo es poco,
    pero es gratis no darlo."""
    corto = acceso.pista_de_mail("ana@gmail.com")
    largo = acceso.pista_de_mail("pablofiscella@gmail.com")
    assert corto.count("•") == largo.count("•"), (
        "la cantidad de puntitos revela el largo del usuario")
    assert len(largo) <= 20, "la pista no entra en la caja y se parte a mitad de palabra"
    assert largo.startswith("p") and largo.endswith("@gmail.com")


def test_la_pagina_de_login_habla_los_dos_idiomas(config_falso):
    assert "This link is yours" in acceso.pagina_login("/x/", "en")
    assert "Este link es tuyo" in acceso.pagina_login("/x/", "es")


def test_no_queda_ningun_marcador_sin_reemplazar(config_falso):
    """Un `{{VOLVER}}` sin reemplazar no rompe la página: la deja andando y sin poder
    volver a ningún lado. Los errores que no se ven son los que llegan al comprador."""
    for lang in ("es", "en"):
        assert "{{" not in acceso.pagina_login("/armar/tok/", lang, "ana@gmail.com")


def test_no_se_puede_usar_la_puerta_como_redirector_a_otro_sitio(config_falso):
    """Sin esto: `/armar/x/` te manda a la puerta, entrás con Google —confiando en el
    dominio— y salís disparado a donde quiera el que armó el link."""
    for malo in ("https://malo.com/x", "//malo.com", "javascript:alert(1)",
                 "http://malo.com", "\\\\malo.com"):
        assert acceso._volver_seguro(malo) == "/", malo
    assert acceso._volver_seguro("/armar/tok/") == "/armar/tok/"


def test_lo_que_viene_de_la_URL_no_se_mete_como_codigo_en_la_pagina(config_falso):
    """Los valores van en atributos `data-*` y no interpolados adentro del <script>:
    dentro de un <script> las entidades HTML no se decodifican, así que escapar las
    comillas ahí no protege — deja el valor roto y la seguridad colgada de un
    razonamiento sutil sobre dos contextos de escape distintos."""
    html = acceso.pagina_login("/x</script><img src=x onerror=alert(1)>", "es")
    assert "<img" not in html
    assert html.count("</script>") == 2      # el de Google y el propio, ninguno más
    assert "&lt;/script&gt;" in html


# ── 5. la ruta de verdad, con el servidor levantado ──────────────────────────

@pytest.fixture
def servidor(monkeypatch, tmp_path):
    """El servicio andando en un puerto libre, con su propio directorio de tokens.

    Se levanta de verdad porque es la única forma de probar un control de acceso: los
    tests de ruta que ya hay en este repo leen el código fuente y comprueban el orden de
    las líneas — hoy mismo uno así se quedó en verde con el código desconectado."""
    import rompecabezas_web as rw
    import servicio

    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"session_secret": SECRETO_FALSO}))
    monkeypatch.setattr(acceso, "CONFIG_TIENDA", str(cfg))

    rompe = tmp_path / "rompe"
    rompe.mkdir()
    monkeypatch.setattr(rw, "ROMPE_DIR", str(rompe))

    srv = ThreadingHTTPServer(("127.0.0.1", 0), servicio.Handler)
    hilo = threading.Thread(target=srv.serve_forever, daemon=True)
    hilo.start()
    yield srv.server_address[1], str(rompe)
    srv.shutdown()
    srv.server_close()


def _token_falso(rompe_dir, token, dueño=None):
    """Un token con los archivos mínimos: el candado se decide por el manifest, así que
    no hace falta generar el rompecabezas entero (que tarda)."""
    d = os.path.join(rompe_dir, token)
    os.makedirs(d, exist_ok=True)
    man = {"tema": "safari", "nombre": "Emma", "titulo": "x",
           "creado": int(time.time()), "idioma": "en"}
    if dueño:
        man["dueño"] = dueño
    with open(os.path.join(d, "manifest.json"), "w") as f:
        json.dump(man, f)
    with open(os.path.join(d, "data.json"), "w") as f:
        json.dump({"v": 1, "tema": "safari", "puzzles": []}, f)
    with open(os.path.join(d, "p0.jpg"), "wb") as f:
        f.write(b"\xff\xd8\xff\xe0jpeg-de-mentira")
    return d


def _pedir(puerto, ruta, cookie=None):
    c = http.client.HTTPConnection("127.0.0.1", puerto, timeout=10)
    c.request("GET", ruta, headers=({"Cookie": cookie} if cookie else {}))
    r = c.getresponse()
    cuerpo = r.read()
    est, hdrs = r.status, dict(r.getheaders())
    c.close()
    return est, hdrs, cuerpo


def test_la_RUTA_deja_pasar_un_token_sin_dueño(servidor):
    puerto, rompe = servidor
    _token_falso(rompe, "libre123")
    est, _, _ = _pedir(puerto, "/armar/libre123/data.json")
    assert est == 200, "un link ya vendido dejó de abrir"


def test_la_RUTA_corta_los_ARCHIVOS_de_un_token_con_dueño(servidor):
    """El agujero que hay que no dejar: proteger el HTML y dejar los archivos sueltos.
    El `data.json` y los `p*.jpg` SON el producto — quien los baja tiene todo, y no
    necesita la página para nada."""
    puerto, rompe = servidor
    _token_falso(rompe, "conduenio", dueño="ana@gmail.com")
    for arch in ("data.json", "p0.jpg"):
        est, _, _ = _pedir(puerto, "/armar/conduenio/%s" % arch)
        assert est == 403, "%s se bajó sin cuenta" % arch


def test_la_RUTA_muestra_la_puerta_en_la_pagina_y_no_el_juego(servidor):
    puerto, rompe = servidor
    _token_falso(rompe, "conduenio2", dueño="ana@gmail.com")
    est, hdrs, cuerpo = _pedir(puerto, "/armar/conduenio2/")
    assert est == 403
    assert hdrs.get("Content-Type", "").startswith("text/html")
    txt = cuerpo.decode("utf-8")
    assert "This link is yours" in txt, "la puerta tiene que hablar el idioma del token"
    assert "ana@gmail.com" not in txt


def test_la_RUTA_deja_entrar_al_dueño(servidor):
    puerto, rompe = servidor
    _token_falso(rompe, "conduenio3", dueño="ana@gmail.com")
    c = "ct3d_acceso=%s" % acceso.sesion_crear("ana@gmail.com")
    est, _, _ = _pedir(puerto, "/armar/conduenio3/data.json", cookie=c)
    assert est == 200


def test_la_RUTA_no_deja_que_CLOUDFLARE_guarde_lo_protegido(servidor):
    """El candado más prolijo no sirve si el CDN contesta antes. Cloudflare cachea .jpg
    por extensión sin ninguna regla: con `public`, la primera visita del dueño deja las
    imágenes servidas en el borde para cualquiera que tenga el link."""
    puerto, rompe = servidor
    _token_falso(rompe, "concandado", dueño="ana@gmail.com")
    _token_falso(rompe, "sincandado")
    c = "ct3d_acceso=%s" % acceso.sesion_crear("ana@gmail.com")

    # El 200 se exige ANTES de mirar el header, y no es un detalle: la primera vez que
    # se escribió esto el token era de 3 letras, el servidor contestaba 404 —sin
    # Cache-Control— y el «no está cacheado» daba en verde sin haber servido nada.
    est, hdrs, _ = _pedir(puerto, "/armar/concandado/p0.jpg", cookie=c)
    assert est == 200, "no se sirvió el archivo, así que el header no prueba nada"
    assert "public" not in hdrs.get("Cache-Control", ""), (
        "un archivo con dueño se estaría cacheando en el borde")
    assert "private" in hdrs.get("Cache-Control", "")

    est2, hdrs2, _ = _pedir(puerto, "/armar/sincandado/p0.jpg")
    assert est2 == 200
    assert "public" in hdrs2.get("Cache-Control", ""), (
        "los links sin dueño tienen que seguir cacheándose: son la mayoría del tráfico")


# ── 6. el mail no se filtra al navegador ─────────────────────────────────────

def test_el_mail_del_comprador_NO_va_al_data_json(tmp_path, monkeypatch):
    """El `data.json` se lo sirve el motor al navegador para que lo lea el player: todo
    lo que se escriba ahí es público. El dueño va al manifest, que no sale nunca."""
    import rompecabezas_web as rw
    monkeypatch.setattr(rw, "ROMPE_DIR", str(tmp_path))
    tema = "safari"
    if not os.path.isdir(os.path.join(RAIZ, "temas", tema)):
        pytest.skip("no está el tema safari en esta copia")
    tok = rw.crear({"nombre": "Emma", "idioma": "en", "dueño": "ana@gmail.com"},
                   tema, token="privacidad1")
    d = os.path.join(str(tmp_path), tok)
    data = open(os.path.join(d, "data.json"), encoding="utf-8").read()
    assert "ana@gmail.com" not in data, "el mail del comprador se filtró al navegador"
    man = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
    assert man["dueño"] == "ana@gmail.com", "el candado no quedó anotado"


def test_sin_dueño_el_manifest_no_lleva_candado(tmp_path, monkeypatch):
    import rompecabezas_web as rw
    monkeypatch.setattr(rw, "ROMPE_DIR", str(tmp_path))
    if not os.path.isdir(os.path.join(RAIZ, "temas", "safari")):
        pytest.skip("no está el tema safari en esta copia")
    tok = rw.crear({"nombre": "Emma"}, "safari", token="sincandado1")
    man = json.load(open(os.path.join(str(tmp_path), tok, "manifest.json"),
                         encoding="utf-8"))
    assert "dueño" not in man


# ── 7. la entrega del rompecabezas web ───────────────────────────────────────
#
# La diferencia con el kit manda todo: el kit se BAJA (una vez bajado ya es del
# comprador y no hay nada que cuidar), esto es un LINK VIVO que se juega en nuestro
# servidor para siempre. Un link vivo se reenvía y sigue andando: no se gasta. Por eso
# el mail se pide ANTES de generar y el rompecabezas nace a nombre de alguien.

def _post(puerto, ruta, cuerpo, cookie=None):
    h = {"Content-Type": "application/json"}
    if cookie:
        h["Cookie"] = cookie
    c = http.client.HTTPConnection("127.0.0.1", puerto, timeout=30)
    c.request("POST", ruta, body=json.dumps(cuerpo).encode(), headers=h)
    r = c.getresponse()
    est, datos = r.status, r.read()
    c.close()
    try:
        return est, json.loads(datos)
    except Exception:
        return est, {}


def test_SIN_cuenta_no_se_genera_NADA(servidor, monkeypatch):
    """EL test de este bloque. Si se generara primero y se pidiera la cuenta después,
    quedaría un link sin dueño ya entregado — y ése no se puede cerrar nunca más sin
    romperle el producto a quien pagó."""
    import etsy_pedidos
    import rompecabezas_web as rw
    puerto, rompe = servidor
    creados = []
    monkeypatch.setattr(rw, "crear", lambda *a, **k: creados.append(a) or "tok123456")
    monkeypatch.setattr(etsy_pedidos, "validar", lambda *a, **k: (True, {}, None))

    est, d = _post(puerto, "/etsy/generar-juego",
                   {"orden": "3210987654", "tema": "safari", "nombre": "Emma"})
    assert est == 401
    assert d.get("necesita_cuenta") is True
    assert not creados, "se generó el rompecabezas antes de saber de quién era"


def test_CON_cuenta_el_link_nace_a_nombre_del_comprador(servidor, monkeypatch):
    import etsy_pedidos
    import rompecabezas_web as rw
    puerto, rompe = servidor
    visto = {}

    def falso_crear(data, tema, token=None):
        visto.update(data)
        visto["tema"] = tema
        return "tok123456"
    monkeypatch.setattr(rw, "crear", falso_crear)
    monkeypatch.setattr(etsy_pedidos, "validar", lambda *a, **k: (True, {}, None))
    monkeypatch.setattr(etsy_pedidos, "registrar_canje", lambda *a, **k: 1)

    c = "ct3d_acceso=%s" % acceso.sesion_crear("ana@gmail.com")
    est, d = _post(puerto, "/etsy/generar-juego",
                   {"orden": "3210987654", "tema": "safari", "nombre": "Emma"}, cookie=c)
    assert est == 200, d
    assert visto.get("dueño") == "ana@gmail.com", "el link nació sin dueño"
    assert visto.get("idioma") == "en", "quien compra en Etsy compra en inglés"
    assert "/armar/tok123456/" in d.get("url", "")


def test_la_entrega_del_juego_pide_SU_producto(servidor, monkeypatch):
    """No alcanza con que la orden exista: tiene que ser de este producto. Es el mismo
    agujero que tenía el kit, y estrenarlo de nuevo en el producto nuevo sería peor."""
    import etsy_pedidos
    import rompecabezas_web as rw
    puerto, rompe = servidor
    pedido = {}

    def falso_validar(numero, shop_id=None, tipo=None):
        pedido["tipo"] = tipo
        return True, {}, None
    monkeypatch.setattr(etsy_pedidos, "validar", falso_validar)
    monkeypatch.setattr(etsy_pedidos, "registrar_canje", lambda *a, **k: 1)
    monkeypatch.setattr(rw, "crear", lambda *a, **k: "tok123456")

    c = "ct3d_acceso=%s" % acceso.sesion_crear("ana@gmail.com")
    _post(puerto, "/etsy/generar-juego",
          {"orden": "3210987654", "tema": "safari"}, cookie=c)
    assert pedido.get("tipo") == "rompecabezas-web"


def test_si_la_orden_no_sirve_no_se_genera(servidor, monkeypatch):
    import etsy_pedidos
    import rompecabezas_web as rw
    puerto, rompe = servidor
    creados = []
    monkeypatch.setattr(rw, "crear", lambda *a, **k: creados.append(1) or "tok123456")
    monkeypatch.setattr(etsy_pedidos, "validar",
                        lambda *a, **k: (False, None, "That order still shows as unpaid."))
    c = "ct3d_acceso=%s" % acceso.sesion_crear("ana@gmail.com")
    est, d = _post(puerto, "/etsy/generar-juego",
                   {"orden": "3210987654", "tema": "safari"}, cookie=c)
    assert est == 403
    assert not creados


def test_quien_soy_devuelve_la_pista_y_no_el_mail(servidor):
    """Esta respuesta la puede pedir cualquiera que tenga la página abierta — y el
    teléfono del adulto lo usa también el chico."""
    puerto, _ = servidor
    c = "ct3d_acceso=%s" % acceso.sesion_crear("anabelen@gmail.com")
    est, hdrs, cuerpo = _pedir(puerto, "/acceso/quien", cookie=c)
    assert est == 200
    d = json.loads(cuerpo)
    assert d["entrado"] is True
    assert "anabelen@gmail.com" not in cuerpo.decode()
    assert d["pista"].endswith("@gmail.com")

    est2, _, cuerpo2 = _pedir(puerto, "/acceso/quien")
    assert json.loads(cuerpo2)["entrado"] is False


def test_la_pagina_del_juego_dice_que_es_un_JUEGO_y_no_un_pdf(servidor):
    """Pablo, textual: «Pero se puede aclarar bien. No es solo el pdf si no web». El
    comprador de Etsy está acostumbrado a que «printable» sea un archivo: si abre esto
    esperando un PDF, la venta termina en un reclamo aunque el producto funcione."""
    puerto, _ = servidor
    est, _, cuerpo = _pedir(puerto, "/etsy/juego")
    assert est == 200
    txt = cuerpo.decode("utf-8")
    assert "{{CLIENT_ID}}" not in txt, "el client id no se inyectó"
    assert "838286795258" in txt or "googleusercontent" in txt
    bajo = txt.lower()
    assert "browser" in bajo, "no dice que se juega en el navegador"
    assert "nothing to print" in bajo, "no aclara que no se imprime"


def test_no_se_puede_martillar_la_entrega_probando_ordenes(servidor, monkeypatch):
    """Cada intento gasta una llamada a la API de Etsy, que tiene cuota diaria. Sin tope,
    alguien probando números inventados la quema — y el que se queda sin poder validar es
    el comprador de verdad, que ya pagó.

    El test pega desde 127.0.0.1 y `_rate_ok` exime el loopback (para no limitar a la
    tienda, que llama por ahí), así que se le da una IP de afuera a mano: si no, esto
    daría verde sin haber ejercido el límite ni una vez."""
    import etsy_pedidos
    import rompecabezas_web as rw
    import servicio
    puerto, _ = servidor
    monkeypatch.setattr(servicio.Handler, "_client_ip", lambda self: "203.0.113.7")
    llamadas = []

    def validar_espia(numero, shop_id=None, tipo=None):
        llamadas.append(numero)
        return False, None, "That order still shows as unpaid."
    monkeypatch.setattr(etsy_pedidos, "validar", validar_espia)
    monkeypatch.setattr(rw, "crear", lambda *a, **k: "tok123456")

    c = "ct3d_acceso=%s" % acceso.sesion_crear("ana@gmail.com")
    codigos = [_post(puerto, "/etsy/generar-juego",
                     {"orden": "321098765%d" % i, "tema": "safari"}, cookie=c)[0]
               for i in range(14)]
    assert 429 in codigos, "se pudo martillar la entrega sin tope"
    assert len(llamadas) <= 10, ("se le pegó a la API de Etsy %d veces" % len(llamadas))


def test_la_pagina_del_juego_respeta_la_tematica_que_trae_el_link():
    """El PDF que Etsy entrega lleva `?tema=safari`, y la página tiene que arrancar en esa.

    Sin esto la lista queda en la PRIMERA por orden alfabético —Camping— y el comprador de
    safari se lleva el rompecabezas equivocado, sin ninguna señal de que algo salió mal.
    Es un test de PARIDAD contra `etsy.html`, que ya lo hacía: la página del juego se
    escribió copiando aquélla y esta parte se quedó afuera. Sólo apareció mirando la
    página con un navegador — leyendo el código no se ve lo que falta.
    """
    kit = open(os.path.join(RAIZ, "etsy.html"), encoding="utf-8").read()
    juego = open(os.path.join(RAIZ, "etsy_juego.html"), encoding="utf-8").read()
    for pagina, nombre in ((kit, "etsy.html"), (juego, "etsy_juego.html")):
        assert "URLSearchParams" in pagina, "%s no lee los parámetros de la URL" % nombre
        assert 'get("tema")' in pagina, "%s no respeta el ?tema= del link" % nombre


def test_el_boton_de_google_habla_ingles():
    """Sin `locale`, Google dibuja el botón en el idioma del NAVEGADOR: en una página que
    está entera en inglés aparecía «Acceder con Google». El comprador de Etsy es de habla
    inglesa, pero el idioma de su navegador no tiene por qué serlo — y el nuestro tampoco,
    que es como se descubrió."""
    juego = open(os.path.join(RAIZ, "etsy_juego.html"), encoding="utf-8").read()
    i = juego.index("renderButton")
    assert 'locale: "en"' in juego[i:i + 300], (
        "el botón de Google va a salir en el idioma del navegador de quien mire")


# ── 8. el header que rompía el botón de Google ───────────────────────────────
#
# 20-ago-2026, encontrado abriendo la página con un navegador de verdad. El botón no
# funcionaba y Google decía «The given origin is not allowed for the given client ID»,
# que es EL MISMO mensaje que da un origen sin autorizar — así que la primera lectura
# fue «falta agregar el origen». Pero el origen estaba: una página de prueba servida en
# ese MISMO origen andaba bien.
#
# La diferencia eran los headers. El motor manda `Referrer-Policy: no-referrer` en todo,
# y GSI necesita que el navegador le diga a Google de qué origen viene. Sin Referer,
# Google no puede verificarlo y contesta lo mismo que si el origen estuviera prohibido.

def test_la_pagina_con_boton_de_google_permite_que_Google_vea_el_origen(servidor):
    puerto, _ = servidor
    _, hdrs, _ = _pedir(puerto, "/etsy/juego")
    rp = hdrs.get("Referrer-Policy", "")
    assert rp != "no-referrer", (
        "con `no-referrer` el botón de Google no funciona: Google no puede ver el origen "
        "y contesta que no está permitido, aunque lo esté")
    assert "strict-origin" in rp


def test_la_puerta_del_candado_tambien_lo_permite(servidor):
    """La pantalla de login también tiene botón de Google, y se sirve desde otra rama del
    código: si sólo se arreglara `/etsy/juego`, el comprador podría entrar a canjear pero
    no a abrir su propio link."""
    puerto, rompe = servidor
    _token_falso(rompe, "puertaref1", dueño="ana@gmail.com")
    est, hdrs, _ = _pedir(puerto, "/armar/puertaref1/")
    assert est == 403
    assert "strict-origin" in hdrs.get("Referrer-Policy", "")


def test_el_RESTO_del_motor_sigue_sin_mandar_referer(servidor):
    """EL contrapeso, y por qué el arreglo es por ruta y no global: los tokens viajan EN
    LA URL. Si `/armar/<token>/` mandara Referer, cualquier recurso externo que el player
    cargue se entera del link — que es justo lo que este trabajo vino a cerrar.

    Se mira una página con token y una respuesta común, porque el header lo pone
    `end_headers`, que es de TODAS las respuestas: un cambio ahí se escapa a todo el
    motor sin que nadie lo note."""
    puerto, rompe = servidor
    _token_falso(rompe, "sinreferer1")
    for ruta in ("/armar/sinreferer1/", "/armar/sinreferer1/data.json", "/health"):
        _, hdrs, _ = _pedir(puerto, ruta)
        assert hdrs.get("Referrer-Policy") == "no-referrer", (
            "%s dejó de proteger el token en la URL" % ruta)


def test_strict_origin_no_filtra_la_ruta_donde_vive_el_token():
    """Por qué `strict-origin` y no `no-referrer-when-downgrade`, que también arreglaría
    el botón: aquélla manda la URL ENTERA a destinos https, o sea el token. Ésta manda
    sólo el origen, siempre. Es un test de la decisión, no del código — está para que el
    día que alguien afloje este header sepa cuál era el límite."""
    import servicio
    fuente = open(os.path.join(RAIZ, "servicio.py"), encoding="utf-8").read()
    assert "no-referrer-when-downgrade" not in fuente, (
        "esa política manda la URL completa: filtraría el token del link")
    assert "unsafe-url" not in fuente
    assert '_ref_policy = "strict-origin"' in fuente


def test_EL_CICLO_COMPLETO_entrar_con_google_y_abrir_el_link(servidor, monkeypatch):
    """De punta a punta: Google verifica → el motor emite su cookie → esa cookie abre el
    link. Los otros tests arman la cookie a mano con `sesion_crear`; éste la toma de la
    respuesta HTTP real del endpoint de login.

    Por qué importa la diferencia: si `cookie_set` emitiera algo que `email_de_la_sesion`
    no sabe leer —otro nombre, otra derivación de secreto, un formato distinto— todos los
    demás tests seguirían en verde y ningún comprador podría entrar. Es la costura entre
    las dos mitades, y es justo donde nadie mira."""
    import acceso as acc
    import servicio
    puerto, rompe = servidor
    _token_falso(rompe, "ciclocompleto", dueño="ana@gmail.com")

    # sin cuenta: no pasa
    est, _, _ = _pedir(puerto, "/armar/ciclocompleto/data.json")
    assert est == 403

    # Google dice que sí (se intercepta la llamada a Google, no la lógica de acceso:
    # lo que se prueba es lo NUESTRO).
    monkeypatch.setattr(acc, "email_de_google", lambda *a, **k: "ana@gmail.com")
    c = http.client.HTTPConnection("127.0.0.1", puerto, timeout=20)
    c.request("POST", "/acceso/google",
              body=json.dumps({"credential": "lo-que-manda-el-boton"}).encode(),
              headers={"Content-Type": "application/json"})
    r = c.getresponse()
    cuerpo = json.loads(r.read())
    set_cookie = r.getheader("Set-Cookie") or ""
    c.close()

    assert r.status == 200 and cuerpo.get("ok") is True
    assert "ana@gmail.com" not in json.dumps(cuerpo), "devolvió el mail entero"
    assert cuerpo.get("pista", "").endswith("@gmail.com")

    # los atributos importan tanto como el valor: sin Domain del dominio padre la cookie
    # no viaja a kit.*, y sin HttpOnly la puede leer cualquier script de la página.
    assert "HttpOnly" in set_cookie and "Secure" in set_cookie
    assert "Domain=.casatridimensional.com.ar" in set_cookie
    assert "SameSite=Lax" in set_cookie, (
        "el link llega de un PDF o un mail: con SameSite=Strict la cookie no viaja en "
        "esa primera navegación y el dueño vería la puerta otra vez")

    # y ahora sí: con ESA cookie —la que emitió el servidor, no una armada a mano— abre
    galleta = set_cookie.split(";")[0]
    for arch in ("data.json", "p0.jpg"):
        est, _, _ = _pedir(puerto, "/armar/ciclocompleto/%s" % arch, cookie=galleta)
        assert est == 200, "la cookie que emite el login no abre el link (%s)" % arch


def test_a_QUIEN_LE_REENVIARON_el_link_no_le_sirve_entrar_con_SU_google(servidor,
                                                                       monkeypatch):
    """EL escenario que este trabajo vino a impedir, entero y por las rutas de verdad.

    No es «alguien sin cuenta»: es alguien con una cuenta de Google perfectamente
    legítima, que entra bien, que el motor reconoce — y que igual no puede abrir ESTE
    link porque no es suyo. Tener sesión no es tener derecho.

    Se prueba por el ciclo completo (login real → cookie real → pedido real) porque es la
    única forma de ver que el «no» ocurre en el lugar correcto: si el endpoint de login
    rechazara a los que no son dueños, se convertiría en una forma de preguntarle al motor
    qué mail compró qué, con sólo tener el link. El login dice que sí; el candado dice que
    no."""
    import acceso as acc
    puerto, rompe = servidor
    _token_falso(rompe, "reenviado1", dueño="ana@gmail.com")

    monkeypatch.setattr(acc, "email_de_google", lambda *a, **k: "curioso@gmail.com")
    c = http.client.HTTPConnection("127.0.0.1", puerto, timeout=20)
    c.request("POST", "/acceso/google",
              body=json.dumps({"credential": "token-legitimo-de-otra-persona"}).encode(),
              headers={"Content-Type": "application/json"})
    r = c.getresponse()
    ok = json.loads(r.read()).get("ok")
    galleta = (r.getheader("Set-Cookie") or "").split(";")[0]
    c.close()

    assert ok is True, ("el login tiene que dejar entrar: quién es dueño de qué se decide "
                        "al servir el link, no acá")
    assert galleta.startswith("ct3d_acceso=")

    # entró bien, el motor lo reconoce...
    est, _, cuerpo = _pedir(puerto, "/acceso/quien", cookie=galleta)
    assert json.loads(cuerpo)["entrado"] is True

    # ...y el link ajeno sigue cerrado, en la página y en los archivos
    est, _, cuerpo = _pedir(puerto, "/armar/reenviado1/", cookie=galleta)
    assert est == 403
    assert "This link is yours" in cuerpo.decode("utf-8")
    assert "ana@gmail.com" not in cuerpo.decode("utf-8"), (
        "le dijo al curioso el mail de quien compró")
    for arch in ("data.json", "p0.jpg"):
        est, _, _ = _pedir(puerto, "/armar/reenviado1/%s" % arch, cookie=galleta)
        assert est == 403, "%s se bajó con una cuenta ajena" % arch
