# Actividades escolares — features pedidas y pendientes

Ideas pedidas por Pablo que **todavía no están construidas**, con el estado real de cada
una. Vive en el repo a propósito: hasta ahora quedaban sólo en notas de sesión y no había
dónde mirarlas.

> Lo que ya está construido no va acá — se documenta en `docs/ACTIVIDADES-WEB.md` y en los
> PRs. Esta lista es para lo que falta.

---

## 1. Botón "¿Cómo es?" — video / mini-lección del concepto

**Pedido de Pablo (24-jul-2026):** en las actividades que enseñan una REGLA —acentuación
(aguda / grave / esdrújula) y por extensión cualquier saber conceptual— tener **siempre**
disponible un botón con un video corto o mini-lección que explique cuál es cuál.
Textual: *"Me gustaría ver cómo podemos hacer eso."*

**Por qué importa:** hoy el player explica **sólo cuando el chico ERRA**
(`ctx.casi(motivo)` → `mostrarExplicacion`, animación + voz). O sea, para entender la regla
hay que equivocarse primero. Un explicador siempre disponible es "instrucción explícita"
además de "descubrimiento guiado" — es lo que hace DreamBox, y sería un diferencial.

**Decisión pendiente:** video real (mp4 servido, pesado, tipo Remotion) vs. animación o
láminas dentro del player (liviano, generado). Ver la regla Pillow-vs-Remotion que ya se
usó para el video del audiolibro.

**Estado:** anotado, nada implementado.

---

## 2. Contenido GENERADO en vez de bancos fijos (anti-memorización)

**Pedido de Pablo (24-jul-2026):** *"no quiero que aprenda por memoria sino porque
entendió el saber"*.

**El problema, medido en el código:** de los 116 juegos del grafo, **37 generan** el
ejercicio cada vez (números nuevos — casi todos de Matemática) pero **66 tienen el ítem
fijo** de una lista, y los bancos tienen **20 ítems de mediana** mientras una partida usa
8-10. Jugando dos veces ya vio el banco entero: a partir de ahí lo que se mide es memoria,
no comprensión.

**Por qué agrandar los bancos NO alcanza:** con 40 ítems se memoriza igual, sólo que más
tarde, y son ~6-7k ítems de escritura (auditoría DC). El arreglo de fondo es **generar el
ejercicio desde la regla**, como ya hace Matemática.

- **Se puede generar** el contenido basado en REGLAS: acentuación, plurales, prefijos,
  sujeto/predicado, y varios de Mate que hoy están fijos.
- **No se puede** el contenido FACTUAL (fotosíntesis, historia, comprensión lectora): ahí
  la respuesta es un dato y la única salida es más ítems.

**Conecta con la venta:** vender "la misma actividad más difícil" sólo tiene sentido si el
contenido no es memorizable. Si no, son las mismas 10 preguntas con otro nombre.

**Estado:** EN CURSO — arrancando por Matemática (decisión de Pablo). `angulos` ya
convertido a generador.

---

## 3. Escalera de compra del "nivel siguiente"

**Pregunta de Pablo (24-jul-2026):** ¿se puede seguir comprando indefinidamente o son unos
pocos niveles?

**Estado real medido:** hoy son **4 compras como máximo** (una por materia) y es un límite
accidental de la tabla (`PRIMARY KEY (email, token, materia)`), no una decisión de
producto. Si fuera escalera grado a grado, el techo lo pone el contenido: termina en 7°, o
sea 12 compras para un chico de 4° y 24 para uno de 1°. **Infinito no puede ser.**

**Los dos bloqueos antes de cobrar:**
1. **El desbloqueo no entrega nada.** Se lee en un solo lugar —el tablero, para cambiar el
   botón por "✅ desbloqueado"—; el motor ni se entera de que existe.
2. **El contenido está desparejo.** Lengua de 6° tiene **1 solo juego**. Cobrar $2000 por
   "el nivel siguiente de Lengua" entregaría una actividad.

**Precio definido (provisorio):** $4000 de lista con 50% off de lanzamiento → $2000.
Configurable en `actividades_materia_precio` / `actividades_materia_descuento`.

**Estado:** el cobro real de Mercado Pago sigue sin enchufar (botón "próximamente"), a
propósito, hasta que haya qué entregar.

---

## 4. Emparejar el contenido por materia y grado

Juegos por grado y materia (los que entregaría un desbloqueo):

| grado | Lengua | Matemática | Naturales | Sociales |
|------:|-------:|-----------:|----------:|---------:|
| 1° | 3 | 3 | 3 | 1 |
| 2° | 4 | 7 | 3 | 0 |
| 3° | 5 | 9 | 5 | 0 |
| 4° | 10 | 15 | 2 | 3 |
| 5° | 3 | 9 | 3 | 5 |
| 6° | **1** | 10 | 4 | 3 |
| 7° | 3 | 7 | 4 | 1 |

Sociales en 2° y 3° está en **cero** y Lengua de 6° en **uno**. Mientras siga así, esas
combinaciones no se pueden vender ni recomendar en serio.

**Estado:** pendiente. Es contenido, no código.
