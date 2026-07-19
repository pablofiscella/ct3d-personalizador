# Qué falta / qué quedó flojo — crítica de completitud

Los 7 dossiers por grado son sólidos y profundos **dentro de cada grado**. El problema es que el pedido del dueño es en buena parte **vertical y transversal**, y eso casi no está resuelto. Su ejemplo textual ("qué tipo de sumas según la edad, desde qué grado divisiones, así con todo") es una pregunta de progresión entre grados, y hoy no hay un solo lugar que la conteste. Lista priorizada.

---

## P0 — Bloqueantes: lo que el dueño pidió y NO está

### 1. Falta el documento de dosificación vertical (`dosificacion-global.md` no existe)
Es el gap #1 y es exactamente su pregunta de ejemplo. No hay ninguna vista que diga, en una tabla, la progresión de un contenido a lo largo de 1°→7°:
- **Sumas:** 1° ≤10 pictórico / 2° hasta 1.000 / 3° con llevada hasta 10.000 / 4° 4-5 cifras / 5°-7° …
- **Divisiones:** ¿desde qué grado? (arrancan como reparto con resto en 3°, algoritmo por partes en 4°, por aproximaciones en 5°, dos cifras en 6°, racionales en 7°) — hoy hay que reconstruirlo leyendo 7 archivos.
- Ídem fracciones, decimales, lectura/comprensión, acentuación/ortografía, geometría, programación.
**Acción:** construir la matriz "contenido × grado" (una fila por hilo curricular, una columna por grado) que muestre el salto de dificultad año a año. Es el entregable que responde su ejemplo literal y hoy no existe.

### 2. No hay tabla consolidada de "cuántas actividades por año" ni justificación de la curva
Él preguntó explícitamente "cuántas actividades por año debería tener". La respuesta existe por grado pero dispersa y **no comparable**: 1°=45(+7), 2°=51, 3°=53, 4°=58, 5°=56, 6°=70(+3), 7°=68. Va a preguntar: **¿por qué 1° tiene 45 y 6° tiene 70? ¿esa curva es intencional o es deriva entre análisis independientes?** Además cada grado usa una taxonomía distinta (Recreo / núcleo-extendido / Tier A-B-C / Capa 0…): imposible comparar de un vistazo.
**Acción:** una tabla única de las 7 columnas con total, núcleo vs. extendido bajo **un solo esquema**, e ítems por año; más un párrafo que justifique la progresión de volumen.

### 3. No se verificó la propuesta contra el DC que ÉL entregó
Los dossiers citan "DC CABA 2024" e indicadores, pero **no hay trazabilidad al PDF que entregó** (página/sección). Varios grados dejan "verificar cada cita al DC contra el documento real" como TODO pendiente, y 7° admite que Inglés "no estaba en la auditoría original". Va a preguntar: **¿esto sale de MI diseño curricular o de lo que el modelo sabe de CABA?** Sin esa validación, el claim "acorde al DC" no está probado.
**Acción:** cruzar cada área/grado contra el documento entregado y citar; marcar lo que el modelo agregó por criterio propio (p. ej. Inglés).

---

## P1 — La primera tanda de preguntas obvias al leer

### 4. No hay plan de construcción total (tiempo, costo, orden, MVP)
Pidió "cómo debería armarlo" y está contestado **por grado**, nunca en total. Faltan los números que él necesita para decidir: **~1.000 ítems × 7 grados ≈ 6.000-7.000 ítems** a escribir y validar, ¿en cuántos meses?, ¿quién los escribe?, ¿qué grado se construye primero?, ¿cuál es el MVP vendible? Dado que la queja viva es de 4°, ¿se arranca por 4°?
**Acción:** roadmap único con orden de grados, esfuerzo total, y definición de MVP.

