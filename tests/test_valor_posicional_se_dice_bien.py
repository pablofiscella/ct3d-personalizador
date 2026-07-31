# -*- coding: utf-8 -*-
"""Las columnas del número se llaman unidades, decenas y centenas.

Pablo, 31-jul-2026: *"«Cálculo redondo» en 2.º grado dice cualquier cosa"*.

Escuchando lo que la actividad le manda a la voz —no leyendo el código— apareció esto:

    "Fijate en qué columna sumás: unidades con unidades, DIECES con dieces, CIENES con
     cienes. Da 270."

**"Cienes" no existe en español** (el plural de "cien" es "cientos") y "dieces", aunque se
puede decir, no es como se llama eso: en matemática son **decenas** y **centenas**, que es
justo el vocabulario que el Diseño Curricular de 2.º manda enseñar y el que la maestra usa
en el pizarrón. O sea que la explicación le enseñaba al chico dos palabras inventadas para
nombrar lo único que la actividad tenía que enseñarle.

NO ERA UN CASO SUELTO. Estaba en **11 lugares**: 3 en el catálogo (cálculo redondo de 2.º,
sumas de miles y multiplicación por dos cifras) y 8 en las mini-lecciones del botón "¿Cómo
es?". Y convivía con el vocabulario correcto: el mismo catálogo dice "decena" y "centena"
seis veces cada una en otras actividades.

OJO CON EL ARTÍCULO al corregirlo: es "**los** dieces" pero "**las** decenas". Un
reemplazo a ciegas dejaba "los decenas" en media docena de frases.
"""
import os
import re
import sys

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import actividades_curriculum as cur  # noqa: E402

# Sólo lo que el chico LEE O ESCUCHA. `actividades_cobertura.py` queda afuera a propósito:
# es el manifiesto interno de qué tema del programa cubre cada actividad, y ahí "dieces y
# sueltos" es el nombre del tema tal como lo dice la didáctica de 1.º. Reescribir el
# registro de un documento fuente para que cumpla una regla de redacción sería falsearlo.
FUENTES = [os.path.join(_BASE, f) for f in (
    "actividades_player.js", "actividades_curriculum.py", "actividades_curriculum.js")]

INVENTADAS = re.compile(r"\b(dieces|cienes)\b", re.I)


def test_no_quedan_palabras_inventadas_en_ningun_lado():
    """EL guardián. Se mira el catálogo, el player, el catálogo COMPILADO (que es lo que
    se sirve) y la tabla de cobertura."""
    malos = []
    for f in FUENTES:
        with open(f, encoding="utf-8") as fh:
            for n, linea in enumerate(fh, 1):
                if INVENTADAS.search(linea):
                    malos.append("%s:%d %s" % (os.path.basename(f), n, linea.strip()[:70]))
    assert not malos, "vuelven las palabras inventadas:\n  " + "\n  ".join(malos)


def test_el_calculo_redondo_de_2do_explica_con_las_palabras_del_programa():
    """La que Pablo abrió. Es la actividad que ENSEÑA valor posicional: si la explicación
    no usa el nombre correcto de las columnas, no enseña lo que dice enseñar."""
    a = [x for x in cur.CATALOGO if x["id"] == "calculo_redondo"][0]
    m = a["plantilla"]["m"]
    for palabra in ("unidades", "decenas", "centenas"):
        assert palabra in m, "la explicación no nombra las %s: %r" % (palabra, m)
    assert a["grado"] == 2


def test_el_articulo_quedo_bien():
    """«los dieces» → «las decenas», no «los decenas». Un reemplazo a ciegas dejaba mal
    concordadas media docena de frases, y suenan raro justo en la actividad que enseña
    a nombrarlas."""
    malos = []
    for f in FUENTES:
        txt = open(f, encoding="utf-8").read()
        for m in re.finditer(r"\blos\s+(decenas|centenas)\b", txt):
            malos.append("%s: «los %s»" % (os.path.basename(f), m.group(1)))
    assert not malos, "concordancia rota: %s" % malos


def test_el_vocabulario_es_el_mismo_en_todo_el_cuaderno():
    """El motivo por el que esto se notaba: el resto del material YA decía decenas y
    centenas. La actividad de 2.º era la que hablaba distinto."""
    n = 0
    for a in cur.CATALOGO:
        textos = [a.get("consigna")] + [b.get("m") for b in (a.get("banco") or [])
                                        if isinstance(b, dict)]
        if a.get("plantilla"):
            textos += [a["plantilla"].get("m"), a["plantilla"].get("q")]
        n += sum(1 for t in textos if t and ("decena" in t.lower() or "centena" in t.lower()))
    assert n >= 12, "el vocabulario correcto retrocedió a %d menciones" % n


def test_las_cuentas_de_calculo_redondo_siguen_dando_bien():
    """No-regresión de lo que SÍ estaba bien: se verificaron 8 rondas reales en el
    navegador y las tres opciones eran enteras y correctas. Lo que fallaba era el texto,
    no la matemática, y arreglar el texto no puede tocar la plantilla."""
    pl = [x for x in cur.CATALOGO if x["id"] == "calculo_redondo"][0]["plantilla"]
    assert pl["q"] == "{a} + {b}" and pl["ok"] == "a + b"
    assert pl["vars"]["b"]["opciones"] == [1, 10, 100], \
        "el DC de 2.º pide sumar y restar 1, 10 y 100"
    assert pl["vars"]["a"]["rango"] == [110, 880] and pl["vars"]["a"]["paso"] == 10
    assert pl["tope"] == 1000
