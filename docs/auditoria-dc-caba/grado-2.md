# 2° grado (7 años)

Dossier definitivo del cuaderno de actividades interactivo para 2° grado, contra el DC 2024 CABA. Integra la auditoría curricular externa, la propuesta de diseño y la devolución del panel revisor (maestra de 2°, alumno de 7 años, auditor pedagógico externo). Donde el panel señaló defectos válidos, el mapa ya viene corregido; la sección 5 lista qué se ajustó y qué se descartó con motivo.

---

## 1. Estado actual — veredicto de auditoría (tabla por juego + los 5 gaps más graves)

El menú actual de 2° ofrece 25 juegos. Solo 6 tienen anclaje curricular real en el grado (24%), y 4 de esos dependen de bancos de 10 ítems que se agotan en una sola partida. Un tercio del menú es material de jardín o de 1° sin recalibrar. El mecanismo de escalado (`if e == 7` sobre 17 juegos base compartidos e idénticos de 1° a 7°) produce exactamente este cuadro.

| # | Juego | Config a los 7 | Veredicto | Justificación (DC 2024) |
|---|-------|----------------|-----------|--------------------------|
| 1 | memotest | 8 pares | SIN ANCLAJE | Memoria visual pura; no figura en ningún eje de 2°. |
| 2 | laberinto | 9×9 a 12×12 | SIN ANCLAJE | El eje Espacio pide comunicar/interpretar posiciones y desplazamientos con instrucciones y planos; arrastrar hasta la estrella no lo hace. |
| 3 | programar_camino | 3 niveles 3×3/4×4 | ALINEADO (parcial) | Cubre secuencias de robot en el plano, pero omite bucle y condición si/entonces (nodales de 2°); es prototipo. |
| 4 | sopa | 10×10, 8 direcciones | MUY DIFÍCIL | Palabras de 10 letras, invertidas y en diagonal, para un lector calibrado en textos de ~100 palabras; es la misma sopa que ve un chico de 12. |
| 5 | sudoku | 4×4 caras | SIN ANCLAJE | Lógica de restricciones no está en 2°; dificultad tolerable, no enseña nada del grado. |
| 6 | sumas | max=10 | MUY FÁCIL | El nodal es "sumas que dan 100 y 1.000" y redondos de tres cifras; resultado ≤10 es de 1°. |
| 7 | restas | max=10 | MUY FÁCIL | El DC pide menos 1/10/100 y redondos de tres cifras; minuendo ≤10 es de 1°. |
| 8 | serie | tope=16, paso +1/+2 | MUY FÁCIL (bug objetivo) | El nodal pide escalas de 10/20/50/100 hasta 1.000; el juego llega a 16 — y 1° recibe tope 30: 2° ve números más chicos que 1°. |
| 9 | patron | nivel 3 (ABC/AABB) | DESALINEADO (inicial) | Patrones de sprites no figuran en 2°; es de inicial/1°. |
| 10 | puntos | estrella 10, corazón 14 | MUY FÁCIL | Serie hasta 14 con dominio del grado en ~1.000; estrella/corazón no son las figuras del DC. |
| 11 | contar | max=9 | MUY FÁCIL | "Conteo y comparación de grandes colecciones"; contar hasta 9 es de sala de 5 (el motor da max=8 a los 5). |
| 12 | colorear | libre | SIN ANCLAJE | Juego libre idéntico en todas las edades. |
| 13 | mas_menos | max=9 | MUY FÁCIL | El indicador de 2° es comparar números de dos y tres cifras; comparar colecciones ≤9 es de inicial. |
| 14 | simon | 5 colores | SIN ANCLAJE | Único juego base que escala por grado, pero no trabaja contenido del DC. |
| 15 | agrupar | matching de idénticos | DESALINEADO (inicial) | Emparejar idénticos es de sala de 2-3; el DC de 2° agrupa por sinónimos/antónimos/familias, nunca por identidad visual. |
| 16 | quefalta | 5 ítems, 2,2 s | SIN ANCLAJE | Memoria de trabajo visual; sin eje. |
| 17 | bingo | grilla 9, pista con imagen | SIN ANCLAJE | Escaneo visual que ni exige leer. |
| 18 | sustantivos | banco 10 | ALINEADO (con reservas) | Propios/comunes es ampliación (apoya la mayúscula nodal); banco de 10 se agota en una partida; la mayúscula de "Rex" regala la respuesta. |
| 19 | sumas_redondas | formá 100/200/300 | ALINEADO | Cubre "sumas que dan 100"; falta llegar a 1.000 (explícito en el DC) y no hay versión resta. |
| 20 | sinonimos_antonimos | banco 10 | ALINEADO | Nodal; distractores-trampa bien diseñados; banco de 10 se agota. |
| 21 | multiplicacion_concepto | 2-5 × 2-4 | ALINEADO | Calca el nodal "sumas reiteradas y signo ×"; rango correcto para el año de introducción. |
| 22 | conductor_aislante | banco 10 | DESALINEADO (otro grado) | El eje de ciencias de 2° es la LUZ y los materiales (opaco/traslúcido/transparente); la conducción del calor no está en 2°. |
| 23 | familia_palabras | banco 10 | ALINEADO (calibración floja) | Nodal, pero distractores sin relación (PAN → ZAPATO) se resuelven por descarte sin mirar la raíz. |
| 24 | trivia_espacial | día/noche | DESALINEADO (de 1°) | El cielo diurno/nocturno es de 1°; 2° pide distinguir fuentes lumínicas de objetos que no emiten luz. |
| 25 | tablas_contrarreloj | {2,5,10} × 1-10, 6 s | DESALINEADO (adelanta 3°) | El DC deja la tabla pitagórica y su memorización para 3°; contra reloj el año en que el concepto recién se presenta. |

**Conteo:** 6 ALINEADO (2 con reservas serias) · 6 MUY FÁCIL · 1 MUY DIFÍCIL · 5 DESALINEADO · 7 SIN ANCLAJE.

### Los 5 gaps más graves

1. **Dígrafos + opacidades ortográficas (Lengua)** — el contenido insignia de 2° (ll/ch/qu/gu/rr; b/v, s/c/z, y/ll, g/j; mb/nv; h), trivialmente gamificable, ausente por completo. El panel sumó un sexto integrante del mismo eje: **separación entre palabras** ("mimamá", "selo dije"), nodal del DC y el error de escritura más frecuente del grado.
2. **Rango numérico a 1.000 + valor posicional (Matemática)** — todo el cálculo del menú opera ≤16 salvo sumas_redondas; el salto a tres cifras que define el grado no existe.
3. **Comprensión lectora de textos (Lengua)** — en el grado cuyo objetivo es consolidar la lectura, el producto no ofrece nada para leer más largo que una palabra.
4. **Repertorio aditivo real y algoritmos intermedios (Matemática)** — sumas/restas max 10 es la única oferta aditiva general; el DC pide llegar a 100/1.000 con estrategias.
5. **Luz y materiales (Conocimiento del Mundo)** — el único eje de ciencias naturales del grado, sin actividad, mientras el menú gasta dos slots en contenido de otros grados (calor, día/noche).