### 5. El motor es UNO solo para los 7 grados y no está consolidado
Es la misma app Flask / `actividades_player.js` / `actividades_web.py`. El "motor de dominio + Capa 0" (compuerta de dominio, distractores por misconception, render del porqué, repaso espaciado, telemetría) se construye **una vez y desbloquea los 7 grados**, pero está descrito 7 veces con distinto nivel de detalle (6° lo hace bloqueante y verificado en código; 1°-3° lo mencionan al pasar). Va a preguntar: **¿es un motor o siete? ¿cuánto sale? ¿va antes que el contenido?**
**Acción:** una sección única "motor compartido" con alcance, costo y la regla de que va primero.

### 6. No se separan los arreglos baratos ("muy fácil" se mata mañana) del rebuild grande
El bug de `serie` invertida (a los 6 tope 30, a los mayores tope 16) y el retiro de los ~10 juegos de inicial del menú de cada grado son **curación de horas** y matan hoy la vergüenza de "muy fácil" — que es la queja concreta de los chicos de 4°. Están dentro de cada "esfuerzo" pero nunca juntados como **"quick wins deployables ya, en toda la banda"**.
**Acción:** lista corta de curaciones baratas transversales, deployables antes que nada.

### 7. "Dominio" está definido de 5 formas distintas para un motor único
1°: 85% primer intento, ventana 10, 2 sesiones. 2°: ≤1 error en 8-10. 3°: 85% últimas 10. 4°: 9/10 primeras exposiciones. 5°: ventana fija estratificada. Cada grado "corrige" al anterior. Si el motor es uno, la regla debe ser **una**.
**Acción:** reconciliar en una definición única (o justificar por qué varía por edad).

---

## P2 — Completitud y confianza (afectan el claim de "excelencia/perfección")

### 8. No hay matriz de cobertura DC→actividad (solo "top-5 gaps")
Cada grado lista los 5 gaps más graves y un "fuera de alcance", pero **no un checklist exhaustivo** que muestre, contenido por contenido del DC, si está cubierto / no / fuera de alcance. Él pidió "revisar si las actividades son acordes al DC… así con todo": quiere el crosswalk completo, no el resumen. Sin él no puede confiar en que no se saltó nada.

### 9. "Fuera de alcance" es grande, se repite y no está cuantificado ni ligado al imprimible
Escritura, cursiva, oral y lectura en voz alta quedan fuera en TODOS los grados, derivadas al "cuaderno imprimible". Nadie dice **qué fracción del DC cubre honestamente lo digital** (¿media Lengua queda afuera?) ni cómo el imprimible completa el resto. Pablo **vende** esto: es su primera pregunta de marketing/posicionamiento.

### 10. Las mecánicas interactivas nuevas están fragmentadas (él pidió "propuestas para las interactivas")
Las primitivas nuevas (tap-zonas, estimar→verificar, cajero, tokens, reloj con arrastre, plano cartesiano, árbol de probabilidad, chat ramificado, nodos-enlaces, barras CPA…) están dispersas por grado. Falta **un catálogo único de mecánicas nuevas** con costo y qué grados desbloquea cada una — que es justo la info de mayor apalancamiento y la que él pidió por nombre.

### 11. El "panel" (maestra/alumno/auditor) parece simulado; la QA docente real sigue pendiente
Todo el peso de "excelencia" descansa en las tres devoluciones del panel, que salvo aviso son **personas simuladas**. Varios grados dejan "validación humana ítem por ítem, no opcional" como TODO. Hay que decir explícito que la revisión real de docentes de cada grado **todavía no se hizo** — es condición para "acercarse a la perfección".

### 12. No hay pipeline de autoría de los ~7.000 ítems
Es el verdadero cuello de botella. ¿Se generan con un skill y se revisan a mano (modelo generar→revisar→cachear de los audiolibros) o se escriben todos a mano? ¿Quién los valida (¿7 docentes, uno por grado?)? Sin esto, el plan no es ejecutable.

---

## P3 — Menores pero van a surgir
- **13.** Trazar qué actividades **específicas** jugaron los chicos de 4° y confirmaron "fáciles", y si esas ya quedaron endurecidas (hoy está inferido, no verificado con ellos).
- **14.** Falta un **ejemplo visual** de una actividad endurecida (Pablo es visual: preview real, no descripción en texto) para "ver" a qué apunta la propuesta.
