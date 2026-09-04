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
import re
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

def _player():
    return open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "actividades_player.js"), encoding="utf-8").read()


# ── el MODO SEÑO: la maestra ve el cuaderno tal cual y lo ordena ──────────────

def test_el_modo_seno_esta_gateado_por_la_url():
    """GUARDIÁN. `actividades_player.js` se sirve DEL REPO: todo lo que se agregue acá
    llega a los cuadernos ya vendidos. El modo seño no puede encenderse solo — arranca
    apagado y sólo lo prende `?seno=1`."""
    js = _player()
    assert "let SENO_ON = false;" in js, "el modo seño dejó de arrancar apagado"
    assert "function senoPedida()" in js
    assert "SENO_ON = !_muestra && senoPedida();" in js, \
        "el modo seño se enciende por otro camino que el parámetro de la URL"


def test_en_modo_seno_no_se_pide_el_nombre_ni_el_sondeo():
    """No es un chico el que entra: preguntarle «¿Quién juega?» a una maestra que viene a
    ordenar el cuaderno es un trámite que no le corresponde, y el sondeo mediría el nivel
    de nadie."""
    js = _player()
    assert "if (SENO_ON) return false;" in js, "el sondeo sigue apareciendo en modo seño"
    i = js.index("SENO_ON = !_muestra && senoPedida();")
    tramo = js[i:i + 400]
    assert "elegirPerfil(NOMBRE_INVITADO)" in tramo and "pintarMenu()" in tramo


def test_el_modo_seno_guarda_en_su_propio_origen():
    """El destino del guardado NO sale del query string: es una ruta relativa del propio
    token. Un destino que viniera de la URL convertiría el cuaderno en un trampolín para
    mandarle un POST a cualquier sitio."""
    js = _player()
    i = js.index("async function _senoGuardar")
    tramo = js[i:i + 900]
    assert 'fetch("orden"' in tramo, "el guardado dejó de ser al propio token"
    assert "http://" not in tramo and "https://" not in tramo, \
        "apareció una URL absoluta en el guardado del modo seño"


def test_arrastrar_y_probar_se_distinguen_por_el_umbral():
    """La carta es a la vez el asa y el botón que abre la actividad. Sin el umbral en
    píxeles, cualquier temblor del dedo contaba como arrastre y probar una tarjeta en el
    celular era imposible."""
    js = _player()
    assert "const UMBRAL = 8;" in js
    assert "< UMBRAL) return;" in js, "se perdió la comparación contra el umbral"
    assert "Math.hypot(" in js


def test_no_se_reordena_mientras_el_flip_anima():
    """Pablo: *"hay momentos en los que entran en una vibración"*. Una de las dos causas:
    `getBoundingClientRect()` devuelve la caja CON el transform, así que durante los 220ms
    de la animación los vecinos están a mitad de camino y el hit-test contesta sobre
    posiciones que ya no son ni las de antes ni las de después.

    Medido con un MutationObserver: 22 reordenamientos por arrastre de tres lugares."""
    js = _player()
    assert "performance.now() < arr.quietoHasta" in js, "volvería la vibración"
    assert "arr.quietoHasta = performance.now() +" in js


def test_hay_histeresis_en_el_borde_de_la_carta_vecina():
    """La otra causa de la vibración: bastaba rozar el borde para intercambiar, y después
    del intercambio el centro seguía sobre el vecino —ahora en el otro lugar—, así que
    volvía a dispararse. El centro tiene que entrar BIEN ADENTRO."""
    js = _player()
    assert "hr.width * 0.3" in js and "hr.height * 0.3" in js, \
        "se perdió el margen que evita el ida y vuelta en el límite"


def test_la_carta_se_vuelve_a_pegar_al_puntero_en_el_MISMO_frame():
    """Pablo: *"se va dos tarjetas al costado y el puntero del mouse queda en otro lado"*.
    El intercambio le cambia la base a la carta —en una grilla, cambiar de fila la corre
    177px en X— y el translate puesto es el de la base anterior. Recalcularlo recién en el
    movimiento siguiente deja UN frame con la carta corrida un ancho de tarjeta.

    Por eso `_senoPegar` se llama en DOS lugares, y los dos hacen falta."""
    js = _player()
    assert js.count("_senoPegar(arr,") >= 2, \
        "el reanclaje después del intercambio se perdió: vuelve el salto al costado"
    assert "function _senoPegar" in js
    # y NO puede volver el reanclaje por deltas acumulados, que era la causa original
    assert "arr.x0 += " not in js, "volvió el reanclaje que acumulaba el error"


def test_la_carta_arrastrada_no_se_escala():
    """El `scale(1.04)` cambiaba el tamaño de la caja y ensuciaba la medición de la
    posición, que es de lo que depende que la carta siga al dedo. El efecto de «levantada»
    lo da la sombra, que no toca la geometría."""
    js = _player()
    i = js.index("function _senoArrastre")
    # sólo el CÓDIGO: el comentario que explica por qué se sacó nombra `scale(` y daría un
    # falso positivo — lo dio, de hecho, la primera vez que se corrió este test.
    codigo = "\n".join(l for l in js[i:i + 6000].splitlines()
                       if not l.strip().startswith(("//", "*", "/*")))
    assert "scale(" not in codigo, "volvió la escala sobre la carta que se arrastra"
    assert "boxShadow" in codigo


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


# ── el BORRADOR es por CURSO, no por grado ────────────────────────────────────

