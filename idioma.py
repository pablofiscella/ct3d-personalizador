#!/usr/bin/env python3
"""El motor escribe en español. Esto le permite escribir en otro idioma SIN duplicar nada.

POR QUÉ EXISTE
──────────────
19-ago-2026. La tienda de Etsy (`Casa3DAR`) quedó conectada y cobra en dólares, que es el
mercado que se quiere. Pero el kit sale con «¡Gracias por venir!» y «Confirmá»: venderle eso
a un comprador de habla inglesa no tiene sentido.

LA FORMA QUE **NO** SE ELIGIÓ, Y POR QUÉ
────────────────────────────────────────
Lo obvio era duplicar: un `temas/<tema>-en/` con sus 44 layouts y sus 12 `tema.json`
traducidos. Se descartó porque **el admin edita los layouts con el editor visual**: cada vez
que moviera un texto en español, la copia en inglés quedaría atrás y en silencio. Dos fuentes
de verdad para la misma pieza es exactamente el problema que ya costó caro.

Acá hay **una sola fuente de verdad —el español— y una tabla de traducción**. Se traduce la
PLANTILLA (`"FELIZ CUMPLE {nombre}"`), no el resultado, así los marcadores sobreviven y el
motor los completa igual con los datos del comprador.

EL GUARDIÁN
───────────
`tests/test_idioma.py` junta TODO lo que el motor puede llegar a imprimir —los specs de
`temas.py`, los 12 `tema.json`, los 44 layouts y los literales de `piezas.py`— y falla si
alguno no tiene traducción. O sea: si mañana se agrega un tema, o el editor guarda un texto
nuevo, el test dice **exactamente cuál falta** en vez de dejar que salga un kit mitad en
inglés y mitad en español.

Es la lección de esta misma mañana: un barrido protege hasta donde mira. Éste mira las
cuatro formas en que el proyecto guarda un texto imprimible.
"""

IDIOMA_ORIGEN = "es"
IDIOMAS = ("es", "en")


def _clave(t):
    """Los textos vienen del editor visual, que deja espacios de más y mayúsculas sueltas
    («al cumple de », «Al cumple de»). La clave normaliza eso; la puntuación NO se toca,
    porque «FELIZ CUMPLE {nombre}» y «¡FELIZ CUMPLE {nombre}!» son piezas distintas."""
    return " ".join(t.split()).casefold()


# Español → inglés. La clave se normaliza con _clave(); el valor va con la caja y la
# puntuación EXACTAS con que tiene que imprimirse (por eso «HAPPY BIRTHDAY» va en mayúscula
# acá y no se calca de la fuente: calcar la caja rompería el marcador «{nombre}»).
EN = {
    # ── invitación ────────────────────────────────────────────────────────────
    "te invitamos al cumple de":      "You're invited to the birthday party of",
    "cumple {edad} años":             "Turning {edad} years old",
    "{edad} años":                    "{edad} years old",
    "confirmá:":                      "RSVP:",
    "confirmar: {telefono}":          "RSVP: {telefono}",
    # el titular de la invitación es propio de cada temática
    "¡estás invitado a mi cumple!":   "You're invited to my birthday!",
    "¡alerta de cumpleaños!":         "BIRTHDAY ALERT!",
    "¡aventura en el bosque!":        "ADVENTURE IN THE WOODS!",
    "¡creemos una obra maestra!":     "Let's create a masterpiece!",
    "¡el espectáculo está por comenzar!": "The show is about to begin!",
    "¡llamado a todos los superhéroes!":  "CALLING ALL SUPERHEROES!",
    "¡obra en construcción!":         "UNDER CONSTRUCTION!",
    "¡se viene una fiesta monstruosa!":   "A MONSTROUS PARTY IS COMING!",
    "¡preparate para una tarde llena de aventuras!":
        "Get ready for an afternoon of adventure!",
    "¡pintaremos recuerdos inolvidables juntos!":
        "We'll paint unforgettable memories together!",
    "¡no faltes, los monstruitos te están esperando!":
        "The little monsters are waiting for you!",
    "¡te esperamos para construir recuerdos inolvidables!":
        "Come build unforgettable memories with us!",
    "¡te esperamos para salvar la diversión!":
        "Come help us save the fun!",
    "¡te esperamos para una tarde llena de magia y diversión!":
        "An afternoon full of magic and fun awaits!",
    "¡te espero para despegar juntos en esta aventura!":
        "Let's take off on this adventure together!",
    "¡te necesitamos para esta misión especial!":
        "We need you for this special mission!",

    # ── afiche, banderín, cajita, sorbetes ────────────────────────────────────
    "feliz cumple {nombre}":          "HAPPY BIRTHDAY {nombre}",
    "¡feliz cumple {nombre}!":        "HAPPY BIRTHDAY {nombre}!",
    "¡bienvenidos!":                  "Welcome!",

    # ── tarjeta de agradecimiento (tres líneas apiladas) ──────────────────────
    "¡gracias por venir!":            "Thank you for coming!",
    "al cumple de":                   "to the birthday party of",
    "bienvenidos al cumple de":       "Welcome to the birthday party of",

    # ── piezas armadas por código (piezas.py) ─────────────────────────────────
    "el cumple de":                   "The birthday party of",
    "¡cumplo {edad}!":                "I'm turning {edad}!",
    "¡cumplo %s!":                    "I'm turning %s!",
    "el primer añito de":             "The first birthday of",
    "los dos añitos de":              "The second birthday of",
    "los tres añitos de":             "The third birthday of",
    "¡un añito salvaje!":             "One year wild!",
    "¡dos añitos salvajes!":          "Two years wild!",
    "¡tres añitos salvajes!":         "Three years wild!",
    "cumple":                         "turns",          # «cumple 5» → «turns 5»
    "¡para pintar!":                  "Time to color!",
    "coloreá y decorá tu cumple":     "Color and decorate your party",

    # ── rompecabezas imprimible (rompecabezas.py) ─────────────────────────────
    # Se sumó el 19-ago-2026 al preparar la publicación de Etsy: el rompecabezas es el
    # único producto que se entrega como descarga instantánea —no lleva personalización—,
    # así que sus hojas tienen que salir en inglés sin que nadie intervenga.
    "rompecabezas %d · %d piezas":    "PUZZLE %d · %d pieces",
    "bandeja %d · armá el rompecabezas acá encima":
        "TRAY %d · build the puzzle on top",
    "pegá esta hoja sobre cartulina o cartón fino y recortá por las líneas.":
        "Glue this sheet onto card stock or thin cardboard and cut along the lines.",
    "así queda":                      "how it looks",
    # ── rompecabezas web: el título que dibuja el servidor en la portada ──────
    "los rompecabezas de %s":         "%s's puzzles",
    "rompecabezas %s":                "%s puzzles",
    "tu rompecabezas":                "Your puzzle",

    "cada pieza tiene un solo lugar. ¡mirá la referencia si te trabás!":
        "Every piece has one spot. Check the picture if you get stuck!",
}

