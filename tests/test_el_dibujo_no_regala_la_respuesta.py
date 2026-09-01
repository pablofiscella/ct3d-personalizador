# -*- coding: utf-8 -*-
"""En NINGÚN banco el dibujo de una opción puede regalar la respuesta.

14/15-ago-2026. Vestir las respuestas con dibujo es para que un chico que todavía no lee
pueda elegir. Mal hecho, es un atajo para acertar sin saber nada — y me comí las dos formas
de arruinarlo antes de encontrar la regla:

1. **El mismo emoji en la pregunta y en la correcta.** «🍋 Un limón es…» → «🍋 ácido». Se gana
   emparejando dibujitos.
2. **Vestir sólo algunas.** Al saltear las chivatas, la correcta quedaba como la ÚNICA sin
   dibujo — un chivato peor, porque se ve de un vistazo.

La regla es **todas o ninguna, y ninguna si el emoji ya está en la pregunta**.

POR QUÉ ESTE ARCHIVO MIRA TODOS LOS BANCOS Y NO EL QUE TOQUÉ
─────────────────────────────────────────────────────────────
El primer guardián miraba sólo «Los cinco sentidos», que es donde había trabajado. Pero la
trampa no es de ese banco: es de cualquiera que mezcle emoji en la pregunta y en las
opciones, y hay 4.201 ítems repartidos en 325 actividades. Un guardián acotado a lo que uno
tocó sólo prueba que uno no se equivocó hoy.

OJO CON DÓNDE SE ARREGLA: `actividades_curriculum.js` está GENERADO por `gen_curriculum.py`.
La fuente es `actividades_curriculum.py`.
"""
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Flechas, símbolos, dingbats, figuras y emoji modernos. El primer clasificador que escribí
# se perdía las flechas (U+2190-21FF, U+2B00-2BFF) y por eso daba 17 actividades «sin dibujo»
# que ya lo tenían: «⬆️ Avanzar» contaba como texto pelado.
EMO = re.compile("[←-⇿⌀-➿⬀-⯿️"
                 "\U0001F300-\U0001FAFF]")


def _bancos():
    """Cada (id de actividad, pregunta, opciones) del catálogo y del player.

    El catálogo se IMPORTA y se recorre como datos. La primera versión de este archivo lo
    leía con una expresión regular sobre el fuente y encontraba 774 ítems de los 4.201 que
    declara el generador: los bancos largos tienen corchetes adentro y el patrón cortaba en
    el primero. Lo cazó el test de control, que existe justamente para eso — sin él, los
    otros dos habrían pasado en verde revisando el 18 % del catálogo y pareciendo completos.
    """
    import sys
    if RAIZ not in sys.path:
        sys.path.insert(0, RAIZ)
    salida = []
    try:
        import actividades_curriculum as cur
        for act in cur.CATALOGO:
            for it in act.get("banco", []) or []:
                if isinstance(it, dict) and it.get("ops"):
                    salida.append((act.get("id", "?"), str(it.get("q", "")), list(it["ops"])))
    except Exception:                      # el catálogo no está: se revisa el player igual
        pass
    js = os.path.join(RAIZ, "actividades_player.js")
    s = open(js, encoding="utf-8").read()
    for m in re.finditer(r'\{ q: "([^"]*)",\s*ops: \[([^\]]*)\]', s):
        salida.append(("player", m.group(1), re.findall(r'"([^"]+)"', m.group(2))))
    return salida


def test_HAY_bancos_que_revisar():
    """El control: si cambia el formato y este archivo deja de encontrar ítems, pasaría en
    verde sin mirar nada."""
    b = _bancos()
    assert len(b) > 3000, "sólo encontré %d ítems de banco: revisar el patrón" % len(b)


def test_el_emoji_de_la_correcta_NO_esta_en_la_pregunta():
    """Si el dibujo que lleva la respuesta correcta ya aparece en la pregunta, el ejercicio
    se gana emparejando dibujitos."""
    malos = []
    for act, q, ops in _bancos():
        if not ops:
            continue
        en_q = set(EMO.findall(q))
        de_ok = EMO.findall(ops[0])
        if de_ok and de_ok[0] in en_q:
            malos.append("%s · «%s» → «%s»" % (act, q[:34], ops[0][:22]))
    assert not malos, (
        "el dibujo de la opción correcta ya está en la pregunta:\n  " + "\n  ".join(malos[:8]))


def test_o_TODAS_las_opciones_tienen_dibujo_o_NINGUNA():
    """Si la correcta es la única con dibujo —o la única sin— se elige por descarte visual,
    que es exactamente lo contrario de lo que el dibujo vino a hacer."""
    mezclados = []
    for act, q, ops in _bancos():
        if len(ops) < 2:
            continue
        con = [bool(EMO.search(o)) for o in ops]
        if len(set(con)) > 1:
            mezclados.append("%s · %s" % (act, " | ".join(o[:16] for o in ops)))
    assert not mezclados, (
        "hay ítems donde unas opciones llevan dibujo y otras no:\n  "
        + "\n  ".join(mezclados[:8]))
