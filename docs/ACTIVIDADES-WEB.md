# Actividades web — cuaderno de actividades INTERACTIVO

> Producto digital vivo (tipo `actividades-web`): las actividades del cuaderno
> imprimible pero JUGABLES en el navegador, entregadas igual que el audiolibro
> (`/act/<token>/`, aparece en Mi biblioteca). Creado 10-jul-2026 a pedido de
> Pablo: "la mejor estética y las mejores actividades… que además de servir
> lúdicamente sirva educativamente".

## Qué es

Una web app táctil personalizada (nombre + edad + tema) con hasta 15 juegos:

| Juego | Skill | Bandas |
|---|---|---|
| ¿Cuántos hay? (contar tocando, suena do-re-mi) | numeración 1-a-1 | todas |
| ¡A pintar! (balde sobre line-art IA del tema) | creatividad/motricidad | todas |
| Memotest (personajes del tema) | memoria de trabajo | todas |
| Sombras (drag & snap a la silueta) | percepción visual | mini/media |
| El distinto / El más grande / ¿Dónde hay más? | atención, tamaño, cantidad | mini/media (+grande) |
| Seguí el patrón (AB→ABCD, se “canta” al acertar) | pre-matemática (predictor fuerte) | todas |
| El laberinto (arrastrás al personaje, paredes frenan) | planificación | media/grande |
| Uní los puntos (estrella/corazón se revela) | secuencia numérica | media/grande |
| Sumas / Restas (con grupos de personajes contables) | aritmética | 5+ |
| Sopa de letras (palabras del tema, drag 8 direcciones) | literacidad | grande |
| Sudoku 4×4 de personajes | lógica | grande |
| La serie (+1/+2) | numeración | grande |

**Principios (investigación 10-jul-2026, ver PR):** targets ≥76px, tap primero
(drag solo con imán y zonas grandes), CERO fail states (el error sacude suave y
deja seguir), feedback inmediato, elogio al ESFUERZO, festejo corto con
auto-avance, sin timers/ads/dark-patterns, estrellas por juego (persisten en
localStorage), banda de edad decide menú y dificultad (mini ≤3 / media 4-5 /
grande 6+), voseo rioplatense.

**El mismo principio del motor:** el código genera y VERIFICA los puzzles
(laberinto con salida por BFS, sopa con todas las palabras colocadas, sudoku de
solución única — reusa los generadores de `cuaderno.py`); el arte sale de los
assets ya existentes del tema (stickers recortados con filtros de calidad,
`colorear*.png`, `overrides/fondos/escena.png`).

## Archivos

- `actividades_web.py` — generador: `crear(data, tema, token=None)` arma
  `actividades/<token>/` (gitignored): `data.json` (paleta + menú por edad +
  puzzles), `p*.png` (recortes; `s*.png` = variante sin halo para sombras),
  `colorear_*.png`, `escena.jpg`, `portada.jpg` (cover de biblioteca/og),
  `manifest.json`. También `estado()/html()/archivo()/preview_mock()`.
- `actividades_player.html` + `actividades_player.js` — el visor. Se sirven
  DESDE EL REPO en cada request (una mejora llega a todos los links vendidos);
  solo `data.json` + assets viven en el token. Rutas relativas → SIEMPRE bajo
  `/act/<token>/` con barra final (sin barra → 301).
- `servicio.py` — ruta `GET /act/<token>[/asset]`; branch `actividades-web` en
  `POST /api/generar` (síncrono, sin IA → rápido; devuelve `download_url`);
  `/api/al-info` también reconoce tokens de actividades (canje en la tienda).
- `productos.py` — `TIPOS["actividades-web"]` (campos nombre+edad, preview =
  portada) y `PERSONALIZADAS`.
- `tests/test_actividades_web.py` — 10 tests (puzzles verificados, whitelist
  de assets, tokens inválidos, paletas completas).

## Paletas

`actividades_web.PALETAS` — una por tema, elegida a mano (bg/card/ink/ac/ac2/
soft/star). `un-espacio-de-locura` es oscura a propósito. Tema nuevo sin
paleta → cae a `_PALETA_DEFAULT` (crema cálida); agregar la paleta al crear el
tema para que quede fina.

## Probar local

```bash
python3 -c "import actividades_web as aw; print(aw.crear({'nombre':'Sofía','edad':'5'},'safari'))"
# servir: CT3D_PORT=8791 CT3D_API_KEY=test python3 servicio.py
# abrir http://localhost:8791/act/<token>/
```

Los 12 temas del catálogo generan OK (validado 10-jul-2026: 4-8 personajes,
3 colorear, escena y 4 sopas cada uno).

## Pendiente para VENDERLO (tienda, repo /opt/ct3d) — patch exacto

La entrega motor→tienda ya funciona sola (la orden guarda el `download_url`
que devuelve `/api/generar`). Falta que la tienda lo trate como visor:

1. `backend/tienda_clientes.py`
   - `listar_compras` (~línea 118) y `armar_biblioteca` (~200):
     `tipo in ("libro-audio", "invitacion-web")` → agregar `"actividades-web"`.
   - Cover (~114 y ~164): para `actividades-web` el cover es
     `url + "portada.jpg"` (la url ya termina en `/`).
   - `categoria_libro` (~169): mapear `actividades-web` → `"libros"` (o crear
     chip nuevo "juegos" si Pablo quiere).
   - `extraer_token` (~124): aceptar también links `/act/<token>`.
2. `backend/tienda_catalogo.py` `_KIT_TIPOS` (~123) y su ESPEJO
   `tienda_kit_admin.TIPOS`: agregar `"actividades-web"` (SKUs tipo
   `KIT-ACTIVIDADES-WEB-SAFARI`).
3. `backend/tienda_templates/mi_cuenta.html` (~79-84): CTA por tipo →
   `actividades-web` = "🎮 Jugar".
4. Publicar el producto en la tienda (ficha + precio) — decisión de Pablo.

## Ideas v2 (no bloquean el lanzamiento)

- Voz rioplatense (clips ElevenLabs pregrabados por consigna; el player ya
  tiene el hook de sonido — NUNCA SpeechSynthesis del browser).
- Trazos (letras/números con el dedo) — fuerte respaldo pedagógico.
- PWA offline (service worker) para jugar sin señal.
- Modo "escuelas" (licencia por aula) — línea aparte, ver memoria
  ct3d-actividades-web-escuelas.
