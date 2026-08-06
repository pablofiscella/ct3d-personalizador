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
# ═════════════════════════════════════════════════════════════════════════════
# REGLA 1 — LA TARJETA DEL GANCHO DURA LO QUE DURA SU VOZ
#
# 6-ago-2026. Pablo: *"el momento en el que habla cuando comienza es más largo que lo que
# dura el banner y se solapa con el audio de la explicación"*.
#
# `T_GANCHO` estaba fijo en 2,5 s. El gancho de esdrújulas dura 2,0 y entraba; los tres que
# se grabaron después duran 3,2, 3,3 y 4,8 — así que la voz del gancho seguía hablando
# mientras arrancaba la explicación. Dos voces encima, que es peor que el silencio original.
#
# Y es un error REPETIDO: el día anterior se arregló que la tarjeta del CIERRE durara lo que
# dura su voz, y no se aplicó lo mismo al gancho. La misma regla, media aplicada.
#
# `T_GANCHO_MIN` es el piso: aunque no haya voz, la pregunta tiene que poder leerse.
# ═════════════════════════════════════════════════════════════════════════════
T_GANCHO_MIN = 2.5

# ─────────────────────────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════
# REGLA 2 — EL GANCHO HABLADO ES UNA PREGUNTA CORTA DEL TEMA
#
# 6-ago-2026. Pablo, comparando: *"en el de las esdrújulas comenzaba mejor diciendo «¿sabés
# la regla de las esdrújulas?». Ese es el gancho: una pregunta"*.
#
# El primer intento grabó el texto ESCRITO del gancho, que es más largo y no siempre es una
# pregunta: «Camión lleva tilde. Camiones no. ¿Sabés por qué?» son una afirmación y después
# una pregunta, y dura 4,8 segundos. La versión que funciona dura 2,0 y es una sola pregunta.
#
# Son dos textos DISTINTOS a propósito, y conviene entender por qué:
#
#   · el ESCRITO puede ser más largo y traer el ejemplo — se lee de un vistazo y se relee
#   · el HABLADO tiene que ser una pregunta y nada más — se escucha una vez, y cada segundo
#     antes de la explicación es un segundo donde alguien suelta
#
# El molde: «¿Sabés <la regla / qué es / por qué> …?» sobre el tema, sin ejemplo.
# ═════════════════════════════════════════════════════════════════════════════

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
# EL CIERRE, a pantalla completa (5-ago-2026). Antes eran dos renglones abajo del video;
# Pablo, comparando con el Short que aprobó: *"terminaba diciendo Kydo siempre pensando en la
# educación, o el eslogan que sea... y ocupaba toda la pantalla"*.
#
# Va como tarjeta entera y no como pie porque es lo único del Short que PIDE algo. Un pedido
# que comparte cuadro con la explicación compite con ella y pierde.
CIERRE_LEMA = "Pensando en la\neducación\nde tus hijos"
CIERRE = "Los 7 grados · 30 días gratis"
CIERRE_URL = "kydo.com.ar"
CIERRE_VOZ = "cierre_a.mp3"       # el remate hablado, el mismo para todas las lecciones
T_CIERRE = 2.8                    # sólo si no hay voz de cierre; si la hay, manda su largo


def voz_cierre():
    """El clip del remate, o None. Es el mismo para todos los Shorts: el cierre no cambia
    con la lección, así que se graba una vez y se reusa."""
    r = os.path.join(VOCES, CIERRE_VOZ)
    return r if os.path.exists(r) else None


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


VOCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ganchos_voz")


def voz_de(nombre):
    """El clip de voz del gancho de esta lección, o None.

    `lec_acentuacion_esdrujulas.mp4` → `ganchos_voz/acentuacion_esdrujulas.mp3`."""
    slug = nombre[4:-4] if nombre.startswith("lec_") else os.path.splitext(nombre)[0]
    ruta = os.path.join(VOCES, slug + ".mp3")
    return ruta if os.path.exists(ruta) else None


IDX_GANCHO = 1


