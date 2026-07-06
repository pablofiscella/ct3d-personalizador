"""Libro de cuento personalizado — cuento infantil imprimible, listo para vender.

El chico es EL PROTAGONISTA: la historia se arma con su nombre/edad y la ambientación
de la temática (mundo, amigos, desafío y tesoro salen de HISTORIAS, con fallback
genérico para temas nuevos). 10 páginas A4: portada · dedicatoria · 7 páginas de
historia · fin. Todo procedural (Pillow) — determinístico por tema+página, así el
mismo pedido genera siempre el mismo libro.

Ilustraciones: cada página deja la MITAD SUPERIOR como escena ilustrada. La base es
procedural (cielo, colinas, sol/estrellas + los personajes del tema recortados de los
stickers, si existen). Para versión "premium" se reemplaza cualquier página con arte
IA subiendo temas/<tema>/overrides/libro/<idx>.png — mismo override system que el
resto de los productos, cero cambio de código.

API: paginas_libro(data, tema) -> [PIL.Image] · pagina_libro(idx, data, tema) -> PIL.Image
"""
import contextlib
import os, json, glob, math, random, threading, re
from libro_historias import ARGUMENTOS_LARGO, CORTO_IDX
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
CREAM = (253, 250, 242)
INK = (60, 52, 62)
GOLD = (212, 175, 55)

PAGINAS_HISTORIA = 7          # legado: páginas de cuento de los temas existentes
PAGINAS_HISTORIA_NUEVO = 12   # temas nuevos (15 páginas en total)
PAGINAS_HISTORIA_LARGO = 17   # catálogo de audiolibros, 4 años o más (20 en total)
PAGINAS_HISTORIA_CORTA = 9    # catálogo de audiolibros, hasta 3 años (12 en total)
TOTAL_PAGINAS = PAGINAS_HISTORIA + 3   # legado — usado solo como valor por default


def _edad_int(edad):
    """Primer número que aparezca en la edad ('5', '3 años', 5) o None."""
    m = re.search(r"\d+", str(edad or ""))
    return int(m.group()) if m else None


def paginas_historia(tema, edad=None, historia=None, catalogo=False):
    """Páginas de historia. El CATÁLOGO de audiolibros (catalogo=True + una de las 8
    historias) usa largo por EDAD desacoplado del tema: 9 hasta 3 años, 17 de 4 en
    adelante. Cualquier otro caso (libro de kit, previews) mantiene el largo legado:
    7 en los temas ya vendidos, 12 en los nuevos. El flag catalogo lo prende SOLO el
    audiolibro, para no cambiarle el largo al libro de kit aunque comparta tema."""
    if catalogo and historia and historia in ARGUMENTOS_LARGO:
        e = _edad_int(edad)
        return PAGINAS_HISTORIA_CORTA if (e is not None and e <= 3) else PAGINAS_HISTORIA_LARGO
    try:
        d = json.load(open(os.path.join(TEMAS, tema, "tema.json")))
        n = d.get("libro_paginas_historia")
        if isinstance(n, int) and n > 0:
            return n
    except Exception:
        pass
    return PAGINAS_HISTORIA_NUEVO


def total_paginas(tema, edad=None, historia=None, catalogo=False):
    return paginas_historia(tema, edad, historia, catalogo) + 3

# ── ambientación por temática (fallback genérico para temas nuevos) ─────────
# REGLAS del diccionario (para que cualquier valor encaje en cualquier arco de
# libro_historias sin romper la gramática — ver skill armar-audiolibros):
#   mundo:    con artículo incluido ("la sabana...", "el gran circo..."). Los arcos
#             solo lo usan tras preposición (en/a/de/hacia/por/sobre) o como sujeto
#             sin adjetivos que concuerden — NUNCA "el {mundo}" ni "todo {mundo}".
#   amigos:   SIEMPRE masculino plural con "los ..." (los arcos usan adjetivos en
#             masculino plural: tristes, cabizbajos, preocupados).
#   desafio:  cláusula simple en pasado, minúscula inicial, SIN ":", "¡" ni "!"
#             (se inserta en «apareció un problema: {desafio}. Nadie sabía...»).
#   solucion: acción en pasado, 3ª persona singular, empieza con verbo (se inserta
#             en «{nombre} {solucion}» seguido de una consecuencia).
#   tesoro:   objeto con artículo ("una .../un ..."), neutro para nene o nena.
HISTORIAS = {
    "safari": {
        "mundo": "la sabana dorada del safari",
        "amigos": "los animales de la selva",
        "desafio": "el pequeño león no encontraba el camino a su casa",
        "solucion": "trepó al árbol más alto y descubrió el sendero escondido",
        "tesoro": "una brújula dorada de exploración",
    },
    "circo": {
        "mundo": "el gran circo de colores",
        "amigos": "los artistas del circo",
        "desafio": "el mago no encontraba su sombrero mágico por ningún lado",
        "solucion": "siguió las huellas de purpurina y encontró el sombrero detrás de la carpa",
        "tesoro": "una entrada mágica para volver al circo cuando quiera",
    },
    "superheroes": {
        "mundo": "la ciudad de los superhéroes",
        "amigos": "los superhéroes de la ciudad",
        "desafio": "un viento travieso se había llevado todas las capas",
        "solucion": "descubrió las capas en la torre más alta y las rescató una por una",
        "tesoro": "una capa brillante hecha a su medida",
    },
    "construccion": {
        "mundo": "la gran obra en construcción",
        "amigos": "los constructores y sus máquinas",
        "desafio": "la grúa no encontraba la última pieza del puente",
        "solucion": "encontró la pieza perdida y guió a la grúa para colocarla",
        "tesoro": "un casco dorado de constructor",
    },
    "bomberos": {
        "mundo": "la estación de bomberos",
        "amigos": "los bomberos valientes",
        "desafio": "un gatito había quedado atrapado en lo alto de un árbol",
        "solucion": "subió por la escalera del camión y lo rescató con mucho cuidado",
        "tesoro": "una medalla de bombero honorario",
    },
    "aviadores": {
        "mundo": "el cielo de los aviadores",
        "amigos": "los pilotos y sus aviones",
        "desafio": "una nube gigante tapaba el camino de vuelta al aeropuerto",
        "solucion": "guió a todos los aviones con la brújula del avión más pequeño",
        "tesoro": "unas alas doradas de piloto",
    },
    "campamento": {
        "mundo": "el bosque del campamento",
        "amigos": "los amigos del campamento",
        "desafio": "la fogata que alumbraba el campamento se había apagado",
        "solucion": "juntó las ramitas más secas y la fogata volvió a brillar",
        "tesoro": "una linterna que guarda luz de estrellas",
    },
    "artistas": {
        "mundo": "el taller de los artistas",
        "amigos": "los pequeños artistas del taller",
        "desafio": "los colores se habían mezclado y todo se había vuelto gris",
        "solucion": "pintó un arcoíris enorme que devolvió cada color a su lugar",
        "tesoro": "un pincel mágico que nunca se queda sin color",
    },
    "monstruos": {
        "mundo": "el país de los monstruos divertidos",
        "amigos": "los monstruos más simpáticos",
        "desafio": "el monstruo más chiquito tenía miedo de la oscuridad",
        "solucion": "le enseñó que en la oscuridad también viven las estrellas",
        "tesoro": "un frasquito con luciérnagas de luz",
    },
    "princesas": {
        "mundo": "el reino encantado de las princesas",
        "amigos": "los amigos del reino encantado",
        "desafio": "la corona real se había perdido antes del gran baile",
        "solucion": "siguió los destellos dorados y encontró la corona en el jardín del castillo",
        "tesoro": "una coronita brillante del reino, hecha a su medida",
    },
    "futbol": {
        "mundo": "el gran estadio de fútbol",
        "amigos": "los jugadores del equipo",
        "desafio": "la pelota dorada se había perdido antes del gran partido",
        "solucion": "encontró la pelota escondida detrás del arco y la trajo de vuelta",
        "tesoro": "una copa dorada de campeón",
    },
    "un-espacio-de-locura": {
        "mundo": "el espacio infinito",
        "amigos": "los astronautas y las estrellas",
        "desafio": "un cometa travieso había escondido la luna",
        "solucion": "persiguió al cometa en su nave y trajo la luna de vuelta",
        "tesoro": "una estrella que brilla de verdad",
    },
}
HISTORIAS["superhéroes"] = HISTORIAS["superheroes"]
HISTORIA_DEFAULT = {
    "mundo": "un mundo mágico",
    "amigos": "sus nuevos amigos",
    "desafio": "el camino de regreso había desaparecido",
    "solucion": "siguió las estrellas más brillantes y encontró el sendero",
    "tesoro": "una estrella de la suerte",
}


