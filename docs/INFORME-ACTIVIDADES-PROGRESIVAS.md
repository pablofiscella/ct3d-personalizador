# Informe: actividades progresivas por edad (4 a 12 años)

> Pedido de Pablo (14-jul-2026): armar una investigación real (currículum NAP +
> metodologías de aprendizaje) que sirva de base para diseñar actividades
> progresivas, empezando por 4 años y subiendo desde ahí. Este informe cruza
> tres fuentes:
> 1. `docs/CURRICULUM-NAP-ARGENTINA.md` — el currículum NAP que Pablo pasó (QUÉ
>    tiene que aprender un chico en cada año escolar).
> 2. Investigación de metodologías de aprendizaje (Piaget, Vygotsky, alfabetización
>    basada en evidencia, Singapore Math, atención sostenida por edad) — CÓMO
>    secuenciar la dificultad de forma pedagógicamente sólida.
> 3. Auditoría real del motor (`cuaderno.py`, `actividades_web.py`,
>    `actividades_player.js`) — QUÉ es capaz de generar HOY, verificado por
>    código (no supuesto).
>
> El proceso repetible para seguir construyendo esto queda en la skill
> `.claude/skills/actividades-progresivas/SKILL.md`.

## 1. Hallazgo principal (el que cambia el orden de trabajo)

**El motor cubre razonablemente Nivel Inicial + 1°/2° grado (4 a 7 años). De 3°
grado en adelante (8 a 12 años) no existe ni un solo tipo de actividad hoy** —
ni multiplicación, ni fracciones, ni decimales, ni geometría con ángulos, ni
álgebra, ni lectoescritura real (sílabas, comprensión, sintaxis), ni ciencias
naturales o sociales curriculares. Esto no es una exageración retórica: se
buscó explícitamente en todo el código (`grep` de "multiplic", "fraccion",
"decimal", "silaba", "sujeto", "cuerpo humano", "virreinato", etc.) y dio
CERO resultados en los tres archivos que arman el cuaderno.

Además, el sistema de bandas de edad actual tiene un problema de fondo: la
banda `"grande"` de `actividades_web._banda()` es `edad >= 6 SIN TOPE
SUPERIOR` — un chico de 12 años recibe literalmente el mismo menú que uno de
6. Esto no es un bug nuevo, es una limitación de diseño heredada de cuando el
producto no necesitaba diferenciar más allá de "cumpleaños infantil".

**Consecuencia práctica**: el pedido de Pablo de "empezar por 4 años e ir
subiendo" es el orden correcto por dos razones, no solo una de negocio
(validar antes de invertir mucho): en 4-7 años el trabajo es sobre todo
CURACIÓN (ordenar/etiquetar lo que ya existe contra el NAP + ampliar rangos),
mientras que en 8-12 años es CONSTRUCCIÓN DE CERO de tipos de actividad
nuevos. Son dos tipos de esfuerzo distintos y conviene no mezclarlos en el
mismo sprint de trabajo.

## 2. Qué dice la investigación pedagógica (resumen accionable)

(Detalle completo y fuentes en la sección de investigación conservada más
abajo — acá solo lo que cambia decisiones de diseño.)

- **Antes de los 7 años, todo tiene que ser manipulable visualmente** — sin
  instrucciones de texto largas, sin lógica abstracta de más de 1-2 pasos
  (Piaget, etapa preoperacional). Coincide con que el motor hoy es
  100% visual/manipulativo para esas edades — es la fortaleza actual, no
  hay que romperla al escalar a más edades.
- **De 7 a 11 años ya hay lógica sobre lo concreto, pero necesita apoyo
  gráfico** — recién a los 11-12 empieza el pensamiento abstracto puro
  (Piaget, operaciones concretas → formales). Esto dice que la matemática de
  3°-5° grado (tabla pitagórica, fracciones, decimales) DEBE tener apoyo
  visual/manipulable (tiras de fracciones, billetes de fantasía — el propio
  NAP que pasó Pablo ya lo propone así) y que recién en 6°-7° se puede pedir
  simbolismo puro (álgebra, ecuaciones sin dibujo).
