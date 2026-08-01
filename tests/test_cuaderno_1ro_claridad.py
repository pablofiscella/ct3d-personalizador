# -*- coding: utf-8 -*-
"""Seis cosas que confundían al chico de 1.º, y por qué cada una importaba.

Pablo, 31-jul-2026, después de recorrer el cuaderno de 1.º entero. Las seis tienen la misma
raíz: **la actividad le pedía algo distinto de lo que le decía**. A un chico de 6 años, que
recién está aprendiendo a leer, un desajuste así no se lee como "un detalle de redacción":
se lee como que no entiende la consigna.

1. «Contá las sílabas» y el audio decía *"¿cuántas palmas tiene la palabra?"*. La palmada es
   la técnica; **sílaba** es la palabra que el DC quiere que aprenda. Diciendo sólo "palmas"
   le escondíamos el nombre de lo que estaba haciendo, y encima no coincidía con el título.

2. «Parejas de letras» decía *"la misma letra en chiquita"* y en otro lado *"minúscula"*:
   dos nombres para lo mismo dentro de la misma actividad.

3. «Armá la palabra» decía *"escuchá la palabra"*. El verbo era el equivocado —lo que hay
   que hacer es armarla— y no nombraba la palabra, así que había que deducirla del emoji.

4. «Suma rápida» dice, en un audio GRABADO, *"tocá dos burbujas"*, y en pantalla había
   cuadraditos.

5. «Detective de figuras» preguntaba *"¿cuántos lados tiene un triángulo?"* sin mostrar
   ningún triángulo. En 1.º eso mide si sabe LEER la palabra "triángulo", no si entiende la
   figura.

6. «Recta gigante» tenía DIEZ zonas y sólo TRES carteles (0, mitad, final). Para ubicar el
   13 entre 0 y 20 había que dividir la recta en décimos de cabeza: razonamiento
   proporcional, que no es de 1.º. Y el bonus por dominio multiplicaba el rango hasta ×5,
   así que al chico que le iba bien le tocaba una recta de 0 a 500.
"""
import json
import os
import re
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import actividades_curriculum as cur  # noqa: E402

PLAYER = os.path.join(_BASE, "actividades_player.js")
CSS = os.path.join(_BASE, "actividades_player.html")


def _act(aid):
    for a in cur.CATALOGO:
        if a["id"] == aid:
            return a
    raise AssertionError("no existe la actividad %s" % aid)


def _player():
    return open(PLAYER, encoding="utf-8").read()


def _cuerpo(src, marca, largo=2200):
    i = src.index(marca)
    return src[i:i + largo]


# ── 1. sílabas ───────────────────────────────────────────────────────────────────

def test_la_consigna_de_silabas_dice_silabas():
    """El título y la voz tienen que hablar del mismo objeto."""
    a = _act("silabas_1")
    assert "sílaba" in a["consigna"].lower(), \
        "la consigna no nombra la sílaba: %r" % a["consigna"]
    assert "sílaba" in a["titulo"].lower()


def test_la_palmada_sigue_estando_porque_es_la_tecnica():
    """No se cambió una palabra por otra: se enseñan las dos. La palmada es CÓMO se cuenta
    y es lo que hace la actividad hacible a los 6 años; sacarla sería arreglar el nombre
    rompiendo el método."""
    assert "palma" in _act("silabas_1")["consigna"].lower()


# ── 2. parejas de letras ─────────────────────────────────────────────────────────

def test_las_letras_se_llaman_siempre_igual():
    """Un nombre por concepto dentro de la actividad, y el del DC primero."""
    a = _act("parejas_letras_1")
    c = a["consigna"].lower()
    assert "minúscula" in c, "la consigna no usa la palabra del DC: %r" % a["consigna"]
    explicaciones = " ".join(b.get("m", "") for b in a["banco"]).lower()
    assert "chiquita" not in explicaciones or "minúscula" in explicaciones, \
        "las explicaciones siguen diciendo «chiquita» sin nombrar «minúscula»"


# ── 3. armá la palabra ───────────────────────────────────────────────────────────