def _font(sz, bold=True):
    for p in glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True):
        try:
            f = ImageFont.truetype(p, sz)
            try: f.set_variation_by_axes([700 if bold else 500])
            except Exception: pass
            return f
        except Exception: pass
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)


def _accent(tema):
    try:
        d = json.load(open(os.path.join(TEMAS, tema, "tema.json")))
        h = ((d.get("kit") or {}).get("accent") or "#6B5BD2").lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except Exception:
        return (107, 91, 210)


def _tint(rgb, p):
    return tuple(int(c + (255 - c) * p) for c in rgb[:3])


def _personajes(tema, n=3):
    """Personajes del tema (recortes de la hoja de stickers), FILTRADOS: un recorte
    real (die-cut) siempre tiene transparencia alrededor; un componente ~100% opaco es
    la hoja entera con fondo blanco (pasa en temas cuyos stickers no traen alpha) y
    pegarla arruina la escena — se descarta."""
    try:
        import cuaderno
        mons = cuaderno.personajes_decorativos(tema, n)
    except Exception:
        return []
    out = []
    for m in mons:
        a = m.getchannel("A")
        op = sum(a.histogram()[129:]) / float(m.width * m.height)
        if op < 0.92:
            out.append(m)
    return out


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


def _wrap(dr, text, font, maxw):
    """Corta el texto en líneas que entran en maxw (por palabras)."""
    lines, cur = [], ""
    for w in str(text).split():
        t = (cur + " " + w).strip()
        if dr.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def _parrafo(dr, text, cx, y, font, color, maxw, lh=1.35, anchor="ma"):
    for ln in _wrap(dr, text, font, maxw):
        dr.text((cx, y), ln, font=font, fill=color, anchor=anchor)
        y += int(font.size * lh)
    return y


# ── argumentos: hilos narrativos distintos (mismo tema, otra historia) ────────
# Cada argumento define los 7 textos de la historia con la ambientación del tema
# ({mundo}/{amigos}/{tesoro} salen de HISTORIAS; {desafio}/{solucion} solo los usa
# el clásico). El cliente elige el argumento al comprar (campo "historia") — así
# la misma temática da libros DIFERENTES y se puede comprar más de uno.
ARGUMENTOS = {
    "aventura": None,   # el clásico (invitación mágica) — textos abajo, en cuento()
    "tesoro": [
        "Esa mañana, {nombre} encontró un mapa antiguo enrollado en su mochila. "
        "Marcaba un camino secreto hacia {mundo}.",
        "Al seguir la primera pista y {conteo}, ¡el mapa empezó a brillar! "
        "La búsqueda del tesoro había comenzado.",
        "En {mundo}, {amigos} conocían las pistas: cada uno le contó a {nombre} "
        "un secreto del camino.",
        "Pero la última pista estaba del otro lado de un río enorme, y nadie "
        "sabía cómo cruzarlo... nadie, excepto {nombre}.",
        "{nombre} armó un puente con troncos y sogas, ¡y cruzaron todos juntos "
        "cantando! Ahí estaba: un cofre dorado.",
        "Adentro brillaba {tesoro}. {amigos} aplaudieron: «¡{nombre} es quien "
        "mejor sigue las pistas en todo {mundo}!»",
        "De vuelta en casa, {nombre} guardó el mapa bajo la almohada. Los "
        "mejores tesoros se encuentran con paciencia y buenos amigos.",
    ],
    "rescate": [
        "Una noche, una lucecita golpeó la ventana de {nombre}: era un mensaje "
        "urgente desde {mundo}. ¡Necesitaban ayuda!",
        "{nombre} no lo dudó: cerró los ojos, empezó a {conteo}... y el viento "
        "lo llevó volando hasta {mundo}.",
        "{amigos} estaban muy preocupados: el más pequeño del grupo se había "
        "perdido y ya estaba oscureciendo.",
        "Buscaron por todos lados sin suerte. Entonces {nombre} tuvo una idea: "
        "«¡Sigamos las huellas más chiquitas!»",
        "Las huellas llevaron a una cueva. {nombre} entró con su linterna, "
        "tomó al pequeño de la mano y lo trajo de vuelta. ¡Qué valiente!",
        "Como agradecimiento, {amigos} le regalaron {tesoro}: la marca de los "
        "héroes de {mundo}.",
        "Esa noche {nombre} durmió con una sonrisa gigante. Ayudar a un amigo "
        "es la aventura más importante de todas.",
    ],
    "gran-dia": [
        "¡Llegó una noticia increíble! En {mundo} se hacía la Gran Fiesta del "
        "año, y {nombre} estaba en la lista de invitados especiales.",
        "{nombre} preparó su mochila, contó hasta {conteo_num} para darse "
        "valor... ¡y salió rumbo a la aventura!",
        "{amigos} lo recibieron ensayando: había juegos, música y un gran "
        "desfile para preparar. ¡Faltaba tan poco!",
        "Pero de pronto, ¡PUM!, una tormenta desarmó todo lo que habían "
        "preparado. Todos se miraron sin saber qué hacer.",
        "«¡No nos rindamos!», dijo {nombre}, y organizó a todos: unos ataban, "
        "otros pintaban... ¡y la fiesta quedó más linda que antes!",
        "La Gran Fiesta fue inolvidable, y {amigos} le entregaron a {nombre} "
        "{tesoro}, el premio al invitado más especial.",
        "Al volver a casa, {nombre} entendió el secreto: los grandes días se "
        "construyen entre todos, con manos que ayudan.",
    ],
}

