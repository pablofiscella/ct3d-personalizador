# 3° grado (8 años)

> Dossier definitivo del cuaderno de actividades interactivo para 3° grado, alineado al Diseño Curricular 2024 de CABA. Integra la auditoría curricular externa, el mapa de diseño y las tres devoluciones del panel (maestra de sala, alumno de 8 años, auditor pedagógico externo). Las críticas válidas ya están incorporadas al mapa de las secciones 2–4; la sección 5 documenta qué se aceptó, qué se ajustó y qué se descartó con su razón. Donde este dossier difiere de la propuesta previa, vale lo que dice acá.

**Posicionamiento honesto del producto (sostener en el marketing).** Esto es **práctica y repaso** del DC de 3°, no "cubre 3° grado". Producción escrita real (redactar 150 palabras), cursiva, lectura en voz alta con evaluación de fluidez, copia y dictado de figuras con trazo y planos construidos por el chico quedan **declaradamente fuera de alcance** de un motor táctil de tap/arrastre. Son medio año de Lengua y buena parte de la geometría de Matemática: venderlos como cubiertos sería humo.

---

## 1. Estado actual — veredicto de auditoría

**Veredicto global.** De los 25 juegos del menú de 8 años, **1 está plenamente alineado a 3°** (tabla_pitagorica), 2 lo están con reservas (cajero_automatico, cuerpos_geometricos), 3 tienen anclaje pero calibración de 1°–2°, **10 son contenido de grados inferiores** (varios de nivel inicial) y **9 no tienen anclaje curricular**. El 88% del menú no trabaja 3°. El menú es una capa de 8 juegos con `if e == 8` montada sobre una base de 17 congelada en la dificultad de los 6 años. Verificado en código: `actividades_web.py:153-154` (sumas/restas max 10), `:176` (tope 30 solo para e==6), `:224` (bloque e==8); `actividades_player.js:3065-3067` (banco de 3 cuerpos). El dato de campo (alumnos de 4° dicen que "algunas son muy fáciles") no es ruido: es la banda entera pidiendo techo.

### Veredicto por juego

| # | Juego | Veredicto | Justificación (DC 3°) |
|---|-------|-----------|------------------------|
| 1 | memotest (8 pares) | **SIN ANCLAJE** | Memoria visual pura; mecánica pre-lectora idéntica a la de 6 años. |
| 2 | laberinto (9-12 celdas) | **SIN ANCLAJE** | El DC pide orientación en cuadrícula con casilleros/nudos y vocabulario; arrastrar no usa referencias ni vocabulario espacial. |
| 3 | programar_camino (3-4 celdas) | **MUY FÁCIL** | TDyP 3° exige bucles anidados y variable; el juego es secuencia lineal sin una sola repetición (nivel 1°). El código lo admite ("provisorio", .py:146-150). |
| 4 | sopa (10×10, 8 direcc.) | **SIN ANCLAJE** | Reconocer palabras sueltas es cierre de 1°; Lengua 3° pide comprender textos de mediana extensión (+150 palabras). |
| 5 | sudoku 4×4 (≤8 huecos) | **MUY FÁCIL** | Lógica sin anclaje; es bit a bit el mismo puzzle del chico de 6 (cuaderno.py:617, `quitadas >= 8: break`). |
| 6 | sumas (max 10) | **DESALINEADO (1°)** | DC 3°: sumas que dan 1.000 y 10.000, algoritmos convencionales. El resultado nunca supera 10. |
| 7 | restas (max 10) | **DESALINEADO (1°)** | DC 3°: restas de 10/100/1.000, algoritmo con préstamo. Minuendo ≤10 es 1°. |
| 8 | serie (tope 16) | **DESALINEADO (1°)** | DC 3°: escalas de 100/200/500/1.000 hasta 10.000. Paso 1-2 hasta 16, y **escala invertida**: el de 6 años recibe tope 30 (.py:176), el de 8 recibe 16 (js:5735). |
| 9 | patron (ABCD) | **DESALINEADO (inicial)** | Patrones de repetición ABC/ABCD son de sala de 5; no existen en el DC de 3°. |
| 10 | puntos (estrella 10, corazón 14) | **SIN ANCLAJE** | Serie hasta 14 por unir puntos: conteo inicial. |
| 11 | contar (max 9) | **DESALINEADO (inicial/1°)** | Conteo 1-9 con sprites; en 3° el indicador es leer/escribir/ordenar números de 3 y 4 cifras. |
| 12 | colorear (tap-balde) | **SIN ANCLAJE** | Recreativo, sin consigna ni corrección; idéntico en todas las bandas. |
| 13 | mas_menos (max 9) | **DESALINEADO (inicial/1°)** | Comparar grupos de 1-9; el DC compara números de 4 cifras, no cantidades perceptuales. |
| 14 | simon (6 colores) | **SIN ANCLAJE** | Memoria de trabajo; no figura en el DC. Es el único juego base con escala fina por edad. |
| 15 | agrupar (sprite→canasta idéntica) | **DESALINEADO (inicial)** | Matching por identidad visual sin categorías es sala de 3-4. Con categorías reales tendría anclaje en Lengua (hiperónimos). Son 8 rondas. |
| 16 | quefalta (5 ítems) | **SIN ANCLAJE** | Memoria visual inmediata; sin correlato en el DC. |
| 17 | bingo (grilla ≤8, pista imagen) | **SIN ANCLAJE** | Emparejar por imagen "sin lectura" (js:5988): mecánica pre-lectora en un grado cuyo marco es consolidar la lectura. |
| 18 | animal_comida (🦁→🥩) | **DESALINEADO (inicial)** | CdM 3° pide respuestas de seres vivos al frío, fototropismo. "El conejo come zanahoria" es sala de 4. |
| 19 | partes_oracion (10 palabras) | **MUY FÁCIL** | El anclaje existe, pero el DC lo pide EN la oración (quién realiza la acción, concordancia). Diez palabras aisladas se memorizan en una sesión. |
| 20 | tabla_pitagorica (2-9, generativo) | **ALINEADO** | Nodal textual directo; distractores que son productos reales de otras tablas. Cubre memorización; no cubre construcción ni relaciones. |
| 21 | tiempos_verbales (Corrí/Corro/Correré) | **MUY FÁCIL** | Ejercita perfecto simple y futuro (foco de 2°); omite imperfecto -aba, perífrasis y condicional (los de 3°). Grado equivocado en ambas direcciones. |
| 22 | estaciones (☀️→Verano) | **DESALINEADO (inicial/1°)** | Asociar emojis a estaciones no figura en CdM 3°. |
| 23 | cuerpos_geometricos (3 cuerpos) | **ALINEADO, mal implementado** | Anclaje real, pero banco de 3 sobre 6 cuerpos, sin lista `usados` (repite en sesión), y "aristas de 🔺" sobre emoji plano solo se responde de memoria. |
| 24 | separador_mezclas (colador/imán) | **DESALINEADO (fuera del DC)** | Métodos de separación no están en el DC 2024 del primer ciclo. Lo nodal es estados de la materia y cambios de estado. |
| 25 | cajero_automatico (2 billetes, ≤$1500) | **ALINEADO, corto** | Anclaje directo (composición aditiva en dinero), pero componer con 2 billetes no cubre el indicador. Único, junto al 20, con números del orden del grado. |

