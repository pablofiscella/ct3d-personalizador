# 1° grado (6 años)

**Dossier definitivo — Cuaderno de actividades interactivo, alineado al Diseño Curricular CABA 2024.**
Integra: auditoría curricular externa del estado actual, propuesta de diseño, y las tres devoluciones del panel (maestra de 1°, alumno de 6, auditor pedagógico externo). Donde el panel encontró defectos válidos, este documento YA los incorpora; los descartes se justifican en la sección 5.

---

## 1. Estado actual — veredicto de auditoría

24 juegos servidos a edad 6 (17 base de banda 6-12 + 7 exclusivos `e==6`). Densidad curricular real: **~21%** (5 de 24 con alineación verdadera). El dato de campo (alumnos de 4° reportan "muy fácil") es coherente: la banda "grande" agrega juegos por edad pero jamás recalibra los base (`_menu()` L224-230), así que la base quedó anclada a Nivel Inicial para toda la banda.

| Juego | Veredicto | Por qué (una línea) |
|---|---|---|
| memotest | SIN ANCLAJE | Memoria visual de sprites; el único memotest anclable (tipos de letra A-a) no existe. |
| contar | MUY FÁCIL | Contar hasta 9 sin agrupar = sala de 5; el DC pide colecciones grandes organizadas de a 10 y serie hasta 100. |
| colorear | SIN ANCLAJE | Juego libre sin consigna ni corrección ("¡Listo!" da win incondicional). |
| sumas | MUY FÁCIL | Tope 10 resuelto contando sprites; el DC pide dígito+dígito hasta 18, n+10, redondos que dan 100. |
| restas | MUY FÁCIL | `a≤10, b<a` con dibujitos; falta todo el tramo −10 y las familias suma↔resta. |
| serie | ALINEADO con déficit | Ancla en regularidades, pero solo +1/+2 ascendente hasta 30; el DC pide escalas ±1 y ±10 hasta ~100. Bug: 6 años ve tope 30 y 7-12 ve 16. |
| patron | SIN ANCLAJE | Patrones AB/AABB no figuran en ningún eje del DC de 1°; es Nivel Inicial. |
| puntos | MUY FÁCIL | Tocar 1…14 en orden es serie de sala de 5 con premio gráfico. |
| mas_menos | MUY FÁCIL | Comparar colecciones visibles de 1-9; el indicador de 1° es ordenar NUMERALES de una y dos cifras. |
| simon | SIN ANCLAJE | Memoria de trabajo con colores; ningún contenido DC (y es el único base que escala por edad). |
| agrupar | MUY FÁCIL | Matching de identidad pura (`r === item`) = sala de 2-3; el DC pide categorías semánticas o características observables. |
| quefalta | SIN ANCLAJE | Memoria visual de 5 ítems. |
| bingo | SIN ANCLAJE | Buscar el sprite idéntico al mostrado; un bingo NUMÉRICO sí anclaría — no es este. Bonus: `tam:9` con grilla real de 8. |
| laberinto | MUY DIFÍCIL | 4 niveles 9×9→12×12 obligatorios, idénticos a los de 12 años (`tams=[9,10,11,12]`, actividades_web.py:724); anclaje débil (destreza motriz, no comunicación espacial). |
| programar_camino | ALINEADO | Calza con TDyP ejes 3-4 y ED (anticipación de secuencias, desplazamientos y giros). El mejor del set. |
| sopa | MUY DIFÍCIL y contraproducente | 10×10, 8 direcciones, diagonales y reversas (`_DIRS`, cuaderno.py:625), idéntica a 12 años, único juego sin perilla; entrena CONTRA la direccionalidad izquierda-derecha que 1° está consolidando. |
| sudoku | SIN ANCLAJE | Lógica de restricciones no figura en el DC de 1°; 4×4 con 8 huecos es exigente como primera exposición. |
| armar_palabra | MUY FÁCIL | Ancla nominal en sílabas pero degradado: 7 palabras casi todas CV, sin distractoras, primer tap 50/50 y segundo forzado, emoji visible. |
| abecedario | DESALINEADO | Orden alfabético relativo de letras lejanas (J-Ñ-R-W) es contenido de 2°-3°; el DC de 1° pide letra-sonido. |
| suma_rapida | ALINEADO | Literalmente el nodal "sumas que dan 10", base del repertorio aditivo. |
| campo_ciudad | MUY FÁCIL | Dicotomía con emojis inequívocos = Inicial; el DC pide zonas del espacio urbano y etapas de producción. |
| planta_fruto | SIN ANCLAJE | Pares emoji arbitrarios; error conceptual: presenta una raíz (zanahoria) como "fruto". |
| materiales | ALINEADO | Indicador textual del DC: "identificar de qué material está hecho un objeto". Le falta el nivel de propiedades. |
| grilla100 | ALINEADO | "Serie escrita hasta 100 identificando regularidades" — el gamificable #1 que el DC sugiere. Faltan modos y distractores conceptuales. |

**Conteo:** 5 ALINEADO (1 con déficit) · 8 MUY FÁCIL · 2 MUY DIFÍCIL · 1 DESALINEADO · 8 SIN ANCLAJE.

### Los 5 gaps más graves

1. **Letra-sonido / conciencia fonémica (Lengua)** — el DC declara el sistema de escritura foco prioritario de 1° y el producto no lo trabaja: es el gap que invalida el claim "cuaderno de 1° grado".
2. **Valor posicional en dieces y unos (Matemática)** — sin esto no hay puente a los cálculos de dos cifras; todo el set numérico vive por debajo de 10/30.
3. **Eje Espacio, formas y medida entero (Matemática)** — geometría, medida y calendario: 0 de 3 bloques nodales.
4. **Lectura y comprensión de oraciones/textos (Lengua)** — ni una actividad de lectura con sentido; la única exposición a texto (sopa) entrena contra la direccionalidad.
5. **Problemas de suma/resta con significado + repertorio ±10 (Matemática)** — solo hay cálculo descontextualizado con opciones múltiples.

---

## 2. Mapa propuesto del año

### Números totales

**45 actividades curriculares + 7 juegos de "Recreo"** (sin sello curricular, sección aparte del menú, visible siempre y gateado por dosis: se abre tras la actividad curricular del día).

