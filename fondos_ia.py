"""Fondos IA por tema para los productos individuales — generaliza el patrón que
funcionó en el gorro (corona_ia.py): la IA genera UNA vez por tema el ARTE de
fondo de la pieza (con su zona limpia donde corresponde) y el motor escribe
SIEMPRE la personalización encima. Nada de texto horneado en la imagen (regla
de oro de la skill armar-kit §0.3 — bug histórico del calendario).

Cache en temas/<tema>/overrides/fondos/<pieza>.png. Sin fondo → cada módulo
cae a su versión procedural (fallback garantizado, skill §0.4)."""
import io
import os

from PIL import Image

import libro_ia

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")


def cover(img, w, h):
    """Escala el fondo a (w,h) PRESERVANDO la proporción: agranda hasta cubrir
    y recorta el excedente centrado. Nunca estira — si el arte (1536x1024,
    ratio 1.5) no coincide con el destino (A4 apaisado, 1.415) se pierde un
    poco de borde en vez de deformar a los personajes."""
    w, h = int(w), int(h)
    esc = max(w / img.width, h / img.height)
    im2 = img.resize((max(w, round(img.width * esc)), max(h, round(img.height * esc))),
                     Image.LANCZOS)
    x0, y0 = (im2.width - w) // 2, (im2.height - h) // 2
    return im2.crop((x0, y0, x0 + w, y0 + h))

# Registro de piezas: tamaño de generación + prompt específico (la referencia de
# estilo del tema —ia_maestra— va SIEMPRE primera; skill §0.1).
PIEZAS = {
    "menu": {
        "size": "1024x1536",
        "prompt": (
            "Marco decorativo VERTICAL para un menú infantil de fiesta, temática '{tema}'. "
            "Decoración del tema en los BORDES (arriba, abajo y costados) con personajes "
            "y motivos de la referencia; el CENTRO amplio, liso y muy claro (crema casi "
            "blanco) ocupando ~70% de la superficie, para superponer después las tarjetas "
            "del menú. Estilo alegre de fiesta."),
    },
    "certificado": {
        "size": "1536x1024",
        "prompt": (
            "Orla/marco APAISADO elegante para un diploma infantil, temática '{tema}'. "
            "Borde decorado en todo el perímetro con motivos y 1-2 personajes de la "
            "referencia en las esquinas inferiores; el CENTRO amplio, liso y muy claro "
            "(crema casi blanco) ocupando ~75% de la superficie, para el texto del "
            "diploma que se agrega después. Festivo pero prolijo, digno de enmarcar."),
    },
    "capsula": {
        "size": "1536x1024",
        "prompt": (
            "Frente APAISADO de un sobre decorado de 'cápsula del tiempo' para un "
            "cumpleaños infantil, temática '{tema}'. Decoración del tema en las esquinas "
            "y bordes (personajes de la referencia espiando por los bordes), y una gran "
            "zona central rectangular LISA y muy clara (crema casi blanco) para la "
            "etiqueta que se agrega después. Un toque mágico/nostálgico (estrellitas, "
            "destellos suaves)."),
    },
    "rompecabezas": {
        "size": "1024x1536",
        "prompt": (
            "Escena VERTICAL completa y vistosa de la temática '{tema}' para un "
            "rompecabezas infantil: los personajes de la referencia GRANDES, "
            "completos y bien centrados (lejos de los bordes) en una escena alegre "
            "de su mundo, colores vivos y detalle de borde a borde, SIN zonas "
            "vacías ni cielos lisos enormes (cada pieza del puzzle debe tener "
            "algo que mirar)."),
    },
    "escena": {
        "size": "1536x1024",
        "prompt": (
            "Paisaje APAISADO del mundo de la temática '{tema}' en tonos SUAVES y "
            "claros (pastel), SIN personajes — es el FONDO de una página de "
            "actividades infantil donde después se pegan figuras encima: cielo, "
            "piso y el lugar del tema bien difuminados de fondo, sin ningún "
            "elemento protagonista que compita con las figuras."),
    },
    "memoria_dorso": {
        "size": "1024x1024",
        "prompt": (
            "Patrón repetitivo DENSO y parejo para el dorso de cartas de un juego de "
            "memoria infantil, temática '{tema}'. Motivos chicos del tema distribuidos "
            "uniformemente en TODA la superficie (sin zona vacía, sin centro despejado, "
            "sin personaje protagonista), tonos medios (ni muy claro ni muy oscuro), "
            "como papel de regalo. Debe verse IGUAL en cualquier recorte cuadrado."),
    },
}


def fondo_path(tema, pieza):
    if pieza not in PIEZAS:
        raise ValueError("pieza inválida: %r" % pieza)
    return os.path.join(TEMAS, tema, "overrides", "fondos", "%s.png" % pieza)


def cargar_fondo(tema, pieza):
    try:
        p = fondo_path(tema, pieza)
    except ValueError:
        return None
    return Image.open(p).convert("RGBA") if os.path.isfile(p) else None


def generar(client, tema, pieza, calidad="medium"):
    """Genera y cachea el fondo IA de una pieza para un tema. Devuelve el path.
    `client` es ia_kit.client.OpenAIImageClient (o cualquier objeto con
    .editar(refs, prompt, size, quality=) -> bytes PNG)."""
    cfg = PIEZAS[pieza]
    refs = libro_ia.referencias(tema)
    if not refs:
        raise RuntimeError(
            "el tema %r no tiene imagen de referencia (ia_maestra.png/stickers) "
            "— agregala antes de generar fondos" % tema)
    prompt = (cfg["prompt"].format(tema=tema.replace("-", " ")) +
              " Mismo estilo, colores y personajes que la imagen de referencia. "
              "SIN NINGÚN TEXTO, LETRA, NÚMERO NI PALABRA en la imagen.")
    raw = None
    for intento in range(1, 5):
        try:
            raw = client.editar(refs, prompt, cfg["size"], quality=calidad)
            break
        except Exception as e:
            # Moderación de salida de OpenAI (moderation_blocked): es probabilística,
            # regenerar suele pasar. Reintentamos hasta 4 veces antes de fallar.
            m = str(e).lower()
            if intento < 4 and ("moderation" in m or "safety system" in m):
                print("[fondos-ia] %s/%s rechazado por moderación (intento %d/4) — regenerando"
                      % (tema, pieza, intento), flush=True)
                continue
            raise
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    dest = fondo_path(tema, pieza)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    img.save(dest)
    return dest