**Resumen:** 1 alineado pleno · 2 alineados con reservas · 3 muy fáciles con anclaje · 10 desalineados (9 hacia abajo, 1 fuera del DC) · 9 sin anclaje.

### Los 5 gaps más graves

1. **Numeración y operaciones en el rango del grado.** El DC opera hasta 10.000 con algoritmos completos (suma con llevada, resta con préstamo); el producto suma hasta 10. Es el corazón de Matemática 3° y está a dos grados de distancia.
2. **Acentuación y ortografía** (agudas/graves/esdrújulas, tildación del pretérito perfecto simple, -aba, mb/nv, z→ces/cito, güe/güi): el contenido estrella de Lengua 3°, con gamificables obvios (tocar la sílaba tónica), sin una sola actividad.
3. **División con resto**: nodal que estrena 3° y define el pasaje al segundo ciclo; inexistente (agrupar es matching, no reparto).
4. **Ausencia total de TEXTO**: ni comprensión ni producción; el ítem más "letrado" del menú es una palabra suelta, contra un DC cuyo indicador es leer y redactar 150+ palabras.
5. **Los dos bloques nuevos de CdM** (observación del cielo + estados de la materia): ambos ausentes, mientras el slot de "ciencias" lo ocupan un juego de inicial (estaciones) y uno fuera del DC (separador_mezclas).

---

## 2. Mapa propuesto del año

### Números totales

| Área | Actividades curriculares | Núcleo | Extendido |
|---|---|---|---|
| Matemática | 18 (M1–M18) | 10 | 8 |
| Lengua | 17 (L1–L17) | 7 | 10 |
| Conocimiento del Mundo | 10 (C1–C10) | 2 | 8 |
| TDyP + Transversales | 8 (T1–T8) | 1 | 7 |
| **Total curricular** | **53** | **20** | **33** |
| Recreo (evergreen, no curricular) | 6 (memotest, sopa, laberinto, sudoku, simon, colorear) | — | — |
| **Catálogo total del grado** | **59** | | |

**Cómo se derivan los números.** Una sentada de un chico de 8-9 años = **una** actividad de 8-10 rondas (15-20 min). Una familia que usa el producto como refuerzo **real** promedia 1-2 sentadas/semana con picos antes de evaluaciones (no las 3-5 del caso ideal). Por eso el catálogo se organiza en **núcleo (20) y extendido (33)**: la rotación **garantiza** el núcleo aun con poco uso (repertorios de Matemática M1–M3, M5–M9, M11, M13 y de Lengua L1–L3, L9, L11), y sirve el extendido según haya tiempo. Corrección de honestidad respecto de la propuesta original: 53 actividades × 2-4 visitas espaciadas = **106-212 sentadas** (no "130-190"; la cuenta iba maquillada para calzar con la demanda anual). El catálogo llena el año con holgura sin agotarse en un mes.

**Tamaño de banco derivado del criterio de dominio.** Dominio = **85% de acierto en las últimas 10 respuestas, al primer intento y sin pista, con ítems variados en valor y posición, sostenido en ≥2 sesiones sin repetir ítems entre sesiones**. Eso exige **≥20 ítems distintos por nivel certificable**. De ahí: banco manual mínimo **16-24**; **generativo con rangos** donde el contenido lo permite (aritmética, cuadrícula, reloj: variación infinita, distractores por regla de error); y bancos troncales **a 40** (L2, L3, M13) porque son los más revisitados. Los bancos que no llegan al mínimo se declaran **"de exposición"** (1-2 visitas, sin certificado de dominio): es honesto para línea de tiempo, Plaza de Mayo, poesía y constelaciones, que son de idea única.

### Reglas transversales (aplican a TODO el mapa)

**Diseño de la interacción**
- **Cero fail states.** Cada distractor tiene **microexplicación del porqué (2-3 líneas, con detalle conceptual: ya tienen 8)**. Al **acertar** no se obliga a leer nada: tick + juice y a seguir (pedido de Benja).
- **Andamiaje que se retira.** 1er error → pista fuerte (ej.: se resalta la columna de las decenas); 2° error → pista sutil; aciertos seguidos → sin pista.
- **CPA para matemática nueva.** Nivel 1 con apoyo pictórico en CSS (billetes, barras, grillas, áreas coloreadas); nivel final solo símbolos. El apoyo se retira igual que las pistas.
- **Rondas.** 8-10 por sentada, con **salida anticipada / bonus de velocidad a partir de la ronda 6** en las actividades de clasificar (a la 6 el chico ya entendió; pedido de Benja).
- Targets ≥48dp; ilustración solo representacional del ítem.

**Estilo de ítem (lint obligatorio antes de escribir los ~750 manuales)**
- Formato: consigna → **correcta** | D1 (error conceptual con misconception nombrada) | D2 (íd.).
- **Opciones de longitud comparable** y posición de la correcta balanceada. Prohibido que la correcta sea siempre la más larga/matizada (test-wiseness). Prohibidos los "chistes-distractor".
- Cada generador entrega su **tabla de reglas de error como código revisable** (entrada → regla ejecutable → distractor); cada manual pasa el lint (a) longitud, (b) misconception nombrada, (c) cero relleno.
- **Validación con ojos de maestra, ítem por ítem, no opcional.**

**Medición de dominio operacionalizada por tipo de mecánica** (defecto estructural que la propuesta original no cubría)
- **Trivia/cloze:** 85% sobre 10, primer intento sin pista.
- **Ordenar secuencia:** "acierto" = secuencia completa correcta **al primer intento**; cualquier sacudida/corrección = ítem fallado. (Sin esto se certifica por persistencia.)
- **Clasificar/matching:** los **últimos pares forzados** (2 elementos ↔ 2 canastas, 50/50 o forzado) **no computan**.
- **Bingo (L17):** las **últimas 2-3 pistas** de cada cartón no computan, o el cartón se renueva antes de agotarse.
- **Trazado (C6):** el trazado es memoria motora de la figura → **el dominio se mide solo sobre las trivias**, no sobre el trazado.
- **Programación (T1/T2):** desafíos fijos son memorizables → variación generativa de parámetros (largo del camino, posición de la meta) para que el dominio mida el constructo, no el recuerdo de la solución.

**Ruta del limbo 60-84%** (el alumno que compra el producto)
- No sube (necesita 85%) ni baja (baja recién con 2 sesiones <60%). Regla nueva: **3 sesiones en la franja → el sistema reintroduce el apoyo pictórico CPA del nivel** (aunque no baje) **y prioriza en la rotación los tipos de ítem donde acumula errores**.

