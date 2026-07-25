"""Catálogo CURRICULAR de actividades — una actividad es UNA entrada de datos.

Por qué existe: hasta ahora agregar una actividad obligaba a tocar CUATRO archivos
(`actividades_player.js` para el juego y su banco, `actividades_web.py` para el menú del
grado, `saberes.py` para el grafo y `actividades_categorias.py` para la categoría) más un
paso de regeneración. Así no se arma nada en el día. Acá la actividad se declara una vez
y de esa declaración salen las cuatro cosas.

Pedido de Pablo (24-jul-2026): *"tomá la información que está en la currícula y sacá todo
de ahí (…) tener algo preparado para armar en poco tiempo lo que nos pidan, que sea fácil
de adaptar"*. Por eso cada entrada lleva `dc` (el contenido del Diseño Curricular que
cubre) y `fuente` (el documento y el ID de donde salió): ninguna actividad se inventa, y
cualquiera puede rastrear de dónde vino.

⚠️ CONOCIMIENTO DEL MUNDO (hallazgo del 24-jul): en el DC 2024 de CABA, **1°, 2° y 3° NO
tienen Ciencias Naturales y Sociales separadas** — tienen un área única, "Conocimiento del
Mundo". Recién se separan en 4°. El producto venía con 4 categorías fijas que no coinciden
con el DC en primer ciclo, y por eso "Sociales de 2°" figuraba en cero: no es un hueco de
contenido, es una materia que a esa edad no existe.
"""

AREA_CDM = "cdm"          # Conocimiento del Mundo — 1° a 3° (DC CABA 2024)

# Mecánicas soportadas. Cada una define la forma del banco y qué campos extra pide la
# actividad. Al sumar una nueva hay que enseñarle a `gen_curriculum.py` a emitirla.
#
#   trivia     → banco [{q, ops, m}]      ops[0] es la correcta   (juegoTriviaTexto)
#   clasificar → banco [{it, cat, m}]     + "consigna" y "categorias" [{cat,label}]
#                                                                  (juegoClasificar)
#   ordenar    → banco [{items: [...]}]   ya en el orden CORRECTO
#                                          + "consigna" y "explica" (juegoOrdenar)
#
# El DC usa mucho clasificar y ordenar, no sólo trivia — y la propia auditoría fija que
# "el menú nunca sirve 3 trivias seguidas": cargar todo como trivia daría un catálogo
# completo y un producto aburrido.
MECANICAS = ("trivia", "clasificar", "ordenar")

# Tamaño mínimo de banco. La auditoría fijó "mínimo real 30 ítems, insignia 40" para 2°;
# por debajo de 12 el banco se agota en una sola partida y la actividad mide memoria.
BANCO_MINIMO = 12


