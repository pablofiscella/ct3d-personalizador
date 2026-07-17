# -*- coding: utf-8 -*-
"""Catálogo de historias de los audiolibros (versión larga, 17 páginas).

Cada arco es una lista de 17 textos-plantilla que usan los placeholders del tema:
{nombre} {mundo} {amigos} {conteo} {conteo_num} {tesoro} {desafio} {solucion}.

El largo se elige por EDAD (ver libro.paginas_historia):
  - 4 años o más  -> 17 páginas de historia (20 en total)  -> arco completo
  - hasta 3 años  -> 9 páginas de historia (12 en total)   -> subconjunto CORTO_IDX

REGLAS DE DISEÑO de los arcos (ver skill armar-audiolibros):
  1. MISIÓN CON HILO: cada arco plantea una misión concreta al principio y la
     resuelve en el clímax — las últimas páginas NUNCA son relleno genérico.
  2. ESQUELETO común (índices 0..16):
       0 gancho · 1 transición ({conteo}) · 2 llegada · 3 MISIÓN revelada ·
       4 apuesta/plan · 5 viaje · 6 obstáculo (a veces {desafio}) · 7 idea ·
       8 acción/{solucion} · 9-10 desarrollo · 11 CLÍMAX (misión cumplida) ·
       12-13 festejo/cierre emocional · 14 despedida + {tesoro} ·
       15 de vuelta en la cama (con un recuerdo sensorial) · 16 sueño + moraleja.
  3. VERSIÓN CORTA COHERENTE: las páginas de CORTO_IDX [0,1,3,6,8,11,14,15,16]
     tienen que leerse de corrido SIN las intermedias: nada de antecedentes que
     solo aparezcan en páginas salteadas ("del otro lado", "cuando volvieron").
  4. GÉNERO NEUTRO: el texto sirve para nene y nena — prohibidos «él/ella»,
     clíticos «lo/la» referidos a {nombre}, y adjetivos que concuerden con el
     protagonista (contento, solo, emocionado...). «feliz» y «con una sonrisa» sí.
  5. SIN CONCORDAR CON {mundo}: nunca "todo {mundo}" ni adjetivos pegados
     ("{mundo} iluminado"); usar aposición ("un lugar más mágico...") o verbos
     sin concordancia ("{mundo} volvió a estar en paz").
  6. UNIVERSAL: nada atado a una temática (ni árbol, ni río, ni sabana) fuera de
     los placeholders — acciones físicas genéricas ("lo más alto de {mundo}",
     "un tramo angosto", "lucecitas brillantes").
  7. MORALEJA ÚNICA por arco (así dos libros de la misma casa no se repiten).
  8. Apto TTS página por página: 60-210 caracteres, sin puntuación decorativa.

Están desacopladas del tema: cualquier tema puede usar cualquier historia.
El texto de cada página se capitaliza automáticamente en libro.cuento (por si un
placeholder como {amigos} cae al comienzo de una oración).
"""

# Índices (0..16) que se conservan en la versión corta (hasta 3 años): mantienen
# gancho, misión, obstáculo, solución, clímax, regalo y SIEMPRE el cierre.
CORTO_IDX = [0, 1, 3, 6, 8, 11, 14, 15, 16]

# Título de tapa/visor/narración por historia (cada libro con SU título — no
# todos "La gran aventura"). Tienen que coincidir con los labels de la tienda.
TITULOS = {
    "aventura": "La invitación mágica",
    "tesoro": "El mapa del tesoro",
    "rescate": "El gran rescate",
    "gran-dia": "El gran día",
    "noche-estrellas": "La noche de las estrellas",
    "cumple-sorpresa": "El cumpleaños sorpresa",
    "pequeno-maestro": "El pequeño maestro",
    "ayudar-a-todos": "El día de ayudar a todos",
    "gran-viaje": "La entrega importante",
    "manos-a-la-obra": "El rincón soñado",
    "gran-torneo": "Los Grandes Juegos",
}

