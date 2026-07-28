# -*- coding: utf-8 -*-
"""La sopa de letras se gradúa por GRADO en la línea escolar.

28-jul-2026. Pablo: *"necesito que veas las sopas de letras y que las palabras que
aparezcan sean temáticas en 1ro y 2do pero en los grados siguientes tienen que
estar acorde a la edad"*.

Lo que había: los 7 grados recibían la MISMA sopa —10×10, 6 palabras del tema de
cumpleaños del token, las 8 direcciones—. Como los 49 tokens con `escolar_on` son
`tema=safari`, un chico de 7° en el mundo "Creadores del Futuro" buscaba MONO,
JIRAFA y CEBRA, las mismas seis palabras que uno de 1°. Es la misma dificultad
invertida que se arregló en `serie` (`actividades_web.py:195-198`), y la sopa se la
había salteado.

Lo que se verifica acá: (a) cada grado recibe la grilla, la cantidad de palabras y
las direcciones de `_SOPA_GRADO`; (b) de 3° para arriba las palabras salen del
vocabulario curricular del grado y NINGUNA es del tema —la aserción que responde
literalmente al pedido—; (c) las 4 sopas de un token dejaron de ser la misma sopa
barajada; (d) la garantía de no-regresión: un token sin `escolar_on` (la compra del
kit) sigue exactamente como estaba.
"""
import json
import os
import random
import shutil
import sys
import zlib

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import actividades_vocabulario as voc  # noqa: E402
import actividades_web as aw  # noqa: E402
import cuaderno  # noqa: E402

TEMA = "safari"
GRADOS = sorted(aw._SOPA_GRADO)
# Las mismas 8 con las que salieron los 49 tokens escolares hasta hoy.
PALABRAS_TEMA = ["LEÓN", "JIRAFA", "CEBRA", "SELVA", "MONO", "SAFARI", "HUELLA", "RÍO"]


def _sopas(grado, escolar=True, semilla=None, palabras=None):
    """Las 4 sopas de un token de ese grado, sin generar el token entero."""
    edad = str(grado + 5)
    seed = zlib.crc32((semilla or ("sopa-g%d" % grado)).encode())
    return aw._sopas_del_token(list(palabras or PALABRAS_TEMA), edad, seed,
                               random.Random(seed), escolar=escolar)


def _paso(cs):
    """Dirección en la que quedó colocada una palabra (dx, dy)."""
    return (cs[1][0] - cs[0][0], cs[1][1] - cs[0][1])


# ── el banco de vocabulario ─────────────────────────────────────────────────────
def test_el_banco_de_vocabulario_es_valido():
    """`validar()` cubre las tres reglas del banco: nada de Ñ (el relleno de la
    grilla es A-Z y la delata), 3° sin tildes (ahí la tilde ES el contenido) y un
    piso de palabras usables por grado."""
    problemas = voc.validar()
    assert not problemas, "\n".join(problemas)


@pytest.mark.parametrize("grado", GRADOS)
def test_ninguna_palabra_delata_su_lugar_en_la_grilla(grado):
    """El relleno de `_wordsearch` es A-Z uniforme (`cuaderno.py:640`): cualquier
    letra que no sea A-Z —una Ñ, una diéresis— no puede salir del relleno y marca
    la palabra a simple vista. Después de `_sin_tilde` no puede quedar ninguna."""
    import string
    for p in voc.usables(grado):
        fuera = set(cuaderno._sin_tilde(p)) - set(string.ascii_uppercase)
        assert not fuera, (grado, p, sorted(fuera))


@pytest.mark.parametrize("grado", GRADOS)
def test_cada_grado_tiene_banco_de_sobra(grado):
    """Con las 8 palabras de un tema, las 4 sopas del token eran la misma sopa
    barajada. El piso está en 24 usables; si alguna vez baja, esto lo dice."""
    usables = voc.usables(grado)
    assert len(usables) >= voc.MINIMO_USABLES, (grado, len(usables))


