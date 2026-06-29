# Motor IA — Piezas del Kit (Plan A) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generar automáticamente todo el catálogo de piezas de fiesta de un tema con `gpt-image-2`, a partir de los personajes ya subidos, dejándolas en staging para que el admin las apruebe y se publiquen con el pipeline existente.

**Architecture:** Un paquete nuevo `ia_kit/` (Python stdlib + Pillow) encapsula: builder multipart, cliente OpenAI Images, validación de imagen, catálogo de prompts, orquestador de generación, registro de jobs en background y aprobación. `servicio.py` solo gana endpoints finos que delegan en `ia_kit/`. El orquestador escribe los borradores en `temas/<tema>/ia_draft/` y `aprobar()` los mueve a los slots/`extras/` que el pipeline (`productos._piezas_kit`) ya consume sin cambios.

**Tech Stack:** Python 3.12, Pillow 11.3.0, stdlib `urllib.request`/`threading`/`json`. Tests con `pytest` (dev-only). Modelo de imagen `gpt-image-2` vía `POST https://api.openai.com/v1/images/edits` (multipart).

## Global Constraints

- **Runtime deps:** solo stdlib + Pillow 11.3.0. NO agregar `requests` ni otras libs de runtime. `pytest` es dev-only (no se importa en código de producción).
- **HTTP saliente:** `urllib.request` con patrón `(status, dict)`, espejando `_tienda_admin` (`servicio.py:91`).
- **Modelo:** `gpt-image-2` (id configurable por env `OPENAI_IMAGE_MODEL`, default `"gpt-image-2"`). Re-verificar id vigente cerca del lanzamiento (deprecaciones dic-2026).
- **Sin texto en las imágenes de IA:** el texto del cliente lo pone el motor existente; los prompts piden zonas limpias para el texto.
- **API key:** `OPENAI_API_KEY` desde env. Si falta, los endpoints responden error claro y NO arrancan.
- **Staging aislado:** los borradores van a `temas/<tema>/ia_draft/`; nada toca slots/`extras/` hasta `aprobar()`.
- **Nombres de archivo (deben matchear el pipeline existente):**
  - Slots base en `temas/<tema>/`: `invitacion_<edad>.png`, `afiche_<edad>.png`.
  - Extras en `temas/<tema>/extras/`: por-edad `<base>_<edad>.png`; universal `<base>.png`.
  - Listas canónicas (de `productos.py:209-211`):
    `_EXTRAS_POR_EDAD = ["afiche","topper","stickers","separadores","etiqueta_botella","cajita_sorpresa","decoracion_sorbetes"]`
    `_EXTRAS_UNIVERSAL = ["banderin","etiquetas_multiuso","wrappers_cupcakes","tarjetas_agradecimiento"]`
- **Decisión "mixto" de edades:** `invitacion` y `afiche` se generan ×3 (una por edad de `tema["edades"]`); el resto ×1 (el número lo pone el motor como texto).
- **Tuplas de pieza del pipeline:** `(filename:str, fn(data)->PIL.Image, is_rgba:bool)` — no lo tocamos, solo escribimos los PNG que `_piezas_kit` levanta.

---

### Task 1: Harness de tests + paquete vacío

**Files:**
- Create: `requirements-dev.txt`
- Create: `ia_kit/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/test_smoke.py`

**Interfaces:**
- Consumes: nada.
- Produces: paquete importable `ia_kit`; comando de tests `python -m pytest`.

- [ ] **Step 1: Crear `requirements-dev.txt`**

```
pytest==8.2.0
```

- [ ] **Step 2: Crear el paquete y los `__init__`**

`ia_kit/__init__.py`:
```python
"""Motor de generación de piezas con IA (OpenAI Images). Solo stdlib + Pillow."""
```
`tests/__init__.py`: (archivo vacío)

- [ ] **Step 3: Escribir el smoke test**

`tests/test_smoke.py`:
```python
import ia_kit


def test_paquete_importa():
    assert ia_kit.__doc__ is not None
```

- [ ] **Step 4: Instalar pytest y correr**

Run: `pip install -r requirements-dev.txt && python -m pytest tests/ -v`
Expected: PASS (1 passed).

- [ ] **Step 5: Commit**

```bash
git add requirements-dev.txt ia_kit/__init__.py tests/__init__.py tests/test_smoke.py
git commit -m "test: harness pytest + paquete ia_kit"
```

---

### Task 2: Builder multipart/form-data

**Files:**
- Create: `ia_kit/multipart.py`
- Test: `tests/test_multipart.py`

**Interfaces:**
- Consumes: nada.
- Produces: `build_multipart(fields: dict[str,str], files: list[tuple[str,str,bytes]]) -> tuple[str, bytes]`
  donde cada file es `(field_name, filename, raw_bytes)`; devuelve `(content_type, body)` con
  `content_type` tipo `"multipart/form-data; boundary=..."`.

- [ ] **Step 1: Escribir el test que falla**

`tests/test_multipart.py`:
```python
from ia_kit.multipart import build_multipart


def test_incluye_campos_y_archivos():
    ct, body = build_multipart(
        {"model": "gpt-image-2", "prompt": "hola"},
        [("image[]", "a.png", b"\x89PNG\r\n")],
    )
    assert ct.startswith("multipart/form-data; boundary=")
    boundary = ct.split("boundary=")[1].encode()
    assert boundary in body
    assert b'name="model"' in body and b"gpt-image-2" in body
    assert b'name="prompt"' in body and b"hola" in body
    assert b'name="image[]"; filename="a.png"' in body
    assert b"\x89PNG\r\n" in body
    assert body.rstrip().endswith(b"--")  # cierre del multipart


def test_varias_imagenes_mismo_campo():
    _, body = build_multipart(
        {}, [("image[]", "a.png", b"AAA"), ("image[]", "b.png", b"BBB")]
    )
    assert body.count(b'name="image[]"') == 2
    assert b"AAA" in body and b"BBB" in body
```

- [ ] **Step 2: Correr y ver fallar**

Run: `python -m pytest tests/test_multipart.py -v`
Expected: FAIL (ModuleNotFoundError: ia_kit.multipart).

