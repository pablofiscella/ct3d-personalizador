---
name: actividades-progresivas
description: Reglas para diseñar/agregar actividades educativas alineadas al currículum NAP argentino y a metodologías de aprendizaje evidence-based, para cualquier edad de 4 a 12 años. Usar SIEMPRE al agregar un tipo de actividad nuevo a cuaderno.py/actividades_web.py/actividades_player.js, al extender bandas de edad, o al diseñar el feature "Modo Maestra / Mamá ocupada" (packs por minutos).
---

# Actividades progresivas por edad — reglas de CT3D

Motor en `/root/ct3d-personalizador`. Insumo curricular en
`docs/CURRICULUM-NAP-ARGENTINA.md` (el currículum NAP que Pablo pasó, año por
año, bimestre por bimestre). Diagnóstico completo del estado actual del motor
en `docs/INFORME-ACTIVIDADES-PROGRESIVAS.md` — leerlo ANTES de tocar código,
tiene el gap-analysis real (qué existe, qué falta, por qué).

**GOAL vigente: cubrir de forma curricularmente sólida los 9 años de
escolaridad (Sala de 4 a 7° grado), en orden, empezando por 4 años (pedido
explícito de Pablo, 14-jul-2026).** Cada año nuevo que se agregue = una
entrada nueva en la tabla de la sección 4, no una excepción suelta.

## 0. Estado real al 14-jul-2026 (no asumir, releer el informe si pasó tiempo)

El motor cubre razonablemente Nivel Inicial + 1°/2° grado (4 a 7 años). **De
3° grado en adelante (8 a 12 años) no existe NINGÚN tipo de actividad** — ni
multiplicación, ni fracciones, ni geometría, ni lectoescritura real
(sílabas/sintaxis/comprensión), ni ciencias naturales o sociales
curriculares. Verificado por grep exhaustivo en `cuaderno.py`,
`actividades_web.py`, `actividades_player.js` — no volver a asumir cobertura
que no está confirmada en código.

La banda de edad `"grande"` de `actividades_web._banda()` es `edad >= 6 SIN
TOPE` — un chico de 12 años recibe el mismo menú que uno de 6. Al construir
contenido para 3°+ grado, esto TIENE que resolverse primero (agregar bandas
nuevas: 1°-2°, 3°-4°, 5°-6°, 7°), si no el contenido nuevo no tiene forma de
mostrarse solo a quien corresponde.

## 1. El orden de trabajo importa — no saltear pasos

1. **4-7 años (Sala 4 a 2° grado): CURACIÓN, no construcción.** El motor ya
   tiene los 23 tipos de `cuaderno.py` — el trabajo es elegir/etiquetar cuáles
   sirven para cada eje NAP y ampliar rangos donde el techo actual quede corto
   (ej. `_a_sumas` hoy resuelve ~7-8 aunque la UI diga `max=10`; 1° grado NAP
   pide hasta 100).
2. **8-12 años (3° a 7° grado): CONSTRUCCIÓN DE CERO.** Necesitan tipos de
   actividad que hoy no existen (tabla pitagórica interactiva, fracciones con
   apoyo visual, geometría, ciencias). No hay atajo: no está "casi hecho",
   está "sin empezar" — presupuestar el esfuerzo en consecuencia.
3. **Un año a la vez, validado antes de seguir al siguiente.** No diseñar 3°
   a 7° grado en un solo sprint especulativo — el patrón de este repo
   (armar-kit, armar-audiolibros) es generar → revisar con datos reales →
   recién ahí escalar al siguiente.

## 2. Principios pedagógicos NO NEGOCIABLES (evidencia real, no gusto propio)

Investigado 14-jul-2026 contra fuentes de consenso amplio (Piaget,
Vygotsky/ZPD, National Reading Panel 2000, enfoque Singapore Math CPA,
estudios de atención sostenida por edad) — ver el informe para el detalle y
las fuentes completas.

