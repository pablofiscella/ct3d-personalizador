"""La pronunciación de las actividades de Inglés.

Las cuatro actividades de Inglés eran de TEXTO: enseñaban a escribirlo, no a decirlo.
La auditoría de 7° las pide como flashcards CON fonética, y es lo primero que marca un
maestro de inglés.

Lo que se verifica acá es lo que se rompe en silencio: que cada término tenga su clip,
que el clip exista de verdad en el repo, y que la voz NO sea la rioplatense de las
consignas — para eso hay una voz nativa inglesa aparte.
"""
import json
import os
import re

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(BASEDIR, "audio_ingles")
PLAYER = open(os.path.join(BASEDIR, "actividades_player.js"), encoding="utf-8").read()

# El ancla lleva el "= {": `GAMES.ingles_basico` a secas aparece ANTES, en un
# comentario de `_botonIngles` que remite acá, y los tests medían 200 KB de otro
# código creyendo que miraban la actividad.


def _manifest():
    return json.load(open(os.path.join(DIR, "manifest.json"), encoding="utf-8"))


def _terminos_esperados():
    """Los términos en inglés de las actividades del catálogo (van entre « »)."""
    import actividades_curriculum as ac
    esperados = set()
    for a in ac.CATALOGO:
        if not a["id"].startswith("ingles"):
            continue
        for i, it in enumerate(a.get("banco") or []):
            if re.search(r"«[^»]+»", it.get("q", "")):
                # el player recibe el id TRUNCADO a 10 (gen_curriculum.py: a["id"][:10]),
                # así que el manifest tiene que estar keyado igual o el botón queda mudo
                esperados.add("%s#%d" % (a["id"][:10], i))
    return esperados


def test_toda_actividad_de_ingles_tiene_su_clip():
    """Un ítem de inglés sin audio es la mitad del contenido: se ve escrito y no se
    sabe cómo suena."""
    faltan = sorted(_terminos_esperados() - set(_manifest()))
    assert not faltan, "ítems de inglés sin clip de pronunciación: %s" % faltan[:10]


def test_los_clips_declarados_existen():
    """Un manifest que apunta a un mp3 que no está deja el botón mudo, y mudo se ve
    igual que roto."""
    faltan = sorted(fn for fn in set(_manifest().values())
                    if not os.path.isfile(os.path.join(DIR, fn)))
    assert not faltan, "declarados en el manifest y ausentes del repo: %s" % faltan[:10]


def test_el_juego_viejo_de_ingles_tambien_suena():
    """`ingles_basico` ya estaba en el menú de 7° antes del catálogo curricular y
    también era mudo."""
    hay = [k for k in _manifest() if k.startswith("ingles_basico#")]
    assert len(hay) >= 20, "ingles_basico tiene %d clips, esperaba el banco entero" % len(hay)


def test_la_voz_del_ingles_no_es_la_de_las_consignas():
    """La voz de las consignas es rioplatense a propósito. Leer inglés con esa voz
    enseñaría una pronunciación equivocada, que es peor que no tener audio."""
    import actividades_web as aw
    clips = set(_manifest().values())
    d = os.path.join(BASEDIR, "audio_consignas")
    consignas = set(os.listdir(d)) if os.path.isdir(d) else set()
    assert not (clips & consignas), "los clips de inglés salen del pozo de consignas"
    assert all(fn.startswith("en_") for fn in clips), \
        "los clips de inglés tienen que vivir aparte, con prefijo en_"
    # y el server tiene que poder servirlos sin abrir la puerta a cualquier archivo
    assert aw._ASSET_RE.fullmatch("en_0123456789abcdef.mp3")
    assert aw._ASSET_RE.fullmatch("ingles_manifest.json")
    for malo in ("en_.mp3", "en_XX.mp3", "../../etc/passwd", "en_0123456789abcdef.mp3.exe"):
        assert not aw._ASSET_RE.fullmatch(malo), "la whitelist acepta %r" % malo


