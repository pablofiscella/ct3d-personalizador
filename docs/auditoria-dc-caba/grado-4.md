# 4° grado (9 años)

Dossier definitivo del cuaderno de actividades interactivo para edad 9, contra el DC CABA 2024. Integra la auditoría curricular externa, la propuesta de diseño y las tres devoluciones del panel (maestra de 4.º, alumno de 9, auditor pedagógico externo). Donde el panel tenía razón, la propuesta cambió; donde no, se dice por qué (sección 5).

---

## 1. Estado actual — veredicto de auditoría

El menú de edad 9 ofrece hoy **25 juegos. Solo 5 tienen anclaje curricular razonable en 4.º**; 10 son contenido de inicial o 1.º grado servido a chicos de 9 años; 8 no trabajan ningún contenido del DC. El dato de campo ("algunas actividades son muy fáciles") está escrito en el código: 16 de 25 juegos son el paquete evergreen con dificultad tope anclada en 1.º grado, con al menos un caso de **dificultad invertida** (el de 6 años recibe series hasta 30; el de 9, hasta 16 — `actividades_web.py` L176). Hallazgo de integridad verificado: el comentario de `actividades_web.py` L274 que fijó `rondas=10` en fracciones afirma un banco de 20 ítems que no existe (son 5, `actividades_player.js` L3553-3559).

### Tabla por juego

| # | Juego | Veredicto | Nota |
|---|---|---|---|
| 1 | suma_columnas | **ALINEADO** | Único calibrado al grado: 4-5 cifras, acarreo visible, lección tras 2 fallos. Solo cubre suma. |
| 2 | acentuacion | **ALINEADO** | Tema nodal, pero hace solo el 3.º paso del proceso que pide el DC (clasificar, sin silabear ni tónica). |
| 3 | angulos | **ALINEADO** | Clasificación OK; falta la mitad de medición (transportador, el grado); 9 valores únicos para 10 rondas. |
| 4 | laboratorio_electrico | **ALINEADO** | Toca conductividad (periferia); el nodal es el circuito armable, que no está; binario con 50 % de azar. |
| 5 | fracciones_equivalentes | **ALINEADO (ampliación)** | Contenido entre `< >` en el DC; se saltó los nodales de fracciones; banco de 5 ítems para 10 rondas. |
| 6 | provincias_region | **ALINEADO (con reservas)** | Regionalización de 4 zonas ajena al DC (sin NEA/NOA), 10 de 24 jurisdicciones, trivia sin mapa. |
| 7 | prefijos_sufijos | **MUY FÁCIL** | Tema correcto; 2 piezas por palabra (50 % al primer toque), 5 ítems, sin sufijos, nunca pregunta significado. |
| 8 | programar_camino | **MUY FÁCIL** | Laberintos 3×3/4×4, ~5 instrucciones; 4.º exige iteraciones, ciclos y depuración. |
| 9 | restas | **DESALINEADO (1.º)** | Minuendo ≤ 10 contra un DC que opera en rangos de 10.000-100.000. |
| 10 | serie | **DESALINEADO (1.º, invertida)** | Tope 16 paso 1-2; e=6 recibe tope 30. Verificado en código. |
| 11 | contar | **DESALINEADO (inicial)** | Contar 1-9 sprites; sala de 5 llega a 8. |
| 12 | mas_menos | **DESALINEADO (inicial)** | Comparar grupos ≤ 9; el DC pide comparar números de 5 cifras. |
| 13 | patron | **DESALINEADO (inicial/1.º)** | Moldes ABC/ABCD; no existe ese contenido en 4.º. |
| 14 | agrupar | **DESALINEADO (inicial)** | Aparear idénticos = sala de 2-3 en mecánica. |
| 15 | bingo | **DESALINEADO (inicial)** | Discriminación visual en grilla 3×3. |
| 16 | puntos | **DESALINEADO (inicial)** | Unir puntos 1-14; la geometría de 4.º es regla, escuadra y compás. |
| 17 | sudoku | **DESALINEADO (1.º ciclo)** | 4×4 se resuelve por inspección; idéntico de 6 a 12 años. |
| 18 | abstractos_concretos | **DESALINEADO (5.º/6.º)** | El nodal de 4.º es propios/comunes; encima el banco lo trivializa. |
| 19 | fotosintesis | **DESALINEADO (otro grado)** | No figura en ningún eje de Naturales de 4.º; distractores infalibles (auto, zapatilla). |
| 20 | memotest | **SIN ANCLAJE** | Memoria visual pura; aceptable como recreativo. |
| 21 | laberinto | **SIN ANCLAJE** | Pasatiempo; sin contenido de 4.º. |
| 22 | sopa | **SIN ANCLAJE** | ≤6 palabras del tema, fallback de cumpleaños; no trabaja ninguna regularidad ortográfica. |
| 23 | simon | **SIN ANCLAJE** | Único evergreen con escalado real (8 colores); sin contenido DC. |
| 24 | quefalta | **SIN ANCLAJE** | Memoria visual de 5 ítems. |
| 25 | colorear | **SIN ANCLAJE** | Recreativo legítimo como descanso. |

**Balance: 4-6 alineados (2 con reservas serias), 2 muy fáciles en tema correcto, 10 desalineados hacia abajo, 1 hacia arriba, 8 sin anclaje.** Ningún juego resultó MUY DIFÍCIL: el desbalance es unidireccional.

### Los 5 gaps más graves

1. **Multiplicación y división** — el corazón operatorio del DC de 4.º sin un solo juego; se eliminó `sumas` por fácil y no se repuso nada multiplicativo.
2. **Fracciones nodales por reparto y medida** — 4.º es EL año en que entran las fracciones; solo hay equivalencia (ampliación) con banco de 5.
3. **Gramática y producción de Lengua** — de todo el eje Conocimiento de la lengua sobrevive solo acentuación; sin sujeto/predicado, conectores, diálogo con raya, estructura narrativa.
4. **Ciencias Sociales histórico completo** — originarios → conquista → colonia → fundaciones de Buenos Aires: cero actividades.
5. **Decimales con dinero/medida + proporcionalidad** — doble incumplimiento: nodal de Matemática y articulación explícita con Ed. Financiera.

El panel agregó dos gaps que la auditoría no había pesado y que este dossier incorpora: **fluidez de tablas** (gatekeeper de M5/M6, pedido por maestra, alumno y auditor por separado) y **comprensión lectora con inferencia** (el contenido de Lengua más evaluado jurisdiccionalmente, ausente del mapa original).

---

## 2. Mapa propuesto del año

### Números totales

**Menú edad 9: 63 juegos = 58 actividades curriculares + 5 comodines de descanso** (hoy: 25, con 5 anclados).

