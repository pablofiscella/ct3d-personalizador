import importlib

import pytest


# ── el cliente de imágenes y su failover ────────────────────────────────────────────
#
# 30-jul-2026 — estos dos tests estaban ROJOS y no era un bug del código. El 03-jul se le
# agregó a `_openai_client()` un **failover a OpenRouter**, porque el tope mensual de OpenAI
# nos frenó generaciones dos veces. Los tests seguían esperando el mundo anterior: uno
# afirmaba "sin key de OpenAI → None" (ahora, si hay key de OpenRouter, devuelve el respaldo)
# y el otro leía `c.api_key` (ahora viene envuelto en el failover, que no expone ese campo).
#
# Y arrastraban un problema peor: `_leer_openrouter_key()` cae a `config.json` —incluido
# `/opt/ct3d/backend/config.json`, el de PRODUCCIÓN— cuando no hay variable de entorno. O sea
# que su resultado dependía de la máquina donde corrieran. Por eso ahora las dos claves se
# fijan sobre el módulo ya cargado, y no por entorno: es lo único que las hace reproducibles.

@pytest.fixture
def factory(monkeypatch):
    """`servicio` recargado, con las dos claves bajo control del test."""
    import servicio
    importlib.reload(servicio)

    def con(openai=None, openrouter=None, modelo="gpt-image-2"):
        monkeypatch.setattr(servicio, "OPENAI_API_KEY", openai or "")
        monkeypatch.setattr(servicio, "OPENROUTER_API_KEY", openrouter or "")
        monkeypatch.setattr(servicio, "OPENAI_IMAGE_MODEL", modelo)
        return servicio._openai_client()
    return con


def test_sin_ninguna_key_no_hay_cliente(factory):
    """Sin nada configurado no se inventa un cliente: el pipeline tiene que poder decir
    'no hay IA' en vez de fallar al primer request."""
    assert factory() is None


def test_solo_openai_da_el_cliente_directo(factory):
    c = factory(openai="sk-xyz")
    assert c is not None and c.api_key == "sk-xyz" and c.model == "gpt-image-2"


def test_solo_openrouter_da_el_respaldo(factory):
    """Sin OpenAI pero con OpenRouter, el respaldo trabaja SOLO. Antes este caso devolvía
    None y el pipeline se quedaba sin IA teniendo con qué generar."""
    from ia_kit.client_openrouter import OpenRouterImageClient
    c = factory(openrouter="or-abc")
    assert isinstance(c, OpenRouterImageClient)


def test_con_las_dos_arma_el_failover_con_openai_de_primario(factory):
    """LA razón de que exista el failover: el tope mensual de OpenAI nos frenó generaciones
    dos veces (03-jul-2026). OpenAI tiene que quedar de PRIMARIO — OpenRouter es respaldo,
    no reemplazo: si se invirtiera, se pagaría el intermediario en cada imagen."""
    from ia_kit.client_openrouter import ClienteImagenesFailover, OpenRouterImageClient
    c = factory(openai="sk-xyz", openrouter="or-abc")
    assert isinstance(c, ClienteImagenesFailover)
    assert c.primario.api_key == "sk-xyz", "el primario tiene que ser el de OpenAI"
    assert isinstance(c.respaldo, OpenRouterImageClient)


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
