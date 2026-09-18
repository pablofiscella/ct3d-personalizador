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
        for clave in ("voz", "consigna", "fin", "va_aca", "sin_elegir"):
            if p.get(clave):
                assert p[clave] in voces, "%s paso %d: voz inexistente %r" % (pieza, i, p[clave])
        for a in (p.get("correctos", []) + (p.get("solo") or []) + list(p.get("acomodar") or {})
                  + (p.get("orden") or [])):
            assert a in cosas, "%s paso %d: no está en la escena: %r" % (pieza, i, a)
        for it in p.get("items", []):
            assert it["animal"] in cosas and it["pista"] in voces
            assert it["grupo"] in [x["id"] for x in p["grupos"]]
        for x in p.get("grupos", []):
            assert x["icono"] in g["imagenes"], "%s paso %d: ícono inexistente" % (pieza, i)
        if p["tipo"] == "elegir":
            ids = [o["id"] for o in p["opciones"]]
            assert p["correcta"] in ids, "%s paso %d: la correcta no es una opción" % (pieza, i)
            assert len(set(ids)) == len(ids), "%s paso %d: opciones repetidas" % (pieza, i)
            if p.get("foco"):
                assert p["foco"] in cosas, "%s paso %d: foco inexistente" % (pieza, i)
            for o in p["opciones"]:
                if o.get("icono"):
                    assert o["icono"] in g["imagenes"], "%s paso %d: dibujo de opción inexistente" % (pieza, i)
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
        if p["tipo"] in ("tocar", "elegir", "ordenar"):
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
            escena = g["escenas"][p["escena"]]["animales"]
            for cosa in (p.get("solo") or escena):
                if cosa in correctos or escena[cosa].get("decorado"):
                    continue          # lo `decorado` es parte del relato: no se puede tocar
                assert not re.search(r"\b%s\b" % re.escape(sin_tildes(cosa)), sin_tildes(dicho)), (
                    "%s paso %d: la voz nombra %r, que está en la escena y no es respuesta"
                    % (pieza, i, cosa))


@pytest.mark.parametrize("pieza", PIEZAS)
def test_la_consigna_termina_en_lo_que_hay_que_hacer(pieza):
    """Pablo, 16-sep-2026: *"cuando pregunto con quién cruzamos la calle y fui a marcar, demoró un
    poco en dejarme marcar a la madre"*.

    Los objetos se habilitan cuando la voz TERMINA la consigna. «Última. Para cruzar, ¿a quién le
    damos la mano? Tocá a esa persona.» se entendía a los 3,6 s y seguía hablando hasta los 8,1: el
    chico que contestaba en cuanto oía la pregunta tocaba y no pasaba nada durante casi cinco
    segundos. Medido palabra por palabra, en todas las demás pausas de las tres piezas esa espera
    es de 0,5 a 0,8 s, porque la consigna termina justo en lo que hay que hacer.

    Así que: si la consigna pregunta, termina en la pregunta."""
    g = guion(pieza)
    for i, p0 in enumerate(g["pasos"]):
        for p in versiones(p0):
            if p["tipo"] not in ("tocar", "elegir", "ordenar") or not p.get("consigna"):
                continue
            texto = g["voces"][p["consigna"]].strip()
            if "?" in texto:
                assert texto.endswith("?"), (
                    "%s paso %d: después de la pregunta la voz sigue hablando y el chico no puede "
                    "contestar: %r" % (pieza, i, texto[texto.rindex("?") + 1:].strip()))


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
        if p["tipo"] == "decir" and i and pasos[i - 1]["tipo"] in ("tocar", "elegir", "clasificar", "ordenar"):
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


