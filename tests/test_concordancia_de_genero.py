# -*- coding: utf-8 -*-
"""Lo que completa el chico tiene que concordar en género con la frase.

Pablo, jugando el cuaderno de 7.º el 30-jul-2026: *"en homófonos una pregunta tenía una
respuesta en masculino y era femenino"*. Era esta:

    «Completá: Ya está … la tarea.»  →  respondía **hecho**

«La tarea» es femenino: va **hecha**. El par hecha/echa sirve igual como homófono, así que
se corrigió el género sin perder el contenido.

POR QUÉ NO LA ENCONTRÉ AL PRIMER INTENTO, que es lo que este test viene a arreglar: barrí
las 4.201 preguntas del catálogo y no estaba, porque **esta actividad vive en
`actividades_player.js`, no en `actividades_curriculum.py`**, y usa otro formato —
`{q, ok, d}` en vez de `{q, ops}`—. Mi primer barrido buscaba `ops:` y pasó de largo 184
preguntas con hueco. Las dos fuentes se revisan acá.

CÓMO DECIDE, y por qué es tan estrecho. Sólo mira el caso indiscutible: un verbo
COPULATIVO, después el hueco, después determinante + sustantivo — «Ya está … la tarea».
Ahí lo que completa es un adjetivo o participio y tiene que concordar, sin discusión.

Sin la copula el chequeo se llena de falsos positivos: en «Se ___ el pelo todas las
mañanas» la respuesta es «ata», que termina en -a y NO es femenino sino un verbo
conjugado. Un guardián que grita por eso se termina apagando, así que prefiere callarse
antes que inventar. Las palabras que no siguen la regla -o/-a (`la mano`, `el día`,
`el agua`) están en las excepciones; si aparece un falso positivo se agrega ahí.
"""
import os
import re
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import actividades_curriculum as cur  # noqa: E402

PLAYER = os.path.join(_BASE, "actividades_player.js")

ART = {"el": "m", "la": "f", "los": "m", "las": "f", "un": "m", "una": "f",
       "unos": "m", "unas": "f", "este": "m", "esta": "f", "ese": "m", "esa": "f",
       "mucho": "m", "mucha": "f", "otro": "m", "otra": "f"}

# Sustantivos que NO siguen la regla -o/-a. Si un test falla por una palabra correcta que
# falta acá, se suma; nunca se relaja el chequeo.
EXCEPCIONES = {
    "mano": "f", "foto": "f", "moto": "f", "radio": "f", "agua": "f", "asta": "f",
    "águila": "f", "aguila": "f", "hacha": "f", "alma": "f", "aula": "f", "área": "f",
    "día": "m", "dia": "m", "mapa": "m", "problema": "m", "tema": "m", "sistema": "m",
    "planeta": "m", "clima": "m", "idioma": "m", "programa": "m", "poeta": "m",
    "sofá": "m", "tranvía": "m",
}


def _genero(palabra):
    """Género por la terminación, o None si la palabra no lo marca."""
    w = (palabra or "").lower().strip(" .,;:!¡?¿«»\"'…")
    if w in EXCEPCIONES:
        return EXCEPCIONES[w]
    if w.endswith(("as", "os")):
        return None                      # plural: lo mira otro chequeo, no éste
    if w.endswith("a"):
        return "f"
    if w.endswith("o"):
        return "m"
    return None


# Verbos que piden un adjetivo o participio detrás: son los que hacen que la
# concordancia sea obligatoria y no opinable.
COPULA = r"(?:est[áa]n?|estaba[n]?|es|son|era[n]?|fue(?:ron)?|qued[óo]|quedaron|parece[n]?|resulta)"


def _revisar(q, correcta):
    """Devuelve el motivo del desacuerdo, o None si está bien (o no aplica)."""
    d = re.search(COPULA + r"\s+(?:…|_{2,})\s*,?\s*"
                  r"(el|la|los|las|un|una|unos|unas|este|esta|ese|esa)\s+(\w+)",
                  q or "", re.I)
    if not d:
        return None
    art, sustantivo = d.group(1).lower(), d.group(2)
    g_sus = _genero(sustantivo)
    g_resp = _genero(correcta)
    if not g_sus or not g_resp or g_sus == g_resp:
        return None
    if g_resp == ART[art]:               # concuerda con el determinante: no es error
        return None
    return "«%s %s» es %s y la respuesta «%s» es %s" % (
        art, sustantivo, "femenino" if g_sus == "f" else "masculino",
        correcta, "femenino" if g_resp == "f" else "masculino")


def _items_del_catalogo():
    for a in cur.CATALOGO:
        for i, it in enumerate(a.get("banco") or [], 1):
            ops = it.get("ops") or []
            if ops:
                yield ("%s ítem %d" % (a["id"], i), it.get("q") or "", ops[0])


def _items_del_player():
    """Los bancos escritos a mano en el player, en su formato `{q, ok, d}`."""
    with open(PLAYER, encoding="utf-8") as f:
        src = f.read()
    pat = re.compile(r'\{\s*q:\s*"((?:[^"\\]|\\.)*)"\s*,\s*ok:\s*"((?:[^"\\]|\\.)*)"')
    for n, m in enumerate(pat.finditer(src), 1):
        yield ("player #%d" % n, m.group(1), m.group(2))


def test_el_catalogo_concuerda_en_genero():
    malas = [(d, q, c, por) for d, q, c in _items_del_catalogo()
             if (por := _revisar(q, c))]
    assert not malas, "\n".join("  %s: «%s» → %s — %s" % m for m in malas)


def test_los_bancos_del_player_concuerdan_en_genero():
    """EL que faltaba. La pregunta que encontró Pablo estaba acá, no en el catálogo."""
    malas = [(d, q, c, por) for d, q, c in _items_del_player()
             if (por := _revisar(q, c))]
    assert not malas, "\n".join("  %s: «%s» → %s — %s" % m for m in malas)


def test_la_tarea_esta_hecha_no_hecho():
    """Caso testigo, para que no vuelva con otro nombre."""
    with open(PLAYER, encoding="utf-8") as f:
        src = f.read()
    assert 'q: "Completá: Ya está … la tarea.", ok: "hecha"' in src, \
        "volvió el «hecho» con «la tarea»"
    assert '"Completá: Ya está … la tarea.", ok: "hecho"' not in src


def test_el_chequeo_detecta_de_verdad():
    """Un guardián que no puede fallar no sirve: se le pasa el error original."""
    # el error real que encontró Pablo
    assert _revisar("Completá: Ya está … la tarea.", "hecho")
    assert _revisar("El postre está … la torta.", "frío")
    # y NO grita con lo que está bien
    assert _revisar("Completá: Ya está … la tarea.", "hecha") is None
    # ni con un verbo conjugado que sólo termina en -a (el falso positivo que lo motivó)
    assert _revisar("Se ___ el pelo todas las mañanas.", "ata") is None
    # ni con los sustantivos que no siguen la regla -o/-a
    assert _revisar("Ya está … la mano derecha.", "sucia") is None
    assert _revisar("Ya está … el día.", "terminado") is None
