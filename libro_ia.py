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
import json
import os
import sys

from PIL import Image

import libro

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")

_CUADRADA = "1024x1024"
_VERTICAL = "1024x1536"
_APAISADA = "1536x1024"

# Qué ilustrar en cada página (0..9). El protagonista va "de espaldas / a lo lejos"
# para que funcione con cualquier chico (la cara nunca se ve).
_ESCENAS = [
    "Portada: una escena vistosa y alegre de {mundo}, con los personajes del tema "
    "celebrando. Composición con AIRE en el tercio superior (ahí va el título después).",
    # Esta página lleva escrito "Este cuento pertenece a <nombre>": el dibujo tiene que
    # ser EL CHICO DEL CUENTO, no un personaje cualquiera del tema. Decía "un personaje
    # del tema" —ambiguo— y cada temática lo interpretó a su manera: bomberos dibujó al
    # elenco saludando (sirve), pero superhéroes dibujó UN nene secundario, distinto al
    # protagonista de la portada. Pablo lo notó al instante (26-jul-2026): "hay un chico
    # morocho que es un superheroe que no es el nene o nena protagonista". Y esa misma
    # imagen es la de la MUESTRA de la ficha, o sea que estaba en la vidriera.
    # {protagonista} ya resuelve el género y lo dibuja siempre de espaldas (la cara nunca
    # se ve), así que funciona con cualquier chico.
    # Redacción sin concordancia de género a propósito: {protagonista} puede ser «una
    # nena…» o «un nene…», y un participio como «acompañado» quedaba mal en femenino.
    "Viñeta tierna y cálida de bienvenida: en primer plano {protagonista}, y a lo lejos "
    "los personajes del tema en {mundo}. Fondo muy claro y despejado, estilo página "
    "de dedicatoria.",
    "Un dormitorio infantil de noche, acogedor: una cama con almohada y un sobre "
    "dorado brillante que asoma bajo la almohada, luz de luna por la ventana.",
    "Un remolino mágico de luces de colores llenando un dormitorio de noche, "
    "destellos y estrellas, sensación de comienzo de viaje.",
    "Una gran fiesta de bienvenida en {mundo}: banderines, globos y una torta, con "
    "los personajes del tema festejando alrededor de {protagonista}.",
    "Momento de preocupación en {mundo}: {desafio}. Los personajes del tema miran "
    "preocupados, cielo con una gran nube gris.",
    "Momento heroico: {protagonista} que {solucion}, mientras "
    "los personajes del tema alientan felices.",
    "Los personajes del tema regalan {tesoro}, presentado brillante y destacado en "
    "el centro de la escena, con destellos dorados.",
    "Una casita de noche con una ventana iluminada cálida, cielo estrellado con "
    "luna, los personajes del tema despidiéndose a lo lejos.",
    "Cielo nocturno estrellado sereno con los personajes del tema despidiéndose, "
    "composición VERTICAL con mucho AIRE despejado en el centro (ahí va la palabra "
    "FIN después).",
]


_ESCENAS_EXT = [
    _ESCENAS[0], _ESCENAS[1],
    _ESCENAS[2], _ESCENAS[3], _ESCENAS[4], _ESCENAS[5], _ESCENAS[6], _ESCENAS[7],
    "Un gran juego grupal en {mundo}: los personajes del tema jugando y riendo a "
    "carcajadas, ambiente muy alegre y colorido.",
    "Un rincón secreto y mágico de {mundo}, con una luz suave y misteriosa "
    "guiando el camino, sensación de descubrimiento.",
    "Un jardín mágico de pequeñas luces brillantes flotando como estrellas "
    "caídas, {protagonista} y los personajes del tema maravillados mirando "
    "alrededor.",
    "Los personajes del tema abrazados en ronda junto a {protagonista}, "
    "prometiendo guardar un secreto, ambiente cálido y tierno.",
    "Un cielo lleno de colores de atardecer sobre {mundo}, los personajes del "
    "tema despidiéndose con una sonrisa cálida, sensación de final feliz.",
    _ESCENAS[8],   # cierre (misma escena que el legado, ahora más adelante)
    _ESCENAS[9],   # FIN
]


# Escenas por ARGUMENTO (idx 2..8 — portada/dedicatoria/fin son comunes): el arte
# por pedido (premium/audiolibro) ilustra la historia que el cliente eligió.
_ESCENAS_POR_HISTORIA = {
    "tesoro": {
        2: "{protagonista} descubriendo un mapa antiguo brillante que sale de una mochila, en un cuarto infantil cálido.",
        3: "Un mapa del tesoro desplegado que brilla con destellos dorados, comienzo de aventura, en {mundo}.",
        4: "{protagonista} y los personajes del tema mirando juntos un mapa del tesoro en {mundo}, señalando pistas.",
        5: "Un río ancho cruzando {mundo}; los personajes del tema miran preocupados desde la orilla.",
        6: "{protagonista} cruzando un puente improvisado de troncos y sogas sobre el río, los personajes del tema festejando; un cofre dorado asoma del otro lado.",
        7: "Un cofre del tesoro abierto irradiando luz dorada con {tesoro} adentro, los personajes del tema celebrando alrededor.",
        8: "Una casita de noche con ventana cálida iluminada, cielo estrellado, un mapa enrollado apoyado junto a la cama.",
    },
    "rescate": {
        2: "Una lucecita mágica golpeando la ventana de un cuarto infantil de noche, sensación de mensaje urgente.",
        3: "{protagonista} volando por el cielo llevado por el viento hacia {mundo}, estrellas y nubes.",
        4: "Los personajes del tema preocupados buscando a un nene pequeño perdido en {mundo}, atardecer.",
        5: "Huellas pequeñitas en el suelo de {mundo} que llevan hacia una cueva; los personajes del tema las siguen con linternas.",
        6: "{protagonista} saliendo de una cueva de la mano de un nene pequeño del tema (un niño, NO un animal), los demás celebrando felices.",
        7: "Los personajes del tema entregando {tesoro} brillante y destacado en el centro, con destellos dorados, ceremonia de héroes.",
        8: "Un cuarto infantil de noche, un chico dormido con sonrisa... mejor: la casita de noche con ventana cálida y una lucecita mágica despidiéndose.",
    },
    "gran-dia": {
        2: "Una carta de invitación gigante y festiva llegando a un cuarto infantil, confetti saliendo del sobre.",
        3: "{protagonista} con mochila caminando con paso decidido hacia {mundo}, camino soleado con banderines a lo lejos.",
        4: "Los personajes del tema preparando una gran fiesta en {mundo}: guirnaldas, música, juegos, mucha actividad alegre.",
        5: "Una tormenta con viento desarmando las decoraciones de la fiesta en {mundo}; los personajes del tema mirando sorprendidos.",
        6: "{protagonista} organizando a los personajes del tema para reconstruir la fiesta: todos ayudando juntos, decoraciones volviendo a su lugar, trabajo en equipo.",
        7: "La gran fiesta espléndida de noche en {mundo} con luces y {tesoro} siendo entregado en el centro con destellos dorados.",
        8: "Cielo nocturno estrellado sereno sobre {mundo}, los personajes del tema despidiéndose a lo lejos con una sonrisa.",
    },
}

