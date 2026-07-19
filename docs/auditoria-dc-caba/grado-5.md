# 5° grado (10 años)

Dossier definitivo del cuaderno de actividades interactivo para 5° grado, integrando: auditoría curricular externa (vs. DC CABA 2024), propuesta de diseño, y panel revisor (maestra de grado, alumno de 5°, auditor pedagógico externo). Todas las observaciones válidas del panel están incorporadas; los descartes se justifican en §5.

---

## 1. Estado actual — veredicto de auditoría

De los 25 juegos que hoy ve un alumno de 5°: **2 alineados, 4 muy fáciles, 11 desalineados (contenido de otro grado), 8 sin anclaje curricular**. Tasa de alineación real: **8%**. El techo aritmético del producto para un chico de 10 años es la suma 5+5=10 y la serie hasta 16, contra un DC que pide operar en el rango del millón. No existe ningún juego "muy difícil": todo el riesgo tira hacia abajo. El parche `suma_columnas` se aplicó solo a 4° (comentario explícito en `actividades_web.py` L290), con lo cual 5° quedó **peor** calibrado que 4°.

| # | Juego | Veredicto | Motivo (vs. DC 5°) |
|---|-------|-----------|--------------------|
| 1 | memotest (8 pares) | SIN ANCLAJE | Memoria visual genérica; idéntico de 6 a 12 años. |
| 2 | laberinto (9-12) | SIN ANCLAJE | Destreza espacial; mismo data.json para toda la banda. |
| 3 | programar_camino | DESALINEADO (1er ciclo) | Secuencias lineales sin repetición; el DC 5° pide variables, bucles, condicionales, sensores. |
| 4 | sopa (10×10) | SIN ANCLAJE | Palabras del tema decorativo, no de la ortografía nodal. |
| 5 | sudoku (4×4, 8 pistas) | SIN ANCLAJE | No figura en el DC; calibrado para 6 años. |
| 6 | sumas (max 10) | DESALINEADO (1°) | La cuenta más difícil es a+b=10; el DC pide rango del millón y problemas de varios pasos. |
| 7 | restas (max 10) | DESALINEADO (1°) | Restas dentro de 10 son repertorio de 1°. |
| 8 | serie (tope 16) | DESALINEADO (1°) | Inversión real: el de 6 años recibe tope 30 (L176) y el de 10, tope 16. |
| 9 | patron (ABC/AABB) | DESALINEADO (Inicial) | Patrones perceptuales de repetición. |
| 10 | puntos (10-14) | DESALINEADO (Inicial/1°) | Contar hasta 14 en orden. |
| 11 | contar (max 9) | DESALINEADO (Inicial) | Conteo perceptual, sala de 5. |
| 12 | colorear | SIN ANCLAJE | Recreativo puro, sin consigna ni corrección. |
| 13 | mas_menos (max 9) | DESALINEADO (Inicial) | Comparar colecciones de hasta 9; el DC 5° compara fracciones y decimales. |
| 14 | simon (8 botones) | SIN ANCLAJE | Único base que escala por año, pero sin contenido de grado. |
| 15 | agrupar (matching idéntico) | DESALINEADO (sala de 3) | Emparejar sprite con canasta del MISMO sprite; ni clasifica por criterio. |
| 16 | quefalta (5 ítems) | SIN ANCLAJE | Memoria visual de 5 elementos. |
| 17 | bingo (3×3) | SIN ANCLAJE | Búsqueda visual entre 9 sprites. |
| 18 | trivia_colonial (V/F) | DESALINEADO (4°) | Sociedad colonial = cierre de 4°; el foco de 5° (1810→1853) no aparece. V/F con reintento = 50% por azar. |
| 19 | camino_digestivo | MUY FÁCIL | Cubre 1 de los 4 sistemas de la nutrición integrada; misma secuencia ×4 rondas = memoria desde la ronda 2. |
| 20 | fracciones_avanzado | ALINEADO | Calza con equivalencias nodales, pero banco de 5 ítems para 10 rondas (el comentario "20 ítems" de L306 es falso) y sin doceavos. |
| 21 | analisis_sintactico | ALINEADO | Núcleos de S/P con timer; dificultad razonable, único juego con presión de tiempo. |
| 22 | pago_exacto | MUY FÁCIL | Anclaje decimal legítimo, tarea aritmética de 1°; denominaciones en centavos que ningún chico de 2026 vio. |
| 23 | actividad_economica | SIN ANCLAJE | Producciones actuales por región no son ni el recorte del siglo XIX ni la clasificación de recursos del DC. |
| 24 | planta_potabilizadora | MUY FÁCIL | Ancla solo en ampliación; secuencia fija repetida 4 veces. |
| 25 | derechos_constitucion (V/F) | MUY FÁCIL | Tema legítimo (Constitución 1853), pero ítems de sentido común y V/F ganable por descarte. |

### Los 5 gaps más graves

1. **Cero lectura en un producto "curricular" de Lengua**: no existe un solo texto de más de una oración; el DC pide leer con fluidez textos de 300+ palabras con inferencias.
2. **Cero multiplicación y división en 5°**: el año de divisibilidad, combinatoria, algoritmos intermedios y c×d+r=D no tiene ni una tabla del 2.
3. **Ausencia total del proceso 1810-1853 en Sociales**: al alumno de 5° se le ofrece el contenido de 4° y nada del suyo.
4. **Numeración: techo en 16 vs. rango del millón**: cinco órdenes de magnitud por debajo del DC.
5. **Perímetro/área y estudio de datos —los dos ejes que ESTRENAN en 5°— sin ninguna actividad**: el producto ignora justo lo nuevo del año.

Hallazgo estructural: la banda 6-12 es una sola y de sus 17 juegos base solo `simon` escala por año; un alumno de 5° comparte sin modificación el 68% de su menú con uno de 1°.