| Área | Actividades | Ítems a mano |
|---|---|---|
| Lengua | 13 | ~397 |
| Matemática | 14 | ~167 + 7 generadores |
| Conocimiento del Mundo | 9 | ~180 |
| TDyP + Transversales | 9 | ~166 + 1 generador |
| **Total** | **45** | **~910 ítems a mano + 8 generadores paramétricos + ~750 clips de audio** (incluye 100 números para el bingo y ~30 fonemas de grabación humana) |

### Reglas de dominio (versión corregida por el panel)

- **Sello de dominio** = ≥85% de precisión **al primer intento** en ventana móvil de 10 ítems (la ventana cruza sesiones), sostenida en **2 sesiones en días distintos**. El primer intento se marca ANTES de cualquier pista; el acierto post-pista no repesca la ventana.
- **Clasificadores de 2 categorías** (C3, parte de C8/T6): se exige además ≥85% a nivel sesión — la ventana móvil sola es estadísticamente floja con 50% de azar (hallazgo 1.1 del auditor).
- **Ordenar secuencias** (L10, C5, C7, T2): el ítem es la secuencia COMPLETA entregada de una vez (botón "listo"); primer intento = primera entrega. Sin crédito parcial ni fuerza bruta.
- **L9**: los ítems resueltos con audio previo NO computan para el sello de lectura (sí como práctica andamiada).
- **Recompensa visible el mismo día**: media medalla al cumplir el día 1, medalla completa al confirmar el día 2 (pedido del alumno: "si hoy hago todo bien y no me dan nada, me siento estafado").
- **Bajada de andamiaje automática** (pedido de la maestra): si no sella en 4 sesiones, vuelve el apoyo pictórico/contable y el rango baja un escalón. El andamiaje no solo se retira: también sabe volver.
- **Repaso espaciado**: cada actividad dominada reaparece a las 2 y 6 semanas con ítems no vistos. Bancos que no dan para repaso limpio lo declaran (**ciclo corto**: revisita sin sello nuevo) — solo C5 queda en ese régimen.

**Regla de bancos:** drill de habilidad núcleo 30-42 ítems; conceptuales 15-24 o techo epistémico documentado (27 letras, 5 complementos de 10, 6 cuerpos); piso 15 salvo techo real o ciclo corto declarado. Generadores con distractores por **plantilla de error conceptual**, nunca ±azar. Los "techos de recursos" (sprites disponibles) se nombran como decisión de presupuesto, no como techo del dominio.

### LENGUA (13) — eje Sistema de escritura, Lectura, Conocimiento de la lengua

| # | Actividad | Mecánica | Banco | Dificultad inicial→final | Contenido DC |
|---|---|---|---|---|---|
| L1 | ¿Con qué sonido empieza? | Tap-selección con audio de fonema (grabación humana; oclusivas con cue silábico) | **36 asimétrico**: 24 de sonido inicial (12 fonemas) + 12 de sonido final SOLO sobre /n/ /s/ /l/ /r/ /d/ — la matriz 12×3 era imposible en español | Nivel 1 = diagnóstico exprés (se pasa rápido) → pares mínimos → sonido final | "Conciencia fonológica: reconocimiento, separación y combinación de fonemas" |
| L2 | La letra del sonido — **REHECHA** | Modo A: fonema→letra solo con las **~20 letras unívocas** del rioplatense. Modo B (contexto de palabra) para las ambiguas: B/V, C/S/Z, C/K/Q, G/J, Y/LL y H muda ("¿con cuál se escribe VACA?") — poner V como distractor de /b/ sería enseñar un error | 36 (20 unívocos + 16 de contexto) | Vocales y continuas (m, s, l) → oclusivas → **b/d en rondas separadas hasta B3** (no fabricar el error espejo) | "Relación sonidos-letras"; "sonido vs. nombre de la consonante" |
| L3 | Sílabas (contar y armar) | Contar sílabas + armar con **2 sílabas distractoras**, imagen oculta hasta el primer intento. Endurece `armar_palabra` | 40 palabras (16 bisílabas, 14 trisílabas, 10 con inversas) | Bisílabas CV → trisílabas → inversas (VEN vs VE) | "Separación y combinación de sílabas en la oralidad" |
| L4 | Armá la palabra / **Dictado** | Slots + fichas de letras con distractoras → **nivel B3-B4: dictado con teclado completo de 27 letras, sin fichas** (el andamiaje por fin se retira donde más importa) | **42 palabras** (10 inversas, **24 trabadas** — duplicadas: son el muro del 2° semestre, 8 mixtas) | Inversas (SOL) → **trabadas desde B2** (PLATO, TREN: los chicos las pelean AHORA, no en noviembre) → dictado | "Lectura y ESCRITURA de palabras con distinto nivel de complejidad fonológica (grupos consonánticos)" |
| L5 | Parejas de letras | **Sello por tap-selección** (muestro G, tocá su minúscula entre 4); el memotest queda como modo de práctica — en un memotest los primeros destapes son azar y el último par sale por descarte: no mide dominio | 27 pares (techo epistémico) | Pares de forma distinta → **b/d contrastadas recién en B3** → imprenta-cursiva (ampliación) | "Identificación de los distintos tipos de letras" |
| L6 | Despegá las palabras | Tap-zonas entre letras (primitiva nueva compartida) | 20 oraciones | **Arranca con 2 palabras y audio previo de la oración**; 5 palabras con artículos al final | "Las palabras como unidades separadas por espacios" |
| L7 | Mayúscula y punto | Tap-zonas (tocar la letra que va con mayúscula, el lugar del punto) | 24 oraciones | Inicio de oración → nombre propio → dos oraciones (el punto separa) | "Mayúscula inicial y punto final" |
| L8 | Leé y encontrá | Tap-selección SIN audio previo (evalúa decodificación); audio después como confirmación | **36** (30 + **6 de tilde**: papá/papa, mamá/mama — nodal que faltaba) | CV frecuentes → pares mínimos (pato/gato/pata/plato) → **trabadas en B3** → rr/tilde | "Lee y escribe palabras con precisión"; "ciertas palabras llevan tilde" |
| L9 | Leo y respondo | Texto 1→4 oraciones; pregunta con 3 opciones (distractor = tipo de pregunta equivocado); **modo "leéselo a alguien"** (pantalla grande, el adulto marca "lo leyó solo / juntos", sin evaluación); **biblioteca releíble** de textos ya dominados | 24 textos (16 literales, 8 inferenciales), voseo | 1 oración literal → 2-4 oraciones → inferenciales (B4); audio pasa de autoplay a bajo demanda | "Respuestas a qué/quién/dónde/cuándo"; "inferencias con pistas textuales" |
| L10 | Ordená el cuento | Ordenar secuencia; entrega completa = 1 ítem; feedback siempre "primero/luego/al final" | **16 secuencias** (subido del piso) | **3 escenas en B2** (lo hacen desde sala de 5: no era material de B4) → 4 escenas con estado interno del personaje en B4 | "Primero…, Luego…, Finalmente…" |
| L11 | ¿Cuál rima? | Tap-selección con audio (la rima es sonora) | 24 ítems | Rima evidente → completar copla | "Textos versificados (canciones, coplas)" |
| L12 | Canastas de palabras | Clasificar en 3 canastas; en nivel 2 la canasta ACCIONES lleva un verbo cerca (SALTAR) para capturar el error alegría→"salto de alegría" | 48 (36 n1-2 + 12 n3) | Categorías concretas → sentimientos/acciones → nombra/acción/describe | "Categorías semánticas; palabras que nombran, indican acciones, describen" |
| L13 | El, la, los, las | Tap-selección: imagen + sustantivo, elegir artículo entre 4 | 24 (con los trampa: el mapa, la mano) | Concordancia transparente → plurales → sustantivos trampa | "Singular/plural, femenino/masculino; concordancia" |

