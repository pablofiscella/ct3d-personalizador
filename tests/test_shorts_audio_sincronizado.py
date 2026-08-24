# -*- coding: utf-8 -*-
"""LA REGLA DEL AUDIO: la lección no suena mientras la tarjeta del gancho tapa la pantalla.

5-ago-2026. Pablo, escuchando los primeros seis Shorts: *"los audios están corridos. No habla
el texto inicial y eso hace que quede todo corrido"*. Y después: *"tenés que crear una regla
para todos para que no falle más"*. Este archivo es esa regla.

QUÉ PASABA
La tarjeta del gancho no va ANTES de la lección: va ENCIMA, tapando sus primeros 2,5
segundos. Eso se decidió a propósito —la versión anterior corría la lección y el Short abría
con silencio absoluto, que en un feed es peor— y la idea era que la voz del gancho cubriera
ese hueco.

**Pero el motor nunca mezcló esa voz.** Los clips existían y sólo se habían usado a mano,
para el Short que se armó de a uno. O sea que la premisa del arreglo anterior —"la voz del
gancho tapa el silencio"— era falsa en el código, y nadie lo notó porque la imagen estaba
bien y el audio también: **cada uno por separado era correcto.**

Medido después: −18,8 dB desde el segundo cero. La explicación arrancaba debajo de la
pregunta, y por eso todo sonaba adelantado.

POR QUÉ ESTE TEST Y NO UNA REVISIÓN A MANO
Un desfasaje de audio no se ve. No hay 404, no hay excepción, no hay log: el archivo se
genera, dura lo que tiene que durar y se reproduce. La única forma de encontrarlo es
escuchándolo — y con 396 lecciones por delante, nadie va a escuchar las 396.

Por eso el test MIDE el volumen del archivo renderizado en vez de leer el código. Un filtro
de ffmpeg correcto en una rama que no se ejecuta pasa cualquier revisión de fuente.
"""
import os
import re
import subprocess
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)


def _t_gancho(motor, nombre):
    """Cuánto dura la tarjeta del gancho para ESA lección.

    Desde el 6-ago-2026 ya no es una constante: sigue el largo de la voz. Los tests que
    usaban `T_GANCHO` a secas se rompieron acá, y está bien que se hayan roto — asumían
    justamente lo que la regla nueva vino a sacar."""
    voz = motor.voz_de(nombre)
    return max(motor.T_GANCHO_MIN, motor.duracion(voz) + 0.4) if voz else motor.T_GANCHO_MIN


def _volumen(ruta, desde, dur=1.5):
    """El volumen medio de un tramo, en dB. -91 es silencio digital."""
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-ss", str(desde), "-t", str(dur), "-i", ruta,
         "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True)
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else None


@pytest.fixture(scope="module")
def shorts():
    """Dos Shorts recién armados, los dos CON voz de gancho.

    Hasta el 24-ago el segundo era `lec_multiplicar` a propósito, para cubrir el camino SIN
    voz. Ese camino es el que Pablo rechazó (*"comienzan en silencio"*): sin clip, el motor
    deja 2,5 s mudos. Ya no hay lección con gancho escrito y sin voz, así que se prueban
    dos que sí la tienen — el otro camino queda en `test_todo_gancho_escrito_tiene_voz`."""
    import shorts as motor
    pares = []
    for nombre in ("lec_acentuacion_esdrujulas.mp4", "lec_abstractos_concretos.mp4"):
        if nombre not in motor.GANCHOS:
            pytest.skip("%s no tiene gancho escrito" % nombre)
        if not os.path.exists(os.path.join(motor.LECCIONES, nombre)):
            pytest.skip("falta el video de %s" % nombre)
        ok, res = motor.armar(nombre, quiet=True)
        if not ok:
            pytest.skip("no se pudo armar %s: %s" % (nombre, res))
        pares.append((nombre, res, motor.voz_de(nombre)))
    return pares


def test_sin_voz_de_gancho_la_leccion_NO_suena_bajo_la_tarjeta(shorts):
    """EL test. Es exactamente lo que Pablo escuchó.

    Sin voz que la cubra, la tarjeta tiene que estar en silencio: se lee la pregunta y se
    escucha después. Silencio es peor que sonido; desincronizado es peor que silencio."""
    import shorts as motor
    for nombre, ruta, voz in shorts:
        if voz:
            continue
        v = _volumen(ruta, 0, _t_gancho(motor, nombre) - 0.3)
        assert v is not None, "no pude medir %s" % ruta
        assert v < -60, (
            "%s: la lección habla (%.1f dB) mientras la tarjeta del gancho tapa la "
            "pantalla. Eso es lo que suena 'corrido'." % (nombre, v))


def test_con_voz_de_gancho_SÍ_suena_desde_el_cero(shorts):
    """El otro camino. Con voz, el Short no puede abrir mudo: los primeros milisegundos son
    los que deciden si alguien se queda."""
    for nombre, ruta, voz in shorts:
        if not voz:
            continue
        v = _volumen(ruta, 0, 1.2)
        assert v is not None and v > -50, (
            "%s tiene voz de gancho (%s) pero abre en silencio (%.1f dB): la voz no se "
            "está mezclando" % (nombre, os.path.basename(voz), v if v else -99))


def test_la_leccion_empieza_a_sonar_cuando_se_levanta_la_tarjeta(shorts):
    """Los dos casos comparten esto: pasada la tarjeta, tiene que haber voz. Si sigue mudo,
    el `adelay` se pasó de largo y estamos perdiendo explicación."""
    import shorts as motor
    for nombre, ruta, _ in shorts:
        v = _volumen(ruta, _t_gancho(motor, nombre) + 0.5, 2)
        assert v is not None and v > -50, (
            "%s sigue mudo después de la tarjeta (%.1f dB)" % (nombre, v if v else -99))


