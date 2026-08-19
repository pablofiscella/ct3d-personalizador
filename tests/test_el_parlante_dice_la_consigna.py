"""El 🔊 dice la consigna, no la muletilla.

Pablo, 16-ago-2026, jugando 1.º: *«puse el parlante y no leyó la consigna»*.

MEDIDO ANTES DE ARREGLAR. En la ronda 3 de «Contá las sílabas» —donde la pantalla ya dice
«Va otra»— tocar el 🔊 pedía `/tts?t=¿Y ahora?`. El botón repetía `_ultimoDicho`, y desde la
ronda 2 lo último que se dijo es una muletilla.

A un chico de 1.º, que no puede leer la consigna y toca el parlante justo para saber qué hay
que hacer, el cuaderno le contestaba «¿Y ahora?».

LOS DOS CASOS SON OPUESTOS Y ESTABAN COLGADOS DE LA MISMA VARIABLE
El arreglo del 29-jul —que Valeria no repita catorce veces la misma frase— es correcto y no
se toca: vale para lo que el cuaderno DICE SOLO. El 🔊 es el caso contrario, el chico
PIDIÉNDOLA, y ahí siempre va la instrucción entera.

Verificado en el navegador: en la ronda donde la pantalla dice «VA OTRA», el 🔊 pide
«¿Cuántas sílabas tiene? Contalas con palmas.».
"""
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER = os.path.join(RAIZ, "actividades_player.js")


def _player():
    return open(PLAYER, encoding="utf-8").read()


def _sin_comentarios(js):
    """El código sin los `/* … */` ni los `// …`.

    Hace falta más de lo que parece: estas funciones van muy comentadas —cada una explica de
    qué defecto viene— y un test que busque un nombre en el texto crudo lo encuentra en la
    explicación. Pasó dos veces el 16-ago: una mutación que rompía la regla de verdad dio
    VERDE porque el nombre seguía escrito dos líneas más arriba, en prosa."""
    js = re.sub(r"/\*.*?\*/", " ", js, flags=re.S)
    return re.sub(r"//[^\n]*", " ", js)


def test_el_parlante_dice_la_consigna_REAL():
    """EL test. Si el botón vuelve a colgarse de `_ultimoDicho` a secas, vuelve a contestar
    «¿Y ahora?» a quien pidió que le lean la consigna."""
    s = _player()
    i = s.find("function repetirLoUltimo")
    assert i > 0, "cambió el nombre de repetirLoUltimo: revisar este test"
    cuerpo = _sin_comentarios(s[i:s.find("\n}", i) + 2])
    assert "_consignaReal" in cuerpo, (
        "el 🔊 volvió a repetir lo último dicho. Desde la ronda 2 eso es una muletilla "
        "—«¿Y esto?», «Va otra»— y no la consigna.")
    assert cuerpo.index("_consignaReal") < cuerpo.index("_ultimoDicho"), (
        "`_ultimoDicho` no puede ganarle a la consigna real: es el respaldo, no la primera "
        "opción")


def test_las_muletillas_salen_de_las_listas_que_ya_existen():
    """`MULETILLAS` se arma de las cuatro listas de `CONSIGNA_CORTA_*`. Escribirlas otra vez
    a mano sería una lista que mañana dice algo distinto de la original — y entonces una
    muletilla nueva se guardaría como si fuera la consigna."""
    s = _player()
    m = re.search(r"const MULETILLAS = new Set\(\[\]\.concat\(([^)]+)\)", s)
    assert m, "MULETILLAS dejó de armarse de las listas de consignas cortas"
    for lista in ("CONSIGNA_CORTA_MASC", "CONSIGNA_CORTA_FEM", "CONSIGNA_CORTA_NEUTRO",
                  "CONSIGNA_CORTA_PREGUNTA"):
        assert lista in m.group(1), "falta %s en MULETILLAS" % lista


def test_la_consigna_real_se_guarda_donde_se_MUESTRA():
    """Se guarda en `ctx.consigna`, que es donde se pone el texto en pantalla — no en
    `reproducirConsigna`, que es donde se dice.

    La diferencia importa: desde el 29-jul una consigna repetida se MUESTRA y no se dice. Si
    se guardara al decirla, la ronda que no habla dejaría la consigna sin recordar."""
    s = _player()
    i = s.find("      consigna(txt, pistaSrc) {")
    assert i > 0, "cambió ctx.consigna: revisar este test"
    assert "recordarConsignaReal" in s[i:i + 800], (
        "la consigna real dejó de guardarse donde se muestra")


def test_al_abrir_otra_actividad_se_olvida_la_anterior():
    """Sin esto, el 🔊 de la actividad nueva leería la consigna de la que el chico acaba de
    dejar — que es peor que no leer nada, porque suena a que anda."""
    s = _player()
    i = s.find("    this.actual = id; this.fallos = 0;")
    assert i > 0, "cambió Shell.abrir: revisar este test"
    assert "olvidarConsignaReal" in s[max(0, i - 400):i + 400], (
        "al abrir una actividad no se olvida la consigna de la anterior")


def test_una_muletilla_NO_se_guarda_como_consigna():
    """El corazón del arreglo, sobre la función real. Si `recordarConsignaReal` dejara de
    filtrar, el 🔊 volvería a decir «¿Y esto?» y el test de arriba seguiría en verde."""
    s = _player()
    i = s.find("function recordarConsignaReal")
    assert i > 0, "desapareció recordarConsignaReal"
    cuerpo = _sin_comentarios(s[i:s.find("\n}", i) + 2])
    assert "MULETILLAS" in cuerpo and "return" in cuerpo, (
        "recordarConsignaReal dejó de descartar las muletillas")
    assert "replace(/<[^>]+>/g" in cuerpo, (
        "no se limpian las marcas de HTML: la consigna se compara contra las muletillas, y "
        "un `<b>` haría que no coincidan")
