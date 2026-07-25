# El motor de aprendizaje — qué toma de ALEKS y de DreamBox, y qué es propio

Este documento explica **por qué el motor hace lo que hace**. La investigación que lo
originó (4 informes comparando ALEKS, DreamBox, Khan e IXL) coincidió en un híbrido:
ALEKS aporta la **estructura** (qué se puede aprender ahora) y DreamBox el **proceso**
(cómo lo está resolviendo). Lo que sigue es qué quedó implementado de cada uno, con la
decisión de diseño que hubo detrás — que suele ser más importante que el código.

> Estado al 25-jul-2026. Todo está gateado por `adaptativo_on` en el `data.json` del
> token: un link vendido sin ese flag se comporta exactamente como antes.

---

## De ALEKS — la estructura

### Grafo de saberes con prerrequisitos

`saberes.py` (153 saberes, 1° a 7°). Cada saber declara sus prerrequisitos y los juegos
que lo miden. `motor_adaptativo.js` lo recibe generado (`gen_motor_adaptativo.py`).

El concepto que se tomó es el **outer fringe**: lo que el chico está listo para aprender
es lo que todavía no sabe pero cuyos prerrequisitos ya cumplió. Eso es lo que se marca
`✨ Recomendado`.

**Nada se bloquea nunca.** Es la regla de oro, y viene de un problema real: las
actividades de mitad de año en adelante, que el chico no vio en la escuela, lo trababan.
Un saber sin prerrequisitos cumplidos se muestra como `🌱 Reforzá antes`, no con candado.

### Nivelación inicial (el sondeo)

ALEKS abre con un diagnóstico que ubica al alumno. Sin eso, todos arrancan de cero aunque
ya sepan, y el motor le hace perder el tiempo al que ya sabe.

La primera vez que entra un perfil (`Sondeo` en `actividades_player.js`), se le ofrecen
**una actividad corta por materia**, de dificultad media-alta. Si le sale bien, se dan por
sabidos ese saber **y sus prerrequisitos** — la inferencia de ALEKS: no se resuelve lo de
arriba sin lo de abajo. En la prueba, 4 preguntas ubicaron 11 saberes.

**Tres decisiones que hacen que esto no rompa nada:**

1. **`ubicado` NO es `dominado`.** Dominado es evidencia sostenida en días distintos: es
   lo que ve el padre en su tablero y lo que dispara la oferta de la materia. Ubicado sólo
   dice por dónde empezar. Si compartieran campo, tres respuestas bien contarían como
   dominio y estaríamos cobrando con evidencia falsa. Hay un test que verifica que ubicar
   el grado **entero** no mueve un solo número del panel de padres.
2. **No puntúa.** Cero estrellas, cero sellos, cero festejo. El chico no está siendo
   evaluado: es el motor averiguando por dónde empezar.
3. **Se puede saltear.** Un chico que no quiere no tiene que pasar por un examen para
   usar su cuaderno.

### Aprendido vs. consolidado

`Store.registrarDominio` marca `dominado` recién cuando el chico resolvió con nivel de
dominio en **dos días distintos**, y `consolidado` cuando además pasó un repaso posterior.
Es la distinción *learned vs. mastered* de ALEKS, y es lo que evita que el mail al padre y
la oferta de la materia salgan por un falso positivo.

---

## De DreamBox — el proceso

### Dificultad que escala con el dominio

`ctx.bonusDominio` (bonus por dominio, **sin** piso de edad — para juegos que ya traen su
nivel por edad en `cfg.nivel`, no duplica) y `ctx.nivelDif` (piso por edad + niveles
ganados). Quien domina una actividad la vuelve a abrir más difícil: `multiplicar` pasa de
`35 × 10` en frío a `67 × 9` al dominarla.

**131 de 176 juegos escalan.** Los que no, en general no tienen gradiente real (un juego
de un solo concepto, como "¿conduce o no conduce?"): ahí la adaptación la da el grafo, no
la dificultad interna. No se fuerza una dificultad falsa.

### Telemetría de proceso

El resultado solo no distingue **"lo sabe"** de **"acertó tanteando"**. Cada primer intento
registra, además de acierto y tipo de error:

