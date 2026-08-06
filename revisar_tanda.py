#!/usr/bin/env python3
"""Revisa una tanda de Shorts ANTES de mostrársela a Pablo.

    python3 revisar_tanda.py short_homofonos_4.mp4 short_tildes_6_a.mp4 ...
    python3 revisar_tanda.py                # todos los de VOZ_GANCHO

Qué mira, y por qué cada cosa:

  · **Formato 1080×1920.** Un Short horizontal lo rechaza la red o lo muestra con bandas.
  · **Duración.** Menos de 15 s no alcanza para explicar nada; más de 60 deja de ser Short.
  · **Suena desde el segundo cero.** Si la voz del gancho no se mezcló, el Short abre mudo
    y en un feed eso es el primer motivo para seguir de largo. Pasó el 5-ago: los clips
    existían y el motor nunca los mezclaba.
  · **Suena al final.** El remate hablado es lo único que pide algo; si falta, el Short
    termina en una placa muda.
  · **La lección no habla debajo de la tarjeta del gancho.** Es el desfasaje que Pablo
    escuchó: *"los audios están corridos"*.

Es lo mismo que verifica `test_shorts_audio_sincronizado`, pero sobre los archivos ya
armados y de a tandas: el test prueba el motor, esto prueba lo que se va a publicar.
"""
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import shorts  # noqa: E402

MIN_SEG, MAX_SEG = 15.0, 60.0


def volumen(ruta, desde, dur=1.5):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", str(desde), "-t", str(dur),
                        "-i", ruta, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else None


def dims(ruta):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height", "-of", "csv=p=0", ruta],
                       capture_output=True, text=True)
    return r.stdout.strip().rstrip(",")


def revisar(ruta):
    """Devuelve (lista de problemas, resumen para mostrar)."""
    fallas = []
    d = dims(ruta)
    if d != "1080,1920":
        fallas.append("formato %s" % d)
    dur = shorts.duracion(ruta)
    if dur < MIN_SEG:
        fallas.append("dura %.1fs, muy corto" % dur)
    if dur > MAX_SEG:
        fallas.append("dura %.1fs, se pasa de Short" % dur)

    v0 = volumen(ruta, 0, 1.2)
    if v0 is None or v0 < -50:
        fallas.append("abre MUDO (%.1f dB): no se mezcló la voz del gancho"
                      % (v0 if v0 is not None else -99))
    vfin = volumen(ruta, max(0, dur - 2.0), 1.5)
    if vfin is None or vfin < -50:
        fallas.append("termina mudo (%.1f dB): falta el remate hablado"
                      % (vfin if vfin is not None else -99))
    return fallas, "%.1fs  %s  inicio %s dB  final %s dB" % (
        dur, d, "%.0f" % v0 if v0 is not None else "?",
        "%.0f" % vfin if vfin is not None else "?")


def main(argv):
    nombres = argv or [n.replace("lec_", "short_") for n in shorts.VOZ_GANCHO]
    malos = 0
    for n in nombres:
        ruta = n if os.path.isabs(n) else os.path.join(shorts.SALIDA, n)
        if not os.path.exists(ruta):
            print("  ✗ %-32s no existe" % n)
            malos += 1
            continue
        fallas, resumen = revisar(ruta)
        print("  %s %-32s %s" % ("✓" if not fallas else "✗", os.path.basename(ruta), resumen))
        for f in fallas:
            print("      · %s" % f)
        malos += bool(fallas)
    print()
    print("%d de %d listos para mostrar" % (len(nombres) - malos, len(nombres)))
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