# Versión extendida (12 páginas, idx 2..13) de las mismas 3 narrativas de arriba +
# las narrativas nuevas (que ya nacen extendidas). idx 2..7 = misma escena que la
# versión legado (páginas sin cambios); idx 8..12 = las 5 páginas nuevas del medio;
# idx 13 = la escena de cierre (la que en el legado estaba en idx 8).
_ESCENAS_POR_HISTORIA_EXT = {
    "tesoro": {
        2: _ESCENAS_POR_HISTORIA["tesoro"][2], 3: _ESCENAS_POR_HISTORIA["tesoro"][3],
        4: _ESCENAS_POR_HISTORIA["tesoro"][4], 5: _ESCENAS_POR_HISTORIA["tesoro"][5],
        6: _ESCENAS_POR_HISTORIA["tesoro"][6], 7: _ESCENAS_POR_HISTORIA["tesoro"][7],
        8: "Los personajes del tema sentados en ronda alrededor de {protagonista}, "
           "admirando de cerca {tesoro} que brilla en el centro, ambiente cálido.",
        9: "Un mapa antiguo que brilla y revela un segundo camino dorado, sorpresa "
           "y asombro en los personajes del tema.",
        10: "Los personajes del tema empujando juntos una piedra enorme en {mundo}, "
            "esfuerzo y trabajo en equipo, polvo de aventura.",
        11: "Una merienda alegre bajo un árbol grande en {mundo}, los personajes "
            "del tema compartiendo comida y riendo.",
        12: "{protagonista} y los personajes del tema reunidos en círculo mirando "
            "juntos el mapa en señal de promesa, atardecer cálido.",
        13: _ESCENAS_POR_HISTORIA["tesoro"][8],
    },
    "rescate": {
        2: _ESCENAS_POR_HISTORIA["rescate"][2], 3: _ESCENAS_POR_HISTORIA["rescate"][3],
        4: _ESCENAS_POR_HISTORIA["rescate"][4], 5: _ESCENAS_POR_HISTORIA["rescate"][5],
        6: _ESCENAS_POR_HISTORIA["rescate"][6], 7: _ESCENAS_POR_HISTORIA["rescate"][7],
        8: "Un nene pequeño del tema (un niño) abrazando fuerte y agradecido a "
           "{protagonista}, ambiente muy tierno.",
        9: "Los personajes del tema caminando juntos en fila por {mundo}, "
           "explorando con confianza.",
        10: "Un rincón mágico escondido de {mundo} lleno de lucecitas como "
            "estrellas caídas, los personajes del tema maravillados.",
        11: "Los personajes del tema decorando con cariño su nuevo rincón "
            "secreto favorito en {mundo}.",
        12: "Los personajes del tema cantando juntos en ronda de noche junto a "
            "las lucecitas mágicas, ambiente feliz y cálido.",
        13: _ESCENAS_POR_HISTORIA["rescate"][8],
    },
    "gran-dia": {
        2: _ESCENAS_POR_HISTORIA["gran-dia"][2], 3: _ESCENAS_POR_HISTORIA["gran-dia"][3],
        4: _ESCENAS_POR_HISTORIA["gran-dia"][4], 5: _ESCENAS_POR_HISTORIA["gran-dia"][5],
        6: _ESCENAS_POR_HISTORIA["gran-dia"][6], 7: _ESCENAS_POR_HISTORIA["gran-dia"][7],
        8: "{protagonista} con {tesoro} puesto, dando la bienvenida a los "
           "personajes del tema que van llegando a la fiesta en {mundo}.",
        9: "Un equipo de música apagado en medio de la fiesta, los personajes "
           "del tema con cara de sorpresa.",
        10: "{protagonista} organizando a los personajes del tema para hacer "
            "música con las manos y los pies, ambiente divertido.",
        11: "Los personajes del tema bailando felices al ritmo de la música "
            "improvisada, mucha energía y color.",
        12: "Los personajes del tema en ronda al atardecer en {mundo}, "
            "agradeciendo a {protagonista} con cariño.",
        13: _ESCENAS_POR_HISTORIA["gran-dia"][8],
    },
    "noche-estrellas": {
        2: "{protagonista} mirando el cielo nocturno desde la ventana de un "
           "cuarto infantil, viendo caer una estrella fugaz hacia {mundo}.",
        3: "{protagonista} en pantuflas saliendo de casa de noche, mirando el "
           "cielo estrellado, camino hacia {mundo}.",
        4: "Los personajes del tema buscando entre las sombras de {mundo} de "
           "noche, con linternas, buscando algo brillante.",
        5: "Momento de oscuridad y desafío en {mundo} de noche: {desafio}, los "
           "personajes del tema desorientados.",
        6: "{protagonista} que {solucion}, iluminando el camino en la "
           "oscuridad, los personajes del tema aliviados.",
        7: "Una estrella fugaz brillante y cansada posada en el suelo de "
           "{mundo}, los personajes del tema acercándose con ternura.",
        8: "Los personajes del tema armando una camita suave de nubes para la "
           "estrella fugaz, ambiente tierno y nocturno.",
        9: "La estrella fugaz brillando fuerte iluminando todo {mundo} como si "
           "fuera de día, luz cálida y mágica.",
        10: "Los personajes del tema jugando a las escondidas entre sombras "
            "iluminadas, mucha alegría.",
        11: "La estrella fugaz entregando {tesoro} brillante a {protagonista}, "
            "momento mágico de despedida.",
        12: "Los personajes del tema mirando juntos el cielo estrellado de "
            "{mundo}, prometiendo cuidarlo cada noche.",
        13: "Un cuarto infantil de noche, cama con ventana abierta al cielo "
            "estrellado, ambiente muy calmo.",
    },
    "cumple-sorpresa": {
        2: "{protagonista} descubriendo un cartel o calendario que marca un "
           "cumpleaños muy pronto, cara de sorpresa emocionada, en {mundo}.",
        3: "{protagonista} planeando en secreto con una libretita, gesto de "
           "'shhh', ambiente de misterio divertido.",
        4: "Los personajes del tema reunidos en secreto susurrando un plan, "
           "ambiente cómplice y divertido en {mundo}.",
        5: "Momento de tensión: {desafio}, los personajes del tema con cara de "
           "preocupación mientras preparan la sorpresa.",
        6: "{protagonista} que {solucion} justo a tiempo, salvando el plan "
           "secreto, alivio y sonrisas.",
        7: "Los personajes del tema decorando {mundo} con globos y "
           "guirnaldas, escondidos detrás de árboles y esquinas.",
        8: "El cumpleañero del tema acercándose sin sospechar nada, los demás "
           "personajes escondidos aguantando la risa.",
        9: "Explosión de sorpresa y alegría: confetti, globos, todos los "
           "personajes del tema festejando alrededor del cumpleañero.",
        10: "Una gran torta de cumpleaños festiva en el centro de {mundo}, los "
            "personajes del tema jugando y riendo alrededor.",
        11: "Los personajes del tema entregando {tesoro} hecho con cariño al "
            "cumpleañero, momento emotivo.",
        12: "El cumpleañero abrazando fuerte a {protagonista}, ambiente muy "
            "tierno y feliz.",
        13: "Una casita de noche con ventana cálida iluminada, globos "
            "desinflándose suavemente afuera, cierre tierno del día.",
    },
    "pequeno-maestro": {
        2: "{protagonista} haciendo algo especial y único frente a los "
           "personajes del tema, que miran admirados en {mundo}.",
        3: "Los personajes del tema pidiéndole con ilusión a {protagonista} "
           "que les enseñe, ambiente de entusiasmo.",
        4: "Primera clase improvisada en {mundo}: los personajes del tema "
           "intentando aprender, gestos torpes y divertidos.",
        5: "Momento de frustración: {desafio}, los personajes del tema "
           "desanimados, caras tristes.",
        6: "{protagonista} que {solucion}, animando con paciencia y una gran "
           "sonrisa a los personajes del tema.",
        7: "Los personajes del tema logrando poco a poco, caras de orgullo y "
           "sorpresa feliz.",
        8: "{protagonista} festejando cada intento de los personajes del "
           "tema, aplausos y ánimo, ambiente cálido.",
        9: "Cada personaje del tema mostrando su propio estilo único de hacer "
           "lo aprendido, variedad y color.",
        10: "Una pequeña muestra o exhibición en {mundo}, los personajes del "
            "tema mostrando lo aprendido con orgullo.",
        11: "Los personajes del tema festejando y entregando {tesoro} a "
            "{protagonista} como agradecimiento.",
        12: "{protagonista} con gesto pensativo y feliz, en medio de los personajes "
            "del tema, ambiente de cierre cálido.",
        13: "Una casita de noche con ventana cálida, libros o herramientas de "
            "aprendizaje apoyados cerca de la cama.",
    },
    "ayudar-a-todos": {
        2: "{protagonista} despertando con energía en un cuarto luminoso, "
           "ganas de hacer algo bueno, en {mundo}.",
        3: "{protagonista} caminando por {mundo} con botas puestas, buscando "
           "a quién ayudar, ambiente soleado.",
        4: "Un personaje del tema triste porque {desafio}, {protagonista} "
           "acercándose con gesto amable.",
        5: "{protagonista} que {solucion}, ayudando con una sonrisa, el "
           "personaje ya más animado.",
        6: "{protagonista} compartiendo su merienda de la mochila con un "
           "personaje del tema con hambre, gesto generoso.",
        7: "Los personajes del tema buscando juntos un juguete perdido entre "
           "plantas y rincones de {mundo}.",
        8: "Alegría de encontrar el juguete perdido, los personajes del tema "
           "festejando juntos.",
        9: "Los personajes del tema cargando algo pesado entre todos, trabajo "
           "en equipo, ambiente de esfuerzo alegre.",
        10: "Atardecer en {mundo}, los personajes del tema cansados pero "
            "sonrientes tras un día de buenas acciones.",
        11: "Los personajes del tema entregando {tesoro} a {protagonista} "
            "como agradecimiento por un día ayudando a todos.",
        12: "{protagonista} en medio de todos los personajes del tema en un "
            "abrazo grupal, ambiente muy cálido.",
        13: "Una casita de noche con ventana cálida iluminada, ambiente "
            "tranquilo tras un día de buenas acciones.",
    },
}


# ---------------------------------------------------------------------------
# Escenas de la versión LARGA (17 páginas de historia = 20 en total) del catálogo
# de audiolibros. idx 2..18 = las 17 páginas de historia (matchean 1:1 el texto de
# libro_historias.ARGUMENTOS_LARGO); portada (0), dedicatoria (1) y FIN (19) salen
# del fallback _ESCENAS_LARGO. En la versión corta (9 páginas, hasta 3 años) el
# render mapea cada página con libro.CORTO_IDX (ver prompt_pagina).
# ---------------------------------------------------------------------------
_AVENTURA_LARGO = [
    "Un dormitorio infantil de noche acogedor; {protagonista} asomándose a "
    "mirar un sobre dorado brillante que aparece bajo la almohada, luz de "
    "luna por la ventana.",
    "Un remolino mágico de luces de colores rodeando a {protagonista} en un "
    "dormitorio de noche, destellos y estrellas, sensación de comienzo de "
    "viaje.",
    "{protagonista} llegando a {mundo}, un lugar enorme y mágico, mirando todo "
    "con asombro.",
    "Una fiesta de bienvenida en {mundo} con banderines y globos, los personajes "
    "del tema alrededor de {protagonista}; al fondo, en lo alto, un gran farol "
    "apagado y gris.",
    "Los personajes del tema explicando con gestos suaves a {protagonista}, "
    "señal de noche que no termina; el gran farol apagado a lo lejos.",
    "{protagonista} adelante con paso firme, guiando en fila a los personajes "
    "del tema por un tramo de camino angosto y oscuro, con una lucecita.",
    "Momento de preocupación a mitad del camino en {mundo}: {desafio}. Los "
    "personajes del tema miran preocupados.",
    "{protagonista} con gesto pensativo y un destello suave como una chispa de "
    "idea sobre la cabeza.",
    "Momento heroico: {protagonista} que {solucion}, mientras los personajes "
    "del tema alientan felices; el camino queda libre.",
    "Los personajes del tema formando una torre amistosa, uno sobre otro, bien "
    "apoyados y estables, y {protagonista} subiendo con cuidado hacia el gran "
    "farol en lo más alto de {mundo}.",
    "{protagonista} arriba de todo junto al gran farol apagado pero intacto, "
    "mirándolo con ternura, cielo estrellado.",
    "{protagonista} soplando despacito una chispa hacia el gran farol, que se "
    "enciende llenando {mundo} de una luz dorada y tibia.",
    "{mundo} completamente iluminado de dorado; los personajes del tema "
    "descubriendo felices un camino que estaba escondido en la oscuridad.",
    "{protagonista} guardando en la mano una chispita de luz del farol, gesto "
    "tierno, el farol brillando arriba.",
    "Los personajes del tema acompañando a {protagonista} hasta una puerta de "
    "luz brillante, con {tesoro} presentado brillante y destacado en el centro.",
    "Un dormitorio infantil de noche; {protagonista} en la cama abriendo la "
    "mano, con una chispita de luz que brilla bajito.",
    "Una casita de noche con ventana cálida iluminada, cielo estrellado sereno "
    "y un farol brillando lejano en el horizonte.",
]

# Fallback largo (idx 0..19): portada, dedicatoria, 17 de historia (aventura), FIN.
_ESCENAS_LARGO = [_ESCENAS[0], _ESCENAS[1]] + _AVENTURA_LARGO + [_ESCENAS[9]]


def _tabla17(escenas17):
    """Arma el dict idx 2..18 desde una lista de 17 escenas."""
    return {2 + i: s for i, s in enumerate(escenas17)}