def test_la_consigna_pide_armar_y_nombra_la_palabra():
    """El verbo tiene que ser el de la tarea, y la palabra tiene que estar dicha."""
    c = _cuerpo(_player(), "GAMES.armar_palabra = {")
    assert re.search(r'"Armá la palabra "\s*\+\s*palabra\.p', c), \
        "la consigna dejó de nombrar la palabra a armar"
    assert "Escuchá la palabra y tocá" not in c, "volvió el verbo equivocado"


def test_no_repite_la_palabra_suelta_despues_de_decirla():
    """Ahora la palabra va DENTRO de la consigna: volver a decirla 1,3 s después era
    decirla dos veces seguidas — lo mismo que Pablo marcó el 30-jul con la voz de Valeria.
    El botón «Escuchar de nuevo» sigue, porque ahí lo pide el chico."""
    c = _cuerpo(_player(), "GAMES.armar_palabra = {", 3200)
    assert "setTimeout(() => reproducirConsigna(palabra.p), 1300)" not in c, \
        "sigue repitiendo la palabra sola justo después de la consigna"
    assert "Escuchar de nuevo" in c, "se perdió el botón para volver a oírla"


# ── 4. burbujas ──────────────────────────────────────────────────────────────────

def test_las_burbujas_son_burbujas():
    """La consigna es un audio GRABADO que dice "burbujas": lo que se ve tiene que serlo."""
    c = _cuerpo(_player(), "GAMES.suma_rapida = {")
    assert "burbujas que sumen 10" in c
    assert '"spriteBtn burbuja"' in c, "los números siguen en cuadraditos"
    css = open(CSS, encoding="utf-8").read()
    assert ".spriteBtn.burbuja" in css and "border-radius: 50%" in css, \
        "falta el CSS que las hace redondas"


def test_la_burbuja_sigue_mostrando_el_numero():
    """Lo que YA estaba bien no se puede romper: el número va adentro de la burbuja."""
    c = _cuerpo(_player(), "GAMES.suma_rapida = {")
    assert "${v}" in c, "la burbuja se quedó sin número adentro"


# ── 5. figuras ───────────────────────────────────────────────────────────────────

def test_todas_las_preguntas_de_figuras_traen_dibujo():
    """TODAS, sin excepción — y el "todas" es el arreglo.

    La primera versión dejó 3 de 12 sin dibujo: las que van al revés (parten de un OBJETO
    —rueda, puerta, techo— y piden la figura). El razonamiento era "dibujar la figura
    regalaría la respuesta", y estaba mal por dos motivos. Pablo lo vio de una, 31-jul-2026:
    *"¿por qué la primera no tiene dibujo?"* — como las preguntas salen mezcladas, le tocó
    una de esas tres y la actividad se leyó como rota.

    Y el motivo de fondo: sin dibujo, "¿qué figura tiene la puerta?" mide si sabe LEER
    "puerta", que es justo lo que en 1.º todavía no sabe. Lo que había que dibujar no era la
    figura, era el OBJETO: verlo no le da el nombre de la figura, lo tiene que poner él.

    Un umbral de "la mayoría" es lo que dejó pasar el hueco, así que acá se exigen todas."""
    banco = _act("figuras_1")["banco"]
    sin_dib = [b["q"] for b in banco if not b.get("dib")]
    assert not sin_dib, "%d de %d preguntas siguen sin dibujo: %s" % (
        len(sin_dib), len(banco), sin_dib)
    src = _player()
    for b in banco:
        assert "  %s:" % b["dib"] in src or "\n  %s:" % b["dib"] in src, \
            "el player no sabe dibujar %r" % b["dib"]


def test_las_preguntas_de_objeto_dibujan_el_objeto_y_no_la_figura():
    """La distinción que hace que el ejercicio siga siendo un ejercicio: en estas tres el
    chico ve el objeto y tiene que NOMBRAR la figura. Si dibujáramos la figura, no quedaría
    nada que resolver."""
    esperado = {"La rueda tiene forma de…": "rueda",
                "¿Qué figura tiene la puerta?": "puerta",
                "El techo de una casita dibujada suele ser un…": "casita"}
    banco = {b["q"]: b.get("dib") for b in _act("figuras_1")["banco"]}
    for q, dib in esperado.items():
        assert banco.get(q) == dib, "%r dibuja %r y tendría que dibujar el objeto %r" % (
            q, banco.get(q), dib)