| Área | Actividades | Composición |
|---|---|---|
| Matemática | 19 | M1-M17 + serie endurecida (fluidez) + fracciones_equivalentes reparada (ampliación) |
| Lengua | 17 | L1-L17 |
| Cs. Naturales | 8 | N1-N8 |
| Cs. Sociales | 8 | S1-S8 |
| Tecnología/Digital | 3 | T1-T3 |
| Transversales | 3 | X1-X3 (X3 = reflexión, no evaluada) |
| Comodines | 5 | memotest, laberinto, simon, colorear, sopa (con listas curriculares) |

De las 58 curriculares: **49 nuevas** sobre mecánicas existentes o extensiones, **9 sobre juegos actuales** endurecidos/reparados (M3, M15, L1, L6, N6, S8, T1, serie, fracciones_equivalentes).

### Tiers de prioridad (corrige la aritmética 54×2=108, que no cerraba)

El presupuesto real es **~80 sesiones efectivas** (36 semanas × 3 sesiones de 15-20 min, menos paros, actos, ausencias y adherencia real — número de la maestra, confirmado por el auditor). La cuenta cierra así:

- **Tier A — 26 nodales duros, dominio gateado**: M1, M2, M4, M5, M6, M7, M8, M9, M10, M11, M12, M15, M17, serie; L1, L2, L5, L6, L8, L9, L10, L17; N6; S3; S8; T1. Presupuesto **diferenciado**: operatorias duras (M4, M5, M6, M7) 4-6 sesiones cada una — la división es LA pared de 4.º y lleva 6-8, no 2; el resto ~2. Total ≈ 60-65 sesiones. serie y M17 son modos de fluidez de 5 minutos que abren cada sesión de Matemática: no consumen sesiones propias.
- **Tier B — 31 por exposición, sin gate de dominio**: M3, M13, M14, M16, fracciones_equivalentes; L3, L4, L7, L11, L12, L13, L14, L15, L16; N1-N5, N7, N8; S1, S2, S4, S5, S6, S7; T2, T3; X1, X2. ~15-20 sesiones propias + re-exposición dentro de las sesiones mixtas.
- **Tier C — no evaluado**: X3 (reflexión ESI, sin fail state, fuera de la aritmética de dominio) + 5 comodines.

**Dominio (redefinido contra la memorización de ítems):** ≥9/10 de aciertos **en primeras exposiciones de cada ítem** (un ítem ya visto no computa para el gate). Definición operativa única para el motor. Complemento: bancos Tier A de texto fijo ≥2× las rondas hasta dominio (**24-40 ítems**) o generador/plantillas; Tier B ≥1,5× por sesión con piso 12 y meta 20+. **Commit-then-check** obligatorio en ordenar, tocar-múltiple y matching (confirmar la respuesta completa antes del feedback); el matching no acredita el último par, que sale por descarte.

**Práctica espaciada:** toda actividad dominada reaparece a ~7 y ~30 días con 5 rondas que mezclan **fallados + aleatorios del banco + 1 ítem de transferencia cercana** (no solo los fallados: 5 rondas sobre 2 ítems es memorización garantizada). Desde B2, **1 de cada 3 sesiones es mixta** (interleaving real durante el año, no solo en diciembre); las mixtas son el vehículo del repaso espaciado y de la re-exposición Tier B.

**Capa de motivación (pedido del alumno, adoptado):** racha suave; **3 estrellas por actividad que se GANAN con dominio y se CONSERVAN pasando los repasos de 7/30 días** (la retención como mecánica visible, no el checkmark); mapa de progreso con **desbloqueo por cadena de prerrequisitos** (no calendario rígido: no castiga al que avanza); **desafío del día** (5 rondas mixtas de pools dominados + generadores: contenido infinito, cero chatarra); **coleccionables del tema comprado** (ganar desbloquea recortes/figuritas del tema — los assets ya existen); récord personal con revancha; **jefe del bimestre** (síntesis mezclada con medalla). Sin ligas ni vidas (ver sección 5). Sin diplomas PDF como mecánica core.

**Panel del adulto (pedido de la maestra, adoptado):** el activo más valioso del diseño — cada distractor anota QUÉ error conceptual representa — se muestra: devolución por chico para familia y docente con el error nombrado en criollo ("confunde la escala del transportador", "truncó el cociente y dejó 10 chicos a pie"), reporte mensual, y el argumento de pantalla dosificada (3×15-20 min) explícito en la ficha. La ficha además dice en criollo el límite: **reconocer no es producir** — escribir de puño y letra, leer de corrido y exponer se trabajan en el cuaderno imprimible.

**Rampa hacia abajo (pedido del auditor, adoptado):** tramo "repaso de 3.º" accesible desde el menú de 9 sin estigma (reusa restas/serie/juegos de bandas menores con estética de 9), para el chico bajo nivel de grado — el que más motiva la compra. Ahí vive también el reloj de agujas (ver sección 5).

### Tablas por área y eje

Convención: **[A]** = Tier A (dominio gateado), **[B]** = Tier B (exposición). Banco "gen." = generador parametrizado con distractores calculados desde el error conceptual.

#### Matemática

| Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|
| **M1. Recta gigante** [A] | Tap-selección sobre zonas de recta CSS | gen. | 0-10.000 rotulada → 0-100.000 extremos → tramo fino (60-70 mil) | Ubicación en la recta; orden en rangos de 10.000/100.000 |
| **M2. Armá el número** [A] | Cajero (fichas 10.000/1.000/100/10/1) + trivia inversa | gen. | 4 cifras → 5 con ceros intermedios → modo multiplicativo | Valor posicional; composición/descomposición aditiva y multiplicativa. Distractor estrella: 34.000.507 (escritura literal de la oralidad) |
| **M3. suma_columnas** [B] | Existente, sin cambios + ronda 0 de estimación en **3 zonas** (no binaria) | gen. | 4→5 cifras | Algoritmo de suma analizado; cálculo aproximado. Consolidación breve de marzo: 1 sesión, no cuenta como "actividad del año" en la ficha |
| **M4. Resta con canje** [A] | Extensión esqueleto columnas + **fase pictórica previa: fichas de 10 que se rompen en 10 de 1** (reusa cajero M2 — el canje se VE antes del badge) | gen. | 3 cifras sin canje → 4 con canje → 5 con canje en cadena sobre ceros | Algoritmo de resta analizado, rangos 10.000/100.000. Errores detectados y nombrados: resta invertida por columna, canje olvidado, cadena sobre ceros |
| **M5. Fábrica de multiplicar** [A] | Fase mental (trivia) → fase pictórica (organizaciones rectangulares) → algoritmo en columnas con 2 filas de productos parciales | gen. | ×10/×100/×1.000 → ×1 cifra → ×2 cifras | ×10/×100/×1.000; estimación; algoritmo por dos cifras. Distractor 4.050 en ×100 queda etiquetado "hipótesis a validar por telemetría" |
| **M6. La división por partes** [A] | Trivia pitagórica inversa → paso a paso con estado (múltiplos amigables tocables, resta acumulada visible) + **estimación de cifras del cociente** | gen. + múltiplos curados | Cocientes de tabla → 2 cifras ÷ 1 → 3 ÷ 2. **Presupuesto 6-8 sesiones**, más niveles de fase 2 | Tabla pitagórica (c:a=b); algoritmo intermedio por aproximaciones con potencias de 10 |
| **M7. Problemas de verdad** [A] | Tap-selección de datos (chips) → resolver; **commit-then-check** | **Generador de plantillas**: ~12 estructuras (2 pasos, dato de sobra, análisis del resto) × números y superficie variables = cientos de enunciados | 1 paso + dato de sobra → 2 pasos → resto con interpretación | Problemas de varios pasos; datos/incógnitas; análisis del resto ("sumar 1 al cociente"); datos en tablas |
| **M8. Reparto justo** [A] | Barras CPA + trivia | 20 escritos (ítem 3 reformulado: se da la medida, se pide la tira — el original se respondía a sí mismo) | Reparto ≤1 → entero y resto → fracción en medida | Fracciones en reparto (resultado de la cuenta de dividir) y en medida |
| **M9. Litros y kilos** [A] | Cajero fraccionario (vasos/pesas 1/2 y 1/4) + trivia; en rondas que cuentan dominio, **predicción antes de tocar** (mata la fuerza bruta del desborde) | 16 (distractor "1/2" del ítem 2 reemplazado por uno etiquetable) | Completar 1 entero → 2 y 1/2 → comparar pesos | 1/2, 1/4, 3/4 con litros y kg; qué falta para el entero; componer cantidades |
| **M10. Duelo de fracciones** [A] | Clasificar 3 categorías (<1 / =1 / >1) + trivia comparativa; barras visibles → a pedido → solo símbolos, **con retiro lento** (pedido del alumno: "yo las necesito") | 16 | Con barras → barras a pedido → símbolo solo | Comparación de igual denominador; fracciones mayores/menores que el entero |
| **M11. Balanza y precios** [A] | Ordenar precios + trivia mental; **contexto rearmado: balanza ($4.523,50 el kg) y medidas (1,75 m; 2,5 kg; 2,25 L)** — sin centavos muertos; pagos con billetes solo en montos enteros | gen. + 16 escenas | Comparar 2 → ordenar 4 → sumar/restar sin algoritmo | Decimales en uso social (precios y medidas); comparación; suma/resta no algorítmica hasta 2 decimales. El error 12,5 < 12,45 sigue siendo el corazón. Ítem "¿alcanza con $10?" pasa de sí/no a 3 opciones (alcanza y sobra / no alcanza / justo, con ítems donde "justo" es correcto) |
| **M12. La mejor oferta** [A] | Completar tabla + trivia de ofertas | 20 (distractor "1.250" reemplazado por uno con error etiquetado) | Valor unitario dado → hallar la unidad → comparar ofertas (con ítems donde conviene el suelto) | Proporcionalidad directa; valor unitario; doble/triple/mitad; oferta conveniente (Ed. Financiera) |
| **M13. ¿Se arma el triángulo?** [B] | Clasificar 4 categorías; **rampa: varillas a escala → solo números** en fase final; ternas donde la percepción no decide (4,6,9 vs 4,5,9) | 20 ternas | Perceptual → numérica | Construcción de triángulos dados los lados; clasificación por lados; desigualdad triangular (ampliación) |
| **M14. Caras y cuerpos** [B] | Matching cuerpo→caras (sin par regalado) + trivia | 14 | Cuerpos simples → compuestos | Cubos y prismas: caras y figuras; circunferencia/círculo conceptual (compás va al cuaderno) |
| **M15. Medí el ángulo** [A] | Clasificación (existente, banco deduplicado) + transportador pictórico + giros | 12 grados únicos + 10 lecturas + **12 giros** (era 8, bajo el mínimo) | Clasificar → leer escala doble → giros | Clasificación agudo/recto/obtuso; el transportador; el grado; giros. Distractor estrella: 135 por 45 (escala equivocada) |
| **M16. Emparejar medidas** [B] | Trivia de equivalencias (acredita progreso) + memotest de pares **como postre** (no otorga progreso: mide posición de cartas, no conversión) | 24 pares (distractor "250" reemplazado) | m-cm → km-m → toneladas | Equivalencias km-m-cm-mm; kg-g-tonelada |
| **M17. Tablas ninja** [A] **(NUEVA por panel)** | Trivia generada, distractores de tabla vecina (54:9 por 63:9), contrarreloj suave; **modo 5 minutos para casa**; abre cada sesión de Matemática | gen. | Tablas 2-5 → 6-9 → pitagórica inversa mezclada | Repertorio multiplicativo a partir de la tabla pitagórica — el gatekeeper de M5/M6 que faltaba; pedido por los tres revisores |
| **serie (endurecida)** [A] | Existente, parámetros nuevos | gen. | `tope: 100000`, pasos `[10, 25, 50, 100, 500, 1000]`, 40 % descendentes, `rondas: 8` | Regularidades de la serie numérica. Corrige la dificultad invertida |
| **fracciones_equivalentes (reparada)** [B] | Existente; banco 5→12; va al B4, después de los nodales | 12 | Con barras → sin barras | Equivalencia de fracciones (ampliación del DC). Corregir el comentario falso de `actividades_web.py` L274 |

#### Lengua

| Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|
| **L1. Clasificador de tildes** [A] | Multi-paso: **audio de la palabra (generar_audio_consignas)** → tocar la sílaba tónica escuchada → clasificar → ¿lleva tilde? La tónica es un fenómeno oral: sin audio es patrón visual, no acentuación | 24 (incluye plurales que cambian de clase: lápiz→lápices) | Tónica con audio → clasificar → regla de tilde | Agudas/graves/esdrújulas: separar, identificar tónica, clasificar — el proceso completo que pide el DC |
| **L2. Cortá la oración** [A] | Tap-en-chips (tocar TODAS las palabras del sujeto, commit-then-check) + botón "sujeto tácito" | 20 | Sujeto inicial → con modificadores → pospuesto → tácito | Sujeto y predicado en oraciones simples; elipsis |
| **L3. Puente de conectores** [B] | Trivia de hueco | 20, **cargado a sin embargo / aunque / sino** (y/o/pero vienen sabidos — maestra) | Copulativos → temporales → adversativos | Conectores copulativos, disyuntivos, temporales, adversativos |
| **L4. ¿Qué clase de palabra?** [B] | Clasificar 3 categorías | 20 | Casos claros → gentilicios → abstractos-trampa ("alegría" es sustantivo) | Sustantivos propios/comunes; adjetivos calificativos y gentilicios |
| **L5. Máquina del tiempo verbal** [A] | Trivia de hueco en mini-narración | 20 | Puntual vs. habitual → descripción en relato | Presente, perfecto simple, imperfecto; "narra en pasado con pocas fluctuaciones" |
| **L6. Fábrica de palabras** [A] | Armar raíz+afijo + **trivia de significado** (lo que evalúa el DC) | 20 con sufijos | Armar → inferir significado | Prefijos/sufijos frecuentes (re-, -ito, -ón, -mente); inferencia de significado |
| **L7. Hiperónimo–hipónimo** [B] | Trivia + intruso; **+4 ítems de sinonimia** (la cita al DC incluía sinonimia y no había ni un ítem) | 20 | Hiperónimo directo → precisión (animal vs. ave: la explicación valida que "animal" es verdadero pero menos preciso — una verdad no se marca como error) | Cohesión léxica: hiperónimos, hipónimos, sinonimia |
| **L8. ¿Ola u hola?** [A] | Trivia de hueco; contrarreloj desde B3 | 20 pares reales rioplatenses (olla/hoya, casa/caza, tubo/tuvo); **máximo 1 grafía inventada por ítem** — "tuvó/botár/holla" eran padding | Sin reloj → contrarreloj | Homófonos heterógrafos |
| **L9. Completá con hue/bue/bur/bus** [A] | Trivia de grupo faltante | 22 | hue → sufijos -bilidad/-aje | Regularidades hue, bue-bur-bus, -cito, -aje, -bilidad |
| **L10. Luz, luces, lucecita** [A] | Trivia de transformación | 14 (banco fijo legítimo: acá memorizar el ítem ES el objetivo) | Plural → diminutivo | Plurales y diminutivos de palabras en -z |
| **L11. ¿Mito, leyenda… o los dos?** [B] | Clasificar 3 categorías; ítems "ambos" **específicos** y genéricos que NO son de ambos (mata la heurística "frase genérica → ambos") | 20 | Rasgos claros → fronterizos | Mitos y leyendas: estructura, semejanzas y diferencias |
| **L12. Detective del paratexto** [B] | Tap-selección sobre doble página CSS | 14 consignas sobre **10 páginas plantilla** (con 4 fijas se memoriza dónde está el glosario) | Elementos directos → función | Índice, glosario, títulos, epígrafes y su relación con el contenido |
| **L13. ¿Para qué se escribió?** [B] | Trivia con texto breve, 5 botones | 18 (ítem "se inauguró la plaza" reescrito: la frontera noticia/relato tenía dos respuestas defendibles) | Instructivo/informativo → argumentativo | Propósito comunicativo (informar, narrar, describir, indicar, argumentar) |
| **L14. Armá el diálogo** [B] | Ordenar intervenciones (commit-then-check) + trivia de raya y marco; **peso invertido: raya/alternancia/marco son lo gateado** (ordenar saludo-pregunta-respuesta se resuelve por pragmática) | 10 diálogos + **16 ítems de raya/marco** (eran 8, bajo el mínimo) | Ordenar → puntuar → marco narrativo | Diálogos con marco narrativo, alternancia y raya de diálogo |
| **L15. Historia en orden** [B] | Ordenar 5-6 tarjetas + clasificar en 3 etapas | 12 relatos | Ordenar → señalar conflicto → causa-consecuencia | Situación inicial – conflicto – resolución; causa-consecuencia |
| **L16. ¡Boom! Onomatopeyas** [B] | Trivia sobre viñetas CSS + ordenar viñetas | 12 | Sonido → intensidad → gag causal | Historietas: onomatopeyas y aspectos gráficos |
| **L17. Detective de textos** [A] **(NUEVA por panel)** | Trivia: texto de 100-150 palabras + pregunta **inferencial** con distractores literales ("está escrito pero no responde la pregunta") | **30 textos** escritos a mano, en espiral todo el año | Inferencia simple → causa implícita → intención de personaje | Reponer información implícita; causa-consecuencia en textos. El agujero más grande de Lengua según la maestra; lo evalúan las pruebas jurisdiccionales |

#### Ciencias Naturales

| Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|
| **N1. Modelador de paisaje** [B] | Clasificar 3 categorías + ordenar E→T→D; escenas **sin la palabra-definición** ("se acumula"→depósito era matching léxico) + casos ambiguos (pedregal al pie del cerro) | 16 | Escenas claras → ambiguas | Erosión, transporte y depósito |
| **N2. Placas en movimiento** [B] | Trivia con diagramas CSS | 14 | Choque → bordes → volcanes | Tectónica de placas; bordes activos; formación del relieve |
| **N3. Huellas del tiempo** [B] | Ordenar estratos + hitos en cinta a escala | **12 columnas** (eran 6, bajo el mínimo) + 12 hitos; variantes que rompen la regla única (columna invertida por plegamiento como ampliación, hitos intermedios) | Estratos → cinta → convivencia humanos/dinos | Fósiles; escala de tiempo geológico vs. humana |
| **N4. Armá el movimiento** [B] | Matching parte→función (sin par regalado) + trivia con esquema del brazo | 16 | Función → mecanismo (el músculo TIRA, no empuja) | SOAM: huesos, músculos, articulaciones; esqueleto interno como ventaja |
| **N5. Laboratorio de imanes** [B] | Trivia de **predicción** (predecir → ver → explicar) | 16 | Polos → imán partido → electrostática con distancia | Dos polos siempre; atracción/repulsión; electrostática decae con distancia |
| **N6. Armá el circuito** [A] | Multi-paso: diagnóstico del circuito (3-4 opciones) → conductividad CON porqué; muere el binario al 50 % | 18 | Circuito abierto → componentes → material vs. percepción | Circuito eléctrico simple: generador, conductor, disipador, interruptor; conductividad. "La corriente tiene que poder VOLVER" |
| **N7. Objeto o material** [B] | Clasificar 3 categorías + trivia de usos | 18 | Claros → transformados (el vidrio: la explicación desarrolla la transformación por las personas) | Natural vs. artificial; objeto ≠ material; propiedades y usos |
| **N8. El cielo de Buenos Aires** [B] | Trivia con diagrama de cielo CSS | 16 | Posición del Sol → día/noche SIN la Luna → sombras y estaciones | Movimiento diario del Sol; mediodía solar; día/noche; solsticios y estaciones |

