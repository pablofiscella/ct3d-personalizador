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
#   parametrica → SIN banco: "plantilla" {q, vars, ok, distractores, tope, m}
#                  El ejercicio se genera cada vez, así que no hay nada que memorizar —
#                  es la mecánica que la auditoría llama "paramétrica".  (juegoParametrico)
MECANICAS = ("trivia", "clasificar", "ordenar", "parametrica")

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

    # ── 1° · clasificar animales por cobertura ───────────────────────────────────
    {
        "id": "animales_cobertura",
        "grado": 1, "area": AREA_CDM,
        "titulo": "¿Pelos, plumas o escamas?", "icono": "🦔",
        "mecanica": "clasificar",
        "consigna": "¿Con qué está cubierto el cuerpo?",
        "categorias": [{"cat": "pelos", "label": "🐻 Pelos"},
                       {"cat": "plumas", "label": "🦜 Plumas"},
                       {"cat": "escamas", "label": "🐟 Escamas"}],
        "dc": "Características de los animales: cobertura del cuerpo",
        "fuente": "docs/auditoria-dc-caba/grado-1.md · C1",
        "saber": {"id": "CDM-1-animales", "nombre": "Cobertura del cuerpo de los animales",
                  "prereqs": []},
        "banco": [
            {"it": "Perro", "cat": "pelos", "m": "El perro tiene el cuerpo cubierto de pelos."},
            {"it": "Gallina", "cat": "plumas", "m": "La gallina tiene plumas, como todas las aves."},
            {"it": "Pez", "cat": "escamas", "m": "El pez tiene escamas que le cubren el cuerpo."},
            {"it": "Gato", "cat": "pelos", "m": "El gato está cubierto de pelos."},
            {"it": "Murciélago", "cat": "pelos",
             "m": "Ojo: vuela, pero NO es un ave. Tiene pelos, no plumas."},
            {"it": "Pingüino", "cat": "plumas",
             "m": "Ojo: no vuela, pero es un ave. Tiene plumas."},
            {"it": "Serpiente", "cat": "escamas", "m": "La serpiente está cubierta de escamas."},
            {"it": "Caballo", "cat": "pelos", "m": "El caballo tiene pelo en todo el cuerpo."},
            {"it": "Loro", "cat": "plumas", "m": "El loro es un ave: tiene plumas."},
            {"it": "Lagartija", "cat": "escamas", "m": "La lagartija tiene escamas."},
            {"it": "Vaca", "cat": "pelos", "m": "La vaca tiene el cuerpo cubierto de pelos."},
            {"it": "Pato", "cat": "plumas", "m": "El pato es un ave: tiene plumas."},
            {"it": "Tiburón", "cat": "escamas", "m": "El tiburón es un pez: tiene escamas."},
            {"it": "Ballena", "cat": "pelos",
             "m": "Ojo: vive en el mar, pero NO es un pez. Tiene pelos, muy poquitos."},
            {"it": "Oveja", "cat": "pelos", "m": "La lana de la oveja es pelo."},
            {"it": "Cocodrilo", "cat": "escamas", "m": "El cocodrilo tiene escamas duras."},
        ],
    },

    # ── 1° · antes / hoy / en los dos ────────────────────────────────────────────
    {
        "id": "antes_y_hoy",
        "grado": 1, "area": AREA_CDM,
        "titulo": "¿Antes, hoy o en los dos?", "icono": "🕰️",
        "mecanica": "clasificar",
        "consigna": "¿Esto era de antes, es de ahora, o hay en los dos?",
        "categorias": [{"cat": "antes", "label": "🕰️ Sólo antes"},
                       {"cat": "hoy", "label": "📱 Sólo hoy"},
                       {"cat": "ambos", "label": "🔁 En los dos"}],
        "dc": "Cambios y continuidades a lo largo del tiempo. La CONTINUIDAD es el "
              "contenido que una dicotomía antes/hoy no puede enseñar",
        "fuente": "docs/auditoria-dc-caba/grado-1.md · C6",
        "saber": {"id": "CDM-1-tiempo", "nombre": "Cambios y continuidades",
                  "prereqs": []},
        "banco": [
            {"it": "El pan", "cat": "ambos", "m": "Se comía antes y se come hoy: es una continuidad."},
            {"it": "El celular", "cat": "hoy", "m": "El celular es de ahora; antes no existía."},
            {"it": "La carreta con caballos", "cat": "antes",
             "m": "Antes se viajaba en carreta; hoy ya casi no se usa."},
            {"it": "Los juegos con pelota", "cat": "ambos",
             "m": "Los chicos jugaban con pelota antes y siguen jugando hoy."},
            {"it": "La computadora", "cat": "hoy", "m": "Es un invento reciente."},
            {"it": "Las velas para alumbrar", "cat": "antes",
             "m": "Antes se alumbraba con velas; hoy usamos luz eléctrica."},
            {"it": "La escuela", "cat": "ambos", "m": "Había escuelas antes y hay hoy."},
            {"it": "Los anillos y collares", "cat": "ambos",
             "m": "La gente usaba adornos antes y los usa hoy."},
            {"it": "La heladera", "cat": "hoy",
             "m": "Antes se guardaba la comida con hielo, no había heladera eléctrica."},
            {"it": "La pluma para escribir", "cat": "antes",
             "m": "Antes se escribía con pluma y tintero."},
            {"it": "La familia", "cat": "ambos", "m": "Siempre hubo familias, aunque cambiaron."},
            {"it": "El televisor", "cat": "hoy", "m": "La tele es un invento del siglo pasado."},
            {"it": "Cocinar con leña", "cat": "antes",
             "m": "Antes se cocinaba con leña; hoy casi siempre con gas o electricidad."},
            {"it": "Los cuentos", "cat": "ambos", "m": "Se contaban cuentos antes y hoy también."},
        ],
    },

    # ── 2° · opaco / traslúcido / transparente ───────────────────────────────────
    {
        "id": "linterna_magica",
        "grado": 2, "area": AREA_CDM,
        "titulo": "La linterna mágica", "icono": "🔦",
        "mecanica": "clasificar",
        "consigna": "Si le ponés la linterna atrás, ¿qué pasa con la luz?",
        "categorias": [{"cat": "opaco", "label": "⬛ No pasa"},
                       {"cat": "translucido", "label": "🌫️ Pasa borroso"},
                       {"cat": "transparente", "label": "🪟 Se ve nítido"}],
        "dc": "Materiales opacos, traslúcidos y transparentes — el eje de ciencias del grado",
        "fuente": "docs/auditoria-dc-caba/grado-2.md · C1",
        "saber": {"id": "CDM-2-opacidad", "nombre": "Opacos, traslúcidos y transparentes",
                  "prereqs": ["CDM-1-materiales"]},
        "banco": [
            {"it": "Una puerta de madera", "cat": "opaco", "m": "La madera no deja pasar nada de luz."},
            {"it": "El vidrio de la ventana", "cat": "transparente",
             "m": "Se ve nítido a través: es transparente."},
            {"it": "Papel manteca", "cat": "translucido",
             "m": "Ojo: pasa luz pero NO se ve nítido. Traslúcido no es lo mismo que transparente."},
            {"it": "Una pared", "cat": "opaco", "m": "La pared no deja pasar luz."},
            {"it": "Una bolsa de nylon fina", "cat": "translucido",
             "m": "Pasa luz pero las formas se ven borrosas."},
            {"it": "Una botella de agua limpia", "cat": "transparente",
             "m": "Se ve con nitidez lo que hay detrás."},
            {"it": "Un libro", "cat": "opaco", "m": "El libro tapa la luz por completo."},
            {"it": "Vidrio esmerilado del baño", "cat": "translucido",
             "m": "Deja pasar la luz pero no se distinguen las formas."},
            {"it": "Los anteojos", "cat": "transparente", "m": "Se ve nítido a través del cristal."},
            {"it": "Una remera", "cat": "opaco", "m": "La tela no deja pasar la luz."},
            {"it": "Una hoja de papel blanca", "cat": "translucido",
             "m": "Con la linterna atrás se ve el resplandor, pero no las formas."},
            {"it": "El agua de un vaso", "cat": "transparente", "m": "Se ve a través del agua limpia."},
            {"it": "Una cortina gruesa", "cat": "opaco", "m": "Está hecha para que no pase la luz."},
            {"it": "Papel celofán de color", "cat": "translucido",
             "m": "Pasa luz teñida, pero no se ve con nitidez."},
        ],
    },

    # ── 2° · artesanal o industrial ──────────────────────────────────────────────
    {
        "id": "artesanal_industrial",
        "grado": 2, "area": AREA_CDM,
        "titulo": "¿Artesanal o industrial?", "icono": "🏭",
        "mecanica": "clasificar",
        "consigna": "¿Cómo se produce esto?",
        "categorias": [{"cat": "artesanal", "label": "🤲 Artesanal"},
                       {"cat": "industrial", "label": "🏭 Industrial"}],
        "dc": "Producción artesanal vs. industrial. El criterio es la TÉCNICA y la ESCALA, "
              "no si hay o no personas trabajando",
        "fuente": "docs/auditoria-dc-caba/grado-2.md · C4",
        "saber": {"id": "CDM-2-produccion", "nombre": "Producción artesanal e industrial",
                  "prereqs": []},
        "banco": [
            {"it": "Una señora teje un pulóver a mano", "cat": "artesanal",
             "m": "Lo hace una persona, de a uno y con sus manos: artesanal."},
            {"it": "Una fábrica hace 5.000 pulóveres por día", "cat": "industrial",
             "m": "Muchísimas unidades iguales con máquinas: industrial."},
            {"it": "Un panadero amasa el pan en el horno del barrio", "cat": "artesanal",
             "m": "De a poco y a mano: artesanal."},
            {"it": "Una máquina llena mil botellas por hora", "cat": "industrial",
             "m": "La escala y la máquina lo hacen industrial."},
            {"it": "Una persona controla una máquina que corta mil chapas", "cat": "industrial",
             "m": "Ojo: que haya una persona NO lo hace artesanal. Manda la máquina y la escala."},
            {"it": "Un alfarero hace una vasija en su torno", "cat": "artesanal",
             "m": "Una pieza por vez, hecha por una persona."},
            {"it": "Se imprimen 10.000 cuadernos iguales", "cat": "industrial",
             "m": "Producción en serie: industrial."},
            {"it": "Una artesana pinta cada mate distinto", "cat": "artesanal",
             "m": "Cada pieza es única: artesanal."},
            {"it": "Una línea de montaje arma autos", "cat": "industrial",
             "m": "Máquinas y gran escala: industrial."},
            {"it": "Un zapatero arregla zapatos en su taller", "cat": "artesanal",
             "m": "Trabajo manual, de a uno."},
            {"it": "Una máquina embolsa fideos sin parar", "cat": "industrial",
             "m": "Producción en serie con máquinas."},
            {"it": "Una señora hace dulce en su cocina", "cat": "artesanal",
             "m": "En casa, en poca cantidad: artesanal."},
            {"it": "Una fábrica hace mil frascos de dulce iguales", "cat": "industrial",
             "m": "El mismo producto, pero a escala industrial."},
            {"it": "Un carpintero hace una mesa por encargo", "cat": "artesanal",
             "m": "Una pieza, hecha a medida."},
        ],
    },

    # ── 2° · el tiempo del verbo ─────────────────────────────────────────────────
    {
        "id": "tiempo_verbo",
        "grado": 2, "area": "lengua",
        "titulo": "¿Ayer, hoy o mañana?", "icono": "⏳",
        "mecanica": "clasificar",
        "consigna": "¿Cuándo pasa lo que dice la oración?",
        "categorias": [{"cat": "ayer", "label": "⬅️ Ayer"},
                       {"cat": "hoy", "label": "📍 Hoy"},
                       {"cat": "manana", "label": "➡️ Mañana"}],
        "dc": "Presente, pasado y futuro. Sin adverbio, lo decide la desinencia del verbo",
        "fuente": "docs/auditoria-dc-caba/grado-2.md · L13",
        "saber": {"id": "LEN-2-tiempos", "nombre": "Presente, pasado y futuro",
                  "prereqs": []},
        "banco": [
            {"it": "Ayer jugamos en la plaza.", "cat": "ayer", "m": "«Jugamos» ya pasó."},
            {"it": "Mañana iremos al museo.", "cat": "manana", "m": "«Iremos» todavía no pasó."},
            {"it": "Hoy leo un cuento.", "cat": "hoy", "m": "«Leo» está pasando ahora."},
            {"it": "Comí una manzana.", "cat": "ayer", "m": "«Comí» ya terminó: es pasado."},
            {"it": "Cantaremos en el acto.", "cat": "manana", "m": "«Cantaremos» es futuro."},
            {"it": "Corro por el patio.", "cat": "hoy", "m": "«Corro» es presente."},
            {"it": "Pintaba un dibujo.", "cat": "ayer", "m": "«Pintaba» es pasado."},
            {"it": "Vamos a la escuela todos los días.", "cat": "hoy",
             "m": "«Vamos» es presente: algo que pasa habitualmente."},
            {"it": "Visitaré a mi abuela.", "cat": "manana", "m": "«Visitaré» es futuro."},
            {"it": "Escribimos una carta la semana pasada.", "cat": "ayer",
             "m": "«Escribimos» con «la semana pasada» es pasado."},
            {"it": "El perro duerme en la alfombra.", "cat": "hoy", "m": "«Duerme» es presente."},
            {"it": "Traeré la pelota.", "cat": "manana", "m": "«Traeré» es futuro."},
            {"it": "Se rompió el vaso.", "cat": "ayer", "m": "«Se rompió» ya ocurrió."},
            {"it": "Estudiaremos para la prueba.", "cat": "manana", "m": "«Estudiaremos» es futuro."},
            {"it": "Ella baila muy bien.", "cat": "hoy", "m": "«Baila» es presente."},
        ],
    },

    # ── 2° · qué tipo de texto es ────────────────────────────────────────────────
    {
        "id": "tipos_de_texto",
        "grado": 2, "area": "lengua",
        "titulo": "¿Qué texto es?", "icono": "📄",
        "mecanica": "clasificar",
        "consigna": "¿Qué clase de texto es este?",
        "categorias": [{"cat": "receta", "label": "🍳 Receta"},
                       {"cat": "invitacion", "label": "🎉 Invitación"},
                       {"cat": "aviso", "label": "📢 Aviso"}],
        "dc": "Tipos textuales: instrucciones, invitaciones, publicidades y señalética",
        "fuente": "docs/auditoria-dc-caba/grado-2.md · L10",
        "saber": {"id": "LEN-2-tipos-texto", "nombre": "Tipos de texto",
                  "prereqs": []},
        "banco": [
            {"it": "«Mezclar la harina con el agua y amasar.»", "cat": "receta",
             "m": "Dice pasos para cocinar: es una receta."},
            {"it": "«¡Te espero el sábado a las 4 en mi casa!»", "cat": "invitacion",
             "m": "Invita a alguien a un evento."},
            {"it": "«¡Gran liquidación! Todo al 50%.»", "cat": "aviso",
             "m": "Quiere vender algo: es un aviso."},
            {"it": "«Ingredientes: 2 huevos, 1 taza de leche.»", "cat": "receta",
             "m": "La lista de ingredientes es parte de la receta."},
            {"it": "«Cumplo 8 años. ¡Vení a festejar!»", "cat": "invitacion",
             "m": "Invita al cumpleaños."},
            {"it": "«Se busca perro perdido. Llamar al 4444-5555.»", "cat": "aviso",
             "m": "Avisa algo al público."},
            {"it": "«Hornear 20 minutos a fuego medio.»", "cat": "receta",
             "m": "Es una instrucción de cocina."},
            {"it": "«Fiesta de fin de año. Salón de la escuela, 18 hs.»", "cat": "invitacion",
             "m": "Invita a un evento con lugar y horario."},
            {"it": "«Cuidado: piso mojado.»", "cat": "aviso",
             "m": "Avisa algo para prevenir: es un cartel de aviso."},
            {"it": "«Batir las claras a nieve.»", "cat": "receta", "m": "Es un paso de la receta."},
            {"it": "«Los esperamos en el acto del 25 de Mayo.»", "cat": "invitacion",
             "m": "Convoca a un acto."},
            {"it": "«Clases de guitarra. Consultá horarios.»", "cat": "aviso",
             "m": "Ofrece un servicio: aviso."},
            {"it": "«Dejar enfriar antes de servir.»", "cat": "receta", "m": "Instrucción de cocina."},
            {"it": "«Prohibido pisar el césped.»", "cat": "aviso", "m": "Es un cartel de aviso."},
        ],
    },

    # ── 2° · ordenar los pasos ───────────────────────────────────────────────────
    {
        "id": "ordenar_pasos",
        "grado": 2, "area": "lengua",
        "titulo": "Ordená los pasos", "icono": "🔢",
        "mecanica": "ordenar",
        "consigna": "Ordená los pasos: ¿qué se hace primero? Tocá en orden.",
        "explica": "Pensá qué tiene que estar listo antes de poder hacer lo siguiente.",
        "dc": "Orden lógico de las acciones en un texto instructivo",
        "fuente": "docs/auditoria-dc-caba/grado-2.md · L9",
        "saber": {"id": "LEN-2-instructivo", "nombre": "Orden en el texto instructivo",
                  "prereqs": []},
        "banco": [
            {"items": ["Juntar los ingredientes", "Mezclar todo en un bol",
                       "Poner la mezcla en el horno", "Servir la torta"]},
            {"items": ["Poner la pava con agua", "Esperar a que hierva",
                       "Poner la yerba en el mate", "Cebar el mate"]},
            {"items": ["Sacar los útiles de la mochila", "Escribir la fecha",
                       "Hacer la tarea", "Guardar todo otra vez"]},
            {"items": ["Elegir la semilla", "Poner tierra en la maceta",
                       "Enterrar la semilla", "Regar todos los días"]},
            {"items": ["Sacar la ropa sucia", "Ponerla en el lavarropas",
                       "Colgarla al sol", "Doblarla y guardarla"]},
            {"items": ["Untar el pan con manteca", "Poner el queso encima",
                       "Cerrar el sándwich", "Cortarlo por la mitad"]},
            {"items": ["Ponerse las medias", "Ponerse las zapatillas",
                       "Atarse los cordones"]},
            {"items": ["Abrir el libro", "Leer el cuento",
                       "Cerrar el libro", "Contarle a alguien de qué se trataba"]},
            {"items": ["Mojarse las manos", "Ponerse jabón",
                       "Enjuagarse", "Secarse con la toalla"]},
            {"items": ["Comprar los globos", "Inflarlos",
                       "Colgarlos en la pared", "Sacarle una foto a la decoración"]},
        ],
    },

    # ── 3° · estados de la materia ───────────────────────────────────────────────
    {
        "id": "estados_tres",
        "grado": 3, "area": AREA_CDM,
        "titulo": "Frío y calor", "icono": "🌡️",
        "mecanica": "clasificar",
        "consigna": "¿En qué estado está?",
        "categorias": [{"cat": "solido", "label": "🧊 Sólido"},
                       {"cat": "liquido", "label": "💧 Líquido"},
                       {"cat": "gaseoso", "label": "☁️ Gaseoso"}],
        "dc": "Estados de la materia. El estado GASEOSO es lo nuevo del grado",
        "fuente": "docs/auditoria-dc-caba/grado-3.md · C1",
        "saber": {"id": "CDM-3-estados", "nombre": "Sólido, líquido y gaseoso",
                  "prereqs": ["CDM-1-estados"]},
        "banco": [
            {"it": "Una piedra", "cat": "solido", "m": "Tiene forma propia: sólido."},
            {"it": "El agua del vaso", "cat": "liquido", "m": "Toma la forma del vaso: líquido."},
            {"it": "El aire", "cat": "gaseoso", "m": "El aire es un gas: ocupa todo el espacio."},
            {"it": "El vapor de la pava", "cat": "gaseoso",
             "m": "El vapor es agua en estado gaseoso."},
            {"it": "Un cubito de hielo", "cat": "solido", "m": "El hielo es agua sólida."},
            {"it": "El humo", "cat": "gaseoso", "m": "El humo se dispersa por el aire: gaseoso."},
            {"it": "La leche", "cat": "liquido", "m": "Se vuelca y toma la forma: líquida."},
            {"it": "El gas de la garrafa", "cat": "gaseoso", "m": "Es un gas, por eso se llama así."},
            {"it": "Una cuchara de metal", "cat": "solido", "m": "Tiene forma propia."},
            {"it": "El aceite", "cat": "liquido", "m": "Toma la forma del recipiente."},
            {"it": "Las burbujas de la gaseosa", "cat": "gaseoso",
             "m": "Adentro de la burbuja hay gas."},
            {"it": "La arena", "cat": "solido", "m": "Cada granito es sólido."},
            {"it": "El jugo", "cat": "liquido", "m": "Es líquido: toma la forma del vaso."},
            {"it": "El vaho que sale de la boca en invierno", "cat": "gaseoso",
             "m": "Es vapor de agua: estado gaseoso."},
        ],
    },

    # ── 3° · línea de tiempo del siglo XX ────────────────────────────────────────
    {
        "id": "linea_siglo_xx",
        "grado": 3, "area": AREA_CDM,
        "titulo": "Línea de tiempo", "icono": "📜",
        "mecanica": "ordenar",
        "consigna": "Ordená del más ANTIGUO al más nuevo. Tocá en orden.",
        "explica": "Pensá qué se inventó primero: lo más viejo va al principio.",
        "dc": "Impacto de las nuevas tecnologías; línea de tiempo",
        "fuente": "docs/auditoria-dc-caba/grado-3.md · C7",
        "saber": {"id": "CDM-3-tecnologias", "nombre": "Cambios tecnológicos en el tiempo",
                  "prereqs": ["CDM-1-tiempo"]},
        "banco": [
            {"items": ["La carreta tirada por caballos", "El tren a vapor",
                       "El auto", "El avión"]},
            {"items": ["La carta en papel", "El telégrafo",
                       "El teléfono de casa", "El celular"]},
            {"items": ["La vela", "El farol a querosén",
                       "La lamparita eléctrica", "La luz LED"]},
            {"items": ["El diario de papel", "La radio",
                       "La televisión", "Internet"]},
            {"items": ["Lavar la ropa en el río", "El lavadero con tabla",
                       "El lavarropas a manija", "El lavarropas automático"]},
            {"items": ["Guardar comida con hielo", "La heladera eléctrica",
                       "El freezer"]},
            {"items": ["Escribir con pluma y tintero", "La máquina de escribir",
                       "La computadora"]},
            {"items": ["La fotografía en blanco y negro", "La foto a color",
                       "La foto digital"]},
            {"items": ["El fuego a leña", "La cocina a gas",
                       "El microondas"]},
        ],
    },

    # ── 2° · qué cuenta lo resuelve ──────────────────────────────────────────────
    {
        "id": "que_cuenta_resuelve",
        "grado": 2, "area": "matematica",
        "titulo": "¿Qué cuenta lo resuelve?", "icono": "🧮",
        "mecanica": "trivia",
        "consigna": "¿Con qué cuenta se resuelve?",
        "dc": "Elegir la operación que resuelve el problema. Rediseñada: era clasificar en "
              "2 cajas y se acertaba el 50% por moneda",
        "fuente": "docs/auditoria-dc-caba/grado-2.md · M9",
        "saber": {"id": "MAT-2-operacion", "nombre": "Elegir la operación adecuada",
                  "prereqs": []},
        "banco": [
            {"q": "Hay 4 paquetes con 6 caramelos cada uno. ¿Cuántos caramelos hay?",
             "ops": ["6 + 6 + 6 + 6", "6 + 4", "6 − 4"],
             "m": "Son 4 grupos iguales de 6: se suma 6 cuatro veces."},
            {"q": "Tenía 20 figuritas y regalé 8. ¿Cuántas me quedan?",
             "ops": ["20 − 8", "20 + 8", "8 − 20"],
             "m": "Si regalás, tenés menos: hay que restar."},
            {"q": "Junté 15 tapitas y después 12 más. ¿Cuántas tengo?",
             "ops": ["15 + 12", "15 − 12", "15 + 2"],
             "m": "Se juntan las dos cantidades: se suma."},
            {"q": "Hay 3 mesas con 5 sillas cada una. ¿Cuántas sillas hay?",
             "ops": ["5 + 5 + 5", "5 + 3", "5 − 3"],
             "m": "Son 3 grupos iguales de 5."},
            {"q": "En el micro había 30 personas y bajaron 12. ¿Cuántas quedaron?",
             "ops": ["30 − 12", "30 + 12", "12 − 30"],
             "m": "Si bajan, quedan menos: se resta."},
            {"q": "Compré 2 cajas de 10 lápices. ¿Cuántos lápices compré?",
             "ops": ["10 + 10", "10 + 2", "10 − 2"],
             "m": "Dos grupos iguales de 10."},
            {"q": "Tenía 45 y me dieron 20 más. ¿Cuántos tengo?",
             "ops": ["45 + 20", "45 − 20", "20 − 45"],
             "m": "Si te dan más, se suma."},
            {"q": "Había 100 globos y se pincharon 25. ¿Cuántos quedan?",
             "ops": ["100 − 25", "100 + 25", "25 − 100"],
             "m": "Se pierden globos: se resta."},
            {"q": "Cada bolsa trae 4 manzanas. Compré 5 bolsas. ¿Cuántas manzanas?",
             "ops": ["4 + 4 + 4 + 4 + 4", "4 + 5", "5 − 4"],
             "m": "Cinco grupos iguales de 4."},
            {"q": "Leí 18 páginas ayer y 22 hoy. ¿Cuántas leí?",
             "ops": ["18 + 22", "22 − 18", "18 − 22"],
             "m": "Se juntan las dos cantidades."},
            {"q": "Tenía 60 pesos y gasté 35. ¿Cuánto me queda?",
             "ops": ["60 − 35", "60 + 35", "35 − 60"],
             "m": "Si gastás, te queda menos."},
            {"q": "Hay 6 cajas con 2 pelotas cada una. ¿Cuántas pelotas?",
             "ops": ["2 + 2 + 2 + 2 + 2 + 2", "6 + 2", "6 − 2"],
             "m": "Seis grupos iguales de 2."},
            {"q": "En el estante hay 40 libros y agrego 15. ¿Cuántos hay?",
             "ops": ["40 + 15", "40 − 15", "15 − 40"],
             "m": "Se agregan: se suma."},
            {"q": "Salieron 8 de los 25 alumnos. ¿Cuántos quedaron en el aula?",
             "ops": ["25 − 8", "25 + 8", "8 + 8"],
             "m": "Si salen, quedan menos."},
        ],
    },

    # ── 2° · adiviná mi figura ───────────────────────────────────────────────────
    {
        "id": "adivina_figura",
        "grado": 2, "area": "matematica",
        "titulo": "Adiviná mi figura", "icono": "🔷",
        "mecanica": "trivia",
        "consigna": "¿Qué figura es?",
        "dc": "Figuras geométricas por sus características: lados, vértices y ángulos "
              "rectos. Las figuras se reconocen aunque estén rotadas",
        "fuente": "docs/auditoria-dc-caba/grado-2.md · M15",
        "saber": {"id": "MAT-2-figuras", "nombre": "Figuras y sus características",
                  "prereqs": []},
        "banco": [
            {"q": "Tengo 3 lados y 3 vértices. ¿Qué soy?",
             "ops": ["Un triángulo", "Un cuadrado", "Un círculo"],
             "m": "Tri- significa tres: el triángulo tiene 3 lados."},
            {"q": "Tengo 4 lados iguales y 4 esquinas rectas. ¿Qué soy?",
             "ops": ["Un cuadrado", "Un rectángulo", "Un triángulo"],
             "m": "El cuadrado tiene los 4 lados iguales; el rectángulo no."},
            {"q": "No tengo ningún lado recto ni esquinas. ¿Qué soy?",
             "ops": ["Un círculo", "Un cuadrado", "Un triángulo"],
             "m": "El círculo es una curva cerrada: no tiene lados."},
            {"q": "Tengo 4 lados y 4 esquinas rectas, pero dos lados son más largos. ¿Qué soy?",
             "ops": ["Un rectángulo", "Un cuadrado", "Un rombo"],
             "m": "El rectángulo tiene los lados iguales de a pares."},
            {"q": "Tengo 4 lados iguales pero estoy inclinado, sin esquinas rectas. ¿Qué soy?",
             "ops": ["Un rombo", "Un cuadrado", "Un círculo"],
             "m": "El rombo tiene 4 lados iguales pero sus ángulos no son rectos."},
            {"q": "Aunque me den vuelta y quede apoyado en una punta, sigo teniendo 3 lados. ¿Qué soy?",
             "ops": ["Un triángulo", "Un cuadrado", "Un rectángulo"],
             "m": "Girar una figura no le cambia la cantidad de lados."},
            {"q": "¿Cuántos vértices tiene un cuadrado?",
             "ops": ["4", "3", "6"],
             "m": "Los vértices son las esquinas: el cuadrado tiene 4."},
            {"q": "¿Cuántos lados tiene un rectángulo?",
             "ops": ["4", "3", "5"],
             "m": "El rectángulo tiene 4 lados."},
            {"q": "Tengo 5 lados. ¿Qué soy?",
             "ops": ["Un pentágono", "Un cuadrado", "Un triángulo"],
             "m": "Penta- significa cinco: el pentágono tiene 5 lados."},
            {"q": "¿Qué figura rueda porque no tiene esquinas?",
             "ops": ["El círculo", "El cuadrado", "El triángulo"],
             "m": "Sin esquinas ni lados rectos, el círculo rueda."},
            {"q": "Tengo 6 lados. ¿Qué soy?",
             "ops": ["Un hexágono", "Un pentágono", "Un cuadrado"],
             "m": "Hexa- significa seis."},
            {"q": "Un cuadrado apoyado en una punta, ¿deja de ser cuadrado?",
             "ops": ["No, sigue siendo cuadrado", "Sí, pasa a ser rombo",
                     "Sí, pasa a ser triángulo"],
             "m": "Girar la figura no la cambia: sigue teniendo 4 lados iguales y ángulos rectos."},
            {"q": "¿Cuántas esquinas rectas tiene un triángulo cualquiera?",
             "ops": ["Puede no tener ninguna", "Siempre 3", "Siempre 1"],
             "m": "Hay triángulos sin ningún ángulo recto."},
            {"q": "¿Qué tienen en común el cuadrado y el rectángulo?",
             "ops": ["Los dos tienen 4 lados y 4 ángulos rectos",
                     "Los dos tienen los 4 lados iguales", "Los dos ruedan"],
             "m": "Ambos tienen 4 lados y 4 ángulos rectos; se diferencian en los lados."},
        ],
    },

    # ── 1° · del campo a tu casa ─────────────────────────────────────────────────
    {
        "id": "campo_a_casa",
        "grado": 1, "area": AREA_CDM,
        "titulo": "Del campo a tu casa", "icono": "🚚",
        "mecanica": "ordenar",
        "consigna": "Ordená cómo llega a tu casa. Tocá en orden.",
        "explica": "Empezá por dónde nace o se produce, y terminá en tu casa.",
        "dc": "De dónde vienen las cosas que usamos: procesos hasta llegar a casa",
        "fuente": "docs/auditoria-dc-caba/grado-1.md · C5",
        "saber": {"id": "CDM-1-origen", "nombre": "De dónde vienen las cosas",
                  "prereqs": []},
        "banco": [
            {"items": ["La gallina pone el huevo", "Se juntan los huevos",
                       "Se llevan al negocio", "Los comemos en casa"]},
            {"items": ["Crece la planta de tomate", "Se juntan los tomates",
                       "Se venden en la verdulería", "Hacemos la ensalada"]},
            {"items": ["La vaca da leche", "La leche va a la fábrica",
                       "Llega al supermercado", "La tomamos en casa"]},
            {"items": ["Se planta la semilla de trigo", "Crece la planta",
                       "Se hace harina", "Se hace el pan"]},
            {"items": ["El árbol da manzanas", "Se juntan las manzanas",
                       "Van al mercado", "Las comemos"]},
            {"items": ["La oveja da lana", "Se hace el hilo",
                       "Se teje la bufanda", "La usamos en invierno"]},
            {"items": ["Se planta la papa", "Se saca de la tierra",
                       "Se lava", "Se cocina en casa"]},
            {"items": ["La abeja hace la miel", "Se saca del panal",
                       "Se envasa en frascos", "La comemos con tostadas"]},
        ],
    },

    # ── 2° · cálculo redondo (PARAMÉTRICA: ejercicio nuevo cada vez) ─────────────
    {
        "id": "calculo_redondo",
        "grado": 2, "area": "matematica",
        "titulo": "Cálculo redondo", "icono": "💯",
        "mecanica": "parametrica",
        "consigna": "¿Cuánto da?",
        "dc": "Sumar y restar 1, 10 y 100 a números de tres cifras. Reemplaza sumas/restas, "
              "que operaban hasta 10 (contenido de 1°)",
        "fuente": "docs/auditoria-dc-caba/grado-2.md · M4",
        "saber": {"id": "MAT-2-redondo", "nombre": "Sumar y restar 1, 10 y 100",
                  "prereqs": []},
        "plantilla": {
            "q": "{a} + {b}",
            "vars": {"a": {"rango": [110, 880], "paso": 10},
                     "b": {"opciones": [1, 10, 100]}},
            "ok": "a + b",
            # distractores POSICIONALES: sumar en la columna equivocada, que es EL error
            "distractores": ["a + b*10", "a + b/10", "a - b"],
            "tope": 1000,
            "m": "Fijate en qué columna sumás: unidades con unidades, dieces con dieces, "
                 "cienes con cienes. Da {ok}.",
        },
    },

    # ── 2° · formá 100 y 1.000 (PARAMÉTRICA) ─────────────────────────────────────
    {
        "id": "forma_redondo",
        "grado": 2, "area": "matematica",
        "titulo": "¿Cuánto falta para llegar?", "icono": "🎯",
        "mecanica": "parametrica",
        "consigna": "¿Cuánto falta?",
        "dc": "Sumas que dan 100 y 1.000 — complementos, nodal del grado",
        "fuente": "docs/auditoria-dc-caba/grado-2.md · M3",
        "saber": {"id": "MAT-2-complemento", "nombre": "Complementos a 100 y 1.000",
                  "prereqs": ["MAT-2-redondo"]},
        "plantilla": {
            "q": "{a} + ___ = {objetivo}",
            "vars": {"a": {"rango": [5, 95], "paso": 5},
                     # la auditoría fija objetivos {100, 500, 1.000}
                     "objetivo": {"opciones": [100, 500, 1000]}},
            "ok": "objetivo - a",
            # trampas de magnitud: confundir el complemento a 100 con el de 1.000
            "distractores": ["100 - a", "objetivo - a - 10", "objetivo - a + 10"],
            "tope": 1000,
            "m": "Pensá cuánto le falta a {a} para llegar. La respuesta es {ok}.",
        },
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
    # una paramétrica no tiene banco: genera ejercicios sin límite, así que va a rondas
    # fijas. (Este `len(a["banco"])` sin guarda tiraba KeyError y, como `_menu_curricular`
    # atrapa cualquier excepción para no dejar al chico sin cuaderno, borraba EN SILENCIO
    # todas las actividades del grado. El fallback defensivo escondía el bug.)
    return [{"id": a["id"], "titulo": a["titulo"], "icono": a["icono"],
             "cfg": {"rondas": 10 if a["mecanica"] == "parametrica"
                     else min(10, max(6, len(a["banco"]) // 2))}}
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
def _validar_plantilla(ref, act):
    """Una plantilla mal declarada no falla al generarse: se queda sin candidatos y el
    juego termina solo. Por eso se valida acá, SIMULANDO tiradas de verdad."""
    problemas = []
    pl = act.get("plantilla") or {}
    for campo in ("q", "vars", "ok", "distractores"):
        if not pl.get(campo):
            problemas.append("%s: la plantilla no declara %r" % (ref, campo))
    if problemas:
        return problemas
    if len(pl["distractores"]) < 2:
        problemas.append("%s: %d distractores, mínimo 2" % (ref, len(pl["distractores"])))
    for n in pl["vars"]:
        if "{%s}" % n not in pl["q"]:
            problemas.append("%s: la variable %r no aparece en el enunciado" % (ref, n))
    # simulación: la plantilla tiene que producir ejercicios válidos de verdad, y VARIADOS
    ok, vistos = 0, set()
    for _ in range(400):
        ej = _simular(pl)
        if ej:
            ok += 1
            vistos.add(ej)
    if ok < 300:
        problemas.append("%s: sólo %d de 400 tiradas dan un ejercicio válido — las guardas "
                         "descartan casi todo" % (ref, ok))
    if len(vistos) < 20:
        problemas.append("%s: sólo %d ejercicios distintos; una paramétrica con tan poca "
                         "variedad no evita la memorización" % (ref, len(vistos)))
    return problemas


def _simular(pl):
    """Una tirada de la plantilla con las MISMAS guardas que el player. Devuelve el
    ejercicio como texto (para contar variedad) o None si las guardas lo descartan."""
    import random
    tope = pl.get("tope", float("inf"))
    entorno = {}
    for n, d in pl["vars"].items():
        if d.get("opciones"):
            entorno[n] = random.choice(d["opciones"])
        else:
            paso = d.get("paso", 1)
            lo, hi = d["rango"]
            entorno[n] = random.randint(-(-lo // paso), hi // paso) * paso
    try:
        ok = _eval(pl["ok"], entorno)
    except Exception:
        return None
    if ok != int(ok) or ok < 0 or ok > tope:
        return None
    ds = []
    for e in pl["distractores"]:
        try:
            d = _eval(e, entorno)
        except Exception:
            continue
        if d == int(d) and 0 <= d <= tope and d != ok and d not in ds:
            ds.append(d)
    if len(ds) < 2:
        return None
    return "%s=%s|%s" % (pl["q"].format(**entorno), int(ok), sorted(int(x) for x in ds[:2]))


def _eval(expr, entorno):
    """Mismo evaluador acotado que el player: sólo números, variables y + - * / ( )."""
    import ast as _ast
    OPS = (_ast.Add, _ast.Sub, _ast.Mult, _ast.Div, _ast.USub)
    arbol = _ast.parse(expr, mode="eval")
    for nodo in _ast.walk(arbol):
        if isinstance(nodo, (_ast.Expression, _ast.Constant, _ast.Name, _ast.Load)):
            continue
        if isinstance(nodo, (_ast.BinOp, _ast.UnaryOp)):
            continue
        if isinstance(nodo, OPS):
            continue
        raise ValueError("expresión no permitida: %s" % expr)
    return eval(compile(arbol, "<plantilla>", "eval"), {"__builtins__": {}}, dict(entorno))


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
        # una paramétrica no tiene banco: su contenido es la plantilla
        obligatorios = ["id", "grado", "area", "titulo", "icono", "mecanica", "dc",
                        "fuente", "saber"]
        obligatorios.append("plantilla" if a.get("mecanica") == "parametrica" else "banco")
        for campo in obligatorios:
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
        if mec == "parametrica":
            problemas.extend(_validar_plantilla(ref, a))
            continue                      # no tiene banco: el ejercicio se genera
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
    # el menú se tiene que poder ARMAR: si esto revienta, `_menu_curricular` lo atrapa y
    # el grado se queda sin ninguna actividad del catálogo, sin ningún error visible.
    for grado in range(1, 8):
        try:
            entradas = menu_de_grado(grado)
        except Exception as e:
            problemas.append("no se puede armar el menú de %d°: %s: %s"
                             % (grado, type(e).__name__, e))
            continue
        if len(entradas) != len(actividades_de(grado)):
            problemas.append("el menú de %d° trae %d entradas y hay %d actividades"
                             % (grado, len(entradas), len(actividades_de(grado))))
    # los prerrequisitos tienen que existir (en el catálogo o en el grafo grande)
    import saberes as grafo
    conocidos = saberes_vistos | set(grafo.SABERES)
    for a in CATALOGO:
        for p in (a.get("saber") or {}).get("prereqs") or []:
            if p not in conocidos:
                problemas.append("%s: prerrequisito inexistente %r" % (a["id"], p))
    return problemas
