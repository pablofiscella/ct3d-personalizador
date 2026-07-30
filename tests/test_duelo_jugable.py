"""El duelo, del lado del chico: la pantalla, el pozo de preguntas y dónde aparece.

`duelos.py` (y su test) cubren el motor: guardar la partida, el código, que no entre un
tercero. Acá se prueba lo otro — lo que hasta el 30-jul-2026 no existía y hacía que el
duelo, estando entero por dentro, fuera injugable: no había pantalla.

Se evalúa el JS REAL con node, incluido el catálogo curricular entero, porque lo que más
puede fallar no es la lógica sino el DATO: que un grado no tenga preguntas suficientes, o
que las traiga con una forma que el motor va a rechazar. Una reimplementación en Python
probaría otra cosa.
"""
import json
import os
import re
import subprocess
import tempfile
import sys

import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
import actividades_web as A  # noqa: E402

DUELO_JS = os.path.join(BASE, "actividades_duelo.js")
CURRICULUM_JS = os.path.join(BASE, "actividades_curriculum.js")
PLAYER_JS = os.path.join(BASE, "actividades_player.js")
HTML = os.path.join(BASE, "actividades_player.html")

# El alfabeto del código, que tiene que ser EL MISMO que el de duelos.py: sin vocales (para
# no formar palabras sin querer) ni caracteres que se confundan al dictarlo en voz alta.
ALFABETO = "23456789BCDFGHJKMNPQRSTVWXYZ"


def _node(cuerpo, escolar=True, edad=9, menu=None):
    """Corre `cuerpo` con actividades_duelo.js y el catálogo REAL cargados.

    Se stubean sólo las funciones del player que el duelo usa (dibujar, sonido, red): lo
    que se está midiendo es la selección de preguntas y el alta en el menú, no el DOM.

    Los archivos se CONCATENAN en uno solo y se corre ese: en archivos separados (o en dos
    `eval` distintos) los `const CUR_*` del catálogo no serían visibles desde el duelo, y el
    pozo daría 0 sin que nada fallara — que es justo lo contrario de lo que queremos medir.
    """
    cabecera = """
      // el catálogo define los CUR_*_BANCO y el índice CUR_DUELO_POR_GRADO; sus factories
      // no importan acá, así que se stubean para que el archivo pueda evaluarse
      var GAMES = {};
      function juegoTriviaTexto(){return {}}; function juegoClasificar(){return {}};
      function juegoOrdenar(){return {}};    function juegoParametrico(){return {}};
      function juegoManipular(){return {}};
      var D = {escolar_on: %s, edad: %d, menu: %s};
      var Store = {data: {activeProfile: "Sofi"}};
      function gradoDelChico(){ return (D && D.edad ? D.edad : 9) - 5; }
      function shuffle(a){ return a; }          // determinista: el test no mide el azar
      function el(){ return {appendChild(){}, addEventListener(){}, classList:{add(){}}}; }
      var Sfx = {ok(){}, casi(){}, pop(){}};
      function toast(){}; function espera(){return Promise.resolve()};
      function volverMenu(){};
      var document = {createElement: () => ({textContent:"", innerHTML:"",
                                             appendChild(){}, addEventListener(){}}),
                      head: {appendChild(){}}};
    """ % ("true" if escolar else "false", edad,
           json.dumps(menu if menu is not None else []))
    fuente = "\n".join([
        cabecera,
        open(CURRICULUM_JS, encoding="utf-8").read(),
        open(DUELO_JS, encoding="utf-8").read(),
        cuerpo,
    ])
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8",
                                     delete=False) as f:
        f.write(fuente)
        ruta = f.name
    try:
        r = subprocess.run(["node", ruta], capture_output=True, text=True)
    finally:
        os.unlink(ruta)
    assert r.returncode == 0, r.stderr[-3000:]
    return json.loads(r.stdout.strip())


# ─────────────────────────────────────────────── el pozo de preguntas

