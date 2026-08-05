# -*- coding: utf-8 -*-
"""Ningún test del motor manda nada al mundo real.

5-ago-2026. Pablo me mandó una captura de su WhatsApp con esto:

    🚩 Tablas ninja · La respuesta está mal · 4.º grado · ronda 3 · dice que 7x8=54
    🚩 el cuaderno · No funciona / no carga
    🚩 CCCCCCCCCC… · Otra cosa · AAAAAAAAAA…

y preguntó *"esto lo hiciste vos no?"*. Sí: era la suite de tests del motor. El token de
todos esos avisos es `tok-test-reporte`, y salieron a las 01:00, 01:10 y 15:27 — cada vez
que corrí `pytest`.

POR QUÉ PASÓ, y es lo que este archivo viene a cerrar
─────────────────────────────────────────────────────
`/opt/ct3d/backend/tests/conftest.py` tiene desde hace días un guardián que impide que los
tests manden WhatsApp y correo de verdad. **Este repo no tenía conftest.py.** Los tests del
motor corren sin ninguna red de contención, y `_act_reporte` llama a `notif_emit` del otro
repo insertándolo en `sys.path` a mano — así que cruza la frontera y sale por el canal real.

Es LA TERCERA VEZ que este agujero se abre por una puerta nueva: el 28-jul los tests
mandaban correos reales, el 2-ago Kydo estrenó su propia salida de correo y saltó el guard
viejo, y ahora el motor manda WhatsApp desde un repo que nadie había pensado como emisor.

El patrón se repite porque el guardián se pone donde APARECIÓ el problema, y la salida al
mundo la abre cualquier módulo nuevo que se le ocurra a alguien. Por eso acá se tapa
`notif_emit` ENTERO —el único punto de salida declarado— y no cada canal por separado.

QUÉ NO HACE
───────────
No falsea la lógica: `notif_emit` sigue devolviendo la forma que devuelve cuando el aviso no
sale ({"emitida": False, …}), que es un estado normal en producción —el tipo puede estar
apagado o en dedup— así que el código bajo prueba no se desvía por un camino raro.
"""
import pytest


@pytest.fixture(autouse=True)
def _ningun_test_avisa_de_verdad(monkeypatch):
    """El guardián. `autouse` a propósito: si hubiera que acordarse de pedirlo, el que se
    olvide vuelve a mandarle un WhatsApp a Pablo y se entera por la captura."""
    import sys
    if "/opt/ct3d/backend" not in sys.path:
        sys.path.insert(0, "/opt/ct3d/backend")
    try:
        import notificaciones
    except Exception:
        return              # sin el módulo de la tienda no hay por dónde salir
    monkeypatch.setattr(
        notificaciones, "notif_emit",
        lambda *a, **kw: {"emitida": False, "motivo": "test"})
    # El canal directo, por si algún módulo lo llama sin pasar por `notif_emit`. Es
    # justamente la puerta por la que se coló la vez anterior.
    if hasattr(notificaciones, "_enviar_wa_personal"):
        monkeypatch.setattr(notificaciones, "_enviar_wa_personal",
                            lambda texto, db_path=None: True)


@pytest.fixture(autouse=True)
def _ningun_test_manda_correo(monkeypatch):
    """El motor manda mails en algunos caminos (entrega de piezas, avisos). Mismo criterio:
    se tapa la salida, no cada llamador."""
    import sys
    if "/opt/ct3d/backend" not in sys.path:
        sys.path.insert(0, "/opt/ct3d/backend")
    for mod, attr, valor in (("email_inbox", "enviar", (True, "")),
                             ("kydo.correo", "enviar", (True, ""))):
        try:
            m = __import__(mod, fromlist=["x"])
        except Exception:
            continue
        if hasattr(m, attr):
            monkeypatch.setattr(m, attr, lambda *a, **kw: valor)
