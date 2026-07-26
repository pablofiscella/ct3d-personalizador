"""La voz por defecto del audiolibro es Valeria (rioplatense), no Lizy (neutra).

Pablo, 25-jul-2026: "Valeria tiene que ser la voz por default". Encaja con la regla de
siempre — la voz del producto tiene que sonar argentina — y con que Valeria ya era el
default de las actividades, así que ahora toda la línea suena igual.
"""
import importlib


def _fresh(tmp_path, monkeypatch):
    monkeypatch.setenv("CT3D_AUDIOLIBROS_DIR", str(tmp_path / "audiolibros"))
    import audiolibro
    return importlib.reload(audiolibro)


def test_la_voz_default_es_valeria(tmp_path, monkeypatch):
    al = _fresh(tmp_path, monkeypatch)
    assert al.VOZ_DEFAULT == "valeria"


def test_la_voz_default_existe_de_verdad(tmp_path, monkeypatch):
    """Un default que no está en el catálogo de voces rompería toda narración."""
    al = _fresh(tmp_path, monkeypatch)
    assert al.VOZ_DEFAULT in al._VOCES_VALIDAS
    assert al.VOZ_DEFAULT in al._EL_VOCES_ALT, "tiene que tener voice_id propio de ElevenLabs"


def test_sin_voz_elegida_narra_con_valeria(tmp_path, monkeypatch):
    """El caso que importa: una compra que no especifica voz (ML, regalo, token viejo)
    tiene que sonar rioplatense, no caer al preset neutro de ElevenLabs."""
    al = _fresh(tmp_path, monkeypatch)
    usados = {}

    def _fake(texto, timeout, seed=None, voice_id=None, settings=None):
        usados["voice_id"] = voice_id
        return b"\xff\xf3" + b"\x00" * 4000

    monkeypatch.setattr(al, "_tts_elevenlabs", _fake)
    monkeypatch.setattr(al, "_duracion_ok", lambda *a, **k: True)
    al.tts_mp3(None, "Había una vez un cuento corto.", voz=None)
    assert usados["voice_id"] == al._EL_VOCES_ALT["valeria"]["voice_id"]


def test_si_el_cliente_elige_otra_voz_se_respeta(tmp_path, monkeypatch):
    """El default no puede pisar la elección del comprador."""
    al = _fresh(tmp_path, monkeypatch)
    usados = {}

    def _fake(texto, timeout, seed=None, voice_id=None, settings=None):
        usados["voice_id"] = voice_id
        return b"\xff\xf3" + b"\x00" * 4000

    monkeypatch.setattr(al, "_tts_elevenlabs", _fake)
    monkeypatch.setattr(al, "_duracion_ok", lambda *a, **k: True)
    al.tts_mp3(None, "Texto.", voz="malena")
    assert usados["voice_id"] == al._EL_VOCES_ALT["malena"]["voice_id"]


def test_lizy_sigue_siendo_elegible(tmp_path, monkeypatch):
    """Dejó de ser el default, pero sigue en el catálogo: hay libros vendidos con ella."""
    al = _fresh(tmp_path, monkeypatch)
    assert "lizy" in al._VOCES_VALIDAS
