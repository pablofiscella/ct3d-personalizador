# Sistema de Kits Personalizables — Temas, Editor y Tienda

> Estado: junio 2026. Documenta el personalizador multi-temática (`/root/ct3d-personalizador`)
> y su integración con la tienda propia (`/opt/ct3d`, `casatridimensional.com.ar`).
> El negocio **migró de WordPress/WooCommerce a e-commerce propio**: el plugin WP quedó obsoleto.

---

## 1. Panorama

El cliente entra a la ficha de un producto kit en la tienda, **diseña su tarjeta en un editor
embebido** (elige edad, escribe datos, mueve textos, cambia tipografía/color/iconos), y al pagar
recibe un **ZIP con las 7 piezas** del kit en PDF (300 DPI), generadas con su personalización y
**el tema del producto**.

```
casatridimensional.com.ar/producto/<slug>   (tienda Flask, /opt/ct3d/backend/tienda.py)
   └─ <iframe> kit.casatridimensional.com.ar/cliente?tema=<TEMA>   (editor, cliente.html)
         └─ postMessage {tema, edad, data, over}  → form del producto → carrito → pago
                └─ webhook pago → tienda_kit.generar(tema del PRODUCTO) → ZIP 7 PDFs
```

Servicio del kit: `ct3d-kit.service` (Python stdlib + Pillow) en `localhost:8787`, público por
Cloudflare en `kit.casatridimensional.com.ar`. Reiniciar tras tocar `.py`:
`systemctl restart ct3d-kit.service`. `cliente.html` se sirve en vivo (no requiere reinicio).

---

## 2. Temas (`temas/<id>/`)

Temas activos: **safari** (base, "Un Añito Salvaje") + 8 nuevos: `construccion`, `monstruos`,
`aviadores`, `bomberos`, `artistas`, `campamento`, `superheroes`, `circo`.

Estructura de un tema:
```
temas/<id>/
  tema.json              # config: piezas, campos de texto, bloque "kit"
  invitacion_{1,2,3}.png # fondo de la invitación por edad (1500×2100)
  afiche_{1,2,3}.png     # fondo del afiche por edad (1728×2456)
  layouts/               # posiciones guardadas desde el editor admin (opcional)
  recortes/              # SOLO safari: cutouts (animalitos/números). Los temas nuevos NO tienen.
```

> Las 8 láminas nuevas vienen de `Downloads/Animalitos/Tarjetas varias/_Laminas_base/` (1060×1484,
> reescaladas al subir). El afiche sale algo blando; para calidad imprenta conviene regenerarlas en alta.

### tema.json
```jsonc
{
  "id": "construccion",
  "nombre": "Construcción — ¡A Construir!",
  "edades": [1, 2, 3],
  "kit": {                         // ← usado por las piezas del ZIP (piezas.py)
    "accent": "#E07B1E",           // color principal (nombre, lemas, marcos)
    "ink":    "#5B4636",           // color de textos secundarios
    "font":   "Fredoka-VF.ttf",    // tipografía display del tema
    "lema":   "¡Cumplo {edad}!",   // frase en topper/cupcakes/etiquetas
    "titulo": "El cumple de"       // título en el topper
  },
  "piezas": {
    "invitacion": { "size": [1500,2100], "bgimage": "invitacion_{edad}.png",
                    "layout_file": "layouts/invitacion.json", "text": [ /* campos */ ] },
    "afiche":     { "size": [1728,2456], "render_scale": 1.0, "bgimage": "afiche_{edad}.png", "text": [...] }
  }
}
```

### Campos de texto (`text[]`)
Cada campo: `id, tpl, font, size, color, x, y, anchor, maxw` (+ opcionales). `x/y/maxw` en fracciones.
Flags nuevos:
- `editable` (bool) — lo edita el cliente.
- `toggleable` (bool) — el cliente puede **incluirlo u ocultarlo**.
- `iconable` (bool) + `icon` (str) — admite **icono** con variantes (default en `icon`).
- `adopts_if_empty` — toma la posición de otro campo si ese está vacío.

Campos típicos de la invitación: `titulo`, `nombre`, `edad` (`¡Cumplo {edad}!`),
`fecha`(icon calendar), `hora`(icon clock), `lugar`(icon pin), `direccion`, `rsvp`.

---

## 3. Editor del cliente (`cliente.html`)

Canvas en JS vanilla. Carga `/cliente/layout?tema=` (campos + catálogos de fuentes e iconos) y
`/cliente-bg.png` (fondo con marca de agua). Capacidades:

- **Edad** numérica libre (1–99) → arma `¡Cumplo N!`, editable, con checkbox **incluir**.
- **Texto sugerido** precargado por campo; el cliente lo edita o lo deja.
- **Incluir/ocultar** por dato (chip "INCLUIR").
- **Iconos** en fecha/hora/lugar con variantes: calendar/calendar2, clock/clock2, pin/pin2 (selector por dato).
- **Color**, **tamaño**, **grosor**, **tipografía** por texto (al tocar un texto en el lienzo).
- **Alineación** izq/centro/der por campo, y **por grupo** (barra "ALINEAR DATOS": fecha/hora/lugar/
  dirección/teléfono se alinean juntos) + **"Mover juntos"** (al arrastrar uno se mueven todos).

La personalización viaja por **postMessage** al contenedor:
`{type:'ct3d-kit', payload:{tema, edad, data:{...}, over:{...}}}`. `confirm:true` al tocar "Confirmar".

### `over` (overrides por campo) — lo que mezcla el motor
`over[id] = {x, y, size, maxw, wght, font, color, icon, hidden, text, anchor}`
- `font`/`icon` se validan contra catálogo. `hidden` oculta. `text` pisa el `tpl`. `anchor` (lm/mm/rm…).

---

## 4. Motor (`generador.py`)

`render(data, spec)` → dibuja el fondo + los textos (con `_effective_texts` = spec + layout guardado),
aplica `adopts_if_empty`, mezcla `data["_over"]`, y dibuja. `draw_text` posiciona icono+texto según
la alineación (l/m/r). `draw_icon` tiene las 6 variantes. Catálogos: `FONTS_CATALOG`, `ICONS_CATALOG`.
`_hex_rgb` parsea colores del cliente.

---

## 5. Piezas del kit (`piezas.py`) — 7 piezas por tema

`piezas_de(tema)` decide el camino con **`has_recortes(tema)`**:
- **safari** (y cualquier tema con `recortes/` propios) → builders originales (cutouts).
- **temas sin recortes** (los 8 nuevos) → builders `*_l` que arman las piezas **desde la lámina**
  (`_band()` recorta la franja de personajes) + colores/fuente/lemas del bloque `kit`.

Piezas: `1_invitacion`, `2_cartel`(afiche), `3_topper_torta`, `4_cupcake_toppers`,
`5_etiquetas_botellita`, `6_tags_souvenir`, `7_banderines`. `generar_kit()` arma el ZIP.
**Safari quedó intacto** (su path no se tocó).

---

## 6. Integración con la tienda (`/opt/ct3d`)

Ver también `docs/TIENDA-KITS.md` en ese repo. Resumen:

- Un producto es **kit** si su `ml_id` empieza con `KIT-` (`tienda_catalogo.es_digital`).
- **Convención `KIT-<TEMA>`** → `tienda_catalogo.tema_de(ml_id)` (ej. `KIT-CONSTRUCCION` → `construccion`;
  alias `KIT-ANITO-SALVAJE` → `safari`). Expuesto como `p.tema`.
- `producto.html`: el iframe del editor carga **`?tema={{ p.tema }}`** (antes estaba fijo en safari).
- `tienda_pago._generar_kits`: genera con el **tema del PRODUCTO** (server-side, anti-tamper), no con
  el que mande el cliente.
- **8 productos kit sembrados ocultos** (`KIT-CONSTRUCCION`, …, `KIT-CIRCO`), precio placeholder $5000,
  `mostrar_en_tienda=0`. Para publicar: dashboard → Productos → precio + thumbnail + "mostrar en tienda".
- Editor embebido ensanchado (breakout CSS en `store.css`: `.product--kit .product-media-col` →
  `min(1440px,95vw)`; bump `store.css?v=`).

---

## 7. Operar / agregar un tema

1. Subir `invitacion_{1,2,3}.png` + `afiche_{1,2,3}.png` a `temas/<id>/` (o por el panel `/dash`).
2. Crear `tema.json` (copiar uno nuevo de ejemplo; setear `kit` + campos). El generador local del
   repo de las láminas (`_tools/build_temas.py`) produce tema.json + imágenes para los 8 temas.
3. Crear el producto en la tienda con `ml_id = KIT-<TEMA>` (mismo `<TEMA>` que la carpeta), precio,
   thumbnail y `mostrar_en_tienda=1`.
4. (Opcional) Afinar posiciones en el editor admin (`/editor`).

Deploy: cambios en `.py` → `systemctl restart ct3d-kit.service`. `cliente.html`/`tema.json`/imágenes →
en vivo. CSS de la tienda → bump `store.css?v=`. Git: `ct3d-personalizador` y `ct3d` se pushean
(timer diario 05:00 o `git push` manual).