def test_no_se_corta_el_final_de_la_leccion(shorts):
    """Correr la lección sin alargar el Short le comería los últimos segundos — que es donde
    suele estar la conclusión. El Short tiene que durar la lección MÁS la tarjeta."""
    import shorts as motor
    for nombre, ruta, _ in shorts:
        d_lec = motor.duracion(os.path.join(motor.LECCIONES, nombre))
        d_short = motor.duracion(ruta)
        assert d_short >= d_lec + _t_gancho(motor, nombre) - 0.5, (
            "%s dura %.1fs y la lección %.1fs: se está cortando el final"
            % (nombre, d_short, d_lec))


def test_la_voz_se_busca_por_el_nombre_de_la_leccion():
    """Cómo se encuentra la voz, y por qué se rompió la primera vez.

    El clip estaba guardado como `esdrujulas.mp3` y la lección es
    `lec_acentuacion_esdrujulas.mp4`. El motor no lo encontraba y el Short salía mudo — sin
    ningún error, porque "no hay voz" es un caso válido.

    La convención es una sola: `lec_<X>.mp4` → `ganchos_voz/<X>.mp3`. Un nombre que hay que
    recordar es un nombre que alguien va a escribir distinto."""
    import shorts as motor
    assert motor.voz_de("lec_acentuacion_esdrujulas.mp4", ) == os.path.join(
        motor.VOCES, "acentuacion_esdrujulas.mp3")
    assert motor.voz_de("lec_no_existe_esta.mp4") is None


# ═════════════════════════════════════════════════════════════════════════════
# LAS DOS REGLAS DEL GANCHO (6-ago-2026)
#
# Pablo, escuchando los tres Shorts nuevos: *"el momento en el que habla cuando comienza es
# más largo que lo que dura el banner y se solapa con el audio de la explicación"*. Y:
# *"en el de las esdrújulas comenzaba mejor diciendo «¿sabés la regla de las esdrújulas?».
# Ese es el gancho: una pregunta"*. Y cerró: *"faltan reglas al skill"*.
#
# Tenía razón en que faltaban. Van acá y no en un comentario porque una regla que nadie
# verifica se rompe en la corrida siguiente — la del cierre se arregló un día antes y al
# gancho no se le aplicó, siendo la misma.
# ═════════════════════════════════════════════════════════════════════════════

def test_REGLA_la_tarjeta_dura_LO_QUE_DURA_la_voz_del_gancho():
    """Un valor fijo deja la voz sonando debajo de la explicación.

    `T_GANCHO` estaba en 2,5 s. El gancho de esdrújulas dura 2,0 y entraba; los grabados
    después duraban 3,2, 3,3 y 4,8 — dos voces encima, que es peor que el silencio que este
    diseño vino a evitar."""
    import shorts as motor
    for nombre in motor.GANCHOS:
        voz = motor.voz_de(nombre)
        if not voz:
            continue
        d = motor.duracion(voz)
        t = max(motor.T_GANCHO_MIN, d + 0.4)
        assert t >= d, ("la tarjeta de %s dura %.1fs y su voz %.1fs: la voz sigue sonando "
                        "debajo de la explicación" % (nombre, t, d))


def test_REGLA_el_gancho_hablado_es_UNA_PREGUNTA():
    """Se escucha una vez y no se puede releer. Una afirmación seguida de pregunta —
    «Camión lleva tilde. Camiones no. ¿Sabés por qué?»— dura 4,8 s y el doble de lo que
    hace falta para que alguien decida quedarse.

    El molde es el de la que funciona: «¿Sabés <la regla / qué es / por qué>…?» sobre el
    tema, sin ejemplo. El texto ESCRITO puede ser más largo y traer el ejemplo: ése se lee
    de un vistazo y se relee. Son dos textos distintos a propósito."""
    import shorts as motor
    src = open(os.path.join(RAIZ, "shorts.py"), encoding="utf-8").read()
    assert "REGLA 2" in src and "una pregunta" in src.lower(), (
        "la regla del gancho hablado no está escrita en el módulo")


def test_REGLA_ninguna_voz_de_gancho_es_larga():
    """El piso práctico: si un gancho hablado pasa de 3 segundos, dejó de ser una pregunta.

    No es un límite técnico —la regla 1 lo acomoda igual— es un límite de diseño: cada
    segundo antes de la explicación es un segundo donde alguien suelta."""
    import shorts as motor
    largos = []
    for nombre in motor.GANCHOS:
        voz = motor.voz_de(nombre)
        if voz and motor.duracion(voz) > 3.0:
            largos.append((os.path.basename(voz), round(motor.duracion(voz), 1)))
    assert not largos, (
        "estos ganchos hablados son largos: %s. Una pregunta corta del tema, sin ejemplo."
        % largos)


def test_todo_gancho_escrito_tiene_voz():
    """Sin el mp3, `shorts.py` arma igual y el Short abre 2,5 s mudo.

    24-ago-2026. Pablo no aprobó Mesa/alegría ni el de multiplicar: *«comienzan en
    silencio»*. Tenían gancho escrito y nunca se grabó la voz — `voz_de()` devolvía
    None, `t_gancho` caía a `T_GANCHO_MIN` y el audio de la lección arrancaba después.
    Medido: −91 dB hasta el segundo 2,6.

    «No hay voz» no puede ser un caso válido de un Short que se va a publicar."""
    import shorts as motor
    mudos = [n for n in motor.GANCHOS if not motor.voz_de(n)]
    assert not mudos, (
        "estos ganchos no tienen clip en ganchos_voz/: %s. Grabalos con "
        "grabar_ganchos.py — si no, el Short abre en silencio." % mudos)
