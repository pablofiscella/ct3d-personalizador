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
