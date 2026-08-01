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
    elif mec == "parametrica":
        # no tiene banco: el contrato es que la plantilla GENERE ejercicios válidos y
        # variados. Se simula de verdad, con las mismas guardas que el player.
        pl = act["plantilla"]
        ejercicios = {cur._simular(pl) for _ in range(600)} - {None}
        assert len(ejercicios) >= 20, \
            "%s: sólo %d ejercicios distintos" % (act["id"], len(ejercicios))
    elif mec == "manipular":
        # tampoco tiene banco: el contrato es que con esas piezas se pueda armar una
        # variedad real de objetivos, y que el chico llegue a cada uno tocando `cuantas`.
        # Se verifica combinando de verdad, no confiando en la declaración.
        import itertools
        pl = act["plantilla"]
        n = pl.get("cuantas", 2)
        objetivos = {sum(c) for c in itertools.combinations_with_replacement(pl["piezas"], n)}
        assert len(objetivos) >= 8, \
            "%s: sólo %d objetivos distintos" % (act["id"], len(objetivos))
        assert all(isinstance(v, int) and v > 0 for v in pl["piezas"]), act["id"]
        assert pl.get("m"), "%s: sin explicación al errar" % act["id"]
    elif mec == "reusa":
        # No tiene contenido propio: REUSA un juego del player, que es donde vive su
        # contrato. Lo único que hay que verificar acá es que ese juego EXISTA — si no, la
        # tarjeta aparece en el menú y no abre, que es el peor síntoma porque no da error.
        # (Nació el 31-jul-2026 para que la resta de 4.º use la misma resta en columnas
        # que 3.º con otro rango, en vez de un segundo juego que haga lo mismo.)
        assert act.get("juego"), "%s: reusa sin decir qué juego" % act["id"]
        player = open(os.path.join(aw.BASEDIR, "actividades_player.js"), encoding="utf-8").read()
        assert "GAMES.%s = {" % act["juego"] in player, \
            "%s: reusa 'GAMES.%s', que no existe en el player" % (act["id"], act["juego"])
        assert not act.get("banco") and not act.get("plantilla"), \
            "%s: reusa un juego Y trae contenido propio; uno de los dos sobra" % act["id"]
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
        if a["mecanica"] == "reusa":
            # no emite ni banco ni plantilla: delega en un juego que ya existe
            assert "GAMES.%s = { crear(ctx) { return GAMES.%s.crear(ctx); } };" % (
                a["id"], a["juego"]) in js, \
                "%s: el JS no delega en %s" % (a["id"], a["juego"])
            continue
        if a["mecanica"] in ("parametrica", "manipular"):
            # emiten la PLANTILLA, no un banco; tiene que ser la misma que el catálogo.
            # El sufijo difiere porque cada emisor nombra su constante distinto.
            suf = "PLANTILLA" if a["mecanica"] == "parametrica" else "PIEZAS"
            pl = re.search(r"const CUR_%s_%s = (\{.*?\n\});" % (a["id"].upper(), suf),
                           js, re.S)
            assert pl, a["id"]
            assert json.loads(pl.group(1)) == a["plantilla"], \
                "%s: la plantilla del JS quedó vieja" % a["id"]
            continue
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


# ── el tope del "¿qué ven en la escuela?" es una decisión de NEGOCIO ─────────────
def _token_de(edad, tok):
    d = os.path.join(aw.ACT_DIR, tok)
    shutil.rmtree(d, ignore_errors=True)
    aw.crear({"nombre": "Test", "edad": edad}, "safari", token=tok)
    return d


