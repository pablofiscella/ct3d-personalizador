"""aventura.py — contenido narrativo RAMIFICADO para el prototipo "Elegí tu aventura":
un grafo de nodos (texto + ilustración + decisiones), a diferencia de libro.py que arma
una historia 100% lineal.

v2 (11-jul-2026, pedido de Pablo): cada CAMINO completo (de inicio a final) tiene que
durar lo mismo que un libro/audiolibro de 20 páginas. Estructura: una espina de postas
narrativas (sin elección, un solo "Seguir →") con 2 puntos de decisión reales —
1) río/montaña (se abre temprano, converge unas postas después) y 2) tesoro/amigos (se
abre cerca del final, cada rama cierra con su propio final) — así CUALQUIER camino que
elija el chico totaliza ~20 nodos, aunque el grafo entero tenga más de 20 nodos únicos
(28 en total para safari) porque las ramas no convergen instantáneo.

REGLAS DE CONSISTENCIA (15-jul-2026, pedido de Pablo — "que no aparezca en otra hoja
del libro con otra ropa", extendido a todo personaje que acompañe de una hoja a las
siguientes). La gráfica se encara DESPUÉS (aventura_ia.py) pero las reglas de escritura
son ahora, para que el texto nunca le pida a la ilustración algo que no puede cumplir:

  1. VESTIMENTA DEL PROTAGONISTA — INTOCABLE EN EL TEXTO. `aventura_ia.py` ya fija la
     ropa del protagonista siempre igual (remera naranja/mostaza, short verde, mochila
     de explorador) en TODAS las escenas de TODOS los temas, vía prompt + imagen de
     referencia encadenada. El texto de acá NUNCA puede narrar que el protagonista se
     pone, se saca, se disfraza o le prestan una prenda/accesorio propio (nada de "se
     puso el sombrero", "se colocó la capa", "se disfrazó de mago") — eso contradice la
     ilustración. El protagonista puede TOCAR, ALCANZAR o DEVOLVER objetos/disfraces
     que son de OTRO personaje ("le alcanzó el sombrero al mago"), nunca vestirlos.

  2. PERSONAJES SECUNDARIOS QUE APARECEN UNA SOLA POSTA — libres. Un personaje que
     aparece y se va en el mismo nodo (o solo en los nodos de UNA rama, ya que el chico
     nunca ve las dos ramas en un mismo camino) no necesita regla especial: no hay
     riesgo de inconsistencia porque no hay "antes y después" que comparar.

  3. COMPAÑEROS RECURRENTES — aparecen en 2+ nodos NO consecutivos de la MISMA rama (o
     en la espina compartida, visible en TODOS los caminos). Estos sí necesitan
     consistencia real, porque el lector los ve más de una vez:
       a. Se identifican por ROL/NOMBRE fijo, no por descripción física variable (el
          "Maestro de Ceremonias", no "un señor con galera roja" que en otra posta pasa
          a describirse distinto).
       b. Una vez introducido, ese rol NUNCA cambia de rasgo descriptivo en una posta
          posterior (ni color, ni prenda, ni especie/tipo de animal, ni tamaño) — si
          hace falta un detalle visual memorable, se dice UNA vez al introducirlo y no
          se vuelve a mencionar (así no hay nada que contradecir después).
       c. Cada tema deja, en un comentario arriba de su bloque en AVENTURAS, la lista
          de sus compañeros recurrentes (rol + en qué nodos aparece) — es la referencia
          rápida para cuando aventura_ia.py necesite armarles SU PROPIA imagen de
          referencia encadenada, igual que ya existe para el protagonista.

  4. SIN CRUCE DE RAMA — un compañero de la rama A (ej. los equilibristas de circo)
     nunca se menciona ni aparece en la rama B (los elefantes) ni en la espina
     posterior, salvo que sea realmente el mismo personaje reencontrado a propósito
     (y en ese caso, va contado como compañero recurrente con su lista de nodos).
"""
import os

import temas as _temas


def _seguir(texto, next_id):
    return {"texto": texto, "opciones": [{"texto": "Seguir →", "next": next_id}]}


def _decision(texto, opciones):
    return {"texto": texto, "opciones": [{"texto": t, "next": n} for t, n in opciones]}


def _final(texto, tipo):
    return {"texto": texto, "final": tipo}


