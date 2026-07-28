"""Cuántas actividades del cuaderno escolar SUBEN de dificultad cuando el chico domina.

Los niveles del cuaderno son escalones de dificultad del MISMO tema (decisión del
25-jul-2026: ningún contenido del Diseño Curricular detrás de un candado). Para que eso
sea verdad y no un cartel, la actividad tiene que ponerse efectivamente más difícil — si
no, "Nivel 3" es una etiqueta que miente.

Este test mide la cobertura real leyendo el player y fija un piso, para que no retroceda
sin que nadie se entere. Medido el 28-jul-2026: 128 de 136 (venía de 102).

Cómo se cuenta: una actividad escala si su cuerpo (o el de la FÁBRICA que la genera, tipo
`juegoTriviaBanco`) usa alguna de las palancas de dificultad. Se recorta el cuerpo contando
llaves de verdad — partir por `\\nGAMES.` daba bloques mezclados y contaba juegos de más.
"""
import os
import re
import sys

import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
import actividades_web as A  # noqa: E402

PLAYER = os.path.join(BASE, "actividades_player.js")

# Las palancas: las tres del ctx + los helpers que las consultan por dentro.
PALANCAS = ("nivelDif", "bonusDominio", "difPiso",
            "_masDificil", "_filtrarPorDominio", "_ordenPorDominio")

# Piso medido el 28-jul-2026. Subilo cuando cubras más; nunca lo bajes para "arreglar" el test.
PISO = 128

# Actividades sin gradiente honesto: son de UN concepto (¿conduce o no?, ¿qué órgano sigue?)
# y no hay forma de hacerlas más difíciles sin inventar dificultad falsa. En estas la
# adaptación la da el GRAFO —cuándo se ofrecen—, no la dificultad interna.
SIN_GRADIENTE = {
    "camino_digestivo",       # el orden del aparato digestivo es siempre el mismo
    "colorear",               # pintar: no tiene dificultad
    "programar_camino",       # el camino ya viene dado por el nivel
    "linea_democracia",       # una línea de tiempo fija
    "planta_potabilizadora",  # las etapas son las que son
    "viaje_inmigrante",       # ídem
    "puntos",                 # unir puntos de una figura
    "suma_rapida",            # el objetivo es 10 FIJO: la consigna GRABADA dice "10"
}


def _cuerpo_por_llaves(src, desde):
    """El bloque {...} que arranca en `desde`, contando llaves y salteando strings,
    comentarios y template literals."""
    i = src.find("{", desde)
    if i < 0:
        return ""
    d, j, n = 0, i, len(src)
    while j < n:
        c = src[j]
        if c in "\"'`":
            q = c
            j += 1
            while j < n and src[j] != q:
                if src[j] == "\\":
                    j += 1
                j += 1
        elif c == "/" and j + 1 < n and src[j + 1] == "/":
            j = src.find("\n", j)
            if j < 0:
                break
        elif c == "/" and j + 1 < n and src[j + 1] == "*":
            j = src.find("*/", j) + 1
            if j <= 0:
                break
        elif c == "{":
            d += 1
        elif c == "}":
            d -= 1
            if d == 0:
                return src[i:j + 1]
        j += 1
    return ""


@pytest.fixture(scope="module")
def escalan():
    """{id: bool} para cada actividad de los menús de 1.º a 7.º."""
    src = open(PLAYER, encoding="utf-8").read()
    cuerpos = {m.group(1): _cuerpo_por_llaves(src, m.end() - 1)
               for m in re.finditer(r"GAMES\.([A-Za-z0-9_]+)\s*=\s*\{", src)}
    fabrica = {m.group(1): m.group(2) for m in
               re.finditer(r"GAMES\.([A-Za-z0-9_]+)\s*=\s*([a-zA-Z_][A-Za-z0-9_]*)\(", src)}
    cuerpo_fab = {}
    for f in set(fabrica.values()):
        m = re.search(r"function %s\s*\(" % re.escape(f), src)
        cuerpo_fab[f] = _cuerpo_por_llaves(src, m.end()) if m else ""

    ids = sorted({it["id"] for e in range(6, 13) for it in A._menu(A._banda(e), e)})
    out = {}
    for i in ids:
        cuerpo = cuerpos.get(i) or cuerpo_fab.get(fabrica.get(i, ""), "")
        out[i] = any(p in cuerpo for p in PALANCAS)
    return out


def test_todas_las_actividades_del_menu_existen_en_el_player(escalan):
    """Si una actividad está en el menú y no en el player, el chico ve una carta que no abre."""
    assert escalan, "no se pudo leer ninguna actividad"


def test_la_cobertura_de_dificultad_no_retrocede(escalan):
    suben = sum(1 for v in escalan.values() if v)
    assert suben >= PISO, (
        "la dificultad por dominio retrocedió: %d de %d (el piso es %d). "
        "Si sacaste una palanca a propósito, bajá PISO y decí por qué."
        % (suben, len(escalan), PISO))


def test_las_que_no_escalan_estan_declaradas(escalan):
    """La lista de excepciones tiene que ser explícita: una actividad que no escala y no
    está declarada es un olvido, no una decisión."""
    no_escalan = {i for i, v in escalan.items() if not v}
    sin_declarar = no_escalan - SIN_GRADIENTE
    assert not sin_declarar, (
        "estas no escalan y no están en SIN_GRADIENTE: %s. "
        "O les ponés dificultad, o las declarás con el motivo." % sorted(sin_declarar))


def test_no_sobran_excepciones(escalan):
    """Si una de las declaradas empezó a escalar, sacala de la lista: una excepción que ya
    no aplica esconde el próximo olvido."""
    sobran = {i for i in SIN_GRADIENTE if escalan.get(i)}
    assert not sobran, "ya escalan, sacalas de SIN_GRADIENTE: %s" % sorted(sobran)