#### Ciencias Sociales

| Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|
| **S1. Los primeros pueblos** [B] | Clasificar 3 categorías (nómades / sedentarios / ambos); ítems "ambos" específicos, no genéricos | 18 | Modos de vida → relación con la naturaleza | Caza-recolección y domesticación; nómades y sedentarios; pueblos del espacio de Buenos Aires |
| **S2. América antes de 1492** [B] | Matching pueblo→tecnología (sin par regalado) + trivia | 18 | Rasgos → origen americano de cultivos | Incas y aztecas; tributos y tecnologías; maíz, papa, tomate, cacao |
| **S3. Línea de tiempo colonial** [A] | Ordenar hitos (commit-then-check) + trivia de porqués; distractores factuales etiquetados como **"plausible-pero-falso"** (categoría propia, no "error conceptual") | 12 hitos + 14 preguntas | Ordenar → explicar (¿por qué DOS fundaciones?) | Conquista; fundaciones de Buenos Aires (1536/1580); Virreinato del Perú → del Río de la Plata (1776) |
| **S4. La sociedad colonial** [B] | Ordenar pirámide + matching sector→derechos/obligaciones; **corrección histórica**: indígenas (tributo y trabajo obligatorio bajo encomienda/mita) y africanos esclavizados son **estratos separados** con estatus legal distinto — el ítem "¿quiénes sin libertad?" con respuesta única era impugnable | 14 | Pirámide → derechos por sector | Sociedad colonial: derechos y obligaciones de los sectores (+ castas como ampliación). Revisión docente externa obligatoria |
| **S5. Ambientes argentinos** [B] | Clasificar 3 categorías; escenas sin palabra-definición | 16 | Claros → fronterizos (alto vs. escalonado-plano) | Ambientes: montaña, llanura, meseta |
| **S6. ¿Urbano, rural o periurbano?** [B] | Clasificar 3 categorías | 18 | Claros → periurbano (el borde que alimenta la ciudad) | Espacios urbanos/rurales/periurbanos; articulación y servicios |
| **S7. ¿Quién se ocupa?** [B] | Clasificar 3 categorías (Nación / Ciudad / Comuna) | 16 | Servicios claros → "¿CABA es una provincia?" | Niveles de gobierno; CABA autónoma y comunas; servicios e impuestos |
| **S8. Provincias, regiones y capitales** [A] | Trivia; banco **24 jurisdicciones** + regiones NOA/NEA/Cuyo/Centro-Pampeana/Patagonia + **capitales** (pedido del alumno: "la seño toma capitales y me falta la mitad de la prueba"); **fuente citable fijada y mostrada** en la explicación, con "en algunos libros vas a ver…" (La Pampa, La Rioja varían según fuente) | 24 + 24 capitales, `rondas: 12` | Región → capital → límites | División jurídico-político-administrativa; extensión y límites. Mapa encastrable = inversión aparte (ola 2) |

#### Tecnología, Diseño y Programación

| Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|
| **T1. Robot por bloques 2.0** [A] | Laberintos `[6, 6, 8]`, bloque **"repetir N veces"**, **presupuesto de bloques** ("resolvelo con 6 o menos" — la estrella de Angry Birds: ganar es fácil, ganar BIEN es el desafío), **modo depuración** (un bloque erróneo: encontrarlo, reemplazarlo, re-ejecutar), leer-y-anticipar | 14 niveles a mano | Sin ciclos → ciclos forzados por presupuesto → depurar → anticipar | Iteraciones y ciclos; creación y depuración iterativa; bloques. Error egocéntrico izquierda/derecha DEL robot |
| **T2. Mecanismos y energía** [B] | Matching mecanismo→transformación + ordenar diagrama de energía + **trivia aparte** para "el motor CREA la energía" (un diagrama ordenable no puede expresar esa creencia — especificación corregida) | 14 | Nombrar → ordenar → etiquetar roles | Bielas, manivelas, levas; circular↔alternativo; conversiones de energía; motor/transmisión/efector |
| **T3. Detectives digitales** [B] | Clasificar **3 categorías reales**: usa IA / no usa IA / **no se puede saber sin más info** (el binario violaba la regla anti-eliminación; la tercera es la lección epistémica correcta) + trivia con indicio tocable | 18 | Reconocer IA → evaluar fuentes → foto increíble del grupo | IA en aplicaciones cotidianas; confiabilidad y procedencia de fuentes, incluso generadas por IA |

#### Transversales

| Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|
| **X1. Separá en origen** [B] | Clasificar 4 categorías | 18 | Claros → finos (botella sucia de aceite) | Ed. Ambiental: corrientes de residuos; separación en origen; compostaje; las R |
| **X2. ¿Necesidad o deseo?** [B] | Clasificar 3 categorías (la tercera — deseo legítimo planificado — evita el moralismo binario) + trivia de meta de ahorro | 16 | Claros → el ocio como derecho | Ed. Financiera: necesidades/deseos; ahorro = ingreso − gasto (decimales viven en M11, proporcionalidad en M12) |
| **X3. Semáforo de la convivencia** [C — reflexión, no evaluada] | Trivia de escenas con consecuencias mostradas, **sin fail state** (decisión pedagógica correcta para ESI; por eso queda fuera del gate de dominio y se declara "actividad de reflexión" — el sesgo de deseabilidad social hace que la elección no mida conducta) | 12 escenas | — | ESI: diálogo ante burlas y exclusiones; a quiénes acudir; huella digital (articula con T3) |

---

## 3. Cambios al catálogo actual (los 25 del menú de hoy)

