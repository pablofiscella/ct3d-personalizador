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
| 2 | Sala de 5 años | Mitad curación (matemática) + primer trabajo de audio/fonética (conciencia fonológica) — ver §5 | Bajo (matemática) / Medio (fonética, mecánica nueva) |
| 3 | 1° grado | Ampliar rango numérico real (hoy tope ~7-8, NAP pide hasta 100) + agregar mecánica de sílabas CV (juego nuevo: "armar palabras arrastrando sílabas", idea que el propio Pablo ya trajo) — reusa el trabajo de audio de Sala de 5 | Medio |
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
| 1 | Conteo oral hasta 15, comparación de colecciones | `contar`, `mas_menos` (rango a ampliar — hoy tope 6) | ⚠️ Necesita ampliar el `max` para esta banda |
| 1 | Escritura del nombre propio, sonido inicial de vocales | — | ❌ No existe (fonética/escritura — confirma el hueco de mecánica que ya señaló la investigación pedagógica) |
| 2 | Conciencia fonológica — sílabas (aplaudirlas) | — | ❌ No existe — necesita audio, es la pieza más nueva a construir |
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
4. Probado en vivo con Playwright (no solo tests unitarios): las 3 mejoras
   funcionan de punta a punta en un navegador real, capturas en la
   conversación.

### Deliberadamente NO hecho en esta pasada (decisión consciente, no olvido)

1. **Audio-guía** — sigue siendo la brecha de UX más urgente identificada
   (§2b), pero es un trabajo grande de verdad (integrar TTS, generar/cachear
   audio por consigna, cambios de UI del player) que merece su propio
   hito enfocado, no una tarea more agregada a esta tanda. `audiolibro.py`
   ya tiene el motor de voz (ElevenLabs, acento argentino) — reusar ese
   mismo camino cuando se aborde.
2. **Auditoría visual completa de las 11 piezas de Sala de 4 contra el
   "detalle seductor"** (§2b) — no se revisó imagen por imagen todavía si
   hay decoración tangencial en `agrupar`/`diferente`/etc. Queda para la
   próxima pasada.
3. **Parametrización real por bimestre** — no se construyó un selector de
   bimestre porque hoy NO existe ningún flujo (compra o "Modo Maestra") que
   pida esa información; hacerlo ahora sería plomería sin nada que la use
   todavía. El ajuste del punto 3 de arriba (edad exacta, no bimestre) es
   la versión que SÍ tiene un consumidor real hoy — el bimestre exacto
   espera a que "Modo Maestra" exista como feature real.
4. **Equivalente impreso (PDF) de `posicion`** — el juego nuevo hoy es
   solo interactivo web; `cuaderno.py` no tiene un generador `_a_posicion`
   todavía. Verificado que esto NO rompe nada (la card de la galería cae a
   un fallback genérico), pero es trabajo pendiente si se quiere paridad
   completa PDF/web.

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
