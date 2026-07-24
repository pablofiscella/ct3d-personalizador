"""Motor de DOMINIO — la capa DreamBox del híbrido (ver `ct3d-motor-adaptativo-saberes`).

Mientras `saberes.py` (capa ALEKS) responde "¿qué está LISTO para aprender?", este módulo
responde "¿el chico DOMINA de verdad este saber?" — y esa es la diferencia clave: no alcanza
con acertar. Se pondera CÓMO lo resolvió (tiempo, pistas, reintentos, racha) y se exige
repetición ESPACIADA con variantes antes de declararlo dominado. Así:
  - no se dispara el mail de upsell por 3 aciertos de suerte seguidos;
  - un acierto rápido sin pistas vale mucho más que uno lento con 5 ayudas;
  - lo tagueado "no visto en clase" no cuenta para dominio (no contamina).

Es 100% funciones puras sobre una lista de INTENTOS (evidencia). No toca DB ni red — la
persistencia por-chico es el ladrillo siguiente. Cada intento (evento de telemetría, estilo
DreamBox) es un dict:

  {
    "saber": "MAT-4-DIV1",
    "ts": 1_700_000_000,          # epoch en segundos (para calcular espaciado)
    "correcto": True,
    "intentos_en_actividad": 1,   # 1 = lo resolvió al primer toque
    "pistas": 0,                  # ayudas visuales pedidas
    "audio": 0,                   # veces que escuchó la explicación
    "tiempo_ms": 9000,
    "tipo_error": None,           # "conceptual" | "calculo" | "consigna" | None
    "no_visto_en_clase": False,   # tag del padre/chico → no cuenta para dominio
  }
"""

# Pesos de la fórmula de dominio M = C·50 + A·20 + T·15 + H·15  (escala 0..100)
PESO_CORRECTITUD = 50
PESO_AUTONOMIA = 20
PESO_TIEMPO = 15
PESO_RACHA = 15

# Umbrales de estado
UMBRAL_DOMINADO = 85     # score >= 85 → candidato a dominado (falta lo espaciado)
UMBRAL_EN_PROGRESO = 50  # 50..84 → en progreso; < 50 sostenido → estancado
UMBRAL_ACIERTO_SOLIDO = 70  # un acierto solo cuenta para el espaciado si su score >= esto
                            # (así 3 aciertos con muchas pistas/reintentos NO dan "dominado")

# Repetición espaciada para alcanzar DOMINADO: 3 aciertos con gaps crecientes.
GAP_1 = 24 * 3600        # entre acierto 1 y 2: > 24 h
GAP_2 = 72 * 3600        # entre acierto 2 y 3: > 72 h
# Intervalos de repaso una vez dominado (días) — anti-olvido, estilo SuperMemo/Anki.
REPASO_DIAS = [7, 21, 45, 90]


# ───────────────────────── Factores del score de un intento ─────────────────────────

def factor_correctitud(it):
    if not it.get("correcto"):
        return 0.0
    return 1.0 if int(it.get("intentos_en_actividad", 1)) <= 1 else 0.5


def factor_autonomia(it):
    """1.0 sin ayuda; baja con pistas (0.3 c/u) y audio-explicación (0.2 c/u)."""
    val = 1.0 - 0.3 * int(it.get("pistas", 0)) - 0.2 * int(it.get("audio", 0))
    return max(0.0, min(1.0, val))


def factor_tiempo(it, t_ideal_ms):
    """1.0 en la ventana esperada. Penaliza IMPULSIVO (<1s → probablemente al azar,
    señal DreamBox) y muy LENTO (no entendió / se trabó)."""
    t = int(it.get("tiempo_ms", 0))
    if t < 1000:
        return 0.3
    if t_ideal_ms <= 0:
        return 1.0
    ratio = t / t_ideal_ms
    if ratio <= 1.5:
        return 1.0
    if ratio <= 3.0:
        return 0.6
    return 0.3


def factor_racha(intentos_saber_hasta_ahora):
    """Proporción de aciertos en los últimos 3 intentos del saber (incluye el actual)."""
    ult = intentos_saber_hasta_ahora[-3:]
    if not ult:
        return 0.0
    return sum(1 for i in ult if i.get("correcto")) / len(ult)


def score_intento(it, t_ideal_ms, intentos_saber_hasta_ahora):
    """Score 0..100 de un intento (la M de la 3ra IA)."""
    c = factor_correctitud(it)
    a = factor_autonomia(it)
    t = factor_tiempo(it, t_ideal_ms)
    h = factor_racha(intentos_saber_hasta_ahora)
    return c * PESO_CORRECTITUD + a * PESO_AUTONOMIA + t * PESO_TIEMPO + h * PESO_RACHA


# ───────────────────────── Evaluación de un saber ─────────────────────────

def _ordenados(intentos):
    return sorted(intentos, key=lambda i: i.get("ts", 0))


