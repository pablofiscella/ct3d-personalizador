# 6° grado (11 años)

Dossier definitivo del cuaderno de actividades interactivo para 6° grado, integrando: auditoría curricular externa (vs. DC CABA 2024), propuesta de diseño, y panel revisor (maestra de grado, alumno de 6° "Fran", auditor pedagógico externo). Todas las observaciones válidas del panel están incorporadas; los descartes se justifican en §5.

**Decisión editorial que ordena todo el dossier:** el mapa de *contenido* es curricularmente sólido, pero el auditor demostró —y yo reverifiqué en el código— que **tres de las cinco "reglas no negociables" que el producto declara cumplir NO existen en el motor** (`actividades_player.js`): no hay compuerta de dominio, no hay generador de distractores conceptuales para lo paramétrico, y no hay render de la explicación del porqué. Por eso el año se organiza en dos capas: **Capa 0 (motor + enganche), que es requisito y va primero**, y encima las ~70 actividades de contenido. Construir 70 actividades sobre el motor actual produce, textual del auditor, "62 actividades ganables por eliminación en 3 horas, vendidas como un año de refuerzo". El contenido no se escala hasta cerrar la Capa 0.

---

## 1. Estado actual — veredicto de auditoría

De los 25 juegos que hoy ve un alumno de 6°: **3 alineados, 1 alineado-en-tema/fácil-en-mecánica, 4 muy fáciles, 12 desalineados (contenido de 1er ciclo/inicial o de otro grado), 5 sin anclaje**. Tasa de alineación real: **~12%**. Verificado en `actividades_web.py`: el bloque `if e == 11` (L318) solo retoca `simon` y agrega 8 trivias; los 17 juegos base se sirven **idénticos a 1° grado**. Agravante regresivo: 4° recibió el parche `suma_columnas` (L290-293) y 6° no — hoy un chico de 11 hace sumas más fáciles que uno de 9.

| # | Juego | Veredicto | Motivo (vs. DC 6°) |
|---|-------|-----------|--------------------|
| 1 | memotest (8 pares) | SIN ANCLAJE | Memoria visual; tolerable como evergreen, no computa cobertura. |
| 2 | laberinto (9-12) | SIN ANCLAJE | Destreza espacial; idéntico de 1° a 7°. |
| 3 | programar_camino (3×3-4×4) | MUY FÁCIL | Secuencial puro; el DC Tec 6° pide condicionales, funciones, bloques↔código. |
| 4 | sopa (10×10) | SIN ANCLAJE | Vocabulario decorativo (CUMPLE, FIESTA), no científico-disciplinar del grado. |
| 5 | sudoku (4×4, 8 pistas) | MUY FÁCIL | Generador del nivel inicial; el propio código lo ubica "recién para lectores" (~6 años). |
| 6 | sumas (a+b ≤ 10, sprites) | DESALINEADO (1°) | Sumar hasta 10 contando dibujos; el DC pide operaciones combinadas con jerarquía. |
| 7 | restas (≤ 10, sprites) | DESALINEADO (1°) | Ni siquiera tiene el reemplazo por columnas que sí tiene 4°. |
| 8 | serie (tope 16, paso 1-2) | DESALINEADO + invertido | Llega a 16 a los 11; a los 6 llega a 30 (tope:30 solo en e==6). |
| 9 | patron (ABC/AABB) | DESALINEADO (Inicial) | Patrones de sprites de sala de 5. |
| 10 | puntos (10-14) | DESALINEADO (jardín) | Unir 10-14 vértices en orden. |
| 11 | contar (≤ 9) | DESALINEADO (Inicial) | Conteo 1-9 con distractores; el DC opera sin restricción de rango. |
| 12 | colorear | SIN ANCLAJE | Recreativo puro, idéntico de 2 a 12 años. |
| 13 | mas_menos (≤ 9) | DESALINEADO (Inicial) | Comparar cardinales; en 6° se comparan fracciones y decimales en la recta. |
| 14 | simon (9 colores) | SIN ANCLAJE | Único base que escala por grado (bien), pero sin contenido DC. |
| 15 | agrupar (matching idéntico) | DESALINEADO (maternal) | Emparejar sprites idénticos; a los 11 clasificar debería ser conceptual. |
| 16 | quefalta (5 ítems) | MUY FÁCIL | Memoria visual de nivel inicial. |
| 17 | bingo (3×3, con pista) | MUY FÁCIL | Reconocimiento visual asistido, sala de 4-5. |
| 18 | celula_partes | DESALINEADO (7°) | Organelas (Golgi, retículo, mitocondria) no están en 6°; el eje es ecosistema, reproducción, calor, astronomía. |
| 19 | hechos_opiniones | MUY FÁCIL (anclaje parcial) | Marcadores obvios ("creo", "feísimo"); el DC 6° pide columna de opinión fundamentada. |
| 20 | sistema_nervioso | DESALINEADO (7°) | Neuronas/sinapsis/reflejos no figuran en 6°; el organismo humano en 6° = reproducción (ESI). |
| 21 | viaje_inmigrante | ALINEADO en tema / FÁCIL en mecánica | Tema nodal, pero 4 etapas fijas ×4 rondas = memoria desde la ronda 2 (JS L4716). |
| 22 | fraccion_de_cantidad | ALINEADO (rango corto) | Único juego de mate a nivel de 6°; resultados topados en 12; distractores al azar (L4807). |
| 23 | sufragio_argentina | ALINEADO | Ley Sáenz Peña 1912, nodal. V/F puro (2 botones, L4876) = 50% por azar. |
| 24 | energia_renovable | ALINEADO (defecto UI) | Estímulo solo-emoji (🌋 geotérmica, ⚫ carbón) mide decodificación del ícono, no el concepto. |
| 25 | poligonos_lados | DESALINEADO (3°-4°) | Nombre→cantidad de lados; la geometría nodal de 6° es mediatriz, paralelogramos, 360°, desarrollos. |