_ESCENAS_POR_HISTORIA_LARGO = {
    "aventura": _tabla17(_AVENTURA_LARGO),
    "tesoro": _tabla17([
        "{protagonista} descubriendo un mapa antiguo enrollado que sale de la "
        "mochila, cuarto infantil cálido.",
        "Un mapa del tesoro que brilla con destellos dorados entre las manos de "
        "{protagonista}, comienzo de aventura.",
        "{protagonista} llegando a {mundo} siguiendo un caminito brillante "
        "marcado por el mapa, todo con aire de secreto.",
        "{nino} y {ninia} alrededor de {protagonista} mirando el mapa "
        "juntos con ojos brillantes, listos para la búsqueda.",
        "Un rincón escondido de {mundo} lleno de brillitos; una única lucecita "
        "con forma de estrella destaca y {protagonista} la señala con asombro.",
        "Una llave dorada brillante junto a una puerta secreta enorme; "
        "{nino} y {ninia} empujándola juntos con esfuerzo.",
        "Un pasillo oscuro y misterioso con ecos en {mundo}; momento de "
        "preocupación: {desafio}.",
        "{protagonista} con los ojos cerrados pensando, una idea iluminándose "
        "como un destello suave sobre la cabeza.",
        "Momento heroico: {protagonista} que {solucion}; al fondo del pasillo "
        "aparece un cofre dorado.",
        "Un cofre dorado con tres cerraduras brillantes; {protagonista}, "
        "{nino} y {ninia} observándolo con curiosidad.",
        "{protagonista} girando las cerraduras del cofre mientras {nino} y "
        "{ninia} acompañan expectantes alrededor.",
        "El cofre abierto de golpe irradiando luz dorada, con {tesoro} "
        "brillando adentro; {protagonista}, {nino} y {ninia} maravillados.",
        "El mapa dado vuelta mostrando una segunda cara que brilla con un "
        "camino dorado nuevo; sorpresa y asombro.",
        "{ninia} contando una historia a {protagonista} y {nino} en ronda, "
        "ambiente cálido de atardecer.",
        "{nino} y {ninia} despidiendo a {protagonista} en la salida de "
        "{mundo}; el cofre guardado brillando a lo lejos.",
        "Un cuarto infantil de noche; {protagonista} guardando el mapa "
        "enrollado debajo de la almohada.",
        "Una casita de noche con ventana cálida, un mapa enrollado apoyado "
        "junto a la cama, cielo estrellado.",
    ]),
    "rescate": _tabla17([
        "Una lucecita mágica golpeando la ventana de un cuarto infantil de "
        "noche, mensaje urgente.",
        "{protagonista} volando por el cielo hacia {mundo}, estrellas y nubes, "
        "sensación de urgencia y valentía.",
        "Atardecer en {mundo}: el sol escondiéndose y las primeras sombras "
        "estirándose por el paisaje.",
        "Los personajes del tema muy preocupados en {mundo} al atardecer, "
        "mirando a lo lejos: falta el más pequeño del grupo.",
        "{protagonista} pidiendo calma con gesto suave a los personajes del "
        "tema, que hablan nerviosos.",
        "Huellas chiquititas en el camino de {mundo}; {protagonista} "
        "alumbrándolas con una linterna, con mucha atención.",
        "{protagonista} pasando primero por un tramo de camino angosto y "
        "tambaleante de noche, los personajes del tema cruzando detrás con "
        "cuidado.",
        "El grupo detenido donde las huellas desaparecen; {protagonista} "
        "escuchando con atención, una mano junto a la oreja.",
        "{protagonista} entrando con una linterna a una cuevita oscura donde "
        "espera un nene humano chiquito (un niño, NO un animal), con frío y "
        "carita de alivio.",
        "{protagonista} saliendo de la cuevita de la mano del nene pequeño (un "
        "niño humano, NO un animal), noche cerrada afuera.",
        "{protagonista} con gesto de idea bajo la noche oscura, las primeras "
        "lucecitas brillantes acercándose alrededor.",
        "Un caminito de lucecitas brillantes en la noche; los personajes del "
        "tema recibiendo al nene pequeño (un niño) con una manta calentita, "
        "saltos de alegría.",
        "El nene pequeño rescatado (un niño) envuelto en la manta, feliz junto "
        "a {protagonista}, ambiente de agradecimiento.",
        "Los personajes del tema de pie cantando de noche junto a las lucecitas "
        "brillantes, con las manos a los costados; a UN COSTADO, separado, el "
        "perro dálmata sentado tranquilo con sus CUATRO patas apoyadas en el "
        "piso, mirando contento. NADIE toca ni sostiene al perro; el perro NO "
        "levanta ni extiende las patas hacia nadie.",
        "Los personajes del tema entregando {tesoro} brillante y destacado en "
        "el centro a {protagonista}, ceremonia de héroes.",
        "Un cuarto infantil de noche; {protagonista} en la cama con las manos "
        "juntitas al pecho y expresión feliz.",
        "Una casita de noche con ventana cálida iluminada, cierre tranquilo y "
        "feliz.",
    ]),
    "gran-dia": _tabla17([
        "Una gran noticia llegando a un cuarto infantil: un sobre festivo con "
        "confetti saliendo, emoción.",
        "{protagonista} con mochila saliendo con paso decidido hacia {mundo}, "
        "camino soleado con banderines a lo lejos.",
        "{mundo} en plena preparación de fiesta: guirnaldas, instrumentos y un "
        "desfile ensayando, mucho movimiento alegre.",
        "Los personajes del tema mostrando a {protagonista} una gran torre de "
        "luces apagada: la tarea más importante de la fiesta.",
        "Ensayo alegre en {mundo}: los personajes del tema practicando el "
        "desfile entre risas, {protagonista} participando.",
        "El cielo poniéndose gris de golpe sobre la fiesta, nubes enormes "
        "dando vueltas, todos mirando para arriba preocupados.",
        "La tormenta desarmando las decoraciones: guirnaldas volando y la "
        "torre de luces apagada; {protagonista} con gesto decidido animando a "
        "los personajes del tema.",
        "{protagonista} organizando equipos: unos atando guirnaldas, otros "
        "secando el escenario, otros juntando luces caídas.",
        "La fiesta rearmándose entre todos en {mundo}, más linda que antes, "
        "trabajo en equipo alegre.",
        "La torre de luces apagada y mojada, goteando; los personajes del "
        "tema mirándola preocupados.",
        "{protagonista} con una idea genial, llenando la torre de lucecitas "
        "brillantes y velitas de colores junto a los personajes del tema.",
        "Cielo despejado: {protagonista} encendiendo la torre de luces, que "
        "brilla hermosa; la Gran Fiesta comenzando en {mundo}.",
        "La fiesta en su esplendor: música, baile y una torta gigante, todos "
        "los personajes del tema felices.",
        "Los personajes del tema riéndose aliviados junto a {protagonista}, "
        "la fiesta brillando alrededor.",
        "Los personajes del tema entregando {tesoro} brillante y destacado a "
        "{protagonista}, agradecimiento y cariño.",
        "Un cuarto infantil de noche; {protagonista} en la cama con una "
        "sonrisa, como recordando música y risas.",
        "Una casita de noche con ventana cálida, banderines lejanos en el "
        "horizonte, cielo estrellado.",
    ]),
    "noche-estrellas": _tabla17([
        "Un cuarto infantil de noche; {protagonista} en la cama con los ojos bien "
        "abiertos mirando el techo, sin poder dormir.",
        "Desde la ventana, una estrella fugaz larga y brillante cayendo detrás "
        "de {mundo}; {protagonista} mirando en pantuflas.",
        "{protagonista} llegando a {mundo} bajo un cielo enorme repleto de "
        "estrellas que titilan.",
        "Los personajes del tema con carita triste bajo un cielo nocturno que "
        "tiene un hueco oscuro sin estrellas sobre {mundo}.",
        "Los personajes del tema y {protagonista} mirando preocupados el hueco "
        "oscuro del cielo, que parece crecer.",
        "El grupo poniéndose en marcha de noche por {mundo}, siguiendo un "
        "resplandor suave y lejano.",
        "{protagonista} en medio de un montón de lucecitas brillantes que se "
        "encienden para alumbrar el camino oscuro.",
        "El grupo cruzando colinas dormidas y rincones calladitos de {mundo}, "
        "el resplandor cada vez más cerca.",
        "Una estrellita chiquita y apagada en el suelo de {mundo}, con "
        "lágrimas de luz; {protagonista} acercándose con ternura.",
        "{protagonista} abrazando despacito a la estrellita caída para "
        "consolarla, ambiente muy tierno.",
        "{protagonista} con gesto de idea junto a la estrellita débil; los "
        "personajes del tema alrededor, atentos.",
        "Los personajes del tema y {protagonista} con los ojos cerrados "
        "pidiendo deseos alrededor de la estrellita, que se enciende radiante.",
        "La estrella elevándose al cielo como un globo dorado, volando hacia "
        "el hueco oscuro; todos mirando desde abajo.",
        "El cielo de {mundo} completito de estrellas otra vez; los personajes "
        "del tema festejando mirando para arriba.",
        "La estrella brillando en lo alto mandando un destello hacia "
        "{protagonista}, con {tesoro} presentado brillante en el centro.",
        "Un cuarto infantil de noche; {protagonista} en la cama mirando por "
        "la ventana una estrella que titila.",
        "Una casita de noche con ventana cálida, cielo estrellado completo y "
        "sereno, una estrella brillando especialmente.",
    ]),
    "cumple-sorpresa": _tabla17([
        "{protagonista} con carita de sorpresa y gesto de secreto (un dedo "
        "junto a la boca), cuarto infantil cálido, una idea brillando.",
        "{protagonista} en marcha hacia {mundo} con paso apurado y sonrisa "
        "cómplice, llevando globos desinflados y cintas de colores.",
        "{protagonista} entrando en puntitas de pie a {mundo}, mirando para "
        "todos lados con complicidad.",
        "{protagonista} contando la misión en voz bajita a los personajes del "
        "tema, todos en ronda cómplice con gestos de silencio.",
        "Los personajes del tema repartiéndose tareas: globos por acá, una "
        "torta por allá, movimiento secreto y divertido.",
        "Los personajes del tema escondiendo decoraciones por los rincones de "
        "{mundo}, aguantándose la risa.",
        "Momento de susto en plena preparación: {desafio}. Los personajes del "
        "tema con cara de preocupación entre globos y guirnaldas.",
        "{protagonista} respirando hondo con gesto concentrado, decoraciones "
        "a medio poner alrededor.",
        "Momento heroico: {protagonista} que {solucion}, salvando los "
        "preparativos; alivio y sonrisas.",
        "Un personaje del tema con carita triste caminando cabizbajo, "
        "creyendo que nadie se acordó de su día.",
        "{protagonista} paseando junto al personaje triste para distraerlo, "
        "mientras atrás los demás terminan de decorar a toda velocidad.",
        "Explosión de sorpresa en {mundo}: mil lucecitas encendiéndose, "
        "globos, y los personajes del tema saltando de sus escondites "
        "alrededor del cumpleañero feliz.",
        "El cumpleañero con los ojos brillantes de emoción, mimado por todos; "
        "{protagonista} sonriendo cerca.",
        "Baile y torta bajo la luna en {mundo}, el cumpleañero siempre "
        "cerquita de {protagonista}.",
        "El cumpleañero entregando a {protagonista} {tesoro} brillante y "
        "destacado, gesto de gratitud.",
        "Un cuarto infantil de noche; {protagonista} durmiéndose con un "
        "gorrito de fiesta todavía puesto.",
        "Una casita de noche con ventana cálida y un globo atado afuera, "
        "cielo estrellado.",
    ]),
    "pequeno-maestro": _tabla17([
        "{ninia} y {nino} haciendo algo increíble propio del tema; "
        "{protagonista} mirando con ojos enormes de admiración.",
        "{protagonista} pidiendo con ilusión que le enseñen; {ninia} y "
        "{nino} entusiasmados alrededor.",
        "{ninia} y {nino} mostrando cómo se hace, despacito; {protagonista} "
        "mirando sin pestañear.",
        "{protagonista} de cola en el piso tras un intento fallido gracioso, "
        "riéndose; {ninia} y {nino} sonriendo con cariño.",
        "{nino} animando con gesto tierno a {protagonista}.",
        "{protagonista} practicando una y otra vez con esfuerzo; {ninia} y "
        "{nino} alentando desde el costado.",
        "¡Primer logro! {protagonista} dando un gran salto de alegría; "
        "{ninia} y {nino} festejando amontonados de risa.",
        "Preparativos de una gran muestra en {mundo}: un escenario armándose, "
        "entusiasmo general.",
        "{nuevo} mirando todo desde lejos; {protagonista} mirando hacia ese "
        "rincón con gesto amable.",
        "{protagonista} acercándose despacito a {nuevo}, gesto de invitación "
        "amable.",
        "{protagonista} enseñando de a pasitos a {nuevo}, con mucha "
        "paciencia, ambiente cálido.",
        "La gran muestra en {mundo}: {protagonista} en el escenario logrando "
        "su número, {nuevo} lográndolo también al lado; {ninia} y {nino} "
        "festejando con sonrisas enormes en el público.",
        "{nuevo} saltando de alegría junto a {protagonista}, gratitud y "
        "orgullo.",
        "{nino} hablando con cariño al grupo en ronda; {protagonista} en el "
        "centro, ambiente emotivo.",
        "{ninia} y {nino} entregando {tesoro} brillante y destacado a "
        "{protagonista}, agradecimiento.",
        "Un cuarto infantil de noche; {protagonista} en la cama con una "
        "sonrisa soñadora.",
        "Una casita de noche con ventana cálida iluminada, cierre tierno y "
        "feliz.",
    ]),
    "ayudar-a-todos": _tabla17([
        "Un problema grandote y vistoso en {mundo} (un gran enredo o desorden "
        "que bloquea el lugar); {alto}, {fuerte} y {chiquito} mirándolo "
        "juntos sin saber qué hacer.",
        "{alto}, {fuerte} y {chiquito} desanimados; {protagonista} "
        "respirando hondo con un destello de idea sobre la cabeza.",
        "{alto}, {fuerte} y {chiquito} sentados cabizbajos, desanimados.",
        "{protagonista} proponiendo con entusiasmo resolverlo entre todos; "
        "{alto}, {fuerte} y {chiquito} levantando la cabeza con esperanza.",
        "{chiquito} escondiéndose en un rinconcito, con gesto de creerse "
        "demasiado pequeña para servir de ayuda.",
        "{protagonista} sonriendo con cariño a {chiquito}, dándole "
        "importancia.",
        "{protagonista} repartiendo tareas: {alto} listo para alcanzar, "
        "{fuerte} lista para empujar, {chiquito} adelante con la misión más "
        "especial.",
        "{alto}, {fuerte} y {chiquito} esforzándose con el problema "
        "grandote, que todavía no cede; caras de esfuerzo.",
        "{chiquito} metiéndose por un huequito imposible y destrabando la "
        "primera parte; {alto} y {fuerte} gritando de alegría junto a "
        "{protagonista}.",
        "{alto} alcanzando lo inalcanzable y {fuerte} empujando con todo; "
        "{protagonista} coordinando como director de orquesta.",
        "Un tropezón gracioso: {alto}, {fuerte}, {chiquito} y {protagonista} "
        "sosteniéndose todos juntos para no caer, riéndose del susto.",
        "¡Lo lograron! El problema resuelto, {mundo} en paz otra vez; "
        "{alto}, {fuerte}, {chiquito} y {protagonista} festejando en grande.",
        "{chiquito} en el centro de la ronda; {alto}, {fuerte} y "
        "{protagonista} festejando muy felices alrededor.",
        "{protagonista} hablando en ronda con {alto}, {fuerte} y {chiquito}, "
        "todos asintiendo con sonrisas.",
        "{alto}, {fuerte} y {chiquito} entregando {tesoro} brillante y "
        "destacado a {protagonista}, celebración.",
        "Un cuarto infantil de noche; {protagonista} acurrucándose en la "
        "cama, sonrisa tranquila.",
        "Una casita de noche con ventana cálida iluminada, cielo estrellado "
        "sereno.",
    ]),
    "gran-viaje": _tabla17([
        "Un paquetito brillante con moño en la puerta de un dormitorio "
        "infantil; {protagonista} mirándolo con curiosidad, luz de "
        "atardecer, sensación de misión por empezar.",
        "{protagonista} con una mochila liviana saliendo al anochecer con "
        "paso decidido, primer paso del gran viaje.",
        "{piloto1} y {piloto2} esperando a {protagonista} con un mapa de "
        "recorrido desplegado: caminitos y tres banderitas (dibujo, sin "
        "letras).",
        "{piloto1} y {piloto2} contando la misión en ronda a "
        "{protagonista}, gesto de urgencia dulce; la luna saliendo.",
        "{piloto1} y {piloto2} repartiéndose el viaje; {protagonista} "
        "sosteniendo con cuidado el paquetito brillante.",
        "{piloto1} y {piloto2} cantando junto a {protagonista} por un "
        "camino de {mundo} mientras el sol se esconde, ambiente alegre.",
        "Un viento travieso en forma de remolino tratando de llevarse el "
        "paquetito; {protagonista} abrazándolo fuerte.",
        "El viento despejando el cielo: las nubes yéndose y un cielo lleno "
        "de estrellas apareciendo.",
        "{protagonista} señalando un atajo iluminado por las estrellas; "
        "{piloto1} y {piloto2} avanzando con energía.",
        "Una parada del viaje con chocolate calentito humeante; {piloto1} "
        "y {piloto2} tomando fuerzas, tacitas y vapor.",
        "El tramo más oscuro del camino de noche; {piloto1} y {piloto2} "
        "avanzando bien juntito, {protagonista} adelante con paso valiente.",
        "La llegada al amanecer: {piloto1} abriendo el paquetito con ojos "
        "brillantes de emoción, primer rayito de sol.",
        "{piloto1} con el regalo bien cerquita, muy emocionado; {piloto2} "
        "y {protagonista} alrededor con ternura.",
        "El festejo de {piloto1} arrancando con el primer sol; "
        "{protagonista} en el lugar de honor.",
        "{piloto1} y {piloto2} entregando {tesoro} brillante y destacado a "
        "{protagonista}, premio de la misión cumplida.",
        "Un cuarto infantil de mañana tempranito; {protagonista} en la cama "
        "con cara de dulce cansancio feliz.",
        "Una casita al amanecer con ventana cálida y un caminito largo "
        "perdiéndose en el horizonte de {mundo}.",
    ]),
    "manos-a-la-obra": _tabla17([
        "Un rincón vacío de {mundo}; los personajes del tema mirándolo con "
        "carita soñadora, imaginando algo lindo.",
        "{protagonista} dibujando un plano con una ramita en el piso; los "
        "personajes del tema mirando con curiosidad.",
        "El plano dibujado en el piso: un rinconcito con mesa, banquitos y "
        "un techito con forma de sonrisa (dibujo simple, sin letras).",
        "Los personajes del tema con ojos brillantes alrededor del plano; "
        "{protagonista} con gesto de manos a la obra.",
        "Cada personaje trayendo materiales: maderitas, sogas y telas de "
        "colores, desfile alegre de cosas.",
        "El grupo midiendo con pasos y marcando con piedritas; las primeras "
        "columnas paradas derechitas.",
        "El techito torcido y la estructura tambaleándose; los personajes "
        "del tema con carita de susto.",
        "{protagonista} comparando el plano con la obra y descubriendo la "
        "pieza que falta, gesto de idea.",
        "Entre todos enderezando el techito y colocando la pieza justa en el "
        "medio; la estructura queda firme.",
        "Los más chiquitos pintando banquitos, los más altos colgando "
        "farolitos, los más fuertes ajustando rincones.",
        "{protagonista} colgando el último farolito al atardecer; todos "
        "dando un paso atrás para mirar.",
        "El rincón terminado en {mundo}: firme, colorido, con farolitos "
        "encendidos; todos mirándolo felices.",
        "La primera merienda bajo el techito nuevo de noche: lluvia suave "
        "afuera y todos secos y felices adentro.",
        "Los personajes del tema en ronda en el rincón nuevo hablando con "
        "cariño; {protagonista} en el medio.",
        "Los personajes del tema entregando {tesoro} brillante y destacado a "
        "{protagonista} en el rincón nuevo.",
        "Un cuarto infantil de noche; {protagonista} mirando con una sonrisa "
        "sus dedos con manchitas de pintura de colores.",
        "Una casita de noche con ventana cálida; a lo lejos, el rinconcito "
        "nuevo de {mundo} con farolitos brillando.",
    ]),
    "gran-torneo": _tabla17([
        "Banderines y preparativos de los Grandes Juegos en {mundo}; "
        "{capitan}, {rapido}, {fuerte} y {chiquito} desanimados a un costado.",
        "{protagonista} animando a {capitan}, {rapido}, {fuerte} y "
        "{chiquito} con una sonrisa, gesto de arranque de entrenamiento.",
        "Entrenamiento desastroso y gracioso: {capitan}, {rapido}, {fuerte} "
        "y {chiquito} corriendo para lados distintos, tropezándose con "
        "suavidad y terminando en el piso riéndose.",
        "{protagonista} explicando el plan a {capitan}, {rapido}, {fuerte} y "
        "{chiquito} en ronda, todos atentos y con ganas.",
        "Cada uno entrenando lo suyo: {rapido} corriendo, {fuerte} "
        "saltando, {chiquito} ensayando una jugada secreta.",
        "{capitan}, {rapido}, {fuerte} y {chiquito} entrenando cada día "
        "mejor, pasándose y esperándose, ambiente de progreso alegre.",
        "{capitan} a un costado con una venda simpática, carita de no poder "
        "jugar; {rapido}, {fuerte} y {chiquito} alrededor, preocupados.",
        "{protagonista} juntando a {rapido}, {fuerte} y {chiquito} en ronda "
        "con gesto de ánimo; {capitan} sonriendo desde el costado.",
        "La entrada a los Grandes Juegos: {rapido}, {fuerte}, {chiquito} y "
        "{protagonista} desfilando con {capitan} al frente alentando desde "
        "el costado; tribunas de {mundo} llenas.",
        "Las primeras pruebas de los juegos: {rapido}, {fuerte} y "
        "{chiquito} mejorando prueba a prueba, energía creciente.",
        "La prueba final cabeza a cabeza con {rival}; expectativa máxima en "
        "las tribunas de {mundo}.",
        "La jugada secreta de {chiquito} saliendo perfecta; el público de "
        "{mundo} festejando con saltos y confetti.",
        "{capitan}, {rapido}, {fuerte}, {chiquito} y {protagonista} "
        "festejando junto a {rival}, todos mezclados, alegría deportiva "
        "enorme.",
        "{capitan} muy emocionado junto a {rapido}, {fuerte} y {chiquito}, "
        "momento tierno de orgullo.",
        "Premiación: {capitan}, {rapido}, {fuerte} y {chiquito} entregando "
        "{tesoro} brillante y destacado a {protagonista}.",
        "Un cuarto infantil de noche; {protagonista} en la cama con una "
        "sonrisa, una cintita de premio colgada cerca.",
        "Una casita de noche con ventana cálida; banderines de los Grandes "
        "Juegos a lo lejos en {mundo}.",
    ]),
}