def test_solo_se_puede_sumar_de_grados_adyacentes():
    """El desbloqueo por materia vende "el nivel siguiente". Si el padre pudiera sumar de
    cualquier grado, se llevaría gratis lo que está en venta — y en las materias flacas
    (5° Lengua tiene 3 actividades, 6° Lengua 1) se llevaría el nivel ENTERO."""
    tok = "test-tope-4to-aabb"
    d = _token_de("9", tok)                     # 4° grado
    try:
        cat = aw.catalogo_actividades()
        pedidos = [{"id": m["id"], "grado": g} for g, v in cat.items() for m in v]
        r = aw.extras_guardar(tok, pedidos)
        grados = {it["grado"] for it in r["items"]}
        assert grados <= {3, 4, 5}, "entraron grados no adyacentes: %s" % (grados - {3, 4, 5})
        # de cada grado adyacente, como mucho 1 por materia
        for g in (3, 5):
            por_materia = {}
            for it in r["items"]:
                if it["grado"] == g:
                    por_materia[it["categoria"]] = por_materia.get(it["categoria"], 0) + 1
            demas = {k: v for k, v in por_materia.items() if v > aw.EXTRAS_TOPE_ADYACENTE}
            assert not demas, "%d° superó el tope por materia: %s" % (g, demas)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_lo_rechazado_del_grado_siguiente_se_ofrece_para_comprar():
    """El tope no puede ser un "no" seco: lo que no entra del año que viene es la oferta
    (pedido de Pablo: "decime pudiste 2 materias y el resto las podés comprar")."""
    tok = "test-tope-ofer-aabb"
    d = _token_de("9", tok)
    try:
        cat = aw.catalogo_actividades()
        # pide TODO lo de 5°: sólo puede entrar 1 por materia, el resto tiene que ofrecerse
        pedidos = [{"id": m["id"], "grado": 5} for m in cat[5]]
        r = aw.extras_guardar(tok, pedidos)
        comprables = [x for x in r["rechazadas"] if x.get("comprable")]
        assert comprables, "no ofrece comprar nada de lo que rechazó"
        for x in comprables:
            assert x.get("materia"), "sin materia: la tienda no sabe qué desbloquear"
            assert x.get("motivo"), "sin motivo visible para el padre"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_del_grado_anterior_no_se_ofrece_comprar():
    """Lo del año pasado es repaso: no está en venta, así que no puede empujar una compra."""
    tok = "test-tope-ant-aabb"
    d = _token_de("9", tok)
    try:
        cat = aw.catalogo_actividades()
        pedidos = [{"id": m["id"], "grado": 3} for m in cat[3]]
        r = aw.extras_guardar(tok, pedidos)
        for x in r["rechazadas"]:
            assert not x.get("comprable"), "ofrece comprar algo del año pasado: %s" % x
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_lo_comprado_entra_sin_tope_ni_limite_de_grado():
    """Una actividad PAGADA ($1000, decisión de Pablo 25-jul) no cuenta contra el cupo
    gratis ni mira el grado: si la pagó, entra. Si no, el padre paga y no recibe."""
    tok = "test-compra-aabb"
    d = _token_de("9", tok)                       # 4° grado
    try:
        cat = aw.catalogo_actividades()
        leng5 = [m["id"] for m in cat[5] if m.get("categoria") == "lengua"]
        assert len(leng5) >= 3, "hace falta contenido de Lengua de 5° para este test"
        pedidos = [{"id": i, "grado": 5} for i in leng5]
        # sin comprar: entra 1 sola (el cupo gratis del grado siguiente)
        libre = aw.extras_guardar(tok, pedidos)
        assert len([x for x in libre["items"] if x["grado"] == 5]) == aw.EXTRAS_TOPE_ADYACENTE
        # comprando 2: entran las 2 pagadas ADEMÁS de la gratis
        pagadas = [{"id": leng5[1], "grado": 5}, {"id": leng5[2], "grado": 5}]
        r = aw.extras_guardar(tok, pedidos, compradas=pagadas)
        de5 = [x for x in r["items"] if x["grado"] == 5]
        assert len(de5) == aw.EXTRAS_TOPE_ADYACENTE + 2, [x["id"] for x in de5]
        assert sum(1 for x in de5 if x["origen"] == "comprada") == 2
        # una comprada de un grado LEJANO también entra: la pagó
        lejana = [{"id": cat[7][0]["id"], "grado": 7}]
        r2 = aw.extras_guardar(tok, lejana, compradas=lejana)
        assert len(r2["items"]) == 1 and r2["items"][0]["origen"] == "comprada"
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ── ningún juego del menú puede faltar en el player ──────────────────────────────
def _games_definidos():
    """Ids que el player registra, en cualquiera de sus dos archivos."""
    ids = set()
    for f in ("actividades_player.js", "actividades_curriculum.js"):
        try:
            src = open(os.path.join(aw.BASEDIR, f), encoding="utf-8").read()
        except OSError:
            continue
        ids |= set(re.findall(r"GAMES\.(\w+)\s*=", src))
    return ids


@pytest.mark.parametrize("edad", [str(e) for e in range(6, 13)])
def test_todo_juego_del_menu_existe_en_el_player(edad):
    """Una carta que el player no sabe abrir es una actividad muerta en el cuaderno.

    Pasó de verdad (25-jul): borrando bancos muertos, una regex se comió `GAMES.reloj` y
    `GAMES.transportador` enteros — el banco del transportador estaba declarado en UNA
    línea y el patrón siguió hasta el `];` del array siguiente. Quedaron en el menú de
    2°, 3° y 5° cartas que no abrían nada, y ningún test lo notó."""
    definidos = _games_definidos()
    menu = aw._menu(aw._banda(edad), edad) + aw._menu_curricular(edad)
    faltan = sorted({m["id"] for m in menu} - definidos)
    assert not faltan, "el menú de %s años ofrece juegos inexistentes: %s" % (edad, faltan)


