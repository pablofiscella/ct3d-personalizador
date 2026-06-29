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
    Pieza("etiqueta_botella", _SQUARE, False, True,  "una etiqueta rectangular para botellita"),
    Pieza("cajita_sorpresa", _SQUARE, False, True,  "el desplegable de una cajita sorpresa"),
    Pieza("decoracion_sorbetes", _SQUARE, False, True,  "banderitas decorativas para sorbetes"),
    Pieza("banderin", _SQUARE, False, True,  "un banderín triangular decorativo"),
    Pieza("etiquetas_multiuso", _SQUARE, False, True,  "una plancha de etiquetas circulares multiuso"),
    Pieza("wrappers_cupcakes", _SQUARE, False, True,  "wrappers (envoltorios) para cupcakes"),
    Pieza("tarjetas_agradecimiento", _PORTRAIT, False, True,  "una tarjeta de agradecimiento vertical"),
]

# Contrato de nombres con productos.py::_piezas_kit (NO cambiar productos.py).
# Estas 7 piezas se leen como extras/<base>_<edad>.png (con fallback a <base>_1.png).
EXTRAS_POR_EDAD = ["afiche", "topper", "stickers", "separadores",
                   "etiqueta_botella", "cajita_sorpresa", "decoracion_sorbetes"]
# Estas 4 se leen como extras/<base>.png (sin edad).
EXTRAS_UNIVERSAL = ["banderin", "etiquetas_multiuso", "wrappers_cupcakes",
                    "tarjetas_agradecimiento"]
# (invitacion no está en ninguna: es el slot raíz temas/<tema>/invitacion_<edad>.png)

_DEF = {"accent": "#E0514A", "ink": "#4A4A4A", "font": "Baloo2-VF.ttf"}


def paleta_de(temas_dir, tema):
    try:
        cfg = json.load(open(os.path.join(temas_dir, tema, "tema.json"), encoding="utf-8"))
    except Exception:
        cfg = {}
    kit = cfg.get("kit", {})
    return {k: kit.get(k, _DEF[k]) for k in _DEF}


def bloque_estilo(paleta):
    return (
        "Estilo: ilustración infantil flat vector, líneas limpias, colores planos. "
        "Paleta principal acento %s, tinta/contornos %s. "
        "Usá EXACTAMENTE los personajes de las imágenes de referencia, sin cambiar su diseño. "
        "Importante: NO escribas ningún texto, número ni letra en la imagen "
        "(no text, no letters); dejá zonas limpias y vacías donde luego se coloca el texto."
        % (paleta["accent"], paleta["ink"])
    )


# Indicaciones de forma/encuadre por pieza (piezas circulares: contener y centrar).
_EXTRA_FORMA = {
    "topper": ("Forma CIRCULAR: encuadrá TODO el diseño dentro de un círculo centrado; "
               "los personajes y la decoración van CONTENIDOS adentro del borde (que nada "
               "se salga del círculo), bien centrados y con margen al borde."),
    "etiquetas_multiuso": ("Etiqueta CIRCULAR: el motivo centrado y completamente CONTENIDO "
                           "dentro de un círculo, sin que ningún elemento cruce el borde."),
}


def prompt_de(paleta, pieza, edad=None):
    partes = ["Creá %s para un kit de cumpleaños." % pieza.sujeto]
    if pieza.por_edad and edad is not None:
        partes.append(
            "El número %d es el PROTAGONISTA: ubicalo en el CENTRO, MUY GRANDE, ilustrado de "
            "forma temática (decorado/formado con los elementos y personajes del tema), no "
            "como texto tipográfico simple. Dejá una franja limpia debajo del número para el "
            "texto del nombre." % int(edad))
    if pieza.key in _EXTRA_FORMA:
        partes.append(_EXTRA_FORMA[pieza.key])
    partes.append(bloque_estilo(paleta))
    return " ".join(partes)