# ── ELENCO FIJO (Pablo, 24-jul-2026 — libro "El día de ayudar a todos" era el
# peor: cada página inventaba un protagonista/personaje distinto porque el
# arco menciona roles con nombre propio —"el más alto", "el más fuerte", "el
# más chiquito"— sin atarlos a un diseño concreto). Para el combo (tema,
# historia) que lo necesite, este dict fija la DESCRIPCIÓN FÍSICA exacta de
# cada rol (debe coincidir con los personajes reales de ia_maestra.png del
# tema) y se inyecta en el prompt de TODAS las escenas donde aparece — así
# nunca se inventa un personaje nuevo. El texto narrado (libro_historias.py)
# sigue usando el nombre de rol genérico ("el más chiquito") para no romper
# la regla de texto universal; solo el PROMPT DE IMAGEN, que ya es por-tema,
# recibe la descripción concreta.
ELENCO_FIJO = {
    ("superheroes", "ayudar-a-todos"): {
        "alto": "el superhéroe de pelo oscuro rizado, antifaz rojo y traje "
                "azul con capa roja y un rayo dorado en el pecho (el "
                "mismo superhéroe en TODAS las escenas, nunca cambia)",
        "fuerte": "la superheroína de pelo oscuro rizado con una estrellita "
                  "dorada en el pelo, antifaz rojo y traje verde azulado con "
                  "capa roja (la misma superheroína en TODAS las escenas, "
                  "nunca cambia)",
        "chiquito": "la superheroína más pequeña del trío, de pelo castaño "
                    "en colitas, antifaz celeste, traje rosa con capa "
                    "celeste y una estrella en el pecho (la misma "
                    "superheroína en TODAS las escenas, nunca cambia)",
    },
    # futbol/gran-torneo (Pablo, 24-jul-2026): la referencia del tema
    # (ia_maestra.png) NO tiene NINGÚN personaje humano — es una hoja de
    # objetos con carita (pelota, trofeo, botín). Sin un elenco fijo el
    # modelo dibuja esos objetos en vez de un equipo de chicos, y solo por
    # momentos inventa nenes sueltos y distintos. Acá se define un plantel
    # de 4 amigos + el protagonista, todos con la MISMA camiseta de local, y
    # el rival con otra camiseta — ver `protagonista_extra`.
    ("futbol", "gran-torneo"): {
        "capitan": "el capitán del equipo, un chico de pelo oscuro corto y "
                   "cinta de capitán en el brazo, camiseta a rayas celestes "
                   "y blancas, short azul y medias blancas (el mismo chico "
                   "en TODAS las escenas, nunca cambia)",
        "rapido": "la compañera más rápida del equipo, de pelo castaño en "
                  "una colita alta, la misma camiseta a rayas celestes y "
                  "blancas, short azul y medias blancas (la misma chica en "
                  "TODAS las escenas, nunca cambia)",
        "fuerte": "el compañero más fuerte del equipo, más robusto y de "
                  "pelo rubio corto, la misma camiseta a rayas celestes y "
                  "blancas, short azul y medias blancas (el mismo chico en "
                  "TODAS las escenas, nunca cambia)",
        "chiquito": "la compañera más chiquita del equipo, la más bajita "
                    "del grupo, pelo negro corto con una vincha, la misma "
                    "camiseta a rayas celestes y blancas, short azul y "
                    "medias blancas (la misma chica en TODAS las escenas, "
                    "nunca cambia)",
        "rival": "el equipo rival, con camiseta roja lisa y short blanco "
                 "(bien distinto a la camiseta celeste y blanca a rayas del "
                 "equipo local)",
        "protagonista_extra": ", con la misma camiseta a rayas celestes y "
                              "blancas, short azul y medias blancas que sus "
                              "compañeros de equipo",
    },
    # artistas/pequeno-maestro (Pablo, 24-jul-2026, "Pequeños artistas"):
    # ia_maestra.png trae 2 personajes fijos del tema (nena de colitas +
    # nene de guardapolvo) — sin elenco fijo, el arte los repetía siempre a
    # ELLOS incluso para el rol de "personaje nuevo" (que la historia pide
    # que sea alguien DISTINTO, nunca visto antes) y confundía cuál de los
    # dos era el protagonista.
    ("artistas", "pequeno-maestro"): {
        "ninia": "la compañera de pelo negro rizado recogido en dos moños "
                 "con vinchas rojas, remera amarilla y guardapolvo blanco "
                 "con manchas de pintura de colores (la misma nena de la "
                 "referencia del tema en TODAS las escenas, nunca cambia)",
        "nino": "el compañero de pelo castaño corto, remera y jean "
                "celeste con guardapolvo blanco lleno de manchas de "
                "pintura de colores (el mismo nene de la referencia del "
                "tema en TODAS las escenas, nunca cambia)",
        "nuevo": "un chico nuevo y tímido, de pelo negro lacio y "
                 "guardapolvo celeste claro liso (bien distinto a los "
                 "guardapolvos blancos con manchas de los demás) — un "
                 "chico DISTINTO a la nena y al nene de guardapolvo "
                 "blanco, nunca el mismo personaje que ellos (el mismo "
                 "chico nuevo en TODAS las escenas, nunca cambia)",
    },
    # campamento/tesoro (Pablo, 24-jul-2026, "El mapa del tesoro"): mismo
    # fix — 2 personajes fijos de la referencia, nombrados siempre para que
    # no aparezcan nenes de más que la escena no pide.
    ("campamento", "tesoro"): {
        "nino": "el compañero de campamento de pelo castaño, remera "
                "celeste y short caqui, con una mochila y un rollo de "
                "dormir al hombro (el mismo chico de la referencia del "
                "tema en TODAS las escenas, nunca cambia)",
        "ninia": "la compañera de campamento de pelo castaño en trenza, "
                 "gorra caqui, pañuelo rojo al cuello y mochila de "
                 "explorador (la misma chica de la referencia del tema en "
                 "TODAS las escenas, nunca cambia)",
        "protagonista_extra": ", con una mochila de explorador y una "
                              "gorra caqui como sus compañeros de "
                              "campamento",
    },
    # aviadores/gran-viaje (Pablo, 24-jul-2026, "La entrega importante"):
    # el protagonista perdía el traje de aviador entre páginas; acá se fija
    # por texto además de encadenar la imagen.
    ("aviadores", "gran-viaje"): {
        "piloto1": "un piloto de campamento aéreo, pelo castaño con "
                   "flequillo, gorro de cuero y antiparras, mameluco "
                   "marrón con cuello de piel blanca y botas marrones (el "
                   "mismo piloto en TODAS las escenas, nunca cambia)",
        "piloto2": "otro piloto de campamento aéreo, pelo castaño en dos "
                   "colitas cortas, gorro de cuero y antiparras, mameluco "
                   "marrón con cuello de piel blanca y botas marrones (el "
                   "mismo piloto en TODAS las escenas, nunca cambia)",
        "protagonista_extra": ", con un traje de aviador marrón, gorro de "
                              "cuero, antiparras y bufanda blanca, igual "
                              "al de los pilotos del grupo",
    },
    # monstruos/aventura (Pablo, 24-jul-2026, "La invitación mágica"): acá
    # el problema NO era falta de elenco (hay ~10 monstruos, de sobra) sino
    # el pijama del protagonista cambiando de color de página en página —
    # alcanza con fijarlo por texto + la cadena de referencias.
    ("monstruos", "aventura"): {
        "protagonista_extra": ", con el mismo pijama celeste de manga "
                              "larga con estrellitas y pantuflas a juego "
                              "(igual en TODAS las escenas, nunca cambia)",
    },
    # safari/noche-estrellas (Pablo, 24-jul-2026, "La noche de las
    # estrellas"): mismo bug que monstruos/aventura — el protagonista sale
    # en pijama a buscar la estrella fugaz y a mitad de historia aparecía
    # con ropa de safari de día en vez de seguir en pijama. El trío fijo
    # (león/jirafa/mono) de la referencia ya se mantenía bien, no hace
    # falta ELENCO_FIJO para ellos.
    ("safari", "noche-estrellas"): {
        "protagonista_extra": ", con el mismo pijama celeste de manga "
                              "larga y pantuflas marrones a juego (igual "
                              "en TODAS las escenas, nunca cambia)",
    },
}

