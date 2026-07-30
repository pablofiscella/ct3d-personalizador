"""Temática COMPLETA por grado: además del elenco (test_actividades_arte_grado.py), el
cuaderno toma del grado la PALETA, la ESCENA (fondo del juego "contar") y las páginas para
COLOREAR — el pedido de Pablo "que toda la temática sea la que tiene la portada".

Lo que se verifica: (a) las 7 paletas de grado cumplen el mismo piso de contraste que las
de tema (si no, el mundo del grado se vería lindo pero sería menos legible que hoy);
(b) cada pieza sale del grado sólo cuando su arte existe de verdad, y si no cae al tema —
la garantía de no-regresión para los links ya vendidos; (c) el colorear del grado llega al
token en B/N puro, que es lo que hace que el balde de pintura no se fugue."""
import json
import os
import shutil
import sys

import pytest
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import actividades_web as aw  # noqa: E402

TEMA = "safari"
EDAD_5TO = "10"          # edad 10 → 5° grado
GRADO = int(EDAD_5TO) - 5


# ── contraste (WCAG) ────────────────────────────────────────────────────────────
def _lum(h):
    h = h.lstrip("#")
    canales = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        canales.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = canales
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contraste(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def test_paletas_de_grado_completas():
    """Mismas claves que las de tema: al player le falta una y rompe el CSS."""
    claves = set(aw._PALETA_DEFAULT)
    for grado, pal in aw.PALETA_GRADO.items():
        assert set(pal) == claves, grado


def test_paletas_de_grado_tienen_los_7_grados():
    assert set(aw.PALETA_GRADO) == set(aw.MUNDO_GRADO) == set(range(1, 8))


@pytest.mark.parametrize("grado", sorted(aw.PALETA_GRADO))
def test_paleta_de_grado_texto_legible(grado):
    """`ink` sobre los 3 fondos donde se escribe: AA (4.5), igual que las paletas de tema."""
    pal = aw.PALETA_GRADO[grado]
    for fondo in ("bg", "card", "soft"):
        r = _contraste(pal["ink"], pal[fondo])
        assert r >= 4.5, "g%d ink/%s = %.2f" % (grado, fondo, r)


@pytest.mark.parametrize("grado", sorted(aw.PALETA_GRADO))
def test_paleta_de_grado_acentos_legibles(grado):
    """Texto BLANCO sobre los acentos (botones .btn y badges .mini-est): AA-large (3.0).

    Es el piso real del producto: los botones son Baloo 21px+ y ninguna paleta de tema
    llega a 4.5 acá — pedirlo sería más estricto que el resto del cuaderno."""
    pal = aw.PALETA_GRADO[grado]
    for acento in ("ac", "ac2"):
        r = _contraste("#FFFFFF", pal[acento])
        assert r >= 3.0, "g%d blanco/%s = %.2f" % (grado, acento, r)


# ── la compuerta: sólo con arte del grado ───────────────────────────────────────
@pytest.fixture
def arte_dir(tmp_path, monkeypatch):
    """Carpeta de arte del grado, en un tmp: `ARTE_DIR` se apunta ahí para que el test
    NUNCA toque el arte real del repo (moverlo de lugar y restaurarlo dejaba el grado en
    un .bak si la corrida se interrumpía — y con los 7 grados ya poblados, eso es perder
    arte de verdad)."""
    monkeypatch.setattr(aw, "ARTE_DIR", str(tmp_path))
    d = tmp_path / ("g%d" % GRADO)
    d.mkdir()
    return str(d)


def _sticker(path, color=(200, 30, 30)):
    im = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    im.paste(color, (60, 60, 240, 240))
    im.save(path)


def _elenco(arte_dir):
    for i in range(4):
        _sticker(os.path.join(arte_dir, "s%02d.png" % i))


def _lineart(path):
    """Dibujo de línea negra sobre blanco, como las páginas para colorear reales."""
    im = Image.new("RGB", (600, 600), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.ellipse((100, 100, 500, 500), outline=(0, 0, 0), width=8)
    im.save(path)


def _escena_png(path, color=(120, 180, 220)):
    Image.new("RGB", (1536, 1024), color).save(path)


def _crear(token, edad=EDAD_5TO, escolar=True):
    d = os.path.join(aw.ACT_DIR, token)
    shutil.rmtree(d, ignore_errors=True)
    aw.crear({"nombre": "Test", "edad": edad, "escolar_on": escolar}, TEMA, token=token)
    return d


def _data(d):
    return json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))


