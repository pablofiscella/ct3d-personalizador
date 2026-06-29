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
               input_fidelity=None, background=None):
        fields = {"model": self.model, "prompt": prompt, "size": size,
                  "quality": quality, "n": "1"}
        # gpt-image-2 NO soporta input_fidelity; solo se manda si se pide explícito.
        if input_fidelity:
            fields["input_fidelity"] = input_fidelity
        if background:
            fields["background"] = background
        # OpenAI /images/edits: para VARIAS imágenes de referencia el campo es "image[]"
        # (lo confirma el propio error "Duplicate parameter: 'image'... use 'image[]'").
        # Mandar "image" repetido da 400 duplicate; "image[]" es la sintaxis de lista.
        files = [("image[]", "ref%d.png" % i, raw) for i, raw in enumerate(refs)]
        ct, body = build_multipart(fields, files)
        last = None
        for intento in range(1, self.max_retries + 1):
            req = urllib.request.Request(_URL, data=body, method="POST", headers={
                "Authorization": "Bearer " + self.api_key, "Content-Type": ct})
            try:
                # timeout SIEMPRE por keyword: el 2º posicional de urlopen es `data`
                # (el cuerpo), no el timeout — pasarlo posicional manda el int como body.
                with self.opener(req, timeout=self.timeout) as r:
                    raw = r.read().decode("utf-8")
            except urllib.error.HTTPError as e:
                try:    # el cuerpo trae el detalle real del error de OpenAI
                    cuerpo = e.read().decode("utf-8", "replace")[:600]
                except Exception:
                    cuerpo = ""
                last = "HTTP %s: %s — %s" % (e.code, e.reason, cuerpo)
                # 4xx no se reintenta, SALVO 429 (rate limit) que es transitorio.
                if e.code != 429 and e.code < 500:
                    raise OpenAIError("OpenAI " + last)
            except (urllib.error.URLError, TimeoutError) as e:
                last = e
            else:
                # Respuesta HTTP exitosa — parse fail-fast, sin reintentos
                try:
                    payload = json.loads(raw)
                    return base64.b64decode(payload["data"][0]["b64_json"])
                except (KeyError, IndexError, TypeError, ValueError) as e:
                    raise OpenAIError("respuesta inesperada de OpenAI: %s" % e)
            if intento < self.max_retries:
                time.sleep(self.base_sleep * intento)
        raise OpenAIError("falló tras %d intentos: %s" % (self.max_retries, last))