def test_todo_juego_del_grafo_existe_en_el_player():
    """Lo mismo para el grafo de saberes: el motor no puede recomendar lo que no existe."""
    definidos = _games_definidos()
    faltan = set()
    for sid, s in saberes.SABERES.items():
        for j in s.get("juegos", []):
            if j not in definidos:
                faltan.add("%s (%s)" % (j, sid))
    assert not faltan, "el grafo apunta a juegos inexistentes: %s" % sorted(faltan)


@pytest.mark.parametrize("grado", list(range(1, 8)))
def test_ningun_saber_del_grado_queda_sin_juego_en_el_menu(grado):
    """Un saber del grado cuyos juegos no están en el menú de ese grado NO se puede dominar.

    El motor da un saber por dominado con CUALQUIERA de sus juegos (`saberDominado` usa
    `.some()`), así que alcanza con que uno esté en el menú. Si no está ninguno, el saber
    queda pendiente para siempre: no rompe nada visible en el cuaderno del chico —el
    recomendador elige sólo entre las cartas del menú—, pero infla el denominador del
    panel de padres y baja el techo del 80% que dispara la oferta de la materia.

    Pasó de verdad (25-jul): `NAT-3-MEZCLAS` apuntaba sólo a `separador_mezclas`, que
    había salido del menú de 3° al reemplazarlo por `estados_materia`. Naturales de 3°
    no podía llegar a 100% aunque el chico hiciera todo."""
    edad = str(grado + 5)
    menu = {m["id"] for m in aw._menu(aw._banda(edad), edad) + aw._menu_curricular(edad)}
    huerfanos = sorted(
        "%s (%s)" % (sid, ", ".join(s.get("juegos", [])) or "sin juegos")
        for sid, s in saberes.SABERES.items()
        if s.get("grado") == grado and not (set(s.get("juegos", [])) & menu)
    )
    assert not huerfanos, (
        "saberes de %d° que ningún juego del menú puede dominar: %s" % (grado, huerfanos))


@pytest.mark.parametrize("grado", list(range(1, 8)))
def test_todo_saber_del_grado_llega_al_panel_de_padres(grado):
    """Un saber cuyo primer juego no tiene categoría es INVISIBLE para el padre.

    `saberCategoria()` resuelve la categoría por el PRIMER juego del saber y devuelve
    null si no la encuentra; `resumenPorCategoria()` saltea los null. Ese saber no suma
    ni al dominado ni al total, así que el tablero miente en los dos sentidos: muestra
    menos de lo que el chico hizo y, al achicar el denominador, dispara antes el 80% de
    dominio que ofrece la materia.

    Pasó de verdad (25-jul): el merge del catálogo curricular vivía sólo dentro de
    `categoria_de()`, y `gen_motor_adaptativo.py` vuelca el dict `CATEGORIA` crudo. Los
    34 juegos del catálogo —los 12 de Conocimiento del Mundo incluidos— quedaron sin
    categoría en el player: 10 de los 22 saberes de 2° no figuraban en el panel."""
    cat = ac.CATEGORIA
    ciegos = sorted(
        "%s (%s)" % (sid, (s.get("juegos") or ["sin juegos"])[0])
        for sid, s in saberes.SABERES.items()
        if s.get("grado") == grado and (not s.get("juegos") or s["juegos"][0] not in cat)
    )
    assert not ciegos, (
        "saberes de %d° que no llegan al panel de padres: %s" % (grado, ciegos))


def test_el_motor_generado_categoriza_todos_los_juegos():
    """El JS que se sirve tiene que traer las categorías, no sólo tenerlas el .py.

    Es el eslabón que falló: `CATEGORIA` estaba incompleto en el módulo, así que el
    generado salió con 142 de 176 juegos y nadie lo notó."""
    src = open(os.path.join(aw.BASEDIR, "motor_adaptativo.js"), encoding="utf-8").read()
    cat_js = json.loads(re.search(r"CATEGORIA_JUEGO\s*=\s*(\{.*?\});", src, re.S).group(1))
    faltan = sorted(set(_games_definidos()) - set(cat_js))
    assert not faltan, "juegos sin categoría en el motor servido: %s" % faltan
