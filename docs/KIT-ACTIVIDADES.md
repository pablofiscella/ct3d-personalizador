# Kit de Actividades — spec, prompts y runbook

> Cómo se crea un **kit de actividades** por tema (cuaderno imprimible para
> imprimir y resolver). Pablo quiere que **lo genere yo (Claude) a pedido**, NO
> desde un botón self-serve. Este doc es el runbook + las reglas + los prompts
> exactos para reproducirlo. Pedido: 30-jun-2026.

## Principio (el mismo del motor)

**OpenAI solo ilustra; el código resuelve y VERIFICA.** Todo lo que tiene
"respuesta correcta" (laberinto con salida, sudoku con solución única, sopa con
todas las palabras puestas, contar, sumas/restas, serie) lo genera y chequea un
algoritmo determinístico. La IA aporta solo lo creativo: los personajes del tema
(de la hoja de stickers) y las **páginas para colorear** (line art). Así nunca
sale un laberinto sin salida ni una palabra mal escrita.

Código: `cuaderno.py` (stdlib + Pillow, sin libs nuevas). Render verificado;
`paginas(tema, edad)` devuelve las páginas listas.

## Estructura del kit (reglas de diseño aprobadas por Pablo)

- **Banner fino arriba** en cada página: a la izquierda la marca
  `CASATRIDIMENSIONAL` (una sola palabra, ver [[marca-casatridimensional]]), a la
  derecha `Actividad N · X años`. En el solucionario dice `Soluciones`.
- **UNA actividad por página**, numerada en el banner (`_Book.sec` arranca página
  nueva + banner + título).
- **Cada actividad LLENA la hoja** (sin medias páginas vacías): las filas se
  reparten a lo alto del área `[b.y, BOT]` con `_slot()`, y figuras/grillas se
  agrandan. Laberintos/sopa/sudoku se centran y agrandan; las escenas (contar,
  buscar) ocupan ~0.6–0.78 del alto.
- **Por banda de edad** (`_construir(b, e)`): el set y la dificultad dependen de
  la edad. Tipos que se repiten con **contenido nuevo** (otra figura/lista de
  palabras/números) para sumar variedad sin saturar.
- **Solucionario** al final (`_solucionario`): acumula por tipo (`soladd`) →
  cubre TODAS las repeticiones (varios laberintos/sopas). `_build()` separa
  actividades y solucionario; la galería de la tienda excluye el solucionario por
  conteo (`nsol.txt`).

### Menús por banda de edad (orden fácil → difícil)

- **2-3 años (~12):** colorear · repasar líneas · sombra · unir iguales · contar
  (1-3) · grande/chico · patrón · ¿cuál tiene más? · unir puntos (estrella, 6) ·
  repasar líneas · buscar (8) · colorear.
- **4-5 años (~18):** trazos · puntos (10) · laberinto (7) · contar (5,3) ·
  patrón · intruso · sombra · sudoku · ¿cuál tiene más? · iguales · grande/chico
  · otra mitad · buscar (14) · laberinto · puntos (corazón) · ta-te-ti · colorear
  ×2.
- **6-7 años (~25):** laberinto (9) · sopa · puntos (10) · contar (5,3) · sombra
  · colorear · sumas · intruso · laberinto circular · patrón · buscar (18) ·
  restas · colorear · sudoku · ¿cuál tiene más? · completar serie · iguales ·
  otra mitad · laberinto · sopa (lista B) · puntos (corazón) · contar (6,4) ·
  grande/chico · ta-te-ti · colorear.

### Catálogo de actividades (generadores en `cuaderno.py`)

Verificables (van al solucionario): laberinto (`_a_laberinto`, BFS garantiza
salida) · laberinto circular (`_a_laberinto_circular`, theta-maze) · sopa de
letras (`_a_sopa`, todas las palabras colocadas y chequeadas) · sudoku 4×4
(`_a_sudoku`, solución única por conteo) · contar (`_a_contar`) · sumas
(`_a_sumas`) · restas (`_a_restas`) · completar serie numérica (`_a_serie`,
regla +1/+2) · ¿cuál tiene más? (`_a_mas_menos`) · grande/chico (`_a_tamano`).
A simple vista (no van al solucionario): unir con su sombra (`_a_sombra`, sombra
= silueta del propio PNG) · ¿cuál es diferente?/intruso (`_a_diferente`) ·
continuá el patrón (`_a_patron`) · unir los iguales (`_a_iguales`) · unir los
puntos (`_a_puntos`, estrella o corazón `_heart_pts`) · encontrá los escondidos
(`_a_buscar`, iSpy) · repasar líneas/trazos (`_a_trazos`) · dibujá la otra mitad
(`_a_otra_mitad`, `_contorno` = silueta limpia) · ta-te-ti (`_a_tateti`) ·
pintá el dibujo (`_a_colorear`).

Listas de palabras de la sopa: `PALABRAS` y `PALABRAS2` (genéricas de cumpleaños,
sin acentos/ñ porque la grilla es A-Z).

## Páginas para COLOREAR — las dibuja OpenAI (gpt-image-2)

