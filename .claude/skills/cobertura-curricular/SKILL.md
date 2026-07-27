---
name: cobertura-curricular
description: Procedimiento OBLIGATORIO para dar de alta o completar un grado escolar (1° a 7°) en actividades-web. Primero se enumeran los temas del Diseño Curricular, después se construye lo que falta, y recién ahí se toca dificultad o precio. Usar SIEMPRE que se pida "completar N° grado", "agregar actividades a un grado", "revisar si falta contenido", o antes de poner un grado a la venta.
---

# Cobertura curricular por grado — el procedimiento

**Regla única, y es la que manda sobre todo lo demás:**

> Todo tema del Diseño Curricular del grado tiene que tener una actividad, y esa
> actividad tiene que estar en el **nivel 1** — el que el chico ve sin pagar ni
> desbloquear nada.

Los niveles 2 y 3 son escalones de **dificultad del mismo tema**, gratis, que se abren
solos cuando el chico domina. **No son contenido distinto y no son un candado.** Si un
tema del año está en el nivel 2, está mal: bajalo al 1.

## Por qué existe esta skill

25-jul-2026. El cuaderno escolar de 4° tenía 42 tarjetas y se veía completo. Cruzado
contra la currícula cubría **29 de los 58 temas** del año: Ciencias Naturales tenía UNA
actividad de ocho, las tres transversales no existían, y diez de los temas que sí
existían estaban detrás del candado de los niveles 2 y 3 — un chico con `nivel_max: 1`
no llegaba nunca a la comprensión lectora ni a los ángulos, que son contenido de 4°.

Pablo lo dijo así: *"Primero quiero que abarques todos los temas de la curricula. Esto
tiene que estar bien claro para crear después los distintos grados."*

Nada de eso fallaba en ningún test. Por eso ahora hay un manifiesto y un test.

## Los tres archivos

| Archivo | Qué es |
|---|---|
| `docs/auditoria-dc-caba/grado-N.md` | **La fuente autorizada.** Auditoría contra el DC CABA 2024 + panel docente: qué temas tiene el año, con qué mecánica, qué banco y qué rampa de dificultad. |
| `actividades_cobertura.py` | **El manifiesto.** Un renglón por tema del DC, con qué actividad lo cubre. Es lo que hace verificable la regla. |
| `tests/test_cobertura_dc.py` | **El guardián.** Falla si un tema no tiene actividad, si la actividad no llega al menú, o si quedó en un nivel con candado. |

## El procedimiento, en orden

### 1. Enumerar los temas del DC — ANTES de escribir nada

Leé `docs/auditoria-dc-caba/grado-N.md`, sección "Mapa propuesto del año". Trae la
cuenta cerrada (para 4°: **58 curriculares + 5 comodines**) y las tablas por área con
un código por tema (M1…, L1…, N1…, S1…, T1…, X1…).

**Los comodines lúdicos NO cuentan.** Memotest, laberinto, sopa, sudoku, simón,
patrón, agrupar, qué falta y bingo van *arriba* de los temas curriculares: son descanso.
Contarlos infla el número y tapa el agujero — fue exactamente lo que pasó en 4°.

### 2. Escribir el manifiesto

Agregá `GRADO_N` a `actividades_cobertura.py`, un dict por tema:

```python
{"cod": "N3", "area": "naturales", "tema": "Huellas del tiempo",
 "dc": "Fósiles; escala de tiempo geológico frente a la humana",
 "cubre": "fosiles_4"},          # o None si todavía no existe
```

`cubre` puede ser una lista si el tema se reparte en varias tarjetas. Si está cubierto
pero incompleto, sumá `"deuda": "qué le falta"` — queda registrado sin bloquear.

Registralo en `DC = {...}` y sumá a `EXTRAS_OK[N]` los ids que están en el menú a
propósito sin ser currícula del año (comodines y repasos de otro grado).

### 3. Correr el informe y dejar que él dicte la lista de trabajo