def test_se_puede_escuchar_ANTES_de_elegir():
    """Pablo, 03-ago-2026, después de una primera versión que sólo lo mostraba antes en
    cinco preguntas: *"en el mismo momento en el que estoy por seleccionar qué opción es,
    debería tener el botón para escuchar; y sólo aparece después de que elijo y desaparece
    rápido porque viene la otra"*.

    Decisión de Pablo, con su costo asumido: en «¿Cómo se dice "agua" en inglés?» el clip
    dice *water*, así que se puede resolver escuchando. Es una actividad para APRENDER a
    decirlo, no para tomar examen — y atar el sonido con cuál de tres escrituras le
    corresponde sigue siendo el trabajo que cuesta en inglés.

    El test anterior exigía lo contrario (el botón recién al acertar). Se cambia a
    propósito y queda escrito por qué, para que no se "arregle" de vuelta."""
    i = PLAYER.index("GAMES.ingles_basico = {")
    cuerpo = PLAYER[i:i + 6000]
    pos_boton = cuerpo.index("_botonIngles(zonaAudio")
    pos_ops = cuerpo.index("const opciones = shuffle")
    assert pos_boton < pos_ops, \
        "el botón de escuchar se dibuja después de las opciones: no está al elegir"
    assert "it.enQ" not in cuerpo, \
        "quedó el gate viejo: en algunas preguntas no se puede escuchar antes"


def test_la_ronda_espera_a_que_termine_el_audio():
    """*"desaparece rápido porque viene la otra"*: al acertar la palabra suena sola y la
    ronda no se va hasta que termina. Con `espera(1600)` pelado se cortaba al medio."""
    i = PLAYER.index("GAMES.ingles_basico = {")
    cuerpo = PLAYER[i:i + 6000]
    assert "_sonarIngles(\"ingles_basico\", idx)" in cuerpo, \
        "al acertar no se reproduce la palabra"
    assert "Promise.all([espera(1600)" in cuerpo, \
        "la ronda no espera a que el audio termine"


# ── el botón de escuchar y la velocidad (03-ago-2026) ──────────────────────────────────
# Pablo, en 7.º: *"aparece en english time, está el escuchar después de que elegís y no
# antes. O sea no se puede escuchar"*. Y: *"cuando se escucha el inglés que sea más
# lento"*.

def _banco_del_player():
    import re as _re
    bloque = _re.search(r"const INGLES_BANCO = \[([\s\S]*?)\n\];", PLAYER).group(1)
    return [l for l in bloque.splitlines() if l.strip().startswith("{")]


def test_se_escucha_mas_lento():
    """Se hace con `playbackRate` y NO regenerando los clips: la voz ya sale con
    `speed 0.8` de ElevenLabs y se MIDIÓ que bajarla a 0.7 —el mínimo— no cambia nada en
    palabras sueltas (el mismo "book": 1.13 s → 1.10 s)."""
    i = PLAYER.index("function _sonarIngles")
    cuerpo = PLAYER[i:i + 2200]
    assert "playbackRate = 0.8" in cuerpo, "el inglés no se reproduce más lento"
    assert "preservesPitch" in cuerpo, \
        "sin preservar el tono la voz suena a cinta ralentizada, peor que rápida"


def test_ninguna_palabra_del_banco_se_queda_sin_clip():
    """`ingles_basico#23` («tree») estaba en el banco y no tenía audio: el botón aparecía
    y no sonaba nada. Se generó con la misma receta de Dorothy."""
    man = _manifest()
    n = len(_banco_del_player())
    faltan = [i for i in range(n) if "ingles_basico#%d" % i not in man]
    assert not faltan, "palabras del banco sin pronunciación: %s" % faltan


def test_escuchar_antes_de_contestar_NO_puntua_como_dominio():
    """Pablo, 03-ago-2026: *"lo que sí, si escucha no se tiene que tomar como bien"*.

    Es lo que hace que el botón pueda estar SIEMPRE sin arruinar la medición: en «¿Cómo se
    dice "agua" en inglés?» el clip dice *water*, así que oírlo y después elegir no prueba
    que lo sepa. Se anota con el mismo mecanismo que la ayuda de las cuentas en columna
    (`_estrellasConAyuda`, 31-jul-2026): el festejo de completar se mantiene, lo que baja
    son las estrellas — que es lo que el motor adaptativo lee como dominio."""
    i = PLAYER.index("GAMES.ingles_basico = {")
    cuerpo = PLAYER[i:i + 4000]
    assert "rondasConAudio" in cuerpo, "escuchar no se anota"
    assert "_estrellasConAyuda(rondasConAudio, rondas)" in cuerpo, \
        "las estrellas no miran si escuchó: resolver oyendo daría 3★ y el motor le subiría"
    # una vez por ronda, no una por toque: si no, escuchar dos veces contaría doble
    assert "if (!escuchoAntes)" in cuerpo, "cada toque del parlante cuenta como una ronda"


