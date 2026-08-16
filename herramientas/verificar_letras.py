#!/usr/bin/env python3
"""Lee cada banderín generado y dice qué letra tiene — para cazar las que salieron mal.

El modelo de imágenes devuelve cada tanto la lámina **sin la letra** (2 de 11 en la
primera tanda de las «A») y, más raro, con **otra** letra. Ningún conteo de archivos lo
detecta: el archivo está, pesa lo mismo y se abre bien. Con 32 letras por tema y 11 temas,
mirarlas de a una no escala.

**No se le dice al modelo qué letra esperamos.** Se le pregunta qué ve y recién después se
compara. Preguntar «¿dice A?» invita a que conteste que sí: es el mismo error que cometió
el control de voz con Whisper, que autocorregía por contexto y daba 100 % sobre un audio
que estaba mal.

    python3 herramientas/verificar_letras.py <tema>
    python3 herramientas/verificar_letras.py --control    # el instrumento contra casos conocidos

El control usa safari, cuyas 32 letras están revisadas a ojo una por una: el verificador
tiene que acertarlas todas, y tiene que decir NINGUNA sobre la lámina pelada. Un
verificador que no pasa su propio control no se usa.
"""
import base64
import glob
import io
import json
import os
import sys
import urllib.request

from PIL import Image

_PROY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = "/opt/ct3d/backend/config.json"
MODELO = os.environ.get("MODELO_VISION", "gpt-4o-mini")
URL = "https://api.openai.com/v1/chat/completions"

ARCHIVO = {"ENIE": "Ñ", "A_TILDE": "Á", "E_TILDE": "É", "I_TILDE": "Í",
           "O_TILDE": "Ó", "U_TILDE": "Ú"}

PREGUNTA = (
    "This is a party pennant flag. Look at it and tell me which single capital letter is "
    "printed on it, if any.\n"
    "Answer with ONLY the letter (for example: A). If the letter has an accent, include it "
    "(Á, É, Í, Ó, Ú, Ñ). If there is no letter printed on the pennant, answer exactly: NONE.\n"
    "Do not explain. One token."
)


def _recorte(path, lado=420):
    """Sólo la mitad inferior, que es donde va la letra: menos tokens y menos ruido."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * 0.10), int(h * 0.40), int(w * 0.90), h))
    im.thumbnail((lado, lado), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80)
    return base64.b64encode(buf.getvalue()).decode()


def leer_letra(path, key):
    cuerpo = json.dumps({
        "model": MODELO,
        "max_tokens": 5,
        "temperature": 0,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": PREGUNTA},
            {"type": "image_url",
             "image_url": {"url": "data:image/jpeg;base64," + _recorte(path), "detail": "low"}},
        ]}],
    }).encode()
    req = urllib.request.Request(URL, data=cuerpo, method="POST", headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode())
    return (d["choices"][0]["message"]["content"] or "").strip().upper().strip(".")


def esperada(archivo):
    base = os.path.splitext(os.path.basename(archivo))[0]
    return ARCHIVO.get(base, base)


def analizar(tema, carpeta=None):
    key = json.load(open(CONFIG))["openai_api_key"]
    carpeta = carpeta or "/root/ct3d-borradores-ml/abecedarios/" + tema
    filas = []
    for f in sorted(glob.glob(os.path.join(carpeta, "*.png"))):
        try:
            visto = leer_letra(f, key)
        except Exception as e:                        # noqa: BLE001 — una lectura rota no corta la tanda
            visto = "ERROR:" + str(e)[:40]
        quiero = esperada(f)
        filas.append((os.path.basename(f), quiero, visto, visto == quiero))
    return filas


def control():
    key = json.load(open(CONFIG))["openai_api_key"]
    ok = True

    lam = os.path.join(_PROY, "temas", "safari", "extras", "banderin.png")
    visto = leer_letra(lam, key)
    print("lámina pelada de safari (no tiene letra) -> el verificador lee: %r" % visto)
    if visto not in ("NONE", "NINGUNA", ""):
        print("  FALSO POSITIVO: le ve una letra a un banderín sin letra")
        ok = False

    filas = analizar("safari")
    fallan = [(f, q, v) for f, q, v, bien in filas if not bien]
    print("safari: %d letras revisadas a ojo · el verificador acierta %d"
          % (len(filas), len(filas) - len(fallan)))
    for f, q, v in fallan:
        print("   %s: esperaba %s, leyó %r" % (f, q, v))
    if len(fallan) > 1:            # una discrepancia puede ser una letra fea de verdad
        ok = False
    print("CONTROL:", "OK" if ok else "NO SIRVE")
    return ok


def main():
    if "--control" in sys.argv:
        raise SystemExit(0 if control() else 1)
    tema = sys.argv[1]
    filas = analizar(tema)
    mal = [(f, q, v) for f, q, v, bien in filas if not bien]
    print("%s: %d letras · %d mal" % (tema, len(filas), len(mal)))
    for f, q, v in mal:
        print("   %s: esperaba %s, se lee %r" % (f, q, v))


if __name__ == "__main__":
    main()