*Fuera de cobertura declarado en ficha:* trazado de letras y cursiva (los cubre el kit imprimible — y la ficha lo dice FUERTE, es la pregunta de agosto), oralidad productiva, escritura colaborativa.

### MATEMÁTICA (14) — ejes Números y operaciones + Espacio, formas y medida

| # | Actividad | Mecánica | Banco | Dificultad inicial→final | Contenido DC |
|---|---|---|---|---|---|
| M1 | Grilla del 100 (+ modo comparar) | Grilla existente; modos: decena con hueco → columna → **parche 3×3** (fila=+10 y columna=+1 a la vez) → **modo comparar numerales** (absorbe mas_menos: 27 vs 72, 39 vs 41). Distractores {cifras invertidas, ±1, ±10} en vez de ±12 azaroso | Generador; rangos 30→60→100 | Por bimestre | "Serie escrita hasta 100, regularidades"; "ordenar números de una o dos cifras" |
| M2 | Dieces y sueltos | Dos fases: ESTIMAR en **bandas (≈10/≈30/≈70, nunca el valor exacto** — si no, la fase 1 filtra la respuesta) → contar con barras de 10 → numeral. Modo inverso con distractor de **escritura aditiva: canta "sesenta y cuatro" → 64 ✔ · 604 ✖ · 46 ✖** (EL error de numeración de 1°, más frecuente que la inversión) | Generador (12-79) + 10 ítems meta | Pictórico → abstracto; el nivel concreto lo aporta el kit imprimible ("buscá 12 porotos") | "Composición y descomposición en unos y dieces"; "estimar" |
| M3 | El kiosco | Cajero "tocá los que suman X". **Máx. 9 monedas de 1 en caja desde nivel 2** (si no, se gana contando de a 1 sin componer jamás); "pagá de otra manera" exige que las combinaciones difieran en cantidad de billetes (fuerza el canje 10 unos = 1 diez). Enmarcado "kiosco de juguete" (precios idealizados) | Generador (10-99) | Redondos → dos cifras → segunda combinación | "Composición aditiva en contextos como dinero"; "combinaciones distintas para un mismo valor" |
| M4 | Serie con saltos | Completar serie. Pasos **±1 y ±10** (se elimina +2: no es del repertorio), tope 100, descendentes desde B3. El generador **FUERZA ítems de cruce de decena** (28,29,__ / 41,40,__) — ahí se caen todos y el azar del rango no alcanza. Distractor de descendentes corregido: 90,80,__,60 → 70 ✔ · 79 ✖ (baja 1) · **60 ✖ (saltea al siguiente escrito)** — "baja la mitad" no es un error documentado | Generador | +1 hasta 60 → ±10 → descendentes | "Escalas ascendentes y DESCENDENTES de 1 en 1 y de 10 en 10" |
| M5 | Parejas que suman 10 (y 100) | La actual + nivel redondos-100 (distractores que suman 110/120) + contrarreloj suave solo B4 | Techo epistémico: 5+5 complementos; generador de pantallas | 10 → 100 → contrarreloj | "Sumas que dan 10… redondos que dan 100" |
| M6 | Repertorio veloz | Tap-selección; absorbe sumas y restas. Plantillas de error por familia: 36+10 → 46 ✔ · 37 ✖ (aplica +1) · 63 ✖; 50−1 → 49 ✔ · 40 ✖ (resta 10); familias 7+3=10→10−7. **Cruce de decena forzado** (9+1, 30−1, 39+1) | Generador | Rondas 1-2 pictóricas (marcos de 10) → solo numerales; contrarreloj B4 | "n±1; n±10; 10−dígito; dobles hasta 18; restas asociadas a sumas" |
| M7 | Problemas del colectivo | Tap-selección sobre escena narrada. **Nivel concreto (≤10, pasajeros contables) entra en B1**: el DC construye el cálculo DESDE los problemas desde marzo, no como unidad tardía | **36 problemas a mano** (8 por significado + 8 concretos B1) | B1 contable → B3 la escena se describe pero no se puede contar (fuerza el cálculo) | "Agregar/quitar/juntar/perder; incógnita en estado final; composición con incógnita en una cantidad" |
| M8 | Armá el cálculo | Slots + fichas con números y signos: componer el cálculo que representa la escena (5−2=3; el error 2−5 se trabaja explícito) | 24 escenas | Suma/resta directa → incógnita (6+□=10) | "Representación simbólica: signos +, − y uso del =" |
| M9 | Bingo de números | Cartón **4×4 real** (se arregla la mentira del `tam:9`) de numerales 0-99; el audio canta "sesenta y cuatro"; el cartón contiene los distractores del cantado (46, 74, 54). Modo anexo "escribilo": tap entre 64 / **604** / 46 (escritura aditiva; el cartón no banca 3 cifras — el ataque principal va acá y en M2) | Generador + 100 audios | Hasta 30 → 60 → 100 | "Relaciones serie oral ↔ escrita"; "uso social de los números" |
| M10 | ¿Dónde está? | Tap-zonas sobre escena: suena la consigna, se toca el objeto que cumple la relación | 24 consignas / 6 escenas | Arriba/abajo → entre → "mirando hacia" (orientación, la más difícil) | "Está entre, arriba de, debajo de, delante de, atrás de, mirando hacia" |
| M11 | Detective de figuras | Tap-selección + tap-zonas para contar vértices. El "¿es un cuadrado? sí/no" se reemplaza por **"tocá TODOS los cuadrados"** sobre 4-6 figuras rotadas (sin moneda al aire). Triángulos escalenos y ROTADOS; cuadrado a 45° | 20 ítems (figuras CSS, cero assets) | 3 lados → 4 lados iguales/no iguales → rotadas | "Triángulo, cuadrado, rectángulo; vértices y lados (cantidad, igualdad)" |
| M12 | Caras y cuerpos | Matching cuerpo ↔ objeto cotidiano (dado, pelota, lata, cucurucho) + contar caras con tap | 18 (techo: 6 cuerpos × 3) | Cuerpo→objeto → caras → cono vs pirámide ("terminan en punta") | "Cubo, prisma, esfera, cilindro, pirámide, cono; caras, aristas, vértices" |
| M13 | Medí con clips | Dos fases estimar→verificar. Spec al ilustrador: en los ítems de comparación **el dibujo CONTRADICE la medida** (banco dibujado más largo, medido con clips más grandes) — si no, "mesa 6 vs banco 4" se responde con 6>4 sin entender medición | 15 (incluye los meta: clips separados/encimados) | Estimar → verificar → meta-ítems | "Longitudes con unidades no convencionales; estima y verifica lo anticipado" |
| M14 | El calendario | La grilla vestida de mes. **Nivel simple en B1** (qué día es hoy, tocá la fecha — es LA rutina de marzo de cualquier aula, no un tema terminal); duraciones (conteo entre fechas, el error inclusivo 4 vs 5) en B3 | 20 ítems / 4 meses plantilla | Fecha → mañana/ayer → duraciones | "Día, semana, mes; calendarios para ubicar acontecimientos y duraciones" |