CATALOGO = [
    # ── 1° grado ────────────────────────────────────────────────────────────────
    {
        "id": "objeto_material",
        "grado": 1, "area": AREA_CDM,
        "titulo": "¿De qué está hecho?", "icono": "🧱",
        "mecanica": "trivia",
        "dc": "Los objetos y los materiales: de qué está hecho, qué propiedad lo hace "
              "servir para eso",
        "fuente": "docs/auditoria-dc-caba/grado-1.md · C4",
        "saber": {"id": "CDM-1-materiales", "nombre": "Objetos, materiales y propiedades",
                  "prereqs": []},
        "banco": [
            {"q": "¿De qué material es una ventana?",
             "ops": ["Vidrio", "Madera", "Tela"],
             "m": "La ventana es de vidrio: deja pasar la luz y por eso se ve a través."},
            {"q": "¿De qué material es un buzo de invierno?",
             "ops": ["Lana", "Vidrio", "Metal"],
             "m": "El buzo es de lana: abriga porque no deja escapar el calor del cuerpo."},
            {"q": "¿De qué material es una cuchara para revolver la sopa caliente?",
             "ops": ["Madera", "Papel", "Tela"],
             "m": "De madera: no se calienta tanto como el metal y no se moja como el papel."},
            {"q": "¿Por qué las botellas son de plástico o vidrio y no de papel?",
             "ops": ["Porque el papel se moja y se rompe", "Porque el papel es caro",
                     "Porque el papel es pesado"],
             "m": "El papel absorbe el agua y se deshace: no sirve para guardar líquidos."},
            {"q": "Dos vasos iguales: uno se cayó y se rompió en pedazos. ¿De qué era?",
             "ops": ["De vidrio", "De plástico", "De goma"],
             "m": "El vidrio es frágil: se rompe al golpearse. El plástico y la goma no."},
            {"q": "¿Qué propiedad tiene que tener un paraguas?",
             "ops": ["Que no deje pasar el agua", "Que sea transparente",
                     "Que sea pesado"],
             "m": "El paraguas tiene que ser impermeable: que el agua no lo atraviese."},
            {"q": "¿De qué material es una llave?",
             "ops": ["Metal", "Cartón", "Lana"],
             "m": "De metal: es duro y resistente, no se dobla al girarlo en la cerradura."},
            {"q": "¿Por qué las ollas tienen el mango de plástico o madera?",
             "ops": ["Para no quemarse la mano", "Para que sean más lindas",
                     "Para que pesen menos"],
             "m": "El metal pasa el calor muy rápido; el plástico y la madera no, así que "
                  "el mango no quema."},
            {"q": "¿Qué material se estira y vuelve a su forma?",
             "ops": ["La goma", "El vidrio", "La piedra"],
             "m": "La goma es elástica: se estira y vuelve. El vidrio y la piedra no."},
            {"q": "¿De qué material es un globo?",
             "ops": ["Goma", "Papel", "Metal"],
             "m": "De goma: se estira cuando entra el aire sin romperse."},
            {"q": "¿Por qué los libros son de papel y no de tela?",
             "ops": ["Porque en el papel se puede escribir e imprimir bien",
                     "Porque el papel abriga", "Porque el papel no se moja"],
             "m": "En el papel la tinta queda nítida; en la tela se correría."},
            {"q": "¿Qué material dejaría pasar la luz?",
             "ops": ["El vidrio", "La madera", "El metal"],
             "m": "El vidrio es transparente: deja pasar la luz. La madera y el metal no."},
            {"q": "¿De qué material conviene una bolsa para llevar cosas pesadas?",
             "ops": ["Tela gruesa", "Papel de servilleta", "Papel de diario"],
             "m": "La tela gruesa resiste el peso; los papeles finos se rompen."},
            {"q": "¿Por qué las sillas de plaza suelen ser de metal o plástico?",
             "ops": ["Porque aguantan la lluvia y el sol", "Porque son transparentes",
                     "Porque son blandas"],
             "m": "Están a la intemperie: el metal y el plástico resisten el agua; el "
                  "cartón se arruinaría."},
        ],
    },

    # ── 2° grado ────────────────────────────────────────────────────────────────
    {
        "id": "luz_propia",
        "grado": 2, "area": AREA_CDM,
        "titulo": "¿Tiene luz propia?", "icono": "🔦",
        "mecanica": "trivia",
        "dc": "Fuentes lumínicas vs. objetos que no emiten luz. Tres categorías: emite / "
              "refleja / no se ve sin luz",
        "fuente": "docs/auditoria-dc-caba/grado-2.md · C2",
        "saber": {"id": "CDM-2-luz", "nombre": "Fuentes de luz y objetos iluminados",
                  "prereqs": ["CDM-1-materiales"]},
        "banco": [
            {"q": "El Sol, ¿tiene luz propia o refleja?",
             "ops": ["Tiene luz propia", "Refleja la luz", "No se ve sin luz"],
             "m": "El Sol es una estrella: produce su propia luz."},
            {"q": "La Luna, ¿tiene luz propia o refleja?",
             "ops": ["Refleja la luz del Sol", "Tiene luz propia", "No se ve nunca"],
             "m": "La Luna no produce luz: se ve porque el Sol la ilumina y ella refleja."},
            {"q": "Un espejo en una pieza a oscuras, ¿se ve?",
             "ops": ["No, porque no tiene luz propia", "Sí, porque brilla solo",
                     "Sí, porque tiene luz adentro"],
             "m": "El espejo refleja la luz que le llega; sin luz no refleja nada."},
            {"q": "Una vela encendida…",
             "ops": ["Tiene luz propia", "Refleja la luz del Sol",
                     "No se ve sin luz"],
             "m": "La llama produce luz: es una fuente lumínica."},
            {"q": "Una lamparita apagada, ¿tiene luz propia?",
             "ops": ["No, sólo cuando está encendida", "Sí, siempre",
                     "Sí, porque es de vidrio"],
             "m": "La lamparita es fuente de luz sólo cuando está encendida."},
            {"q": "Una luciérnaga…",
             "ops": ["Tiene luz propia", "Refleja la luz", "No se ve de noche"],
             "m": "La luciérnaga produce su propia luz: es un ser vivo luminoso."},
            {"q": "Un cartel reflectante en la ruta, de noche…",
             "ops": ["Refleja la luz de los autos", "Tiene luz propia",
                     "No se ve nunca"],
             "m": "No produce luz: devuelve la de los faros, por eso se ve tanto."},
            {"q": "La pantalla del celular encendida…",
             "ops": ["Tiene luz propia", "Refleja la luz del ambiente",
                     "No se ve en la oscuridad"],
             "m": "La pantalla emite su propia luz; por eso se ve a oscuras."},
            {"q": "Una manzana arriba de la mesa, de noche y sin luz…",
             "ops": ["No se ve, porque no tiene luz propia", "Se ve igual",
                     "Tiene luz propia"],
             "m": "La manzana sólo se ve cuando algo la ilumina."},
            {"q": "Las estrellas del cielo…",
             "ops": ["Tienen luz propia", "Reflejan la luz de la Luna",
                     "No se ven nunca"],
             "m": "Cada estrella produce su propia luz, como el Sol."},
            {"q": "El fuego de una fogata…",
             "ops": ["Tiene luz propia", "Refleja la luz", "No calienta"],
             "m": "El fuego produce luz y calor: es una fuente lumínica."},
            {"q": "Un vidrio de ventana de día, ¿por qué se ve?",
             "ops": ["Porque el Sol lo ilumina", "Porque tiene luz propia",
                     "Porque es de metal"],
             "m": "El vidrio no emite luz: lo vemos porque la luz del Sol lo atraviesa e "
                  "ilumina."},
            {"q": "Una linterna prendida…",
             "ops": ["Tiene luz propia", "Refleja la luz de la Luna",
                     "No se ve de noche"],
             "m": "La linterna produce luz: por eso sirve para alumbrar."},
            {"q": "El agua de una pileta con sol, ¿brilla porque tiene luz propia?",
             "ops": ["No, refleja la luz del Sol", "Sí, tiene luz propia",
                     "Sí, porque está fría"],
             "m": "El agua refleja la luz del Sol; no la produce."},
        ],
    },

    # ── 3° grado ────────────────────────────────────────────────────────────────
    {
        "id": "derechos_escenarios",
        "grado": 3, "area": AREA_CDM,
        "titulo": "¿Se respeta el derecho?", "icono": "⚖️",
        "mecanica": "trivia",
        "dc": "Derechos de niños y niñas, también en entornos digitales; diálogo y "
              "consenso frente al conflicto",
        "fuente": "docs/auditoria-dc-caba/grado-3.md · C10",
        "saber": {"id": "CDM-3-derechos", "nombre": "Derechos de niñas y niños",
                  "prereqs": ["CDM-2-luz"]},
        "banco": [
            {"q": "En la escuela dejan a un chico afuera del juego por cómo habla. ¿Qué derecho no se respeta?",
             "ops": ["A no ser discriminado", "A tener juguetes nuevos",
                     "A elegir la maestra"],
             "m": "Excluir a alguien por cómo habla, cómo es o de dónde viene es "
                  "discriminación."},
            {"q": "Una nena de 8 años trabaja todo el día y no va a la escuela. ¿Qué derecho no se respeta?",
             "ops": ["A la educación", "A tener una mascota", "A mirar televisión"],
             "m": "Todos los chicos tienen derecho a ir a la escuela; el trabajo infantil "
                  "lo impide."},
            {"q": "Un chico se enferma y lo atienden en el hospital sin pagar. ¿Qué derecho se está cumpliendo?",
             "ops": ["A la salud", "A la vivienda", "Al juego"],
             "m": "La atención de la salud es un derecho, no un favor."},
            {"q": "En el recreo nadie deja jugar a los más chicos. ¿Qué está en juego?",
             "ops": ["El derecho al juego", "El derecho a la vivienda",
                     "El derecho a votar"],
             "m": "Jugar es un derecho de la infancia, no un premio."},
            {"q": "Alguien sube a internet una foto tuya sin permiso. ¿Qué derecho no se respeta?",
             "ops": ["A la privacidad, también en internet",
                     "A tener celular propio", "A jugar en línea"],
             "m": "Los derechos valen igual en el mundo digital: tu imagen es tuya."},
            {"q": "Dos chicos se pelean por una pelota. ¿Cuál es la mejor salida?",
             "ops": ["Hablar y acordar turnos", "Que gane el más fuerte",
                     "Esconder la pelota"],
             "m": "El diálogo y el acuerdo resuelven el conflicto; la fuerza sólo lo tapa."},
            {"q": "En una reunión de grado no dejan opinar a los chicos. ¿Qué derecho no se respeta?",
             "ops": ["A ser escuchado", "A llegar tarde", "A no ir a la escuela"],
             "m": "Los chicos tienen derecho a dar su opinión sobre lo que les afecta."},
            {"q": "Un chico no tiene dónde vivir. ¿Qué derecho no se está cumpliendo?",
             "ops": ["A una vivienda digna", "A tener bicicleta",
                     "A elegir la comida"],
             "m": "Una vivienda digna es un derecho básico."},
            {"q": "Todos los chicos del grado tienen nombre y documento. ¿Qué derecho es?",
             "ops": ["A la identidad", "Al deporte", "A la tecnología"],
             "m": "Tener nombre, apellido y documento es el derecho a la identidad."},
            {"q": "Un chico en silla de ruedas no puede entrar porque hay escalones. ¿Qué falta?",
             "ops": ["Que el lugar sea accesible para todos",
                     "Que se quede en casa", "Que lo carguen siempre"],
             "m": "Los espacios tienen que ser accesibles: es parte de la igualdad de "
                  "derechos."},
            {"q": "En un grupo de chat se burlan de un compañero todos los días. ¿Qué hay que hacer?",
             "ops": ["Contarle a una persona adulta de confianza",
                     "Sumarse para no quedar afuera", "Hacer de cuenta que no pasa"],
             "m": "El hostigamiento también existe en lo digital; hay que pedir ayuda a "
                  "una persona adulta."},
            {"q": "Una familia habla otro idioma en casa. ¿Eso está bien?",
             "ops": ["Sí, es parte de su identidad y cultura",
                     "No, hay que hablar sólo uno", "Sólo si viven en otro país"],
             "m": "Respetar la lengua y la cultura de cada familia es un derecho."},
            {"q": "En la escuela dan de comer a quien lo necesita. ¿Qué derecho se cumple?",
             "ops": ["A la alimentación", "A la propiedad", "Al trabajo"],
             "m": "Alimentarse bien es un derecho, y la escuela ayuda a garantizarlo."},
            {"q": "Un chico quiere jugar al fútbol y le dicen que es sólo para varones. ¿Qué pasa ahí?",
             "ops": ["Se lo discrimina: el deporte es para todos",
                     "Está bien, es la regla", "Tiene que elegir otro juego"],
             "m": "Limitar una actividad por el género es discriminación."},
        ],
    },

    # ── 1° · clasificar (mecánica nueva) ─────────────────────────────────────────
    {
        "id": "solido_liquido",
        "grado": 1, "area": AREA_CDM,
        "titulo": "¿Sólido o líquido?", "icono": "💧",
        "mecanica": "clasificar",
        "consigna": "¿Es sólido o líquido?",
        "categorias": [{"cat": "solido", "label": "🧊 Sólido"},
                       {"cat": "liquido", "label": "💧 Líquido"}],
        "dc": "Los materiales y sus estados: sólido y líquido; casos límite",
        "fuente": "docs/auditoria-dc-caba/grado-1.md · C3",
        "saber": {"id": "CDM-1-estados", "nombre": "Sólidos y líquidos",
                  "prereqs": ["CDM-1-materiales"]},
        "banco": [
            {"it": "Piedra", "cat": "solido", "m": "La piedra tiene forma propia: es sólida."},
            {"it": "Agua", "cat": "liquido", "m": "El agua toma la forma del recipiente: es líquida."},
            {"it": "Leche", "cat": "liquido", "m": "La leche se vuelca y toma la forma del vaso: líquida."},
            {"it": "Madera", "cat": "solido", "m": "La madera mantiene su forma: es sólida."},
            {"it": "Hielo", "cat": "solido",
             "m": "Ojo: el hielo es agua SÓLIDA. Tiene forma propia, no se vuelca."},
            {"it": "Miel", "cat": "liquido",
             "m": "La miel es espesa, pero se vuelca y toma la forma del frasco: es líquida."},
            {"it": "Harina", "cat": "solido",
             "m": "La harina parece que se vuelca, pero son muchos granitos sólidos."},
            {"it": "Aceite", "cat": "liquido", "m": "El aceite se vuelca y toma la forma: líquido."},
            {"it": "Vidrio", "cat": "solido", "m": "El vidrio tiene forma propia: es sólido."},
            {"it": "Jugo", "cat": "liquido", "m": "El jugo toma la forma del vaso: líquido."},
            {"it": "Arena", "cat": "solido",
             "m": "La arena se derrama, pero cada granito es sólido."},
            {"it": "Goma de borrar", "cat": "solido", "m": "Tiene forma propia: sólida."},
            {"it": "Champú", "cat": "liquido", "m": "Es espeso pero se vuelca: líquido."},
            {"it": "Cubito de caldo", "cat": "solido", "m": "Tiene forma propia: es sólido."},
        ],
    },

    # ── 3° · ordenar (mecánica nueva) ────────────────────────────────────────────
    {
        "id": "circuito_alimento",
        "grado": 3, "area": AREA_CDM,
        "titulo": "El viaje del alimento", "icono": "🥛",
        "mecanica": "ordenar",
        "consigna": "Ordená el recorrido: ¿qué pasa primero? Tocá en orden.",
        "explica": "Pensá el camino desde donde se produce hasta que llega a tu casa.",
        "dc": "Circuito productivo: de la fase agraria a la comercial",
        "fuente": "docs/auditoria-dc-caba/grado-3.md · C3",
        "saber": {"id": "CDM-3-circuitos", "nombre": "Circuitos productivos",
                  "prereqs": ["CDM-2-luz"]},
        "banco": [
            {"items": ["La vaca da leche en el tambo", "Un camión lleva la leche a la fábrica",
                       "En la fábrica hacen el queso", "El queso llega al supermercado"]},
            {"items": ["Se siembra el trigo", "Se cosecha el trigo",
                       "En el molino lo hacen harina", "La panadería hace el pan"]},
            {"items": ["Se plantan las papas", "Se sacan las papas de la tierra",
                       "Se lavan y se embolsan", "Se venden en la verdulería"]},
            {"items": ["La oveja da lana", "Se esquila la oveja",
                       "Se hila la lana", "Se teje el pulóver"]},
            {"items": ["Se juntan las uvas", "Se llevan a la bodega",
                       "Se hace el jugo", "Se vende embotellado"]},
            {"items": ["El árbol da naranjas", "Se cosechan las naranjas",
                       "En la fábrica hacen el jugo", "El jugo llega al kiosco"]},
            {"items": ["Se cría la gallina", "Se juntan los huevos",
                       "Se guardan en maples", "Se venden en el almacén"]},
            {"items": ["Se corta el árbol", "Se lleva el tronco al aserradero",
                       "Se hacen las tablas", "Se arma la silla"]},
            {"items": ["Se cultiva el algodón", "Se cosecha el algodón",
                       "Se hila y se teje la tela", "Se cose la remera"]},
        ],
    },
]