---

## 2. Mapa propuesto del año

### Números totales

| Concepto | Cantidad |
|---|---|
| Actividades curriculares | **56** = 39 núcleo + 17 extensión |
| — Matemática | 18 (17 núcleo + 1 ext.) |
| — Lengua | 16 (8 núcleo + 8 ext.) |
| — Cs. Naturales | 8 (5 núcleo + 3 ext.) |
| — Cs. Sociales | 9 (6 núcleo + 3 ext.) |
| — Tecnología + Transversales | 5 (3 núcleo + 2 ext.) |
| Evergreen de recreo cognitivo (no cuentan como curriculares) | 6: memotest, colorear, simon + sopa/laberinto/sudoku endurecidos |
| Ítems fijos escritos y verificados a mano | **~890** (Lengua ~465 incl. 30 textos ×5 preguntas, Naturales ~150, Sociales ~150, resto fijo de Mate/Tec ~120) |
| Plantillas paramétricas (matemática + T1; valores regenerados con restricciones) | **~300** → banco efectivo >3.000 ítems |
| Generadores puros | M18 (tablas/cálculo) y T2 (niveles con semilla) |
| Textos de lectura (L1) | 30 al lanzamiento + 2 nuevos por mes (drop mensual) |

**Dosificación honesta (ajuste del auditor):** ~100-110 sesiones/año × 1,5 actividades − recreo cognitivo presupuestado ≈ 140-155 slots. Dimensionado a **4 encuentros promedio** (no al mínimo teórico de 3): el año típico cierra el **núcleo (39 actividades, ~70% del mapa)** y así se comunica; la extensión es para ritmo alto. El cuartil inferior no rompe la aritmética porque la práctica extra en matemática consume plantillas paramétricas, no banco fijo.

**Sesión y rondas (ajuste del alumno):** bloques de **6 rondas** con botón "una más" para encadenar; sesión objetivo 20-25 min ≈ 2 bloques + recreo. L1 define su propia unidad: 1 texto + 5 preguntas ≈ 10 min (la regla "10 rondas" no aplica a lectura; la sesión se define por mecánica).

**Dominio (redefinido según auditor — reemplaza la ventana móvil):**
- Se evalúa sobre los **últimos 10 ítems al cierre de sesión (ventana fija, no móvil)**.
- **Estratificado**: la ventana debe incluir ítems dif 2-3; no se certifica dominio jugando solo dif 1.
- Cuenta **solo sin andamiaje** (barras CPA retiradas; quedan como pista de primer error).
- Tras un error, el progreso se acredita con un **ítem isomorfo** (misma estructura, otros valores), nunca repitiendo el mismo.
- Cierre = ≥85% al primer intento en 2 sesiones distintas + 1 repaso espaciado a 2-4 semanas. **El dominio decae**: repaso vencido no hecho → la actividad se reabre.

**Scoring por mecánica (política única, sin "se acepta pero"):** submit atómico en ordenar-secuencia y cajero (el par/la secuencia se entrega como acto único); precisión = taps correctos/taps totales con tope de errados en grillas; matching con un lado sobrecargado (más opciones que blancos) o puntuando solo los primeros n−1 pares; base rate **≥25-30%** para la tercera categoría en todos los clasificadores; presupuesto de bloques en T2 (el bucle es obligatorio, no opcional); toda respuesta es correcta o no lo es — el matiz va al feedback, jamás al puntaje. Feedback de error: **1-2 líneas máximo** ("valla = cerco"), nunca un párrafo.

**Capa de motivación (pedido del alumno + mitigaciones del auditor):** racha diaria con aviso; puntos solo al primer intento con medalla bronce/plata/oro y récord personal en juegos de fluidez ("contra tu yo de ayer"); **mapa de desbloqueo por bimestre** (senda visible, lo cerrado en modo teaser — mata la percepción de "lo terminé en 2 semanas") con **coronita de dominado** por actividad; **reto del día**: 5 ítems interleaved de todo lo ya dominado, una vez por día; **examen de eje** acumulativo al cierre de cada bimestre; orden libre dentro del bimestre desbloqueado; sets de sprites para la sub-banda 10-12 (fútbol, espacio, misterio, gamer). **Panel de padres**: "12/56 dominadas · 78% de precisión al primer intento · 3 repasos vencidos" — el diferencial del producto (dominio, no completitud) hecho visible; sin esto, se compite en la única dimensión donde el producto es caro: cantidad aparente.

### MATEMÁTICA (18) — ⚙ = plantillas paramétricas (banco efectivo ilimitado; aguanta la ráfaga pre-evaluación y elimina la memorización de banco)

