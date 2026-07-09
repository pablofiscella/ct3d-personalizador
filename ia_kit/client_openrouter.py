"""Cliente de imágenes vía OpenRouter (Image API unificada) + failover.

OpenRouter proxea 30+ modelos de imagen (incluidos los GPT Image de OpenAI) con
crédito propio — sirve como RESPALDO cuando la cuenta directa de OpenAI toca su
tope mensual (billing_hard_limit, nos frenó 2 veces el 03-jul), y para modelos
más baratos en piezas simples.

Misma interfaz que ia_kit.client.OpenAIImageClient: .editar(refs, prompt, size,
quality=) -> bytes PNG. El failover se arma en servicio._openai_client() cuando
existe OPENROUTER_API_KEY en el entorno.
"""
import base64
import json
import time
import urllib.request

_URL = "https://openrouter.ai/api/v1/images"

# "1024x1536" (formato OpenAI que usa todo el pipeline) -> aspect_ratio OpenRouter
_ASPECT = {"1024x1024": "1:1", "1024x1536": "2:3", "1536x1024": "3:2"}


class OpenRouterError(Exception):
    pass


class OpenRouterImageClient:
    def __init__(self, api_key, model="openai/gpt-5.4-image-2", opener=None,
                 max_retries=3, base_sleep=1.0, timeout=180):
        self.api_key = api_key
        self.model = model
        self.opener = opener or urllib.request.urlopen
        self.max_retries = max_retries
        self.base_sleep = base_sleep
        self.timeout = timeout

    def editar(self, refs, prompt, size, quality="medium",
               input_fidelity=None, background=None):
        body = {"model": self.model, "prompt": prompt, "n": 1,
                "quality": quality, "output_format": "png",
                "aspect_ratio": _ASPECT.get(size, "1:1")}
        if background:
            body["background"] = background
        if refs:
            body["input_references"] = [
                {"type": "image_url",
                 "image_url": {"url": "data:image/png;base64," +
                               base64.b64encode(raw).decode()}}
                for raw in refs]
        data = json.dumps(body).encode()
        last = None
        for intento in range(1, self.max_retries + 1):
            req = urllib.request.Request(_URL, data=data, method="POST", headers={
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json"})
            try:
                with self.opener(req, timeout=self.timeout) as r:
                    raw = r.read().decode("utf-8")
            except urllib.error.HTTPError as e:
                try:
                    cuerpo = e.read().decode("utf-8", "replace")[:600]
                except Exception:
                    cuerpo = ""
                last = "HTTP %s: %s — %s" % (e.code, e.reason, cuerpo)
                if e.code != 429 and e.code < 500:
                    raise OpenRouterError("OpenRouter " + last)
            except (urllib.error.URLError, TimeoutError) as e:
                last = e
            else:
                try:
                    payload = json.loads(raw)
                    return base64.b64decode(payload["data"][0]["b64_json"])
                except (KeyError, IndexError, TypeError, ValueError) as e:
                    raise OpenRouterError("respuesta inesperada: %s" % e)
            if intento < self.max_retries:
                time.sleep(self.base_sleep * intento)
        raise OpenRouterError("falló tras %d intentos: %s" % (self.max_retries, last))


def _es_falla_por_disponibilidad(e):
    """True SOLO si OpenAI falló por algo que OpenRouter PUEDE cubrir: crédito/cuota
    agotada, tope de facturación, rate-limit (429) o caída del servicio (5xx/red).
    Un rechazo de contenido/seguridad (HTTP 400) u otro 4xx inmediato devuelve
    False: ese error se re-lanza tal cual, porque OpenRouter no lo arregla y
    enmascararlo como '402 sin crédito' esconde la causa real (pasó con el fondo
    memoria_dorso — OpenAI lo rechazó por 'safety system' y el failover lo tapó,
    Pablo 8-jul-2026)."""
    m = str(e).lower()
    if "safety system" in m or "moderation" in m or "content_policy" in m:
        return False
    if any(s in m for s in ("insufficient_quota", "billing", "hard_limit",
                            "exceeded your current quota")):
        return True
    # ia_kit.client sólo agota reintentos ("falló tras N intentos") en 429/5xx/red;
    # los 4xx de contenido cortan de una, sin ese prefijo.
    return "falló tras" in m


class ClienteImagenesFailover:
    """Intenta con el primario (OpenAI directo). Cae al respaldo (OpenRouter) SÓLO
    si el fallo es por crédito/cuota/límite o caída de OpenAI —lo que OpenRouter
    puede cubrir—; ante un rechazo de contenido/seguridad u otro error real,
    re-lanza el error del primario sin tocar el respaldo. Los dos exponen .editar()."""

    def __init__(self, primario, respaldo):
        self.primario = primario
        self.respaldo = respaldo

    def editar(self, refs, prompt, size, quality="medium", **kw):
        try:
            return self.primario.editar(refs, prompt, size, quality=quality, **kw)
        except Exception as e:
            if not _es_falla_por_disponibilidad(e):
                raise   # error real (p.ej. rechazo de seguridad 400): que se vea
            print("[ia] OpenAI sin disponibilidad (%s) — probando respaldo OpenRouter"
                  % str(e)[:120], flush=True)
            return self.respaldo.editar(refs, prompt, size, quality=quality)
