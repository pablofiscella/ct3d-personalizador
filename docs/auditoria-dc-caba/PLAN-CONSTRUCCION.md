# Plan de construcción — actividades año tras año

> Plan de ejecución para llevar el cuaderno de actividades interactivo a estar alineado al Diseño Curricular de CABA en los 7 grados. Deriva de la auditoría (`README.md` + dossiers por grado). Es el "cómo lo hacemos", no el "qué falta".

## Decisiones tomadas (Pablo, 19-jul-2026)

1. **Arrancamos por las fundaciones**, no por contenido: quick wins + Capa 0 (motor de dominio) antes de construir actividades nuevas. Razón: los quick wins matan la queja "muy fácil" esta semana, y sin Capa 0 cualquier contenido nuevo no mide si el chico aprende.
2. **Autoría AI-asistida con revisión**: un skill genera borradores de ítems y distractores → Claude los cura contra las reglas pedagógicas → se cachean (mismo modelo que los audiolibros: generar → revisar → cachear → reusar). La **validación docente real** queda como capa final por grado, cuando Pablo consiga la docente.

---

## Fase 0 — Fundaciones (una sola vez, desbloquea los 7 grados)

### 0A · Quick wins — deployables esta semana (curación, no rebuild)

Van primero porque bajan la vergüenza del "muy fácil" ya, con horas de trabajo.

| # | Qué | Dónde (a confirmar en código) | Esfuerzo |
|---|---|---|---|
| 1 | **Bug `serie` invertida** — a los 6 años tope 30, a los mayores 16 (está al revés) | generador de `serie` en `actividades_web.py` / player | minutos |
| 2 | **Retirar del menú de los grandes los ~10 juegos de inicial** (contar, mas_menos, patron, agrupar, colorear, puntos…) que hoy aparecen idénticos a los 6 y a los 12 | `actividades_web._menu()` / `_banda()` | horas (config) |
| 3 | **Abrir bandas de edad por grado** — hoy `"grande"` = `edad >= 6 sin tope`; sin esto nada nuevo se segmenta | `actividades_web._banda()` | horas |

> **La #3 es prerequisito de todo lo demás.** Bandas objetivo: 1°, 2°, 3°, 4°, 5°, 6°, 7° por separado (o pares donde el contenido no difiera). Al abrirlas, revisar que cada juego existente quede asignado a la(s) banda(s) que le corresponde por el dossier — no dejar herencia silenciosa de la banda vieja.

### 0B · Capa 0 — el motor de dominio (el trabajo grande de esta fase)

Es lo que hoy NO existe y hace que todas las reglas pedagógicas de los dossiers sean aspiracionales. Se construye una vez y sirve a los 7 grados. Cinco componentes:

1. **Compuerta de dominio.** Hoy `win()` se dispara por `ronda >= rondas`. Cambiar a: se "aprueba" un contenido cuando el chico alcanza el criterio de dominio (abajo) sobre **ítems que no vio antes**. Completar deja de ser sinónimo de aprobar.
2. **Explicación del porqué en el error.** Hoy hay 82 llamadas a `casi()` y ninguna explica nada. Extender `casi()` para recibir y mostrar una razón corta por ítem (una frase a los 6-7 años, más detalle desde los 8). Requiere que cada ítem del banco cargue su explicación → lo genera el pipeline de autoría.
3. **Distractores por misconception.** Hoy los distractores paramétricos son `rint()` al azar. Reemplazar por: cada ítem trae sus distractores etiquetados con el error conceptual real que representan (ej. resta sin pedir prestado). Para los generadores infinitos, una función de "error típico" en vez de random.
4. **Telemetría por ítem.** Registrar acierto/error al **primer intento** por ítem, por token. Esto es lo que nos deja **ver con datos** qué actividad quedó muy fácil o muy difícil — la respuesta con evidencia a "algunas son muy fáciles", de acá en adelante.
5. **Repaso espaciado.** Cola de repaso por ítem para que el dominio se sostenga en el tiempo (no se certifica un tema en una sola sesión).

**Definición ÚNICA de "dominio"** (la síntesis global encontró 5 definiciones distintas en los dossiers — se unifica en esta, que es la única aritméticamente correcta): *≤1 error en una ventana de 8-10 ítems, al primer intento, sin pista, sostenido en 2 sesiones separadas ≥2 días + 1 repaso espaciado.* La pista, si se usa, deja el ítem fuera del cómputo de dominio.

---

## El loop repetible por grado (Fases 1-7)

Una vez listas las fundaciones, cada grado se construye con el mismo proceso — este es el "cómo armamos cada año". Se apoya en la skill `actividades-progresivas` (reglas no negociables) y en el dossier ya escrito de ese grado.

