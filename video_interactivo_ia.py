"""video_interactivo_ia.py — imágenes y voz de un VIDEO INTERACTIVO (piloto, 15-sep-2026).

Pablo: *"hacer un video interactivo. El video se pausa y hace una pregunta. El chico responde y si
no contesta bien le puede dar una pista. O seleccionar objetos según lo que le diga el video"*.

Todo sale de `videos_interactivos/<pieza>/guion.json`: los textos de la voz, las imágenes y los
pasos. Este script genera lo que falta y NO rehace lo que ya está (se paga una vez):

    python3 video_interactivo_ia.py <pieza> imagenes [clave ...]
    python3 video_interactivo_ia.py <pieza> voces    [clave ...]
    python3 video_interactivo_ia.py <pieza> revisar          # transcribe cada voz y la compara

POR QUÉ LOS ANIMALES VAN SUELTOS Y NO DIBUJADOS EN LA ESCENA
───────────────────────────────────────────────────────────
Lo que el chico toca tiene que ser EXACTAMENTE lo que ve. Si el pez viniera pintado en el fondo,
habría que adivinar dónde quedó; suelto, su caja ES la zona tocable, y además puede nadar. Es la
regla del video de Kydo: el fondo se pide SIN el elemento y el elemento va sobre verde puro,
porque gpt-image no hace fondos transparentes.

LA REFERENCIA DE ESTILO ES LA TAPA DEL GRADO de Kydo: el piloto tiene que parecer del cuaderno,
no un video de otro lado.
"""
import io
import json
import os
import re
import sys
import unicodedata

import numpy as np
from PIL import Image

KIT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(KIT, "videos_interactivos")
REF_ESTILO = "/opt/ct3d/backend/tienda_static/img/grados/%d.webp"

ESTILO = ("Ilustración infantil con el MISMO estilo de dibujo de la imagen de referencia: dibujo "
          "cálido y amigable, colores ricos, sombreado suave y contornos redondeados. Anatomía "
          "correcta de cada animal. NO copiar a los personajes, carteles ni objetos de la "
          "referencia: sólo su estilo. Sin ningún texto, letra, número ni cartel en la imagen.")
VERDE = ("Fondo VERDE PURO y liso (#00FF00) en toda la imagen, sin suelo, sin sombra y sin nada "
         "más alrededor. El dibujo mismo NO tiene nada verde. El elemento completo, centrado y "
         "con margen, sin tocar los bordes.")


def carpeta(pieza):
    return os.path.join(BASE, pieza)


def guion(pieza):
    with open(os.path.join(carpeta(pieza), "guion.json"), encoding="utf-8") as f:
        return json.load(f)


def _ref_png(ruta):
    buf = io.BytesIO()
    Image.open(ruta).convert("RGB").save(buf, "PNG")
    return buf.getvalue()