ARGUMENTO_LABELS = {"aventura": "La invitación mágica (clásico)",
                    "tesoro": "El mapa del tesoro",
                    "rescate": "El gran rescate",
                    "gran-dia": "El gran día",
                    "noche-estrellas": "La noche de las estrellas",
                    "cumple-sorpresa": "El cumpleaños sorpresa",
                    "pequeno-maestro": "El pequeño maestro",
                    "ayudar-a-todos": "El día de ayudar a todos"}

# Versión extendida (12 páginas) de las 4 narrativas clásicas: para los temas NUEVOS
# (15 páginas en total). Los primeros 6 textos son IDÉNTICOS a ARGUMENTOS (arriba) —
# no se toca el contenido ya vendido — se le suman 5 páginas de historia en el medio
# y el cierre (idéntico al original) pasa al final.
ARGUMENTOS_EXT = {
    "tesoro": ARGUMENTOS["tesoro"][:6] + [
        "Todos se sentaron en ronda para admirar {tesoro} de cerca. {amigos} le "
        "contaron a {nombre} la leyenda de quién lo había escondido hace tantos años.",
        "De pronto, el mapa volvió a brillar: ¡tenía una segunda cara! Mostraba un "
        "camino nuevo, más corto, de vuelta a casa a través de {mundo}.",
        "En el camino encontraron una piedra enorme bloqueando el paso. Entre "
        "todos, empujando juntos y contando hasta tres, lograron correrla.",
        "Como festejo por el trabajo en equipo, armaron una merienda bajo un "
        "árbol, y {nombre} repartió un pedacito de aventura para cada amigo.",
        "Antes de despedirse, {amigos} le prometieron a {nombre} que el mapa "
        "tendría siempre una pista nueva esperando para la próxima vez.",
    ] + ARGUMENTOS["tesoro"][6:],
    "rescate": ARGUMENTOS["rescate"][:6] + [
        "El pequeño rescatado abrazó fuerte a {nombre} y le contó que se había "
        "perdido siguiendo una mariposa brillante que quería atrapar.",
        "«¿Y si la buscamos juntos, pero esta vez sin separarnos?», propuso "
        "{nombre}. Todos se tomaron de la mano y salieron a explorar {mundo}.",
        "La mariposa los llevó hasta un lugar precioso que nadie en {mundo} "
        "conocía: un rincón lleno de luces que parecían pequeñas estrellas caídas.",
        "{amigos} decidieron que ese sería su nuevo lugar de encuentro secreto, "
        "y todos prometieron cuidarlo entre todos.",
        "Ya de noche, cantaron juntos alrededor de las lucecitas, felices de que "
        "la aventura hubiera terminado bien para todos.",
    ] + ARGUMENTOS["rescate"][6:],
    "gran-dia": ARGUMENTOS["gran-dia"][:6] + [
        "Con {tesoro} bien puesto, {nombre} fue el encargado de dar la "
        "bienvenida a cada invitado que llegaba a {mundo}.",
        "A mitad de la fiesta, la música se cortó de repente. ¡El equipo de "
        "sonido se había quedado sin pilas!",
        "{nombre} tuvo una idea genial: organizó a {amigos} para hacer música "
        "con las manos, los pies y lo que tenían a mano.",
        "La banda improvisada sonó tan bien que todos terminaron bailando más "
        "fuerte que antes, ¡y nadie extrañó la música original!",
        "Cuando el sol empezó a esconderse, {amigos} armaron una ronda final "
        "para agradecerle a {nombre} por no dejar que nada arruinara el gran día.",
    ] + ARGUMENTOS["gran-dia"][6:],
    "noche-estrellas": [
        "Una noche, {nombre} miraba el cielo desde la ventana cuando vio caer "
        "una estrella fugaz directo hacia {mundo}.",
        "Sin pensarlo dos veces, se puso las pantuflas y salió a buscarla, "
        "contando los pasos hasta {conteo_num} para no perderse.",
        "En {mundo}, {amigos} también habían visto la estrella caer y ya "
        "estaban buscando entre las sombras.",
        "Pero la noche era muy oscura, y {desafio}. Nadie encontraba el "
        "camino... nadie, excepto {nombre}.",
        "Con valentía, {nombre} {solucion}, y así encontraron la luz que los "
        "guiaba.",
        "Siguiendo el brillo, llegaron hasta la estrella fugaz: estaba cansada "
        "de tanto viajar y solo quería un lugar donde descansar.",
        "{amigos} le armaron una camita de nubes suaves, y {nombre} le cantó "
        "una canción bajito para que se sintiera en casa.",
        "La estrella, agradecida, empezó a brillar tan fuerte que iluminó todo "
        "{mundo} como si fuera de día.",
        "Con esa luz mágica, todos jugaron a las escondidas entre las sombras "
        "que ya no daban miedo.",
        "Antes de despedirse, la estrella le regaló a {nombre} {tesoro}, para "
        "recordar esa noche para siempre.",
        "{amigos} prometieron cuidar el cielo de {mundo} cada noche, por si "
        "otra estrella necesitaba ayuda.",
        "De vuelta en su cama, {nombre} se durmió mirando las estrellas, "
        "sabiendo que ahora tenía una amiga ahí arriba.",
    ],
    "cumple-sorpresa": [
        "{nombre} descubrió un secreto: ¡mañana era el cumpleaños de su mejor "
        "amigo en {mundo}, y nadie lo sabía!",
        "Emocionado, empezó a {conteo} para calmar los nervios y se puso manos "
        "a la obra con el plan más secreto de todos.",
        "Primero necesitaba ayuda, así que fue a buscar a {amigos} y les contó "
        "la misión, susurrando para que nadie escuchara.",
        "Todos se pusieron a preparar la sorpresa, pero {desafio}, y el plan "
        "estuvo a punto de arruinarse.",
        "Por suerte, {nombre} {solucion} justo a tiempo, y la fiesta sorpresa "
        "se pudo salvar.",
        "Decoraron cada rincón de {mundo} con globos y guirnaldas, escondidos "
        "detrás de cada esquina, esperando el momento justo.",
        "Cuando el cumpleañero se acercó sin sospechar nada, todos contuvieron "
        "la risa lo más fuerte que pudieron.",
        "«¡SORPRESA!», gritaron {amigos} a la vez, y el cumpleañero se llevó "
        "el susto más lindo de su vida.",
        "Hubo torta, juegos y muchas risas. {nombre} había pensado en cada "
        "detalle para que fuera un día inolvidable.",
        "Como regalo especial, todos juntos le entregaron {tesoro}, hecho con "
        "mucho cariño entre todos.",
        "El cumpleañero, con lágrimas de alegría, abrazó a {nombre} y le dijo "
        "que nunca iba a olvidar ese día.",
        "Esa noche, {nombre} se durmió pensando que las mejores sorpresas son "
        "las que se preparan con el corazón.",
    ],
    "pequeno-maestro": [
        "En {mundo}, {nombre} sabía hacer algo muy especial que nadie más "
        "sabía hacer todavía.",
        "Un día, {amigos} le pidieron: «¿Nos enseñás? ¡Queremos aprender igual "
        "que vos!». {nombre} se puso a {conteo} de la emoción.",
        "La primera clase empezó con muchas ganas, pero a nadie le salía bien "
        "al principio.",
        "Entonces pasó algo: {desafio}, y todos empezaron a desanimarse "
        "pensando que nunca iban a aprender.",
        "{nombre} no se rindió: {solucion}, y les mostró que equivocarse "
        "también es parte de aprender.",
        "Poco a poco, uno por uno, {amigos} empezaron a lograrlo, ¡y las caras "
        "de orgullo no se podían esconder!",
        "{nombre} festejaba cada intento, aunque no saliera perfecto: «¡Lo "
        "importante es probar!», repetía siempre con una sonrisa.",
        "Con el tiempo, cada amigo encontró su propia forma de hacerlo, un "
        "poquito distinta y única a la vez.",
        "Organizaron una muestra en {mundo} para mostrarle a todos lo que "
        "habían aprendido juntos.",
        "Todos aplaudieron fuerte, y {amigos} le agradecieron a {nombre} con "
        "{tesoro}, por ser el mejor maestro que tuvieron.",
        "{nombre} entendió que enseñar algo que uno ama es tan lindo como "
        "aprenderlo por primera vez.",
        "Esa noche, {nombre} se durmió pensando en la próxima cosa nueva que "
        "le encantaría compartir con sus amigos.",
    ],
    "ayudar-a-todos": [
        "Esa mañana, {nombre} se despertó con muchas ganas de hacer algo "
        "bueno por todos en {mundo}.",
        "Se puso las botas, empezó a {conteo} para tomar impulso, y salió a "
        "caminar por {mundo} buscando a quién ayudar primero.",
        "El primero en aparecer fue un amigo muy triste porque {desafio}, y "
        "no sabía cómo resolverlo solo.",
        "{nombre} pensó rápido y {solucion}. El amigo sonrió agradecido y se "
        "sumó a la aventura.",
        "Juntos siguieron caminando y encontraron a otro de {amigos} que se "
        "había quedado sin merienda para compartir.",
        "Sin dudarlo, {nombre} repartió lo que tenía en su mochila para que "
        "nadie se quedara con hambre.",
        "Más adelante, alguien había perdido un juguete muy querido en algún "
        "rincón de {mundo}.",
        "Todos se organizaron en equipos y, buscando entre risas, lo "
        "encontraron escondido detrás de unas plantas.",
        "Ya cansados pero felices, se cruzaron con el último amigo del día, "
        "que necesitaba una mano para cargar algo pesado.",
        "Entre todos lo cargaron como si nada, demostrando que las cosas "
        "pesadas pesan menos cuando se ayudan entre varios.",
        "Al caer la tarde, {amigos} se juntaron para agradecerle a {nombre} "
        "regalándole {tesoro}, por un día lleno de buenas acciones.",
        "{nombre} volvió a casa cansado pero con el corazón lleno, pensando "
        "que ayudar a los demás es la mejor forma de jugar.",
    ],
}


