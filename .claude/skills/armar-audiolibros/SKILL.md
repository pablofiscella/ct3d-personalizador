---
name: armar-audiolibros
description: Reglas para armar/modificar los AUDIOLIBROS y LIBROS de cuento de CT3D (historias modulares, voz, ilustraciones, largo por edad, catálogo, preview y entrega). Usar SIEMPRE al tocar libro.py, libro_historias.py, libro_ia.py, audiolibro.py, o los productos de audiolibro en la tienda (/opt/ct3d).
---

# Armar audiolibros y libros de cuento — reglas de CT3D

Motor en `/root/ct3d-personalizador`. Tienda/catálogo en `/opt/ct3d/backend`. Un audiolibro = páginas ilustradas + narración por página + page-flip, servido en `kit.casatridimensional.com.ar/al/<token>`.

**GOAL vigente: cero errores de diálogo y de imágenes.** Todo error nuevo se convierte en una regla acá y en un chequeo en `tests/test_historias_catalogo.py` (el guardián). NUNCA arreglar solo el caso puntual.

## 0. SISTEMA MODULAR (texto gratis, arte por combo)

- **8 historias** (`libro_historias.ARGUMENTOS_LARGO`, 17 págs c/u) × **N temáticas** (`libro.HISTORIAS`) = el texto de cualquier combo se arma solo por sustitución de tokens: `{nombre} {mundo} {amigos} {conteo} {conteo_num} {tesoro} {desafio} {solucion}`.
- El ARTE es por combo (tema, historia, edad, género) → **generar UNA vez → revisar → cachear (escenas_dir por pedido) → reusar**. Solo se vende lo ya revisado.
- Antes de generar arte: `python3 -m pytest tests/test_historias_catalogo.py -q` **tiene que pasar**. Si falla, primero el texto.

## 1. DICCIONARIO POR TEMA (`libro.HISTORIAS`) — gramática obligatoria

Para que cualquier valor encaje en cualquier arco:
- `mundo`: CON artículo («la sabana dorada del safari»). Los arcos solo lo usan tras preposición o como sujeto sin adjetivos → **nunca** escribir «el {mundo}», «todo {mundo}» ni «{mundo} lleno/iluminado/entero» en un arco.
- `amigos`: SIEMPRE **masculino plural** con «los ...» (los arcos usan «tristes/cabizbajos/preocupados»).
- `desafio`: cláusula simple en pasado, **minúscula inicial, sin `:` `¡` `!`** — se inserta en «apareció un problema: {desafio}. Nadie sabía qué hacer... nadie, excepto {nombre}».
- `solucion`: pasado, 3ª persona singular, **empieza con verbo** — se inserta en «{nombre} {solucion}» + consecuencia.
- `tesoro`: objeto con artículo («una/un ...»), neutro para nene o nena.
- Tema nuevo ⇒ agregar entrada acá + `tema.json` + **`ia_maestra.png` OBLIGATORIA** (sin referencia el arte sale con personajes random — pasó con princesas; `generar_ilustraciones` con catalogo=True ahora lo rechaza con error claro, y el test lo verifica para los temas publicados). Sumarlo a `TEMAS_CATALOGO` del test y correr el test.

## 2. DISEÑO DE ARCOS (`libro_historias.py`) — misión con hilo

1. **Misión concreta** planteada al principio y resuelta en el clímax. Las últimas páginas NUNCA son relleno («jugaron, miraron estrellas, se despidieron» = PROHIBIDO como cierre genérico).
2. **Esqueleto** (0..16): 0 gancho · 1 transición ({conteo}) · 2 llegada · 3 misión · 4 plan · 5 viaje · 6 obstáculo ({desafio} si aplica) · 7 idea · 8 acción ({solucion}) · 9-10 desarrollo · 11 **clímax** · 12-13 festejo · 14 despedida + {tesoro} · 15 cama + recuerdo sensorial · 16 sueño + **moraleja única** por arco.
3. **Versión corta coherente**: `CORTO_IDX [0,1,3,6,8,11,14,15,16]` debe leerse de corrido — nada de «del otro lado / cuando volvieron / adentro» que dependa de páginas salteadas.
4. **Género neutro** (el motor NO adapta el texto): prohibidos «él/ella», clíticos «lo/la» referidos a {nombre}, adjetivos concordados con el protagonista (contento, emocionado, tranquilo, solito, acurrucado, invitado, pensativo...). Permitidos: «feliz», «con una sonrisa», verbos («se acurrucó»).
5. **Universal**: sin árbol/río/sabana/claro/hojita fuera de tokens — usar «lo más alto de {mundo}», «un tramo angosto», «lucecitas brillantes», «un rinconcito». Tiene que funcionar en monstruos, pintores, astronautas, princesas y lo que venga.
6. El **rescatado/amiguito** es siempre un **nene humano** en las imágenes; en el texto llamarlo «amiguito / el pequeño» (nunca especie).
7. Apto TTS: 55–230 caracteres por página, texto limpio sin puntuación decorativa.
8. Nada de «patas» para el protagonista (es un niño: piernas)... y mejor ni piernas: reescribir.
9. **Comillas: “ ” inglesas, NUNCA « »** — los padres leen «» como «>>» y lo toman por un error. Los arcos pueden escribirse con «» (fuente), pero `libro._capitalizar_frases` las convierte a “ ” en el render/TTS; el test lo verifica.

