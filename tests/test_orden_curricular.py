# -*- coding: utf-8 -*-
"""Las tarjetas salen en el orden del Diseño Curricular.

Pablo, 30-jul-2026: *"quiero saber si el orden de las tarjetas en cada categoría están
ordenadas cronológicamente de acuerdo al orden que figura en la currícula"*.

No lo estaban. Salían en el orden en que están escritas en `actividades_curriculum.py`, y
lo que se fue agregando después quedó pegado al final: **53 de 325 tarjetas fuera de
lugar**, con 2.º Lengua casi entero barajado (12 de 14) y "Club de lectura" —que es L1,
por donde el DC arranca el año— apareciendo última de todas.

DE DÓNDE SALE EL ORDEN. Del código del DC que ya viene en la `fuente` de cada actividad
(`docs/auditoria-dc-caba/grado-2.md · L3`). No hubo que inventar ni cargar nada: el dato
ya estaba, sólo no se usaba para ordenar.

PERO EL CÓDIGO SOLO NO ALCANZA. Pablo: *"en primer grado no tiene que aparecer armar una
frase cuando todavía no sabe las vocales"*. Hay actividades que dependen de otra que el
programa numera DESPUÉS, así que ordenar sólo por número las ponía antes que aquello que
necesitan: 5 casos, 2 de ellos introducidos por el propio orden por código. Los
prerrequisitos ya estaban declarados (205 relaciones en `saberes.py`, campo
`prerrequisitos`) y nadie los usaba para ordenar.

Por eso el orden es TOPOLÓGICO con el DC de desempate, y por eso este archivo tiene dos
tests: el del DC admite que un prerrequisito lo pise, y el de prerrequisitos no admite
ninguna excepción. Si los dos se contradicen, manda el prerrequisito.

CÓMO CONVIVE CON EL MOTOR ADAPTATIVO. En el cuaderno el player reagrupa por categoría y
ordena por `Adapt.peso()`, que es lo que le conviene hacer al chico AHORA (Repasá →
Recomendado → disponible → Dominado). Ese sort es estable, así que este orden queda de
desempate: entre dos actividades igual de recomendadas, primero va la que el programa da
primero. Los dos criterios conviven; no compiten.

OJO AL DESPLEGAR: el menú queda CONGELADO en el data.json de cada token, así que los
cuadernos ya entregados mantienen el orden viejo hasta que se los regenere.
"""
import os
import re
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import actividades_curriculum as cur  # noqa: E402


def _codigo(a):
    """Usa la función REAL, no una copia: cuando el test duplicaba la regla se
    desincronizó al primer cambio y marcó como error lo que estaba bien."""
    return cur._orden_dc(a)


def _prereqs(sid):
    import saberes
    s = saberes.SABERES.get(sid) or {}
    return list(s.get("prerrequisitos") or s.get("prereqs") or [])


def _juegos_que_deben_ir_antes(ids):
    """{juego: {juegos del mismo grado que tienen que venir antes}}"""
    import saberes
    SAB = saberes.SABERES
    de_saber = {}
    for sid, s in SAB.items():
        for j in (s.get("juegos") or []):
            if j in ids:
                de_saber.setdefault(sid, []).append(j)
    necesita = {j: set() for j in ids}
    for sid, s in SAB.items():
        for j in (s.get("juegos") or []):
            if j not in ids:
                continue
            for pre in _prereqs(sid):
                for jp in de_saber.get(pre, []):
                    if jp != j:
                        necesita[j].add(jp)
    return necesita


@pytest.mark.parametrize("grado", range(1, 8))
def test_ninguna_actividad_va_antes_de_su_prerrequisito(grado):
    """EL guardián, y el que no admite excepciones: es el pedido textual de Pablo."""
    idx = {a["id"]: a for a in cur.CATALOGO}
    orden = {e["id"]: i for i, e in enumerate(cur.menu_de_grado(grado))}
    necesita = _juegos_que_deben_ir_antes(set(orden))
    malas = ["«%s» va antes que «%s», que es su prerrequisito"
             % (idx[j]["titulo"], idx[jp]["titulo"])
             for j, pos in orden.items() for jp in necesita[j] if orden[jp] > pos]
    assert not malas, "%d.º:\n  %s" % (grado, "\n  ".join(malas))


@pytest.mark.parametrize("grado", range(1, 8))
def test_el_menu_sigue_el_orden_del_dc(grado):
    """Dentro de cada eje los números crecen, SALVO que un prerrequisito lo obligue —
    ahí manda el prerrequisito, que es la razón de ser del orden."""
    idx = {a["id"]: a for a in cur.CATALOGO}
    menu = cur.menu_de_grado(grado)
    orden = {e["id"]: i for i, e in enumerate(menu)}
    necesita = _juegos_que_deben_ir_antes(set(orden))
    ultimo, fuera = {}, []
    for e in menu:
        pre, n = _codigo(idx[e["id"]])
        if pre in ultimo and n < ultimo[pre]:
            # La inversión es correcta si ESTA actividad necesita algo que el DC numera
            # DESPUÉS: ese prerrequisito tuvo que adelantarse y la empujó.
            justificada = any(_codigo(idx[jp])[1] > n for jp in necesita[e["id"]])
            if not justificada:
                fuera.append("%s%d («%s») va después de %s%d sin motivo"
                             % (pre, n, e["titulo"], pre, ultimo[pre]))
        else:
            ultimo[pre] = n
    assert not fuera, "%d.º tiene %d tarjeta(s) fuera del orden del DC:\n  %s" % (
        grado, len(fuera), "\n  ".join(fuera))


@pytest.mark.parametrize("grado", range(1, 8))
def test_ordenar_no_pierde_ni_duplica_ninguna(grado):
    """Ordenar no puede cambiar QUÉ actividades tiene el grado, sólo en qué orden."""
    ids_menu = [e["id"] for e in cur.menu_de_grado(grado)]
    ids_cat = [a["id"] for a in cur.actividades_de(grado)]
    assert sorted(ids_menu) == sorted(ids_cat), "el menú dejó de coincidir con el catálogo"
    assert len(ids_menu) == len(set(ids_menu)), "hay una actividad repetida en el menú"


def test_la_primera_de_lengua_de_5to_es_la_que_abre_el_ano():
    """Caso testigo del peor síntoma: «Club de lectura» es L1 y aparecía ÚLTIMA."""
    idx = {a["id"]: a for a in cur.CATALOGO}
    lengua = [e for e in cur.menu_de_grado(5) if idx[e["id"]]["area"] == "lengua"]
    assert lengua and lengua[0]["id"] == "club_lectura_5", \
        "Lengua de 5.º no empieza por L1: empieza por %s" % (lengua[0]["titulo"] if lengua else "—")


def test_las_que_no_tienen_numero_van_al_final_de_su_eje():
    """El DC no numera todo. Las sin número NO pueden abrir el eje: le robarían el primer
    lugar a la que el programa da primero (pasó con Lengua de 5.º)."""
    assert cur._orden_dc({"fuente": "docs/… · L"}) > cur._orden_dc({"fuente": "docs/… · L1"})
    assert cur._orden_dc({"fuente": "docs/… · L"}) > cur._orden_dc({"fuente": "docs/… · L16"})
    assert cur._orden_dc({"fuente": "docs/… · M2"}) < cur._orden_dc({"fuente": "docs/… · M10"}), \
        "M10 tiene que ir después de M2: el número se compara como número, no como texto"
    assert cur._orden_dc({}) == ("ZZ", 999), "sin fuente, al final y sin romper"
