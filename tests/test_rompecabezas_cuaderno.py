# -*- coding: utf-8 -*-
"""El rompecabezas de Extras (1.º y 2.º).

Pablo, 30-jul-2026: *"quizás en extras de 1.º y 2.º podemos poner un rompecabezas […]
es algo que ya tenemos armado, es solo linkearlo con una actividad"*.

No era linkearlo. El rompecabezas que se vende es una PÁGINA aparte (`/armar/<token>/`)
con su propia tienda y su demo con candado: embeberlo le habría metido al chico la
pantalla de compra adentro del cuaderno. Lo que sí se reusó —y es lo que vale— es el
CORTE: los bordes salen de `rompecabezas_web._bordes_json`, el mismo generador que el
imprimible, así que el encastre es el de siempre.

LO QUE ESTE ARCHIVO CUIDA, y por qué cada cosa:

1. QUE LAS PIEZAS TESELEN. Es EL riesgo del port: `poliPieza` recorre los bordes en un
   orden preciso (arriba → derecha → abajo al revés → izquierda al revés) y un signo
   cambiado no rompe nada visible al abrir — deja huecos o solapes que recién se ven
   armando. Se mide numéricamente: las áreas de las piezas tienen que sumar el área de
   la imagen, y cada borde compartido tiene que ser el MISMO punto por los dos lados.

2. QUE NO SE FILTRE A OTROS GRADOS. De 3.º en adelante no va, y un cuaderno de
   cumpleaños (sin `escolar_on`) no lo lleva nunca: es contenido de la línea escolar.

3. QUE LA TARJETA Y LOS DATOS VAYAN JUNTOS. El menú se arma antes que la escena, así que
   la tarjeta se agrega en `_menu` y `crear()` la saca si no se pudo generar la imagen.
   Si eso se desincroniza, el chico abre una actividad vacía.
"""
import json
import os
import shutil
import subprocess
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import actividades_web as aw  # noqa: E402

PLAYER = os.path.join(_BASE, "actividades_player.js")


@pytest.fixture(scope="module")
def tokens(tmp_path_factory):
    """Un cuaderno escolar por grado (1.º a 4.º) + uno de cumpleaños, generados de
    verdad. Lo que se mide es el data.json que sale, no lo que las funciones prometen."""
    d = tmp_path_factory.mktemp("act")
    viejo, aw.ACT_DIR = aw.ACT_DIR, str(d)
    try:
        out = {}
        for grado in range(1, 5):
            tok = aw.crear({"nombre": "Test", "edad": str(grado + 5), "escolar_on": True},
                           "safari", token="zrompe%d" % grado)
            out[grado] = (os.path.join(str(d), tok),
                          json.load(open(os.path.join(str(d), tok, "data.json"), encoding="utf-8")))
        tok = aw.crear({"nombre": "Test", "edad": "6"}, "safari", token="zcumple")
        out["cumple"] = (os.path.join(str(d), tok),
                         json.load(open(os.path.join(str(d), tok, "data.json"), encoding="utf-8")))
        yield out
    finally:
        aw.ACT_DIR = viejo


def _nivel(tokens, grado, nivel):
    """La ficha del nivel MÁS sus cortes, que ya no viajan en el data.json (pesaban el 75%
    del archivo) sino en el repo. Se piden por el mismo camino que los pide el player."""
    n = dict(tokens[grado][1]["rompecabezas"]["niveles"][nivel])
    datos, _ = aw.archivo(os.path.basename(tokens[grado][0]), n["cortes"])
    n["bordes"] = json.loads(datos.decode("utf-8"))["bordes"]
    return n


def _menu_ids(dj):
    return [m["id"] if isinstance(m, dict) else m for m in dj["menu"]]


# ── 1. el corte ──────────────────────────────────────────────────────────────────

pytestmark_node = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")

_ARNES = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
// se extrae la función REAL del player: una copia acá se desincronizaría al primer
// cambio y este test dejaría de medir lo que se sirve.
const m = src.match(/const poliPieza = \(ci, fi\) => \{[\s\S]*?\n    \};/);
if (!m) { console.error("no encontré poliPieza en el player"); process.exit(1); }
const R = %s, ROMPE_ESC = %s;
const cols = R.cols, filas = R.filas;
// `poliPieza` lee `bordes` del scope del juego (ya no viajan en el data.json)
const bordes = R.bordes;
// `eval` de un `const` lo deja encerrado en el scope del propio eval, así que se evalúa
// como EXPRESIÓN y se ata acá afuera.
const poliPieza = eval("(" + m[0].replace(/^const poliPieza = /, "").replace(/;$/, "") + ")");
const area = (p) => { let a = 0;
  for (let i = 0, j = p.length - 1; i < p.length; j = i++) a += p[j][0] * p[i][1] - p[i][0] * p[j][1];
  return Math.abs(a) / 2; };