_ELENCO_FALLBACK = {
    "alto": "el más alto de los personajes del tema",
    "fuerte": "el más fuerte de los personajes del tema",
    "chiquito": "el más chiquito de los personajes del tema",
    "capitan": "el capitán del equipo de los personajes del tema",
    "rapido": "el más rápido de los personajes del tema",
    "rival": "el equipo rival",
    "nino": "un nene de los personajes del tema",
    "ninia": "una nena de los personajes del tema",
    "nuevo": "un personaje nuevo del tema, distinto a los demás",
    "piloto1": "el primero de los personajes del tema",
    "piloto2": "el segundo de los personajes del tema",
    "protagonista_extra": "",
}


def _elenco(tema, historia):
    """Roles con nombre propio ({alto}/{fuerte}/{chiquito}) para el prompt de
    imagen. Si el combo (tema, historia) no tiene un elenco fijo definido,
    cae al genérico de siempre (compatibilidad con el resto de historias)."""
    return {**_ELENCO_FALLBACK, **ELENCO_FIJO.get((tema, (historia or "").lower()), {})}


def _paleta(tema):
    import json
    try:
        k = json.load(open(os.path.join(TEMAS, tema, "tema.json"))).get("kit") or {}
    except Exception:
        k = {}
    return {"accent": k.get("accent") or "#6B5BD2", "ink": k.get("ink") or "#4a4a4a"}


