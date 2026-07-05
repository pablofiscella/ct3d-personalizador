# -*- coding: utf-8 -*-
"""Catálogo de historias de los audiolibros (versión larga, 17 páginas).

Cada arco es una lista de 17 textos-plantilla que usan los placeholders del tema:
{nombre} {mundo} {amigos} {conteo} {conteo_num} {tesoro} {desafio} {solucion}.

El largo se elige por EDAD (ver libro.paginas_historia):
  - 4 años o más  -> 17 páginas de historia (20 en total)  -> arco completo
  - hasta 3 años  -> 9 páginas de historia (12 en total)   -> subconjunto CORTO_IDX

Están desacopladas del tema: cualquier tema puede usar cualquier historia.
El texto de cada página se capitaliza automáticamente en libro.cuento (por si un
placeholder como {amigos} cae al comienzo de una oración).
"""

# Índices (0..16) que se conservan en la versión corta (hasta 3 años): mantienen
# el arranque, algunos hitos del viaje y SIEMPRE el cierre para dormir.
CORTO_IDX = [0, 1, 3, 6, 8, 11, 14, 15, 16]

ARGUMENTOS_LARGO = {
    # ------------------------------------------------------------------ aventura
    "aventura": [
        "Esta noche, antes de dormir, {nombre} encontró una invitación brillante "
        "debajo de la almohada. Decía: «Te esperamos en {mundo}».",
        "Con el corazón lleno de curiosidad, {nombre} cerró los ojos y empezó a "
        "{conteo}. ¡De golpe la habitación se llenó de luces de colores!",
        "Cuando las luces se apagaron, {nombre} ya no estaba en su cuarto: había "
        "llegado a {mundo}, más grande y más mágico de lo que imaginaba.",
        "{amigos} lo recibieron con una gran fiesta de bienvenida, con guirnaldas, "
        "música y un cartel enorme que decía su nombre.",
        "Le mostraron cada rincón de {mundo}, y {nombre} no paraba de reírse de lo "
        "hermoso y divertido que era todo por ahí.",
        "Pero de pronto todo se detuvo: {desafio}. Nadie sabía qué hacer... nadie, "
        "excepto {nombre}.",
        "{nombre} respiró hondo, miró a su alrededor y se dio cuenta de que tenía "
        "una idea que podía funcionar.",
        "Con valentía y una gran sonrisa, {nombre} {solucion}. ¡Todos festejaron "
        "su ingenio dando saltos de alegría!",
        "Para celebrar, {amigos} propusieron un juego gigante, y todos se turnaron "
        "para inventar la payasada más divertida.",
        "Una música suave los llevó hasta un rincón secreto de {mundo}, lleno de "
        "luciérnagas que parpadeaban como si saludaran.",
        "Ahí, {amigos} le contaron a {nombre} las historias más antiguas del lugar, "
        "y él escuchó con los ojos bien abiertos.",
        "Como agradecimiento, {amigos} le regalaron {tesoro}: un recuerdo para "
        "siempre de esa noche tan especial.",
        "Jugaron a las escondidas entre las sombras tibias, y {nombre} fue el mejor "
        "encontrando a cada amigo escondido.",
        "Cuando empezó a dar sueño, se sentaron todos juntos a mirar el cielo, "
        "y contaron las estrellas hasta perder la cuenta.",
        "{amigos} lo acompañaron de vuelta por el camino de luces, prometiéndole "
        "que la próxima aventura ya lo estaba esperando.",
        "«Volvé cuando quieras», le susurraron, «acá siempre vas a tener amigos "
        "que te quieren». Y {nombre} sintió el pecho calentito.",
        "De vuelta en su cama, {nombre} se durmió con una sonrisa. Porque quien es "
        "valiente y ayuda a los demás, siempre tiene una nueva aventura esperando.",
    ],
    # -------------------------------------------------------------------- tesoro
    "tesoro": [
        "Esa mañana, {nombre} encontró un mapa antiguo enrollado en su mochila. "
        "Marcaba un camino secreto hacia {mundo}.",
        "Al seguir la primera pista y {conteo}, ¡el mapa empezó a brillar! La "
        "búsqueda del tesoro había comenzado.",
        "En {mundo}, {amigos} conocían las pistas: cada uno le contó a {nombre} un "
        "secreto del camino.",
        "La primera pista los llevó a un jardín de flores gigantes, donde había que "
        "encontrar la única flor con forma de estrella.",
        "{nombre} la encontró enseguida, y al tocarla apareció la siguiente pista "
        "escondida entre sus pétalos.",
        "Pero la última pista estaba del otro lado de un río enorme, y nadie sabía "
        "cómo cruzarlo... nadie, excepto {nombre}.",
        "{nombre} armó un puente con troncos y sogas, ¡y cruzaron todos juntos "
        "cantando! Ahí estaba: un cofre dorado.",
        "Adentro brillaba {tesoro}. {amigos} aplaudieron: «¡{nombre} es quien mejor "
        "sigue las pistas en todo {mundo}!».",
        "Todos se sentaron en ronda para admirarlo de cerca, y {amigos} le contaron "
        "la leyenda de quién lo había escondido hace tantos años.",
        "De pronto, el mapa volvió a brillar: ¡tenía una segunda cara! Mostraba un "
        "camino nuevo, más corto, de vuelta a casa.",
        "En el camino encontraron una piedra enorme bloqueando el paso. Entre "
        "todos, empujando juntos y contando hasta tres, lograron correrla.",
        "Detrás de la piedra apareció una cueva llena de cristales que brillaban "
        "con todos los colores, como un arco iris guardado.",
        "Como festejo por el trabajo en equipo, armaron una merienda bajo un árbol, "
        "y {nombre} repartió un pedacito de aventura para cada amigo.",
        "Mientras merendaban, se rieron recordando cada pista y cada susto del "
        "camino, que ahora parecían pura diversión.",
        "Antes de despedirse, {amigos} le prometieron a {nombre} que el mapa "
        "tendría siempre una pista nueva esperando para la próxima vez.",
        "{nombre} guardó el mapa con muchísimo cuidado, sabiendo que era el "
        "comienzo de un montón de aventuras por venir.",
        "De vuelta en casa, {nombre} guardó el mapa bajo la almohada. Los mejores "
        "tesoros se encuentran con paciencia y buenos amigos.",
    ],
    # ------------------------------------------------------------------- rescate
    "rescate": [
        "Una noche, una lucecita golpeó la ventana de {nombre}: era un mensaje "
        "urgente desde {mundo}. ¡Necesitaban ayuda!",
        "{nombre} no lo dudó: cerró los ojos, empezó a {conteo}... y el viento lo "
        "llevó volando hasta {mundo}.",
        "{amigos} estaban muy preocupados: el más pequeño del grupo se había "
        "perdido y ya estaba oscureciendo.",
        "Todos hablaban al mismo tiempo, nerviosos, pero {nombre} pidió calma y "
        "propuso buscar señales con mucha atención.",
        "Buscaron por todos lados sin suerte. Entonces {nombre} tuvo una idea: "
        "«¡Sigamos las huellas más chiquitas!».",
        "Las huellas los llevaron por un sendero de árboles altos, donde el viento "
        "hacía ruiditos que parecían susurros.",
        "Al final del sendero encontraron una cueva oscura, y de adentro venía un "
        "llantito muy bajito. ¡Era el pequeño!",
        "{nombre} entró con su linterna, tomó al pequeño de la mano y lo trajo de "
        "vuelta. ¡Qué valiente!",
        "El pequeño rescatado abrazó fuerte a {nombre} y le contó que se había "
        "perdido siguiendo una mariposa brillante que quería atrapar.",
        "«¿Y si la buscamos juntos, pero esta vez sin separarnos?», propuso "
        "{nombre}. Todos se tomaron de la mano y salieron a explorar.",
        "La mariposa los llevó hasta un lugar precioso que nadie en {mundo} "
        "conocía: un rincón lleno de luces como pequeñas estrellas caídas.",
        "{amigos} decidieron que ese sería su nuevo lugar de encuentro secreto, y "
        "todos prometieron cuidarlo entre todos.",
        "Como agradecimiento, {amigos} le regalaron a {nombre} {tesoro}: la marca "
        "de los héroes de {mundo}.",
        "El más pequeño le hizo prometer que volvería a visitarlo, y {nombre} le "
        "dijo que sí, mil veces sí.",
        "Ya de noche, cantaron juntos alrededor de las lucecitas, felices de que "
        "la aventura hubiera terminado bien para todos.",
        "Uno a uno se fueron despidiendo con un abrazo, y {nombre} sintió que "
        "tenía amigos de verdad en {mundo}.",
        "Esa noche {nombre} durmió con una sonrisa gigante. Ayudar a un amigo es "
        "la aventura más importante de todas.",
    ],
    # ------------------------------------------------------------------ gran-dia
    "gran-dia": [
        "¡Llegó una noticia increíble! En {mundo} se hacía la Gran Fiesta del año, "
        "y {nombre} estaba en la lista de invitados especiales.",
        "{nombre} preparó su mochila, contó hasta {conteo_num} para darse valor... "
        "¡y salió rumbo a la aventura!",
        "{amigos} lo recibieron ensayando: había juegos, música y un gran desfile "
        "para preparar. ¡Faltaba tan poco!",
        "A {nombre} le dieron la tarea más importante: guiar el desfile con una "
        "linterna de estrellas en la mano.",
        "Practicaron toda la tarde, marchando y riendo, hasta que todo salía "
        "redondito y hermoso.",
        "Pero de pronto, ¡PUM!, una tormenta desarmó todo lo que habían preparado. "
        "Todos se miraron sin saber qué hacer.",
        "Algunos querían rendirse, pero {nombre} los miró y dijo bajito: «Todavía "
        "podemos arreglarlo si lo hacemos juntos».",
        "«¡No nos rindamos!», dijo {nombre}, y organizó a todos: unos ataban, "
        "otros pintaban... ¡y la fiesta quedó más linda que antes!",
        "Con {tesoro} bien puesto, {nombre} fue el encargado de dar la bienvenida "
        "a cada invitado que llegaba a {mundo}.",
        "El desfile arrancó con {nombre} al frente, y su linterna de estrellas "
        "iluminó todo el camino como por arte de magia.",
        "A mitad de la fiesta, la música se cortó de repente. ¡El equipo de sonido "
        "se había quedado sin pilas!",
        "{nombre} tuvo una idea genial: organizó a {amigos} para hacer música con "
        "las manos, los pies y lo que tenían a mano.",
        "La banda improvisada sonó tan bien que todos terminaron bailando más "
        "fuerte que antes, ¡y nadie extrañó la música original!",
        "Hubo torta, luces y un cielo lleno de fuegos artificiales de colores que "
        "dibujaban figuras sobre {mundo}.",
        "Cuando el sol empezó a esconderse, {amigos} armaron una ronda final para "
        "agradecerle a {nombre} por salvar el gran día.",
        "«Sos parte de {mundo} para siempre», le dijeron, y le entregaron una "
        "medalla de luciérnagas que brillaba suavecito.",
        "Al volver a casa, {nombre} entendió el secreto: los grandes días se "
        "construyen entre todos, con manos que ayudan.",
    ],
    # ----------------------------------------------------------- noche-estrellas
    "noche-estrellas": [
        "Esa noche, {nombre} no podía dormir. Daba vueltas en la cama mirando el "
        "techo, con los ojos bien abiertos y ni una pizca de sueño.",
        "De repente, por la ventana vio caer una estrella fugaz, larga y "
        "brillante, que se perdió justo detrás de {mundo}.",
        "Sin pensarlo, se puso las pantuflas y, contando los pasos hasta "
        "{conteo_num}, salió despacito a buscarla en la oscuridad.",
        "Apenas cruzó la puerta, apareció en {mundo} bajo un cielo enorme lleno de "
        "estrellas que titilaban como si le hicieran cosquillas a la noche.",
        "{amigos} lo estaban esperando: también habían visto caer la estrella y no "
        "querían buscarla solos en la oscuridad.",
        "«¿Me acompañás?», le preguntaron. {nombre} dijo que sí, y todos juntos se "
        "pusieron en marcha siguiendo un brillito lejano.",
        "El camino estaba muy oscuro, pero {nombre} encontró un montón de "
        "luciérnagas y les pidió que los alumbraran. ¡Y aceptaron encantadas!",
        "Con esa lucecita tibia siguieron adelante, cruzando puentes de nubes y "
        "colinas dormidas, cada vez más cerca del resplandor.",
        "Al final del camino la encontraron: la estrella fugaz estaba en el suelo, "
        "chiquita y apagada, llorando lágrimas de luz.",
        "«No encuentro el camino de vuelta al cielo», dijo bajito, «y tengo miedo "
        "de quedarme sola acá abajo para siempre».",
        "{nombre} se acercó despacio y la abrazó. «No estás sola», le dijo, «te "
        "vamos a ayudar a volver a tu lugar allá arriba».",
        "{amigos} le armaron una camita de nubes suaves, y {nombre} le cantó una "
        "canción bajito hasta que la estrella dejó de temblar.",
        "Poco a poco, la estrella se fue sintiendo mejor, y con cada mimo su luz "
        "volvía a encenderse, más y más fuerte.",
        "Cuando estuvo lista, {nombre} pidió un deseo: que sus amigos estuvieran "
        "siempre juntos, pasara lo que pasara.",
        "La estrella brilló tan fuerte que se elevó como un globo de luz, y desde "
        "el cielo les guiñó un ojo a todos, agradecida.",
        "«Cada vez que no puedas dormir, mirá para arriba y buscame», le dijo a "
        "{nombre}. «Ahí voy a estar, cuidándote».",
        "De vuelta en su cama, {nombre} miró por la ventana, encontró su estrella "
        "titilando, y se durmió sabiendo que tenía una amiga allá en el cielo.",
    ],
    # ---------------------------------------------------------- cumple-sorpresa
    "cumple-sorpresa": [
        "Esa mañana en {mundo}, {nombre} sintió que algo raro pasaba: {amigos} "
        "andaban de acá para allá, tapándose la boca para no reírse.",
        "«Buen día», saludó {nombre}. Y todos contestaron a las apuradas y "
        "salieron corriendo, escondiendo algo detrás de la espalda.",
        "«¿Estarán enojados conmigo?», pensó {nombre} con la pancita apretada. "
        "Pero decidió no preocuparse y salió a jugar como siempre.",
        "Detrás de un arbusto escuchó cuchicheos: «...tiene que ser una "
        "sorpresa...». {nombre} se tapó los oídos: no quería arruinar nada.",
        "En el camino encontró un globo de colores perdido. Y más allá, una "
        "guirnalda. Y unas huellas con brillos que llevaban al claro grande.",
        "{nombre} se moría de curiosidad, pero se dijo: «Si es una sorpresa, la "
        "mejor parte es esperar». Y siguió jugando, haciéndose el distraído.",
        "Para pasar el rato, se puso a {conteo} las nubes que pasaban, imaginando "
        "qué linda sería la sorpresa que le estaban preparando.",
        "Una mariposa lo invitó a seguirla. {nombre} caminó despacito, con el "
        "corazón latiendo de emoción, adivinando que algo lindo lo esperaba.",
        "En el camino ayudó a una tortuga a cargar unos frascos de dulce. «Son "
        "para una fiesta muy especial», le guiñó el ojo la tortuga.",
        "El cielo se fue tiñendo de naranja. {amigos} lo llamaron desde lejos: "
        "«¡{nombre}, vení, te tenemos algo!». Y él corrió sin pensarlo.",
        "Cuando llegó al claro, todo estaba oscuro y calladito. {nombre} dio un "
        "pasito... y de repente: «¡SORPRESA!». Se encendieron mil lucecitas.",
        "¡Era una fiesta para él! Guirnaldas, {tesoro} en el centro y {amigos} con "
        "gorritos, saltando de alegría. {nombre} no lo podía creer.",
        "«Estuvimos todo el día preparándola en secreto», contaron. «Por eso "
        "andábamos raros. ¡Queríamos verte la carita!». Y {nombre} se rió fuerte.",
        "«Pensé que estaban enojados», confesó {nombre}. «¡Jamás!», dijeron "
        "{amigos}. «Guardar una sorpresa tan grande era dificilísimo».",
        "Bailaron, jugaron y comieron torta hasta que salió la luna. {nombre} "
        "entendió que la mejor sorpresa no era la fiesta, sino tener amigos así.",
        "Antes de irse, cada amigo le dio un abrazo y un regalito hecho a mano, y "
        "{nombre} los guardó cerquita del corazón.",
        "De vuelta en su camita, con un gorrito todavía puesto, {nombre} se durmió "
        "con una sonrisa gigante, soñando con la sorpresa más linda del mundo.",
    ],
    # ---------------------------------------------------------- pequeno-maestro
    "pequeno-maestro": [
        "En {mundo} había algo que {nombre} miraba con ojos grandes: {amigos} "
        "sabían hacer una cosa increíble, y él se moría de ganas de aprenderla.",
        "«¿Me enseñan?», preguntó. «¡Claro!», dijeron {amigos}. «Pero se necesita "
        "paciencia y muchas ganas». {nombre} tenía las dos cosas de sobra.",
        "El primer intento fue un desastre gracioso: {nombre} se enredó, se cayó "
        "de cola y todo salió al revés. Pero en vez de llorar, se rió.",
        "«No sale a la primera, y está bien», le dijo el más viejito de {amigos}. "
        "«Todos empezamos así. Lo importante es volver a intentarlo».",
        "{nombre} practicó una vez. Y otra. Y otra más. Cada día un poquito, sin "
        "apurarse, mientras {amigos} lo alentaban desde el costado.",
        "Para no perder la cuenta de sus intentos, aprendió a {conteo}, y cada "
        "número era un pasito más cerca de lograrlo.",
        "Al principio le temblaban las patas. Después, apenas un poquito. Y una "
        "tarde, casi sin darse cuenta... ¡le salió por primera vez!",
        "«¡Lo logré!», gritó {nombre} saltando. {amigos} lo abrazaron tan fuerte "
        "que casi se caen todos juntos, riéndose a carcajadas.",
        "Con los días, {nombre} fue mejorando muchísimo. Ya no le costaba nada; "
        "hasta inventaba sus propios truquitos nuevos.",
        "Un día llegó a {mundo} un amiguito nuevo, chiquito y tímido, que miraba "
        "todo desde lejos sin animarse a jugar.",
        "«Yo nunca voy a poder hacer eso, es muy difícil», suspiró el nuevo, y "
        "bajó las orejitas, tristón.",
        "{nombre} se acordó de cuando él era así, y se acercó despacito. «¿Te "
        "enseño? Yo también pensaba que no podía, y mirá ahora».",
        "Con mucha paciencia le mostró de a pasitos, igual que le habían enseñado "
        "a él. «No importa si te caés. Yo me caí mil veces».",
        "Practicaron juntos toda la tarde. {nombre} no se cansaba de decirle «vas "
        "genial», y el amiguito cada vez se animaba más y más.",
        "Y entonces pasó: ¡el nuevo lo logró! Dio un gritito de alegría, y {nombre} "
        "sintió algo calentito en el pecho, más lindo que cualquier premio.",
        "En agradecimiento, {amigos} le regalaron {tesoro} a {nombre}, por ser el "
        "maestro más paciente y cariñoso de todo {mundo}.",
        "Esa noche, en su camita, {nombre} se durmió feliz, sabiendo que lo que "
        "aprendemos con cariño se vuelve más lindo cuando lo compartimos.",
    ],
    # ----------------------------------------------------------- ayudar-a-todos
    "ayudar-a-todos": [
        "Una mañana, en {mundo}, algo no andaba bien: un problema grandote "
        "apareció y todos se quedaron mirándolo sin saber qué hacer.",
        "«Es demasiado difícil», dijo uno. «Somos muy chiquitos», dijo otro. "
        "{amigos} se sentaron cabizbajos, creyendo que no podían.",
        "{nombre} miró a su alrededor y tuvo una idea. «¿Y si lo resolvemos entre "
        "todos? Cada uno sabe hacer algo distinto».",
        "«Pero yo soy muy pequeño para servir de algo», dijo el más chiquito de "
        "{amigos}, escondiéndose detrás de una hojita.",
        "«Justamente por eso sos importante», le sonrió {nombre}. «Vos llegás a "
        "lugares donde los grandes no entran. Te necesitamos».",
        "Al más alto de {amigos}, {nombre} le pidió que alcanzara las cosas de "
        "arriba. «¡Para eso soy buenísimo!», dijo, estirándose orgulloso.",
        "Al más fuerte le tocó empujar; al más rapidito, ir y venir con los "
        "mensajes; al más tranquilo, pensar el plan con calma.",
        "«¿Y yo?», preguntó una vocecita: era el más miedoso. «Vos nos vas a dar "
        "ánimo», dijo {nombre}. «Sin alguien que aliente, nadie sigue».",
        "Así, cada uno con su tarea, empezaron. Para arrancar todos juntos, "
        "{nombre} los hizo {conteo} en voz alta: ¡y a trabajar!",
        "El chiquito se metió por un huequito imposible. El alto alcanzó lo "
        "inalcanzable. El fuerte empujó con todo. ¡De a poco, la cosa se movía!",
        "{nombre} los coordinaba: «¡Ahora vos! ¡Ahora vos!». Como una orquesta, "
        "cada uno entraba en su momento justo.",
        "Hubo un tropezón y todo casi se viene abajo. Pero se agarraron entre "
        "todos, se rieron del susto y volvieron a empezar más unidos.",
        "Y entonces, con un último empujón de todos juntos... ¡lo lograron! El "
        "problema se resolvió y {mundo} volvió a estar lindo y en paz.",
        "{amigos} saltaban festejando. Y el más chiquito, el que creía que no "
        "servía, estaba en el medio de todos, hecho un héroe.",
        "«¿Vieron?», dijo {nombre}. «Solos parecía imposible. Pero cada uno, con "
        "su granito, hizo algo que ninguno podía hacer solo».",
        "Para celebrarlo, {amigos} le regalaron {tesoro} a {nombre}, por "
        "enseñarles que todos, todos, son importantes.",
        "De vuelta en casa, {nombre} se acurrucó en la cama pensando en sus "
        "amigos, y se durmió sabiendo que juntos no hay nada imposible.",
    ],
}

# Chequeo de integridad: todos los arcos deben tener 17 páginas y el corto 9.
assert all(len(v) == 17 for v in ARGUMENTOS_LARGO.values()), \
    {k: len(v) for k, v in ARGUMENTOS_LARGO.items() if len(v) != 17}
assert len(CORTO_IDX) == 9 and max(CORTO_IDX) < 17