**Capa de motivación y medición** (convergencia del panel: la palanca de retención y de venta)
- **Cola de repaso a nivel ítem** (spaced repetition de los errores concretos): los ítems fallados reaparecen a intervalos crecientes **cruzando actividades**. Los bancos ya existen: es scheduling, la rejugabilidad más barata y de mayor efecto.
- **Desafío del día:** 8 ítems mezclados **solo de repertorios ya dominados** (mantenimiento + interleaving de retrieval; resuelve el "¿qué pasa con M5 dominado en junio, en noviembre?"). Generativo en matemática, rejugable todo el año.
- **Mapa de dominio visible** por eje y nivel CPA: para el chico, progreso ("mapa del camino" tipo Duolingo/Mario); para el padre, el "qué está aprendiendo" con **reporte bimestral ligado a los indicadores de logro del DC**. Convierte la honestidad del "fuera de alcance" en argumento de venta.
- **Racha diaria + progreso que se guarda + desbloqueables** (skins/stickers para el memotest, un laberinto secreto, un colorear especial): ganar en matemática habilita algo que el chico quiere en otro lado. **Juice al acertar** (confetti, sonido, personaje que festeja), no un tick verde en silencio.
- **Modo "mañana tengo prueba":** el adulto elige el tema y el motor toma como Duolingo, repitiendo **justo lo que sale mal** (usa la cola de repaso). Es lo que el padre pagaría.
- **Recreo ganado:** una sentada curricular habilita el recreo del día. Suave, sin castigo. El chico **siempre puede entrar a su favorito** igual (libre elección preservada).
- **Modo "explicá vos":** tras dominar, el ítem se invierte — se muestra la respuesta errada de un personaje y el chico elige POR QUÉ está mal (reusa las microexplicaciones como opciones). Metacognición barata, es lo que la maestra le toma en la evaluación.

### MATEMÁTICA

| Act. | Mecánica | Banco | Dificultad (3 niveles) | Contenido DC 3° |
|---|---|---|---|---|
| **M1 · Serie gigante** | Completar serie (`serie` endurecido) | Generativo | paso 100 asc. ≤3.000 → 200/500/1.000 mezclados, desc., cruzando miles ≤10.000 | Escalas de 100/200/500/1.000; serie hasta 10.000 |
| **M2 · Tres en fila** | Tap entre **3** numerales (nunca 2); consigna rotativa mayor/menor/entre (`mas_menos` endurecido) | Generativo | **arranca en 4 cifras** con cifras engañosas → rangos anchos; ≥⅓ con distractores fuera de rango por poco | Leer, comparar y ordenar números de 3-4 cifras |
| **M3 · Cajero de miles** | Tocar N billetes 1.000/100/10/1 con contador visible (`cajero` endurecido; CPA: los billetes son el material) | Generativo | 3 cifras sin ceros → 4 cifras con cero intermedio → "menor cantidad de billetes" | Valor posicional; composición aditiva de 4 cifras en dinero |
| **M4 · Mil más, mil menos** | Tap-selección (trivia) | 20 manual + generador | cien más/menos → mil más/menos → doble/triple/mitad de redondos | Relaciones mil/cien más-menos, doble, triple, mitad |
| **M5 · Sumas con llevada** | Tap-selección; nivel 1 con sumandos en billetes (CPA), nivel 3 solo cifras (`sumas` endurecido) | Generativo (reglas de error) | sin llevada → una → dos llevadas → estimación al cien | Algoritmo convencional de suma; miles+cienes+dieces; cálculo aproximado |
| **M6 · Restas con préstamo** | Espejo de M5 (`restas` endurecido) | Generativo | sin préstamo → un préstamo → **préstamo a través del cero** (502−178) → resta a 1.000/100 | Algoritmo convencional de resta; restas de 10/100/1.000 |
| **M7 · Parejas que dan 1.000** | Tocar 2 que sumen X sobre pozo de 6 (mecánica del cajero) | Generativo (casi-pares como trampa) | redondos de a 100 → de a 50 → de a 10 → parejas que dan 10.000 | Repertorio: sumas que dan 1.000 y 10.000 |
| **M8 · Tabla pitagórica** | Grilla de 9 productos reales + modo relaciones + modo factor desconocido (`tabla_pitagorica` ampliado — **no tocar el core**) | Generativo + banco relaciones 24 | tablas 2-6 → 2-9 → relaciones → factor desconocido | Construcción, relaciones entre productos, memorización; división como factor desconocido |
| **M9 · Rayo ×10 ×100 ×1.000** | Contrarreloj suave | Generativo | dígito×10 → dígito×1.000 → bidígito×100 | Repertorio multiplicativo ×10/×100/×1.000 |
| **M10 · Multiplicación en partes** | 2 pasos: elegir descomposición, luego total. **Nivel 1 con grilla de áreas coloreadas de M12 (CPA)** | Generativo | ×2 cifras (con área) → ×3 cifras → solo símbolos | Algoritmos intermedios y por una cifra |
| **M11 · Reparto con resto** | Trivia pictórica generativa: sprites en pantalla (CPA), repartir entre N; doble respuesta (a cada uno + sobran) | Generativo | **niveles 2-5 ≤20 (entra B2)** → 2-9 ≤90 → "¿alcanza para uno más?" | Reparto/partición; resto 0 y ≠0; estrategias sin algoritmo |
| **M12 · Bandeja de huevos** | Trivia pictórica (grilla de sprites en CSS) + completar tabla proporcional | 20 manual | leer la grilla → tabla directa → tabla con salto | Organizaciones rectangulares; series proporcionales; suma vs. multiplicación |
| **M13 · Fábrica de problemas** | Texto breve (2-3 líneas) + tap-selección | **40 manual (incluye problemas de dos pasos)** | elegir el cálculo → incógnita inicial / comparación → dato inútil, pregunta respondible, **dos pasos** | Incógnita en estado inicial; comparación; datos necesarios/innecesarios; pregunta-cálculo |
| **M14 · Batalla en la cuadrícula** | Grilla del 100 reetiquetada; **framing de "impacto/agua" con juice** (no batalla naval con barcos ocultos: eso rompe el constructo) | Generativo | tocar el casillero nombrado → nombrar la celda de un sprite → trayectos | Orientación en cuadrícula con casilleros/nudos y vocabulario |
| **M15 · Detective de figuras** | Trivia con figuras en SVG/CSS inline; **rombo con escala NO uniforme (diagonales visiblemente desiguales)** + ítem de cuadrado rotado clasificado como cuadrado | 24 manual | 4 figuras conocidas → rombo/paralelogramo → propiedades de diagonales | Rombo y paralelogramo; vértices, lados, diagonales; dictado de figuras (invertido) |
| **M16 · Cuerpos y sus caras** | Trivia + matching figura→cuerpo; **desarrollo plano (net) en grilla CSS para poder CONTAR**; lista `usados` (`cuerpos_geometricos` reconstruido) | 24 manual con `usados` | caras → vértices/aristas → relaciones figura-cara | 6 cuerpos; caras/aristas/vértices; relaciones figura-cara |
| **M17 · La hora justa** | Reloj analógico en CSS; **agujas movibles con arrastre** (mecánica nueva que sube de "aparte" al mapa) | Generativo | en punto/media → cuartos → duraciones → a.m./p.m. y equivalencias | Lectura de hora en reloj de aguja y digital; duraciones; calendario |
| **M18 · Medí como experto** | Trivia de estimación/unidad + barras CPA en CSS (litro en cuartos; tocar-N-que-llenan) | 24 manual | elegir unidad → estimar → cuartos y medios con barra (ampliación) | m/cm/mm; litro y vaso; g/kg; estimación; medios y cuartos |