Mención inmediata: **bucle y condicional en TDyP** (la novedad formal de 2°, con programar_camino como vehículo natural) y el menú que se contradice a sí mismo (sumas_redondas opera con 100-300 mientras sumas da 3+4; multiplicacion_concepto introduce lo que tablas_contrarreloj exige automatizado).

---

## 2. Mapa propuesto del año (números totales; tabla por área/eje)

Convenciones: en los ítems de ejemplo, la **primera opción en negrita es la correcta**; los distractores llevan entre paréntesis el error conceptual real que representan. "Paramétrica" = ítems infinitos desde plantillas con rangos por nivel y **guardas de colisión obligatorias** (distractor ≠ correcta, sin duplicados, sin negativos, sin cruzar el tope 1.000). "Banco" = ítems manuscritos y verificados. Todas las actividades de sistema de escritura son fonética CON AUDIO (regla NRP): dependen de `generar_audio_consignas`; sin ese audio NO se publican.

### Números totales

| Área | Actividades curriculares | Composición |
|---|---|---|
| Lengua | **19** | 16 nuevas (se suma L19 separación de palabras, pedido de la maestra) + 3 existentes endurecidas |
| Matemática | **18** | 12 nuevas + 5 recalibradas de existentes (serie, sumas_redondas, mas_menos, bingo, puntos) + 1 mantenida ampliada (multiplicacion_concepto) |
| Conocimiento del Mundo | **7** | 7 nuevas: C1-C6 + C8 plantas; C7 geoformas queda como extra SIN cómputo curricular hasta reformularse; salen del grado conductor_aislante y trivia_espacial |
| Tecnologías, Diseño y Programación | **4** | 3 nuevas + 1 endurecida (programar_camino) |
| Transversales | **3** (+1 gateada) | residuos, plato GAPA, señales viales; ESI-autoprotección gateada a revisión especialista |
| **Total curricular** | **51** | |
| Recreo (sin cómputo curricular) | 7 | memotest, colorear, sudoku, simon (modo infinito), quefalta, laberinto, sopa recalibrada |
| Modos de sistema | 2 | "Desafío de la semana" (repaso mixto interleaved sobre todo lo dominado) y modo "Encontrá el error" (reusa el 100% de los bancos, sube el nivel cognitivo) |

### Reglas selladas del sistema (correcciones del auditor, van hardcodeadas)

- **Dominio:** a lo sumo **1 error en una sesión de 8-10 ítems** (equivale a ≥87,5-90%; corrige el "≥85% = 8-9 de 10" que era aritméticamente falso), al primer intento, en **dos sesiones no consecutivas separadas ≥2 días**, sobre **ítems no vistos o con superficie cambiada**. El motor lo verifica de verdad: los ítems que recibieron feedback solo pueden reaparecer en repasos ≥3 semanas después.
- **Pista:** ítem respondido tras pedir pista **sale del cómputo de dominio** (ni acierto ni error). Sin esta regla toda la métrica quedaba comprometida.
- **Remediación:** tras 2 sesiones fallidas de una actividad → bajar a N1, reactivar el apoyo pictórico y activar el prerrequisito. "El menú insiste" sin cambiar nada es grind, no andamiaje, y era el fail state de progresión del chico que más lo necesita.
- **Entrada a mitad de año:** los bimestres se desanclan de los meses (son bloques B1-B4) y una **sesión diagnóstica de colocación** (10-12 ítems ancla de B1/B2) posiciona al chico que compra en agosto. Es la experiencia de compra de la mayoría de los clientes.
- **Strands paralelos:** el menú ofrece siempre al menos 1 actividad de numeración + 1 de otro eje, y el chico elige el orden dentro del set activo. Mitiga el riesgo de "pagué geometría y nunca llegó" y respeta el pedido del alumno de elegir.
- **Anti-monotonía:** el menú nunca sirve 3 trivias seguidas; intercala mecánicas (ordenar, clasificar, construir, matching). Pedido textual del alumno, coincide con la literatura de variedad de práctica.
- **Capa de motivación (chatarra cero, costo bajo):** racha de días, mapa de progreso con estados visibles "en camino / casi / dominado" (el criterio duro se mantiene interno), récord personal ("ayer 7/10, hoy 9/10"), monedas cosméticas (caritas de sudoku, colores, gorro del laberinto) y cierre de sesión con cofre/sonido. Nada de esto toca la pedagogía; todo responde al pedido del alumno y al R-4 del auditor (el 9/10 sin estados intermedios era un fail state motivacional).
- **Tablero para padres:** reporte de dos líneas por semana desde la telemetría de dominio que ya existe por diseño ("Esta semana dominó el valor posicional con 3 cifras; le cuesta la resta de 100"). La feature de valor percibido más barata del proyecto.

### Dimensionamiento honesto

51 actividades × 5-7 sesiones (3-4 de dominio + 2-3 repasos espaciados) ≈ **260-360 sesiones-actividad**. A 2 actividades curriculares por día de uso (~25-30 min con recreo en el medio), el mapa cubre un ciclo lectivo completo a 3-4 días/semana **con margen** — ya no "cierra exacto" con la punta optimista, que era la sobreventa del ~20% que marcó el auditor. Con la adherencia hogareña realista (1-2 días/semana), los strands paralelos garantizan que igual se toquen todos los ejes. Bancos: **mínimo real 30 ítems, insignia 40** (L2, M8, L7), nivelados N1/N2/N3; los techos menores se documentan caso por caso.

### LENGUA

