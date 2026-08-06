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
    """Dos Shorts recién armados: uno CON voz de gancho y otro SIN.

    Son los dos caminos del filtro, y hay que probar los dos: el bug vivía justamente en que
    uno de ellos —el que no tiene voz— nunca se había escuchado."""
    import shorts as motor
    pares = []
    for nombre in ("lec_acentuacion_esdrujulas.mp4", "lec_multiplicar.mp4"):
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
        v = _volumen(ruta, 0, motor.T_GANCHO - 0.3)
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
        v = _volumen(ruta, motor.T_GANCHO + 0.5, 2)
        assert v is not None and v > -50, (
            "%s sigue mudo después de la tarjeta (%.1f dB)" % (nombre, v if v else -99))


def test_no_se_corta_el_final_de_la_leccion(shorts):
    """Correr la lección sin alargar el Short le comería los últimos segundos — que es donde
    suele estar la conclusión. El Short tiene que durar la lección MÁS la tarjeta."""
    import shorts as motor
    for nombre, ruta, _ in shorts:
        d_lec = motor.duracion(os.path.join(motor.LECCIONES, nombre))
        d_short = motor.duracion(ruta)
        assert d_short >= d_lec + motor.T_GANCHO - 0.5, (
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
