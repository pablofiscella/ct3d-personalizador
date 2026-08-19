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


def test_la_opcion_tocada_se_marca_SIN_CASTIGARLA():
    """La marca dice «ésta ya la probaste», no «está mal».

    La política del producto está escrita, y es anterior a esta auditoría:
    `docs/auditoria-dc-caba/grado-4.md:278` — *«las vidas convierten el error en castigo y
    contradicen la política del producto: EL ERROR ES EL MATERIAL DE ENSEÑANZA, cada
    distractor existe para explicar»*. Y `README.md:123`: *«hay 82 llamadas a la función de
    error, ninguna explica qué estuvo mal: sólo sacude»*.

    Mi primera versión puso una **✗ roja**, que es exactamente el lenguaje que esa política
    descarta. Lo cazó Pablo. Marcar la acción es necesario —sin eso el chico no ata lo que
    hizo con lo que pasó—; teñirla de rojo con una cruz es otra cosa.

    Lo que sí se refuerza en verde es el ACIERTO, que es el lado que la política quiere
    subrayado.
    """
    h = _html()
    assert "--tocada:" in h, "no está el color neutro de «ésta ya la probaste»"
    assert re.search(r"\.op-texto\.casi[^{]*\{[^}]*box-shadow[^}]*var\(--tocada\)", h, re.S), (
        "la opción tocada no tiene borde propio: quedaría avisada sólo por color")
    assert re.search(r'\.op-texto\.casi::after[^{]*\{[^}]*content:\s*"↻"', h), (
        "falta el ↻ («volvé a intentar»): sin signo, el aviso depende de distinguir el color")
    assert not re.search(r'\.casi::after[^{]*\{[^}]*content:\s*"[✗✘×]"', h), (
        "la opción tocada volvió a marcarse con una cruz: eso es lenguaje de castigo y "
        "contradice docs/auditoria-dc-caba/grado-4.md:278")
    assert re.search(r'\.op-texto\.bien::after[^{]*\{[^}]*content:\s*"✓"', h), (
        "falta el ✓ del acierto: es el lado que la política quiere reforzado")