- [ ] **Step 3: Implementar**

`ia_kit/multipart.py`:
```python
"""Construye un cuerpo multipart/form-data con stdlib (urllib no lo hace)."""
import os
import binascii


def _boundary():
    return "----ct3d" + binascii.hexlify(os.urandom(16)).decode()


def build_multipart(fields, files):
    b = _boundary()
    sep = ("--" + b).encode()
    out = bytearray()
    for name, value in fields.items():
        out += sep + b"\r\n"
        out += ('Content-Disposition: form-data; name="%s"\r\n\r\n' % name).encode()
        out += str(value).encode("utf-8") + b"\r\n"
    for name, filename, raw in files:
        out += sep + b"\r\n"
        out += ('Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
                % (name, filename)).encode()
        out += b"Content-Type: application/octet-stream\r\n\r\n"
        out += raw + b"\r\n"
    out += sep + b"--\r\n"
    return "multipart/form-data; boundary=" + b, bytes(out)
```

- [ ] **Step 4: Correr y ver pasar**

Run: `python -m pytest tests/test_multipart.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add ia_kit/multipart.py tests/test_multipart.py
git commit -m "feat: builder multipart/form-data para OpenAI /edits"
```

---

### Task 3: Validación de imagen generada

**Files:**
- Create: `ia_kit/validate.py`
- Test: `tests/test_validate.py`

**Interfaces:**
- Consumes: nada.
- Produces:
  - `validar_png(raw: bytes, size_esperado: tuple[int,int] | None = None, tol: float = 0.06) -> PIL.Image.Image`
    — abre el PNG; si `size_esperado` se da, valida que el ratio coincida dentro de `tol`
    (relativo); levanta `ImagenInvalida` si no abre o el ratio no coincide.
  - `class ImagenInvalida(Exception)`.

- [ ] **Step 1: Escribir el test que falla**

`tests/test_validate.py`:
```python
import io
import pytest
from PIL import Image
from ia_kit.validate import validar_png, ImagenInvalida


def _png(w, h):
    buf = io.BytesIO()
    Image.new("RGB", (w, h), "white").save(buf, "PNG")
    return buf.getvalue()


def test_acepta_ratio_correcto():
    im = validar_png(_png(1536, 2176), size_esperado=(1536, 2176))
    assert im.size == (1536, 2176)


def test_acepta_misma_relacion_distinta_escala():
    # mismo ratio (3:2) a otra escala -> válido
    validar_png(_png(1536, 1024), size_esperado=(768, 512))


def test_rechaza_ratio_distinto():
    with pytest.raises(ImagenInvalida):
        validar_png(_png(1024, 1024), size_esperado=(1536, 2176))


def test_rechaza_bytes_corruptos():
    with pytest.raises(ImagenInvalida):
        validar_png(b"no soy un png")
```

- [ ] **Step 2: Correr y ver fallar**

Run: `python -m pytest tests/test_validate.py -v`
Expected: FAIL (ModuleNotFoundError).

- [ ] **Step 3: Implementar**

`ia_kit/validate.py`:
```python
"""Valida la imagen devuelta por OpenAI antes de aceptarla."""
import io
from PIL import Image


class ImagenInvalida(Exception):
    pass


def validar_png(raw, size_esperado=None, tol=0.06):
    try:
        im = Image.open(io.BytesIO(raw))
        im.load()
    except Exception as e:
        raise ImagenInvalida("no se pudo abrir la imagen: %s" % e)
    if size_esperado:
        r_real = im.size[0] / im.size[1]
        r_esp = size_esperado[0] / size_esperado[1]
        if abs(r_real - r_esp) / r_esp > tol:
            raise ImagenInvalida(
                "ratio %.3f != esperado %.3f" % (r_real, r_esp))
    return im
```

- [ ] **Step 4: Correr y ver pasar**

Run: `python -m pytest tests/test_validate.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add ia_kit/validate.py tests/test_validate.py
git commit -m "feat: validación de imagen generada (ratio/abre)"
```

---

### Task 4: Cliente OpenAI Images (con reintentos, transporte inyectable)

**Files:**
- Create: `ia_kit/client.py`
- Test: `tests/test_client.py`

**Interfaces:**
- Consumes: `build_multipart` (Task 2).
- Produces:
  - `class OpenAIImageClient(api_key: str, model: str = "gpt-image-2", opener=None, max_retries: int = 3, base_sleep: float = 1.0, timeout: int = 180)`
  - `.editar(refs: list[bytes], prompt: str, size: str, quality: str = "medium", input_fidelity: str = "high", background: str | None = None) -> bytes`
    — POST a `/v1/images/edits`; devuelve los **bytes PNG** (decodifica `data[0].b64_json`).
    Reintenta en `urllib.error.URLError`/`HTTPError>=500`/timeout hasta `max_retries`.
  - `class OpenAIError(Exception)`.
  - `opener` es un callable `(urllib.request.Request, timeout) -> response-like` (default
    `urllib.request.urlopen`); se inyecta en tests para no pegarle a la red.

- [ ] **Step 1: Escribir el test que falla**

`tests/test_client.py`:
```python
import base64
import io
import json
import urllib.error
import pytest
from ia_kit.client import OpenAIImageClient, OpenAIError


class _Resp:
    def __init__(self, payload):
        self._b = json.dumps(payload).encode()
    def read(self):
        return self._b
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False


def _ok_payload():
    return {"data": [{"b64_json": base64.b64encode(b"PNGDATA").decode()}]}


def test_editar_devuelve_bytes_decodificados():
    calls = {}
    def opener(req, timeout):
        calls["ct"] = req.headers.get("Content-type")
        calls["auth"] = req.headers.get("Authorization")
        return _Resp(_ok_payload())
    c = OpenAIImageClient("sk-test", opener=opener)
    out = c.editar([b"ref1"], "dibuja", "1024x1024")
    assert out == b"PNGDATA"
    assert calls["auth"] == "Bearer sk-test"
    assert calls["ct"].startswith("multipart/form-data")


def test_reintenta_en_500_y_despues_ok():
    estado = {"n": 0}
    def opener(req, timeout):
        estado["n"] += 1
        if estado["n"] == 1:
            raise urllib.error.HTTPError(req.full_url, 500, "boom", {}, io.BytesIO(b""))
        return _Resp(_ok_payload())
    c = OpenAIImageClient("sk-test", opener=opener, max_retries=3, base_sleep=0)
    assert c.editar([b"ref"], "x", "1024x1024") == b"PNGDATA"
    assert estado["n"] == 2


def test_falla_tras_agotar_reintentos():
    def opener(req, timeout):
        raise urllib.error.URLError("sin red")
    c = OpenAIImageClient("sk-test", opener=opener, max_retries=2, base_sleep=0)
    with pytest.raises(OpenAIError):
        c.editar([b"ref"], "x", "1024x1024")
```