### CONOCIMIENTO DEL MUNDO (9)

| # | Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|---|
| C1 | Clasificador de animales | 3 canastas (pelos/plumas/escamas; luego extremidades) | 24 animales anti-misconception (murciélago→pelos, pingüino→plumas) | Cobertura → extremidades | "Características observables: cobertura, extremidades; clasificación por criterios" |
| C2 | Armá la planta | Tap-zonas sobre dibujo + pregunta funcional. Reemplaza planta_fruto (que presentaba una raíz como fruto) | **16** (subido del piso: + preguntas funcionales y comparación entre plantas) | Partes → función ("¿con qué toma agua?") | "Partes de las plantas: hojas, tallos, raíces" |
| C3 | ¿Sólido o líquido? | Clasificar en 2 — rige la regla reforzada de binarios (85% por sesión además de la ventana) | 24 materiales, casos límite adelante (miel, harina, hielo) | Claros → viscosos/granulares | "Estados sólido y líquido; viscosidad y fluidez" |
| C4 | Objeto, material y propiedades | Trivia actual + nivel propiedades + nivel propiedad→uso ("dos vasos iguales: uno se rompió — ¿de qué era?") | 24 (10 actuales + 14) | Objeto→material → propiedades → uso | "Distinción objeto/material; dureza, fragilidad, elasticidad" |
| C5 | Del campo a tu casa | Ordenar secuencia (entrega completa) | 10 procesos — **ciclo corto declarado**: revisita sin sello nuevo (techo de recursos nombrado como tal) | 4 tarjetas → 5 con trabajos | "Etapas de producción de un bien primario; trabajos y herramientas" |
| C6 | ¿Antes, hoy o en los dos? | Clasificar en 3 (la CONTINUIDAD es el contenido que una dicotomía no puede enseñar) | 24 (16 genéricos: pan, juegos, anillos; 8 de la sociedad antigua) | Antes/hoy → en los dos | "Cambios y continuidades entre una sociedad antigua y el presente". *La ficha no promete "la sociedad que ve tu hijo en la escuela": el DC deja la elección a cada escuela; Egipto es la variante inicial* |
| C7 | Mi cuerpo y las etapas | Tap-zonas sobre silueta + ordenar etapas. Partes básicas se pasan rápido (diagnóstico); lo valioso son las etapas — con el abuelo MÁS BAJO que el papá (desarma "más alto = más grande"). Distractores rehechos: "¿qué cambia de bebé a nene?" → camina y habla ✔ · **"se hace más chico" ✖ (inversión) · "le cambia el color de ojos" ✖ (cambio no-desarrollo)** | 18 (12 partes + 6 secuencias) | Partes → etapas → cambios | "Cuerpo humano y sus partes; cambios en las etapas de la vida" (articula ESI). *Los nombres que fija la ESI se mantienen; la ficha a las familias lo avisa ANTES del primer comentario, no después* |
| C8 | Cuidarnos | Clasificar + matching necesidad→institución ("jugar sin parar": dosis, no demonización) | 20 | Prácticas → instituciones | "Prácticas saludables; instituciones que colaboran con el cuidado" |
| C9 | Las zonas de la ciudad | **Pasa de canastas a tap-zonas sobre plano urbano** ("tocá una zona de circulación") — mejor contenido y una canasta menos en el menú. + **4 ítems de paisaje** (nodal que faltaba) | 20 (16 zonas + 4 paisaje) | 3 zonas → 5 zonas → paisaje | "Zonas de vivienda, circulación, industria, comercio, recreación"; "el paisaje como conjunto de elementos" |

### TDyP + TRANSVERSALES (9)

