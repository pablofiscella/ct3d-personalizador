# Rompecabezas web — rompecabezas INTERACTIVO

> Producto digital vivo (tipo `rompecabezas-web`): las escenas del tema hechas
> rompecabezas JUGABLES en el navegador, entregadas igual que el audiolibro y
> el cuaderno interactivo (`/armar/<token>/`, aparece en Mi biblioteca).
> Creado 11-jul-2026 a pedido de Pablo: "hacer lo mismo que hiciste con el
> cuaderno interactivo pero con rompecabezas".

## Qué es

Una web app táctil personalizada (nombre + edad + tema): hasta 6 rompecabezas
por tema (el fondo IA dedicado del puzzle imprimible + escenas del libro).
TODAS las bandas llegan al tope de ~50 piezas (pedido de Pablo 11-jul-2026);
el tope real es 48 (6x8, fotos 3:4) o 49 (7x7, cuadradas) — los conteos ≤50
con piezas CUADRADAS; 50 exacto solo factoriza 5x10 (piezas 2:1). El player
muestra el conteo real.

| Banda | Edad | Niveles (piezas) |
|---|---|---|
| mini | ≤3 | 4 · 6 · 12 · 20 · 30 · ~50 |
| media | 4-5 | 6 · 12 · 20 · 30 · ~50 |
| grande | 6+ | 12 · 20 · 30 · ~50 |

**El mismo principio del motor:** las formas de las piezas las genera el código
— `rompecabezas._bordes_grilla` (knobs Bézier con bulbo más ancho que su
cuello y jitter determinístico, la MISMA receta del imprimible) exportadas a
`data.json` como polilíneas unitarias; el player solo las mapea a su celda
(contrato: cada borde va de (0,0) a (1,0), perpendicular escalada por celda
× 0.9). El test `test_piezas_particionan_la_imagen` verifica por shoelace que
las piezas particionan EXACTAMENTE la imagen (sin huecos ni solapes).

**Principios del player (los del cuaderno interactivo):** drag con imán (32%
de la celda), CERO fail states (una pieza mal soltada queda donde está, nunca
castiga), tablero-bandeja con contornos + fantasma de la imagen (como la
página-bandeja del imprimible), botón «Espiar» (mantener apretado), progreso
guardado por nivel en localStorage (cerrar y seguir después), estrellas por
nivel, festejo corto con auto-avance al nivel siguiente, sin timers, voseo.

## Archivos

- `rompecabezas_web.py` — generador: `crear(data, tema, token=None)` arma
  `rompecabezas_web/<token>/` (gitignored): `data.json` (paleta compartida con
  actividades_web + puzzles + bordes), `p*.jpg`/`t*.jpg` (imágenes y thumbs,
  cover-crop a 3:4 / 1:1 / 4:3 según el arte — NUNCA estira), `masco.png`
  (recorte limpio del tema para header/festejo; opcional), `portada.jpg`
  (cover 900×1200 de Mi biblioteca: el arte con los cortes encima),
  `manifest.json`. También `estado()/html()/archivo()/preview_mock()`.
- `rompecabezas_player.html` + `rompecabezas_player.js` — el visor (canvas +
  pointer events, Path2D por pieza). Se sirven DESDE EL REPO en cada request
  (una mejora llega a todos los links vendidos); solo `data.json` + assets
  viven en el token. Rutas relativas → SIEMPRE bajo `/armar/<token>/` con
  barra final (sin barra → 301).
- `servicio.py` — ruta `GET /armar/<token>[/asset]`; branch `rompecabezas-web`
  en `POST /api/generar` (síncrono, sin IA → rápido; devuelve `download_url`);
  `/api/al-info` también reconoce estos tokens (canje en la tienda).
- `productos.py` — `TIPOS["rompecabezas-web"]` (campos nombre+edad, preview =
  portada) y `PERSONALIZADAS`.
- `tests/test_rompecabezas_web.py` — 11 tests (partición exacta de piezas,
  bordes bien formados y determinísticos, whitelist de assets, bandas).

## Imágenes por tema

`_imagenes_tema`: `overrides/fondos/rompecabezas.png` (el arte dedicado del
puzzle imprimible) + escenas de `overrides/libro/*.png` espaciadas parejo,
hasta 6. Todo arte YA REVISADO que vive en el repo — acá no se genera IA.
Los 12 temas del catálogo generan OK (validado 11-jul-2026: 6 puzzles y
mascota cada uno, data.json 33-65KB, ~1.3MB por token).

## Demo por tema (dash)

Cada tema tiene un rompecabezas de MUESTRA con token fijo `demo-<tema>`
(edad 3 → lista todos los niveles): lo crea/actualiza el botón **🎮
Rompecabezas web** de la tarjeta del tema (`POST /dash/rompe-demo?tema=X`,
síncrono, sin IA) y también se refresca solo al final del job de **⚡ Armar
TODO el tema** (así el demo siempre refleja el arte vigente).

## Probar local

```bash
python3 -c "import rompecabezas_web as rw; print(rw.crear({'nombre':'Sofía','edad':'5'},'safari'))"
# servir: CT3D_PORT=8791 CT3D_API_KEY=test python3 servicio.py
# abrir http://localhost:8791/armar/<token>/
```

## Pendiente para VENDERLO (tienda, repo /opt/ct3d) — patch exacto

La entrega motor→tienda ya funciona sola (la orden guarda el `download_url`
que devuelve `/api/generar`). Falta que la tienda lo trate como visor —
mismo patch que se aplicó para actividades-web:

1. `backend/tienda_clientes.py`
   - `_VISORES`: agregar `"rompecabezas-web"`.
   - Cover: para `rompecabezas-web` el cover es `url + "portada.jpg"` (la url
     ya termina en `/`) — misma rama que actividades-web.
   - `categoria_libro`: mapear `rompecabezas-web` → el chip que use
     actividades-web ("juegos"/"libros").
   - `extraer_token`: aceptar también links `/armar/<token>`.
2. `backend/tienda_catalogo.py` `_KIT_TIPOS` y su ESPEJO
   `tienda_kit_admin.TIPOS`: agregar `"rompecabezas-web"` (SKUs tipo
   `KIT-ROMPECABEZAS-WEB-SAFARI`) + precio en `tienda_kit_admin` (referencia:
   actividades-web = 14900) + label "Rompecabezas Interactivo — Juegos Web".
3. `backend/tienda_templates/mi_cuenta.html`: CTA por tipo →
   `rompecabezas-web` = "🧩 Armar" (+ frase de regalo).
4. Publicar el producto en la tienda (ficha + precio) — decisión de Pablo.

## Ideas v2 (no bloquean el lanzamiento)

- Sumar el rompecabezas como carta DENTRO del cuaderno interactivo (menú de
  actividades) reusando el mismo data.json — un solo motor, dos entradas.
- Rotación de piezas como modo "difícil" opcional (6+) — la investigación de
  UX infantil recomienda SIN rotación por defecto.
- Foto propia del cliente como puzzle extra (subida en el editor de compra).
- PWA offline (service worker) para jugar sin señal.