*Ejemplos de ítems de referencia (con las correcciones del auditor aplicadas):*
- **M5:** 356+267 → **623** | 613 (olvidó la llevada de las unidades) | 523 (olvidó la de las decenas). *Estimación:* 498+305 ≈ **800** | 700 (redondeó ambos para abajo) | 900 (redondeó ambos para arriba). *(Se elimina el "2.400 redondeó mal" en sumas exactas: no es error conceptual de la suma.)*
- **M6:** 502−178 → **324** | 476 (restó la menor de la mayor en cada columna: el bug universal) | 334 (no propagó el préstamo por el cero). *(Se eliminan el "760" —restar solo cienes da 700, la etiqueta no produce el número— y el "845" con la duda del autor impresa.)*
- **M8 relaciones (reformulado):** "¿Qué **otra** cuenta da lo mismo que 6×7?" → **7×6** | 6×6 | 7×7. *(Ya no se imprime el producto en el enunciado: antes la respuesta estaba a la vista.)*
- **M11:** 23 entre 4 → **5 a cada uno, sobran 3** | 4 y sobran 7 (el resto no puede superar la cantidad de amigos) | 6 (imposible: 6×4=24>23). *(Se elimina "6 y sobra 1" en 30÷5: no hay proceso mental que produzca resto 1 en división exacta.)*
- **M13:** "Juan tenía figuritas. Le regalaron 25 y ahora tiene 60. ¿Cuántas tenía?" → **60−25=35** | 60+25=85 (vio "le regalaron" y sumó) | 25 (repitió un dato). *Dos pasos:* "Compró 3 paquetes de 6 figus y regaló 4. ¿Cuántas le quedaron?" → **14** | 18 (no restó las regaladas) | 9 (restó antes de multiplicar).
- **M14 nivel 2:** el sprite está en C4; distractor = **la celda D3 real leída con fila/columna invertidas** (celda válida transpuesta), no la etiqueta rota "4D" que se autodelata por formato.

### LENGUA

| Act. | Mecánica | Banco | Dificultad | Contenido DC 3° |
|---|---|---|---|---|
| **L1 · La sílaba fuerte** | Sílabas como botones tocables (tokens) + AUDIO de la palabra; nivel 2 clasificar aguda/grave/esdrújula | 24 con audio; **nivel 1 solo palabras de ≥3 sílabas** (las bisílabas van a clasificación: tocar la tónica de "ratón" es 50/50) | tocar la tónica → clasificar → **clasificar oyendo palabras nuevas sin apoyo visual** (no "leer la tilde": eso es trivial o exige reglas de 4°/5°) | Agudas, graves, esdrújulas (adopción progresiva). **El feedback enuncia la regla**: "las agudas llevan tilde cuando terminan en n, s o vocal" |
| **L2 · Ponele la tilde** | Cloze de 3 opciones: la MISMA palabra con la tilde en distinto lugar o sin tilde (nunca 2) | **40 manual** | pares de sentido con contexto → sin apoyo del dibujo → mezcla con sustantivos (medico/médico). **+ modo dictado** (audio dicta, elegir entre 3 escrituras parecidas) | Tildación del pretérito perfecto simple; reglas de acentuación |
| **L3 · Fábrica de ortografía** | Completar palabra tocando la grafía | **40 manual** | -aba y -ces → mb/nv → diéresis y ampliaciones (-ción, ge/gi). **+ modo dictado** | -aba; z→-ces/-cito; mb/nv; diéresis güe/güi |
| **L4 · Orden de diccionario** | Ordenar secuencia de 5 palabras | 20 sets | **arranca en desempate por 2ª letra** (ordenar por 1ª distinta lo traen de 2°) → por 3ª letra | Orden alfabético (nodal e indicador de logro) |
| **L5 · Armá el diálogo** | Ordenar parlamentos de 2 personajes + trivia de signos | 20 | signos → raya → ordenar turnos | Raya de diálogo; ¿?/¡!; estructura del diálogo |
| **L6 · Detrás del telón** | Clasificar parlamento / didascalia / partes de la obra | 20 (exposición) | — | Teatro: actos/escenas; parlamentos y didascalias |
| **L7 · ¿Qué globo va?** | Clasificar habla/pensamiento/grito con globos en CSS + onomatopeyas | 16 | — | Historieta: tipos de globo; onomatopeyas; relaciones entre viñetas |
| **L8 · Versos y estrofas** | Poema breve real en pantalla + trivia | **18 poemas (exposición)** × 2 preguntas | contar versos/estrofas → sentido figurado | Poema: estrofas y versos; lenguaje figurado |
| **L9 · El texto manda** | Texto de 60-150 palabras + 3 preguntas tap-selección; **2ª tanda de preguntas por texto** (explícita/principal/inferencial rotan por relectura) | **24-30 textos** × 3 + 2ª tanda + "temporada 2" a mitad de año | explícita → idea principal → inferencia/causa | Comprensión de narrativos/expositivos/instructivos; esencial vs. secundario; causa-consecuencia |
| **L10 · Conectores nivel 2** | Cloze tap-selección | 24 | adversativos → continuativos → concesivos | Conectores adversativos y continuativos; cohesión |
| **L11 · ¿Quién hace qué?** | Tokens tocables DENTRO de la oración + cloze de concordancia (`partes_oracion` reconstruido) | 24 oraciones | quién realiza la acción → concordancia singular/plural → persona | Partes de la oración en contexto; concordancia |
| **L12 · Tiempos de verdad** | Cloze con contexto temporal que obliga a elegir (`tiempos_verbales` reconstruido) | 24 | imperfecto -aba → condicional → perífrasis de futuro | Presente, imperfecto -aba, perífrasis de futuro, condicional |
| **L13 · Fábrica de palabras** | Trivia de derivación (las 3 derivadas son los distractores) | 24 (16 familias) | — | Sufijos derivativos; prefijos/sufijos frecuentes |
| **L14 · ¿Hiato o diptongo?** | Trivia de separación en sílabas CON audio | 24 | diptongo → hiato → contar sílabas | Segmentación con hiatos y diptongos |
| **L15 · Familia grande, familia chica** | Clasificar en 3 canastas-hiperónimo rotativas (`agrupar` reconstruido) | 24 en 8 categorías | canasta directa → ítem inverso (familia grande) | Hiperónimos e hipónimos |
| **L16 · Inicio, desarrollo, cierre** | Ordenar 3-4 bloques de texto + detectar intruso | 18 micro-narraciones | ordenar → intruso → identificar el conflicto | Inicio/desarrollo/cierre; relaciones temporales y causales; conflicto |
| **L17 · Bingo de definiciones** | Grilla de 8, **pista textual** (no imagen) (`bingo` reconvertido) | 24 definiciones | — | Vocabulario: definiciones, sinónimos, ejemplos de uso |

*Correcciones de contenido aplicadas:* L1 nivel 3 redefinido (oír palabras nuevas, no leer la tilde); las opciones-relleno "que hay queso en la mesa" (L8) y "d-í-a" (L14) se eliminan; el error de escritura aditiva "9.1000" sale de L1/M1 como opción impresa y se testea en formato reconocimiento: "¿Cómo se escribe el número después de 9.999?" → **10.000** | 9.100 | 9.910.

### CONOCIMIENTO DEL MUNDO

