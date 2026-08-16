#!/usr/bin/env python3
"""Abecedario de banderines de un tema: generar, normalizar y revisar.

Cada letra es el banderín del tema con esa letra dibujada encima, pedido a OpenAI con la
lámina `temas/<tema>/extras/banderin.png` como referencia — la referencia fija el estilo y
el prompt sólo dice qué agregar (la misma receta que la hoja de personajes de los cuentos).
Las letras terminan en `temas/<tema>/letras/` y ahí las levanta `piezas.banderin_letras`.

    python3 herramientas/abecedario.py generar princesas    # pide las 32 a OpenAI
    python3 herramientas/abecedario.py limpiar princesas    # fondo negro -> blanco
    python3 herramientas/abecedario.py revisar princesas    # grilla para MIRARLAS
    python3 herramientas/abecedario.py instalar princesas   # optimiza y copia al tema

Tres cosas que se aprendieron haciendo el de safari (16-ago-2026) y conviene no volver a
descubrir:

1. **El modelo barato alcanza.** `gpt-image-1-mini` sale US$0,011 la imagen contra
   US$0,053 de `gpt-image-2`, y para agregarle una letra a un dibujo que ya existe rinde
   igual. TODO el abecedario va con el MISMO modelo: mezclar dos da letras que no combinan.
2. **El fondo sale negro sin patrón** — 10 de 32 en safari. Un fondo negro impreso arruina
   la hoja, y no se puede umbralizar a secas porque el dibujo también tiene zonas oscuras:
   se rellena desde las esquinas, que sólo toca lo conectado con el borde.
3. **Hay que MIRAR las 32.** El modelo escribe mal una letra cada tanto y eso no lo detecta
   ningún conteo de archivos. Por eso `revisar` escribe abajo de cada banderín qué debería
   decir: se comparan de una mirada.

Barato de verdad: el Batch API acepta `/v1/images/edits` con 50 % de descuento a cambio de
esperar hasta 24 h. Para pregenerar abecedarios no urge nada — vale la pena si se hacen
todos los temas de una.
"""
import base64
import glob
import json
import os
import sys
import time

_PROY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROY)

CONFIG = "/opt/ct3d/backend/config.json"
MODELO = os.environ.get("MODELO_IMG", "gpt-image-1-mini")

# A-Z más lo que usan los nombres de acá: sin la Ñ ni las vocales con tilde, «Tomás» o
# «Iñaki» salen con un hueco en la guirnalda.
LETRAS = [chr(c) for c in range(ord("A"), ord("Z") + 1)] + ["Ñ", "Á", "É", "Í", "Ó", "Ú"]

# El nombre del archivo no lleva tilde ni Ñ: el zip del kit y el repo viajan entre sistemas
# de archivos que normalizan los acentos distinto.
ARCHIVO = {"Ñ": "ENIE", "Á": "A_TILDE", "É": "E_TILDE", "Í": "I_TILDE",
           "Ó": "O_TILDE", "Ú": "U_TILDE"}

PROMPT = (
    "Take this party pennant/bunting flag illustration and add the single capital letter "
    "'{letra}' to it, keeping EVERYTHING else exactly as it is: same triangular pennant "
    "shape, same characters, same plants, same balloons, same colors, same flat "
    "storybook illustration style, same cream background.\n\n"
    "The letter must be:\n"
    "- ONE single capital letter '{letra}', spelled exactly, nothing else, no other text\n"
    "- LARGE and bold, taking about a third of the pennant width, clearly readable from "
    "across a room\n"
    "- placed in the lower-middle area of the triangle, over the foliage, WITHOUT covering "
    "the animals or characters\n"
    "- hand-drawn in the same style as the artwork, in the artwork's dark accent color, "
    "with a soft cream rounded plaque or label behind it so it reads against the leaves\n\n"
    "Keep the white margin around the pennant so it can be cut out. Do not add any other "
    "letters, words, numbers or decorations."
)


def crudas(tema):
    return "/root/ct3d-borradores-ml/abecedarios/" + tema


def destino_tema(tema):
    return os.path.join(_PROY, "temas", tema, "letras")


def ruta(carpeta, letra):
    return os.path.join(carpeta, "%s.png" % ARCHIVO.get(letra, letra))


def generar(tema):
    """Pide a OpenAI las letras que falten. Reanudable: lo que ya está en disco no se
    vuelve a pagar."""
    from ia_kit.client import OpenAIImageClient

    lam = os.path.join(_PROY, "temas", tema, "extras", "banderin.png")
    if not os.path.exists(lam):
        raise SystemExit("no encuentro la lámina: " + lam)
    ref = open(lam, "rb").read()
    carpeta = crudas(tema)
    os.makedirs(carpeta, exist_ok=True)
    cli = OpenAIImageClient(json.load(open(CONFIG))["openai_api_key"], model=MODELO)
    print("modelo: %s · tema: %s" % (MODELO, tema))

    pedidas = fallidas = 0
    for i, letra in enumerate(LETRAS, 1):
        destino = ruta(carpeta, letra)
        if os.path.exists(destino) and os.path.getsize(destino) > 50000:
            continue
        try:
            raw = cli.editar([ref], PROMPT.format(letra=letra), "1024x1024", quality="medium")
            open(destino, "wb").write(raw if isinstance(raw, bytes) else base64.b64decode(raw))
            pedidas += 1
            print("  %2d/%d  %s  ok" % (i, len(LETRAS), letra), flush=True)
        except Exception as e:                       # noqa: BLE001 — una letra rota no corta la tanda
            fallidas += 1
            print("  %2d/%d  %s  FALLÓ: %s" % (i, len(LETRAS), letra, str(e)[:120]), flush=True)
            time.sleep(2)
    print("pedidas: %d · fallidas: %d · en disco: %d de %d"
          % (pedidas, fallidas, sum(os.path.exists(ruta(carpeta, x)) for x in LETRAS), len(LETRAS)))


