# Fase 0B — Capa 0: motor de dominio (spec técnico)

> Especificación concreta contra el código real de `actividades_player.js`. Es el prerequisito de todo el contenido nuevo (ver `PLAN-CONSTRUCCION.md`): sin esto, ninguna actividad mide si el chico aprende, y todas las reglas de los dossiers quedan aspiracionales.

## Hallazgo que abarata todo: hay un solo cuello de botella

Los ~80 juegos NO tocan la lógica de acierto/error directamente. Todos pasan por **una única fábrica de contexto**, `Shell.ctx(item)` (`actividades_player.js:307-344`), que les da cinco funciones:

- `ctx.rondas(n)` / `ctx.ronda(i)` — progreso (los puntitos).
- `ctx.bien(txt)` — acierto: toast de festejo (`:331`).
- `ctx.casi()` — error: hace `self.fallos++` y un sonido (`:332`). **No recibe qué ítem era, ni por qué estuvo mal.**
- `ctx.win(estrellas)` — completado: estrellas = 3 si `fallos===0`, 2 si `<=2`, 1 si más (`:333-341`). Lo dispara el juego cuando `ronda >= rondas`.

**Consecuencia:** la compuerta de dominio, la telemetría y el andamiaje se construyen **una sola vez, acá**, y funcionan para todos los juegos sin tocarlos uno por uno. Lo único que sí necesita datos por-ítem (y por eso se hace junto con la autoría de contenido, no acá) son la explicación del error y los distractores por misconception.

## Estado actual verificado (los 3 huecos)

1. **`win()` premia completar, no dominar** (`:333-335`). Se dispara por `ronda >= rondas` en cada juego (ej. `:1147`, `:1225`). Las estrellas miran `self.fallos` acumulado, pero un chico puede llegar a `fallos<=2` **acertando por eliminación** o **eventualmente** — no hay noción de "acertó al primer intento".
2. **`casi()` no explica nada** (`:332`). Solo suma un fallo y suena. La regla pedagógica "todo error dispara el porqué" no tiene dónde vivir.
3. **Distractores al azar.** En los generadores paramétricos las opciones incorrectas salen de `rint()` (ej. serie `:5748` `seq[falta] + rint(-3,3)`) — no representan un error conceptual real.

## Los 5 componentes a construir

### C1 · Registro de primer intento (la base de todo)

Hoy `fallos` es un contador plano. Se necesita, por ronda: **¿acertó al PRIMER intento, sin pista?** Cambio en `ctx` (central):

- Al empezar cada ronda el juego declara el ítem: `ctx.item(itemId)` (nuevo, opcional; si no se llama, se usa un id sintético `juego#ronda`).
- `ctx.bien()` y `ctx.casi()` ya saben en qué ítem están → registran `{itemId, primerIntento: (esta es la 1ª respuesta de la ronda), correcto}`.
- Se expone `self.aciertosPrimerIntento` además de `self.fallos`.

Sin tocar los juegos: `bien`/`casi` ya se llaman en todos; solo se les agrega el registro. `ctx.item()` es aditivo (los juegos que no lo llaman siguen andando).

### C2 · Compuerta de dominio (redefinir `win`)

Separar **dos estados** que hoy están fundidos:

- **Completado** (lo que ya existe): terminó las rondas → festejo. Se mantiene, no se rompe la sensación de logro.
- **Dominado** (nuevo): alcanzó el criterio ÚNICO del proyecto — *≤1 error en una ventana de 8-10 ítems, al primer intento, sin pista, sostenido en 2 sesiones separadas ≥2 días + 1 repaso espaciado* (ver `dosificacion-global.md` §3.1; es la única definición aritméticamente correcta de las 5 que traían los dossiers).

`win()` pasa a calcular estrellas desde **aciertos al primer intento**, no desde `fallos` totales. El sello de "dominado" (que habilita el diploma / marca el tema como cerrado) se otorga solo cuando se cumple el criterio de ventana sostenido — se guarda en `Store` (que ya persiste progreso, `:160`).

### C3 · Explicación del porqué (extender `casi`)

`ctx.casi(motivo)` acepta un string opcional y lo renderiza (una frase a los 6-7, más detalle desde los 8). El motivo viene del ítem:
- Bancos escritos a mano: cada ítem trae su campo `porque` (lo produce el pipeline de autoría, `PLAN-CONSTRUCCION.md`).
- Generadores paramétricos: una función `motivo(a, b, elegido)` por juego (ej. en resta: "te olvidaste de pedir prestado").
- Fallback si no hay motivo: el comportamiento actual (solo sacude), para no bloquear el rollout — pero se loguea como "sin_motivo" para saber qué falta.

### C4 · Distractores por misconception

Reemplazar el `rint()` de las opciones incorrectas por el error típico real:
- Bancos: los distractores ya vienen etiquetados por misconception desde la autoría.
- Generadores: una función `distractores(correcto, contexto)` por familia de juego que produce los errores clásicos (resta sin pedir prestado, confundir decena/unidad, etc.) en vez de ruido aleatorio.

### C5 · Telemetría por ítem

En `ctx` (central), cada `{itemId, juego, edad, primerIntento, correcto, conPista}` se acumula y se manda al motor (endpoint nuevo `POST /act/<token>/telemetria`, batch, sin bloquear el juego). Con esto **vemos con datos** qué actividad quedó muy fácil (≈100% al primer intento) o muy difícil (baja tasa) — la respuesta con evidencia a "algunas son muy fáciles", de acá en adelante, y el insumo para calibrar cada grado tras publicarlo (paso 6 del loop por grado).

## Orden de construcción de la Capa 0

1. **C1 + C5 primero (telemetría de primer intento).** Es aditivo, no cambia ninguna mecánica, y empieza a juntar datos ya — incluso sirve para medir el efecto de la Fase 0A. Bajo riesgo.
2. **C2 (compuerta de dominio).** Cambia el significado de las estrellas y agrega el sello "dominado". Verificar en vivo que ningún juego rompa (todos pasan por `win`).
3. **C3 + C4 (explicación + distractores).** Van de la mano con la autoría de contenido: se activan por ítem a medida que los bancos traen `porque` y distractores etiquetados. Fallback seguro mientras tanto.

## Qué NO es la Capa 0 (límites)

- No reescribe los juegos. Los cambios son en `ctx` (central) + datos por-ítem (autoría).
- No incluye el contenido nuevo de cada grado (eso es Fase 1-7).
- El repaso espaciado (la cola de repaso entre sesiones) es parte de C2 pero puede ir en una segunda pasada si aprieta el tiempo — el criterio de dominio "en 2 sesiones" ya lo deja preparado.

## Verificación esperada

- C1/C5: abrir un token, jugar, confirmar que la telemetría registra primer-intento correcto/incorrecto por ítem (Playwright + inspección del endpoint).
- C2: un juego "ganado por eliminación" (respondiendo cualquier cosa hasta acertar) NO debe otorgar el sello "dominado"; uno jugado bien al primer intento, sí.
- C3: forzar un error en un ítem con `porque` y confirmar que se muestra la explicación.
- Tests guardián nuevos para la lógica de ventana de dominio (es lógica pura, testeable sin browser).