```bash
python3 -c "import actividades_cobertura as c; c.informe(4)"
```

Sale la cuenta por área, los `FALTA`, los `DEUDA` y los `ROTO` (declarado pero ausente
del menú, o con candado). **Esa es la lista de trabajo. No la estimes a ojo.**

### 4. Construir lo que falta — una actividad = una entrada de datos

No se escribe JavaScript. Se agrega una entrada a `CATALOGO` en
`actividades_curriculum.py` y `gen_curriculum.py` emite el `.js`.

Mecánicas disponibles: `trivia`, `clasificar`, `ordenar`, `parametrica`.

```python
{
    "id": "fosiles_4", "grado": 4, "area": "naturales",
    "titulo": "Huellas del tiempo", "icono": "🦴",
    "mecanica": "ordenar",
    "consigna": "Ordená del MÁS ANTIGUO al MÁS NUEVO. Tocá en orden.",
    "explica": "Lo de abajo se depositó primero: es lo más viejo.",
    "dc": "Fósiles; escala de tiempo geológico",
    "fuente": "docs/auditoria-dc-caba/grado-4.md · N3",
    "saber": {"id": "NAT-4-fosiles", "nombre": "Fósiles y tiempo geológico",
              "prereqs": ["NAT-4-erosion"]},
    "banco": [...],
}
```

El `saber` engancha solo al grafo adaptativo (`saberes.py` lee el catálogo). Los
`prereqs` tienen que existir, en el catálogo o en el grafo grande.

Reglas de contenido que el validador exige y conviene entender:

- **Trivia:** `ops[0]` es la correcta (el player baraja). Mínimo 3 opciones, sin
  repetidas, sin consignas repetidas dentro del banco. `m` es la explicación que ve el
  chico **al errar**: tiene que nombrar el error conceptual, no repetir la respuesta.
- **Clasificar:** de 2 a 4 categorías, todas con al menos un ítem. Una categoría sin
  ítems es un botón que nunca es correcto y se aprende a descartar.
- **Ordenar:** mínimo 8 secuencias de 3+ tarjetas, sin secuencias repetidas.
- **Paramétrica:** sin banco; se valida **simulando 400 tiradas**. Necesita ≥300
  válidas y ≥20 ejercicios distintos, o el generador no evita la memorización.
- **Banco mínimo 12 ítems** (8 secuencias en `ordenar`). Con menos se agota en una
  partida y mide memoria en vez de aprendizaje — ver [[ct3d-memorizacion-bancos]].
- **Los distractores modelan el error real**, no son números al azar. Si el tema tiene
  un error clásico documentado en la auditoría, ese error es una opción. Ejemplos que
  ya están: `34.000.507` (escribir el número como se dice), `4-5-9` en triángulos (la
  suma de los cortos IGUALA al largo y no cierra), `a - b + 10` (quedarse con el canje).

### 4-bis. Construir de a tandas, commiteando cada una

Un grado son 45-70 actividades y **no entran en una sentada**. La construcción se hace
por tandas —normalmente un área por tanda— y **cada tanda se commitea y pushea**.

Apenas escribís el manifiesto, sumá el grado a `EN_CONSTRUCCION` en
`actividades_cobertura.py`:

```python
EN_CONSTRUCCION = {5}
```

Con eso, los temas que todavía no construiste **no rompen la suite** — pero un id
inexistente o una actividad con candado siguen fallando. Sin esta compuerta, declarar el
manifiesto pone la suite en rojo por 50 temas pendientes y ya no se puede commitear nada
hasta terminar el grado entero, que es exactamente lo que hay que evitar.

El ciclo por tanda:

```bash
# escribir las N actividades del área
python3 gen_curriculum.py && python3 gen_motor_adaptativo.py
python3 -m pytest tests/test_cobertura_dc.py tests/test_actividades_curriculum.py -q
git add -A && git commit -m "feat(escolar): N° — <área> (X de Y temas)" && git push
```

