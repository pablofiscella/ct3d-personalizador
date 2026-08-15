# -*- coding: utf-8 -*-
"""Un chico de 1.º puede usar el cuaderno sin leer, y ve qué tocó cuando se equivoca.

14-ago-2026. De la auditoría de 1.º a 7.º medida en un navegador de verdad. Tres defectos
que sólo se ven jugando, y que ningún test podía ver porque son de comportamiento:

1. **EL MENÚ ERA MUDO.** Un chico de 1.º entra a 68 tarjetas y 279 palabras, y para elegir
   tiene que LEER. Adentro de la actividad la seño habla —verificado: dos pedidos de audio
   al entrar— pero el menú era el único tramo mudo del recorrido, y es el primero. El 🔊 del
   encabezado dice «Sonido»: silencia, no lee.

2. **LA CONSIGNA SE DECÍA UNA VEZ Y SE PERDÍA.** No había forma de volver a escucharla: ni
   tocando el texto, ni el 🔊. Un chico de seis años que se distrae cuatro segundos —que es
   lo que hace un chico de seis años— se quedaba sin consigna y sin poder leerla.

3. **LA MARCA DEL ERROR DURABA 450 ms.** 35 juegos hacían
   `setTimeout(() => b.classList.remove("casi"), 450)`. El chico tocaba, la opción se
   sacudía menos de medio segundo, y no quedaba ninguna huella: no podía asociar su acción
   con el resultado, que es de lo que está hecho aprender de un error. Y peor: el bloque
   `prefers-reduced-motion` pone todas las animaciones en 0,01 ms, así que con esa
   preferencia activada el error **no se avisaba en absoluto** — el único canal era una
   animación, y hay una opción del sistema que la borra.

Este archivo mira el CÓDIGO, que es donde el defecto puede volver. Lo que se ve en pantalla
está verificado aparte con Playwright contra el espejo dev.
"""
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER = os.path.join(RAIZ, "actividades_player.js")
HTML = os.path.join(RAIZ, "actividades_player.html")


def _player():
    return open(PLAYER, encoding="utf-8").read()


def _html():
    return open(HTML, encoding="utf-8").read()


def test_la_marca_del_error_NO_se_borra_sola():
    """EL test. Cualquier juego que vuelva a poner el `setTimeout` de 450 ms deja otra vez
    al chico sin saber qué tocó. Eran 35; tiene que seguir habiendo cero."""
    quedan = re.findall(r'setTimeout\(\(\) => \w+\.classList\.remove\("casi"\)[^)]*\)', _player())
    assert not quedan, (
        "%d juegos vuelven a borrar la marca del error a los milisegundos. La marca se "
        "limpia sola al empezar la pregunta siguiente (ctx.ronda), no con un timeout."
        % len(quedan))


def test_la_marca_se_limpia_al_cambiar_de_pregunta():
    """La otra mitad: si no se limpiara, la equivocación de una pregunta quedaría pintada
    sobre la siguiente. Se hace en `ronda()`, que es por donde pasan los 76 juegos."""
    s = _player()
    i = s.find("      ronda(i) {")
    assert i > 0, "cambió la forma de ctx.ronda: revisar este test"
    assert '#juego .casi' in s[i:i + 900], "ronda() ya no limpia las marcas de la anterior"


def test_el_error_se_avisa_por_MAS_QUE_COLOR():
    """Color, borde y un signo. Un chico que no distingue el rojo tiene que ver igual que
    se equivocó — y el que tiene las animaciones apagadas, también."""
    h = _html()
    assert "--mal:" in h, "no está definido el color del error"
    assert re.search(r"\.op-texto\.casi[^{]*\{[^}]*box-shadow[^}]*var\(--mal\)", h, re.S), (
        "la opción equivocada no tiene borde propio: quedaría avisada sólo por color")
    assert re.search(r'\.op-texto\.casi::after[^{]*\{[^}]*content:\s*"✗"', h), (
        "falta el signo ✗: sin él, el aviso depende de distinguir el color")
    assert re.search(r'\.op-texto\.bien::after[^{]*\{[^}]*content:\s*"✓"', h), (
        "falta el ✓ del acierto: la misma regla vale para el lado bueno")


def test_la_consigna_se_puede_volver_a_escuchar():
    """Y el texto que se repite es el ÚLTIMO que dijo la seño, no una constante: así vale
    también para las correcciones y para cualquier juego que se agregue mañana."""
    s = _player()
    assert s.count('id="consignaRepetir"') >= 2, (
        "el botón de repetir tiene que estar en las DOS pantallas que arman la consigna "
        "(la del juego y la del sondeo)")
    assert "function repetirLoUltimo" in s and "_ultimoDicho" in s
    assert re.search(r"function reproducirConsigna\(txt, recordar\) \{\s*"
                     r"if \(txt && recordar !== false\) _ultimoDicho = txt;", s), (
        "reproducirConsigna dejó de recordar lo que dijo: el botón de repetir queda mudo")
    # y repetir devuelve la pregunta Y las opciones, en ese orden
    i = s.find("function repetirLoUltimo")
    assert "leerOpciones()" in s[i:i + 400], (
        "el botón de repetir dejó de decir las opciones: el chico vuelve a escuchar la "
        "pregunta y sigue sin saber qué dice cada respuesta")


