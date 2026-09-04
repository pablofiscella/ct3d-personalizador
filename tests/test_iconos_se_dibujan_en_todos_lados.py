"""Los íconos de las tarjetas tienen que DIBUJARSE en el dispositivo de una escuela.

Pablo, 04-sep-2026, con una captura: *"este icono desapareció de varias tarjetas. Se ve
así en algunas"* — un rectángulo vacío en «La palabra que abarca».

Era 🪆 (matrioska, U+1FA86), del bloque **U+1FA70–1FAFF**, que es Unicode 12 a 15
(2019-2022). Un teléfono o una computadora de unos años no tiene esos glifos y dibuja el
«tofu»: el cuadradito. Y no falla ruidosamente — la tarjeta se ve rota y nadie se entera
hasta que alguien manda una foto.

POR QUÉ ESTE BLOQUE Y NO TODOS LOS EMOJI. Los de Unicode 11 y anteriores (🧩 🤖 🧪 🧭…)
están en cualquier dispositivo desde 2018 y se usan en el cuaderno sin problema. El corte
está donde está la adopción real, no en «emoji nuevo = malo».

DÓNDE IMPORTA MÁS: son las tarjetas que ve un chico en su cuaderno y una maestra en la
demo que se le muestra a la escuela. Un cuadradito ahí no es un detalle estético.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import actividades_curriculum as ac  # noqa: E402

#: «Symbols and Pictographs Extended-A»: todo lo que entró de Unicode 12 en adelante.
NUEVO_DESDE, NUEVO_HASTA = 0x1FA70, 0x1FAFF


def _nuevos(texto):
    return [c for c in (texto or "") if NUEVO_DESDE <= ord(c) <= NUEVO_HASTA]


def test_ningun_icono_del_catalogo_es_de_unicode_12_o_posterior():
    malos = []
    for a in ac.CATALOGO:
        for c in _nuevos(a.get("icono")):
            malos.append("%s (%s.º grado): %s U+%04X"
                         % (a.get("titulo", "?"), a.get("grado", "?"), c, ord(c)))
    assert not malos, (
        "estos íconos se ven como un cuadradito vacío en dispositivos de unos años:\n  "
        + "\n  ".join(malos))


def test_todas_las_actividades_tienen_icono():
    """Una tarjeta sin ícono no se rompe, pero queda un hueco donde el chico espera algo."""
    sin = [a.get("titulo", "?") for a in ac.CATALOGO if not (a.get("icono") or "").strip()]
    assert not sin, "actividades sin ícono: %s" % sin[:8]


def test_el_menu_del_player_tampoco_los_usa():
    """El otro lugar donde se escriben íconos a mano: los menús por banda de edad."""
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "actividades_web.py")
    malos = []
    for m in re.finditer(r'"icono":\s*"([^"]*)"', open(p, encoding="utf-8").read()):
        for c in _nuevos(m.group(1)):
            malos.append("%s U+%04X" % (c, ord(c)))
    assert not malos, "íconos que no se dibujan en `actividades_web.py`: %s" % malos