| # | Actividad | Mecánica | Banco | Dificultad | Contenido DC |
|---|---|---|---|---|---|
| T1 | Llevá el robot | La actual + niveles 4×4/5×5 con obstáculos y dos soluciones + **modo predicción CON GENERADOR** (programa aleatorio corto sobre grilla, verificación automática — 8 ítems fijos eran memorizables en una sesión, y la predicción es la única evidencia real de anticipación) | 12 niveles + generador de predicción | 3×3 → giros → predicción | TDyP ejes 3-4; ED: "anticipación y prueba de secuencias… desplazamientos y giros" |
| T2 | Pasos en orden (y el intruso) | Ordenar secuencia (entrega completa) + "tocá el paso que está mal" | **24** (16 + 8 intruso; subido del piso) | Orden → intruso | "Recetas simples; relevancia del ORDEN, detectar incongruencias" |
| T3 | Herramientas y oficios | Matching herramienta→tarea→quién (género alternado sistemáticamente) | 15 | Herramienta → oficio | "Herramientas, funciones, oficios"; ESI: sin distinción de género |
| T4 | Separá los residuos | Clasificar; **colores genéricos "reciclables/basura"** con nota CABA en ficha (se vende a todo el país) + circuito circular vs lineal | 24 (servilleta engrasada, cáscara: los que rompen la regla superficial) | Claros → trampa → circuito | "Reciclables y no reciclables; separación en origen; circuitos" |
| T5 | Antes y ahora | Matching por FUNCIÓN (carta↔audio; el error es emparejar por parecido visual) | **16** (subido del piso) | Directos → por función | "Procesos del pasado y actuales (comunicación, alimentos)" |
| T6 | Íconos y datos | Matching ícono→función + clasificar dato (compartir/proteger). El ítem del "amigo del juego online" queda: es el error de familiaridad aparente que la ciudadanía digital de 1° debe atacar (y al alumno del panel le pasó en serio) | 20 | Íconos → datos privados | ED: "datos personales e información privada y resguardos" |
| T7 | Emociones | Matching escena narrada→emoción; cero fail state. Nivel alegría/tristeza se pasa rápido (es de sala de 3); el valor está en **vergüenza/miedo y pudor** | **15** (subido del piso; emociones del DC × escenas) | Básicas exprés → vergüenza/pudor | ESI: "alegría, miedo, vergüenza, pudor, amor y sus formas de expresión" |
| T8 | Armá el plato | Clasificar en grupos GAPA (papa→cereales y papa: "llena como el pan") | 24 | Claros → trampas GAPA | "Grupos y proporciones de la gráfica de las GAPA" |
| T9 | ¿Cruzo o espero? | Trivia de escenario con 3 opciones (la tercera siempre plausible e insegura) | **16** (subido del piso) | Semáforo → sin senda | "Rol de peatón; semáforo, senda; cuidado de sí y de otros" |

### Recreo (7 juegos, sin sello — número único y definitivo)

memotest · colorear (páginas nuevas desbloqueables con estrellas) · simon (tope de secuencia subido: cortaba justo cuando se ponía bueno) · quefalta · **laberinto recalibrado** (`tams:[6,7,8,9]`, gana con 2 de 4) · **sopa recalibrada** (6×6, 4 palabras, direcciones solo → y ↓) · **puntos renumerado** (de 10 en 10 hasta 100 — refuerza la escala sin sello).

### Capa de motivación (pedidos del alumno, filtrados)

Racha con mascota propia · estrellas CANJEABLES por cosméticos y contenido (páginas de colorear, niveles extra del robot, sprites de memotest — nunca para saltear contenido curricular) · **mapa del año con candaditos** (doble uso: para el chico es progresión visible; para el adulto es la vista de 45 casilleros con el contenido DC de cada uno — resuelve también el "el padre que paga en marzo ve 13 actividades") · elegir entre 3-4 propuestas del día · media medalla hoy / medalla mañana · botón "mostrale a alguien" · Recreo siempre visible, gateado por dosis. Sin cofres aleatorios (ver §5).

---

## 3. Cambios al catálogo actual (los 24 servidos hoy a edad 6)

| Juego | Decisión | Detalle exacto |
|---|---|---|
| memotest | MOVER a Recreo | La mecánica se reusa como modo práctica de L5; el sello de letras sale de tap-selección. |
| contar | RETIRAR de 6 | Reemplazado por M2. Queda en banda 3-5, donde corresponde. |
| colorear | MANTENER en Recreo | Juego libre declarado; páginas desbloqueables con estrellas. |
| sumas | ENDURECER (fusiona en M6) | `max:18, rondas:8`; sprites solo rondas 1-2, luego marcos de 10, luego numerales; distractores por plantilla de error; cruce de decena forzado. |
| restas | ENDURECER (fusiona en M6) | Agrega n−10, 10−dígito y familias suma↔resta. |
| serie | ENDURECER (es M4) | `pasos:[+1,−1,+10,−10]` (se elimina +2), `tope:100, rondas:8`, descendentes B3, cruces forzados. **Y corregir el bug invertido: 7-12 debe tener tope ≥ que 6** (hoy 6 ve 30 y 7-12 ve 16). |
| patron | RETIRAR de 6 | Nivel Inicial; queda en mini/media. |
| puntos | MOVER a Recreo, renumerado | De 10 en 10 hasta 100 (refuerzo de escala); con 1-14 era serie de sala de 5. |
| mas_menos | ABSORBER como modo de M1 | "Comparar" numerales de 2 cifras: pares trampa 27 vs 72, 39 vs 41; anclaje real en orden de la serie (resuelve el huérfano señalado por el auditor). |
| simon | MOVER a Recreo | Sin contenido DC; tope de secuencia subido. |
| agrupar | RETIRAR de 6 | Matching de identidad = sala de 2-3; su esqueleto de canastas se reusa en L12. |
| quefalta | MOVER a Recreo | Memoria visual sin anclaje. |
| bingo | ENDURECER (es M9) | Numerales 0-99 dictados con audio, distractores dentro del cartón; cartón 4×4 REAL (arregla `tam:9` vs grilla de 8). |
| laberinto | ENDURECER + Recreo | `tams:[6,7,8,9]`, gana con 2 de 4 (hoy: 9-12 obligatorios los 4, idéntico a 12 años). Anclaje débil → Recreo. |
| programar_camino | MANTENER y ampliar | Es T1: niveles 4×4/5×5, modo predicción con generador. El alumno del panel lo terminó en un rato y quería más: la queja más útil del dossier. |
| sopa | ENDURECER + Recreo | Perilla nueva: pasar `edad` a `_sopa_json` y filtrar `_DIRS` — a los 6: 6×6, 4 palabras, solo → y ↓ (hoy entrena CONTRA la direccionalidad). La 10×10 de 8 direcciones pasa a 8+. Sin anclaje de 1° → Recreo (resuelve el huérfano). |
| sudoku | MOVER a 7+ | Sin anclaje en el DC de 1° y exigente como primera exposición. No queda en 1° ni en su Recreo. |
| armar_palabra | ENDURECER (es L3) | Banco 7→40; +2 distractoras por ronda (hoy el primer tap es 50/50 y el segundo forzado — "cuando un juego no se puede perder, no es un juego"); imagen oculta; `rondas:6`. |
| abecedario | RETIRAR de 1° → 2°-3° | El orden alfabético relativo no es contenido de 1°; en 2°: modo "ventana de 6 letras contiguas". Su slot lo ocupa L2. |
| suma_rapida | MANTENER y ampliar | Es M5: nivel redondos-100 + contrarreloj B4. |
| campo_ciudad | RETIRAR | Nivel Inicial; reemplazado por C9 y C5. |
| planta_fruto | RETIRAR | Sin anclaje y con error conceptual (raíz como fruto); reemplazado por C2. |
| materiales | MANTENER y ampliar | Es C4: banco 10→24, niveles propiedades y propiedad→uso. |
| grilla100 | MANTENER y ENDURECER | Es M1: modos columna/parche/comparar; distractores {invertido, ±1, ±10}. |