## 2b. TÍTULO POR HISTORIA (regla explícita — pasó y no debe repetirse)

- **Cada historia tiene SU título** en `libro_historias.TITULOS` y ese título va en: la TAPA (`libro.portada`), la NARRACIÓN de la tapa (`audiolibro._textos_narracion`) y el TÍTULO del visor (manifest `titulo` → `audiolibro.html`). **PROHIBIDO un título global hardcodeado** («La gran aventura de...» quedó solo como fallback del libro de kit legado, sin historia).
- Historia nueva ⇒ agregar su entrada en `TITULOS` (el test exige `set(TITULOS) == set(ARGUMENTOS_LARGO)` y títulos únicos) y que coincida con el label del dropdown de la tienda y de `tienda_audiolibros.PARES`.
- Síntoma del bug histórico: en Productos todos los libros parecían "el mismo" porque todas las tapas decían «La gran aventura de Alex».

## 3. ESCENAS (`libro_ia._ESCENAS_POR_HISTORIA_LARGO`) — 1:1 con el texto

- 17 escenas por historia (idx 2..18) que ilustran EXACTAMENTE lo que dice cada página. Historia nueva ⇒ tabla nueva + test.
- **Poses prohibidas** (inventan la 5ta pata): dar la mano, chocar los cinco, saludar/aplaudir en cuatro patas, «tomados de la mano» con animales. Festejo seguro: sonrisas, saltos, confetti. «de la mano» SOLO entre humanos y aclarando «(un niño, NO un animal)».
- **Adjetivos sobre {protagonista} en escenas**: el género se sustituye al armar el prompt → «una nena ... pensativo» queda mal. Usar «con gesto pensativo», «en medio de», «de cola en el piso» (nunca pensativo/despierto/rodeado/sentado/atento sueltos).
- Protagonista = NENE o NENA humano, PRINCIPAL y prominente, de espaldas/lejos (cara nunca visible); animales secundarios. El nombre lo escribe el motor, NO va en la imagen.
- Solo personajes de la REFERENCIA del tema (nada de leones en superhéroes). Sin texto/números/letras. Encuadre abierto: personajes en el ~60% central, completos, aire en los 4 lados.

## 4. ILUSTRACIONES (gpt-image-2 vía `libro_ia.py`)

