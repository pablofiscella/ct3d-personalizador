"""Guardián del prototipo "Elegí tu aventura" (aventura_web): arma el token con el grafo
personalizado, sirve el visor y las escenas (arte propio por nodo), y el whitelist
bloquea lo demás."""
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
    assert m["inicio"] == "hook"
    assert "Sofía" in m["nodos"]["hook"]["texto"]
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

    visitar("hook", set())


def test_todo_camino_dura_unas_20_postas(tmp_path):
    """Pedido de Pablo: cualquier camino elegido tiene que durar lo mismo que un
    libro/audiolibro de 20 páginas. Recorre cada rama real (tomando SIEMPRE la opción
    0 o SIEMPRE la 1 en cada decisión) y verifica que cada camino completo totaliza
    ~20 nodos, no menos."""
    tok = _crear(tmp_path, "Mila")
    d = os.path.join(str(tmp_path), tok)
    with open(os.path.join(d, "manifest.json"), encoding="utf-8") as f:
        nodos = json.load(f)["nodos"]

    def recorrer(nid, pick, pasos):
        pasos.append(nid)
        nodo = nodos[nid]
        if nodo.get("final"):
            return pasos
        opts = nodo["opciones"]
        siguiente = opts[pick if len(opts) > 1 else 0]["next"]
        return recorrer(siguiente, pick, pasos)

    for pick in (0, 1):
        camino = recorrer("hook", pick, [])
        assert 18 <= len(camino) <= 22, f"camino {pick} mide {len(camino)}: {camino}"


def test_html_inyecta_json_valido_y_titulo(tmp_path):
    tok = _crear(tmp_path, "Tomás")
    h = avw.html(tok)
    assert h is not None
    assert "La aventura de Tomás" in h
    assert "&quot;" not in h.split("window.AVENTURA_NODOS")[1][:400]
    assert '"hook"' in h
    assert "player.js?v=" in h
    # cache-buster por escena: sin esto el navegador seguía mostrando arte viejo
    # después de regenerarlo (pasó real con el fix de vestimenta)
    assert '"imagen": "hook.png?v=' in h
    assert '"imagen": "amigos_final.png?v=' in h


def test_archivo_whitelist(tmp_path):
    tok = _crear(tmp_path)
    # safari ya tiene arte PROPIO generado (aventura_ia.py) para los 28 nodos, así que
    # el manifest apunta directo a <nodo_id>.png (no al placeholder reciclado).
    for a in ("player.js", "manifest.json", "hook.png", "amigos_final.png"):
        r = avw.archivo(tok, a)
        assert r is not None, f"debería servir {a}"
    assert avw.archivo(tok, "player.js")[1].startswith("text/javascript")
    assert avw.archivo(tok, "hook.png")[1] == "image/png"
    for bad in ("hack.png", "../manifest.json", "2.png", "9.png", "libro-99.png",
                "circo.png", "../../etc/passwd", "data.json"):
        assert avw.archivo(tok, bad) is None, f"NO debería servir {bad}"


def test_arte_propio_tiene_prioridad_sobre_placeholder(tmp_path):
    """aventura._imagen_archivo: sin arte propio en overrides/aventura/ cae al
    placeholder reciclado del libro; en cuanto aventura_ia.py genera el archivo del
    nodo, ese pasa a usarse (aislado del disco real con un TEMAS_DIR de prueba)."""
    temas_dir = tmp_path / "temas"
    os.makedirs(temas_dir / "safari" / "overrides" / "aventura")
    original = aventura._temas.TEMAS_DIR
    aventura._temas.TEMAS_DIR = str(temas_dir)
    try:
        assert aventura._imagen_archivo("safari", "hook") == "libro-2.png"
        (temas_dir / "safari" / "overrides" / "aventura" / "hook.png").write_bytes(b"x")
        assert aventura._imagen_archivo("safari", "hook") == "hook.png"
    finally:
        aventura._temas.TEMAS_DIR = original


def test_tema_sin_aventura_armada_falla_claro(tmp_path):
    avw.AV_DIR = str(tmp_path)
    try:
        avw.crear({"nombre": "X", "tema": "circo"})
        assert False, "debería fallar: circo no tiene aventura en aventura.AVENTURAS"
    except ValueError:
        pass


def test_temas_disponibles():
    assert aventura.temas_disponibles() == ["safari"]
