"""La tabla tarjeta → clase de «Mi seño particular» (`seno_clases.py`).

Pablo, 11-sep-2026: *"icono de seño en cada tarjeta con practicas"*.

ES UNA COPIA Y ESTE ARCHIVO ES EL PRECIO
────────────────────────────────────────
Los temas de la seño viven en `kydo/seno/` del repo de ct3d. Este motor atiende a las DOS
marcas, así que no puede importar `kydo.*` en ejecución —del otro lado ya existe la regla
espejada, con su test—. Entonces el dato se copia con `gen_seno_clases.py`, y lo que impide
que la copia se pudra es esto.

LO QUE MÁS IMPORTA CORRE SIN CT3D, A PROPÓSITO
──────────────────────────────────────────────
La comparación contra la fuente necesita `/opt/ct3d` y se saltea donde no está (el CI). Pero
el modo de fallar más peligroso no es que la tabla quede vieja: es que quede **vacía o
recortada en silencio** —el cuaderno perdería todos los íconos y ningún test lo notaría—, y
eso se puede vigilar sin la otra punta. Por eso el piso de cantidad y la forma se comprueban
siempre.
"""
import importlib
import os
import sys

import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
CT3D = "/opt/ct3d/backend"

import seno_clases  # noqa: E402


# ── lo que corre SIEMPRE ─────────────────────────────────────────────────────────
def test_la_tabla_no_esta_vacia_ni_recortada():
    """El fallo más peligroso es el silencioso: `gen_seno_clases.py` corrido sin ct3d, o con
    el catálogo de saberes a medias, dejaría el cuaderno sin un solo ícono y nada fallaría.

    El piso es holgado a propósito: no fija el número exacto —que crece cuando se escriben
    clases nuevas— pero sí avisa si se desplomó."""
    total = sum(len(v) for v in seno_clases.CLASES.values())
    assert total >= 140, "la tabla quedó en %d tarjetas: se generó mal" % total
    assert sorted(seno_clases.CLASES) == [1, 2, 3, 4, 5, 6, 7], (
        "faltan grados: %s" % sorted(seno_clases.CLASES))


def test_la_forma_es_la_que_espera_el_player():
    """El player lee (id del tema, título). Un valor de otra forma rompería la tarjeta."""
    for grado, tarjetas in seno_clases.CLASES.items():
        assert isinstance(grado, int) and 1 <= grado <= 7, "grado raro: %r" % grado
        for act, par in tarjetas.items():
            assert isinstance(act, str) and act, "id de tarjeta vacío en %d.º" % grado
            assert isinstance(par, tuple) and len(par) == 2, (
                "%s de %d.º no es (tema, título): %r" % (act, grado, par))
            tema, titulo = par
            assert isinstance(tema, str) and tema, "%s: tema vacío" % act
            assert isinstance(titulo, str) and titulo, "%s: título vacío" % act


def test_de_devuelve_none_y_no_revienta():
    """Una tarjeta sin clase es lo normal —hoy son la mayoría— así que preguntar por ella
    tiene que ser barato y silencioso, no una excepción."""
    assert seno_clases.de(2, "no-existe-esta-tarjeta") is None
    assert seno_clases.de(99, "cualquiera") is None
    assert seno_clases.de(None, None) is None


def test_toda_tarjeta_de_la_tabla_ESTA_en_el_menu_de_su_grado():
    """Un ícono para una tarjeta que ese grado no tiene no se dibuja nunca: la entrada sobra
    y esconde que la clase quedó sin llegar a nadie. Se comprueba contra el menú de verdad.

    No necesita ct3d: el menú es de este repo."""
    import actividades_curriculum as ac
    import actividades_web as aw

    sobran = []
    for grado, tarjetas in seno_clases.CLASES.items():
        ids = {it["id"] for it in (ac.menu_de_grado(grado) or [])}
        ids |= {it["id"] for it in (aw._menu(aw._banda(str(grado + 5)), str(grado + 5),
                                             escolar=True) or [])}
        sobran += ["%d.º %s" % (grado, a) for a in tarjetas if a not in ids]
    assert not sobran, "tarjetas que no existen en su grado:\n  " + "\n  ".join(sobran)