def test_el_audio_del_ACIERTO_no_cuenta_como_ayuda():
    """El que suena solo al acertar es premio, no ayuda: el chico ya eligió. Si contara,
    todas las rondas quedarían marcadas y nadie podría sacar 3★ nunca."""
    i = PLAYER.index("GAMES.ingles_basico = {")
    cuerpo = PLAYER[i:i + 4000]
    j = cuerpo.index("ctx.bien()")
    assert "rondasConAudio++" not in cuerpo[j:], \
        "el audio que suena al acertar se está anotando como ayuda"


# ── que cada clip diga LO QUE TIENE QUE DECIR (03-ago-2026) ────────────────────────────
# Pablo, apretando el botón: *"apretás el botón y hasta habla en español o responde otra
# cosa"*.
#
# Los clips se habían generado usando la RESPUESTA de cada pregunta. Es correcto en 19 de
# las 24 —«¿Cómo se dice "perro" en inglés?» → *dog*— pero en las otras cinco la respuesta
# es en castellano («¿Qué significa "book"?» → libro), así que el botón de una actividad
# de inglés decía "libro", "rojo", "feliz", "amarillo" y "3" con voz británica.
#
# No se podía auditar: el nombre del archivo era un hash opaco, así que un clip equivocado
# se veía igual que uno correcto. Ahora el nombre ES el hash del texto y de la voz, y este
# test recalcula los 67 y compara. Un clip mal apareado no llega a producción.

VOZ_INGLES = "ThT5KcBeYPX3keUQqHPh"


def _termino_ingles_de_cada_clave():
    """Qué palabra INGLESA le toca a cada clave, leída de las fuentes de verdad.

    En `ingles_basico` el término es la respuesta cuando la pregunta pide el inglés
    («¿Cómo se dice "perro" en inglés?» → dog); si no, está en « » dentro de la pregunta
    («¿Qué significa "book"?» → book). Es exactamente la distinción que se había perdido."""
    import re as _re
    import actividades_curriculum as ac
    fuera = {}
    bloque = _re.search(r"const INGLES_BANCO = \[([\s\S]*?)\n\];", PLAYER).group(1)
    for i, linea in enumerate(l for l in bloque.splitlines() if l.strip().startswith("{")):
        q = _re.search(r'q: "([^"]*)"', linea).group(1)
        ok = _re.search(r'ok: "([^"]*)"', linea).group(1)
        fuera["ingles_basico#%d" % i] = ok if "en inglés?" in q \
            else _re.search(r"«([^»]+)»", q).group(1)
    for a in ac.CATALOGO:
        if not a["id"].startswith("ingles"):
            continue
        for i, it in enumerate(a.get("banco") or []):
            m = _re.search(r"«([^»]+)»", it.get("q", ""))
            if m:
                fuera["%s#%d" % (a["id"][:10], i)] = m.group(1)
    return fuera


def test_ningun_clip_dice_otra_cosa():
    """EL test. El nombre del archivo es `sha1(voz|texto)`, así que se puede verificar sin
    escuchar: si el clip fuera de otra palabra, el hash no daría."""
    import hashlib
    man = _manifest()
    terminos = _termino_ingles_de_cada_clave()
    malos = []
    for k, fn in man.items():
        t = terminos.get(k)
        if t is None:
            malos.append((k, "clave sin término en las fuentes"))
            continue
        esperado = "en_" + hashlib.sha1(
            (VOZ_INGLES + "|" + t).encode()).hexdigest()[:16] + ".mp3"
        if fn != esperado:
            malos.append((k, "debería decir %r y el archivo no corresponde" % t))
    assert not malos, "clips mal apareados: %s" % malos[:5]


def test_ningun_clip_de_ingles_dice_una_palabra_en_castellano():
    """El síntoma tal cual: una actividad de inglés no puede pronunciar «libro» ni «rojo».
    Se mira contra las RESPUESTAS en castellano del propio banco, que es de donde salieron."""
    import re as _re
    terminos = _termino_ingles_de_cada_clave()
    bloque = _re.search(r"const INGLES_BANCO = \[([\s\S]*?)\n\];", PLAYER).group(1)
    for i, linea in enumerate(l for l in bloque.splitlines() if l.strip().startswith("{")):
        q = _re.search(r'q: "([^"]*)"', linea).group(1)
        if "en inglés?" in q:
            continue                      # ahí la respuesta SÍ es el inglés
        ok = _re.search(r'ok: "([^"]*)"', linea).group(1)
        dice = terminos["ingles_basico#%d" % i]
        assert dice != ok, \
            "#%d dice %r, que es la respuesta en castellano de «%s»" % (i, dice, q)


