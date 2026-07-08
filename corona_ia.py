"""Arte IA del gorro y la corona (fondos temáticos), generado UNA vez por tema
con OpenAI, igual que calendario (fondo.png) y libro (ilustración): la IA solo
aporta el arte — el motor dibuja encima lo suyo (troqueles, gemas, marcas).

Desde el 8-jul-2026 (feedback Pablo) NINGUNA de las dos piezas lleva nombre
("se pone en el momento"): el gorro va sin insignia (su prompt ya no pide zona
limpia) y la corona rediseñada (2 tiras con picos unidos) SÍ usa arte IA — su
prompt pide un friso denso y parejo porque el recorte es una banda horizontal."""
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
        # OJO: sin "zona limpia para la insignia" — desde el 8-jul-2026 el gorro va
        # SIN nombre (se pone en el momento, feedback Pablo) y un claro circular en
        # el arte queda como un agujero vacío.
        forma = ("un sector circular (como una porción de torta vista desde arriba, "
                 "con el vértice angosto arriba y el borde curvo ancho abajo) que al "
                 "enrollarse forma un gorro cónico de cumpleaños para armar. Personajes "
                 "del tema abajo (en el borde curvo ancho) y motivos chicos repartidos "
                 "por TODA la superficie hasta las puntas y esquinas, SIN ninguna zona "
                 "vacía, clara ni despejada en el centro")
    else:
        # La corona recorta una BANDA horizontal del centro de la imagen (cover):
        # patrón parejo tipo friso, sin escena con protagonistas que queden cortados.
        forma = ("un friso/guarda horizontal DENSO y PAREJO con motivos chicos del "
                 "tema repartidos uniformemente (como papel de regalo), tonos medios, "
                 "sin personajes grandes protagonistas y sin zonas vacías — se recorta "
                 "en franjas horizontales para armar una corona de cumpleaños, así que "
                 "debe verse bien en CUALQUIER franja horizontal de la imagen")
    return (
        "Ilustración infantil APAISADA (horizontal) para imprimir y recortar, temática "
        "'%s'. Diseño de fondo/patrón decorativo para un %s de cumpleaños: %s. Mismo "
        "estilo, colores y personajes que la imagen de referencia. Que llene TODO el "
        "encuadre (sin márgenes en blanco). SIN NINGÚN TEXTO, LETRA, NÚMERO NI PALABRA "
        "en la imagen."
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
    raw = client.editar(refs, _prompt(tema, pieza), "1536x1024", quality=calidad)
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    dest = fondo_path(tema, pieza)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    img.save(dest)
    return dest