# ── consultas ───────────────────────────────────────────────────────────────────
def actividades_de(grado=None, area=None):
    """Actividades del catálogo, filtrables por grado y/o área."""
    return [a for a in CATALOGO
            if (grado is None or a["grado"] == grado)
            and (area is None or a["area"] == area)]


def menu_de_grado(grado):
    """Entradas de menú (mismo formato que `actividades_web._menu`) para ese grado."""
    return [{"id": a["id"], "titulo": a["titulo"], "icono": a["icono"],
             "cfg": {"rondas": min(10, max(6, len(a["banco"]) // 2))}}
            for a in actividades_de(grado)]


def categorias():
    """{id_juego: area} — lo consume actividades_categorias para agrupar el menú."""
    return {a["id"]: a["area"] for a in CATALOGO}


def saberes():
    """{id_saber: {...}} en el formato de `saberes.py`, listo para sumar al grafo."""
    out = {}
    for a in CATALOGO:
        s = a["saber"]
        out[s["id"]] = {
            "nombre": s["nombre"], "eje": a["area"], "grado": a["grado"],
            # el grafo usa "prerrequisitos" (no "prereqs"): acá se traduce una sola vez
            "prerrequisitos": list(s.get("prereqs") or []), "juegos": [a["id"]],
            "dificultad": s.get("dificultad", 2),
        }
    return out


# ── validación ──────────────────────────────────────────────────────────────────
def _validar_banco(ref, mecanica, act, banco):
    """Chequeos propios de cada mecánica. Cada una tiene su forma y sus trampas."""
    problemas, vistas = [], set()
    if mecanica == "trivia":
        for i, it in enumerate(banco):
            donde = "%s ítem %d" % (ref, i)
            if not it.get("q") or not it.get("m"):
                problemas.append("%s: sin consigna o sin explicación del error" % donde)
            ops = it.get("ops") or []
            if len(ops) < 3:
                problemas.append("%s: %d opciones, mínimo 3" % (donde, len(ops)))
            if len(set(ops)) != len(ops):
                problemas.append("%s: opciones repetidas" % donde)
            if it.get("q") in vistas:
                problemas.append("%s: consigna repetida en el mismo banco" % donde)
            vistas.add(it.get("q"))
    elif mecanica == "clasificar":
        cats = act.get("categorias") or []
        if not act.get("consigna"):
            problemas.append("%s: falta 'consigna'" % ref)
        if not 2 <= len(cats) <= 4:
            problemas.append("%s: %d categorías; el DC usa 2, 3 o 4" % (ref, len(cats)))
        claves = {c.get("cat") for c in cats}
        if len(claves) != len(cats):
            problemas.append("%s: categorías repetidas" % ref)
        usadas = set()
        for i, it in enumerate(banco):
            donde = "%s ítem %d" % (ref, i)
            if not it.get("it") or not it.get("m"):
                problemas.append("%s: sin ítem o sin explicación del error" % donde)
            if it.get("cat") not in claves:
                problemas.append("%s: categoría %r no declarada" % (donde, it.get("cat")))
            if it.get("it") in vistas:
                problemas.append("%s: ítem repetido en el mismo banco" % donde)
            vistas.add(it.get("it"))
            usadas.add(it.get("cat"))
        # una categoría sin ítems es un botón que nunca es correcto: se aprende a
        # descartarlo y deja de ser una opción real
        for c in claves - usadas:
            problemas.append("%s: la categoría %r no tiene ningún ítem" % (ref, c))
    elif mecanica == "ordenar":
        if not act.get("consigna") or not act.get("explica"):
            problemas.append("%s: falta 'consigna' o 'explica'" % ref)
        for i, it in enumerate(banco):
            donde = "%s secuencia %d" % (ref, i)
            items = it.get("items") or []
            if len(items) < 3:
                problemas.append("%s: %d tarjetas, mínimo 3" % (donde, len(items)))
            if len(set(items)) != len(items):
                problemas.append("%s: tarjetas repetidas dentro de la secuencia" % donde)
            clave = tuple(items)
            if clave in vistas:
                problemas.append("%s: secuencia repetida en el mismo banco" % donde)
            vistas.add(clave)
    return problemas


def validar():
    """Devuelve la lista de problemas del catálogo (vacía = está sano).

    Se corre en los tests: una actividad mal declarada tiene que fallar acá y no
    aparecer rota en el cuaderno de un chico."""
    problemas, ids, saberes_vistos = [], set(), set()
    for a in CATALOGO:
        ref = "%s (%d°)" % (a.get("id", "?"), a.get("grado", 0))
        for campo in ("id", "grado", "area", "titulo", "icono", "mecanica", "dc",
                      "fuente", "saber", "banco"):
            if not a.get(campo):
                problemas.append("%s: falta '%s'" % (ref, campo))
        if a.get("id") in ids:
            problemas.append("%s: id repetido" % ref)
        ids.add(a.get("id"))
        if a.get("mecanica") not in MECANICAS:
            problemas.append("%s: mecánica desconocida %r" % (ref, a.get("mecanica")))
        if a.get("area") == AREA_CDM and a.get("grado") not in (1, 2, 3):
            problemas.append("%s: Conocimiento del Mundo sólo existe en 1°-3° del DC" % ref)
        banco = a.get("banco") or []
        mec = a.get("mecanica")
        # "ordenar" mide por SECUENCIAS, no por ítems sueltos: 12 secuencias de 4-5
        # tarjetas ya son muchas rondas distintas, así que el piso es más bajo.
        minimo = 8 if mec == "ordenar" else BANCO_MINIMO
        if len(banco) < minimo:
            problemas.append("%s: banco de %d ítems, mínimo %d (si no se agota en una "
                             "partida y mide memoria)" % (ref, len(banco), minimo))
        problemas.extend(_validar_banco(ref, mec, a, banco))
        s = a.get("saber") or {}
        if s.get("id") in saberes_vistos:
            problemas.append("%s: saber repetido %s" % (ref, s.get("id")))
        saberes_vistos.add(s.get("id"))
    # los prerrequisitos tienen que existir (en el catálogo o en el grafo grande)
    import saberes as grafo
    conocidos = saberes_vistos | set(grafo.SABERES)
    for a in CATALOGO:
        for p in (a.get("saber") or {}).get("prereqs") or []:
            if p not in conocidos:
                problemas.append("%s: prerrequisito inexistente %r" % (a["id"], p))
    return problemas
