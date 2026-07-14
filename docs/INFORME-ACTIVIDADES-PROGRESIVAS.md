# Informe: actividades progresivas por edad (4 a 12 años)

> Pedido de Pablo (14-jul-2026): armar una investigación real (currículum NAP +
> metodologías de aprendizaje) que sirva de base para diseñar actividades
> progresivas, empezando por 4 años y subiendo desde ahí — **"lo más serio
> posible... no solo las actividades sino la gráfica y estética que
> acompañe... los chicos tienen que aprender de verdad"**. Este informe cruza
> cinco fuentes:
> 1. `docs/CURRICULUM-NAP-ARGENTINA.md` — el currículum NAP que Pablo pasó (QUÉ
>    tiene que aprender un chico en cada año escolar, los 9 años completos).
> 2. Investigación de metodologías de aprendizaje (Piaget, Vygotsky, alfabetización
>    basada en evidencia, Singapore Math, atención sostenida por edad) — CÓMO
>    secuenciar la dificultad de forma pedagógicamente sólida.
> 3. Auditoría real del motor (`cuaderno.py`, `actividades_web.py`,
>    `actividades_player.js`) — QUÉ es capaz de generar HOY, verificado por
>    código (no supuesto).
> 4. Investigación de diseño gráfico basado en evidencia (tipografía, color,
>    ilustración, layout) — CÓMO tiene que verse para que el diseño ayude al
>    aprendizaje en vez de solo decorarlo.
> 5. Investigación de verificación de aprendizaje real (distractores,
>    mastery learning, feedback correctivo) — cómo asegurar que "completar
>    la actividad" signifique "aprendió", no "adivinó".
>
> El proceso repetible para seguir construyendo esto queda en la skill
> `.claude/skills/actividades-progresivas/SKILL.md`.

## 1. Hallazgo principal (el que cambia el orden de trabajo)

**El motor cubre razonablemente Nivel Inicial + 1°/2° grado (4 a 7 años). De 3°
grado en adelante (8 a 12 años) no existe ni un solo tipo de actividad hoy** —
ni multiplicación, ni fracciones, ni decimales, ni geometría con ángulos, ni
álgebra, ni lectoescritura real (sílabas, comprensión, sintaxis), ni ciencias
naturales o sociales curriculares. Esto no es una exageración retórica: se
buscó explícitamente en todo el código (`grep` de "multiplic", "fraccion",
"decimal", "silaba", "sujeto", "cuerpo humano", "virreinato", etc.) y dio
CERO resultados en los tres archivos que arman el cuaderno.

Además, el sistema de bandas de edad actual tiene un problema de fondo: la
banda `"grande"` de `actividades_web._banda()` es `edad >= 6 SIN TOPE
SUPERIOR` — un chico de 12 años recibe literalmente el mismo menú que uno de
6. Esto no es un bug nuevo, es una limitación de diseño heredada de cuando el
producto no necesitaba diferenciar más allá de "cumpleaños infantil".

**Consecuencia práctica**: el pedido de Pablo de "empezar por 4 años e ir
subiendo" es el orden correcto por dos razones, no solo una de negocio
(validar antes de invertir mucho): en 4-7 años el trabajo es sobre todo
CURACIÓN (ordenar/etiquetar lo que ya existe contra el NAP + ampliar rangos),
mientras que en 8-12 años es CONSTRUCCIÓN DE CERO de tipos de actividad
nuevos. Son dos tipos de esfuerzo distintos y conviene no mezclarlos en el
mismo sprint de trabajo.

## 2. Qué dice la investigación pedagógica (resumen accionable)

(Detalle completo y fuentes en la sección de investigación conservada más
abajo — acá solo lo que cambia decisiones de diseño.)

- **Antes de los 7 años, todo tiene que ser manipulable visualmente** — sin
  instrucciones de texto largas, sin lógica abstracta de más de 1-2 pasos
  (Piaget, etapa preoperacional). Coincide con que el motor hoy es
  100% visual/manipulativo para esas edades — es la fortaleza actual, no
  hay que romperla al escalar a más edades.
- **De 7 a 11 años ya hay lógica sobre lo concreto, pero necesita apoyo
  gráfico** — recién a los 11-12 empieza el pensamiento abstracto puro
  (Piaget, operaciones concretas → formales). Esto dice que la matemática de
  3°-5° grado (tabla pitagórica, fracciones, decimales) DEBE tener apoyo
  visual/manipulable (tiras de fracciones, billetes de fantasía — el propio
  NAP que pasó Pablo ya lo propone así) y que recién en 6°-7° se puede pedir
  simbolismo puro (álgebra, ecuaciones sin dibujo).