| ID | Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|---|
| L1 | Fichas de sonido | Audio dice la palabra; tap-selección entre 3 escrituras (N1-N2); constructor: ordenar fichas-sílaba CON fichas-distractor no usadas (qui/ki, que/ke) para que las bisílabas no sean binarias | 30, cargado **70/30 hacia qu/gu/rr y la u muda de gue/gui** (ch/ll vienen sabidas de 1°) | Bisílabas de un dígrafo → trisílabas con dos dificultades → constructor | Dígrafos ll, ch, qu, gu, rr |
| L2 | ¿Con cuál va? | Audio + tap-selección entre 3 escrituras; palabras con DOS puntos de opacidad (dos distractores reales) | **40 (insignia)** | Una opacidad doble (b/v + s/c en la misma palabra) → dos combinadas → sin imagen de apoyo | Opacidades b/v, s/c/z, y/ll, g/j. Ítem: audio "cebolla" → **cebolla** \| seboya (seseo + y/ll) \| sebolla (solo s/c) |
| L3 | Suena fuerte, suena suave | Audio en contexto de oración (pares mínimos solo se distinguen así) + tap-selección de 3 | 30 | Par mínimo con dibujo → sin dibujo → regla contextual pura | r-rr, que/qui, gue/gui. Ítem: "Ese anillo es muy caro" → **caro** \| carro (rr cambia la palabra: par mínimo real) \| calo (sustituye r por l: error fonológico documentado) |
| L4 | Detective mb, nv y h | Audio + tap-selección de 3 | 30 | mb/nv → h → combinadas | -mb-, -nv-, palabras con h. Ítem: **bombero** \| bonbero (n antes de b) \| bonvero. Ternas validadas contra cuadernos reales antes de escribir el banco (se retiran "chiquo"/"karo": fabricados; entra "qeso" — qu sin u — que sí es frecuentísimo) |
| L5 | La sílaba fuerte | Tocar la sílaba tónica sobre fichas; modo contar con **ventana variable** ({n−2,n−1,n}, {n,n+1,n+2}…) para matar el exploit de la mediana; **agudas solo trisílabas o más** (café bisílaba era binario) | 30 | Graves → agudas → esdrújulas para ENSEÑAR; el **dominio se mide sobre listas mixtas** (el bloqueo puro acreditaba la heurística "toco la penúltima") | Sílabas, sílaba tónica, acentuación de palabras frecuentes |
| L6 | Ponele los signos | Oración con huecos; tocar el signo correcto; audio da la entonación; N3: tocar DÓNDE van mayúscula/punto sin huecos marcados | 30 | ¿? vs ¡! con audio → coma en enumeración → mayúscula/punto libres | Mayúscula inicial, punto final, ¿? ¡!, coma |
| L19 | Palabras bien separadas (**NUEVA, pedido de la maestra**) | Audio + elegir entre 3 segmentaciones escritas | 30 | Dos palabras ("mi mamá") → tres → clíticos ("se lo dije / selo dije / se lodije") | "Separación entre palabras" — nodal del DC y el error de escritura n°1 del grado; Tier 2 puro sobre la trivia existente |
| L7 | Leé y descubrí | Texto renderizado (60→100 palabras) + trivia de 4 preguntas servidas desde un **pool de 6-7 por texto** (blindaje anti-memoria); botón de audio DESPUÉS de intentar leer; **disponible desde B1 para el que ya lee** (strand lectura) | 12 textos × 6-7 preguntas ≈ **75-84 ítems (insignia)** | 60 palabras y explícitas → 100 palabras, implícitas y secuencia | Comprensión: información explícita/implícita, secuencia, personaje/conflicto/plan, emociones; indicador "lee textos de ~100 palabras". Los 12 textos salen también como **mini-biblioteca imprimible** (pedido n°1 de las familias) |
| L8 | Armá el cuento | Ordenar 4-5 tarjetas de texto; **N1-N2 con conectores temporales (andamiaje), N3 SIN conectores** (con ellos el orden se resolvía por léxico, no por estructura); superficie paramétrica: mismo esqueleto causal, cambian protagonista y objetos (perro/hueso → ardilla/bellota) | 12 esqueletos × 2-3 superficies ≈ 30 rondas | Con conectores → sin conectores; el primer intento se computa sobre las decisiones reales (la última tarjeta es gratis) | Estructura narrativa: situación inicial, conflicto, acciones, desenlace |
| L9 | Ordená los pasos | Ordenar 4-5 pasos escritos (recetas, fabricación); misma parametrización de superficie que L8; primer intento sobre decisiones reales o 5 tarjetas | 15 esqueletos × variantes ≈ 30+ rondas | 4 pasos → 5 con trampa de deseo ("servir" tentador antes de tiempo) | Orden lógico de las acciones en un texto instructivo |
| L10 | ¿Qué texto es? | Clasificar fragmentos renderizados en 3 categorías que rotan por ronda | 30 | Receta/invitación/publicidad → señal/etiqueta/noticia | Tipos textuales: publicidades, etiquetas, instrucciones, señalética |
| L11 | Buscá el dato | Documento CSS (invitación, envase, cartel) con zonas tocables; consigna pide UN dato | 12 documentos × 3 consignas = 36 | Dato directo → dato de formato parecido como trampa → sellos/advertencias | Información relevante según tipo de texto (dirección/horario; precios, sellos, octógonos) |
| L12 | Conectores | Oración con hueco + trivia 3 opciones | 30 | y/e/ni → o/u (regla ante o-) → temporales | Conectores copulativos, disyuntivos y temporales |
| L13 | El tiempo del verbo | Clasificar oraciones en 3 franjas (AYER/HOY/MAÑANA) | 30 | N1 con adverbio → N2 sin adverbio (decide la desinencia) → N3 con "hoy"+pretérito, **subconjunto a validar en campo** antes de construir el nivel entero (el auditor objetó la teoría del distractor; "hoy comí" es gramatical y frecuente en rioplatense) | Presente, pasado y futuro |
| L14 | Nombra, describe o es acción | Clasificar la palabra **pintada DENTRO de una oración** ("El brillo del sol me molesta") — la palabra suelta era trampa mal puesta: "brillo"/"salta" son ambiguas fuera de contexto (fix de la maestra) | 30 | Función evidente → familias de la misma raíz en rondas distintas (fuerza mirar la función, no el significado) | Palabras que nombran, describen e indican acciones |
| L15 | ¿Afirma, niega, pregunta o exclama? | Trivia 4 botones; N1 oración escrita con signos + audio; N3 SOLO audio (decide la entonación) — **gateado a QA humano de entonación** del TTS; si no pasa, se degrada a N2 sin culpa | 30 | Con signos y audio → sin signos → solo audio | Oraciones que afirman, niegan, preguntan, exclaman |
| L16 | sinonimos_antonimos (endurecida) | La existente; distractores-sinónimo en antónimos ya bien diseñados: se conservan como plantilla | 10 → 30, nivelado N1-N3 | Frecuentes → matices | Sinónimos y antónimos (nodal) |
| L17 | familia_palabras (endurecida) | La existente con distractores nuevos: mismo campo semántico (PAN→**panadería** \| masa) o parecido ortográfico (pino); nunca más ZAPATO/ESCUELA | 10 → 30 | Familias transparentes → raíces con cambio (nieve/nevar) | Familias morfológicas y campo semántico |
| L18 | ¿Dónde van las mayúsculas? (ex sustantivos) | **Multi-select**: oración completa en minúsculas, "tocá TODAS las palabras que van con mayúscula" (6-8 palabras; azar <5%) — el rediseño "¿va con mayúscula? sí/no" introducía un binario y se descartó | 30 oraciones | Nombre propio único → propio + inicio de oración → trampas (día de la semana, "río" común vs "Río Negro") | Sustantivos propios y comunes (ampliación) al servicio de la mayúscula (nodal) |

*Fuera del player y declarado en la ficha con botón visible: trazado de cursiva → cuaderno imprimible (cada sesión de Lengua cierra con UNA consigna de cuaderno: "escribí en cursiva las 3 palabras que acertaste hoy" — yapa de la maestra, adoptada). Oralidad productiva y lectura en voz alta evaluada: fuera de esta versión (exigen grabador y evaluación); es la inversión futura más pedida por el propio alumno. L2 y L4 se comunican a las familias como "dictado sin pelearse" — puente que la familia entiende.*