- Prompt global ya blindado: patas EXACTAS (4 = 4), cuadrúpedo NUNCA saluda/da la mano/aplaude; solo bípedos erguidos saludan; protagonista niño prominente; solo personajes de referencia; sin texto.
- **CONSISTENCIA DE PERSONAJES ENTRE PÁGINAS (regla explícita, causa raíz encontrada 24-jul-2026 — el bug que peor rindió: pijama verde en una página y azul en la siguiente, protagonistas que cambiaban de cara/ropa/género de página en página, personajes secundarios que se multiplicaban o se inventaban de nuevo cada vez, en "Pequeños artistas", "La invitación mágica", "La entrega importante", "El día de ayudar a todos", "El mapa del tesoro" y "Fútbol")**. Causa: cada página se generaba SOLA, con la única referencia de ESTILO del tema (`ia_maestra.png`) y sin ninguna instrucción de continuidad — el modelo no tenía forma de saber que la página 3 debía verse igual que la 2. Arreglado en `libro_ia.generar_ilustraciones` (mismo mecanismo que ya usaba `aventura_ia.py` para "Elegí tu aventura", generalizado acá):
  - **Referencias encadenadas**: además de `ia_maestra.png`, cada página recibe como referencia de imagen la del PROTAGONISTA (la primera página generada en la corrida cuya escena lo menciona) y la del ELENCO/extras (la primera página que muestra a los personajes secundarios) — todas las páginas siguientes que los vuelven a mostrar copian ESA imagen, no reinventan. Si se regeneran solo algunas páginas de un combo ya cacheado, `_autoancla` busca esas referencias entre las páginas YA generadas en `dest_dir` (no hace falta pasarlas a mano); `ref_protagonista_path`/`ref_elenco_path` fuerzan una imagen puntual ya aprobada.
  - **Instrucción de continuidad en el prompt** (texto, además de la imagen): "es el MISMO personaje de página en página, nunca uno nuevo ni parecido" + "ningún personaje de las referencias aparece más de UNA vez dentro de la misma escena" (ataca también el "se repiten los mismos personajes en una misma imagen").
  - **QA de visión extendido** (`qa_vision_catalogo`): ahora también recibe las referencias de protagonista/elenco y devuelve `duplicado` (mismo personaje dos veces en la escena) e `inconsistente` (diseño/ropa distinto al de la referencia) — cualquiera de los dos regenera la página.
  - **Al pedir arte nuevo de un combo roto, SIEMPRE vaciar el cache viejo primero** (`catalogo_arte/<tema>/<historia>/<genero>/`) para que la corrida arranque de página 0 y las anclas se construyan bien desde el principio; regenerar solo páginas sueltas sobre un combo ya inconsistente perpetúa la inconsistencia.
