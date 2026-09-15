"""Los VIDEOS INTERACTIVOS: que lo que el guion nombra EXISTA, y que enseñen lo que dicen enseñar.

Pablo, 15-sep-2026: *"el video se pausa y hace una pregunta… si no contesta bien le puede dar una
pista"*. Hoy hay dos piezas: `todo_lo_que_nada` (2.º, grupos de animales) y `con_que_sonido` (1.º,
sonido inicial). Los tests recorren TODAS las que haya en `videos_interactivos/`.

Lo que cuida este archivo, y por qué cada cosa:

1. **Todo lo que el guion nombra existe.** Una imagen o una voz que falta no rompe nada visible: el
   reproductor sigue y el chico se queda mirando un hueco en silencio.
2. **Cada pausa tiene sus TRES pistas.** La escalera —pista corta, se ilumina, Carpi lo muestra— es
   la regla del cuaderno: nunca hay un «perdiste». Con dos pistas, el tercer error deja al chico
   trabado.
3. **El contenido dice la verdad.** El delfín va en mamífero; y en la pieza de sonidos, cada objeto
   de una pausa empieza de verdad con el sonido que pide la voz.
4. **Los textos que lee la voz** no llevan números en cifras ni «e» delante de palabra con i-: las dos
   cosas las pronuncia mal el motor (ver la skill `video-divulgacion`).
5. **`/vi/` no sirve archivos de otra carpeta.**
"""
import json
import os
import re
import sys
import unicodedata

import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import video_interactivo_web as viw   # noqa: E402

PIEZAS = sorted(p for p in os.listdir(os.path.join(BASE, "videos_interactivos"))
                if os.path.isfile(os.path.join(BASE, "videos_interactivos", p, "guion.json")))


def guion(pieza):
    with open(os.path.join(BASE, "videos_interactivos", pieza, "guion.json"), encoding="utf-8") as f:
        return json.load(f)


def existe(pieza, nombre):
    """En la carpeta de la pieza o en `_comun` (donde vive Carpi, que es de todas)."""
    return viw.ruta_de(pieza, nombre) is not None