def test_los_siete_grados_tienen_preguntas():
    """Sin pozo el duelo no existe para ese grado. Se mide el catálogo REAL, así que si
    alguien saca actividades de trivia de un grado, esto avisa."""
    out = _node("""
      const r = {};
      for (let g = 1; g <= 7; g++) r[g] = _dueloPozo(g).length;
      console.log(JSON.stringify(r));
    """)
    for g in range(1, 8):
        assert out[str(g)] >= 5, "el grado %s tiene %s preguntas" % (g, out[str(g)])
    # y bastante más que 5: con el mínimo justo, dos duelos seguidos repetirían todo
    flacos = {g: n for g, n in out.items() if n < 40}
    assert not flacos, "grados con pozo flaco (repetirían preguntas): %s" % flacos


def test_las_preguntas_estan_bien_formadas():
    """La forma tiene que ser la que el motor acepta (`duelos._sanear_pregunta`): si no,
    el chico juega, toca «guardar» y recibe un 400 con la partida ya jugada."""
    out = _node("""
      const malas = [];
      for (let g = 1; g <= 7; g++) {
        _dueloPozo(g).forEach((p, i) => {
          if (!p.q || typeof p.q !== "string") malas.push(g + "#" + i + " sin pregunta");
          else if (!Array.isArray(p.ops) || p.ops.length < 2) malas.push(g + "#" + i + " sin opciones");
          else if (p.ops.length > 4) malas.push(g + "#" + i + " más de 4 opciones");
          else if (p.ok !== 0) malas.push(g + "#" + i + " la correcta no es ops[0]");
          else if (p.ops.some((o) => !o || !String(o).trim())) malas.push(g + "#" + i + " opción vacía");
        });
      }
      console.log(JSON.stringify(malas.slice(0, 20)));
    """)
    assert out == [], "preguntas que el motor rechazaría: %s" % out


def test_elige_cinco_sin_repetir():
    out = _node("""
      const r = {};
      for (let g = 1; g <= 7; g++) {
        const p = _dueloElegir5(g);
        r[g] = {n: p.length, distintas: new Set(p.map((x) => x.q)).size};
      }
      console.log(JSON.stringify(r));
    """)
    for g in range(1, 8):
        assert out[str(g)]["n"] == 5, "el grado %s no dio 5 preguntas" % g
        assert out[str(g)]["distintas"] == 5, "el grado %s repitió una pregunta" % g


def test_las_cinco_cruzan_materias():
    """Cinco de Lengua seguidas harían que el duelo dependa de qué le gusta a cada uno en
    vez de lo que estudiaron los dos."""
    out = _node("""
      const r = {};
      for (let g = 1; g <= 7; g++) {
        const hay = new Set(_dueloPozo(g).map((x) => x.cat)).size;
        const dio = new Set(_dueloElegir5(g).map((x) => x.cat)).size;
        r[g] = {hay: hay, dio: dio};
      }
      console.log(JSON.stringify(r));
    """)
    for g in range(1, 8):
        hay, dio = out[str(g)]["hay"], out[str(g)]["dio"]
        assert dio >= min(hay, 2), \
            "el grado %s tiene %s materias y el duelo usó %s" % (g, hay, dio)


@pytest.mark.parametrize("grado", [1, 2, 3, 4, 5, 6, 7])
def test_el_motor_ACEPTA_lo_que_manda_el_player(grado, tmp_path, monkeypatch):
    """La costura que de verdad puede romper: el player elige las 5 preguntas y el motor
    las sanea. Si las formas se separan, el chico juega los 5 turnos, toca «guardar» y
    recibe un 400 con la partida ya jugada — el peor momento para enterarse.

    Se pasa la salida REAL de `_dueloElegir5` por `duelos.crear` REAL, sin inventar el
    dato en el medio."""
    import duelos
    monkeypatch.setattr(duelos, "DUELOS_DIR", str(tmp_path / "duelos"))
    preguntas = _node("console.log(JSON.stringify(_dueloElegir5(%d)));" % grado)
    codigo, d = duelos.crear(grado, preguntas, "Sofi", 3)
    assert codigo, "el motor rechazó las preguntas del player: %s" % d
    assert len(d["preguntas"]) == 5
    # y el segundo juega EXACTAMENTE las mismas
    assert [p["q"] for p in duelos.leer(codigo)["preguntas"]] == [p["q"] for p in preguntas]


