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
