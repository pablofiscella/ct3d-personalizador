# Motor de generación automática de piezas con IA — Diseño

**Fecha:** 2026-06-28
**Repo:** `ct3d-personalizador`
**Estado:** Diseño aprobado (pendiente revisión final del spec)

## 1. Contexto y problema

Hoy, agregar un tema nuevo al motor de kits implica que un humano **dibuje a mano** las
piezas (invitación, cartel, toppers, etiquetas, banderines, etc.) y las suba como PNG al
panel `/dash`. El motor (stdlib + Pillow, sin dependencias pesadas) ya está pensado para
**consumir esas piezas como imágenes**: las toma de `temas/<tema>/extras/` (y de los slots
`invitacion_*`/`afiche_*`), les superpone el texto del cliente con layouts de coordenadas
fraccionales, arma el ZIP y lo publica a la tienda (`facturas_api`, servicio aparte en
`:8091`).

El objetivo es **reemplazar al "humano que dibuja"** por un motor que, a partir de unos pocos
**personajes** del tema, genere automáticamente **todo el catálogo de piezas vendibles** con
estilo consistente, "casi automático y sin errores". El pipeline aguas abajo (armado de kit,
overlay de texto, publicación) **no cambia**.

## 2. Objetivo

Subir los personajes de un tema → el sistema genera todas las piezas/imágenes vendibles
(piezas de fiesta **y** packs de actividades) → se revisan en un panel → se publican. El
costo de generación es **una sola vez por tema**, no por venta.

## 3. Alcance v1

**Incluye** un motor unificado que cubre las dos familias de producto:

- **Piezas de fiesta** (catálogo actual del kit): invitación, cartel/afiche, topper de torta,
  toppers de cupcakes, etiquetas de botellita, banderines, stickers, separadores, cajita
  sorpresa, wrappers de cupcakes, tarjetas de agradecimiento.
- **Packs de actividades** (cuaderno): portada, laberinto, memotest, encontrar diferencias,
  hojas para colorear, unir puntos, buscar sombras, contar animales, certificado, etc.
  Reusa el generador algorítmico ya existente (`cuaderno.py`).

**No incluye (fuera de alcance, va en specs posteriores):**

- El flujo de "agregar opcionales al pedido inicial por WhatsApp" → vive en la tienda
  (`facturas_api`), otro servicio y otro spec.
- Piezas nuevas fuera del catálogo actual (se pueden sumar después).

## 4. Principio central: "OpenAI solo ilustra; el código hace lo determinístico"

La división de trabajo es la clave de la confiabilidad y del costo bajo:

| Responsabilidad | Quién la hace |
|---|---|
| Texto exacto (nombre, fecha, edad, lugar) | **Motor** (overlay Pillow, layouts existentes) |
| Puzzles/actividades (laberinto, sudoku, memotest, unir puntos, sopa de letras) | **Motor** (algorítmico — `cuaderno.py` ya lo hace) |
| Composición y export de cada hoja a PNG/PDF independiente | **Motor** (compositor) |
| Ilustraciones (personajes, decoración, fondos, estilo) | **OpenAI Images** (`gpt-image-2`) |
| Decisión de qué va en cada pieza (planificación) | **GPT texto** (paso 1, devuelve JSON) |

Por qué: los modelos de imagen son excelentes ilustrando pero **poco confiables con texto
exacto** y con geometría precisa (un laberinto resoluble, un sudoku válido). Sacar esas dos
cosas del modelo elimina los errores típicos de raíz, y hace que la IA genere **pocas
ilustraciones** en vez de una imagen completa por hoja → mucho más barato y escalable.

## 5. Arquitectura

### 5.1 Componentes nuevos