_RE_INICIO_FRASE = re.compile(r'(^|[.!?]\s+|[¡¿]\s*|»\s+)([a-záéíóúüñ])')


def _capitalizar_frases(texto):
    """Pone mayúscula al inicio del texto y después de cada punto/signo, y cambia
    las comillas españolas «» por inglesas “” (las « se leen como '>>' y los
    padres las toman por un error — regla del catálogo). Necesario porque los
    placeholders como {amigos} (\"los animales de la selva\") caen a veces al
    comienzo de una oración y quedarían en minúscula."""
    t = _RE_INICIO_FRASE.sub(lambda m: m.group(1) + m.group(2).upper(), texto)
    return t.replace("«", "“").replace("»", "”")


def cuento(data, tema="safari", catalogo=False):
    """Los textos de la historia, personalizados con nombre/edad + la ambientación
    del tema. Con catalogo=True (audiolibro) usa la versión rica del catálogo con
    largo por edad; si no, el largo legado (7/12). Testeable sin renderizar (el
    nombre TIENE que aparecer en el cuento)."""
    h = HISTORIAS.get(tema, HISTORIA_DEFAULT)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    edad = str(data.get("edad") or "").strip()
    conteo = ("contar hasta %s" % edad) if edad.isdigit() else "contar hasta tres"
    historia_raw = str(data.get("historia") or "").strip().lower()
    historia = historia_raw or "aventura"
    ctx = dict(h)
    ctx.update({"nombre": nombre, "conteo": conteo,
                "conteo_num": edad if edad.isdigit() else "tres"})
    # Catálogo de audiolibros: versión rica de 17 páginas, o su subconjunto de 9
    # para los más chiquitos (largo por edad). Solo si el audiolibro lo pide.
    arco_largo = ARGUMENTOS_LARGO.get(historia_raw) if catalogo else None
    if arco_largo is not None:
        n = paginas_historia(tema, edad, historia_raw, catalogo=True)
        arco = arco_largo if n >= PAGINAS_HISTORIA_LARGO else [arco_largo[i] for i in CORTO_IDX]
        return [_capitalizar_frases(t.format(**ctx)) for t in arco]
    # ----- legado: temas viejos / libro de kit (sin historia elegida) -----
    extendido = paginas_historia(tema) > PAGINAS_HISTORIA
    arco = (ARGUMENTOS_EXT if extendido else ARGUMENTOS).get(historia)
    if arco:
        return [_capitalizar_frases(t.format(**ctx)) for t in arco]
    base = [
        "Esta noche, antes de dormir, %s encontró una invitación brillante debajo "
        "de la almohada. Decía: «Te esperamos en %s»." % (nombre, h["mundo"]),
        "Al cerrar los ojos y %s, la habitación se llenó de luces de colores. "
        "¡El viaje había comenzado!" % conteo,
        "En %s, %s recibieron a %s con una gran fiesta de bienvenida."
        % (h["mundo"], h["amigos"], nombre),
        "Pero de pronto todo se detuvo: %s. Nadie sabía qué hacer... "
        "nadie, excepto %s." % (h["desafio"], nombre),
        "Con valentía y una gran sonrisa, %s %s. ¡Todos festejaron su ingenio!"
        % (nombre, h["solucion"]),
        "Como agradecimiento, %s le regalaron %s: un recuerdo para siempre."
        % (h["amigos"], h["tesoro"]),
    ]
    cierre = ("De vuelta en casa, %s se durmió con una sonrisa. Porque quien es "
              "valiente y ayuda a los demás, siempre tiene una nueva aventura "
              "esperando." % nombre)
    if not extendido:
        return [_capitalizar_frases(t) for t in base + [cierre]]
    return [_capitalizar_frases(t) for t in base + [
        "Para festejar, %s propusieron un juego gigante en %s, y todos se "
        "turnaron para inventar la payasada más divertida."
        % (h["amigos"], h["mundo"]),
        "De repente, una música suave los llevó hasta un rincón secreto de %s "
        "que %s nunca le habían mostrado a nadie." % (h["mundo"], h["amigos"]),
        "Ahí, %s descubrió algo mágico: un pequeño jardín de luces que solo se "
        "veía cuando todos estaban juntos y felices." % nombre,
        "%s prometió cuidar ese secreto junto con %s, y todos se abrazaron "
        "fuerte antes de despedirse por ese día." % (nombre, h["amigos"]),
        "El cielo se llenó de colores mientras %s y %s se decían adiós, "
        "sabiendo que el jardín de luces los esperaría en la próxima visita."
        % (nombre, h["amigos"]),
        cierre,
    ]]


