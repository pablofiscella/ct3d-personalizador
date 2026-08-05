# -*- coding: utf-8 -*-
"""Correr la suite del motor no puede mandarle un WhatsApp a nadie.

5-ago-2026. Pablo mandó una captura de su WhatsApp con tres avisos de "🚩 Reportaron un
error en el cuaderno" —uno con `AAAAAAAA…` de 300 caracteres— y preguntó *"esto lo hiciste
vos no?"*.

Sí. El token de todos era `tok-test-reporte`: los mandó `tests/test_reportar_error.py`, tres
veces en el día, cada vez que corrí `pytest`.

CÓMO ESTABA ABIERTA LA PUERTA: la app (`/opt/ct3d/backend`) tiene un `conftest.py` con
guardianes desde hace días. **Este repo no tenía conftest.py.** Y `_act_reporte` mete
`/opt/ct3d/backend` en `sys.path` a mano para llamar a `notif_emit` — o sea que los tests
del motor cruzan al otro repo y salen por el canal real, sin pasar por ninguna de sus redes.

LA TERCERA VEZ DEL MISMO AGUJERO: 28-jul los tests mandaban correos reales; 2-ago Kydo
estrenó su propia salida de correo y saltó el guard viejo; hoy el motor manda WhatsApp desde
un repo que nadie había pensado como emisor. **El guardián siempre se puso donde apareció el
problema, y la salida al mundo la abre cualquier módulo nuevo.**

Por eso este test no comprueba "no se manda WhatsApp": comprueba que exista el conftest y que
tape el ÚNICO PUNTO DE SALIDA declarado. Un test que persiga cada canal se queda corto con el
canal siguiente.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFTEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conftest.py")


def test_este_repo_tiene_conftest():
    """EL test. Sin él, la suite del motor corre sin ninguna contención — y eso no se nota
    hasta que a alguien le suena el teléfono."""
    assert os.path.isfile(CONFTEST), (
        "el motor no tiene tests/conftest.py: sus tests salen al mundo real")


def test_el_guardian_tapa_notif_emit():
    """Se tapa el punto de salida ENTERO, no cada canal.

    `notif_emit` es, por diseño, el único lugar por donde sale una notificación. Parchear
    WhatsApp y dejar el correo —o al revés— es exactamente cómo este agujero se reabrió dos
    veces."""
    src = open(CONFTEST, encoding="utf-8").read()
    assert "notif_emit" in src, "el guardián no tapa el punto de salida de las notificaciones"
    assert "autouse=True" in src, (
        "el guardián no es autouse: el que se olvide de pedirlo vuelve a mandar avisos reales")


def test_el_guardian_esta_ACTIVO_en_esta_corrida():
    """Que el archivo exista no alcanza: tiene que estar aplicándose ahora.

    Se comprueba llamando de verdad. Si algún día el parche deja de tomar —un import
    distinto, un módulo recargado— este test se cae en vez de que se entere Pablo por la
    captura de su teléfono."""
    if "/opt/ct3d/backend" not in sys.path:
        sys.path.insert(0, "/opt/ct3d/backend")
    try:
        import notificaciones
    except Exception:
        return              # sin el módulo de la tienda no hay salida posible
    r = notificaciones.notif_emit("reporte_cuaderno", titulo="prueba del guardián",
                                  detalle="si esto llega a un teléfono, el guardián no anda",
                                  wa_texto="prueba")
    assert isinstance(r, dict) and not r.get("emitida"), (
        "`notif_emit` emitió de verdad durante un test: %r" % (r,))
    assert r.get("motivo") == "test", (
        "no está el guardián del conftest: el aviso salió por el camino real (%r)" % (r,))