- **Matemática: enfoque Concreto → Pictórico → Abstracto (Singapore Math)** —
  validado internacionalmente. Cualquier operación nueva se presenta primero
  con objetos, después con dibujos/barras, recién al final con el símbolo
  solo. El motor ya hace esto PARCIALMENTE (grupos de personajes contables)
  pero hay que sistematizarlo como regla para todo contenido numérico nuevo.
- **Alfabetización: fonética sistemática, no reconocimiento visual de
  palabras** (National Reading Panel 2000, evidencia sólida). La secuencia
  validada es conciencia fonológica ORAL (rimas, sonidos aislados) → combinar
  sonidos → sílabas escritas → palabras → oraciones. El motor hoy NO tiene
  ningún componente de sonido en las actividades de lengua (todo es visual:
  sopa de letras, "código secreto" con símbolos) — es un hueco real, no solo
  de contenido sino de MECÁNICA (falta un componente de audio/fonética que
  hoy no existe en ningún juego).
- **Andamiaje (Vygotsky/ZPD): la ayuda tiene que retirarse gradualmente**, no
  ser siempre igual. El sistema de "pistas" que ya existe en varios juegos
  debería graduarse (pista fuerte en el primer error → más sutil en el
  segundo → sin pista si acierta seguido) en vez de dar siempre la misma
  ayuda — mejora concreta y barata sobre lo que ya está construido.
- **"Cero fail states" ya está respaldado por evidencia real**, no es solo
  buena UX: la investigación sobre juegos educativos infantiles distingue
  "confusión productiva" (motiva) de "confusión desesperanzada" (hace
  abandonar) — dar salida ANTES de que se acumule frustración es clave
  específicamente en chicos chicos (tienen menos estrategias emocionales que
  un adulto para tolerar el fracaso). Mantener este principio al escalar a
  más edades, no relajarlo.
- **Atención sostenida por edad — tabla para armar packs de "30 minutos"**:

| Edad/grado | Atención por actividad | Actividades distintas en 30 min | Andamiaje |
|---|---|---|---|
| 4-5 años (inicial) | 8-12 min | 3-4 actividades cortas y variadas | Pista visual fuerte y constante |
| 6-7 años (1°-2°) | 12-15 min | 2-3 actividades | Pista fuerte → se retira si acierta 2 veces seguidas |
| 8-9 años (3°-4°) | 15-20 min | 2 actividades + 1 repaso corto | Pista solo a pedido (botón "ayuda") |
| 10-11 años (5°-6°) | 20-25 min | 1-2 actividades profundas | Pista mínima; el feedback explica el POR QUÉ |
| 12 años (7°) | 25-30 min | 1 actividad larga o 2 medianas | Casi sin andamiaje, autonomía |

Esta tabla es directamente el motor de dosificación del feature "Modo
Maestra / Mamá ocupada" (30 minutos según edad) — ya queda lista para usar.

## 2b. Diseño gráfico y verificación de aprendizaje real (investigación adicional, 14-jul-2026)

Pablo pidió explícitamente que la seriedad no fuera solo pedagógica sino
también gráfica, y que "los chicos tienen que aprender de verdad" — dos
preguntas que no había investigado en la primera ronda. Resumen aplicable
(detalle completo y fuentes en `.claude/skills/actividades-progresivas/SKILL.md`
§4b-4c):

### El hallazgo más importante para este negocio puntual

**El "efecto de detalle seductor" está confirmado por meta-análisis: una
ilustración linda pero tangencial al contenido de la actividad EMPEORA la
retención del aprendizaje, aunque haga que el material se vea "más
profesional".** El negocio de Pablo depende de arte IA vistoso — esto no
dice "sacar el arte", dice que el criterio de "¿está bueno este arte?" tiene
que incluir "¿representa el contenido de ESTA consigna puntual, o es
decoración alrededor de ella?". Un personaje del tema haciendo algo ajeno a
la pregunta resta aprendizaje real aunque sume atractivo visual. La
recomendación aplicable: estilo realista cuando el objetivo de la pieza es
enseñar contenido nuevo (ciencias, por ejemplo), estilo cartoon/estilizado
cuando el objetivo es enganche/motivación (portada, festejo, mascota) — no
un único estilo parejo en todo el catálogo por default estético.

### Otros hallazgos de diseño gráfico (accionables)

- **Contraste AAA (7:1), no el AA legal mínimo** — es el estándar de facto
  en educación seria. Ya verificado contra el sistema de paletas actual:
  `ink/card` da 11-13:1 (excelente); `ac` da ~3-3.6:1 pero NUNCA se usa como
  color de texto hoy (confirmado por grep) — correcto tal cual está.