# ── escena ilustrada (base procedural; se reemplaza por arte IA vía override) ─
def _cielo(im, box, top, bottom):
    """Degradé vertical simple dentro de box (resize de una columna de 1px)."""
    x0, y0, x1, y1 = box
    h = max(2, y1 - y0)
    col = Image.new("RGB", (1, h))
    for i in range(h):
        t = i / (h - 1)
        col.putpixel((0, i), tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    im.paste(col.resize((max(1, x1 - x0), h)), (x0, y0))


def _estrella(dr, cx, cy, r, color):
    pts = [(cx + (r if i % 2 == 0 else r * 0.45) * math.cos(-math.pi / 2 + i * math.pi / 5),
            cy + (r if i % 2 == 0 else r * 0.45) * math.sin(-math.pi / 2 + i * math.pi / 5))
           for i in range(10)]
    dr.polygon(pts, fill=color)


# ── motivos narrativos: cada página dibuja LO QUE CUENTA su texto ────────────
_COLS = [(224, 85, 107), (63, 167, 214), (232, 155, 44), (95, 184, 122),
         (139, 91, 210), (255, 214, 98)]


def _dash(dc, pts, color, width=7, dash=26):
    """Línea punteada siguiendo la polilínea pts (para caminos/senderos)."""
    import itertools
    total = 0
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        n = max(1, int(L // dash))
        for i in range(0, n, 2):
            t0, t1 = i / n, min(1, (i + 1) / n)
            dc.line([ax + (bx - ax) * t0, ay + (by - ay) * t0,
                     ax + (bx - ax) * t1, ay + (by - ay) * t1], fill=color, width=width)
        total += L


def _m_dormitorio(dc, W, H, acc, rnd):
    """Pág. 1: la cama y la invitación brillante debajo de la almohada."""
    bx0, bx1, by0, by1 = W * 0.24, W * 0.76, H * 0.50, H * 0.80
    dc.rounded_rectangle([bx0 - W * 0.05, by0 - H * 0.14, bx0 + W * 0.01, by1], 18,
                         fill=(139, 94, 60))                       # respaldo
    dc.rounded_rectangle([bx0, by0, bx1, by1], 24, fill=_tint(acc, 0.30))   # colchón/manta
    dc.rounded_rectangle([bx0, by0 + (by1 - by0) * 0.42, bx1, by1], 24, fill=acc)  # frazada
    dc.ellipse([bx0 + W * 0.02, by0 - H * 0.045, bx0 + W * 0.20, by0 + H * 0.055],
               fill=(255, 255, 255))                               # almohada
    # el sobre brillante (asomando sobre la almohada)
    sx0, sy0, sx1, sy1 = bx0 + W * 0.055, by0 - H * 0.145, bx0 + W * 0.165, by0 - H * 0.045
    dc.rounded_rectangle([sx0, sy0, sx1, sy1], 8, fill=(255, 248, 214), outline=GOLD, width=4)
    dc.line([sx0, sy0, (sx0 + sx1) / 2, (sy0 + sy1) / 2], fill=GOLD, width=4)
    dc.line([sx1, sy0, (sx0 + sx1) / 2, (sy0 + sy1) / 2], fill=GOLD, width=4)
    for dx, dy in ((-0.035, -0.03), (0.16, -0.05), (0.13, 0.02)):
        _estrella(dc, sx0 + W * dx, sy0 + H * dy, 14, GOLD)


def _m_luces(dc, W, H, acc, rnd):
    """Pág. 2: la habitación se llena de luces de colores (espiral mágica)."""
    cx, cy = W / 2, H * 0.46
    for i in range(30):
        ang = i * 0.55
        rad = W * 0.03 + i * W * 0.013
        r = 10 + (i % 4) * 4
        px, py = cx + rad * math.cos(ang), cy + rad * 0.72 * math.sin(ang)
        dc.ellipse([px - r, py - r, px + r, py + r], fill=_COLS[i % len(_COLS)])
    for _ in range(8):
        _estrella(dc, rnd.randint(40, W - 40), rnd.randint(30, H - 60),
                  rnd.randint(10, 18), (255, 250, 220))


def _m_fiesta(dc, W, H, acc, rnd):
    """Pág. 3 (y portada): fiesta de bienvenida — banderines, globos y torta."""
    # banderines colgados de una cuerda
    for lado in (0, 1):
        x0, y0 = (0, H * 0.03) if lado == 0 else (W * 0.52, H * 0.16)
        x1, y1 = (W * 0.48, H * 0.16) if lado == 0 else (W, H * 0.03)
        dc.line([x0, y0, x1, y1], fill=(120, 110, 130), width=4)
        for i in range(6):
            t = (i + 0.5) / 6
            px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            dc.polygon([(px - 22, py), (px + 22, py), (px, py + 44)],
                       fill=_COLS[(i + lado) % len(_COLS)])
    # globos
    for i, fx in enumerate((0.14, 0.26, 0.76, 0.88)):
        gx, gy = W * fx, H * (0.36 + (i % 2) * 0.08); r = W * 0.045
        dc.line([gx, gy + r * 1.2, gx, gy + r * 1.2 + H * 0.14], fill=(120, 110, 130), width=3)
        dc.ellipse([gx - r, gy - r * 1.2, gx + r, gy + r * 1.2], fill=_COLS[i % len(_COLS)])
    # torta
    tx, ty, tw, th = W * 0.5, H * 0.66, W * 0.115, H * 0.075
    dc.rounded_rectangle([tx - tw, ty, tx + tw, ty + th], 16, fill=_COLS[2])
    dc.rounded_rectangle([tx - tw * 0.72, ty - th * 0.8, tx + tw * 0.72, ty], 12, fill=_COLS[0])
    for k in range(3):
        vx = tx - tw * 0.45 + k * tw * 0.45
        dc.line([vx, ty - th * 0.8, vx, ty - th * 1.5], fill=(63, 167, 214), width=5)
        dc.ellipse([vx - 7, ty - th * 1.75, vx + 7, ty - th * 1.5], fill=(255, 214, 98))


def _m_problema(dc, W, H, acc, rnd):
    """Pág. 4: el problema — nube gris grande con un signo de pregunta."""
    cx, cy = W * 0.5, H * 0.26
    for dx, dy, r in ((0, 0, W * 0.13), (-W * 0.12, H * 0.03, W * 0.095),
                      (W * 0.12, H * 0.03, W * 0.095), (0, H * 0.055, W * 0.11)):
        dc.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(172, 172, 186))
    dc.text((cx, cy + H * 0.01), "?", font=_font(int(H * 0.17)), fill="white", anchor="mm")
    # caminos que se separan (¿por dónde ir?)
    _dash(dc, [(W * 0.5, H * 0.88), (W * 0.42, H * 0.70), (W * 0.20, H * 0.56)], (255, 255, 255), 7)
    _dash(dc, [(W * 0.5, H * 0.88), (W * 0.58, H * 0.70), (W * 0.80, H * 0.56)], (255, 255, 255), 7)


def _m_solucion(dc, W, H, acc, rnd):
    """Pág. 5: la solución — el árbol más alto con el sendero descubierto."""
    tx, tw = W * 0.66, W * 0.028
    dc.rounded_rectangle([tx - tw, H * 0.36, tx + tw, H * 0.80], 10, fill=(139, 94, 60))
    for dx, dy, r in ((0, -0.06, 0.105), (-0.085, 0.0, 0.085), (0.085, 0.0, 0.085),
                      (0, 0.065, 0.09)):
        dc.ellipse([tx + W * dx - W * r, H * 0.30 + H * dy - W * r,
                    tx + W * dx + W * r, H * 0.30 + H * dy + W * r], fill=(95, 184, 122))
    _estrella(dc, tx, H * 0.145, 26, GOLD)      # la meta, bien arriba
    _dash(dc, [(W * 0.10, H * 0.86), (W * 0.30, H * 0.78), (W * 0.48, H * 0.82),
               (tx, H * 0.80)], (255, 255, 255), 7)


def _m_tesoro(dc, W, H, acc, rnd):
    """Pág. 6: el regalo/tesoro de agradecimiento."""
    gx0, gx1, gy0, gy1 = W * 0.40, W * 0.60, H * 0.42, H * 0.68
    dc.rounded_rectangle([gx0, gy0, gx1, gy1], 14, fill=acc)
    dc.rounded_rectangle([gx0 - W * 0.02, gy0 - H * 0.07, gx1 + W * 0.02, gy0], 10,
                         fill=_tint(acc, 0.25))
    dc.rectangle([(gx0 + gx1) / 2 - W * 0.018, gy0 - H * 0.07, (gx0 + gx1) / 2 + W * 0.018, gy1],
                 fill=(255, 250, 220))
    for s in (-1, 1):   # moño
        dc.ellipse([(gx0 + gx1) / 2 + (s * W * 0.055) - W * 0.045, gy0 - H * 0.135,
                    (gx0 + gx1) / 2 + (s * W * 0.055) + W * 0.045, gy0 - H * 0.065],
                   outline=(255, 250, 220), width=8)
    for fx, fy in ((0.30, 0.36), (0.70, 0.34), (0.26, 0.62), (0.74, 0.62), (0.5, 0.28)):
        _estrella(dc, W * fx, H * fy, 16, GOLD)


def _m_casa(dc, W, H, acc, rnd):
    """Pág. 7: de vuelta en casa, a dormir (casita de noche, ventana encendida)."""
    hx0, hx1, hy0, hy1 = W * 0.36, W * 0.64, H * 0.42, H * 0.76
    dc.polygon([(hx0 - W * 0.04, hy0), (hx1 + W * 0.04, hy0), ((hx0 + hx1) / 2, H * 0.24)],
               fill=acc)                                            # techo
    dc.rectangle([hx0, hy0, hx1, hy1], fill=(246, 240, 228))        # cuerpo
    dc.rounded_rectangle([hx0 + W * 0.035, hy0 + H * 0.13, hx0 + W * 0.10, hy1], 8,
                         fill=(139, 94, 60))                        # puerta
    vx0, vy0 = hx1 - W * 0.115, hy0 + H * 0.055                     # ventana encendida
    dc.rounded_rectangle([vx0, vy0, vx0 + W * 0.08, vy0 + H * 0.09], 6,
                         fill=(255, 224, 120), outline=(139, 94, 60), width=4)
    dc.line([vx0 + W * 0.04, vy0, vx0 + W * 0.04, vy0 + H * 0.09], fill=(139, 94, 60), width=3)
    dc.line([vx0, vy0 + H * 0.045, vx0 + W * 0.08, vy0 + H * 0.045], fill=(139, 94, 60), width=3)
    for i, (dx, dy) in enumerate(((0.03, -0.05), (0.065, -0.10), (0.10, -0.15))):
        dc.text((hx1 + W * dx, vy0 + H * dy), "z", font=_font(30 + i * 12),
                fill=(255, 250, 220), anchor="mm")


_MOTIVOS = [_m_dormitorio, _m_luces, _m_fiesta, _m_problema, _m_solucion, _m_tesoro, _m_casa]
_NOCTURNOS = (_m_dormitorio, _m_casa)
_INTERIORES = (_m_dormitorio, _m_luces)   # sin colinas (pasan adentro / en la magia)


def _escena(im, dr, box, tema, pagina, acc, motivo=None, idx_pieza=None):
    """Ilustración de una página que REPRESENTA lo que cuenta el texto. Si hay
    ilustración override para idx_pieza (subida por el dash o generada con IA),
    va esa. Si no, la escena procedural: cada página de historia tiene su motivo
    (_MOTIVOS[n]): cama+invitación → luces mágicas → fiesta → problema (nube con ?)
    → solución (árbol y sendero) → tesoro → casita de noche. Encima van los
    personajes del tema. Determinística (misma página -> misma escena). Se pinta en
    una capa aparte y se pega con máscara redondeada, así nada se desborda del panel."""
    if idx_pieza is not None and _panel_ilustracion(im, dr, box, tema, idx_pieza, acc):
        return
    x0, y0, x1, y1 = box
    W = x1 - x0; H = y1 - y0
    rnd = random.Random("%s-%d" % (tema, pagina))
    if motivo is None:
        motivo = _MOTIVOS[pagina] if 0 <= pagina < len(_MOTIVOS) else _m_fiesta
    noche = motivo in _NOCTURNOS
    magico = motivo is _m_luces
    capa = Image.new("RGBA", (W, H))
    dc = ImageDraw.Draw(capa)
    if noche:
        _cielo(capa, (0, 0, W, H), (44, 42, 92), (108, 100, 168))
    elif magico:
        _cielo(capa, (0, 0, W, H), (66, 52, 120), (140, 120, 200))
    else:
        _cielo(capa, (0, 0, W, H), _tint(acc, 0.55), _tint(acc, 0.88))
    # colinas / piso
    if motivo not in _INTERIORES:
        for k, p in enumerate((0.35, 0.18)):
            hy = H - int(H * (0.30 - k * 0.13))
            col = _tint(acc, p) if not noche else _tint((44, 42, 92), 0.25 + k * 0.2)
            dc.ellipse([-W * 0.3 + k * W * 0.5, hy, W * 0.9 + k * W * 0.5, H + H * 0.5], fill=col)
    elif motivo is _m_dormitorio:
        dc.rectangle([0, H * 0.78, W, H], fill=_tint(acc, 0.20))    # piso del cuarto
    if noche:
        dc.ellipse([W * 0.76, H * 0.06, W * 0.88, H * 0.06 + W * 0.12], fill=(250, 245, 210))
        for _ in range(12):
            _estrella(dc, rnd.randint(30, W - 30), rnd.randint(20, int(H * 0.4)),
                      rnd.randint(8, 15), (255, 250, 220))
    elif not magico:
        # sol con rayos + nubes
        scx, scy, sr = W * 0.13, H * 0.06 + W * 0.06, W * 0.06
        for i in range(12):
            a = i * math.pi / 6
            dc.line([scx + sr * 1.15 * math.cos(a), scy + sr * 1.15 * math.sin(a),
                     scx + sr * 1.5 * math.cos(a), scy + sr * 1.5 * math.sin(a)],
                    fill=(255, 214, 98), width=9)
        dc.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=(255, 214, 98))
        for _ in range(2):
            nx = rnd.randint(int(W * 0.30), int(W * 0.85)); ny = rnd.randint(40, int(H * 0.22))
            for dx, dy, r in ((0, 0, 40), (-36, 10, 30), (38, 12, 30)):
                dc.ellipse([nx + dx - r, ny + dy - r, nx + dx + r, ny + dy + r],
                           fill=(255, 255, 255))
    # el motivo narrativo de la página
    motivo(dc, W, H, acc, rnd)
    # personajes del tema acompañando (salvo en el dormitorio, que es "antes del viaje")
    mons = _personajes(tema, 4) if motivo is not _m_dormitorio else []
    if mons:
        posiciones = [(0.22, 0.78, 0.34), (0.82, 0.76, 0.30), (0.5, 0.84, 0.24)]
        rnd.shuffle(mons)
        for (fx, fy, fh), m in zip(posiciones[:1 + pagina % 3], mons):
            _paste_h(capa, m, W * fx, H * fy, H * fh)
    # pegar con máscara redondeada (recorta lo que sobresale) + marco
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], 36, fill=255)
    im.paste(capa, (x0, y0), mask)
    dr.rounded_rectangle(box, 36, outline=_tint(acc, 0.25), width=6)


