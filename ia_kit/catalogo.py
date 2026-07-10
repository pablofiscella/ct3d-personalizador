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
    Pieza("topper", _SQUARE, False, True,  "un topper de torta circular: disco decorado para apoyar SOBRE la torta"),
    Pieza("topper_palito", _SQUARE, False, True,  "un cake topper para clavar con palito en la torta"),
    Pieza("base_torta", _SQUARE, False, True,  "una base/mat circular GRANDE decorada que va DEBAJO de la torta"),
    Pieza("stickers", _SQUARE, False, True,  "una plancha de stickers variados del personaje"),
    Pieza("separadores", _PORTRAIT, False, False, "una lámina con varios separadores/marcalibros verticales en hilera, cada uno con FONDO de color y diseño temático que LLENA su tira de punta a punta (nada de fondo transparente ni zonas vacías)"),
    Pieza("etiqueta_botella", _SQUARE, False, False,  "una etiqueta rectangular para botellita, diseño completo que llena todo el rectángulo"),
    Pieza("cajita_sorpresa", _SQUARE, False, False, "una ilustración decorativa para las caras de una cajita sorpresa"),
    Pieza("decoracion_sorbetes", _SQUARE, False, True,  "banderitas decorativas para sorbetes"),
    Pieza("banderin", _SQUARE, False, True,  "un banderín triangular decorativo"),
    Pieza("etiquetas_multiuso", _SQUARE, False, False, "una plancha de etiquetas circulares multiuso"),
    Pieza("wrappers_cupcakes", _SQUARE, False, False,  "una plancha de wrappers (envoltorios) para cupcakes, diseño completo que llena el rectángulo"),
    Pieza("tarjetas_agradecimiento", _PORTRAIT, False, False,  "una tarjeta de agradecimiento vertical, diseño completo que llena todo el rectángulo"),
    Pieza("colorear", _SQUARE, False, False, "una página para colorear (line art)"),
]

# Contrato de nombres con productos.py::_piezas_kit (NO cambiar productos.py).
# Estas 7 piezas se leen como extras/<base>_<edad>.png (con fallback a <base>_1.png).
EXTRAS_POR_EDAD = ["afiche", "topper", "topper_palito", "base_torta", "stickers",
                   "separadores", "etiqueta_botella", "cajita_sorpresa", "decoracion_sorbetes"]
# Estas 4 se leen como extras/<base>.png (sin edad).
EXTRAS_UNIVERSAL = ["banderin", "etiquetas_multiuso", "wrappers_cupcakes",
                    "tarjetas_agradecimiento"]
# (invitacion no está en ninguna: es el slot raíz temas/<tema>/invitacion_<edad>.png)

# Piezas por-edad que se generan SOLO en la 1ª edad y luego se REPLICAN al resto cambiando
# el número (para que las edades queden consistentes en vez de generarse por separado).
REPLICABLE = {"afiche"}

# Piezas que son IGUALES en todas las edades (no llevan número: el editor lo agrega) -> se
# generan UNA sola vez y se copian a todas las edades.
UNA_SOLA = {"invitacion"}

_DEF = {"accent": "#E0514A", "ink": "#4A4A4A", "font": "Baloo2-VF.ttf"}


