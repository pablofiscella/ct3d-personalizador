#!/usr/bin/env python3
"""Convierte una lección en video de Kydo en un Short vertical con gancho.

    python3 shorts.py --uno lec_acentuacion_esdrujulas.mp4    un solo Short, para mirar
    python3 shorts.py --todos                                 los que tengan gancho
    python3 shorts.py --listar                                qué lecciones hay y qué falta

POR QUÉ EXISTE
──────────────
Pablo, 4-ago-2026: *"quiero que tratemos de lograr un mejor video como producto. Creo que
si armamos un buen motor podemos hacer un buen video"*.

Kydo ya tiene **396 lecciones en video** de 16 a 43 segundos (mediana 29), con voz. Cada una
contesta lo que un padre escribe en YouTube a las nueve de la noche. O sea: **los Shorts ya
están hechos y pagados**, sólo que no tienen forma de Short.

Medido antes de escribir esto, mirando el segundo cero de una lección: un título de 12 px
arriba a la izquierda y una palabra en el medio de un fondo casi vacío, en 1280×720
horizontal. Falla en las cuatro cosas que importan — sin tensión, sin texto grande, sin
movimiento, sin formato vertical.

LO QUE DICE LA INVESTIGACIÓN, Y CÓMO ESTÁ APLICADO
──────────────────────────────────────────────────
Entre el 50% y el 60% de los que abandonan un Short lo hacen en los **primeros 3 segundos**,
y el 63% de los videos con mejor tasa de clic enganchan en ese lapso. De ahí sale toda la
estructura; cada decisión tiene su motivo al lado.

1. **Gancho en dos tiempos.** Primero el disparador (0–1,25 s): UNA pregunta que el que mira
   necesita contestar. Después el anclaje (1,25–2,5 s): para quién es y cuánto dura, así a
   los 3 segundos ya sabe si esto es para él. La pregunta sola se lee como clickbait; el
   anclaje solo no genera ninguna tensión.

2. **Pregunta específica, con un ejemplo de verdad.** «¿Por qué "música" lleva tilde y
   "musical" no?» abre una brecha concreta; «Aprendé acentuación» no abre nada. La regla:
   imposible de contestar con sí o no, y con la palabra real, no con la categoría.

3. **Micro-cortes al principio.** Los dos tiempos son dos planos distintos de ~1,25 s. El
   CORTE es lo que frena el pulgar: un plano fijo de 2,5 s se lee como una foto y se pasa.

4. **Texto grande, legible SIN sonido.** La mayoría mira sin audio en el primer pase. Un
   gancho que depende de la voz no existe.

5. **Nada de "Hola, ¿cómo están?".** Son los milisegundos más caros del video.

6. **La lección NO se toca.** El contenido educativo aguanta 35–45 s si la recompensa es
   clara, y éstas duran 29 de mediana. El contenido ya era bueno: faltaba la puerta.

LO QUE ESTE MOTOR **NO** HACE, A PROPÓSITO
──────────────────────────────────────────
No inventa el gancho con IA. Los ganchos viven en `GANCHOS`, escritos a mano, porque son la
única parte del video que decide si alguien lo ve — y una frase genérica ahí se nota de
inmediato. Generarlos automáticamente sería ahorrar el 3% del trabajo y arruinar el 100% del
resultado. Una lección sin gancho escrito **no se publica**: aparece en `--listar` para que
alguien lo escriba.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
LECCIONES = os.path.join(BASE, "lecciones_video")
SALIDA = os.path.join(BASE, "shorts_out")
PLAYER = os.path.join(BASE, "actividades_player.js")

# Vertical 9:16: el mismo lienzo sirve para Shorts, Reels y TikTok.
W, H = 1080, 1920

# El margen lateral. Pablo, mirando el primer prototipo: *"está pegado a los bordes"*. Con
# 80 px de cada lado quedan 920 útiles, y el tamaño de fuente se calcula contra ESE número
# midiendo con la fuente de verdad, no estimando.
MARGEN = 80

# La marca de Kydo, sacada de sus plantillas: el que llega por el video tiene que reconocer
# la página cuando cae.
TINTA = "0x121926"
FONDO = "0xF4F6FA"
ACENTO = "0x1F6FA8"
BLANCO = "0xFFFFFF"

# DejaVu tiene los acentos y los signos de apertura. Una fuente sin esa cobertura dibuja
# cuadraditos justo en el fotograma que más importa.
FUENTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FUENTE_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Los tiempos del gancho. El disparador entero antes de 1,5 s y el anclaje antes de 3.
T_DISPARO = 1.25
T_ANCLA = 1.25
T_GANCHO = T_DISPARO + T_ANCLA

# ─────────────────────────────────────────────────────────────────────────────
# LOS GANCHOS, uno por lección y escritos a mano.
#
#   q   la pregunta. Específica, con un ejemplo real, nunca de sí o no.
#   a   el anclaje: materia y grado. Es lo que hace que el padre de 5.º se quede y el de
#       1.º se vaya — y que se vaya rápido es BUENO: retener a quien no puede comprar le
#       enseña al algoritmo a buscar más gente que no compra.
#
# Van los de la primera tanda. El resto sale en `--listar` para irlos escribiendo.
# ─────────────────────────────────────────────────────────────────────────────
GANCHOS = {
    "lec_acentuacion_esdrujulas.mp4": {
        "q": "¿Por qué «música»\nlleva tilde\ny «musical» no?",
        "a": "Lengua · 5.º grado",
    },
    "lec_acentuacion_agudas.mp4": {
        "q": "«Camión» lleva tilde.\n«Camiones» no.\n¿Sabés por qué?",
        "a": "Lengua · 4.º grado",
    },
    "lec_acentuacion_graves.mp4": {
        "q": "¿Por qué «árbol»\nlleva tilde\ny «arboles» no?",
        "a": "Lengua · 4.º grado",
    },
    "lec_acentuacion_tonica.mp4": {
        "q": "¿Cuál es la sílaba\nfuerte de\n«ferrocarril»?",
        "a": "Lengua · 3.º grado",
    },
    "lec_multiplicar.mp4": {
        "q": "¿Por qué se corre\nun lugar al\nmultiplicar?",
        "a": "Matemática · 4.º grado",
    },
    "lec_abstractos_concretos.mp4": {
        "q": "«Mesa» y «alegría».\n¿Cuál de los dos\nse puede tocar?",
        "a": "Lengua · 4.º grado",
    },
}

# El cierre va al FINAL, cuando el que mira ya recibió algo. Pedir antes de dar es el mismo
# error que tenía el correo a las escuelas.
CIERRE = "Los 7 grados, gratis 30 días"
CIERRE_URL = "kydo.com.ar"


def _fuente_ok():
    return os.path.exists(FUENTE) and os.path.exists(FUENTE_R)


ed = None  # se resuelve tarde: PIL sólo hace falta para medir texto


def _medir(texto, ruta_fuente, tam):
    """Cuánto mide esa línea en píxeles, con la fuente DE VERDAD.

    Se mide en vez de estimar. Estimar el ancho como `chars × 0,6 × tamaño` es lo que
    tenía el gancho pegado a los bordes: con acentos, comillas angulares y mayúsculas, el
    error se va al 20% y una línea que “entraba” terminaba tocando los dos costados."""
    global ed
    if ed is None:
        from PIL import ImageFont
        ed = ImageFont.truetype
    try:
        f = ed(ruta_fuente, tam)
        try:
            c = f.getbbox(texto)
            return c[2] - c[0]
        except AttributeError:
            return f.getsize(texto)[0]
    except Exception:
        return int(len(texto) * tam * 0.62)      # peor caso: la estimación de antes


def tam_que_entra(lineas, ruta_fuente, ancho_util, tam_max, tam_min=40):
    """El tamaño de fuente MÁS GRANDE con el que la línea más larga entra en el ancho útil.

    Pablo, mirando el primer prototipo: *"está pegado a los bordes, no está centrado. Texto
    más grande"*. Las dos cosas se arreglan acá: se agranda hasta el límite real en vez de
    fijar un número a ojo, y el límite se calcula contra un ancho con márgenes de verdad."""
    for t in range(int(tam_max), int(tam_min) - 1, -2):
        if all(_medir(l, ruta_fuente, t) <= ancho_util for l in lineas):
            return t
    return tam_min


def bloque_centrado(entrada, salida, texto, ruta_fuente, color, tam, y_centro,
                    interlinea=1.22, enable=""):
    """Cada línea con su PROPIO `drawtext`, centrada por separado.

    `drawtext` con saltos de línea centra el BLOQUE pero deja las líneas alineadas a la
    izquierda adentro — por eso el gancho se veía desparejo aunque el x fuera (w-text_w)/2.
    Dibujando línea por línea, cada una queda centrada de verdad."""
    lineas = [l for l in texto.split("\n") if l.strip()]
    alto = tam * interlinea
    y0 = y_centro - (len(lineas) - 1) * alto / 2.0
    cond = (":enable='%s'" % enable) if enable else ""
    partes, act = [], entrada
    for i, linea in enumerate(lineas):
        sig = salida if i == len(lineas) - 1 else "%s_%d" % (salida, i)
        partes.append(
            "[%s]drawtext=fontfile=%s:text='%s':fontcolor=%s:fontsize=%d:"
            "x=(w-text_w)/2:y=%d-text_h/2%s[%s]"
            % (act, ruta_fuente, esc(linea), color, tam, int(y0 + i * alto), cond, sig))
        act = sig
    return partes


def esc(t):
    """Escapa el texto para `drawtext`, que interpreta `:`, `'`, `%` y la barra.

    Sin esto, un gancho con dos puntos —que son la mitad de los buenos— rompe el filtro, y
    ffmpeg falla con un error que no menciona el texto por ningún lado."""
    t = t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\u2019")
    return t.replace("%", "\\%")


def titulos_de_lecciones():
    """Lee `COMO_ES_VIDEO` del player: la única fuente de qué explica cada lección.

    Se lee del JS en vez de duplicar la tabla acá. Duplicarla significaría acordarse de dos
    lugares el día que se agregue una lección, y el que se olvida es siempre el segundo."""
    try:
        js = open(PLAYER, encoding="utf-8").read()
    except OSError:
        return {}
    out = {}
    for m in re.finditer(r'\{\s*t:\s*"([^"]+)"\s*,\s*f:\s*"(lec_[a-z0-9_]+\.mp4)"', js):
        out[m.group(2)] = m.group(1)
    for m in re.finditer(r'auto:\s*"(lec_[a-z0-9_]+\.mp4)"', js):
        out.setdefault(m.group(1), "")
    return out


def _filtro(g, dur_leccion):
    """El filtro de ffmpeg, en piezas para que se pueda leer.

    La lección va escalada al ancho completo y centrada. NO se recorta: recortar 16:9 a 9:16
    se comería el texto de la explicación, que es justo lo que la lección viene a mostrar.

    EL GANCHO VA ENCIMA, NO ANTES. La primera versión corría la lección 2,5 segundos para
    dejarle lugar al gancho, y el resultado eran **2,5 segundos de silencio absoluto** al
    abrir — medido: −91 dB hasta el segundo 3, y recién ahí entraba la voz. Lo cazó Pablo
    mirando el prototipo: *"que comience diciendo «si la sílaba…»"*.

    Y tenía razón por partida doble. Un Short que abre mudo desperdicia los milisegundos que
    más valen, justo cuando la mitad de la gente decide si sigue. Encima el gancho de texto
    y la voz se refuerzan en vez de turnarse.

    Se puede tapar sin perder nada porque el arranque de la lección es casi un fondo vacío
    —lo medimos: en el segundo cero hay una palabra chica y nada más—, así que la tarjeta
    del gancho no está escondiendo contenido. Y de paso el Short dura 2,5 segundos menos."""
    q, a = esc(g["q"]), esc(g["a"])
    cierre, url = esc(CIERRE), esc(CIERRE_URL)
    t0 = T_GANCHO
    fin = dur_leccion

    return ";".join([
        "color=c=%s:s=%dx%d:d=%.2f[bg]" % (FONDO, W, H, fin),

        # La lección desde el segundo CERO, imagen y voz en su tiempo original: sin
        # `setpts` ni `adelay`, que eran los que metían el silencio.
        "[0:v]scale=%d:-2[lec]" % W,
        "[bg][lec]overlay=(W-w)/2:(H-h)/2[v0]",

        # GANCHO, TIEMPO 1 — la pregunta, pantalla entera. Tarjeta sólida encima de todo:
        # el primer fotograma tiene que ser 100% gancho, sin nada de la lección asomando.
        "[v0]drawbox=x=0:y=0:w=%d:h=%d:color=%s@1:t=fill:enable='lt(t,%.2f)'[v1]"
        % (W, H, TINTA, T_DISPARO),
    ] + bloque_centrado(
        "v1", "v2", g["q"], FUENTE, BLANCO,
        tam_que_entra(g["q"].split("\n"), FUENTE, W - 2 * MARGEN, 130),
        H // 2, enable="lt(t,%.2f)" % T_DISPARO,
    ) + [
        # GANCHO, TIEMPO 2 — el anclaje. Otro plano y otro color: el corte frena el pulgar.
        "[v2]drawbox=x=0:y=0:w=%d:h=%d:color=%s@1:t=fill:"
        "enable='between(t,%.2f,%.2f)'[v3]" % (W, H, ACENTO, T_DISPARO, T_GANCHO),
    ] + bloque_centrado(
        "v3", "v4", g["a"], FUENTE, BLANCO,
        tam_que_entra(g["a"].split("\n"), FUENTE, W - 2 * MARGEN, 116),
        H // 2 - 80, enable="between(t,%.2f,%.2f)" % (T_DISPARO, T_GANCHO),
    ) + [
        "[v4]drawtext=fontfile=%s:text='en %d segundos':fontcolor=%s@0.85:fontsize=62:"
        "x=(w-text_w)/2:y=%d-text_h/2:enable='between(t,%.2f,%.2f)'[v5]"
        % (FUENTE_R, int(round(dur_leccion)), BLANCO, H // 2 + 70, T_DISPARO, T_GANCHO),
    ] + bloque_centrado(
        # DURANTE LA LECCIÓN — la pregunta arriba, siempre. El que entra por la mitad (en
        # Shorts, casi todo el mundo) tiene que saber qué mira sin rebobinar.
        #
        # Pablo, sobre el primer prototipo: *"el texto de arriba está muy chico"*. Y hay
        # lugar de sobra: la lección ocupa una banda de 608 px en el centro, así que arriba
        # quedan 656 px libres. Estaba chico por pereza mía, no por falta de espacio.
        "v5", "v6", g["q"], FUENTE, TINTA,
        tam_que_entra(g["q"].split("\n"), FUENTE, W - 2 * MARGEN, 78),
        300, enable="gte(t,%.2f)" % t0,
    ) + [

        # EL CIERRE — los últimos 2,5 s. Recién acá se pide algo.
        "[v6]drawtext=fontfile=%s:text='%s':fontcolor=%s:fontsize=54:"
        "x=(w-text_w)/2:y=h-330:enable='gte(t,%.2f)'[v7]"
        % (FUENTE, cierre, TINTA, fin - 2.5),
        "[v7]drawtext=fontfile=%s:text='%s':fontcolor=%s:fontsize=64:"
        "x=(w-text_w)/2:y=h-250:enable='gte(t,%.2f)'[vout]"
        % (FUENTE, url, ACENTO, fin - 2.5),

        # El audio, TAL CUAL, sin correr. Acá vivía el `adelay` que metía los 2,5 segundos
        # de silencio al abrir: se sacó junto con el `setpts` del video, y los dos tienen
        # que irse juntos o la voz queda desfasada de la imagen. `apad` se queda porque
        # evita que el archivo termine antes que la imagen si el audio es más corto.
        "[0:a]apad[aout]",
    ])


def duracion(ruta):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", ruta], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def armar(nombre, salida_dir=SALIDA, leccion_dir=LECCIONES, quiet=False):
    """Arma UN Short. Devuelve (ok, mensaje-o-ruta)."""
    entrada = os.path.join(leccion_dir, nombre)
    if not os.path.exists(entrada):
        return False, "no existe %s" % nombre
    g = GANCHOS.get(nombre)
    if not g:
        return False, ("%s no tiene gancho escrito. Se escribe a mano en GANCHOS: es la "
                       "parte que decide si alguien lo mira." % nombre)
    if not _fuente_ok():
        return False, "falta DejaVu Sans (paquete fonts-dejavu)"
    dur = duracion(entrada)
    if dur <= 0:
        return False, "no puedo leer la duración de %s" % nombre

    os.makedirs(salida_dir, exist_ok=True)
    destino = os.path.join(salida_dir, nombre.replace("lec_", "short_"))
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", entrada,
           "-filter_complex", _filtro(g, dur),
           "-map", "[vout]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-r", "30",
           "-c:a", "aac", "-b:a", "128k",
           "-t", "%.2f" % dur, destino]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return False, "ffmpeg falló: %s" % (r.stderr.strip()[:400] or "sin detalle")
    if not quiet:
        print("   %s  (%.0fs)" % (os.path.basename(destino), dur))
    return True, destino


def listar():
    titulos = titulos_de_lecciones()
    todas = sorted(f for f in os.listdir(LECCIONES) if f.endswith(".mp4"))
    con = [f for f in todas if f in GANCHOS]
    sin = [f for f in todas if f not in GANCHOS]
    print("Lecciones: %d · con gancho: %d · falta escribir: %d\n"
          % (len(todas), len(con), len(sin)))
    for f in con:
        print("  ✔ %-42s %s" % (f, GANCHOS[f]["q"].replace("\n", " ")))
    print()
    for f in sin[:25]:
        print("  · %-42s %s" % (f, titulos.get(f, "")))
    if len(sin) > 25:
        print("  … y %d más" % (len(sin) - 25))


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--uno", help="una lección puntual, para mirarla")
    p.add_argument("--todos", action="store_true", help="todas las que tengan gancho")
    p.add_argument("--listar", action="store_true", help="qué hay y qué falta")
    a = p.parse_args()

    if not shutil.which("ffmpeg"):
        print("falta ffmpeg", file=sys.stderr)
        return 1
    if a.listar:
        listar()
        return 0
    if a.uno:
        ok, msg = armar(a.uno)
        print(msg if not ok else "listo: %s" % msg)
        return 0 if ok else 1
    if a.todos:
        hechos = 0
        for f in sorted(GANCHOS):
            ok, msg = armar(f)
            if ok:
                hechos += 1
            else:
                print("   ✘ %s" % msg)
        print("\n%d Shorts en %s" % (hechos, SALIDA))
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
