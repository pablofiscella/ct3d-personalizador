# Rompecabezas web — rompecabezas INTERACTIVO

> Producto digital vivo (tipo `rompecabezas-web`): las escenas del tema hechas
> rompecabezas JUGABLES en el navegador, entregadas igual que el audiolibro y
> el cuaderno interactivo (`/armar/<token>/`, aparece en Mi biblioteca).
> Creado 11-jul-2026 a pedido de Pablo: "hacer lo mismo que hiciste con el
> cuaderno interactivo pero con rompecabezas".

## Qué es

Una web app táctil por temática, SIN datos para completar (Pablo 11-jul-2026:
no pide nombre ni edad): hasta 6 rompecabezas por tema (el fondo IA dedicado
del puzzle imprimible + escenas del libro) y en cada uno se elige el nivel —
4 · 6 · 12 · 20 · 30 · ~50 piezas, siempre los mismos para toda compra. El
tope real es 48 (6x8, fotos 3:4) o 49 (7x7, cuadradas) — los conteos ≤50 con
piezas CUADRADAS; 50 exacto solo factoriza 5x10 (piezas 2:1). El player
muestra el conteo real. El IMPRIMIBLE (rompecabezas.py) usa las MISMAS 6
escenas con grillas progresivas 4→48 (GRILLAS_SET), cada hoja con su bandeja.

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

## Demo por tema (dash + PÚBLICO)

Cada tema tiene un rompecabezas de MUESTRA con token fijo `demo-<tema>`
(edad 3 → lista todos los niveles): lo crea/actualiza el botón **🎮
Rompecabezas web** de la tarjeta del tema (`POST /dash/rompe-demo?tema=X`,
síncrono, sin IA) y también se refresca solo al final del job de **⚡ Armar
TODO el tema** (así el demo siempre refleja el arte vigente).

**Demo PÚBLICA "Probalo gratis" (17-jul-2026):** ruta pública `GET
/probar/rompecabezas/<tema>` (helper `servicio._demo_rompecabezas_token`, sin
admin) que crea el `demo-<tema>` si falta y redirige a `/armar/demo-<tema>/`.
La abre el botón **"🧩 Probalo gratis"** de la ficha en la tienda (aparece en
`rompecabezas-web` y `rompecabezas-foto`, apunta al tema del producto). En
**modo demo** (el player detecta `location.pathname` con `/armar/demo-`) se
deja armar solo la **MITAD** de los rompecabezas (`ceil(n/2)`); el resto van
con candado 🔒 + CTA de compra + un banner. **Gateado a la URL demo** → los
links YA VENDIDOS (`/armar/<token-aleatorio>/`) quedan idénticos (sin candado).

## Probar local

```bash
python3 -c "import rompecabezas_web as rw; print(rw.crear({'nombre':'Sofía','edad':'5'},'safari'))"
# servir: CT3D_PORT=8791 CT3D_API_KEY=test python3 servicio.py
# abrir http://localhost:8791/armar/<token>/
```

## Integración a la tienda — ✅ HECHO (ya se vende, $9.500)

El rompecabezas-web ya está EN VENTA (SKUs `KIT-ROMPECABEZAS-WEB-<TEMA>`, con
ficha, precio, editor de foto y el botón "Probalo gratis"). El patch de abajo
quedó como referencia histórica de lo que se aplicó.

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


## El candado por cuenta (20-ago-2026)

Un token de `/armar/` puede tener **dueño**: un mail anotado en su `manifest.json`. Si lo
tiene, el link **sólo abre para esa persona**; si no lo tiene, abre con la sola URL, como
siempre.

**El candado es opt-in y eso no es un detalle.** Todo lo vendido por Mercado Libre son
links sin dueño. Si el candado aplicara a todos, cada cliente que ya pagó se quedaría
afuera de un día para el otro.

### Por qué este producto lo necesita y el kit no

El kit se entrega como un archivo: una vez bajado ya es del comprador y no hay nada más
que cuidar. El rompecabezas web es un **link vivo** — se juega en nuestro servidor, cada
vez, para siempre. Un link vivo se reenvía y sigue andando: no se "gasta". En Mercado
Libre eso no importaba (el link se lo mandamos a una persona por mensaje), pero en Etsy el
comprador se **baja** el archivo de entrega, y ese archivo se reenvía.

Pedido de Pablo, textual: *«Tiene que haber alguna forma asociada al mail. Si se loguea en
casatridimensional tiene acceso y no otros»* y *«con cuenta de google, no tiene que crearse
una cuenta para casatridimensional»*.

### Cómo se pone

```python
rompecabezas_web.crear({"nombre": "Emma", "idioma": "en",
                        "dueño": "ana@gmail.com"}, tema)
```

El mail va al `manifest.json`, **nunca** al `data.json`: ese se lo sirve el motor al
navegador para que lo lea el player, así que todo lo que se escriba ahí es público.

### Las dos puertas

1. **La cuenta de la tienda** (`ct3d_cliente`): es una cookie de
   `.casatridimensional.com.ar`, así que llega también a `kit.*` y el motor la valida solo
   (`acceso.email_de_la_tienda`). Se valida **entera** —firma y vencimiento—, no que
   exista: el resto del motor mira `"ct3d_cliente=" in cookie` porque ahí decide un banner,
   y acá decide un acceso.
2. **Google** (`POST /acceso/google`), para el comprador de Etsy que no tiene cuenta
   nuestra. **No se le crea ninguna**: el mail sólo sirve para reconocerlo. El ID token se
   verifica contra Google y se compara el `aud` — eso último es lo único que Google no
   puede chequear por nosotros, y sin eso un token de cualquier otra app entra igual.

### Tres cosas que hay que saber antes de tocar esto

- **El candado va antes de servir los archivos, no sólo la página.** El producto son el
  `data.json` y los `p*.jpg`, que se piden aparte: con el candado sólo en el HTML, alcanza
  con pedir los archivos derecho. Hay un test que mueve el candado al lugar equivocado para
  comprobar que se nota.
- **Los archivos con dueño van `Cache-Control: private, no-store`.** Cloudflare cachea
  `.jpg` **por extensión**, sin necesidad de ninguna regla (al revés que `/preview`, que sí
  necesitó una porque su ruta no tiene extensión). Con `public`, la primera visita del dueño
  dejaba las imágenes servidas en el borde para cualquiera con el link.
- **Un archivo suelto recibe 403 seco, no la pantalla de login.** El `<img>` no es una
  persona: mostrarle un HTML de login a una etiqueta de imagen no sirve para nada. La página
  sí la pide una persona, y a ella se le muestra la puerta (`acceso.pagina_login`), en el
  idioma del token.

### La entrega por Etsy

`/etsy/juego` (HTML en `etsy_juego.html`) → el comprador entra con Google, pone su número
de orden y `POST /etsy/generar-juego` crea el rompecabezas a su nombre. El mail se pide
**antes** de generar: al revés quedaría un link sin dueño ya entregado, y ése no se puede
cerrar nunca más sin romperle el producto a quien pagó.

`etsy_pedidos.validar(orden, tipo="rompecabezas-web")` exige que la orden incluya una
publicación de este producto, según `etsy_productos.json`. **Mientras esa lista esté vacía,
la entrega falla cerrada**: es lo correcto hasta que las publicaciones existan.

Tests: `tests/test_acceso.py` y `tests/test_etsy_entrega.py`.
