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
import shutil
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


def versiones(paso):
    """Las versiones de un paso: las `variantes` que se sortean, o el paso tal cual.

    Un paso con variantes le hace otra pregunta a cada chico —y al mismo chico si lo repite—, así
    que cada variante tiene que cumplir sola lo mismo que cumpliría el paso."""
    if paso.get("variantes"):
        return [dict(paso, **v) for v in paso["variantes"]]
    return [paso]


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
    for i, p0 in enumerate(g["pasos"]):
      assert p0["escena"] in escenas, "%s paso %d: escena inexistente %r" % (pieza, i, p0["escena"])
      for p in versiones(p0):
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
    for i, p0 in enumerate(guion(pieza)["pasos"]):
      for p in versiones(p0):
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


@pytest.mark.parametrize("pieza", PIEZAS)
def test_la_voz_no_nombra_algo_de_la_escena_que_no_sea_la_respuesta(pieza):
    """Pablo, 15-sep-2026: *"elegí mesa y me dijo que ya estaba sin seleccionar libro"*.

    La pausa de la ele usaba el LIBRO como palabra de referencia —«tocá lo que empieza igual que
    libro»— y el libro estaba dibujado en la escena, tocable, y NO era la respuesta. La consigna
    señalaba con el dedo lo único que estaba mal tocar. Si una voz nombra algo que SE PUEDE TOCAR,
    ese algo tiene que ser una de las respuestas.

    Vale sólo para las pausas de `tocar`: en `elegir` la escena no se toca —se responde con botones—
    y nombrar al delfín que se está mirando es justamente la consigna."""
    g = guion(pieza)
    for i, p0 in enumerate(g["pasos"]):
        for p in versiones(p0):
            if p["tipo"] != "tocar":
                continue
            correctos = set(p.get("correctos") or [])
            dicho = " ".join(g["voces"][p[c]] for c in ("consigna", "fin") if p.get(c))
            dicho += " " + " ".join(g["voces"][k] for k in (p.get("pistas") or []))
            for cosa in (p.get("solo") or g["escenas"][p["escena"]]["animales"]):
                if cosa in correctos:
                    continue
                assert not re.search(r"\b%s\b" % re.escape(sin_tildes(cosa)), sin_tildes(dicho)), (
                    "%s paso %d: la voz nombra %r, que está en la escena y no es respuesta"
                    % (pieza, i, cosa))


@pytest.mark.parametrize("pieza", PIEZAS)
def test_ningun_cierre_repite_el_festejo_que_acaba_de_sonar(pieza):
    """La otra mitad de *"después como que se juntó"*: los festejos son «¡Muy bien!», «¡Eso es!» y
    «¡Genial!», se sortea uno, y cada cierre de pausa EMPEZABA con esas mismas palabras. Una de cada
    tres veces se oía «¡Eso es!» y, medio segundo después, «¡Eso es! Libro y lámpara empiezan
    igual». El festejo festeja; el cierre cuenta lo que se aprendió."""
    g = guion(pieza)

    def primera(texto):
        pal = re.findall(r"[a-zñ]+", sin_tildes(texto))
        return pal[0] if pal else ""

    arranques = {primera(g["voces"][k]) for k in g["voces"] if k.startswith("festejo")}
    assert arranques, "%s: no hay festejos" % pieza
    pasos = g["pasos"]
    for i, p in enumerate(pasos):
        despues_de_festejo = []
        for v in versiones(p):
            if v.get("fin"):
                despues_de_festejo.append(v["fin"])
        # y lo que se dice en el paso siguiente, si el anterior terminó festejando
        if p["tipo"] == "decir" and i and pasos[i - 1]["tipo"] in ("tocar", "elegir", "clasificar"):
            despues_de_festejo.append(p["voz"])
        for clave in despues_de_festejo:
            assert primera(g["voces"][clave]) not in arranques, (
                "%s/%s empieza igual que un festejo: se oye dos veces seguido" % (pieza, clave))


