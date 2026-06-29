"""Catálogo de piezas, paleta del tema y construcción de prompts."""
import json
import os
from collections import namedtuple

Pieza = namedtuple("Pieza", "key size por_edad recorte sujeto")

_PORTRAIT = "1536x2176"   # A4-ish vertical
_SQUARE = "1024x1024"

# key, size, por_edad, recorte, sujeto (la línea variable del prompt)
PIEZAS = [
    Pieza("invitacion", _PORTRAIT, True,  False, "una invitación de cumpleaños vertical"),
    Pieza("afiche", _PORTRAIT, True,  False, "un cartel/afiche vertical de bienvenida"),
    Pieza("topper", _SQUARE, False, True,  "un topper de torta circular con el personaje"),
    Pieza("stickers", _SQUARE, False, True,  "una plancha de stickers variados del personaje"),
    Pieza("separadores", _PORTRAIT, False, True,  "separadores/marcalibros verticales"),
    Pieza("etiqueta_botella", _SQUARE, False, False,  "una etiqueta rectangular para botellita, diseño completo que llena todo el rectángulo"),
    Pieza("cajita_sorpresa", _SQUARE, False, True,  "el desplegable de una cajita sorpresa"),
    Pieza("decoracion_sorbetes", _SQUARE, False, True,  "banderitas decorativas para sorbetes"),
    Pieza("banderin", _SQUARE, False, True,  "un banderín triangular decorativo"),
    Pieza("etiquetas_multiuso", _SQUARE, False, True,  "una plancha de etiquetas circulares multiuso"),
    Pieza("wrappers_cupcakes", _SQUARE, False, False,  "una plancha de wrappers (envoltorios) para cupcakes, diseño completo que llena el rectángulo"),
    Pieza("tarjetas_agradecimiento", _PORTRAIT, False, False,  "una tarjeta de agradecimiento vertical, diseño completo que llena todo el rectángulo"),
]

# Contrato de nombres con productos.py::_piezas_kit (NO cambiar productos.py).
# Estas 7 piezas se leen como extras/<base>_<edad>.png (con fallback a <base>_1.png).
EXTRAS_POR_EDAD = ["afiche", "topper", "stickers", "separadores",
                   "etiqueta_botella", "cajita_sorpresa", "decoracion_sorbetes"]
# Estas 4 se leen como extras/<base>.png (sin edad).
EXTRAS_UNIVERSAL = ["banderin", "etiquetas_multiuso", "wrappers_cupcakes",
                    "tarjetas_agradecimiento"]
# (invitacion no está en ninguna: es el slot raíz temas/<tema>/invitacion_<edad>.png)

# Piezas por-edad que se generan SOLO en la 1ª edad y luego se REPLICAN al resto cambiando
# el número (para que las edades queden consistentes en vez de generarse por separado).
REPLICABLE = {"afiche"}

_DEF = {"accent": "#E0514A", "ink": "#4A4A4A", "font": "Baloo2-VF.ttf"}


def paleta_de(temas_dir, tema):
    try:
        cfg = json.load(open(os.path.join(temas_dir, tema, "tema.json"), encoding="utf-8"))
    except Exception:
        cfg = {}
    kit = cfg.get("kit", {})
    return {k: kit.get(k, _DEF[k]) for k in _DEF}


def bloque_estilo(paleta):
    # Estilo común. OJO: el espacio para texto NO va acá — solo las piezas con texto
    # (invitación/afiche) lo piden; las decorativas deben ir centradas y llenas.
    return (
        "Estilo: ilustración infantil flat vector, líneas limpias, colores planos. "
        "Paleta principal acento %s, tinta/contornos %s. "
        "Usá EXACTAMENTE los personajes de las imágenes de referencia, sin cambiar su diseño. "
        "Importante: NO escribas ningún texto, número ni letra en la imagen (no text, no letters)."
        % (paleta["accent"], paleta["ink"])
    )


