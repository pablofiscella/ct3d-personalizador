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
    "Viñeta tierna y suave de un personaje del tema saludando, estilo página de "
    "dedicatoria, fondo muy claro y despejado.",
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
    "tema despidiéndose con la mano en alto, sensación de final feliz.",
    _ESCENAS[8],   # cierre (misma escena que el legado, ahora más adelante)
    _ESCENAS[9],   # FIN
]


# Escenas por ARGUMENTO (idx 2..8 — portada/dedicatoria/fin son comunes): el arte
# por pedido (premium/audiolibro) ilustra la historia que el cliente eligió.
_ESCENAS_POR_HISTORIA = {
    "tesoro": {
        2: "Un chico dormido... no: {protagonista} descubriendo un mapa antiguo brillante que sale de una mochila, en un cuarto infantil cálido.",
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
        4: "Los personajes del tema preocupados buscando a un amiguito perdido en {mundo}, atardecer.",
        5: "Huellas pequeñitas en el suelo de {mundo} que llevan hacia una cueva; los personajes del tema las siguen con linternas.",
        6: "{protagonista} saliendo de una cueva de la mano de un personajito pequeño del tema, los demás celebrando aliviados con los brazos en alto.",
        7: "Los personajes del tema entregando {tesoro} brillante y destacado en el centro, con destellos dorados, ceremonia de héroes.",
        8: "Un cuarto infantil de noche, un chico dormido con sonrisa... mejor: la casita de noche con ventana cálida y una lucecita mágica despidiéndose.",
    },
    "gran-dia": {
        2: "Una carta de invitación gigante y festiva llegando a un cuarto infantil, confetti saliendo del sobre.",
        3: "{protagonista} con mochila caminando decidido hacia {mundo}, camino soleado con banderines a lo lejos.",
        4: "Los personajes del tema preparando una gran fiesta en {mundo}: guirnaldas, música, juegos, mucha actividad alegre.",
        5: "Una tormenta con viento desarmando las decoraciones de la fiesta en {mundo}; los personajes del tema mirando sorprendidos.",
        6: "{protagonista} organizando a los personajes del tema para reconstruir la fiesta: todos ayudando juntos, decoraciones volviendo a su lugar, trabajo en equipo.",
        7: "La gran fiesta espléndida de noche en {mundo} con luces y {tesoro} siendo entregado en el centro con destellos dorados.",
        8: "Cielo nocturno estrellado sereno sobre {mundo}, los personajes del tema despidiéndose a lo lejos con las manos en alto.",
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
        12: "{protagonista} y los personajes del tema dándose la mano en señal de "
            "promesa, mirando juntos el mapa, atardecer cálido.",
        13: _ESCENAS_POR_HISTORIA["tesoro"][8],
    },
    "rescate": {
        2: _ESCENAS_POR_HISTORIA["rescate"][2], 3: _ESCENAS_POR_HISTORIA["rescate"][3],
        4: _ESCENAS_POR_HISTORIA["rescate"][4], 5: _ESCENAS_POR_HISTORIA["rescate"][5],
        6: _ESCENAS_POR_HISTORIA["rescate"][6], 7: _ESCENAS_POR_HISTORIA["rescate"][7],
        8: "Un personajito pequeño del tema abrazando fuerte y agradecido a "
           "{protagonista}, ambiente muy tierno.",
        9: "Los personajes del tema tomados de la mano en fila caminando juntos "
           "por {mundo}, explorando con confianza.",
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
        11: "Los personajes del tema aplaudiendo y entregando {tesoro} a "
            "{protagonista} como agradecimiento.",
        12: "{protagonista} pensativo y feliz, rodeado de los personajes del "
            "tema, ambiente de cierre cálido.",
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
        12: "{protagonista} rodeado de todos los personajes del tema en un "
            "abrazo grupal, ambiente muy cálido.",
        13: "Una casita de noche con ventana cálida iluminada, ambiente "
            "tranquilo tras un día de buenas acciones.",
    },
}


def _paleta(tema):
    import json
    try:
        k = json.load(open(os.path.join(TEMAS, tema, "tema.json"))).get("kit") or {}
    except Exception:
        k = {}
    return {"accent": k.get("accent") or "#6B5BD2", "ink": k.get("ink") or "#4a4a4a"}


def tam_pagina(tema, idx):
    """La página FIN es a hoja completa (vertical); el resto son paneles ~cuadrados."""
    if idx == libro.total_paginas(tema) - 1:
        return _VERTICAL
    # la dedicatoria va en un panel apaisado (700x524): generarla cuadrada
    # obligaba a recortar 12%% arriba y abajo — apaisada casi no se recorta
    if idx == 1:
        return _APAISADA
    return _CUADRADA


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


