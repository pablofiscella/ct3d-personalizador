import os
import json
import importlib


def _fresh_audiolibro(tmp_path, monkeypatch):
    """Recarga el módulo apuntando AUDIOLIBROS_DIR a un dir temporal."""
    monkeypatch.setenv("CT3D_AUDIOLIBROS_DIR", str(tmp_path / "audiolibros"))
    import audiolibro
    return importlib.reload(audiolibro)


def test_estado_ciclo_de_vida(tmp_path, monkeypatch):
    al = _fresh_audiolibro(tmp_path, monkeypatch)
    tok = "AbC012_def-GhI"   # 14 chars, dentro de [8,32]

    # Token desconocido → None
    assert al.estado(tok) is None

    # marcar_generando → 'generando' + marcador en disco
    al.marcar_generando(tok)
    assert os.path.isfile(os.path.join(al.AUDIOLIBROS_DIR, tok, ".generando"))
    assert al.estado(tok) == "generando"

    # Al terminar (manifest escrito, marcador quitado) → 'listo'
    with open(os.path.join(al.AUDIOLIBROS_DIR, tok, "manifest.json"), "w") as f:
        json.dump({"tema": "safari", "nombre": "T", "paginas": 10, "creado": 1}, f)
    al._quitar_generando(tok)
    assert not os.path.isfile(os.path.join(al.AUDIOLIBROS_DIR, tok, ".generando"))
    assert al.estado(tok) == "listo"


def test_manifest_gana_sobre_marcador(tmp_path, monkeypatch):
    al = _fresh_audiolibro(tmp_path, monkeypatch)
    tok = "Zz001122_abcd"
    al.marcar_generando(tok)
    with open(os.path.join(al.AUDIOLIBROS_DIR, tok, "manifest.json"), "w") as f:
        json.dump({"paginas": 10}, f)
    # Aunque quede el marcador, si hay manifest el visor debe considerarlo listo.
    assert al.estado(tok) == "listo"


def test_token_invalido_no_crea_nada(tmp_path, monkeypatch):
    al = _fresh_audiolibro(tmp_path, monkeypatch)
    assert al.estado("x") is None            # muy corto
    assert al.estado("con espacios!") is None
    al.marcar_generando("bad token!")        # inválido → no-op
    assert not os.path.isdir(os.path.join(al.AUDIOLIBROS_DIR, "bad token!"))


def _escribir_manifest(al, tok, **extra):
    d = os.path.join(al.AUDIOLIBROS_DIR, tok)
    os.makedirs(d, exist_ok=True)
    base = {"tema": "safari", "nombre": "Sofía", "titulo": "El cuento", "paginas": 10}
    base.update(extra)
    with open(os.path.join(d, "manifest.json"), "w") as f:
        json.dump(base, f)


def test_html_cta_url_lleva_la_voz_del_manifest(tmp_path, monkeypatch):
    """14-jul-2026: Pablo quiere saber con qué voz se creó cada cuenta nueva
    que entra por el banner "guardar en cuenta" — el link tiene que llevar
    la voz que efectivamente narró ESE audiolibro, no un valor fijo."""
    al = _fresh_audiolibro(tmp_path, monkeypatch)
    tok = "TokenVozMalena01"
    _escribir_manifest(al, tok, voz="malena")
    html = al.html(tok)
    assert "cta_url=" not in html  # el % ya interpoló, no queda el placeholder
    assert "mi-cuenta/crear?voz=malena" in html


def test_html_cta_url_default_lizy_si_manifest_viejo_sin_voz(tmp_path, monkeypatch):
    """Manifests generados ANTES de este cambio no tienen "voz" — no debe
    romper, cae a lizy (el default histórico real)."""
    al = _fresh_audiolibro(tmp_path, monkeypatch)
    tok = "TokenSinVozViejo1"
    _escribir_manifest(al, tok)  # sin "voz"
    html = al.html(tok)
    assert "mi-cuenta/crear?voz=lizy" in html


def test_tts_mp3_rutea_voz_alternativa_elevenlabs(monkeypatch):
    """14-jul-2026: Malena (_EL_VOCES_ALT) tiene que pasar SU voice_id/
    settings a _tts_elevenlabs — nunca los de Lizy — y sin tocar OpenAI."""
    import audiolibro as al
    llamadas = []

    def fake_el(texto, timeout=120, seed=None, voice_id=None, settings=None):
        llamadas.append(("el", voice_id, settings))
        return b"x" * 20000  # bytes suficientes para pasar _duracion_ok

    def fake_openai(api_key, texto, timeout, voz):
        llamadas.append(("openai", voz))
        return b"y" * 20000

    monkeypatch.setattr(al, "_tts_elevenlabs", fake_el)
    monkeypatch.setattr(al, "_tts_openai", fake_openai)
    monkeypatch.setattr(al, "_duracion_ok", lambda texto, mp3: True)

    al.tts_mp3(api_key="k", texto="Hola", voz="malena", seed=1)
    assert llamadas[-1] == ("el", "p7AwDmKvTdoHTBuueGvP", {"stability": 0.5})

    llamadas.clear()
    al.tts_mp3(api_key="k", texto="Hola", voz=None, seed=1)
    assert llamadas[-1] == ("el", None, None)   # default → Lizy (sin override)

    llamadas.clear()
    al.tts_mp3(api_key="k", texto="Hola", voz="fable", seed=1)
    assert llamadas == [("openai", "fable")]    # voz OpenAI: ni pasa por ElevenLabs
