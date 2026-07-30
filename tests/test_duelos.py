"""Duelos: dos chicos, las mismas 5 preguntas, por turnos.

Lo que más se cuida acá no es que funcione, es lo que NO tiene que pasar: que no haya
ningún campo de texto libre (la regla de Pablo: sin chat), que el código no exponga un
cuaderno, y que nadie pueda jugar dos veces la misma partida para ganarse a sí mismo.
"""
import json
import os
import sys

import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
import duelos  # noqa: E402


def _preguntas(n=5):
    return [{"q": "¿Cuánto es %d × 3?" % i, "ops": [str(i * 3), str(i * 3 + 1), "99"],
             "ok": 0, "cat": "matematica"} for i in range(1, n + 1)]


@pytest.fixture(autouse=True)
def dir_temporal(tmp_path, monkeypatch):
    """Cada test con su propio directorio: si escribieran en el del repo, un test dejaría
    partidas de mentira en producción."""
    monkeypatch.setattr(duelos, "DUELOS_DIR", str(tmp_path / "duelos"))


# ───────────────────────────────────────────────────────────── el circuito

def test_crear_y_leer():
    cod, d = duelos.crear(4, _preguntas(), "Sofi", 4)
    assert cod and duelos.CODIGO_RE.match(cod)
    assert d["grado"] == 4 and len(d["preguntas"]) == 5
    assert d["jugadores"][0] == {"nombre": "Sofi", "aciertos": 4, "t": d["jugadores"][0]["t"]}
    assert duelos.leer(cod)["codigo"] == cod


def test_el_segundo_juega_las_MISMAS_preguntas():
    """Es el punto del duelo: si a cada uno le tocaran preguntas distintas, comparar los
    aciertos no significaría nada."""
    cod, d1 = duelos.crear(4, _preguntas(), "Sofi", 5)
    d2 = duelos.leer(cod)
    assert [p["q"] for p in d2["preguntas"]] == [p["q"] for p in d1["preguntas"]]
    d3, err = duelos.sumar_jugador(cod, "Juan", 3)
    assert err is None and len(d3["jugadores"]) == 2
    assert [j["nombre"] for j in d3["jugadores"]] == ["Sofi", "Juan"]


def test_no_entra_un_tercero():
    """Es un duelo, no una liga."""
    cod, _ = duelos.crear(4, _preguntas(), "Sofi", 5)
    duelos.sumar_jugador(cod, "Juan", 3)
    d, err = duelos.sumar_jugador(cod, "Pedro", 5)
    assert d is None and "completa" in err


def test_el_mismo_nombre_no_juega_dos_veces():
    """Sin esto, el que crea la partida se responde a sí mismo hasta ganar."""
    cod, _ = duelos.crear(4, _preguntas(), "Sofi", 2)
    d, err = duelos.sumar_jugador(cod, "sofi", 5)      # distinta capitalización
    assert d is None and "ya jugó" in err


# ─────────────────────────────────────────── nada de esto puede entrar (sin chat)

def test_no_se_guarda_ningun_texto_libre():
    """La regla de Pablo: sin chat. El único campo con letras de una persona es el nombre
    del perfil. Si alguien manda campos extra, no tienen que quedar guardados."""
    cod, d = duelos.crear(4, [dict(p, mensaje="hola vivís cerca?", chat="dale",
                                   telefono="1155551234") for p in _preguntas()],
                          "Sofi", 5)
    crudo = json.dumps(duelos.leer(cod), ensure_ascii=False)
    for prohibido in ("mensaje", "chat", "telefono", "vivís cerca", "1155551234"):
        assert prohibido not in crudo, "quedó guardado %r: eso es un canal de texto" % prohibido
    assert set(d["preguntas"][0]) == {"q", "ops", "ok", "cat"}


def test_el_nombre_se_limpia_y_se_acota():
    cod, d = duelos.crear(4, _preguntas(), "<b>Sofi</b> http://malo.com " + "x" * 60, 5)
    n = d["jugadores"][0]["nombre"]
    assert len(n) <= 20
    for c in "<>/:":
        assert c not in n


def test_sin_nombre_no_queda_vacio():
    _, d = duelos.crear(4, _preguntas(), "   ", 5)
    assert d["jugadores"][0]["nombre"] == "Alguien"


# ───────────────────────────────────────────────── el código no es un cuaderno

def test_el_codigo_no_expone_ningun_token():
    """Lo más importante de seguridad: el link lleva el id de la PARTIDA. Si llevara el
    token del cuaderno, compartirlo sería repartir la puerta del cuaderno de un chico."""
    cod, d = duelos.crear(4, _preguntas(), "Sofi", 5)
    crudo = json.dumps(d)
    assert "token" not in crudo
    # y el código es sólo del alfabeto sin ambigüedades: ni vocales ni 0/O/1/I/L
    assert not set(cod) & set("AEIOU01ILO")


def test_un_codigo_inventado_no_devuelve_nada():
    assert duelos.leer("XXXXX") is None
    assert duelos.leer("") is None
    assert duelos.leer("../../etc/passwd") is None
    assert duelos.leer("AEIOU") is None          # fuera del alfabeto


def test_sumar_a_un_codigo_inventado_no_crea_nada():
    d, err = duelos.sumar_jugador("QQQQQ", "Juan", 5)
    assert d is None and err == "no existe"
    assert not os.path.exists(os.path.join(duelos.DUELOS_DIR, "QQQQQ.json"))


# ──────────────────────────────────────────────────────── validaciones

@pytest.mark.parametrize("grado", [0, 8, -1, "cuarto", None])
def test_grado_invalido(grado):
    cod, motivo = duelos.crear(grado, _preguntas(), "Sofi", 5)
    assert cod is None and "grado" in motivo


def test_tienen_que_ser_exactamente_cinco():
    assert duelos.crear(4, _preguntas(3), "Sofi", 3)[0] is None
    assert duelos.crear(4, _preguntas(6), "Sofi", 6)[0] is None


def test_una_pregunta_sin_respuesta_valida_se_descarta():
    """`ok` fuera de rango haría que ninguna opción sea correcta y el chico no pueda ganar."""
    malas = _preguntas(5)
    malas[0]["ok"] = 9
    assert duelos.crear(4, malas, "Sofi", 5)[0] is None


def test_los_aciertos_no_pueden_exceder_las_preguntas():
    _, d = duelos.crear(4, _preguntas(), "Sofi", 99)
    assert d["jugadores"][0]["aciertos"] == 5
    _, d2 = duelos.crear(4, _preguntas(), "Sofi", -3)
    assert d2["jugadores"][0]["aciertos"] == 0


# ──────────────────────────────────────────────────────────── limpieza

def test_las_partidas_viejas_se_borran():
    import time
    cod, _ = duelos.crear(4, _preguntas(), "Sofi", 5)
    p = os.path.join(duelos.DUELOS_DIR, cod + ".json")
    viejo = time.time() - 40 * 86400
    os.utime(p, (viejo, viejo))
    assert duelos.limpiar() == 1
    assert duelos.leer(cod) is None


def test_las_recientes_no_se_tocan():
    cod, _ = duelos.crear(4, _preguntas(), "Sofi", 5)
    assert duelos.limpiar() == 0
    assert duelos.leer(cod) is not None