@pytest.mark.parametrize("grado", [3, 4, 5, 6, 7])
def test_de_3ro_para_arriba_el_banco_es_curricular(grado):
    """Cuatro áreas declaradas, para que la sopa cruce matemática, lengua,
    naturales y sociales en vez de ser una lista suelta."""
    assert set(voc.VOCABULARIO[grado]) == {"matematica", "lengua", "naturales", "sociales"}


@pytest.mark.parametrize("grado", [1, 2])
def test_1ro_y_2do_van_por_el_mundo_del_grado(grado):
    """Pablo pidió temáticas en 1° y 2°: son las del mundo que el chico ya tiene en
    la portada (`MUNDO_GRADO`), no las del tema de cumpleaños del token."""
    assert list(voc.VOCABULARIO[grado]) == ["mundo"]
    assert aw.MUNDO_GRADO[grado]


# ── la tabla por grado llega al cuaderno ────────────────────────────────────────
@pytest.mark.parametrize("grado", GRADOS)
def test_cada_grado_recibe_su_grilla_y_su_cantidad(grado):
    cfg = aw._SOPA_GRADO[grado]
    sopas = _sopas(grado)
    assert len(sopas) == 4, "grado %d se quedó con %d sopas" % (grado, len(sopas))
    for i, s in enumerate(sopas):
        # La grilla es EXACTAMENTE la de la auditoría, igual en las 4 sopas: cada
        # columna de más achica la celda y en un teléfono chico eso se paga caro.
        assert s["n"] == cfg["n"], (grado, i, s["n"])
        assert len(s["palabras"]) == len(s["lindas"])
        assert 4 <= len(s["palabras"]) <= cfg["palabras"], (grado, i, s["lindas"])
        for p in s["lindas"]:
            assert 3 <= len(p) <= cfg["max"], (grado, p)


@pytest.mark.parametrize("grado", GRADOS)
def test_las_dos_primeras_sopas_son_mas_faciles(grado):
    """El gradiente del token va por CANTIDAD de palabras, no por tamaño de
    grilla: las dos primeras esconden una menos (con piso en 4)."""
    cfg = aw._SOPA_GRADO[grado]
    sopas = _sopas(grado)
    esperado = max(4, cfg["palabras"] - 1)
    for i, s in enumerate(sopas):
        assert len(s["palabras"]) == (esperado if i < 2 else cfg["palabras"]), (grado, i)


@pytest.mark.parametrize("grado", GRADOS)
def test_la_grilla_crece_con_el_grado(grado):
    """El orden entre grados no se puede invertir: es exactamente el bug que se
    arregló en `serie` y del que la sopa se había salvado."""
    cfg = aw._SOPA_GRADO[grado]
    if grado > 1:
        previo = aw._SOPA_GRADO[grado - 1]
        assert cfg["n"] >= previo["n"], (grado, cfg["n"], previo["n"])
        assert cfg["palabras"] >= previo["palabras"]
        assert cfg["max"] >= previo["max"]


@pytest.mark.parametrize("grado", GRADOS)
def test_las_soluciones_reconstruyen_la_palabra(grado):
    """Contrato de siempre (test_actividades_web.py:293), ahora con grillas de
    tamaño variable: `sol` tiene que leerse desde `filas[y][x]`."""
    for s in _sopas(grado):
        for w, cs in s["sol"].items():
            assert "".join(s["filas"][y][x] for x, y in cs) == w, (grado, w)
        assert len(s["filas"]) == s["n"]
        for fila in s["filas"]:
            assert len(fila) == s["n"]


# ── la respuesta literal al pedido ──────────────────────────────────────────────
@pytest.mark.parametrize("grado", [3, 4, 5, 6, 7])
def test_de_3ro_para_arriba_no_queda_ni_una_palabra_del_tema(grado):
    """LA aserción del pedido: en 3°-7° no puede aparecer una palabra de safari
    (ni de ningún tema de cumpleaños) — tienen que ser acordes a la edad."""
    del_tema = {cuaderno._sin_tilde(p) for p in PALABRAS_TEMA}
    banco = {cuaderno._sin_tilde(p) for p in voc.usables(grado)}
    for s in _sopas(grado):
        usadas = set(s["palabras"])
        assert not (usadas & del_tema), (grado, sorted(usadas & del_tema))
        assert usadas <= banco, (grado, sorted(usadas - banco))