La pieza `colorear` está en `ia_kit/catalogo.PIEZAS` (NO en las listas EXTRAS →
se genera/aprueba en el panel IA pero NO se vende como pieza de kit; la consume
el cuaderno). El cuaderno usa `colorear*.png` de `extras/` o `ia_draft/`
(`_colorear_imgs`); si no hay, cae a line art por código (`_lineart`, peor).

### Prompt exacto (en `catalogo.prompt_de`, key `colorear`)

```
Creá una PÁGINA PARA COLOREAR infantil con los personajes del tema de las
imágenes de referencia (mismos personajes, sin cambiar su diseño). DIBUJO SOLO
EN LÍNEAS: contornos negros de grosor MEDIO —ni finos ni muy gruesos, como un
libro de colorear infantil estándar—, limpios y CERRADOS, sobre fondo BLANCO
liso. Una escena simple y clara, personajes grandes y centrados, con espacios
amplios para pintar. SIN relleno, SIN color, SIN grises, SIN sombras, SIN
texturas, SIN tramas, SIN texto ni números. Estilo libro de colorear, line art,
blanco y negro.
```

(30-jun: se moderó de "gruesos" a "grosor MEDIO" — con "gruesos" algunos temas
salían con trazo demasiado pesado, ej. un-espacio-de-locura.)

NO usa el bloque de estilo flat-vector (ese pide colores planos). Para **varias
escenas distintas** del mismo tema, se le agrega al final una línea
` Escena sugerida: <descripción>.` (ej.: "un payaso haciendo malabares y un león
saltando un aro"). Referencias = `ia_kit/orquestador._refs(tema_dir)` (los
recortes / arte base del tema).

### Garantía B/N por código

`orquestador._limpiar_colorear(im)`: aplana sobre blanco → umbral (`<165` → negro)
→ `MinFilter(3)` (engrosa el trazo). Mata cualquier gris/sombra que el modelo
cuele. Es idempotente (el cuaderno lo re-aplica al leer). **Regla clave:** para
line-art se EXTRAEN BORDES, nunca se "saca el color" (eso da blobs negros).

## RUNBOOK — generar el kit de un tema (lo hago yo a pedido)

1. **Páginas para colorear (OpenAI).** Sacar `OPENAI_API_KEY` del proceso vivo
   sin imprimirla:
   ```bash
   OAKEY=$(sudo tr '\0' '\n' < /proc/$(systemctl show -p MainPID --value ct3d-kit.service)/environ | grep ^OPENAI_API_KEY= | cut -d= -f2-)
   ```
   Generar SIEMPRE las 3 escenas (nunca menos — el cuaderno usa 3 slots de
   colorear; si falta alguna, cae al fallback `_lineart` por detección de
   bordes, que con personajes de la IA con sombreado/degradé da un BLOB NEGRO
   roto e ilegible, no "un trazo grueso": confirmado 30-jun con
   un-espacio-de-locura, que solo tenía 1 variante). Con el prompt de arriba +
   `Escena sugerida`, pasar cada una por `_limpiar_colorear` y guardarlas en
   `temas/<tema>/ia_draft/colorear.png`, `colorear_2.png`, `colorear_3.png`
   (quedan pendientes de aprobar en el panel; el cuaderno ya las toma desde
   `ia_draft/`). Calidad `low` (borrador). Cada llamada gpt-image-2 tarda >60s
   → correr de a una con `timeout` alto, NO 2 secuenciales en un Bash de 120s.
   Después de generar/reemplazar cualquier colorear*.png hay que borrar
   `temas/<tema>/actividades_cache/<edad>/` para que el cuaderno no sirva la
   versión vieja cacheada.
2. **Render del cuaderno** para revisar: `cuaderno.paginas(tema, edad)` para
   edad 6/5/3, armar un montage y MIRARLO (no asumir). Verificar: banner, que
   cada hoja se llene, personajes reales del tema, colorear distintas.
3. **Ajustar** lo que haga falta en `cuaderno.py` y volver a renderizar.
4. **Tests:** `python3 -m pytest -q` (incluye `tests/test_cuaderno.py`).
5. **Deploy:** commit en el worktree → `git -C /root/ct3d-personalizador merge
   --ff-only worktree-motor-ia-plan` → limpiar cachés
   (`find temas -maxdepth 2 \( -name actividades_cache -o -name actividades_mon
   -o -name actividades_preview \) -type d -exec rm -rf {} +`, NO tocar
   `actividades_override`) → `sudo systemctl restart ct3d-kit.service`.

OJO: el cuaderno se cachea en `temas/<tema>/actividades_cache/<edad>/`; si cambié
`cuaderno.py` o las imágenes de colorear, hay que borrar ese caché (y
`actividades_mon` si cambió la extracción de personajes) para regenerar.

## Archivos clave

- `cuaderno.py` — todo el motor del cuaderno (banner, `_Book`, `_construir` por
  edad, generadores `_a_*`, `_build`/`paginas`, solucionario, cache + overrides).
- `ia_kit/catalogo.py` — pieza `colorear` + prompt.
- `ia_kit/orquestador.py` — `_limpiar_colorear` (garantía B/N).
- `tests/test_cuaderno.py` — humo (build por banda, separación de solucionario).

Relacionado: [[motor-ia-generacion-piezas]], [[cuaderno-actividades]],
[[marca-casatridimensional]]. Doc del motor general: `docs/MOTOR-IA.md`.