- **Matemática: enfoque Concreto → Pictórico → Abstracto (Singapore Math)** —
  validado internacionalmente. Cualquier operación nueva se presenta primero
  con objetos, después con dibujos/barras, recién al final con el símbolo
  solo. El motor ya hace esto PARCIALMENTE (grupos de personajes contables)
  pero hay que sistematizarlo como regla para todo contenido numérico nuevo.
- **Alfabetización: fonética sistemática, no reconocimiento visual de
  palabras** (National Reading Panel 2000, evidencia sólida). La secuencia
  validada es conciencia fonológica ORAL (rimas, sonidos aislados) → combinar
  sonidos → sílabas escritas → palabras → oraciones. El motor hoy NO tiene
  ningún componente de sonido en las actividades de lengua (todo es visual:
  sopa de letras, "código secreto" con símbolos) — es un hueco real, no solo
  de contenido sino de MECÁNICA (falta un componente de audio/fonética que
  hoy no existe en ningún juego).
- **Andamiaje (Vygotsky/ZPD): la ayuda tiene que retirarse gradualmente**, no
  ser siempre igual. El sistema de "pistas" que ya existe en varios juegos
  debería graduarse (pista fuerte en el primer error → más sutil en el
  segundo → sin pista si acierta seguido) en vez de dar siempre la misma
  ayuda — mejora concreta y barata sobre lo que ya está construido.
- **"Cero fail states" ya está respaldado por evidencia real**, no es solo
  buena UX: la investigación sobre juegos educativos infantiles distingue
  "confusión productiva" (motiva) de "confusión desesperanzada" (hace
  abandonar) — dar salida ANTES de que se acumule frustración es clave
  específicamente en chicos chicos (tienen menos estrategias emocionales que
  un adulto para tolerar el fracaso). Mantener este principio al escalar a
  más edades, no relajarlo.
- **Atención sostenida por edad — tabla para armar packs de "30 minutos"**:

| Edad/grado | Atención por actividad | Actividades distintas en 30 min | Andamiaje |
|---|---|---|---|
| 4-5 años (inicial) | 8-12 min | 3-4 actividades cortas y variadas | Pista visual fuerte y constante |
| 6-7 años (1°-2°) | 12-15 min | 2-3 actividades | Pista fuerte → se retira si acierta 2 veces seguidas |
| 8-9 años (3°-4°) | 15-20 min | 2 actividades + 1 repaso corto | Pista solo a pedido (botón "ayuda") |
| 10-11 años (5°-6°) | 20-25 min | 1-2 actividades profundas | Pista mínima; el feedback explica el POR QUÉ |
| 12 años (7°) | 25-30 min | 1 actividad larga o 2 medianas | Casi sin andamiaje, autonomía |

Esta tabla es directamente el motor de dosificación del feature "Modo
Maestra / Mamá ocupada" (30 minutos según edad) — ya queda lista para usar.

## 3. Estado real del motor, por tipo de contenido (verificado por código)

| Área NAP | Estado hoy | Evidencia |
|---|---|---|
| Motricidad / discriminación visual (inicial) | ✅ Cubierto | `cuaderno._construir` banda `e<=3`/`e<=5`: colorear, trazos, sombra, iguales, tamaño |
| Matemática básica (conteo, patrón, +/- de un dígito) | ⚠️ Parcial, techo bajo | `_a_sumas`: sumando A 1-4, resultado real ~7-8 (no llega a 10 pese al parámetro `max=10` en la UI) |
| Sílabas, alfabetización, comprensión lectora | ❌ No existe | 0 resultados grepeando fonología/sílaba/sujeto/predicado/ortografía en los 3 archivos |
| Multiplicación, tabla pitagórica, división | ❌ No existe | 0 resultados |
| Fracciones, decimales, porcentajes | ❌ No existe | 0 resultados |
| Geometría (ángulos, perímetro, área, cuerpos) | ❌ No existe | 0 resultados |
| Álgebra, proporcionalidad, estadística | ❌ No existe | 0 resultados |
| Ciencias Naturales (cuerpo, animales, plantas, materia) | ❌ No existe (solo decorativo) | 0 resultados de contenido curricular; los "temas" son estética, no currícula |
| Ciencias Sociales (historia, geografía argentina) | ❌ No existe | 0 resultados |

