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


def test_demo_rompecabezas_token_tema_invalido(monkeypatch):
    """Auditoría 16-jul-2026 (demo pública): tema inexistente → None (la ruta
    /probar/rompecabezas/<tema> devuelve 404)."""
    import servicio
    monkeypatch.setattr(servicio.temas, "existe", lambda t: False)
    assert servicio._demo_rompecabezas_token("no-existe") is None
    assert servicio._demo_rompecabezas_token("") is None


def test_demo_rompecabezas_token_reusa_si_existe(monkeypatch):
    """Si el demo-<tema> ya está generado, NO regenera (hits repetidos baratos)."""
    import servicio, rompecabezas_web
    monkeypatch.setattr(servicio.temas, "existe", lambda t: True)
    monkeypatch.setattr(servicio.os.path, "exists", lambda p: True)
    llamado = {"crear": False}
    monkeypatch.setattr(rompecabezas_web, "crear",
                        lambda *a, **k: llamado.__setitem__("crear", True))
    assert servicio._demo_rompecabezas_token("safari") == "demo-safari"
    assert llamado["crear"] is False


def test_demo_rompecabezas_token_crea_si_falta(monkeypatch):
    """Si falta el demo, lo crea con nombre vacío (genérico, sin foto del cliente)."""
    import servicio, rompecabezas_web
    monkeypatch.setattr(servicio.temas, "existe", lambda t: True)
    monkeypatch.setattr(servicio.os.path, "exists", lambda p: False)
    creado = {}
    monkeypatch.setattr(rompecabezas_web, "crear",
                        lambda data, tema, token=None: creado.update(data=data, tema=tema, token=token) or token)
    assert servicio._demo_rompecabezas_token("Circo!") == "demo-circo"   # slug normaliza
    assert creado == {"data": {"nombre": ""}, "tema": "circo", "token": "demo-circo"}