@pytest.mark.parametrize("pieza", PIEZAS)
def test_ninguna_voz_dura_mas_que_el_tope_del_reproductor(pieza):
    """El reproductor se pone un tope por si un audio no carga, para no quedarse esperando un
    «ended» que no llega. Calculado por el largo del texto, ese tope CORTABA voces de verdad: siete
    de las dos piezas duraban más que el suyo (15-sep-2026). Cortar no se nota como silencio —se
    nota como que la consigna siguiente arranca encima de la que todavía habla—.

    El tope se lee del reproductor, no se copia acá: si alguien afloja la cuenta, esto lo mide."""
    import subprocess
    if not shutil.which("ffprobe"):
        pytest.skip("sin ffprobe para medir los audios")
    js = open(os.path.join(BASE, "video_interactivo_player.js"), encoding="utf-8").read()
    m = re.search(r"setTimeout\(fin, Math\.max\((\d+), texto\.length \* (\d+)\)\)", js)
    assert m, "no se encontró el tope en el reproductor"
    piso, por_letra = int(m.group(1)), int(m.group(2))
    g = guion(pieza)
    largas = []
    for clave, texto in g["voces"].items():
        ruta = viw.ruta_de(pieza, "voz_%s.mp3" % clave)
        dur = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta],
            capture_output=True, text=True).stdout.strip() or 0)
        tope = max(piso, len(texto) * por_letra) / 1000.0
        if dur > tope:
            largas.append("%s dura %.1fs y el tope es %.1fs" % (clave, dur, tope))
    assert not largas, "%s: el reproductor las corta: %s" % (pieza, largas)


# ── el contenido de cada pieza, que es lo que ningún chequeo genérico ve ──────────────────

def test_todo_lo_que_nada_clasifica_bien_a_cada_animal():
    """El delfín es mamífero y el pingüino es ave: si alguien los cambia de grupo, el video enseña
    algo falso y nadie se entera hasta que lo vea una maestra."""
    esperado = {"pez": "pez", "delfin": "mamifero", "pinguino": "ave"}
    for p in guion("todo_lo_que_nada")["pasos"]:
        for it in p.get("items", []):
            assert esperado[it["animal"]] == it["grupo"], "%s quedó en %s" % (it["animal"], it["grupo"])


def test_con_que_sonido_solo_escribe_sonidos_que_la_voz_PUEDE_decir():
    """Dos trampas del castellano, las dos encontradas escuchando (15-sep-2026):

    1. Las OCLUSIVAS (p, t, k) no se pronuncian solas, sin vocal: la toma decía «pe», el nombre de la
       letra, que es lo contrario de lo que enseña esta pieza.
    2. Los DÍGRAFOS: «ll» es una letra distinta («elle»), así que la ele repetida sale como «ele ele
       ele» — lo marcó Pablo escuchándolo. Igual «rr» y «ch».

    Quedan los que se sostienen y no forman dígrafo: mmm, sss, nnn, fff, jjj. Para los demás, la
    consigna se dice sin nombrar el sonido: «tocá lo que empieza igual que libro»."""
    g = guion("con_que_sonido")
    se_pueden_escribir = set("msnfj")
    for i, p0 in enumerate(g["pasos"]):
        for p in versiones(p0):
            if p["tipo"] != "tocar":
                continue
            for letra in re.findall(r"\b([a-záéíóúñ])\1{2,}\b", sin_tildes(g["voces"][p["consigna"]])):
                assert letra in se_pueden_escribir, (
                    "paso %d: escribe el sonido %r alargado, y la voz lo lee como nombre de letra" % (i, letra))


def test_con_que_sonido_las_cosas_empiezan_con_el_sonido_que_pide_la_voz():
    """El corazón de la pieza: si en la pausa del sonido mmm se cuela la pelota, el chico aprende mal."""
    g = guion("con_que_sonido")
    for i, p0 in enumerate(g["pasos"]):
      for p in versiones(p0):
        if p["tipo"] != "tocar":
            continue
        pedido = re.findall(r"\b([a-záéíóúñ])\1{2,}\b", sin_tildes(g["voces"][p["consigna"]]))
        if not pedido:
            continue      # pausas que no nombran el sonido: «igual que libro», las rimas, la letra
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
def test_cada_pieza_tiene_su_propio_telon_final(pieza):
    """Estaba escrito adentro del reproductor —«No todo lo que nada es pez»—, así que la pieza de
    los sonidos terminaba con la moraleja de la otra. Lo que es de la pieza vive en su guion."""
    c = guion(pieza).get("cierre_pantalla") or {}
    assert c.get("titulo") and c.get("texto"), "%s: sin cierre_pantalla" % pieza
    js = open(os.path.join(BASE, "video_interactivo_player.js"), encoding="utf-8").read()
    assert c["texto"] not in js, "%s: el cierre está escrito en el reproductor" % pieza


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