# ── ilustraciones subidas / generadas con IA (override POR ESCENA) ───────────
# ── arte por VENTA (libro premium) ───────────────────────────────────────────
# El libro premium ilustra cada pedido con arte único (libro_ia con dest_dir).
# usar_escenas_dir() redirige _panel_ilustracion a ese directorio mientras se
# renderizan las páginas del pedido. Thread-local: la generación premium corre en
# su propio hilo (servicio._api_generar) y no pisa los renders concurrentes del
# dash ni de otros pedidos.
_ESCENAS_LOCAL = threading.local()


@contextlib.contextmanager
def usar_escenas_dir(path):
    """Dentro del with, las ilustraciones salen de <path>/<idx>.png (si existen)
    en vez de los overrides del tema. Para el libro premium (arte por pedido)."""
    prev = getattr(_ESCENAS_LOCAL, "dir", None)
    _ESCENAS_LOCAL.dir = path
    try:
        yield
    finally:
        _ESCENAS_LOCAL.dir = prev


@contextlib.contextmanager
def usar_genero(genero):
    """Dentro del with, el arte de las escenas prefiere la variante por género
    (<idx>_nena.png / <idx>_nene.png) si existe — para que 'Valentina' no aparezca
    con un nene dibujado en las páginas donde está el protagonista."""
    prev = getattr(_ESCENAS_LOCAL, "genero", None)
    g = (genero or "").strip().lower()
    _ESCENAS_LOCAL.genero = "nena" if g in ("nena", "niña", "nina", "f") else \
                            ("nene" if g in ("nene", "niño", "nino", "varon", "varón", "m") else None)
    try:
        yield
    finally:
        _ESCENAS_LOCAL.genero = prev