def test_el_cuadrado_girado_se_dibuja_como_rombo():
    """La pregunta más difícil del banco es «un cuadrado apoyado en una punta, ¿sigue siendo
    cuadrado?». Es JUSTO la que no se puede ilustrar con un emoji, y la razón por la que el
    dibujo se hace con SVG."""
    b = [x for x in _act("figuras_1")["banco"] if "apoyado en una punta" in x["q"]]
    assert b and b[0].get("dib") == "rombo"


def test_dibujar_es_opcional_y_no_toca_el_resto_del_catalogo():
    """El motor de trivia lo comparten 212 actividades: un ítem sin `dib` no cambia nada."""
    src = _player()
    c = _cuerpo(src, "function juegoTriviaTexto(")
    assert "item.dib ?" in c, "el dibujo dejó de ser opcional"
    CON_DIBUJO = {"figuras_1", "figuras_3", "cuadrilateros_6",    # geometría
                  "calendario_1", "proporcionalidad_grafico_7"}   # calendario y plano
    otras = [a["id"] for a in cur.CATALOGO
             if a.get("mecanica") == "trivia" and a["id"] not in CON_DIBUJO
             and any(b.get("dib") for b in a.get("banco") or [])]
    assert not otras, "se coló `dib` en otra actividad sin querer: %s" % otras


# ── 6. la recta ──────────────────────────────────────────────────────────────────

def test_la_recta_chica_rotula_todas_las_marcas():
    """Con rango chico deja de ser «estimá la proporción» y pasa a ser «buscá entre qué dos
    números va», que es lo que el DC pide a los 6 años."""
    c = _cuerpo(_player(), "GAMES.recta_numerica = {", 6000)
    assert "max <= 100" in c, "la recta no distingue el rango chico del grande"
    assert "for (let i = 0; i <= 10; i++)" in c, "no rotula las once marcas"


def test_la_recta_no_se_pasa_del_rango_del_grado():
    """El bonus por dominio multiplicaba el rango hasta ×5: en 1.º (techo 100) terminaba
    dando una recta de 0 a 500. Misma familia que el bug de dificultad invertida de «serie»."""
    c = _cuerpo(_player(), "GAMES.recta_numerica = {", 6000)
    assert "Math.min(techo" in c, "el rango puede volver a pasarse del techo del grado"


@pytest.mark.parametrize("edad,techo", [(6, 100), (7, 1000), (8, 10000)])
def test_el_techo_de_cada_grado_es_el_de_su_cfg(edad, techo):
    """El techo no está inventado en el player: sale del `max2` que el DC ya le fijó a cada
    grado en el menú. Si mañana cambia ahí, el player lo sigue solo."""
    import actividades_web as aw
    m = [x for x in aw._menu("grande", str(edad), True) if x["id"] == "recta_numerica"]
    assert m and m[0]["cfg"]["max2"] == techo, \
        "%d.º ya no tiene max2=%d" % (edad - 5, techo)


# ── que el cuaderno de 1.º siga entero ───────────────────────────────────────────

def test_las_seis_siguen_en_el_menu_de_primero():
    """Ninguna se arregló sacándola: el pedido era que se entendieran, no que no estuvieran."""
    import actividades_web as aw
    ids = {x["id"] for x in aw._menu("grande", "6", True)} | {
        x["id"] for x in aw._menu_curricular("6")}
    for a in ("silabas_1", "parejas_letras_1", "armar_palabra", "suma_rapida",
              "figuras_1", "recta_numerica"):
        assert a in ids, "%s desapareció del cuaderno de 1.º" % a


# ── la misma falla, en los otros grados ──────────────────────────────────────────

