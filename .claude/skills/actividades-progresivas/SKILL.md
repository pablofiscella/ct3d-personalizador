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
| 1 | Sala de 4 años | 🔜 Próximo — mapeo bimestre a bimestre ya hecho, informe §5: 11/11 contenidos matemáticos ya tienen juego | Curación (bajo esfuerzo) |
| 2 | Sala de 5 años | Mapeo ya hecho, informe §5 — mitad matemática lista, mitad fonética sin construir | Curación (matemática) + construcción (audio/fonética) |
| 3 | 1° grado | Desglose disponible en el currículum | Curación + ampliar rango numérico + sílabas CV (reusa el audio de Sala 5) |
| 4 | 2° grado | Desglose disponible en el currículum (completado 14-jul) | Curación + banda propia (hoy comparte con 12 años) + cursiva + multiplicación conceptual |
| 5 | 3° grado | Desglose disponible en el currículum | Construcción (tabla pitagórica, miles, geometría) |
| 6 | 4°-5° grado | Pendiente — 4° sin desglose de Pablo | Construcción (fracciones CPA, decimales, historia real) |
| 7 | 6°-7° grado | Desglose disponible en el currículum | Construcción (porcentaje, álgebra informal, ciencias avanzadas) |

## 5. Antes de diseñar contenido nuevo para un año — checklist

1. Releer la sección de ese grado en `docs/CURRICULUM-NAP-ARGENTINA.md`. Si
   dice "⚠️ PENDIENTE" (solo 4° grado al 14-jul-2026), pedirle el desglose a
   Pablo ANTES de inventar contenido — no rellenar el hueco con suposición
   propia.
2. Confirmar la banda de edad en el motor: ¿existe ya una banda separada para
   este grado, o hay que crear una (ver hallazgo de la banda `"grande"` sin
   tope, sección 0)?
3. Aplicar CPA (matemática) o fonética sistemática (lengua) según corresponda
   — sección 2, no negociable.
4. Diseñar el andamiaje/pistas gradual desde el arranque — sección 2, punto 5.
5. Un tipo de actividad nuevo = un test guardián nuevo (mismo criterio que el
   resto del motor: lo que tiene respuesta correcta se VERIFICA por código —
   ver `tests/test_actividades_web.py`/`tests/test_certificado.py` como
   ejemplo de estilo).
6. Actualizar la tabla de la sección 4 de ESTA skill cuando el año quede
   validado — que no quede desactualizada para la próxima sesión.