- **Nunca codificar significado solo por color** — siempre con ícono/forma/
  texto acompañando.
- **Tipografía = la letra que el chico está aprendiendo a escribir a mano**
  (formas de una sola vía, b/d bien diferenciadas) — Baloo/Nunito (ya en
  uso) están alineadas con este criterio.
- **Audio-guía es la brecha de UX más urgente para 4-5 años** — más urgente
  que sumar juegos nuevos, porque a esa edad no se puede depender de que el
  chico lea la consigna solo.
- **Targets táctiles ≥48×48dp con ≥64px de separación.**

### Verificación de aprendizaje real: un hueco CONFIRMADO en el motor actual

No es solo teoría — se verificó contra código real. `GAMES.mas_menos`
(`actividades_player.js:1448`) tiene solo 2 grupos para elegir por ronda, y
reintentos ilimitados sin penalización (cero fail states). Un chico puede
"ganar" las 5 rondas tocando sistemáticamente "el que no toqué antes" —
eliminación pura — sin haber entendido nunca qué significa "más" o "menos".
Es EXACTAMENTE el riesgo que anticipa la investigación: cero fail states +
pocas opciones + sin exigir precisión en el primer intento = se puede
completar sin aprender. Esto no invalida "cero fail states" (sigue siendo
correcto, con evidencia real detrás) — significa que cero fail states no
alcanza SOLO, necesita además: (1) suficientes opciones para que adivinar
no sea viable, o (2) distinguir "acertó al primer toque" de "acertó
eventualmente" y solo contar lo primero como dominio real.