**Por qué importa:** si se corta la sesión, se acaba el crédito o se cae la corrida, lo
único que se pierde es la tanda en curso. Todo lo anterior está pusheado, validado y
verde, y la rama se retoma desde ahí sin rehacer nada. El motor tampoco se rompe nunca en
el medio: un grado a medio construir es un grado con menos actividades, todas
funcionando.

Cuando el informe da 0 FALTA, **sacá el grado de `EN_CONSTRUCCION`** y corré la suite: ahí
recién se exige completo. Ese es el commit que cierra el grado.

### 5. Verificar

```bash
python3 gen_curriculum.py                                    # regenera el .js
python3 -c "import actividades_cobertura as c; c.informe(4)" # 0 FALTA, 0 ROTO
python3 -m pytest tests/test_cobertura_dc.py -q
```

**Mirarlo en el producto, no en la carpeta.** El `.py` validado y el `.js` regenerado no
prueban que el chico lo vea: abrí el cuaderno del grado y contá las tarjetas. Es la regla
de [[ct3d-contenido-cargado-sin-enchufar]] — las 7 portadas de grado vivieron un día
enteras en el repo sin que ningún código las leyera.

### 6. Recién ahora, dificultad

Con la currícula completa y abierta, el escalón de dificultad va **adentro** de cada
actividad, con `ctx.bonusDominio` en `actividades_player.js`. La auditoría ya especificó
tres escalones por tema en la columna "Dificultad" de cada tabla (por ejemplo, división:
`cocientes de tabla → 2 cifras ÷ 1 → 3 ÷ 2`). No hay que inventarlos.

## Lo que NO se hace

- **No se gatea contenido del año detrás de `nivel_max`.** `_NIVEL_ACTIVIDAD` en
  `actividades_web.py` está vacío a propósito y debe seguir vacío para los temas del
  grado en curso.
- **No se cuentan los comodines lúdicos como cobertura.**
- **No se declara un tema "cubierto" por una actividad parecida de otro grado.** Si el
  banco no da para lo que pide el DC, va con `deuda` o se construye.
- **No se pone un grado a la venta con `FALTA` en el informe.**

## Contenido que pide revisión docente

Hay temas que se pueden escribir bien y aun así no deberían salir sin que los mire una
persona: **Ciencias Sociales** (afirmaciones históricas) y **ESI**. Ningún test valida
que una interpretación histórica sea justa.

Al escribirlos, dos reglas que ya vienen de las auditorías:

- **No fijar tesis historiográficas discutidas como si fueran hechos.** Por eso 5° tiene
  la categoría "antecedente, no causa directa" (la Revolución Francesa influyó, pero no
  causó la Revolución de Mayo) y 4° trata a los indígenas bajo encomienda y a las
  personas africanas esclavizadas como estratos con estatus legal **distinto**.
- **Nombrar lo incompleto.** La libertad de vientres fue un avance real Y no abolió la
  esclavitud: las dos cosas son ciertas y el ítem lo dice.

Pendiente de revisión: los 5 temas de Sociales de 5° y los de 4° que la auditoría marcó
con "revisión docente externa obligatoria".

## Estado al 26-jul-2026

| Grado | Manifiesto | Cobertura | Deudas |
|---|---|---|---|
| 1° | sí | **45/45** | 0 |
| 2° | sí | **53/53** | 0 |
| 3° | sí | **53/53** | 0 |
| 4° | sí | **58/58** | 0 |
| 5° | sí | **56/56** | 0 |
| 6° | sí | **70/70** | 0 |
| 7° | sí | **68/68** | 0 |

**Los siete grados están cerrados: 403 temas del DC, 0 deudas, todos en nivel 1.**
`EN_CONSTRUCCION` está vacío, así que el guardián falla si cualquier grado pierde un
tema. Toda actividad que enseña una regla tiene además su mini-lección; las 8 que no la
tienen son enumeración de datos, a propósito.

