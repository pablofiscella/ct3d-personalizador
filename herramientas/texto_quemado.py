#!/usr/bin/env python3
"""¿Qué arte del kit tiene TEXTO EN ESPAÑOL quemado en los píxeles?

POR QUÉ
───────
19-ago-2026. Se le agregó idioma al motor (`idioma.py`) para poder vender los kits en Etsy,
que cobra en dólares. El motor ya escribe en inglés — pero eso sólo alcanza para el texto que
DIBUJA el motor. Mirando las 15 piezas de monstruos en inglés apareció lo otro: el topper
dice «¡FELIZ CUMPLE!», «TOPPER PARA TORTA» y «TOPPERS PARA CUPCAKES»; la etiqueta de botella
dice «¡FELIZ CUMPLE!»; la cajita dice «CAJITA SORPRESA». **Eso son píxeles del PNG**, no
texto: ninguna tabla de traducción lo toca.

Un comprador de Estados Unidos abriría el kit y encontraría media hoja en español. Antes de
decidir qué hacer hay que saber CUÁNTO hay, y eso es lo que cuenta este script.

CÓMO LEER EL RESULTADO
──────────────────────
Sale un `quemado.json` con, por cada PNG, el texto que se le ve. Es un INVENTARIO, no un
veredicto: lo que diga hay que mirarlo con los ojos antes de tocar un archivo.

LO QUE YA COSTÓ APRENDER Y ESTÁ CONTEMPLADO
───────────────────────────────────────────
- **Se manda la imagen ENTERA.** El verificador del abecedario mandaba sólo la mitad de
  abajo y por eso inventó 7 errores en monstruos: en ese tema la letra cae más arriba.
- **Se lee el CUERPO del error HTTP, no el número.** El «429» de OpenAI de agosto no era
  límite de ritmo: el cuerpo decía «You have no credits remaining».
- **Hay un control.** Se le pasa a propósito un PNG sin texto y otro con texto conocido: si
  el modelo se equivoca en el control, el inventario entero no vale.

    python3 herramientas/texto_quemado.py              # todas las extras de las 12 temáticas
    python3 herramientas/texto_quemado.py --solo monstruos
"""
import base64
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = "/opt/ct3d/backend/config.json"
MODELO = "gpt-4o-mini"
SALIDA = os.path.join(RAIZ, "salida", "quemado.json")

# El prompt insiste en «letras escritas» porque la primera versión pedía «todo el texto que
# veas» y el modelo empezó a NOMBRAR LOS OBJETOS DIBUJADOS: en el afiche de artistas, que no
# tiene una sola letra, contestó «Birthday Party / Happy Birthday», y en los sorbetes
# —pinceles y paletas dibujados— contestó «Palette · Paint · Brush · Canvas». Describir no es
# leer, y confundirlos manda a arreglar archivos que están sanos.
PROMPT = (
    "Look at this image, which is artwork for a printable birthday party kit.\n"
    "Your job is to TRANSCRIBE, not to describe.\n"
    "List every sequence of LETTERS that is actually WRITTEN in the image — real "
    "typography you could point at, letter by letter.\n"
    "Rules:\n"
    "- Do NOT name objects, themes or concepts you see. If you are naming what something "
    "IS rather than reading letters printed on it, do not report it.\n"
    "- If you are not sure the letters are really there, do not report them.\n"
    "- Report the text EXACTLY as written, including accents and punctuation.\n"
    "- Ignore digits alone (like a big '5') and single letters.\n"
    "- If no words are written anywhere, answer exactly: NONE\n"
    "Answer as a plain list, one text per line, nothing else."
)


def _key():
    return json.load(open(CONFIG))["openai_api_key"]


def _mirar(ruta, key):
    b64 = base64.b64encode(open(ruta, "rb").read()).decode()
    payload = {
        "model": MODELO,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": PROMPT},
            # detail alto: el texto quemado suele ser chico y en "low" se pierde
            {"type": "image_url", "image_url": {
                "url": "data:image/png;base64," + b64, "detail": "high"}},
        ]}],
        "max_tokens": 300,
        "temperature": 0,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            d = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        # el CUERPO, no el número: el «429» de agosto decía «no credits remaining»
        cuerpo = ""
        try:
            cuerpo = e.read().decode("utf-8", "replace")[:400]
        except Exception:
            pass
        raise RuntimeError("HTTP %s — %s" % (e.code, cuerpo)) from None
    txt = (d["choices"][0]["message"]["content"] or "").strip()
    if txt.upper().startswith("NONE"):
        return []
    return [l.strip(" -•\t") for l in txt.splitlines() if l.strip()]


_ES = "áéíóúñ¿¡ÁÉÍÓÚÑ"
_PALABRAS_ES = ("feliz", "cumple", "cumpleaños", "gracias", "venir", "sorpresa", "torta",
                "topper", "banderin", "banderín", "para", "invitación", "invitacion",
                "bienvenidos", "confirmá", "confirmar", "años", "año", "etiqueta",
                "menú", "menu", "recuerdo", "souvenir", "vasos", "sorbetes", "wrapper")