def aciertos_espaciados(intentos, t_ideal_ms):
    """Cadena de aciertos VÁLIDOS (correctos, sin ayuda excesiva, NO 'no_visto') con
    gaps crecientes (>24h, >72h). Devuelve la lista de intentos que forman la cadena
    (hasta 3 para dominio; si hay más aciertos espaciados posteriores, se agregan para
    los repasos). Un acierto vale para la cadena SOLO si fue 'sólido' (score >= umbral):
    así 3 aciertos con muchas pistas o reintentos NO alcanzan para dominar."""
    seq = _ordenados(intentos)
    scores = [score_intento(seq[k], t_ideal_ms, seq[: k + 1]) for k in range(len(seq))]
    validos = [
        seq[k] for k in range(len(seq))
        if seq[k].get("correcto") and not seq[k].get("no_visto_en_clase")
        and scores[k] >= UMBRAL_ACIERTO_SOLIDO
    ]
    gaps = [GAP_1, GAP_2]
    cadena = []
    for it in validos:
        if not cadena:
            cadena.append(it)
            continue
        req = gaps[min(len(cadena) - 1, len(gaps) - 1)]
        if it["ts"] - cadena[-1]["ts"] > req:
            cadena.append(it)
    return cadena


def esta_dominado(intentos, t_ideal_ms):
    """Dominado = 3 aciertos espaciados VÁLIDOS y SÓLIDOS (gaps 24h/72h, sin 'no_visto',
    score alto en cada uno)."""
    return len(aciertos_espaciados(intentos, t_ideal_ms)) >= 3


def dominio_actual(intentos, t_ideal_ms):
    """Score 0..100 del estado ACTUAL: promedio de los scores de los últimos 3 intentos
    del saber (refleja cómo viene ahora, no el histórico entero)."""
    seq = _ordenados(intentos)
    if not seq:
        return 0.0
    scores = [score_intento(seq[k], t_ideal_ms, seq[: k + 1]) for k in range(len(seq))]
    ult = scores[-3:]
    return sum(ult) / len(ult)


def tipo_error_frecuente(intentos, ventana=3):
    """El tipo de error más común entre los últimos fallos → decide qué animación
    específica mostrar (capa DreamBox: no otra actividad difícil, sino LA explicación)."""
    fallos = [i for i in _ordenados(intentos) if not i.get("correcto") and i.get("tipo_error")]
    fallos = fallos[-ventana:]
    if not fallos:
        return None
    from collections import Counter
    return Counter(i["tipo_error"] for i in fallos).most_common(1)[0][0]


def estado(intentos, t_ideal_ms):
    """Estado de dominio de un saber:
       'no_iniciado' | 'en_progreso' | 'estancado' | 'aprendido' | 'dominado'
       - dominado  → 3 aciertos espaciados (consolidado, listo para el mail a padres)
       - aprendido → score >= 85 pero todavía sin el espaciado (dominio TENTATIVO,
                      distinción learned-vs-mastered de ALEKS: aún no avisar a los padres)
       - estancado → los últimos 3 intentos con score < 50 (activar fallback a prereq)
       - en_progreso / no_iniciado según haya o no evidencia."""
    if not intentos:
        return "no_iniciado"
    if esta_dominado(intentos, t_ideal_ms):
        return "dominado"
    seq = _ordenados(intentos)
    scores = [score_intento(seq[k], t_ideal_ms, seq[: k + 1]) for k in range(len(seq))]
    ult = scores[-3:]
    if len(ult) >= 3 and all(s < UMBRAL_EN_PROGRESO for s in ult):
        return "estancado"
    if dominio_actual(intentos, t_ideal_ms) >= UMBRAL_DOMINADO:
        return "aprendido"
    return "en_progreso"


def evaluar_saber(intentos, t_ideal_ms):
    """Resumen completo del saber para un chico (lo que consume el motor/paneles)."""
    esp = aciertos_espaciados(intentos, t_ideal_ms)
    return {
        "estado": estado(intentos, t_ideal_ms),
        "dominio": round(dominio_actual(intentos, t_ideal_ms), 1),
        "aciertos_espaciados": len(esp),
        "total_intentos": len(intentos),
        "tipo_error_frecuente": tipo_error_frecuente(intentos),
        "listo_para_mail_padres": esta_dominado(intentos, t_ideal_ms),  # solo dominado real
    }


def proximo_repaso_ts(intentos, ahora_ts, t_ideal_ms):
    """Cuándo conviene repasar un saber dominado (anti-olvido). Devuelve epoch, o None
    si todavía no está dominado. Usa el nº de repasos ya hechos para espaciar más."""
    esp = aciertos_espaciados(intentos, t_ideal_ms)
    if len(esp) < 3:
        return None
    repasos_hechos = max(0, len(esp) - 3)
    dias = REPASO_DIAS[min(repasos_hechos, len(REPASO_DIAS) - 1)]
    return esp[-1]["ts"] + dias * 86400


def necesita_refuerzo(intentos, t_ideal_ms):
    """¿Hay que intervenir con refuerzo dirigido? Devuelve dict con el motivo y el
    tipo de error, o None. Dispara la animación específica (no otra actividad difícil)."""
    if estado(intentos, t_ideal_ms) == "estancado":
        return {"motivo": "estancado", "tipo_error": tipo_error_frecuente(intentos)}
    te = tipo_error_frecuente(intentos, ventana=3)
    fallos_recientes = [i for i in _ordenados(intentos)[-3:]
                        if not i.get("correcto") and i.get("tipo_error") == te]
    if te and len(fallos_recientes) >= 2:
        return {"motivo": "error_repetido", "tipo_error": te}
    return None
