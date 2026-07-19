# Auditoría curricular y mapa de actividades 1°→7° — Cuaderno de actividades interactivo

**Contra el Diseño Curricular 2024 del Nivel Primario de la Ciudad de Buenos Aires** (el PDF que pasaste — 1er ciclo — más el de 2do ciclo de la misma fuente oficial, que hacía falta para llegar a 7°).

Fecha: 18-19 de julio de 2026. Método: 62 análisis independientes (11 extractores del DC por área, 7 inventarios del código real, 7 auditorías, 7 propuestas de diseño, 21 revisores en panel — maestra de CABA, alumno de la edad y auditor pedagógico externo por grado — y 2 síntesis globales).

---

## 0. Respuestas directas a lo que preguntaste

**"¿Las actividades de cada año son acordes al Diseño Curricular?"**
**No todavía.** Hoy un chico grande recibe casi el mismo menú que uno de 1°: de los 25 juegos que ve un chico de 6° grado, **17 son idénticos a los de 1° grado** (verificado en el código, `actividades_web.py`). El anclaje curricular real por grado hoy es: 1°≈ parcial, 2° 24%, 4° 5 de 25 juegos, 5° 8%, 6° ~12%. Por eso los chicos de 4° te dijeron "muy fácil": **tienen razón, y el dato está en el código**, no es percepción.

**"¿Cuántas actividades por año debería tener?"**
Entre **45 (1°) y ~70 (6°-7°)**, con esta curva: 1°→45, 2°→51, 3°→53, 4°→58, 5°→56, 6°→70, 7°→68. Pero el número que importa no es ese: es el **núcleo garantizado** de ~25-40 actividades por año que el chico **realmente domina**. El resto es exposición. (Detalle y por qué en §3.)

**"¿Cuántos ejercicios de cada temática para entender un contenido?"**
Para **entender de verdad** (llegar a dominio) un tema: **~3 a 5 sesiones de 8-10 rondas ≈ 30-50 ejercicios de ese tema**, servidos desde un **banco de 24-40 ítems distintos** (o un generador infinito para pura práctica: cuentas, ortografía, tablas). Menos de ~30 no fija; un banco fijo chico "se quema" en la segunda pasada y deja de enseñar.

**"Qué tipo de sumas según la edad, desde qué grado divisiones, así con todo."**
Esa es la matriz vertical de §1 — el corazón de este informe.

**"Quiero que se acerque a la perfección."**
El camino existe y está detallado grado por grado (7 dossiers anexos). Pero hay **una condición previa que vale para los 7 grados a la vez**: hoy el motor no verifica aprendizaje real (§4). Sin eso, todas las reglas pedagógicas son aspiracionales. Es lo primero a construir.

---

## 1. Matriz vertical — la progresión de cada contenido a lo largo de 1°→7°

Esta es tu pregunta literal ("qué sumas según la edad, desde qué grado divisiones"). Una fila por hilo curricular, una columna por grado. Sale del DC de CABA cruzado con la propuesta de diseño de cada grado.

### Matemática

| Hilo | 1° (6a) | 2° (7a) | 3° (8a) | 4° (9a) | 5° (10a) | 6° (11a) | 7° (12a) |
|---|---|---|---|---|---|---|---|
| **Numeración (hasta)** | 100 | 1.000 | 10.000 | 100.000 | 1.000.000 | sin tope | sist. numeración / sexagesimal |
| **Suma / resta** | ≤18, pictórico (concreto) | reagrupamiento hasta 1.000 | con llevada y préstamo a 10.000 | canje en cadena a 100.000 | dentro de racionales | con fracciones y decimales | integrado a potencias |
| **Multiplicación** | — | concepto de × (sumas repetidas) | tabla pitagórica completa | × por 2 cifras | repaso + propiedades | primos, permutaciones | potencias, × de fracciones |
| **División** | — | — | **reparto con resto** (arranca acá) | algoritmo "por partes" | por aproximaciones + divisibilidad | **por 2 cifras** (cuenta larga: c×d+r) | de racionales, ÷ de fracciones |
| **Fracciones** | — | — | — | **arranque** (reparto y medida) | equivalencias, suma-resta simple | suma-resta distinto denominador + producto | × y ÷ de fracciones |
| **Decimales** | — | — | — | primer contacto (dinero) | décimos/centésimos | operaciones | proporcionalidad, % |
| **Geometría** | formas básicas | figuras + atributos | cuerpos + desarrollos planos | ángulos + transportador (lectura) | construcciones + desigualdad triangular | polígonos, círculo | área/perímetro, cuerpos |
| **Medida** | comparar (largo/corto) | longitud no convencional | m/cm/mm, g/kg | + km, t (equivalencias) | profundiza equivalencias | sistema sexagesimal (tiempo/ángulo) | proporcionalidad de medidas |