**Hallazgo estructural transversal (reverificado en código, no solo en la prosa del auditor):** el motor incumple 3 de las 5 reglas estrella para las 25 y para cualquier actividad nueva:
- **Sin compuerta de dominio.** `win()` se dispara con `ronda >= rondas` (30+ llamadas idénticas). 1 estrella también cuenta como "completado" y se guarda (`Store.setStars`, L337). No existe umbral 80-90% ni tracking de "acertó al primer intento".
- **Se gana por eliminación.** El clic incorrecto solo llama `casi()` (L332: incrementa contador + sonido) y reintenta el MISMO ítem; el correcto avanza. Con 3 opciones y reintentos ilimitados, se completa en ≤3 clics por ronda. Los V/F (sufragio) son 50% por moneda.
- **Sin explicación del porqué.** 82 llamadas a `casi(` en el archivo; **ninguna** pasa un texto de explicación. La regla "todo error dispara el porqué (más detalle a los 11)" no está implementada.
- **Distractores paramétricos al azar.** `fraccion_de_cantidad`: `item.correcta + rint(-3,3)` (L4807). `poligonos_lados`: `item.lados + rint(-2,2)` (L4993). Valores cercanos aleatorios, no errores conceptuales.

### Los 5 gaps más graves

1. **Lengua = 0 actividades.** Área troncal ausente, con 15 gamificables ya especificados en el DC. Y dentro de Lengua, **comprensión lectora = 0**: no hay un solo texto de más de una oración para leer y responder.
2. **Proporcionalidad + decimales + porcentajes = 0.** El corazón de Matemática de 6° (descuentos, presupuesto, escalas, cociente decimal) sin nada; es además lo más gamificable del diseño.
3. **Probabilidad y estadística (moda; sucesos posibles/imposibles/seguros) = 0.** Contenido que el DC hace nodal **por primera vez** en 6°; ausencia total.
4. **Reproducción humana / pubertad (Naturales + ESI) = 0**, mientras se sirven célula y sistema nervioso, que son de 7°.
5. **Geometría de 6° (mediatriz, paralelogramos, 360°, desarrollos de cilindros/conos) = 0**, enmascarada por `poligonos_lados`, que es de 3°-4°.

---

## 2. Mapa propuesto del año

### Capa 0 — Motor y enganche (REQUISITO, va antes que el contenido)

No es una actividad: es la base sin la cual las 70 actividades "son marketing, no mecánica" (auditor). Convergen acá el auditor (dominio, distractores, porqué), la maestra ("el 'explicá por qué está mal' es el corazón del valor, el maestro suplente cuando no hay adulto al lado") y Fran ("por qué vuelvo mañana solo").

| # | Cambio de motor | Qué resuelve | Regla / crítica que cierra |
|---|---|---|---|
| C0-1 | **Compuerta de dominio real**: puntaje por *primer intento*, umbral 80-90%, no se cierra la ronda por reintento, se **re-sirven** los ítems fallados. | Convierte "clic hasta acertar" en práctica. Habilita la espiral (dominar B2 antes de B3). | Regla "acertó 1° intento ≠ acertó eventualmente"; auditor §1. |
| C0-2 | **Campo `porque` por distractor + render en `casi()`.** Reusa las racionalizaciones ya escritas en cada ítem. Más detalle a los 11. | Entrega la garantía "explicación del porqué"; es el mayor multiplicador de aprendizaje por ítem. | Regla "cero fail state con porqué"; auditor §3; maestra §3. |
| C0-3 | **Generador de distractores por misconception** (computa el resultado del error, no `rint`). Ej.: "solo dividió por el denominador", "numerador×total", "movió un solo lugar". | Hace conceptuales los distractores de los ~22 paramétricos de Mate/Lengua. | Regla "distractor = error real, NUNCA al azar"; auditor §2. |
| C0-4 | **Generalizar "ordenar secuencia"** a bancos variados (hoy `viaje_inmigrante` tiene 4 etapas hardcodeadas). | Base real de L2, N4, N6, S1, S5, T4, Tr5 sin memorización de posición. | Auditor §1.d. |
| C0-5 | **Capa de enganche**: racha diaria (🔥), XP/nivel, mapa del año que se pinta, elegir qué jugar, contrarreloj contra uno mismo en los paramétricos, "nivel jefe" (difícil, con corona) al dominar, desbloqueables (temas/avatar). | La única sección que responde "por qué vuelvo solo un domingo". Sin esto es "un cuaderno de tareas muy lindo" (Fran). | Fran §3 (completa, hoy ausente del plan); auditor §5 (re-jugabilidad con valor). |
| C0-6 | **Modo repaso espaciado / gateo por bimestre**: resucita ítems ya dominados semanas después. | Hace real la "práctica espaciada" que el mapa promete pero el motor no gatea. | Auditor §5.c; espiral de §4. |

### Números totales

| Concepto | Cantidad |
|---|---|
| **Actividades curriculares** | **70** |
| — Matemática | 23 |
| — Lengua | 16 |
| — Ciencias Naturales | 11 |
| — Ciencias Sociales | 10 |
| — Tecnología, Diseño y Programación | 5 |
| — Transversales (ESI/FEC/Financiera/Ambiental/Digital) | 5 |
| **Evergreen sin anclaje** (repaso/recompensa, NO computan cobertura) | 3 |
| **Total propuestas** | **73** |
| De las cuales: nuevas a construir | ~62 |
| Endurecidas desde un juego existente | ~8 |
| Retiradas de e==11 | 11 |
| Movidas a 7° (e==12) | 2 |

**Bancos (recalibrados por el panel):** los **paramétricos** (~22 actividades de Mate/Lengua) son de generación infinita — bien. Los de **banco fijo de contenido rico** suben de 12-16 a **25-30 ítems** (con 12-16, la 2ª pasada repite 8/10 y queda quemado a mitad de año). Los de **tope real** (planetas 8, poderes 3, ecorregiones 3, etapas del ciclo 4-5, etapas de diseño 5) no se agrandan —la realidad los fija—: la variedad viene de **bancos grandes de ítems asociados** (especies por ecorregión, funciones por poder, mitos por fase), no de 12. Total curado a mano ≈ **1.200 ítems verificados** (revisado al alza desde los "850" del diseño, que mezclaban infinitos con topes de 3-8). **Todos los distractores pasan un control matemático** antes de construir (ver §5, punto de la maestra).