# ── el manifest se renueva con el player (03-ago-2026) ─────────────────────────────────
# Pablo, después de regenerar los clips: *"no se escucha"*, y enseguida *"dice cualquier
# cosa"*. Los archivos nuevos estaban bien y servidos con 200 — lo que fallaba era el
# CACHÉ: el manifest se pedía sin `?v=`, el navegador se quedaba con el viejo, y ése
# apunta a los 66 archivos que la regeneración borra. Silencio; y mientras algunos mp3
# seguían en caché y otros no, cualquier cosa.

def test_el_manifest_se_pide_con_version():
    """Sin `?v=`, arreglar una pronunciación no le llega NUNCA al que ya abrió el
    cuaderno: se queda con el manifest viejo hasta que el navegador decida soltarlo."""
    i = PLAYER.index("async function _cargarInglesManifest")
    cuerpo = PLAYER[i:i + 1800]
    assert 'fetch("ingles_manifest.json")' not in cuerpo, \
        "el manifest se pide pelado: el navegador lo cachea y los clips nuevos no llegan"
    assert '"?v=" + encodeURIComponent(v)' in cuerpo, "no se le agrega la versión"


def test_la_version_del_player_mira_los_audios_de_ingles():
    """Regenerar los clips cambia sus NOMBRES y borra los viejos. Si la versión no se
    moviera, el player cacheado seguiría pidiendo archivos que ya no existen."""
    import importlib
    import os
    import time
    aw = importlib.import_module("actividades_web")
    p = os.path.join(aw.INGLES_DIR, "manifest.json")
    antes = aw._player_version()
    st = os.stat(p)
    try:
        os.utime(p, (st.st_atime, st.st_mtime + 60))
        assert aw._player_version() != antes, \
            "tocar los audios de inglés no cambia la versión del player"
    finally:
        os.utime(p, (st.st_atime, st.st_mtime))
    assert aw._player_version() == antes, "no se restauró el mtime"


# ── los iconos se tienen que VER (03-ago-2026) ─────────────────────────────────────────
# Pablo: *"desaparecieron los iconos de inglés, tarjeta 1 (english time) y tarjeta 4
# (vocabulario en inglés)"*.
#
# No se habían borrado: las dos usaban 🇬🇧, que es una BANDERA — dos "indicadores
# regionales" (G + B) que el sistema tiene que componer. **Windows no compone banderas**:
# Chrome dibuja las dos letras sueltas ("GB" en un recuadro gris, como se veía en la
# primera captura) o directamente nada. Y la mayoría de las familias del país abre el
# cuaderno desde una notebook con Windows.
#
# También estaba 🇦🇷 en «Camino a la independencia», con el mismo problema.

def test_ningun_icono_es_una_bandera():
    """Las banderas son el único emoji que depende de que el SISTEMA las componga. El
    resto (📗, ⏱️, 🗣️, 🔤, 🎖️) se dibuja igual en Windows, Android, iPhone y Linux."""
    import re as _re
    import actividades_curriculum as ac
    BANDERA = _re.compile("[\U0001F1E6-\U0001F1FF]")
    malos = [(a["id"], a.get("icono")) for a in ac.CATALOGO
             if BANDERA.search(a.get("icono") or "")]
    ruta = os.path.join(BASEDIR, "actividades_web.py")
    src = open(ruta, encoding="utf-8").read()
    for m in _re.finditer(r'"id": "([^"]+)"[^}]*?"icono": "([^"]*)"', src):
        if BANDERA.search(m.group(2)):
            malos.append((m.group(1), m.group(2)))
    assert not malos, ("estos iconos son banderas y en Windows no se ven: %s" % malos)


def test_las_dos_de_ingles_tienen_icono():
    """El control: que no se hayan quedado sin ninguno al sacarles la bandera."""
    import actividades_curriculum as ac
    src = open(os.path.join(BASEDIR, "actividades_web.py"), encoding="utf-8").read()
    assert '"titulo": "English time", "icono": "' in src
    i = src.index('"titulo": "English time", "icono": "')
    icono = src[i + len('"titulo": "English time", "icono": "'):].split('"')[0]
    assert icono.strip(), "English time se quedó sin icono"
    voc = [a for a in ac.CATALOGO if a["id"] == "ingles_vocabulario_7"][0]
    assert (voc.get("icono") or "").strip(), "Vocabulario en inglés se quedó sin icono"