| Actividad | Mecánica | Banco | Dificultad d1→d3 | Contenido DC 5° |
|---|---|---|---|---|
| M1. Recta del millón (núcleo) | Tap en zona de recta CSS + componer MC3 ⚙ | 16 plantillas | 4 cifras con ticks rotulados → 7 cifras sin rotular | Lectura/escritura/orden en el rango del millón; recta; valor posicional; composición por unidad seguida de ceros |
| M2. Traductor romano (ext.) | MC3 + matching sobrecargado | 20 | ≤39 → regla sustractiva (IX, XL, CM) | Sistema romano (nodal): diferencias con el decimal (posicionalidad, el 0) |
| M3. Misiones de varios pasos (núcleo) | Trivia MC3 con tabla de datos + respuesta escrita (tecladito) ⚙ | 16 plantillas | 2 pasos ≤1.000 → 3 pasos, 4-5 cifras, dato de más | Problemas de varios pasos con las 4 operaciones; tratamiento de la información |
| M4. Combinador de conjuntos (núcleo) | MC3 anticipación + verificación pictórica en grilla (CPA) ⚙ | 24 plantillas | 2×3 → 4×5 y tres conjuntos | Combinatoria (nodal nuevo); pasaje a escritura multiplicativa |
| M5. La cuenta escondida (núcleo) | MC3 + modo "detectá el imposible" + tecladito ⚙ | 20 plantillas | divisor de 1 cifra → 2 cifras | c×d+r=D con r<d; análisis del resto |
| M6. Cazamúltiplos (núcleo) | Grilla del 100 contrarreloj (récord/medallas) + MC descomposición ⚙ | grillas generadas + 12 plantillas MC | múltiplos de 2/5/10 → 6/7/8 y comunes | Divisibilidad (nodal nuevo): múltiplos, divisores, descomposición multiplicativa |
| M7. División por aproximaciones (núcleo) | Ordenar pasos + MC anticipación + **modo guiado con tecladito** (hacer la división entera paso a paso) + **modelo pictórico de reparto (CPA)** ⚙ | 24 plantillas | ÷1 cifra en 3 pasos → ÷2 cifras económico | Algoritmos intermedios de la división; anticipar cifras del cociente |
| M8. Duelo de fracciones (núcleo; evoluciona `fracciones_avanzado`) | Clasificar 3 cajas (<½, ½-1, >1) + matching equivalentes, barra CPA ⚙ | 24 (familias generadas, CON doceavos y sextos) | barras visibles → solo símbolo | Comparación vs. entero y vs. ½; equivalencias tercios/sextos/doceavos, quintos/décimos |
| M9. Reconstruí el entero (núcleo) | MC3 con barras/colecciones pictóricas ⚙ | 20 plantillas | desde 1/4 → desde 3/4 o 2/5; luego discreto | Reconstrucción de la unidad (nodal); fracción de un natural |
| M10. Panadería de fracciones (núcleo) | MC3 con barras CPA que se juntan/parten ⚙ | 24 plantillas | mismo denominador → ½+¼+⅛ mezclados → fracción×natural | Suma/resta de medios/cuartos/octavos; dobles y triples; fracción como operador |
| M11. Del décimo a la coma (núcleo) | Matching + componer MC, barra de 10/100 (CPA) ⚙ | 20 plantillas | décimos → centésimos → composición mixta | Equivalencia fracción decimal↔expresión decimal; estructura de la notación |
| M12. Cajero con coma (núcleo; evoluciona `pago_exacto`) | "Tocá 2-3 que sumen X" con **entrega atómica del par** + MC vuelto; precios ARS verosímiles y **actualizables por inflación** ⚙ | 20 plantillas | 2 precios con ,50 → 3 precios y vuelto de $10.000 → natural×decimal | Suma/resta de decimales con anticipación; natural×decimal + Ed. Financiera |
| M13. ¿Proporcional o no? + Receta elástica (núcleo) | Clasificar 3 cajas (sí/no/no se puede saber, base rate ≥25%) + MC tabla ⚙ | 20 plantillas + 8 recetas fijas | con valor unitario → sin unidad → recetas con ½ y ¼ kg | Proporcionalidad directa; proporcional vs. no proporcional; recetas |
| M14. Geometría constructiva (núcleo, 3 modos) | A: MC "¿se arma este triángulo?" con animación de varillas y **tercera opción real** ("se arma, pero distinto del pedido", casos de suma igual); B: Plegado imposible (elegir desarrollo, láminas 2D); C: **lectura de transportador en lámina** ("¿mide 40° o 140°?") | 30 fijos (10+10+10) | casos obvios → casos límite | Desigualdad triangular (nodal); suma de ángulos; clasificación; desarrollos planos (nodal); medición de ángulos |
| M15. Perímetro vs. baldosas (núcleo) | MC perímetro + grilla tocable (precisión por tap) ⚙ | 20 plantillas | rectángulos → figuras en L → igual perímetro, distinta área | Fórmulas de perímetro; área con unidades no convencionales — eje que ESTRENA |
| M16. Encuesta y gráfico (núcleo) | Clasificar→tabla suma sola→barras CSS crecen + MC lectura | 16 escenarios (frecuencias regeneradas) | leer tabla → armar tabla → concluir | Tablas de frecuencias (nodal); barras y circulares — eje que APARECE |
| M17. Equivalencias de medida (núcleo) — **NUEVA** | MC3 + tecladito de conversión ⚙ | 20 plantillas | l↔ml y m↔cm directas → km/m/cm, kg/g, l/cl/ml combinadas con decimales | Unidades convencionales y equivalencias (nodal que estrena; refuerzo natural de decimales) — gap señalado por maestra y auditor |
| M18. Fluidez de tablas y cálculo (núcleo) — **NUEVA** | Contrarreloj estilo simon/arcade con **tecladito numérico** (respuesta escrita, sin opciones), medallas y récord diario; 100% generado | generador (tablas 2-9, ×/÷ inverso, cálculo mental) | tablas del 2/5/10 → 7/8/9 → divisiones asociadas | Remediación de fluidez multiplicativa (base de M5/M6/M7) — pedido n°1 de las familias y del propio alumno |

### LENGUA (16)

