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

## Estado al 25-jul-2026

| Grado | Manifiesto | Cobertura |
|---|---|---|
| 4° | sí | **58/58** — 1 deuda (S8: faltan las 24 capitales y las 5 regiones) |
| 1°, 2°, 3°, 5°, 6°, 7° | **no** | sin auditar contra su `grado-N.md`; el test los saltea |

Para cada grado que sigue: paso 1 y listo, el informe dice el resto.