- [ ] **Step 2: Correr y ver fallar**

Run: `python -m pytest tests/test_client.py -v`
Expected: FAIL (ModuleNotFoundError).

- [ ] **Step 3: Implementar**

`ia_kit/client.py`:
```python
"""Cliente de OpenAI Images (/v1/images/edits) con urllib stdlib."""
import base64
import json
import time
import urllib.request
import urllib.error

from .multipart import build_multipart

_URL = "https://api.openai.com/v1/images/edits"


class OpenAIError(Exception):
    pass


class OpenAIImageClient:
    def __init__(self, api_key, model="gpt-image-2", opener=None,
                 max_retries=3, base_sleep=1.0, timeout=180):
        self.api_key = api_key
        self.model = model
        self.opener = opener or urllib.request.urlopen
        self.max_retries = max_retries
        self.base_sleep = base_sleep
        self.timeout = timeout

    def editar(self, refs, prompt, size, quality="medium",
               input_fidelity="high", background=None):
        fields = {"model": self.model, "prompt": prompt, "size": size,
                  "quality": quality, "input_fidelity": input_fidelity, "n": "1"}
        if background:
            fields["background"] = background
        files = [("image[]", "ref%d.png" % i, raw) for i, raw in enumerate(refs)]
        ct, body = build_multipart(fields, files)
        last = None
        for intento in range(1, self.max_retries + 1):
            req = urllib.request.Request(_URL, data=body, method="POST", headers={
                "Authorization": "Bearer " + self.api_key, "Content-Type": ct})
            try:
                with self.opener(req, self.timeout) as r:
                    payload = json.loads(r.read().decode("utf-8") or "{}")
                return base64.b64decode(payload["data"][0]["b64_json"])
            except urllib.error.HTTPError as e:
                last = e
                if e.code < 500:  # 4xx no se reintenta
                    raise OpenAIError("OpenAI HTTP %s: %s" % (e.code, e.reason))
            except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as e:
                last = e
            if intento < self.max_retries:
                time.sleep(self.base_sleep * intento)
        raise OpenAIError("falló tras %d intentos: %s" % (self.max_retries, last))
```

- [ ] **Step 4: Correr y ver pasar**

Run: `python -m pytest tests/test_client.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add ia_kit/client.py tests/test_client.py
git commit -m "feat: cliente OpenAI Images con reintentos y transporte inyectable"
```

---

### Task 5: Catálogo de piezas + prompts + paleta

**Files:**
- Create: `ia_kit/catalogo.py`
- Test: `tests/test_catalogo.py`

**Interfaces:**
- Consumes: lee `temas/<tema>/tema.json` (bloque `kit`: `accent`, `ink`, `font`).
- Produces:
  - `PIEZAS: list[Pieza]` con `Pieza = namedtuple("Pieza", "key size por_edad recorte sujeto")`.
    `size` es string OpenAI (`"1536x2176"` portrait, `"1024x1024"` square).
    `por_edad=True` solo para `invitacion` y `afiche`. `recorte=True` para piezas con
    fondo transparente (topper, stickers, banderin, etc.).
  - `paleta_de(temas_dir: str, tema: str) -> dict` → `{"accent","ink","font"}` (con defaults
    si faltan).
  - `bloque_estilo(paleta: dict) -> str` — texto fijo reusado en todos los prompts.
  - `prompt_de(paleta: dict, pieza: Pieza, edad: int | None) -> str`.
- Las `key` de `PIEZAS` cubren exactamente: `invitacion`, `afiche`, y las de
  `_EXTRAS_POR_EDAD`/`_EXTRAS_UNIVERSAL` salvo `afiche` (ya listado). `topper` y `stickers`
  son `por_edad=False` (mixto: número como texto).

- [ ] **Step 1: Escribir el test que falla**

`tests/test_catalogo.py`:
```python
import json
import os
from ia_kit import catalogo


def _tema(tmp_path):
    d = tmp_path / "safari"
    d.mkdir()
    (d / "tema.json").write_text(json.dumps(
        {"id": "safari", "kit": {"accent": "#E0514A", "ink": "#4A4A4A", "font": "Baloo2-VF.ttf"}}))
    return str(tmp_path)


def test_paleta_lee_tema_json(tmp_path):
    pal = catalogo.paleta_de(_tema(tmp_path), "safari")
    assert pal["accent"] == "#E0514A" and pal["ink"] == "#4A4A4A"


def test_paleta_default_si_falta(tmp_path):
    d = tmp_path / "x"; d.mkdir(); (d / "tema.json").write_text("{}")
    pal = catalogo.paleta_de(str(tmp_path), "x")
    assert pal["accent"] and pal["ink"]  # hay defaults


def test_invitacion_y_afiche_por_edad():
    keys = {p.key: p for p in catalogo.PIEZAS}
    assert keys["invitacion"].por_edad is True
    assert keys["afiche"].por_edad is True
    assert keys["topper"].por_edad is False


def test_prompt_incluye_paleta_y_sin_texto():
    pal = {"accent": "#E0514A", "ink": "#4A4A4A", "font": "Baloo2"}
    inv = next(p for p in catalogo.PIEZAS if p.key == "invitacion")
    txt = catalogo.prompt_de(pal, inv, edad=3)
    assert "#E0514A" in txt
    assert "sin texto" in txt.lower() or "no text" in txt.lower()
    assert "3" in txt  # la edad ilustrada


def test_catalogo_cubre_extras_canonicos():
    keys = {p.key for p in catalogo.PIEZAS}
    por_edad = ["afiche", "topper", "stickers", "separadores",
                "etiqueta_botella", "cajita_sorpresa", "decoracion_sorbetes"]
    universal = ["banderin", "etiquetas_multiuso", "wrappers_cupcakes", "tarjetas_agradecimiento"]
    for b in por_edad + universal + ["invitacion"]:
        assert b in keys, b
```