def test_ninguna_actividad_promete_una_figura_que_no_muestra():
    """Pablo, 31-jul-2026, empezando 3.º: *"Detective de figuras, apenas empieza dice «mirá
    bien la figura» y no hay figura"*.

    Era el mismo bug de 1.º en otra actividad, y al ir a buscarlo estaba en tres: `figuras_3`
    (3.º, consigna "Mirá bien la figura", 0 de 12 con dibujo) y `cuadrilateros_6` (6.º,
    "Mirá los lados, los ángulos y las diagonales", 0 de 15).

    La regla que fija este test: si la CONSIGNA le pide al chico mirar algo, tiene que haber
    algo que mirar. Es más fuerte que "todas las preguntas de figuras traen dibujo", porque
    lo que rompe la confianza es la promesa incumplida."""
    # La regla se acota a la promesa LITERAL de algo dibujado. Un primer intento buscó
    # cualquier "mirá" y marcó doce actividades, casi todas legítimas: "mirá la última cifra"
    # se refiere al número que está EN la pregunta, "mirá cómo está armado el poema" al poema
    # que ya se muestra, y "mirá el cielo del sur" es una figura retórica. Marcar eso como
    # error habría llevado a rellenar de dibujos actividades que no los necesitan.
    import re as _re
    PIDE_MIRAR = _re.compile(
        r"mir[áa]\s+(bien\s+)?(la\s+figura|el\s+dibujo|la\s+imagen|el\s+gr[áa]fico)", _re.I)
    malas = []
    for a in cur.CATALOGO:
        c = a.get("consigna") or ""
        banco = a.get("banco") or []
        if not (PIDE_MIRAR.search(c) and banco):
            continue
        sin = [b for b in banco if isinstance(b, dict) and not b.get("dib")]
        if sin:
            malas.append("%d.º %s (%r): %d de %d sin dibujo" % (
                a["grado"], a["id"], c, len(sin), len(banco)))
    assert not malas, "consignas que piden mirar algo que no está:\n  " + "\n  ".join(malas)


@pytest.mark.parametrize("aid,grado,cuantas", [("figuras_3", 3, 12), ("cuadrilateros_6", 6, 15)])
def test_las_de_geometria_de_3ro_y_6to_dibujan_todas(aid, grado, cuantas):
    a = [x for x in cur.CATALOGO if x["id"] == aid][0]
    assert a["grado"] == grado and len(a["banco"]) == cuantas
    sin = [b["q"] for b in a["banco"] if not b.get("dib")]
    assert not sin, "%s: %d sin dibujo: %s" % (aid, len(sin), sin[:2])
    src = _player()
    for b in a["banco"]:
        assert "\n  %s:" % b["dib"] in src, "el player no sabe dibujar %r" % b["dib"]


def test_la_adivinanza_de_2do_SIGUE_sin_dibujo():
    """La excepción, y es a propósito. «Adiviná mi figura» es una ADIVINANZA: "tengo 3 lados
    y 3 vértices, ¿qué soy?". Mostrarle la figura no arregla nada — le da la respuesta y
    borra el juego. Su consigna («¿Qué figura es?») tampoco promete nada visible."""
    a = [x for x in cur.CATALOGO if x["id"] == "adivina_figura"][0]
    assert not any(b.get("dib") for b in a["banco"]), \
        "se le pusieron dibujos a la adivinanza: ahora se contesta mirando"
    assert "¿Qué soy?" in " ".join(b["q"] for b in a["banco"])


# ── las tres que prometían algo visual ───────────────────────────────────────────

def test_el_calendario_de_1ro_se_puede_LEER():
    """Pablo, 31-jul-2026, sobre las tres que quedaban: *"hacelas ahora"*.

    «El calendario» decía "Mirá el calendario" y no había ninguno, así que la actividad
    medía si el chico se ACORDABA de memoria en vez de si sabe leer un calendario — que es
    lo que pide el DC de 1.º.

    OJO: el primer intento fue un ÍCONO de calendario. Cumplía la letra —ya había un
    calendario— pero no el fondo: estaba vacío, y "¿qué día viene después del lunes?" seguía
    sin poder contestarse mirando. Por eso este test no se conforma con que haya un dibujo,
    exige que tenga los días y los números."""
    a = [x for x in cur.CATALOGO if x["id"] == "calendario_1"][0]
    sin = [b["q"] for b in a["banco"] if not b.get("dib")]
    assert not sin, "%d preguntas del calendario sin dibujo: %s" % (len(sin), sin[:2])
    src = _player()
    i = src.index("function _calendarioDibujado")
    cuerpo = src[i:i + 1800]
    assert "_DIAS_CAL" in cuerpo, "el calendario no muestra los días de la semana"
    assert "n <= 28" in cuerpo, "el calendario no muestra los números"
    assert '_DIAS_CAL = ["L", "M", "M", "J", "V", "S", "D"]' in src