- **ELENCO FIJO (roles con nombre propio, no "los personajes del tema" genérico)**: si una historia menciona roles recurrentes con identidad propia (p.ej. "el más alto/el más fuerte/el más chiquito" en `ayudar-a-todos`, o "el equipo de 4 amigos" + "el equipo contrario" en `gran-torneo`/fútbol), **la cantidad de roles con nombre propio tiene que ser IGUAL a la cantidad de personajes que realmente dibuja `ia_maestra.png` de ese tema** — si el arco pide 4 roles distintos y la referencia solo tiene 3 personajes, el modelo inventa un 4to cada vez (pasó en "El día de ayudar a todos": el arco pedía alto/fuerte/rápido/chiquito contra solo 3 superhéroes dibujados). Fix: `libro_ia.ELENCO_FIJO[(tema, historia)]` fija la DESCRIPCIÓN FÍSICA exacta de cada rol (debe coincidir con el diseño real de `ia_maestra.png`: pelo, color de traje, accesorios) y se inyecta como `{alto}`/`{fuerte}`/`{chiquito}` en las escenas de `_ESCENAS_POR_HISTORIA_LARGO` de ESE combo — el texto narrado (`libro_historias.py`) sigue usando el nombre de rol genérico (no rompe la regla de texto universal); solo el prompt de IMAGEN, que ya es por-tema, recibe la descripción concreta. Sin entrada en `ELENCO_FIJO`, cae al genérico de siempre (`el más alto de los personajes del tema`) — no rompe temas sin elenco definido. Tema/historia nuevo con roles con nombre propio ⇒ mirar `ia_maestra.png`, contar los personajes reales, y que el arco pida EXACTAMENTE esa cantidad de roles (ajustar el arco en `libro_historias.py` y las escenas en `libro_ia.py` si no coincide — así se corrigió `ayudar-a-todos`, que pedía 4 roles contra 3 personajes: se sacó "el más rápido").
- **NO overpoblar la escena**: aunque no haya un elenco con nombre propio, "los personajes del tema" en una escena son SIEMPRE los mismos 2-4 personajes de la referencia — nunca aparecen personajes sueltos que la escena no pide (pasó en "El mapa del tesoro": nenes de más en los bordes de página que el texto no menciona). Si la escena no nombra explícitamente más personajes, no los agregues al prompt.
- **ESCENARIO COMPLETO (regla explícita — pasó en 57 páginas de 10 libros y no debe repetirse)**: TODA escena lleva piso con textura del tema (pasto/arena/piso del taller/alfombra/césped) Y fondo del lugar (paredes/cielo/ambiente). Los personajes NUNCA flotan en fondo liso blanco/crema. CAUSA RAÍZ: si la referencia del tema es una hoja de STICKERS con fondo blanco (artistas, superhéroes, construcción...), el modelo copia ese vacío — el prompt lo prohíbe explícito («la referencia es SOLO para el diseño de los personajes»). GUARDIA: `libro_ia._piso_blanco` (detector de píxeles, gratis) corre en el QA de cada venta y en los barridos; >45% de la imagen en el color de fondo de las esquinas (claro) = flotando → regenerar. La dedicatoria (fondo claro a propósito) está exenta.
- **PERSONAJES PARADOS SOBRE EL PISO (regla explícita — pasó en aviadores hoja 5)**: cada personaje se apoya ENCIMA del suelo, cuerpo entero, pies sobre la tierra; NUNCA medio enterrado/hundido ni cortado por la línea del piso o del horizonte (se veían pilotos "sepultados hasta la cintura" detrás de una lomita). El QA de borde NO lo agarra (no es el borde de la imagen) → la defensa es el prompt.
- `arte_catalogo` corre el **QA de visión dirigido también en la VENTA** (`qa_vision_catalogo`, con la referencia del tema) sobre las páginas recién generadas + 1 ronda de regeneración — el customizable de $25k tiene la misma protección que el lote.
- **Detector de piso blanco** (`libro_ia._piso_blanco`, píxeles, gratis): franja inferior >50% casi-blanca = suelo sin textura → regenerar. Corre en el QA de venta (salvo la dedicatoria, clara a propósito). Los libros pre-regla se barrieron completos el 2026-07-06 (28 páginas en 5 libros).
- **QA de generación** (`verificar_ilustracion`, gpt-4o-mini): rechazar SOLO defectos graves (texto legible, cuerpo deforme, patas de más/menos, cara cortada por el borde). Ante duda → OK (QA estricto = 3x costo).
- **QA de visión post-lote** (obligatorio antes de mostrar/cachear): revisar cada página por (a) cantidad de patas, (b) protagonista presente y humano, (c) personajes ajenos al tema, (d) rescatado humano. Regenerar solo las que fallan. Después revisión humana (Pablo/Matías) UNA vez por combo.
- **El QA de visión DEBE recibir también la ia_maestra del tema** y la regla «los personajes de la referencia NUNCA son intrusos» + «el nene/nena protagonista NUNCA es intruso» — sin eso tira falsos positivos en cadena (pasó 2 veces: el protagonista humano marcado intruso, y el elefante obrero de construcción marcado intruso).
- **Indicaciones del editor por tema** (`libro_ia.nota_tema`, archivo `temas/<tema>/libro_notas.txt`): se inyectan al final de TODOS los prompts de esa temática. Se editan desde `/dash/libro-admin?token=...&tema=...&historia=...` (grilla de páginas + regeneración por página, que actualiza el CACHE del combo → impacta en todas las ventas futuras).
- **NUMERACIÓN de páginas al reportar (convención de Pablo)**: cuenta la TAPA como "hoja 1" y la dedicatoria como "hoja 2" → su **"hoja N" = índice de render N-1** (hoja 5 → pag_04/idx 4; hoja 16 → pag_15/idx 15). El número del CÍRCULO impreso en la página es idx-1. Verificar SIEMPRE mirando la imagen antes de regenerar (script `fix_pagina.py <tag> <idx>`).
- Arte por pedido en `generar_ilustraciones(client, tema, dest_dir=esc, genero=..., historia=..., catalogo=True, edad=..., verificar=True)`; se cachea en `escenas_dir`. `fin()` usa `_escena_efectiva_path` (NO `override_escena_path`).

## 5. VOZ (ElevenLabs Lizy sobre eleven_v3 — validar SIEMPRE)

