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

## El manifest

`manifest.json` mapea `<idPrefijo>#<indice>` → archivo. **El idPrefijo viene
TRUNCADO a 10 caracteres** (`gen_curriculum.py`: `pfx = a["id"][:10]`), así que la
clave de `ingles_vocabulario_7` es `ingles_voc#0`. Con la clave sin truncar el
manifest carga con 200 y el botón queda **mudo, sin ningún error**.