Formato de las tablas: actividad · mecánica (reuso) · banco · dificultad inicial→final · contenido DC. **(N)** = actividad nueva agregada por pedido del panel. **(◎)** = MVP táctil que NO cubre el nodal completo sin su simulación (marcado honesto).

### MATEMÁTICA (23)

| Actividad | Mecánica | Banco | Dif. | Contenido DC |
|---|---|---|---|---|
| M1 Números gigantes | ordenar/tap-posición | paramétrico | 5-6 cifras → 7-9 mismas cifras | Lectura, orden y valor posicional sin restricción de rango |
| M2 Criba de primos | grilla del 100 + contrarreloj | grilla + 25 preg. | guiada → libre contrarreloj | Primos y compuestos; múltiplos/divisores comunes |
| M3 Detector de divisibilidad | clasificar canastas + contrarreloj | paramétrico | 1 criterio → los 3 | Criterios por 2, 5, 10 |
| M4 Armá el cálculo | armar expresión con fichas | paramétrico | sin () → con () | Operaciones combinadas y jerarquía |
| M5 Reconstruí la división | completar / tap | paramétrico | hallar r → hallar D → restos imposibles | c×d+r=D; r<d |
| M6 Podio de permutaciones | ordenar + multiplicar | paramétrico | 3→4 elementos; 2 conjuntos | Combinatoria: permutaciones; combinación de 2 conjuntos |
| M7 Fracción de una cantidad | **barra CPA** → símbolo | paramétrico (sin tope 12) | total múltiplo → no múltiplo | Fracción de un natural, numerador ≠ 1 |
| **M7b Fracciones equivalentes (N)** | barra CPA + matching | paramétrico | amplificar → simplificar | Equivalencia (cimiento de comparar/sumar/restar) |
| M8 Zoom en la recta **(◎)** | recta con zoom (MVP = tap "¿cuál está entre?") | paramétrico | elegir entre → colocar | Densidad; orden en la recta |
| **M8b Suma y resta de fracciones (N)** | **barra CPA**, común denominador | paramétrico | igual denom. → distinto denom. | Suma/resta con distinto denominador (EL muro de 6°) |
| M9 Parejas que dan 1 | memotest | 14 cartas | inversas simples → mezcladas | Fracción inversa (producto = 1) |
| M10 Área fraccionaria **(◎)** | pintar cuadrícula CPA | paramétrico | no simplifica → simplifica | Multiplicación de fracciones como área |
| M11 Corredor de la coma | mover coma (MVP = tap resultado) | paramétrico | ×10 → cadenas + redondeo | ×/÷ por la unidad seguida de ceros; valor posicional decimal |
| M12 Multiplicar con coma | tap anticipando cifras decimales | paramétrico | 1 factor decimal → 2 | Multiplicación de decimales; cociente decimal |
| M13 La tienda de descuentos | tap comparando ofertas | paramétrico | % simple → sucesivos/2×1 | Descuentos y aumentos, incluso sucesivos; oferta conveniente |
| **M13b Porcentaje de una cantidad (N)** | barra CPA, "saco el 30% de 8.000" | paramétrico | % redondos → cualquiera | Porcentaje de una cantidad (hermano de M7, top-3 de lo que no entienden) |
| M14 Proporcionalidad aplicada | repartir 100% + tap escala | paramétrico | completar % → escala con unidades | Presupuesto con %; escalas; constante |
| M15a Cuadriláteros y ángulos | clasificar/V-F + completar | 25 ítems | reconocer → hallar dato | Mediatriz; paralelogramos; ángulos interiores = 360° |
| M15b Cuerpos y desarrollos | tap "¿qué desarrollo arma?" (line-art 2D) | 25 ítems | reconocer → asociar | Desarrollo plano de cilindros y conos; cuerpos |
| M16 Mismo área, otro borde | manipular rectángulo en grilla + tap | paramétrico | observar → fórmula | Independencia área/perímetro; fórmulas; m²↔cm² |
| M17 La moda de la encuesta | cargar datos → barras → tap moda | 25 sets | moda evidente → cercana | Frecuencias absolutas/relativas; gráficos; moda |
| M18 ¿Seguro, posible o imposible? | clasificar en 3 + justificar | 25 ítems | cotidiano → dados/bolitas | Sucesos posibles/imposibles/seguros (nodal NUEVO de 6°) |
| **M-prob Resolvé el problema (N)** | leer enunciado corto → elegir la operación/planteo | 30 problemas | 1 paso → varios pasos | Problemas de varios pasos; decidir la operación (pedido #1 de familias y de Fran) |

> **Gap declarado con honestidad (maestra §1 y Fran §4): la división por dos cifras — la CUENTA larga — NO tiene una mecánica que la enseñe.** M5 trabaja la relación c×d+r=D y el resto, no el algoritmo. Se propone una **práctica guiada paso a paso asistida** (bajar cifra, multiplicar, restar) como *inversión aparte* con andamiaje C0-2; hasta construirla, se rotula en la ficha docente: "esto entrena el resto y la estimación, no reemplaza practicar la cuenta larga". No se vende como cubierta.

**Distractores destacados (misconception real, ya con el control matemático aplicado — corrigiendo dos errores que señaló la maestra):**
- M13b: 30% de $8.000 = $2.400 (distractor: $240 — corrió mal la coma; distractor: $5.600 — calculó el 70%).
- M12 (corregido): **2,5 × 4 = 10** (distractor: 8 — hizo 2×4 e ignoró el 0,5; distractor: 12,5 — hizo 2,5×5). *(El distractor original "2,20" no mapeaba a ningún error real.)*
- M12 (corregido): **3 ÷ 4 = 0,75** (distractor: 1,33 — invirtió y calculó 4÷3; distractor: 0,7 — truncó en el décimo). *(El original "0,34" no correspondía a un error limpio.)*
- M8b: 1/2 + 1/3 = 5/6 (distractor: 2/5 — sumó numeradores y denominadores; distractor: 2/6 — igualó denominadores sin ajustar numeradores).

### LENGUA (16)

| Actividad | Mecánica | Banco | Dif. | Contenido DC |
|---|---|---|---|---|
| **L0 Leé y respondé (N)** | **texto corto (120-180 pal.) + opción múltiple inferencial** | 25 textos | literal → inferencia/predicción | Comprensión lectora real: qué quiso decir / qué va a pasar / por qué |
| **L0b Idea principal y cuadro sinóptico (N)** | subrayar idea central + armar cuadro (ordenar/arrastrar) | 20 textos | idea principal → jerarquizar | Técnicas de estudio (puente a la secundaria) |
| L1 Anatomía de la noticia | rotular zonas (etiqueta→zona) | 25 notas | 3 partes → 6 + crónica | Partes de la noticia; crónica |
| L2 Resolvé el caso | ordenar secuencia + clasificar roles | 25 casos | 3 elementos → caso completo | Relato policial: enigma/pistas/hipótesis/resolución |
| L3 Bestiario de la ciencia ficción | matching personaje→definición | 25 | 2 → los 4 | CF: robot, androide, cyborg, científico |
| L4 ¿Fuente confiable? | tap la más confiable | 25 | contraste → matices | .edu/.org/.gob/.com/.net; palabras clave |
| L5 Del directo al indirecto | tap/completar verbo y conector | 25 | persona → persona + tiempo | Discurso directo↔indirecto; biografía↔autobiografía |
| L6 Clasificá pronombres | clasificar en categorías | 25 | 2 tipos → los 4 | Pronombres personales/posesivos/demostrativos/indefinidos |
| **L7a Radiografía de la oración (N-desdoble)** | tap sobre palabras | 25 | núcleos → modificadores | Sintagma nominal y verbal; núcleo/especificador/modificador |
| **L7b OD, OI y transitividad (N-desdoble)** | tap sobre palabras | 25 | OD vs adjunto → OD/OI → transitivo/intransitivo | Complementos vs adjuntos; verbos transitivos/intransitivos |
| L8 Conectores en acción | completar texto | 25 | temporales → causales | Conectores temporales/locativos/causales-consecutivos/síntesis |
| L9 Basta de repetir | tap el reemplazo | 25 | sinónimo → hiperónimo → pronombre | Cohesión léxica; referencia pronominal |
| L10 Sonidos del poema | tap sobre el verso | 25 | 2 recursos → los 5 | Aliteración, onomatopeya, personificación, comparación, hipérbole |
| L11 Conjugá el verbo | completar/tap según contexto temporal | paramétrico | presente → imperfecto vs perfecto simple | Conjugación del indicativo |
| **L12a Tildes rebeldes (N-desdoble)** | tap "¿lleva tilde?" | 25 | agudas/graves/esdrújulas → diacrítica/-mente/hiato | Acentuación (unidad entera, hoy media actividad) |
| **L12b Puntuación fina (N-desdoble)** | tap "¿qué signo va?" | 20 | coma/punto → paréntesis/comillas/suspensivos | Puntuación |

> **hechos_opiniones (existente)** se endurece y se pliega dentro de L0/L4: hecho *verificable* vs opinión *fundamentada*, sin los marcadores gratis ("creo", "feísimo") que Fran detecta sin leer, como puente a la columna de opinión.

### CIENCIAS NATURALES (11)

⚠ **Bloque ESI (N4-N6): el producto señaliza arriba que hay contenido de educación sexual integral**, con nota para la familia (pedido de la maestra §1: evitar la sorpresa de "ciclo menstrual" y "métodos" sin aviso).

| Actividad | Mecánica | Banco | Dif. | Contenido DC |
|---|---|---|---|---|
| N1 Armá la red del ecosistema | conectar nodos (MVP matching) + clasificar | 25 | clasificar → armar red | Autótrofo/heterótrofo; sistemas abiertos |
| N2 Roles y niveles | clasificar en 3 + arrastrar al nivel | 25 | roles → niveles | Productores/consumidores/descomponedores; especie/población/comunidad; CABA antrópica |
| N3 Ecorregiones de Buenos Aires | matching ecorregión→especies (mapa) | 3 regiones × banco grande de especies | nombrar → asociar | Pampa, Espinal, Delta e islas |
| N4 Línea de la vida y la pubertad ⚠ESI | ordenar + matching cambio→causa | 25 | ordenar → refutar "todos igual" | Etapas de la vida; pubertad y hormonas; variabilidad individual |
| N5 El ciclo menstrual y los mitos ⚠ESI | ordenar fases + V/F con fundamento **(+3ª opción)** | 4-5 fases + 25 mitos | fases → refutar mitos | Ovulación vs menstruación; creencias |
| N6 Del cigoto al feto ⚠ESI | ordenar + matching método→qué previene | 25 | ordenar → asociar métodos | Fecundación; cigoto/embrión/feto; anticonceptivos; preservativo e ITS |
| N7 Estados, partículas y calor **(◎)** | slider de partículas (MVP = tap "¿qué pasa?") | 25 | predecir → explicar → flujo de calor | Modelo de partículas; calor en tránsito; equilibrio térmico |
| N8 Elegí el material térmico | tap el material adecuado | 25 | usos claros → casos límite | Conductividad, dilatación y usos |
| N9 Del geocentrismo al heliocentrismo | tap modelo + ordenar planetas | 8 planetas + 25 preg. | identificar → ordenar a escala | Geo→heliocéntrico; sistema solar a escala; Venus/Júpiter |
| **N10a Tiempo vs. clima (N-desdoble)** | clasificar tiempo/clima | 25 | variables → distinguir | Variables meteorológicas; tiempo vs clima |
| **N10b Efecto invernadero (N-desdoble)** | clasificar fuentes directo/indirecto (+ slider, inversión) | 25 | reconocer GEI → mitigación | Gases de efecto invernadero; procesos directos/indirectos |

> **(◎) N7 honesto:** sin la simulación de partículas, el MVP táctil cubre el *vocabulario* ("las partículas se separan"), NO el *modelo*. La maestra y el auditor coinciden: acá la simulación no es lujo, es el aprendizaje. Se marca como inversión aparte con fallback táctil declarado.

### CIENCIAS SOCIALES (10)

| Actividad | Mecánica | Banco | Dif. | Contenido DC |
|---|---|---|---|---|
| S1 Línea de tiempo 1862-1930 | ordenar hitos | 25 hitos | 4 → 8 fechas cercanas | Unificación 1862, federalización 1880, Ley 1420, Sáenz Peña 1912, Yrigoyen 1916, golpe 1930 |
| S2 ¿1ª o 2ª Revolución Industrial? | clasificar + modo centrales/periféricos | 25 | energías → división del trabajo | Vapor vs petróleo/electricidad; centrales/periféricos |
| S3 Construcción del Estado y agroexportación | matching presidente→obra + conectar circuito | 25 | asociar → armar circuito | Mitre/Sarmiento/Avellaneda; modelo agroexportador; ferrocarril y puerto |
| S4 Inmigración: censos y conventillo | leer tabla/gráfico + tap + escena | 25 | leer un dato → comparar décadas | Inmigración ultramarina; censos; conventillo; Ley 1420 |
| S5 El voto antes y después | V/F **(+3ª opción)** + ordenar | 25 | voto → secuencia radical | Sáenz Peña 1912; gobiernos radicales; golpe 1930 |
| S6 La Gran Guerra y la crisis del '29 | clasificar bandos + causa/consecuencia | 25 | bandos → cadena causal | 1ª Guerra Mundial; crisis de 1929 y su impacto en Argentina |
| S7 Mercosur y la energía que viaja | clasificar países + matching instalación→función | 25 | parte/asociado → infraestructura | Integración regional; grandes instalaciones de energía |
| **S8a Demografía en gráficos (N-desdoble)** | matching variable→definición/gráfico | 25 | definiciones → leer gráfico | Natalidad, mortalidad, esperanza de vida; censos |
| **S8b Escalas ambientales (N-desdoble)** | clasificar por escala | 25 | local → global | Escalas local/regional/global; mitigación de riesgo |
| S9 Mi Buenos Aires querido | matching ícono→año + trivia con imágenes | 25 | emparejar → años cercanos | Tango UNESCO, fileteado; Obelisco 1936, línea A 1913, Reserva 1986, Mataderos 1889 |

### TECNOLOGÍA, DISEÑO Y PROGRAMACIÓN (5)

| Actividad | Mecánica | Banco | Dif. | Contenido DC |
|---|---|---|---|---|
| T1 Elegí el instrumento | tap + armar diagrama de bloques | 25 | instrumento → medida absurda → diagrama | Instrumento y escala; sensor→procesamiento→display |
| T2 ¿Secuencial o condicional? | armar-programa Logo con bloque SI + tap | 25 mini-algoritmos | secuencial → condicional → el más corto | Algoritmos no lineales (condicionales); comparación de algoritmos |
| T3 Bloques ↔ código | matching bloque↔código | 25 | 1 estructura → bucles + condicionales | Programación en bloques y su relación con el código |
| T4 Las 5 etapas del diseño | ordenar + arrastrar acción→etapa | 5 etapas + banco grande de acciones | ordenar → clasificar | Empatizar/definir/idear/prototipar/evaluar |
| T5 Invernadero reactivo y sensores | armar reglas si-entonces + clasificar sensores + tap autoría | 25 | una regla → varias + señal de autoría | Control reactivo; sensores analógico/digital; autoría de contenidos IA |

> T5 concentra tres nodales; se acepta el agrupamiento pero se dosifica con banco de 25 y tres modos rotados. Si se prioriza, se desdobla "Capas de internet y sesgos de la IA" como 6ª.

### TRANSVERSALES (5)

| Actividad | Mecánica | Banco | Dif. | Contenido DC |
|---|---|---|---|---|
| Tr1 Chat seguro (grooming) | **chat ramificado** (MVP ordenar + tap acción) | 15 escenas | reconocer etapa → acción → detectar el secreto | Grooming como delito; cómo actuar (ESI+ED) |
| Tr2 Mitos, ITS y tipos de violencia | V/F **(+3ª opción)** + clasificar | 25 | mitos → clasificar violencia | ITS/VIH: vías y prevención; tipos de violencia (ESI) |
| Tr3 Los tres poderes y la ley | clasificar función→poder + ordenar el camino de la ley | 3 poderes + banco grande de funciones | asignar → ordenar | Poderes; sanción de leyes; sufragio (FEC) |
| Tr4 Billetera virtual y presupuesto | detectar estafa (tap) + repartir presupuesto | 25 | detectar señal → armar presupuesto | Medios de pago y seguridad; presupuesto con % (Financiera/ED) |
| Tr5 Economía circular y el Riachuelo | reconstruir ciclo (ordenar) + ordenar hitos | 25 | clasificar → reconstruir | Lineal vs circular; obsolescencia; cuenca Matanza-Riachuelo (EA) |

### EVERGREEN sin anclaje (3) — repaso/recompensa, NO computan cobertura
memotest (8 pares del tema) · laberinto (9×9-12×12) · colorear. Disponibles todo el año como pausa/recompensa. **simon** se mantiene aparte como memoria (único base que ya escala por grado).

---

## 3. Cambios al catálogo actual (los 25 juegos de e==11)

Verificado en `actividades_web.py` L318-343: `if e == 11` solo retoca `simon` y agrega 8 curriculares; los 17 base son idénticos a 1°.

| # | Juego actual | Acción | Detalle / parámetros nuevos |
|---|---|---|---|
| 1 | memotest | **MANTENER** | Evergreen. `pares: 8` OK. |
| 2 | laberinto | **MANTENER** | Evergreen. Tamaños 9-12 OK. |
| 3 | programar_camino | **ENDURECER → T2** | Agregar bloque condicional (SI) + comparar dos programas; niveles 5×5-6×6; 8-12 pasos. Es nodal de Tec, no evergreen. |
| 4 | sopa | **MANTENER + RECALIBRAR** | Cambiar banco genérico (CUMPLE, FIESTA) por vocabulario de 6° (heliocéntrico, ecorregión, sufragio, androide, mediatriz). |
| 5 | sudoku | **ENDURECER** | Retirar 4×4-8 pistas (inicial). Subir a **6×6 con menos pistas** o retirar de e==11. |
| 6 | sumas (≤10) | **RETIRAR de e==11** | Contenido de 1°. Su lugar lo ocupa M4 (jerarquía). |
| 7 | restas (≤10) | **RETIRAR de e==11** | Contenido de 1°. Su lugar lo ocupa M5 (división/resto). |
| 8 | serie (tope 16) | **RETIRAR de e==11** | Nivel 1°-2° con dificultad invertida. Su lugar lo ocupa M1. |
| 9 | patron (ABC/AABB) | **RETIRAR de e==11** | Nivel inicial. |
| 10 | puntos (10-14) | **RETIRAR de e==11** | Nivel jardín. |
| 11 | contar (≤9) | **RETIRAR de e==11** | Nivel inicial. |
| 12 | colorear | **MANTENER** | Evergreen/recompensa. |
| 13 | mas_menos (≤9) | **RETIRAR de e==11** | Comparación de 6° = fracciones/decimales en la recta → M8. |
| 14 | simon (9/3×3) | **MANTENER** | Único base que ya escala por grado; memoria/recompensa. |
| 15 | agrupar (idénticos) | **RETIRAR de e==11** | Matching de idénticos es maternal. La *mecánica* de clasificar se reusa cargada con contenido conceptual (M3, N2, S2…). |
| 16 | quefalta (5 ítems) | **RETIRAR de e==11** | Nivel inicial. |
| 17 | bingo (3×3) | **RETIRAR de e==11** | Nivel inicial. |
| 18 | celula_partes | **MOVER a 7° (e==12)** | Organelas no son de 6°. Su lugar lo ocupan N1/N2 (ecosistema). |
| 19 | hechos_opiniones | **ENDURECER** | Sacar marcadores obvios; hecho verificable vs opinión fundamentada; se pliega en L0/L4. |
| 20 | sistema_nervioso | **MOVER a 7° (e==12)** | Neuronas/sinapsis no están en 6°. Su lugar lo ocupan N4-N6 (reproducción/pubertad). |
| 21 | viaje_inmigrante | **ENDURECER → S4** | Hoy 4 etapas fijas ×4. Banco variado: censos, condiciones de vida, causas de emigración. Requiere C0-4 (generalizar ordenar). |
| 22 | fraccion_de_cantidad | **ENDURECER → M7** | Sacar tope 12; **barra CPA** antes del símbolo; distractores conceptuales vía C0-3 (reemplaza `rint(-3,3)`). |
| 23 | sufragio_argentina | **ENDURECER → S5** | Banco ampliado (radicales, 1930); **agregar 3ª opción** (hoy V/F puro = 50% azar); nota docente: Ley 13.010 (1947) excede el recorte. |
| 24 | energia_renovable | **ENDURECER → N10b** | Reemplazar estímulo solo-emoji (🌋 ambiguo) por **texto + imagen**; sumar GEI y mitigación. |
| 25 | poligonos_lados | **RETIRAR de e==11** | Nombre→lados es de 3°-4°. Su lugar lo ocupan M15a/M15b (geometría real de 6°). |

**Resumen:** MANTENER 4 (memotest, laberinto, colorear, simon) · ENDURECER 8 (programar_camino, sopa, sudoku, hechos_opiniones, viaje_inmigrante, fraccion_de_cantidad, sufragio, energia) · MOVER a 7° 2 (célula, sistema_nervioso) · **RETIRAR de e==11 11** (sumas, restas, serie, patron, puntos, contar, mas_menos, agrupar, quefalta, bingo, poligonos).

---

## 4. Progresión del año (4 bimestres)

Principio **espiral** (lo abstracto se reusa aplicado más adelante) **corregido con la advertencia de la maestra**: geometría, medida y probabilidad **NO van al final** —el B4 en la escuela porteña real es el más corto y comido (actos, muestra, integradoras, cierre de notas desde noviembre, viaje de egresados)—. Geometría se **reparte** todo el año (las construcciones necesitan meses), probabilidad se **adelanta a septiembre**, se **aliviana B2** (estaba con 7 mate de golpe) y B4. **Mi Buenos Aires (S9) se adelanta a junio**, cerca del Día de Buenos Aires (11/6), en vez de desperdiciar el anclaje al final. El B4 queda de **cierre y aplicación**, no de contenido nuevo.

**Bimestre 1 (mar-may) — Arranque, números y primeras figuras.**
- Mate: M1 números gigantes, M2 criba de primos, M3 divisibilidad, M4 jerarquía, **M15a cuadriláteros y ángulos** (geometría entra temprano).
- Lengua: **L0 leé y respondé**, L6 pronombres, L7a radiografía de la oración, L1 anatomía de la noticia.
- Naturales: N1 red del ecosistema, N2 roles y niveles, N3 ecorregiones.
- Sociales: S1 línea de tiempo, S3 construcción del Estado.
- Ramp: opciones muy contrastadas, andamiaje fuerte al primer error (C0-2).

**Bimestre 2 (may-jul) — Fracciones con base sólida y ESI.** *(aligerado: fracciones dosificadas, no las siete de una)*
- Mate: M5 división/resto, **M7 fracción de cantidad (CPA)**, **M7b equivalentes**, **M8b suma/resta de fracciones**, M9 inversa. *(M6, M10, M11 pasan a B3 para no saturar.)*
- Lengua: L5 directo↔indirecto, L8 conectores, L11 conjugá el verbo, **L7b OD/OI**.
- Naturales: **⚠ bloque ESI señalizado** — N4 pubertad, N5 ciclo menstrual, N6 del cigoto al feto.
- Sociales: S2 Revolución Industrial, S4 inmigración/censos.
- Tec: T1 instrumento, T2 secuencial/condicional.
- Ramp: 3 opciones y distractores conceptuales cercanos; andamiaje de fuerte a sutil.

**Bimestre 3 (ago-sep) — Decimales, proporcionalidad, probabilidad y géneros.** *(probabilidad adelantada acá)*
- Mate: M6 permutaciones, M10 área fraccionaria, M11 corredor de la coma, M12 multiplicar con coma, M13 tienda de descuentos, **M13b porcentaje de una cantidad**, M14 proporcionalidad, **M18 seguro/posible/imposible** (lo nuevo del año, donde SÍ hay clases), **M-prob resolvé el problema**.
- Lengua: L2 resolvé el caso, L3 bestiario CF, L9 cohesión léxica, L4 fuentes, **L0b idea principal y cuadro sinóptico**.
- Naturales: N7 estados/partículas/calor, N8 material térmico.
- Sociales: S5 el voto, S6 Gran Guerra y '29.
- Tec: T3 bloques↔código, T4 las 5 etapas.
- Transversales: Tr1 chat seguro, Tr3 los tres poderes.
- Ramp: descuentos sucesivos (contra "20+10=30"), contrarreloj en divisibilidad y decimales.

**Bimestre 4 (oct-dic) — Cierre, geometría restante y aplicación.** *(sin contenido nuevo difícil)*
- Mate: **M15b cuerpos y desarrollos**, M16 mismo área otro borde, **M17 la moda** (estadística, más liviana que probabilidad). *(geometría ya se venía trabajando desde B1.)*
- Lengua: L10 sonidos del poema, **L12a tildes**, **L12b puntuación**.
- Naturales: N9 helio/geocentrismo, N10a tiempo vs clima, N10b efecto invernadero.
- Sociales: S7 Mercosur, S8a demografía, S8b escalas. *(S9 Mi Buenos Aires ya se jugó en junio.)*
- Tec: T5 invernadero reactivo.
- Transversales: Tr2 ITS/violencia, Tr4 billetera y presupuesto, Tr5 economía circular.
- Ramp: distractores al máximo de cercanía; el modo repaso espaciado (C0-6) resucita fracciones de B2 y decimales de B3.

*(Nota de calendario: el producto no obliga el orden —Fran pide "elegí yo qué jugar" (C0-5)—; los bimestres son la ruta sugerida y la que gatea el repaso espaciado, no una fila forzada.)*

---

## 5. Lo que dijo el panel y qué se ajustó

### Auditor externo (el que reordenó el dossier)
- **Motor incumple 3 reglas estrella.** ACEPTADO como columna vertebral: **Capa 0 (C0-1/2/3)** es requisito y precede al contenido. Reverifiqué en código: `win()` con `ronda>=rondas`, `casi()` sin explicación (82 llamadas), distractores `rint` (L4807/L4993). Se reclasifica en §6 lo que el diseño metía como "horas de curación": son **cambios de motor**.
- **V/F = 50% por azar.** ACEPTADO: sufragio/S5, N5, Tr2 pasan a **3ª opción** o a modo con justificación gateada.
- **"Ordenar secuencia" memorizable (hardcoded).** ACEPTADO: C0-4 generaliza el motor antes de reusarlo en L2/N4/N6/S1/S5/T4/Tr5.
- **CPA sobrevendido.** ACEPTADO: M7 usa la barra pero es *integración nueva* (hoy `fraccion_de_cantidad` es texto+botones); M10 y M14 son mecánicas nuevas, reclasificadas de categoría B a C en §6.
- **Sobre-empaquetado (M15, M16, N10, S8, T5).** ACEPTADO parcial: se **desdoblan** M15→M15a/b, N10→N10a/b, S8→S8a/b (los que además ayudan al calendario). M16 y T5 se mantienen agrupados con banco de 25 y modos rotados, por dosificación aceptable.
- **10 rondas de tap no llenan 20-25 min / se agota en horas.** ACEPTADO: la Capa 0 de enganche (C0-5) + bancos de 25-30 + paramétricos infinitos + repaso espaciado (C0-6) son la respuesta; el valor deja de medirse en "cantidad de juegos".

### Maestra de grado
- **B4 es una fantasía; geometría y probabilidad mal ubicadas.** ACEPTADO: §4 reescrita — geometría desde B1, probabilidad a B3 (sep), B2 y B4 aliviados.
- **Tres agujeros de mate.** ACEPTADO: **M8b** (suma/resta de fracciones con su propia actividad y CPA) + **M7b equivalentes** como base; **M13b** porcentaje de una cantidad explícito; **división por dos cifras** declarada NO cubierta (con práctica guiada como inversión aparte). Ya no viven como "modo" de un memotest.
- **Comprensión lectora = 0 y técnicas de estudio cortadas.** ACEPTADO: **L0** (leé y respondé inferencial) y **L0b** (idea principal/cuadro sinóptico) dejan de ser "13ª hipotética".
- **Ortografía subdimensionada.** ACEPTADO: desdoble **L12a tildación / L12b puntuación**; sintaxis desdoblada **L7a/L7b**.
- **Señalizar ESI.** ACEPTADO: banda ⚠ y nota a la familia en N4-N6.
- **Bancos fijos se queman; control matemático a los distractores.** ACEPTADO: banco rico 12-16 → **25-30**; corregidos los dos distractores rotos de M12; control a los ~1.200.
- **N1/N2 arrancan casi sabidos; riesgo de fatiga por "clasificar".** ACEPTADO como nota de diseño: se rotan mecánicas y N1/N2 quedan de calentamiento en B1, no de contenido fuerte.

### Alumno (Fran, 6° B)
- **"Por qué vuelvo mañana solo" (racha, XP, mapa, ranking, contrarreloj, jefe, desbloqueables).** ACEPTADO como **C0-5**: era el gran ausente del plan y es de las cosas de más impacto. Contrarreloj (que ya existe en 2 juegos) se extiende a los paramétricos.
- **"Poquitas mecánicas buenas > 850 de tocar" / abandona el V/F y las listas.** ACEPTADO: menos tap-puro (3ª opción, construir en M4, programar en T2, decidir en Tr1/L2), y se prioriza terminar la Capa 0 antes que sumar actividades.
- **Lo difícil de verdad: división larga, fracciones distinto denominador, problemas leídos, OD/OI, leer textos largos.** ACEPTADO: M8b, M-prob, L0, L7b lo cubren; la división larga se declara con honestidad (no se le miente diciendo que M5 la enseña).
- **Producción escrita.** RECONOCIDO pero NO resuelto: escribir un texto propio no es evaluable con este motor sin corrección abierta. Se deja fuera del alcance y se nombra como límite (no se finge cubierto).

### Descartes (con motivo)
- **Simulaciones animadas ricas (partículas N7, zoom de densidad M8, emisiones N10b):** se dejan como *inversión aparte* con MVP táctil marcado **(◎)**, reconociendo que el fallback cubre vocabulario y no el modelo. Motivo: rozan el límite "sin assets pesados" del producto; se construyen solo si se priorizan, sin bloquear el resto.
- **6ª de Tecnología ("Capas de internet y sesgos de IA"):** postergada; entra como modo dentro de T5/T1. Motivo: contenido acotado, no justifica actividad propia en la v1.
- **Reordenar Sociales por efemérides completo:** ACEPTADO solo en parte (adelanto de S9 a junio). El recorte del DC 6° es 1862-1930 y Mayo/San Martín no entran; forzar efemérides distorsionaría el currículo. Se adelanta lo que sí ancla (Día de Buenos Aires) y se deja la nota para la ficha docente.

---

## 6. Esfuerzo de construcción

Archivos: `/root/ct3d-personalizador/actividades_web.py` (menú y `cfg` por edad) y `/root/ct3d-personalizador/actividades_player.js` (registro `GAMES.*` y bancos `*_BANCO`).

### FASE 0 — MOTOR (bloqueante; sin esto el resto es marketing)
Lo que el diseño clasificaba como "curación/horas" y en realidad es trabajo de motor:
- **C0-1 Compuerta de dominio**: reescribir `win()`/estado de ronda — puntaje por primer intento, umbral 80-90%, no cerrar por reintento, re-servir fallados. Toca las 30+ ramas `if (ronda >= rondas) ctx.win()`.
- **C0-2 Campo `porque` + render en `casi()`**: cambio de esquema del banco (un `porque` por distractor) + UI en las 82 llamadas a `casi(`.
- **C0-3 Generador de distractores por misconception**: reemplaza `item.correcta + rint(...)` (L4807, L4993, L5317, L5451, L5748…) por funciones que computan el resultado del error, por tipo.
- **C0-4 Generalizar "ordenar secuencia"** a bancos variados.
- **C0-5 Capa de enganche** (racha/XP/mapa/contrarreloj/jefe/desbloqueables) y **C0-6 repaso espaciado/gateo por bimestre**.

### A) CURACIÓN — parámetros / quitar del menú (horas, sin mecánica)
- **Sacar de e==11** los 11 juegos de nivel inicial (marcar cada base con edad mínima real en `_menu()`).
- **sudoku** a 6×6; **sopa** con vocabulario de 6°; **mover célula y sistema_nervioso** a `if e==12` (2 líneas).
- **fraccion_de_cantidad → M7**: quitar tope, conectar barra CPA (que existe en CSS pero este juego no la usa hoy).

### B) BANCO NUEVO sobre mecánica ya existente — el grueso del trabajo de contenido
Escribir a mano ~1.200 ítems verificados con distractor conceptual y su `porque`, reusando mecánicas probadas:
- **tap-selección/trivia** (base de los 8 curriculares): M1, M4, M5, M6, M11, M12, M13, M13b, M14, M18, M-prob, L0, L3, L4, L5, L8, L9, L10, L11, L12a, L12b, N8, N9, S6, T1, T3, Tr2, Tr4.
- **clasificar en canastas** (reusa `agrupar`): M3, N1, N2, N10a, N10b, S2, S8b, T2, T5.
- **matching parte→función** (reusa célula): L6, M15b, N3, N6, S3, S7, S8a, T3, Tr3.
- **ordenar secuencia** (tras C0-4): L2, N4, N6, S1, S5, T4, Tr5.
- **memotest** (reusa): M9. **grilla del 100** (existe): M2. **contrarreloj** (existe): modo avanzado de M2, M3, M12.

### C) MECÁNICA NUEVA — mínima, con MVP sobre lo existente + versión rica como inversión aparte
1. **Rotular zonas de imagen** (arrastrar etiqueta) — L1 (reusable en T1).
2. **Tap sobre palabras** (spans clickeables ≥48dp) — L7a, L7b, L10.
3. **Recta con zoom / soltar fracción** — M8 (MVP tap; zoom = inversión). **(◎)**
4. **Conectar nodos** — N1, S3, S7 (MVP matching; tirar líneas = inversión).
5. **Chat ramificado** — Tr1 (MVP ordenar+tap; árbol de decisión = inversión).
6. **Slider de partículas/emisiones** — N7, N10b, T5 (MVP tap; simulación animada = inversión). **(◎)**
7. **armar-programa con condicional (SI)** — T2, T5 (extiende el prototipo Logo).
8. **barra CPA integrada al símbolo** — M7, M7b, M8b, M13b (el widget existe en CSS; la *integración* con la mecánica de fracciones es nueva, no "ya está").
9. **Texto + preguntas inferenciales** — L0, L0b (render de párrafo + set de preguntas gateadas).
10. **Práctica guiada de división larga** (paso a paso asistido) — inversión aparte declarada.

**Balance de esfuerzo (corregido respecto del diseño original):** ~15% **Fase 0 de motor** (antes escondido como "horas"; es lo bloqueante) · ~55% **escribir bancos** sobre mecánica probada (el corazón del valor) · ~10% curación · ~20% mecánica nueva liviana con MVP, más las simulaciones **(◎)** marcadas como inversión gráfica opcional con fallback táctil que cubre vocabulario —no el modelo—. **Orden no negociable: primero Fase 0 (al menos C0-1 dominio y C0-2 porqué), después contenido a escala.**