- Voz **Lizy** (`rrErIO88ehxTnspOjKvf`) sobre **`eleven_v3` modo Natural (stability 0.5)** con **etiquetas de emoción automáticas y conservadoras** (`audiolibro._etiquetas_v3`): `[whispers]` cuando el texto susurra, `[soft]` en cierres de sueño, `[excited]` en páginas con doble exclamación. Elegido por Pablo en A/B (2026-07-06) contra multilingual_v2. Las etiquetas van SOLO al TTS, jamás al render.
- Key en `/opt/ct3d/backend/config.json → elevenlabs_api_key` (restringida: text_to_speech, sin voices_read). Wireado en `audiolibro.py` (`_EL_MODEL/_EL_SETTINGS`, `tts_mp3`; OpenAI = respaldo).
- OJO v3: los clones profesionales (PVC) NO están optimizados para v3 — si se clona una locutora (plan de voz de marca), evaluar volver a `multilingual_v2` (settings viejos: stability 0.30, style 0.48, speed 0.88).
- NO meter puntuación extra (`…`, `<break>`): entrecorta. Texto limpio de corrido.
- **Verificar 44100 Hz** en el mp3 (= ElevenLabs). 24000 Hz = cayó al respaldo OpenAI → revisar key/timeout.
- **Selector con 2 grupos en la tienda (19-jul-2026, `producto.html` dropdown `kf-voz`)**: "Voces argentinas" (acento rioplatense confirmado en la Voice Library) vs. "Voces neutras" (sin acento marcado) — cada opción tiene preview real en `tienda_static/voces/<key>.mp3` (mismo texto de referencia para las nuevas: "Che, vení que te cuento un secreto..."). Pedido de Pablo para poder escuchar y decidir el default con más libertad, no solo confiar en la descripción del catálogo de ElevenLabs.
  - **Argentinas**: Malena `p7AwDmKvTdoHTBuueGvP` (default recomendado), Lionel `MjtZn5tagxL1RO6w9ER5` (M storytelling), Regis `zR7eV8hMFnxhSSAcCYW0` (M suave), Dante `DzZyY3xqjLUXGaT9wykC` (M joven porteño), Valeria `9oPKasc15pfAbMr7N6Gs` (F joven), Melanie `bN1bDXgDIGX5lw0rtY2B` (F cálida profesional).
  - **Neutras**: Lizy `rrErIO88ehxTnspOjKvf` (default histórico — OJO: es voz nativa española/Latam genérica en el catálogo de ElevenLabs, NO está tageada como argentina, el acento se lograba antes solo por el texto en voseo), Jhenny `EDitztUwd7lban76PAZs`, Gaby `yqTu7PvIL2rV3ubtjNlx` (ElevenLabs) + fable/nova/onyx (OpenAI, respaldo/alternativa neutra histórica).
  - Descartadas tras escuchar: Lalo `XmoCtjPCefjeLDu0eMSl`, Mariana `9rvdnhrYoXoUt4igKpBw`. También evaluadas y descartadas antes: Lucía `yA5jrK1S9cpCAojBYyMu`, Andrea `CDrROTHWaKY3O9vD3F3t`, Isabel `ChvF2eSRaJsHDVJhdmbG` (ver memoria ct3d-audiolibro-voz).
  - Todas con `settings={"stability": 0.5}` (igual que Lizy/Malena) para comparar en igualdad de condiciones. Mecanismo: agregar la key a `_EL_VOCES_ALT` alcanza — `tts_mp3` la rutea sola.

## 6. LARGO POR EDAD y CATÁLOGO

- `catalogo=True` (solo audiolibro): hasta 3 años → 12 págs (9 historia, `CORTO_IDX`); 4+ → 20 págs (17). Kit legado NO usa catálogo.
- Tienda: **customizables** $25.000 (`KIT-LIBRO-AUDIO-<TEMA>`, cliente elige historia) y **no-customizables** (`tienda_audiolibros.py`: historia FIJA por SKU vía PARES, tiers `-C` $15k / `-L` $20k, `aplicar()` inyecta historia+edad server-side). `seed()` crea/actualiza; publicar con el toggle del panel.
- **princesas y futbol ya tienen diccionario** — todo tema del catálogo DEBE tener entrada en `libro.HISTORIAS` (si cae al fallback genérico es un bug).

## 7. PREVIEW y ENTREGA

- Ficha: primeras 6 páginas reales con marca de agua (`?wm=1`) + resto 🔒 (`audiolibro_cfg.paginas`). Admin ve TODO con «Ver libro completo» (dash Productos).
- Email de compra (`tienda_emails.confirmacion_html`): botón al audiolibro + instructivo de biblioteca en `/mi-cuenta`. Se agrega a `tienda_clientes`.
- Visor mobile: controles en 2 filas, botón reinicio (↺), link público.

## 8. FLUJO para generar un combo (y cachearlo)

1. `pytest tests/test_historias_catalogo.py -q` → verde.
2. `generar_ilustraciones(...)` con catalogo=True (respeta reglas + QA por página).
3. QA de visión post-lote (patas / protagonista / intrusos) → regenerar falladas.
4. `audiolibro.crear(data, tema, api_key, escenas_dir=esc, token=...)` → verificar mp3 44100 Hz.
5. Revisión humana UNA vez → queda cacheado y se reusa en cada venta (no se regenera).
6. Preview: `fotos_json` = 6 primeras con `?wm=1`.