def recortar_verde(raw):
    """PNG sobre verde → RGBA recortado al dibujo. Mismo criterio que el colorkey del montaje."""
    im = np.asarray(Image.open(io.BytesIO(raw)).convert("RGB")).astype(int)
    dist = np.abs(im - np.array([0, 255, 0])).sum(axis=2)
    alfa = np.clip((dist - 90) * 255 // 140, 0, 255).astype(np.uint8)   # borde suave
    # el verde que se cuela en el borde del dibujo se neutraliza para que no quede halo
    rgb = im.copy()
    verdoso = (rgb[..., 1] > rgb[..., 0] + 40) & (rgb[..., 1] > rgb[..., 2] + 40) & (alfa < 255)
    rgb[verdoso, 1] = np.maximum(rgb[verdoso, 0], rgb[verdoso, 2])
    rgba = np.dstack([rgb.astype(np.uint8), alfa])
    ys, xs = np.where(alfa > 24)
    if not len(xs):
        raise ValueError("no quedó dibujo después de sacar el verde")
    return Image.fromarray(rgba, "RGBA").crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def generar_imagenes(pieza, claves=None, calidad="medium"):
    import servicio  # carga OPENAI_API_KEY de env o config.json
    client = servicio._openai_client()
    if not client:
        raise SystemExit("falta OPENAI_API_KEY")
    g = guion(pieza)
    ref = _ref_png(REF_ESTILO % g.get("grado", 2))
    dest_dir = carpeta(pieza)
    hechas = []
    personaje = None
    ruta_personaje = os.path.join(dest_dir, "carpi_hablando.webp")
    if os.path.exists(ruta_personaje):
        personaje = _ref_png(ruta_personaje)
    for clave, spec in g["imagenes"].items():
        if claves and clave not in claves:
            continue
        dest = os.path.join(dest_dir, clave + ".webp")
        if os.path.exists(dest) and not claves:
            continue
        if spec["tipo"] == "escena":
            prompt = spec["prompt"] + " " + ESTILO
            raw = client.editar([ref], prompt, spec.get("size", "1536x1024"), quality=calidad)
            Image.open(io.BytesIO(raw)).convert("RGB").save(dest, "WEBP", quality=86)
        else:
            refs = [ref] + ([personaje] if spec.get("personaje") and personaje
                            and clave != "carpi_hablando" else [])
            prompt = spec["prompt"] + " " + ESTILO + " " + VERDE
            raw = client.editar(refs, prompt, "1024x1024", quality=calidad)
            im = recortar_verde(raw)
            im.thumbnail((640, 640))
            im.save(dest, "WEBP", quality=90)
            if clave == "carpi_hablando":
                personaje = _ref_png(dest)
        hechas.append(dest)
        print("imagen:", os.path.relpath(dest, KIT), flush=True)
    return hechas


def generar_voces(pieza, claves=None):
    import audiolibro
    import actividades_web as aw
    g = guion(pieza)
    hechas = []
    for n, (clave, texto) in enumerate(g["voces"].items()):
        if claves and clave not in claves:
            continue
        dest = os.path.join(carpeta(pieza), "voz_%s.mp3" % clave)
        if os.path.exists(dest) and not claves:
            continue
        # VI_TOMA cambia la semilla: con la misma, ElevenLabs devuelve el mismo audio y
        # «regrabar» una toma dudosa no cambiaría nada.
        toma = int(os.environ.get("VI_TOMA", "0") or 0)
        mp3 = audiolibro._tts_elevenlabs(texto, seed=4242 + n * 137 + toma * 7919,
                                         voice_id=aw.VOZ_ACTIVIDADES)
        if not mp3:
            raise SystemExit("ElevenLabs no devolvió audio para %s" % clave)
        with open(dest, "wb") as f:
            f.write(mp3)
        hechas.append(dest)
        print("voz:", os.path.relpath(dest, KIT), len(mp3), "bytes", flush=True)
    return hechas


def _palabras(texto):
    t = unicodedata.normalize("NFD", texto.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-zñ]+", t)


def revisar_voces(pieza):
    """Transcribe cada voz y la compara con su texto. La voz es la que se va a oír: se verifica
    lo grabado, no el guion. Devuelve la lista de claves con diferencias."""
    import difflib
    import urllib.request
    import audiolibro
    from ia_kit.multipart import build_multipart
    # Se transcribe con ElevenLabs (Scribe) y no con Whisper de OpenAI: el 15-sep-2026 la cuenta
    # de OpenAI se quedó sin crédito a mitad del piloto, y el servidor no tiene Whisper local.
    # Es además la misma cuenta que grabó la voz.
    key = audiolibro._elevenlabs_key()
    if not key:
        raise SystemExit("falta la clave de ElevenLabs")
    g = guion(pieza)
    malas = []
    for clave, texto in g["voces"].items():
        ruta = os.path.join(carpeta(pieza), "voz_%s.mp3" % clave)
        with open(ruta, "rb") as f:
            audio = f.read()
        ct, body = build_multipart({"model_id": "scribe_v1", "language_code": "spa"},
                                   [("file", "voz.mp3", audio)])
        req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body,
                                     method="POST", headers={"xi-api-key": key,
                                                             "Content-Type": ct})
        with urllib.request.urlopen(req, timeout=120) as r:
            oido = json.loads(r.read().decode("utf-8")).get("text", "")
        a, b = _palabras(texto), _palabras(oido)
        dif = [op for op in difflib.SequenceMatcher(None, a, b).get_opcodes() if op[0] != "equal"]
        estado = "OK" if not dif else "REVISAR"
        if dif:
            malas.append(clave)
        print("%-18s %s · oído: %s" % (clave, estado, oido), flush=True)
    return malas


if __name__ == "__main__":
    pieza, que = sys.argv[1], sys.argv[2]
    claves = sys.argv[3:] or None
    if que == "imagenes":
        generar_imagenes(pieza, claves)
    elif que == "voces":
        generar_voces(pieza, claves)
    elif que == "revisar":
        sys.exit(1 if revisar_voces(pieza) else 0)
    else:
        raise SystemExit("uso: video_interactivo_ia.py <pieza> imagenes|voces|revisar [clave ...]")