def tam_pagina(tema, idx, edad=None, historia=None, catalogo=False):
    """La página FIN es a hoja completa (vertical); el resto son paneles ~cuadrados."""
    if idx == libro.total_paginas(tema, edad, historia, catalogo) - 1:
        return _VERTICAL
    # la dedicatoria va en un panel apaisado (700x524): generarla cuadrada
    # obligaba a recortar 12%% arriba y abajo — apaisada casi no se recorta
    if idx == 1:
        return _APAISADA
    return _CUADRADA


# ── indicaciones del editor por tema (Pablo): se guardan en el tema y se
# inyectan en TODOS los prompts de ilustración de esa temática — así un arreglo
# pedido una vez impacta en cada regeneración futura de cualquier libro del tema.
def nota_tema(tema):
    p = os.path.join(TEMAS, tema, "libro_notas.txt")
    try:
        return open(p, encoding="utf-8").read().strip()
    except OSError:
        return ""


def guardar_nota_tema(tema, texto):
    p = os.path.join(TEMAS, tema, "libro_notas.txt")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write((texto or "").strip())


def _protagonista(genero):
    """Frase del protagonista para las escenas donde aparece. El campo llega libre
    del formulario («nena», «niña», «nene», «varón»…) — se normaliza acá. Siempre
    de espaldas/lejos: la cara nunca se ve (funciona con cualquier chico)."""
    g = (genero or "").strip().lower()
    if g in ("nena", "niña", "nina", "mujer", "girl", "f"):
        return "una nena pequeña vista de espaldas (nunca se le ve la cara)"
    if g in ("nene", "niño", "nino", "varon", "varón", "boy", "m"):
        return "un nene pequeño visto de espaldas (nunca se le ve la cara)"
    return "un niño visto de espaldas (nunca se le ve la cara)"


def _escena_para(tema, idx, historia=None, catalogo=False, edad=None):
    """(escena SIN formatear, hlow) — el lookup de qué texto de escena
    corresponde a la página idx. Separado de `prompt_pagina` para que
    `generar_ilustraciones` pueda mirar el template CRUDO (con {protagonista}
    todavía sin sustituir) y decidir si esta página sirve de ANCLA de
    continuidad de personajes (ver ELENCO FIJO / referencias encadenadas)."""
    hlow = (historia or "").strip().lower()
    if not catalogo and not hlow:
        # sin historia explícita, el arte sigue la historia DEL TEMA (tema.json
        # «libro_historia») — la misma que usa el texto en libro.cuento()
        hlow = libro.historia_de_tema(tema) or ""
    if catalogo and hlow in _ESCENAS_POR_HISTORIA_LARGO:
        n_hist = libro.paginas_historia(tema, edad, historia, catalogo=True)
        total = n_hist + 3
        if idx <= 1 or idx >= total - 1:                       # portada, dedicatoria, FIN
            escena = _ESCENAS_LARGO[0 if idx == 0 else (1 if idx == 1 else -1)]
        else:                                                  # páginas de historia
            j = idx - 2
            story_i = j if n_hist >= libro.PAGINAS_HISTORIA_LARGO else libro.CORTO_IDX[j]
            escena = _ESCENAS_POR_HISTORIA_LARGO[hlow].get(2 + story_i,
                                                           _ESCENAS_LARGO[2 + story_i])
    else:
        extendido = libro.paginas_historia(tema) > libro.PAGINAS_HISTORIA
        tabla = _ESCENAS_POR_HISTORIA_EXT if extendido else _ESCENAS_POR_HISTORIA
        fallback = _ESCENAS_EXT if extendido else _ESCENAS
        arco = tabla.get(hlow, {})
        escena = arco.get(idx, fallback[idx])
    return escena, hlow


def prompt_pagina(tema, idx, genero=None, historia=None, catalogo=False, edad=None):
    """Prompt de la ilustración de la página idx, con la ambientación de la historia
    del tema (libro.HISTORIAS) y el mismo bloque de estilo del resto del kit.
    genero («nena»/«nene», opcional): cómo dibujar al protagonista en las escenas
    donde aparece — lo usa el libro premium, que ilustra por pedido.
    catalogo=True (audiolibro): usa las escenas de la versión larga (17 páginas) con
    largo por edad; la versión corta (9, hasta 3 años) mapea con libro.CORTO_IDX."""
    h = dict(libro.HISTORIAS.get(tema, libro.HISTORIA_DEFAULT))
    pal = _paleta(tema)
    escena, hlow = _escena_para(tema, idx, historia=historia, catalogo=catalogo, edad=edad)
    elenco = _elenco(tema, hlow)
    h["protagonista"] = _protagonista(genero) + elenco.pop("protagonista_extra", "")
    h.update(elenco)
    escena = escena.format(**h)
    return (
        "Ilustración para la página de un libro de cuentos infantil profesional. "
        "Escena: %s "
        "Estilo: ilustración infantil cálida, formas suaves y redondeadas, colores "
        "planos con paleta acento %s y tinta %s. "
        "Usá ÚNICAMENTE los personajes de las imágenes de referencia, manteniendo su "
        "diseño. NO agregues NINGÚN otro personaje, animal ni criatura que no esté en "
        "la referencia (por ejemplo, si el tema es de superhéroes NO metas animales de "
        "safari) — solo los personajes del tema y el escenario que pide la escena. "
        "PROTAGONISTA: el protagonista es SIEMPRE un NIÑO o NIÑA humano (un nene o una "
        "nena) — NUNCA un animal ni una mascota — y es el personaje PRINCIPAL y más "
        "prominente de la escena, en primer plano, para "
        "que se entienda que la historia es sobre ÉL. Si en la escena hay un animal o "
        "mascota, tiene que quedar CLARO que el protagonista es el niño y el animal es "
        "secundario (más chico o atrás). Nunca confundir al niño con un animal. "
        "CONTINUIDAD DE PERSONAJES (obligatoria, prioridad máxima): si además "
        "de la referencia de estilo se incluyen imágenes de referencia del "
        "PROTAGONISTA y/o del ELENCO de esta misma historia, el protagonista y "
        "cada personaje secundario mantienen EXACTAMENTE el mismo diseño que "
        "en esas referencias — mismo color y tipo de ropa (nunca cambia de "
        "pijama a otro color, ni de manga corta a larga, ni de un peinado a "
        "otro), mismo pelo, mismos accesorios. Es el MISMO personaje de página "
        "en página, nunca uno nuevo ni parecido. Ningún personaje de las "
        "referencias aparece más de UNA vez dentro de la misma escena (nunca "
        "dos copias del mismo personaje, ni el protagonista duplicado). "
        "La escena llena TODA la imagen, sin marcos, bordes ni viñetas. "
        "ESCENARIO COMPLETO (obligatorio): la escena tiene SIEMPRE un fondo "
        "completo que llena toda la imagen — piso con textura y color del tema "
        "(pasto, arena, piso de madera del taller, alfombra de circo, césped...), "
        "y detrás el lugar (paredes, cielo, árboles, edificios, el ambiente de la "
        "temática). Los personajes NUNCA flotan sobre un fondo liso, blanco o "
        "crema vacío. Si la imagen de referencia tiene fondo blanco (hoja de "
        "stickers), usála SOLO para el diseño de los personajes: el fondo de la "
        "escena lo pintás COMPLETO igual. "
        "PERSONAJES PARADOS SOBRE EL PISO (obligatorio): cada personaje se apoya "
        "ENCIMA del suelo, con el cuerpo ENTERO visible y los pies sobre la "
        "tierra. NUNCA medio enterrado, hundido, ni cortado por la línea del "
        "piso o del horizonte (nada de personajes 'sepultados hasta la cintura' "
        "porque el suelo les tapa las piernas). Si el piso sube (una lomita), los "
        "personajes van ADELANTE, completos, no detrás de la loma. "
        "IMPORTANTE (encuadre): plano ABIERTO/alejado. Los personajes ocupan como "
        "mucho el 60%% central de la imagen, SIEMPRE completos y bien adentro, con "
        "MUCHO aire (espacio vacío de fondo) en los CUATRO lados —arriba, abajo, "
        "izquierda y derecha— porque al encuadrar la página se recortan los bordes "
        "y no se les puede cortar la cara ni el cuerpo. Ningún personaje pegado al borde. "
        "REGLA CRÍTICA de patas: los animales de CUATRO patas (león, jirafa, cebra, "
        "elefante, PERRO, gato, etc.) van SIEMPRE con EXACTAMENTE 4 patas (contá: "
        "cuatro, ni una más ni una menos) apoyadas en el piso y NUNCA "
        "saludan ni levantan una pata — al levantar una pata el dibujo casi siempre "
        "inventa una QUINTA pata, y eso está MAL. Un animal en 4 patas NO saluda. "
        "SOLO los personajes que están parados en DOS patas (como un mono erguido) "
        "pueden saludar con una mano. Los animales NUNCA se dan la mano ni chocan los "
        "cinco, y un animal en cuatro patas TAMPOCO aplaude ni junta las patas "
        "delanteras en el aire (para festejar alcanza con sonrisas, saltos con las "
        "cuatro patas juntas o confetti). Cada animal con la cantidad EXACTA de patas de "
        "su especie: ni una de más ni de menos, y la cola es la cola, NO una pata extra. "
        "Importante: NO escribas ningún texto, número ni letra (no text, no letters)."
        % (escena, pal["accent"], pal["ink"])
        + ((" INDICACIÓN DEL EDITOR (OBLIGATORIA, prioridad máxima): %s" % nota)
           if (nota := nota_tema(tema)) else "")
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


_QA_URL = "https://api.openai.com/v1/chat/completions"


# Recorte real que hará libro.py al encuadrar el arte en el panel (object-fit:
# cover): el QA debe mirar ESTA versión — el arte crudo puede verse bien y aun
# así quedar con caras cortadas tras el recorte (pasó con safari pág 4).
_PANEL_WH = {1: (700, 524)}          # dedicatoria; historia (2..8) usa el default
_PANEL_WH_DEF = (1060, 962)

def _como_en_panel(png_bytes, idx):
    """PNG del arte recortado exactamente como quedará en el panel de la página."""
    from PIL import Image
    import io
    W, H = _PANEL_WH.get(int(idx), _PANEL_WH_DEF)
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    s = max(W / img.width, H / img.height)
    im2 = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))))
    x = (im2.width - W) // 2
    y = int((im2.height - H) * 0.78)
    buf = io.BytesIO()
    im2.crop((x, y, x + W, y + H)).save(buf, format="PNG")
    return buf.getvalue()


