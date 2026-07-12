"""aventura_ia.py — ilustraciones IA del prototipo "Elegí tu aventura": UNA imagen POR
NODO del grafo (aventura.AVENTURAS), a diferencia de libro_ia.py que ilustra las 10
páginas fijas del libro lineal.

Reusa el mismo bloque de reglas de estilo/consistencia de personajes que libro_ia
(protagonista humano de espaldas, 4 patas exactas por animal, escenario completo, plano
abierto con aire en los bordes — reglas afinadas con iteración real) y la referencia de
estilo del tema (temas/<tema>/ia_maestra.png). Se guarda en
temas/<tema>/overrides/aventura/<nodo_id>.png — CARPETA PROPIA, nunca pisa
temas/<tema>/overrides/libro/ (esas imágenes son del libro lineal, un producto distinto).

Uso: OPENAI_API_KEY=... python aventura_ia.py <tema> [nodo_id]
"""
import io
import os

from PIL import Image

import aventura
import libro_ia

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")

_APAISADA = "1536x1024"

# {protagonista} SIEMPRE como sujeto seguido de GERUNDIO (nunca un adjetivo tipo
# "parado/parada"): así una sola escena sirve para "un nene..." y "una nena..." sin
# problema de concordancia de género (mismo truco que usa libro_ia._ESCENAS_*).
_ESCENAS = {
    "safari": {
        # ── espina 1-4 ──────────────────────────────────────────────────────
        "hook": "{protagonista} encontrando un mapa viejo y doblado en el fondo de "
               "una mochila abierta, dentro de una carpa de campamento acogedora, "
               "con una X dorada brillando en el papel.",
        "camino": "{protagonista} saliendo de un campamento de safari al amanecer, "
                 "con una mochila al hombro, caminando hacia la sabana dorada bajo "
                 "un cielo rosado de primera luz.",
        "sabana": "{protagonista} caminando entre pastizales altos y dorados de la "
                 "sabana, rodeado a lo lejos de cebras y jirafas pastando "
                 "tranquilas bajo el sol.",
        "bifurcacion": "{protagonista} mirando un mapa viejo desplegado en las "
                       "manos, en la entrada de la sabana dorada del safari, donde "
                       "el camino se bifurca: un sendero baja hacia un río a lo "
                       "lejos, y otro sube hacia una montaña rocosa. Luz cálida de "
                       "mañana.",
        # ── rama río 5-7 ────────────────────────────────────────────────────
        "rio_1": "{protagonista} caminando por la orilla de un río en la sabana, "
                "con pájaros de colores volando sobre los juncos y un grupo de "
                "elefantes chapoteando en el agua a lo lejos. En la otra orilla, "
                "una familia de monitos agitando los brazos pidiendo ayuda.",
        "rio_2": "{protagonista} mirando hacia la otra orilla del río, donde una "
                "familia de monitos agita los brazos pidiendo ayuda desde unas "
                "rocas.",
        "rio_3": "{protagonista} caminando con cuidado sobre piedras dentro de un "
                "río poco profundo, acercándose a una familia de monitos que lo "
                "esperan aliviados en la otra orilla.",
        # ── rama montaña 5-7 ────────────────────────────────────────────────
        "montana_1": "{protagonista} subiendo por rocas doradas iluminadas por el "
                     "sol, en la ladera empinada de una montaña rocosa de la "
                     "sabana.",
        "montana_2": "{protagonista} agachado mirando unas huellas extrañas "
                     "marcadas en el polvo de un sendero rocoso, que se pierden "
                     "entre las piedras.",
        "montana_3": "{protagonista} subiendo por rocas doradas iluminadas por el "
                     "sol, llegando a la entrada oscura de una cueva en la ladera "
                     "de una montaña rocosa. Una pequeña estrella tallada marca la "
                     "entrada de la cueva.",
        # ── espina 8-15 ─────────────────────────────────────────────────────
        "reencuentro": "{protagonista} agachándose para levantar un pedazo de mapa "
                       "viejo y rasgado, enganchado en las ramas de un arbusto, con "
                       "una gran meseta dorada de fondo.",
        "jirafas": "{protagonista} caminando por una meseta dorada de la sabana, "
                  "con un grupo de jirafas altas estirando el cuello con "
                  "curiosidad para mirarlo pasar.",
        "ravine": "{protagonista} cruzando con los brazos abiertos un tronco caído "
                 "que hace de puente sobre una pequeña quebrada rocosa de la "
                 "sabana.",
        "marcas": "{protagonista} observando unas marcas doradas y brillantes "
                 "talladas sobre unas rocas de la sabana, como pistas antiguas de "
                 "un camino.",
        "tormenta": "{protagonista} cubriéndose la cara con un brazo mientras el "
                    "viento levanta arena y hojas a su alrededor, bajo un cielo "
                    "gris de tormenta en la sabana.",
        "refugio": "{protagonista} agachado y a resguardo detrás de unas piedras "
                  "grandes, junto a un grupo de animales de la selva también "
                  "refugiados de la tormenta.",
        "calma": "{protagonista} de pie mirando la sabana dorada iluminada por el "
                "sol de la tarde después de la tormenta, con el cielo despejado y "
                "luz cálida.",
        "encrucijada": "{protagonista} parado en un cruce de caminos de la sabana "
                       "al atardecer, con una luz dorada brillando entre unas "
                       "rocas hacia un lado, y sombras de animales asomando hacia "
                       "el otro.",
        # ── final tesoro 16-20 ──────────────────────────────────────────────
        "tesoro_1": "{protagonista} caminando hacia un brillo dorado que se filtra "
                    "entre unas rocas cubiertas de flores silvestres, al atardecer "
                    "en la sabana.",
        "tesoro_2": "{protagonista} entrando a una pequeña gruta escondida cubierta "
                    "de flores silvestres y luz dorada, con algo brillante "
                    "destellando en el centro.",
        "tesoro_3": "{protagonista} acercándose a una piedra lisa dentro de una "
                    "gruta iluminada, donde descansa una brújula dorada brillante.",
        "tesoro_4": "{protagonista} sosteniendo con las dos manos una brújula "
                    "dorada brillante recién encontrada entre las rocas de una "
                    "cueva, con una expresión de asombro y alegría, luz dorada "
                    "mágica alrededor del objeto.",
        "tesoro_final": "{protagonista} de pie en la sabana dorada al atardecer, "
                        "sosteniendo en alto una brújula dorada brillante, con una "
                        "gran sonrisa de triunfo.",
        # ── final amigos 16-20 ──────────────────────────────────────────────
        "amigos_1": "{protagonista} corriendo decidido por la sabana dorada al "
                    "atardecer, hacia el sonido de voces de animales pidiendo "
                    "ayuda.",
        "amigos_2": "{protagonista} encontrando a un grupo de animales de la selva "
                    "(león, jirafa, elefante) reunidos y preocupados, algo "
                    "perdidos en la sabana al atardecer.",
        "amigos_3": "{protagonista} caminando adelante guiando con calma a un "
                    "grupo de animales de la selva por un sendero de la sabana "
                    "dorada al atardecer.",
        "amigos_4": "{protagonista} caminando junto a un grupo de animales de la "
                    "selva, todos más tranquilos, acercándose a la sabana abierta "
                    "bajo un cielo dorado.",
        "amigos_final": "{protagonista} en medio de un grupo alegre de animales de "
                        "la selva (león, elefante, jirafa, monitos) celebrando "
                        "todos juntos como amigos, atardecer dorado en la sabana.",
    },
}


