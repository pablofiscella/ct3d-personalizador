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

---

## 5. Contenido de 1° a 3°: qué está cargado y qué falta (y por qué)

El catálogo (`actividades_curriculum.py`) tiene **17 actividades / 221 ítems**, todas con
su contenido del DC y el documento del que salieron. Pero la auditoría especifica **51
actividades sólo para 2°**, y hay dos bloqueos suyos que impiden cargar la mayoría:

### Bloqueo A — 11 actividades de 2° son PARAMÉTRICAS

La auditoría las define como *"ítems infinitos desde plantillas con rangos por nivel y
guardas de colisión obligatorias"*. No son bancos: son generadores. El catálogo hoy sólo
emite mecánicas de banco (trivia, clasificar, ordenar).

Falta una mecánica `parametrica` que declare plantilla + rangos + guardas. Es además la
que resuelve de raíz la memorización (ver punto 2), así que es el mismo trabajo.

Afecta: M1 serie con saltos, M3 formá 100/1.000, M4 cálculo redondo, M5 suma paso a paso,
M6 ¿cuál es mayor?, M7 bingo numérico, M11 tabla proporcional, M13 doble o mitad, y las
equivalentes de 1° y 3°.

### Bloqueo B — el contenido insignia de 2° EXIGE AUDIO

Regla NRP, textual de la auditoría: *"Todas las actividades de sistema de escritura son
fonética CON AUDIO; dependen de `generar_audio_consignas`; **sin ese audio NO se
publican**"*.

Eso incluye lo que la propia auditoría llama el contenido insignia del grado y su gap más
grave: **dígrafos (ll, ch, qu, gu, rr) y opacidades ortográficas (b/v, s/c/z, y/ll, g/j)**.
Cargarlas como trivia de texto sería publicar algo que enseña mal — el chico elegiría por
cómo se ve la palabra escrita, que es justo lo contrario de lo que la actividad mide.

Afecta: L1 fichas de sonido, L2 ¿con cuál va?, L3 suena fuerte/suave, L4 detective mb/nv/h,
L19 palabras bien separadas.

### Tamaño de banco

La auditoría fija para 2° **mínimo 30 ítems, 40 los insignia**. Los bancos cargados van
entre **14 y 16**: son válidos y jugables (el validador exige 12), pero por debajo de ese
estándar. Agrandarlos es data entry sobre el catálogo, sin tocar código.

### Orden sugerido

1. Mecánica `parametrica` → destraba 11 actividades de 2° y ataca la memorización.
2. Audio de consignas → destraba las 5 de sistema de escritura, el gap más grave del grado.
3. Engrosar los bancos cargados de 14-16 a 30.