- [ ] **Step 2: Correr y ver fallar**

Run: `python -m pytest tests/test_catalogo.py -v`
Expected: FAIL (ModuleNotFoundError).

- [ ] **Step 3: Implementar**

`ia_kit/catalogo.py`:
```python
"""Catálogo de piezas, paleta del tema y construcción de prompts."""
import json
import os
from collections import namedtuple

Pieza = namedtuple("Pieza", "key size por_edad recorte sujeto")

_PORTRAIT = "1536x2176"   # A4-ish vertical
_SQUARE = "1024x1024"

# key, size, por_edad, recorte, sujeto (la línea variable del prompt)
PIEZAS = [
    Pieza("invitacion", _PORTRAIT, True,  False, "una invitación de cumpleaños vertical"),
    Pieza("afiche", _PORTRAIT, True,  False, "un cartel/afiche vertical de bienvenida"),
    Pieza("topper", _SQUARE, False, True,  "un topper de torta circular con el personaje"),
    Pieza("stickers", _SQUARE, False, True,  "una plancha de stickers variados del personaje"),
    Pieza("separadores", _PORTRAIT, False, True,  "separadores/marcalibros verticales"),
    Pieza("etiqueta_botella", _SQUARE, False, True,  "una etiqueta rectangular para botellita"),
    Pieza("cajita_sorpresa", _SQUARE, False, True,  "el desplegable de una cajita sorpresa"),
    Pieza("decoracion_sorbetes", _SQUARE, False, True,  "banderitas decorativas para sorbetes"),
    Pieza("banderin", _SQUARE, False, True,  "un banderín triangular decorativo"),
    Pieza("etiquetas_multiuso", _SQUARE, False, True,  "una plancha de etiquetas circulares multiuso"),
    Pieza("wrappers_cupcakes", _SQUARE, False, True,  "wrappers (envoltorios) para cupcakes"),
    Pieza("tarjetas_agradecimiento", _PORTRAIT, False, True,  "una tarjeta de agradecimiento vertical"),
]

_DEF = {"accent": "#E0514A", "ink": "#4A4A4A", "font": "Baloo2-VF.ttf"}


def paleta_de(temas_dir, tema):
    try:
        cfg = json.load(open(os.path.join(temas_dir, tema, "tema.json"), encoding="utf-8"))
    except Exception:
        cfg = {}
    kit = cfg.get("kit", {})
    return {k: kit.get(k, _DEF[k]) for k in _DEF}


def bloque_estilo(paleta):
    return (
        "Estilo: ilustración infantil flat vector, líneas limpias, colores planos. "
        "Paleta principal acento %s, tinta/contornos %s. "
        "Usá EXACTAMENTE los personajes de las imágenes de referencia, sin cambiar su diseño. "
        "Importante: NO escribas ningún texto, número ni letra en la imagen "
        "(no text, no letters); dejá zonas limpias y vacías donde luego se coloca el texto."
        % (paleta["accent"], paleta["ink"])
    )


def prompt_de(paleta, pieza, edad=None):
    partes = ["Creá %s para un kit de cumpleaños." % pieza.sujeto]
    if pieza.por_edad and edad is not None:
        partes.append(
            "Integrá el número %d de forma ilustrada y decorativa (como globo o adorno), "
            "no como texto tipográfico." % int(edad))
    partes.append(bloque_estilo(paleta))
    return " ".join(partes)
```

- [ ] **Step 4: Correr y ver pasar**

Run: `python -m pytest tests/test_catalogo.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add ia_kit/catalogo.py tests/test_catalogo.py
git commit -m "feat: catálogo de piezas, paleta y prompts (sin texto)"
```

---

### Task 6: Orquestador de generación (a staging)

**Files:**
- Create: `ia_kit/orquestador.py`
- Test: `tests/test_orquestador.py`

**Interfaces:**
- Consumes: `OpenAIImageClient` (Task 4), `catalogo` (Task 5), `validar_png` (Task 3),
  `quitar_fondo.remove_bg` (existente). Lee `tema["edades"]` vía `temas.cargar_tema`.
- Produces:
  - `generar_tema(client, temas_dir, tema, edades, progress=None, solo=None, quitar=quitar_fondo.remove_bg) -> dict`
    — genera la maestra y cada pieza del `catalogo.PIEZAS`; piezas `por_edad` se generan
    una por cada edad en `edades`; el resto una vez. Las `recorte` pasan por `quitar`.
    Guarda PNG en `temas/<tema>/ia_draft/` con nombres:
    `invitacion_<edad>.png`, `afiche_<edad>.png`, `<base>_<edad>.png` (por_edad no-slot),
    `<base>.png` (universal). `solo` (set de keys) limita a esas piezas (para regenerar).
    `progress(evt: dict)` se llama por pieza con `{"pieza","edad","ok","error"}`.
    Devuelve `{"generadas": [...], "errores": [...]}`.
  - El cliente se inyecta → tests sin red. `quitar` se inyecta (default `remove_bg` real).

- [ ] **Step 1: Escribir el test que falla**

