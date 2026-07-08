---
name: armar-kit
description: Reglas para generar TODO el kit de cumpleaños de una temática con arte IA profesional y consistente (stickers, actividades, menú, rompecabezas, gorro/corona, memoria, certificado, papertoys, cápsula, rutina, milestone, invitación, afiche, banderines, toppers). Usar SIEMPRE al tocar ia_kit/, piezas.py, cuaderno.py, o cualquier módulo de producto individual (menu_infantil, rompecabezas, corona, memoria, papertoys, capsula_tiempo, antifaces, certificado, rutina, baby_shower).
---

# Armar el kit completo — reglas de CT3D

Motor en `/root/ct3d-personalizador`. Hermana de `armar-audiolibros` (misma filosofía: cada
error de producción → una regla acá + una cláusula de prompt + un test guardián — NUNCA
arreglar solo el caso puntual).

**GOAL vigente: un solo botón genera TODO el kit de una temática, con la misma impronta
gráfica que el libro, cero piezas con defecto.** Modelo: generar → QA → revisar →
cachear → reusar. Solo se vende lo revisado. Toda pieza conserva su fallback procedural
(ninguna puede quedar "sin nada").

## 0. ARQUITECTURA (la receta del libro, generalizada)

1. **`ia_maestra.png` es la ÚNICA ancla de estilo del tema.** Va como PRIMERA referencia
   en TODA generación (libro ya lo hace: `libro_ia.referencias()`; el kit debe unificar
   `ia_kit/orquestador._refs()` que hoy la agrega última). Sin maestra NO se genera
   catálogo (error claro, nunca arte con personajes random).
2. **Botón único** = composición de los flujos existentes, no código nuevo de generación:
   maestra (→ aprobación humana, es el punto de máximo apalancamiento) → piezas del kit
   en paralelo (4 threads) → libro al final (lo más largo). Incremental (`solo_faltantes`)
   para re-ejecutar sin regastar. Job en background + polling `/dash/ia-estado` (los POST
   síncronos daban 504 en el proxy).
3. **El texto personalizado NUNCA va horneado en la imagen IA** — lo escribe SIEMPRE el
   motor encima, en una "ventana" definida por pieza (insignia circular del gorro, banda
   de la corona, panel del libro). Bug histórico: el calendario con overrides renderizados
   tapaba la personalización de cada cliente.
4. **QA por perfil de pieza** (no un QA genérico): primero detectores deterministas gratis
   (tipo `_piso_blanco`), después visión (gpt-4o-mini) mirando SOLO los 2-4 defectos
   graves de ESA pieza + "ante duda OK" (QA estricto = 3x costo) + la ia_maestra como
   referencia anti-falsos-positivos. Rechazo → 1 reintento con el motivo appendeado al
   prompt → fallback procedural + log para revisión humana.
5. **Notas del editor por tema** (patrón `libro_ia.nota_tema`): un arreglo pedido una vez
   se inyecta en TODOS los prompts futuros de esa temática.
6. **Moderación aleatoria de OpenAI**: la misma referencia a veces pasa y a veces no —
   reintentar hasta 4 veces SOLO si el error es moderación (patrón de
   `generar_variantes_colorear`), generalizarlo a toda pieza.
7. **Control de gasto**: `calidad=low` para iterar, `medium/high` recién al aprobar;
   presupuesto por corrida; failover OpenRouter ya resuelto en `servicio._openai_client()`.

## 1. IMPRENTA — reglas transversales (aplican a TODA pieza)

- **DPI: dibujar a 300dpi REAL.** `piezas.generar_kit()` exporta el PDF con
  `resolution=300` SIEMPRE, sin mirar la imagen → todo módulo que dibuje a
  `Wp,Hp=1240x1754` (~150dpi) imprime a la MITAD del tamaño físico (A5 en vez de A4).
  corona.py ya se corrigió (dibuja 3508x2480); **al rediseñar cada módulo, migrarlo a
  300dpi** (A4 vertical = 2480x3508, apaisado = 3508x2480; `_PXMM = 2480/210`).
  Auditoría 7-jul-2026: además de los 8 tipos del gotcha, TAMBIÉN dibujan a 150dpi
  **baby_shower (6 piezas), cuaderno y libro** — con consecuencias físicas graves:
  antifaz de 9cm (no entra en una cara), cartas de memoria de 3cm, cubo de 3.7cm.
  A 300dpi real solo estaban: corona/gorro, milestone, colorear/juegos y las
  hojas-grilla del kit.
