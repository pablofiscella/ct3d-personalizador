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


def test_el_boton_no_regala_la_respuesta():
    """Lo que protege este test: que oír el clip nunca CONTESTE la pregunta.

    Escrito el 27-jul daba por hecho que en `ingles_basico` el término en inglés es
    siempre la respuesta, y por eso exigía que el botón se pintara después de acertar,
    siempre. Es cierto en 19 de las 24 preguntas, pero no en las cinco donde el inglés
    está en el ENUNCIADO («¿Qué significa "book"?» → libro): ahí escuchar no revela nada
    y el botón tardío dejaba la actividad sin su mitad — Pablo lo encontró jugando el
    03-ago-2026, *"o sea no se puede escuchar"*.

    Así que lo que se exige ahora es lo mismo de siempre, bien dicho: **el botón que
    diría la respuesta sigue apareciendo recién al acertar**."""
    i = PLAYER.index("GAMES.ingles_basico")
    cuerpo = PLAYER[i:i + 3000]
    tardio = cuerpo.index("if (!it.enQ) {")        # el que revelaría la respuesta
    assert cuerpo.index("ctx.bien()") < tardio, \
        "el botón de audio se pinta antes de acertar: daría la respuesta servida"


# ── el botón de escuchar y la velocidad (03-ago-2026) ──────────────────────────────────
# Pablo, en 7.º: *"aparece en english time, está el escuchar después de que elegís y no
# antes. O sea no se puede escuchar"*. Y: *"cuando se escucha el inglés que sea más
# lento"*.

def _banco_del_player():
    import re as _re
    bloque = _re.search(r"const INGLES_BANCO = \[([\s\S]*?)\n\];", PLAYER).group(1)
    return [l for l in bloque.splitlines() if l.strip().startswith("{")]


def test_cuando_el_ingles_esta_en_la_PREGUNTA_se_puede_escuchar_antes():
    """El caso que reportó Pablo. En «¿Qué significa "book"?» la respuesta es en
    castellano (libro/mesa/silla): oír el término NO la revela, y es el ejercicio.
    Esconder el botón hasta después de contestar dejaba la actividad sin su mitad."""
    import re as _re
    marcadas = [l for l in _banco_del_player() if "enQ" in l]
    assert len(marcadas) == 5, "cambió el banco: hay %d preguntas con el inglés en el enunciado" % len(marcadas)
    for l in marcadas:
        # el término entre « » de la pregunta tiene que ser el INGLÉS, no la respuesta
        entre = _re.search(r"«([^»]+)»", l).group(1)
        ok = _re.search(r'ok: "([^"]*)"', l).group(1)
        assert entre != ok, "en %r el término de la pregunta es la respuesta" % l.strip()[:60]


def test_cuando_el_ingles_es_la_RESPUESTA_el_boton_sigue_apareciendo_despues():
    """El control. Si se mostrara siempre, «¿Cómo se dice "libro" en inglés?» se
    resolvería tocando el parlante: la respuesta servida."""
    assert "if (!it.enQ) {" in PLAYER, "se perdió el gate del botón tardío"
    i = PLAYER.index("GAMES.ingles_basico")
    cuerpo = PLAYER[i:i + 3000]
    assert cuerpo.index("if (it.enQ)") < cuerpo.index("if (!it.enQ)"), \
        "el botón temprano tiene que decidirse ANTES de dibujar las opciones"


def test_no_queda_una_tarjeta_blanca_vacia():
    """La barra en blanco de la captura: un `.tablero` vacío se dibuja igual. La zona del
    audio sólo se agrega cuando tiene algo adentro."""
    i = PLAYER.index("GAMES.ingles_basico")
    cuerpo = PLAYER[i:i + 3000]
    j = cuerpo.index('const zonaAudio = el("div", "tablero")')
    entre = cuerpo[j:cuerpo.index("if (it.enQ)", j)]
    assert "appendChild(zonaAudio)" not in entre, \
        "la zona del audio se agrega al DOM antes de saber si va a tener botón"


def test_se_escucha_mas_lento():
    """Se hace con `playbackRate` y NO regenerando los clips: la voz ya sale con
    `speed 0.8` de ElevenLabs y se MIDIÓ que bajarla a 0.7 —el mínimo— no cambia nada en
    palabras sueltas (el mismo "book": 1.13 s → 1.10 s)."""
    i = PLAYER.index("function _botonIngles")
    cuerpo = PLAYER[i:i + 1800]
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
