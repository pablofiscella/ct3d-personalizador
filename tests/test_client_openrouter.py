"""Cliente OpenRouter + failover — con opener fake, sin red."""
import base64
import io
import json
import os
import sys

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