def parece_espanol(t):
    b = t.lower()
    if any(c in t for c in _ES):
        return True
    return any(p in b for p in _PALABRAS_ES)


def main():
    args = sys.argv[1:]
    solo = args[args.index("--solo") + 1] if "--solo" in args else None
    key = _key()

    patron = os.path.join(RAIZ, "temas", solo or "*", "extras", "*.png")
    files = sorted(glob.glob(patron))
    if not files:
        print("no hay extras en %s" % patron)
        return

    # ── control ───────────────────────────────────────────────────────────────
    # Sin esto, un inventario vacío no se distingue de un modelo ciego. Los tres archivos
    # de abajo se MIRARON con los ojos antes de ponerlos acá, y eso importa: la primera
    # versión del control daba por sentado que `cajita_sorpresa_1.png` tenía texto y lo
    # marcó como falla del modelo. El modelo tenía razón — la cajita de 1 año es otro
    # diseño, un cubo estampado sin una sola palabra. Un control armado de memoria acusa
    # al instrumento de un error propio.
    # Las dos mitades del control cuidan errores OPUESTOS, y hacen falta las dos:
    #   · con texto esperado  → que no se le escape lo que sí está (falso negativo);
    #   · sin texto esperado  → que no invente (falso positivo). `afiche_7` de artistas está
    #     acá justamente porque es donde el modelo se cayó: no tiene una letra y contestó
    #     «Birthday Party». `decoracion_sorbetes_1` es la otra trampa: dibujos de paletas y
    #     pinceles que el modelo leyó como las palabras «Palette» y «Brush».
    # Los cuatro archivos se miraron con los ojos antes de ponerlos acá.
    CONTROL = [("temas/monstruos/extras/cajita_sorpresa_2.png", "CAJITA SORPRESA"),
               ("temas/monstruos/extras/topper_5.png", "FELIZ CUMPLE"),
               ("temas/monstruos/extras/cajita_sorpresa_1.png", None),
               ("temas/artistas/extras/afiche_7.png", None),
               ("temas/artistas/extras/decoracion_sorbetes_1.png", None)]
    print("control (mirado con los ojos antes de confiar en el modelo)…")
    fallo = []
    for rel, esperado in CONTROL:
        p = os.path.join(RAIZ, rel)
        if not os.path.exists(p):
            # Un control que se saltea no controla. La primera versión apuntaba a
            # `topper.png`, que no existe —son `topper_1..5`—, y el bucle lo pasaba de
            # largo en silencio: quedaba media prueba menos sin que nada lo dijera.
            fallo.append("%s: el archivo del control no existe" % rel)
            continue
        r = _mirar(p, key)
        visto = " · ".join(r) if r else "NADA"
        print("  %-46s -> %s" % (rel, visto))
        if esperado is None and r:
            fallo.append("%s: vio texto donde no hay" % rel)
        if esperado and esperado.lower() not in visto.lower():
            fallo.append("%s: no vio %r" % (rel, esperado))
    if fallo:
        print("\nEL CONTROL FALLÓ — el inventario no vale, no seguir:\n  "
              + "\n  ".join(fallo))
        return

    print("\n%d imágenes…\n" % len(files))
    res = {}
    for i, f in enumerate(files, 1):
        rel = os.path.relpath(f, RAIZ)
        try:
            textos = _mirar(f, key)
        except Exception as e:                      # noqa: BLE001
            print("%3d/%d  %-46s FALLÓ: %s" % (i, len(files), rel, str(e)[:120]))
            continue
        es = [t for t in textos if parece_espanol(t)]
        res[rel] = {"todo": textos, "espanol": es}
        if es:
            print("%3d/%d  %-46s ESPAÑOL: %s" % (i, len(files), rel, " · ".join(es)))

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    cones = {k: v for k, v in res.items() if v["espanol"]}
    print("\n%d de %d PNG tienen texto en español quemado." % (len(cones), len(res)))
    # Se cuentan TEMÁTICAS DISTINTAS, no archivos. La primera versión hacía `.append()` por
    # archivo y después informaba `len()` como si fueran temáticas: decía «4 temáticas»
    # cuando eran 4 variantes de edad de UNA sola. Un resumen que exagera el alcance manda
    # a arreglar donde no hay nada roto.
    porpieza = {}
    for k in cones:
        pieza = re.sub(r"_\d+$", "", os.path.basename(k).replace(".png", ""))
        porpieza.setdefault(pieza, {}).setdefault(k.split(os.sep)[1], []).append(k)
    for p, portema in sorted(porpieza.items(), key=lambda x: -len(x[1])):
        archivos = sum(len(v) for v in portema.values())
        print("  %-24s %d archivo(s) en %d temática(s): %s"
              % (p, archivos, len(portema), ", ".join(sorted(portema))))
    print("\ndetalle: %s" % SALIDA)


if __name__ == "__main__":
    main()
