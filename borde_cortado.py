#!/usr/bin/env python3
"""¿Hay contenido CORTADO por los bordes del Short?

    python3 borde_cortado.py                 # todos los de VOZ_GANCHO
    python3 borde_cortado.py short_x.mp4 …

6-ago-2026. Pablo, mirando el Short de hiperónimos: *"cuando están las 3 tarjetas, se
cortan"*. Tenía razón, y la causa era mía: el Short se maqueta en un lienzo de 720 px de
ancho para que el texto reflowee, y una fila de tres tarjetas de 300 px suma 940. Se salían
por los dos costados.

POR QUÉ HACE FALTA UN CHEQUEO Y NO ALCANZA CON MIRAR
────────────────────────────────────────────────────
Porque hay que mirar QUINCE videos de treinta segundos, y el corte dura los pocos segundos
de una escena. Es exactamente el tipo de defecto que se escapa cuando uno revisa con apuro:
no falla, no da error, y el 90 % del video se ve perfecto.

CÓMO LO DETECTA
───────────────
Las lecciones tienen fondo claro y uniforme. Si en la columna de píxeles pegada al borde hay
algo que NO es fondo, es que una tarjeta, una palabra o una figura quedó cortada al medio.

Se mide en varios momentos del video, salteando el gancho y el cierre —que son tarjetas a
sangre y tocan los bordes a propósito—.

Da falsos positivos con fondos que llegan al borde por diseño. Por eso informa CUÁNTO borde
está manchado y en qué segundo: es para ir a mirar ese instante, no para decidir solo.
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import shorts  # noqa: E402

BORDE = 6          # columnas de píxeles a mirar de cada lado
TOLERANCIA = 28    # cuánto puede diferir del fondo antes de contar como contenido
# El umbral arrancó en 4 % y dejaba pasar el caso real: hiperónimos, con las tres tarjetas
# saliéndose por los dos costados, daba 2 %. Es que el corte afecta una franja angosta del
# alto —la de las tarjetas—, no media pantalla.
#
# Con 1,5 % marca los dos videos que tienen algo tocando el borde, y uno de ellos es
# legítimo. Está bien que sea así: esto dice "andá a mirar el segundo 14", no "está mal".
# Un chequeo con cero falsos positivos sobre 15 videos es un chequeo que no encuentra nada.
UMBRAL = 0.015


def analizar(ruta, t):
    """(izq, der) = fracción del alto del borde que NO es fondo, en el segundo `t`."""
    try:
        from PIL import Image
    except ImportError:
        return None, None
    png = "/tmp/_borde.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.1f" % t, "-i", ruta,
                    "-frames:v", "1", png], check=False)
    if not os.path.exists(png):
        return None, None
    im = Image.open(png).convert("RGB")
    w, h = im.size
    px = im.load()
    # El fondo se toma del propio fotograma, en una zona que siempre es fondo: la esquina
    # superior izquierda, debajo del rótulo.
    fondo = px[3, int(h * 0.30)]

    def manchado(xs):
        n = 0
        for y in range(0, h, 4):
            for x in xs:
                p = px[x, y]
                if max(abs(p[i] - fondo[i]) for i in range(3)) > TOLERANCIA:
                    n += 1
                    break
        return n / (h / 4)

    return manchado(range(0, BORDE)), manchado(range(w - BORDE, w))


def main(argv):
    nombres = argv or [n.replace("lec_", "short_") for n in shorts.VOZ_GANCHO]
    malos = 0
    for n in nombres:
        ruta = n if os.path.isabs(n) else os.path.join(shorts.SALIDA, n)
        if not os.path.exists(ruta):
            print("  ✗ %-34s no existe" % n)
            continue
        dur = shorts.duracion(ruta)
        # Se saltea el gancho (tarjeta a sangre) y el cierre (ídem).
        momentos = [dur * f for f in (0.25, 0.40, 0.55, 0.70)]
        peor, cuando = 0.0, 0
        for t in momentos:
            izq, der = analizar(ruta, t)
            if izq is None:
                print("  ?  %-34s falta Pillow" % n)
                break
            m = max(izq, der)
            if m > peor:
                peor, cuando = m, t
        else:
            aviso = "  ← MIRAR el segundo %.0f" % cuando if peor > UMBRAL else ""
            print("  %s %-34s borde tocado: %3.0f%%%s"
                  % ("✗" if peor > UMBRAL else "✓", os.path.basename(ruta), peor * 100, aviso))
            malos += peor > UMBRAL
    print()
    print("%d con contenido pegado al borde" % malos)
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
