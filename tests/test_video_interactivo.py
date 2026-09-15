"""El VIDEO INTERACTIVO: que lo que el guion nombra EXISTA, y que la voz no tenga trampas.

Pablo, 15-sep-2026: *"el video se pausa y hace una pregunta… si no contesta bien le puede dar una
pista"*. El piloto es `todo_lo_que_nada` (2.º grado, saber CDM-2-animales).

Lo que cuida este archivo, y por qué cada cosa:

1. **Todo lo que el guion nombra existe.** Una imagen o una voz que falta no rompe nada visible: el
   reproductor sigue y el chico se queda mirando un hueco en silencio. Eso no se ve en una prueba a
   ojo, se ve acá.
2. **Cada pausa tiene sus TRES pistas.** La escalera —pista corta, se ilumina, Carpi lo muestra— es
   la regla pedagógica del cuaderno: nunca hay un «perdiste». Con dos pistas, el tercer error deja
   al chico trabado.
3. **Los textos que lee la voz** no llevan números en cifras ni «e» delante de palabra con i-: las
   dos cosas las pronuncia mal el motor de voz, y ya costaron regrabaciones (ver la skill
   `video-divulgacion`).
4. **La página no sirve archivos de otra carpeta.** `/vi/<pieza>/<archivo>` toma lo que le pidan.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import video_interactivo_web as viw   # noqa: E402

PIEZA = "todo_lo_que_nada"
CARPETA = os.path.join(BASE, "videos_interactivos", PIEZA)
GUION = json.load(open(os.path.join(CARPETA, "guion.json"), encoding="utf-8"))


def _existe(nombre):
    return os.path.isfile(os.path.join(CARPETA, nombre))


def test_cada_imagen_del_guion_esta_generada():
    faltan = [k for k in GUION["imagenes"] if not _existe(k + ".webp")]
    assert not faltan, "imágenes que el guion nombra y no están: %s" % faltan


def test_cada_voz_del_guion_esta_grabada():
    faltan = [k for k in GUION["voces"] if not _existe("voz_%s.mp3" % k)]
    assert not faltan, "voces que el guion nombra y no están: %s" % faltan


def test_los_pasos_apuntan_a_escenas_animales_y_voces_que_existen():
    escenas, voces = GUION["escenas"], GUION["voces"]
    for i, p in enumerate(GUION["pasos"]):
        assert p["escena"] in escenas, "paso %d: escena inexistente %r" % (i, p["escena"])
        animales = escenas[p["escena"]]["animales"]
        for clave in ("voz", "consigna", "fin", "va_aca"):
            if p.get(clave):
                assert p[clave] in voces, "paso %d: voz inexistente %r" % (i, p[clave])
        for a in p.get("correctos", []) + (p.get("solo") or []) + list(p.get("acomodar") or {}):
            assert a in animales, "paso %d: animal inexistente %r" % (i, a)
        for it in p.get("items", []):
            assert it["animal"] in animales, "paso %d: item inexistente %r" % (i, it["animal"])
            assert it["pista"] in voces, "paso %d: pista inexistente %r" % (i, it["pista"])
            assert it["grupo"] in [g["id"] for g in p["grupos"]], "paso %d: grupo inexistente" % i
        for g in p.get("grupos", []):
            assert g["icono"] in GUION["imagenes"], "paso %d: ícono inexistente %r" % (i, g["icono"])


def test_cada_pausa_tiene_las_tres_pistas():
    """La escalera completa: pista corta → se ilumina → Carpi lo muestra. Con menos, el chico que
    se equivoca tres veces se queda sin salida, que es justo lo que este formato no puede hacer."""
    for i, p in enumerate(GUION["pasos"]):
        if p["tipo"] in ("tocar", "elegir"):
            assert len(p.get("pistas") or []) == 3, "paso %d (%s) tiene %d pistas" % (
                i, p["tipo"], len(p.get("pistas") or []))
        if p["tipo"] == "clasificar":
            assert p.get("va_aca"), "la clasificación necesita el «va acá» del tercer error"
            for it in p["items"]:
                assert it.get("pista"), "cada animal necesita su propia pista: %r" % it["animal"]


def test_el_animal_de_cada_item_esta_en_la_escena_y_su_grupo_es_el_correcto():
    """El contenido, no el código: el delfín va en mamífero y el pingüino en ave. Si alguien los
    cambia de grupo, el video enseña algo falso."""
    esperado = {"pez": "pez", "delfin": "mamifero", "pinguino": "ave"}
    for p in GUION["pasos"]:
        for it in p.get("items", []):
            assert esperado[it["animal"]] == it["grupo"], (
                "%s quedó clasificado como %s" % (it["animal"], it["grupo"]))


def test_los_textos_de_la_voz_no_tienen_las_trampas_conocidas():
    for clave, texto in GUION["voces"].items():
        assert not re.search(r"\d", texto), "%s: número en cifras (el motor los lee mal)" % clave
        assert not re.search(r"\be\s+[iíhH]", texto), "%s: «e» delante de palabra con i-" % clave
        assert texto.strip() == texto and len(texto) > 3, "%s: texto vacío o con espacios sueltos" % clave


def test_la_pagina_se_arma_y_no_deja_marcadores_sin_reemplazar():
    page = viw.html(PIEZA)
    assert page and "window.GUION = {" in page
    assert "{{" not in page, "quedó un marcador sin reemplazar"
    assert "¿Todo lo que nada es pez?" in page


def test_la_pagina_no_publica_los_prompts_de_produccion():
    """Los prompts son de la cocina: no le sirven al reproductor y describen cómo se fabrica el
    material. Viajan los nombres, no las recetas."""
    page = viw.html(PIEZA)
    assert "Ilustración infantil" not in page and "pingüino de Magallanes" not in page


def test_sirve_el_reproductor_las_imagenes_y_la_voz():
    js, ct = viw.archivo(PIEZA, "player.js")
    assert b"KYDO_VI_RESULTADO" in js and "javascript" in ct
    img, ct = viw.archivo(PIEZA, "fondo_costa.webp")
    assert img[:4] == b"RIFF" and ct == "image/webp"
    mp3, ct = viw.archivo(PIEZA, "voz_intro.mp3")
    assert len(mp3) > 1000 and ct == "audio/mpeg"


def test_no_sirve_nada_de_afuera_de_la_pieza():
    for malo in ("../servicio.py", "/etc/passwd", "guion.json", "player.js.bak", "", "..%2fx.webp"):
        assert viw.archivo(PIEZA, malo) is None, "sirvió %r" % malo
    assert viw.html("no_existe") is None
    assert viw.archivo("no_existe", "player.js") is None


def test_el_reproductor_no_pide_nada_de_afuera():
    """Todo se sirve bajo /vi/<pieza>/: una URL absoluta a otro dominio rompería el cuaderno del
    chico el día que ese dominio no esté."""
    for arch in ("video_interactivo_player.html", "video_interactivo_player.js"):
        txt = open(os.path.join(BASE, arch), encoding="utf-8").read()
        assert "http://" not in txt and "https://" not in txt, "%s pide algo de afuera" % arch