### Lengua

| Hilo | 1° | 2° | 3° | 4° | 5° | 6° | 7° |
|---|---|---|---|---|---|---|---|
| **Comprensión (largo de texto)** | palabra → 4 oraciones | 60-100 palabras | 60-150 | 100-150 (inferencial) | 200-350 | ≥350 (*hoy 120-180 = regresión a corregir*) | 1-2 páginas |
| **Alfabetización / lectura** | fonética: letras unívocas, sílabas | palabras y oraciones | fluidez lectora | lectura de estudio | lectura crítica | subgéneros (CF, policial) | fantástico/terror, ensayo |
| **Acentuación** | (fonemas) | — | **introduce** agudas/graves/esdrújulas | + regla de tilde | tilde diacrítica | + hiato, adverbios en -mente | homófonos, integración |
| **Gramática** | — | separación de palabras | clases de palabra | **sujeto / predicado** | OD/OI (introduce) | OD/OI + transitividad | análisis completo con predicativo |
| **Conectores** | — | copulativos | + temporales | adversativos (y/o/pero ya sabidos) | causales | consecutivos/concesivos | integración argumentativa |
| **Producción escrita** | *(mayormente al imprimible)* | palabra/oración | oración/párrafo | párrafo | texto breve | texto estructurado | texto argumentativo |

### Ciencias (Conocimiento del Mundo 1°-3° → Naturales + Sociales 4°-7°)

| Hilo | 1° | 2° | 3° | 4° | 5° | 6° | 7° |
|---|---|---|---|---|---|---|---|
| **Historia argentina** | zonas / antes-hoy | roles y trabajos | comunidad / pasado cercano | originarios, conquista, colonia | 1806-1853 (independencia) | 1862-1930 (organización nacional) | s.XX: peronismo, 1976, democracia |
| **Estados de la materia** | sólido / líquido | (luz) | + gaseoso, cambios de estado | mezclas y separaciones | integrado | partículas y calor | — |
| **Astronomía** | día/noche | — | el cielo, el Sol | — | fases lunares, eclipses | modelo heliocéntrico | rotación/traslación, eclipses |
| **Cuerpo humano** | partes | cuidados | aparato digestivo | — | integrado (sistemas) | reproducción (ESI) | nervioso, inmune, célula |
| **Seres vivos** | animales/plantas | germinación | clasificación | ambientes | fotosíntesis | redes tróficas (roles) | ecosistema (construir la red) |

### Programación (Tecnología, Diseño y Programación)

| Hilo | 1° | 2° | 3° | 4° | 5° | 6° | 7° |
|---|---|---|---|---|---|---|---|
| **Pensamiento computacional** | secuencia (avanzar/girar) | **condicional** si/entonces | **bucle** repetir ×N + anidado | bucle + depuración | **variable** | eventos | paralelismo / integración |

> **Ojo con la matriz de programación:** hoy los dossiers re-presentan "repetir + depurar" como novedad en 3°, 4° **y** 5° (meseta). La columna de arriba es la línea **corregida** — un hito nuevo por año. Hay que asignar cada concepto a un solo grado.

---

## 2. Auditoría — estado actual grado por grado (veredicto duro)