ARGUMENTOS_LARGO = {
    # ------------------------------------------------- aventura (El Farol)
    "aventura": [
        "Esta noche, antes de dormir, {nombre} encontró una invitación brillante "
        "debajo de la almohada. Decía: «Te esperamos en {mundo}».",
        "Con el corazón lleno de curiosidad, {nombre} cerró los ojos y empezó a "
        "{conteo}. ¡De golpe la habitación se llenó de luces de colores!",
        "Cuando las luces se apagaron, {nombre} ya no estaba en su cuarto: había "
        "llegado a {mundo}, un lugar más grande y más mágico de lo que imaginaba.",
        "{amigos} le dieron la bienvenida con una fiesta, pero enseguida le "
        "contaron un secreto: el gran farol que ilumina {mundo} se había apagado.",
        "«Sin ese farol», le explicaron, «esta noche no se termina más y nadie "
        "puede volver a su casa». {nombre} decidió ayudarlos a encenderlo.",
        "El camino al farol cruzaba un tramo angosto y oscuro. {nombre} fue "
        "adelante con paso firme, guiando a todos, pasito a pasito.",
        "Pero a mitad del camino apareció un problema: {desafio}. Nadie sabía "
        "qué hacer... nadie, excepto {nombre}.",
        "{nombre} respiró hondo, miró bien a su alrededor y sintió una idea "
        "encenderse, chiquita y valiente como una chispa.",
        "Con valentía y una gran sonrisa, {nombre} {solucion}. ¡Y el camino al "
        "farol quedó libre!",
        "El farol esperaba en lo más alto de {mundo}, allá arriba de todo. Entre "
        "todos armaron una torre de amigos para que {nombre} subiera.",
        "Arriba había una sorpresa: el farol no estaba roto. Solo le faltaba una "
        "chispa de valentía para volver a brillar.",
        "{nombre} sopló despacito, con todo su cariño... y el farol se encendió, "
        "llenando {mundo} de una luz dorada y tibia.",
        "Con la luz de vuelta, {amigos} encontraron por fin el camino a casa, "
        "que había estado escondido en la oscuridad.",
        "Antes de bajar, {nombre} guardó una chispita del farol en la mano, bien "
        "cerradita, por si alguna otra noche alguien la necesitaba.",
        "{amigos} acompañaron a {nombre} hasta la puerta de luz y le regalaron "
        "{tesoro}, para que nunca le faltara luz propia.",
        "De vuelta en su cama, {nombre} abrió la mano despacito: la chispita "
        "seguía ahí, brillando bajito.",
        "Y se durmió con una sonrisa. Porque quien es valiente y ayuda a los "
        "demás, siempre lleva una luz que no se apaga.",
    ],
    # ------------------------------------------- tesoro (El cofre de tres llaves)
    "tesoro": [
        "Esa mañana, {nombre} encontró un mapa antiguo enrollado en la mochila. "
        "Marcaba un camino secreto hacia {mundo}, ¡y un tesoro escondido al final!",
        "Al seguir la primera pista y {conteo}, el mapa empezó a brillar entre "
        "sus manos. ¡La búsqueda del tesoro había comenzado!",
        "El camino brillante llevó a {nombre} directo a {mundo}, donde todo "
        "parecía guardar un secreto esperando ser descubierto.",
        "{amigos} ya estaban esperando con los ojos brillantes: cada uno conocía "
        "un pedacito del camino, pero nadie había visto nunca el tesoro. "
        "¡Irían todos juntos!",
        "La primera pista los llevó a un rincón escondido de {mundo}: había que "
        "encontrar la única lucecita con forma de estrella. Y {nombre} la encontró.",
        "Al tocarla, apareció una llave dorada y una puerta secreta. Era "
        "pesadísima: la empujaron entre todos, contando hasta tres... ¡y se abrió!",
        "El camino los llevó hasta un pasillo oscuro y lleno de ecos. Y justo "
        "ahí, el último obstáculo: {desafio}. Nadie sabía qué hacer... nadie, "
        "excepto {nombre}.",
        "{nombre} cerró los ojos un momentito, pensó en todo lo aprendido en el "
        "camino... y sonrió: tenía una idea.",
        "Con una gran sonrisa, {nombre} {solucion}. Y al fondo del pasillo "
        "apareció, por fin, un cofre dorado.",
        "El cofre tenía tres cerraduras brillantes. {nombre} descubrió el "
        "secreto: había que girarlas todas a la vez, con manos amigas ayudando.",
        "Contaron hasta tres y giraron juntos. Clic, clic, clic...",
        "¡El cofre se abrió de golpe, irradiando luz! Adentro brillaba {tesoro}, "
        "que esperaba hacía cien años a alguien con un corazón valiente.",
        "Justo entonces, el mapa se dio vuelta solito: ¡tenía una segunda cara! "
        "Mostraba un atajo secreto para volver a casa.",
        "El más sabio de {amigos} les contó: «Cuiden bien ese tesoro, y el mapa "
        "les mostrará siempre una aventura nueva».",
        "{amigos} acompañaron a {nombre} hasta la salida de {mundo}, prometiendo "
        "cuidar el escondite del cofre hasta la próxima visita.",
        "De vuelta en casa, {nombre} guardó el mapa debajo de la almohada, "
        "todavía tibio de tanta aventura.",
        "Y se durmió pensando en la próxima pista. Porque los mejores tesoros "
        "se encuentran con paciencia y buenos amigos.",
    ],
    # ---------------------------------------------- rescate (El amiguito perdido)
    "rescate": [
        "Una noche, una lucecita golpeó la ventana de {nombre}: era un mensaje "
        "urgente desde {mundo}. ¡Necesitaban ayuda, rápido!",
        "{nombre} no lo dudó: cerró los ojos, empezó a {conteo}... y en un abrir "
        "y cerrar de ojos ya estaba volando hacia {mundo}.",
        "Al llegar, la noche estaba cerquita: el sol se escondía y las primeras "
        "sombras se estiraban por {mundo}.",
        "{amigos} estaban muy asustados: el amiguito más pequeño de {mundo} se "
        "había perdido, y de noche iba a tener frío.",
        "Todos hablaban a la vez, nerviosos. {nombre} pidió calma: «Busquemos "
        "sus huellas antes de que oscurezca del todo».",
        "Buscaron por todos lados con la linterna, hasta que {nombre} encontró "
        "la primera pista en el camino: ¡huellas chiquititas!",
        "Siguiendo las huellas chiquititas, llegaron a un tramo angosto que se "
        "hamacaba con el viento. {nombre} pasó primero, despacito, y los demás "
        "cruzaron detrás.",
        "Del otro lado, las huellas desaparecían. Todos se miraron sin saber "
        "seguir... hasta que {nombre} escuchó un llantito bajito, muy cerquita.",
        "El llantito venía de una cuevita oscura. {nombre} entró con la linterna "
        "y ahí estaba el pequeño, con frío y un poquito de miedo. «Vine a "
        "buscarte. Ya estás a salvo».",
        "Salieron de la cuevita de la mano. Pero afuera ya era noche cerrada, y "
        "el camino de vuelta no se veía por ningún lado.",
        "Entonces {nombre} tuvo una idea: llamó a las lucecitas brillantes de la "
        "noche, y entre todas armaron un caminito de luz.",
        "Las lucecitas alumbraron el camino, y así llevaron al pequeño de vuelta "
        "a su casa. {amigos} los recibieron con una manta calentita y saltos de "
        "alegría.",
        "«¡Gracias, {nombre}!», decían todos. El pequeño, ya calentito, pidió "
        "una promesa: «¿Volvés a jugar conmigo?». Y {nombre} dijo que sí, mil "
        "veces sí.",
        "Esa noche hubo festejo en {mundo}: cantaron bajito alrededor de las "
        "lucecitas, felices de estar todos juntos otra vez.",
        "Antes de la despedida, {amigos} le entregaron a {nombre} {tesoro}: la "
        "marca de los héroes de {mundo}.",
        "De vuelta en su cama, {nombre} todavía tenía las manos tibias de tanto "
        "abrazo.",
        "Y se durmió con una sonrisa gigante. Porque ayudar a un amigo es la "
        "aventura más importante de todas.",
    ],
    # ------------------------------------------- gran-dia (La torre de luces)
    "gran-dia": [
        "¡Llegó una noticia increíble! En {mundo} se preparaba la Gran Fiesta "
        "del año, y {amigos} mandaron a pedir una ayuda muy especial: ¡la de "
        "{nombre}!",
        "{nombre} preparó la mochila, contó hasta {conteo_num} para darse "
        "valor... ¡y salió rumbo a {mundo}!",
        "Al llegar, todo era movimiento: guirnaldas por acá, música por allá y "
        "un gran desfile ensayando. ¡Faltaba poquito para la fiesta!",
        "A {nombre} le dieron la tarea más importante de todas: encender la "
        "torre de luces que abría la Gran Fiesta.",
        "Practicaron toda la tarde entre risas, hasta que cada cosa salía "
        "redondita y hermosa.",
        "Pero el cielo se puso gris de golpe, y unas nubes enormes empezaron a "
        "dar vueltas sobre la fiesta. Todos miraron para arriba, preocupados.",
        "¡De pronto, una tormenta! El viento se llevó las guirnaldas y apagó la "
        "torre de luces. Algunos querían rendirse, pero {nombre} dijo bajito: "
        "«Todavía podemos arreglarlo... si lo hacemos juntos».",
        "{nombre} organizó los equipos: unos ataban las guirnaldas, otros "
        "secaban el escenario, otros juntaban las luces caídas.",
        "De a poco, entre todos, la fiesta volvió a armarse, ¡todavía más linda "
        "que antes de la tormenta!",
        "Pero quedaba un problema: la torre de luces no prendía. Se había "
        "mojado con la lluvia, y sin ella la fiesta no podía empezar.",
        "Entonces {nombre} tuvo una idea genial: ¡llenaron la torre de "
        "lucecitas brillantes y velitas de colores!",
        "Cuando el cielo se despejó, {nombre} encendió la torre ante todos... "
        "¡y brillaba más lindo que nunca! La Gran Fiesta había comenzado.",
        "Hubo música, baile y una torta gigante, y todos decían que era la "
        "mejor fiesta de la historia de {mundo}.",
        "«¡Y casi se arruina!», se reían {amigos}. «Menos mal que {nombre} "
        "nunca se rinde».",
        "En agradecimiento por salvar el gran día, {amigos} le entregaron a "
        "{nombre} {tesoro}, y le guardaron un lugar para la próxima fiesta.",
        "De vuelta en su cama, a {nombre} todavía le sonaban en los oídos la "
        "música y las risas.",
        "Y se durmió feliz. Porque los grandes días se construyen entre todos, "
        "con manos que ayudan.",
    ],
    # -------------------------------------- noche-estrellas (La estrella caída)
    "noche-estrellas": [
        "Esa noche, {nombre} no podía dormir. Daba vueltas en la cama mirando "
        "el techo, con los ojos bien abiertos y ni una pizca de sueño.",
        "De repente, por la ventana, vio caer una estrella fugaz que se perdió "
        "justo detrás de {mundo}. {nombre} se puso las pantuflas y salió a "
        "buscarla, contando los pasos hasta {conteo_num}.",
        "Apenas cruzó la puerta, {nombre} apareció en {mundo}, bajo un cielo "
        "enorme lleno de estrellas que titilaban como haciéndole cosquillas a "
        "la noche.",
        "{amigos} esperaban con carita triste: sin esa estrella, el cielo de "
        "{mundo} había quedado con un hueco oscuro y frío.",
        "«Si no la ayudamos a volver antes del amanecer», dijeron, «el hueco va "
        "a crecer y se van a apagar las demás». ¡Había que apurarse!",
        "Se pusieron en marcha siguiendo el último resplandor, que brillaba "
        "bajito a lo lejos, como pidiendo ayuda.",
        "El camino estaba tan oscuro que no se veía nada. {nombre} llamó a las "
        "lucecitas brillantes de la noche y les pidió que alumbraran. "
        "¡Aceptaron encantadas!",
        "Cruzaron colinas dormidas y rincones calladitos, cada vez más cerca "
        "del resplandor.",
        "Y ahí estaba: la estrella, en el suelo, chiquita y apagada, llorando "
        "lágrimas de luz. «Me caí y no sé cómo volver», susurró.",
        "{nombre} la abrazó despacito. «No estás sola. Te vamos a llevar de "
        "vuelta a tu lugar, arriba de todo».",
        "Pero la estrella estaba muy débil para volar. Entonces {nombre} tuvo "
        "una idea: «¡Regalémosle un deseo cada uno, para devolverle el brillo!».",
        "Uno a uno le regalaron deseos, y con cada deseo la estrella brillaba "
        "más fuerte. El último fue el de {nombre}... ¡y la estrella se encendió "
        "de golpe, radiante!",
        "Ya con toda su luz, se elevó como un globo dorado y voló derechito a "
        "tapar el hueco del cielo. La noche entera volvió a brillar.",
        "{amigos} festejaron mirando para arriba: el cielo de {mundo} estaba "
        "otra vez completito, sin ningún hueco.",
        "Desde su lugar en el cielo, la estrella le mandó a {nombre} un último "
        "destello con {tesoro} adentro, y le dijo: «Cada vez que no puedas "
        "dormir, buscame: ahí voy a estar».",
        "De vuelta en su cama, {nombre} miró por la ventana y la encontró "
        "enseguida, titilando justo sobre su casa.",
        "Y se durmió en paz, con una sonrisa. Porque desde esa noche, una amiga "
        "del cielo le cuida los sueños.",
    ],
    # ------------------------------------- cumple-sorpresa (La misión secreta)
    "cumple-sorpresa": [
        "{nombre} descubrió un secreto: ¡al día siguiente era el cumpleaños de "
        "su mejor amigo de {mundo}, y nadie se había dado cuenta!",
        "Con el corazón a mil, {nombre} empezó a {conteo} para calmar los "
        "nervios, y armó el plan más secreto de todos: ¡una fiesta sorpresa!",
        "Llegó a {mundo} en puntitas de pie, mirando para todos lados, cuidando "
        "que el cumpleañero no sospechara nada.",
        "{nombre} reunió a {amigos} y les contó la misión en voz bajita: "
        "«Mañana es su cumpleaños. ¡Vamos a prepararle la sorpresa más linda "
        "de {mundo}!».",
        "Se repartieron las tareas: unos buscaban los globos, otros preparaban "
        "la torta... y {nombre} cuidaba el secreto, que era lo más difícil.",
        "Escondieron todo por los rincones de {mundo}, sin hacer ni un "
        "ruidito, aguantándose la risa.",
        "Pero de pronto apareció un problema: {desafio}. ¡El plan entero estaba "
        "en peligro! Nadie sabía qué hacer... nadie, excepto {nombre}.",
        "{nombre} respiró hondo. Si no lo resolvían rapidito, ¡adiós fiesta "
        "sorpresa!",
        "{nombre} pensó rápido y {solucion}, salvando el plan justo a tiempo.",
        "Justo entonces apareció el cumpleañero, con carita triste: creía que "
        "nadie se había acordado de su día.",
        "{nombre} disimuló y lo invitó a dar un paseo largo, mientras {amigos} "
        "terminaban de decorar a toda velocidad.",
        "Esa tarde, cuando el cumpleañero se acercó al lugar de la fiesta, todo "
        "estaba oscuro y calladito. Dio un pasito... y de repente: "
        "«¡SORPRESA!». Se encendieron mil lucecitas.",
        "El cumpleañero no lo podía creer: ¡sí se habían acordado! Se le "
        "llenaron los ojos de lágrimas, de las lindas.",
        "Bailaron, jugaron y comieron torta hasta que salió la luna, y el "
        "cumpleañero se quedó pegadito a {nombre} toda la noche.",
        "Antes de la despedida, el cumpleañero le regaló a {nombre} {tesoro} y "
        "le dijo: «Gracias por acordarte de mí. Esto es para vos».",
        "De vuelta en casa, {nombre} se metió en la cama con el gorrito de "
        "fiesta todavía puesto.",
        "Y se durmió feliz. Porque las mejores sorpresas son las que se "
        "preparan con el corazón.",
    ],
    # -------------------------------------- pequeno-maestro (Aprender y enseñar)
    "pequeno-maestro": [
        "En {mundo} había algo que {nombre} miraba siempre con ojos enormes: "
        "{amigos} sabían hacer una cosa increíble, y {nombre} soñaba con "
        "aprenderla.",
        "«¿Me enseñan?», preguntó {nombre}. «¡Claro! Pero se necesita "
        "paciencia». Para darse valor, {nombre} empezó a {conteo}... ¡y arrancó "
        "la primera clase!",
        "{amigos} le mostraron cómo se hacía, despacito y con cuidado, mientras "
        "{nombre} miraba sin pestañear.",
        "El primer intento fue un desastre gracioso: {nombre} se enredó, se "
        "cayó de cola y todo salió al revés. Pero en vez de llorar... ¡se rió!",
        "«No sale a la primera, y está bien», dijo el más viejito de {amigos}. "
        "«Todos empezamos así. Lo importante es intentarlo de nuevo».",
        "{nombre} practicó una vez, y otra, y otra más. Cada día un poquito, "
        "sin apurarse, mientras {amigos} alentaban desde el costado.",
        "Y una tarde, casi sin darse cuenta... ¡le salió por primera vez! "
        "{amigos} festejaron tan fuerte que se cayeron todos juntos, muertos "
        "de risa.",
        "Justo llegó una gran noticia: ¡en {mundo} habría una muestra para que "
        "cada uno enseñara lo que sabía hacer! {nombre} empezó a preparar su "
        "número.",
        "Pero mientras practicaba, {nombre} vio a un amiguito nuevo, chiquito "
        "y tímido, mirando todo desde lejos. «Yo nunca voy a poder», suspiraba.",
        "{nombre} se acordó de cuando recién empezaba, y se acercó despacito: "
        "«¿Te enseño? Yo me caí mil veces, y mirá ahora».",
        "Practicaron juntos toda la tarde, de a pasitos, con mucha paciencia. "
        "«¡Vas genial!», repetía {nombre}, y el amiguito se animaba más y más.",
        "Llegó el día de la muestra: a {nombre} le salió perfecto y todos "
        "festejaron fuerte. Pero lo más lindo fue cuando el amiguito nuevo "
        "subió también... ¡y lo logró!",
        "El amiguito saltaba de alegría, y buscó a {nombre} entre todos para "
        "decirle: «¡Gracias por enseñarme!».",
        "«Aprender es difícil», dijeron {amigos}, «pero enseñar con paciencia "
        "es todavía más lindo. Y {nombre} hizo las dos cosas».",
        "En agradecimiento, {amigos} le regalaron a {nombre} {tesoro}, el "
        "premio de {mundo} para quien enseña con el corazón.",
        "De vuelta en su cama, {nombre} pensaba en la carita de orgullo del "
        "amiguito nuevo.",
        "Y se durmió feliz. Porque lo que aprendemos con cariño se vuelve más "
        "lindo cuando lo compartimos.",
    ],
    # ------------------------------------- ayudar-a-todos (Cada uno su granito)
    "ayudar-a-todos": [
        "Una mañana, en {mundo}, apareció un problema grandote, y todos se "
        "quedaron mirándolo sin saber qué hacer.",
        "«Es demasiado difícil», dijo uno. «Somos muy chiquitos», dijo otro. "
        "Pero {nombre} respiró hondo, empezó a {conteo}... y le brotó una idea.",
        "{amigos} estaban sentados cabizbajos, convencidos de que nadie iba a "
        "poder resolverlo.",
        "«¿Y si lo resolvemos entre todos?», propuso {nombre}. «Cada uno sabe "
        "hacer algo distinto. ¡Juntos podemos!». Y {amigos} levantaron la "
        "cabeza con un brillito de esperanza.",
        "«Pero yo soy muy pequeño para servir de algo», dijo el más chiquito, "
        "escondiéndose en un rinconcito.",
        "«Justamente por eso sos importante», le sonrió {nombre}. «Vos llegás "
        "a lugares donde los grandes no entran. Te necesitamos».",
        "{nombre} le dio a cada uno una tarea: el más alto alcanzaba, el más "
        "fuerte empujaba, el más rápido avisaba... y el más chiquito tenía la "
        "misión más secreta de todas.",
        "Al principio costó un montón: el problema era grandote de verdad, y "
        "más de uno quiso rendirse otra vez.",
        "Pero el más chiquito se metió por un huequito donde nadie más "
        "entraba... ¡y destrabó la primera parte! Todos gritaron de alegría.",
        "El más alto alcanzó lo inalcanzable, el más fuerte empujó con todo, y "
        "{nombre} los coordinaba como una orquesta: «¡Ahora vos! ¡Ahora vos!».",
        "Hubo un tropezón y casi se arruina todo... pero se sostuvieron en "
        "grupo, se rieron del susto y siguieron, más unidos que nunca.",
        "Con un último esfuerzo de todos juntos... ¡lo lograron! El problema "
        "se resolvió, y {mundo} volvió a estar en paz.",
        "{amigos} saltaban festejando, y el más chiquito —el que creía que no "
        "servía— quedó en el medio de la ronda, hecho un héroe.",
        "«¿Vieron?», dijo {nombre}. «Solos parecía imposible. Pero cada uno, "
        "con su granito, hizo algo que ninguno podía hacer solo».",
        "Para celebrarlo, {amigos} le regalaron a {nombre} {tesoro}, por "
        "enseñarles que todos, todos, son importantes.",
        "De vuelta en su cama, {nombre} se acurrucó pensando en el gran equipo "
        "que habían formado.",
        "Y se durmió con una sonrisa. Porque juntos, no hay nada imposible.",
    ],
    # ------------------------------------------- gran-viaje (La entrega importante)
    "gran-viaje": [
        "Esa tarde llegó a la puerta de {nombre} un paquetito brillante con un "
        "moño y un pedido: «Esto tiene que llegar esta misma noche a la otra "
        "punta de {mundo}. ¿Nos ayudás?».",
        "{nombre} preparó una mochila liviana, empezó a {conteo} para darse "
        "coraje... ¡y el viaje más importante comenzó!",
        "Al llegar a {mundo}, {amigos} esperaban con un mapa del recorrido: era "
        "un camino largo, largo, con tres paradas.",
        "«Este encargo es para el abuelito más querido de {mundo}», contaron. "
        "«Mañana es su gran día, y sin esto no hay festejo». ¡Había que llegar "
        "antes del amanecer!",
        "Se repartieron el viaje: los que conocían el principio irían adelante, "
        "y {nombre} cuidaría el paquetito durante todo el camino.",
        "La primera parte fue fácil y divertida: cantaron canciones de viaje "
        "mientras el sol se escondía despacito.",
        "En la primera parada, un viento fuerte y travieso quiso llevarse el "
        "paquetito. {nombre} lo abrazó fuerte: «¡De acá no te vas!».",
        "El viento sopló y sopló... hasta que se cansó. Y de tanto soplar, "
        "¡despejó el cielo y dejó todas las estrellas a la vista!",
        "Con las estrellas de guía, {nombre} encontró un atajo que no estaba "
        "en el mapa, y el grupo avanzó más rápido que nunca.",
        "En la segunda parada los esperaba una sorpresa: un puesto de "
        "chocolate calentito, para seguir el viaje con fuerzas.",
        "La última parte era la más oscura de todas. {nombre} fue adelante, "
        "pasito a pasito, y el grupo avanzó bien juntito, sin separarse.",
        "Justo antes del amanecer... ¡llegaron! El abuelito abrió el paquetito "
        "y se le llenaron los ojos de lágrimas felices: era un regalo hecho "
        "por todos sus amigos de {mundo}.",
        "«Pensé que nadie se acordaba de mí», dijo bajito. «¡Y este regalo "
        "viajó toda la noche para llegar!». Y lo apretó contra el corazón.",
        "El festejo del abuelito arrancó con el primer rayito de sol, y el "
        "lugar de honor fue para {nombre}, que había llegado desde más lejos "
        "que nadie.",
        "{amigos} le regalaron a {nombre} {tesoro}, el premio de {mundo} para "
        "quien nunca abandona una misión.",
        "De vuelta en su cama, {nombre} todavía sentía en las manos el "
        "calorcito del chocolate del viaje.",
        "Y se durmió feliz. Porque los caminos largos se hacen cortitos "
        "cuando se caminan con amigos.",
    ],
    # --------------------------------------- manos-a-la-obra (El rincón soñado)
    "manos-a-la-obra": [
        "En {mundo} había un sueño que nadie cumplía: un rincón propio para "
        "juntarse a jugar, con techito para los días de lluvia. Pero nadie "
        "sabía por dónde empezar.",
        "«Yo sé por dónde», dijo {nombre}: «¡por el principio!». Empezó a "
        "{conteo} para ordenar las ideas... y dibujó un plano en el piso.",
        "Era un plano hermoso: un rinconcito con mesa, banquitos y un techito "
        "con forma de sonrisa.",
        "{amigos} miraron el plano con los ojos brillantes: «¿De verdad "
        "podemos construirlo nosotros?». «Entre todos, sí», dijo {nombre}. "
        "¡Manos a la obra!",
        "Cada uno trajo lo que tenía: maderitas, sogas, telas de colores y un "
        "montón de ganas.",
        "Midieron con pasos, marcaron con piedritas y levantaron las primeras "
        "columnas, derechitas como soldaditos.",
        "Pero al colocar el techito... ¡CRAC!, quedó torcido, y todo empezó a "
        "tambalearse. Algunos se asustaron: «¡Se va a caer!».",
        "{nombre} miró el plano, miró el techito, y encontró el error: faltaba "
        "una pieza en el medio, la más importante de todas.",
        "«Equivocarse es parte de construir», dijo {nombre}, y entre todos "
        "enderezaron el techito con la pieza justa en el lugar justo. ¡Ahora "
        "sí quedaba firme!",
        "Los más chiquitos pintaron los banquitos, los más altos colgaron "
        "farolitos, y los más fuertes ajustaron cada rincón.",
        "Al atardecer, {nombre} colgó el último farolito, y todos dieron un "
        "paso atrás para mirar.",
        "Ahí estaba: el rincón soñado de {mundo}, firme y lleno de colores, "
        "hecho a pura mano y corazón. ¡El sueño se había cumplido!",
        "Lo estrenaron esa misma noche con una merienda bajo el techito "
        "nuevo. ¡Hasta la lluvia vino a probarlo... y adentro nadie se mojó!",
        "«Cada vez que juguemos acá», dijeron {amigos}, «nos vamos a acordar "
        "de quién nos enseñó a empezar por el principio».",
        "Y le regalaron a {nombre} {tesoro}, con un lugar reservado para "
        "siempre en el rincón nuevo.",
        "De vuelta en su cama, {nombre} todavía tenía un poquito de pintura "
        "de colores en los dedos.",
        "Y se durmió feliz. Porque lo que se construye con las manos y con "
        "amigos, queda para siempre.",
    ],
    # ------------------------------------------ gran-torneo (Los Grandes Juegos)
    "gran-torneo": [
        "¡Gran noticia! Se venían los Grandes Juegos, los más divertidos del "
        "año en {mundo}... pero {amigos} estaban desanimados: «Siempre nos "
        "sale todo al revés».",
        "«Al revés se empieza», dijo {nombre} con una sonrisa. «¡Vamos a "
        "entrenar!». Y para arrancar, los puso a todos a {conteo} bien fuerte.",
        "El primer entrenamiento fue un lío: todos corrían para lados "
        "distintos y se chocaban. ¡Pero terminaron riéndose en el piso!",
        "{nombre} propuso el plan: «Entrenamos juntos todos los días, cada "
        "uno en lo suyo, y a los Grandes Juegos vamos EN EQUIPO».",
        "El más rápido practicó las carreras, el más fuerte los saltos, y el "
        "más chiquito... ¡la jugada secreta!",
        "Día a día salía mejor: ya no se chocaban. Se pasaban, se esperaban, "
        "se alentaban.",
        "Pero justo antes de los juegos, el capitán del equipo se dio un "
        "porrazo y no podía jugar. «Sin nuestro capitán no somos nada», "
        "dijeron todos, cabizbajos.",
        "{nombre} juntó al equipo en ronda: «El capitán nos va a alentar "
        "desde afuera. Y nosotros vamos a jugar en su nombre, con el corazón "
        "el doble de grande».",
        "Y el día de los juegos, el equipo entró con el capitán al frente, "
        "alentando desde el costado con la voz más fuerte de {mundo}.",
        "La primera prueba salió regular. La segunda, un poquito mejor. ¡Y en "
        "la tercera ya nadie los paraba!",
        "La prueba final iba cabeza a cabeza con el otro equipo. Todo se "
        "definía en la última jugada... ¡la jugada secreta del más chiquito!",
        "El más chiquito hizo su jugada, todos entraron en el momento justo... "
        "¡y salió PERFECTA! Todo el público de {mundo} saltó a festejar el "
        "jugadón.",
        "Los dos equipos terminaron festejando juntos y mezclados, porque "
        "había sido el juego más lindo de la historia de los Grandes Juegos.",
        "El capitán abrazó a todo el equipo: «Nunca jugamos tan bien... ¡y yo "
        "mirándolos desde afuera! Ahora sé que somos un equipo de verdad».",
        "En la premiación, {amigos} le regalaron a {nombre} {tesoro}, por "
        "enseñarles a jugar en equipo.",
        "De vuelta en su cama, {nombre} todavía escuchaba los festejos y las "
        "risas de los Grandes Juegos.",
        "Y se durmió feliz. Porque cuando jugás en equipo, ya ganaste antes "
        "de empezar.",
    ],
}

# Chequeo de integridad: todos los arcos deben tener 17 páginas y el corto 9.
assert all(len(v) == 17 for v in ARGUMENTOS_LARGO.values()), \
    {k: len(v) for k, v in ARGUMENTOS_LARGO.items() if len(v) != 17}
assert len(CORTO_IDX) == 9 and max(CORTO_IDX) < 17


# ================================================================
# Historias del LIBRO-kit, movidas desde libro.py (unificación 17-jul-2026:
# todas las historias en un solo lugar). ARGUMENTOS_EXT usa ARGUMENTOS → va después.
# ================================================================

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

ARGUMENTOS_EXT = {
    "tesoro": ARGUMENTOS["tesoro"][:6] + [
        # OJO gramática de arcos ({tesoro} puede ser fem/masc y largo): nunca
        # referirlo con pronombres (lo/la) ni colgarle adverbios detrás
        "Todos se sentaron en ronda para mirar de cerca {tesoro}. {amigos} le "
        "contaron a {nombre} la leyenda del tesoro, escondido hace tantos años.",
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