### MATEMÁTICA

| ID | Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|---|
| M1 | Serie con saltos (ex `serie`) | Completar serie, recalibrada; corrige el bug tope 16 < tope 30 de 1° | Paramétrica con guardas | +10/+100 desde redondos → +20/+50 → descendentes cruzando centenas | Escalas de 10/20/50/100 hasta ~1.000. Ítem frontera: 480, 490, ___ → **500** \| 510 (arrastra el paso viejo tras cruzar — reemplaza al "410 invierte cifras", que era perceptual y no de escala) \| 600 (salta a la centena) |
| M2 | Cajero de cienes, dieces y unos | Multi-tap de billetes (100/10/1) hasta armar el número; contador visible; **capa diagnóstica de estados de error** (detecta que armó 370 pidiendo 307 y explica el cero posicional) — presupuestada completa en Tier 3, no era "la mitad chica" | Paramétrica | 2 cifras → 3 cifras con cero intermedio → equivalencias ("140 usando SOLO dieces" recién en N3, posterior a la composición canónica: exige el reagrupamiento que M5 evita) | Valor posicional: composición/descomposición en unos, dieces y cienes con dinero — EL hito conceptual del grado |
| M3 | Formá 100 y 1.000 (ex `sumas_redondas`) | Tocar 2 que sumen el objetivo; modo resta | Paramétrica | Objetivos {100, 500, 1.000}; pares-trampa de magnitud (40/60 en tablero con objetivo 1.000) → 1.000−n·100 | Sumas que dan 100 y 1.000; restas de 100 y 1.000 menos un número |
| M4 | Cálculo redondo (reemplaza `sumas`/`restas`) | Trivia 3 opciones; N1 con billetes del cajero al lado (pictórico CPA), N3 solo números | Paramétrica con plantilla de distractor posicional | ±1/±10/±100 → redondos de tres cifras → redondo+dígito | Cálculo mental: 460+100 → **560** \| 470 (sumó 10) \| 461 (sumó 1) |
| M5 | Suma paso a paso | Multi-paso guiado (cienes → dieces → unos → componer) | Paramétrica | Sin reagrupamiento (nodal) → **N4 opcional CON reagrupamiento, visible y encontrable** (ampliación DC; "las cuentas de llevar" es el pedido n°2 de las familias y "la resta prestando" lo que hace llorar al alumno — existe, marcado como ampliación) | Algoritmos intermedios y convencionales. Ítem: 234+152 → **300/80/6 → 386** \| 30086 (concatena parciales) \| 368 (traspone) |
| M6 | ¿Cuál es mayor? (ex `mas_menos`) | Tres numerales grandes, sin sprites; **bloques de consigna estable dentro de la ronda + audio obligatorio al cambiar** mayor↔menor (la alternancia medía lectura de consigna) | Paramétrica con pares trampa | 2 cifras → 3 cifras → trampas 340/304/289, 99/102 | Comparación de números de dos y tres cifras |
| M7 | Bingo numérico (ex `bingo`) | Grilla de 9 números de 3 cifras; consigna relacional escrita + audio ("tocá el que es cien más que 240") | Paramétrica | ±1/±10/±100 → "está entre" | Relaciones numéricas: uno/diez/cien más o menos, estar entre |
| M8 | Problemas con cabeza | Enunciado breve + (a veces) tocar el dato que sobra + trivia con distractores de estrategia; **semi-paramétrico: rotan nombres y números sobre el mismo esqueleto** (un problema releído se responde de memoria) | **40 esqueletos (insignia)** × superficies | Transformación directa → incógnita en la transformación → dato que sobra | Comparación, transformación con incógnita, datos necesarios/innecesarios. Ítem: "tenía 38, ahora 50, ¿cuántas ganó?" → **12** \| 88 (ve 'ganó' y suma) \| 50 (repite el estado final) |
| M9 | ¿Qué cuenta lo resuelve? | **Rediseñada por binario**: era clasificar en 2 cajas (50% por moneda); ahora trivia de cálculo: "4 paquetes con 6 cada uno, ¿qué cuenta lo resuelve?" → **4×6** \| 4+6 (suma los números que ve) \| 6−4; conecta directo con la escritura multiplicativa de M10 | 30 | "cada uno" evidente → cantidades distintas de contraste → mezclados | Suma vs. multiplicación: sumar cantidades distintas vs. reiterar la misma |
| M10 | Escribilo con × (`multiplicacion_concepto`) | Mantener; ampliar en B4: sumandos 2-6, veces 2-5; modo inverso (4×3 → **3+3+3+3** \| 4+3 \| 4+4+4+4) | Paramétrica | Directo → inverso | Sumas reiteradas, signo × |
| M11 | Tabla proporcional | Completar tabla de 2 columnas; apoyo pictórico N1, abstracto N3; **los ítems inversos (___→20 cuando 1→5) se gatean a M12 dominada** (son partición pura: primero el concreto) | Paramétrica | Directa → salteada → inversa (post-M12) | Multiplicación en contexto de proporcionalidad |
| M12 | Repartí justo | Repartidor uno-a-uno (concreto CPA) + trivia sobre el resultado; **movida a B3 junto a M9/M10** (reparto se enseña con la multiplicación, no un bimestre después) | 30 escenarios | Reparto exacto → con resto → partición ("¿cuántos floreros?") | Reparto equitativo/no equitativo y partición |
| M13 | Doble o mitad | Trivia; **etapa pictórica N1 agregada** (pares de objetos espejados — violaba la regla CPA al ser trivia pura desde N1); timer opcional recién en N3 | Paramétrica | Pictórico ≤10 → abstracto ≤20 → dobles de decenas (35→70) | Dobles y mitades de números sencillos |
| M14 | El plano del aula | Grilla CSS con objetos; consignas de posición (tocar casillero) y trayectos (tocar en secuencia) | 30 consignas / 6 planos | Posiciones → trayectos con condición ("pasando por") → puntos de vista; distractor de vista superior corregido: **vista lateral** (rectángulo con patas) en vez del "círculo" genérico | Planos, posiciones y desplazamientos, puntos de vista |
| M15 | Adiviná mi figura | Trivia con pistas sucesivas; figuras CSS ROTADAS a propósito; **movida a B2** (geometría se intercala todo el año, no es postre) | 30 | Figuras por lados/vértices → cuadrado rotado vs rombo → cuerpos por caras | Triángulo/cuadrado/círculo/rectángulo; cubo, prisma, esfera, cilindro, pirámide, cono |
| M16 | Medí y pesá | Regla y balanza CSS estáticas que se LEEN + trivia; **movida a B3** | 30 | Regla desde 0 → regla que empieza en 2 (EL error) → conveniencia de unidades | Longitud con regla/cinta, peso con balanzas, estimación |
| M17 | ¿Cuántos días dura? | Calendario CSS + trivia; N2 pide tocar inicio y fin; **movida a B1 como rutina de marzo** (pedido de la maestra: el calendario es rutina diaria desde el día uno y engancha con los cumpleaños); N3 opcional: reloj de agujas en punto/y media, marcado AMPLIACIÓN sin cómputo DC (demanda real del aula, pedido del alumno) | 12 escenarios + paramétrica | Duración simple → off-by-one de extremos → semanas | Día, semana, mes y año; calendario para duraciones |
| M18 | Uní los puntos con saltos (ex `puntos`) | Los puntos se numeran con escalas (10, 20, 30… / 50, 100, 150…); mismas figuras, cero assets nuevos | Paramétrica | +10 → +50 → +100 | Escalas (curación barata que vuelve curricular un juego trivial) |

