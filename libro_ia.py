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
    "Viñeta tierna y suave de un personaje del tema sonriendo con dulzura, estilo "
    "página de dedicatoria, fondo muy claro y despejado.",
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
    "Un dormitorio infantil de noche acogedor: una cama con un sobre dorado "
    "brillante asomando bajo la almohada, luz de luna por la ventana.",
    "Un remolino mágico de luces de colores llenando un dormitorio de noche, "
    "destellos y estrellas, sensación de comienzo de viaje.",
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
        "Los personajes del tema alrededor de {protagonista} mirando el mapa "
        "juntos con ojos brillantes, listos para la búsqueda.",
        "Un rincón escondido de {mundo} lleno de brillitos; una única lucecita "
        "con forma de estrella destaca y {protagonista} la señala con asombro.",
        "Una llave dorada brillante junto a una puerta secreta enorme; los "
        "personajes del tema empujándola todos juntos con esfuerzo.",
        "Un pasillo oscuro y misterioso con ecos en {mundo}; momento de "
        "preocupación: {desafio}.",
        "{protagonista} con los ojos cerrados pensando, una idea iluminándose "
        "como un destello suave sobre la cabeza.",
        "Momento heroico: {protagonista} que {solucion}; al fondo del pasillo "
        "aparece un cofre dorado.",
        "Un cofre dorado con tres cerraduras brillantes; {protagonista} y los "
        "personajes del tema observándolo con curiosidad.",
        "{protagonista} girando las cerraduras del cofre mientras los "
        "personajes del tema acompañan expectantes alrededor.",
        "El cofre abierto de golpe irradiando luz dorada, con {tesoro} "
        "brillando adentro; todos maravillados.",
        "El mapa dado vuelta mostrando una segunda cara que brilla con un "
        "camino dorado nuevo; sorpresa y asombro.",
        "El más sabio de los personajes del tema contando una historia al "
        "grupo en ronda, ambiente cálido de atardecer.",
        "Los personajes del tema despidiendo a {protagonista} en la salida de "
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
        "Los personajes del tema haciendo algo increíble propio del tema; "
        "{protagonista} mirando con ojos enormes de admiración.",
        "{protagonista} pidiendo con ilusión que le enseñen; los personajes "
        "del tema entusiasmados alrededor.",
        "Los personajes del tema mostrando cómo se hace, despacito; "
        "{protagonista} mirando sin pestañear.",
        "{protagonista} de cola en el piso tras un intento fallido gracioso, "
        "riéndose; los personajes del tema sonriendo con cariño.",
        "El más viejito de los personajes del tema animando con gesto tierno "
        "a {protagonista}.",
        "{protagonista} practicando una y otra vez con esfuerzo; los "
        "personajes del tema alentando desde el costado.",
        "¡Primer logro! {protagonista} dando un gran salto de alegría; los "
        "personajes del tema festejando amontonados de risa.",
        "Preparativos de una gran muestra en {mundo}: un escenario armándose, "
        "entusiasmo general.",
        "Un personaje nuevo chiquito y tímido mirando todo desde lejos; "
        "{protagonista} mirando hacia ese rincón con gesto amable.",
        "{protagonista} acercándose despacito al personaje nuevo tímido, "
        "gesto de invitación amable.",
        "{protagonista} enseñando de a pasitos al personaje nuevo, con mucha "
        "paciencia, ambiente cálido.",
        "La gran muestra en {mundo}: {protagonista} en el escenario logrando "
        "su número, el personaje nuevo lográndolo también al lado; el público "
        "del tema festejando con sonrisas enormes.",
        "El personaje nuevo saltando de alegría junto a {protagonista}, "
        "gratitud y orgullo.",
        "El más viejito de los personajes del tema hablando con cariño al "
        "grupo en ronda; {protagonista} en el centro, ambiente emotivo.",
        "Los personajes del tema entregando {tesoro} brillante y destacado a "
        "{protagonista}, agradecimiento.",
        "Un cuarto infantil de noche; {protagonista} en la cama con una "
        "sonrisa soñadora.",
        "Una casita de noche con ventana cálida iluminada, cierre tierno y "
        "feliz.",
    ]),
    "ayudar-a-todos": _tabla17([
        "Un problema grandote y vistoso en {mundo} (un gran enredo o desorden "
        "que bloquea el lugar); los personajes del tema mirándolo sin saber "
        "qué hacer.",
        "Los personajes del tema desanimados; {protagonista} respirando hondo "
        "con un destello de idea sobre la cabeza.",
        "Los personajes del tema sentados cabizbajos, desanimados.",
        "{protagonista} proponiendo con entusiasmo resolverlo entre todos; "
        "los personajes del tema levantando la cabeza con esperanza.",
        "El personaje más chiquito escondiéndose en un rinconcito, "
        "creyéndose demasiado pequeño.",
        "{protagonista} sonriendo con cariño al personaje más chiquito, "
        "dándole importancia.",
        "{protagonista} repartiendo tareas: el más alto, el más fuerte y el "
        "más rápido, cada uno listo; el más chiquito adelante con la misión "
        "especial.",
        "El grupo esforzándose con el problema grandote, que todavía no "
        "cede; caras de esfuerzo.",
        "El personaje más chiquito metiéndose por un huequito imposible y "
        "destrabando la primera parte; todos gritando de alegría.",
        "El más alto alcanzando lo inalcanzable y el más fuerte empujando "
        "con todo; {protagonista} coordinando como director de orquesta.",
        "Un tropezón grupal gracioso: todos sosteniéndose en grupo para no "
        "caer, riéndose del susto.",
        "¡Lo lograron! El problema resuelto, {mundo} en paz otra vez; "
        "festejo grupal enorme.",
        "El personaje más chiquito en el medio de la ronda, festejado como "
        "un héroe.",
        "{protagonista} hablando al grupo en ronda, todos asintiendo con "
        "sonrisas.",
        "Los personajes del tema entregando {tesoro} brillante y destacado a "
        "{protagonista}, celebración.",
        "Un cuarto infantil de noche; {protagonista} acurrucándose en la "
        "cama, sonrisa tranquila.",
        "Una casita de noche con ventana cálida iluminada, cielo estrellado "
        "sereno.",
    ]),
    "gran-viaje": _tabla17([
        "Un paquetito brillante con moño en la puerta de un dormitorio "
        "infantil, luz de atardecer, sensación de misión por empezar.",
        "{protagonista} con una mochila liviana saliendo al anochecer con "
        "paso decidido, primer paso del gran viaje.",
        "Los personajes del tema esperando a {protagonista} con un mapa de "
        "recorrido desplegado: caminitos y tres banderitas (dibujo, sin letras).",
        "Los personajes del tema contando la misión en ronda a "
        "{protagonista}, gesto de urgencia dulce; la luna saliendo.",
        "El grupo repartiéndose el viaje; {protagonista} sosteniendo con "
        "cuidado el paquetito brillante.",
        "El grupo de viaje cantando por un camino de {mundo} mientras el sol "
        "se esconde, ambiente alegre.",
        "Un viento travieso en forma de remolino tratando de llevarse el "
        "paquetito; {protagonista} abrazándolo fuerte.",
        "El viento despejando el cielo: las nubes yéndose y un cielo lleno "
        "de estrellas apareciendo.",
        "{protagonista} señalando un atajo iluminado por las estrellas; el "
        "grupo avanzando con energía.",
        "Una parada del viaje con chocolate calentito humeante; los "
        "personajes del tema tomando fuerzas, tacitas y vapor.",
        "El tramo más oscuro del camino de noche; el grupo avanzando bien "
        "juntito, {protagonista} adelante con paso valiente.",
        "La llegada al amanecer: el más viejito de los personajes del tema "
        "abriendo el paquetito con ojos brillantes de emoción, primer rayito "
        "de sol.",
        "El más viejito del tema con el regalo bien cerquita, muy emocionado; "
        "todos alrededor con ternura.",
        "El festejo del viejito arrancando con el primer sol; {protagonista} "
        "en el lugar de honor.",
        "Los personajes del tema entregando {tesoro} brillante y destacado a "
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
        "Banderines y preparativos de los Grandes Juegos en {mundo}; los "
        "personajes del tema desanimados a un costado.",
        "{protagonista} animando al equipo con una sonrisa, gesto de "
        "arranque de entrenamiento.",
        "Entrenamiento desastroso y gracioso: los personajes del tema "
        "corriendo para lados distintos, chocándose con suavidad y "
        "terminando en el piso riéndose.",
        "{protagonista} explicando el plan al equipo en ronda, todos atentos "
        "y con ganas.",
        "Cada personaje entrenando lo suyo: el más rápido corriendo, el más "
        "fuerte saltando, el más chiquito ensayando una jugada secreta.",
        "El equipo entrenando cada día mejor, pasándose y esperándose, "
        "ambiente de progreso alegre.",
        "El capitán del equipo a un costado con una venda simpática, carita "
        "de no poder jugar; el equipo alrededor, preocupado.",
        "{protagonista} juntando al equipo en ronda con gesto de ánimo; el "
        "capitán sonriendo desde el costado.",
        "La entrada a los Grandes Juegos: el equipo desfilando con el "
        "capitán al frente alentando desde el costado; tribunas de {mundo} "
        "llenas.",
        "Las primeras pruebas de los juegos: el equipo mejorando prueba a "
        "prueba, energía creciente.",
        "La prueba final cabeza a cabeza con el otro equipo; expectativa "
        "máxima en las tribunas de {mundo}.",
        "La jugada secreta del más chiquito saliendo perfecta; el público de "
        "{mundo} festejando con saltos y confetti.",
        "Los dos equipos festejando juntos y mezclados, alegría deportiva "
        "enorme.",
        "El capitán muy emocionado junto al equipo, momento tierno de "
        "orgullo.",
        "Premiación: los personajes del tema entregando {tesoro} brillante y "
        "destacado a {protagonista}.",
        "Un cuarto infantil de noche; {protagonista} en la cama con una "
        "sonrisa, una cintita de premio colgada cerca.",
        "Una casita de noche con ventana cálida; banderines de los Grandes "
        "Juegos a lo lejos en {mundo}.",
    ]),
}


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