**Balance:** 6 RETIRADOS de 1° (contar, patron, agrupar, campo_ciudad, planta_fruto, abecedario) · 1 MOVIDO de grado (sudoku→7+; abecedario reaparece en 2°-3°) · 7 a RECREO (memotest, colorear, simon, quefalta, laberinto, sopa, puntos) · 1 ABSORBIDO como modo (mas_menos→M1) · 5 ENDURECIDOS dentro del mapa (sumas y restas→M6, serie→M4, bingo→M9, armar_palabra→L3) · 4 MANTENER-y-ampliar (programar_camino, suma_rapida, materiales, grilla100 — los 4 que la auditoría marcó alineados). Sin huérfanos: sopa, puntos y mas_menos tienen destino definido.

---

## 4. Progresión del año (4 bimestres)

**Lógica transversal de dificultad:**
1. **Pictórico honesto que se desvanece** (no "CPA estricto": sprites en pantalla son pictórico; la fase CONCRETA la aporta el kit imprimible y objetos de la casa, con consignas puente "buscá 12 porotos" — sinergia declarada con el producto imprimible).
2. **Rango numérico**: 30 (B1) → 60 (B2) → 100 (B3-B4).
3. **Distractores que se acercan**: en B1 el conceptual convive con uno lejano; en B3-B4 las tres opciones son errores plausibles.
4. **Andamiaje que se retira Y que vuelve**: pista fuerte al primer error (el ítem ya quedó marcado fallado ANTES de la pista), ninguna tras 3 aciertos; bajada automática si no sella en 4 sesiones.
5. **Confundibles separados**: b/d no comparten ronda hasta B3; primero se fija cada uno.
6. **Contrarreloj solo en B4** y solo donde el DC pide fluidez.
7. **Regla de menú anti-monotonía**: nunca dos actividades de canastas/clasificar el mismo día (el alumno detectó 7 "canastas disfrazadas"; C9 además cambió de mecánica).

**Desbloqueo: híbrido con adelanto acotado.** Base por calendario bimestral; dominar habilita el bimestre siguiente DE ESA ÁREA (máximo 1 de adelanto). El chico que llega al techo entra en modo profundización (mezcladito + dictado + robot generado), nunca se queda sin contenido; el intensivo no agota el año en 10 semanas.

**Política de priorización ante atraso (el uso real son 2-3 sesiones/semana, no 4):** núcleo obligatorio = L1-L4, L8, M1, M2, M5, M6, M7 (≈60% del valor curricular). Con atraso, el menú prioriza núcleo + sus repasos; el resto se degrada a modo exposición (jugable, sin exigencia de sello). Sesión de referencia: 15-20 min; **los drills duran 6-8 min y 8-12 ítems — 12-15 min es techo, no promedio**.

### Bimestre 1 (marzo-abril) — "Sonidos, letras y números hasta 30" · 11 actividades nuevas
Marzo real son ~6 semanas útiles (período de inicio, diagnóstico, feriados): se bajó de 13 a 11 y las primeras semanas son diagnóstico exprés (L1 n1, T7 básicas, C7 partes).
**Lengua:** L1, L2 (gateada por "voy con la seño"), L3-contar. **Matemática:** M1 (≤30), M5 n1, M6 (n±1, dobles), **M7 nivel concreto** (el sentido entra desde marzo, no en agosto), **M14 nivel simple** (el calendario es LA rutina de marzo). **CdM:** C1. **TDyP/Transv.:** T1 (3×3), T7.

### Bimestre 2 (mayo-junio) — "Armo palabras, armo números" · 12 nuevas
**Lengua:** L3-armar con distractoras, **L4 (inversas + primeras trabadas** — el muro es de julio, no de noviembre), L5 (b/d separadas), L8, **L10 (3 escenas** — bajada de B4: lo hacen desde sala de 5). **Matemática:** M2, M3, M4 (±1 ≤60, cruces forzados), M9 (≤60), **M11 (figuras** — la geometría no depende del rango numérico; no se apila toda en noviembre). **CdM:** C2, C3. **TDyP/Transv.:** T2.

### Bimestre 3 (agosto-septiembre) — "Leo oraciones, resuelvo problemas" · 13 nuevas
**Lengua:** **L6** (movida de B2: despegar ELGATODUERME exige poder leer; arranca con 2 palabras y audio), L7, L9 (literales + modo "leéselo a alguien"), L11. **Matemática:** M6 (±10 completo), M7 (sin conteo posible), M8, M4 (descendentes), M10, M13, M14 (duraciones). **CdM:** C4-propiedades, C5, **C6** (adelantada: motivación de mitad de año), C7-etapas, C9. **TDyP/Transv.:** T3, T4.

### Bimestre 4 (octubre-diciembre) — "Textos, trabadas completas y fluidez" · 9 nuevas (el bimestre corto va liviano)
Octubre-diciembre rinde 8-9 semanas; **lo introducido después de fines de octubre sella con ciclo corto declarado** (el repaso de 6 semanas cae fuera del ciclo lectivo — se acepta por escrito, no se disimula). Después de la 2ª semana de noviembre no entra nada nuevo.
**Lengua:** L12, L13; consolidación: L4 trabadas completas + **dictado con teclado**, L9 inferenciales, L10 4-escenas, rr/tilde en L8. **Matemática:** M12; consolidación: M1 parche 3×3, M5-100 + contrarreloj, M6 abstracto + contrarreloj. **CdM:** C8. **TDyP/Transv.:** T5, T6, T8, T9; T1 5×5 + predicción.

Cada bimestre, las dominadas rotan como repaso espaciado (2-3/semana, ítems no vistos). El **modo mezcladito** (interleaving de ítems de todas las selladas del área) se activa por actividad al sellarla: convierte contenido "terminado" en práctica infinita sin escribir un ítem nuevo.