1. **Antes de los 7 años: todo manipulable visualmente, sin texto de
   instrucciones largo, sin lógica de más de 1-2 pasos.** Es la fortaleza
   actual del motor — no romperla al escalar a más edades.
2. **De 7 a 11 años: lógica sobre lo concreto, siempre con apoyo gráfico.**
   Recién a los 11-12 se puede pedir abstracción pura (símbolos sin dibujo).
   Cualquier actividad de fracciones/decimales para 3°-5° grado necesita
   representación visual (tiras, tramos, dibujos) ANTES del símbolo — nunca
   arrancar directo con la ecuación.
3. **Matemática nueva = Concreto → Pictórico → Abstracto**, siempre en ese
   orden (Singapore Math, validado internacionalmente). Objetos primero,
   dibujos/barras después, símbolo solo al final.
4. **Alfabetización = fonética sistemática, no reconocimiento visual de
   palabras** (evidencia sólida, National Reading Panel). Secuencia:
   conciencia fonológica ORAL (rimas, sonidos aislados) → combinar sonidos →
   sílabas escritas → palabras → oraciones. El motor hoy NO tiene componente
   de AUDIO en ningún juego de lengua — cualquier actividad de alfabetización
   nueva necesita sonido, no solo imagen (hueco de mecánica, no solo de
   contenido).
5. **Andamiaje gradual, no constante.** El sistema de "pistas" debe dar ayuda
   fuerte en el primer error, más sutil en el segundo, y retirarse si el
   chico acierta seguido — nunca la misma ayuda siempre (Vygotsky/ZPD). Si un
   juego nuevo tiene pistas, implementar la gradación desde el diseño, no
   como mejora posterior.
6. **CERO fail states sigue siendo la regla, con más razón en chicos
   chicos** — está respaldado por investigación real (la "confusión
   productiva" motiva, la "confusión desesperanzada" hace abandonar; los
   chicos tienen menos estrategias emocionales que un adulto para tolerar el
   fracaso). El error sacude suave y deja seguir — SIEMPRE, en cualquier
   actividad nueva de cualquier edad.

## 3. Tabla de dosificación — "Modo Maestra / Mamá ocupada" (packs por minutos)

Base directa para el feature "necesito 30 minutos de actividades para tal
edad" (roadmap 14-jul-2026). NO improvisar la mezcla — usar esta tabla:

| Edad/grado | Atención por actividad | Actividades distintas en 30 min | Andamiaje |
|---|---|---|---|
| 4-5 años (inicial) | 8-12 min | 3-4 actividades cortas y variadas | Pista visual fuerte y constante |
| 6-7 años (1°-2°) | 12-15 min | 2-3 actividades | Pista fuerte → se retira si acierta 2 veces seguidas |
| 8-9 años (3°-4°) | 15-20 min | 2 actividades + 1 repaso corto | Pista solo a pedido (botón "ayuda") |
| 10-11 años (5°-6°) | 20-25 min | 1-2 actividades profundas | Pista mínima; el feedback explica el POR QUÉ, no solo "mal" |
| 12 años (7°) | 25-30 min | 1 actividad larga o 2 medianas | Casi sin andamiaje, autonomía |

## 4. Roadmap — actualizar esta tabla a medida que se avanza (no dejarla vieja)