def verificar_ilustracion(api_key, png_bytes, escena, timeout=60):
    """Mira la ilustración generada con un modelo de visión y devuelve (ok, motivo).
    Chequea lo que más sale mal: texto/letras pegadas, personajes deformes o
    cortados, y que la imagen tenga que ver con la escena pedida. Best-effort:
    si el QA falla (red, etc.) se considera OK — no frena la venta."""
    import base64 as _b64
    import urllib.request as _rq
    try:
        body = json.dumps({
            "model": os.environ.get("OPENAI_QA_MODEL", "gpt-4o-mini"),
            "max_tokens": 60,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text":
                 "Sos control de calidad de ilustraciones de un libro infantil. "
                 "Mirá SOLO si la imagen tiene un defecto GRAVE que haría que un "
                 "cliente que pagó la devuelva. Marcá MAL únicamente si ves alguno "
                 "de estos: (1) palabras o letras legibles escritas en la imagen "
                 "(estrellas, manchas o adornos NO cuentan), (2) un personaje con el "
                 "cuerpo deforme o roto (miembros fusionados, retorcidos, dos cabezas), "
                 "(3) un animal con una cantidad de patas claramente incorrecta para "
                 "su especie (una pata levantada saludando SUMA; la cola NO es una "
                 "pata), (4) un personaje con la CARA o gran parte del cuerpo CORTADA "
                 "por el borde de la imagen (que roce el borde pero se vea completo "
                 "es OK). "
                 "NO mires ni marques NADA de esto (siempre respondé OK): la pose "
                 "(de frente, de espaldas o de costado da igual), la expresión o si "
                 "tiene los ojos abiertos/cerrados, si la escena coincide o no con "
                 "algo puntual, cuántos personajes hay, el estilo, los colores, ni "
                 "el encuadre mientras no haya un corte grave de cara/cuerpo. "
                 "Ante CUALQUIER duda respondé OK. Respondé SOLO 'OK' o "
                 "'MAL: <motivo corto>'."},
                {"type": "image_url", "image_url": {"url":
                 "data:image/png;base64," + _b64.b64encode(png_bytes).decode(),
                 "detail": "high"}}]}]}).encode()
        req = _rq.Request(_QA_URL, data=body, method="POST", headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json"})
        with _rq.urlopen(req, timeout=timeout) as r:
            out = json.loads(r.read())
        resp = (out["choices"][0]["message"]["content"] or "").strip()
        if resp.upper().startswith("OK"):
            return True, ""
        return False, resp[:160]
    except Exception as e:
        return True, "qa saltado: %s" % str(e)[:80]


def _es_ancla_elenco(cruda):
    """Heurística: ¿esta escena (texto CRUDO, sin formatear) muestra el elenco
    fijo/secundario (y no solo al protagonista solo)? Sirve para elegir qué
    página generada usar como referencia de continuidad del ELENCO."""
    return ("{alto}" in cruda or "{fuerte}" in cruda or "{chiquito}" in cruda
            or "personajes del tema" in cruda)


def _autoancla(tema, historia, catalogo, edad, dest_dir, excluir):
    """Si `dest_dir` ya tiene páginas generadas de ANTES (p.ej. se regeneran
    solo algunas páginas de un combo ya cacheado), busca ahí una que sirva de
    referencia de PROTAGONISTA y otra de ELENCO — así las páginas nuevas
    quedan parecidas a las vecinas que ya estaban bien, en vez de arrancar
    de cero. `excluir`: índices que se van a regenerar ahora (no sirven de
    ancla porque pueden ser justamente los que están mal)."""
    ref_p = ref_e = None
    if not dest_dir or not os.path.isdir(dest_dir):
        return ref_p, ref_e
    total = libro.total_paginas(tema, edad, historia, catalogo)
    for idx in range(total):
        if ref_p is not None and ref_e is not None:
            break
        if idx in excluir:
            continue
        p = os.path.join(dest_dir, "%d.png" % idx)
        if not os.path.isfile(p):
            continue
        cruda, _ = _escena_para(tema, idx, historia=historia, catalogo=catalogo, edad=edad)
        if ref_p is None and "{protagonista}" in cruda:
            ref_p = open(p, "rb").read()
        if ref_e is None and idx >= 2 and _es_ancla_elenco(cruda):
            ref_e = open(p, "rb").read()
    return ref_p, ref_e


def generar_ilustraciones(client, tema, paginas=None, calidad="medium", progress=None,
                          dest_dir=None, genero=None, historia=None,
                          verificar=False, fallos_log=None, catalogo=False, edad=None,
                          ref_protagonista_path=None, ref_elenco_path=None):
    """Genera y guarda las ilustraciones de `paginas` (default: las 10). Devuelve la
    lista de paths escritos. `client` es ia_kit.client.OpenAIImageClient (o cualquier
    objeto con .editar(refs, prompt, size, quality=) -> bytes PNG).

    dest_dir: si se pasa, guarda en <dest_dir>/<idx>.png en vez de los overrides del
    tema — es el modo LIBRO PREMIUM (arte único por pedido; se renderiza después con
    libro.usar_escenas_dir(dest_dir)).

    CONSISTENCIA DE PERSONAJES (Pablo, 24-jul-2026 — sin esto cada página podía
    reinventar la ropa o el personaje: pasó pijama verde en una página y azul
    en la siguiente, protagonistas distintos de página en página). Además de
    la referencia de ESTILO del tema (ia_maestra.png), se encadenan DOS
    anclas más a medida que se generan las páginas EN ORDEN: la del
    PROTAGONISTA (la primera página cuya escena lo menciona) y la del ELENCO/
    extras (la primera página que muestra a los personajes secundarios). Cada
    página siguiente que vuelve a mostrar a ese personaje recibe también su
    imagen como referencia — mismo mecanismo que `aventura_ia.py`, generalizado
    acá a los libros/audiolibros del catálogo. `ref_protagonista_path` /
    `ref_elenco_path` fuerzan un ancla ya aprobada (recomendado al regenerar
    páginas sueltas de un combo ya revisado); si no se pasan, se intenta
    encontrar una en `dest_dir` (páginas ya cacheadas) y si tampoco hay, se
    arma sola con la primera página de ESTA corrida que corresponda."""
    paginas = list(paginas) if paginas is not None else \
        list(range(libro.total_paginas(tema, edad, historia, catalogo)))
    refs = referencias(tema)
    if catalogo and not refs:
        # Sin referencia el arte sale con personajes/estilo random (y el camino
        # del boceto no soporta el catálogo). Regla: tema del catálogo => tiene
        # que existir temas/<tema>/ia_maestra.png (o la hoja de stickers).
        raise RuntimeError(
            "el tema %r no tiene imagen de referencia (ia_maestra.png/stickers) "
            "— agregala antes de generar el catálogo" % tema)
    ref_protagonista = (open(ref_protagonista_path, "rb").read()
                        if ref_protagonista_path else None)
    ref_elenco = open(ref_elenco_path, "rb").read() if ref_elenco_path else None
    if ref_protagonista is None or ref_elenco is None:
        auto_p, auto_e = _autoancla(tema, historia, catalogo, edad, dest_dir, set(paginas))
        ref_protagonista = ref_protagonista or auto_p
        ref_elenco = ref_elenco or auto_e
    out = []
    for n, idx in enumerate(paginas):
        if progress:
            progress("Página %d de %d (pieza %d)…" % (n + 1, len(paginas), idx))
        cruda, _hlow = _escena_para(tema, idx, historia=historia, catalogo=catalogo, edad=edad)
        base = list(refs) if refs else [_boceto(tema, idx)]
        if ref_protagonista is not None:
            base.append(ref_protagonista)
        if ref_elenco is not None:
            base.append(ref_elenco)
        r = base
        prompt = prompt_pagina(tema, idx, genero=genero, historia=historia,
                               catalogo=catalogo, edad=edad)
        if not refs:
            prompt = ("Redibujá este boceto como ilustración profesional, conservando "
                      "la composición. " + prompt)
        tam = tam_pagina(tema, idx, edad=edad, historia=historia, catalogo=catalogo)
        try:
            raw = client.editar(r, prompt, tam, quality=calidad)
        except Exception as e:
            # Un bloqueo de moderación de OpenAI (o cualquier error de red/API) en
            # UNA página NO puede tirar abajo el combo entero (pasó 24-jul-2026:
            # una página con "S dorada" en el prompt disparó moderation_blocked y
            # crasheó toda la corrida, perdiendo las páginas ya generadas antes).
            # Se trata igual que un rechazo de QA: se deja constancia y se sigue.
            if fallos_log:
                with open(fallos_log, "a", encoding="utf-8") as fl:
                    fl.write("pagina %d: ERROR generando: %s\n" % (idx, str(e)[:300]))
            if progress:
                progress("Página %d: error generando (%s) — se sigue con las demás"
                         % (idx, str(e)[:120]))
            continue
        qa_key = os.environ.get("OPENAI_API_KEY")
        if verificar and qa_key:
            ok, motivo = verificar_ilustracion(qa_key, _como_en_panel(raw, idx), prompt)
            if not ok:
                if progress:
                    progress("Página %d rechazada por QA (%s) — reintento…" % (idx, motivo))
                try:
                    raw2 = client.editar(r, prompt + " MUY IMPORTANTE: " + motivo,
                                         tam, quality=calidad)
                    ok2, motivo2 = verificar_ilustracion(qa_key, _como_en_panel(raw2, idx), prompt)
                except Exception as e:
                    ok2, motivo2 = False, "error en reintento: %s" % str(e)[:200]
                if ok2:
                    raw = raw2
                else:
                    # dos rechazos: NO guardar (la página cae al arte del tema) y
                    # dejar constancia para revisión humana
                    if fallos_log:
                        with open(fallos_log, "a", encoding="utf-8") as fl:
                            fl.write("pagina %d: %s / %s\n" % (idx, motivo, motivo2))
                    if progress:
                        progress("Página %d: QA rechazó 2 veces — usa arte del tema" % idx)
                    continue
        img = Image.open(io.BytesIO(raw)).convert("RGBA")   # valida que sea imagen
        if dest_dir:
            dest = os.path.join(dest_dir, "%d.png" % idx)
        else:
            dest = libro.override_escena_path(tema, idx)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        img.save(dest)
        out.append(dest)
        if ref_protagonista is None and "{protagonista}" in cruda:
            ref_protagonista = raw          # ancla para el resto de la corrida
        if ref_elenco is None and idx >= 2 and _es_ancla_elenco(cruda):
            ref_elenco = raw
    return out


# ---------------------------------------------------------------------------
# CACHE de arte del catálogo: generar UNA vez por combo (tema, historia,
# género) -> revisar -> REUSAR en cada venta. Clave = índice del libro LARGO
# (20 págs); la versión corta (hasta 3 años) usa un SUBCONJUNTO de las mismas
# escenas (CORTO_IDX), así el arte largo cubre las dos edades. La voz NO se
# cachea (dice el nombre del nene) — se narra por pedido.
# ---------------------------------------------------------------------------
CATALOGO_ARTE = os.path.join(KIT, "catalogo_arte")


def _genero_arte(genero):
    g = (genero or "").strip().lower()
    return "nena" if g in ("nena", "niña", "nina", "mujer", "girl", "f") else "nene"


def indices_largo(tema, edad, historia):
    """Índice de render del pedido -> índice del libro LARGO (clave del cache).
    Libro largo: identidad. Libro corto (12 págs): portada y dedicatoria (0,1),
    las 9 escenas de CORTO_IDX, y el FIN largo (19)."""
    total = libro.total_paginas(tema, edad, historia, True)
    if total - 3 >= libro.PAGINAS_HISTORIA_LARGO:
        return list(range(total))
    return [0, 1] + [2 + j for j in libro.CORTO_IDX] + \
           [2 + libro.PAGINAS_HISTORIA_LARGO]


def _escena_larga(tema, li, historia, genero="nene"):
    """(texto de escena renderizado, ¿lleva protagonista?) del índice LARGO li."""
    h = dict(libro.HISTORIAS.get(tema, libro.HISTORIA_DEFAULT))
    elenco = _elenco(tema, historia)
    h["protagonista"] = _protagonista(genero) + elenco.pop("protagonista_extra", "")
    h.update(elenco)
    if li == 0:
        esc = _ESCENAS_LARGO[0]
    elif li == 1:
        esc = _ESCENAS_LARGO[1]
    elif li >= 19:
        esc = _ESCENAS_LARGO[-1]
    else:
        esc = _ESCENAS_POR_HISTORIA_LARGO[historia][li]
    return esc.format(**h), ("{protagonista}" in esc)


def _piso_blanco(path, umbral=0.45):
    """True si la escena quedó 'flotando': gran parte de la imagen es un fondo
    liso claro (blanco/crema) sin escenario — regla de Pablo: escenario completo
    SIEMPRE (piso con textura + fondo del lugar). Detecta el color de fondo por
    las esquinas y mide cuánta imagen es ese color casi uniforme. Gratis y
    determinista. La dedicatoria (fondo claro a propósito) NO pasa por acá."""
    try:
        im = Image.open(path).convert("RGB").resize((80, 80))
        px = im.load()
        esquinas = [px[x, y] for x, y in ((2, 2), (77, 2), (2, 77), (77, 77))]
        base = tuple(sum(c[i] for c in esquinas) // 4 for i in range(3))
        if min(base) < 200:                 # fondo oscuro/colorido = hay escenario
            return False
        cerca = sum(1 for y in range(80) for x in range(80)
                    if all(abs(px[x, y][i] - base[i]) <= 14 for i in range(3)))
        return cerca / 6400 > umbral
    except Exception:
        return False


def qa_vision_catalogo(api_key, png_bytes, tema, escena, espera_nino,
                       ref_bytes=None, ref_protagonista=None, ref_elenco=None,
                       timeout=90):
    """(ok, motivo) — QA de visión dirigido a los errores históricos del
    catálogo: patas de más / protagonista que no es un chico humano / personajes
    de otra temática / personaje duplicado / inconsistencia con la página
    anterior. Compara contra la REFERENCIA del tema (sus personajes NUNCA son
    intrusos — p.ej. el elefante obrero de construcción) y, si se pasan,
    contra las referencias de PROTAGONISTA/ELENCO ya ancladas en esta corrida
    (Pablo, 24-jul-2026 — el pijama cambiaba de color de una página a otra sin
    que nada lo detectara). Best-effort: si el QA falla (red, etc.) devuelve
    OK para no frenar la venta."""
    import base64 as _b64
    import urllib.request as _rq
    nino = ("nino_falta=true si NO aparece un nene o nena HUMANO como figura "
            "principal, o si el protagonista parece ser un animal o mascota "
            "en vez de un chico humano; "
            if espera_nino else
            "nino_falta=false SIEMPRE (esta escena no lleva chico); ")
    consist = (
        "También se incluyen imágenes de referencia del PROTAGONISTA y/o del "
        "ELENCO de esta misma historia (ya aprobadas en páginas anteriores): "
        "inconsistente=true SOLO si el protagonista o algún personaje "
        "secundario de la escena a evaluar tiene un diseño, ropa, color o "
        "peinado CLARAMENTE distinto al de esas referencias (por ejemplo, "
        "pijama de otro color, otro tipo de prenda, otro peinado). Si no hay "
        "diferencia clara o no se puede comparar bien, poné false. "
        if (ref_protagonista or ref_elenco) else
        "inconsistente=false SIEMPRE (no hay referencia de personaje previa "
        "para comparar en esta página). ")
    txt = ("Sos QA de ilustraciones de un libro de cuentos infantil. "
           "Temática: %s. Escena esperada: %s "
           "La PRIMERA imagen es la REFERENCIA oficial del tema: TODOS los "
           "personajes que aparecen en ella son válidos (aunque sean "
           "animales), NUNCA intrusos, aparezcan donde aparezcan. Las "
           "imágenes de referencia siguientes (si las hay) son del "
           "PROTAGONISTA y del ELENCO ya aprobados. La ÚLTIMA imagen es la "
           "ilustración a evaluar. El protagonista humano (nene o nena) "
           "NUNCA es un intruso. Respondé SOLO un JSON: "
           '{"patas_mal": bool, "nino_falta": bool, "intrusos": bool, '
           '"duplicado": bool, "inconsistente": bool, "detalle": "texto corto"}. '
           "patas_mal=true si ALGÚN animal de cuatro patas tiene una cantidad "
           "de patas visiblemente incorrecta (5 o más, o 3 o menos), o si un "
           "animal en cuatro patas da la mano, choca los cinco, aplaude o "
           "saluda con una pata levantada; la cola NO es una pata. %s"
           "intrusos=true SOLO si aparecen personajes que NO están en la "
           "referencia y claramente pertenecen a OTRA temática. "
           "duplicado=true SOLO si el MISMO personaje (mismo diseño) aparece "
           "dos o más veces dentro de la escena a evaluar (dos copias del "
           "mismo personaje, o el protagonista repetido). %s"
           "Ante la MÍNIMA duda en cualquier campo, poné false."
           % (tema, escena, nino, consist))
    contenido = [{"type": "text", "text": txt}]
    if ref_bytes:
        contenido.append({"type": "image_url", "image_url": {
            "url": "data:image/png;base64," + _b64.b64encode(ref_bytes).decode(),
            "detail": "low"}})
    for extra in (ref_protagonista, ref_elenco):
        if extra:
            contenido.append({"type": "image_url", "image_url": {
                "url": "data:image/png;base64," + _b64.b64encode(extra).decode(),
                "detail": "low"}})
    contenido.append({"type": "image_url", "image_url": {
        "url": "data:image/png;base64," + _b64.b64encode(png_bytes).decode(),
        "detail": "high"}})
    try:
        body = json.dumps({"model": os.environ.get("OPENAI_QA_MODEL", "gpt-4o-mini"),
                           "max_tokens": 160,
                           "messages": [{"role": "user", "content": contenido}]}
                          ).encode()
        req = urllib.request.Request(_QA_URL, data=body, method="POST", headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            out = json.loads(r.read())
        resp = out["choices"][0]["message"]["content"] or ""
        v = json.loads(resp[resp.find("{"):resp.rfind("}") + 1])
        if (v.get("patas_mal") or v.get("nino_falta") or v.get("intrusos")
                or v.get("duplicado") or v.get("inconsistente")):
            return False, str(v.get("detalle") or "")[:160]
        return True, ""
    except Exception as e:
        return True, "qa saltado: %s" % str(e)[:80]


def arte_catalogo(client, tema, historia, genero, edad, dest_dir,
                  progress=None, fallos_log=None):
    """Arte de un pedido del catálogo usando el CACHE por combo. Si el combo ya
    está generado (y revisado), copia en segundos y NO regenera nada; si faltan
    escenas, genera SOLO esas (siempre en clave larga) y quedan cacheadas para
    la próxima venta. Devuelve los índices de render con arte listo."""
    import shutil
    hist = (historia or "").strip().lower()
    g = _genero_arte(genero)
    cache = os.path.join(CATALOGO_ARTE, tema, hist, g)
    os.makedirs(cache, exist_ok=True)
    os.makedirs(dest_dir, exist_ok=True)
    idxs = indices_largo(tema, edad, hist)
    faltan = [li for li in idxs
              if not os.path.isfile(os.path.join(cache, "%d.png" % li))]
    if faltan:
        if client is None:
            raise RuntimeError("faltan escenas del combo y no hay cliente de imágenes")
        if progress:
            progress("cache %s/%s/%s: generando %d escenas nuevas…"
                     % (tema, hist, g, len(faltan)))
        generar_ilustraciones(client, tema, paginas=faltan, dest_dir=cache,
                              genero=g, historia=hist, catalogo=True, edad="5",
                              verificar=True, progress=progress,
                              fallos_log=fallos_log)
        # QA de visión dirigido sobre lo recién generado (la misma protección
        # que el lote del catálogo, ahora también en la VENTA del customizable):
        # patas / protagonista humano / intrusos vs. la referencia del tema.
        qa_key = os.environ.get("OPENAI_API_KEY")
        if qa_key:
            refs = referencias(tema)
            ref_b = refs[0] if refs else None
            ref_p, ref_e = _autoancla(tema, hist, True, "5", cache, set())
            malas = []
            for li in faltan:
                p = os.path.join(cache, "%d.png" % li)
                if not os.path.isfile(p):
                    continue
                if li != 1 and _piso_blanco(p):        # dedicatoria es clara a propósito
                    malas.append(li)
                    if progress:
                        progress("QA pág %d: suelo blanco sin textura — se regenera" % li)
                    continue
                escena, espera = _escena_larga(tema, li, hist, g)
                ok, det = qa_vision_catalogo(qa_key, open(p, "rb").read(),
                                             tema, escena, espera, ref_b,
                                             ref_protagonista=ref_p, ref_elenco=ref_e)
                if not ok:
                    malas.append(li)
                    if progress:
                        progress("QA visión pág %d: %s — se regenera" % (li, det))
            if malas:
                generar_ilustraciones(client, tema, paginas=malas,
                                      dest_dir=cache, genero=g, historia=hist,
                                      catalogo=True, edad="5", verificar=True,
                                      progress=progress, fallos_log=fallos_log)
    elif progress:
        progress("cache %s/%s/%s: combo completo, sin regenerar" % (tema, hist, g))
    usados = []
    for j, li in enumerate(idxs):
        src = os.path.join(cache, "%d.png" % li)
        if os.path.isfile(src):                    # el QA pudo descartar alguna
            shutil.copyfile(src, os.path.join(dest_dir, "%d.png" % j))
            usados.append(j)
        elif progress:
            progress("página %d sin arte cacheado (QA lo descartó) — arte del tema" % j)
    return usados


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