| Juego actual | Decisión | Detalle / parámetros exactos |
|---|---|---|
| suma_columnas | **MANTENER** (→ M3) | Ya alineado. + ronda 0 de estimación en 3 zonas. Se declara consolidación breve, 1 sesión. |
| acentuacion | **ENDURECER** (→ L1) | Proceso completo multi-paso CON AUDIO: escuchar → tónica → clasificar → tilde. Banco 10→24. |
| angulos | **ENDURECER** (→ M15) | Deduplicar el 90; + transportador pictórico (distractor 180−x) + giros; bancos 12+10+12; `rondas: 12`. |
| laboratorio_electrico | **ENDURECER** (→ N6) | Fase diagnóstico de circuito (3-4 opciones) + conductividad con porqué. Muere el binario. Banco 10→18. |
| prefijos_sufijos | **ENDURECER** (→ L6) | Entra el significado; sufijos incluidos; banco 5→20. |
| provincias_region | **ENDURECER** (→ S8) | Banco 10→24 jurisdicciones + capitales; regiones NOA/NEA/Cuyo/Centro-Pampeana/Patagonia; fuente citada; `rondas: 12`. |
| fracciones_equivalentes | **ENDURECER/REPARAR** | Banco 5→12 reales; reubicada al B4 (es ampliación: va DESPUÉS de los nodales M8-M10); **corregir el comentario falso de `actividades_web.py` L274**. |
| programar_camino | **ENDURECER** (→ T1) | Laberintos `[6, 6, 8]`, bloque repetir, presupuesto de bloques, modo depuración. |
| serie | **ENDURECER** | `tope: 100000`, pasos `[10, 25, 50, 100, 500, 1000]`, 40 % descendentes, `rondas: 8`. Corrige la dificultad invertida (hoy tope 16 en e=9 vs 30 en e=6). Cambio de parámetros, barato. |
| sopa | **ENDURECER (comodín con valor)** | `dim: 12`; listas curriculares de 8+ palabras (hue/bue/bur/bus, gentilicios, vocabulario de Naturales del bimestre) en vez del fallback de cumpleaños. |
| sudoku | **RETIRAR de edad 9** | 4×4 se resuelve por inspección. Solo vuelve con generador 6×6 de solución única (opcional, ola 2). |
| restas | **RETIRAR de edad 9** | Minuendo ≤10 = 1.º grado. Lo reemplaza M4. Vive en bandas menores y en el tramo puente "repaso de 3.º". |
| contar | **RETIRAR de edad 9** | Sala de 5. Queda en bandas mini/media. |
| mas_menos | **RETIRAR de edad 9** | Comparación de colecciones = inicial; la de 4.º (5 cifras) vive en M1/M2. |
| patron | **RETIRAR de edad 9** | Moldes ABC/ABCD = inicial; sin contenido en el DC de 4.º. |
| agrupar | **RETIRAR de edad 9** | Aparear idénticos = sala de 3. La clasificación CON criterio vive en N7, S1, S5, S6, X1. |
| bingo | **RETIRAR de edad 9** | Discriminación visual de inicial. |
| puntos | **RETIRAR de edad 9** | Contar hasta 14 = inicial; la geometría de 4.º es M13/M14. |
| quefalta | **RETIRAR de edad 9** | Memoria visual sin currículo; bandas menores. |
| abstractos_concretos | **MOVER a 6.º** | Abstracto/concreto no es de 4.º (el nodal es propios/comunes → L4). Al moverlo, endurecer el banco. |
| fotosintesis | **MOVER a 5.º** | No está en ningún eje de Naturales de 4.º. Al moverlo, rehacer distractores: "oscuridad" y "abono" sí; "música" no (chatarra simpática, no error real — auditor). |
| memotest | **MANTENER (comodín)** | `pares: 8`. No cuenta como actividad curricular en la ficha. |
| laberinto | **MANTENER (comodín)** | Tamaños 9-12. |
| simon | **MANTENER (comodín)** | 8 colores; único evergreen con escalado real. |
| colorear | **MANTENER (comodín)** | Descanso explícitamente no curricular. |

**Cuenta verificada (corrige la inconsistencia que señaló el auditor: "8 retirados" que eran 9 y un desglose que sumaba 23):** 25 actuales = **5 mantenidos** (suma_columnas + 4 comodines) + **9 endurecidos/reparados** (acentuacion, angulos, laboratorio_electrico, prefijos_sufijos, provincias_region, fracciones_equivalentes, programar_camino, serie, sopa) + **9 retirados de la edad** (sudoku, restas, contar, mas_menos, patron, agrupar, bingo, puntos, quefalta) + **2 movidos de grado** (abstractos_concretos, fotosintesis). 5+9+9+2 = 25. Nada se borra del motor: los retirados siguen sirviendo a bandas menores y al tramo puente.

---

## 4. Progresión del año (4 bimestres)

Re-secuenciada contra el **calendario escolar real** (pedido central de la maestra, adoptado completo): el B4 se descarga (lo que queda para noviembre no se da), la sociedad colonial llega ANTES del acto del 25 de Mayo, paratexto y propósito van a marzo (es cuando se explora el manual), la unidad Tierra (erosión→placas→fósiles) va pegada, ambientes junto a provincias, y el repaso espaciado de originarios/conquista se calza a la semana del 12 de octubre. Fracciones: M8 al cierre del B2, el grueso en B3 (en muchas aulas de CABA entran en agosto — no se vende "como en el aula" sin esa nota).

Reglas transversales de progresión: andamiaje que se retira dentro de cada actividad (pista fuerte → sutil → nada) y entre bimestres (CPA: concreto/pictórico → a pedido → símbolo, con **retiro lento en fracciones**); contrarreloj recién en B3; **desde B2, 1 de cada 3 sesiones es mixta** (interleaving durante el año + vehículo del repaso espaciado); **serie y M17 abren cada sesión de Matemática con 5 minutos de fluidez**; desafío del día disponible siempre; **jefe del bimestre** al cierre de cada uno.

**Bimestre 1 (marzo-mayo) — Base numérica, oración y exploración de textos.**
Matemática: M1 Recta, M2 Armá el número, M3 suma_columnas (consolidación breve), M17 Tablas ninja (arranca), M4 Resta con canje (fase pictórica), serie como fluidez. Lengua: **L12 Paratexto y L13 Propósito (movidas a marzo)**, L1 Tildes con audio, L2 Cortá la oración, L4 Clase de palabra. Sociales: S1 Primeros pueblos, S2 América antes de 1492. Naturales: N1 Paisaje. Tecnología: T1 niveles sin ciclo. **X3 Convivencia en marzo** (cuando se arman los grupos — validado por la maestra, no se toca).

**Bimestre 2 (mayo-julio) — Multiplicar, dividir, colonia antes del 25 de Mayo.**
Matemática: M5 Fábrica de multiplicar (mental → algoritmo), M6 División por partes (arranca; sigue en B3: 6-8 sesiones), M8 Reparto justo (al CIERRE del bimestre, después de división), M13 Triángulos (geometría repartida, descarga el B4). Lengua: L3 Conectores (adversativos cargados), L5 Tiempo verbal, L6 Fábrica de palabras, L11 Mito o leyenda, L15 Historia en orden, L17 Detective de textos (arranca, sigue todo el año). Sociales: **S3 Línea colonial + S4 Sociedad colonial, completas antes del acto del 25 de Mayo**. Naturales: **N2 Placas + N3 Huellas del tiempo (pegadas a N1: la unidad Tierra no se parte)**, N4 SOAM. Tecnología: T1 con ciclos y presupuesto de bloques, T2 Mecanismos.