### CONOCIMIENTO DEL MUNDO

| ID | Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|---|
| C1 | Linterna mágica | Clasificar en 3 categorías; la escena muestra el objeto delante de una luz y QUÉ se ve detrás (CSS con opacidades, literal) | 30 | Casos claros → papel manteca ("pasa luz = transparente", el error nuclear) → materiales ambiguos | Materiales opacos, traslúcidos y transparentes — el eje de ciencias del grado |
| C2 | ¿Tiene luz propia? | **3 categorías: emite / refleja / no se ve sin luz** (el binario original se corrigió; "refleja" ES el contenido: Luna, espejo, cartel reflectante); pista a demanda → el ítem sale del cómputo | 30 | Sol/vela/lamparita → Luna y espejo (las trampas centrales) → luciérnaga, pantalla | Fuentes lumínicas vs. objetos que no emiten luz |
| C3 | ¿Cómo se desplaza? | Clasificar (nada/vuela/camina/repta) + matching estructura→movimiento | 30 | Casos claros → pingüino, murciélago (rompen el estereotipo) → doble clasificación | Desplazamiento animal según el medio; la más blanda de CdM (viene sabida de jardín), la rescatan las trampas |
| C4 | ¿Artesanal o industrial? | Clasificar escenas + ordenar etapas de producción | 30 | Escala evidente → "una persona controla la máquina" (el criterio es técnica y escala, no presencia humana) → etapas con trampa | Producción artesanal vs. industrial y sus etapas |
| C5 | La ciudad funciona | Matching necesidad → servicio → trabajador | 30 | Directo → concepciones erróneas ("el agua viene de la lluvia a la canilla") | Servicios urbanos de CABA, trabajos del circuito |
| C6 | ¿Se contagia o no? | Clasificar + trivia de prevención | 30 | Varicela/piojos → celiaquía/diabetes ("se contagia por el mate", a desarmar) → prevención y no-discriminación | Enfermedades contagiosas vs. no contagiosas; celiaquía y diabetes |
| C8 | El germinador (**NUEVA, pedido de la maestra**) | Escenas de plantas + trivia diagnóstica ("esta planta está amarilla y caída, ¿qué le faltó?" → **luz** \| agua \| tierra) + ordenar el ciclo semilla→brote→planta→flor | 30 | Necesidades una a una → diagnóstico combinado → ciclo completo | Crecimiento de plantas: luz, agua, suelo — todos los 2° de CABA hacen el germinador y las familias lo continúan en casa; conecta con L8 ítem 3 |
| (C7) | Geoformas | Clasificar siluetas — **queda FUERA del cómputo curricular** hasta reformularse: la silueta ES la respuesta (matching perceptual, no geografía); reformulación posible: N3 con nombres de lugares sin imagen | 18 (extra) | — | Llanuras, montañas, costas (decorativa por ahora) |

*Sociedad del pasado (feudo/colonia) sigue fuera: el DC deja elegir contexto a cada escuela; una versión única desalinearía con la mitad de las aulas (la maestra lo confirmó). Si se hace, elegible por la familia.*

### TECNOLOGÍAS, DISEÑO Y PROGRAMACIÓN

| ID | Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|---|
| T1 | Programá el camino 2.0 (ex `programar_camino`) | 6 niveles (3×3 → 6×6), botón-evento de inicio ("tocá la bandera"), nivel depuración: programa con UN bloque mal → tocarlo y corregirlo | Niveles diseñados + paramétrica | Secuencias → con evento → depuración | Secuencias de robot en el plano; eventos; depuración (ampliación). Era el juego favorito del alumno y "dura NADA": deja de ser prototipo |
| T2 | Descubrí el bucle | Trivia sobre programas de bloques: elegir el "repetir N veces […]" equivalente; en N3 de T1 el límite de bloques OBLIGA a usar el bucle (restricción real, no decorativa — "me obligan a ser inteligente", dixit el alumno) | 24 + paramétrica | Bucle simple → contar repeticiones vs. bloques (el error central) → bucle + resto suelto | Bucle ("repetir N veces") — nodal NUEVO de 2°, hoy ausente |
| T3 | Si… entonces | Escena del robot + encastrar la condición correcta; **se elimina el ítem "SI manzana Y roja"** (conjunción lógica: fuera del DC de 2° y salto cognitivo serio — coincidieron maestra y auditor) | 24 (techo documentado: condiciones simples relevantes a los 7) | Condición directa → condición invertida como distractor → acción cruzada | Condición si/entonces — nodal nuevo de 2° |
| T4 | ¿Sensor, actuador o estructura? | **3 categorías** (el binario sensor/actuador se corrigió agregando "estructura": rueda sin motor, carcasa, chasis — curricular: el DC habla de "partes y funciones") | 24 (techo documentado: partes reconocibles a los 7) | Pares fáciles → micrófono/parlante (ambos "de sonido": distingue dirección) → botón ("siente que lo tocan") | Robots: partes y funciones; sensores y actuadores |

### TRANSVERSALES

| ID | Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|---|
| X1 | Circuito del residuo | Ordenar secuencia + clasificar en **3 estados**: verde / negro / "verde PERO enjuagado primero" (el binario de 2 tachos se corrigió con contenido genuino de la norma porteña) | 30 | Casos claros → servilleta sucia ("es papel = reciclable", EL error) → enjuague previo | Reciclables/no reciclables, recolección diferenciada, cooperativas de recuperadores |
| X2 | Plato GAPA | Armar el plato multi-tap con la gráfica GAPA visible + clasificar; feedback constructivo sobre plato armado (lógica presupuestada en Tier 3) | 30 | Bebida → octógonos ("de vez en cuando", no prohibición) → armar plato completo | GAPA: variedad, agua, octógonos |
| X3 | Señales viales | Matching señal→significado + trivia de decisión peatonal | 20 (techo documentado: señales relevantes al peatón de 7) | Señales → semáforo en rojo con calle vacía ("esperar igual") → movilidad inclusiva | Normas y señales, rol de peatón, rampas |
| X4 | Decir no y avisar (**GATEADA**) | Escenas + elegir respuesta de autoprotección; **no se publica sin redacción y revisión de especialista** (no negociable, ratificado por todo el panel) | 15 (el especialista define) | — | ESI: "decir no", secretos para contar, personas de confianza |

