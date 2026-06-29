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
                # timeout SIEMPRE por keyword: el 2º posicional de urlopen es `data`
                # (el cuerpo), no el timeout — pasarlo posicional manda el int como body.
                with self.opener(req, timeout=self.timeout) as r:
                    raw = r.read().decode("utf-8")
            except urllib.error.HTTPError as e:
                last = e
                if e.code < 500:  # 4xx no se reintenta
                    raise OpenAIError("OpenAI HTTP %s: %s" % (e.code, e.reason))
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