def override_escena_path(tema, nodo_id):
    return os.path.join(TEMAS, tema, "overrides", "aventura", "%s.png" % nodo_id)


def prompt_nodo(tema, nodo_id, genero=None):
    """Mismo bloque de reglas de estilo/consistencia que libro_ia.prompt_pagina —
    ajustado con iteración real (ver skill armar-audiolibros) — aplicado a la escena
    de este nodo en vez de a una página fija del libro lineal."""
    escena = _ESCENAS[tema][nodo_id].format(protagonista=libro_ia._protagonista(genero))
    pal = libro_ia._paleta(tema)
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
        "izquierda y derecha— porque al encuadrar la escena se recortan los bordes "
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
           if (nota := libro_ia.nota_tema(tema)) else "")
    )


def generar_ilustraciones(client, tema, nodos=None, calidad="medium", progress=None,
                          genero=None, verificar=True, fallos_log=None):
    """Genera y guarda la ilustración de cada nodo (default: todos los del tema).
    Devuelve la lista de paths escritos. `client` es ia_kit.client.OpenAIImageClient
    (o cualquier objeto con .editar(refs, prompt, size, quality=) -> bytes PNG)."""
    nodos = list(nodos) if nodos is not None else sorted(aventura.AVENTURAS[tema])
    refs = libro_ia.referencias(tema)
    if not refs:
        raise RuntimeError(
            "el tema %r no tiene imagen de referencia (ia_maestra.png/stickers) "
            "— agregala antes de generar la aventura" % tema)
    qa_key = os.environ.get("OPENAI_API_KEY")
    out = []
    for n, nid in enumerate(nodos):
        if progress:
            progress("Nodo %d de %d (%s)…" % (n + 1, len(nodos), nid))
        prompt = prompt_nodo(tema, nid, genero=genero)
        raw = client.editar(refs, prompt, _APAISADA, quality=calidad)
        if verificar and qa_key:
            ok, motivo = libro_ia.verificar_ilustracion(qa_key, raw, prompt)
            if not ok:
                if progress:
                    progress("Nodo %s rechazado por QA (%s) — reintento…" % (nid, motivo))
                raw2 = client.editar(refs, prompt + " MUY IMPORTANTE: " + motivo,
                                     _APAISADA, quality=calidad)
                ok2, motivo2 = libro_ia.verificar_ilustracion(qa_key, raw2, prompt)
                if ok2:
                    raw = raw2
                else:
                    if fallos_log:
                        with open(fallos_log, "a", encoding="utf-8") as fl:
                            fl.write("nodo %s: %s / %s\n" % (nid, motivo, motivo2))
                    if progress:
                        progress("Nodo %s: QA rechazó 2 veces — se deja sin generar" % nid)
                    continue
        img = Image.open(io.BytesIO(raw)).convert("RGBA")   # valida que sea imagen
        dest = override_escena_path(tema, nid)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        img.save(dest)
        out.append(dest)
    return out


if __name__ == "__main__":
    import sys
    import servicio  # carga OPENAI_API_KEY/OPENROUTER_API_KEY de env o config.json

    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nodos = [sys.argv[2]] if len(sys.argv) > 2 else None
    client = servicio._openai_client()
    if not client:
        raise SystemExit("falta OPENAI_API_KEY / OPENROUTER_API_KEY")
    hechos = generar_ilustraciones(client, tema, nodos, progress=print)
    print("Listo:", hechos)
