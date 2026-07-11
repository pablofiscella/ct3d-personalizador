"""Guardián del prototipo "Elegí tu aventura" (aventura_web): arma el token con el grafo
personalizado, sirve el visor y las escenas (reusadas del libro de cuento), y el
whitelist bloquea lo demás."""
import json
import os

import aventura
import aventura_web as avw


def _crear(tmp_path, nombre="Sofía", genero=None):
    avw.AV_DIR = str(tmp_path)          # aislar del disco real
    data = {"nombre": nombre, "tema": "safari"}
    if genero:
        data["genero"] = genero
    return avw.crear(data)


def test_crear_arma_token_con_manifest(tmp_path):
    tok = _crear(tmp_path)
    d = os.path.join(str(tmp_path), tok)
    assert os.path.isfile(os.path.join(d, "manifest.json"))
    with open(os.path.join(d, "manifest.json"), encoding="utf-8") as f:
        m = json.load(f)
    assert m["tema"] == "safari"
    assert m["inicio"] == "inicio"
    assert "Sofía" in m["nodos"]["inicio"]["texto"]
    assert avw.estado(tok) == "listo"
    assert avw.estado("noexiste_zzz") is None


def test_grafo_llega_siempre_a_un_final(tmp_path):
    """Recorre TODOS los caminos posibles desde el inicio: ninguno debe quedar colgado
    (nodo sin 'final' y sin 'opciones') y todos deben terminar en un nodo final."""
    tok = _crear(tmp_path, "Tomás")
    d = os.path.join(str(tmp_path), tok)
    with open(os.path.join(d, "manifest.json"), encoding="utf-8") as f:
        nodos = json.load(f)["nodos"]

    def visitar(nid, vistos):
        assert nid not in vistos, f"ciclo detectado en {nid}"
        nodo = nodos[nid]
        if nodo.get("final"):
            assert not nodo.get("opciones")
            return
        assert nodo.get("opciones"), f"nodo {nid} no es final y no tiene opciones"
        for op in nodo["opciones"]:
            assert op["next"] in nodos, f"{nid} apunta a un nodo inexistente: {op['next']}"
            visitar(op["next"], vistos | {nid})

    visitar("inicio", set())


def test_html_inyecta_json_valido_y_titulo(tmp_path):
    tok = _crear(tmp_path, "Tomás")
    h = avw.html(tok)
    assert h is not None
    assert "La aventura de Tomás" in h
    assert "&quot;" not in h.split("window.AVENTURA_NODOS")[1][:400]
    assert '"inicio"' in h
    assert "player.js?v=" in h


def test_archivo_whitelist(tmp_path):
    tok = _crear(tmp_path)
    for a in ("player.js", "2.png", "8.png", "manifest.json"):
        r = avw.archivo(tok, a)
        assert r is not None, f"debería servir {a}"
    assert avw.archivo(tok, "player.js")[1].startswith("text/javascript")
    assert avw.archivo(tok, "2.png")[1] == "image/png"
    for bad in ("hack.png", "../manifest.json", "9.png", "1.png", "0.png",
                "../../etc/passwd", "data.json"):
        assert avw.archivo(tok, bad) is None, f"NO debería servir {bad}"


def test_genero_usa_variante_nena_si_existe(tmp_path):
    tok = _crear(tmp_path, "Valentina", genero="nena")
    d = os.path.join(str(tmp_path), tok)
    with open(os.path.join(d, "manifest.json"), encoding="utf-8") as f:
        nodos = json.load(f)["nodos"]
    # 6.png tiene variante _nena para safari (ver temas/safari/overrides/libro/)
    assert nodos["montana2"]["imagen"] == "6_nena.png"
    assert avw.archivo(tok, "6_nena.png") is not None


def test_tema_sin_aventura_armada_falla_claro(tmp_path):
    avw.AV_DIR = str(tmp_path)
    try:
        avw.crear({"nombre": "X", "tema": "circo"})
        assert False, "debería fallar: circo no tiene aventura en aventura.AVENTURAS"
    except ValueError:
        pass


def test_temas_disponibles():
    assert aventura.temas_disponibles() == ["safari"]