**Regla no negociable para toda actividad nueva (y para revisar las
existentes con el tiempo)**: los distractores (opciones incorrectas) tienen
que representar errores conceptuales reales de esa habilidad, no valores al
azar; ninguna actividad da "completado" con un solo acierto, hace falta
precisión sostenida (80-90%, estándar de Bloom's mastery learning) en
preguntas que varíen en cada intento; todo error dispara una explicación
corta del porqué, no solo "¡mal! probá de nuevo".

## 3. Estado real del motor, por tipo de contenido (verificado por código)

| Área NAP | Estado hoy | Evidencia |
|---|---|---|
| Motricidad / discriminación visual (inicial) | ✅ Cubierto | `cuaderno._construir` banda `e<=3`/`e<=5`: colorear, trazos, sombra, iguales, tamaño |
| Matemática básica (conteo, patrón, +/- de un dígito) | ⚠️ Parcial, techo bajo | `_a_sumas`: sumando A 1-4, resultado real ~7-8 (no llega a 10 pese al parámetro `max=10` en la UI) |
| Sílabas, alfabetización, comprensión lectora | ❌ No existe | 0 resultados grepeando fonología/sílaba/sujeto/predicado/ortografía en los 3 archivos |
| Multiplicación, tabla pitagórica, división | ❌ No existe | 0 resultados |
| Fracciones, decimales, porcentajes | ❌ No existe | 0 resultados |
| Geometría (ángulos, perímetro, área, cuerpos) | ❌ No existe | 0 resultados |
| Álgebra, proporcionalidad, estadística | ❌ No existe | 0 resultados |
| Ciencias Naturales (cuerpo, animales, plantas, materia) | ❌ No existe (solo decorativo) | 0 resultados de contenido curricular; los "temas" son estética, no currícula |
| Ciencias Sociales (historia, geografía argentina) | ❌ No existe | 0 resultados |

## 4. Roadmap propuesto (empezando por 4 años, como pidió Pablo)

| Orden | Edad/grado | Tipo de trabajo | Esfuerzo relativo |
|---|---|---|---|
| 1 | Sala de 4 años | ✅ Primer incremento shippeado 14-jul-2026 (§5b): mas_menos con feedback elaborado, juego nuevo `posicion`, `contar` diferenciado por edad. Faltan: audio-guía, auditoría visual completa, versión impresa de `posicion` | Bajo |
| 2 | Sala de 5 años | ✅ Primer incremento shippeado 14-jul-2026 (§5c): `contar`/`mas_menos` con rango ampliado, juego nuevo `silabas` (primera mecánica de audio real del motor). Falta: sonido inicial de vocales, consonantes M/P/S/L, escritura del nombre — quedan fuera de esta primera pasada | Bajo (matemática) / Medio (fonética, mecánica nueva) |
| 3 | 1° grado | ✅ Primer incremento shippeado 14-jul-2026 (§5d): rango de `serie` ampliado a 30 (Bimestre 1), juego nuevo `armar_palabra` (sílabas CV, Bimestre 2). Falta: abecedario, cuerpo humano, animales/plantas, barrio/transportes, efemérides, materiales/luz, "la tiendita" con dinero, grilla 1-100 — construcción nueva, backlog | Medio |
| 4 | 2° grado | Separar de la banda "grande" (hoy comparte banda con 1° y con 12 años); sílabas complejas, cursiva, multiplicación conceptual (arreglos rectangulares), números hasta 1.000 — desglose bimestral ya disponible en `docs/CURRICULUM-NAP-ARGENTINA.md` | Medio |
| 5 | 3° grado | Construir de cero: tabla pitagórica interactiva, números de 4 cifras, cuerpos geométricos, primeras nociones de ciencias naturales/sociales curriculares | Alto |
| 6 | 4°-5° grado | Fracciones (con apoyo visual — tiras, CPA), decimales, geometría con compás, primera historia argentina real (colonia, Revolución de Mayo) | Alto |
| 7 | 6°-7° grado | Porcentaje, proporcionalidad, álgebra informal, estadística, ciencias naturales avanzadas (célula, sistema nervioso/endocrino), historia/geografía argentina contemporánea | Alto |

Los pasos 5-7 comparten un patrón: necesitan tipos de actividad NUEVOS (no
extender parámetros de los 23 que ya existen), así que conviene diseñarlos
recién cuando 1-4 estén validados y haya aprendido de esa primera ronda real.

## 5. Diseño concreto del primer paso: Sala de 4 y Sala de 5 años

Actualizado 14-jul-2026 con el desglose bimestral real que mandó Pablo (ver
`docs/CURRICULUM-NAP-ARGENTINA.md`). Cruzado contra el menú EXACTO de la
banda `"media"` de `actividades_web._menu()` (línea 96-115) — 14 juegos base
+ `sumas` desde los 5 años.

### Sala de 4 años — mapeo bimestre a bimestre

| Bimestre | Contenido NAP | Juego del motor que sirve | Estado |
|---|---|---|---|
| 1 | Conteo oral hasta 5 | `contar` (hoy `max=6`, acotar a 5 en la config del bimestre) | ✅ Listo, solo ajustar parámetro |
| 1 | Tamaños grande/chico | `tamano` | ✅ Listo tal cual |
| 1 | Noción espacial (arriba/abajo, adentro/afuera) | — | ❌ No existe ningún juego de posición espacial |
| 2 | Clasificación por un atributo (color/forma) | `agrupar` (2 canastas — encaja literal) | ✅ Listo, curar qué se clasifica por bimestre |
| 2 | Número y cantidad hasta 3 | `contar` (max=3) | ✅ Listo |
| 3 | Formas círculo y cuadrado | `agrupar`/`diferente` con set curado de esas 2 formas | ⚠️ Necesita curar contenido visual, no motor nuevo |
| 3 | Conteo hasta 10 | `puntos`, `contar` (max ajustado) | ✅ Listo |
| 3 | Longitud largo/corto | `tamano` (mismo mecanismo que grande/chico, reetiquetado) | ⚠️ Reusar el juego con otro par de atributos |
| 4 | El triángulo | mismo criterio que círculo/cuadrado | ⚠️ Curar set visual |
| 4 | Correspondencia uno a uno (un plato por oso) | `sombra` (empareja 1 a 1, pero por SILUETA no por "reparto") | ⚠️ Se acerca conceptualmente, no es idéntico — evaluar si alcanza o hace falta variante |
| 4 | Cuantificadores muchos/pocos | `mas_menos` (`max=6`, YA disponible desde los 4 años en el código — no tiene el gate `e>=5` que sí tiene `sumas`) | ✅ Listo |

**11 de 11 contenidos matemáticos/lógicos de Sala de 4 tienen un juego que ya
sirve o casi sirve — CERO juegos nuevos que construir.** El único contenido
sin ningún camino hoy es la noción espacial arriba/abajo/adentro/afuera
(Bimestre 1) — evaluar si vale la pena un juego chico nuevo o si se puede
dejar fuera de la primera versión.

**Nota de diseño explícita del propio material de Pablo, que hay que
respetar literal:** *"Las actividades interactivas a esta edad deben ser
visualmente limpias, con audio-guía (los chicos no leen todavía) y basadas
en arrastrar, tocar o emparejar."* — el motor hoy NO tiene audio-guía en
ningún juego (confirmado en la auditoría: cero componente de sonido más allá
de efectos de feedback). Antes de vender esto como "para 4 años" con
seriedad pedagógica, agregar consigna leída en voz alta es más importante
que agregar juegos nuevos.

### Sala de 5 años — mapeo bimestre a bimestre

| Bimestre | Contenido NAP | Juego del motor que sirve | Estado |
|---|---|---|---|
| 1 | Conteo oral hasta 15, comparación de colecciones | `contar`, `mas_menos` (`max=8` para edad exacta 5, ampliado 14-jul-2026) | ✅ Listo |
| 1 | Escritura del nombre propio, sonido inicial de vocales | — | ❌ No existe (fonética/escritura — queda para 1° grado) |
| 2 | Conciencia fonológica — sílabas (aplaudirlas) | `silabas` (nuevo, construido 14-jul-2026 — ver §5c) | ✅ Listo |
| 2 | Registro escrito hasta 10 | `contar`/`puntos` con rango ampliado | ⚠️ Ajuste de parámetro |
| 3 | Iniciación a la suma | `sumas` (`max=5`, YA existe específicamente desde los 5 años — `if e>=5` en el código) | ✅ Listo, coincide exacto con el NAP |
| 3 | Consonantes M/P/S/L y rimas | — | ❌ No existe |
| 4 | Escritura espontánea de palabras simples | — | ❌ No existe |
| 4 | Serie numérica 1-10, antes/después | `patron`, `puntos` | ⚠️ Se acerca, curar consigna específica de "antes/después" |

**Sala de 5 es la mitad y mitad**: todo lo MATEMÁTICO ya tiene un juego que
sirve o casi sirve (curación + ajuste de rango, igual que Sala de 4). Todo lo
de LENGUAJE es la introducción real de la conciencia fonológica — y ahí sí
hace falta construcción nueva, con audio, no solo curación. Es exactamente
el patrón que anticipó la investigación pedagógica (sección 2): la
alfabetización necesita mecánica de sonido que hoy no existe en el motor.

### Conclusión y recomendación de secuencia

No arrancar por "Sala de 4 y Sala de 5" como un solo bloque parejo — son dos
tipos de trabajo distintos:

1. **Primero, Sala de 4 completa + la mitad matemática de Sala de 5**: pura
   curación de parámetros y contenido visual sobre los 14 juegos que ya
   existen. Bajo esfuerzo, se puede shippear rápido y aprender el proceso.
2. **Después, el componente de audio/fonética** (conciencia fonológica de
   Sala de 5, y por extensión las sílabas CV de 1° grado que ya estaban en
   el roadmap): esto es un tipo de trabajo nuevo para el motor — el primer
   juego con componente de AUDIO real, no solo visual. Vale la pena tratarlo
   como su propio hito, no colarlo dentro del trabajo de curación.

## 5b. Plan de implementación — Sala de 4 años

### Construido 14-jul-2026 (Pablo: "empecemos... si hay que mejorar las
actividades que hicimos podés hacerlo")

1. ✅ **Arreglado el hueco de "aprender de verdad" en `mas_menos`.**
   Feedback elaborado real (§2b, punto 3 del informe / §4c de la skill): al
   errar, ambos grupos muestran su cantidad en un número grande 1.4s antes
   de dejar reintentar — un anclaje concreto para volver a contar, en vez
   de solo sacudir sin explicar nada. No cambia el criterio de estrellas
   (ya exigía 0 errores para 3⭐, correcto), mejora la CALIDAD del intento
   fallido.
2. ✅ **Construido `GAMES.posicion`** — el único contenido de Sala de 4 sin
   ningún juego (noción espacial arriba/abajo/adentro/afuera, Bimestre 1).
   Una caja de referencia + 2 posiciones CONTRASTANTES del mismo eje por
   ronda (nunca arriba vs. afuera, siempre arriba↔abajo o adentro↔afuera) —
   mismo criterio de distractor-no-al-azar que pide §2b. Agregado a la
   banda `media` de `actividades_web._menu()` (4 y 5 años).
3. ✅ **Diferenciado `contar` por edad exacta, no solo por banda** — Sala de
   4 pide "conteo oral hasta el 5" (NAP); hasta ahora 4 y 5 años
   compartían el mismo `max=6`. Mismo patrón que ya usaba `sumas`
   (`if e >= 5`), extendido con `if e == 4`.
4. ✅ **Audio-guía construido — resultó MUCHO más chico de lo estimado.**
   Las consignas son texto FIJO del player (nunca personalizado por
   compra), así que no hace falta generar audio por token: se graban UNA
   vez, se sirven como asset del repo (igual criterio que `player.js`/las
   fuentes). `actividades_web.generar_audio_consignas()` reusa
   `audiolibro.tts_mp3()` (ElevenLabs Lizy, acento argentino) tal cual
   estaba planeado. Grabadas las 22 consignas de los 15 juegos de la banda
   `media` (924KB total). El player las reproduce automáticamente al
   mostrar cada consigna, respetando el mute que ya existía — best-effort:
   si un texto no tiene grabación, sigue en silencio, nunca bloquea.
   Bug real encontrado y corregido en el camino: el emoji ⭐ (laberinto) no
   entraba en el rango Unicode que se limpiaba antes de mandar el texto a
   la voz — la primera grabación intentaba "leer" el símbolo.
5. Probado en vivo con Playwright (no solo tests unitarios): las 4 mejoras
   funcionan de punta a punta en un navegador real, capturas en la
   conversación.

### Deliberadamente NO hecho en esta pasada (decisión consciente, no olvido)

1. ✅ **Auditoría visual completa contra el "detalle seductor"** — hecha
   14-jul-2026 (los 15 juegos de la banda `media`, uno por uno, código
   real). **Resultado: no hay violaciones reales del principio.** El
   engine ya evita el problema por diseño — en todos los juegos, el sprite
   mostrado es el CONTENIDO directo de la tarea (lo que hay que contar,
   emparejar, clasificar, comparar), no decoración alrededor. Único uso de
   fondo de escena (`D.escena` en `contar`) es funcional (superficie donde
   se apoyan los objetos a contar), no decorativo. `contar` además ya tiene
   un mecanismo de "distractor" DELIBERADO (otro personaje que NO hay que
   contar, con pista visual clara de cuál sí) — discriminación visual
   legítima, no ruido al azar. No hace falta ningún cambio; se confirma
   como fortaleza existente, no como deuda.
2. **Parametrización real por bimestre** — no se construyó un selector de
   bimestre porque hoy NO existe ningún flujo (compra o "Modo Maestra") que
   pida esa información; hacerlo ahora sería plomería sin nada que la use
   todavía. El ajuste de `contar` por edad exacta (punto 3 de arriba) es
   la versión que SÍ tiene un consumidor real hoy — el bimestre exacto
   espera a que "Modo Maestra" exista como feature real.
3. **Equivalente impreso (PDF) de `posicion`** — el juego nuevo hoy es
   solo interactivo web; `cuaderno.py` no tiene un generador `_a_posicion`
   todavía. Verificado que esto NO rompe nada (la card de la galería cae a
   un fallback genérico), pero es trabajo pendiente si se quiere paridad
   completa PDF/web.
4. **Audio-guía solo cubre Sala de 4 (banda `media`)** — las otras bandas
   (`mini`, `grande`) y sus juegos propios (sopa, sudoku, restas, etc.) NO
   tienen consignas grabadas todavía. Extender es mecánico (agregar los
   textos nuevos a `generar_audio_consignas()`, que es idempotente — no
   regenera lo que ya existe) pero hay que hacerlo cuando se aborden esas
   edades. El festejo ("¡Muy bien, {nombre}!") tampoco tiene voz — incluye
   el nombre del perfil, que varía por chico, no es texto fijo grabable de
   la misma manera.

## 5c. Plan de implementación — Sala de 5 años

### Construido 14-jul-2026 (Pablo: "hace merge y continua con 5 años")

1. ✅ **Ampliado `contar`/`mas_menos` para edad exacta 5** — NAP pide "conteo
   oral hasta el 15" y "comparación de colecciones"; antes 4 y 5 compartían
   el mismo `max=6` de la banda `media`. Mismo patrón de diferenciación por
   edad exacta que ya se usó en Sala de 4 (§5b, punto 3): `if e == 5` sube
   `contar`/`mas_menos` a `max=8`.
2. ✅ **Construido `GAMES.silabas`** — la conciencia fonológica (Bimestre 2,
   "aplaudir sílabas") era el único contenido de Sala de 4/5 sin ningún
   camino, y el primer juego del motor que depende de AUDIO real, no solo de
   sprites. Diseño:
   - Banco de 13 palabras (1 a 4 sílabas) con su emoji — **la palabra NUNCA
     se muestra escrita** (a los 5 años todavía no leen; el objetivo es
     ESCUCHAR, no leer). El emoji se muestra como `❓` y solo se revela al
     acertar, como festejo — evita que el chico "adivine por asociación
     visual" en vez de escuchar de verdad (mandato explícito de Pablo:
     "los chicos tienen que aprender de verdad con estas actividades").
   - Distractores por contraste real, no al azar: siempre ±1 sílaba de la
     respuesta correcta (mismo criterio que `posicion` en Sala de 4 — un
     distractor de "6 sílabas" para una palabra de 2 no mide nada).
   - Botón "🔊 Escuchar de nuevo" + reproducción automática de la palabra al
     entrar a cada ronda — reusa `reproducirConsigna()` del sistema de
     audio-guía de Sala de 4 (§5b, punto 4), llamado directo (no vía
     `ctx.consigna()`, que pisaría el texto de instrucción visible).
   - Agregado a la banda `media` SOLO para edad exacta 5 (`if e == 5`), no
     para 4 — a los 4 años el NAP todavía no pide conciencia fonológica.