@pytest.mark.parametrize("grado", [3, 4, 5, 6, 7])
def test_cada_sopa_cruza_mas_de_un_area(grado):
    """El reparto es round-robin entre áreas: con un sample plano una sopa de 7°
    podía salir entera de matemática y se perdía el cruce curricular."""
    por_area = {a: {cuaderno._sin_tilde(p.strip().upper()) for p in ws}
                for a, ws in voc.VOCABULARIO[grado].items()}
    for s in _sopas(grado):
        areas = {a for a, ws in por_area.items() if ws & set(s["palabras"])}
        assert len(areas) >= 2, (grado, s["lindas"], sorted(areas))


@pytest.mark.parametrize("grado", GRADOS)
def test_las_4_sopas_del_token_no_repiten_ni_una_palabra(grado):
    """Antes las 4 sopas eran 6 palabras de las mismas 8: el chico resolvía cuatro
    veces la misma sopa. El banco de cada grado tiene de sobra para las cuatro
    (`evitar=usadas` en `_sopas_del_token`), así que no debería repetirse nada."""
    cfg = aw._SOPA_GRADO[grado]
    assert len(voc.usables(grado)) >= 4 * cfg["palabras"], "banco justo: revisar el piso"
    assert cfg["n"] <= 12, "grilla más grande = celda más chica en el teléfono"
    todas = [w for s in _sopas(grado) for w in s["palabras"]]
    repetidas = sorted({w for w in todas if todas.count(w) > 1})
    assert not repetidas, (grado, repetidas)


# ── direcciones: lo que pidieron las auditorías para los grados chicos ──────────
def test_en_1ro_las_palabras_van_solo_a_la_derecha_o_para_abajo():
    """`docs/auditoria-dc-caba/grado-1.md:173`: la sopa de 8 direcciones "entrena
    CONTRA la direccionalidad" a los 6 años, cuando el chico recién aprende para
    qué lado se lee. Nada de reversas ni diagonales."""
    for s in _sopas(1):
        for w, cs in s["sol"].items():
            assert _paso(cs) in [(1, 0), (0, 1)], (w, _paso(cs))


def test_en_2do_no_hay_palabras_invertidas():
    """`grado-2.md:176`: en 2° entra la diagonal DE IDA, pero ninguna invertida."""
    permitidas = [(1, 0), (0, 1), (1, 1)]
    for i, s in enumerate(_sopas(2)):
        for w, cs in s["sol"].items():
            paso = _paso(cs)
            assert paso in permitidas, (i, w, paso)
            if i < 2:
                assert paso != (1, 1), "las 2 primeras de 2° van sin diagonal"


@pytest.mark.parametrize("grado", [3, 4, 5, 6, 7])
def test_de_3ro_para_arriba_siguen_las_8_direcciones(grado):
    assert aw._SOPA_GRADO[grado]["dirs"] == "todas"
    assert aw._dirs_sopa("todas") is None, "None = el juego completo de cuaderno._DIRS"


# ── no-regresión: la compra del kit no se toca ─────────────────────────────────
@pytest.mark.parametrize("grado", GRADOS)
def test_sin_flag_escolar_la_sopa_queda_como_estaba(grado):
    """LA garantía comercial: el que compró un kit de safari para un cumpleaños
    sigue recibiendo safari en 10×10 con 6 palabras, tenga la edad que tenga."""
    sopas = _sopas(grado, escolar=False)
    assert len(sopas) == 4
    del_tema = {cuaderno._sin_tilde(p) for p in PALABRAS_TEMA}
    for s in sopas:
        assert s["n"] == 10, s["n"]
        assert len(s["palabras"]) == 6, s["lindas"]
        assert set(s["palabras"]) <= del_tema, s["lindas"]


