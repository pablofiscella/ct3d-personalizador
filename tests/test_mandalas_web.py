"""Guardián de la modalidad WEB del kit de mándalas (mandalas_web): crea el token con el
PDF adentro, sirve el visor y los assets desde el repo, y el whitelist bloquea lo demás."""
import json
import os
import zipfile

import mandalas_web as mw


def _crear(tmp_path, nombre="Sofía"):
    mw.MW_DIR = str(tmp_path)          # aislar del disco real
    return mw.crear({"nombre": nombre, "tema": "safari"})


def test_crear_arma_token_con_pdf_y_manifest(tmp_path):
    tok = _crear(tmp_path)
    d = os.path.join(str(tmp_path), tok)
    assert os.path.isfile(os.path.join(d, "kit.zip"))
    assert os.path.isfile(os.path.join(d, "manifest.json"))
    # el kit.zip trae las 8 páginas del PDF
    assert len(zipfile.ZipFile(os.path.join(d, "kit.zip")).namelist()) == mw.NIVELES + 2
    assert mw.estado(tok) == "listo"
    assert mw.estado("noexiste_zzz") is None


def test_html_inyecta_js_valido_y_boton_pdf(tmp_path):
    tok = _crear(tmp_path, "Tomás")
    h = mw.html(tok)
    assert h is not None
    # NIVELES se inyecta como JSON CRUDO (no HTML-escapeado) → JS válido
    assert '"src": "mandala_1.png"' in h
    assert "&quot;" not in h.split("window.MANDALAS")[1][:400]
    assert "Tomás" in h                       # título personalizado
    assert 'href="kit.zip"' in h              # botón de descarga del PDF
    assert "player.js?v=" in h


def test_archivo_whitelist(tmp_path):
    tok = _crear(tmp_path)
    ok = {}
    for a in ("player.js", "mandala_1.png", "mandala_6.png", "kit.zip", "portada.jpg"):
        r = mw.archivo(tok, a)
        assert r is not None, f"debería servir {a}"
        ok[a] = r[1]
    assert ok["player.js"].startswith("text/javascript")
    assert ok["kit.zip"] == "application/zip"
    assert ok["mandala_1.png"] == "image/png"
    # bloqueados: fuera del whitelist, traversal, niveles inexistentes
    for bad in ("hack.png", "../manifest.json", "mandala_9.png", "../../etc/passwd", "data.json"):
        assert mw.archivo(tok, bad) is None, f"NO debería servir {bad}"


def test_mandalas_salen_del_repo_no_del_token(tmp_path):
    """Las 6 mándalas se sirven del repo (mandalas_arte/), no se copian al token."""
    tok = _crear(tmp_path)
    d = os.path.join(str(tmp_path), tok)
    assert not os.path.isfile(os.path.join(d, "mandala_1.png"))  # NO está en el token
    assert mw.archivo(tok, "mandala_1.png") is not None          # pero se sirve igual