1. **Partir del dossier del grado** (`grado-N.md`) + la sección del DC. El diseño ya está hecho: qué actividades, qué bancos, qué mantener/endurecer/retirar/mover.
2. **Confirmar la banda** (abierta en Fase 0A#3) y aplicar los movimientos de catálogo del dossier (retirar/mover juegos).
3. **Por cada actividad del núcleo:**
   - ¿La mecánica existe? → construir la nueva o endurecer la existente con los parámetros exactos del dossier.
   - ¿El banco? → generar con el **pipeline de autoría** (abajo), revisar, cachear.
   - Aplicar reglas de la skill: CPA en matemática, fonética + audio en lengua para chicos, distractores por error real, andamiaje gradual, cero fail states.
4. **Verificar en vivo** (Playwright headless, como todo el motor) + un test guardián por tipo nuevo.
5. **Deployar**: branch propio → PR → merge (con confirmación de Pablo por PR) → restart de `ct3d-kit.service` chequeando `activos==0` antes.
6. **Medir 1-2 semanas con la telemetría de la Capa 0** → ajustar dificultad con datos reales, no a ojo.
7. **Validación docente** de ese grado (capa final, cuando esté la docente) antes de dar el grado por "de excelencia".

### Pipeline de autoría AI-asistido (la fábrica de ítems)

El cuello de botella real son ~6.000-7.000 ítems. El pipeline:

1. **Skill generador** (nuevo, o extensión de `actividades-progresivas`): dado (grado, juego, contenido DC, cantidad), produce N ítems con enunciado, respuesta correcta, **distractores etiquetados por misconception**, **explicación del porqué**, y nivel de dificultad.
2. **Revisión (Claude)**: cada tanda se cura contra las reglas — distractor conceptual real (no genérico), dificultad acorde al grado, sin ambigüedad, sin "detalle seductor". Lo dudoso se descarta o reescribe.
3. **Cacheo**: los ítems aprobados se guardan en el formato de banco del juego (JSON), versionados en el repo.
4. **Validación docente** (capa final por grado): revisión humana ítem por ítem antes de publicar el grado. Es la condición del claim "excelencia".

> Regla heredada del rollout NAP: **cada error encontrado → regla nueva en la skill.** El generador mejora tanda a tanda; el objetivo es que converja a generar ítems correctos casi solos.

---

## Orden de grados y por qué

Después de las fundaciones, por **vecindad de mecánicas** (cada grado reusa lo construido en el anterior):

1. **4° grado** — es donde está la queja viva y real; grado modelo del proceso completo.
2. **3° y 5°** — comparten mecánicas con 4° (fracciones, división, comprensión).
3. **2° y 6°** — 6° hay que recortarlo a un núcleo de ~40 (hoy sobredimensionado a 70).
4. **1° y 7°** — 1° es más curación (base de inicial ya existe); 7° suma Inglés y álgebra inicial.

## Dosificación objetivo (recordatorio, del informe)

- **~45 (1°) a ~70 (6°-7°) actividades por grado**, con **núcleo garantizado de ~25-40** que el chico realmente domina.
- **Para entender un tema: 30-50 ejercicios** (3-5 sesiones × 8-10 rondas), de un **banco de 24-40 ítems** — o **generador infinito** para drill puro (cuentas, ortografía, tablas).
- Regla que fija los números: **el banco se dimensiona desde el criterio de dominio (banco ≥ 2× rondas de una sesión).**

## Definición de "grado terminado" (Definition of Done)

Un grado está "de excelencia" cuando: (a) su menú refleja el mapa del dossier (movimientos de catálogo aplicados); (b) todas las actividades del núcleo tienen banco lleno con distractores por misconception y explicación del porqué; (c) pasan por la compuerta de dominio real (Capa 0); (d) verificado en vivo + tests guardián; (e) telemetría muestra la curva de dificultad esperada (ni piso ni techo); (f) validado por una docente del grado.

## Riesgos y cómo los manejamos

- **Ítems generados con IA de calidad dudosa** → doble filtro (revisión Claude + validación docente); regla nueva a la skill por cada error.
- **Sobredimensionar** (construir 70 actividades que nadie termina) → foco en el **núcleo** primero; el resto es exposición, se agrega si hay tiempo.
- **Romper links ya vendidos** → el player se sirve del repo, las mejoras llegan a todos; verificar siempre en vivo, no solo en worktree fresco (el cache en disco difiere).
- **Restart mata jobs** → nunca reiniciar `ct3d-kit.service` sin chequear `activos==0` en `/dash/ia-estado`.

---

**Próximo paso concreto sugerido:** arrancar la Fase 0A (los 3 quick wins) en un worktree, verificarlos en vivo y abrir PR — es lo más barato y lo que más rápido cambia la percepción. En paralelo, especificar la Capa 0 al detalle (los 5 componentes contra el código real de `actividades_player.js`).