def test_el_porque_aparece_DONDE_esta_mirando():
    """`CAPA-0-MOTOR-DOMINIO.md:19` fija la regla: **todo error dispara el porqué**. El
    porqué existe, pero el globo estaba clavado con `bottom:88px` fijo — en un teléfono eso
    cae a unos 640 px de la opción que acaba de tocar, fuera de su campo visual. Explicar
    bien en el lugar equivocado es no explicar."""
    s = _player()
    i = s.find("function mostrarExplicacion")
    bloque = s[i:i + 1800]
    assert "_ultimaOpcion" in bloque, (
        "la explicación volvió a posicionarse sola, sin mirar dónde tocó el chico")
    assert "getBoundingClientRect" in bloque


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
    # y repetir devuelve la pregunta Y las opciones, en ese orden.
    #
    # Se lee el CUERPO de la función, no los primeros 400 bytes: el 16-ago el arreglo del
    # parlante agregó un comentario y `leerOpciones()` quedó fuera del recorte — rojo con el
    # código intacto. Un test que se rompe cuando se comenta el código no mide el código.
    i = s.find("function repetirLoUltimo")
    assert i > 0, "cambió el nombre de repetirLoUltimo: revisar este test"
    cuerpo = s[i:s.find("\n}", i) + 2]
    assert "leerOpciones()" in cuerpo, (
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
    assert re.search(r"Promise\.resolve\(reproducirConsigna\(txt\)\)\.then\(", s), (
        "las opciones tienen que leerse DESPUÉS de la consigna, no encima")
    assert re.search(r'if \(typeof leerOpciones === "function"\) leerOpciones\(\);', s), (
        "el método consigna() se extrae y se ejecuta suelto en otro test: no puede dar por "
        "sentado que exista leerOpciones")
    assert "_menuQueHabla()" in s[s.find("function leerOpciones"):s.find("function leerOpciones") + 300], (
        "leer las opciones tiene que estar acotado al ciclo inicial")


def test_la_voz_no_lee_los_emojis():
    """El sintetizador lee «🌾» como su nombre o lo saltea. El dibujo es para el ojo; la voz
    dice la palabra.

    Mira el CUERPO de la función y no los primeros 700 bytes: con la ventana, tres líneas de
    comentario agregadas el 15-ago-2026 empujaron el `replace` fuera del recorte y el test dio
    rojo con el código intacto. **Un test que se rompe cuando se comenta el código no está
    midiendo el código.**"""
    s = _player()
    i = s.find("function _opcionesEnPantalla")
    assert i > 0, "cambió el nombre de _opcionesEnPantalla: revisar este test"
    cuerpo = s[i:s.find("\n}", i) + 2]
    assert "Extended_Pictographic" in cuerpo, (
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


def test_la_correccion_llega_en_DOS_TIEMPOS():
    """Primero la regla, y el dato recién si vuelve a fallar.

    La política dice «todo error dispara el porqué» (CAPA-0-MOTOR-DOMINIO.md:19) y se
    cumplía — pero el porqué llegaba COMPLETO al primer error y muchas veces trae la
    respuesta adentro: «"queso" se escribe con QU: empieza con la letra Q». Con eso no hay
    segundo intento.

    No hubo que inventar cómo partirlo: **214 explicaciones ya están escritas en dos
    partes**, separadas por «: » — la regla antes, el dato después. Los autores ya habían
    hecho el trabajo; lo que faltaba era usarlo.

    Donde no hay ese corte se muestra entera, como hasta ahora: nunca peor que hoy.
    """
    s = _player()
    assert "function _enDosTiempos" in s, "no existe el partidor de la explicación"
    i = s.find("function _enDosTiempos")
    assert 'indexOf(": ")' in s[i:i + 500], "el corte dejó de buscarse donde lo escribieron"
    assert "fallos >= 2" in s[i:i + 500], "la segunda vez tiene que llegar completa"
    j = s.find("      casi(motivo) {")
    assert "_enDosTiempos(motivo, self._rondaFallos)" in s[j:j + 400], (
        "casi() volvió a mostrar la explicación entera al primer error")
    assert "self._rondaFallos = 0" in s, (
        "los fallos no se reinician por ronda: la regla tiene que darse de nuevo en cada "
        "pregunta")


def test_el_globo_encuentra_a_QUE_anclarse():
    """Un arreglo escrito y sin efecto es peor que ninguno: quedó puesto y el globo siguió
    en el fondo de la pantalla porque `marcarLoQueToco` apagaba la referencia ANTES de que
    el globo se posicionara. Medido en el navegador: y=661 antes, y=266 después."""
    s = _player()
    assert "_ultimaMarcada" in s, (
        "el globo depende de `_ultimaOpcion`, que `marcarLoQueToco` apaga antes de tiempo")
    i = s.find("function mostrarExplicacion")
    assert "_ultimaMarcada" in s[i:i + 1800], (
        "mostrarExplicacion volvió a mirar sólo la referencia que ya está apagada")


def test_el_dibujo_de_las_opciones_NO_regala_la_respuesta():
    """Vestir las respuestas con dibujo es para que un chico que no lee pueda elegir. Mal
    hecho, es un atajo para acertar sin saber nada. Dos formas de arruinarlo, y me comí las
    dos antes de encontrar la regla:

    1. **El mismo emoji en la pregunta y en la correcta.** «🍋 Un limón es…» → «🍋 ácido».
       Se gana emparejando dibujitos.
    2. **Vestir sólo algunas.** Al saltear las chivatas, la correcta quedaba como la ÚNICA
       sin dibujo — un chivato peor, porque es visible de un vistazo.

    La regla es **todas o ninguna**, y ninguna si el emoji ya está en la pregunta.
    """
    s = _player()
    i = s.index("const SENTIDOS_BANCO = [")
    banco = s[i:s.index("];", i)]
    emo = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
    mezclados, chivatos = [], []
    for linea in banco.split("\n"):
        m = re.search(r'q: "([^"]+)".*?ops: \[([^\]]*)\]', linea)
        if not m:
            continue
        preg, ops = m.group(1), re.findall(r'"([^"]+)"', m.group(2))
        con = [bool(emo.search(o)) for o in ops]
        if len(set(con)) > 1:
            mezclados.append(ops)
        de_preg = set(emo.findall(preg))
        if ops and emo.search(ops[0]) and emo.findall(ops[0])[0] in de_preg:
            chivatos.append(ops[0])
    assert not mezclados, (
        "hay ítems donde unas opciones tienen dibujo y otras no: la correcta se elige por "
        "descarte visual. Ejemplos: %s" % mezclados[:2])
    assert not chivatos, (
        "el dibujo de la opción correcta ya está en la pregunta: se acierta emparejando. "
        "Ejemplos: %s" % chivatos[:3])
