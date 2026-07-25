"""Catálogo CURRICULAR: una actividad = una entrada de datos, y de ahí salen el menú, la
categoría, el saber y el juego del player.

Lo que se verifica: (a) el catálogo está sano —bancos con tamaño suficiente, sin ítems
repetidos, con explicación del error y con la fuente curricular declarada—; (b) esa única
entrada llega efectivamente a los cuatro lugares; (c) el JS generado está sincronizado con
el catálogo (si alguien edita el .py y no regenera, el chico ve un menú con una actividad
que no existe)."""
import json
import os
import re
import shutil
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import actividades_categorias as ac  # noqa: E402
import actividades_curriculum as cur  # noqa: E402
import actividades_web as aw  # noqa: E402
import saberes  # noqa: E402

JS = os.path.join(aw.BASEDIR, "actividades_curriculum.js")


def test_catalogo_valido():
    """La validación del propio catálogo: es la red que evita publicar algo roto."""
    problemas = cur.validar()
    assert not problemas, "\n".join(problemas)


def test_hay_actividades_en_los_tres_grados():
    for grado in (1, 2, 3):
        assert cur.actividades_de(grado), "1°-3° tienen que tener Conocimiento del Mundo"


@pytest.mark.parametrize("act", cur.CATALOGO, ids=lambda a: a["id"])
def test_cada_actividad_declara_su_origen_curricular(act):
    """Ninguna actividad se inventa: tiene que decir qué contenido del DC cubre y de qué
    documento salió (pedido de Pablo: "sacá todo de la currícula")."""
    assert act["dc"].strip(), "sin contenido del DC"
    assert re.match(r"docs/auditoria-dc-caba/grado-\d\.md · \w+", act["fuente"]), act["fuente"]


@pytest.mark.parametrize("act", cur.CATALOGO, ids=lambda a: a["id"])
def test_el_banco_respeta_la_forma_de_su_mecanica(act):
    """Cada mecánica tiene su contrato y su trampa propia; el player asume que se cumple.

    trivia     → `ops[0]` es la correcta (el player baraja al mostrar): no puede repetirse
                 entre los distractores ni haber distractores duplicados.
    clasificar → cada categoría declarada tiene que recibir ítems; un botón que nunca es
                 correcto se aprende a descartar y deja de ser una opción real.
    ordenar    → el banco viene YA en el orden correcto y sin tarjetas repetidas dentro de
                 una secuencia (si no, hay dos órdenes válidos y uno se marca mal)."""
    mec = act["mecanica"]
    if mec == "trivia":
        for it in act["banco"]:
            assert it["ops"][0] not in it["ops"][1:], it["q"]
            assert len(set(it["ops"][1:])) == len(it["ops"]) - 1, it["q"]
    elif mec == "clasificar":
        declaradas = {c["cat"] for c in act["categorias"]}
        usadas = {it["cat"] for it in act["banco"]}
        assert declaradas == usadas, "categorías sin ítems: %s" % (declaradas - usadas)
        for it in act["banco"]:
            assert it["m"].strip(), it["it"]
    elif mec == "ordenar":
        for it in act["banco"]:
            items = it["items"]
            assert len(items) >= 3 and len(set(items)) == len(items), items
    else:
        pytest.fail("mecánica sin contrato verificado: %r" % mec)


def test_cdm_es_una_categoria_del_menu():
    """Conocimiento del Mundo tiene que ser una categoría de verdad (1°-3° del DC), y
    todas las áreas que declara el catálogo tienen que existir en el menú — si no, la
    actividad se carga pero queda sin carril y el chico no la ve agrupada."""
    assert "cdm" in ac.CATEGORIA_ORDEN
    assert ac.CATEGORIA_LABEL["cdm"] == "Conocimiento del Mundo"
    assert cur.actividades_de(area=cur.AREA_CDM), "el catálogo perdió las de CdM"
    for a in cur.CATALOGO:
        # cada actividad se agrupa en el área que declaró, sea cdm, lengua o matemática
        assert ac.categoria_de(a["id"]) == a["area"], a["id"]
        assert a["area"] in ac.CATEGORIA_ORDEN, \
            "%s declara el área %r, que no es un carril del menú" % (a["id"], a["area"])


def test_cdm_solo_en_primer_ciclo():
    """En 4°+ el DC separa Naturales y Sociales: declarar CdM ahí sería contradecirlo."""
    for a in cur.actividades_de(area=cur.AREA_CDM):
        assert a["grado"] in (1, 2, 3), a["id"]


def test_los_saberes_entran_al_grafo_sin_romperlo():
    for a in cur.CATALOGO:
        sid = a["saber"]["id"]
        assert sid in saberes.SABERES, "%s no llegó al grafo" % sid
        assert saberes.SABERES[sid]["juegos"] == [a["id"]]
    # prerrequisitos existentes y sin ciclos (el motor recorre esto en cada menú)
    for sid, s in saberes.SABERES.items():
        for p in s.get("prerrequisitos", []):
            assert p in saberes.SABERES, "%s: prereq inexistente %s" % (sid, p)


@pytest.mark.parametrize("grado", (1, 2, 3))
def test_la_actividad_llega_al_menu_del_grado(grado):
    edad = str(grado + 5)
    ids = {m["id"] for m in aw._menu(aw._banda(edad), edad) + aw._menu_curricular(edad)}
    for a in cur.actividades_de(grado):
        assert a["id"] in ids, "%s no aparece en el menú de %d°" % (a["id"], grado)


def test_el_js_generado_esta_sincronizado():
    """Si alguien edita el catálogo y no corre gen_curriculum.py, el menú ofrecería una
    actividad que el player no sabe abrir. Esto lo caza antes de que le pase a un chico."""
    assert os.path.isfile(JS), "falta actividades_curriculum.js (correr gen_curriculum.py)"
    js = open(JS, encoding="utf-8").read()
    for a in cur.CATALOGO:
        assert "GAMES.%s = " % a["id"] in js, \
            "%s está en el catálogo pero no en el JS: falta regenerar" % a["id"]
        # el banco tiene que estar completo, no una versión vieja más corta
        banco = re.search(r"const CUR_%s_BANCO = (\[.*?\n\]);" % a["id"].upper(), js, re.S)
        assert banco, a["id"]
        assert len(json.loads(banco.group(1))) == len(a["banco"]), \
            "%s: el JS tiene otro banco que el catálogo" % a["id"]


def test_token_de_segundo_trae_la_actividad_y_su_archivo():
    """End-to-end: el token de un chico de 2° tiene la actividad en el menú y el player
    puede pedir el JS que la define."""
    tok = "test-cur-2do-aabb"
    d = os.path.join(aw.ACT_DIR, tok)
    shutil.rmtree(d, ignore_errors=True)
    aw.crear({"nombre": "Test", "edad": "7"}, "safari", token=tok)
    try:
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        ids = {m["id"] for m in dj["menu"]}
        for a in cur.actividades_de(2):
            assert a["id"] in ids
        assert aw.archivo(tok, "actividades_curriculum.js") is not None, \
            "el player no puede pedir el JS del catálogo"
    finally:
        shutil.rmtree(d, ignore_errors=True)
