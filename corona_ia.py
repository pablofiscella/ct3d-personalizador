"""Arte IA de gorro/corona: un fondo temático (patrón/personajes del tema) generado
UNA vez por tema con OpenAI, igual que calendario (fondo.png) y libro (ilustración):
la IA solo aporta el arte de fondo — el nombre/edad SIEMPRE los escribe el motor
encima, nunca quedan "horneados" en la imagen (evita el bug que tuvo calendario,
donde un override ya renderizado tapaba la personalización de cada cliente)."""
import io
import os

from PIL import Image

import libro_ia

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")

_PIEZAS = ("gorro", "corona")


def fondo_path(tema, pieza):
    if pieza not in _PIEZAS:
        raise ValueError("pieza inválida: %r" % pieza)
    return os.path.join(TEMAS, tema, "overrides", "corona", "fondo_%s.png" % pieza)


def cargar_fondo(tema, pieza):
    p = fondo_path(tema, pieza)
    return Image.open(p).convert("RGBA") if os.path.isfile(p) else None


def _prompt(tema, pieza):
    nombre_tema = tema.replace("-", " ")
    if pieza == "gorro":
        forma = ("un sector circular (como una porción de torta vista desde arriba, "
                 "con el vértice angosto arriba y el borde curvo ancho abajo) que al "
                 "enrollarse forma un gorro cónico de cumpleaños para armar")
    else:
        forma = ("una franja horizontal ancha, decorada de punta a punta, pensada para "
                 "recortar y armar como una corona de cumpleaños desplegada y aplanada")
    return (
        "Ilustración infantil para imprimir y recortar, temática '%s'. Diseño de fondo/"
        "patrón decorativo para un %s de cumpleaños: %s. Mismo estilo, colores y "
        "personajes que la imagen de referencia. Que llene TODO el encuadre (sin "
        "márgenes en blanco). SIN NINGÚN TEXTO, LETRA, NÚMERO NI PALABRA en la imagen — "
        "el nombre del cumpleañero se agrega después, aparte. Que tenga zonas con buen "
        "contraste (no todo claro) para que un texto blanco se lea bien encima."
        % (nombre_tema, pieza, forma)
    )


def generar(client, tema, pieza, calidad="medium"):
    """Genera y cachea el fondo de 'gorro' o 'corona' para un tema. Devuelve el path.
    `client` es ia_kit.client.OpenAIImageClient (o cualquier objeto con
    .editar(refs, prompt, size, quality=) -> bytes PNG)."""
    refs = libro_ia.referencias(tema)
    if not refs:
        raise RuntimeError(
            "el tema %r no tiene imagen de referencia (ia_maestra.png/stickers) "
            "— agregala antes de generar el gorro/corona" % tema)
    raw = client.editar(refs, _prompt(tema, pieza), "1024x1536", quality=calidad)
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    dest = fondo_path(tema, pieza)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    img.save(dest)
    return dest