def _filtro(g, dur_leccion, voz=None, llena=False, t_cierre=T_CIERRE, vc=False,
            t_gancho=T_GANCHO_MIN):
    """El filtro completo. `voz` es el clip del gancho (o None) y `vc` si hay remate hablado.

    Los índices de entrada de ffmpeg dependen de qué clips existan: la lección es siempre 0,
    el gancho 1 si está, y el cierre va después. Se calcula acá y no se escribe a mano
    porque un índice fijo revienta en silencio el día que falta un clip."""
    idx_cierre = IDX_GANCHO + (1 if voz else 0)
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
    t0 = t_gancho
    # El Short dura la lección MÁS la tarjeta del gancho: la lección ya no se pisa, empieza
    # cuando la tarjeta se levanta. Si `fin` siguiera siendo `dur_leccion`, se cortarían los
    # últimos 2,5 segundos de la explicación — que es donde suele estar la conclusión.
    # La lección entera MÁS el gancho adelante MÁS el cierre atrás. El cierre se AGREGA,
    # no se superpone: hasta ahora arrancaba en `fin_leccion` y tapaba los últimos
    # segundos de la explicación mientras la voz todavía hablaba.
    #
    # Pablo, mirando el que ya había publicado: *"el audio sigue donde está el final.
    # Debería haber seguido el video hasta que termine de hablar y recién después el remate"*.
    #
    # En el Short que él aprobó el orden es ése: la lección cierra con su «En resumen», se
    # calla, y ahí entra la tarjeta. El remate es lo último que se ve y lo único que pide
    # algo — compartirlo con la explicación lo convierte en ruido.
    fin_leccion = dur_leccion + t_gancho
    fin = fin_leccion + t_cierre

    return ";".join([
        "color=c=%s:s=%dx%d:d=%.2f[bg]" % (FONDO, W, H, fin),

        # IMAGEN Y SONIDO SE CORREN JUNTOS. El `setpts` acá y el `adelay` de abajo son la
        # misma decisión partida en dos: si se mueve uno solo, la boca va por un lado y la
        # voz por otro. El comentario de la versión anterior ya lo advertía —"los dos tienen
        # que irse juntos"— y se cumplió sacando los dos; ahora se cumple poniéndolos.
        # LA LECCIÓN NO SE ENCOGE SI YA VIENE VERTICAL.
        #
        # `scale=W:-2` sobre un video 1280×720 lo deja de 1080×608 en un lienzo de 1920: usa
        # el 32% de la pantalla y las tarjetas de ejemplo quedan ilegibles en un teléfono.
        # Eso ya estaba medido y descartado —el aviso viejo con la ilustración al 35% dio
        # **3 segundos de reproducción promedio y 0,7% de finalización sobre 51.550
        # impresiones**— y aun así lo repetí, porque no leí el comentario que lo decía.
        #
        # `force_original_aspect_ratio=increase` + recorte centrado: una lección que ya nace
        # 1080×1920 pasa igual, y una horizontal se agranda hasta llenar en vez de flotar en
        # el medio. Lo correcto es renderizar la lección vertical desde la fuente; esto es
        # la red para el que todavía no la tenga.
        "[0:v]scale=%d:%d:force_original_aspect_ratio=increase,"
        "crop=%d:%d,setpts=PTS+%.2f/TB[lec]" % (W, H, W, H, t_gancho),
        "[bg][lec]overlay=0:0[v0]",

        # GANCHO, TIEMPO 1 — la pregunta, pantalla entera. Tarjeta sólida encima de todo:
        # el primer fotograma tiene que ser 100% gancho, sin nada de la lección asomando.
        # La tarjeta cubre TODO el gancho, no sólo el primer tramo. Antes duraba `T_DISPARO`
        # porque después entraba la tarjeta del anclaje; sin ella quedaba un hueco de 1,25 s
        # con la lección a la vista y su audio todavía retenido.
        "[v0]drawbox=x=0:y=0:w=%d:h=%d:color=%s@1:t=fill:enable='lt(t,%.2f)'[v1]"
        % (W, H, TINTA, t_gancho),
    ] + bloque_centrado(
        "v1", "v2", g["q"], FUENTE, BLANCO,
        tam_que_entra(g["q"].split("\n"), FUENTE, W - 2 * MARGEN, 130),
        H // 2, enable="lt(t,%.2f)" % t_gancho,
    ) + [
        # EL ANCLAJE SE FUE (6-ago-2026). Era una segunda tarjeta con «Lengua · 5.º
        # grado» y «en 20 segundos», entre el gancho y la lección. Pablo, mirando el primer
        # Short armado desde la vertical: *"la parte que dice lengua 5 grado 20 segundos no
        # va"*.
        #
        # Estaba justificada así: "el anclaje hace que el padre de 5.º se quede y el de 1.º
        # se vaya, y que se vaya rápido es BUENO". El razonamiento no es malo, pero pone una
        # pantalla más entre la pregunta y la respuesta — y en un Short, cada pantalla que
        # no es la respuesta es una oportunidad de que suelten.
        #
        # Sacarlo además devuelve 1,25 s al principio, que es donde más valen.
        "[v2]null[v5]",
    ] + (bloque_centrado(
        # DURANTE LA LECCIÓN — la pregunta arriba. El que entra por la mitad (en Shorts,
        # casi todo el mundo) tiene que saber qué mira sin rebobinar.
        #
        # SÓLO SI LA LECCIÓN NO LLENA LA PANTALLA. La justificación original era "la lección
        # ocupa una banda de 608 px en el centro, así que arriba quedan 656 libres" — y eso
        # valía con el video horizontal encogido. Con una lección que nace vertical no hay
        # lugar: el recordatorio se le monta encima al contenido y tapa la explicación.
        #
        # Lo vio Pablo en el primer Short armado desde la vertical. Es la misma clase de
        # error que el resto del día: una decisión correcta bajo un supuesto que después
        # cambió, y el supuesto estaba escrito al lado.
        "v5", "v6", g["q"], FUENTE, TINTA,
        tam_que_entra(g["q"].split("\n"), FUENTE, W - 2 * MARGEN, 78),
        300, enable="gte(t,%.2f)" % t0,
    ) if not llena else ["[v5]null[v6]"]) + [

        # EL CIERRE — tarjeta ENTERA, los últimos segundos. Recién acá se pide algo, y por
        # eso no comparte cuadro con la explicación: un pedido que compite con el contenido
        # pierde. Fondo sólido encima de todo, como la tarjeta del gancho.
        "[v6]drawbox=x=0:y=0:w=%d:h=%d:color=%s@1:t=fill:enable='gte(t,%.2f)'[c0]"
        % (W, H, TINTA, fin_leccion),
    ] + bloque_centrado(
        "c0", "c1", CIERRE_LEMA, FUENTE, BLANCO,
        tam_que_entra(CIERRE_LEMA.split("\n"), FUENTE, W - 2 * MARGEN, 108),
        int(H * 0.40), enable="gte(t,%.2f)" % fin_leccion,
    ) + [
        "[c1]drawtext=fontfile=%s:text='%s':fontcolor=%s:fontsize=72:"
        "x=(w-text_w)/2:y=%d:enable='gte(t,%.2f)'[c2]"
        % (FUENTE, url, ACENTO, int(H * 0.62), fin_leccion),
        "[c2]drawtext=fontfile=%s:text='%s':fontcolor=%s:fontsize=44:"
        "x=(w-text_w)/2:y=%d:enable='gte(t,%.2f)'[vout]"
        % (FUENTE, cierre, BLANCO, int(H * 0.70), fin_leccion),

        # ── LA REGLA DEL AUDIO (5-ago-2026) ────────────────────────────────────────
        #
        # **La voz de la lección NO puede sonar mientras la tarjeta del gancho tapa la
        # pantalla.** Es lo único que hay que respetar acá, y se rompió de la forma más
        # fácil de no ver: la imagen y el sonido eran correctos por separado.
        #
        # Pablo lo escuchó: *"los audios están corridos. No habla el texto inicial y eso
        # hace que quede todo corrido"*. Medido después: −18,8 dB desde el segundo cero, o
        # sea la explicación arrancando debajo de la pregunta.
        #
        # POR QUÉ ESTABA ASÍ, y no fue un descuido: la versión anterior corría la lección
        # 2,5 s y el Short abría con silencio absoluto, que en un feed es peor. La solución
        # fue taparlo con la voz del gancho... pero el motor NUNCA mezcló esa voz. Sólo
        # existía en el Short que se armó a mano. O sea que la premisa del arreglo anterior
        # —"la voz del gancho cubre el silencio"— no era cierta en el código.
        #
        # Ahora hay dos caminos y ninguno desincroniza:
        #
        #   · CON voz de gancho  → la voz suena desde 0 y la lección entra cuando termina
        #     la tarjeta. Que es lo que se quería desde el principio.
        #   · SIN voz de gancho  → la lección se corre lo que dura la tarjeta. Vuelven los
        #     2,5 s sin explicación, pero se lee la pregunta y no se pierde nada de la
        #     lección. Silencio es peor que nada; desincronizado es peor que silencio.
        #
        # Y el video se corre junto con el audio (`setpts`), o volvemos a tener el problema
        # inverso: el sonido atrasado respecto de la imagen.
    ] + [
        # ── EL AUDIO ───────────────────────────────────────────────────────────────
        # Tres piezas que no se pisan: el gancho hablado al principio, la lección en el
        # medio, y el remate al final. Cada una entra cuando la anterior terminó.
        #
        # Pablo pidió las tres: *"el gancho estaba hablado"* y *"el cierre hablando como al
        # comienzo"*. Un Short mudo en las puntas desperdicia justo los momentos donde se
        # decide si alguien se queda y si alguien hace clic.
        "[0:a]adelay=%d|%d[lecA]" % (int(t_gancho * 1000), int(t_gancho * 1000)),
    ] + ([
        "[%d:a]adelay=0|0[ganA]" % IDX_GANCHO,
    ] if voz else []) + ([
        "[%d:a]adelay=%d|%d[cieA]" % (idx_cierre, int(fin_leccion * 1000),
                                      int(fin_leccion * 1000)),
    ] if vc else []) + [
        "%samix=inputs=%d:dropout_transition=0:normalize=0[am]"
        % ("[lecA]" + ("[ganA]" if voz else "") + ("[cieA]" if vc else ""),
           1 + (1 if voz else 0) + (1 if vc else 0)),
        "[am]apad[aout]",
    ])


