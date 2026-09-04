"""El panel de la MAESTRA: desglose tarjeta por tarjeta, y el orden que ella arma.

Pablo, 04-sep-2026: *"Me gustarían dos cosas: una es el desglose de qué es lo que hizo en
cada tarjeta. Me gustaría que la profe pueda ordenar las tarjetas como creo que las tiene
que ver el alumno."*

Lo que se verifica acá y no es adorno:

1. **«No la abrió» y «practicando» no son lo mismo.** Es la distinción entera de la
   pantalla: una pide volver a explicar, la otra pide dar la hoja. Si el desglose las
   confunde, la maestra lee mal a su curso.
2. **El orden se sanea contra el menú REAL del token.** El panel ordena una lista para
   todo el curso y cada cuaderno tiene el menú de SU grado: un id que en ese token no
   existe tiene que caerse acá y no llegar al player.
3. **Un orden parcial no esconde el resto del cuaderno.** Si la seño ordenó Matemática y
   nada más, el chico tiene que seguir viendo Lengua.
4. **El player conserva el camino sin orden.** Es lo que hace que esto se pueda soltar a
   links ya vendidos: sin `orden_seno` el menú sale exactamente como salía.
"""
import json
import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import actividades_web as aw  # noqa: E402
import desglose as dg  # noqa: E402

TEMA = "safari"
_TOK = "test-seno-desglose"


@pytest.fixture(scope="module")
def token():
    d = os.path.join(aw.ACT_DIR, _TOK)
    shutil.rmtree(d, ignore_errors=True)
    # 4.º grado: el que tiene fracciones, que es el ejemplo con el que Pablo preguntó si
    # el sistema distingue un tema de otro.
    aw.crear({"nombre": "Sofía", "edad": "9", "escolar_on": True}, TEMA, token=_TOK)
    yield _TOK
    shutil.rmtree(d, ignore_errors=True)


def _escribir_progreso(token, perfil, **kw):
    """Deja un progreso.json como el que manda el player, para un solo perfil."""
    p = os.path.join(aw.ACT_DIR, token, "progreso.json")
    json.dump({"profiles": {perfil: kw}}, open(p, "w", encoding="utf-8"),
              ensure_ascii=False)


# ── 1. el desglose ────────────────────────────────────────────────────────────

def test_desglose_trae_una_tarjeta_por_actividad_del_menu(token):
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    r = dg.desglose(token)
    assert r is not None
    tarjetas = list(r["perfiles"].values())[0]["tarjetas"]
    assert len(tarjetas) == len(d["menu"])
    assert {t["id"] for t in tarjetas} == {m["id"] for m in d["menu"]}


def test_token_inexistente_da_none_no_explota():
    assert dg.desglose("no-existe-este-token") is None


def test_cuaderno_sin_jugar_dice_no_la_abrio_en_todas(token):
    """El cuaderno recién entregado: la maestra tiene que poder verlo ANTES de que el
    chico lo abra — es la mitad de lo que se muestra al ofrecerlo en persona."""
    shutil.rmtree(os.path.join(aw.ACT_DIR, token, "progreso.json"), ignore_errors=True)
    try:
        os.remove(os.path.join(aw.ACT_DIR, token, "progreso.json"))
    except OSError:
        pass
    r = dg.desglose(token)
    tarjetas = list(r["perfiles"].values())[0]["tarjetas"]
    assert tarjetas, "un cuaderno sin progreso igual tiene que listar sus tarjetas"
    assert all(t["sello"] == "sin_datos" for t in tarjetas)
    assert all(not t["abrio"] for t in tarjetas)
    assert list(r["perfiles"].values())[0]["hechas"] == 0


def test_no_la_abrio_y_practicando_no_se_confunden(token):
    """LA distinción de la pantalla. `sopa` se jugó y no se domina; el resto ni se tocó."""
    _escribir_progreso(token, "Sofía",
                       niveles={"sopa": 2},
                       dominados=[],
                       estado={"stars": {"sopa": 1},
                               "dominio": {"sopa": {"dias": ["2026-09-01"],
                                                    "sello": "practicando",
                                                    "repasarEn": 0}}})
    tarjetas = {t["id"]: t for t in dg.desglose(token)["perfiles"]["Sofía"]["tarjetas"]}
    sopa = tarjetas["sopa"]
    assert sopa["sello"] == "practicando" and sopa["abrio"]
    assert sopa["estrellas"] == 1 and sopa["escalon"] == 2 and sopa["veces"] == 1
    assert sopa["dias"] == ["2026-09-01"]

    otras = [t for i, t in tarjetas.items() if i != "sopa"]
    assert all(t["sello"] == "sin_datos" for t in otras)
    assert all(t["sello_txt"] == "No la abrió" for t in otras)


def test_dominado_cuenta_como_dominada_y_practicando_no(token):
    _escribir_progreso(token, "Sofía",
                       niveles={"sopa": 3, "memotest": 1},
                       dominados=["LEN-4-VOCAB"],
                       estado={"stars": {"sopa": 3, "memotest": 1},
                               "dominio": {
                                   "sopa": {"dias": ["2026-09-01", "2026-09-02"],
                                            "sello": "dominado", "repasarEn": 0},
                                   "memotest": {"dias": ["2026-09-01"],
                                                "sello": "practicando", "repasarEn": 0}}})
    p = dg.desglose(token)["perfiles"]["Sofía"]
    assert p["hechas"] == 2
    assert p["dominadas"] == 1, "practicando NO es dominada"


