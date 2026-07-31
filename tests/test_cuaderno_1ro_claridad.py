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

def test_las_preguntas_de_figuras_traen_la_figura():
    """Las que hablan de una figura concreta tienen que mostrarla."""
    banco = _act("figuras_1")["banco"]
    con_dib = [b for b in banco if b.get("dib")]
    assert len(con_dib) >= 8, "sólo %d de %d preguntas muestran la figura" % (
        len(con_dib), len(banco))
    src = _player()
    for b in con_dib:
        assert '%s:' % b["dib"] in src, "el player no sabe dibujar %r" % b["dib"]


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
    sin_dib = [a["id"] for a in cur.CATALOGO
               if a.get("mecanica") == "trivia" and a["id"] != "figuras_1"
               and any(b.get("dib") for b in a.get("banco") or [])]
    assert not sin_dib, "se coló `dib` en otra actividad sin querer: %s" % sin_dib


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