---

## 5. Lo que dijo el panel y qué se ajustó

### De la maestra — incorporado
- **B1 descargado** de 13 → 11 con arranque diagnóstico; **B4 descargado** a 9 nuevas y nada nuevo pasada la 2ª semana de noviembre.
- **M14 a B1** (rutina de marzo) y duraciones a B3; **L10 a B2** (B4 solo la versión con estado interno); **L6 a B3** con arranque de 2 palabras + audio; **M11 a B2** (la geometría no se corre a noviembre).
- **b/d separadas hasta B3** en L5 y en los distractores de L2: los confundibles no se presentan juntos la primera vez.
- **Escritura aditiva (604)** como distractor en M2-inverso y modo "escribilo" de M9; **cruce de decena FORZADO** en los generadores de M4 y M6.
- **Trabadas duplicadas** (L4: 12→24) y adelantadas a B2; trabadas en L8 desde B3.
- **Bajada de andamiaje automática** (4 sesiones sin sellar → vuelve el apoyo pictórico) — el andamiaje ahora tiene camino de ida y de vuelta.
- **Tilde** (nivel de 6 ítems en L8) y **paisaje** (4 ítems en C9): los dos nodales que faltaban.
- **Modo "voy con la seño"** (pedido 1): el adulto marca letras enseñadas y tope numérico del grado; L2/L4/L8 y M1/M9 no sirven nada por delante.
- **Plan del uso real** (pedido 3): política de priorización con núcleo obligatorio, y **reporte al adulto en 3 colores por eje, sin porcentajes**, con el error conceptual en cristiano ("confunde 47 con 74: está invirtiendo cifras").
- **Ficha para la familia**: qué hacemos y qué no por eje (cuenta parada NO en 1° y por qué; cursiva en el imprimible, dicho FUERTE; aviso ESI de C7 antes del llamado del lunes).
- **Modo "leéselo a alguien"** en L9, sin evaluación.
- L1 n1 / T7 básicas / C7 partes = diagnóstico exprés, se pasan rápido.
- Bancos chicos: subidos (L10 16, C2 16, T2 24, T5 16, T7 15, T9 16) o **ciclo corto declarado** (C5) — exactamente la alternativa que ella pidió ("o agrandan, o cambian la regla y lo dicen").
- Sesión de drill 6-8 min, 8-12 ítems, sin estirar.