def test_dos_divisiones_del_mismo_grado_no_se_pisan_el_borrador(token):
    """Pablo, cuando le conté el riesgo: *"a menos que sea A y B"*. Ése es justo el caso —
    casi toda escuela tiene dos divisiones—, y el cuaderno de MUESTRA donde la maestra
    arma el orden es UNO por grado. Sin la clave del curso, la seño de 4.º B le pisaba el
    borrador a la de 4.º A."""
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    ids = [m["id"] for m in d["menu"]]
    a, bb = ids[:3], ids[3:6]

    aw.orden_seno_guardar(token, a, curso="4A")
    aw.orden_seno_guardar(token, bb, curso="4B")

    assert aw.orden_seno_leer(token, "4A") == a, "4.º B le pisó el borrador a 4.º A"
    assert aw.orden_seno_leer(token, "4B") == bb
    assert aw.orden_seno_leer(token, "4C") == [], "una división sin borrador no hereda otro"


def test_el_borrador_NO_cambia_el_cuaderno_de_muestra_publico(token):
    """El de muestra es el cuaderno que abre cualquiera desde «probalo gratis». El orden a
    medio armar de una maestra no puede cambiárselo a todo el que entre a probar."""
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    ids = [m["id"] for m in d["menu"]][:4]
    aw.orden_seno_guardar(token, [])          # se parte de un cuaderno sin orden propio
    aw.orden_seno_guardar(token, ids, curso="4A")
    # `orden_seno` es lo que el player usa para ordenar el menú del que entra
    assert aw.orden_seno_leer(token) == [], \
        "el borrador de una maestra le cambió el cuaderno de muestra a todo el mundo"
    assert aw.orden_seno_leer(token, "4A") == ids, "y el borrador sí quedó guardado"


def test_el_curso_se_sanea_no_se_confia_en_la_url(token):
    """El código viaja en el query string del link, así que lo puede escribir cualquiera."""
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    ids = [m["id"] for m in d["menu"]][:2]
    for feo in ("../../etc", "a b", "4A/../x", "x" * 60, ""):
        r = aw.orden_seno_guardar(token, ids, curso=feo)
        # o lo rechaza como curso (y guarda el orden del chico) o lo normaliza, pero nunca
        # crea una clave con esos caracteres
        for k in (json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"),
                                 encoding="utf-8")).get("orden_seno_cursos") or {}):
            assert re.match(r"^[A-Z0-9_-]{1,40}$", k), "clave de curso sin sanear: %r" % k
        assert r["ok"]


def test_sin_curso_sigue_guardando_el_orden_del_chico(token):
    """Compatibilidad: así es como la tienda le escribe el orden al cuaderno de cada alumno."""
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    ids = [m["id"] for m in d["menu"]][:3]
    aw.orden_seno_guardar(token, ids)
    assert aw.orden_seno_leer(token) == ids


# ── la MUESTRA PÚBLICA no guarda nada ────────────────────────────────────────

def test_la_muestra_publica_no_guarda_NADA(token):
    """Pablo, pidiendo el botón para la web de Kydo: *"que te lleve a una muestra que no
    grabe nada. Porque es bien genérico para muchas escuelas"*. El cuaderno de muestra es
    UNO, así que veinte escuelas mirando la demo escribirían todas en la misma clave."""
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    ids = [m["id"] for m in d["menu"]][:3]
    aw.orden_seno_guardar(token, [])                      # se parte de cero
    r = aw.orden_seno_guardar(token, ids, curso=aw.CURSO_MUESTRA)
    assert r["ok"] and r["guardado"] is False
    assert aw.orden_seno_leer(token, aw.CURSO_MUESTRA) == [], "guardó el borrador de la demo"


def test_la_muestra_NO_cae_al_camino_sin_curso(token):
    """LA trampa de este arreglo, y sería peor que el problema: si «EJEMPLO» se descartara
    como curso inválido, el pedido caería en la rama «sin curso» y escribiría en
    `orden_seno` — o sea que le cambiaría el cuaderno de muestra A TODO EL MUNDO."""
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    ids = [m["id"] for m in d["menu"]][:3]
    aw.orden_seno_guardar(token, [])
    aw.orden_seno_guardar(token, ids, curso=aw.CURSO_MUESTRA)
    assert aw.orden_seno_leer(token) == [], \
        "la demo terminó cambiándole el cuaderno de muestra a todo el mundo"


def test_un_curso_de_verdad_SI_guarda(token):
    """El control: el corte es sólo para la clave reservada."""
    d = json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"), encoding="utf-8"))
    ids = [m["id"] for m in d["menu"]][:3]
    r = aw.orden_seno_guardar(token, ids, curso="4A")
    assert r["ok"] and aw.orden_seno_leer(token, "4A") == ids


def test_el_player_no_ofrece_guardar_en_la_muestra():
    """Un botón que no hace lo que dice es peor que no estar."""
    js = _player()
    assert "function senoEsMuestra()" in js
    assert 'if (!muestra) guardar.addEventListener' in js, \
        "en la muestra el botón de guardar sigue enganchado"
    assert "Es una muestra: no se guarda" in js


def test_se_puede_volver_a_ver_la_ayuda():
    """Pablo: *"quiero volver a ver la ayuda, supongo que tenés que borrar el local
    storage"*. Ése es justamente el motivo del link: el recorrido se ve una vez y repetirlo
    exigía borrar una clave del navegador, que no se le puede pedir a nadie."""
    js = _player()
    assert "data-verayuda" in js, "no hay forma de volver a ver la ayuda"
    assert "localStorage.removeItem(SENO_TOUR_KEY)" in js