def paleta_de(temas_dir, tema):
    try:
        cfg = json.load(open(os.path.join(temas_dir, tema, "tema.json"), encoding="utf-8"))
    except Exception:
        cfg = {}
    kit = cfg.get("kit", {})
    pal = {k: kit.get(k, _DEF[k]) for k in _DEF}
    # pedido de contenido para la hoja de stickers (tema.json::stickers_pedido):
    # qué motivos dibujar — p.ej. fútbol pide pelotas/botines/copas/banderas
    # argentinas, no genéricos (feedback Pablo 10-jul-2026)
    if cfg.get("stickers_pedido"):
        pal["stickers_pedido"] = str(cfg["stickers_pedido"])
    return pal


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
    "base_torta": ("Es un DISCO CIRCULAR grande (base/mat para apoyar la torta encima): patrón "
                   "y personajes decorativos repartidos por todo el círculo, CENTRADO, que LLENE "
                   "el disco sin salirse del borde; el centro puede ir más despejado."),
    "topper_palito": ("Cake topper para clavar con palito: UN solo grupo COMPACTO con los "
                      "personajes del tema bien JUNTOS y pegados (idealmente sobre un mismo "
                      "objeto/vehículo) formando UNA sola silueta maciza, NO una escena ancha "
                      "con figuras separadas, sin huecos internos. Dejá MARGEN libre abajo. "
                      "Fondo BLANCO liso para recortar. SIN texto y SIN palito (el palito lo "
                      "agrega el sistema)."),
    "etiquetas_multiuso": ("Es una PLANCHA rectangular LLENA de etiquetas circulares en grilla. "
                           "Cada etiqueta es un círculo RELLENO (con color/fondo sólido, tipo "
                           "sello/medalla) y un personaje CENTRADO adentro que la llene bien; "
                           "NINGÚN círculo vacío, hueco ni transparente. El fondo de la lámina "
                           "entre los círculos es blanco liso. Diseño completo que llena el "
                           "rectángulo."),
    "wrappers_cupcakes": ("2 o 3 wrappers de cupcake (forma de arco/abanico) apilados, TODOS "
                          "COMPLETOS y enteros DENTRO del cuadro, con MARGEN en todos los bordes; "
                          "que ninguno se corte arriba ni abajo (mejor menos cantidad y enteros)."),
    "cajita_sorpresa": ("Es la ILUSTRACIÓN DECORATIVA para las caras de una cajita (la caja la "
                        "arma el sistema): personajes del tema repartidos, coloridos, sobre un "
                        "fondo temático que LLENE TODO el cuadro (sin bordes blancos). NO dibujes "
                        "la caja, ni el molde, ni líneas de doblez: SOLO la decoración."),
    "stickers": ("Stickers del tema: SOLO los personajes del tema y objetos DISTINTIVOS "
                 "e inconfundibles de la temática (los que un chico reconoce al instante como "
                 "del tema). PROHIBIDO el relleno genérico: NADA de nubes, pasto o follaje "
                 "suelto, confeti, cuadraditos/rombos/círculos de colores, serpentinas, "
                 "estrellitas sueltas ni formas abstractas — cada sticker tiene que dar ganas "
                 "de pegarlo. La MAYOR variedad posible de motivos temáticos distintos, "
                 "ordenados en una GRILLA o filas parejas que LLENE bien la lámina. Cada sticker "
                 "SEPARADO del de al lado por un espacio en blanco claro (un margen entre cada "
                 "uno): que NO se toquen ni se superpongan, porque al recortarlos con borde se "
                 "pegarían. Cada figura COMPACTA y maciza, SIN huecos internos ni elementos "
                 "flotando con espacios en el medio (nada de aros/arcos abiertos). CADA STICKER "
                 "ES UNA SOLA SILUETA SÓLIDA Y CONECTADA, sin partes finas ni piezas separadas "
                 "que parezcan cortadas: NADA de antenas, hilos, cables, palitos o astas finas "
                 "con una bolita o estrella colgando arriba; si un objeto llevaría una antena o "
                 "algo que sobresale, dibujalo PEGADO al cuerpo con base ancha, nunca con un hilo "
                 "fino. Ninguna parte del sticker debe quedar flotando lejos del cuerpo principal. "
                 "Cada sticker es UNA figura ENTERA e independiente (un personaje, un animal, un "
                 "objeto); NO guirnaldas ni banderines en tira, NO recuadros/etiquetas/marcos en "
                 "blanco, NO manchas/salpicaduras ni elementos diminutos sueltos. Sobre fondo "
                 "BLANCO liso."),
}


# Texto personalizado en extras: EN PAUSA. Se hará con un editor (posición/tamaño/nombre)
# en vez de auto-posicionar. Por ahora vacío -> esas piezas quedan decorativas.
_CON_TEXTO = set()

_ZONA_LIMPIA = ("SIEMPRE dejá un ÁREA CENTRAL amplia, limpia y despejada (sin dibujos ni texto) "
                "para el texto que se agrega después; la decoración temática va SOLO alrededor.")


def prompt_de(paleta, pieza, edad=None):
    if pieza.key == "colorear":
        # Página para colorear: line art puro. NO usa el bloque de estilo (que pide colores
        # planos); el modelo dibuja SOLO contornos negros sobre blanco y el código garantiza
        # el B/N puro después. Usa los personajes del tema de las referencias.
        return ("Creá una PÁGINA PARA COLOREAR infantil con los personajes del tema de las "
                "imágenes de referencia (mismos personajes, sin cambiar su diseño). "
                "DIBUJO SOLO EN LÍNEAS: contornos negros de grosor MEDIO —ni finos ni muy "
                "gruesos, como un libro de colorear infantil estándar—, limpios y CERRADOS, "
                "sobre fondo BLANCO liso. Una escena simple y clara, personajes grandes y "
                "centrados, con espacios amplios para pintar. SIN relleno, SIN color, SIN "
                "grises, SIN sombras, SIN texturas, SIN tramas, SIN texto ni números. Estilo "
                "libro de colorear, line art, blanco y negro.")
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
        if pieza.key == "stickers" and paleta.get("stickers_pedido"):
            partes.append("Motivos pedidos para esta lámina: %s."
                          % paleta["stickers_pedido"])
    else:
        # piezas decorativas sin texto -> composición centrada y llena.
        partes.append("Composición CENTRADA y equilibrada que aproveche bien el espacio, "
                      "sin grandes zonas vacías.")
    partes.append(bloque_estilo(paleta))
    return " ".join(partes)