def test_el_menu_habla_en_el_ciclo_inicial_y_no_despues():
    """Las dos mitades. En 1.º y 2.º la corneta es la diferencia entre poder elegir y no
    poder. De 4.º para arriba serían 68 cornetas de ruido — y en 6.º y 7.º leerían como
    material para más chicos, que es justo lo que un preadolescente rechaza."""
    s = _player()
    assert "function _menuQueHabla" in s, "no existe la regla de cuándo habla el menú"
    m = re.search(r"function _menuQueHabla\(\) \{ return ([^;]+); \}", s)
    assert m and "<= 3" in m.group(1), (
        "la corneta del menú tiene que estar acotada al ciclo inicial, y quedó: %s"
        % (m.group(1) if m else "?"))
    assert 'class="hablar"' in s, "la tarjeta no dibuja la corneta"
    assert 'closest(".hablar")' in s, (
        "tocar la corneta tiene que decir el nombre SIN abrir el juego")


def test_el_boton_de_repetir_es_grande_para_una_mano_chica():
    """44 px es el piso para un dedo de seis años. Un botón chico al lado de la consigna
    sería un botón que el chico no acierta, o que abre otra cosa por error."""
    h = _html()
    m = re.search(r"#consigna \.repetir \{[^}]*\}", h, re.S)
    assert m, "no está el estilo del botón de repetir"
    anchos = [int(x) for x in re.findall(r"(?:width|height):\s*(\d+)px", m.group(0))]
    assert anchos and min(anchos) >= 44, "el botón de repetir mide menos de 44px: %s" % anchos


def test_las_OPCIONES_tambien_se_escuchan_en_el_ciclo_inicial():
    """14-ago-2026. Pablo, sobre «¿Es del campo o de la ciudad?» —un girasol y dos botones
    que dicen «🌾 Campo» y «🏙️ Ciudad»—: *«¿cómo sabe un chico de primero qué es, sin saber
    leer?»*.

    Le habíamos arreglado la consigna y lo dejábamos adivinando la RESPUESTA: medido, la
    palabra iba a 13 px, el emoji va inline y medía los mismos 13 px, y nadie las decía.

    Este caso es el que explica por qué una auditoría de propiedades no alcanza: el botón
    pasaba TODOS los chequeos —contraste bien, caja de 134×48, sin depender del color— y
    fallaba en la única pregunta que ninguna métrica hacía.
    """
    s = _player()
    assert "function leerOpciones" in s, "las opciones no se leen en voz"
    assert "function _opcionesEnPantalla" in s
    assert re.search(r"reproducirConsigna\(txt\)\.then\(\(\) => leerOpciones\(\)\)", s), (
        "las opciones tienen que leerse DESPUÉS de la consigna, no encima")
    assert "_menuQueHabla()" in s[s.find("function leerOpciones"):s.find("function leerOpciones") + 300], (
        "leer las opciones tiene que estar acotado al ciclo inicial")


def test_la_voz_no_lee_los_emojis():
    """El sintetizador lee «🌾» como su nombre o lo saltea. El dibujo es para el ojo; la voz
    dice la palabra."""
    s = _player()
    i = s.find("function _opcionesEnPantalla")
    assert "Extended_Pictographic" in s[i:i + 700], (
        "el texto que va a la voz no limpia los emojis")


def test_el_ciclo_inicial_agranda_las_opciones():
    """13 px para la palabra Y para el dibujo, que es lo único que ese chico puede
    interpretar. En el ciclo inicial crecen las dos cosas."""
    h = _html()
    m = re.search(r"body\.ciclo1[^{]*\{[^}]*font-size:\s*(\d+)px", h, re.S)
    assert m, "no está la regla de tamaño del ciclo inicial"
    assert int(m.group(1)) >= 20, "las opciones de 1.º siguen chicas: %spx" % m.group(1)
    assert "function _marcarCiclo" in _player(), "nadie marca el <body> como ciclo inicial"


def test_la_marca_del_error_alcanza_a_los_juegos_SIN_la_clase_op():
    """«¿Campo o ciudad?» arma sus botones sin `.op`. Escuchar por clase era escuchar una
    convención que no todos los juegos siguen; el contenedor lo comparten los 76."""
    s = _player()
    assert 'closest("#juego button, .op, .op-texto")' in s, (
        "la marca del error volvió a depender de que el juego use la clase .op")