3. ✅ **QA de audio reforzado — bug real encontrado y corregido en el
   camino.** Al generar las 14 grabaciones nuevas (consigna fija + 13
   palabras del banco), la toma de "MARIPOSA" salió a 0.71s — sospechosamente
   corta contra otras palabras de las mismas 4 sílabas ("ELEFANTE" a 2.22s).
   Verificado que era una toma real apurada/cortada (no un bug de caché,
   comparando el contenido de los archivos) regenerando "MARIPOSA" con 3
   seeds distintos (1.02s / 2.14s / 1.83s) — confirma que 0.71s no era
   representativo. Mismo problema encontrado en "BICICLETA". Solución
   generalizada, no solo parche puntual: `_duracion_minima()` (piso de
   duración por conteo de vocales, proxy de sílabas) + reescritura de
   `generar_audio_consignas()` para reintentar hasta 4 tomas con seeds
   distintas y quedarse con la más larga si ninguna supera el piso — nunca
   vuelve a vender una toma apurada sin darse cuenta.
4. ✅ Probado en vivo con Playwright (no solo tests unitarios): manifest de
   audio carga, la consigna y la palabra se narran solas al entrar a cada
   ronda, "Escuchar de nuevo" repite la palabra, los distractores ±1 no
   revelan el emoji al fallar, acertar revela el emoji correcto con feedback
   positivo, y el juego completa las 5 rondas con el sistema de estrellas
   reflejando los errores cometidos (capturas en la conversación).