---

## 3. Cambios al catálogo actual (mantener / endurecer con parámetros / retirar / mover)

| Juego | Decisión | Parámetros / destino exactos |
|---|---|---|
| memotest | MANTENER (recreo) | Sin cómputo curricular. Curación opcional pares palabra↔sprite; **jamás comunicarla como actividad de lectura** (sería reconocimiento visual de palabras, prohibido por la regla NRP). Escalar pares con el uso (el alumno pidió "más de 8"). |
| laberinto | MANTENER (recreo) | e=7: tams [9,10]; 11×11/12×12 para e≥10. **Fix UX**: tolerancia al soltar el dedo en el arrastre (retomar donde se soltó, no reiniciar) — la queja real del alumno era fricción de input, no dificultad. |
| programar_camino | ENDURECER | = T1: 6 niveles 3×3→6×6, evento de inicio, bloque "repetir" (T2 integrado), nivel depuración. Deja de ser prototipo. |
| sopa | ENDURECER (recalibrar A LA BAJA) | e=7: grilla 8×8, palabras 3-7 letras, niveles 1-2 horizontal/vertical de ida, 3-4 suman diagonal de ida; SIN invertidas. Pasa a recreo con valor de vocabulario ("terminar es lo divertido, no empezar"). |
| sudoku | MANTENER (recreo) | 4×4 es correcto a los 7. Caritas nuevas como cosmético comprable con monedas. |
| sumas | RETIRAR de 2° | max=10 es repertorio de 1°. Reemplaza M4. Queda para e≤6. |
| restas | RETIRAR de 2° | Ídem; reemplaza M4 modo resta. El nivel CON reagrupamiento vive en M5-N4 opcional. |
| serie | ENDURECER | = M1: e=7 tope=1000, pasos {10,20,50,100}, descendentes desde N2. Corrige el bug tope 16 < tope 30 de 1°. |
| patron | RETIRAR de 2° | Nivel inicial; queda en bandas mini/media. |
| puntos | ENDURECER (curación barata) | = M18: numerar con escalas. Mismas figuras, cero assets nuevos. |
| contar | RETIRAR de 2° | max=9 es de sala de 5. |
| colorear | MANTENER (recreo) | Válvula de descompresión; colores especiales como cosmético. |
| mas_menos | ENDURECER (convertir) | = M6: tres numerales de 2-3 cifras con pares trampa, sin sprites; bloques de consigna estable + audio al cambiar mayor/menor. rondas=8. |
| simon | MANTENER (recreo) | **Modo infinito con récord personal** (hoy termina en 6 y el chico quiere ver hasta dónde llega). |
| agrupar | RETIRAR de 2° | Matching de idénticos es de sala de 2-3 ("lo hace mi prima de TRES años"). |
| quefalta | MANTENER (recreo) | Bajo costo, sin cómputo. |
| bingo | ENDURECER (convertir) | = M7: grilla de 9 números de 3 cifras, consigna relacional escrita+audio. tam=9 igual. |
| sustantivos | ENDURECER (convertir) | = L18 multi-select: oración completa en minúsculas, "tocá TODAS las que van con mayúscula". Corrige a la vez la mayúscula que regalaba la respuesta (descubierto también por el alumno) y el binario sí/no del primer rediseño. Banco 10→30. |
| sumas_redondas | ENDURECER | = M3: objetivos {100, 500, 1000}, pares-trampa de magnitud, modo resta. |
| sinonimos_antonimos | ENDURECER | = L16: banco 10→30 nivelado; conservar los distractores-trampa como plantilla. |
| multiplicacion_concepto | MANTENER | = M10; en B4 ampliar sumandos 2-6, veces 2-5, modo inverso. |
| conductor_aislante | MOVER a otro grado | El calor no es de 2° (el grado trabaja LUZ). Banco reutilizable donde el DC trate calor y materiales (verificar 3°-4° antes de reubicar). Su slot lo ocupa C1. |
| familia_palabras | ENDURECER | = L17: banco 10→30; distractores de campo semántico (PAN→MASA) o parecido ortográfico (PAN→PINO). |
| trivia_espacial | MOVER a 1° | Día/noche es de 1°; ahí rinde. Su slot lo ocupa C2. |
| tablas_contrarreloj | MOVER a 3° | La memorización contra reloj es de 3° (textual en el DC). Si se conserva algo en 2°: solo {2,10}, factor ≤5, timer 10 s, como **desafío opcional con copita** (no obligatorio — pedido del alumno) y recién con multiplicacion_concepto dominada. |

**Neto: de 25 juegos, 5 se retiran y 3 se mueven (8 salen del grado), 10 se endurecen/convierten (9 a curriculares + sopa recalibrada a recreo) y 7 se mantienen (6 recreo + multiplicacion_concepto curricular). Nada se tira: los retirados sirven a otras edades y los movidos se llevan su banco.**

---

## 4. Progresión del año (4 bimestres)

Los bloques se **desanclan de los meses**: son B1→B4 secuenciales, cada uno con gate de dominio y remediación especificada (2 sesiones fallidas → N1 + pictórico + prerrequisito). La **sesión diagnóstica de colocación** (10-12 ítems ancla) posiciona al que entra a mitad de año. El menú muestra el set activo del bloque (10-14 actividades) + las dominadas en modo repaso espaciado (a la semana, al mes, ≥3 semanas para ítems ya corregidos) + recreo siempre disponible + "Desafío de la semana" desde que hay ≥5 dominadas. Regla de strands: siempre hay a la vista 1 actividad de numeración + 1 de otro eje, y el chico elige el orden. Palancas de dificultad del año: rango numérico (2→3 cifras→composiciones), retirada del apoyo pictórico CPA, longitud/opacidad del texto (60→100 palabras; explícito→implícito), retirada del andamiaje.

**B1 — Consolidar la base.** Lengua: L1 dígrafos (70/30 hacia qu/gu/rr), L5 sílaba fuerte, L6 signos N1 (mayúscula/punto), **L19 separación de palabras**; L7 N1 disponible como strand de lectura para el que ya lee (la maestra: "el que lee necesita leer desde marzo"). Matemática: M1 serie (+10/+100), M6 cuál es mayor, M2 cajero N1 (2 cifras), M3 formá 100, **M17 calendario como rutina** (cumpleaños, "¿cuántos faltan?"). CdM: C2 luz propia. TDyP: T1 niveles base. Transversal: X3 señales. Es el bloque de diagnóstico: lo que no se domina acá se remedia antes de abrir B2. Fast-track opcional: el tercio avanzado puede adelantar L2.

**B2 — El salto a tres cifras y a leer textos.** Lengua: L7 núcleo (60-80 palabras), L8 armá el cuento, **L2 opacidades** (con pares de doble opacidad desde el arranque — resuelve la contradicción "solo b/v" que dejaba un distractor fabricado), L3 r-rr/que-qui, L12 conectores. Matemática: M2 cajero N2-N3 (3 cifras, cero intermedio), M4 cálculo redondo, M5 suma paso a paso, M13 doble/mitad (con etapa pictórica), **M15 figuras** (geometría se intercala, no es postre). CdM: C1 linterna mágica, **C8 germinador**. TDyP: T2 bucle. Repaso espaciado de todo B1.