# ─────────────────────────────────────────── dónde aparece (y dónde no)

def test_aparece_en_el_cuaderno_escolar():
    out = _node("""
      sumarDueloDeCompaneros();
      console.log(JSON.stringify(D.menu.map((m) => m.id)));
    """, escolar=True)
    assert "duelo" in out


def test_NO_aparece_en_un_cuaderno_de_cumpleanos():
    """Es un juego entre compañeros de un mismo grado; los cuadernos de la otra línea no
    tienen grado ni curso. Y es la misma regla de separación de las dos marcas."""
    out = _node("""
      sumarDueloDeCompaneros();
      console.log(JSON.stringify(D.menu.map((m) => m.id)));
    """, escolar=False)
    assert out == []


def test_no_se_duplica_si_ya_estaba():
    """Se inyecta en cada arranque: sin esta guarda, recargar dejaría dos tarjetas."""
    out = _node("""
      sumarDueloDeCompaneros(); sumarDueloDeCompaneros();
      console.log(JSON.stringify(D.menu.filter((m) => m.id === "duelo").length));
    """)
    assert out == 1


def test_la_tarjeta_tiene_titulo_e_icono():
    out = _node("""
      sumarDueloDeCompaneros();
      console.log(JSON.stringify(D.menu.find((m) => m.id === "duelo")));
    """)
    assert out["titulo"] and out["icono"]
    assert out["nivel"] == 1, "no puede quedar detrás de un candado: no es contenido del DC"


def test_queda_en_EXTRAS_y_no_en_una_materia():
    """Pedido de Pablo: "que quede en extras". Cae solo, porque `Adapt.categoria()` devuelve
    "logica" —que se muestra con el título "Extras"— para lo que no está en el grafo de
    saberes. Y esa categoría además está excluida del plan adaptativo y del panel de padres,
    que es justo lo que queremos: el duelo no mide."""
    motor = open(os.path.join(BASE, "motor_adaptativo.js"), encoding="utf-8").read()
    assert '"logica": "Extras"' in motor, "cambió el nombre de la categoría Extras"
    # cae en Extras porque NO está mapeado a ninguna materia: `categoria()` devuelve
    # "logica" para lo que no encuentra
    m = re.search(r"CATEGORIA_JUEGO\s*=\s*\{(.*?)\n\};", motor, re.S)
    assert m, "no se encontró el mapa de categorías"
    assert '"duelo"' not in m.group(1), "el duelo quedó en una materia en vez de Extras"
    assert 'CATEGORIA_JUEGO[actId] || "logica"' in motor, "cambió el fallback a Extras"


def test_el_duelo_no_alimenta_el_motor_adaptativo():
    """El chico responde UNA vez, apurado y compitiendo: tomar eso como evidencia de dominio
    ensuciaría lo que el motor decide enseñarle después. Es un juego, no una evaluación."""
    src = _sin_comentarios(open(DUELO_JS, encoding="utf-8").read())
    for prohibido in ("ctx.bien(", "ctx.casi(", "ctx.win(", "Store.marcarItemOk",
                      "Tel.push"):
        assert prohibido not in src, "el duelo llama a %s: eso mide dominio" % prohibido


def _sin_comentarios(src):
    """El fuente sin comentarios ni strings de texto largo.

    Hace falta porque el archivo DOCUMENTA lo que no hace ("no llama a ctx.bien()", "si
    llevara el token…"). Sin esto, los tests de abajo fallan por la explicación en vez de
    por el código — y peor: pasarían si alguien borra el comentario."""
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)     # bloque
    return re.sub(r"(?m)//.*$", " ", src)                  # línea