**INGLÉS se resolvió mapeándolo al carril de Lengua** (26-jul). El menú tiene seis
carriles y están fijos: abrir un séptimo cambiaría la pantalla de categorías de los
siete grados por tres actividades de uno solo. El área real del DC quedó escrita en el
campo `dc`, así que la decisión es reversible si algún día se justifica el carril.

**Revisión docente pendiente** (ningún test la reemplaza): los 5 temas de Sociales de
5°, los de 4° marcados en su auditoría, de 6° el bloque entero de Sociales (S1-S9) más
el de ESI (N4, N5, N6, Tr1, Tr2), y de 7° el bloque de dictadura y memoria (CS1, CS2,
CS3, CS6) más el de ESI (CN11, X1, X2). La auditoría pide además que el producto
**avise a la familia** antes de que el chico se encuentre con el bloque ESI: eso
todavía no está hecho.

**Sobre el contenido sensible, dos criterios que ya están aplicados y conviene sostener:**

- **La dictadura y el terrorismo de Estado se escriben con los hechos que NO están en
  disputa** —plan sistemático, desaparición forzada, centros clandestinos, apropiación
  de bebés, la CONADEP, el Juicio a las Juntas, la imprescriptibilidad— y **ninguna
  cifra discutida se convierte en ítem de opción múltiple.**
- **Grooming y consumo problemático se escriben como contenido de PROTECCIÓN**:
  reconocer la señal, que la culpa nunca es del chico, y la vía de denuncia real. Nunca
  describiendo cómo se comete.

### Lo que se aprendió construyendo 6° y 7°

- **El evaluador de plantillas sólo admite `+ - * / ( )`.** Sin condicionales, sin
  potencias, sin `%`. Las guardas van en el DISEÑO de los rangos: si el total es
  múltiplo de 120 y el denominador divide siempre, el resultado cae entero solo. Un
  `ok` con ternario devuelve 0 de 400 tiradas válidas y el juego se queda sin ejercicios.
- **Antes de escribir, buscá si el grado ya tiene actividades.** 6° tenía cuatro, y tres
  cubrían su tema a medias (pronombres sin indefinidos, conectores sin locativos). Se
  reemplazan conservando el mismo `saber`, así el grafo adaptativo no se mueve.
- **Las fracciones y los decimales no se parametrizan**: se escriben como texto y el
  evaluador sólo hace aritmética con enteros. Esos temas van con banco fijo, grande.
- **`ordenar` necesita 8 secuencias DISTINTAS.** Para un proceso de etapas fijas (las 5
  del diseño), la variedad sale de cambiar el PROYECTO, no las etapas: nueve problemas
  distintos recorridos por las mismas cinco etapas.
- **Una consigna repetida dentro del banco falla.** «¿Cuál está bien escrita?» nueve
  veces no pasa el validador: cada ítem pide su propia pregunta.
- **Un distractor que COINCIDE con la respuesta se descarta**, y si quedan menos de dos
  la tirada entera se tira. En 7° el distractor `a / 10` era el resultado mismo cuando
  el porcentaje valía 10, y un `tope` corto mataba otro: la paramétrica bajó de 400
  tiradas válidas a 221 sin ningún error visible. Si el validador se queja de "las
  guardas descartan casi todo", el problema casi siempre son los distractores, no la
  fórmula.
- **Los `saber` no pueden repetirse en todo el catálogo**, ni siquiera entre grados
  distintos. `SOC-7-democracia` chocaba con una actividad vieja del mismo grado.
- **El guardián de video se parametriza por EDAD.** Al cerrar un grado hay que sumar su
  edad a `test_toda_explicacion_tiene_video`, o las mini-lecciones nuevas quedan sin
  vigilar. Hacerlo destapó, en 6° y en 7°, mini-lecciones viejas sin video que nadie
  había declarado nunca.

Para cada grado que sigue: paso 1 y listo, el informe dice el resto.