| Grado | Juegos hoy en el menú | Con anclaje real al DC del grado | Diagnóstico central |
|---|---|---|---|
| **1°** | ~11-16 | parcial | Base de inicial razonable, pero mezclada; sobra "colorear/puntos" sin currículum |
| **2°** | 25 | 6 (24%) | Mayoría son binarios de inicial; falta multiplicación como concepto, comprensión real |
| **3°** | 25 | ~8 | Falta división (reparto con resto), tabla pitagórica, cuerpos; **bug real: `serie` invertida** (a los 6 años tope 30, a los mayores tope 16) |
| **4°** | 25 | **5** | 16 juegos son evergreen anclado en 1°/inicial; faltan mult/división, fracciones nodales, gramática. **Acá está la queja "muy fácil" — confirmada en código** |
| **5°** | 25 | **2 (8%)** | Techo aritmético en 16 contra un rango del millón; casi nada alineado |
| **6°** | 25 | 3 (~12%) | **17 de 25 juegos son idénticos a 1° grado** (`actividades_web.py` L318) |
| **7°** | 25 | pocos | Falta álgebra inicial, Inglés (no estaba ni en el catálogo), s.XX |

**Causa raíz común:** la banda de edad `"grande"` del motor es `edad ≥ 6 sin tope` — un chico de 12 recibe el mismo menú que uno de 6. **Hasta que no se abran bandas por grado, ningún contenido nuevo tiene forma de mostrarse solo a quien corresponde.** Es lo primero de lo primero.

---

## 3. Cuántas actividades y ejercicios por año (la dosificación)

| | 1° | 2° | 3° | 4° | 5° | 6° | 7° |
|---|---|---|---|---|---|---|---|
| **Actividades curriculares** | 45 | 51 | 53 | 58 | 56 | 70* | 68 |
| — Matemática | 14 | 18 | 18 | 19 | 18 | 23 | 16 |
| — Lengua | 13 | 19 | 17 | 17 | 16 | 16 | 15 |
| — Ciencias (Nat+Soc / CdM) | 9 | 7 | 10 | 16 | 17 | 21 | 20 |
| — Tec + Transversales (+Inglés en 7°) | 9 | 7 | 8 | 6 | 5 | 10 | 17 |
| **Núcleo garantizado (llega a dominio)** | ~20 | ~24 | 20 | 26 | 39 | ~40 | ~50 |
| **+ Juegos de recreo (sin sello curricular)** | 7 | 7 | 6 | 5 | 6 | 3 | 1 |

\* 6° está sobredimensionado (70) para el presupuesto de tiempo real de un año; hay que recortarle el núcleo a ~40 y mandar el resto a exposición, como hicieron 4°, 5° y 7°.

**Ítems por banco, según para qué sirve el juego:**
- **Drill de núcleo** (aritmética, ortografía, tablas): **generador paramétrico infinito** → imposible de memorizar.
- **Conceptual nodal de alto uso** (trivia/clasificar importante): **24-40 ítems** escritos a mano.
- **Exposición / menor uso**: **16-20 ítems**.
- **Techo epistémico** (hay 27 letras, 6 cuerpos geométricos, 8 planetas — la realidad fija el número): banco chico **declarado "de exposición"**, 1-2 visitas, sin certificado de dominio. Honesto, no se disimula.

**La regla única que justifica todos estos números:** el banco se dimensiona **desde el criterio de dominio**, no al revés. Dominio = ~85-90% al primer intento, sin pista, sostenido en 2 sesiones separadas ≥2 días + 1 repaso. Para certificar eso sin que el chico memorice el banco, cada ronda debe servir ítems **que no vio** → el banco tiene que ser **al menos 2× las rondas de una sesión**. Con rondas de 8-10, el piso es ~16-20, lo nodal 24-40, y lo drilleable se hace generador infinito.

**En una línea, para vos:** *apuntá a ~50 actividades por año, con un núcleo de ~30 que el chico realmente domina; cada tema se entiende con 3-5 sesiones (30-50 ejercicios) de un banco de 24-40 ítems, o de un generador infinito para lo que es pura práctica.*

---

## 4. La condición previa que vale para los 7 grados: el "motor de dominio" (Capa 0)

Este es el hallazgo de mayor impacto de toda la auditoría, y hay que decirlo una sola vez, fuerte: **el motor hoy no verifica que el chico aprenda.** Verificado en código (`actividades_player.js`) por el análisis de 6°:

1. **No hay compuerta de dominio:** `win()` se dispara por `ronda >= rondas`, no por acierto sostenido. Un chico "gana" por completar, aunque no haya entendido.
2. **No hay explicación del porqué:** hay 82 llamadas a la función de error (`casi()`), **ninguna** explica qué estuvo mal. Solo sacude.
3. **Los distractores paramétricos son al azar** (`rint()`), no errores conceptuales reales. Un juego con pocas opciones se gana por eliminación.