# ── la comparación contra la fuente (necesita ct3d) ──────────────────────────────
def _de_la_fuente():
    """Rearma la tabla desde `kydo/seno/`. None si ct3d no está o si saberes llegó corto."""
    if not os.path.isdir(CT3D):
        return None
    sys.path.insert(0, CT3D)
    try:
        from saberes import SABERES
        import actividades_curriculum as ac
        import actividades_web as aw
        # El catálogo de saberes se arma con un try/except que suma las 325 del currículum:
        # sin el repo del motor en el path llega por la mitad, en silencio, y la comparación
        # diría cualquier cosa. Mejor no comparar que comparar contra algo roto.
        if len(SABERES) < 300:
            return None
        temas = {}
        for m in ["temas", "temas_lengua"] + ["temas_lengua_%d" % g for g in range(1, 8)]:
            try:
                mod = importlib.import_module("kydo.seno." + m)
            except ModuleNotFoundError:
                continue
            for v in vars(mod).values():
                if isinstance(v, dict) and isinstance(v.get("id"), str) and v.get("saber"):
                    temas.setdefault(v["id"], v)
        if not temas:
            return None
        out = {}
        for t in sorted(temas.values(), key=lambda x: x["id"]):
            s = SABERES.get(t["saber"])
            if not s:
                continue
            for j in (s.get("juegos") or []):
                out.setdefault(t["grado"], {}).setdefault(j, (t["id"], t["titulo"]))
        limpio = {}
        for g in range(1, 8):
            ids = {it["id"] for it in (ac.menu_de_grado(g) or [])}
            ids |= {it["id"] for it in (aw._menu(aw._banda(str(g + 5)), str(g + 5),
                                                 escolar=True) or [])}
            hay = {j: v for j, v in (out.get(g) or {}).items() if j in ids}
            if hay:
                limpio[g] = hay
        return limpio
    except Exception:
        return None


def test_la_copia_SIGUE_al_dia():
    """Si esto falla, no está mal el test: está vieja la tabla. Se regenera con
    `python3 gen_seno_clases.py`, parado en este repo."""
    real = _de_la_fuente()
    if real is None:
        pytest.skip("ct3d no está (o su catálogo llegó recortado): no hay contra qué comparar")
    difs = []
    for g in sorted(set(real) | set(seno_clases.CLASES)):
        r, m = real.get(g) or {}, seno_clases.CLASES.get(g) or {}
        for act in sorted(set(r) - set(m)):
            difs.append("%d.º %s: la seño tiene «%s» y la copia no lo trae" % (g, act, r[act][0]))
        for act in sorted(set(m) - set(r)):
            difs.append("%d.º %s: la copia lo tiene y la seño ya no" % (g, act))
        for act in sorted(set(r) & set(m)):
            if tuple(r[act]) != tuple(m[act]):
                difs.append("%d.º %s: la copia dice %s y la seño dice %s"
                            % (g, act, tuple(m[act]), tuple(r[act])))
    assert not difs, "la copia quedó vieja:\n  " + "\n  ".join(difs)


def test_ninguna_clase_es_de_OTRO_grado():
    """La seño sólo abre la clase del grado del cuaderno: si `tema["grado"] != grado`
    redirige al índice. Una entrada con la clase de otro año manda al chico a un rebote.

    Es el motivo por el que la tabla se indexa por grado y no por tarjeta: «La serie» y
    «Recta gigante» aparecen en 1.º y 2.º con el saber de 4.º, y sin esta regla habrían
    quedado apuntando a la clase de 4.º (38 tarjetas, medido el 11-sep-2026)."""
    if not os.path.isdir(CT3D):
        pytest.skip("ct3d no está")
    sys.path.insert(0, CT3D)
    try:
        from kydo.seno import temas as _t
    except Exception:
        pytest.skip("no se pudo leer los temas de la seño")
    grado_de = {}
    for m in ["temas", "temas_lengua"] + ["temas_lengua_%d" % g for g in range(1, 8)]:
        try:
            mod = importlib.import_module("kydo.seno." + m)
        except ModuleNotFoundError:
            continue
        for v in vars(mod).values():
            if isinstance(v, dict) and isinstance(v.get("id"), str) and v.get("grado"):
                grado_de.setdefault(v["id"], v["grado"])
    malas = []
    for grado, tarjetas in seno_clases.CLASES.items():
        for act, (tema, _tit) in tarjetas.items():
            g = grado_de.get(tema)
            if g is None:
                # UN TEMA QUE LA SEÑO NO TIENE ES PEOR QUE UNO DE OTRO GRADO: el de otro
                # grado rebota al índice, éste da 404. La primera versión decía
                # `if g is not None and g != grado` y por lo tanto **pasaba en verde con un
                # tema inventado** — se descubrió ensuciando la tabla a propósito el
                # 11-sep-2026, no corriéndola. Un test que sólo se mira pasar no se probó.
                malas.append("%d.º %s → %s, que NO existe en la seño" % (grado, act, tema))
            elif g != grado:
                malas.append("%d.º %s → %s, que es de %d.º" % (grado, act, tema, g))
    assert not malas, "clases que la seño no va a abrir:\n  " + "\n  ".join(malas)