**Bimestre 3 (agosto-octubre) — Fracciones a fondo, problemas de verdad, decimales.**
Matemática: M6 consolidación, M7 Problemas de verdad (integra todo lo operatorio; generador de plantillas), M9 Litros y kilos, M10 Duelo de fracciones, M11 Balanza y precios, M14 Caras y cuerpos, M15 Ángulos completo. Lengua: L8 Ola u hola (con contrarreloj), L9 hue/bue, L10 Luz-luces, L14 Armá el diálogo, L17 sigue. Sociales: **S5 Ambientes + S8 Provincias y capitales (juntas)**. Naturales: N5 Imanes, N6 Circuito. X1 Residuos. Se activa el repaso espaciado de B1 dentro de las mixtas.

**Bimestre 4 (octubre-diciembre) — Proporcionalidad, cierre y síntesis (descargado: ~12 actividades, no 18).**
Matemática: M12 Mejor oferta, M16 Medidas, fracciones_equivalentes (ampliación: ahora sí, con los nodales puestos). Lengua: L7 Hiperónimos, L16 Onomatopeyas. Sociales: S6 Urbano/rural, S7 Quién se ocupa; **repaso espaciado de S1-S2 calzado a la semana del 12 de octubre** (alineación con el aula a costo cero). Naturales: N7 Materiales, **N8 Cielo (con el solsticio a la vuelta de la esquina — validado, no se toca)**. Tecnología: T3 Detectives digitales. X2 Necesidad o deseo. Diciembre: **modo repaso mezclado del año** (interleaving puro sobre ítems ya vistos) + jefe final del año con medalla.

Cómo sube la dificultad en concreto: rangos 3→5 cifras (M4), pictórico→algoritmo (M4/M5), mental→algoritmo (M5), barras visibles→a pedido→símbolo (M8-M10→fracciones_equivalentes cierra el ciclo), varillas a escala→solo números (M13), sin tiempo→contrarreloj (L8, M17), clasificar→justificar el porqué (N6, T3), ordenar→depurar→anticipar (T1).

---

## 5. Lo que dijo el panel y qué se ajustó

### Adoptado de la maestra

1. **Re-secuenciación completa contra el calendario real** — B4 descargado (geometría a B2/B3), colonial antes del 25 de Mayo, paratexto/propósito a marzo, unidad Tierra pegada, ambientes junto a provincias, repaso de originarios al 12 de octubre. Es la sección 4 entera.
2. **División redimensionada**: 6-8 sesiones, más niveles de fase 2, estimación de cifras del cociente. El supuesto "todo se domina en 2 sesiones" se reemplazó por presupuestos diferenciados.
3. **Comprensión lectora con inferencia**: actividad nueva L17, Tier A, 30 textos. Tenía razón: era el agujero más grande de Lengua y es solo banco, no motor.
4. **M7 a generador de plantillas** (~12 estructuras × superficie variable) — supera su pedido de "40+ enunciados": mejor que 40 fijos que también se memorizan.
5. **Decimales sin centavos muertos**: M11 rearmada sobre balanza y medidas (1,75 m; 2,5 kg; $4.523,50 el kg).
6. **Panel del adulto**: devolución con el error conceptual nombrado en criollo, reporte mensual, argumento de pantalla dosificada en la ficha, y el límite "reconocer no es producir" dicho a las familias.
7. **Presupuesto realista de 80 sesiones** y su corolario: **la Ola 1 ES el año** (sección 6). Bancos de texto fijo evaluado a 24-40 ítems.
8. Menores: M3 declarada consolidación breve; conectores cargados a sin embargo/aunque/sino; nota "en muchas aulas las fracciones entran en agosto".

### Adoptado del alumno

1. **Capa de motivación completa**: racha, 3 estrellas (fusionadas con la insignia-de-retención del auditor: se conservan pasando los repasos), mapa de progreso con desbloqueos, coleccionables del tema comprado, récord con revancha, desafío del día, jefe del bimestre. Sin diplomas PDF como mecánica.
2. **Tablas contrarreloj** (M17): su "agujero más grande" coincidió con maestra y auditor. Con modo 5 minutos para casa.
3. **Capitales en S8**: "la seño toma capitales" — banco de 24 capitales agregado.
4. **Barras de fracciones con retiro lento** (M10): "yo las necesito" — el andamiaje se va más despacio y queda "a pedido" un bimestre más.
5. **Muchas rondas de división**: coincide con la maestra; 6-8 sesiones.
6. Su lectura de qué engancha (presupuesto de bloques = estrellas de Angry Birds, depuración = "me siento hacker", predicción en imanes, consecuencias en X3) validó esos diseños tal cual estaban: no se tocan.

### Adoptado del auditor externo

1. **Dominio redefinido contra memorización** (la falla estructural n.º 1): computa solo primeras exposiciones, 9/10 en ventana de 10; bancos Tier A ≥2×; **commit-then-check** en ordenar/tocar-múltiple; matching sin par regalado. Transversal a todo el motor.
2. **Tiers en lugar de 54×2=108**: 26 Tier A gateadas + 31 Tier B por exposición + Tier C; comodines, repaso, fluidez y adherencia presupuestados. X3 fuera de la aritmética de dominio, declarada "reflexión, no evaluada".
3. **CPA real en operaciones**: fase pictórica en M4 (fichas que se rompen, reusando el cajero de M2) y M5 (organizaciones rectangulares) antes del algoritmo.
4. **Audio en L1** (la enmienda de mayor retorno por peso: la tónica es oral) y generador de plantillas en M7.
5. **Blindaje de contenido impugnable**: S4 con estratos históricamente correctos (encomienda/mita ≠ esclavitud), S8 con fuente citada y nota de variantes, L7 con ítems de sinonimia, L13 ítem reescrito, categoría "plausible-pero-falso" para distractores factuales (S3), revisión docente externa de todos los bancos de Sociales/Naturales, verificación de cada cita al DC contra el documento real antes de la ficha.
6. **Anti-gaming puntual**: M13 fase solo-números y ternas no perceptuales; M16 memotest como postre; N1/S5/S6 sin palabra-definición; L11/S1 ítems "ambos" no genéricos; L14 con el peso en raya/alternancia; T3 con tercera categoría; M3 estimación a 3 zonas; M11 sin binarios; M9 con predicción; N3 con 12 columnas y variantes.
7. **Bancos bajo mínimo corregidos**: L14 raya 8→16, N3 6→12, M15 giros 8→12, L12 4→10 páginas.
8. **Interleaving desde B2** (1 de cada 3 sesiones mixta) y repaso espaciado mezclado (fallados + aleatorios + transferencia).
9. **Rampa hacia abajo**: tramo "repaso de 3.º" sin estigma para el chico bajo nivel — el riesgo espejo de "muy fácil" es "muy difícil" y ese padre churnea más rápido.
10. **Integridad interna**: cuentas de la sección 3 corregidas y verificadas (5+9+9+2=25); serie y fracciones_equivalentes ahora DENTRO de los números del año; el costo real de ~600+ ítems repriced como semanas de trabajo experto con QA docente y **telemetría por ítem desde el día uno**.