@pytest.mark.parametrize("pieza", PIEZAS)
def test_lo_que_se_toca_aparece_con_la_pregunta(pieza):
    """Pablo lo marcó DOS veces, en dos piezas distintas: *"tardó en permitirme seleccionar la vaca"*
    (16-sep-2026) y *"hay que hacer click en la pantalla para… poder seleccionar los objetos"*
    (18-sep-2026).

    Los objetos se habilitan cuando la voz termina la consigna. Si ya estaban en pantalla desde antes
    —porque la escena no cambió—, el chico mira una escena viva que no le responde, y el navegador
    encima no le cambia el puntero a la manito hasta que mueve el mouse o hace clic. Medido antes de
    arreglarlo: 17 s en «¿Con qué sonido empieza?», 18 en el piloto, 22 en «¿Cruzo o espero?».

    Lo que se mide acá es el tiempo MUERTO: lo que la escena está a la vista ANTES de que arranque la
    consigna. Lo que dura la pregunta no se cuenta: el chico no puede contestar antes de oírla."""
    import subprocess
    if not shutil.which("ffprobe"):
        pytest.skip("sin ffprobe para medir las voces")
    g = guion(pieza)

    def dura(clave):
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                            "csv=p=0", viw.ruta_de(pieza, "voz_%s.mp3" % clave)],
                           capture_output=True, text=True)
        return float(r.stdout.strip() or 0)

    escena, muerto = None, 0.0
    for i, p in enumerate(g["pasos"]):
        if p["escena"] != escena:
            escena, muerto = p["escena"], 0.0        # escena nueva: lo que se toca recién aparece
        if p["tipo"] == "decir":
            muerto += dura(p["voz"]) + 1.1           # el respiro después de la voz y entre pasos
            continue
        if p["tipo"] in ("tocar", "ordenar", "clasificar"):
            assert muerto <= 3.0, (
                "%s paso %d: lo que hay que tocar está a la vista %.1f s antes de que empiece la "
                "consigna. Que la escena con los objetos entre CON la pregunta." % (pieza, i, muerto))
        muerto = 0.0