- **Área A4/Carta universal**: contenido dentro de un área centrada de **190x255 mm** —
  el mismo PDF imprime al 100% en A4 y Letter sin escalar (clave: clientes argentinos
  imprimen en las dos).
- **Sangrado 3mm** solo para fondos/patrones; **texto y elementos clave a ≥5mm del
  corte**. Línea de corte = sólida; doblez = guiones; nunca esquinas agudas en troqueles.
- **Tipografía mínima 12pt** en piezas infantiles (scripts ≥14pt); texto calado (claro
  sobre color) ≥10pt sin serifas finas. Máximo 2 tipografías por pieza, roles fijos
  (display SOLO títulos/nombres — Fredoka ya es la display de la casa).
- **Página "Cómo imprimir"** en todo kit: papel recomendado por pieza (cardstock
  200-300g para armables, adhesivo inkjet para stickers), "imprimir al 100%/tamaño
  real", cuadrado de prueba de 5cm para verificar escala.
- Line-art (colorear): negro 100% puro, sin grises ni degradés.

## 2. IMPRONTA CONSISTENTE (lo que separa premium de amateur)

- **La invitación es la pieza ancla**: define marco, paleta y jerarquía; todo deriva de ella.
- **Paleta cerrada** del tema (accent de `tema.json` + 3-5 colores derivados) — ninguna
  pieza introduce un color nuevo.
