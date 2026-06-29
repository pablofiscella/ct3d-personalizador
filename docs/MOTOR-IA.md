# Motor IA — generación de piezas del kit

Genera **todo el catálogo de piezas vendibles** de un tema (invitación, afiche, toppers,
stickers, cajita, etc.) a partir de los personajes del tema, usando OpenAI `gpt-image-2`.

## Principio central: "OpenAI solo ilustra"

La IA **solo dibuja arte**. Todo lo determinístico lo hace el **código**:

- **Texto exacto** (nombre, fecha, edad): lo agrega el editor/`generador.draw_text`, no la IA.
- **Geometría técnica** (molde de cajita, círculos del topper, palito, borde de stickers que
  no se pegan): la hace el código. Los modelos de imagen NO producen moldes plegables ni
  cortes precisos de forma confiable.

Regla práctica: si una pieza tiene una parte **técnica** (que debe ser exacta), esa parte la
hace el código y la IA solo aporta la decoración.

## Pipeline

1. Subir personajes del tema a `temas/<tema>/recortes/` (si no hay, usa el arte base
   `invitacion_*/afiche_*` como referencia).
2. **Generar** (`/dash` → "Generar kit con IA"): siempre en **baja** (`low`). Escribe los
   borradores en `temas/<tema>/ia_draft/`. Corre en background (gpt-image-2 es lento); la
   barra muestra `X/N piezas`.
3. **Revisar / regenerar** por pieza (↺) o por edad. Replicar afiche a otras edades (⧉).
4. **Aprobar y publicar**: upscalea a resolución de impresión (`upscale.py`, LANCZOS) y mueve
   los borradores a los slots/extras que levanta `productos._piezas_kit`.

La **resolución mejora al APROBAR** (misma imagen, no se re-genera distinta).

### Imagen maestra de estilo
Antes de las piezas se genera una "lámina maestra" (ancla de estilo) y se cachea en
`temas/<tema>/ia_maestra.png` (fuera de `ia_draft`, no se publica). Se manda como referencia
extra a cada pieza → consistencia. Al regenerar una pieza suelta se reusa la maestra cacheada
(1 sola llamada a OpenAI).

## Procesamiento por pieza (qué le hace el código)

Definido en `ia_kit/catalogo.py` (PIEZAS, prompts) y aplicado en `ia_kit/orquestador.py::_trabajo`.

| Pieza | Tipo | Procesamiento por código |
|---|---|---|
| `invitacion` | slot, **UNA_SOLA** | sin número (lo pone el editor). Se genera **1 sola vez** y se copia a todas las edades **al aprobar** (`aprobar.py`). |
| `afiche` | slot, **REPLICABLE** | número ilustrado. En el batch solo edad 1; las otras se **replican** (⧉) cambiando el número. |
| `topper` | extra, círculo | máscara **circular** por código (`_mascara_circular`). Disco para apoyar sobre la torta. |
| `topper_palito` | extra, die-cut | escena compacta die-cut + **palito de madera sólido** agregado por código (`_palito`). El prompt pide grupo compacto y NO dibujar el palito. |
| `base_torta` | extra, círculo | máscara **circular** grande (va debajo de la torta). |
| `stickers` | extra, die-cut | plancha con borde por figura vía **`expand_labels`** (ver abajo): no se pegan entre sí. |
| `separadores` | extra, recorte | quita-fondo + recorte a bbox. |
| `etiqueta_botella` | extra, rectángulo | lámina completa (sin quita-fondo). |
| `cajita_sorpresa` | extra, **molde por código** | la IA decora; el **molde de cubo (6 caras + solapas + dobleces)** lo arma `cajita.py`. |
| `decoracion_sorbetes` | extra, recorte | quita-fondo + recorte. |
| `banderin` | universal, recorte | quita-fondo + recorte. |
| `etiquetas_multiuso` | universal, rectángulo | **lámina completa** (sin quita-fondo): círculos **rellenos** tipo sello. Si tuviera quita-fondo, quedarían huecas adentro. |
| `wrappers_cupcakes` | universal, rectángulo | lámina completa. |
| `tarjetas_agradecimiento` | universal, rectángulo | lámina completa. |

Conteo total del panel para edades [1,2,3] = **14** (1 invitación + 1 afiche + 12 extras).

## Algoritmos geométricos (los hace el código)