| Orden | Edad/grado | Estado (14-jul-2026) | Tipo de trabajo |
|---|---|---|---|
| 1 | Sala de 4 años | ✅ Shippeado 14-jul-2026 (ver informe §5b): mejoras + juego nuevo + audio-guía + auditoría visual, todo hecho. Falta: `posicion` en el cuaderno impreso | Curación (bajo esfuerzo) |
| 2 | Sala de 5 años | ✅ Shippeado 14-jul-2026 (ver informe §5c): rango de `contar`/`mas_menos` ampliado + juego nuevo `silabas` (primer juego de audio real del motor) + QA de duración de TTS. Falta: vocales/consonantes/rimas/escritura (quedan para 1° grado) | Curación (matemática) + construcción (audio/fonética) |
| 3 | 1° grado | ✅ Cerrado 14-jul-2026 (ver informe §5d-§5e): un juego por cada "Idea web" del NAP en los 4 bimestres (7 juegos nuevos/curados). Falta a propósito: "la tiendita" con dinero + contenido sin "Idea web" propia (ciencias, escuela/barrio, efemérides) — pasada aparte, no deuda | Curación (matemática) + construcción (audio/fonética/clasificación) |
| 4 | 2° grado | ✅ Cerrado 14-jul-2026 (ver informe §5f): 8 juegos nuevos, uno por "Idea web" del NAP en los 4 bimestres — incluye `tablas_contrarreloj`, primera mecánica de TIMER del motor. No hizo falta banda propia: `if e == 7` alcanza | Curación (matemática) + construcción (clasificación/timer) |
| 5 | 3° grado | ✅ Cerrado 14-jul-2026 (ver informe §5g): 8 juegos, uno por "Idea web" del NAP — 6 reusaron patrones de 1°/2° grado, solo 2 necesitaron forma nueva. Cuerpos geométricos simplificado (sin rotación 3D real, el motor no tiene render 3D) | Construcción (reusa patrones ya probados donde se puede) |
| 6 | 4° grado | ✅ Cerrado 14-jul-2026 (ver informe §5h): 8 juegos, uno por "Idea web" del NAP. PRIMERA representación visual de fracciones del motor (barras CPA) — bug real de CSS (width:100% dentro de un `<button>` shrink-to-fit) encontrado y arreglado en vivo. Mapa de provincias y transportador simplificados a trivia (assets/mecánicas que el motor no tiene) | Construcción (fracciones CPA, primer render visual nuevo) |
| 7 | 5° grado | ✅ Cerrado 14-jul-2026 (ver informe §5i): 8 juegos, uno por "Idea web" del NAP. SEGUNDA mecánica de timer (`analisis_sintactico`). 0 simplificaciones a trivia por falta de asset — primer año sin ninguna | Construcción (reusa patrones probados, decimales sin bugs de punto flotante) |
| 8 | 6° grado | ✅ Cerrado 14-jul-2026 (ver informe §5j): 8 juegos, uno por "Idea web" del NAP. 3 simplificaciones de simulación a contenido directo (el año con más de todos) — cada una con su propia razón, no una regla genérica | Construcción (reusa patrones probados) |
| 9 | 7° grado | Desglose disponible en el currículum — fin del NAP (año de egreso) | Construcción (álgebra informal, sistema solar, geopolítica) |

## 4b. Diseño gráfico no negociable (investigado 14-jul-2026, evidencia real)

Pablo: *"quiero que sea lo más serio posible... no solo las actividades sino
la gráfica y estética que acompañe... los chicos tienen que aprender de
verdad."* No es gusto estético — cada regla acá tiene evidencia detrás (ver
el informe para las fuentes completas).

1. **Toda ilustración en una actividad tiene que ser REPRESENTACIONAL del
   contenido de ESA actividad puntual — nunca decorativa.** Este es el
   hallazgo más importante para este negocio: el "efecto de detalle
   seductor" está confirmado por meta-análisis — una imagen linda pero
   tangencial al contenido EMPEORA la retención, aunque el material se vea
   "más profesional". Un personaje del tema haciendo algo que no tiene que
   ver con la consigna resta, no suma. Esto NO dice "sacar el arte IA" — dice
   que el arte de cada pieza tiene que estar al servicio de la consigna, no
   ser decoración alrededor de ella.
2. **Contraste mínimo AAA (7:1 para texto normal), no el AA legal mínimo.**
   Es el estándar de facto en educación seria. Ya verificado en el sistema
   de paletas actual (`actividades_web.PALETAS`): `ink`/`card` da 11-13:1 en
   los temas chequeados (excelente); `ac` (acento) da ~3-3.6:1 contra `card`
   — CORRECTO porque hoy `--ac` nunca se usa como color de texto normal
   (confirmado por grep), solo como fondo/borde/decoración, donde el umbral
   de 3:1 aplica. Si en algún momento se usa `--ac` como color de texto,
   volver a chequear contraste antes de shippear.