def prompt_pagina(tema, idx, genero=None, historia=None, catalogo=False, edad=None):
    """Prompt de la ilustración de la página idx, con la ambientación de la historia
    del tema (libro.HISTORIAS) y el mismo bloque de estilo del resto del kit.
    genero («nena»/«nene», opcional): cómo dibujar al protagonista en las escenas
    donde aparece — lo usa el libro premium, que ilustra por pedido.
    catalogo=True (audiolibro): usa las escenas de la versión larga (17 páginas) con
    largo por edad; la versión corta (9, hasta 3 años) mapea con libro.CORTO_IDX."""
    h = dict(libro.HISTORIAS.get(tema, libro.HISTORIA_DEFAULT))
    h["protagonista"] = _protagonista(genero)
    pal = _paleta(tema)
    hlow = (historia or "").strip().lower()
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


def generar_ilustraciones(client, tema, paginas=None, calidad="medium", progress=None,
                          dest_dir=None, genero=None, historia=None,
                          verificar=False, fallos_log=None, catalogo=False, edad=None):
    """Genera y guarda las ilustraciones de `paginas` (default: las 10). Devuelve la
    lista de paths escritos. `client` es ia_kit.client.OpenAIImageClient (o cualquier
    objeto con .editar(refs, prompt, size, quality=) -> bytes PNG).

    dest_dir: si se pasa, guarda en <dest_dir>/<idx>.png en vez de los overrides del
    tema — es el modo LIBRO PREMIUM (arte único por pedido; se renderiza después con
    libro.usar_escenas_dir(dest_dir))."""
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
    out = []
    for n, idx in enumerate(paginas):
        if progress:
            progress("Página %d de %d (pieza %d)…" % (n + 1, len(paginas), idx))
        r = refs or [_boceto(tema, idx)]
        prompt = prompt_pagina(tema, idx, genero=genero, historia=historia,
                               catalogo=catalogo, edad=edad)
        if not refs:
            prompt = ("Redibujá este boceto como ilustración profesional, conservando "
                      "la composición. " + prompt)
        tam = tam_pagina(tema, idx, edad=edad, historia=historia, catalogo=catalogo)
        raw = client.editar(r, prompt, tam, quality=calidad)
        qa_key = os.environ.get("OPENAI_API_KEY")
        if verificar and qa_key:
            ok, motivo = verificar_ilustracion(qa_key, _como_en_panel(raw, idx), prompt)
            if not ok:
                if progress:
                    progress("Página %d rechazada por QA (%s) — reintento…" % (idx, motivo))
                raw2 = client.editar(r, prompt + " MUY IMPORTANTE: " + motivo,
                                     tam, quality=calidad)
                ok2, motivo2 = verificar_ilustracion(qa_key, _como_en_panel(raw2, idx), prompt)
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
    h["protagonista"] = _protagonista(genero)
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
                       ref_bytes=None, timeout=90):
    """(ok, motivo) — QA de visión dirigido a los 3 errores históricos del
    catálogo: patas de más / protagonista que no es un chico humano / personajes
    de otra temática. Compara contra la REFERENCIA del tema (sus personajes
    NUNCA son intrusos — p.ej. el elefante obrero de construcción). Best-effort:
    si el QA falla (red, etc.) devuelve OK para no frenar la venta."""
    import base64 as _b64
    import urllib.request as _rq
    nino = ("nino_falta=true si NO aparece un nene o nena HUMANO como figura "
            "principal, o si el protagonista parece ser un animal o mascota "
            "en vez de un chico humano; "
            if espera_nino else
            "nino_falta=false SIEMPRE (esta escena no lleva chico); ")
    txt = ("Sos QA de ilustraciones de un libro de cuentos infantil. "
           "Temática: %s. Escena esperada: %s "
           "La PRIMERA imagen es la REFERENCIA oficial del tema: TODOS los "
           "personajes que aparecen en ella son válidos (aunque sean "
           "animales), NUNCA intrusos, aparezcan donde aparezcan. La SEGUNDA "
           "imagen es la ilustración a evaluar. El protagonista humano (nene "
           "o nena) NUNCA es un intruso. Respondé SOLO un JSON: "
           '{"patas_mal": bool, "nino_falta": bool, "intrusos": bool, '
           '"detalle": "texto corto"}. '
           "patas_mal=true si ALGÚN animal de cuatro patas tiene una cantidad "
           "de patas visiblemente incorrecta (5 o más, o 3 o menos), o si un "
           "animal en cuatro patas da la mano, choca los cinco, aplaude o "
           "saluda con una pata levantada; la cola NO es una pata. %s"
           "intrusos=true SOLO si aparecen personajes que NO están en la "
           "referencia y claramente pertenecen a OTRA temática. Ante la "
           "MÍNIMA duda en un campo, poné false." % (tema, escena, nino))
    contenido = [{"type": "text", "text": txt}]
    if ref_bytes:
        contenido.append({"type": "image_url", "image_url": {
            "url": "data:image/png;base64," + _b64.b64encode(ref_bytes).decode(),
            "detail": "low"}})
    contenido.append({"type": "image_url", "image_url": {
        "url": "data:image/png;base64," + _b64.b64encode(png_bytes).decode(),
        "detail": "high"}})
    try:
        body = json.dumps({"model": os.environ.get("OPENAI_QA_MODEL", "gpt-4o-mini"),
                           "max_tokens": 140,
                           "messages": [{"role": "user", "content": contenido}]}
                          ).encode()
        req = urllib.request.Request(_QA_URL, data=body, method="POST", headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            out = json.loads(r.read())
        resp = out["choices"][0]["message"]["content"] or ""
        v = json.loads(resp[resp.find("{"):resp.rfind("}") + 1])
        if v.get("patas_mal") or v.get("nino_falta") or v.get("intrusos"):
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
                                             tema, escena, espera, ref_b)
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