**B3 — Multiplicación completa y tipos de texto.** Lengua: L10 qué texto es, L11 buscá el dato, L13 tiempo del verbo, L14 clases de palabras (en oración), L4 mb/nv/h. Matemática: M8 problemas, M9 qué cuenta lo resuelve, M10 escribilo con ×, **M12 repartí justo** (pegada a la multiplicación, como se enseña), M11 tabla proporcional (ítems inversos recién con M12 dominada), **M16 medida**. CdM: C3 desplazamiento, C5 la ciudad funciona. TDyP: T3 si/entonces (sin AND). Transversal: X1 residuos.

**B4 — Integración y cierres.** Lengua: L15 afirma/niega/pregunta/exclama, L9 instructivos, L16-L18 a pleno, L7 en N3 (100 palabras, implícitas). Matemática: **solo 3 nuevas** — M14 plano, M3 formá 1.000, M18 puntos con saltos — más ampliación de M10 y M5-N4 opcional; los repasos espaciados de todo el año pesan más que lo nuevo. CdM: C6 contagia, C4 artesanal/industrial (+C7 como extra). TDyP: T4 sensor/actuador/estructura, T1 depuración. Transversal: X2 plato GAPA. El "Desafío de la semana" interleaved es el corazón del bloque.

*El B4 original tenía 18 estrenos (7 de matemática, con el eje completo de espacio/forma/medida): era un embudo que garantizaba que el comprador nunca viera la geometría que pagó. Redistribuido según maestra + auditor: M17→B1, M15→B2, M16 y M12→B3; B4 queda con 8 estrenos y los repasos.*

Regla CPA transversal (completada): nada abstracto antes que su concreto — M2 siempre antes que M4 y M5; M9/M10 antes que M11; **M12 antes que M11-inverso**; **M13 con pictórico antes que abstracto**; multiplicacion_concepto dominada antes de cualquier contrarreloj.

---

## 5. Lo que dijo el panel y qué se ajustó

### Incorporado de la maestra
1. **Reordenamiento del año de Matemática** (su pedido n°1): M17→B1 como rutina, M15→B2, M16→B3, M12→B3 junto a M9/M10. El B4 original "no entraba ni en un año sin paros".
2. **L19 separación de palabras** (su pedido n°2): actividad nueva nodal, "mimamá/selo dije" es el error de escritura n°1 del grado. Tier 2 puro.
3. **Blindaje anti-memoria** (su pedido n°3): M8 semi-paramétrico, pool de preguntas en L7, superficies variables en secuencias, dominio solo con ítems no vistos verificado por el motor.
4. L1 cargada 70/30 hacia qu/gu/rr/gue-gui (ch/ll vienen de 1°). L2 sale de B1 (b/v en marzo no es para todos), con fast-track para avanzados. L7 disponible desde B1 para el que lee. L14 con la palabra en oración. C8 plantas/germinador (C7 geoformas pasa a extra sin cómputo, coincidiendo con el auditor). AND de T3 eliminado. Mini-biblioteca imprimible de los 12 textos. M5-N4 con reagrupamiento existente y visible. Cursiva con botón visible en la ficha + consigna de cuaderno al cierre de cada sesión de Lengua (su yapa). L2/L4 comunicadas como "dictado sin pelearse".

### Incorporado del alumno (Benja, 7)
1. **Capa de motivación completa**: racha, mapa con estados y candados, monedas cosméticas, récord personal ("ganarle al yo de ayer"), cofre al cierre, elegir el orden dentro del set activo.
2. **Mezcla de mecánicas**: nunca 3 trivias seguidas — su crítica más aguda ("un montón de los nuevos son EL MISMO juego con otras palabras") y la más barata de resolver en el menú.
3. Simon infinito con récord; sopa recalibrada a la baja ("difícil-que-me-sale"); laberinto con tolerancia de arrastre (era fricción de input, no dificultad); tablas como desafío opcional con copita; constructor de fichas como capa N4 en L1/L2/L4/L19 ("lo más parecido a escribir") — coincide con el R-5.3 del auditor; restas prestando en M5-N4; reloj de agujas como ampliación opcional de M17; T1 con 6 niveles y depuración ("el mejor de todos y dura NADA"); M8 con muchos problemas y explicación del porqué. Su detección del exploit de sustantivos ("miro la letra grande y gano sin leer") confirmó el B-1 del auditor.

### Incorporado del auditor externo (los 5 bloqueantes, resueltos)
1. **Los 7 binarios eliminados**: L18 multi-select de mayúsculas (B-1), M9 → trivia de cálculo (B-2), T4 con "estructura" (B-3), C2 con "refleja" (B-4), X1 con "verde pero enjuagado" (B-5), L5 agudas trisílabas (B-6), L1 constructor con fichas-distractor (B-7).
2. **Métrica sellada**: umbral exacto "≤1 error en sesión de 8-10" (corrige el 85%≠8/10), pista → ítem fuera del cómputo, repetidos solo en repasos ≥3 semanas.
3. **Bancos**: mínimo real 30, insignia 40 (L2, M8), pool 6-7 preguntas/texto en L7 (~75-84 ítems), superficie paramétrica en secuencias, sub-mínimos subidos (T2/T3/T4/M12) o con techo documentado (T3→24, T4→24, X3→20).
4. **B4 redistribuido** (coincidió con la maestra; donde difirieron — M17 a B2 vs B1 — se adoptó B1, que tiene el argumento pedagógico más fuerte: rutina diaria de marzo); M12-concreto antes de M11-inverso; etapa pictórica en M13; equivalencias de M2 en N3.
5. **Remediación del gate especificada + diagnóstico de colocación** para compras a mitad de año.
Y de las recomendadas: guardas de colisión en todas las paramétricas; QA humano del 100% de clips de pares mínimos y entonación (L15-N3 se degrada a N2 sin culpa si el TTS no pasa); validación de ternas L1-L4 contra ~20 cuadernos reales antes de escribir los bancos (se retiran "chiquo"/"karo", entra "qeso"); tablero para padres; estados visibles de progreso; "Desafío de la semana" interleaved; modo "Encontrá el error"; distractores D-2 (M1: 510 arrastre en vez de 410 inversión) y D-3 (M14: vista lateral) corregidos; C7 descontada; capa diagnóstica de M2 y lógicas de feedback de C5/X2 presupuestadas en Tier 3 (D-7); dimensionamiento re-expresado sin el ~20% de sobreventa (A-2); memotest-palabras jamás comunicado como lectura (R-7).

