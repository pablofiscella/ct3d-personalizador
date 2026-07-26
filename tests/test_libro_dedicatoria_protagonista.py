"""26-jul-2026 — la hoja del nombre dibujaba a un chico que no era el protagonista.

Pablo, mirando el audiolibro que acababa de comprar: "hay un chico morocho que es un
superheroe que no es el nene o nena protagonista". La página lleva escrito «Este cuento
pertenece a <nombre>» y mostraba a un secundario. Y la misma imagen es la de la MUESTRA
de la ficha, así que estaba también en la vidriera.

Causa: la escena de la dedicatoria pedía "un personaje del tema" —ambiguo—. Cada
temática lo resolvió a su manera: bomberos dibujó al elenco saludando (sirve),
superhéroes eligió un nene secundario distinto al de la portada.

El motor ya tenía la pieza para resolverlo: `_protagonista(genero)`, que además de
elegir nena/nene lo dibuja siempre de espaldas para que funcione con cualquier chico.
La dedicatoria simplemente no lo usaba.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_la_dedicatoria_pide_al_protagonista():
    """LA regresión: si vuelve a pedir 'un personaje' cualquiera, vuelve el bug."""
    import libro_ia
    assert "{protagonista}" in libro_ia._ESCENAS[1], (
        "la escena de la dedicatoria no menciona al protagonista")


def test_la_version_larga_usa_la_misma_escena():
    """El audiolibro usa `_ESCENAS_LARGO`. Comparten el objeto: si alguien las separa,
    hay que acordarse de arreglar las dos."""
    import libro_ia
    assert libro_ia._ESCENAS_LARGO[1] is libro_ia._ESCENAS[1]


def test_el_prompt_resuelve_el_genero_en_la_dedicatoria():
    import libro_ia
    nena = libro_ia.prompt_pagina("superheroes", 1, genero="nena")
    nene = libro_ia.prompt_pagina("superheroes", 1, genero="nene")
    assert "una nena" in nena and "un nene" in nene.replace("una nena", "")
    assert nena != nene, "el género tiene que cambiar el prompt de esta página"


def test_el_protagonista_de_la_dedicatoria_nunca_muestra_la_cara():
    """La convención del libro: el protagonista va de espaldas para que cualquier chico
    se identifique. Si esta página mostrara una cara, volvería a ser 'un chico que no es
    el mío'."""
    import libro_ia
    p = libro_ia.prompt_pagina("superheroes", 1, genero="nena")
    assert "nunca se le ve la cara" in p


def test_el_prompt_no_rompe_en_ningun_tema():
    """`escena.format(**h)` explota con un placeholder que la historia no tenga. La
    dedicatoria usa {mundo}, que HISTORIA_DEFAULT también define."""
    import libro
    import libro_ia
    for tema in sorted(libro.HISTORIAS):
        for g in (None, "nena", "nene"):
            libro_ia.prompt_pagina(tema, 1, genero=g)
    libro_ia.prompt_pagina("tema-que-no-existe", 1)      # cae a HISTORIA_DEFAULT


def test_sin_concordancia_de_genero_rota():
    """El texto no puede llevar participios que concuerden: {protagonista} puede ser
    «una nena…» o «un nene…» y quedaría «una nena … acompañado»."""
    import libro_ia
    escena = libro_ia._ESCENAS[1]
    for palabra in ("acompañado", "solo,", "contento", "listo"):
        assert palabra not in escena, "concordancia de género rota: %r" % palabra