- **`ia_kit.py`** — Cliente de OpenAI y orquestador de generación.
  - `planificar(tema, familia) -> dict` — Paso 1: llama a un modelo de **texto** (GPT) con el
    tema + catálogo y devuelve un **JSON de composición** (qué personaje/decoración/variante va
    en cada pieza). Plantilla de salida fija y validada contra un schema.
  - `generar_maestra(tema, personajes) -> Image` — genera la **imagen maestra de estilo** del
    tema (una sola), que sirve de ancla de consistencia para el resto.
  - `generar_ilustracion(tema, personajes, maestra, pieza_spec, edad=None) -> Image` — genera
    la ilustración de una pieza, referenciando *personajes + maestra*.
  - Lee `OPENAI_API_KEY` de env (junto a las demás vars en `servicio.py:29-32`).

- **`prompts_piezas.py`** (o tabla dentro de `ia_kit.py`) — Catálogo de prompts por pieza.
  Cada entrada define: formato/tamaño, composición, instrucción explícita de *"dejá zonas
  vacías/limpias para el texto"*, y un **bloque de estilo fijo** (hex de la paleta del tema
  `accent`/`ink`, tipografía/feel, "flat vector", tratamiento de fondo). Solo varía la línea
  de sujeto por pieza → estilo uniforme.

- **Compositor** — Toma la ilustración generada + el JSON de composición + (si aplica) la
  actividad algorítmica, coloca personajes/decoración y produce el PNG final de la pieza.
  Para piezas del kit se apoya en lo que ya hace `generador.py`/`piezas.py`; para actividades
  se apoya en `cuaderno.py`.

### 5.2 Reuso (sin cambios)

- **`quitar_fondo.py`** — `gpt-image-2` **no** soporta fondo transparente nativo; las piezas
  de recorte (toppers, stickers, banderines) se generan con fondo y se les quita acá.
- **`productos.generar` / `piezas.generar_kit`** — armado del kit + ZIP.
- **`cuaderno.py`** — generación algorítmica de actividades + solucionario.
- **`/dash/publicar` → `/kit-admin/publicar`** — publicación a la tienda.

### 5.3 Endpoints nuevos (en `servicio.py` `do_POST`, guardados por `_admin_ok()`)

- `POST /dash/ia-generar?tema=&familia=` — corre el flujo completo (planificar → maestra →
  ilustraciones → compositor → quitar_fondo) en background. Deja los borradores en staging:
  `temas/<tema>/ia_draft/`.
- `POST /dash/ia-regenerar?tema=&pieza=&edad=` — regenera una sola pieza.
- `POST /dash/ia-aprobar?tema=` — mueve los borradores aprobados de `ia_draft/` a
  `extras/` + slots `invitacion_*`/`afiche_*`. A partir de ahí el pipeline existente corre igual.
- (Lectura) estado del borrador para la grilla de preview.

### 5.4 Panel

Sección nueva en `dash.html`: botón "Generar con IA", grilla de preview de los borradores,
botones **aprobar** (todo) y **regenerar** (por pieza). Un único gate humano.

## 6. Flujo de datos (end to end)

1. Admin sube los **personajes** (reusa `/dash/upload` slots `animal_*` → `temas/<tema>/recortes/`).
2. `POST /dash/ia-generar` → `ia_kit.planificar()` (GPT texto → JSON de composición).
3. `ia_kit.generar_maestra()` (1 imagen).
4. Por cada pieza del catálogo: `ia_kit.generar_ilustracion()` referenciando personajes + maestra.
   - **Decisión "mixto" de edades:** invitación y cartel se generan **×3** (una por edad, con el
     número ilustrado); el resto de las piezas se genera **×1** (el número de edad lo pone el
     motor como texto).
5. Validación + reintento por imagen; piezas de recorte pasan por `quitar_fondo`.
6. Compositor arma cada hoja y la guarda en `ia_draft/` con nombre propio
   (`invitacion_1.png`, `topper.png`, `01-portada.png`, …). **Una imagen por llamada a OpenAI**
   (la API no devuelve packs nombrados; el código administra nombre y guardado).
7. Admin revisa la grilla, regenera lo que no le gusta, **aprueba**.
8. `ia-aprobar` mueve a `extras/`/slots → pipeline existente arma kit + publica.

## 7. Modelo OpenAI y parámetros

