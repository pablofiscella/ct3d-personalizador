# -*- coding: utf-8 -*-
"""Una pregunta no se repite en dos actividades que el mismo chico puede jugar.

29-jul-2026. Pablo, mirando el cuaderno: *"cada vez que la voz de Valeria pregunte algo
no se tiene que repetir en las otras, como vi que pasa en «Nodos, enlaces y capas de la
red» y en «Evento, acción y paralelismo». Debe haber otras seguramente"*.

Había 27. El síntoma es la voz porque el audio se cachea por hash del TEXTO
(`servicio._tts_dinamico`): dos actividades con la misma pregunta escrita comparten el
mismo mp3, así que Valeria dice literalmente la misma frase dos veces y se nota mucho
más que leyéndolo.

QUÉ CUENTA COMO "EL MISMO CHICO". No alcanza con mirar dentro de un grado: el cuarto
escalón «🚀 Más allá» le ofrece actividades del grado SIGUIENTE
(`actividades_player.js`, `esMasAlla`). Por eso el par 6.º↔7.º repite tanto como el
6.º↔6.º — de hecho ahí estaban 25 de los 27 casos, incluidos los dos que vio Pablo.

POR QUÉ SÓLO IGUALDAD EXACTA. Se probó con similitud de texto y da muchísimos falsos
positivos: «1/2 + 1/3 =» y «1/2 ÷ 1/4 =» se parecen en un 86% y son ejercicios
distintos, igual que «¿Qué hace una polea?» y «¿Qué hace una leva?». Un guardián que
grita por eso se termina apagando. Acá se exige lo indiscutible: dos preguntas
IDÉNTICAS que un mismo chico puede escuchar. Las reescrituras triviales
(«¿Qué es un actuador?» vs «¿Qué hace un actuador?») se corrigieron a mano.
"""
import os
import sys
from collections import defaultdict

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import actividades_curriculum as cur  # noqa: E402


def _preguntas_por_grado():
    porg = defaultdict(list)
    for a in cur.CATALOGO:
        for it in (a.get("banco") or []):
            q = (it.get("q") or "").strip()
            if q:
                porg[a["grado"]].append((a["id"], q))
    return porg


def _repetidas():
    """[(pregunta, act_a, grado_a, act_b, grado_b)] que un chico puede oír dos veces."""
    porg = _preguntas_por_grado()
    vistos, out = set(), []
    for g in sorted(porg):
        por_texto = defaultdict(set)
        for aid, q in porg[g]:
            por_texto[q].add(aid)
        for gg in (g, g + 1):                       # su grado y el de «Más allá»
            if gg not in porg:
                continue
            for aid, q in porg[gg]:
                for oid in por_texto.get(q, ()):
                    if oid == aid:
                        continue
                    k = tuple(sorted((oid, aid))) + (q,)
                    if k in vistos:
                        continue
                    vistos.add(k)
                    out.append((q, oid, g, aid, gg))
    return out


def test_ninguna_pregunta_se_repite_para_un_mismo_chico():
    """EL guardián. Si falla, la voz va a decir la misma frase en dos actividades."""
    reps = _repetidas()
    detalle = "\n".join(
        "  «%s»\n      %d.º %s  ↔  %d.º %s" % (q, ga, a, gb, b)
        for q, a, ga, b, gb in reps)
    assert not reps, (
        "%d pregunta(s) repetidas entre actividades que el mismo chico puede jugar "
        "(su grado o el siguiente, por «Más allá»):\n%s" % (len(reps), detalle))


@pytest.mark.parametrize("act", cur.CATALOGO, ids=lambda a: a["id"])
def test_ninguna_actividad_repite_una_pregunta_adentro(act):
    """Lo mismo puertas adentro: la misma pregunta dos veces en el mismo juego."""
    qs = [(it.get("q") or "").strip() for it in (act.get("banco") or [])]
    qs = [q for q in qs if q]
    repes = sorted({q for q in qs if qs.count(q) > 1})
    assert not repes, "%s repite: %s" % (act["id"], repes)


def test_el_catalogo_sigue_siendo_valido():
    """Las correcciones no pueden dejar el catálogo inconsistente."""
    problemas = cur.validar()
    assert not problemas, "\n".join(problemas)


def test_las_dos_que_vio_pablo_quedaron_separadas():
    """Caso testigo: el evento de programación estaba en 6.º y en 7.º casi igual."""
    def qs(aid):
        a = next((x for x in cur.CATALOGO if x["id"] == aid), None)
        assert a, "no existe la actividad %s" % aid
        return {(it.get("q") or "").strip() for it in (a.get("banco") or [])}

    siete = qs("eventos_paralelismo_7")
    seis = qs("bloques_codigo_6")
    assert "¿Qué es un evento en programación?" in siete, \
        "la definición de evento vive en la actividad que trata de eventos"
    assert not any("evento en programación" in q for q in seis), \
        "6.º volvió a definir «evento en programación», que ya define 7.º"
    assert not (siete & seis), "las dos actividades comparten preguntas"