AVENTURAS = {
    "safari": {
        # ── espina compartida (1-4): el gancho hasta la primera decisión ──────
        "hook": _seguir(
            "{nombre} encontró un mapa viejo y doblado en el fondo de la mochila, con "
            "una X dorada marcada en el corazón de la sabana. Algo importante esperaba "
            "ser descubierto.", "camino"),
        "camino": _seguir(
            "Al amanecer, {nombre} se colgó la mochila al hombro y salió del "
            "campamento, con el mapa bien guardado y el corazón lleno de ganas de "
            "aventura.", "sabana"),
        "sabana": _seguir(
            "El sol pintaba de dorado la sabana entera. Manadas de cebras y jirafas "
            "pastaban tranquilas mientras {nombre} caminaba entre los pastizales "
            "altos, siguiendo el camino del mapa.", "bifurcacion"),
        "bifurcacion": _decision(
            "{nombre} llegó al punto exacto donde el mapa se dividía en dos: un "
            "sendero bajaba hacia un río a lo lejos, y otro subía hacia una montaña "
            "rocosa. ¿Por dónde seguir la aventura?",
            [("Ir hacia el río 🌊", "rio_1"), ("Subir la montaña ⛰️", "montana_1")]),

        # ── rama río (5-7) ──────────────────────────────────────────────────
        "rio_1": _seguir(
            "El camino del río estaba lleno de vida: pájaros de colores volaban entre "
            "los juncos y un grupo de elefantes chapoteaba felices en el agua.", "rio_2"),
        "rio_2": _seguir(
            "De pronto, {nombre} escuchó gritos a lo lejos: una familia de monitos, en "
            "la otra orilla, agitaba los brazos pidiendo ayuda.", "rio_3"),
        "rio_3": _seguir(
            "Con cuidado, {nombre} avanzó por las piedras del río hasta llegar junto a "
            "los monitos asustados, que enseguida se calmaron al verlo llegar.",
            "reencuentro"),

        # ── rama montaña (5-7) ──────────────────────────────────────────────
        "montana_1": _seguir(
            "El camino de la montaña era empinado y caluroso. {nombre} subió con "
            "cuidado entre las rocas doradas, agarrándose fuerte en cada escalón de "
            "piedra.", "montana_2"),
        "montana_2": _seguir(
            "A mitad de camino, {nombre} encontró unas huellas extrañas en el polvo, "
            "que se perdían hacia un sendero escondido entre las rocas.", "montana_3"),
        "montana_3": _seguir(
            "Siguiendo las huellas, {nombre} llegó hasta la entrada de una cueva "
            "marcada con una pequeña estrella tallada en la piedra.", "reencuentro"),

        # ── espina compartida (8-15): las ramas se juntan, hasta la 2ª decisión ─
        "reencuentro": _seguir(
            "Un poco más adelante, {nombre} encontró un pedazo de mapa rasgado "
            "enganchado en unas ramas: mostraba que el camino seguía derecho, más "
            "allá de una gran meseta dorada.", "jirafas"),
        "jirafas": _seguir(
            "Cruzando la meseta, un grupo de jirafas altísimas observaba con "
            "curiosidad, estirando el cuello para ver mejor al pequeño explorador.",
            "ravine"),
        "ravine": _seguir(
            "El camino se cortaba en una pequeña quebrada. {nombre} cruzó despacio "
            "por un tronco caído, con los brazos abiertos para no perder el "
            "equilibrio.", "marcas"),
        "marcas": _seguir(
            "Del otro lado, unas marcas doradas brillaban tenues sobre las rocas, "
            "como si alguien —hace mucho tiempo— hubiera dejado pistas para "
            "encontrar el camino.", "tormenta"),
        "tormenta": _seguir(
            "El cielo se puso gris de repente: un viento fuerte levantó arena y "
            "hojas por todos lados. Había que buscar refugio, ¡rápido!", "refugio"),
        "refugio": _seguir(
            "{nombre} se escondió detrás de unas piedras grandes junto a un grupo de "
            "animales asustados, todos juntos esperando que pasara la tormenta.",
            "calma"),
        "calma": _seguir(
            "Cuando el viento se calmó, la sabana entera brillaba dorada bajo el sol "
            "de la tarde, más hermosa que nunca.", "encrucijada"),
        "encrucijada": _decision(
            "El camino volvía a dividirse: hacia un costado brillaba una luz dorada "
            "entre las rocas; hacia el otro, se escuchaban voces de animales pidiendo "
            "ayuda otra vez. ¿Qué hacer?",
            [("Seguir la luz dorada ✨", "tesoro_1"),
             ("Ir a ayudar a los animales 🦁", "amigos_1")]),

        # ── final tesoro (16-20) ────────────────────────────────────────────
        "tesoro_1": _seguir(
            "{nombre} siguió el brillo dorado entre las rocas, con el corazón "
            "latiendo fuerte de emoción.", "tesoro_2"),
        "tesoro_2": _seguir(
            "La luz llevaba hasta una pequeña gruta escondida, cubierta de flores "
            "silvestres, donde algo dorado destellaba en el centro.", "tesoro_3"),
        "tesoro_3": _seguir(
            "Ahí, sobre una piedra lisa, estaba la brújula dorada de exploración de "
            "la que hablaba la leyenda del safari.", "tesoro_4"),
        "tesoro_4": _seguir(
            "{nombre} la levantó con las dos manos, sintiendo cómo brillaba cálida, "
            "como si supiera que había encontrado a su dueño.", "tesoro_final"),
        "tesoro_final": _final(
            "Con la brújula dorada en la mano, {nombre} supo que ya nunca más se "
            "perdería un camino — y que esta aventura sería la primera de muchas.",
            "tesoro"),

        # ── final amigos (16-20) ────────────────────────────────────────────
        "amigos_1": _seguir(
            "{nombre} corrió hacia las voces, sin dudarlo ni un segundo.", "amigos_2"),
        "amigos_2": _seguir(
            "Eran los animales de la selva: se habían perdido buscando el mismo "
            "tesoro, y no sabían cómo volver a casa.", "amigos_3"),
        "amigos_3": _seguir(
            "{nombre} recordó cada paso del camino recorrido y, con calma, los fue "
            "guiando de vuelta hacia la sabana abierta.", "amigos_4"),
        "amigos_4": _seguir(
            "Uno por uno, los animales fueron reconociendo el camino, cada vez más "
            "tranquilos y agradecidos.", "amigos_final"),
        "amigos_final": _final(
            "Al llegar a la sabana dorada, todos festejaron juntos: {nombre} había "
            "encontrado algo mejor que un tesoro — un montón de amigos para "
            "siempre.", "amigos"),
    },

    "circo": {
        # COMPAÑERO RECURRENTE: el Maestro de Ceremonias — aparece en pista,
        # bifurcacion, reencuentro, encrucijada, oscuridad, heroe_1, heroe_2,
        # heroe_final. Identificado solo por rol (sin rasgo físico descrito) — nada
        # que contradecir entre apariciones. Es quien necesita imagen de referencia
        # propia cuando se encare la gráfica.
        # ── espina compartida (1-4): el gancho hasta la primera decisión ──────
        "hook": _seguir(
            "Esa tarde llegó a nombre de {nombre} un sobre dorado con letras que "
            "brillaban: «Esta noche sos Ayudante de Pista Honorario en la Gran "
            "Función». Faltaban solo unas horas para el show.", "carpa"),
        "carpa": _seguir(
            "{nombre} entró por la puerta de artistas, justo detrás de la carpa "
            "rayada, donde todo era un remolino de lentejuelas, risas y música "
            "de ensayo.", "pista"),
        "pista": _seguir(
            "En el centro de la pista, el Maestro de Ceremonias hacía las últimas "
            "pruebas de luces. Al ver a {nombre}, sonrió: «¡Justo a tiempo! Hay "
            "dos números que todavía necesitan una mano».", "bifurcacion"),
        "bifurcacion": _decision(
            "«Los equilibristas están terminando de armar la cuerda floja allá "
            "arriba, y los elefantes están nerviosos antes de su entrada. "
            "¿A quién ayudamos primero?»",
            [("Ir con los equilibristas 🎪", "cuerda_1"),
             ("Ir con los elefantes 🐘", "elefantes_1")]),

        # ── rama cuerda floja (5-7) ────────────────────────────────────────
        "cuerda_1": _seguir(
            "Arriba, entre las luces, dos equilibristas terminaban de tensar la "
            "cuerda. {nombre} les alcanzó cada broche brillante, uno por uno, "
            "con mucho cuidado.", "cuerda_2"),
        "cuerda_2": _seguir(
            "«Nos falta la sombrilla de plumas», dijo una de las equilibristas, "
            "buscando entre los baúles de vestuario sin encontrarla por ningún "
            "lado.", "cuerda_3"),
        "cuerda_3": _seguir(
            "{nombre} la encontró colgada de una cortina, brillando con cada "
            "movimiento. Se la alcanzó justo a tiempo para el último ensayo.",
            "reencuentro"),

        # ── rama elefantes (5-7) ───────────────────────────────────────────
        "elefantes_1": _seguir(
            "Detrás de la carpa, los elefantes se movían inquietos: el ruido del "
            "público que iba llegando los ponía nerviosos antes de salir a "
            "escena.", "elefantes_2"),
        "elefantes_2": _seguir(
            "{nombre} se acercó despacio, hablándoles bajito, y les acarició la "
            "trompa a cada uno hasta que, de a poco, se fueron calmando.",
            "elefantes_3"),
        "elefantes_3": _seguir(
            "El más chiquito de todos apoyó la trompa en el hombro de {nombre}, "
            "agradecido, justo cuando llamaban a los elefantes a formar fila "
            "para la entrada.", "reencuentro"),

        # ── espina compartida (8-15): las ramas se juntan, hasta la 2ª decisión ─
        "reencuentro": _seguir(
            "Con todo listo, {nombre} volvió al centro de la pista, donde el "
            "Maestro de Ceremonias repasaba el programa de la noche con una "
            "sonrisa nerviosa y feliz.", "payasos"),
        "payasos": _seguir(
            "Los payasos pasaron corriendo, haciendo malabares con pelotas de "
            "colores mientras se probaban narices nuevas, una más grande que "
            "la otra.", "luces"),
        "luces": _seguir(
            "El técnico de luces probó cada foco: rojo, dorado, violeta... la "
            "carpa entera se llenó de colores por un instante, como un arcoíris "
            "gigante.", "publico"),
        "publico": _seguir(
            "Del otro lado de la cortina llegaba un murmullo cada vez más "
            "fuerte: el público entraba a las gradas, buscando los mejores "
            "lugares para ver todo de cerca.", "apagon"),
        "apagon": _seguir(
            "De repente, todas las luces titilaron y se apagaron por completo. "
            "Un «oooh» de sorpresa recorrió las gradas — algo se había cortado "
            "justo antes de empezar.", "oscuridad"),
        "oscuridad": _seguir(
            "En la oscuridad, {nombre} sintió que alguien le ponía una vela "
            "encendida en la mano: el Maestro de Ceremonias, guiando a todos "
            "con calma hacia el centro de la pista.", "velas"),
        "velas": _seguir(
            "Una por una, se fueron encendiendo velas por toda la carpa, hasta "
            "que la oscuridad se llenó de lucecitas cálidas, casi más lindas "
            "que las luces eléctricas.", "encrucijada"),
        "encrucijada": _decision(
            "El Maestro de Ceremonias miró a {nombre} con una idea brillando en "
            "los ojos: «El show tiene que empezar igual. ¿Querés salir a "
            "abrir la función, o preferís ayudarme a resolver esto desde "
            "bambalinas?»",
            [("Salir a abrir el show ✨", "estrella_1"),
             ("Ayudar desde bambalinas 🔧", "heroe_1")]),

        # ── final estrella (16-20) ──────────────────────────────────────────
        "estrella_1": _seguir(
            "{nombre} caminó hasta el centro de la pista, con una vela en la "
            "mano y el corazón latiendo fuerte de emoción.", "estrella_2"),
        "estrella_2": _seguir(
            "El público, a la luz de las velas, hizo silencio total — todos los "
            "ojos puestos en el pequeño Ayudante de Pista Honorario.",
            "estrella_3"),
        "estrella_3": _seguir(
            "Con voz clara, {nombre} anunció: «¡Bienvenidos a la Gran Función!» "
            "y la carpa entera estalló en aplausos, más fuerte que nunca.",
            "estrella_4"),
        "estrella_4": _seguir(
            "Justo en ese instante, las luces volvieron de golpe, como si "
            "hubieran esperado esa señal para encenderse todas juntas.",
            "estrella_final"),
        "estrella_final": _final(
            "El show empezó con {nombre} todavía en el centro de la pista, "
            "aplaudido por todo el circo — la función más brillante que la "
            "carpa había visto jamás.", "estrella"),

        # ── final héroe de bambalinas (16-20) ────────────────────────────────
        "heroe_1": _seguir(
            "{nombre} siguió al Maestro de Ceremonias hasta el tablero de "
            "luces, donde un cable se había soltado justo detrás de una "
            "caja de fusibles.", "heroe_2"),
        "heroe_2": _seguir(
            "Con manos firmes, {nombre} sostuvo la linterna mientras el "
            "Maestro conectaba el cable de nuevo, con cuidado de no "
            "apurarse.", "heroe_3"),
        "heroe_3": _seguir(
            "Del otro lado de la cortina se escuchaban los aplausos: los "
            "payasos habían salido a hacer reír al público mientras tanto, "
            "ganando tiempo con malabares.", "heroe_4"),
        "heroe_4": _seguir(
            "Con un último clic, las luces volvieron todas juntas, más "
            "brillantes que antes — {nombre} había salvado la función desde "
            "las sombras.", "heroe_final"),
        "heroe_final": _final(
            "Nadie en el público supo nunca lo que había pasado detrás de la "
            "cortina — pero el Maestro de Ceremonias sí, y le regaló a "
            "{nombre} el título de Verdadero Mago de la Carpa.", "heroe"),
    },

    "artistas": {
        # COMPAÑERO RECURRENTE: la Profe Lula — aparece en taller, mural, encargo,
        # coleccion, salpicon, calma, revelacion, decision, mezcla_1, mezcla_2,
        # mezcla_final. Identificada solo por rol, sin rasgo físico descrito.
        # ── espina compartida (1-4) ────────────────────────────────────────
        "hook": _seguir(
            "El taller de los pequeños artistas olía a témpera fresca. Esa tarde, "
            "la Profe Lula anunció que faltaban solo horas para abrir la Gran "
            "Feria de Arte, y el mural más grande del taller seguía a medio "
            "terminar.", "mural"),
        "mural": _seguir(
            "{nombre} se acercó a mirarlo: era enorme, cubría toda una pared, "
            "pero le faltaban colores y formas por todos lados todavía.", "encargo"),
        "encargo": _seguir(
            "«Necesito un ayudante para terminarlo a tiempo», dijo la Profe Lula, "
            "con un pincel en cada mano. «¿Te sumás?» {nombre} asintió sin "
            "dudarlo.", "coleccion"),
        "coleccion": _decision(
            "«Todavía falta pintar el cielo con muchos colores, y pegar las "
            "formas de papel que faltan». ¿Con qué parte del mural empezamos?",
            [("Pintar el cielo de colores 🎨", "colores_1"),
             ("Pegar las formas de papel ✂️", "formas_1")]),

        # ── rama colores (5-7) ──────────────────────────────────────────────
        "colores_1": _seguir(
            "{nombre} mojó el pincel en un pote de témpera dorada y empezó a "
            "pintar grandes trazos curvos por todo el cielo del mural.",
            "colores_2"),
        "colores_2": _seguir(
            "La Profe Lula mezclaba colores nuevos en una paleta: azul con "
            "amarillo daba verde, rojo con blanco daba rosa — un truco de magia "
            "de verdad.", "colores_3"),
        "colores_3": _seguir(
            "Juntos llenaron el cielo entero de un arcoíris gigante, tan "
            "brillante que parecía tener luz propia.", "reencuentro"),

        # ── rama formas (5-7) ────────────────────────────────────────────────
        "formas_1": _seguir(
            "{nombre} juntó las formas de papel de colores que faltaban: "
            "círculos, estrellas y espirales recortadas por todo el taller.",
            "formas_2"),
        "formas_2": _seguir(
            "Con pegamento y mucho cuidado, fue ubicando cada forma en su "
            "lugar del mural, como piezas de un rompecabezas gigante.",
            "formas_3"),
        "formas_3": _seguir(
            "Cuando la última espiral quedó pegada, el mural entero cobró "
            "una textura nueva, con relieve y brillo por todos lados.",
            "reencuentro"),

        # ── espina compartida (8-15) ──────────────────────────────────────
        "reencuentro": _seguir(
            "La Profe Lula dio un paso atrás para mirar el mural completo: "
            "«¡Ya casi está! Solo falta el detalle final», dijo con una "
            "sonrisa enorme.", "pinceles"),
        "pinceles": _seguir(
            "Sobre la mesa central, un montón de pinceles limpios esperaban en "
            "fila, cada uno de un tamaño distinto, listos para el último "
            "toque.", "publico"),
        "publico": _seguir(
            "Afuera del taller ya se escuchaban voces: las familias empezaban "
            "a llegar temprano, ansiosas por ver la Feria de Arte de este "
            "año.", "salpicon"),
        "salpicon": _seguir(
            "Justo entonces, un frasco de pintura violeta se volcó sin querer "
            "y dejó un salpicón enorme justo en el medio del mural.",
            "sorpresa"),
        "sorpresa": _seguir(
            "Todos se quedaron quietos un segundo, mirando la mancha — hasta "
            "que la Profe Lula soltó una risa: «¡Eso también es arte!»",
            "calma"),
        "calma": _seguir(
            "Con esa idea dando vueltas, el taller entero volvió a respirar "
            "tranquilo, mirando la mancha violeta como una posibilidad nueva.",
            "revelacion"),
        "revelacion": _seguir(
            "{nombre} miró la mancha con atención: tenía una forma curiosa, "
            "casi como una flor gigante esperando a que alguien la "
            "descubriera.", "decision"),
        "decision": _decision(
            "La Profe Lula le pasó un pincel a {nombre}: «Tenés dos caminos: "
            "tapar la mancha con más color, o convertirla en la parte más "
            "linda del mural». ¿Qué hacemos?",
            [("Convertir la mancha en una flor 🌸", "flor_1"),
             ("Sumar a todo el taller a repintar 🖌️", "equipo_1")]),

        # ── final flor (16-20) ──────────────────────────────────────────────
        "flor_1": _seguir(
            "{nombre} tomó el pincel más fino y empezó a dibujar pétalos "
            "alrededor de la mancha violeta, con trazos suaves y curvos.",
            "flor_2"),
        "flor_2": _seguir(
            "De a poco, la mancha se fue transformando: ya no era un error, "
            "era el centro de una flor enorme en medio del mural.",
            "flor_3"),
        "flor_3": _seguir(
            "La Profe Lula sumó unas hojas verdes alrededor, y la flor quedó "
            "como si siempre hubiera sido parte del plan.", "flor_4"),
        "flor_4": _seguir(
            "El mural entero pareció cobrar vida con esa flor gigante en el "
            "centro, brillando distinta a todo lo demás.", "flor_final"),
        "flor_final": _final(
            "Cuando las familias entraron a la Feria de Arte, todas se "
            "detuvieron frente a la flor violeta — nadie imaginó que un "
            "accidente pudiera volverse lo más lindo del mural.", "flor"),

        # ── final equipo (16-20) ─────────────────────────────────────────────
        "equipo_1": _seguir(
            "{nombre} corrió a buscar a todos los artistas del taller: «¡Los "
            "necesitamos a todos para el final!», anunció con una sonrisa.",
            "equipo_2"),
        "equipo_2": _seguir(
            "Uno por uno, cada chico y cada chica del taller tomó un pincel y "
            "eligió un rincón del mural para darle su propio toque.",
            "equipo_3"),
        "equipo_3": _seguir(
            "Entre todos, mezclaron colores nuevos, agregaron detalles "
            "pequeños y taparon la mancha con un remolino de color "
            "colectivo.", "equipo_4"),
        "equipo_4": _seguir(
            "La Profe Lula miraba maravillada: nunca el mural había tenido "
            "tantas manos distintas trabajando juntas al mismo tiempo.",
            "equipo_final"),
        "equipo_final": _final(
            "El mural quedó terminado justo cuando abrieron las puertas — no "
            "por una sola idea, sino por todo un taller de pequeños artistas "
            "trabajando juntos, con {nombre} al frente.", "equipo"),
    },

    "aviadores": {
        # COMPAÑERO RECURRENTE: el Capitán Vega — aparece en hangar, revision,
        # briefing, reencuentro, radio, niebla, calma, decision, faro_1, faro_2,
        # faro_final, aterrizaje_1, aterrizaje_2, aterrizaje_final. Identificado
        # solo por rol, sin rasgo físico descrito.
        # ── espina compartida (1-4) ────────────────────────────────────────
        "hook": _seguir(
            "Esa mañana, {nombre} recibió una gorra de piloto y una invitación: "
            "«Copiloto Honorario para la Gran Carrera Aérea» — la carrera más "
            "esperada del año, esa misma tarde.", "revision"),
        "revision": _seguir(
            "En el hangar, el Capitán Vega revisaba su avión de punta a punta, "
            "silbando bajito mientras controlaba cada instrumento del "
            "tablero.", "briefing"),
        "briefing": _seguir(
            "«Antes de despegar hay dos cosas por hacer», dijo el Capitán "
            "Vega, señalando un mapa desplegado sobre una mesa metálica.",
            "bifurcacion"),
        "bifurcacion": _decision(
            "«Hay que trazar la ruta con la brújula, y cargar el correo "
            "especial de la carrera. ¿Con cuál empezamos?»",
            [("Trazar la ruta con la brújula 🧭", "ruta_1"),
             ("Cargar el correo especial ✉️", "correo_1")]),

        # ── rama ruta (5-7) ──────────────────────────────────────────────────
        "ruta_1": _seguir(
            "{nombre} desplegó el mapa sobre el ala del avión y siguió con el "
            "dedo cada línea, marcando el camino que atravesaba montañas y "
            "nubes.", "ruta_2"),
        "ruta_2": _seguir(
            "El Capitán Vega le mostró cómo usar la brújula: la aguja siempre "
            "señalaba el norte, sin importar cuánto girara el avión en el "
            "aire.", "ruta_3"),
        "ruta_3": _seguir(
            "Juntos marcaron la ruta final con una línea roja bien clara, "
            "lista para seguir apenas despegaran.", "reencuentro"),

        # ── rama correo (5-7) ──────────────────────────────────────────────
        "correo_1": _seguir(
            "{nombre} ayudó a cargar bolsas llenas de sobres y paquetes "
            "atados con piolín, cada uno con un destino distinto anotado.",
            "correo_2"),
        "correo_2": _seguir(
            "El más pesado de todos era un paquete redondo, envuelto con "
            "cuidado: la copa dorada para el ganador de la carrera.",
            "correo_3"),
        "correo_3": _seguir(
            "Entre los dos acomodaron todo bien firme dentro del avión, para "
            "que nada se moviera durante el vuelo.", "reencuentro"),

        # ── espina compartida (8-15) ──────────────────────────────────────
        "reencuentro": _seguir(
            "Con todo listo, el Capitán Vega dio la señal: el motor rugió y "
            "el avión empezó a rodar por la pista, cada vez más rápido.",
            "despegue"),
        "despegue": _seguir(
            "Las ruedas se despegaron del suelo y, de golpe, todo el "
            "aeródromo quedó chiquito allá abajo, como un dibujo desde "
            "arriba.", "vuelo"),
        "vuelo": _seguir(
            "El cielo se abrió enorme y celeste. Otros aviones de la carrera "
            "volaban cerca, todos en fila, siguiendo la misma ruta trazada.",
            "radio"),
        "radio": _seguir(
            "Por la radio del avión se escuchaban las voces de los otros "
            "pilotos, avisando cada tanto su posición en el cielo.", "niebla"),
        "niebla": _seguir(
            "De repente, una nube espesa envolvió el avión entero: no se "
            "veía nada más allá del vidrio de la cabina.", "calma"),
        "calma": _seguir(
            "El Capitán Vega respiró tranquilo: «Tranquilo, para esto "
            "practicamos», dijo, sin soltar el timón ni un segundo.",
            "instrumentos"),
        "instrumentos": _seguir(
            "{nombre} miró el tablero: cada aguja y cada lucecita seguían "
            "funcionando, mostrando el camino aunque no se viera nada "
            "afuera.", "decision"),
        "decision": _decision(
            "«Hay dos formas de salir de esto», dijo el Capitán Vega. «Seguir "
            "la brújula hasta el faro de la costa, o bajar despacio hasta un "
            "aeródromo chiquito para esperar que se despeje». ¿Qué elegimos?",
            [("Seguir la brújula hasta el faro 🗼", "faro_1"),
             ("Aterrizar y esperar 🛬", "aterrizaje_1")]),

        # ── final faro (16-20) ──────────────────────────────────────────────
        "faro_1": _seguir(
            "{nombre} no despegó los ojos de la brújula ni un segundo, "
            "guiando al Capitán Vega con la voz firme: «Más a la "
            "izquierda... así, derecho».", "faro_2"),
        "faro_2": _seguir(
            "De a poco, entre la niebla, empezó a verse una luz que giraba: "
            "el faro de la costa, justo donde debía estar.", "faro_3"),
        "faro_3": _seguir(
            "El avión salió de la nube justo sobre el mar, con el sol "
            "brillando de nuevo sobre las alas plateadas.", "faro_4"),
        "faro_4": _seguir(
            "Los demás aviones de la carrera aparecieron detrás, siguiendo "
            "la misma luz que {nombre} había encontrado primero.",
            "faro_final"),
        "faro_final": _final(
            "Cruzaron la meta con el sol de frente, primeros en llegar — "
            "gracias a un copiloto que nunca soltó la brújula.", "faro"),

        # ── final aterrizaje (16-20) ─────────────────────────────────────────
        "aterrizaje_1": _seguir(
            "El Capitán Vega bajó despacio la velocidad, buscando con la "
            "mirada un claro entre la niebla para aterrizar con seguridad.",
            "aterrizaje_2"),
        "aterrizaje_2": _seguir(
            "{nombre} avistó una pista chiquita, casi escondida entre unos "
            "árboles: «¡Ahí, a la derecha!», gritó justo a tiempo.",
            "aterrizaje_3"),
        "aterrizaje_3": _seguir(
            "Las ruedas tocaron tierra suavemente, y el avión frenó justo "
            "frente a un pequeño aeródromo de campo, casi vacío.",
            "aterrizaje_4"),
        "aterrizaje_4": _seguir(
            "Esperaron ahí, tomando algo caliente que les convidó un "
            "guardián del lugar, hasta que la niebla se despejó del todo.",
            "aterrizaje_final"),
        "aterrizaje_final": _final(
            "Cuando por fin despegaron de nuevo, el cielo estaba "
            "completamente limpio — y aunque llegaron últimos a la carrera, "
            "el Capitán Vega dijo que ese había sido el vuelo más sabio de "
            "todos.", "aterrizaje"),
    },

    "bomberos": {
        # COMPAÑERO RECURRENTE: la Capitana Ruiz — aparece en estacion, alarma,
        # equipo, reencuentro, humo, calle, calma, decision, manguera_1,
        # manguera_final, escalera_1, escalera_final. Identificada solo por rol,
        # sin rasgo físico descrito.
        # ── espina compartida (1-4) ────────────────────────────────────────
        "hook": _seguir(
            "Esa tarde, la estación de bomberos abría sus puertas para la "
            "Gran Jornada de Puertas Abiertas, y {nombre} llegó justo a "
            "tiempo con un casco chiquito prestado.", "alarma"),
        "alarma": _seguir(
            "De repente, una sirena sonó fuerte: no era un simulacro, era una "
            "alarma real. La Capitana Ruiz corrió hacia el camión sin perder "
            "un segundo.", "equipo"),
        "equipo": _seguir(
            "«¡Vamos, ayudante!», le gritó a {nombre} mientras se subía al "
            "camión. Un local de la esquina tenía mucho humo saliendo por "
            "la puerta.", "bifurcacion"),
        "bifurcacion": _decision(
            "Al llegar, la Capitana Ruiz repartió tareas rápido: «Necesito "
            "gente en la manguera y gente en la escalera. ¿Con cuál te "
            "quedás?»",
            [("Ir con el equipo de manguera 💦", "manguera_1"),
             ("Ir con el equipo de escalera 🪜", "escalera_1")]),

        # ── rama manguera (5-7) ────────────────────────────────────────────
        "manguera_1": _seguir(
            "{nombre} ayudó a desenrollar la manguera larga, estirándola "
            "bien derecha desde el camión hasta la puerta del local.",
            "manguera_2"),
        "manguera_2": _seguir(
            "Dos bomberos sostuvieron la manguera con fuerza mientras "
            "{nombre} abría la válvula despacio, tal como le habían "
            "enseñado.", "manguera_3"),
        "manguera_3": _seguir(
            "Un chorro de agua salió disparado hacia el humo, mientras "
            "adentro alguien tosía pero ya se escuchaba más tranquilo.",
            "reencuentro"),

        # ── rama escalera (5-7) ────────────────────────────────────────────
        "escalera_1": _seguir(
            "{nombre} ayudó a sostener la base de la escalera mientras se "
            "extendía, alta y firme, hasta la ventana del primer piso.",
            "escalera_2"),
        "escalera_2": _seguir(
            "Un bombero subió con cuidado, y desde abajo {nombre} le "
            "avisaba cada paso: «¡Un poco más, ya casi llegás!»",
            "escalera_3"),
        "escalera_3": _seguir(
            "Por la ventana asomó un gatito asustado, que el bombero bajó "
            "con mucho cuidado, envuelto en una manta.", "reencuentro"),

        # ── espina compartida (8-15) ──────────────────────────────────────
        "reencuentro": _seguir(
            "El humo empezó a despejarse, y la Capitana Ruiz salió del local "
            "con el pulgar arriba: «¡Todo controlado, nadie salió "
            "lastimado!»", "vecinos"),
        "vecinos": _seguir(
            "Los vecinos, que se habían juntado en la vereda, aplaudieron "
            "fuerte al ver salir a todo el equipo sano y salvo.", "humo"),
        "humo": _seguir(
            "Un último hilo de humo gris salía todavía por una ventana "
            "chica, en la parte de atrás del local, casi escondida.",
            "calle"),
        "calle": _seguir(
            "La Capitana Ruiz frunció el ceño: «Ahí atrás hay un depósito. "
            "Vamos a revisar que esté todo bien», dijo, ya caminando hacia "
            "allá.", "calma"),
        "calma": _seguir(
            "{nombre} caminó junto a ella, con el casco bien puesto, listo "
            "para ayudar en lo que hiciera falta.", "deposito"),
        "deposito": _seguir(
            "Adentro del depósito, unas cajas de cartón se habían quemado "
            "apenas en una esquina — nada grave, pero había que asegurarse "
            "bien.", "revision2"),
        "revision2": _seguir(
            "{nombre} ayudó a mover las cajas a un lugar seguro, mientras la "
            "Capitana Ruiz revisaba que no quedara ninguna brasa "
            "escondida.", "decision"),
        "decision": _decision(
            "«Ya está todo controlado», dijo la Capitana Ruiz. «Ahora hay "
            "que avisarle a la gente que todo está bien. ¿Querés salir a "
            "contarlo, o te quedás ayudando a guardar el equipo?»",
            [("Salir a avisar a los vecinos 📢", "aviso_1"),
             ("Quedarse guardando el equipo 🧰", "orden_1")]),

        # ── final aviso (16-20) ──────────────────────────────────────────────
        "aviso_1": _seguir(
            "{nombre} tomó el megáfono que le prestó un bombero y salió "
            "hacia la vereda, donde todos esperaban noticias.", "aviso_2"),
        "aviso_2": _seguir(
            "«¡Todo está controlado!», anunció {nombre} con voz fuerte y "
            "clara, y un aplauso enorme recorrió toda la calle.", "aviso_3"),
        "aviso_3": _seguir(
            "Los vecinos se acercaron a saludar, algunos con mates y "
            "termos, agradecidos por la rapidez de todo el equipo.",
            "aviso_4"),
        "aviso_4": _seguir(
            "La Capitana Ruiz miró la escena con orgullo: el pequeño "
            "ayudante había calmado a todo el barrio con solo unas "
            "palabras.", "aviso_final"),
        "aviso_final": _final(
            "Esa noche, la Jornada de Puertas Abiertas terminó con "
            "{nombre} como la voz oficial del barrio — el ayudante que "
            "supo cuándo hablar fuerte y claro.", "aviso"),

        # ── final orden (16-20) ─────────────────────────────────────────────
        "orden_1": _seguir(
            "{nombre} se quedó en la estación, ayudando a enrollar la "
            "manguera larga con cuidado, vuelta por vuelta.", "orden_2"),
        "orden_2": _seguir(
            "Guardó cada casco en su lugar y revisó que la escalera "
            "quedara bien plegada, lista para la próxima alarma.",
            "orden_3"),
        "orden_3": _seguir(
            "La Capitana Ruiz lo miraba trabajar con una sonrisa: «Un buen "
            "equipo también se nota en cómo deja todo listo», le dijo.",
            "orden_4"),
        "orden_4": _seguir(
            "Cuando todo quedó en su lugar, el camión brillaba entero, "
            "listo para salir a la próxima llamada en cualquier momento.",
            "orden_final"),
        "orden_final": _final(
            "La Capitana Ruiz le entregó a {nombre} un casco propio, de "
            "verdad: «Para el ayudante que cuida el equipo tan bien como "
            "cuida a la gente».", "orden"),
    },

    "campamento": {
        # COMPAÑERO RECURRENTE: la Guía Coral — aparece en hook, mapa, encargo,
        # reencuentro, fogon, canciones, cielo, apagada, decision, luciernagas_1,
        # luciernagas_final, estrellas_1, estrellas_final. Identificada solo por
        # rol, sin rasgo físico descrito.
        # ── espina compartida (1-4) ────────────────────────────────────────
        "hook": _seguir(
            "La primera noche de campamento, la Guía Coral juntó a todos "
            "alrededor del fogón apagado: «Esta noche hacemos la Gran Caminata "
            "Nocturna, la tradición más vieja del campamento».", "mapa"),
        "mapa": _seguir(
            "Desplegó un mapa dibujado a mano, lleno de senderos que se "
            "perdían entre los árboles del bosque, hacia un claro secreto.",
            "encargo"),
        "encargo": _seguir(
            "«Necesito ayuda con dos cosas antes de salir», dijo la Guía "
            "Coral, mirando a {nombre} con una sonrisa cómplice.", "bifurcacion"),
        "bifurcacion": _decision(
            "«Hay que marcar el sendero con cintas de colores, y afinar las "
            "guitarras para cantar en el claro. ¿Con cuál empezamos?»",
            [("Marcar el sendero 🎗️", "sendero_1"),
             ("Afinar las guitarras 🎸", "guitarra_1")]),

        # ── rama sendero (5-7) ────────────────────────────────────────────
        "sendero_1": _seguir(
            "{nombre} caminó entre los árboles atando cintas de colores en "
            "las ramas más bajas, marcando el camino de ida y de vuelta.",
            "sendero_2"),
        "sendero_2": _seguir(
            "En un tronco caído encontró la marca perfecta para girar: una "
            "cinta roja bien visible, atada por algún campamento anterior.",
            "sendero_3"),
        "sendero_3": _seguir(
            "Con el sendero entero marcado, {nombre} volvió corriendo, "
            "orgulloso de dejar el camino listo para todos.", "reencuentro"),

        # ── rama guitarra (5-7) ───────────────────────────────────────────
        "guitarra_1": _seguir(
            "{nombre} ayudó a repartir las guitarras entre los campamentistas "
            "más grandes, una por una, con mucho cuidado.", "guitarra_2"),
        "guitarra_2": _seguir(
            "La Guía Coral enseñó a afinar cada cuerda, girando las clavijas "
            "despacio hasta que sonaban todas parejas.", "guitarra_3"),
        "guitarra_3": _seguir(
            "Ensayaron juntos la canción de cierre del campamento, la misma "
            "que se cantaba desde hacía años alrededor del fogón.",
            "reencuentro"),

        # ── espina compartida (8-15) ──────────────────────────────────────
        "reencuentro": _seguir(
            "Con todo listo, la Guía Coral encendió una linterna grande: «¡A "
            "caminar!», anunció, y el grupo entero salió detrás de ella "
            "hacia el bosque.", "fogon"),
        "fogon": _seguir(
            "El sendero marcado los llevó entre árboles altos, con el sonido "
            "de grillos y hojas crujiendo bajo cada paso.", "canciones"),
        "canciones": _seguir(
            "En el camino, alguien empezó a tararear la canción del "
            "campamento, y de a poco todos se fueron sumando, bajito.",
            "cielo"),
        "cielo": _seguir(
            "Entre las copas de los árboles se veía un cielo lleno de "
            "estrellas, más claro y brillante que en cualquier otra noche "
            "del año.", "apagada"),
        "apagada": _seguir(
            "De repente, la linterna de la Guía Coral empezó a titilar y, "
            "con un último parpadeo, se apagó por completo.", "oscuridad"),
        "oscuridad": _seguir(
            "El grupo se quedó quieto un segundo en la oscuridad, hasta que "
            "los ojos se fueron acostumbrando a la luz de la luna.",
            "calma"),
        "calma": _seguir(
            "«Tranquilos», dijo la Guía Coral, «el bosque de noche tiene su "
            "propia luz, solo hay que aprender a mirarla».", "decision"),
        "decision": _decision(
            "«Podemos seguir las luciérnagas que se ven entre los "
            "arbustos, o guiarnos con las estrellas más brillantes del "
            "cielo». ¿Qué camino elegimos?",
            [("Seguir las luciérnagas ✨", "luciernagas_1"),
             ("Guiarse con las estrellas 🌟", "estrellas_1")]),

        # ── final luciérnagas (16-20) ──────────────────────────────────────
        "luciernagas_1": _seguir(
            "{nombre} notó las primeras luces chiquitas parpadeando entre "
            "los arbustos, como un camino de puntitos dorados.",
            "luciernagas_2"),
        "luciernagas_2": _seguir(
            "El grupo entero siguió el rastro de luciérnagas, que parecían "
            "flotar justo por donde tenían que caminar.", "luciernagas_3"),
        "luciernagas_3": _seguir(
            "Las luces los llevaron directo al claro secreto, donde ya se "
            "veía la silueta de un círculo de piedras para el fogón.",
            "luciernagas_4"),
        "luciernagas_4": _seguir(
            "{nombre} encendió el fogón con un fósforo largo, y el fuego "
            "prendió justo cuando la última luciérnaga se perdía entre los "
            "árboles.", "luciernagas_final"),
        "luciernagas_final": _final(
            "Alrededor del fuego, cantaron la canción de cierre bajo un "
            "cielo lleno de estrellas — {nombre} había guiado al campamento "
            "entero con la luz más pequeña del bosque.", "luciernagas"),

        # ── final estrellas (16-20) ─────────────────────────────────────────
        "estrellas_1": _seguir(
            "{nombre} miró hacia arriba y encontró la estrella más "
            "brillante de todas, justo sobre el árbol más alto del "
            "bosque.", "estrellas_2"),
        "estrellas_2": _seguir(
            "Caminando siempre hacia esa estrella, guió al grupo entre los "
            "troncos, con paso firme y seguro.", "estrellas_3"),
        "estrellas_3": _seguir(
            "La estrella los llevó justo al claro secreto, donde el círculo "
            "de piedras esperaba, listo para el fogón de cierre.",
            "estrellas_4"),
        "estrellas_4": _seguir(
            "La Guía Coral encendió el fuego con las ramas más secas, y las "
            "chispas subieron como si quisieran alcanzar las estrellas.",
            "estrellas_final"),
        "estrellas_final": _final(
            "Con la guitarra sonando y el fuego crepitando, {nombre} supo "
            "que había aprendido algo nuevo: el cielo también sabe guiar el "
            "camino a casa.", "estrellas"),
    },

    "construccion": {
        # COMPAÑERO RECURRENTE: el Ingeniero Bruno — aparece en hook, planos,
        # encargo, reencuentro, grua, viento, calma, decision, palanca_1,
        # palanca_final, equipo_1, equipo_final. Identificado solo por rol, sin
        # rasgo físico descrito.
        # ── espina compartida (1-4) ────────────────────────────────────────
        "hook": _seguir(
            "Esa mañana, el Ingeniero Bruno recibió a {nombre} en la obra con "
            "un casco amarillo: «Hoy inauguramos la plaza nueva, y todavía "
            "falta la pieza más grande», dijo, señalando un plano enorme.",
            "planos"),
        "planos": _seguir(
            "El plano mostraba una plaza con juegos, un puente de madera y "
            "una torre de mirador que todavía no estaba terminada.",
            "encargo"),
        "encargo": _seguir(
            "«Necesito ayuda con dos cosas antes de que llegue la grúa "
            "grande», dijo el Ingeniero Bruno, revisando una lista larga en "
            "una tablilla.", "bifurcacion"),
        "bifurcacion": _decision(
            "«Hay que pintar los juegos de colores, y ajustar los tornillos "
            "del puente de madera. ¿Con cuál empezamos?»",
            [("Pintar los juegos 🎨", "pintura_1"),
             ("Ajustar el puente de madera 🔧", "puente_1")]),

        # ── rama pintura (5-7) ────────────────────────────────────────────
        "pintura_1": _seguir(
            "{nombre} tomó un pincel grande y empezó a pintar el tobogán de "
            "un amarillo brillante, con cuidado de no manchar el piso.",
            "pintura_2"),
        "pintura_2": _seguir(
            "Los otros trabajadores pintaron las hamacas de rojo y azul, "
            "hasta que la plaza entera empezó a llenarse de color.",
            "pintura_3"),
        "pintura_3": _seguir(
            "Cuando terminaron, los juegos brillaban como nuevos bajo el "
            "sol de la mañana.", "reencuentro"),

        # ── rama puente (5-7) ─────────────────────────────────────────────
        "puente_1": _seguir(
            "{nombre} ayudó a revisar cada tabla del puente de madera, "
            "probando que ninguna se moviera al pisarla.", "puente_2"),
        "puente_2": _seguir(
            "Con una llave grande, ajustó tornillo por tornillo junto a un "
            "trabajador, hasta que el puente quedó firme y sin ruidos.",
            "puente_3"),
        "puente_3": _seguir(
            "{nombre} cruzó el puente de punta a punta para probarlo: ni un "
            "solo crujido, listo para todos los chicos de la plaza.",
            "reencuentro"),

        # ── espina compartida (8-15) ──────────────────────────────────────
        "reencuentro": _seguir(
            "El Ingeniero Bruno revisó su lista: «¡Excelente! Ya solo falta "
            "la torre de mirador», dijo, mirando hacia el cielo con la "
            "última pieza en camino.", "grua"),
        "grua": _seguir(
            "Una grúa enorme llegó despacio, cargando la pieza final: el "
            "techo puntiagudo de la torre de mirador, brillante y nuevo.",
            "publico"),
        "publico": _seguir(
            "Del otro lado de la plaza, las familias del barrio ya se "
            "juntaban para la inauguración, esperando ver la plaza "
            "terminada.", "viento"),
        "viento": _seguir(
            "Justo cuando la grúa levantaba el techo hacia lo más alto, un "
            "viento fuerte lo hizo balancearse peligrosamente en el aire.",
            "tension"),
        "tension": _seguir(
            "Todos contuvieron la respiración: el techo se mecía de un lado "
            "a otro, sin terminar de encajar en su lugar.", "calma"),
        "calma": _seguir(
            "El Ingeniero Bruno levantó una mano: «Despacio, sin apuro», "
            "dijo con voz tranquila, calculando el próximo movimiento.",
            "idea"),
        "idea": _seguir(
            "{nombre} miró la escena con atención: el techo necesitaba algo "
            "que lo sostuviera firme mientras encajaba en su lugar.",
            "decision"),
        "decision": _decision(
            "«Puedo intentar guiarlo con una palanca larga desde abajo, o "
            "podemos llamar a todo el equipo para sostenerlo entre todos». "
            "¿Qué hacemos?",
            [("Guiarlo con una palanca 🔩", "palanca_1"),
             ("Llamar a todo el equipo 👷", "equipo_1")]),

        # ── final palanca (16-20) ────────────────────────────────────────
        "palanca_1": _seguir(
            "{nombre} tomó una palanca larga de metal y la apoyó despacio "
            "contra la base del techo que se balanceaba.", "palanca_2"),
        "palanca_2": _seguir(
            "Con fuerza pareja, empujó apenas lo justo para que el techo "
            "dejara de mecerse y quedara derecho en el aire.", "palanca_3"),
        "palanca_3": _seguir(
            "El Ingeniero Bruno dio la señal a la grúa: «¡Ahora sí, bajalo "
            "despacio!», y el techo encajó perfecto en su lugar.",
            "palanca_4"),
        "palanca_4": _seguir(
            "Un aplauso espontáneo salió desde las familias que miraban "
            "todo desde la vereda, sorprendidas por la puntería de "
            "{nombre}.", "palanca_final"),
        "palanca_final": _final(
            "La torre de mirador quedó terminada, derecha y firme — gracias "
            "a una palanca bien usada y a un ayudante con mano segura.",
            "palanca"),

        # ── final equipo (16-20) ─────────────────────────────────────────
        "equipo_1": _seguir(
            "{nombre} corrió a juntar a todos los trabajadores disponibles: "
            "«¡Necesitamos manos firmes, ahora!», gritó fuerte.", "equipo_2"),
        "equipo_2": _seguir(
            "Uno por uno, formaron una fila debajo del techo, con los "
            "brazos listos para sostenerlo apenas bajara un poco más.",
            "equipo_3"),
        "equipo_3": _seguir(
            "Cuando la grúa lo bajó despacio, todos empujaron juntos, "
            "parejo, hasta que el techo encajó justo en su lugar.",
            "equipo_4"),
        "equipo_4": _seguir(
            "El Ingeniero Bruno miró la escena orgulloso: nunca había visto "
            "tantas manos trabajando juntas con tanta precisión.",
            "equipo_final"),
        "equipo_final": _final(
            "La torre de mirador quedó terminada justo a tiempo para la "
            "inauguración — no por una sola idea, sino por todo un equipo "
            "trabajando junto a {nombre}.", "equipo"),
    },

    "futbol": {
        # COMPAÑERO RECURRENTE: el Director Técnico Nando — aparece en hook,
        # vestuario, encargo, reencuentro, cancha, lesion, calma, decision,
        # aliento_1, aliento_final, jugada_1, jugada_final. Identificado solo
        # por rol, sin rasgo físico descrito.
        # ── espina compartida (1-4) ────────────────────────────────────────
        "hook": _seguir(
            "Esa tarde, {nombre} recibió una camiseta especial: «Ayudante "
            "Oficial del Equipo» para el Gran Partido de la final, esa misma "
            "noche en el estadio.", "vestuario"),
        "vestuario": _seguir(
            "En el vestuario, el Director Técnico Nando repasaba la "
            "formación en una pizarra, con flechas y nombres por todos "
            "lados.", "encargo"),
        "encargo": _seguir(
            "«Antes de salir a la cancha necesito ayuda con dos cosas», dijo "
            "el Director Técnico Nando, guardando la tiza en el bolsillo.",
            "bifurcacion"),
        "bifurcacion": _decision(
            "«Hay que ayudar al arquero a entrar en calor, y a los "
            "delanteros a practicar la jugada final. ¿Con quién vamos "
            "primero?»",
            [("Ir con el arquero 🧤", "arquero_1"),
             ("Ir con los delanteros ⚽", "delanteros_1")]),

        # ── rama arquero (5-7) ────────────────────────────────────────────
        "arquero_1": _seguir(
            "{nombre} le pateó pelotas suaves al arquero, una tras otra, "
            "mientras él las atajaba saltando de un palo al otro.",
            "arquero_2"),
        "arquero_2": _seguir(
            "«Necesito unos tiros más difíciles», pidió el arquero, "
            "estirando bien los brazos antes del partido.", "arquero_3"),
        "arquero_3": _seguir(
            "{nombre} pateó lo más fuerte que pudo hacia el ángulo, y el "
            "arquero voló para atajarla justo a tiempo.", "reencuentro"),

        # ── rama delanteros (5-7) ─────────────────────────────────────────
        "delanteros_1": _seguir(
            "{nombre} corrió junto a los delanteros, practicando pases "
            "cortos y rápidos de un lado a otro de la cancha.",
            "delanteros_2"),
        "delanteros_2": _seguir(
            "Ensayaron la jugada especial: un pase largo, una gambeta y un "
            "remate, una y otra vez hasta que salió perfecta.",
            "delanteros_3"),
        "delanteros_3": _seguir(
            "El equipo entero festejó cuando la pelota entró limpia en el "
            "arco, lista para intentarlo de verdad esa noche.",
            "reencuentro"),

        # ── espina compartida (8-15) ──────────────────────────────────────
        "reencuentro": _seguir(
            "Con todo listo, el equipo salió a la cancha entre aplausos: el "
            "estadio estaba completamente lleno para la gran final.",
            "cancha"),
        "cancha": _seguir(
            "El partido empezó parejo, con las dos hinchadas cantando fuerte "
            "desde las tribunas, todo el tiempo.", "primer_tiempo"),
        "primer_tiempo": _seguir(
            "Llegó el entretiempo con el marcador empatado, y el equipo "
            "volvió al vestuario respirando agitado pero con ánimo.",
            "lesion"),
        "lesion": _seguir(
            "El capitán del equipo entró rengueando, con el tobillo "
            "hinchado: se había torcido el pie en una jugada del primer "
            "tiempo.", "preocupacion"),
        "preocupacion": _seguir(
            "Todos se quedaron en silencio: sin el capitán, no sabían cómo "
            "iban a organizar la jugada final que tanto habían practicado.",
            "calma"),
        "calma": _seguir(
            "El Director Técnico Nando respiró hondo: «Tranquilos, todavía "
            "tenemos con qué», dijo, mirando al resto del equipo.",
            "idea"),
        "idea": _seguir(
            "{nombre} levantó la mano con una idea: había visto toda la "
            "práctica de la jugada especial, paso por paso.", "decision"),
        "decision": _decision(
            "«Puedo salir a la tribuna a levantar el ánimo de la hinchada, "
            "o puedo ayudarte a armar la jugada final desde el banco». "
            "¿Qué hacemos?",
            [("Salir a alentar a la hinchada 📣", "aliento_1"),
             ("Ayudar a armar la jugada 📋", "jugada_1")]),

        # ── final aliento (16-20) ──────────────────────────────────────────
        "aliento_1": _seguir(
            "{nombre} corrió hacia la tribuna con una bandera del equipo, "
            "agitándola fuerte para que todos la vieran.", "aliento_2"),
        "aliento_2": _seguir(
            "La hinchada entera se puso de pie, cantando más fuerte que "
            "nunca, contagiada por la energía de {nombre}.", "aliento_3"),
        "aliento_3": _seguir(
            "El equipo, desde la cancha, escuchó el canto crecer y salió al "
            "segundo tiempo con una energía renovada.", "aliento_4"),
        "aliento_4": _seguir(
            "Con la hinchada empujando cada jugada, el equipo encontró el "
            "gol de la victoria en el último minuto.", "aliento_final"),
        "aliento_final": _final(
            "Cuando sonó el pitazo final, el Director Técnico Nando abrazó "
            "a {nombre}: «Ese gol también fue tuyo, desde la tribuna».",
            "aliento"),

        # ── final jugada (16-20) ─────────────────────────────────────────
        "jugada_1": _seguir(
            "{nombre} se sentó junto al Director Técnico Nando y le mostró "
            "en la pizarra cada paso de la jugada especial, de memoria.",
            "jugada_2"),
        "jugada_2": _seguir(
            "Entre los dos armaron una variante nueva, pensada para un "
            "equipo sin el capitán en la cancha.", "jugada_3"),
        "jugada_3": _seguir(
            "El equipo salió al segundo tiempo con la jugada nueva bien "
            "aprendida, repitiéndola en la cabeza antes de intentarla.",
            "jugada_4"),
        "jugada_4": _seguir(
            "En el minuto final, la ejecutaron perfecta: pase largo, "
            "gambeta y gol — tal como {nombre} la había dibujado.",
            "jugada_final"),
        "jugada_final": _final(
            "El estadio explotó de festejo, y el Director Técnico Nando "
            "levantó a {nombre} en hombros: el verdadero armador de la "
            "jugada del campeonato.", "jugada"),
    },

    "monstruos": {
        # COMPAÑERO RECURRENTE: la Anfitriona Mona — aparece en hook, salon,
        # encargo, reencuentro, tambor, silencio, calma, decision, ritmo_1,
        # ritmo_final, palmas_1, palmas_final. Identificada solo por rol, sin
        # rasgo físico descrito.
        # ── espina compartida (1-4) ────────────────────────────────────────
        "hook": _seguir(
            "Esa noche era la Fiesta Monstruosa, la más grande del año, y la "
            "Anfitriona Mona recibió a {nombre} en la puerta con una invitación "
            "brillante: «¡Justo a tiempo, necesitamos una mano!»", "salon"),
        "salon": _seguir(
            "El salón entero estaba decorado con telarañas de colores y "
            "globos morados, pero todavía faltaban un montón de detalles "
            "antes de que llegaran los invitados.", "encargo"),
        "encargo": _seguir(
            "«Hay dos cosas urgentes», dijo la Anfitriona Mona, revisando una "
            "lista escrita con tinta violeta brillante.", "bifurcacion"),
        "bifurcacion": _decision(
            "«Hay que colgar las luces de telaraña por todo el salón, y "
            "preparar la gelatina morada gigante para la mesa dulce. "
            "¿Con cuál empezamos?»",
            [("Colgar las luces de telaraña 🕸️", "luces_1"),
             ("Preparar la gelatina morada 🍮", "gelatina_1")]),

        # ── rama luces (5-7) ──────────────────────────────────────────────
        "luces_1": _seguir(
            "{nombre} subió a una escalera y fue colgando las lucecitas "
            "moradas y verdes entre las telarañas de colores del techo.",
            "luces_2"),
        "luces_2": _seguir(
            "Un monstruito chiquito le alcanzaba cada cable desde abajo, "
            "saltando de la emoción con cada luz que se encendía.",
            "luces_3"),
        "luces_3": _seguir(
            "Cuando la última lucecita se encendió, el salón entero brilló "
            "como una noche estrellada, morada y verde.", "reencuentro"),

        # ── rama gelatina (5-7) ────────────────────────────────────────────
        "gelatina_1": _seguir(
            "{nombre} ayudó a mezclar la gelatina morada gigante en una "
            "olla enorme, revolviendo fuerte con una cuchara de madera.",
            "gelatina_2"),
        "gelatina_2": _seguir(
            "Le sumaron ojitos de caramelo flotando adentro, uno por uno, "
            "hasta que quedó bien monstruosa y divertida.", "gelatina_3"),
        "gelatina_3": _seguir(
            "La llevaron entre todos hasta la mesa dulce, temblorosa y "
            "brillante, lista para la fiesta.", "reencuentro"),

        # ── espina compartida (8-15) ──────────────────────────────────────
        "reencuentro": _seguir(
            "Con todo listo, la Anfitriona Mona aplaudió contenta: «¡Ya "
            "pueden entrar los invitados!», y la puerta se abrió de par en "
            "par.", "invitados"),
        "invitados": _seguir(
            "Monstruos de todos los tamaños y colores fueron llegando, "
            "riendo y saludando, llenando el salón de música y alboroto.",
            "tambor"),
        "tambor": _seguir(
            "En el centro, el Tambor Gigante marcaba el ritmo de la fiesta: "
            "todos bailaban al compás de sus latidos profundos.",
            "publico"),
        "publico": _seguir(
            "Los más chiquitos formaron una ronda alrededor del tambor, "
            "saltando cada vez que sonaba un golpe fuerte.", "silencio"),
        "silencio": _seguir(
            "De repente, el Tambor Gigante dejó de sonar: se le había roto "
            "la cuerda que sostenía el parche justo en medio del baile, y "
            "todos los monstruos se quedaron quietos, sin saber qué hacer.",
            "calma"),
        "calma": _seguir(
            "La Anfitriona Mona levantó las manos: «Tranquilos, una fiesta "
            "sin ritmo todavía puede encontrar el suyo», dijo con calma.",
            "idea"),
        "idea": _seguir(
            "{nombre} miró alrededor: había otras formas de hacer ritmo, "
            "sin necesitar el tambor roto.", "decision"),
        "decision": _decision(
            "«Puedo intentar arreglar el tambor con una cuerda nueva, o "
            "puedo enseñarle a todos un ritmo nuevo con las manos». "
            "¿Qué hacemos?",
            [("Arreglar el tambor 🥁", "ritmo_1"),
             ("Enseñar un ritmo con palmas 👏", "palmas_1")]),

        # ── final ritmo (16-20) ──────────────────────────────────────────
        "ritmo_1": _seguir(
            "{nombre} encontró una cuerda larga y trepó con cuidado hasta "
            "el borde del Tambor Gigante para atarla en su lugar.",
            "ritmo_2"),
        "ritmo_2": _seguir(
            "Con nudos firmes, fue tensando el parche de nuevo, probando "
            "el sonido con cada vuelta de cuerda.", "ritmo_3"),
        "ritmo_3": _seguir(
            "Al primer golpe, el tambor volvió a sonar profundo y fuerte, "
            "como si nunca se hubiera roto.", "ritmo_4"),
        "ritmo_4": _seguir(
            "Todos los monstruos festejaron con un grito enorme, volviendo "
            "a bailar al compás del tambor arreglado.", "ritmo_final"),
        "ritmo_final": _final(
            "La fiesta siguió hasta tarde, con {nombre} tocando el primer "
            "redoble del tambor arreglado — el héroe silencioso de la "
            "Fiesta Monstruosa.", "ritmo"),

        # ── final palmas (16-20) ─────────────────────────────────────────
        "palmas_1": _seguir(
            "{nombre} se subió a una silla y empezó a marcar un ritmo "
            "nuevo con las palmas: pam, pam-pam, pam.", "palmas_2"),
        "palmas_2": _seguir(
            "Un monstruito lo copió, después otro, hasta que el salón "
            "entero empezó a aplaudir el mismo compás.", "palmas_3"),
        "palmas_3": _seguir(
            "El ritmo de palmas creció tanto que hasta hacía temblar la "
            "gelatina morada de la mesa dulce.", "palmas_4"),
        "palmas_4": _seguir(
            "La Anfitriona Mona bailaba al frente, encantada con el nuevo "
            "ritmo inventado esa misma noche.", "palmas_final"),
        "palmas_final": _final(
            "Desde esa Fiesta Monstruosa en adelante, el ritmo de palmas "
            "de {nombre} quedó como tradición — más fuerte que cualquier "
            "tambor.", "palmas"),
    },

    "princesas": {
        # COMPAÑERO RECURRENTE: la Dama Elena — aparece en hook, jardin,
        # encargo, reencuentro, salon, nubes, calma, decision, interior_1,
        # interior_final, lluvia_1, lluvia_final. Identificada solo por rol,
        # sin rasgo físico descrito.
        # ── espina compartida (1-4) ────────────────────────────────────────
        "hook": _seguir(
            "Esa tarde llegó un pergamino sellado con cera dorada: {nombre} "
            "estaba invitado como Dama o Caballero de Honor al Gran Baile de "
            "esta noche en el castillo.", "jardin"),
        "jardin": _seguir(
            "En el jardín del castillo, la Dama Elena terminaba de acomodar "
            "guirnaldas de flores entre los rosales, apurada por el tiempo.",
            "encargo"),
        "encargo": _seguir(
            "«Necesito ayuda con dos cosas antes de que caiga la tarde», "
            "dijo la Dama Elena, con una canasta de flores en la mano.",
            "bifurcacion"),
        "bifurcacion": _decision(
            "«Hay que terminar de decorar el jardín con flores, y ayudar en "
            "la cocina real con el banquete. ¿Con cuál empezamos?»",
            [("Decorar el jardín 🌸", "jardin_1"),
             ("Ayudar en la cocina real 🍰", "cocina_1")]),

        # ── rama jardín (5-7) ──────────────────────────────────────────────
        "jardin_1": _seguir(
            "{nombre} fue colgando guirnaldas de flores entre los arcos de "
            "piedra, con pétalos rosados cayendo suavemente al piso.",
            "jardin_2"),
        "jardin_2": _seguir(
            "En el centro del jardín, armaron una fuente decorada con "
            "flores flotando, que brillaba bajo el sol de la tarde.",
            "jardin_3"),
        "jardin_3": _seguir(
            "El jardín entero quedó transformado, listo para recibir a "
            "todos los invitados del reino.", "reencuentro"),

        # ── rama cocina (5-7) ─────────────────────────────────────────────
        "cocina_1": _seguir(
            "{nombre} ayudó a decorar una torre de pasteles pequeños, cada "
            "uno con una flor de azúcar distinta encima.", "cocina_2"),
        "cocina_2": _seguir(
            "Entre todos armaron una fuente enorme de frutas brillantes, "
            "acomodadas en forma de corona real.", "cocina_3"),
        "cocina_3": _seguir(
            "El banquete quedó listo justo a tiempo, oliendo a vainilla y "
            "flores frescas por toda la cocina.", "reencuentro"),

        # ── espina compartida (8-15) ──────────────────────────────────────
        "reencuentro": _seguir(
            "La Dama Elena revisó todo con una sonrisa enorme: «¡El reino "
            "entero va a maravillarse esta noche!», dijo, mirando el "
            "jardín listo.", "salon"),
        "salon": _seguir(
            "Dentro del castillo, el Gran Salón brillaba con candelabros "
            "encendidos y una alfombra roja que llevaba hasta el trono.",
            "invitados"),
        "invitados": _seguir(
            "Los primeros invitados empezaron a llegar, vestidos de gala, "
            "riendo y saludando desde la entrada del jardín.", "nubes"),
        "nubes": _seguir(
            "De repente, unas nubes grises y espesas taparon el cielo "
            "sobre el jardín, justo cuando el baile estaba por empezar "
            "afuera.", "gotas"),
        "gotas": _seguir(
            "Cayeron las primeras gotas de lluvia sobre las flores del "
            "jardín, y los invitados miraron hacia arriba, preocupados.",
            "calma"),
        "calma": _seguir(
            "La Dama Elena respiró hondo: «Un poco de lluvia no va a "
            "arruinar esta noche», dijo, con una idea brillando en los "
            "ojos.", "idea"),
        "idea": _seguir(
            "{nombre} miró el jardín mojándose de a poco y el Gran Salón "
            "seco del otro lado — había dos formas de salvar el baile.",
            "decision"),
        "decision": _decision(
            "«Podemos mudar todo el baile adentro del Gran Salón, o armar "
            "un baile bajo la lluvia con paraguas para todos». ¿Qué "
            "hacemos?",
            [("Mudar el baile al Gran Salón 🏰", "interior_1"),
             ("Bailar bajo la lluvia con paraguas ☂️", "lluvia_1")]),

        # ── final interior (16-20) ──────────────────────────────────────
        "interior_1": _seguir(
            "{nombre} corrió a avisar a los músicos, que enseguida movieron "
            "sus instrumentos hacia el Gran Salón, sin perder el ritmo.",
            "interior_2"),
        "interior_2": _seguir(
            "Entre todos, trasladaron las guirnaldas de flores y las "
            "acomodaron alrededor de las columnas del salón.", "interior_3"),
        "interior_3": _seguir(
            "La fuente decorada quedó afuera, brillando bajo la lluvia, "
            "visible desde los ventanales altos del salón.", "interior_4"),
        "interior_4": _seguir(
            "Cuando la orquesta empezó a tocar, el Gran Salón se llenó de "
            "vueltas y risas, como si siempre hubiera sido ahí.",
            "interior_final"),
        "interior_final": _final(
            "El Gran Baile terminó siendo el más recordado del reino — "
            "gracias a un cambio de planes rápido y a un salón lleno de "
            "flores.", "interior"),

        # ── final lluvia (16-20) ─────────────────────────────────────────
        "lluvia_1": _seguir(
            "{nombre} corrió a buscar la canasta de paraguas de colores "
            "que se guardaba junto a la entrada del castillo.", "lluvia_2"),
        "lluvia_2": _seguir(
            "Repartió uno a cada invitado, y de a poco el jardín se llenó "
            "de paraguas abiertos, como flores gigantes de colores.",
            "lluvia_3"),
        "lluvia_3": _seguir(
            "La orquesta empezó a tocar bajo un toldo, y todos bailaron "
            "entre las gotas, riendo con cada salpicón.", "lluvia_4"),
        "lluvia_4": _seguir(
            "La Dama Elena giraba con su paraguas abierto, encantada con "
            "la idea de {nombre} de no cancelar nada.", "lluvia_final"),
        "lluvia_final": _final(
            "Esa noche quedó como la leyenda del Baile Bajo la Lluvia — el "
            "único del reino que ninguna nube pudo cancelar.", "lluvia"),
    },

    "superheroes": {
        # COMPAÑERO RECURRENTE: la Comandante Vela — aparece en hook, academia,
        # encargo, reencuentro, ceremonia, alarma, calma, decision, vuelo_1,
        # vuelo_final, cuerdas_1, cuerdas_final. Identificada solo por rol, sin
        # rasgo físico descrito.
        # ── espina compartida (1-4) ────────────────────────────────────────
        "hook": _seguir(
            "Esa noche era la Gran Graduación de Héroes, y {nombre} recibió "
            "una insignia especial: Aprendiz Honorario, válida por una sola "
            "noche en la Academia de Superhéroes.", "academia"),
        "academia": _seguir(
            "La Comandante Vela recibió a {nombre} en el patio de "
            "entrenamiento, donde los héroes hacían sus últimos ejercicios "
            "antes de la ceremonia.", "encargo"),
        "encargo": _seguir(
            "«Antes de la ceremonia hay dos entrenamientos por terminar», "
            "dijo la Comandante Vela, señalando dos grupos distintos.",
            "bifurcacion"),
        "bifurcacion": _decision(
            "«Podés entrenar con los héroes voladores, o con los héroes de "
            "fuerza. ¿Con cuál equipo querés empezar?»",
            [("Entrenar con los voladores 🦸", "vuelo_e1"),
             ("Entrenar con los de fuerza 💪", "fuerza_1")]),

        # ── rama voladores (5-7) ──────────────────────────────────────────
        "vuelo_e1": _seguir(
            "{nombre} practicó planeos cortos entre dos plataformas, "
            "sostenido con cuidado por un héroe volador que lo guiaba de "
            "cerca.", "vuelo_e2"),
        "vuelo_e2": _seguir(
            "Aprendió a leer el viento antes de cada salto, sintiendo "
            "hacia dónde soplaba con la mano abierta.", "vuelo_e3"),
        "vuelo_e3": _seguir(
            "En el último ejercicio, planeó solo de una plataforma a otra, "
            "aterrizando derecho entre aplausos.", "reencuentro"),

        # ── rama fuerza (5-7) ─────────────────────────────────────────────
        "fuerza_1": _seguir(
            "{nombre} practicó a levantar cajas de entrenamiento cada vez "
            "más pesadas, junto a un héroe de fuerza que le enseñaba la "
            "postura correcta.", "fuerza_2"),
        "fuerza_2": _seguir(
            "Aprendió que la fuerza de verdad también es saber pedir ayuda "
            "para levantar algo entre varios.", "fuerza_3"),
        "fuerza_3": _seguir(
            "En equipo, levantaron una plataforma de entrenamiento entera, "
            "todos empujando parejo al mismo tiempo.", "reencuentro"),

        # ── espina compartida (8-15) ──────────────────────────────────────
        "reencuentro": _seguir(
            "Con los entrenamientos terminados, la Comandante Vela llamó a "
            "todos al patio central: «¡Es hora de la ceremonia!», anunció "
            "con orgullo.", "ceremonia"),
        "ceremonia": _seguir(
            "Los héroes graduados formaron una fila, con sus capas "
            "brillando bajo las luces de la Academia.", "publico"),
        "publico": _seguir(
            "Las familias de todo el barrio se juntaron a mirar desde las "
            "gradas, aplaudiendo cada nombre que se anunciaba.", "alarma"),
        "alarma": _seguir(
            "De repente, una alarma sonó fuerte: un globo gigante del "
            "festival de la ciudad se había soltado de sus cuerdas y "
            "flotaba sin control.", "tension"),
        "tension": _seguir(
            "El globo, enorme y brillante, se acercaba cada vez más a los "
            "cables de luz del barrio, arrastrado por el viento.",
            "calma"),
        "calma": _seguir(
            "La Comandante Vela no perdió la calma: «Tenemos justo el "
            "equipo entrenado para esto», dijo, mirando a {nombre}.",
            "idea"),
        "idea": _seguir(
            "{nombre} recordó todo lo aprendido esa tarde: había dos formas "
            "de resolver esto, cada una con su propio equipo.", "decision"),
        "decision": _decision(
            "«Podés volar a buscar el globo con el equipo volador, o "
            "ayudar a sujetar las cuerdas desde el suelo con el equipo de "
            "fuerza». ¿Qué hacemos?",
            [("Volar a buscar el globo 🎈", "vuelo_1"),
             ("Sujetar las cuerdas desde el suelo 🪢", "cuerdas_1")]),

        # ── final vuelo (16-20) ────────────────────────────────────────────
        "vuelo_1": _seguir(
            "{nombre} se elevó junto a los héroes voladores, planeando "
            "directo hacia el globo gigante que se alejaba en el cielo.",
            "vuelo_2"),
        "vuelo_2": _seguir(
            "Con cuidado, alcanzó una de las cuerdas sueltas y la sostuvo "
            "firme, sintiendo el tirón del viento.", "vuelo_3"),
        "vuelo_3": _seguir(
            "Entre todos los voladores, guiaron el globo despacio de "
            "vuelta hacia la plaza del festival.", "vuelo_4"),
        "vuelo_4": _seguir(
            "Lo bajaron justo en el centro de la plaza, entre gritos de "
            "alegría de todo el público.", "vuelo_final"),
        "vuelo_final": _final(
            "La Comandante Vela le prendió a {nombre} una capa de verdad: "
            "«Primera misión cumplida, desde el cielo».", "vuelo"),

        # ── final cuerdas (16-20) ─────────────────────────────────────────
        "cuerdas_1": _seguir(
            "{nombre} corrió con el equipo de fuerza hacia donde el globo "
            "arrastraba una cuerda larga por el piso.", "cuerdas_2"),
        "cuerdas_2": _seguir(
            "Todos juntos tomaron la cuerda con fuerza, plantando bien los "
            "pies para no dejarse arrastrar por el viento.", "cuerdas_3"),
        "cuerdas_3": _seguir(
            "Con un tirón parejo y coordinado, fueron bajando el globo "
            "centímetro a centímetro hacia la plaza.", "cuerdas_4"),
        "cuerdas_4": _seguir(
            "El globo tocó el piso suavemente, justo antes de llegar a los "
            "cables de luz del barrio.", "cuerdas_final"),
        "cuerdas_final": _final(
            "La Comandante Vela le prendió a {nombre} una capa de verdad: "
            "«Primera misión cumplida, con los pies bien puestos en el "
            "suelo».", "cuerdas"),
    },

    "un-espacio-de-locura": {
        # COMPAÑERO RECURRENTE: la Comandante Estela — aparece en hook,
        # estacion, encargo, reencuentro, cupula, parpadeo, calma, decision,
        # cables_1, cables_final, funcion_1, funcion_final. Identificada solo
        # por rol, sin rasgo físico descrito.
        # ── espina compartida (1-4) ────────────────────────────────────────
        "hook": _seguir(
            "Esa noche era la Gran Lluvia de Estrellas, y {nombre} recibió "
            "un traje de Astronauta Junior para ayudar en la estación "
            "espacial durante el espectáculo.", "estacion"),
        "estacion": _seguir(
            "La Comandante Estela recibió a {nombre} flotando suavemente "
            "en la cúpula de observación, con las estrellas ya asomando "
            "afuera.", "encargo"),
        "encargo": _seguir(
            "«Antes de que empiece la lluvia de estrellas, hay dos cosas "
            "por preparar», dijo la Comandante Estela, revisando un "
            "panel de controles.", "bifurcacion"),
        "bifurcacion": _decision(
            "«Hay que calibrar el telescopio grande, y preparar el mapa "
            "de estrellas para mostrarles a los visitantes. ¿Con cuál "
            "empezamos?»",
            [("Calibrar el telescopio 🔭", "telescopio_1"),
             ("Preparar el mapa de estrellas 🗺️", "mapa_1")]),

        # ── rama telescopio (5-7) ──────────────────────────────────────────
        "telescopio_1": _seguir(
            "{nombre} ayudó a girar el telescopio gigante hacia el punto "
            "exacto del cielo donde caerían las primeras estrellas.",
            "telescopio_2"),
        "telescopio_2": _seguir(
            "Ajustó cada lente con cuidado, hasta que la imagen se vio "
            "clara y brillante en la pantalla de la cúpula.", "telescopio_3"),
        "telescopio_3": _seguir(
            "El telescopio quedó listo, apuntando derecho hacia donde "
            "empezaría el espectáculo.", "reencuentro"),

        # ── rama mapa (5-7) ────────────────────────────────────────────────
        "mapa_1": _seguir(
            "{nombre} ayudó a desplegar un mapa de estrellas gigante, "
            "brillante en la oscuridad de la sala de proyecciones.",
            "mapa_2"),
        "mapa_2": _seguir(
            "Marcó cada constelación con una lucecita de color, "
            "practicando cómo señalarlas para los visitantes.", "mapa_3"),
        "mapa_3": _seguir(
            "El mapa quedó completo, listo para guiar a todos durante la "
            "lluvia de estrellas.", "reencuentro"),

        # ── espina compartida (8-15) ──────────────────────────────────────
        "reencuentro": _seguir(
            "Con todo listo, la Comandante Estela abrió las compuertas de "
            "la cúpula: «¡Que empiece el espectáculo!», anunció con "
            "emoción.", "cupula"),
        "cupula": _seguir(
            "Familias enteras llegaron flotando despacio hasta la cúpula, "
            "mirando hacia arriba con los ojos bien abiertos.", "visitantes"),
        "visitantes": _seguir(
            "Las primeras estrellas fugaces empezaron a cruzar el cielo, "
            "una tras otra, entre exclamaciones de sorpresa.", "parpadeo"),
        "parpadeo": _seguir(
            "De repente, las luces de la cúpula empezaron a parpadear, y "
            "la pantalla del telescopio se apagó por completo.", "sorpresa"),
        "sorpresa": _seguir(
            "Un cable se había soltado en algún panel, justo en medio del "
            "mejor momento de la lluvia de estrellas.", "calma"),
        "calma": _seguir(
            "La Comandante Estela respiró tranquila: «No es grave, "
            "tenemos con qué resolverlo», dijo, mirando los paneles de "
            "control.", "idea"),
        "idea": _seguir(
            "{nombre} miró la cúpula a oscuras y a los visitantes "
            "esperando — había dos formas de salvar el espectáculo.",
            "decision"),
        "decision": _decision(
            "«Puedo ir a revisar los cables sueltos en el panel de "
            "control, o puedo mantener a los visitantes entretenidos con "
            "una función de luces mientras se arregla». ¿Qué hacemos?",
            [("Revisar los cables 🔌", "cables_1"),
             ("Armar una función de luces ✨", "funcion_1")]),

        # ── final cables (16-20) ─────────────────────────────────────────
        "cables_1": _seguir(
            "{nombre} se deslizó junto a la Comandante Estela hasta el "
            "panel de control, siguiendo cada cable con la mirada.",
            "cables_2"),
        "cables_2": _seguir(
            "Encontró el cable suelto, escondido detrás de una placa "
            "metálica, y lo sostuvo firme mientras la Comandante lo "
            "conectaba.", "cables_3"),
        "cables_3": _seguir(
            "Con un clic, las luces de la cúpula volvieron todas juntas, "
            "más brillantes que antes.", "cables_4"),
        "cables_4": _seguir(
            "La pantalla del telescopio se encendió justo a tiempo para "
            "mostrar la estrella fugaz más grande de la noche.",
            "cables_final"),
        "cables_final": _final(
            "Los visitantes aplaudieron sin saber lo que había pasado "
            "detrás de escena — pero la Comandante Estela sí, y le dio a "
            "{nombre} el título de Ingeniero Estelar.", "cables"),

        # ── final función (16-20) ─────────────────────────────────────────
        "funcion_1": _seguir(
            "{nombre} tomó unas luces portátiles y empezó a dibujar formas "
            "en el aire oscuro de la cúpula: espirales, estrellas, "
            "cometas.", "funcion_2"),
        "funcion_2": _seguir(
            "Los chicos más chiquitos se acercaron encantados, siguiendo "
            "cada movimiento de luz con los ojos bien abiertos.",
            "funcion_3"),
        "funcion_3": _seguir(
            "Entre risas y aplausos, nadie notó cuánto tiempo pasó hasta "
            "que las luces de la cúpula volvieron de golpe.", "funcion_4"),
        "funcion_4": _seguir(
            "El telescopio se encendió otra vez, justo para la parte más "
            "brillante de la lluvia de estrellas.", "funcion_final"),
        "funcion_final": _final(
            "La Comandante Estela se acercó sonriendo: «Mientras "
            "arreglábamos todo, vos armaste tu propio espectáculo» — le "
            "dijo, entregándole el título de Ingeniero Estelar.",
            "funcion"),
    },
}