### Del alumno (Benja) — incorporado
- **Robot con más niveles y predicción generada** (su queja #1: "lo terminé y no había más"). Simon con tope subido en Recreo; laberinto gana con 2 de 4 ("si mamá dice a bañarse en el tercero, perdí todo" — tenía razón).
- **Sopa sin diagonales ni reversas a los 6** ("eso es TRAMPA, no difícil" — es la misma conclusión del auditor curricular, dicha mejor).
- Capa de motivación completa: racha con mascota, **estrellas que compran cosas** (cosméticos y contenido, nunca saltear lo curricular), mapa con candaditos, elegir entre 3-4, **media medalla hoy / medalla mañana** (su objeción al sello de 2 días era válida: sin recompensa visible el día 1, el sistema se percibe como estafa), botón "mostrale a alguien", Recreo visible siempre.
- **Regla anti-reskin**: nunca dos canastas el mismo día; C9 cambió de mecánica (tap-zonas sobre plano). Detectó 7 canastas disfrazadas: era cierto.
- **Trabadas ahora, no en noviembre**; b/d con mucha práctica (es "su jefe final"); **biblioteca releíble** en L9 ("quiero releer el del perro de Ana": la relectura de textos conocidos construye fluidez — pedido pedagógicamente impecable).
- Dictados: cubierto con el **dictado con teclado** de L4.

### Del alumno — descartado (una línea cada uno)
- **Cursiva/trazado en tablet**: sigue fuera — exige canvas de dibujo libre y evaluación de trazo (otra inversión de motor); lo cubre el imprimible y la ficha lo dice fuerte.
- **Copiar del pizarrón**: fuera de alcance — escritura libre + memoria de trabajo no entran en el motor actual.
- **Cofre sorpresa diario**: no se implementan mecánicas de azar tipo loot en un producto infantil; la novedad diaria la dan la rotación de actividades y la estrella canjeable.

### Del auditor externo — incorporado (los 3 críticos, el presupuesto y la segunda línea)
- **Crítico 1 — Motor de dominio presupuestado** como ítem propio y mayor del esfuerzo (§6.D): telemetría por ítem, scheduler de espaciado, política de atraso, reporte, interleaving, diagnóstico persistente de errores.
- **Crítico 2 — Audio de fonemas**: ~30 fonemas por **grabación humana** (no TTS: a "d" le diría "de"), protocolo de QA fonético, cue silábico para oclusivas (no se pronuncian aisladas).
- **Crítico 3 — L2 rehecha**: banco unívoco de ~20 letras en modo fonema→letra; B/V, C/S/Z, C/K/Q, G/J, Y/LL y H pasan a modo contexto de palabra. El distractor J para /g/ se elimina (confusión ortográfica, no fonológica).
- Ventana reforzada para binarios (85% por sesión); **sello de L5 por tap-selección** (el memotest no mide dominio); **M3 con máx. 9 monedas de 1** y combinaciones que difieran en billetes; **L9: ítems con audio no computan al sello**; **secuencias: ítem = entrega completa**; M11 sin sí/no; T1-predicción con generador.
- Distractores corregidos: L1 PAN→PALO (contiene /l/ medial), M4 "baja la mitad"→"saltea al siguiente escrito", M13 con conflicto dibujo-vs-medida especificado al ilustrador, C7 sin relleno, L12 con canasta ACCIONES operativa, L3 conteo de letras reservado a palabras donde muerde (SOL), M2 estimación en bandas sin el valor exacto. **L1 con banco asimétrico documentado** (la matriz 12×3 era imposible: posición final solo admite /n/ /s/ /l/ /r/ /d/).
- **M7-concreto a B1** (el DC construye el cálculo desde los problemas, no al revés); **dictado con teclado** como techo de L4 (sin él, "escribe" era reconocimiento asistido todo el año); B4 descargado con ciclo corto por escrito; **"CPA" renombrado a pictórico** con puente concreto vía imprimible.
- Huérfanos resueltos (sopa→Recreo, puntos→Recreo renumerado, mas_menos→modo de M1); pista post-error no repesca la ventana; ventana cruza sesiones (definido); Recreo = 7 (número único, corregida la inconsistencia 4/5/6).
- Comercial: **desbloqueo híbrido** con adelanto acotado; **mapa del año** para adultos; **reporte de error conceptual** (el diferenciador que ningún competidor tiene); **Recreo gateado por dosis**; modo mezcladito. Claims: C6 sin prometer la sociedad de cada escuela, T4 con colores genéricos, kiosco "de juguete", C7 con comunicación ESI preparada.
- Audio recalculado: **~750 clips** (no 500) + fonemas humanos.
- Tap-zonas con **spec de geometría** previa (targets ≥48dp: oración partida en renglones con zoom por tramos, vértices magnificados) antes de estimarla.

### Del auditor — matizado (una línea)
- "El padre ve pocas actividades en marzo": resuelto con el mapa-del-año, pero **no** se acelera el drip — el menú corto a los 6 es decisión pedagógica (sobrecarga de elección), no contenido retaceado; el mapa lo hace visible sin romperlo.

---

## 6. Esfuerzo de construcción

### A. Curación (parámetros y flags sobre lo existente — días)
- `serie`→M4: pasos ±1/±10, tope 100, cruces forzados + **fix del bug invertido 6 vs 7-12**.
- `laberinto`: `tams:[6,7,8,9]` por edad + victoria con 2 de 4.
- `sopa`: pasar `edad` a `_sopa_json`, filtrar `_DIRS` (→ y ↓, 6×6, 4 palabras).
- `grilla100`→M1: distractores {invertido, ±1, ±10}; modos columna/parche/comparar.
- `suma_rapida`→M5: redondos-100 + contrarreloj B4 (timer existente).
- `puntos`: renumerar de 10 en 10 (Recreo).
- `mas_menos`: absorber como modo comparar de M1 (numerales 2 cifras, pares trampa).
- `bingo`→M9: cartón 4×4 real (fix `tam:9`).
- Flag "Recreo" (7 juegos) + gate por dosis; retiros de `_menu()` a los 6: contar, patron, agrupar, campo_ciudad, planta_fruto, abecedario; sudoku a 7+.
- Modo "voy con la seño" (config del adulto: letras enseñadas + tope numérico) como filtro de los bancos de L2/L4/L8 y M1/M9.

### B. Bancos nuevos sobre mecánica existente (~910 ítems a mano + 8 generadores + ~750 audios)
- **Tap-selección/trivia con distractores conceptuales**: L1, L2, L8, L9, L11, L13, M6, M7, M11, M12, C4, C8, T3, T5, T6, T7, T9.
- **Clasificar en canastas**: L12, C1, C3, C6, T4, T8 (regla reforzada de binarios; máx. una por día en el menú).
- **Ordenar secuencia** (entrega completa): L10, C5, C7-etapas, T2.
- **Slots + fichas con distractoras**: L3, L4, M8.
- **Cajero "tocar los que suman X"**: M3, M5-100.
- **Grilla**: M1 (modos nuevos), M14 (la grilla vestida de mes).
- **Programa Logo**: T1 (niveles nuevos).
- **Memotest**: L5 modo práctica (el sello va por tap-selección).
- **Bingo**: M9 (numerales + 100 audios).
- **Audio** (~750 clips): consignas + ítems ElevenLabs voseo (pipeline `generar_audio_consignas` existente) **+ ~30 fonemas por grabación humana con protocolo de QA fonético y cue silábico para oclusivas** — esto último es diseño de audio, no horas de TTS.
- Verificación: todo banco pasa QA de contenido (distractor = error conceptual documentado, cero ítems con doble respuesta válida) antes de entrar al scheduler.

### C. Mecánica nueva (2 primitivas + 3 modos)
1. **Tap-zonas sobre imagen/texto** (con spec de geometría ≥48dp: renglones con zoom, vértices magnificados): habilita L6, L7, M10, M11, C2, C7, C9 y enriquece M12 — la mejor inversión por ratio del mapa.
2. **Fase doble estimar→verificar** (wrapper sobre trivia; estimación en bandas): habilita M2 y M13.
3. **Modo predicción con generador** en programar_camino (programa aleatorio corto, verificación automática).
4. **Dictado con teclado completo** (suena la palabra, teclado de 27 letras, sin fichas): techo de L4 y extensión de vida de todo el banco de Lengua.
5. **Modo "leéselo a alguien"** en L9 (pantalla grande + registro del adulto, sin evaluación).

### D. Motor de dominio y capa de producto (NUEVO — el ítem más grande del presupuesto; era la omisión más cara del documento anterior)
- **Telemetría por ítem**: primer intento (marcado pre-pista), uso de audio, sesión, fecha.
- **Scheduler**: ventana móvil cross-sesión, sello a 2 días, repasos a 2 y 6 semanas con ítems no vistos, ciclo corto donde está declarado, bajada de andamiaje a las 4 sesiones, **modo mezcladito** post-sello, **diagnóstico persistente de errores** (si el patrón inversión-de-cifras o epéntesis reaparece, re-sirve esa familia de ítems — las plantillas de error dejan de ser solo distractores).
- **Menú**: 12-18 visibles, rotación bimestral, desbloqueo híbrido (adelanto máx. 1 bimestre por área), política de priorización ante atraso (núcleo obligatorio), regla anti-reskin, Recreo gateado, elección entre 3-4 diarias.
- **Capa adulto**: mapa del año (45 casilleros con contenido DC y estado), reporte 3 colores por eje + error conceptual en lenguaje llano, ficha para la familia (cuenta parada, cursiva, ESI, tachos), modo "voy con la seño".
- **Capa chico**: racha/mascota, estrellas canjeables, candaditos, media medalla/medalla, "mostrale a alguien", biblioteca releíble.

### Explícitamente FUERA de alcance (se declara en ficha, no se simula)
- Trazado de letras y cursiva con direccionalidad (canvas de dibujo libre) → kit imprimible.
- Cuerpos geométricos 3D manipulables → matching a objetos cotidianos (M12), que es como lo enseña el DC.
- Medición libre con regla (unidades convencionales) → M13 cubre lo no convencional; la regla física, al imprimible.
- Oralidad productiva (narrar/renarrar con la voz) → requeriría captura y evaluación de audio; L9/L10 cubren lo receptivo y el modo "leéselo a alguien" acompaña sin evaluar.
- Copia del pizarrón (escritura libre cronometrada).