- **Style card en el prompt**: bloque fijo antepuesto a TODOS los prompts del kit
  ("ilustración infantil acuarela/flat, contornos gruesos uniformes, paleta del tema,
  mismo estilo que la referencia"). La referencia visual (ia_maestra) manda; el texto
  del style card refuerza.
- **Personajes con hoja de modelo**: los MISMOS 1-3 personajes del tema (recortes de la
  hoja de stickers vía `cuaderno.personajes_decorativos`, cache autoinvalidante por
  mtime) aparecen en menú, rutina, certificado, memoria, puzzle, toppers... El estilo
  flat/acuarela con contorno es el más fácil de mantener consistente entre decenas de
  piezas.
- **BUG conocido de `personajes_decorativos` (auditoría 7-jul-2026)**: elige recortes
  por TAMAÑO → en artistas pegaba una MESA y un FRASCO como "personajes" en
  rompecabezas/cápsula/certificado/papertoys/corona, duplicaba el mismo personaje
  (2 monitos idénticos), y prioriza `ia_draft/` (borrador) sobre `extras/` (aprobado).
  Regla: el selector debe distinguir personaje-de-objeto (QA de visión barato sobre los
  recortes cacheados, UNA vez por tema: "¿es un personaje/animal o un objeto?") y
  preferir lo aprobado.
- **Color de acento roto en 5 de 13 temas** (sin `kit.accent` en tema.json → violeta
  genérico): safari (¡el tema insignia!), futbol, princesas, superheroes (dir duplicada
  con tilde y sin stickers), un-espacio-de-locura. Además hay DOBLE fallback
  inconsistente (piezas.accent()→TERRA, módulos individuales→violeta). Completar los
  tema.json y unificar el fallback.
- **PROHIBIDO usar emoji en texto renderizado** (🎨 ✂ ⬅ salen como cuadraditos tofu —
  Fredoka no tiene esos glifos). Íconos SIEMPRE dibujados o de la biblioteca de recortes.
- **Boilerplate repetido**: `_font/_accent/_tint/_personajes/_paste_h` están copy-pegados
  en 8+ módulos — al rediseñar, consolidar en un helper común (cada fix hoy se hace 8
  veces).
- **Motivos reutilizados a 2-3 escalas**: el patrón del tema se reubica/rota/reescala por
  pieza — nunca copy-paste idéntico. Reusar los assets de los stickers DENTRO de las
  actividades (el bingo usa los mismos íconos, el I-spy los mismos personajes) refuerza
  la impronta y abarata generación.
- **Contorno blanco de 2-3mm** en TODO recortable (stickers, props, toppers, personajes
  del puzzle) — es EL rasgo visual "sticker pro" y además perdona desregistros de corte.
- Assets aislados + composición programática: la IA genera ARTE (personajes, escenas,
  patrones); el layout, textos, troqueles y die-lines los pone SIEMPRE el motor (Pillow).
  Nunca pedirle a la IA "la pieza terminada con texto".

## 3. STICKERS (plancha kiss-cut) — `ia_kit` pieza `stickers`

- Separación entre stickers **≥3mm** (premium 6mm); margen exterior de plancha ≥5mm;
  ningún sticker menor a 2.5cm. El `_regrid_stickers` del orquestador ya reacomoda —
  mantener sus garantías y sumar el chequeo de separación como test.
- **Borde blanco de 2-3mm alrededor de cada figura** (el orquestador ya lo hace con
  `_sticker_borde` — no perderlo en rediseños).
- Tamaño estrella: **círculo de 5cm (2")** — sirve de sticker Y de topper de cupcake.
- La hoja de stickers es el INSUMO de `personajes_decorativos` para todas las demás
  piezas → su calidad multiplica: QA de visión específico = (a) figuras completas no
  cortadas, (b) sin texto, (c) personajes del tema únicamente, (d) figuras separadas
  (no amasijos pegados — el detector de densidad de `_extraer_monstruos` ya filtra,
  pero mejor que no lleguen).
- Instrucción al cliente: papel adhesivo inkjet (láser derrite muchos adhesivos).

## 4. ACTIVIDADES (cuaderno) — `cuaderno.py`

- **La actividad ES temática, no lleva el tema de adorno**: laberinto = "ayudá al
  {personaje} a llegar a {meta del tema}"; contar = objetos del tema; sopa de letras =
  vocabulario del tema; bingo/I-spy = los MISMOS íconos de la hoja de stickers.
- **Dificultad por edad** (calibración de la industria):
  - 2-3: colorear formas gigantes (5-10 elementos), aparear figura-sombra, trazos
    gruesos, contar 1-3, laberinto de camino único con **camino ≥2cm de ancho**.
  - 4-5: laberinto simple, unir puntos 1-10/1-20, contar 1-10, 3-5 diferencias, sopa
    **6x6 con 4-6 palabras solo horizontales/verticales**, trazado del nombre, color
    por número (≤5 colores, zonas grandes).
  - 6-8: laberinto complejo, unir puntos 1-50+, sopa 10x10 con diagonales, crucigrama
    con pistas pictográficas, 7-10 diferencias, código secreto, I-spy con conteo.
- **Anatomía de página**: encabezado (título + motivo del tema) · UNA línea de
  instrucción · zona de actividad enmarcada · pie con nombre del kit + nº de página.
  Dificultad progresiva dentro del pack. **Página final de soluciones** (miniaturas
  4-up) — ya existe el solucionario, mantenerlo.
- Lo verificable por código SIGUE siendo por código (laberinto con salida por BFS, sopa
  con palabras realmente colocadas — filosofía actual de cuaderno.py, NO delegar a IA).
- **Colorear (line-art)**: contorno exterior 6-8pt para 2-3 años · 4-6pt para 4-5 ·
  2-4pt para 6-8; interiores un escalón más finos; **<8 zonas de color para menores de
  5**; personaje central grande + 2-3 props + marco temático; nombre del niño en
  outline gigante para colorear; paths cerrados; sin sangrado (margen 1.5-2cm).
  `_limpiar_colorear` garantiza B/N puro — mantener.

## 5. MENÚ INFANTIL — `menu_infantil.py`

- Formato: A4 vertical con fondo IA (marco del tema + centro claro) o fallback
  procedural. Encabezado ≈20% de la altura ("Menú del día" + nombre).
- **Tarjetas SEMITRANSPARENTES (regla de Pablo, 8-jul-2026)**: el arte IA suele poner
  a los personajes ABAJO de la hoja y las tarjetas opacas los tapaban — alpha ~190
  deja ver el arte a través sin perder legibilidad de lo escrito.
- **El menú se entrega INCOMPLETO a propósito (regla de Pablo, 8-jul-2026)**: si el
  comprador no cargó la comida, cada sección lleva RENGLONES en blanco para escribir
  a mano — NUNCA inventar el menú de la fiesta de otro con defaults. Los 4 campos del
  cliente (entrada/plato/postre/bebida) siguen siendo opcionales en la tienda.
- Un ícono por ítem dibujado por código (no emoji).

## 6. ROMPECABEZAS — `rompecabezas.py`

- **Piezas con knobs REALES, no cortes rectos**: cada borde interior = 3 segmentos de
  Bézier cúbicas formando un knob; bulbo ≈20-25% del largo del borde, más ancho que su
  cuello (traba de verdad); jitter aleatorio en posición/tamaño de knobs (cada pieza
  única). Es EL diferenciador pro.
- Grillas por edad (hoja carta apaisada, arte 24x18cm): **4x3=12 piezas de 6x6cm**
  (3-5 años) · **5x4=20 piezas de ~4.8x4.5cm** (5-7). Menores de 3: piezas ≥5cm
  (seguridad: nada que entre en cilindro de Ø3.2cm).
- Nombre en 100-150pt ocupando ~40% de la altura, sobre escena IA del tema (no fondo liso).
- Premium: **página-bandeja** con el contorno de las piezas impreso (se arma encima) +
  imagen de referencia del puzzle armado.

## 7. GORRO Y CORONA — `corona.py` (YA rediseñado — es el modelo a seguir)

- Ver docstring de `corona.py`: A4 apaisado 300dpi, 3 talles por edad (S 1-2: arco
  36cm · M 3-5: 41cm · L 6-9: 44cm), lengüeta+ranura sin pegamento, 2 agujeros para
  elástico con refuerzo, nombre/edad en insignia circular crema (nunca texto directo
  sobre el arte).
- Fondo IA del gorro vía `corona_ia.py` (apaisado 1536x1024, recortado a la forma del
  abanico). **La corona NO usa fondo IA** (picos angostos fragmentan cualquier
  ilustración) — color liso + personajes recortados.
- Mejoras pendientes de la investigación: arte con **layout radial** en el abanico (los
  motivos orientados a lo largo del radio quedan derechos al cerrar el cono — pedirlo
  en el prompt); puntas de picos redondeadas; refuerzo impreso (anillo) en los agujeros.

## 8. MEMORIA — `memoria.py`

- Carta **cuadrada 63x63mm** (toddlers: 75-90mm), esquinas redondeadas 4-6mm, 12 cartas
  (3x4) por hoja con marcas de corte.
- Pares por edad: 2 años: 3-6 · 3-4: 6-10 · 5-6: 10-15 · 7+: 15-24 (hoy son 12 fijos
  — parametrizar por edad).
- **DORSO obligatorio** (hoja aparte para pegar dorso con dorso): patrón del tema
  repetitivo, IDÉNTICO en todas, tonos medios/oscuros que enmascaren la transparencia
  — jamás liso claro. Es la pieza donde más se nota lo amateur.
- Frentes: pares de la biblioteca de stickers (mismo asset, no dos generaciones
  distintas del mismo personaje — deben ser IDÉNTICOS para poder aparear).

## 9. ANTIFACES / PHOTO BOOTH — `antifaces.py`

- Antifaz infantil: **15-17cm de ancho**; centros de ojos a **52-55mm** con agujeros
  Ø30-35mm (cubre de 3 a 10 años); anillos de refuerzo impresos en agujeros laterales.
- Props: anteojos 15-20cm, bigotes 10-13cm, globos de diálogo 20-25cm con frases del
  TEMA; palito al COSTADO (no al centro: tapa la cara), entrando ⅓ de la altura.
- Contorno blanco 3-5mm en todas las piezas (coherente con stickers). Set premium:
  12-20 props mezclando frases + accesorios.

## 10. CERTIFICADO — `certificado.py`

- A4 apaisado. Jerarquía clásica: orla del tema → título temático («Certificado de
  Súper Explorador») → "otorgado a" → **NOMBRE 40-60pt (el elemento más grande)** →
  motivo (1-2 líneas) → fecha + firma → **sello/roseta** (estrella con cintas) abajo,
  flanqueado por personajes del tema.
- Máximo 2 tipografías, layout simétrico, blancos generosos.

## 11. PAPER TOYS — `papertoys.py`

- Cubo: caras de **5-7cm**, pestañas trapezoidales de **8-10mm con chanfles a 45°**,
  una pestaña por arista abierta (nunca dos encontradas), **pestañas NUMERADAS en
  orden de pegado**, base al final.
- **El arte continúa a través de las aristas** (caras adyacentes empalman al plegar) —
  esto separa pro de amateur. Mapeo: frente=cara del personaje · laterales=brazos/patrón
  · arriba=pelo · abajo=patas.
- Marcar (score) los dobleces con línea de guiones.

## 12. CÁPSULA DEL TIEMPO — `capsula_tiempo.py`

- Kit completo, no una hoja: cartel 8x10" para la mesa · **tarjetas de deseos 5x7"**
  con prompts («Espero que ames ___») · tarjeta "snapshot" del año (precios de hoy,
  canción del momento) · papel de carta («para leer a los 18») · **etiqueta de sobre
  «No abrir hasta {año+15}»** · checklist de qué guardar.
- Tipografía más sobria/elegante que el resto del kit (es la pieza emocional), misma paleta.

## 13. RUTINA VISUAL — `rutina.py`

- Tablero A4 + **fichas cuadradas de 5-6cm** (recortables, para velcro/imán).
  **3-5 pasos toddlers, máximo 5-8**. Mañana=sol/amarillo, noche=luna/azul.
- Pictograma pro: UNA acción por ficha, **el MISMO personaje del tema ejecutando la
  acción**, fondo mínimo, contornos gruesos. (Es la pieza donde más rinde la
  consistencia de personaje: 12+ poses del mismo personaje — candidata a set IA
  dedicado "hoja de poses" por tema.)

## 14. MILESTONE (mes a mes) — piezas del tipo `milestone`

- **Tarjetas cuadradas 4x4" (10x10cm)**, 4-up por hoja carta. Set: portada + meses
  1-12 + extras (primera sonrisa, primer diente, primeros pasos) = 13-17 tarjetas.
- **El número/mes ocupa ≥25-30% de la altura** (se lee en una foto a 1-2m), alto
  contraste, marco IDÉNTICO en todo el set (solo cambia numeral + micro-motivo).

## 15. INVITACIÓN · AFICHE · BANDERINES · TOPPERS (kit clásico, `ia_kit`/`piezas.py`)

- Invitación: **5x7"** impresa 2-up + versión digital **1080x1920** (WhatsApp/story).
  Jerarquía: nombre+edad héroe → fecha/hora → lugar → RSVP.
- Cartel de bienvenida: 8x10" (mesa) y 18x24" (caballete) — diseñar pensado para
  escalar; letra ≥2.5cm por cada 3m de distancia de lectura.
- Banderines: triángulo 5x7" a 7.5x10", 2 por hoja, **una letra por banderín ≥60% de
  la altura**, solapa superior de 2cm que se dobla sobre el hilo (más pro que
  perforar).
- Toppers: círculo 5cm, **dos círculos espejados encapsulando el palito** (sandwich),
  12-20 por hoja, borde festoneado = lectura premium instantánea.
- Satélites: carpitas de comida 3.5x2" plegadas · etiquetas de botella 9x2.4" ·
  tags 2x3" con perforación 5mm · wrappers en arco 21-25x5cm.

## 16. AUDITORÍA 7-jul-2026 — bugs confirmados por producto (con render a la vista)

Ranking peor→mejor y qué corregir (muestras en el job dir `tmp/audit/`, regenerables
con `render_audit.py`):

1. **antifaces — INUTILIZABLE**: el "antifaz mariposa" son dos aros sin forma de máscara
   ni agujeros de ojos; bigotes irreconocibles y SUPERPUESTOS entre sí (grilla de 400px
   con piezas de ~570px); lentes superpuestos y cortados. Rediseño total con siluetas IA.
2. **papertoys — el cubo NO ARMA**: red inválida (fila de 4 + 2 caras contiguas abajo se
   superponen al plegar), sin solapas reales (las instrucciones mencionan solapas que no
   existen), 6ª cara vacía. La **cajita_sorpresa del kit ya resuelve un troquel válido —
   copiar ese approach**.
3. **rompecabezas — sin puzzle real**: el nombre gigante se dibuja ENCIMA de la grilla
   (colisión total), el nombre aparece 2 veces, `_generar_piezas()`/`_dibujar_base()`
   son CÓDIGO MUERTO (nunca se llaman).
4. **cápsula — bug lógico**: "NO ABRIR HASTA tus {edad} años" usa la edad ACTUAL (la
   descripción de tienda promete abrir en 5/10/18 años). El sobre tiene una MESA dentro
   del "sello". La carta (preguntas+líneas) se salva.
5. **certificado**: la medalla pisa el título "CERTIFICADO", el sello es un círculo
   vacío, muebles sobre la línea de firma.
6. **menú**: mitad inferior de la hoja EN BLANCO; dice "Coloreá el menú" y no hay nada
   para colorear (todo relleno sólido); emoji tofu.
7. **milestone**: los 12 marcos del anillo SE SUPERPONEN entre sí; y la descripción en
   TIPOS dice "12 tarjetas" pero el producto real es 1 póster — sincerar (o hacer las
   tarjetas 4x4" de la sección 14, que es lo premium).
8. **memoria**: dorso DESALINEADO 90px (~15mm) del frente → la impresión doble faz no
   coincide; 3-4 pares casi idénticos entre sí (injugable a los 4 años); cartas con
   recortes mezclados (2 figuras juntas).
9. **corona (pieza 2)**: quedó 2 generaciones atrás del gorro — picos lisos ralos, mucho
   vacío.
10. **rutina**: la mejor procedural (solo detalles: stickers cortados en el header,
    header navy fijo que ignora la paleta).
11. **baby_shower**: el mejor tipografiado procedural (Pacifico/Dancing/Poppins) pero
    sin ilustración; usa 4 sub-temas EN CÓDIGO, ignora tema.json e IA.
12. **kit (piezas.py + extras IA) — el estándar de la casa**, con bugs de OVERLAY de
    texto: el afiche de artistas queda con el recuadro del nombre VACÍO; edad>3 cae
    silenciosamente a `_1.png` (muestra "1" para edad 4); el banderín escribe "¡FELIZ
    CUMPLE {nombre}!" cruzado ENCIMA del arte; la cajita parte el texto entre 2 caras
    cruzando pliegues; las tarjetas de agradecimiento escriben el texto sobre el moño
    mientras el marco festoneado diseñado para el texto queda vacío. Regla: cada extra
    con texto necesita su `zona_motor` (spec de posición) — nunca centrado ciego.
13. **gorro con fondo IA (artistas/princesas): casi profesional** — falta generar el
    fondo para los otros 11 temas y filtrar muebles del selector de personajes.

## 17. FLUJO del botón único — IMPLEMENTADO 8-jul-2026

Botón **«⚡ Armar TODO el tema»** en la tarjeta de cada temática del dash →
`POST /dash/armar-tema?tema=X` (`servicio._armar_tema`). Flujo:

1. **Dry-run primero** (`?dry=1`): devuelve el desglose de lo que FALTA (kit /
   colorear / fondos / gorro / libro) — el dash lo muestra y pide confirmación
   antes de gastar. Todo es INCREMENTAL: lo generado no se toca.
2. **Piezas del kit** vía `ia_orq.generar_tema(solo_faltantes=True,
   reusar_maestra=True)` — crea la ia_maestra si no existe. REGLA: una pieza
   cuenta como generada si está en `ia_draft/` **o aprobada en `extras/`**
   (`_pieza_existe`) — mirar solo el draft hacía que un tema con todo aprobado
   figurara como "faltan todas" y se regenerara entero (bug real, artistas).
3. **Variantes de colorear** (3) + limpieza del `actividades_cache`.
4. **Fondos IA de productos individuales** (`fondos_ia.PIEZAS`) + **gorro**
   (`corona_ia`).
5. **Ilustraciones del libro** (las 10, lo más caro — `?libro=0` lo saltea).
6. Los procedurales (menú, memoria, puzzle, cubo, certificado...) heredan
   automáticamente los personajes/fondos nuevos (caches autoinvalidantes).
7. Al terminar: revisión humana en la galería + aprobar el draft. Solo se vende
   lo revisado.
8. Cada defecto que aparezca: regla acá + cláusula de prompt + test guardián.

## Reglas de oro

- **300dpi real en todo módulo nuevo/rediseñado** (el exportador PDF asume 300 — dibujar
  a menos = imprimir a la mitad).
- La IA genera ARTE; el motor pone layout, texto, troqueles y medidas. El texto del
  cliente JAMÁS queda horneado en una imagen.
- ia_maestra primera referencia SIEMPRE; sin maestra no hay catálogo.
- Contorno blanco en todo recortable; separaciones de troquel ≥3mm; esquinas redondeadas.
- Personajes idénticos entre piezas = recortes de la MISMA hoja de stickers (no
  regeneraciones sueltas).
- QA barato primero (píxeles), visión después (solo defectos graves de ESA pieza, ante
  duda OK), 1 reintento con motivo, fallback procedural siempre.
- Generar → QA → revisar → cachear → reusar. Solo se vende lo revisado.
- Commit/push SOLO cuando Pablo lo pide.
