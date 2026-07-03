"""Ilustraciones IA del libro de cuento — genera con OpenAI (gpt-image-2) el arte de
las 10 páginas y lo guarda como override de escena (libro.override_escena_path), el
MISMO lugar donde caen las imágenes subidas a mano por el dash. Así los dos caminos
(generar con API / subir la tuya) son intercambiables página por página.

Se genera UNA VEZ por temática (el arte no lleva texto: nombre y dedicatoria los
escribe el motor sobre cada venta). Estilo consistente: usa como referencia la
ia_maestra del tema (o la hoja de stickers); si el tema no tiene nada, manda la
página procedural como boceto para redibujar.

Uso:
  - Dash: botón «Generar ilustraciones con IA» en la galería del producto libro
    (POST /dash/libro-ia?tema=X[&pieza=N]).
  - CLI:  OPENAI_API_KEY=... python libro_ia.py <tema> [pagina]
"""
import io
import os
import sys

from PIL import Image

import libro

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")

_CUADRADA = "1024x1024"
_VERTICAL = "1024x1536"

# Qué ilustrar en cada página (0..9). El protagonista va "de espaldas / a lo lejos"
# para que funcione con cualquier chico (la cara nunca se ve).
_ESCENAS = [
    "Portada: una escena vistosa y alegre de {mundo}, con los personajes del tema "
    "celebrando. Composición con AIRE en el tercio superior (ahí va el título después).",
    "Viñeta tierna y suave de un personaje del tema saludando, estilo página de "
    "dedicatoria, fondo muy claro y despejado.",
    "Un dormitorio infantil de noche, acogedor: una cama con almohada y un sobre "
    "dorado brillante que asoma bajo la almohada, luz de luna por la ventana.",
    "Un remolino mágico de luces de colores llenando un dormitorio de noche, "
    "destellos y estrellas, sensación de comienzo de viaje.",
    "Una gran fiesta de bienvenida en {mundo}: banderines, globos y una torta, con "
    "los personajes del tema festejando alrededor de un niño visto de espaldas.",
    "Momento de preocupación en {mundo}: {desafio}. Los personajes del tema miran "
    "preocupados, cielo con una gran nube gris.",
    "Momento heroico: un niño visto de espaldas o de lejos que {solucion}, mientras "
    "los personajes del tema lo alientan felices.",
    "Los personajes del tema regalan {tesoro}, presentado brillante y destacado en "
    "el centro de la escena, con destellos dorados.",
    "Una casita de noche con una ventana iluminada cálida, cielo estrellado con "
    "luna, los personajes del tema despidiéndose a lo lejos.",
    "Cielo nocturno estrellado sereno con los personajes del tema despidiéndose, "
    "composición VERTICAL con mucho AIRE despejado en el centro (ahí va la palabra "
    "FIN después).",
]


def _paleta(tema):
    import json
    try:
        k = json.load(open(os.path.join(TEMAS, tema, "tema.json"))).get("kit") or {}
    except Exception:
        k = {}
    return {"accent": k.get("accent") or "#6B5BD2", "ink": k.get("ink") or "#4a4a4a"}


def tam_pagina(idx):
    """La página FIN es a hoja completa (vertical); el resto son paneles ~cuadrados."""
    return _VERTICAL if idx == libro.TOTAL_PAGINAS - 1 else _CUADRADA


def prompt_pagina(tema, idx):
    """Prompt de la ilustración de la página idx, con la ambientación de la historia
    del tema (libro.HISTORIAS) y el mismo bloque de estilo del resto del kit."""
    h = libro.HISTORIAS.get(tema, libro.HISTORIA_DEFAULT)
    pal = _paleta(tema)
    escena = _ESCENAS[idx].format(**h)
    return (
        "Ilustración para la página de un libro de cuentos infantil profesional. "
        "Escena: %s "
        "Estilo: ilustración infantil cálida, formas suaves y redondeadas, colores "
        "planos con paleta acento %s y tinta %s. "
        "Usá los personajes de las imágenes de referencia manteniendo su diseño. "
        "La escena llena TODA la imagen, sin marcos, bordes ni viñetas. "
        "Importante: NO escribas ningún texto, número ni letra (no text, no letters)."
        % (escena, pal["accent"], pal["ink"])
    )


def referencias(tema):
    """Imágenes de referencia de estilo/personajes del tema (bytes). Prioridad:
    ia_maestra (el look aprobado del kit IA) > hoja de stickers. Vacía si no hay."""
    for rel in ("ia_maestra.png", os.path.join("ia_draft", "stickers_1.png"),
                os.path.join("extras", "stickers_1.png")):
        p = os.path.join(TEMAS, tema, rel)
        if os.path.isfile(p):
            return [open(p, "rb").read()]
    return []


def _boceto(tema, idx):
    """Sin referencias del tema: la página procedural achicada sirve de boceto —
    la IA la redibuja conservando la composición (la escena ya cuenta la historia)."""
    pg = libro.pagina_libro(idx, {"nombre": "", "edad": "", "dedicatoria": ""}, tema)
    pg.thumbnail((1024, 1024), Image.LANCZOS)
    buf = io.BytesIO()
    pg.convert("RGB").save(buf, "PNG")
    return buf.getvalue()


def generar_ilustraciones(client, tema, paginas=None, calidad="medium", progress=None):
    """Genera y guarda las ilustraciones de `paginas` (default: las 10). Devuelve la
    lista de paths escritos. `client` es ia_kit.client.OpenAIImageClient (o cualquier
    objeto con .editar(refs, prompt, size, quality=) -> bytes PNG)."""
    paginas = list(paginas) if paginas is not None else list(range(libro.TOTAL_PAGINAS))
    refs = referencias(tema)
    out = []
    for n, idx in enumerate(paginas):
        if progress:
            progress("Página %d de %d (pieza %d)…" % (n + 1, len(paginas), idx))
        r = refs or [_boceto(tema, idx)]
        prompt = prompt_pagina(tema, idx)
        if not refs:
            prompt = ("Redibujá este boceto como ilustración profesional, conservando "
                      "la composición. " + prompt)
        raw = client.editar(r, prompt, tam_pagina(idx), quality=calidad)
        img = Image.open(io.BytesIO(raw)).convert("RGBA")   # valida que sea imagen
        dest = libro.override_escena_path(tema, idx)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        img.save(dest)
        out.append(dest)
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: OPENAI_API_KEY=... python libro_ia.py <tema> [pagina 0-9]")
        sys.exit(1)
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("Falta OPENAI_API_KEY en el entorno.")
        sys.exit(1)
    from ia_kit.client import OpenAIImageClient
    tema = sys.argv[1]
    paginas = [int(sys.argv[2])] if len(sys.argv) > 2 else None
    cl = OpenAIImageClient(key, model=os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2"))
    paths = generar_ilustraciones(cl, tema, paginas, progress=print)
    print("OK — %d ilustraciones:" % len(paths))
    for p in paths:
        print(" ", p)