| Act. | Mecánica | Banco | Dificultad | Contenido DC 3° |
|---|---|---|---|---|
| **C1 · Frío y calor** | Clasificar sólido/líquido/gaseoso + trivia de cambios | 20 | (sólido/líquido de 2°) → **el gaseoso, que es lo nuevo** → cambios de estado | Estados de la materia; temperatura; cambios por temperatura. *Reemplaza a separador_mezclas* |
| **C2 · ¿Cambió el material?** | Clasificar cambió la forma / de estado / se transformó | 18 | — | Cambios que no modifican la naturaleza vs. cocción/fermentación |
| **C3 · De la vaca al queso** | Ordenar circuito + trivia de estado por etapa | 6 circuitos (techo real) × 5-6 etapas + 12 trivias | — | Circuito productivo de fase agraria a comercial; estados por etapa |
| **C4 · Llega el invierno** | Matching ser vivo → respuesta al frío + trivia de luz | 16 | — | Respuestas al frío (migración, hibernación, estadio larvario); fototropismo. *Reemplaza a estaciones y animal_comida* |
| **C5 · Detectives del cielo** | 3 niveles: astro/no astro, luz propia/refleja, causas | 24 | clasificar → clasificar → causas | Bloque nuevo: astros; Sol como estrella cercana; la Luna refleja; el aire tapa las estrellas de día |
| **C6 · Constelaciones del sur** | Trazar Cruz del Sur (5), Tres Marías (8), Escorpio (14) + trivia (`puntos` con contenido del grado) | 3 trazados (exposición) + **24 trivias (donde se mide dominio)** | trazar → trivia | Constelaciones como figuras inventadas; el giro del cielo |
| **C7 · Línea de tiempo del s. XX** | Ordenar secuencia temporal + trivia de impacto | 18 (exposición) | — | Impacto de nuevas tecnologías; línea de tiempo |
| **C8 · Plaza de Mayo, antes y ahora** | Trivia de cambio/permanencia sobre escenas descriptas | 18 (exposición) | — | Cambios y permanencias de espacios públicos; patrimonio; inmigración |
| **C9 · El viaje del alimento** | Ordenar recorrido digestivo + clasificar grupos + trivia | 18 | — | Transformación del alimento en el organismo; alimentación equilibrada |
| **C10 · ¿Se respeta el derecho?** | Trivia de 3 opciones por escenario (derecho en juego + qué hacer) | 16 (con contraejemplos) | — | Derechos de niños/as, entornos digitales; diálogo y consenso |

*Corrección de redacción (C1):* evitar "lo que VES salir de la pava es gas" — el penacho blanco son microgotas líquidas; el gas es invisible. El ítem se mantiene ("el vapor es agua en estado gaseoso") pero sin instalar la misconception inversa.

### TECNOLOGÍA, DISEÑO Y PROGRAMACIÓN + TRANSVERSALES

| Act. | Mecánica | Banco | Dificultad | Contenido DC 3° / transversal |
|---|---|---|---|---|
| **T1 · Repetí y ganá** | `programar_camino` + bloque "repetir ×N" con contador + límite de bloques que OBLIGA a usarlo + **animación del robot moviéndose** (no teletransportado) | **18 desafíos + variación generativa** | repetir simple → repetir con giro (cuadrado) → repetir anidado | Bucles; bucles anidados; algoritmos |
| **T2 · Cazador de bugs** | Programa + grilla, ejecución paso a paso; tocar el bloque errado | **18 programas + variación** | 1 bug: giro → cantidad en el repetir → bloque de más | Depuración; reconocer y modificar errores |
| **T3 · La variable contadora** | Trivia de predicción del valor final de una variable visible (puntos/vidas) | 18 | suma en bucle → resta por evento → con condicional | Variable con secuencia, condicional y bucles |
| **T4 · Mundo digital** | Clasificar por nivel; **arranca por el nivel de datos que viajan** (hardware/software es sabido) | 36 (12 por nivel) | datos por la red → plataforma/app/interfaz → hardware/software | Hardware/software; plataforma/app/interfaz; redes físicas vs. de datos |
| **T5 · ¿Con qué se mueve?** | Clasificar fósil / alternativa / fuerza humana o animal | 16 | — | Combustibles fósiles y alternativos; tracción a sangre |
| **T6 · Detectives de octógonos** | Comparar 3 rótulos en CSS y elegir | **16-20** | — | Etiquetado frontal (octógonos); decisiones informadas (transversal alimentaria) |
| **T7 · ¿Confiable o sospechoso?** | Trivia de acción (3 conductas) | 16 con **≥1 contraejemplo cada 3-4 ítems** | — | Suplantación de identidad; alertar a un adulto; datos personales (transversal digital) |
| **T8 · ¿Va al compost?** | Clasificar compost / reciclables / peligrosos | 20 | — | Separación en origen; compostaje; recolección diferenciada (transversal ambiental) |

*Corrección de estilo (T7/C10 y transversal a C5, C8, C10):* eliminar el sesgo de longitud (la correcta no puede ser siempre la más larga y matizada). En T7/C10, mantener el ítem-contraejemplo (la amiga real a la que SÍ se le responde) en proporción ≥1/4, para que el chico discierna en vez de aplicar la meta-regla "elegí la opción prudente y larga".

*Distractores-relleno eliminados del banco (auditor §2):* C6 "para sacar fotos" y "porque no había tele"; C7 "llegaron las noticias"; C8 "una casualidad" y "para venderlo mejor"; T4 "agua"; M18 "una heladera". Cada uno se reemplaza por una misconception infantil documentada.

**Fuera de alcance del motor (declarado, no disimulado):** producción escrita real (150 palabras), cursiva, lectura en voz alta con evaluación de fluidez, copia y dictado de figuras con trazo, planos construidos por el chico. Son nodales que un motor táctil no evalúa con honestidad. Se ofrecen como **proxys parciales honestos** donde la tecnología alcanza: el **modo dictado** de L2/L3 (la voz dicta, el chico elige entre 3 escrituras parecidas — usa el pipeline de audio existente) cubre parte del pedido de dictado sin prometer escritura libre.

---

## 3. Cambios al catálogo actual (las 25 del menú)

