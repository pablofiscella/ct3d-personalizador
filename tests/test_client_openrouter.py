"""Cliente OpenRouter + failover — con opener fake, sin red."""
import base64
import io
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ia_kit.client_openrouter import (OpenRouterImageClient, OpenRouterError,
                                      ClienteImagenesFailover)

PNG = base64.b64encode(b"fake-png-bytes").decode()


class _Resp:
    def __init__(self, payload):
        self._b = json.dumps(payload).encode()
    def read(self):
        return self._b
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass


def test_editar_arma_request_y_decodifica():
    reqs = []
    def opener(req, timeout=None):
        reqs.append(json.loads(req.data))
        return _Resp({"data": [{"b64_json": PNG}]})
    cl = OpenRouterImageClient("key", opener=opener)
    out = cl.editar([b"ref-bytes"], "un prompt", "1024x1536", quality="high")
    assert out == b"fake-png-bytes"
    body = reqs[0]
    assert body["aspect_ratio"] == "2:3" and body["quality"] == "high"
    assert body["input_references"][0]["image_url"]["url"].startswith("data:image/png;base64,")


def test_failover_usa_respaldo():
    class _Primario:
        def editar(self, *a, **k):
            raise RuntimeError("billing_hard_limit_reached")
    class _Respaldo:
        def editar(self, *a, **k):
            return b"desde-openrouter"
    fo = ClienteImagenesFailover(_Primario(), _Respaldo())
    assert fo.editar([], "p", "1024x1024") == b"desde-openrouter"


def test_failover_no_toca_respaldo_si_primario_anda():
    class _Primario:
        def editar(self, *a, **k):
            return b"desde-openai"
    class _Respaldo:
        def editar(self, *a, **k):
            raise AssertionError("no debería llamarse")
    fo = ClienteImagenesFailover(_Primario(), _Respaldo())
    assert fo.editar([], "p", "1024x1024") == b"desde-openai"


def test_failover_no_tapa_rechazo_de_seguridad():
    """Un rechazo de contenido/seguridad de OpenAI (HTTP 400) NO debe caer a
    OpenRouter: eso enmascaraba la causa real como '402 sin crédito' (bug de Pablo
    8-jul-2026). Se re-lanza el error real del primario."""
    class _Primario:
        def editar(self, *a, **k):
            raise RuntimeError("OpenAI HTTP 400: Bad Request — "
                               "Your request was rejected by the safety system.")
    class _Respaldo:
        def editar(self, *a, **k):
            raise AssertionError("no debería tocar OpenRouter en un rechazo de seguridad")
    fo = ClienteImagenesFailover(_Primario(), _Respaldo())
    with pytest.raises(RuntimeError, match="safety system"):
        fo.editar([], "p", "1024x1024")


def test_failover_cae_si_se_agotan_los_reintentos():
    """429/5xx/red agotan reintentos en ia_kit.client ('falló tras N intentos'):
    ESO sí lo cubre OpenRouter, así que cae al respaldo."""
    class _Primario:
        def editar(self, *a, **k):
            raise RuntimeError("falló tras 3 intentos: HTTP 429: Too Many Requests")
    class _Respaldo:
        def editar(self, *a, **k):
            return b"desde-openrouter"
    fo = ClienteImagenesFailover(_Primario(), _Respaldo())
    assert fo.editar([], "p", "1024x1024") == b"desde-openrouter"