| Actividad | Mecánica | Banco | Dificultad d1→d3 | Contenido DC 5° |
|---|---|---|---|---|
| L1. Club de lectura (núcleo) — mecánica nueva estrella | Panel de texto + MC3 + señalar referente con **chips de palabras candidatas / zoom de párrafo (targets ≥48dp)** | **30 textos × 5 = 150** + 2 textos/mes | 200 palabras literales → 350 con inferencias entre párrafos | Inferencias; correferencia; información relevante; géneros DC completos: **fantástico, humor, noticia, teatro breve y poema** (criterio editorial: textos con intriga/humor real, no moraleja escolar) |
| L2. Cazador de recursos poéticos (ext.) | Tap en verso + clasificar rimas en 3 cajas | 20 | recursos marcados → poema limpio | Personificación, comparación, metáfora; rima asonante/consonante |
| L3. Verbos en tres cajas (ext.) | Clasificar 3 cajas; **modo arcade con combo, solo post-dominio** | 24 | verbos sueltos → en oración (contexto decide) | Verbos de acción, estado y psicológicos |
| L4. ¿OD u OI? (núcleo) | MC3 sobre palabra destacada, **SIN timer** (timer solo como modo fluidez opcional post-dominio); prueba de sustitución (lo/le) en el feedback | 20 | oraciones simples → con ambos objetos | Objeto directo e indirecto — el análisis más difícil del año, después de L14 |
| L5. Grados del adjetivo (ext.) | MC3 completar/transformar | 16 | regulares → mejor/peor, -ísimo | Comparativo y superlativo |
| L6. Futuro o condicional (ext.) | MC completar; ítem de registro ("¿me podés…?") reescrito con scoring binario y registro como contenido explícito | 20 | contraste claro → cortesía/hipótesis | Futuro y condicional; perífrasis "voy a + infinitivo" |
| L7. Vaya, valla o baya (núcleo) | MC con los 3 homófonos REALES (sin "cassar" ni grafías inventadas; tercer confundible real tipo "ahí") | 24 | contextos transparentes → doble candidato | Homófonos heterógrafos: ay/hay, casar/cazar, vaya/valla/baya |
| L8. Acentuación (núcleo) | MC tocar versión correcta (sin "queé") | 24 | **d1 = agudas/graves/esdrújulas (repaso general de 4°)** → d2-d3 diacrítica (qué/que, él/el, mí/mi, sé/se), hiatos, -mente | Acentuación general + tilde diacrítica + -mente (la diacrítica entra a mitad de año, como en el aula) |
| L9. Prefijos poderosos (ext.) | Matching sobrecargado prefijo+base↔significado | 20 | pares transparentes → falsos prefijos (insecto, destino) | Prefijos in-/des-/micro-/sub-/anti- |
| L10. Una palabra, varios sentidos (ext.) | MC acepción por contexto | 16 | acepciones lejanas → cercanas | Polisemia; acepción según contexto |
| L11. Arquitecto de textos (ext.) | Ordenar bloques (submit atómico) + matching rótulo↔zona; **el e-mail es el caso de entrada** y la carta papel el formato histórico-escolar | 30 (12 cartas/mails + 8 entrevistas + 10 noticias) | bloques rotulados → sin rotular | Estructura de carta física y digital, entrevista, noticia (título, bajada, epígrafe) |
| L12. Dos puntos y raya (núcleo) | Tap en posición del signo + MC entre versiones | 16 | diálogo simple → narrador intercalado | Dos puntos en discurso directo (indicador); voz de narrador vs. diálogo |
| L13. ¿Opinión o argumento? (ext.) | Modo A: clasificar opinión/argumento/hecho (cajas consistentes); Modo B aparte: publicidad — ¿argumento o recurso persuasivo? | 20 | enunciados sueltos → dentro de nota/aviso | Argumentativos: notas de opinión y publicidades |
| L14. Sujeto y predicado completos (núcleo) — **NUEVA** | Delimitar S/P por bloques-chip en oraciones largas + identificar núcleos (extiende `analisis_sintactico`) | 20 | oración simple bimembre → sujeto extenso, unimembres | Sujeto/predicado y núcleos — indicador explícito del DC y **prerrequisito de L4**; responde también al reclamo del alumno ("analizar oraciones enteras, no una palabra en negrita") |
| L15. ¿Cantó o cantaba? (núcleo) — **NUEVA** | MC completar narración breve | 24 | contraste puro → dentro de un párrafo de cuento | Pretérito perfecto simple vs. imperfecto en la narración — la traba n°1 al escribir cuentos (gap señalado por la maestra) |
| L16. El conector justo (núcleo) — **NUEVA** | Cloze MC3 | 20 | pero/porque/entonces → aunque/mientras/sin embargo | Conectores y cohesión (nodal; gap señalado por la maestra) |

### CIENCIAS NATURALES (8)

| Actividad | Mecánica | Banco | Dificultad d1→d3 | Contenido DC 5° |
|---|---|---|---|---|
| N1. Armá el ciclo hidrológico (núcleo; reemplaza `planta_potabilizadora`) | Ordenar secuencia (submit atómico) + matching proceso↔cambio de estado; recorridos DISTINTOS por ronda | 12 recorridos + 8 MC | 3 pasos rotulados → 5 pasos + estado en cada uno | Ciclo hidrológico como modelo; tres estados en los subsistemas |
| N2. Homogénea o heterogénea (núcleo) | Clasificar 2 cajas + "no es mezcla" (base rate ≥30%) | 18 | casos visuales → trampa (sal disuelta, agua destilada) | Mezclas; clasificación |
| N3. Laboratorio de disolución (núcleo) | MC predicción con partículas ilustradas (sprites 2D); **un factor por vez** (ítem "depende" eliminado: control de variables, que es la habilidad del DC) | 20 | un factor → dos combinados con control | Modelo de partículas; factores: tamaño, temperatura, agitación |
| N4. El plato GAPA (ext.) | Clasificar grupos + MC proporciones + detective de etiquetas/sellos | 20 | clasificar → plato proporcionado → sellos | GAPA; etiquetado frontal (Transversal Alimentaria) |
| N5. Recorrido de la nutrición (núcleo; reemplaza `camino_digestivo`) | Ordenar recorridos VARIADOS (nutriente/oxígeno/desecho por sistemas distintos) + matching órgano↔sistema↔función | 12 recorridos + 10 matching | 1 sistema → 2-3 sistemas → integradora | Nutrición como proceso integrado (digestivo, circulatorio, respiratorio, excretor) hasta la célula |
| N6. Luz: opaco, traslúcido, transparente (ext.) | Clasificar 3 cajas + MC predicción de sombra (láminas fijas) | 18 | materiales cotidianos → tamaño de sombra | Materiales frente a la luz; propagación rectilínea; reflexión |
| N7. Sonido: vibraciones y cualidades (ext.) | Clasificar + MC con audio; **detección de mute: difiere el ítem sonoro, no penaliza** | 18 | cualidades separadas → combinadas + medios | Sonido como vibración; no en vacío; volumen/altura/timbre |
| N8. Fases de la Luna y eclipses (núcleo) | MC con láminas Sol-Tierra-Luna + ordenar fases | 16 | reconocer → explicar el porqué → eclipses | Fases (la Luna siempre iluminada por la mitad); eclipses como sombras. El distractor "la sombra de la Tierra la tapa" es LA misconception — validado con entusiasmo por el propio alumno |