`tests/test_orquestador.py`:
```python
import io
import os
from PIL import Image
from ia_kit import orquestador


class _FakeClient:
    def __init__(self):
        self.prompts = []
    def editar(self, refs, prompt, size, **kw):
        self.prompts.append((prompt, size))
        w, h = (int(x) for x in size.split("x"))
        buf = io.BytesIO(); Image.new("RGB", (w, h), "white").save(buf, "PNG")
        return buf.getvalue()


def _tema_dir(tmp_path):
    d = tmp_path / "safari"; (d / "recortes").mkdir(parents=True)
    (d / "tema.json").write_text('{"kit":{"accent":"#111111","ink":"#222222"}}')
    # un personaje de referencia
    Image.new("RGBA", (64, 64), (255, 0, 0, 255)).save(d / "recortes" / "animal_1.png")
    return str(tmp_path)


def test_genera_slots_por_edad_y_universales(tmp_path):
    td = _tema_dir(tmp_path)
    c = _FakeClient()
    res = orquestador.generar_tema(c, td, "safari", edades=[1, 2, 3],
                                   quitar=lambda im, protect=True: im)
    draft = os.path.join(td, "safari", "ia_draft")
    # invitacion y afiche x3
    for e in (1, 2, 3):
        assert os.path.exists(os.path.join(draft, "invitacion_%d.png" % e))
        assert os.path.exists(os.path.join(draft, "afiche_%d.png" % e))
    # universal x1
    assert os.path.exists(os.path.join(draft, "banderin.png"))
    # por_edad False (topper) -> "topper.png" x1
    assert os.path.exists(os.path.join(draft, "topper.png"))
    assert not res["errores"]


def test_solo_limita_piezas(tmp_path):
    td = _tema_dir(tmp_path)
    res = orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1],
                                   solo={"banderin"}, quitar=lambda im, protect=True: im)
    draft = os.path.join(td, "safari", "ia_draft")
    assert os.path.exists(os.path.join(draft, "banderin.png"))
    assert not os.path.exists(os.path.join(draft, "invitacion_1.png"))


def test_progress_se_invoca(tmp_path):
    td = _tema_dir(tmp_path)
    eventos = []
    orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1],
                             solo={"banderin"}, progress=eventos.append,
                             quitar=lambda im, protect=True: im)
    assert any(e["pieza"] == "banderin" and e["ok"] for e in eventos)
```

- [ ] **Step 2: Correr y ver fallar**

Run: `python -m pytest tests/test_orquestador.py -v`
Expected: FAIL (ModuleNotFoundError).

- [ ] **Step 3: Implementar**

`ia_kit/orquestador.py`:
```python
"""Orquesta la generación de todas las piezas de un tema hacia ia_draft/."""
import glob
import os

import quitar_fondo
from . import catalogo
from .validate import validar_png

_SLOTS = {"invitacion", "afiche"}   # van a temas/<tema>/ (no a extras/)


def _refs(tema_dir):
    paths = sorted(glob.glob(os.path.join(tema_dir, "recortes", "*.png")))
    return [open(p, "rb").read() for p in paths]


def _guardar(im, draft_dir, nombre):
    os.makedirs(draft_dir, exist_ok=True)
    im.save(os.path.join(draft_dir, nombre))


def generar_tema(client, temas_dir, tema, edades, progress=None, solo=None,
                 quitar=quitar_fondo.remove_bg):
    tema_dir = os.path.join(temas_dir, tema)
    draft = os.path.join(tema_dir, "ia_draft")
    pal = catalogo.paleta_de(temas_dir, tema)
    refs = _refs(tema_dir)
    # imagen maestra de estilo: ancla de consistencia, se manda como ref extra
    maestra = client.editar(refs, "Lámina maestra de estilo del tema. " +
                            catalogo.bloque_estilo(pal), catalogo._SQUARE)
    refs_full = refs + [maestra]
    generadas, errores = [], []

    def _emit(pieza, edad, ok, error=""):
        if progress:
            progress({"pieza": pieza, "edad": edad, "ok": ok, "error": error})
        (generadas if ok else errores).append({"pieza": pieza, "edad": edad, "error": error})

    for p in catalogo.PIEZAS:
        if solo and p.key not in solo:
            continue
        edades_pieza = edades if p.por_edad else [None]
        for edad in edades_pieza:
            try:
                raw = client.editar(refs_full, catalogo.prompt_de(pal, p, edad), p.size)
                im = validar_png(raw, size_esperado=tuple(int(x) for x in p.size.split("x")))
                im = im.convert("RGBA")
                if p.recorte:
                    im = quitar(im, protect=True)
                    bb = im.getbbox()
                    if bb:
                        im = im.crop(bb)
                if p.key in _SLOTS or p.por_edad:
                    nombre = "%s_%d.png" % (p.key, edad)
                else:
                    nombre = "%s.png" % p.key
                _guardar(im, draft, nombre)
                _emit(p.key, edad, True)
            except Exception as e:  # una pieza que falla no frena las demás
                _emit(p.key, edad, False, str(e))
    return {"generadas": generadas, "errores": errores}
```

- [ ] **Step 4: Correr y ver pasar**

Run: `python -m pytest tests/test_orquestador.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add ia_kit/orquestador.py tests/test_orquestador.py
git commit -m "feat: orquestador de generación de piezas a ia_draft/"
```

---

### Task 7: Registro de jobs en background

**Files:**
- Create: `ia_kit/jobs.py`
- Test: `tests/test_jobs.py`

**Interfaces:**
- Consumes: nada (stdlib `threading`).
- Produces:
  - `iniciar(fn) -> str` (job_id). `fn(emit)` corre en un thread; `emit(dict)` agrega un evento.
  - `estado(job_id) -> dict` → `{"estado": "corriendo|listo|error", "eventos": [...], "error": str|None}`.
  - Thread-safe. Job desconocido → `{"estado": "desconocido", ...}`.

- [ ] **Step 1: Escribir el test que falla**

`tests/test_jobs.py`:
```python
import time
from ia_kit import jobs


def _esperar(job_id, timeout=3):
    t0 = time.time()
    while time.time() - t0 < timeout:
        st = jobs.estado(job_id)
        if st["estado"] in ("listo", "error"):
            return st
        time.sleep(0.01)
    raise AssertionError("timeout")


def test_job_corre_y_termina():
    def fn(emit):
        emit({"pieza": "a", "ok": True})
    jid = jobs.iniciar(fn)
    st = _esperar(jid)
    assert st["estado"] == "listo"
    assert st["eventos"][0]["pieza"] == "a"


def test_job_captura_error():
    def fn(emit):
        raise RuntimeError("boom")
    st = _esperar(jobs.iniciar(fn))
    assert st["estado"] == "error" and "boom" in st["error"]


def test_job_desconocido():
    assert jobs.estado("nope")["estado"] == "desconocido"
```

