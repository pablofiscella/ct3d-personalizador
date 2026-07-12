"""Guardián de la narración por nodo del prototipo "Elegí tu aventura"
(aventura_audio + el enganche en aventura_web): un MP3 por nodo, progresivo (retoma
donde quedó si se corta a mitad de camino), servido con el mismo whitelist que las
imágenes."""
import os

import aventura_audio
import aventura_web as avw


def _tts_falso(llamadas):
    def tts(api_key, texto, timeout=120, voz=None, seed=None):
        llamadas.append(texto)
        return b"MP3FAKE:" + texto[:8].encode("utf-8")
    return tts


def _crear(tmp_path, nombre="Sofía"):
    avw.AV_DIR = str(tmp_path)
    return avw.crear({"nombre": nombre, "tema": "safari"})


def test_generar_arma_un_mp3_por_nodo(tmp_path):
    llamadas = []
    nodos = {"hook": {"texto": "Sofía encontró un mapa."},
              "camino": {"texto": "Sofía salió del campamento."}}
    dest = tmp_path / "audio"
    out = aventura_audio.generar("tok123", nodos, str(dest),
                                 tts=_tts_falso(llamadas), progress=None)
    assert len(out) == 2
    assert len(llamadas) == 2
    assert os.path.isfile(dest / "hook.mp3")
    assert os.path.isfile(dest / "camino.mp3")


def test_generar_es_progresivo_no_repite_nodos_ya_generados(tmp_path):
    llamadas = []
    nodos = {"hook": {"texto": "texto A"}, "camino": {"texto": "texto B"}}
    dest = tmp_path / "audio"
    aventura_audio.generar("tok123", nodos, str(dest), tts=_tts_falso(llamadas))
    assert len(llamadas) == 2
    # segunda corrida: ya están los dos, no debería llamar al tts de nuevo
    aventura_audio.generar("tok123", nodos, str(dest), tts=_tts_falso(llamadas))
    assert len(llamadas) == 2


def test_estado_audio_none_parcial_listo(tmp_path):
    tok = _crear(tmp_path)
    reg = avw._cargar(tok)
    nodos = reg["nodos"]
    assert avw.estado_audio(tok) is None

    llamadas = []
    algunos = dict(list(nodos.items())[:3])
    aventura_audio.generar(tok, algunos, avw.audio_dir(tok), tts=_tts_falso(llamadas))
    assert avw.estado_audio(tok) == "parcial"

    aventura_audio.generar(tok, nodos, avw.audio_dir(tok), tts=_tts_falso(llamadas))
    assert avw.estado_audio(tok) == "listo"


def test_generar_audio_wrapper_llama_a_aventura_audio_generar(tmp_path, monkeypatch):
    tok = _crear(tmp_path)
    llamados = {}

    def fake_generar(token, nodos, dest_dir, api_key=None, tts=None, progress=None):
        llamados["token"] = token
        llamados["dest_dir"] = dest_dir
        llamados["api_key"] = api_key
        llamados["n_nodos"] = len(nodos)
        return []

    monkeypatch.setattr(aventura_audio, "generar", fake_generar)
    avw.generar_audio(tok, api_key="clave-x")
    assert llamados["token"] == tok
    assert llamados["dest_dir"] == avw.audio_dir(tok)
    assert llamados["api_key"] == "clave-x"
    assert llamados["n_nodos"] == 28


def test_generar_audio_falla_claro_si_el_token_no_existe(tmp_path):
    avw.AV_DIR = str(tmp_path)
    try:
        avw.generar_audio("noexiste_zzz")
        assert False, "debería fallar: el token no existe"
    except ValueError:
        pass


def test_archivo_sirve_mp3_generado_y_bloquea_lo_demas(tmp_path):
    tok = _crear(tmp_path)
    reg = avw._cargar(tok)
    llamadas = []
    aventura_audio.generar(tok, {"hook": reg["nodos"]["hook"]}, avw.audio_dir(tok),
                           tts=_tts_falso(llamadas))

    r = avw.archivo(tok, "hook.mp3")
    assert r is not None
    assert r[1] == "audio/mpeg"

    # nodo real de la aventura pero sin audio generado todavía -> 404, no error
    assert avw.archivo(tok, "camino.mp3") is None
    # nombre que no es un nodo real -> bloqueado por el whitelist
    assert avw.archivo(tok, "hack.mp3") is None
    assert avw.archivo(tok, "../hook.mp3") is None