## Reglas de oro
- Texto: misión con hilo, género neutro, universal, corto coherente, moraleja única. El test es el guardián.
- **Título: cada historia con SU título** (tapa + narración + visor). Nunca uno global.
- Imagen: 4 patas = 4; nadie da la mano/aplaude en 4 patas; protagonista nene/nena prominente; solo personajes de la referencia; rescatado humano; **escenario completo SIEMPRE** (piso con textura + fondo del lugar — nunca personajes flotando en blanco).
- **Consistencia: cada escena recibe la imagen del protagonista y del elenco de las páginas anteriores del MISMO combo, no solo la referencia de estilo del tema** — es el mismo personaje, con la misma ropa, de página en página; nunca se repite un personaje dos veces en la misma imagen. Roles con nombre propio (alto/fuerte/chiquito, equipo/rival...) = misma cantidad que personajes reales en `ia_maestra.png`, con descripción física fija en `ELENCO_FIJO`.
- Voz: Lizy 0.88, 44100 Hz, texto limpio.
- Generar → revisar → cachear → reusar. Solo se vende lo revisado. Al regenerar un combo roto, vaciar el cache viejo primero (no parchear sobre inconsistencia ya instalada).
- Commit/push en ambos repos SOLO cuando Pablo lo pide.

## Pendiente (backlog de consistencia, detectado 24-jul-2026 — no regenerado todavía)
Mismo bug de raíz (sin referencias encadenadas): confirmado por Claude directamente en `monstruos/aventura` y `artistas/pequeno-maestro`, reportado por Pablo en el resto. Quedan para una próxima pasada, priorizados por Pablo:
- `artistas/pequeno-maestro` ("Pequeños artistas") — **confirmado visualmente, variante nueva del bug**: `ia_maestra.png` de artistas ya trae 2 personajes fijos (nena de colitas + nene de guardapolvo azul) que son "los personajes del tema", NO el protagonista. En las páginas donde la historia pide un protagonista genérico (de espaldas, cara nunca visible) + un "personaje nuevo chiquito y tímido" aparte, el arte generado solo repite esos 2 personajes fijos de siempre — el protagonista no aparece por separado y el rol "nuevo/chiquito" termina siendo la nena de la referencia en vez de un chico distinto. Mismo fix que `ayudar-a-todos`: un `ELENCO_FIJO` para artistas (los 2 de referencia) + dejar que la cadena de anclas (protagonista/elenco) haga de la actual escena en curso un personaje realmente aparte del elenco fijo.
- `monstruos/aventura` ("La invitación mágica"): pijama del protagonista cambia de color y de manga/pantalón corto-largo entre páginas — **confirmado visualmente** (verde pág. 2 → azul pág. 3, mismo combo).
- `aviadores/gran-viaje` ("La entrega importante", tema aviadores): según Pablo el protagonista pierde el traje de aviador/aviadora en varias páginas del medio del libro (no confirmado en el detalle, se ve consistente en las primeras páginas revisadas). Pablo sugiere fijar el género en NENA (ya predomina en el arte existente) para minimizar cuántas páginas hay que regenerar.
- `tesoro` ("El mapa del tesoro"): según Pablo, en el combo que revisó aparecen personajes de más que la escena no pide, y el protagonista debería llevar un uniforme fijo (bombero, según su reporte) que no se sostiene en todas las páginas, y el nene rescatado cambia de ropa entre páginas cuando debería ser la misma (envuelto en la frazada roja al final). OJO al retomar: el combo que Pablo miraba no es necesariamente `campamento/tesoro` (el único cacheado hoy en el repo, y que a simple vista SÍ es consistente) — puede ser un combo `bomberos/tesoro` generado en una venta puntual; ubicarlo primero (o pedirle el link a Pablo) antes de tocar nada.
- `futbol/gran-torneo` ("Los Grandes Juegos"): según Pablo, aparecen varios nenes sueltos en una página y en el resto solo objetos (trofeos/pelotas) — necesita `ELENCO_FIJO` nuevo: equipo de 4 amigos + protagonista con la MISMA camiseta todo el libro, rival con otro color; ver `ia_maestra.png` de futbol para fijar los diseños antes de escribir el dict.
