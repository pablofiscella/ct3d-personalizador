# ct3d-personalizador — Motor de piezas imprimibles

> **Propósito:** Motor Python que genera kits de cumpleaños personalizables con IA (OpenAI gpt-image-2 para el cuaderno).
> Repo hermano: `/opt/ct3d/` (backend Flask + dashboard que consume este motor).

## Qué es

Motor procedural de **10 tipos de piezas imprimibles:**
- Kit completo (invitación, cartel, actividades, etc.)
- Productos individuales: certificado, corona, antifaces, menú, rompecabezas, cápsula, calendario, papertoys, memoria
- **Cuaderno de actividades interactivo** (`actividades_web.py`): las actividades del cuaderno pero JUGABLES en el navegador (memotest, sopa, laberinto, pintar, contar…), entregado como link vivo `/act/<token>/` igual que el audiolibro. Player en `actividades_player.html/.js` (se sirve del repo → mejoras llegan a links ya vendidos). Doc: `docs/ACTIVIDADES-WEB.md`.
- **Rompecabezas interactivo** (`rompecabezas_web.py`): las escenas del tema hechas rompecabezas JUGABLES en el navegador (drag con imán, piezas con knobs Bézier reales — la MISMA receta del imprimible exportada a data.json), entregado como link vivo `/armar/<token>/`. Player en `rompecabezas_player.html/.js` (se sirve del repo → mejoras llegan a links ya vendidos). **Demo pública "Probalo gratis" (17-jul-2026):** ruta `GET /probar/rompecabezas/<tema>` (sin admin) que sirve el rompecabezas de MUESTRA del tema (token fijo `demo-<tema>`, sin la foto del cliente) — la abre el botón "Probalo gratis" de la ficha en la tienda. En modo demo (URL `/armar/demo-`) el player deja armar solo la MITAD de los rompecabezas (el resto con candado + CTA de compra); gateado a la URL → los links vendidos no se ven afectados. Doc: `docs/ROMPECABEZAS-WEB.md`.
- **Libro de cuento personalizado** (`libro.py`): 10 páginas donde el chico es el protagonista — portada, dedicatoria, 7 páginas de historia (cada una con escena procedural que ILUSTRA lo que cuenta el texto: cama+invitación → luces mágicas → fiesta → problema → solución → tesoro → casita de noche) y FIN. Historia ambientada por temática (`libro.HISTORIAS`, con fallback genérico). Campos: nombre, edad, dedicatoria.
- **"Elegí tu aventura" — PROTOTIPO** (`aventura.py` + `aventura_web.py`, 11-jul-2026): a diferencia de `libro.py` (100% lineal), acá el chico ELIGE el camino en un grafo de nodos con decisiones (por ahora solo tema `safari`: 2 puntos de decisión, 2 finales, 28 nodos únicos — cualquier camino elegido dura ~20 postas, igual que un libro/audiolibro lineal), entregado como link vivo `/leer/<token>/`. Ilustración PROPIA por nodo (`temas/<tema>/overrides/aventura/<nodo_id>.png`, generada con `aventura_ia.py` — protagonista con vestimenta y mochila fijas, encadenando una imagen de referencia entre nodos para consistencia real, no solo texto). Player en `aventura_player.html/.js`. **Narración por nodo (opcional, 12-jul-2026):** `aventura_audio.py` genera un MP3 por nodo (texto ya personalizado con el nombre del chico) con el mismo motor de voz del audiolibro (`audiolibro.tts_mp3` — ElevenLabs Lizy, acento argentino); a diferencia del arte, el audio se genera POR COMPRA en `aventura_web/<token>/audio/<nodo_id>.mp3` (no se puede cachear por tema: el texto lleva el nombre adentro). El player narra automáticamente al mostrar cada nodo y sigue frenado esperando el click del chico para avanzar (ya era el comportamiento del player, no cambió) — si el token no tiene audio generado, el visor lee igual, en silencio. Sin integración a tienda todavía: es solo para validar el mecanismo antes de invertir en más temas/contenido.
  - **Ilustraciones (2 caminos, mismo destino):** el override `temas/{tema}/overrides/libro/{idx}.png` es SOLO el arte de la escena (NO la página completa: el texto personalizado siempre lo escribe el motor — por eso `productos.piezas_tipo` saltea el override genérico para `libro`). (1) Subida manual: botón 📤 de cada página en la galería del dash. (2) IA: botón «✨ Generar 10 con IA» en el dash (`POST /dash/libro-ia?tema=X[&pieza=N]`, job + polling con `/dash/ia-estado`) o CLI `OPENAI_API_KEY=... python libro_ia.py <tema> [pagina]`. Prompts en `libro_ia.py` (usan la ambientación de `libro.HISTORIAS`; referencia de estilo: `ia_maestra.png` o stickers del tema; arte SIN texto). Se genera una vez por tema, no por venta.