def _escena_efectiva_path(tema, idx):
    """Path del arte de la página idx: primero el del pedido premium (si este hilo
    está dentro de usar_escenas_dir), después el override del tema."""
    d = getattr(_ESCENAS_LOCAL, "dir", None)
    if d:
        p = os.path.join(d, "%d.png" % int(idx))
        if os.path.isfile(p):
            return p
    g = getattr(_ESCENAS_LOCAL, "genero", None)
    if g:
        base = override_escena_path(tema, idx)
        pg = base.replace(".png", "_%s.png" % g)
        if os.path.isfile(pg):
            return pg
    return override_escena_path(tema, idx)


def override_escena_path(tema, idx):
    """La ILUSTRACIÓN de la página idx (0..9): temas/<tema>/overrides/libro/<idx>.png.
    A diferencia del resto de los productos, en el libro el override NO reemplaza la
    página completa: es solo el ARTE de la escena, y el motor sigue escribiendo el
    texto personalizado encima (si tapara la página entera, el nombre del chico
    quedaría fijo dentro de la imagen). Por eso productos.piezas_tipo saltea el
    override genérico para el tipo 'libro'. La imagen llega acá de dos maneras:
    subida a mano por el dash (botón 📤 de la pieza) o generada con IA (libro_ia.py)."""
    import temas as _temas
    return os.path.join(_temas.TEMAS_DIR, tema or "safari", "overrides", "libro",
                        "%d.png" % int(idx))


def _cover(img, W, H, anchor_y=0.5):
    """Escala y recorta la imagen para CUBRIR WxH (estilo object-fit: cover).
    anchor_y: qué parte conservar si sobra alto (0=arriba, 1=abajo). Las
    ilustraciones ancladas abajo (0.78) sacrifican cielo, nunca personajes:
    en los cuentos los personajes pisan el piso — un recorte centrado les
    cortaba la cara (safari pág 4) y ni el QA de visión lo detectaba."""
    s = max(W / img.width, H / img.height)
    im2 = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)
    x = (im2.width - W) // 2
    y = int((im2.height - H) * anchor_y)
    return im2.crop((x, y, x + W, y + H))


def _panel_ilustracion(im, dr, box, tema, idx, acc):
    """Si hay ilustración override para la página idx, la pega en el panel (cover +
    máscara redondeada + marco) y devuelve True. Si no hay, False (escena procedural)."""
    p = _escena_efectiva_path(tema, idx)
    if not os.path.isfile(p):
        return False
    x0, y0, x1, y1 = box
    W, H = x1 - x0, y1 - y0
    art = _cover(Image.open(p).convert("RGBA"), W, H, anchor_y=0.78)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], 36, fill=255)
    im.paste(art, (x0, y0), mask)
    dr.rounded_rectangle(box, 36, outline=_tint(acc, 0.25), width=6)
    return True


def _pie(dr, acc, y=Hp - 52):
    dr.text((Wp / 2, y), "casatridimensional.com.ar",
            font=_font(20, False), fill=_tint(acc, 0.35), anchor="mm")


def _fit_fs(nombre, fs, maxw):
    while _font(fs).getlength(nombre) > maxw and fs > 40:
        fs -= 4
    return fs


