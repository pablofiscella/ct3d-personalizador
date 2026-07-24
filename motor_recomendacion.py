"""Motor de RECOMENDACIÓN — el capstone que une las dos mitades del híbrido.

`saberes.py` (ALEKS) dice qué está LISTO. `motor_dominio.py` (DreamBox) dice cómo viene el
chico. Este módulo los combina y responde la única pregunta que importa en cada momento:

    ¿Qué le conviene hacer a este chico AHORA?

Prioridad (del spec, orden probado en ALEKS/DreamBox):
  P1 · REPASO   — un saber dominado cuyo repaso espaciado ya venció (anti-olvido).
  P2 · REFUERZO — un saber donde se está trabando (estancado o error repetido): se va al
                  prerrequisito más débil (fallback ALEKS) o al mismo saber con la animación
                  específica del tipo de error (DreamBox).
  P3 · AVANZAR  — un saber del "outer fringe" (listo para aprender), priorizando lo ya
                  empezado y la menor dificultad. NUNCA algo cuyos prereqs no estén.
  —  · DESAFÍO  — si no hay nada de lo anterior, dominó todo lo alcanzable → modo creador.

Nada bloquea: si un saber no está listo, simplemente no se elige (queda pendiente).

Entrada = `historial`: dict {saber_id: [intentos]} (la evidencia por saber del chico).
100% puro — la persistencia de ese historial por-chico es el ladrillo de infra siguiente.
"""

import saberes as S
import motor_dominio as D

T_IDEAL_DEFAULT_MS = 12000  # ventana de tiempo esperada por defecto (se afinará por saber)


def _dominados(historial, t_ideal_ms):
    return {sid for sid, its in historial.items() if D.esta_dominado(its, t_ideal_ms)}


def _juego_de(sid, historial):
    """Elige un juego que mida el saber, rotando: el MENOS jugado (variantes, no repetir
    lo mismo). None si el saber no tiene juego (hueco de contenido)."""
    juegos = S.SABERES[sid]["juegos"]
    if not juegos:
        return None
    from collections import Counter
    veces = Counter(i.get("juego") for i in historial.get(sid, []) if i.get("juego"))
    return sorted(juegos, key=lambda j: (veces.get(j, 0), juegos.index(j)))[0]


def _prereq_mas_debil(sid, historial, t_ideal_ms):
    """Para el fallback: el prerrequisito no dominado con menor dominio; si todos están
    dominados, el propio saber."""
    prereqs = S.SABERES[sid]["prerrequisitos"]
    no_dom = [p for p in prereqs if not D.esta_dominado(historial.get(p, []), t_ideal_ms)]
    cand = no_dom or prereqs
    if not cand:
        return sid
    return min(cand, key=lambda p: D.dominio_actual(historial.get(p, []), t_ideal_ms))


def siguiente(historial, ahora_ts, t_ideal_ms=T_IDEAL_DEFAULT_MS):
    """Devuelve la recomendación de qué hacer ahora:
       {tipo, saber, nombre, juego, motivo[, animacion_tipo_error]}"""
    dominados = _dominados(historial, t_ideal_ms)

    # P1 · Repaso espaciado vencido (el más atrasado primero)
    vencidos = []
    for sid in dominados:
        pr = D.proximo_repaso_ts(historial[sid], ahora_ts, t_ideal_ms)
        if pr is not None and pr <= ahora_ts:
            vencidos.append((pr, sid))
    if vencidos:
        vencidos.sort()
        sid = vencidos[0][1]
        return {"tipo": "repaso", "saber": sid, "nombre": S.SABERES[sid]["nombre"],
                "juego": _juego_de(sid, historial), "motivo": "toca repasar para no olvidar"}

    # P2 · Refuerzo (estancado / error repetido)
    for sid, its in historial.items():
        ref = D.necesita_refuerzo(its, t_ideal_ms)
        if ref:
            objetivo = _prereq_mas_debil(sid, historial, t_ideal_ms) if ref["motivo"] == "estancado" else sid
            return {"tipo": "refuerzo", "saber": objetivo, "nombre": S.SABERES[objetivo]["nombre"],
                    "juego": _juego_de(objetivo, historial),
                    "motivo": f"{ref['motivo']} en {S.SABERES[sid]['nombre']}",
                    "animacion_tipo_error": ref.get("tipo_error")}

    # P3 · Avanzar (outer fringe), priorizando lo ya empezado y menor dificultad
    fringe = S.outer_fringe(dominados)
    if fringe:
        def prio(sid):
            est = D.estado(historial.get(sid, []), t_ideal_ms)
            empezado = 0 if est in ("en_progreso", "aprendido", "estancado") else 1
            return (empezado, S.SABERES[sid]["dificultad"], sid)
        sid = sorted(fringe, key=prio)[0]
        return {"tipo": "avanzar", "saber": sid, "nombre": S.SABERES[sid]["nombre"],
                "juego": _juego_de(sid, historial), "motivo": "listo para aprender"}

    # Nada listo → dominó todo lo alcanzable → modo creador/desafío
    return {"tipo": "desafio", "saber": None, "nombre": None, "juego": None,
            "motivo": "dominó todo lo disponible — modo creador/desafío"}