- [ ] **Step 2: Correr y ver fallar**

Run: `python -m pytest tests/test_jobs.py -v`
Expected: FAIL (ModuleNotFoundError).

- [ ] **Step 3: Implementar**

`ia_kit/jobs.py`:
```python
"""Registro mínimo de jobs en background (en memoria, thread-safe)."""
import threading
import uuid

_LOCK = threading.Lock()
_JOBS = {}


def iniciar(fn):
    jid = uuid.uuid4().hex
    with _LOCK:
        _JOBS[jid] = {"estado": "corriendo", "eventos": [], "error": None}

    def _emit(evt):
        with _LOCK:
            _JOBS[jid]["eventos"].append(evt)

    def _run():
        try:
            fn(_emit)
            with _LOCK:
                _JOBS[jid]["estado"] = "listo"
        except Exception as e:
            with _LOCK:
                _JOBS[jid]["estado"] = "error"
                _JOBS[jid]["error"] = str(e)

    threading.Thread(target=_run, daemon=True).start()
    return jid


def estado(job_id):
    with _LOCK:
        st = _JOBS.get(job_id)
        if not st:
            return {"estado": "desconocido", "eventos": [], "error": None}
        return {"estado": st["estado"], "eventos": list(st["eventos"]), "error": st["error"]}
```

- [ ] **Step 4: Correr y ver pasar**

Run: `python -m pytest tests/test_jobs.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add ia_kit/jobs.py tests/test_jobs.py
git commit -m "feat: registro de jobs en background"
```

---

### Task 8: Aprobación (mover staging → slots/extras)

**Files:**
- Create: `ia_kit/aprobar.py`
- Test: `tests/test_aprobar.py`

**Interfaces:**
- Consumes: nombres producidos por el orquestador (Task 6) en `ia_draft/`.
- Produces:
  - `aprobar(temas_dir, tema) -> dict` — mueve cada PNG de `temas/<tema>/ia_draft/`:
    `invitacion_*.png` y `afiche_*.png` → `temas/<tema>/` (slots base);
    el resto → `temas/<tema>/extras/`. Devuelve `{"movidas": [...], "n": int}`. Vacía `ia_draft/`.
  - `listar_draft(temas_dir, tema) -> list[str]` — nombres de archivo presentes en `ia_draft/`.

- [ ] **Step 1: Escribir el test que falla**

`tests/test_aprobar.py`:
```python
import os
from PIL import Image
from ia_kit import aprobar


def _draft(tmp_path, *nombres):
    d = tmp_path / "safari" / "ia_draft"; d.mkdir(parents=True)
    for n in nombres:
        Image.new("RGBA", (8, 8)).save(d / n)
    return str(tmp_path)


def test_slots_van_a_la_raiz_del_tema(tmp_path):
    td = _draft(tmp_path, "invitacion_1.png", "afiche_2.png", "banderin.png", "topper.png")
    res = aprobar.aprobar(td, "safari")
    base = os.path.join(td, "safari")
    assert os.path.exists(os.path.join(base, "invitacion_1.png"))
    assert os.path.exists(os.path.join(base, "afiche_2.png"))
    assert os.path.exists(os.path.join(base, "extras", "banderin.png"))
    assert os.path.exists(os.path.join(base, "extras", "topper.png"))
    assert res["n"] == 4
    assert not os.listdir(os.path.join(base, "ia_draft"))


def test_listar_draft(tmp_path):
    td = _draft(tmp_path, "banderin.png")
    assert aprobar.listar_draft(td, "safari") == ["banderin.png"]
```

- [ ] **Step 2: Correr y ver fallar**

Run: `python -m pytest tests/test_aprobar.py -v`
Expected: FAIL (ModuleNotFoundError).

- [ ] **Step 3: Implementar**

`ia_kit/aprobar.py`:
```python
"""Mueve los borradores aprobados de ia_draft/ a los slots/extras que usa el pipeline."""
import os
import shutil

_SLOT_PREFIJOS = ("invitacion_", "afiche_")


def listar_draft(temas_dir, tema):
    d = os.path.join(temas_dir, tema, "ia_draft")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


def aprobar(temas_dir, tema):
    base = os.path.join(temas_dir, tema)
    draft = os.path.join(base, "ia_draft")
    extras = os.path.join(base, "extras")
    os.makedirs(extras, exist_ok=True)
    movidas = []
    for nombre in listar_draft(temas_dir, tema):
        origen = os.path.join(draft, nombre)
        if nombre.startswith(_SLOT_PREFIJOS):
            destino = os.path.join(base, nombre)
        else:
            destino = os.path.join(extras, nombre)
        shutil.move(origen, destino)
        movidas.append(nombre)
    return {"movidas": movidas, "n": len(movidas)}
```

- [ ] **Step 4: Correr y ver pasar**

Run: `python -m pytest tests/test_aprobar.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add ia_kit/aprobar.py tests/test_aprobar.py
git commit -m "feat: aprobar mueve ia_draft a slots/extras"
```

---

### Task 9: Endpoints en servicio.py

**Files:**
- Modify: `servicio.py` (env block ~29-32; imports propios; `do_POST` ~656; `do_GET` ~323)
- Test: `tests/test_endpoints.py`

**Interfaces:**
- Consumes: `ia_kit.jobs`, `ia_kit.orquestador`, `ia_kit.aprobar`, `ia_kit.client.OpenAIImageClient`,
  `temas.cargar_tema`, `temas.TEMAS_DIR`, `temas.existe`.
- Produces (handlers en `Handler`, todos con `_admin_ok()`):
  - `POST /dash/ia-generar?tema=` → arranca job, responde `{"ok":True,"job":<id>}`.
  - `GET /dash/ia-estado?job=` → `{"ok":True,"estado":...,"eventos":[...]}`.
  - `POST /dash/ia-regenerar?tema=&pieza=` → corre `generar_tema(..., solo={pieza})` síncrono, `{"ok":True}`.
  - `POST /dash/ia-aprobar?tema=` → `aprobar(...)`, `{"ok":True,"n":...}`.
  - Helper módulo `_openai_client()` → `OpenAIImageClient(OPENAI_API_KEY, model=OPENAI_IMAGE_MODEL)` o
    `None` si falta la key.