- **Cajita** (`cajita.py::armar_cajita`): red de cubo en cruz (6 caras) + solapas trapezoidales
  en bordes libres + líneas de doblez punteadas. Las caras laterales/posterior se **rotan**
  (`_ROT_CARA`: izq +90°, der −90°, atrás 180°) para que queden derechas al plegar.
- **Stickers — borde que no se pega** (`orquestador._plancha_stickers`): método probado =
  **connected-component labeling + expansión de etiquetas acotada por distancia**
  (equivalente a `skimage.expand_labels` / al offset de corte de Cricut/Silhouette),
  implementado en Pillow puro con **BFS multi-fuente** (`_etiquetar` + `_expandir_labels`,
  sin numpy). Cada figura crece su borde hasta un máximo O hasta la **línea media** con la
  vecina; luego se **talla una franja transparente** (`gap`) en esa línea media (boundary
  dilatado con MaxFilter, sin tocar la figura) → entre dos stickers queda espacio claro para
  que la **imprenta detecte dónde corta cada uno**. Funciona con **cualquier forma**, no solo
  círculos. Reporta `aviso` si el arte trae figuras ya pegadas (muy pocas componentes → hay
  que regenerar, p.ej. campamento/superheroes salieron pegados y se rehicieron).
- **Palito del topper** (`orquestador._palito`): dowel de madera sólido con borde blanco,
  abajo-centro. Más confiable que pedírselo a la IA (lo dibujaba con líneas finas que el
  quita-fondo borraba).
- **Die-cut genérico** (`_borde_sticker`): silueta sólida (cierra gaps + rellena huecos) +
  borde blanco. Para figuras únicas (topper_palito); los stickers usan `_plancha_stickers`.

## Archivos

- `ia_kit/catalogo.py` — piezas, paleta, prompts.
- `ia_kit/orquestador.py` — orquesta la generación + procesamiento por pieza.
- `ia_kit/cajita.py` — molde de la cajita.
- `ia_kit/aprobar.py` — mueve borradores a slots/extras (copia invitación a todas las edades).
- `ia_kit/upscale.py` — upscale a impresión al aprobar.
- `ia_kit/client.py`, `multipart.py` — cliente OpenAI (multipart `image[]`).
- `ia_kit/jobs.py` — mini-registro de jobs en background.
- `tests/` — pytest (49+ tests).

## Deploy / operación

El servicio corre desde `/root/ct3d-personalizador` (rama `main`) como `ct3d-kit.service`,
puerto `CT3D_PORT=8787`. El desarrollo se hace en el worktree `.claude/worktrees/motor-ia-plan`.

**Loop de deploy:** editar en el worktree → `git -C /root/ct3d-personalizador merge --ff-only
worktree-motor-ia-plan` → `sudo systemctl restart ct3d-kit.service` (chequear antes que NO
haya conexión a `:443`, = generación en curso). **`dash.html` se sirve desde disco en cada
request** → sus cambios aplican al recargar, SIN reiniciar; solo el código Python necesita
restart.

**Regenerar una pieza por API** (el servicio ya tiene la `OPENAI_API_KEY`):
```
POST http://127.0.0.1:8787/dash/ia-regenerar?tema=<T>&pieza=<P>&calidad=low
  header: X-API-Key: $CT3D_API_KEY
→ {job}; pollear /dash/ia-estado?job=<id>
```
Auth: header `X-API-Key` contra `CT3D_API_KEY`. (Ojo: el puerto 8092 es otro servicio Flask,
NO el kit.)

## Variables de entorno (systemd)
- `OPENAI_API_KEY` — la misma del audio/voz coral.
- `OPENAI_IMAGE_MODEL=gpt-image-2` (re-verificar id por deprecaciones).
- `OPENAI_CALIDAD=low` (los borradores siempre en baja; el upscale es al aprobar).
- `CT3D_API_KEY` — token admin del panel. `CT3D_PORT=8787`.

## Gotchas de OpenAI (resueltos)
- `timeout` va por keyword a `urlopen` (el 2º posicional es `data`).
- Campo multipart `image[]` (no `image`) para múltiples refs; `Content-Type: image/png` por archivo.
- `gpt-image-2` NO soporta `input_fidelity`.
- Sin refs no manda imagen → fallback al arte base.
- Regenerar es lento → background + maestra cacheada (evita 504/524 del proxy).