def test_la_tarjeta_dice_que_saber_mide_con_nombre_legible(token):
    """Sin esto la maestra ve «MAT-4-FRAC-EQUIV» y no «Fracciones equivalentes»."""
    tarjetas = {t["id"]: t for t in dg.desglose(token)["perfiles"]["Sofía"]["tarjetas"]}
    con_saber = [t for t in tarjetas.values() if t["mide"]]
    assert con_saber, "en 4.º grado tiene que haber tarjetas con saber asociado"
    for t in con_saber:
        for m in t["mide"]:
            assert m["nombre"] and m["nombre"] != m["id"], m
            assert m["grado"] <= 4, "no se le nombra a la maestra un saber de más arriba"


def test_un_saber_dominado_se_marca_en_la_tarjeta(token):
    """El cruce que contesta «fracciones mal, sumas bien»: el saber viaja con su sello."""
    import saberes
    sid = "MAT-4-SUMA"
    juego = saberes.SABERES[sid]["juegos"][0]
    _escribir_progreso(token, "Sofía", niveles={}, dominados=[sid], estado={})
    tarjetas = {t["id"]: t for t in dg.desglose(token)["perfiles"]["Sofía"]["tarjetas"]}
    if juego not in tarjetas:
        pytest.skip("ese juego no está en el menú de este token")
    mide = {m["id"]: m for m in tarjetas[juego]["mide"]}
    assert mide[sid]["dominado"] is True


def test_perfil_acota_a_un_solo_chico(token):
    """Un cuaderno puede tener hermanos; para la maestra son filas distintas."""
    p = os.path.join(aw.ACT_DIR, token, "progreso.json")
    json.dump({"profiles": {"Sofía": {"niveles": {}}, "Beni": {"niveles": {}}}},
              open(p, "w", encoding="utf-8"), ensure_ascii=False)
    assert set(dg.desglose(token)["perfiles"]) == {"Sofía", "Beni"}
    assert set(dg.desglose(token, "Beni")["perfiles"]) == {"Beni"}


# ── 2. el orden que arma la maestra ───────────────────────────────────────────

def test_el_orden_se_sanea_contra_el_menu_del_token(token):
    """El panel ordena UNA lista para todo el curso, pero cada token tiene el menú de su
    grado: lo que en este cuaderno no existe se cae acá y no llega al player."""
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    reales = [m["id"] for m in d["menu"]][:3]
    r = aw.orden_seno_guardar(token, reales + ["actividad-que-no-existe", reales[0]])
    assert r["ok"]
    assert r["ids"] == reales, "descarta lo inexistente y no duplica"
    assert aw.orden_seno_leer(token) == reales


def test_orden_parcial_no_esconde_el_resto_del_cuaderno(token):
    """La seño ordenó tres tarjetas: las otras siguen estando en el menú del chico."""
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    assert len(d["menu"]) > 3, "el menú de 4.º tiene que tener más de tres tarjetas"
    aw.orden_seno_guardar(token, [m["id"] for m in d["menu"]][:3])
    d2 = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    assert len(d2["menu"]) == len(d["menu"]), "guardar el orden no toca el menú"
    assert len(d2["orden_seno"]) == 3


def test_lista_vacia_deshace_el_orden(token):
    """Vacío es «la maestra deshizo lo que había», no «no me mandaron nada»."""
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    aw.orden_seno_guardar(token, [m["id"] for m in d["menu"]][:2])
    assert aw.orden_seno_leer(token)
    aw.orden_seno_guardar(token, [])
    assert aw.orden_seno_leer(token) == []


def test_token_sin_orden_devuelve_lista_vacia_no_error(token):
    tok = _TOK + "-limpio"
    d = os.path.join(aw.ACT_DIR, tok)
    shutil.rmtree(d, ignore_errors=True)
    aw.crear({"nombre": "Beni", "edad": "9", "escolar_on": True}, TEMA, token=tok)
    try:
        assert aw.orden_seno_leer(tok) == []
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_guardar_en_token_inexistente_no_explota():
    r = aw.orden_seno_guardar("no-existe-este-token", ["sopa"])
    assert r["ok"] is False


def test_el_orden_sobrevive_a_regenerar_el_token(token):
    """El trabajo de la docente no es un dato del padrón: re-armar el cuaderno no lo borra.

    Es el mismo patrón que `adaptativo_on` y `nivel_max`, y existe porque ya se perdió
    configuración por regenerar un token."""
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    quiere = [m["id"] for m in d["menu"]][:4]
    aw.orden_seno_guardar(token, quiere)
    aw.crear({"nombre": "Sofía", "edad": "9", "escolar_on": True}, TEMA, token=token)
    assert aw.orden_seno_leer(token) == quiere


# ── 3. el player ──────────────────────────────────────────────────────────────

def test_el_player_conserva_el_orden_de_siempre_sin_orden_seno():
    """GUARDIÁN. `actividades_player.js` se sirve DEL REPO: lo que se toque acá llega a
    todos los cuadernos ya vendidos. El camino sin `orden_seno` tiene que seguir siendo
    el de antes, byte por byte de comportamiento — por eso el comparador viejo sigue
    escrito como fallback y este test se rompe si alguien lo borra."""
    js = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "actividades_player.js"), encoding="utf-8").read()
    assert "Adapt.peso(a.id) - Adapt.peso(b.id)" in js, \
        "se borró el orden de siempre: los cuadernos ya entregados cambiarían solos"
    assert "D.orden_seno" in js