# ────────────────────────────────────────────── seguridad y coherencia

def test_el_codigo_usa_el_MISMO_alfabeto_que_el_motor():
    """El filtro del input y el generador del servidor tienen que coincidir: si no, el chico
    puede tipear un código que el motor rechaza, o al revés no poder tipear uno válido."""
    import duelos
    src = open(DUELO_JS, encoding="utf-8").read()
    m = re.search(r"replace\(/\[\^([0-9A-Z]+)\]/g", src)
    assert m, "no se encontró el filtro del input del código"
    assert sorted(m.group(1)) == sorted(duelos.ALFABETO), \
        "el alfabeto del player no es el de duelos.py"
    assert not set(m.group(1)) & set("AEIOU01ILO")


def test_la_pantalla_nunca_manda_el_token():
    """Lo más importante de seguridad: el link del duelo lleva el id de la PARTIDA. Si el
    player mandara el token, compartir un código sería repartir la puerta del cuaderno."""
    src = _sin_comentarios(open(DUELO_JS, encoding="utf-8").read())
    assert "token" not in src.lower(), "el player del duelo nombra el token"
    # y lo que manda son exactamente los campos del contrato
    for campo in ("grado", "preguntas", "nombre", "aciertos"):
        assert campo in src


def test_sin_catalogo_no_rompe_el_cuaderno():
    """Falla en silencio a propósito: sin preguntas el chico se queda sin duelo, nunca sin
    cuaderno. Es la misma regla que las actividades extra del padre."""
    js = """
      const fs = require('fs');
      var GAMES = {}, D = {escolar_on: true, edad: 9, menu: []};
      var Store = {data:{activeProfile:"x"}};
      function gradoDelChico(){return 4}; function shuffle(a){return a};
      function el(){return {appendChild(){}, addEventListener(){}, classList:{add(){}}}};
      var Sfx={ok(){},casi(){},pop(){}}; function toast(){}; function espera(){};
      function volverMenu(){};
      var document={createElement:()=>({appendChild(){},addEventListener(){}}),
                    head:{appendChild(){}}};
      eval(fs.readFileSync(%s, 'utf8'));   // sin CUR_DUELO_POR_GRADO definido
      sumarDueloDeCompaneros();
      console.log(JSON.stringify(D.menu.length));
    """ % json.dumps(DUELO_JS)
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-2000:]
    assert json.loads(r.stdout.strip()) == 0


# ─────────────────────────────────────────────────── que llegue al chico

def test_el_motor_sirve_el_archivo():
    """Sin esto el <script> da 404 y no hay duelo. Sale del REPO y no de la carpeta del
    token: mejorar el duelo tiene que llegar a los cuadernos ya entregados."""
    assert A._ASSET_RE.fullmatch("duelo.js"), "el asset no está permitido"
    assert os.path.isfile(A.TEMPLATE_DUELO)
    assert A.TEMPLATE_DUELO.endswith("actividades_duelo.js")


def test_el_html_lo_carga_despues_del_catalogo():
    """Necesita GAMES (player.js) y el pozo (actividades_curriculum.js): cargado antes, se
    registra sobre un GAMES que todavía no existe."""
    html = open(HTML, encoding="utf-8").read()
    assert "duelo.js" in html
    assert html.index("actividades_curriculum.js") < html.index("duelo.js")
    assert html.index("player.js") < html.index("duelo.js")


def test_el_player_lo_engancha_al_arrancar():
    """El menú queda CONGELADO en el token el día de la compra, así que un juego nuevo sólo
    llega si se inyecta desde el navegador."""
    src = open(PLAYER_JS, encoding="utf-8").read()
    assert "sumarDueloDeCompaneros" in src
    # con `typeof`: si el archivo no cargó, el cuaderno tiene que abrir igual
    assert 'typeof sumarDueloDeCompaneros === "function"' in src