INICIO = "hook"


def temas_disponibles():
    return sorted(AVENTURAS)


def _imagen_archivo(tema, nodo_id):
    """nodo_id -> nombre de archivo dentro de overrides/aventura/ (ilustración PROPIA
    del nodo, generada por aventura_ia.py). Si todavía no se generó, cae a un
    placeholder reciclado del libro lineal (arte genérico del tema) — no debería
    pasar para safari, que ya tiene arte propio en los 28 nodos."""
    p = os.path.join(_temas.TEMAS_DIR, tema, "overrides", "aventura", f"{nodo_id}.png")
    if os.path.isfile(p):
        return f"{nodo_id}.png"
    return "libro-2.png"  # placeholder genérico (portada/escena 1 del libro del tema)


def grafo(tema, nombre="", genero=None):
    """Arma el grafo de nodos con el {nombre} ya reemplazado y el archivo de imagen
    resuelto. `genero` no afecta la ilustración todavía (el arte propio de cada nodo
    usa un protagonista neutro/de espaldas) — queda como posible mejora futura."""
    nodos = AVENTURAS.get(tema)
    if not nodos:
        return None
    out = {}
    for nid, n in nodos.items():
        out[nid] = {
            "texto": n["texto"].format(nombre=nombre or "el explorador"),
            "imagen": _imagen_archivo(tema, nid),
            "opciones": n.get("opciones", []),
            "final": n.get("final"),
        }
    return out
