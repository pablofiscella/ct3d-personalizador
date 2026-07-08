"""Historia propia POR TEMA (regla de Pablo, 8-jul-2026): cada tema que estrena
libro se casa con un argumento NUEVO de la reserva, sin repetir entre temas.
Los 11 libros ya generados usan el clásico; el 12º tema usa la historia 12."""
import json
import os

import pytest

import libro
import libro_ia


def _crear_tema(base, nombre, **extra):
    d = os.path.join(base, nombre)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "tema.json"), "w", encoding="utf-8") as f:
        json.dump({"nombre": nombre, **extra}, f)
    return d


@pytest.fixture
def temas_tmp(tmp_path, monkeypatch):
    base = str(tmp_path / "temas")
    os.makedirs(base)
    monkeypatch.setattr(libro, "TEMAS", base)
    monkeypatch.setattr(libro_ia, "TEMAS", base)
    return base


def test_asignacion_en_orden_y_sin_repetir(temas_tmp):
    _crear_tema(temas_tmp, "tema-a")
    _crear_tema(temas_tmp, "tema-b")
    a = libro.asignar_historia_tema("tema-a")
    b = libro.asignar_historia_tema("tema-b")
    assert a[0] == "tesoro" and a[2] == 12          # el 12º libro, como pidió Pablo
    assert b[0] == "rescate" and b[2] == 13
    assert a[0] != b[0]
    # persistida en tema.json
    d = json.load(open(os.path.join(temas_tmp, "tema-a", "tema.json")))
    assert d["libro_historia"] == "tesoro"


def test_asignacion_idempotente(temas_tmp):
    _crear_tema(temas_tmp, "tema-a")
    primera = libro.asignar_historia_tema("tema-a")
    segunda = libro.asignar_historia_tema("tema-a")
    assert primera == segunda


def test_reserva_agotada_devuelve_none(temas_tmp):
    for i, h in enumerate(libro.ORDEN_HISTORIAS_NUEVAS):
        _crear_tema(temas_tmp, "tema-%d" % i, libro_historia=h)
    _crear_tema(temas_tmp, "tema-extra")
    assert libro.proxima_historia_libre() is None
    assert libro.asignar_historia_tema("tema-extra") is None


def test_cuento_usa_la_historia_del_tema(temas_tmp):
    # tema formato nuevo (12 páginas) con historia asignada: el texto sale del
    # arco de esa historia, no del clásico de la invitación mágica
    _crear_tema(temas_tmp, "tema-a", libro_historia="tesoro")
    textos = libro.cuento({"nombre": "Simón", "edad": "5"}, "tema-a")
    assert len(textos) == libro.PAGINAS_HISTORIA_NUEVO
    assert "mapa" in textos[0].lower()              # arranque de "El mapa del tesoro"
    assert any("Simón" in t for t in textos)
    assert "invitación brillante" not in textos[0]  # no es el clásico


def test_cuento_sin_asignacion_sigue_siendo_el_clasico(temas_tmp):
    _crear_tema(temas_tmp, "tema-b", libro_paginas_historia=7)
    textos = libro.cuento({"nombre": "Emma", "edad": "4"}, "tema-b")
    assert "invitación brillante" in textos[0]


def test_prompt_pagina_ilustra_la_historia_del_tema(temas_tmp):
    # las ilustraciones siguen la MISMA historia que el texto (sin pasar historia=)
    _crear_tema(temas_tmp, "tema-a", libro_historia="tesoro")
    p = libro_ia.prompt_pagina("tema-a", 2)
    assert "mapa antiguo" in p                      # escena 2 de "tesoro"
    assert "sobre dorado" not in p                  # no la escena clásica