| campo | qué es | para qué |
|---|---|---|
| `ms1` | ms hasta el primer toque | tardar mucho = no entendió la **consigna** (≠ contenido difícil) |
| `ms` | ms hasta responder | cuánto le costó resolver |
| `toq` | toques antes de responder | muchos toques + acierto = probó hasta que salió |

Se sanean en el servidor: el player corre en el dispositivo del chico, así que nada de lo
que manda es confiable.

### El informe que la lee

`telemetria_informe.py` agrega la telemetría de **todos** los cuadernos. Existe porque el
dato se venía escribiendo desde el 19-jul y no lo leía nadie.

La distinción que lo hace útil: **"consigna confusa"** (mala precisión + mucho tiempo
hasta el primer toque) se arregla redactando; **"contenido difícil"** (mala precisión pero
responde rápido) se arregla bajando la dificultad. Confundirlas hace perder el tiempo.

```
python3 telemetria_informe.py                 # todos
python3 telemetria_informe.py --grado 4       # un grado
python3 telemetria_informe.py --json          # para procesar
```

No reporta actividades con menos de 5 primeros intentos: dos respuestas no son un dato.

### Instrucción explícita — el botón "¿Cómo es?"

DreamBox combina descubrimiento guiado **con** instrucción explícita. Nosotros sólo
explicábamos cuando el chico **erraba**, o sea que para entender la regla había que
equivocarse primero.

`COMO_ES` tiene **63 mini-lecciones** (regla + ejemplo trabajado), disponibles siempre y
leídas en voz alta. Sólo llevan entrada las actividades que enseñan una **regla**: las que
evalúan un dato no, porque un botón que dice obviedades enseña a ignorar el botón.

Es texto y no video a propósito: un video por actividad son 149 videos que producir,
versionar y servir. Si un tema puntual amerita video, se le agrega a **esa** entrada sin
cambiar el mecanismo.

---

## Lo propio — lo que ninguno de los dos tiene

### Modo Profe: crear y corregir, no sólo resolver

- **Modo Creador** — el chico *inventa*: una cuenta que dé un número objetivo, o una
  oración armada con fichas (con concordancia de número validada de verdad).
- **Modo Maestro** — el chico *corrige al robot*: una cuenta mal resuelta, o una oración
  mal escrita, y se le explica **cuál era la regla** que el robot violó.

Sin teclado, siempre: se elige entre fichas. Si no, se convierte en un ejercicio de tipeo.

### Anti-memorización por diseño

De 176 juegos, **111 generan** el ejercicio en vez de sacarlo de una lista. El criterio:

- **Con regla → se genera.** `valor_posicional` pasó de 14 preguntas fijas a 242 ítems
  computados. Guarda importante: se descartan las ambiguas ("en 121, ¿cuánto vale el 1?"
  tiene dos respuestas), porque un ítem ambiguo le enseña al chico que la regla no cierra.
- **Factual → no se puede.** Fotosíntesis, historia, comprensión lectora: la respuesta es
  un dato y la única salida es más ítems.

**Regla que costó aprender:** la variedad va **completa desde el arranque**; el dominio
sólo empuja hacia lo difícil. Dos veces se ató la variedad al bonus por dominio y el
resultado fue un chico nuevo viendo siempre los mismos 3 casos.

### Informe para la maestra

`/act/<token>/informe` (y `/mi-cuenta/informe/<token>` desde la cuenta del padre): salida
imprimible en lenguaje curricular — nombre del saber y eje del DC, no "tablas ninja: 3
estrellas", que a una maestra no le dice nada.

Es una **salida, no una integración**: la genera la familia y la lleva. La escuela no tiene
cuenta ni carga nada. La dirección fue explícita: el producto no debe depender de que la
maestra haga algo, porque eso sería otro "trabado".

Distingue dominado de trabajado. Decirle a una maestra que un chico domina algo porque
acertó una vez es la forma más rápida de que no vuelva a leer el informe.

---

## Qué falta

- **Bancos factuales**: ~6-7k ítems según la auditoría del DC. Es volumen de autoría, no
  código. Ver `FEATURES-PENDIENTES.md` §2.
- **Convertir a generador** los juegos con regla que siguen con ítem fijo (de los 65 que
  quedan, una parte tiene regla).
- **Video real** para algún concepto puntual, si se decide que la mini-lección de texto no
  alcanza.
- **Leer la telemetría del piloto.** El agregador está; lo que falta es el dato, y lo
  generan los chicos.