def test_grado_con_arte_es_la_compuerta(arte_dir):
    """`_grado_con_arte` es lo que habilita TODA la temática del grado: pide las DOS
    condiciones (token escolar + arte instalado)."""
    assert aw._grado_con_arte(EDAD_5TO, True) == GRADO
    assert aw._grado_con_arte(EDAD_5TO, False) is None, "sin flag escolar manda el tema"
    assert aw._grado_con_arte("no-es-un-numero", True) is None
    shutil.rmtree(arte_dir, ignore_errors=True)
    assert aw._grado_con_arte(EDAD_5TO, True) is None, "sin carpeta de arte no hay grado"


def test_compra_por_tema_conserva_su_tema(arte_dir):
    """LA garantía comercial: un token SIN flag escolar (la compra del kit, donde el
    cliente eligió safari/princesas) no se convierte en el mundo del grado por la edad —
    ni el elenco, ni el header, ni la paleta, ni la escena, ni las páginas de colorear."""
    _elenco(arte_dir)
    _escena_png(os.path.join(arte_dir, "escena.png"), (7, 190, 133))
    _lineart(os.path.join(arte_dir, "colorear_0.png"))
    tok = "test-tem-kit-aabb"
    d = _crear(tok, escolar=False)
    try:
        dj = _data(d)
        assert dj["paleta"] == aw._paleta(TEMA), "le pisaron la paleta del tema comprado"
        assert dj["tema_nombre"] != aw.MUNDO_GRADO[GRADO], dj["tema_nombre"]
        assert all(p.startswith("p") for p in dj["personajes"]), dj["personajes"]
        im = Image.open(os.path.join(d, "escena.jpg")).convert("RGB")
        assert im.getpixel((im.width // 2, im.height // 2))[1] != 190, "escena del grado"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_el_flag_escolar_se_preserva_al_regenerar(arte_dir):
    """Regenerar un token escolar no lo devuelve al tema (no se pierde lo entregado)."""
    _elenco(arte_dir)
    tok = "test-tem-pres-aabb"
    d = _crear(tok)
    try:
        assert _data(d)["escolar_on"] is True
        aw.crear({"nombre": "Test", "edad": EDAD_5TO}, TEMA, token=tok)   # sin el flag
        dj = _data(d)
        assert dj["escolar_on"] is True, "se perdió la línea escolar al regenerar"
        assert dj["paleta"] == aw.PALETA_GRADO[GRADO]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_paleta_sale_del_grado(arte_dir):
    _elenco(arte_dir)
    tok = "test-tem-pal-aabb"
    d = _crear(tok)
    try:
        assert _data(d)["paleta"] == aw.PALETA_GRADO[GRADO]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_sin_arte_la_paleta_sigue_siendo_la_del_tema(arte_dir):
    """No-regresión: el token de un grado sin arte queda idéntico a como salía antes."""
    shutil.rmtree(arte_dir, ignore_errors=True)
    tok = "test-tem-pal2-aabb"
    d = _crear(tok)
    try:
        assert _data(d)["paleta"] == aw._paleta(TEMA)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_escena_sale_del_grado(arte_dir):
    """Con escena.png del grado, el fondo del juego "contar" es el del mundo del grado."""
    _elenco(arte_dir)
    marca = (7, 190, 133)
    _escena_png(os.path.join(arte_dir, "escena.png"), marca)
    tok = "test-tem-esc-aabb"
    d = _crear(tok)
    try:
        assert _data(d)["escena"] == "escena.jpg"
        im = Image.open(os.path.join(d, "escena.jpg")).convert("RGB")
        r, g, b = im.getpixel((im.width // 2, im.height // 2))
        assert abs(r - marca[0]) < 12 and abs(g - marca[1]) < 12 and abs(b - marca[2]) < 12, \
            "la escena del token no es la del grado: %s" % ((r, g, b),)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_sin_escena_del_grado_cae_a_la_del_tema(arte_dir):
    """Arte del grado a medio generar (elenco sí, escena no) → escena del tema, no None."""
    _elenco(arte_dir)
    tok = "test-tem-esc2-aabb"
    d = _crear(tok)
    try:
        assert _data(d)["escena"] == aw._escena(TEMA, d), "se perdió la escena del tema"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_colorear_sale_del_grado(arte_dir):
    _elenco(arte_dir)
    for i in range(2):
        _lineart(os.path.join(arte_dir, "colorear_%d.png" % i))
    tok = "test-tem-col-aabb"
    d = _crear(tok)
    try:
        cols = _data(d)["colorear"]
        assert cols == ["colorear_0.png", "colorear_1.png"], cols
        for fn in cols:
            assert os.path.exists(os.path.join(d, fn)), "falta %s en el token" % fn
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_colorear_del_grado_llega_en_blanco_y_negro(arte_dir):
    """Sin B/N puro el balde de pintura se fuga por los grises del antialias."""
    _elenco(arte_dir)
    _lineart(os.path.join(arte_dir, "colorear_0.png"))
    tok = "test-tem-col2-aabb"
    d = _crear(tok)
    try:
        im = Image.open(os.path.join(d, "colorear_0.png")).convert("L")
        tonos = {p for p in im.getdata()}
        assert tonos <= {0, 255}, "quedaron grises: %s" % sorted(tonos)[:8]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_sin_colorear_del_grado_cae_al_del_tema(arte_dir):
    """Arte del grado sin páginas de colorear → las del tema (el juego no se queda vacío)."""
    _elenco(arte_dir)
    tok = "test-tem-col3-aabb"
    d = _crear(tok)
    try:
        assert _data(d)["colorear"], "el token quedó sin páginas para colorear"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_otro_grado_no_hereda_la_tematica(arte_dir):
    """Cada grado usa SU carpeta: el arte de 5° no se filtra a un token de 2°."""
    _elenco(arte_dir)
    _escena_png(os.path.join(arte_dir, "escena.png"), (7, 190, 133))
    tok = "test-tem-otro-aabb"
    d = _crear(tok, edad="7")                     # 2° grado
    try:
        assert _data(d)["paleta"] != aw.PALETA_GRADO[GRADO]
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ── el flag como interruptor de la LÍNEA ESCOLAR ────────────────────────────────
@pytest.mark.parametrize("valor,esperado", [
    (True, True), (False, False), (None, False),
    # el POST /api/generar stringifica los campos extra: sin _flag, "False" sería True
    ("True", True), ("False", False), ("true", True), ("false", False),
    ("1", True), ("0", False), ("", False), ("off", False),
])
def test_flag_tolera_el_valor_stringificado(valor, esperado):
    assert aw._flag(valor) is esperado


def test_escolar_enciende_el_motor_adaptativo(arte_dir):
    """`escolar_on` es UN interruptor: mundo del grado + motor adaptativo. Si no, quedan
    medios estados (arte del grado con menú plano, o menú adaptativo sobre safari)."""
    _elenco(arte_dir)
    tok = "test-tem-adapt-aabb"
    d = _crear(tok)
    try:
        dj = _data(d)
        assert dj["escolar_on"] is True and dj["adaptativo_on"] is True
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_token_por_tema_no_enciende_el_adaptativo(arte_dir):
    """No-regresión: la compra por tema queda como siempre, con el menú de siempre."""
    _elenco(arte_dir)
    tok = "test-tem-adapt2-aabb"
    d = _crear(tok, escolar=False)
    try:
        dj = _data(d)
        assert dj["escolar_on"] is False and dj["adaptativo_on"] is False
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_escolar_apagado_explicito_no_se_enciende(arte_dir):
    """`escolar_on=False` del payload llega como la cadena "False": debe APAGAR."""
    _elenco(arte_dir)
    tok = "test-tem-adapt3-aabb"
    d = _crear(tok, escolar="False")
    try:
        dj = _data(d)
        assert dj["escolar_on"] is False, "un False explícito encendió la línea escolar"
        assert dj["tema_nombre"] != aw.MUNDO_GRADO[GRADO]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_adaptativo_se_preserva_al_regenerar(arte_dir):
    """Los 3 tokens de prueba traen adaptativo_on puesto A MANO en data.json; hasta
    ahora `crear()` no lo manejaba y regenerarlos lo perdía."""
    _elenco(arte_dir)
    tok = "test-tem-adapt4-aabb"
    d = _crear(tok, escolar=False)
    try:
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        dj["adaptativo_on"] = True                       # como se hizo a mano en prod
        json.dump(dj, open(os.path.join(d, "data.json"), "w", encoding="utf-8"))
        aw.crear({"nombre": "Test", "edad": EDAD_5TO}, TEMA, token=tok)   # regenerar
        assert _data(d)["adaptativo_on"] is True, "se perdió el flag al regenerar"
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ── la portada ilustrada del grado ──────────────────────────────────────────────
def test_los_7_grados_tienen_su_portada_cargada():
    """Están en el repo desde el 24-jul. Si falta una, ese grado cae a la tarjeta
    genérica sin que nadie se entere."""
    faltan = [g for g in range(1, 8)
              if not os.path.isfile(os.path.join(aw.PORTADA_DIR, "%d.png" % g))]
    assert not faltan, "grados sin portada: %s" % faltan


def test_la_portada_del_grado_LA_USA_alguien():
    """LA lección del 25-jul: las 7 portadas estuvieron un día enteras en el repo y
    ningún código las leía — el cliente veía la tarjeta genérica. Subir un asset no es
    entregarlo. Este test falla si alguien vuelve a dejar la carpeta huérfana."""
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "actividades_web.py"), encoding="utf-8").read()
    assert "PORTADA_DIR" in src and "_portada_de_grado" in src
    i = src.index("portada.jpg\"), quality=88")
    assert "_portada_de_grado" in src[max(0, i - 400):i], \
        "la portada del grado no se está usando al guardar portada.jpg"


@pytest.mark.parametrize("grado,edad", [(1, "6"), (2, "7"), (4, "9"), (7, "12")])
def test_la_portada_no_se_deforma(grado, edad, tmp_path, monkeypatch):
    """1° y 2° vinieron en 2:3 y el resto en 3:4. Un resize directo a 900×1200 estiraría
    las caras de los chicos; se hace contain con relleno.

    Arma el arte del grado que prueba (la fixture `arte_dir` sólo crea el de GRADO), pero
    deja PORTADA_DIR apuntando al real: lo que se está probando es justamente que las
    portadas de verdad no se deformen."""
    monkeypatch.setattr(aw, "ARTE_DIR", str(tmp_path))
    (tmp_path / ("g%d" % grado)).mkdir()
    im = aw._portada_de_grado(edad, True)
    assert im is not None, "sin portada para %d°" % grado
    assert im.size == (900, 1200)
    orig = Image.open(os.path.join(aw.PORTADA_DIR, "%d.png" % grado))
    # el contenido escalado tiene que conservar la proporción original
    esc = min(900 / orig.width, 1200 / orig.height)
    nw, nh = int(orig.width * esc), int(orig.height * esc)
    assert abs((nw / nh) - (orig.width / orig.height)) < 0.01


def test_el_kit_por_tema_NO_usa_la_portada_del_grado():
    """La compuerta de siempre: un cuaderno comprado por tema sigue con su tarjeta."""
    assert aw._portada_de_grado("9", False) is None


# ── un cuaderno escolar es de UN chico ──────────────────────────────────────────
def _perfiles(escolar, nombres, previos=None):
    """Corre `elegirPerfil` del player REAL con node y devuelve los perfiles que quedan.

    Se evalúa el código servido, no una reimplementación: lo que falló acá es una
    interacción entre tres funciones del player, y una copia en Python probaría otra cosa.
    """
    import json
    import subprocess
    src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "actividades_player.js")
    js = """
      const fs = require('fs');
      const src = fs.readFileSync(%s, 'utf8');
      const g = (a, b) => { const i = src.indexOf(a); return src.slice(i, src.indexOf(b, i)); };
      var D = {escolar_on: %s, nombre: "Peque"};
      var Store = {data: {profiles: %s, activeProfile: null}, save() {}};
      eval(g('const NOMBRE_GENERICO', 'function elegirPerfil(')
           + g('function elegirPerfil(', '  Store.save();') + '}'
           + 'function cerrarPerfil(){};function pintarHeader(){};function pintarMenu(){};'
           // `_perfilNuevo` se stubea: desde el 29-jul `elegirPerfil` lo llama para sembrar
           // el avatar heredado, y este test recorta el archivo por marcadores, así que la
           // función real no entra en el recorte. Se devuelve lo mismo que había antes del
           // avatar: este test cubre el manejo de PERFILES, no el avatar (eso está en
           // test_dificultad_por_dominio.py).
           + 'function _perfilNuevo(){return {stars:{}}};');
      for (const n of %s) elegirPerfil(n);
      console.log(JSON.stringify({p: Object.keys(Store.data.profiles),
                                  activo: Store.data.activeProfile}));
    """ % (json.dumps(src_path), "true" if escolar else "false",
           json.dumps(previos or {}), json.dumps(nombres))
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout.strip())