def sin_tildes(t):
    t = unicodedata.normalize("NFD", (t or "").lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def test_hay_piezas():
    assert PIEZAS, "no hay ninguna pieza en videos_interactivos/"


@pytest.mark.parametrize("pieza", PIEZAS)
def test_cada_imagen_y_cada_voz_del_guion_existen(pieza):
    g = guion(pieza)
    faltan = [k + ".webp" for k in g["imagenes"] if not existe(pieza, k + ".webp")]
    faltan += ["voz_%s.mp3" % k for k in g["voces"] if not existe(pieza, "voz_%s.mp3" % k)]
    assert not faltan, "%s: el guion nombra lo que no está: %s" % (pieza, faltan)


@pytest.mark.parametrize("pieza", PIEZAS)
def test_los_pasos_apuntan_a_escenas_cosas_y_voces_que_existen(pieza):
    g = guion(pieza)
    escenas, voces = g["escenas"], g["voces"]
    for i, p in enumerate(g["pasos"]):
        assert p["escena"] in escenas, "%s paso %d: escena inexistente %r" % (pieza, i, p["escena"])
        cosas = escenas[p["escena"]]["animales"]
        for clave in ("voz", "consigna", "fin", "va_aca"):
            if p.get(clave):
                assert p[clave] in voces, "%s paso %d: voz inexistente %r" % (pieza, i, p[clave])
        for a in p.get("correctos", []) + (p.get("solo") or []) + list(p.get("acomodar") or {}):
            assert a in cosas, "%s paso %d: no está en la escena: %r" % (pieza, i, a)
        for it in p.get("items", []):
            assert it["animal"] in cosas and it["pista"] in voces
            assert it["grupo"] in [x["id"] for x in p["grupos"]]
        for x in p.get("grupos", []):
            assert x["icono"] in g["imagenes"], "%s paso %d: ícono inexistente" % (pieza, i)
    for e in escenas.values():
        assert e["fondo"] in g["imagenes"]
        for c in e["animales"].values():
            assert c["img"] in g["imagenes"]


@pytest.mark.parametrize("pieza", PIEZAS)
def test_cada_pausa_tiene_las_tres_pistas(pieza):
    """La escalera completa: pista corta → se ilumina → Carpi lo muestra. Con menos, el chico que se
    equivoca tres veces se queda sin salida, que es lo que este formato no puede hacer."""
    for i, p in enumerate(guion(pieza)["pasos"]):
        if p["tipo"] in ("tocar", "elegir"):
            assert len(p.get("pistas") or []) == 3, "%s paso %d tiene %d pistas" % (
                pieza, i, len(p.get("pistas") or []))
        if p["tipo"] == "clasificar":
            assert p.get("va_aca"), "%s: falta el «va acá» del tercer error" % pieza
            for it in p["items"]:
                assert it.get("pista"), "%s: %r sin pista propia" % (pieza, it["animal"])


@pytest.mark.parametrize("pieza", PIEZAS)
def test_los_textos_de_la_voz_no_tienen_las_trampas_conocidas(pieza):
    for clave, texto in guion(pieza)["voces"].items():
        assert not re.search(r"\d", texto), "%s/%s: número en cifras" % (pieza, clave)
        assert not re.search(r"\be\s+[iíhH]", texto), "%s/%s: «e» delante de i-" % (pieza, clave)
        assert texto.strip() == texto and len(texto) > 3, "%s/%s: texto raro" % (pieza, clave)


# ── el contenido de cada pieza, que es lo que ningún chequeo genérico ve ──────────────────

def test_todo_lo_que_nada_clasifica_bien_a_cada_animal():
    """El delfín es mamífero y el pingüino es ave: si alguien los cambia de grupo, el video enseña
    algo falso y nadie se entera hasta que lo vea una maestra."""
    esperado = {"pez": "pez", "delfin": "mamifero", "pinguino": "ave"}
    for p in guion("todo_lo_que_nada")["pasos"]:
        for it in p.get("items", []):
            assert esperado[it["animal"]] == it["grupo"], "%s quedó en %s" % (it["animal"], it["grupo"])


def test_con_que_sonido_pide_sonidos_que_se_pueden_ALARGAR():
    """En castellano las oclusivas (p, t, k) NO se pueden pronunciar solas, sin vocal: la voz terminaba
    diciendo el NOMBRE de la letra, que es lo contrario de lo que enseña esta pieza (15-sep-2026, se
    cambió la pausa de la pe por la de la ele). Sólo sonidos que se sostienen."""
    g = guion("con_que_sonido")
    alargables = set("mslnfrjz")
    for p in g["pasos"]:
        if p["tipo"] != "tocar":
            continue
        pedido = re.findall(r"\b([a-záéíóúñ])\1{2,}\b", sin_tildes(g["voces"][p["consigna"]]))
        for letra in pedido:
            assert letra in alargables, "la pausa pide el sonido %r, que no se puede decir solo" % letra


def test_con_que_sonido_las_cosas_empiezan_con_el_sonido_que_pide_la_voz():
    """El corazón de la pieza: si en la pausa del sonido mmm se cuela la pelota, el chico aprende mal."""
    g = guion("con_que_sonido")
    for i, p in enumerate(g["pasos"]):
        if p["tipo"] != "tocar":
            continue
        pedido = re.findall(r"\b([a-záéíóúñ])\1{2,}\b", sin_tildes(g["voces"][p["consigna"]]))
        if not pedido:
            continue                       # la última pausa pide la LETRA, no el sonido
        letra = pedido[0]
        cosas = g["escenas"][p["escena"]]["animales"]
        if all(c.startswith("letra_") for c in cosas):
            # la pausa que une el sonido con su letra: la tarjeta correcta tiene que ser ESA letra
            assert p["correctos"] == ["letra_" + letra], (
                "paso %d: el sonido %r tendría que llevar a la letra %r y lleva a %s"
                % (i, letra, letra, p["correctos"]))
            continue
        for cosa in p["correctos"]:
            assert sin_tildes(cosa).startswith(letra), (
                "paso %d: %r no empieza con el sonido %r" % (i, cosa, letra))
        for cosa in cosas:
            if cosa not in p["correctos"]:
                assert not sin_tildes(cosa).startswith(letra), (
                    "paso %d: %r empieza con %r y quedó fuera de la respuesta" % (i, cosa, letra))


# ── la página y el servicio ───────────────────────────────────────────────────────────────

@pytest.mark.parametrize("pieza", PIEZAS)
def test_la_pagina_se_arma_sin_marcadores_y_sin_los_prompts(pieza):
    page = viw.html(pieza)
    assert page and "window.GUION = {" in page
    assert "{{" not in page, "%s: quedó un marcador sin reemplazar" % pieza
    assert "Ilustración infantil" not in page, "%s: se publicaron los prompts" % pieza


@pytest.mark.parametrize("pieza", PIEZAS)
def test_sirve_el_reproductor_y_los_archivos_de_la_pieza(pieza):
    g = guion(pieza)
    js, ct = viw.archivo(pieza, "player.js")
    assert b"KYDO_VI_RESULTADO" in js and "javascript" in ct
    fondo = list(g["escenas"].values())[0]["fondo"] + ".webp"
    img, ct = viw.archivo(pieza, fondo)
    assert img[:4] == b"RIFF" and ct == "image/webp"
    mp3, ct = viw.archivo(pieza, "voz_%s.mp3" % list(g["voces"])[0])
    assert len(mp3) > 1000 and ct == "audio/mpeg"


def test_no_sirve_nada_de_afuera_de_la_pieza():
    for malo in ("../servicio.py", "/etc/passwd", "guion.json", "player.js.bak", "", "..%2fx.webp"):
        assert viw.archivo(PIEZAS[0], malo) is None, "sirvió %r" % malo
    assert viw.html("no_existe") is None
    assert viw.archivo("no_existe", "player.js") is None


def test_el_reproductor_no_pide_nada_de_afuera():
    """Todo se sirve bajo /vi/<pieza>/: una URL absoluta a otro dominio rompería el cuaderno del chico
    el día que ese dominio no esté."""
    for arch in ("video_interactivo_player.html", "video_interactivo_player.js"):
        txt = open(os.path.join(BASE, arch), encoding="utf-8").read()
        assert "http://" not in txt and "https://" not in txt, "%s pide algo de afuera" % arch
