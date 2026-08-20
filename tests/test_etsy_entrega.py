"""La entrega a un comprador de Etsy: que entregue a quien compró, y a nadie más.

POR QUÉ ESTE TEST EXISTE
────────────────────────
19-ago-2026. Se probó contra la API de Etsy —no se supuso— y salieron dos cosas que definen
todo el diseño:

    GET /shops/{id}/receipts   → 403, falta el permiso `transactions_r`
    GET .../conversations      → 404, **NO HAY API DE MENSAJERÍA en Etsy v3**

O sea que no se le puede mandar el archivo al comprador por código. La entrega es de
autogestión: el comprador entra a `/etsy`, pone su número de orden y sus datos, y se baja el
kit. El vendedor no toca nada.

LO QUE HAY QUE PROTEGER, Y ES UNA SOLA COSA
───────────────────────────────────────────
El link vive dentro de un PDF que Etsy le entrega sólo al que compró — pero **un PDF se
reenvía**. Lo único que separa «producto pago» de «producto gratis» es que la orden se
valide de verdad. Por eso el sistema **falla CERRADO**: ante cualquier duda —falta el
permiso, se cayó la API, el número es raro— NO entrega.

Un test que sólo comprobara el camino feliz dejaría pasar exactamente el bug que arruina el
negocio: que ante un error se entregue igual.
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import etsy_pedidos  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(autouse=True)
def registro_limpio(tmp_path, monkeypatch):
    """Cada test con su propio registro de canjes: si compartieran archivo, uno le
    contaría los canjes al otro y los resultados dependerían del orden."""
    monkeypatch.setattr(etsy_pedidos, "REGISTRO", str(tmp_path / "canjes.json"))
    yield


# ── que NO entregue ───────────────────────────────────────────────────────────

def test_un_numero_que_no_es_numero_no_gasta_una_llamada(monkeypatch):
    """Antes de preguntarle nada a Etsy se mira la forma: son dígitos y nada más."""
    llamadas = []
    monkeypatch.setattr(etsy_pedidos, "_get", lambda *a, **k: llamadas.append(a))
    for basura in ("", "   ", "abc", "12", "3210987654; DROP TABLE", "../../etc/passwd",
                   "1234567890" * 5):
        ok, info, err = etsy_pedidos.validar(basura)
        assert not ok, basura
        assert err
    assert not llamadas, "se le preguntó a Etsy por un número que no tenía forma de orden"


def test_SIN_PERMISO_no_entrega(monkeypatch):
    """El caso real de hoy: al token le falta `transactions_r`.

    Es EL test del diseño. Si ante la falta de permiso el sistema entregara igual
    —«bueno, no puedo verificar, se lo doy»— el kit sería gratis para cualquiera que
    tuviera el link. Falla cerrado."""
    def explota(*a, **k):
        raise etsy_pedidos.SinPermiso("lacks scope for this request (requires scope: transactions_r)")
    monkeypatch.setattr(etsy_pedidos, "_get", explota)
    ok, info, err = etsy_pedidos.validar("3210987654")
    assert not ok
    assert "message us" in err.lower() or "escribinos" in err.lower()


def test_si_la_API_se_cae_no_entrega(monkeypatch):
    """Un error de red no puede convertirse en un kit regalado."""
    def explota(*a, **k):
        raise RuntimeError("HTTP 500 en /receipts — boom")
    monkeypatch.setattr(etsy_pedidos, "_get", explota)
    ok, _, err = etsy_pedidos.validar("3210987654")
    assert not ok and err


def test_una_orden_de_otra_tienda_no_existe_y_no_entrega(monkeypatch):
    def explota(*a, **k):
        raise RuntimeError("HTTP 404 en /receipts — Resource not found")
    monkeypatch.setattr(etsy_pedidos, "_get", explota)
    ok, _, err = etsy_pedidos.validar("3210987654")
    assert not ok
    assert "orden" in err.lower() or "order" in err.lower()


def test_una_orden_SIN_PAGAR_no_entrega(monkeypatch):
    monkeypatch.setattr(etsy_pedidos, "_get",
                        lambda *a, **k: {"receipt_id": 1, "is_paid": False})
    ok, _, err = etsy_pedidos.validar("3210987654")
    assert not ok


def test_is_paid_ausente_se_trata_como_NO_pagada(monkeypatch):
    """Si Etsy dejara de mandar el campo, la duda se resuelve para el lado seguro."""
    monkeypatch.setattr(etsy_pedidos, "_get", lambda *a, **k: {"receipt_id": 1})
    ok, _, _ = etsy_pedidos.validar("3210987654")
    assert not ok


# ── que SÍ entregue, y cuántas veces ──────────────────────────────────────────

def _paga(*a, **k):
    return {"receipt_id": 3210987654, "is_paid": True, "name": "Emma's mum"}


def test_una_orden_pagada_entrega(monkeypatch):
    monkeypatch.setattr(etsy_pedidos, "_get", _paga)
    ok, info, err = etsy_pedidos.validar("3210987654")
    assert ok and err is None
    assert info["canjes_usados"] == 0


def test_se_puede_volver_a_generar_pero_no_infinitas_veces(monkeypatch):
    """Volver a pedirlo tiene que ser gratis —el comprador se equivoca escribiendo la
    fecha— pero no puede ser infinito, o la orden se convierte en una canilla."""
    monkeypatch.setattr(etsy_pedidos, "_get", _paga)
    for i in range(etsy_pedidos.MAX_CANJES):
        ok, info, err = etsy_pedidos.validar("3210987654")
        assert ok, "el canje %d debería estar permitido: %s" % (i + 1, err)
        etsy_pedidos.registrar_canje("3210987654", "tok%d" % i, {"nombre": "Emma"})
    ok, _, err = etsy_pedidos.validar("3210987654")
    assert not ok, "pasado el tope tiene que dejar de entregar"
    assert str(etsy_pedidos.MAX_CANJES) in err


def test_el_tope_es_POR_ORDEN_no_global(monkeypatch):
    """Que un comprador agote sus canjes no puede dejar sin kit al siguiente."""
    monkeypatch.setattr(etsy_pedidos, "_get", _paga)
    for i in range(etsy_pedidos.MAX_CANJES):
        etsy_pedidos.registrar_canje("1111111111", "t%d" % i, {})
    assert not etsy_pedidos.validar("1111111111")[0]
    assert etsy_pedidos.validar("2222222222")[0], "otra orden tiene que poder generar"


def test_el_registro_sobrevive_a_releerlo(monkeypatch):
    monkeypatch.setattr(etsy_pedidos, "_get", _paga)
    etsy_pedidos.registrar_canje("3210987654", "tok", {"nombre": "Emma"})
    assert etsy_pedidos.canjes_de("3210987654") == 1
    d = json.load(open(etsy_pedidos.REGISTRO, encoding="utf-8"))
    assert d["3210987654"]["canjes"][0]["nombre"] == "Emma"
    # y el número se guarda como TEXTO: si se guardara como int, buscarlo con str fallaría
    assert "3210987654" in d


# ── la página y la ruta ───────────────────────────────────────────────────────

def _sin_comentarios(html):
    """Lo que el comprador VE. Los comentarios del código no se renderizan.

    La primera versión de este test miraba el archivo entero y falló por la palabra
    «Confirmá»… escrita dentro de un comentario que explica por qué la página está en
    inglés. Un test que marca la documentación como defecto enseña a ignorarlo."""
    import re as _re
    sin = _re.sub(r"<!--.*?-->", " ", html, flags=_re.S)          # comentarios HTML
    # Los `//` de JS también van al final de una línea, no sólo al principio: la primera
    # versión sólo miraba `^//` y dejó pasar un comentario de cola. El `(?<!:)` es para no
    # comerse las URLs, donde `//` viene después de dos puntos.
    sin = _re.sub(r"(?<!:)//[^\n]*", " ", sin)
    return sin


def test_la_pagina_del_comprador_existe_y_esta_en_ingles():
    p = os.path.join(RAIZ, "etsy.html")
    assert os.path.exists(p), "falta etsy.html, que es lo que abre el comprador"
    html = open(p, encoding="utf-8").read()
    assert "/etsy/generar" in html, "la página no llama a la ruta que genera"
    assert "/etsy/opciones" in html, "la página no carga las temáticas del motor"
    # la abre alguien que compró en Etsy: no puede pedirle nada en español
    visible = _sin_comentarios(html)
    import re as _re
    acentos = _re.findall(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]*[áéíóúñ¡¿][a-zA-ZáéíóúñÁÉÍÓÚÑ]*", visible)
    assert not acentos, "la página del comprador tiene español a la vista: %s" % sorted(set(acentos))
    for palabra in ("Confirmá", "Descargar", "cumpleaños", "Nombre del"):
        assert palabra not in visible, "la página del comprador tiene español: %r" % palabra


def test_TODO_lo_que_ve_el_comprador_esta_en_ingles(monkeypatch):
    """No alcanza con que la página esté en inglés: **los mensajes de error también los lee
    él**, y salen de otro archivo.

    Se descubrió probando la ruta de verdad contra el motor levantado, no leyendo el código:
    la página estaba impecable en inglés y el servidor contestaba «Ese no parece un número
    de orden de Etsy». El test que había miraba `etsy.html` y nada más — otra vez un barrido
    que protege hasta donde mira."""
    casos = []
    # los mensajes de rechazo, uno por rama
    casos.append(etsy_pedidos.validar("no-es-un-numero")[2])
    monkeypatch.setattr(etsy_pedidos, "_get",
                        lambda *a, **k: {"receipt_id": 1, "is_paid": False})
    casos.append(etsy_pedidos.validar("3210987654")[2])

    def sin_permiso(*a, **k):
        raise etsy_pedidos.SinPermiso("requires scope: transactions_r")
    monkeypatch.setattr(etsy_pedidos, "_get", sin_permiso)
    casos.append(etsy_pedidos.validar("3210987654")[2])

    def no_existe(*a, **k):
        raise RuntimeError("HTTP 404 en /receipts")
    monkeypatch.setattr(etsy_pedidos, "_get", no_existe)
    casos.append(etsy_pedidos.validar("3210987654")[2])

    def se_cayo(*a, **k):
        raise RuntimeError("HTTP 500 en /receipts")
    monkeypatch.setattr(etsy_pedidos, "_get", se_cayo)
    casos.append(etsy_pedidos.validar("3210987654")[2])

    monkeypatch.setattr(etsy_pedidos, "_get", _paga)
    for i in range(etsy_pedidos.MAX_CANJES):
        etsy_pedidos.registrar_canje("3210987654", "t%d" % i, {})
    casos.append(etsy_pedidos.validar("3210987654")[2])

    import re as _re
    for m in casos:
        assert m, "hay una rama que rechaza sin explicar por qué"
        malo = _re.findall(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]*[áéíóúñ¡¿][a-zA-ZáéíóúñÁÉÍÓÚÑ]*", m)
        assert not malo, "mensaje en español para un comprador de Etsy: %r" % m


def test_los_nombres_de_las_tematicas_tambien_estan_en_ingles():
    """El selector de la página se llena desde el motor. Si los nombres salen en español,
    el comprador elige entre «Bomberos al Rescate» y «Un espacio de locura»."""
    import idioma
    import temas as _t
    faltan = []
    for t in _t.list_temas():
        tid = t["id"] if isinstance(t, dict) else str(t)
        if tid not in idioma.NOMBRE_TEMA_EN:
            faltan.append(tid)
    assert not faltan, ("estas temáticas no tienen nombre en inglés y saldrían en español "
                        "en el selector del comprador: %s" % faltan)
    import re as _re
    for tid, nom in idioma.NOMBRE_TEMA_EN.items():
        assert not _re.search(r"[áéíóúñ¡¿]", nom), "%s: el nombre 'en inglés' tiene español: %r" % (tid, nom)


def test_la_ruta_esta_conectada_en_el_servicio():
    s = open(os.path.join(RAIZ, "servicio.py"), encoding="utf-8").read()
    assert '"/etsy/generar"' in s and "_etsy_generar" in s
    assert '"/etsy"' in s and '"/etsy/opciones"' in s


def test_el_kit_de_etsy_se_pide_SIEMPRE_en_ingles():
    """Quien compra en Etsy compra en inglés. Si esta línea se cayera, el comprador
    recibiría un kit que dice «Confirmá» y no habría test que lo notara aguas abajo."""
    s = open(os.path.join(RAIZ, "servicio.py"), encoding="utf-8").read()
    i = s.index("def _etsy_generar")
    cuerpo = s[i:i + 4000]
    assert 'datos["idioma"] = "en"' in cuerpo


def test_la_ruta_falla_cerrada_ante_un_error_de_validacion():
    """Que `validar` reviente no puede terminar en un kit entregado: el handler atrapa la
    excepción y devuelve 503, nunca el link."""
    s = open(os.path.join(RAIZ, "servicio.py"), encoding="utf-8").read()
    i = s.index("def _etsy_generar")
    cuerpo = s[i:i + 4000]
    assert "except Exception" in cuerpo and "503" in cuerpo


def test_el_canje_se_anota_DESPUES_de_que_el_kit_existe():
    """Si se anotara antes, un error del servidor le comería un intento al comprador —que
    ya pagó— sin darle nada a cambio.

    Se comparan las posiciones de la LLAMADA de verdad, no de un texto que también aparece
    en el docstring: la primera versión medía contra la mención de «/api/generar» en el
    comentario de arriba, así que la mutación que movía el registro quedaba en verde. Un
    test que mide contra su propia documentación no mide nada."""
    s = open(os.path.join(RAIZ, "servicio.py"), encoding="utf-8").read()
    i = s.index("def _etsy_generar")
    cuerpo = s[i:s.index("def _duelo_crear", i)]
    assert cuerpo.index("registrar_canje(orden") > cuerpo.index("urlopen(req")


def test_el_tope_cuenta_igual_si_el_numero_llega_como_entero(monkeypatch):
    """El número de orden puede llegar como texto o como entero según quién llame. Si el
    registro guardara una forma y se leyera la otra, el tope no contaría nada y una sola
    orden generaría kits sin límite."""
    monkeypatch.setattr(etsy_pedidos, "_get", _paga)
    for i in range(etsy_pedidos.MAX_CANJES):
        etsy_pedidos.registrar_canje(3210987654, "t%d" % i, {})       # se guarda con ENTERO
    # y se lee de las DOS formas: son funciones públicas del módulo, así que su contrato es
    # aceptar el número como venga. Probar sólo una deja la otra sin red.
    assert etsy_pedidos.canjes_de(3210987654) == etsy_pedidos.MAX_CANJES, "leído como entero"
    assert etsy_pedidos.canjes_de("3210987654") == etsy_pedidos.MAX_CANJES, "leído como texto"
    ok, _, err = etsy_pedidos.validar(3210987654)                     # entero
    assert not ok, "el tope no contó: la orden podría generar kits sin límite"
    ok, _, _ = etsy_pedidos.validar("3210987654")                     # texto
    assert not ok


# ── que la orden sea DE ESTE producto ─────────────────────────────────────────
#
# 19-ago-2026. Encontrado leyendo `validar` para agregar el producto web: comprobaba
# que la orden existiera y estuviera paga, y nada más. La tienda tiene 22 publicaciones
# —11 kits a USD 12 y 11 rompecabezas imprimibles a USD 7— así que el número de orden
# del de USD 7, que Etsy entrega directo sin pasar por acá, servía para armar además el
# de USD 12. Cinco veces, que es el tope de canjes.

KIT_ID, PUZZLE_ID = 4558813047, 4559060474


@pytest.fixture
def mapa(tmp_path, monkeypatch):
    import json as _json
    p = tmp_path / "productos.json"
    p.write_text(_json.dumps({"kit": [KIT_ID], "rompecabezas": [PUZZLE_ID]}))
    monkeypatch.setattr(etsy_pedidos, "MAPA_PRODUCTOS", str(p))
    return p


def _recibo_con(*listing_ids):
    def _f(ruta, *a, **k):
        if ruta.endswith("/transactions"):
            return {"results": [{"listing_id": i} for i in listing_ids]}
        return {"receipt_id": 3210987654, "is_paid": True, "name": "Emma's mum"}
    return _f


def test_la_orden_de_OTRO_producto_no_arma_el_kit(monkeypatch, mapa):
    """EL test de este bloque. Compró el rompecabezas de USD 7 —y ya lo tiene, Etsy se
    lo entregó— y con ese número quiere el kit de USD 12."""
    monkeypatch.setattr(etsy_pedidos, "_get", _recibo_con(PUZZLE_ID))
    ok, _, err = etsy_pedidos.validar("3210987654", tipo="kit")
    assert not ok, "una orden de otro producto armó el kit"
    assert "order doesn" in err or "check" in err


def test_la_orden_del_kit_SI_arma_el_kit(monkeypatch, mapa):
    monkeypatch.setattr(etsy_pedidos, "_get", _recibo_con(KIT_ID))
    ok, info, err = etsy_pedidos.validar("3210987654", tipo="kit")
    assert ok and err is None


def test_una_orden_con_LOS_DOS_productos_arma_el_kit(monkeypatch, mapa):
    """Comprar las dos cosas juntas es lo normal, no la excepción: son la misma tienda y
    el mismo cumpleaños. Si el chequeo pidiera que la orden sea SÓLO del kit, el
    comprador que más gastó sería el único que no puede canjear."""
    monkeypatch.setattr(etsy_pedidos, "_get", _recibo_con(PUZZLE_ID, KIT_ID))
    ok, _, err = etsy_pedidos.validar("3210987654", tipo="kit")
    assert ok, err


def test_si_no_se_puede_saber_QUE_compro_no_se_entrega(monkeypatch, mapa):
    """Misma política que el resto del archivo: falla cerrado. Se agrega porque acá la
    tentación es al revés — «la orden existe y está paga, ya está» — y esa es justo la
    forma de razonar que dejó el agujero."""
    def sin_transacciones(ruta, *a, **k):
        if ruta.endswith("/transactions"):
            raise RuntimeError("HTTP 404 en GET .../transactions")
        return {"receipt_id": 3210987654, "is_paid": True}
    monkeypatch.setattr(etsy_pedidos, "_get", sin_transacciones)
    ok, _, err = etsy_pedidos.validar("3210987654", tipo="kit")
    assert not ok and err


def test_sin_mapa_de_productos_no_se_entrega(monkeypatch, tmp_path):
    """Si el archivo no está, no se sabe qué publicación es qué — y no saber no puede
    significar «dale igual»."""
    monkeypatch.setattr(etsy_pedidos, "MAPA_PRODUCTOS", str(tmp_path / "no-existe.json"))
    monkeypatch.setattr(etsy_pedidos, "_get", _recibo_con(KIT_ID))
    ok, _, err = etsy_pedidos.validar("3210987654", tipo="kit")
    assert not ok and err


def test_sin_tipo_se_comporta_como_antes(monkeypatch, mapa):
    """Compatibilidad: los llamadores que no pasan `tipo` no se rompen, y tampoco gastan
    la llamada de las transacciones."""
    rutas = []

    def espia(ruta, *a, **k):
        rutas.append(ruta)
        return {"receipt_id": 3210987654, "is_paid": True}
    monkeypatch.setattr(etsy_pedidos, "_get", espia)
    ok, _, _ = etsy_pedidos.validar("3210987654")
    assert ok
    assert not any(r.endswith("/transactions") for r in rutas)


def test_el_recibo_que_YA_trae_sus_transacciones_no_pide_otra_vez(monkeypatch, mapa):
    """Una llamada menos por venta. Y —más importante— un camino menos que puede fallar
    justo cuando alguien está esperando lo que pagó."""
    rutas = []

    def espia(ruta, *a, **k):
        rutas.append(ruta)
        return {"receipt_id": 3210987654, "is_paid": True,
                "transactions": [{"listing_id": KIT_ID}]}
    monkeypatch.setattr(etsy_pedidos, "_get", espia)
    ok, _, err = etsy_pedidos.validar("3210987654", tipo="kit")
    assert ok, err
    assert not any(r.endswith("/transactions") for r in rutas)


def test_la_pagina_del_kit_pide_el_producto_kit():
    """El chequeo puede existir y no estar enchufado. Se mira el llamador real."""
    s = open(os.path.join(RAIZ, "servicio.py"), encoding="utf-8").read()
    i = s.index("def _etsy_generar")
    cuerpo = s[i:s.index("def _duelo_crear", i)]
    assert 'validar(orden, tipo="kit")' in cuerpo, (
        "la página del kit valida sin decir qué producto espera")


def test_el_mapa_de_productos_del_repo_tiene_las_11_publicaciones():
    """El archivo real, no uno de mentira: si queda vacío o a medias, el comprador de una
    temática que falte se queda afuera — y eso no lo dice ningún otro test."""
    import json as _json
    p = os.path.join(RAIZ, "etsy_productos.json")
    assert os.path.isfile(p), "falta etsy_productos.json"
    d = _json.load(open(p, encoding="utf-8"))
    assert len(d.get("kit") or []) == 11, "los kits publicados son 11, uno por temática"
    assert len(set(d["kit"])) == 11, "hay ids repetidos"
    assert not (set(d["kit"]) & set(d.get("rompecabezas") or [])), (
        "una publicación no puede ser de dos productos a la vez")