TABLAS = {"en": EN}


# El NOMBRE de cada temática, para la página del comprador de Etsy. Va acá y no en cada
# `tema.json` porque el nombre en español es el que usa el panel de Pablo, y no se toca.
# Se descubrió mirando la página andando: el selector le ofrecía «Bomberos al Rescate» a un
# comprador de Estados Unidos.
NOMBRE_TEMA_EN = {
    "artistas": "Little Artists",
    "aviadores": "Little Pilots",
    "bomberos": "Firefighters to the Rescue",
    "campamento": "Camping — Forest Adventure",
    "circo": "Circus — The Big Show",
    "construccion": "Construction — Let's Build!",
    "futbol": "Soccer / Football",
    "monstruos": "Monsters — Monstrous Party",
    "princesas": "Princesses",
    "safari": "Safari — Jungle Animals",
    "superheroes": "Superheroes",
    "un-espacio-de-locura": "Outer Space",
}


def nombre_tema(tema_id, nombre_es, lang):
    """El nombre de la temática en el idioma pedido; si falta, el original."""
    if lang == "en":
        return NOMBRE_TEMA_EN.get(tema_id) or nombre_es
    return nombre_es


def traducir(texto, idioma):
    """La plantilla en el idioma pedido. Sin traducción, devuelve el original.

    Devolver el original —y no reventar— es a propósito: que falte una traducción tiene que
    salir en el test, no romperle el kit a un comprador. El test es el que no perdona."""
    if not isinstance(texto, str) or not texto.strip():
        return texto
    if not idioma or idioma == IDIOMA_ORIGEN:
        return texto
    tabla = TABLAS.get(idioma)
    if not tabla:
        return texto
    t = tabla.get(_clave(texto))
    if t is None:
        return texto
    # se respeta el espacio final del original: «cumple » + edad se arma concatenando
    if texto.endswith(" ") and not t.endswith(" "):
        t += " "
    return t


def sin_traduccion(textos, idioma):
    """Cuáles de estos textos NO tienen traducción. Lo usa el guardián."""
    if idioma == IDIOMA_ORIGEN:
        return []
    tabla = TABLAS.get(idioma) or {}
    faltan = []
    for t in textos:
        if not isinstance(t, str) or not t.strip():
            continue
        if _clave(t) not in tabla:
            faltan.append(t)
    return sorted(set(faltan))


def singular_edad(texto, idioma):
    """«Turning 1 years old» no existe. Cada idioma arregla su plural acá.

    El motor ya hacía esto para el español (« años» → « año») escrito a mano adentro de
    `_field_text`. Al sumar idiomas, esa regla dejó de ser una sola: vive acá."""
    reglas = {"es": ((" años", " año"),),
              "en": ((" years old", " year old"), (" years", " year"))}
    for viejo, nuevo in reglas.get(idioma or IDIOMA_ORIGEN, ()):
        texto = texto.replace(viejo, nuevo)
    return texto


def de(data):
    """El idioma que pidió el comprador. Sin dato, español: no cambia nada de lo que ya anda."""
    if not isinstance(data, dict):
        return IDIOMA_ORIGEN
    i = str(data.get("idioma") or IDIOMA_ORIGEN).strip().lower()[:2]
    return i if i in IDIOMAS else IDIOMA_ORIGEN