3. **Ningún significado codificado SOLO por color** — siempre acompañar con
   ícono, forma o texto (un chico daltónico o con dificultad de atención no
   puede depender solo del color para entender la consigna).
4. **Tipografía = la letra que el chico está aprendiendo a escribir a
   mano.** Formas de una sola vía (a, g simples, no las de imprenta con
   gancho ambiguo), diferenciación clara entre b/d. El motor ya usa Baloo
   (títulos) y Nunito (cuerpo) — ambas rounded sans-serif, alineadas con
   esto; no hace falta cambiar de fuente, sí verificar que las variantes
   usadas efectivamente tengan formas de una sola vía en minúscula.
5. **Una sola acción clara por pantalla para 4-6 años, con audio-guía
   SIEMPRE presente** — nunca depender de que el chico lea la consigna
   solo. ✅ Construido 14-jul-2026 para la banda `media` (`actividades_web
   .generar_audio_consignas()`, reusa `audiolibro.tts_mp3` — las consignas
   son texto FIJO del player, se graban UNA vez y se sirven como asset del
   repo, NO por token). Al agregar un juego nuevo o una banda nueva,
   agregar sus textos de consigna a esa función (es idempotente, no
   regastás en lo ya grabado) — no lanzar contenido nuevo para 4-7 años
   sin su audio.
6. **Targets táctiles ≥48×48dp con ≥64px de separación** entre elementos
   interactivos — a los 4-7 años el control motor fino todavía falla.
7. **El estilo de ilustración se elige según el OBJETIVO de esa pieza
   puntual**: realista si el objetivo es comprensión/memoria de contenido
   nuevo (ciencias, por ejemplo); estilizado/cartoon si el objetivo es
   engagement/motivación (portada, festejo, mascota). No aplicar un único
   estilo a todo el catálogo por default estético — la elección tiene que
   ser deliberada pieza por pieza.

## 4c. Verificación de aprendizaje real no negociable (investigado 14-jul-2026)

Pablo: *"los chicos tienen que aprender de verdad con estas actividades."*
Confirmado con código real (no solo teoría): `GAMES.mas_menos`
(`actividades_player.js:1448`) tiene un hueco real — con solo 2 grupos para
elegir y reintentos ilimitados sin penalización, un chico puede "ganar" las
5 rondas por ELIMINACIÓN (tocar el que no tocó antes) sin haber entendido
nunca "más" o "menos". Es EXACTAMENTE el riesgo que anticipa la
investigación: cero fail states + pocas opciones + sin exigir precisión en
el primer intento = se puede completar sin aprender.

1. **Todo distractor incorrecto debe representar un error conceptual real
   de esa habilidad, nunca un valor al azar.** Ej: en una resta, el
   distractor no es "cualquier número", es el resultado de restar sin
   pedir prestado correctamente (el error típico real).
2. **Ninguna actividad "completa" con un solo acierto — exigir 80-90% de
   precisión sostenida en preguntas VARIADAS** (estándar de Bloom's mastery
   learning), no la misma pregunta repetida hasta acertar por casualidad.
3. **Cada pregunta debe cambiar de valores/posición en cada intento** — si
   memorizar dónde tocar alcanza para ganar, el juego está mal diseñado
   (esto YA lo hace bien `mas_menos` en los VALORES pero no soluciona el
   problema de fondo: con solo 2 opciones, la eliminación sigue ganando).
4. **Distinguir "acertó al primer intento" (evidencia real de dominio) de
   "acertó eventualmente" (no es evidencia de nada)** — solo el primero
   debería contar para el criterio de "listo, siguiente nivel" o para
   habilitar el diploma de logro. Esto es un cambio real a evaluar en
   `Store`/`win()` del player: hoy no se distingue.