- Nota de testabilidad: la lógica pura ya está testeada (Tasks 6-8). Acá testeamos
  `_openai_client()` (helper de fábrica) sin levantar el server.

- [ ] **Step 1: Escribir el test que falla**

`tests/test_endpoints.py`:
```python
import importlib


def test_factory_devuelve_none_sin_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    import servicio
    importlib.reload(servicio)
    assert servicio._openai_client() is None


def test_factory_crea_cliente_con_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-xyz")
    monkeypatch.setenv("OPENAI_IMAGE_MODEL", "gpt-image-2")
    import servicio
    importlib.reload(servicio)
    c = servicio._openai_client()
    assert c is not None and c.api_key == "sk-xyz" and c.model == "gpt-image-2"
```

- [ ] **Step 2: Correr y ver fallar**

Run: `python -m pytest tests/test_endpoints.py -v`
Expected: FAIL (AttributeError: module 'servicio' has no attribute '_openai_client').

- [ ] **Step 3: Agregar env vars + import + factory en `servicio.py`**

Después de `BASE_URL` (línea ~32) agregar:
```python
OPENAI_API_KEY     = os.environ.get("OPENAI_API_KEY", "")
OPENAI_IMAGE_MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2")
```
En el bloque de imports propios (junto a `import productos, temas, quitar_fondo`):
```python
from ia_kit import jobs as ia_jobs, orquestador as ia_orq, aprobar as ia_aprobar
from ia_kit.client import OpenAIImageClient
```
A nivel módulo (cerca de `_tienda_admin`):
```python
def _openai_client():
    if not OPENAI_API_KEY:
        return None
    return OpenAIImageClient(OPENAI_API_KEY, model=OPENAI_IMAGE_MODEL)
```

- [ ] **Step 4: Correr y ver pasar el test del factory**