def test_en_el_cuaderno_escolar_cambiar_el_nombre_no_agrega_otro_chico():
    """Pablo (25-jul-2026): puso "Peque" —el placeholder precargado—, quiso corregirlo,
    y el cuaderno le creó un segundo perfil. Siguió intentando y llegó a TRES.
    "No quiero dos usuarios con la misma actividad, lo haría todo más complejo"."""
    r = _perfiles(True, ["Peque", "Pablo", "Lalo"])
    assert r["p"] == ["Lalo"], "quedaron %s" % r["p"]
    assert r["activo"] == "Lalo"


def test_renombrar_se_lleva_el_progreso():
    """Si al corregir el nombre se perdieran las estrellas, el chico empezaría de cero
    por un error de tipeo del padre."""
    r = _perfiles(True, ["Pablo"], previos={"Peque": {"stars": {"sopa": 3}}})
    assert r["p"] == ["Pablo"]


def test_no_se_pierde_progreso_al_renombrar_el_unico_perfil():
    """Con un solo chico, poner otro nombre ES renombrar: el perfil pasa a llamarse así
    y las estrellas viajan con él."""
    r = _perfiles(True, ["Otro"], previos={"Hermana": {"stars": {"sopa": 3}}})
    assert r["p"] == ["Otro"] and r["activo"] == "Otro"