def _es_vertical(ruta):
    """¿El video ya viene en formato vertical (o más alto que 9:16)?

    Decide si el recordatorio del gancho tiene lugar arriba o le tapa la lección."""
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0", ruta],
                       capture_output=True, text=True)
    try:
        w, h = [int(x) for x in r.stdout.strip().split(",")[:2]]
        return h / float(w) >= 1.6          # 9:16 es 1.777; 4:3 es 0.75
    except Exception:
        return False


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
    voz = voz_de(nombre)
    # ¿La lección ya llena el cuadro vertical? Se mide, no se supone: el mismo motor tiene
    # que servir para las lecciones horizontales viejas y las verticales nuevas.
    llena = _es_vertical(entrada)
    # El remate hablado y cuánto dura. La tarjeta del cierre dura LO QUE DURA LA VOZ, no un
    # número fijo: con 2,8 s escritos a mano y un clip de 3,2 el final quedaba cortado a
    # mitad de frase.
    vc = voz_cierre()
    t_cierre = max(T_CIERRE, duracion(vc) + 0.3) if vc else T_CIERRE
    # REGLA 1: la tarjeta dura lo que dura la voz del gancho, más un respiro. Con un valor
    # fijo, un gancho hablado más largo sigue sonando debajo de la explicación.
    t_gancho = max(T_GANCHO_MIN, duracion(voz) + 0.4) if voz else T_GANCHO_MIN
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", entrada]
    if voz:
        cmd += ["-i", voz]                     # entrada 1: la voz del gancho
    if vc:
        cmd += ["-i", vc]                      # y después: el remate
    cmd += ["-filter_complex", _filtro(g, dur, voz, llena, t_cierre, bool(vc), t_gancho),
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "128k",
            # La lección MÁS la tarjeta: si se cortara en `dur`, se perderían los últimos
            # 2,5 segundos de la explicación, que es donde suele estar la conclusión.
            "-t", "%.2f" % (dur + t_gancho + t_cierre), destino]
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