def test_el_banco_del_grado_no_se_usa_si_no_hay_arte_del_grado(monkeypatch, tmp_path):
    """Misma compuerta que el resto de la temática (`_grado_con_arte`): sin la
    carpeta de arte del grado, el cuaderno cae al tema y no promete un mundo que
    no muestra."""
    monkeypatch.setattr(aw, "ARTE_DIR", str(tmp_path))
    sopas = _sopas(7)
    del_tema = {cuaderno._sin_tilde(p) for p in PALABRAS_TEMA}
    assert sopas and all(s["n"] == 10 and set(s["palabras"]) <= del_tema for s in sopas)


def test_si_el_banco_falla_el_cuaderno_sale_igual(monkeypatch):
    """El vocabulario nunca puede voltear la generación de un token: si el módulo
    explota, la sopa sale con el tema de siempre (criterio de `_menu_curricular`)."""
    def _boom(*a, **k):
        raise RuntimeError("banco roto")
    monkeypatch.setattr(voc, "usables", _boom)
    sopas = _sopas(6)
    assert len(sopas) == 4 and all(s["n"] == 10 for s in sopas)


# ── el token completo, punta a punta ───────────────────────────────────────────
def test_token_escolar_de_7mo_no_trae_safari():
    """El camino real (`aw.crear` → `data.json`), que es lo que lee el player."""
    tok = "test-sopa-7mo-zz"
    d = os.path.join(aw.ACT_DIR, tok)
    shutil.rmtree(d, ignore_errors=True)
    try:
        aw.crear({"nombre": "Test", "edad": "12", "escolar_on": True}, TEMA, token=tok)
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        assert dj["sopas"], "7° escolar sin sopas"
        del_tema = {cuaderno._sin_tilde(p) for p in PALABRAS_TEMA}
        for s in dj["sopas"]:
            assert s["n"] >= 12, s["n"]
            assert not (set(s["palabras"]) & del_tema), s["lindas"]
        cfg = [it["cfg"] for it in dj["menu"] if it["id"] == "sopa"]
        assert cfg and cfg[0].get("n") == 12, cfg
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_el_codigo_secreto_sigue_saliendo_del_tema():
    """`cuaderno._construir` elige la palabra del "Código secreto" de la MISMA
    lista que la sopa, y `_a_codigo` saltea la página EN SILENCIO si la palabra
    tiene más letras distintas que stickers hay. El vocabulario curricular es más
    largo, así que el código secreto no puede engancharse a ese banco."""
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "cuaderno.py"), encoding="utf-8").read()
    assert "import actividades_vocabulario" not in src, (
        "cuaderno.py no debe leer el banco por grado: se lo llevaría el código secreto")
    # y la palabra del código secreto sigue saliendo del tema, corta y con pocas
    # letras distintas (`_a_codigo` necesita un sticker por letra)
    ws = cuaderno._tema_palabras(TEMA) or list(cuaderno.PALABRAS)
    pal = min([w for w in ws if 5 <= len(w) <= 8] or ws, key=len)
    assert pal in ws and len(set(cuaderno._sin_tilde(pal))) <= 8, pal


def test_la_sopa_impresa_no_voltea_el_pdf_con_una_palabra_larga():
    """`_a_sopa` no tenía filtro de largo: una palabra más larga que la grilla
    agotaba los 120 seeds y el assert volteaba el PDF ENTERO, no la página."""
    assert cuaderno._wordsearch(["ELECTRODOMESTICO"], 12, 1) == (None, None)


def test_direcciones_reducidas_disponibles_en_cuaderno():
    """Los juegos reducidos viven en cuaderno.py junto a `_DIRS` y el default no
    cambió: el kit imprimible sigue con las 8."""
    assert cuaderno._DIRS_RECTA == [(1, 0), (0, 1)]
    assert cuaderno._DIRS_IDA == [(1, 0), (0, 1), (1, 1)]
    assert len(cuaderno._DIRS) == 8
    g, _sol = cuaderno._wordsearch(["CASA", "SOL"], 8, 3, dirs=cuaderno._DIRS_RECTA)
    assert g, "no colocó con direcciones reducidas"