- **Modelo de imagen:** `gpt-image-2` (flagship, abr-2026; `gpt-image-1` se deprecia oct-2026).
- **Endpoint:** `POST /v1/images/edits` (multipart), **hasta 16 imágenes de referencia** →
  se mandan los personajes + la maestra en cada llamada.
- `input_fidelity: "high"` para mantener la identidad de los personajes.
- **Tamaños:** `gpt-image-2` admite resoluciones casi arbitrarias (borde ≤ 3840px, múltiplos de
  16, ratio ≤ 3:1). Invitación/cartel/afiche → vertical tipo A4 (ej. 1536×2176); toppers/
  etiquetas → cuadrado.
- **Transparencia:** no nativa en `gpt-image-2` → matar fondo con `quitar_fondo`.
- **Texto:** OpenAI no escribe texto del cliente; lo overlaya el motor.
- **Calidad:** `medium` para borradores de preview; `high` para la tanda final aprobada.
  Opción **Batch API** (50% off, async) para la tanda final.
- **Consistencia:** no hay `seed`. La técnica es generar primero la **maestra** y pasarla como
  referencia a cada pieza, + bloque de estilo fijo reusado textualmente.

## 8. Costo por tema (estrategia "mixto")

Invitación ×3 + cartel ×3 + 9 piezas ×1 + 1 maestra ≈ **16 imágenes/tema**:

- Borrador (medium): **≈ US$0,80/tema**
- Final (high): **≈ US$2,90/tema** (≈ **US$1,45** con Batch API)

Costo de **una sola vez por tema**; el tema se vende infinitas veces. (Cifras a confirmar con
la calculadora oficial de OpenAI cerca del lanzamiento.)

## 9. Confiabilidad ("casi automático y sin errores")

- Texto siempre exacto (motor) — no depende de la IA.
- Puzzles siempre válidos e imprimibles (algoritmo) — no depende de la IA.
- **Validación por imagen** (tamaño, ratio, transparencia correcta) + **reintento automático**
  ante error de API o imagen inválida.
- **Un único gate** de aprobación visual antes de publicar; regenerar por pieza.
- **Rate limits** (IPM por tier de OpenAI): concurrencia propia limitada + cola para no
  exceder el tier; tanda final por Batch API (async, encaja con la latencia alta de `high`).

## 10. Manejo de errores

- Fallo de API / timeout → reintento con backoff (N intentos); si persiste, la pieza queda
  marcada "falló" en la grilla para regenerar a mano (no bloquea las demás).
- Imagen inválida (tamaño/ratio fuera de lo esperado) → descartar y regenerar.
- Falta `OPENAI_API_KEY` → error claro en el panel, no se arranca la tanda.
- Staging aislado (`ia_draft/`): nada toca `extras/`/slots hasta que el admin aprueba, así una
  tanda a medias nunca rompe un tema ya publicado.

## 11. Testing

- **Unit (sin red):** construcción de prompts (bloque de estilo fijo + sujeto por pieza),
  validación del JSON de composición contra schema, validación de imagen (mock), mapeo
  pieza→tamaño, ruteo de piezas de recorte a `quitar_fondo`.
- **Integración con OpenAI mockeado:** flujo `ia-generar` completo con un cliente OpenAI falso
  que devuelve PNGs de prueba; verifica nombres de archivo, conteo (×3 vs ×1), staging.
- **Smoke real (manual, opt-in):** una corrida real en `medium` sobre un tema de prueba,
  detrás de una flag, para no gastar en CI.
- Reusar la suite existente del motor para confirmar que el pipeline aguas abajo no se rompe.

## 12. Riesgos / a revisar cerca del lanzamiento

- **Deprecaciones de OpenAI** (varias para dic-2026): re-verificar el id de modelo vigente.
- **Transparencia** de `gpt-image-2` sigue sin ser nativa: confirmar que `quitar_fondo` da
  calidad suficiente en toppers/stickers, o evaluar `gpt-image-1.5` (ojo su deprecación).
- **Precio exacto por imagen:** validar con la calculadora oficial con los tamaños reales.
- **Tier de rate limit:** asegurar Tier 2+ antes de tandas grandes.