def test_el_mes_del_calendario_es_generico_a_proposito():
    """No es el mes real: el cuaderno se juega cualquier día y un calendario que no coincide
    con hoy confunde más de lo que ayuda. Lo que se practica es la ESTRUCTURA."""
    src = _player()
    i = src.index("function _calendarioDibujado")
    assert "Date" not in src[i:i + 1800], "el calendario empezó a depender de la fecha real"


def test_donde_esta_muestra_la_escena():
    """«¿Dónde está?» decía "Mirá dónde está cada cosa" sin nada que mirar, así que "el
    pájaro vuela ___ del árbol" medía si sabe LEER «pájaro» y «árbol» —que a los 6 años es
    justo lo que no sabe— en vez de si entiende «arriba»."""
    a = [x for x in cur.CATALOGO if x["id"] == "donde_esta_1"][0]
    sin = [b["q"] for b in a["banco"] if not b.get("escena")]
    assert not sin, "%d preguntas de posición sin escena: %s" % (len(sin), sin[:2])
    src = _player()
    for b in a["banco"]:
        rel = b["escena"]["rel"]
        assert "  %s: (a, b)" % rel in src, "el player no sabe dibujar la posición %r" % rel


def test_la_escena_de_posicion_usa_emoji_y_no_dibujos_a_mano():
    """Decisión: un pájaro o un gato dibujados a mano salen mal y se vuelven otro acertijo.
    El emoji lo reconoce cualquier chico, y acá lo que se enseña es la POSICIÓN."""
    a = [x for x in cur.CATALOGO if x["id"] == "donde_esta_1"][0]
    for b in a["banco"]:
        for k in ("a", "b"):
            assert len(b["escena"][k]) <= 4 and not b["escena"][k].isascii(), \
                "la escena dejó de usar emoji: %r" % b["escena"]


def test_proporcionalidad_de_7mo_ya_no_promete_un_grafico_que_no_esta():
    """Acá el arreglo NO fue dibujar en todas, y es la diferencia con las otras dos.

    La mayoría de las preguntas son de tabla o de cuenta ("si 1 kg cuesta $500…"), donde un
    gráfico no aporta; y en las que SÍ son sobre el plano, dibujar la recta REGALA la
    respuesta —la pregunta es justamente cómo se ve. Así que: la consigna deja de prometer,
    y las cuatro que hablan del plano muestran los EJES con el origen marcado, que hace
    concreto qué es "el origen" sin contestar nada."""
    a = [x for x in cur.CATALOGO if x["id"] == "proporcionalidad_grafico_7"][0]
    assert "Mirá" not in a["consigna"], \
        "la consigna volvió a prometer algo que no está: %r" % a["consigna"]
    con = [b for b in a["banco"] if b.get("dib")]
    assert len(con) == 4, "cambió cuáles preguntas muestran el plano (%d)" % len(con)
    assert all(b["dib"] == "plano_ejes" for b in con)
    src = _player()
    i = src.index("plano_ejes:")
    cuerpo = src[i:i + 500]
    assert "polygon" in cuerpo and "circle" in cuerpo, "el plano perdió las flechas o el origen"
    assert "line x1=" in cuerpo


def test_el_plano_no_dibuja_ninguna_recta():
    """Si mañana alguien le agrega la recta, le está dando la respuesta a cuatro preguntas.

    La ventana se corta en la coma que cierra la entrada: con un tamaño fijo se metía en la
    figura siguiente y contaba SUS líneas."""
    src = _player()
    i = src.index("plano_ejes:")
    cuerpo = src[i:src.index("\n  ", src.index("',", i))]
    # sólo los dos ejes y las dos flechas; una recta más sería una tercera línea inclinada
    assert cuerpo.count("<line") == 2, \
        "el plano tiene %d líneas y tendría que tener los dos ejes" % cuerpo.count("<line")