@pytest.mark.parametrize("pieza", PIEZAS)
def test_la_pausa_de_agrupar_dice_el_gesto(pieza):
    """Pablo, 18-sep-2026, sobre «Detectives del cielo»: *"le falta que diga que elijas un objeto y
    después la tarjeta"*.

    Agrupar se hace en DOS toques —primero la cosa, después el grupo— y eso no se adivina mirando.
    El piloto lo decía en su consigna y en la pieza nueva se pasó por alto. Además, si el chico toca
    el grupo sin haber elegido nada, tiene que oír qué hacer: antes sólo parpadeaban las cosas y el
    que no entendió el orden se quedaba tocando el grupo sin respuesta."""
    g = guion(pieza)
    for i, p in enumerate(g["pasos"]):
        if p["tipo"] != "clasificar":
            continue
        assert "despu" in sin_tildes(g["voces"][p["consigna"]]), (
            "%s paso %d: la consigna no dice que primero se toca la cosa y después el grupo" % (pieza, i))
        assert p.get("sin_elegir"), (
            "%s paso %d: sin `sin_elegir`, tocar el grupo sin elegir nada no dice nada" % (pieza, i))


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
def test_el_tilde_tiene_donde_pararse_en_cada_dibujo(pieza):
    """Pablo, 15-sep-2026: *"el check queda en el aire porque esa parte no tiene imagen"*.

    El tilde del acierto se cuelga del borde del dibujo. Estaba clavado en la esquina de la CAJA, y
    los dibujos tienen aire transparente alrededor: en la silla esa esquina no tenía nada y el tilde
    flotaba en el vacío; el pingüino igual (los dos se espejaron), y la moto, que ocupa sólo la
    mitad de abajo de su caja, tampoco.

    Ahora el reproductor busca el punto del dibujo donde el tilde tape más o menos la mitad. Este
    test se asegura de que ese punto EXISTA en cada dibujo: uno demasiado fino o demasiado chico no
    tendría dónde apoyarlo y volvería a quedar en el aire."""
    from PIL import Image
    import numpy as np

    g = guion(pieza)
    for nombre in sorted({c["img"] for e in g["escenas"].values() for c in e["animales"].values()}):
        im = Image.open(viw.ruta_de(pieza, nombre + ".webp")).convert("RGBA")
        esc = 64.0 / max(im.size)
        im = im.resize((max(1, round(im.width * esc)), max(1, round(im.height * esc))))
        a = (np.array(im)[:, :, 3] > 40).astype(float)
        ch, cw = a.shape
        lado = max(2, round(0.34 * cw))
        s = np.pad(a, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
        mejor = 0.0
        ys, xs = np.where(a > 0)
        for y, x in zip(ys, xs):
            xa, xb = max(0, x - lado // 2), min(cw, x + lado // 2)
            ya, yb = max(0, y - lado // 2), min(ch, y + lado // 2)
            tapa = (s[yb, xb] - s[ya, xb] - s[yb, xa] + s[ya, xa]) / (lado * lado)
            mejor = max(mejor, 1 - abs(tapa - 0.55) * 2)
        assert mejor > 0.5, ("%s/%s: no hay dónde apoyar el tilde sin que quede en el aire "
                             "(lo mejor da %.2f)" % (pieza, nombre, mejor))


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
def test_todo_lo_que_se_baja_lleva_la_version_de_la_pieza(pieza):
    """Pablo, 15-sep-2026: *"se quedó ahí y no dijo nada más después de la rima"*.

    Su navegador tenía el reproductor de la primera vez —se sirve con caché de horas y el nombre no
    cambia nunca— corriendo contra el guion nuevo, donde la última pausa pasó a sortearse. El
    reproductor viejo no sabía leerla y el video se trabó a la mitad, con la pantalla puesta.

    La regla es la misma que en los videos del canal: **contenido distinto, dirección distinta**. Si
    una sola imagen, voz o línea del reproductor queda sin versión, vuelve a pasar, y del modo más
    difícil de ver: a quien lo abre por primera vez le anda bien."""
    page = viw.html(pieza)
    v = viw.version(pieza)
    assert len(v) == 10 and 'src="player.js?v=%s"' % v in page
    assert 'window.VI_V = "%s"' % v in page
    js = open(os.path.join(BASE, "video_interactivo_player.js"), encoding="utf-8").read()
    for n, linea in enumerate(js.split("\n"), 1):
        if re.search(r"\.(webp|mp3)", linea) and re.search(r'\.src = |src="', linea):
            assert "A(" in linea, "reproductor:%d arma una dirección sin versión: %s" % (n, linea.strip())
    for n, linea in enumerate(open(os.path.join(BASE, "video_interactivo_player.html"),
                                   encoding="utf-8").read().split("\n"), 1):
        if re.search(r'src="[^"]+\.(webp|mp3|js)"', linea):
            assert "{{VERSION}}" in linea, "la página pide algo sin versión en la línea %d" % n


def test_la_version_cambia_cuando_cambia_lo_que_el_chico_recibe():
    """Sirve si se mueve con el contenido y sólo con él: por fecha de archivo se tiraría la caché
    entera en cada despliegue (`probar` reescribe todo), y por nada nunca llegaría un arreglo."""
    pieza = PIEZAS[0]
    antes = viw.version(pieza)
    assert antes == viw.version(pieza), "la versión cambia sola entre dos llamadas"
    ruta = os.path.join(BASE, "video_interactivo_player.js")
    original = open(ruta, "rb").read()
    try:
        open(ruta, "wb").write(original + b"\n// un cambio\n")
        assert viw.version(pieza) != antes, "cambió el reproductor y la versión no se movió"
    finally:
        open(ruta, "wb").write(original)
    assert viw.version(pieza) == antes


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


# ── en el cuaderno: la sección «Videos interactivos» ─────────────────────────────────────

CUADERNO_JS = os.path.join(BASE, "actividades_player.js")
CUADERNO_HTML = os.path.join(BASE, "actividades_player.html")


def test_el_indice_lista_todas_las_piezas_con_su_grado():
    """El cuaderno pide la lista EN VIVO (`/vi/indice.json`): un video nuevo tiene que aparecer en
    los cuadernos ya entregados, cuyo `data.json` quedó congelado el día de la compra."""
    idx = viw.indice()
    assert sorted(v["pieza"] for v in idx) == PIEZAS
    for v in idx:
        assert v["grado"] in range(1, 8) and v["titulo"] and len(v["version"]) == 10
        datos, ct = viw.archivo(v["pieza"], "portada.webp")
        assert ct == "image/webp" and datos[:4] == b"RIFF"
        assert len(datos) < 80000, "%s: la miniatura pesa %d bytes" % (v["pieza"], len(datos))


def test_la_seccion_va_despues_de_las_materias_y_antes_de_extras():
    """Pablo, 16-sep-2026: *"después de naturales, sociales, exactas, etc. Pero antes de las
    extras"*. Se pone al llegar a Extras («logica») ANTES del `return` de categoría vacía —si no,
    un grado sin Extras se quedaría sin videos— y, si no se puso, al final."""
    js = open(CUADERNO_JS, encoding="utf-8").read()
    i = js.find("Adapt.ordenCategorias().forEach((cat) => {\n      if (cat === \"logica\" && !_videosPuestos)")
    assert i > 0, "la sección de videos ya no se pone al llegar a Extras"
    j = js.find("if (!delCat.length) return;", i)
    assert js.find("stage.appendChild(_seccionVideos())", i) < j, "queda después del return"
    assert "if (!_videosPuestos) stage.appendChild(_seccionVideos());" in js


def test_las_tarjetas_de_video_no_son_actividades():
    """El modo seño arrastra toda `.carta` y guarda su orden, y el buscador y la voz del menú las
    recorren: una tarjeta de video con esa clase terminaría en el orden de la maestra."""
    js = open(CUADERNO_JS, encoding="utf-8").read()
    ini, fin = js.find("function _seccionVideos()"), js.find("function abrirVideoInteractivo(")
    bloque = js[ini:fin]
    assert ini > 0 and fin > ini
    assert '"vi-carta' in bloque and '"carta' not in bloque and "menu-cat" not in bloque


def test_los_videos_son_de_kydo_y_se_abren_sin_salir_del_cuaderno():
    """Son de la línea escolar: el cuaderno de cumpleaños no los pide. Y se abren en un marco con
    un botón: en el cuaderno del chico el único `<a>` es el del diploma. El aviso de «terminado»
    sólo se acepta si viene del mismo sitio."""
    js = open(CUADERNO_JS, encoding="utf-8").read()
    ini = js.find("let VIDEOS_VI = [];")
    fin = js.find("/* ── arranque ── */", ini)
    bloque = js[ini:fin]
    assert "if (!D || !D.escolar_on) return;" in bloque
    assert "v.grado === grado" in bloque
    for enlace in ("<a href", 'el("a"', 'createElement("a")', "window.open", "location.href"):
        assert enlace not in bloque, "los videos sacan al chico del cuaderno: %s" % enlace
    assert "if (ev.origin !== location.origin) return;" in bloque
    assert "cargarVideosInteractivos()" in js[js.find("async function boot()"):]


def test_en_primero_los_videos_tambien_se_ven_en_mayusculas():
    """Pablo, 15-ago-2026: *«todo el cuaderno de primero tiene que verse en mayúsculas»*. Los
    videos ahora viven adentro del cuaderno. Los `<button>` no heredan `text-transform`: cada uno
    se nombra, o las opciones quedan en minúscula debajo de un subtítulo en mayúscula."""
    html = open(CUADERNO_HTML, encoding="utf-8").read()
    for sel in ("body.g1 .vi-carta .nombre", "body.g1 .vi-volver"):
        assert sel in html, "falta %s en la regla de 1.º" % sel
    vp = open(os.path.join(BASE, "video_interactivo_player.html"), encoding="utf-8").read()
    assert '<body class="g{{GRADO}}">' in vp
    regla = vp[vp.find("body.g1 .cab b"):]
    regla = regla[:regla.find("}")]
    for sel in (".subs", ".empezar", ".op span", ".grupo span", ".telon h1"):
        assert "body.g1 " + sel in regla, "el video de 1.º deja %s en minúscula" % sel
    assert 'class="g1"' in viw.html("cruzo_o_espero")


def test_el_telon_se_mide_con_la_escena_y_no_con_la_ventana():
    """16-sep-2026, abriendo los videos desde el cuaderno en un celular: la escena mide unos
    358×239 y el telón —Carpi, título, subtítulo y botón— no entraba; el «▶ Empezar» quedaba
    cortado por la mitad. Medido con `vw` se achicaba por el ANCHO, que en un celular vertical no
    es lo que falta. Medido en el navegador después del arreglo: el botón entra entero en 358×239 y
    en 328×219. Los recorridos automáticos no lo veían porque tocan el botón «a la fuerza»."""
    vp = open(os.path.join(BASE, "video_interactivo_player.html"), encoding="utf-8").read()
    assert ".pantalla{container-type:size}" in vp
    for sel in (".telon h1{", ".telon img{", ".empezar{"):
        reglas = [r for r in re.findall(re.escape(sel) + r"[^}]*}", vp) if "cqh" in r]
        assert reglas, "%s no se mide con el alto de la escena" % sel


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