Run: `python -m pytest tests/test_endpoints.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Agregar los handlers (dentro de `class Handler`)**

```python
    def _ia_generar(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        client = _openai_client()
        if client is None:
            return self._json(503, {"ok": False, "error": "falta OPENAI_API_KEY"})
        edades = temas.cargar_tema(tema).get("edades", [1, 2, 3])
        def trabajo(emit):
            ia_orq.generar_tema(client, temas.TEMAS_DIR, tema, edades, progress=emit)
        jid = ia_jobs.iniciar(trabajo)
        return self._json(200, {"ok": True, "job": jid})

    def _ia_estado(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        st = ia_jobs.estado(q.get("job", [""])[0])
        return self._json(200, {"ok": True, **st})

    def _ia_regenerar(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        pieza = re.sub(r"[^a-z0-9_]", "", (q.get("pieza", [""])[0] or "").lower())[:30]
        client = _openai_client()
        if client is None:
            return self._json(503, {"ok": False, "error": "falta OPENAI_API_KEY"})
        edades = temas.cargar_tema(tema).get("edades", [1, 2, 3])
        try:
            ia_orq.generar_tema(client, temas.TEMAS_DIR, tema, edades, solo={pieza})
            return self._json(200, {"ok": True})
        except Exception as e:
            return self._json(500, {"ok": False, "error": str(e)})

    def _ia_aprobar(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        res = ia_aprobar.aprobar(temas.TEMAS_DIR, tema)
        generador._specs_cache.pop(tema, None)
        return self._json(200, {"ok": True, **res})
```

- [ ] **Step 6: Rutas en `do_POST` (junto a `/dash/upload-pieza`) y `do_GET`**

En `do_POST` agregar:
```python
        if path == "/dash/ia-generar":
            return self._ia_generar()
        if path == "/dash/ia-regenerar":
            return self._ia_regenerar()
        if path == "/dash/ia-aprobar":
            return self._ia_aprobar()
```
En `do_GET` (junto a las rutas `/dash/...`):
```python
        if path == "/dash/ia-estado":
            return self._ia_estado()
```

- [ ] **Step 7: Verificar import y arranque sin romper**

Run: `python -c "import servicio; print('ok')"`
Expected: imprime `ok` (sin ImportError).
Run: `python -m pytest tests/ -v`
Expected: PASS (toda la suite previa sigue verde).

- [ ] **Step 8: Commit**

```bash
git add servicio.py tests/test_endpoints.py
git commit -m "feat: endpoints /dash/ia-generar|estado|regenerar|aprobar"
```

---

### Task 10: Panel /dash — sección "Generar con IA"

**Files:**
- Modify: `dash.html` (sección de tema + JS de fetch)

**Interfaces:**
- Consumes: `POST /dash/ia-generar`, `GET /dash/ia-estado?job=`, `POST /dash/ia-regenerar`,
  `POST /dash/ia-aprobar` (Task 9). Auth: header `X-API-Key` como el resto del panel.

> Esta tarea es UI (HTML/JS) y se valida manualmente — no lleva test unitario.

- [ ] **Step 1: Agregar el bloque UI en la vista de tema**

Insertar en `dash.html`, dentro del panel del tema seleccionado:
```html
<section id="ia-kit">
  <h3>Generar piezas con IA</h3>
  <button id="ia-generar">✨ Generar kit con IA</button>
  <div id="ia-progreso"></div>
  <div id="ia-grilla" class="grilla"></div>
  <button id="ia-aprobar" hidden>✅ Aprobar y publicar</button>
</section>
```

- [ ] **Step 2: Agregar el JS (polling de estado + grilla + aprobar/regenerar)**

```html
<script>
const TEMA = window.TEMA_ACTUAL;           // ya expuesto por dash.html
const H = {"X-API-Key": window.API_KEY};   // ya expuesto por dash.html
async function iaGenerar() {
  const r = await fetch(`/dash/ia-generar?tema=${TEMA}`, {method:"POST", headers:H});
  const {job, error} = await r.json();
  if (!job) return alert(error || "no arrancó");
  poll(job);
}
async function poll(job) {
  const r = await fetch(`/dash/ia-estado?job=${job}`, {headers:H});
  const st = await r.json();
  document.getElementById("ia-progreso").textContent =
    `${st.estado} — ${st.eventos.length} piezas`;
  if (st.estado === "corriendo") return setTimeout(()=>poll(job), 2000);
  pintarGrilla();
  document.getElementById("ia-aprobar").hidden = false;
}
function pintarGrilla() {
  // Poblar con <img src=/dash/ia-draft/${TEMA}/<archivo>> + botón Regenerar por pieza.
  // El listado de archivos sale de los eventos del job (pieza+edad -> nombre).
  const g = document.getElementById("ia-grilla");
  g.innerHTML = "";
}
async function iaRegenerar(pieza) {
  await fetch(`/dash/ia-regenerar?tema=${TEMA}&pieza=${pieza}`, {method:"POST", headers:H});
  pintarGrilla();
}
async function iaAprobar() {
  const r = await fetch(`/dash/ia-aprobar?tema=${TEMA}`, {method:"POST", headers:H});
  const {n} = await r.json();
  alert(`${n} piezas aprobadas y listas para publicar`);
}
document.getElementById("ia-generar").onclick = iaGenerar;
document.getElementById("ia-aprobar").onclick = iaAprobar;
</script>
```
> Nota: para previsualizar los borradores hay que servir `ia_draft/`. Si el handler de
> estáticos existente en `do_GET` no cubre `temas/<tema>/ia_draft/...`, agregar en Task 9 una
> ruta GET `/dash/ia-draft/<tema>/<archivo>` que lea de `ia_draft/` (con `_admin_ok()` y
> sanitización del nombre, sin `..`). Verificar contra el handler de estáticos existente.

- [ ] **Step 3: Verificación manual**

1. `OPENAI_API_KEY=sk-... python servicio.py` (o el systemd con la env seteada).
2. Entrar a `/dash`, elegir un tema con personajes en `recortes/`.
3. Click "Generar kit con IA" → el progreso avanza y aparece la grilla.
4. Regenerar una pieza puntual → se actualiza.
5. "Aprobar y publicar" → confirmar que los archivos aparecieron en `temas/<tema>/` y `extras/`.
6. Generar un kit normal del tema y confirmar que ahora usa el arte de IA.

- [ ] **Step 4: Commit**

```bash
git add dash.html
git commit -m "feat: panel /dash sección Generar con IA"
```

---

### Task 11: Docs + runbook de smoke real

**Files:**
- Modify: `README.md`
- Create: `docs/superpowers/MOTOR-IA-RUNBOOK.md`

**Interfaces:** ninguna (documentación).

- [ ] **Step 1: Documentar la env var en README**

Agregar a la sección de configuración:
```markdown
### Generación con IA (OpenAI)
- `OPENAI_API_KEY` (requerida para `/dash/ia-*`) — key de OpenAI con acceso a imágenes.
- `OPENAI_IMAGE_MODEL` (default `gpt-image-2`).
Costo aprox.: ~US$0,80 (medium) / ~US$2,90 (high) por tema, una sola vez.
```

- [ ] **Step 2: Runbook con el smoke real**

`docs/superpowers/MOTOR-IA-RUNBOOK.md`:
```markdown
# Runbook — Motor IA piezas del kit
1. Setear `OPENAI_API_KEY` en el env del servicio (systemd `ct3d-kit.service`).
2. Asegurar Tier 2+ de OpenAI (≥20 IPM) antes de tandas grandes.
3. Subir personajes del tema (recortes/) por /dash.
4. /dash → "Generar kit con IA" (medium para borrador).
5. Revisar grilla, regenerar lo que falle, Aprobar.
6. Verificar costo real en el dashboard de OpenAI vs estimado.
7. Re-verificar id de modelo vigente (deprecaciones dic-2026).
```

- [ ] **Step 3: Correr toda la suite**

Run: `python -m pytest tests/ -v`
Expected: PASS (toda la suite verde).

- [ ] **Step 4: Commit**

```bash
git add README.md docs/superpowers/MOTOR-IA-RUNBOOK.md
git commit -m "docs: env vars y runbook del motor IA"
```

---

## Self-Review

**Spec coverage:**
- Subir personajes → generar todas las piezas: Tasks 5-6 (catálogo + orquestador). ✓
- OpenAI solo ilustra / sin texto: Task 5 (prompts piden "sin texto"); el texto lo pone el
  pipeline existente. ✓
- `gpt-image-2` vía `/v1/images/edits` con refs (personajes + maestra): Tasks 4, 6. ✓
- Edades "mixto" (invitación/afiche ×3, resto ×1): Task 6 (`por_edad`). ✓
- Transparencia vía `quitar_fondo`: Task 6 (`recorte` → `quitar`). ✓
- Validación + reintento por imagen: Tasks 3, 4. ✓
- Staging + gate de aprobación: Tasks 6 (ia_draft), 8 (aprobar), 10 (panel). ✓
- Background job (latencia alta): Task 7. ✓
- Reuso del pipeline sin cambios: Task 8 escribe a slots/extras que `_piezas_kit` ya levanta. ✓
- Costo/env documentado: Task 11. ✓
- **Fuera de alcance (Plan B):** packs de actividades + planificador GPT-texto. Documentado arriba.

**Placeholder scan:** sin TBD/TODO en código. Task 10 (UI) tiene `pintarGrilla()` con cuerpo
mínimo y comentario de poblamiento porque depende del handler de estáticos existente; su
verificación es manual (Step 3) — es UI, no lógica testeable.

**Type consistency:** `editar(refs, prompt, size, ...)` se usa igual en Tasks 4 y 6 (y en el
`_FakeClient` del test). `generar_tema(client, temas_dir, tema, edades, progress, solo, quitar)`
consistente entre Task 6 y Task 9. `aprobar(temas_dir, tema)` consistente entre Tasks 8 y 9.
Nombres de archivo (`invitacion_<edad>.png`, `<base>.png`) consistentes entre Tasks 6, 8 y las
constantes de `productos.py`. ✓