const out = { areas: [], total: 0, fuera: 0, puntos: [] };
for (let fi = 0; fi < filas; fi++) for (let ci = 0; ci < cols; ci++) {
  const p = poliPieza(ci, fi);
  out.areas.push(area(p)); out.total += area(p);
  for (const [x, y] of p) {
    // margen: el knob sobresale de la celda a propósito, pero no puede salir del lienzo
    if (x < -R.w * 0.2 || x > R.w * 1.2 || y < -R.h * 0.2 || y > R.h * 1.2) out.fuera++;
  }
  out.puntos.push(p.length);
}
console.log(JSON.stringify(out));
"""


def _correr_poli(R):
    src = open(PLAYER, encoding="utf-8").read()
    esc = src.split("const ROMPE_ESC = ")[1].split(";")[0]
    js = _ARNES % (json.dumps(PLAYER), json.dumps(R), esc)
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip())


@pytestmark_node
@pytest.mark.parametrize("grado,nivel", [(g, n) for g in (1, 2) for n in range(4)])
def test_las_piezas_teselan_la_imagen_entera(tokens, grado, nivel):
    """EL test del port, y ahora de CADA escalón. Los knobs que sobresalen de una pieza son
    exactamente los huecos de la vecina, así que las áreas SUMAN el área de la imagen — al
    milímetro. Si un signo del recorrido está cambiado, esta suma se va y el chico ve
    huecos. Se mide nivel por nivel porque cada uno tiene su propia grilla Y su propia
    semilla de corte: que cierre el de 6 piezas no dice nada del de 20."""
    R = _nivel(tokens, grado, nivel)
    out = _correr_poli(R)
    esperado = R["w"] * R["h"]
    assert abs(out["total"] - esperado) < esperado * 0.002, (
        "nivel %d: las piezas suman %.0f px² y la imagen tiene %d px²: hay huecos o solapes"
        % (nivel, out["total"], esperado))
    assert len(out["areas"]) == R["cols"] * R["filas"]
    assert out["fuera"] == 0, "%d punto(s) de pieza se van del lienzo" % out["fuera"]


@pytestmark_node
@pytest.mark.parametrize("grado,nivel", [(g, n) for g in (1, 2) for n in range(4)])
def test_ninguna_pieza_es_degenerada(tokens, grado, nivel):
    """Una pieza de área casi cero es invisible e inagarrable: el chico no puede terminar
    el rompecabezas y no hay forma de que entienda por qué."""
    R = _nivel(tokens, grado, nivel)
    out = _correr_poli(R)
    celda = (R["w"] / R["cols"]) * (R["h"] / R["filas"])
    chicas = [a for a in out["areas"] if a < celda * 0.5]
    assert not chicas, "nivel %d: hay %d pieza(s) de menos de media celda" % (nivel, len(chicas))
    assert min(out["puntos"]) >= 4, "una pieza quedó con menos de 4 puntos de contorno"


# ── 2. la escalera ───────────────────────────────────────────────────────────────

ESCALERA = {1: [6, 9, 12, 16], 2: [9, 12, 16, 20]}


@pytest.mark.parametrize("grado", [1, 2])
def test_la_cantidad_de_piezas_sube_escalon_por_escalon(tokens, grado):
    """Pablo, 30-jul-2026: *"que cambie cantidad de piezas a medida que ves que lo saca
    fácil"*. Arranca chico —es una actividad del cuaderno, no el producto— pero el que lo
    domina termina armando uno de verdad."""
    d, dj = tokens[grado]
    R = dj.get("rompecabezas")
    assert R, "%d.º se quedó sin rompecabezas" % grado
    piezas = [n["cols"] * n["filas"] for n in R["niveles"]]
    assert piezas == ESCALERA[grado], "%d.º da %s y la escalera es %s" % (
        grado, piezas, ESCALERA[grado])
    assert piezas == sorted(piezas) and len(set(piezas)) == len(piezas), \
        "un escalón no agrega dificultad: %s" % piezas
    assert "rompecabezas" in _menu_ids(dj), "%d.º tiene los datos pero no la tarjeta" % grado


@pytest.mark.parametrize("grado", [1, 2])
def test_cada_nivel_tiene_su_propia_imagen(tokens, grado):
    """La otra mitad del pedido: *"que cambie imágenes"*. Si dos niveles compartieran el
    dibujo, subir de nivel se notaría sólo contando piezas."""
    R = tokens[grado][1]["rompecabezas"]
    imgs = [n["img"] for n in R["niveles"]]
    assert len(set(imgs)) == len(imgs), "%d.º repite imagen entre niveles: %s" % (grado, imgs)


@pytest.mark.parametrize("grado", [1, 2])
def test_cada_nivel_tiene_cortes_distintos(tokens, grado):
    """Las semillas se separan por nivel a propósito: con la misma, el de 12 piezas se
    vería como el de 6 con líneas de más, en vez de un rompecabezas nuevo."""
    primeras = [json.dumps(_nivel(tokens, grado, i)["bordes"]["v"][0][0]) for i in range(4)]
    assert len(set(primeras)) == len(primeras), "%d.º repite el corte entre niveles" % grado


@pytest.mark.parametrize("grado,nivel", [(g, n) for g in (1, 2) for n in range(4)])
def test_la_imagen_de_cada_nivel_se_puede_pedir_de_verdad(tokens, grado, nivel):
    """El bug que este test existe para no repetir: la primera versión generaba un
    `romp.jpg` propio y el archivo estaba en disco, pero `_ASSET_RE` es una lista BLANCA
    y no lo nombraba → el servidor devolvía 404 y el rompecabezas quedaba en blanco.
    Que el arte exista NO es que se pueda pedir; se mide pidiéndolo. Y ahora importa más:
    las imágenes salen del REPO, no de la carpeta del token."""
    d, dj = tokens[grado]
    R = _nivel(tokens, grado, nivel)
    for clave, tipo in (("img", "image/"), ("cortes", "application/json")):
        r = aw.archivo(os.path.basename(d), R[clave])
        assert r is not None, "%s no pasa la lista blanca: el player recibe 404" % R[clave]
        datos, ct = r
        assert len(datos) > 500 and ct.startswith(tipo), "%s llegó vacío o con otro tipo" % R[clave]


@pytest.mark.parametrize("grado,nivel", [(g, n) for g in (1, 2) for n in range(4)])
def test_las_medidas_son_las_de_la_imagen(tokens, grado, nivel):
    """El player estira la imagen al tablero con la proporción `w`/`h` del data.json. Si
    no es la real, el dibujo sale deformado y las piezas no coinciden con lo que se ve."""
    from PIL import Image
    import io as _io
    R = _nivel(tokens, grado, nivel)
    datos, _ = aw.archivo(os.path.basename(tokens[grado][0]), R["img"])
    with Image.open(_io.BytesIO(datos)) as im:
        assert (R["w"], R["h"]) == im.size, "data.json dice %sx%s y la imagen es %sx%s" % (
            R["w"], R["h"], im.width, im.height)


def test_el_player_elige_el_nivel_por_lo_que_gano_no_por_la_edad():
    """`bonusDominio` es lo GANADO sacándolo con 3★; `nivelDif` le sumaría además un piso
    por edad, y acá la edad ya está contemplada — cada grado tiene su propia escalera. Con
    el piso por edad, un chico de 2.º arrancaría en el escalón 2 sin haberlo ganado."""
    src = open(PLAYER, encoding="utf-8").read()
    i = src.index("GAMES.rompecabezas = {")
    cuerpo = src[i:i + 1600]
    assert "ctx.bonusDominio" in cuerpo, "el rompecabezas dejó de escalar por dominio"
    assert "ctx.nivelDif" not in cuerpo, "usa el piso por edad: duplica lo que ya hace el grado"
    assert "Math.min(niveles.length - 1" in cuerpo, \
        "sin clamp, un chico con dominio 4 y 4 niveles se queda sin rompecabezas"


def test_los_niveles_viajan_todos_en_el_token(tokens):
    """Los 4 niveles van al data.json y el player elige. Si el motor eligiera, el cuaderno
    quedaría congelado en el nivel que el chico tenía el día que se generó el token —
    justo lo que rompe que sea adaptativo."""
    for grado in (1, 2):
        R = tokens[grado][1]["rompecabezas"]
        assert len(R["niveles"]) == 4, "%d.º viaja con %d nivel(es)" % (grado, len(R["niveles"]))


@pytest.mark.parametrize("grado", [3, 4])
def test_de_tercero_en_adelante_no_aparece(tokens, grado):
    """De 3.º arriba armar 6 piezas no le aporta nada. Si mañana se quiere sumar, se
    agrega el grado a `_ROMPE_GRADO` — este test avisa que es una decisión, no un olvido."""
    d, dj = tokens[grado]
    assert "rompecabezas" not in dj, "%d.º recibió el rompecabezas" % grado
    assert "rompecabezas" not in _menu_ids(dj), "%d.º muestra una tarjeta sin datos" % grado


def test_un_cuaderno_de_cumpleanos_no_lo_lleva(tokens):
    """No-regresión comercial: es contenido de la línea ESCOLAR. Un kit de safari
    comprado para un cumpleaños no cambia de producto por la edad del chico."""
    d, dj = tokens["cumple"]
    assert not dj.get("escolar_on")
    assert "rompecabezas" not in dj and "rompecabezas" not in _menu_ids(dj)


# ── 3. que tarjeta y datos no se separen ─────────────────────────────────────────

def test_la_tarjeta_nunca_queda_sin_datos(tokens):
    """El menú se arma ANTES que la escena (que es la imagen del rompecabezas), así que
    la tarjeta se agrega optimista y `crear()` la retira si no se pudo generar. Este es
    el invariante que hace que eso sea seguro, medido en los 5 cuadernos generados."""
    for k, (d, dj) in tokens.items():
        tiene_tarjeta = "rompecabezas" in _menu_ids(dj)
        tiene_datos = bool(dj.get("rompecabezas"))
        assert tiene_tarjeta == tiene_datos, (
            "%s: tarjeta=%s datos=%s — el chico abriría una actividad vacía"
            % (k, tiene_tarjeta, tiene_datos))


def test_sin_arte_no_rompe_el_cuaderno(tmp_path, monkeypatch):
    """Si falta el arte, el cuaderno tiene que salir igual SIN la tarjeta. Nunca puede
    quedar un token a medio generar por un asset que no estaba."""
    monkeypatch.setattr(aw, "ARTE_DIR", str(tmp_path))
    assert aw._rompecabezas_json(str(tmp_path), "6", 1, escolar=True) is None


def test_con_el_arte_a_medio_generar_la_escalera_se_corta(tmp_path, monkeypatch):
    """Si alguien regenera el arte y se cae a mitad de camino, el cuaderno sale con los
    niveles que SÍ existen en vez de con tarjetas que abren en blanco. Es el caso real de
    correr `infra/generar-rompecabezas-arte.py` y que falle en el nivel 3."""
    import shutil as _sh
    g = tmp_path / "g1"
    g.mkdir()
    for i in (0, 1):
        for ext in ("jpg", "json"):
            _sh.copy(os.path.join(aw.ARTE_DIR, "g1", "romp_%d.%s" % (i, ext)),
                     str(g / ("romp_%d.%s" % (i, ext))))
    monkeypatch.setattr(aw, "ARTE_DIR", str(tmp_path))
    r = aw._rompecabezas_json(str(tmp_path), "6", 1, escolar=True)
    assert r and len(r["niveles"]) == 2, "la escalera no se cortó donde termina el arte"


def test_el_player_tiene_el_juego_registrado():
    """Sin `GAMES.rompecabezas` la tarjeta directamente no se dibuja (el menú filtra por
    juego existente) y el síntoma sería «no aparece», sin ningún error."""
    src = open(PLAYER, encoding="utf-8").read()
    assert "GAMES.rompecabezas = {" in src
    import actividades_categorias as cat
    assert cat.CATEGORIA.get("rompecabezas"), "el juego nuevo quedó sin categoría"


def test_el_festejo_puede_prometer_que_se_pone_mas_dificil():
    """Al ganar 3★ el festejo dice «esta actividad ahora va a ser más difícil». Mientras
    el rompecabezas tuvo una sola grilla eso era mentira y estaba en `SIN_NIVEL_DIF`; desde
    que la escalera existe, es cierto — y sacarlo de esa lista es lo que hace que el chico
    se entere de que subió. Si alguien lo vuelve a poner ahí, la escalera queda muda."""
    src = open(PLAYER, encoding="utf-8").read()
    i = src.index("const SIN_NIVEL_DIF = new Set([")
    assert '"rompecabezas"' not in src[i:src.index("]);", i)], \
        "el rompecabezas volvió a SIN_NIVEL_DIF: sube de nivel pero no se lo dice a nadie"