def prompt_pagina(tema, idx, genero=None, historia=None):
    """Prompt de la ilustración de la página idx, con la ambientación de la historia
    del tema (libro.HISTORIAS) y el mismo bloque de estilo del resto del kit.
    genero («nena»/«nene», opcional): cómo dibujar al protagonista en las escenas
    donde aparece — lo usa el libro premium, que ilustra por pedido."""
    h = dict(libro.HISTORIAS.get(tema, libro.HISTORIA_DEFAULT))
    h["protagonista"] = _protagonista(genero)
    pal = _paleta(tema)
    extendido = libro.paginas_historia(tema) > libro.PAGINAS_HISTORIA
    tabla = _ESCENAS_POR_HISTORIA_EXT if extendido else _ESCENAS_POR_HISTORIA
    fallback = _ESCENAS_EXT if extendido else _ESCENAS
    arco = tabla.get((historia or "").strip().lower(), {})
    escena = arco.get(idx, fallback[idx]).format(**h)
    return (
        "Ilustración para la página de un libro de cuentos infantil profesional. "
        "Escena: %s "
        "Estilo: ilustración infantil cálida, formas suaves y redondeadas, colores "
        "planos con paleta acento %s y tinta %s. "
        "Usá los personajes de las imágenes de referencia manteniendo su diseño. "
        "La escena llena TODA la imagen, sin marcos, bordes ni viñetas. "
        "IMPORTANTE: los personajes SIEMPRE completos y lejos de los bordes de la "
        "imagen (dejá margen de seguridad alrededor: al encuadrar la página se "
        "recortan los bordes y no se les puede cortar la cara ni el cuerpo). "
        "IMPORTANTE: cada animal con la cantidad EXACTA de patas de su especie "
        "(4 patas: nunca una de más ni de menos, ni siquiera si está saludando o "
        "en movimiento — la cola es la cola, no una pata extra). Si un personaje "
        "saluda con una pata/mano levantada, dibujalo SIEMPRE de pie con las otras "
        "3 patas apoyadas y bien separadas (nunca sentado saludando: sentado es más "
        "difícil de dibujar bien y las patas quedan amontonadas o poco claras). "
        "Importante: NO escribas ningún texto, número ni letra (no text, no letters)."
        % (escena, pal["accent"], pal["ink"])
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
                 "Ilustración de libro infantil. Escena pedida: «%s». "
                 "¿Tiene alguno de estos problemas de forma EVIDENTE e inaceptable? "
                 "(1) palabras o letras legibles dentro de la imagen (las estrellas, "
                 "manchas o decoraciones NO cuentan), (2) personajes claramente "
                 "deformes o rotos, (3) la imagen no tiene NINGUNA relación con la "
                 "escena, (4) algún personaje TOCANDO un borde de la imagen (al "
                 "encuadrar la página el borde se recorta y le cortaría la cara o "
                 "el cuerpo — eso es MAL aunque en esta imagen se vea completo), "
                 "(5) algún animal con una cantidad de patas/piernas incorrecta para "
                 "su especie (contá con cuidado: una pata levantada saludando SUMA, "
                 "la cola NO es una pata). "
                 "Ante la duda en 1-3 respondé OK — solo marcá MAL si un cliente "
                 "que pagó lo devolvería. En 4 y 5 mirá con detenimiento antes de "
                 "responder OK. Respondé SOLO 'OK' o 'MAL: <motivo corto>'."
                 % escena[:400]},
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
                          verificar=False, fallos_log=None):
    """Genera y guarda las ilustraciones de `paginas` (default: las 10). Devuelve la
    lista de paths escritos. `client` es ia_kit.client.OpenAIImageClient (o cualquier
    objeto con .editar(refs, prompt, size, quality=) -> bytes PNG).

    dest_dir: si se pasa, guarda en <dest_dir>/<idx>.png en vez de los overrides del
    tema — es el modo LIBRO PREMIUM (arte único por pedido; se renderiza después con
    libro.usar_escenas_dir(dest_dir))."""
    paginas = list(paginas) if paginas is not None else list(range(libro.total_paginas(tema)))
    refs = referencias(tema)
    out = []
    for n, idx in enumerate(paginas):
        if progress:
            progress("Página %d de %d (pieza %d)…" % (n + 1, len(paginas), idx))
        r = refs or [_boceto(tema, idx)]
        prompt = prompt_pagina(tema, idx, genero=genero, historia=historia)
        if not refs:
            prompt = ("Redibujá este boceto como ilustración profesional, conservando "
                      "la composición. " + prompt)
        raw = client.editar(r, prompt, tam_pagina(tema, idx), quality=calidad)
        qa_key = os.environ.get("OPENAI_API_KEY")
        if verificar and qa_key:
            ok, motivo = verificar_ilustracion(qa_key, _como_en_panel(raw, idx), prompt)
            if not ok:
                if progress:
                    progress("Página %d rechazada por QA (%s) — reintento…" % (idx, motivo))
                raw2 = client.editar(r, prompt + " MUY IMPORTANTE: " + motivo,
                                     tam_pagina(tema, idx), quality=calidad)
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