### CIENCIAS SOCIALES (9)

| Actividad | Mecánica | Banco | Dificultad d1→d3 | Contenido DC 5° |
|---|---|---|---|---|
| S1. Línea de tiempo 1806-1853 (núcleo) | Ordenar tarjetas, submit atómico. **Versión corta (1806-1810) pegada al 25 de Mayo; versión completa como SÍNTESIS de B4** | pool 16 hitos / 12 mazos | 4 hitos gruesos → 8 con Triunviratos/Directorio → con años | Indicador: línea de tiempo del proceso revolucionario e instituciones |
| S2. ¿Causa interna o externa? (núcleo) | Clasificar 3 cajas (interna/externa/**antecedente, no causa directa** — reformulación del ítem del Virreinato para no fijar tesis historiográficas como hecho) | 16 | casos claros → matizados | Crisis del orden colonial: circunstancias internas y externas; multicausalidad |
| S3. El debate de Mayo (núcleo) | Clasificar Moreno/Saavedra/los dos coincidían (base rate ≥25%) | 15 | posturas núcleo → matices | Debate Moreno-Saavedra |
| S4. Los símbolos de la Asamblea (núcleo) | Matching sobrecargado + MC3 | 15 | reconocer → función/historia | Asamblea del XIII: libertad de vientres, moneda, símbolos |
| S5. Próceres y gestas (ext.) | Matching figura↔gesta; **arranca por los ítems difíciles** (Belgrano economista y abogado) — el nivel base "San Martín cruzó los Andes" viene sabido de los actos | 16 | aportes menos famosos → cruces de perfiles | Gesta Sanmartiniana; Belgrano; Güemes |
| S6. ¿Unitario o federal? (núcleo; absorbe `derechos_constitucion`) | Clasificar 3 cajas + MC3 con distractores conceptuales (los ítems obvios del V/F, afuera) | 20 | ideas núcleo → consecuencias y art. 1 | Unitarios/federales; Constitución de 1853 como acuerdo y ley suprema (+ FEC) |
| S7. Armá el mapa de América (núcleo) | Matching país↔subcontinente (sobrecargado) + tap en lámina | 20 | subcontinentes → vecinos y límites → escala/símbolos | Mapa político de América; Andes; límites; escalas |
| S8. Clasificador de recursos (ext.; reemplaza `actividad_economica`) | Clasificar 3 cajas + MC valorización | 16 | casos claros → mismo lugar, dos usos | Recursos forestales/mineros/panorámicos; valorización en el s. XIX |
| S9. Mi Buenos Aires querido (ext.) — **NUEVA** | Matching lugar↔función↔época + tap en lámina de Plaza de Mayo | 16 | reconocer Cabildo/Casa Rosada/Catedral → qué pasó ahí en 1810 → barrios | Eje "la ciudad": Plaza de Mayo, Cabildo, barrios — gap señalado por la maestra (la salida al Cabildo se hace todos los años); conecta con S1/S3 |

### TECNOLOGÍA + TRANSVERSALES (5)

| Actividad | Mecánica | Banco | Dificultad d1→d3 | Contenido DC 5° |
|---|---|---|---|---|
| T1. La caja de la variable (núcleo) | Predicción MC3 sobre **bloques visuales estilo Scratch** (caja + bloque "sumar 3 a x"; la notación algebraica x=x+3 queda eliminada — fix de la maestra) ⚙ | 20 plantillas | 1 variable → 2 variables e intercambio | Variables: declaración, asignación, contar y sumar |
| T2. El bloque que falta (núcleo; endurece `programar_camino`) | Motor Logo + bloque REPETIR ×N + modo depurador (tocar el bloque culpable); **presupuesto de bloques por nivel** (el bucle es obligatorio: "avanzar ×4 suelto" ya no puntúa); niveles con semilla variable | 15 niveles ⚙ | repetir simple 6×6 → anidado con giro 8×8 → depurar | Bucles, condicionales, depuración |
| T3. Si el sensor detecta… (ext.) | Matching sensor↔actuador + MC predicción en casita ilustrada | 16 | 1 regla → 2 reglas + riego temporizado | Entrada/salida; sensores y actuadores; sistemas temporizados |
| T4. ¿Es phishing? (núcleo) | MC3 (seguro/trampa/dudoso-verificar) + tap en LA pista; **banco ampliado** (el juego mejor recibido por el alumno) con señuelos atractivos que exigen criterio, no virtud ("le paso solo el barrio, no la dirección exacta") | 24 | trampas burdas → remitente casi idéntico | Phishing; datos personales; identidad digital (Tec/ESI/ED) |
| T5. Presupuesto del proyecto (ext.) | Clasificar 3 cajas + cajero + MC; distractores sin deseabilidad social obvia | 15 escenarios | clasificar → presupuesto que cierra → absorber imprevisto | Ed. Financiera: ingreso-gasto, necesario/prescindible, ahorro/endeudamiento (refuerza M12/M13) |

---

## 3. Cambios al catálogo actual (los 25 del menú e==10)

**Resumen: 4 mantener · 8 endurecer · 12 retirar de 5° (2 de ellos absorbidos por actividades nuevas) · 1 mover de grado.**

| Juego actual | Decisión | Parámetros / destino |
|---|---|---|
| memotest (8 pares) | MANTENER | Evergreen de recreo cognitivo; nunca contado como curricular. |
| colorear | MANTENER | Recreo declarado (descanso atencional); su tiempo se resta del presupuesto de sesiones. |
| simon (8 bot.) | MANTENER | Único base que ya escala; recreo cognitivo con récord. |
| analisis_sintactico | MANTENER + ampliar | Banco 10→20; base de L14 (delimitación S/P completa) y de L4 (OD/OI, sin timer). |
| laberinto (9-12) | ENDURECER | data.json sub-banda 10-12: tamaños [12,14,15,16]; récord de tiempo. |
| programar_camino | ENDURECER | Se convierte en T2: 6×6/8×8 + repetir ×N + depurador + presupuesto de bloques + semilla. |
| sopa (10×10) | ENDURECER | 12×12, 8 palabras; pool desde el banco ortográfico del grado (-mente, prefijos, homófonos correctos). |
| sudoku (4×4, 8 pistas) | ENDURECER | `_sudoku_make` parametrizado: 6×6 con 14-16 pistas para e≥10; el 4×4 queda en 6-8. |
| serie (tope 16) | ENDURECER | Tope 1.000.000; pasos 10/100/1.000 y series de múltiplos (conecta con M6); corrige la inversión vs. 1°. |
| fracciones_avanzado | ENDURECER | Base de M8: banco 5→24 con doceavos y sextos, rondas sin repetición, y **corregir el comentario falso de actividades_web.py L306**. |
| pago_exacto | ENDURECER | Se convierte en M12: precios ARS reales con coma, actualizables, 2-3 sumandos, vuelto, entrega atómica; mueren los centavos de dólar. |
| derechos_constitucion | ENDURECER (absorbido) | Ítems obvios afuera; lo aprovechable pasa a S6 como MC3 con distractores conceptuales. |
| sumas (max 10) | RETIRAR de 5° | Propagar `suma_columnas` de 4° con cfg {cifras:5-6} — cierra la regresión reconocida en L290. |
| restas (max 10) | RETIRAR de 5° | Reemplaza `resta_columnas` con préstamo, 4-5 cifras (distractor: resta sin pedir prestado). |
| patron (ABC/AABB) | RETIRAR de 5° | Contenido de Inicial; queda en banda 6-8. |
| puntos (10-14) | RETIRAR de 5° | Conteo preescolar. |
| contar (max 9) | RETIRAR de 5° | Nivel Inicial. |
| mas_menos (max 9) | RETIRAR de 5° | Inicial. |
| agrupar (matching idéntico) | RETIRAR de 5° | Sala de 3; su slot lo ocupa la familia "clasificar por criterio" (L3, N2, S2…). |
| quefalta | RETIRAR de 5° | Sin contenido de grado. |
| bingo (3×3) | RETIRAR de 5° | Opcional futuro: bingo de múltiplos (M6), solo si sobra tiempo. |
| actividad_economica | RETIRAR de 5° | Sin anclaje en el DC 5°; parte del banco se recicla en S8. |
| camino_digestivo | RETIRAR (absorbido) | N5 lo reemplaza con recorridos variados por 4 sistemas; muere la secuencia fija ×4. |
| planta_potabilizadora | RETIRAR (absorbido) | N1 cubre agua con banco variado; la secuencia fija ×4 muere. |
| trivia_colonial | MOVER a 4° | Es exactamente el contenido de 4°; en 5° lo reemplazan S1-S6 + S9. |

Reglas transversales: los V/F de 2 opciones desaparecen (3 opciones o tercera categoría con base rate ≥25-30%); el puntaje de dominio cuenta solo el primer intento; cada error dispara una explicación de 1-2 líneas; rondas por bloque (6) ≤ banco por estrato en todo juego conceptual. En contenido cuyo objetivo ES memorizar (S1 cronología, S4 símbolos, S5 próceres) la repetición de banco es deseable y la regla "banco ≥ 2× rondas" no aplica.

---

## 4. Progresión del año (4 bimestres)

Recableado según la maestra (efemérides, fracciones tempranas, B4 aliviado) y el auditor (L1 en los cuatro bimestres, volumen por bimestre realista). Cada bimestre introduce ~10 actividades núcleo; la extensión se habilita con el bimestre y es de orden libre. El mapa de desbloqueo muestra la senda completa con lo no habilitado en modo teaser.

**B1 (mar-abr) — Base numérica, fluidez y contexto pre-Mayo** · Núcleo: M1, M3, **M18 (tablas desde el día 1: remediación de llegada)** + suma/resta de columnas (curación) · L1 (textos de 200), L8 dif 1 (**repaso agudas/graves/esdrújulas**), L14 (sujeto/predicado), L16 (conectores) · S2 (causas — mientras el aula repasa lo colonial) · N1, N2 · T1. Ext.: M2, L3. Andamiaje pleno, sin timers (salvo M18, que es fluidez por definición).

**B2 (may-jun) — Multiplicar/dividir + fracciones arrancan + Mayo en mayo** · Núcleo: M5, M6, M7, **M8, M9 (fracciones empiezan acá, no en agosto: necesitan meses de ida y vuelta)** · L4 (sin timer, con L14 ya dominada), L7 · **S1 versión corta 1806-1810 pegada al 25 de Mayo**, S3 (debate), S4 (símbolos, Belgrano en junio) · T2. Ext.: S5, N4, L2 · L1 continúa (textos de 250). Entran los contrarreloj de fluidez (M6, M18 récords).

**B3 (jul-sep) — Racionales completos + camino a 1853** · Núcleo: M4, M10, M11, M12 · L12, L15 · S6 (unitarios/federales), **S7 (mapa de América, adelantado desde B4)** · N3, N5. Ext.: L5, L6, L9, L10, N6, N7, T3 · L1 continúa (textos de 300). Las barras CPA pasan a pista de primer error cuando se sostiene 85%.

**B4 (oct-nov) — Medida, datos, proporcionalidad + síntesis** · Núcleo: M13, M14, M15, M16, M17 · L1 (textos de 350) · **S1 completa 1806-1853 como actividad de SÍNTESIS** · N8 · T4. Ext.: L11, L13, S8, S9, T5. **Carga nueva ≈ la mitad del borrador anterior** (noviembre real termina el 20): lo que no se llega, ya está cubierto por núcleo de B1-B3.

**Mecanismos de dificultad (no deseo):** (1) tags dif 1-3 con **banco por estrato ≥ rondas del bloque** y servicio adaptativo; el dominio exige ventanas con dif 2-3; (2) repaso espaciado: cada bimestre reinyecta ~20% de ítems anteriores intercalados + reto del día interleaved + examen de eje al cierre; (3) andamiaje que se retira solo (pista fuerte → sutil → nada) y dominio contado únicamente sin pista; (4) timers solo en fluidez (M6, M18, modos arcade post-dominio) — **nunca en comprensión ni en análisis** (L1, L4); (5) cierre = ≥85% al primer intento (últimos 10, ventana fija) en 2 sesiones + 1 repaso; el dominio decae si el repaso vence.

---

## 5. Lo que dijo el panel y qué se ajustó

### Maestra — adoptado
1. **Calendario recableado**: S1 corta en B2 (25 de Mayo) y completa como síntesis de B4; Sociales alineado a efemérides; fracciones (M8/M9) desde B2; S7 adelantado a B3; B4 con la mitad de la carga.
2. **L4 sin timer** y con prerrequisito explícito: **L14 sujeto/predicado completos** (nueva). Nota: su afirmación "no hay ninguna actividad de sujeto/predicado" era parcialmente inexacta (`analisis_sintactico` trabaja núcleos), pero el reclamo de fondo —delimitación de S/P completos en oraciones largas antes de OD/OI— es válido y L14 lo cubre.
3. **L8**: dif 1 = repaso de acentuación general en B1; la diacrítica a mitad de año.
4. **Gaps cerrados con 4 actividades nuevas**: L15 (imperfecto vs. perfecto simple), L16 (conectores), M17 (equivalencias de medida), M18 (fluidez de tablas — "es de 3°" no le importa a la familia que abre la app buscando eso, y sin tablas no hay división ni múltiplos). Más **S9 Mi Buenos Aires querido** (eje de ciudad que faltaba entero).
5. **L1 a 30 textos** con teatro y poesía incluidos + 2 textos/mes.
6. **Ítems paramétricos en lo numérico** (su punto "en cuentas, ítem fijo es plata tirada" coincide con el auditor y se adopta entero): resuelve también la ráfaga pre-evaluación (30 familias, misma actividad, misma semana).
7. **Ítems rotos corregidos**: "season 4" (M2.1), terna pitagórica (M14.1 → tercera opción real), "cassar" (L7.3 → confundible real), T1 en bloques Scratch (no álgebra), política única para "cuenta como casi" (eliminado: scoring binario, matiz al feedback).
8. **QA con docente del grado**: lectura completa de los ~890 ítems fijos por maestra de 5° antes de publicar, dentro del pipeline de §6.

### Alumno (Bauti) — adoptado
1. **Bloques de 6 rondas** con "una más" (en vez de 10 fijas); feedback de error de 1-2 líneas máximo.
2. **Capa de motivación completa**: racha con aviso, puntos solo al primer intento, medallas bronce/plata/oro y récord personal, mapa de desbloqueo por bimestre con coronita de "dominado", reto del día, orden libre dentro del bimestre, "contra tu yo de ayer" en fluidez.
3. **M18 tablas contrarreloj** (su pedido textual), **tecladito numérico** para responder sin opciones en matemática ("si siempre me dan 3 opciones, aprendo a elegir, no a saber"), **modo guiado de división entera** en M7 (hacerla paso a paso, no solo elegir).
4. **Lectura de transportador** como modo C de M14 ("¿mide 40° o 140°?").
5. **T4 phishing ampliado** a 24 ítems (su favorito), sprites para 10-12 (fútbol, espacio, misterio, gamer), premios/récords en sopa y laberinto, precios del cajero actualizables.
6. Criterio editorial de L1: textos con intriga/humor real — "huelo un texto de escuela a un kilómetro".

### Alumno — descartado o diferido (con motivo)
- **Monedas/skins**: diferido a fase 2 — economía cosmética que exige balanceo propio y no aporta dominio; racha + medallas + coronitas cubren el loop de retorno primero.
- **Duelo contra amigos**: fuera de alcance — no hay capa social en el motor; queda el duelo "contra tu tiempo de ayer".
- **Modo "tomame la lección" oral**: descartado — requiere entrada de voz que el motor no tiene; el reto del día y el examen de eje cubren el "saber qué no sé antes de la prueba". Se declara junto con producción escrita como límite honesto del producto.

### Auditor externo — adoptado (las 6 condiciones)
1. **Pipeline de QA de ítems** (ver §6): verificación aritmética automatizada de todo ítem computable + rúbrica por ítem (clave única defendible, rationale↔valor del distractor, stem autosuficiente) + lectura docente + piloto con chicos para L1. Los tres ítems rotos que detectó (M3.1: 430 = "suma todo", no "resta antes"; M10.2: el distractor de conversión errada es 3/8, no 2/8; M2.1: basura editorial) quedan corregidos en la especificación y motivan el pipeline.
2. **Dominio redefinido**: ventana fija de últimos 10 (no móvil), estratificada con dif 2-3 obligatoria, solo sin andamiaje, re-test isomorfo tras error, decaimiento por repaso vencido.
3. **Banco por estrato ≥ rondas** + plantillas paramétricas en matemática (mata el bug de `fracciones_avanzado` también dentro de los estratos).
4. **Política de scoring por mecánica**: submit atómico (ordenar, cajero), precisión por tap con tope (grillas), matching sobrecargado, presupuesto de bloques en T2 (sin bucle no se puntúa), eliminación de todo "se acepta pero".
5. **Base rate ≥25-30%** para terceras categorías en todos los clasificadores.
6. **Dosificación con holgura**: 39 núcleo + 17 extensión a 4 encuentros promedio; se comunica "el año cierra el núcleo (~70% del mapa)", no "56 actividades"; recreo cognitivo presupuestado. **Panel de padres** con métricas de dominio.
7. Además: L1 presente en los 4 bimestres (200→350), sesión definida por mecánica, M7 con modelo pictórico CPA, chips/zoom ≥48dp para tap-en-palabra, N7 con detección de mute, ítems reescritos (M6.3 "¿cuál NO es descomposición de 24?", N3.3 con control de variables, S2.3 "causa directa vs. antecedente", M12.1, M4.3, L8 "queé", M12.3, T4.3/T5.1 sin deseabilidad social, L13 con cajas consistentes), drops mensuales de textos, examen de eje bimestral, desbloqueo por bimestre como mitigación de la percepción de completitud.

Ninguna crítica estructural del panel fue descartada; los únicos descartes son los tres del alumno listados arriba, todos por límites del motor o secuencia de inversión, no por desacuerdo pedagógico.

---

## 6. Esfuerzo de construcción

### A. Curación (solo parámetros, horas)
laberinto [12-16] · sudoku 6×6 (parametrizar `_sudoku_make`) · sopa 12×12/8 palabras con pool ortográfico · serie tope 1M + pasos grandes + múltiplos · propagar suma_columnas/resta_columnas a e==10 (cierra la regresión de L290) · retirar los 10 juegos preescolares del menú e==10 · corregir el comentario falso de L306 · bloques de 6 rondas y rondas ≤ banco por estrato en todos los juegos · récord/medallas en sopa, laberinto, simon.

### B. Banco nuevo sobre mecánica existente (el grueso: ~44 de 56 actividades; el costo dominante es autoría + verificación, no código)
- **MC de 3 con distractores conceptuales**: M2, M3, M4, M5, M9, M10, M11, M14, M15, M17, L5, L6, L7, L8, L10, L15, L16, N3, N6, N7, N8, S4, T1, T3, T4.
- **Clasificar en 2-3 cajas** (base rate ≥25-30%): L3, L13, M8, M13, N2, N4, S2, S3, S6, S8, T5.
- **Matching sobrecargado**: L9, L11, S5, S7, S9, N5, T3.
- **Ordenar secuencia (submit atómico)**: S1, N1, N5, M7, L11.
- **Cajero (entrega atómica)**: M12, T5.
- **Grillas (precisión por tap)**: M6, M15.
- **Barras CPA existentes**: M8, M9, M10, M11, M13.
- **Volumen**: ~890 ítems fijos escritos a mano + ~300 plantillas paramétricas (banco efectivo >3.000) + 30 textos de L1 (+2/mes en régimen).
- **Pipeline de QA obligatorio antes de publicar** (condición 1 del auditor): (a) verificación aritmética automatizada de todo ítem computable; (b) rúbrica por ítem: clave única defendible, valor del distractor ↔ rationale del error, stem autosuficiente, feedback ≤2 líneas; (c) lectura completa por docente de 5°; (d) piloto con chicos reales para L1 y las 4 actividades nuevas de mecánica.

### C. Mecánicas nuevas (5, mínimas)
1. **Lector con preguntas** (panel 200-350 palabras + MC + referente por chips/zoom ≥48dp): habilita L1, L2, L12, L14 — el gap n°1 de la auditoría; se reusa íntegro en 6°/7°.
2. **Bloque repetir ×N + modo depurador + presupuesto de bloques** sobre el motor Logo existente: habilita T2 y salda bucles del DC.
3. **Tecladito numérico** (respuesta escrita sin opciones): habilita M18, el modo guiado de división de M7 y respuesta abierta en M3/M5/M12/M17 — pedido directo del alumno y condición para que el producto certifique "saber", no "elegir".
4. **Recta numérica por zonas** (MC sobre 3 zonas resaltadas de barra CSS, sin drag): M1.
5. **Barras de frecuencia CSS que crecen** (divs sobre clasificar): M16.

### D. Sistema transversal (se construye una vez, se amortiza en todos los grados)
Motor de dominio v2 (ventana fija, estratos, ítems isomorfos, decaimiento y reapertura) · motor de plantillas paramétricas con restricciones · capa de motivación (racha, medallas/récords, mapa de desbloqueo por bimestre, coronita, reto del día interleaved, examen de eje) · **panel de padres** (dominadas, precisión al primer intento, repasos vencidos — sobre datos que el sistema ya registra) · detección de mute para ítems con audio.

### Fuera de alcance declarado (límites honestos del motor; inversión aparte si algún día se quiere)
Construcción geométrica libre con regla/transportador (la lectura de transportador en láminas de M14 sí entra) · plegado 3D real (se resuelve con láminas MC) · simulador físico de luz/sonido (láminas + audio existente) · producción escrita real y oralidad/lección oral (requieren corrección abierta y voz; se declara a los docentes, no se promete) · capa social/duelo entre amigos · economía de monedas/skins (fase 2).