def limpiar(tema, pasadas=4):
    """Fondo negro -> blanco, rellenando desde las esquinas.

    Repite hasta que ninguna esquina quede oscura: **una sola pasada NO alcanza.** Cuando
    el negro tiene un degradé, el relleno de tolerancia fija se corta a mitad de camino y
    deja un borde que la pasada siguiente sí agarra — pasó con la K y la U de safari, que
    quedaron sucias después de la primera corrida y se dieron por limpias."""
    import cv2
    import numpy as np

    def esquinas_oscuras(img):
        h, w = img.shape[:2]
        return [(x, y) for (x, y) in ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2))
                if img[y, x].mean() < 90]

    afectadas, sucias = [], []
    for f in sorted(glob.glob(os.path.join(crudas(tema), "*.png"))):
        img = cv2.imread(f)
        if img is None or not esquinas_oscuras(img):
            continue
        h, w = img.shape[:2]
        for _ in range(pasadas):
            puntos = esquinas_oscuras(img)
            if not puntos:
                break
            mask = np.zeros((h + 2, w + 2), np.uint8)
            for p in puntos:
                cv2.floodFill(img, mask, p, (255, 255, 255),
                              (45, 45, 45), (45, 45, 45), cv2.FLOODFILL_FIXED_RANGE)
        cv2.imwrite(f, img)
        afectadas.append(os.path.basename(f))
        if esquinas_oscuras(img):
            sucias.append(os.path.basename(f))
    print("%d con fondo oscuro, blanqueadas: %s" % (len(afectadas), ", ".join(afectadas)))
    if sucias:
        print("  QUEDARON SUCIAS (mirar a mano): %s" % ", ".join(sucias))


def revisar(tema, salida=None):
    """Grilla con todas las letras y, abajo de cada una, la que DEBERÍA decir."""
    from PIL import Image, ImageDraw, ImageFont

    salida = salida or "/tmp/abecedario_%s.png" % tema
    inverso = {v: k for k, v in ARCHIVO.items()}
    archivos = sorted(glob.glob(os.path.join(crudas(tema), "*.png")))
    if not archivos:
        raise SystemExit("no hay letras en " + crudas(tema))
    cols, celda, pie = 8, 230, 34
    filas = (len(archivos) + cols - 1) // cols
    hoja = Image.new("RGB", (cols * celda, filas * (celda + pie)), "white")
    d = ImageDraw.Draw(hoja)
    try:
        fuente = ImageFont.truetype(os.path.join(_PROY, "fonts", "Poppins-Medium.ttf"), 22)
    except OSError:
        fuente = ImageFont.load_default()
    for i, f in enumerate(archivos):
        r, c = divmod(i, cols)
        im = Image.open(f).convert("RGB")
        im.thumbnail((celda - 12, celda - 12), Image.LANCZOS)
        hoja.paste(im, (c * celda + (celda - im.width) // 2,
                        r * (celda + pie) + (celda - im.height) // 2))
        base = os.path.splitext(os.path.basename(f))[0]
        d.text((c * celda + celda // 2, r * (celda + pie) + celda + 6),
               "debe decir  " + inverso.get(base, base), fill=(20, 20, 20), font=fuente, anchor="ma")
    hoja.save(salida)
    print("%d letras -> %s   MIRALAS antes de instalar" % (len(archivos), salida))


def instalar(tema):
    """Optimiza (paleta de 192 colores: 60 % menos peso, sin diferencia visible) y copia
    a temas/<tema>/letras/, que es de donde las lee el motor."""
    from PIL import Image

    destino = destino_tema(tema)
    os.makedirs(destino, exist_ok=True)
    total = n = 0
    for f in sorted(glob.glob(os.path.join(crudas(tema), "*.png"))):
        d = os.path.join(destino, os.path.basename(f))
        Image.open(f).convert("RGB").quantize(colors=192, method=Image.MEDIANCUT).save(d, optimize=True)
        total += os.path.getsize(d)
        n += 1
    faltan = [x for x in LETRAS if not os.path.exists(ruta(destino, x))]
    print("%d letras instaladas en %s · %.1f MB" % (n, destino, total / 1024 / 1024))
    if faltan:
        print("  OJO, faltan %d: %s — con una que falte, la guirnalda entera sale con el "
              "método dibujado" % (len(faltan), " ".join(faltan)))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    acciones = {"generar": generar, "limpiar": limpiar, "revisar": revisar, "instalar": instalar}
    accion = acciones.get(sys.argv[1])
    if not accion:
        raise SystemExit("acción desconocida: %s (hay: %s)" % (sys.argv[1], ", ".join(acciones)))
    accion(sys.argv[2])