### Deliberadamente NO hecho en esta pasada

1. **Sonido inicial de vocales, consonantes M/P/S/L y rimas, escritura del
   nombre propio** (Bimestres 1, 3 y 4) — quedan fuera: son contenido de
   lecto-escritura más cercano a 1° grado que a Sala de 5, y el roadmap
   (§4, paso 3) ya prevé reusar el trabajo de audio de `silabas` para la
   mecánica de sílabas CV de 1° grado. Construirlos ahora sería adelantar
   trabajo de un año que todavía no se diseñó.
2. **Audio-guía de `silabas` en las otras bandas** — igual que en Sala de 4
   (§5b, punto 4 de "NO hecho"), las 14 grabaciones nuevas cubren solo esta
   pieza; extender a `mini`/`grande` sigue pendiente para cuando se aborden
   esas edades.
3. **Equivalente impreso (PDF) de `silabas`** — es un juego 100% de audio,
   no tiene un análogo natural en papel; no se intentó forzar uno.

## 5d. Plan de implementación — 1° grado

1° grado es el primer año donde el trabajo deja de ser 100% curación — el
propio roadmap (§4) ya lo anticipaba como esfuerzo "Medio", no "Bajo" como
Sala de 4/5. Bimestre a bimestre, 1° grado toca CUATRO áreas NAP (Prácticas
del Lenguaje, Matemática, Ciencias Naturales, Ciencias Sociales), no solo los
3 ejes integrados de nivel inicial — y el motor hoy solo tiene contenido real
para Matemática y una pieza de Lenguaje. Este primer incremento se acotó
deliberadamente a esas dos, dejando Ciencias Naturales/Sociales para una
pasada aparte (son construcción de tipos de actividad enteramente nuevos, no
ajuste de los que ya existen — mismo criterio de "no mezclar tipos de
esfuerzo distintos en el mismo sprint" que ya se usó en Sala de 4/5, §5
conclusión).

