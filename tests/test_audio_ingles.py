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
    """En `ingles_basico` el término en inglés ES la respuesta, así que el botón
    aparece recién al acertar. En las otras el inglés está en la consigna."""
    i = PLAYER.index("GAMES.ingles_basico")
    cuerpo = PLAYER[i:i + 2500]
    pos_boton = cuerpo.index("_botonIngles(zonaAudio")
    pos_bien = cuerpo.index("ctx.bien()")
    assert pos_bien < pos_boton, ("el botón de audio se pinta antes de acertar: "
                                  "daría la respuesta servida")