**Tecnología:** Pillow (procedural generation) + OpenAI gpt-image-2 (cuaderno de actividades con IA) + override system (cliente puede reemplazar cualquier pieza).

**Donde vive:** `/root/ct3d-personalizador/` (repo `ct3d-personalizador.git`)

## Git: Procedimiento obligatorio

**NUNCA terminar una sesión sin confirmar que TODO está commiteado y pusheado:**

```bash
cd /root/ct3d-personalizador
git status
git add <archivos>
git commit -m "tipo: descripción"
git push origin main    # Pre-push hook bloquea si hay cambios sin trackear
```

### Pre-push hook (protección automática)
El hook en `.git/hooks/pre-push` bloquea push si hay archivos críticos sin trackear:
- `.py`, `.jsx`, `.html`, `.md` sin stagear → BLOQUEADO
- `.png` (overrides personalizados) sin trackear → BLOQUEADO

## Estructura

```
temas/                      # Temáticas (safari, circo, superhéroes, etc.)
  {tema}/                   # Carpeta por tema
    tema.json              # Config (colores, personajes)
    ia_maestra.png         # Imagen base del cuaderno IA (gitignored)
    overrides/             # Reemplazos del cliente (commiteados)
      tipo/
        0.png, 1.png...    # Piezas reemplazadas

productos.py               # Registry de tipos + generadores
certificado.py, corona.py, antifaces.py, menu_infantil.py, etc.
cuaderno.py               # Generador IA del cuaderno de actividades
piezas.py                 # Utilidades (marca de agua, RGBA→RGB, etc.)

tests/
  test_productos_overrides.py
  test_cuaderno.py
  ...
```

## Comandos clave

```bash
# Generar preview de una pieza (con marca de agua)
# GET /preview?tipo=certificado&tema=safari&nombre=Sofía

# Dashboard (panel de gestión del kit)
# Abierto en editor_simple.html (simple editor) y dash.html (panel completo)

# Tests
pytest tests/ -v
```

## Reglas

1. **Campos personalizables por tipo:** Si un tipo nuevo necesita campos (como menú), agregarlos a `productos.TIPOS[tipo]["campos"]` y `campos_labels`.
2. **Override system:** Cualquier pieza puede reemplazarse subiendo `temas/{tema}/overrides/{tipo}/{idx}.png`.
3. **Editor genérico:** `editor_simple.html` carga `/tipos` y arma inputs automáticamente — **NO tocar para agregar campos nuevos**, editar el tipo en `productos.py`.
4. **Tests:** Siempre que cambies un tipo, agregar test que verifique:
   - Piezas procedurales se generan
   - Override reemplaza la pieza
   - Campos se respetan en el preview
5. **GOTCHA DPI (real, encontrado 7-jul-2026 haciendo gorro/corona):** `piezas.generar_kit()`
   exporta SIEMPRE el PDF con `resolution=300` (generador.DPI), sin mirar a qué escala
   se dibujó el PNG. La mayoría de los "productos individuales" (certificado, antifaces,
   menú, rompecabezas, cápsula, papertoys, memoria, rutina) usan `Wp,Hp = 1240,1754`
   (pensado como ~150dpi de A4) — es decir que **sus PDF salen a la MITAD del tamaño
   físico real** (A5 en vez de A4) desde que existen, no es algo que rompí ahora. Recién
   se corrigió para `corona.py` (gorro/corona ahora dibujan a 1240·2=2480 base, A4
   apaisado a 300dpi real — ver su docstring). Los otros 8 tipos siguen con el bug;
   decidir con Pablo si vale la pena corregirlos (implica re-escalar constantes en
   píxeles fijos de cada archivo, no solo cambiar Wp,Hp).

7. **El cuaderno es del CHICO, no del adulto** (27-jul-2026). El link del cuaderno lo
   tiene el chico, pero el adulto se lo configura en SU teléfono y se lo presta — o sea
   que la sesión del adulto está abierta en ese navegador. Por eso:
   - **El player NO tiene ninguna salida a la cuenta.** El 📚 que llevaba a `/mi-cuenta`
     se sacó: gatear por login no servía, porque quien pasa el gate es el teléfono y no
     la persona. Hoy queda UN solo `<a>` en todo el cuaderno y es el diploma.
   - **La marca del cuaderno sale de `escolar_on`:** Kydo en la línea escolar,
     Casatridimensional en la de cumpleaños. Va en el header, en el título de la pestaña
     y en el HTML que sirve el motor (`_es_escolar`), con respaldo a `data.json` para los
     cuadernos YA ENTREGADOS, cuyo manifest es viejo.