### Construido 14-jul-2026 (Pablo: "dale", tras confirmar seguir con 1° grado)

1. ✅ **Rango de `serie` ampliado para 1° grado** — NAP Bimestre 1: "números
   del 1 al 30", "anterior y posterior en un tablero". `serie` (¿qué número
   falta en la secuencia?) YA hacía exactamente esto pero con techo fijo
   ~16; se agregó `cfg.tope` (default 16, retrocompatible con toda otra
   edad/banda que no lo pase) y se fijó en 30 solo para edad exacta 6.
   Verificado en vivo: la secuencia llega a números en el rango 20+ donde
   antes topeaba ~16.
2. ✅ **Construido `GAMES.armar_palabra`** — NAP Bimestre 2: "sílabas
   directas (consonante+vocal)... construir palabras arrastrando sílabas
   desordenadas (ej. PE-LO-TA)", idea que el propio Pablo ya había traído.
   Diseño:
   - Banco de 7 palabras CV-CV o CV-CV-CV con emoji (GATO, LUNA, CASA, SAPO,
     MOTO, PATO, PELOTA) — reusa el pipeline de audio de `silabas` (Sala de
     5); GATO/LUNA/CASA/PELOTA ya tenían grabación, se generaron 3 nuevas
     (SAPO, MOTO, PATO) + la consigna nueva.
   - **Sin drag real — TAP en orden** (mismo criterio de robustez mobile que
     `agrupar`, documentado en su propio comentario del código: "tap, sin
     drag — más robusto en mobile"). Las sílabas se muestran mezcladas como
     botones; tocar la siguiente en secuencia la "coloca" en el primer hueco
     vacío de arriba; tocar una fuera de orden sacude sin colocar nada
     (cero fail states, igual que el resto del motor).
   - Sin distractores: TODAS las sílabas mostradas pertenecen a la palabra
     — el desafío es la SECUENCIA, no filtrar sílabas ajenas (a diferencia
     de `silabas`, que sí necesita distractores de cantidad).
   - Agregado a la banda `grande` SOLO para edad exacta 6 (no se filtra a
     edades mayores que comparten la misma banda).
3. ✅ **Bug real de QA de audio encontrado y corregido — el espejo del bug
   de Sala de 5.** "SAPO" (2 vocales, esperable ~0.7-1s como GATO/PATO/MOTO)
   salió en una toma de 2.72s — el piso de duración (`_duracion_minima`,
   Sala de 5) no lo agarra porque 2.72s NO es una toma corta, es una toma
   RARA/larga. Verificado real regenerando con 3 seeds distintos (1.02-1.67s
   en las alternativas, ninguna cerca de 2.72s). Solución generalizada, no
   parche puntual: `_duracion_maxima()` (techo simétrico al piso, mismo
   proxy por vocales) + reescritura de `generar_audio_consignas()` para que
   el criterio de "mejor toma" sea la distancia al rango `[mínimo, máximo]`
   en vez de solo "la más larga" — agarra tomas cortadas Y tomas raras de
   más, cualquiera de las dos.
4. ✅ Probado en vivo con Playwright: `armar_palabra` completa rondas con
   sílabas en el orden correcto Y rechaza (sacude, no coloca) sílabas fuera
   de orden; `serie` alcanza números 20+ donde antes topeaba ~16. Sin errores
   de consola. Suite completa en verde.

### Deliberadamente NO hecho en esta pasada

1. **Ciencias Naturales (cuerpo humano, animales por alimentación/cobertura,
   plantas) y Ciencias Sociales (la escuela, el barrio, transportes,
   efemérides)** — de los 4 bimestres de 1° grado, son contenido curricular
   enteramente nuevo para el motor (hoy CERO tipos de actividad de ciencias
   reales, confirmado en el hallazgo principal §1) — construcción de cero,
   no curación; se deja para una pasada dedicada, mismo criterio que separó
   Sala de 4 (curación) de 3°+ grado (construcción) en el roadmap original.
2. **Abecedario / orden alfabético, escritura del nombre propio y de
   compañeros** (Bimestre 1) — necesita un tipo de actividad nuevo
   (ordenar/reconocer letras), no un juego existente curado.
3. **"La tiendita" con billetes/monedas de fantasía y la grilla numérica
   1-100** (Bimestre 4, números hasta 100) — el mecanismo CONCRETO de
   `sumas`/`restas` (sprites contables uno por uno) no escala a 100 objetos
   en pantalla; el propio NAP sugiere dinero de fantasía como paso
   PICTÓRICO/simbólico (Singapore Math CPA) para números grandes — es un
   juego nuevo, no una extensión de parámetro de los que ya existen.
4. **Audio-guía de `armar_palabra`/`serie` en las otras bandas** — mismo
   patrón que Sala de 4/5: las grabaciones nuevas cubren solo esta pieza.
5. **Equivalente impreso (PDF) de `armar_palabra`** — no se intentó forzar
   un análogo en papel para un juego pensado para tap-en-orden.

## 6. Pendientes que dependen de Pablo (no técnicos)

1. ~~Desglose bimestral de 4° grado~~ — completado 14-jul-2026. El currículum
   de los 9 años de escolaridad ya está completo en
   `docs/CURRICULUM-NAP-ARGENTINA.md`.
2. Decisión de alcance: ¿el feature "Modo Maestra" (30 min) es un producto
   nuevo con su propio precio, o una forma nueva de comprar/generar lo que
   ya existe (actividades imprimibles / actividades-web)?
3. Validar si de verdad conviene ir grado por grado en orden, o si hay algún
   año con más demanda de mercado (ej. jardín/1er grado, por ser la franja
   etaria del cumpleaños infantil que ya es el core del negocio) que
   convenga priorizar aunque no sea el primero cronológicamente.