| # | Juego | Decisión | Detalle exacto |
|---|---|---|---|
| 1 | memotest | **MANTENER (recreo)** | Sin cambios; no-curricular, baja su peso en la rotación. Skins desbloqueables como premio. |
| 2 | laberinto | **MANTENER (recreo) + curación** | e==8 sirve tamaños 12-14 (generar 13-14 en `_armar_data`); deja de contar como actividad de espacio. |
| 3 | programar_camino | **ENDURECER → T1 (+ T2/T3)** | Bloque "repetir ×N" + límite de bloques + animación del robot + ejecución paso a paso (habilita T2) + variable visible (habilita T3). |
| 4 | sopa | **MANTENER (recreo) + curación corregida** | e==8 mezcla palabras del banco, **PERO se excluyen las palabras cuyo punto ES la tilde o la diéresis** (nada de PINGUINO/TAMBIEN sin tilde en la grilla: enseñaría el error). Van solo palabras que la grilla no falsea (BOMBERO, ENVASE). |
| 5 | sudoku | **ENDURECER o RETIRAR** | Generador 6×6 (bloques 2×3), 12-16 huecos, solución única. Si no se invierte, **RETIRAR de 8** (hoy es bit a bit el de 6). Prioridad baja: por debajo del reloj. |
| 6 | sumas | **ENDURECER → M5** | cfg `{max:1000, rondas:8, modo:"algoritmo"}`; distractores por regla de error de llevada; nivel 1 con billetes; se eliminan los sprites de conteo. |
| 7 | restas | **ENDURECER → M6** | Espejo de M5; distractor obligatorio "restó la menor de la mayor"; préstamo por el cero en nivel final. **Prioridad alta (pedido explícito del alumno: "esa la necesito ahora").** |
| 8 | serie | **ENDURECER → M1 + FIX del bug** | cfg `{tope:10000, pasos:[100,200,500,1000], rondas:8}`. **Bug invertido: hoy e==6 recibe tope 30 y e==8 recibe 16** (`actividades_web.py:169-176` + `actividades_player.js:5735`). Tope explícito por edad, no por default del js. **Va primero: es un bug.** |
| 9 | patron | **RETIRAR de 8** | Sala de 5; queda en edades 4-6. |
| 10 | puntos | **MOVER contenido → C6** | Misma mecánica de trazado; estrella/corazón → Cruz del Sur, Tres Marías, Escorpio + trivia post-trazado. |
| 11 | contar | **RETIRAR de 8** | Conteo 1-9 es inicial; queda en edades menores. |
| 12 | colorear | **MANTENER (recreo)** | Válvula de descanso; dibujo especial desbloqueable. |
| 13 | mas_menos | **ENDURECER → M2** | Deja los sprites; 3 numerales de 4 cifras con consigna rotativa. |
| 14 | simon | **MANTENER (recreo)** | Ya tiene escala fina por edad; memoria de trabajo. El alumno lo jugaría igual. |
| 15 | agrupar | **ENDURECER → L15** | Canastas de "sprite idéntico" → hiperónimos rotativos; banco 24; rondas 10 con salida a la 6. |
| 16 | quefalta | **RETIRAR de 8** | Memoria visual pre-lectora; edades menores. |
| 17 | bingo | **ENDURECER → L17** | Pista de imagen → definición textual; banco 24; grilla de 8 conservada; últimas 2-3 pistas no computan dominio. |
| 18 | animal_comida | **RETIRAR de 8 y MOVER a 4-5** | Sala de 4; su slot temático lo toma C4. |
| 19 | partes_oracion | **ENDURECER → L11** | Palabras EN oración con tokens tocables + concordancia; banco 20-24. |
| 20 | tabla_pitagorica | **MANTENER + ampliar → M8** | Modo relaciones (reformulado, sin imprimir el producto) + modo factor desconocido; rondas 6→8. **No tocar el core: es el mejor juego actual.** |
| 21 | tiempos_verbales | **ENDURECER → L12** | Banco nuevo 24 con imperfecto -aba, condicional y perífrasis; se retira el de 4 raíces. |
| 22 | estaciones | **RETIRAR de 8 y MOVER a inicial/1°** | Asociar emoji-estación no figura en CdM 3°. |
| 23 | cuerpos_geometricos | **ENDURECER → M16** | Banco 3→24 (6 cuerpos + relaciones); lista `usados`; desarrollo plano en CSS para poder CONTAR; rondas 8. |
| 24 | separador_mezclas | **RETIRAR de 3°** | Fuera del DC 2024 de todo el primer ciclo. Guardar el banco por si el DC de 2° ciclo lo lista; su slot lo toman C1 y C2. |
| 25 | cajero_automatico | **ENDURECER → M3** | De 2 billetes a composición completa de 4 cifras con contador; modo "menor cantidad de billetes". |

**Balance:** 6 recreo · 12 endurecidas/reconvertidas · 6 retiradas del grado (5 bajan de edad, 1 sale del ciclo) · 1 migra de contenido (puntos→C6). **Nada se tira**: todo lo retirado sigue sirviendo a otras edades.

**Fallbacks de implementación a declarar ahora (auditor §3.7):** el desarrollo plano en grilla CSS de M16 funciona para cubo y prismas; **la esfera no tiene desarrollo y el cono (círculo + sector) no es grillable** → fallback: para cono/cilindro/esfera, **vista explotada de caras**, no net. Sin esto, el contar caras del cono vuelve a ser memoria.

---

## 4. Progresión del año (4 bimestres)

**Decisión estructural:** el menú de 8 años deja de ser "banda grande + parche `if e == 8`" y pasa a ser una **lista explícita por edad**. La banda sigue como fallback, pero 3° tiene catálogo curado.

**Cómo funciona la rotación (resuelve la contradicción aritmética que marcó el auditor).** El bimestre ordena la **aparición** de su cohorte de ~13 actividades, pero **escalonadas a lo largo de sus 8-9 semanas**. En una **semana** dada, el player muestra 10-12: **3-4 nuevas** de las que ya "abrieron" ese bimestre + 6-8 de repaso espaciado de bimestres anteriores (interleaving). El avance de **nivel** dentro de cada actividad lo gobierna el **dominio (85% sostenido)**, no el calendario; el nivel **baja un escalón tras dos sesiones <60%** (piso de frustración), y el limbo 60-84% dispara la ruta de remediación de la sección 2. El apoyo CPA está en nivel 1 y se retira en nivel 3.

**Bimestre 1 (marzo-abril) — Base numérica, conciencia fonológica y LECTURA desde el día 1.**
Entran: **M1** (paso 100 ≤3.000), **M2** (4 cifras), **M3** (3-4 cifras), **M4** (cien más/menos), **M5**–**M6** (sin llevada → una), **L1** (tocar la tónica), **L9** (comprensión, textos 60-80 palabras) ← **adelantado**, **L4** (desde la 2ª letra), **L14**, **L16**, **C1**, **C2**, **T4** (empezando por el nivel de datos), **T8**.
*Cambio clave del panel:* la lectura (L9) arranca en marzo, no en julio — es el gap n.º 1 del producto y el pedido n.º 1 de las familias.

**Bimestre 2 (mayo-junio) — Algoritmos, tablas, división concreta y el 25 de Mayo.**
Entran: **M5**–**M6** pleno (dos llevadas, préstamo por el cero), **M7**, **M8** (construcción y tablas 2-6), **M9**, **M11** (reparto con resto **nivel 1**, ≤20) ← **adelantado**, **M12**, **M14** ← **adelantado**, **M17** (la hora) ← **adelantado**, **L1** clasificar (nivel 2), **L5**, **L11**, **C3**, **C4**, **C8** (Plaza de Mayo, al lado del acto del 25) ← **adelantado**, **T1** (repetir simple), **T6**.
*Cambios del panel:* el reloj (M17) sube de B4 a B2; la división concreta (M11 nivel 1) entra acá; C8 se muda junto al 25 de Mayo; L1 formaliza la clasificación acá (no en marzo).

**Bimestre 3 (julio-septiembre) — Reglas estrella de Lengua, división plena, problemas, textos largos y cielo.**
Entran: **M8** completo (tablas 7-9 + relaciones + factor desconocido), **M10**, **M11** pleno (2-9 ≤90 + "¿uno más?"), **M13** (problemas, incluidos dos pasos), **M15**, **L2** (tildar el perfecto simple) ← **corrido a B3**, **L3** (-aba, -ces), **L6**, **L7**, **L9** (textos creciendo a 150 palabras + 2ª tanda), **L10**, **L12** (tiempos de 3°), **L15**, **C5**, **C6**, **T2**, **T3**, **T5**.
*Cambios del panel:* L2 se corre de B2 a B3 (el aula lo formaliza en el 2° semestre; el DC dice "adopción progresiva"); B3 se descarga moviendo M11/M14/M17 a B2, para que la rotación cierre.

