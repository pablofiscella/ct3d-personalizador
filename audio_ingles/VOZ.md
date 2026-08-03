# La voz de las actividades de Inglés

**Dorothy** — ElevenLabs `ThT5KcBeYPX3keUQqHPh`, modelo `eleven_multilingual_v2`,
`stability 0.75`, `similarity_boost 0.75`, **`speed 0.8`**.

Es **británica** y va deliberadamente más lenta y más pareja que la voz de las
consignas. No es una elección estética: el chico está aprendiendo a pronunciar, y
una voz expresiva que varía la entonación entre tomas suena artificial y enseña peor
que una pareja y articulada.

Pablo la eligió el 27-jul-2026 comparando seis candidatas británicas con la misma
frase. La anterior era Rachel, que descartó por sonar robótica.

## Por qué NO es la voz de las consignas

Las consignas van con Valeria, rioplatense, y eso es correcto para el español. Leer
inglés con una voz entrenada en español le enseñaría al chico una pronunciación
equivocada — que es **peor que no tener audio**. Por eso los clips de inglés viven
en `audio_ingles/` y no en `audio_consignas/`, y hay un test que lo verifica.

## Al agregar términos nuevos

```python
import audiolibro
mp3 = audiolibro._tts_elevenlabs(
    texto, voice_id="ThT5KcBeYPX3keUQqHPh",
    settings={"stability": 0.75, "similarity_boost": 0.75, "speed": 0.8},
    model="eleven_multilingual_v2")
```

El `model` va explícito: el default del repo es `eleven_v3`, que **no admite
`speed`**, y el clip saldría al ritmo del audiolibro en vez del que se aprobó.

## Qué dice cada clip (03-ago-2026)

Pablo, apretando el botón: *"apretás el botón y hasta habla en español o responde otra
cosa"*. Los clips se habían generado con la RESPUESTA de cada pregunta. Correcto en 19 de
las 24 de `ingles_basico` —«¿Cómo se dice "perro" en inglés?» → *dog*— pero en **cinco** la
respuesta es en castellano («¿Qué significa "book"?» → libro), así que el botón de una
actividad de inglés decía *libro*, *rojo*, *feliz*, *amarillo* y *3* con voz británica.

**La regla:** el clip dice el término INGLÉS. Es la respuesta cuando la pregunta pide el
inglés; si no, es lo que está entre « » en la pregunta.

**El nombre del archivo ES auditable:** `en_<sha1(voice_id|texto)[:16]>.mp3`. Antes era un
hash opaco y un clip equivocado se veía igual que uno correcto — por eso el error sobrevivió
desde que se armó la actividad. `test_ningun_clip_dice_otra_cosa` recalcula los 67 y compara,
así que un clip mal apareado ya no llega a producción.

## El manifest

`manifest.json` mapea `<idPrefijo>#<indice>` → archivo. **El idPrefijo viene
TRUNCADO a 10 caracteres** (`gen_curriculum.py`: `pfx = a["id"][:10]`), así que la
clave de `ingles_vocabulario_7` es `ingles_voc#0`. Con la clave sin truncar el
manifest carga con 200 y el botón queda **mudo, sin ningún error**.