8. **Las portadas de grado se rellenan con desenfoque, no con color plano** (27-jul-2026).
   El arte de 1.º y 2.º vino en 2:3 y el resto en 3:4. `_portada_de_grado` hace CONTAIN
   —recortar el alto se comería el banner de arriba o la tira de íconos de abajo— y el
   sobrante se llena con la MISMA imagen a cover y desenfocada. Con el color plano
   quedaban 48 px de banda a cada lado y en la biblioteca se veía literalmente más
   angosta que las demás. Hay test que recorre los SIETE grados.

6. **NUNCA reiniciar `ct3d-kit.service` sin chequear jobs activos** (real, 7-jul-2026:
   un restart mío mató el armar-tema de Pablo justo antes de la etapa del libro — los
   jobs viven en memoria y mueren sin rastro). Antes de cualquier restart:
   `curl -s "http://127.0.0.1:8787/dash/ia-estado" -H "X-API-Key: $(cat .api_key)"`
   → si `activos > 0`, esperar a que termine.

## Performance — caché de previews (`/preview`) (17-jul-2026)

Las miniaturas de la tienda las genera `/preview` en vivo con Pillow. La mayoría
rinde en ~0.7s, pero el **compuesto del rompecabezas-web arma el rompecabezas
entero → cold render de 40-70s**. Tres capas para que eso NO enlentezca la tienda:

1. **Caché en disco** (`.cache/preview/`, `servicio.py:PREVIEW_CACHE_TTL`): **7 días**
   (era 6h). La frescura NO depende del TTL — se invalida por tema con
   `_preview_cache_clear` al regenerar arte. Una vez renderizado, se sirve de disco
   en ~0.002s.
2. **Cloudflare** cachea `/preview` en el borde: Cache Rule en el panel CF →
   `starts_with(uri.path,"/preview") and host eq "kit.casatridimensional.com.ar"` →
   Eligible for cache (respeta el Cache-Control del origen). Sin esta regla, CF
   marcaba `cf-cache-status: DYNAMIC` (no cacheaba, porque `/preview` no tiene
   extensión de archivo) y cada request pegaba al motor.
3. **Re-warm de madrugada** (`/opt/ct3d/infra/ct3d-preview-warm.py` +
   `ct3d-preview-warm.timer`, Lun y Jue 04:30 ART): borra el caché de los pesados
   (rompecabezas) y los regenera frescos ANTES de que venzan los 7 días, en horario
   sin tráfico → ningún usuario se come nunca el cold render. Ver corrida:
   `journalctl -u ct3d-preview-warm.service`.

**GOTCHA:** el render del compuesto sigue siendo lento (40-70s); no se reescribió.
Si algún preview tarda de golpe, es un cold render (cache vencido/borrado): warmealo
pidiendo la URL, o corré `systemctl start ct3d-preview-warm.service`.

## El espejo DEV (28-jul-2026) — probar antes de tocar el vivo

El motor tiene un espejo corriendo en el puerto **9787** (`ct3d-dev-kit.service`), con su
propio árbol en `/srv/ct3d-dev/personalizador` y sus propios `pedidos/`. Doc completa:
`/opt/ct3d/docs/DEV.md`.

```bash
probar <rama-ct3d> --motor <rama-de-este-repo>   # para el espejo en esas ramas + smoke
promover --motor                                 # sube main a producción (NO reinicia si
                                                 # hay jobs de IA corriendo: los respeta)
dev-shell                                        # consola dentro del espejo
```

- La puerta del espejo vive en `servicio.py` (`DEV`, `_dev_ok`, `_dev_entrada`) y es
  **inerte en producción**: sin `CT3D_ENTORNO=dev` no se evalúa nada.
- Exceptúa las llamadas de loopback que no vinieron por el túnel — la tienda le pide
  progreso, portadas e informes al motor sin cookie.
- Se sigue aplicando la regla 6: **nunca reiniciar `ct3d-kit` con jobs activos**. `promover
  --motor` lo chequea solo contra `/dash/ia-estado`.

## Mi responsabilidad (Claude)

Cada sesión termino reportándote el estado de GIT en ambos repos (este y `/opt/ct3d/`).

---

**Contacto:** repo GitHub `pablofiscella/ct3d-personalizador`