# ── páginas ──────────────────────────────────────────────────────────────────
def portada(data, tema="safari"):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    edad = str(data.get("edad") or "").strip()
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    _cielo(im, (0, 0, Wp, Hp), _tint(acc, 0.80), _tint(acc, 0.95))
    dr.rounded_rectangle([55, 55, Wp - 55, Hp - 55], 40, outline=acc, width=8)
    dr.rounded_rectangle([80, 80, Wp - 80, Hp - 80], 30, outline=_tint(acc, 0.55), width=3)
    dr.text((Wp / 2, 330), "La gran aventura de", font=_font(66, False), fill=INK, anchor="mm")
    fs = _fit_fs(nombre, 170, Wp - 320)
    dr.text((Wp / 2, 480), nombre, font=_font(fs), fill=acc, anchor="mm")
    etiqueta = ("Un cuento personalizado · %s años" % edad) if edad else "Un cuento personalizado"
    ew = max(520, _font(36).getlength(etiqueta) + 90)
    dr.rounded_rectangle([Wp / 2 - ew / 2, 585, Wp / 2 + ew / 2, 665], 40, fill=acc)
    dr.text((Wp / 2, 625), etiqueta, font=_font(36), fill="white", anchor="mm")
    _escena(im, dr, (140, 760, Wp - 140, Hp - 260), tema, -1, acc, motivo=_m_fiesta,
            idx_pieza=0)
    _estrella(dr, Wp / 2, Hp - 165, 34, GOLD)
    # la portada tiene marco doble hasta Hp-55 (las demás páginas no) — el pie
    # sube para no quedar tapado por esa línea
    _pie(dr, acc, y=Hp - 100)
    return im


def dedicatoria(data, tema="safari"):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    dedic = (str(data.get("dedicatoria") or "").strip()) or \
        "Que nunca dejes de soñar, de jugar y de creer en vos."
    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([90, 90, Wp - 90, Hp - 90], 40, outline=_tint(acc, 0.4), width=4)
    dr.text((Wp / 2, 420), "Este cuento pertenece a", font=_font(44, False), fill=INK, anchor="mm")
    fs = _fit_fs(nombre, 120, Wp - 360)
    dr.text((Wp / 2, 560), nombre, font=_font(fs), fill=acc, anchor="mm")
    dr.line([Wp * 0.28, 650, Wp * 0.72, 650], fill=_tint(acc, 0.45), width=3)
    _estrella(dr, Wp * 0.24, 650, 18, GOLD); _estrella(dr, Wp * 0.76, 650, 18, GOLD)
    _parrafo(dr, "“" + dedic + "”", Wp / 2, 800, _font(40, False), INK, Wp - 420)
    if not _panel_ilustracion(im, dr, (270, 1010, Wp - 270, Hp - 220), tema, 1, acc):
        mons = _personajes(tema, 1)
        if mons:
            _paste_h(im, mons[0], Wp / 2, Hp - 460, 320)
    _pie(dr, acc)
    return im


def pagina_historia(n, data, tema="safari", catalogo=False):
    """Página n del cuento: escena ilustrada arriba + texto abajo + número."""
    acc = _accent(tema)
    textos = cuento(data, tema, catalogo)
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    _escena(im, dr, (90, 90, Wp - 90, int(Hp * 0.60)), tema, n, acc, idx_pieza=n + 2)
    # banda de texto
    dr.rounded_rectangle([90, int(Hp * 0.63), Wp - 90, Hp - 150], 36, fill=CREAM + (255,),
                         outline=_tint(acc, 0.5), width=3)
    _parrafo(dr, textos[n], Wp / 2, int(Hp * 0.63) + 90, _font(42, False), INK, Wp - 340, lh=1.45)
    # número de página (portada y dedicatoria no cuentan)
    dr.ellipse([Wp / 2 - 44, Hp - 190, Wp / 2 + 44, Hp - 102], fill=acc)
    dr.text((Wp / 2, Hp - 146), str(n + 1), font=_font(44), fill="white", anchor="mm")
    _pie(dr, acc)
    return im


def fin(data, tema="safari", catalogo=False):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    ov = _escena_efectiva_path(tema, total_paginas(tema, data.get("edad"), data.get("historia"), catalogo) - 1)
    if os.path.isfile(ov):
        # ilustración a página completa + banda oscura translúcida para que el
        # FIN y el mensaje se lean sobre cualquier arte
        im.paste(_cover(Image.open(ov).convert("RGBA"), Wp, Hp), (0, 0))
        velo = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
        ImageDraw.Draw(velo).rounded_rectangle(
            [Wp * 0.12, Hp * 0.22, Wp * 0.88, Hp * 0.60], 46, fill=(44, 42, 92, 170))
        im.alpha_composite(velo)
    else:
        _cielo(im, (0, 0, Wp, Hp), (44, 42, 92), (108, 100, 168))
        rnd = random.Random(tema + "-fin")
        puestas = 0
        while puestas < 26:
            sx, sy = rnd.randint(120, Wp - 120), rnd.randint(120, Hp - 320)
            if Hp * 0.24 < sy < Hp * 0.58 and Wp * 0.14 < sx < Wp * 0.86:
                continue    # no pisar el FIN ni el mensaje
            _estrella(dr, sx, sy, rnd.randint(8, 20), (255, 250, 220))
            puestas += 1
        mons = _personajes(tema, 3)
        for fx, m in zip((0.28, 0.5, 0.72), mons):
            _paste_h(im, m, Wp * fx, Hp - 420, 260)
    dr.rounded_rectangle([70, 70, Wp - 70, Hp - 70], 40, outline=_tint(acc, 0.6), width=6)
    dr.text((Wp / 2, Hp * 0.34), "FIN", font=_font(220), fill=(255, 250, 220), anchor="mm")
    _parrafo(dr, "Y colorín colorado, la aventura de %s apenas ha comenzado." % nombre,
             Wp / 2, int(Hp * 0.48), _font(44, False), (238, 234, 255), Wp - 360, lh=1.45)
    dr.text((Wp / 2, Hp - 130), "Un cuento hecho especialmente para vos",
            font=_font(30, False), fill=(210, 204, 240), anchor="mm")
    _pie(dr, acc)
    return im


def pagina_libro(idx, data, tema="safari", catalogo=False):
    """Página idx del libro: 0=portada, 1=dedicatoria, 2..N=historia, última=fin."""
    if idx == 0:
        return portada(data, tema)
    if idx == 1:
        return dedicatoria(data, tema)
    if idx == total_paginas(tema, data.get("edad"), data.get("historia"), catalogo) - 1:
        return fin(data, tema, catalogo)
    return pagina_historia(idx - 2, data, tema, catalogo)


def paginas_libro(data, tema="safari", catalogo=False):
    n = total_paginas(tema, data.get("edad"), data.get("historia"), catalogo)
    return [pagina_libro(i, data, tema, catalogo) for i in range(n)]


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Valentina"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/libro"
    os.makedirs(out, exist_ok=True)
    for i, pg in enumerate(paginas_libro({"nombre": nombre, "edad": "4",
                                          "dedicatoria": "Para la aventurera de la casa."}, tema)):
        pg.convert("RGB").save(os.path.join(out, "%02d.png" % i))
    print("OK ->", out)
