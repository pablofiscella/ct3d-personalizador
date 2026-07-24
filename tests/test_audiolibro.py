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


def test_instrucciones_openai_son_por_genero_de_voz():
    """15-jul-2026, pedido de Pablo sobre onyx ("voz masculina profunda"): "hace
    lo mismo con las voces de los hombres, mas entonacion y emocion". Antes,
    _INSTRUCCIONES era un único texto fijo que decía "female storyteller" para
    TODAS las voces, onyx incluida — bug real, no solo falta de emoción."""
    import audiolibro as al
    masc = al._instrucciones("onyx", "Texto neutro.")
    fem = al._instrucciones("nova", "Texto neutro.")
    assert "male storyteller" in masc
    assert "female storyteller" not in masc
    assert "female storyteller" in fem


def test_historia_desde_titulo_reconstruye_la_key(tmp_path, monkeypatch):
    """muestra_voz necesita re-narrar el texto EXACTO de un demo viejo que
    nunca guardó `historia` en su manifest — solo se puede reconstruir
    revirtiendo el armado de _titulo_libro contra TITULOS."""
    al = _fresh_audiolibro(tmp_path, monkeypatch)
    assert al._historia_desde_titulo(
        "La noche de las estrellas — el cuento de Alex", "Alex") == "noche-estrellas"
    assert al._historia_desde_titulo(
        "El mapa del tesoro — el cuento de Sofía", "Sofía") == "tesoro"
    # título del fallback genérico (libro de kit legado, sin historia) → None
    assert al._historia_desde_titulo("La gran aventura de Alex", "Alex") is None
    # nombre que no coincide con el del título → no matchea el sufijo → None
    assert al._historia_desde_titulo(
        "La noche de las estrellas — el cuento de Alex", "Otro") is None


def test_muestra_voz_bug_real_texto_no_coincidia_con_la_pagina(tmp_path, monkeypatch):
    """24-jul-2026, bug reportado: al elegir una voz distinta de Lizy en la
    ficha, la previa narraba un texto de referencia genérico grabado una
    sola vez ("Che, vení que te cuento un secreto...") en vez del texto REAL
    de la página 2 que se ve en pantalla — con ~25 libros de catálogo, cada
    uno con su propia historia, nunca podía coincidir. muestra_voz() tiene
    que narrar el mismo texto que pag_02, solo que en otra voz."""
    al = _fresh_audiolibro(tmp_path, monkeypatch)
    tok = "TokenPreviewNoche01"
    _escribir_manifest(al, tok, tema="safari", nombre="Alex",
                        titulo="La noche de las estrellas — el cuento de Alex")
    textos_esperados = al._textos_narracion(
        {"nombre": "Alex", "historia": "noche-estrellas"}, "safari")

    llamadas = []
    monkeypatch.setattr(al, "tts_mp3", lambda api_key, texto, voz=None, seed=None:
                         llamadas.append((texto, voz)) or b"FAKE" * 100)

    mp3 = al.muestra_voz(tok, "malena")
    assert mp3 == b"FAKE" * 100
    assert llamadas == [(textos_esperados[2], "malena")]   # el texto de pag_02, no uno genérico


def test_muestra_voz_cachea_en_disco_no_regenera(tmp_path, monkeypatch):
    al = _fresh_audiolibro(tmp_path, monkeypatch)
    tok = "TokenCacheVoz0001"
    _escribir_manifest(al, tok, titulo="El cuento")   # sin historia reconstruible: cae al default del tema, no importa acá

    llamadas = []
    monkeypatch.setattr(al, "tts_mp3", lambda api_key, texto, voz=None, seed=None:
                         llamadas.append(voz) or b"FAKE")

    b1 = al.muestra_voz(tok, "malena")
    b2 = al.muestra_voz(tok, "malena")
    assert b1 == b2 == b"FAKE"
    assert llamadas == ["malena"]   # la 2da vez sirve del cache, no vuelve a llamar TTS
    assert os.path.isfile(os.path.join(al.AUDIOLIBROS_DIR, tok, "muestra_malena.mp3"))


def test_muestra_voz_si_pide_la_voz_del_manifest_sirve_el_real_sin_tts(tmp_path, monkeypatch):
    al = _fresh_audiolibro(tmp_path, monkeypatch)
    tok = "TokenVozRealSirve1"
    _escribir_manifest(al, tok, voz="malena")
    d = os.path.join(al.AUDIOLIBROS_DIR, tok)
    with open(os.path.join(d, "pag_02.mp3"), "wb") as f:
        f.write(b"AUDIO REAL DE LA PAGINA 2")

    llamado = []
    monkeypatch.setattr(al, "tts_mp3", lambda *a, **k: llamado.append(1) or b"NO DEBERIA USARSE")

    assert al.muestra_voz(tok, "malena") == b"AUDIO REAL DE LA PAGINA 2"
    assert not llamado


def test_muestra_voz_voz_invalida_o_token_inexistente(tmp_path, monkeypatch):
    al = _fresh_audiolibro(tmp_path, monkeypatch)
    tok = "TokenVozInvalida01"
    _escribir_manifest(al, tok)
    assert al.muestra_voz(tok, "no-existe") is None
    assert al.muestra_voz("token-no-existe-123", "malena") is None


def test_archivo_rutea_muestra_voz(tmp_path, monkeypatch):
    """El endpoint real (servicio.py /al/<token>/<arch>) llama a archivo() con
    lo que venga después del token — tiene que reconocer 'muestra_<voz>.mp3'
    y no solo 'pag_NN.(jpg|mp3)'."""
    al = _fresh_audiolibro(tmp_path, monkeypatch)
    tok = "TokenArchivoRuteo1"
    _escribir_manifest(al, tok)
    monkeypatch.setattr(al, "tts_mp3", lambda api_key, texto, voz=None, seed=None: b"X" * 50)

    r = al.archivo(tok, "muestra_dante.mp3")
    assert r == (b"X" * 50, "audio/mpeg")
    assert al.archivo(tok, "muestra_no-existe.mp3") is None
    assert al.archivo(tok, "otracosa.mp3") is None


def test_instrucciones_openai_varian_ritmo_segun_contenido():
    """15-jul-2026, 2ª vuelta: Pablo sobre la muestra ya corregida por género:
    "le falta emocion, esta lento y sin cambio de ritmo". La 1ª vuelta no
    tocó Pacing (seguía diciendo "slow, 120-130 wpm" SIEMPRE) ni variaba nada
    entre llamadas — a diferencia de ElevenLabs (etiqueta v3 por NODO), cada
    llamada a _tts_openai mandaba las mismas instructions fijas sin importar
    el contenido de ESE texto puntual."""
    import audiolibro as al
    excitado = al._instrucciones("onyx", "¡Qué sorpresa! ¡Vamos ya!")
    dormir = al._instrucciones("onyx", "Y así, {nombre} se durmió tranquilo.")
    neutro = al._instrucciones("onyx", "Caminó despacio por el sendero.")
    assert "Pick up the pace" in excitado
    assert "Slow way down" in dormir
    assert "150 to 170 words per minute" in neutro
    # el caso base ya NO es el ritmo lento de bedtime fijo de antes
    assert "120 to 130 words per minute" not in neutro
    assert "Slow and unhurried" not in neutro
