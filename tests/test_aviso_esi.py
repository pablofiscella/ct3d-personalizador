"""El aviso de ESI a la familia.

Pedido explícito de la maestra en la auditoría de 6°: "evitar la sorpresa de 'ciclo
menstrual' y 'métodos' sin aviso". El contenido de Educación Sexual Integral es
currícula obligatoria (Ley 26.150) y por eso NO se oculta ni se gatea — pero la
familia tiene que poder verlo venir.

Lo que se verifica acá es la parte que se puede romper en silencio: que toda actividad
marcada como ESI en el manifiesto esté declarada en el player. Si mañana alguien agrega
un tema de ESI a un grado y se olvida del aviso, esto falla.
"""
import os
import re

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER = open(os.path.join(BASEDIR, "actividades_player.js"), encoding="utf-8").read()


def _esi_del_player():
    i = PLAYER.index("const ESI_IDS = new Set([")
    return set(re.findall(r'"([a-z0-9_]+)"', PLAYER[i:PLAYER.index("]);", i)]))


def _esi_del_manifiesto():
    import actividades_cobertura as c
    ids = set()
    for grado in c.DC:
        for t in c.temas(grado):
            if "ESI" not in t["tema"] and "(ESI)" not in t["dc"]:
                continue
            cubre = t["cubre"] if isinstance(t["cubre"], list) else [t["cubre"]]
            ids.update(a for a in cubre if a)
    return ids


def test_todo_tema_esi_del_manifiesto_tiene_aviso():
    """Un tema de ESI sin aviso es exactamente la sorpresa que hay que evitar."""
    faltan = sorted(_esi_del_manifiesto() - _esi_del_player())
    assert not faltan, ("estas actividades son ESI en el manifiesto y no están en "
                        "ESI_IDS del player: %s" % faltan)


def test_el_aviso_no_declara_actividades_muertas():
    """Si una entrada de ESI_IDS ya no corresponde a ningún juego, la marca 👪 no se
    pinta nunca y la lista deja de significar algo."""
    import actividades_curriculum as ac
    conocidos = {a["id"] for a in ac.CATALOGO}
    # `sistema_reproductor` es un juego base de 7°, no una entrada del catálogo
    conocidos.add("sistema_reproductor")
    muertas = sorted(_esi_del_player() - conocidos)
    assert not muertas, "ESI_IDS declara ids que no existen: %s" % muertas


def test_el_aviso_no_bloquea_la_actividad():
    """Avisar no es censurar: la nota tiene que dejar seguir al juego.

    Si alguien la convierte en una compuerta, el contenido curricular obligatorio queda
    detrás de un candado — justo lo que la regla de cobertura prohíbe."""
    i = PLAYER.index("function notaESI(")
    cuerpo = PLAYER[i:i + 3000]
    assert "alContinuar()" in cuerpo, "la nota no continúa al juego después de leerla"
    assert "Empezar" in cuerpo, "falta el botón que sigue a la actividad"


def test_la_nota_nombra_la_ley_y_donde_consultar():
    """Las dos cosas que la vuelven útil para la familia: que entienda que es currícula
    oficial (y no una decisión del producto) y adónde ir con una duda."""
    i = PLAYER.index("function notaESI(")
    cuerpo = PLAYER[i:i + 3000]
    assert "26.150" in cuerpo, "la nota no cita la ley de ESI"
    assert "centro de salud" in cuerpo, "la nota no dice dónde consultar"


def test_el_aviso_aparece_en_las_dos_ramas_del_menu():
    """Las actividades curriculares se muestran con y sin motor adaptativo, así que el
    aviso tiene que estar ANTES de que el menú se bifurque."""
    i = PLAYER.index("function pintarMenuPlano(")
    cuerpo = PLAYER[i:i + 6000]
    pos_aviso = cuerpo.index("esi-aviso")
    pos_rama = cuerpo.index("if (adaptOn) {")
    assert pos_aviso < pos_rama, ("el aviso se pinta dentro de una sola rama del menú: "
                                  "el otro camino queda sin avisar")
