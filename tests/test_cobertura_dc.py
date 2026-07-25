# -*- coding: utf-8 -*-
"""La currícula del grado tiene que estar COMPLETA y ABIERTA.

Este test existe por un agujero real (25-jul-2026): el cuaderno escolar de 4° salía con
42 tarjetas y se veía completo, pero cubría 29 de los 58 temas que el Diseño Curricular
le fija al año — Ciencias Naturales tenía UNA actividad de ocho y las tres transversales
no existían. Encima, diez de los temas que sí existían estaban detrás del candado de los
niveles 2 y 3, así que un chico con `nivel_max: 1` no llegaba nunca a la comprensión
lectora ni a los ángulos, que son contenido del año que está cursando.

Nada de eso fallaba: había que cruzar el menú contra la currícula a mano para verlo.

La regla que fija este test, y que vale para construir cualquier grado nuevo:

    TODO tema del DC del grado tiene una actividad, esa actividad ESTÁ en el menú, y
    está en el NIVEL 1.

Ver `actividades_cobertura.py` (el manifiesto) y `docs/COBERTURA-CURRICULAR.md` (el
procedimiento para dar de alta un grado).
"""
import pytest

import actividades_cobertura as cob
import actividades_curriculum as cur


GRADOS_AUDITADOS = sorted(cob.DC)


def test_hay_al_menos_un_grado_auditado():
    """Si el manifiesto quedara vacío, todo lo de abajo pasaría sin probar nada."""
    assert GRADOS_AUDITADOS, "actividades_cobertura.DC no declara ningún grado"


@pytest.mark.parametrize("grado", GRADOS_AUDITADOS)
def test_todos_los_temas_del_dc_tienen_actividad(grado):
    """Ningún tema del año puede quedar sin construir."""
    faltan = cob.faltantes(grado)
    assert not faltan, "%d°: %d temas del DC sin actividad: %s" % (
        grado, len(faltan), ", ".join("%s %s" % (t["cod"], t["tema"]) for t in faltan))


@pytest.mark.parametrize("grado", GRADOS_AUDITADOS)
def test_la_curricula_del_grado_esta_completa_y_en_nivel_1(grado):
    """La regla entera: declarada, presente en el menú real y sin candado.

    `problemas()` mira el menú que de verdad se le arma al chico, no el catálogo: una
    actividad puede estar escrita y no llegar nunca a la pantalla
    ([[ct3d-contenido-cargado-sin-enchufar]])."""
    fallas = cob.problemas(grado)
    assert not fallas, "%d°:\n  - %s" % (grado, "\n  - ".join(fallas))


@pytest.mark.parametrize("grado", GRADOS_AUDITADOS)
def test_el_manifiesto_no_declara_actividades_inventadas(grado):
    """Cada id declarado existe: o es del catálogo curricular, o es un juego del player.

    Sin esto, un typo en el manifiesto se leería como 'tema cubierto'."""
    del_catalogo = {a["id"] for a in cur.CATALOGO}
    menu = cob._menu_real(grado)
    for tema in cob.temas(grado):
        for aid in cob._ids(tema):
            assert aid in del_catalogo or aid in menu, (
                "%d° %s %s: el id '%s' no existe ni en el catálogo ni en el menú"
                % (grado, tema["cod"], tema["tema"], aid))


@pytest.mark.parametrize("grado", GRADOS_AUDITADOS)
def test_cada_tema_del_dc_esta_declarado_una_sola_vez(grado):
    """Dos temas con el mismo código serían un error de copiar y pegar del manifiesto."""
    codigos = [t["cod"] for t in cob.temas(grado)]
    repetidos = sorted({c for c in codigos if codigos.count(c) > 1})
    assert not repetidos, "%d°: códigos repetidos en el manifiesto: %s" % (
        grado, ", ".join(repetidos))


@pytest.mark.parametrize("grado", GRADOS_AUDITADOS)
def test_cada_tema_declara_su_fuente_curricular(grado):
    """Un tema sin 'dc' es una fila sin justificación: no se puede auditar después."""
    for t in cob.temas(grado):
        assert t.get("dc"), "%d° %s: no dice qué contenido del DC cubre" % (grado, t["cod"])
        assert t.get("area"), "%d° %s: sin área" % (grado, t["cod"])


def test_el_catalogo_curricular_es_valido():
    """El mismo chequeo que corre gen_curriculum.py antes de emitir el .js.

    Se repite acá para que un banco mal armado falle en `pytest` y no recién cuando
    alguien intenta regenerar el player."""
    problemas = cur.validar()
    assert not problemas, "catálogo inválido:\n  - " + "\n  - ".join(problemas)


def test_ninguna_actividad_del_catalogo_quedo_fuera_del_menu():
    """Escribir la actividad no alcanza: tiene que llegar a la pantalla del chico.

    Es la regla de [[ct3d-contenido-cargado-sin-enchufar]] hecha test: las 7 portadas de
    grado vivieron un día en el repo sin que ningún código las leyera."""
    for grado in range(1, 8):
        declaradas = {a["id"] for a in cur.CATALOGO if a["grado"] == grado}
        if not declaradas:
            continue
        en_menu = set(cob._menu_real(grado))
        huerfanas = sorted(declaradas - en_menu)
        assert not huerfanas, (
            "%d°: estas actividades están en el catálogo pero no llegan al menú: %s"
            % (grado, ", ".join(huerfanas)))