Las reglas pedagógicas que proponen los 7 dossiers (primer intento, sin pista, distractores por error real, repaso espaciado) **son aspiracionales hasta que se construya esta Capa 0.** Es **un solo desarrollo que desbloquea los 7 grados a la vez** — no siete. Va **antes** que el contenido nuevo: no tiene sentido escribir 6.000 ítems para un motor que no mide si se aprenden.

---

## 5. Quick wins — matar el "muy fácil" esta semana (curación de horas, no rebuild)

Antes de cualquier construcción grande, hay arreglos baratos y deployables ya, en toda la banda, que matan la vergüenza concreta que reportaron los chicos de 4°:

1. **Bug `serie` invertida:** a los 6 años el tope es 30, a los mayores 16. Está al revés. Fix de minutos.
2. **Retirar del menú de los grados grandes los ~10 juegos de inicial** (contar, más/menos, patrón, agrupar, colorear, puntos…) que hoy aparecen idénticos a los 6 y a los 12 años. Es curación de configuración, no código nuevo.
3. **Abrir bandas de edad por grado** en `actividades_web._banda()` (hoy "grande" = 6 sin tope). Sin esto nada nuevo se puede segmentar.

Estos tres, solos, ya cambian la percepción de "esto es para bebés" mientras se construye el resto.

---

## 6. Plan de construcción — cómo armarlo, en qué orden

**El volumen total honesto:** ~1.000 ítems por grado × 7 ≈ **6.000-7.000 ítems** a escribir y validar a mano, más ~15-20 mecánicas interactivas nuevas, más la Capa 0.

**Orden recomendado (MVP primero):**

1. **Capa 0 — motor de dominio** (compuerta de dominio, explicación del porqué, distractores por misconception, telemetría por ítem). Una vez, desbloquea todo.
2. **Quick wins** (§5) en paralelo — deployables ya.
3. **4° grado primero** como MVP de contenido: es donde está la queja viva y real. Probar el modelo completo (auditoría→propuesta→construcción→validación docente) en un grado antes de escalar.
4. **Bajar por vecindad:** 3° y 5° (comparten mecánicas con 4°), después 2° y 6°, después 1° y 7°.
5. **Pipeline de autoría:** decidir el modelo generar→revisar→cachear (como los audiolibros) vs. escritura 100% a mano, y **quién valida** (idealmente una docente real por grado — hoy el "panel" es simulado; la QA humana sigue pendiente y es condición para el claim de "excelencia").

**Catálogo de mecánicas interactivas nuevas** (lo que pediste como "propuestas para las interactivas"), reutilizables entre grados: barras de fracciones CPA, cajero/contador de billetes, tokens tocables, reloj con agujas arrastrables, plano cartesiano, árbol de probabilidad, chat ramificado, nodos-y-enlaces (redes tróficas), tap-zonas sobre lámina, estimar→verificar, repetir×N + depurador (programación). Cada una se construye una vez y sirve a varios grados.

---

## 7. Lo que queda honestamente afuera (y hay que comunicar al vender)

Escritura libre, cursiva, oralidad y lectura en voz alta quedan **fuera de lo digital** en todos los grados — el motor no corrige texto abierto ni evalúa voz. Eso lo completa el **cuaderno imprimible**. Hay que cuantificar qué fracción del DC cubre honestamente lo digital vs. el papel y decirlo de frente: es tu primer argumento de posicionamiento, no una debilidad a esconder.

---

## Anexos (documentos detallados, uno por grado)

Cada dossier tiene: auditoría juego por juego, mapa completo del año por área/eje con bancos y ejemplos de ítems con sus distractores, qué mantener/endurecer/retirar/mover, progresión por bimestre, lo que dijo el panel y qué se ajustó, y el esfuerzo de construcción.

- `grado-1.md` … `grado-7.md` — dossiers por grado
- `dosificacion-global.md` — coherencia vertical y modelo de dosificación (fuente de §1 y §3)
- `faltantes.md` — crítica de completitud (qué revisar antes de dar por cerrado)