**Bimestre 4 (octubre-noviembre) — Medida, cuerpos, derivación e integración.**
Entran: **M16** (cuerpos), **M18** (con la ampliación de medios/cuartos SOLO acá, con barras), **L8**, **L13**, **L17**, **C7** (línea de tiempo), **C9**, **C10**, **T7**. Repaso intensivo contrarreloj de repertorios (M5-M9, M11, L1-L3, L9) apuntando al cierre de ciclo.
*Cambio del panel:* L12 y M17 **ya no** están en B4 (nacían en octubre y no alcanzaban a consolidarse en ~8 semanas); un repertorio definitorio no puede nacer en el último bimestre.

**Priorización de la rotación:** las 20 del núcleo se garantizan aun con 1-2 sentadas/semana; el extendido se sirve según haya tiempo. El **desafío del día** y la **cola de repaso por ítem** mantienen vivos los repertorios ya dominados en bimestres previos (resuelve el "¿qué pasa con M5 dominado en junio, en noviembre?").

---

## 5. Lo que dijo el panel y qué se ajustó

### Maestra de sala

| Crítica | Decisión | Ajuste |
|---|---|---|
| Comprensión (L9) en B3 es el error más grave del calendario | **Aceptada** | L9 a **B1** (60-80 palabras → 150); banco a **24-30 textos** |
| L2 (tildar) en mayo es temprano; L1 clasificar a B2, L2 a B3 | **Aceptada** | L1 tónica en B1, L1 clasificar en B2, L2 en B3 |
| Plaza de Mayo (C8) en octubre desperdicia el 25 de Mayo | **Aceptada** | C8 a **B2** |
| El reloj en B4 copia el peor vicio del aula; y estático es medio juego | **Aceptada (doble)** | M17 a **B2** + **mover agujas con arrastre** sube al mapa como mecánica nueva |
| División nivel 1 (reparto ≤20) puede entrar en B2 | **Aceptada** | M11 nivel 1 en B2; factor desconocido/estrategias en B3 |
| Sopa con TAMBIEN/PINGUINO sin tilde es un tiro en el pie | **Aceptada** | Se excluyen de la sopa las palabras cuyo punto es tilde/diéresis; quedan BOMBERO, ENVASE |
| M13 (problemas) es EL trabón de 3° y tiene el banco más chico; faltan dos pasos | **Aceptada** | M13 a **40 ítems** con problemas de dos pasos (el más gordo, no el más chico) |
| Las reglas de tilde nunca aparecen en el feedback | **Aceptada** | El feedback de L1/L2 **enuncia la regla** (n/s/vocal) para que el chico justifique en la evaluación |
| L4 nivel 1 y M2 con 3 cifras vienen sabidos de 2° | **Aceptada** | L4 arranca en desempate por 2ª letra; M2 arranca en 4 cifras |
| ¿Quién valida ítem por ítem con ojos de maestra? | **Aceptada** | Validación humana **no opcional** + lint automático (regla en sección 2) |
| Uso real es 1-2 sentadas/semana, no 3-5 | **Aceptada** | Núcleo (20) vs. extendido (33); la rotación garantiza el núcleo |
| Dictado con audio + elegir sería oro y está al alcance | **Aceptada (parcial)** | **Modo dictado** en L2/L3 con el pipeline de voz existente; se mantiene fuera de alcance la escritura libre |

### Alumno (8 años)

| Crítica | Decisión | Ajuste |
|---|---|---|
| Gano y no pasa NADA; quiero racha, que se guarde, desbloquear, mapa, que ganar se sienta | **Aceptada** | Capa de motivación/medición: racha, progreso guardado, desbloqueables, mapa de dominio visible, juice al acertar |
| 10 rondas de clasificar es mucho; a la 6 dejame pasar | **Aceptada** | Salida anticipada / bonus de velocidad desde la ronda 6 en clasificar |
| Cuando ACIERTO no me hagas leer nada | **Aceptada** | Microexplicación solo en el error |
| El reloj: quiero MOVER las agujas | **Aceptada** | Mecánica de arrastre de agujas (coincide con la maestra) |
| Textos de carpinchos/figuritas/goles/plata, no manual del cole | **Aceptada** | L9 y M13 con contextos de interés (animales, figuritas, dinero, deporte) |
| Restas con cero en el medio: la necesito AHORA | **Aceptada** | M6 con préstamo por el cero, prioridad alta en el orden de ataque |
| M8: repetime las que me salen mal, no todas mezcladas | **Aceptada** | La cola de repaso por ítem prioriza los productos fallados; "modo prueba" refuerza lo flojo |
| Modo "mañana tengo prueba" que me toma como Duolingo | **Aceptada** | Modo prueba (el adulto fija el tema; usa la cola de repaso) |
| Batalla en la cuadrícula = batalla naval de verdad con barcos que se hunden | **Ajustada (parcial)** | Se agrega framing de impacto y juice, **pero no barcos ocultos**: eso convertiría el constructo (leer coordenadas con vocabulario) en un juego de adivinar. El nombre promete batalla; se cumple con hit/miss y efecto, no con azar |
| Récords y competir contra otros | **Ajustada (parcial)** | Sí "récord propio de ayer"; **no** multijugador (no hay infra y desvía del refuerzo individual) |
| Cursiva, lectura en voz alta, dictado real quedaron afuera | **Descartada como cubierta, reconocida como límite** | Cursiva y voz alta siguen **fuera de alcance** (un motor táctil no las evalúa con honestidad); el dictado se cubre parcialmente con el modo dictado. Se sostiene en el marketing: es práctica y repaso, no "cubre 3°" |

### Auditor pedagógico externo