# Indicaciones de forma/encuadre por pieza (piezas circulares: centrar y llenar el círculo).
_EXTRA_FORMA = {
    "topper": ("Es CIRCULAR: un único círculo; poné el personaje/escena CENTRADO y que LLENE "
               "bien el círculo (sin dejar el centro vacío), sin que nada se salga del borde."),
    "etiquetas_multiuso": ("Es una PLANCHA de varias etiquetas circulares en grilla; en CADA "
                           "círculo poné UN personaje CENTRADO que LLENE bien la etiqueta "
                           "(no en un costado, no con el centro vacío), sin salirse del borde."),
    "wrappers_cupcakes": ("2 o 3 wrappers de cupcake (forma de arco/abanico) apilados, TODOS "
                          "COMPLETOS y enteros DENTRO del cuadro, con MARGEN en todos los bordes; "
                          "que ninguno se corte arriba ni abajo (mejor menos cantidad y enteros)."),
    "cajita_sorpresa": ("Plantilla DESPLEGABLE (troquel plano) de una cajita que se arma y "
                        "CIERRA: tiene que tener LAS 6 CARAS conectadas (base, las 4 paredes y "
                        "la TAPA) más las lengüetas/solapas para pegar y cerrar; líneas de "
                        "doblez punteadas. Vista plana de frente, decoración temática en las caras."),
    "stickers": ("Pocos stickers del personaje MUY SEPARADOS entre sí, con MUCHO espacio en "
                 "blanco entre cada uno (al menos medio sticker de distancia): que NO se toquen "
                 "ni queden cerca, porque al recortarlos con borde se pegarían. Cada figura "
                 "COMPACTA y maciza, SIN huecos internos ni elementos flotando con espacios en "
                 "el medio (nada de aros/arcos abiertos). Sobre fondo BLANCO liso."),
}


# Texto personalizado en extras: EN PAUSA. Se hará con un editor (posición/tamaño/nombre)
# en vez de auto-posicionar. Por ahora vacío -> esas piezas quedan decorativas.
_CON_TEXTO = set()

_ZONA_LIMPIA = ("SIEMPRE dejá un ÁREA CENTRAL amplia, limpia y despejada (sin dibujos ni texto) "
                "para el texto que se agrega después; la decoración temática va SOLO alrededor.")


def prompt_de(paleta, pieza, edad=None):
    partes = ["Creá %s para un kit de cumpleaños." % pieza.sujeto]
    if pieza.key == "invitacion":
        # Se personaliza en el editor (nombre/fecha/EDAD se agregan después).
        partes.append(
            "Es una invitación que se personaliza después en un editor: NO incluyas el número "
            "de edad ni ningún texto. Dejá un ÁREA CENTRAL amplia, limpia y despejada para el "
            "texto (nombre, fecha y edad se agregan luego); poné solo la decoración temática "
            "alrededor (marco/escena con los personajes).")
    elif pieza.key == "afiche":
        # Cartel: número grande ilustrado (protagonista) + recuadro limpio ABAJO para el nombre.
        n = (" El número %d es el PROTAGONISTA: GRANDE e ilustrado de forma temática." % int(edad)) if edad is not None else ""
        partes.append("Cartel de bienvenida." + n +
                      " SIEMPRE dejá ABAJO un recuadro/cartel rectangular limpio y despejado "
                      "(tipo etiqueta, sin dibujos ni texto adentro) para el nombre que se "
                      "agrega después.")
    elif pieza.key in _CON_TEXTO:
        partes.append(_ZONA_LIMPIA)
    elif pieza.key in _EXTRA_FORMA:
        # piezas con forma/encuadre específico (circulares, stickers, etc.)
        partes.append(_EXTRA_FORMA[pieza.key])
    else:
        # piezas decorativas sin texto -> composición centrada y llena.
        partes.append("Composición CENTRADA y equilibrada que aproveche bien el espacio, "
                      "sin grandes zonas vacías.")
    partes.append(bloque_estilo(paleta))
    return " ".join(partes)