def test_la_limpieza_no_se_lleva_un_perfil_con_progreso():
    """Si quedaron varios de antes del arreglo, sólo se descartan los VACÍOS: uno con
    estrellas es el trabajo de alguien y no se borra en silencio."""
    r = _perfiles(True, ["Pablo"],
                  previos={"Peque": {"stars": {}}, "Jugó": {"stars": {"sopa": 3}}})
    assert "Jugó" in r["p"], "se borró un perfil con progreso: %s" % r["p"]
    assert "Peque" not in r["p"], "quedó el vacío: %s" % r["p"]


def test_el_kit_por_tema_sigue_admitiendo_hermanos():
    """Un cuaderno de cumpleaños se comparte en casa; ahí varios perfiles SÍ tienen
    sentido. El cambio es sólo para el escolar, que es de un grado puntual."""
    r = _perfiles(False, ["Sofía", "Tomás", "Mia"])
    assert sorted(r["p"]) == ["Mia", "Sofía", "Tomás"]


def test_el_placeholder_no_se_precarga():
    """Que el input diga "Peque" invita a aceptarlo — y era lo que después no se podía
    corregir sin sumar un perfil."""
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "actividades_player.js"), encoding="utf-8").read()
    i = src.index("const deLaCompra")
    assert "NOMBRE_GENERICO" in src[i:i + 200]