| Crítica | Decisión | Ajuste |
|---|---|---|
| §1.1 El dominio solo está definido para trivia (ordenar/clasificar/matching/trazado/programación se certifican por persistencia) | **Aceptada** | Reglas de dominio por tipo de mecánica (sección 2): ordenar = correcto al primer intento; últimos pares forzados no computan; C6 mide solo trivias; T1/T2 con variación generativa |
| §1.2 ¿Los aciertos con pista cuentan? | **Aceptada** | Solo el primer intento sin pista computa para el 85% |
| §1.3 El limbo 60-84% no tiene ruta de remediación | **Aceptada** | 3 sesiones en la franja → reintroduce CPA y prioriza los ítems fallados |
| §1.4 M8 relaciones tiene la respuesta impresa; L1 bisílabas 50/50; bingo eliminación pura; sesgo de longitud; M14 etiqueta rota | **Aceptada** | M8 reformulado sin imprimir el producto; L1 nivel 1 ≥3 sílabas; últimas pistas del bingo no computan; regla de longitud comparable; M14 distractor = celda válida transpuesta |
| §2 Distractores-relleno y sin regla generativa | **Aceptada** | Eliminados los chistes y los rellenos listados; los generadores entregan su tabla de reglas de error como código; M6 "760"/"845", M10 "848", M11 "6 y sobra 1", M5 "2.400", T1 "5" corregidos |
| §3.1 El rombo CSS (cuadrado rotado) tiene diagonales iguales: enseña la misconception | **Aceptada** | Rombo con escala no uniforme (diagonales desiguales) + ítem de cuadrado rotado clasificado como cuadrado |
| §3.2 La sopa deshace lo que enseña L3 | **Aceptada** | Coincide con la maestra: fuera de la sopa las palabras cuyo punto es la tilde/diéresis |
| §3.3 L1 nivel 3 imposible o trivial | **Aceptada** | Nivel 3 = clasificar oyendo palabras nuevas sin apoyo visual (no leer la tilde) |
| §3.4 M10 viola la regla CPA propia | **Aceptada** | Nivel 1 de M10 con la grilla de áreas coloreadas de M12 |
| §3.5 Rotación vs. calendario: B3 introducía 15-16 nuevas | **Aceptada** | Aparición escalonada dentro del bimestre; M11/M14/M17 adelantados a B2; L2 a B3 |
| §3.6 Repertorios que nacen en B4 no se consolidan | **Aceptada** | M17 y L12 salen de B4 (M17→B2, L12→B3); M16 queda en B4 como tema conceptual, no repertorio de retrieval |
| §3.7 Esfera/cono no grillables; redacción del vapor | **Aceptada** | Fallback de vista explotada para cono/cilindro/esfera; redacción de C1 corregida |
| §4.1 La cuenta 53×2-4 estaba maquillada | **Aceptada** | Se declara el rango real 106-212 sentadas |
| §4.2 8 bancos por debajo del mínimo | **Aceptada** | C6/L8/C7/C8 → "de exposición" (1-2 visitas, sin certificado); T1/T2/T3/T6 crecen a ≥18-20 + variación |
| §4.3 Los bancos de comprensión son consumibles | **Aceptada** | 2ª tanda de preguntas por texto (rotan por relectura con propósito distinto) + temporada 2 de textos a mitad de año |
| §4.4 Falta núcleo vs. extendido | **Aceptada** | 20 núcleo garantizadas por la rotación; 33 extendido |
| §5 Cola de repaso por ítem, desafío del día, mapa de dominio, modo explicá vos, recreo ganado | **Aceptada** | Todas en la capa de motivación/medición (sección 2) |

**Lo que el panel confirmó y NO se toca:** el menú explícito por edad; el balance mantener/endurecer/retirar (nada se tira, todo baja de edad); la honestidad del "fuera de alcance"; el diseño de L2 (tres veces la misma palabra), M6 (476, el bug universal), M12 (5+6=11), L9 (detalle-verdadero-vs-idea-principal); y la elección de las mecánicas nuevas (repetir×N, tokens, contador) como las que más contenido de 3° habilitan por peso de desarrollo.

---

## 6. Esfuerzo de construcción

### A · Curación pura (ajustar cfg/parámetros — horas, no días)
- **FIX del bug de `serie` invertida** (tope explícito por edad: `actividades_web.py:169-176` + `actividades_player.js:5735`). **Es un bug: va primero.**
- Retiros del menú de 8 (lista explícita por edad): patron, contar, quefalta, estaciones, animal_comida, separador_mezclas.
- laberinto 12-14 para e==8; **sopa con exclusión de palabras de tilde/diéresis**; rondas, pesos y salida anticipada de la rotación; marcar recreo vs. curricular; marcar bancos "de exposición".

### B · Banco/generador nuevo sobre mecánica EXISTENTE (el grueso: ~750+ ítems manuales verificados a mano + 9 generadores Python)
- **Generadores con distractores por regla de error** (Python, sin tocar el player), cada uno con su **tabla de reglas como código revisable**: M1, M2, M3\*, M5, M6, M7, M9, M10, M11, M14, M17 (\*M3 requiere además el contador, ver C).
- **Bancos manuales** sobre trivia/cloze/clasificar/ordenar/matching/tocar-N: M4, M8-relaciones, M12, M13 (**40**), M15 (**24**, rombo con diagonales desiguales), M16 (**24** con `usados`), M18, L1-L10 (L2/L3 a **40**, L9 a **24-30 textos + 2ª tanda**), L11-L17, C1-C10 (C6/C7/C8 de exposición), T2-T8 (T6 a 16-20; T7 con contraejemplos). Los **textos de L9** y los poemas/micro-narraciones de L8/L16 son el ítem de mayor costo unitario y de mayor valor diferencial (hoy el producto no tiene NI UN texto).
- **Audio por palabra** para L1, L2, L3 (dictado), L14 (~90 palabras): pipeline de voz existente (ElevenLabs / generar_audio_consignas). Es producción, no desarrollo.
- **Ilustración representacional en CSS inline** (sin assets pesados): figuras de M15 (rombo con escala no uniforme), desarrollos/vistas explotadas de M16, reloj de M17, barras de M18, grillas de áreas de M10/M12, globos de L7, rótulos de T6.
- **Lint + validación humana** de los 750: (a) longitud comparable, (b) misconception nombrada y ejecutable, (c) cero chistes, (d) ojos de maestra ítem por ítem.

### C · Mecánica nueva mínima (4 mecánicas + capa de motivación)
1. **Bloque "repetir ×N" + ejecución paso a paso + animación del robot** en programar_camino → habilita **T1, T2 y T3** (todo el eje de programación de 3°). La inversión más rentable del mapa.
2. **Tokens tocables dentro de una palabra/oración** (extensión de tap-selección) → habilita **L1** (sílaba tónica) y **L11** (quién hace qué).
3. **Contador de billetes múltiples** (extensión de "tocar 2 que sumen X" a N con total visible) → habilita **M3** y el modo vasos de **M18**.
4. **Mover agujas del reloj con arrastre** → habilita **M17** completo. Sube de "inversión aparte" al mapa por pedido convergente de maestra y alumno; **prioridad por encima del generador de sudoku 6×6**.
- **Capa de motivación y medición** (engine-level, transversal, no por-actividad): dominio operacionalizado por tipo de mecánica, ruta del limbo 60-84%, **cola de repaso por ítem**, **desafío del día**, **mapa de dominio visible + reporte bimestral**, racha/guardado/desbloqueables/juice, modo prueba, modo "explicá vos", recreo ganado. Es lo que separa "catálogo grande" de "producto que un padre renueva".
- Inversión Python chica adicional: generador de sudoku 6×6 (si no se hace, sudoku se retira de 8 sin culpa).

### Declarado como inversión APARTE (no se promete)
Viñetas de historieta ilustradas, "Entrená a la máquina" (IA con ejemplos y sesgos), grabación de lectura en voz alta con evaluación de fluidez, canvas de trazo para cursiva y copia de figuras. Cada una es una mecánica o pipeline de assets nueva; se evalúan como features separadas si 3° valida ventas.

### Orden de ataque sugerido
1. **Curación A completa** — incluye el bug de `serie`.
2. **M5/M6/M1/M2/M3 + L1/L2** — los dos gaps estrella (rango numérico y acentuación); **M6 con préstamo por el cero, prioridad de la casa**.
3. **M11 (división) + L9 (texto real desde B1)** — los otros dos nodales ausentes.
4. Las 4 mecánicas de C **en paralelo** con quien escriba bancos (la de repetir y la de agujas primero).
5. El resto de B por bimestre de aparición; la capa de motivación en paralelo desde el inicio (es scheduling y UI, no bloquea los bancos).
