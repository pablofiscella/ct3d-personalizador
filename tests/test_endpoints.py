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
