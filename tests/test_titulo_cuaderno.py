"""El título grande del cuaderno.

Pablo lo vio en 7.º: decía **"Las actividades de Peque"**. "Peque" es el placeholder del
formulario cuando nadie escribe su nombre, y se filtraba al título — 45 cuadernos lo tenían.
Un nombre de relleno en el título es peor que no tener nombre.

Y para el escolar el título ahora es el GRADO, no el nombre: a los 12 años que el cuaderno
te trate por el nombre como a un nene de sala de 5 no ayuda; el grado sí dice algo.
"""
import os
import sys

import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
import actividades_web as A  # noqa: E402


@pytest.mark.parametrize("edad,grado", [(6, 1), (9, 4), (12, 7)])
def test_el_escolar_se_titula_por_el_grado(edad, grado):
    assert A.titulo_cuaderno("Sofía", edad, escolar=True) == "Cuaderno de %d.º grado" % grado
    # y no importa el nombre: ni el de relleno ni uno real cambian el título
    assert A.titulo_cuaderno("Peque", edad, escolar=True) == "Cuaderno de %d.º grado" % grado


def test_el_nombre_de_relleno_nunca_llega_al_titulo():
    """Es el bug que vio Pablo. Vale para las dos líneas de producto."""
    assert "Peque" not in A.titulo_cuaderno("Peque", 9)
    assert "Peque" not in A.titulo_cuaderno("Peque", 12, escolar=True)
    assert "Peque" not in A.titulo_cuaderno(" Peque ", 9)


def test_en_cumpleanos_el_nombre_real_SI_va():
    """Ahí el nombre es el regalo: no se toca."""
    assert A.titulo_cuaderno("Sofía", 9) == "Las actividades de Sofía"


def test_sin_nombre_queda_generico():
    for n in ("", "   ", None):
        assert A.titulo_cuaderno(n, 9) == "Cuaderno de actividades"


@pytest.mark.parametrize("edad", [None, 0, 99, "nueve", 5, 13])
def test_una_edad_que_no_da_grado_no_rompe(edad):
    """Fuera de 1.º-7.º cae al genérico en vez de inventar "Cuaderno de 94.º grado"."""
    t = A.titulo_cuaderno("Peque", edad, escolar=True)
    assert t == "Cuaderno de actividades", t


def test_el_relleno_espeja_al_del_player():
    """`NOMBRE_RELLENO` acá y `NOMBRE_GENERICO` en el player tienen que ser el MISMO texto:
    si se separan, el player deja de precargar el nombre y Python deja de filtrarlo."""
    import re
    js = open(os.path.join(BASE, "actividades_player.js"), encoding="utf-8").read()
    m = re.search(r'const NOMBRE_GENERICO\s*=\s*"([^"]+)"', js)
    assert m, "no se encontró NOMBRE_GENERICO en el player"
    assert m.group(1) == A.NOMBRE_RELLENO