### Descartado o diferido (y por qué)

- **Ligas y vidas estilo Duolingo (alumno)**: descartado. Las vidas convierten el error en castigo y contradicen la política del producto (el error es el material de enseñanza: cada distractor existe para explicar); las ligas requieren comparación social entre chicos de 9, indeseable pedagógicamente y cara en infra. Racha + estrellas + coleccionables + récord propio cubren el mismo loop sin esos costos.
- **Reloj de agujas (alumno)**: no entra en los 58 — no es contenido nodal del DC de 4.º (el DC lo ubica antes). Como la necesidad es real, vive en el tramo puente "repaso de 3.º", accesible desde el menú de 9.
- **Escribir con teclado la palabra (alumno; "reconocer no es producir", maestra)**: el reclamo es válido y queda registrado, pero es mecánica nueva de input de texto con corrección — va a Ola 2 (modo dictado reusando generar_audio_consignas). Mientras tanto, el límite se declara en la ficha en criollo.
- **Sudoku 6×6 "de verdad" (alumno)**: sigue opcional en ola 2 — es comodín sin anclaje curricular y el generador de solución única es esfuerzo real; no compite contra los gaps nodales.
- **"Que M3 no cuente" (maestra)**: adoptado a medias — cuenta en el menú (consolidación tiene valor en marzo) pero se declara breve y no infla la ficha.
- **"Verificar el 4.050 de M5 con datos de aula" (auditor)**: no se reemplaza todavía — queda etiquetado "hipótesis a validar" y la telemetría por ítem (que este dossier ya presupuesta) lo confirma o lo mata con datos reales, que es exactamente el mecanismo que el auditor pidió instalar.

---

## 6. Esfuerzo de construcción

### A. Curación pura (parámetros y datos; horas, no días)

serie (tope/pasos/rondas — corrige la dificultad invertida), sopa (listas curriculares), retiros del menú e==9 (9 juegos), movidas de abstractos_concretos y fotosintesis (con rehecho de distractores), reubicación de fracciones_equivalentes al B4 y banco 5→12, deduplicación del banco de angulos, banco de capitales para S8, y el **fix de integridad: corregir el comentario falso de `actividades_web.py` L274** — las calibraciones no pueden decidirse sobre comentarios que mienten.

### B. Bancos nuevos sobre mecánica existente (el grueso — y repriced con honestidad)

~40 actividades que son "solo contenido" suman **~600+ ítems escritos a mano, verificados, con cada distractor etiquetado** (error conceptual real, o "plausible-pero-falso" en lo factual): son **semanas de trabajo experto, no un residuo**. Se presupuestan además: **QA curricular externa** (una docente de 4.º revisa todos los bancos, con veto en Sociales/Naturales) y **telemetría por ítem desde el día uno** (índice de dificultad + análisis de distractores — la etiqueta por distractor la hace posible y es la ventaja competitiva del producto).

Reparto por mecánica: trivia con distractores (M6-f1, M7, M11, M12, M16, M17, L3, L5, L7, L8, L9, L10, L13, L16, L17, N2, N3, N4, N5, N7, N8, S2, S3, S7, S8, T3, X2, X3); clasificar 3-4 categorías (L4, L11, M10, M13, N1, N7, S1, S5, S6, T3, X1, X2); matching (M14, N4, S2, S4, T2); ordenar secuencia (L14, L15, N1, N3, S3, S4, T2); cajero (M2, M9, M11); barras CPA (M8, M9, M10); memotest (M16 postre); contrarreloj (L8, M17). Regla de fábrica: banco ≥2× para Tier A (24-40) o generador; ≥12-20 para Tier B; regla anti-eliminación (≥3 opciones/categorías) sin excepciones.

### C. Mecánica nueva mínima (en orden de retorno)

0. **Reglas de motor transversales** (primero: sin esto el producto mide lo que critica): dominio por primeras exposiciones (9/10), commit-then-check, matching sin par regalado, telemetría por ítem.
1. **Reuso del esqueleto de columnas** para M4 y M5 **con fase pictórica** (fichas que se rompen — reusa el cajero de M2; badge "−1" y dos filas de productos parciales). La palanca más grande: cubre los dos gaps operatorios más graves.
2. **Trivia multi-paso** (wrapper de estado): habilita L1 (audio→tónica→clase→tilde), M7 (datos→resolver), N6 (diagnóstico→porqué). Un wrapper, tres actividades.
3. **Tap-en-chips** (targets generados del ítem, ≥48dp): L1, L2, M1, L12. Casi gratis.
4. **M17 Tablas ninja**: trivia generada + contrarreloj existente — casi gratis y desbloquea M5/M6.
5. **División por partes** (M6 fase 2): múltiplos tocables con resta acumulada visible + estimación de cifras.
6. **Generador de plantillas para M7** (estructuras fijas, superficie variable).
7. **Bloques "repetir" + presupuesto + depuración** en T1.
8. **Capa de motivación v1**: racha, estrellas con retención, mapa de prerrequisitos, desafío del día (rondas mixtas: pools dominados + generadores), coleccionables (reusa recortes del tema), jefe del bimestre (modo síntesis).
9. **Panel del adulto v1**: reporte con errores nombrados — el activo más monetizable; justifica renovación mejor que cualquier contador de juegos.
10. **Opcionales solo si sobra capacidad (ola 2)**: modo escritura con teclado/dictado, sudoku 6×6 con solución única, mapa encastrable de provincias, animaciones CSS de mecanismos (en v1 son diagramas estáticos).

### Regla de corte

**La Ola 1 ES el año** (conclusión de la maestra, confirmada por la aritmética del auditor). Ola 1 = Tier A completo (26) + Tier B de B1-B3 + C0-C8 + panel adulto v1 ≈ 45 actividades publicadas. Ola 2 = Tier B de B4 restante + opcionales = diciembre, verano y puente a 5.º. Con la Ola 1 publicada, el menú de 4.º pasa de 5/25 juegos con anclaje curricular a ~45 anclados sobre 50 visibles — y la queja de campo ("algunas actividades son muy fáciles") deja de tener base en el código, sin haberla convertido en su espejo ("muy difícil"): para eso están la rampa de 3.º y el andamiaje que se retira despacio.
