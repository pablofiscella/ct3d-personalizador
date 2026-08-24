#!/usr/bin/env python3
"""Graba la voz del gancho de cada Short, con Valeria.

    python3 grabar_ganchos.py                 # las que falten
    python3 grabar_ganchos.py --rehacer       # todas, pisando las que ya están

POR QUÉ ES UN CLIP APARTE Y NO LA PRIMERA LÍNEA DE LA LECCIÓN
─────────────────────────────────────────────────────────────
La lección arranca explicando; el Short arranca preguntando. Son dos textos con dos trabajos
distintos: uno enseña y el otro hace que alguien se quede. Por eso el gancho hablado vive en
`VOZ_GANCHO` y no sale del guion.

LAS DOS REGLAS QUE SE VERIFICAN ACÁ (6-ago-2026)
────────────────────────────────────────────────
Pablo, escuchando los tres primeros: *"el momento en el que habla cuando comienza es más
largo que lo que dura el banner y se solapa con el audio de la explicación"*. Y: *"ese es el
gancho: una pregunta"*.

  1. **Es una pregunta.** Se chequea que empiece con «¿». Una afirmación seguida de pregunta
     —«Camión lleva tilde. Camiones no. ¿Sabés por qué?»— dura 4,8 s y es el doble de lo que
     hace falta.
  2. **Dura menos de 3 segundos.** No es un límite técnico (el motor acomoda la tarjeta al
     largo de la voz): es de diseño. Cada segundo antes de la explicación es un segundo en
     el que alguien suelta.

Si un clip sale largo, este script lo dice y NO lo deja pasar en silencio. Es la diferencia
entre enterarse acá o enterarse mirando el Short terminado.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import shorts  # noqa: E402

VOZ_VALERIA = "9oPKasc15pfAbMr7N6Gs"      # la misma del cuaderno, no una voz de stock
TOPE = 3.0


def grabar(nombre, texto, rehacer=False):
    import audiolibro
    destino = os.path.join(shorts.VOCES, nombre.replace("lec_", "").replace(".mp4", ".mp3"))
    if os.path.exists(destino) and not rehacer:
        return destino, shorts.duracion(destino), "ya estaba"
    audio = audiolibro._tts_elevenlabs(texto, voice_id=VOZ_VALERIA)
    if not audio:
        return None, 0, "ElevenLabs no devolvió audio (¿falta la clave?)"
    os.makedirs(shorts.VOCES, exist_ok=True)
    with open(destino, "wb") as f:
        f.write(audio)
    return destino, shorts.duracion(destino), "grabado"


def main(argv):
    rehacer = "--rehacer" in argv
    problemas = []
    for nombre, texto in shorts.VOZ_GANCHO.items():
        if not texto.lstrip().startswith("¿"):
            problemas.append("%s: el gancho hablado no es una pregunta" % nombre)
            continue
        ruta, dur, que = grabar(nombre, texto, rehacer)
        if not ruta:
            problemas.append("%s: %s" % (nombre, que))
            continue
        largo = " ← LARGO, pasa de %.1fs" % TOPE if dur > TOPE else ""
        print("  %-30s %4.1fs  %-9s %s%s" % (
            os.path.basename(ruta), dur, que, texto[:44], largo))
        if dur > TOPE:
            problemas.append("%s dura %.1fs" % (os.path.basename(ruta), dur))
    print()
    if problemas:
        print("REVISAR:")
        for p in problemas:
            print("   · %s" % p)
        return 1
    print("las %d voces están y ninguna pasa de %.0f segundos" % (len(shorts.VOZ_GANCHO), TOPE))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