### Descartado o diferido (con motivo)
- **Alumno: "que me escuchen leer A MÍ"** — grabación y evaluación de voz siguen fuera del motor en esta versión; queda registrado como la inversión futura de mayor demanda real (es LO que más le cuesta de 2°, según él mismo).
- **Alumno: "empiecen L15 por el modo solo-audio"** — se mantiene la progresión con texto+signos primero: sin apoyo visual el error no se puede explicar, y el modo solo-audio depende del QA de entonación pendiente; sí se adopta comunicarlo como "el juego de adivinar por la voz".
- **Auditor D-6 (L13-N3)** — no se descarta el ítem "hoy comí" pero el nivel entero no se construye hasta validar en campo que el error "hoy fuerza presente" existe con la frecuencia supuesta; "Mañana fuimos" queda anotado como semilla de una actividad de detección de error, distinta.
- **Maestra: "sumar textos aunque las preguntas vengan después"** — parcial: los 12 textos salen imprimibles ya; textos extra sin preguntas se difieren al ciclo de contenido posterior al lanzamiento para no diluir el QA inicial.

---

## 6. Esfuerzo de construcción (curación / banco nuevo / mecánica nueva)

### Tier 1 — Curación pura (tocar parámetros/cfg; horas, no días)
- serie: tope y pasos por edad (arregla el bug 16<30).
- sopa: params de grilla/direcciones/largo por edad en `_sopa_json`.
- laberinto: tams por edad + tolerancia de arrastre (UX).
- puntos: numeración con escalas (M18).
- sumas_redondas: objetivos {500, 1000} + modo resta.
- simon: modo infinito con récord.
- Gates `if e == 7`: retirar sumas/restas/contar/agrupar/patron del menú de 7; mover conductor_aislante, trivia_espacial, tablas_contrarreloj; regla anti-3-trivias-seguidas en el orden del menú.
- sudoku/memotest/colorear/quefalta: cero trabajo.

### Tier 2 — Banco nuevo sobre mecánica existente (EL trabajo del producto)
- **Trivia 3-4 opciones:** L1, L2, L3, L4, L19, L12, L13, L15, M8 (esqueletos), M9, M13*, M16, M17, T2, T3, C8 (trivia diagnóstica) — (*paramétricas: el trabajo es la plantilla de distractores conceptuales + guardas).
- **Clasificar 2-3 categorías:** L10, L14, C1, C2, C3, C4, C6, X1, X2 (parte), T4.
- **Ordenar secuencia (con superficie paramétrica):** L8, L9, X1 (circuito), C4 (etapas), C8 (ciclo).
- **Matching parte→función:** C5, X3.
- **Completar serie:** M1, M11.
- **Bancos ampliados de existentes:** L16 10→30, L17 10→30 (regla nueva de distractores), L18 30 oraciones multi-select.
- **Render de texto largo + trivia (plantilla liviana):** L7 — único con front nuevo chico (texto de 100 palabras + botón de audio); el esfuerzo real son los 12 textos con pool de 6-7 preguntas.
- **Volumen total estimado: ~1.150-1.250 ítems manuscritos** (sube desde ~850-950 por los mínimos de 30/40, el pool de L7, L19 y C8). Se escribe por bloque siguiendo la sección 4 (B1 primero ≈ 280 ítems), nunca todo junto.
- **Validación previa:** ternas de L1-L4 contra ~20 cuadernos reales de 2° antes de escribir los bancos de sistema de escritura.
- **Audio:** L1-L6, L19 y L15 requieren clips por ítem vía `generar_audio_consignas` (existente). Prerrequisito de publicación + **QA humano del 100% de los clips de pares mínimos (caro/carro) y de entonación (L15)** con criterio de rechazo definido.

### Tier 3 — Mecánica nueva (en orden de valor curricular por línea de código)
1. **Cajero multi-tap + capa diagnóstica (M2):** multi-selección con contador Y reconocimiento de estados de error (armó 370 pidiendo 307 → explica el cero posicional). Presupuestada completa: la capa diagnóstica es la mitad grande del trabajo, no un extra. Desbloquea el hito del grado y el apoyo CPA de M4/M5.
2. **Bloque "repetir" + depuración en programar_camino (T1/T2):** media; hay prototipo y el comentario del código ya lo pedía. Desbloquea los DOS nodales nuevos de TDyP.
3. **Multi-select "tocá todas" (L18):** chica; reusable para futuros multi-target.
4. **Multi-paso guiado con estado (M5):** chica; encadenar 3 trivias + composición.
5. **Tap sobre zonas de documento (L11):** media; reusable para envases (X2) y carteles (X3).
6. **Repartidor uno-a-uno (M12):** chica.
7. **Tap sobre grilla con objetos (M14):** chica; reusa el render de grilla.
8. **Constructor de fichas con distractores (capa N4 de L1/L2/L4/L19):** media; producción real de escritura dentro del motor — cubre parcialmente el hueco más grande del mapa.
9. **Motor de dominio y repaso:** reglas selladas (umbral por tamaño de sesión, pista fuera de cómputo, remediación, colocación, repetidos ≥3 semanas, strands). Es transversal a toda la banda 6-12, no solo a 2°.
10. **Capa de motivación:** racha, mapa con estados, monedas cosméticas, récord, cofre. Sin valor pedagógico directo, alto valor de retención; el alumno fue explícito: es lo que lo haría volver solo.
11. **Tablero para padres:** vista de la telemetría que ya existe por diseño. La feature de valor percibido más barata del proyecto.
12. **Desafío de la semana (interleaved) y modo "Encontrá el error":** costo casi cero de contenido (reusan bancos); el interleaving es de lo mejor documentado en consolidación y el "encontrá el error" duplica la vida útil de cada banco.

### Fuera del motor (inversión aparte, NO prometer)
- Trazado de cursiva → cuaderno imprimible (con botón visible en la ficha + consigna de cierre por sesión).
- Grabación de voz para oralidad/lectura en voz alta → fuera de esta versión; primera candidata para la siguiente.
- Balanza/regla manipulables con drag de precisión → la versión de LECTURA (M16) cubre el nodal.
- Fotos reales de paisajes → C7 sigue en siluetas y fuera del cómputo; si algún día se invierte en assets, es la candidata.

### Orden de ataque (mayor deuda curricular por esfuerzo)
1. Tier 1 completo (un día: elimina lo vergonzoso — la serie más fácil que 1°, el material de jardín) + motor de dominio con reglas selladas (sin esto, nada de lo demás mide).
2. L2 + L1 + L5 + L19 (el contenido insignia de Lengua: trivia + audio existente; validar ternas contra cuadernos primero).
3. M2 cajero (con capa diagnóstica) + M4 + M6 (el salto a tres cifras).
4. L7 comprensión lectora con pool (la carencia más visible para un padre) + mini-biblioteca imprimible.
5. C1 + C2 (la ciencia del grado; liberan los dos juegos desalineados) + C8 germinador.
6. T2 + T3 sobre programar_camino 2.0.
7. Capa de motivación + tablero para padres (retención; barato sobre telemetría existente).
8. El resto por bloque según la sección 4, con X4-ESI solo tras revisión especialista.