5. **Todo error dispara una explicación corta del PORQUÉ** — una frase a
   los 4-5 años, más detalle de los 8 en adelante — nunca solo "¡mal!
   probá de nuevo" (`ctx.casi()` hoy no explica nada, solo sacude).
6. **Cero fail states se mantiene — es una decisión correcta y respaldada
   por evidencia (ver sección 2, punto 6) — pero nunca a costa del punto
   2.** La ausencia de penalización no reemplaza la exigencia de dominio
   real; son dos ejes independientes, no uno a costa del otro.

## 5. Antes de diseñar contenido nuevo para un año — checklist

1. Releer la sección de ese grado en `docs/CURRICULUM-NAP-ARGENTINA.md`
   (currículum completo desde el 14-jul-2026, los 9 años tienen desglose
   bimestral). Si en algún momento aparece un año sin detalle, pedírselo a
   Pablo ANTES de inventar contenido — no rellenar el hueco con suposición
   propia. **Priorizar las "Ideas web" de cada bimestre por sobre
   "Contenidos" en general** (encontrado 14-jul-2026 cerrando 1° grado):
   "Contenidos" es el currículum completo (sirve también para el cuaderno
   PDF), pero "Ideas web" ya viene curado específicamente para el medio
   interactivo — seguirlo literalmente da un alcance concreto y defendible
   en vez de tener que inventar CÓMO gamificar un tema abstracto (cuerpo
   humano, efemérides) sin ninguna guía. Lo que quede en "Contenidos" sin
   una "Idea web" propia es candidato a PDF o a una pasada de diseño aparte,
   no una obligación de la primera pasada web de ese año.
2. Confirmar la banda de edad en el motor: ¿existe ya una banda separada para
   este grado, o hay que crear una (ver hallazgo de la banda `"grande"` sin
   tope, sección 0)?
3. Aplicar CPA (matemática) o fonética sistemática (lengua) según corresponda
   — sección 2, no negociable.
4. Diseñar el andamiaje/pistas gradual desde el arranque — sección 2, punto 5.
5. Revisar la ilustración de la pieza contra la sección 4b, punto 1: ¿el arte
   representa el contenido de ESTA consigna puntual, o es decoración
   tangencial? Si es decoración, o se saca o se convierte en representacional
   — nunca se deja "porque queda lindo".
6. Diseñar los distractores (opciones incorrectas) a partir de errores
   conceptuales reales de esa habilidad — sección 4c, punto 1 — nunca al
   azar.
7. Confirmar que la actividad exige precisión sostenida en preguntas
   variadas antes de dar "completado" (sección 4c, puntos 2-4) — si un
   juego con pocas opciones se puede ganar por eliminación (como
   `mas_menos` hoy), documentarlo como deuda conocida aunque no se arregle
   en esa misma sesión.
8. Un tipo de actividad nuevo = un test guardián nuevo (mismo criterio que el
   resto del motor: lo que tiene respuesta correcta se VERIFICA por código —
   ver `tests/test_actividades_web.py`/`tests/test_certificado.py` como
   ejemplo de estilo).
9. Para 4-7 años: agregar los textos de consigna NUEVOS a
   `actividades_web.generar_audio_consignas()` (sección 4b, punto 5) — no
   lanzar contenido sin su audio grabado en esa franja.
10. Actualizar la tabla de la sección 4 de ESTA skill cuando el año quede
    validado — que no quede desactualizada para la próxima sesión.
11. **Si el juego usa `setInterval` (timers, cuentas regresivas, etc.)**:
    el shell del player (`Shell.abrir()`) no tiene ningún hook de "se cerró
    el juego anterior" — un intervalo que sigue vivo después de que el
    jugador navegó a otra pantalla puede corromper `Shell.fallos`
    (compartido entre juegos) del juego que esté abierto en ese momento.
    Encontrado y resuelto armando `tablas_contrarreloj` (2° grado,
    14-jul-2026, primer timer del motor): en cada tick, chequear si el
    nodo DOM que ancla al juego sigue `.isConnected` y auto-apagarse
    (`clearInterval`) si no — sin tocar el shell compartido.