## 4. Roadmap propuesto (empezando por 4 años, como pidió Pablo)

| Orden | Edad/grado | Tipo de trabajo | Esfuerzo relativo |
|---|---|---|---|
| 1 | Sala de 4 años | Curar + etiquetar lo existente contra los 3 ejes NAP | Bajo — ver diseño abajo |
| 2 | Sala de 5 años | Ídem + pedirle a Pablo el desglose bimestral que falta (ver pendientes en el doc de currículum) | Bajo |
| 3 | 1° grado | Ampliar rango numérico real (hoy tope ~7-8, NAP pide hasta 100) + agregar mecánica de sílabas CV (juego nuevo: "armar palabras arrastrando sílabas", idea que el propio Pablo ya trajo) | Medio |
| 4 | 2° grado | Separar de la banda "grande" (hoy comparte banda con 1° y con 12 años); sílabas complejas; números hasta 50-80; pedirle a Pablo el desglose bimestral que falta | Medio |
| 5 | 3° grado | Construir de cero: tabla pitagórica interactiva, números de 4 cifras, cuerpos geométricos, primeras nociones de ciencias naturales/sociales curriculares | Alto |
| 6 | 4°-5° grado | Fracciones (con apoyo visual — tiras, CPA), decimales, geometría con compás, primera historia argentina real (colonia, Revolución de Mayo) | Alto |
| 7 | 6°-7° grado | Porcentaje, proporcionalidad, álgebra informal, estadística, ciencias naturales avanzadas (célula, sistema nervioso/endocrino), historia/geografía argentina contemporánea | Alto |

Los pasos 5-7 comparten un patrón: necesitan tipos de actividad NUEVOS (no
extender parámetros de los 23 que ya existen), así que conviene diseñarlos
recién cuando 1-4 estén validados y haya aprendido de esa primera ronda real.

## 5. Diseño concreto del primer paso: Sala de 4 años

Con los 3 ejes NAP (Comunicación y Lenguajes / Indagación del Ambiente /
Desarrollo Personal y Social) y el catálogo real del motor:

| Eje NAP | Juegos del motor que ya sirven | Qué falta |
|---|---|---|
| Comunicación y Lenguajes | colorear, trazos (motricidad fina — pre-escritura) | Nada de "expresión oral" ni "iniciación a la literatura" — son ejes que no se prestan a una actividad autocorregible, mejor dejarlos fuera del producto digital y no forzarlos |
| Indagación del Ambiente | memotest/agrupar con personajes del tema (animales, objetos) puede reetiquetarse como "el cuerpo", "los animales" si se cura el set de imágenes por sub-eje | Nada específico de "objetos cotidianos" o "tecnología simple" hoy |
| Desarrollo Personal y Social | patrón, tamaño, iguales, sombra (motricidad fina/gruesa indirecta) | El eje de "juego compartido" no aplica a un producto de un jugador — dejar fuera |

**Conclusión para Sala de 4**: no hace falta ni un juego nuevo — hace falta
CURAR cuáles de los 18 juegos de la banda "media" se muestran y con qué
personajes/etiqueta, para que el pack de 30 minutos elegido no se sienta
"genérico" sino directamente relacionado a lo que el chico ve en el jardín.
Es exactamente el tipo de trabajo bajo-esfuerzo/alto-impacto ideal para
arrancar y aprender el proceso antes de meterse en los años donde hay que
construir contenido nuevo de cero.

## 6. Pendientes que dependen de Pablo (no técnicos)

1. Desglose bimestral de Sala de 4, Sala de 5, 2° grado y 4° grado — nunca
   llegaron a pasarse (ver `docs/CURRICULUM-NAP-ARGENTINA.md`).
2. Decisión de alcance: ¿el feature "Modo Maestra" (30 min) es un producto
   nuevo con su propio precio, o una forma nueva de comprar/generar lo que
   ya existe (actividades imprimibles / actividades-web)?
3. Validar si de verdad conviene ir grado por grado en orden, o si hay algún
   año con más demanda de mercado (ej. jardín/1er grado, por ser la franja
   etaria del cumpleaños infantil que ya es el core del negocio) que
   convenga priorizar aunque no sea el primero cronológicamente.
