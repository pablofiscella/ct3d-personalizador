"""Grafo de SABERES — cimiento del motor de aprendizaje adaptativo (híbrido ALEKS+DreamBox).

PILOTO: 4° Matemática (CABA). Ver diseño en memoria `ct3d-motor-adaptativo-saberes`.

MÉTODO (corregido 24-jul tras el error del bingo): cada saber se mapea a los juegos que
REALMENTE lo miden, verificado LEYENDO LA CONSIGNA del juego (no adivinando por el nombre).
Regla dura: un juego solo cuenta como evidencia de un saber si (a) está en el menú de 4°,
(b) su consigna testea ESE contenido curricular, y (c) tiene dificultad de 4° (no 1°-2°).
Los juegos LÚDICOS que operan con sprites del tema (bingo=matching de imágenes,
agrupar=clasificar en canastas, patron=seguir secuencia visual, memotest, sudoku de caras,
quefalta, laberinto, simon) NO son evidencia de ningún saber → van a la categoría EXTRAS
(ver actividades_categorias.py) y NUNCA se marcan "recomendado" como contenido a aprender.

Idea (ALEKS-Lite): el conocimiento es el conjunto de SABERES dominados; cada uno tiene
prerrequisitos. El "outer fringe" (no dominado + prereqs cumplidos) = lo que está listo para
aprender AHORA. Nada bloquea: lo no listo queda pendiente mientras el motor ofrece el fringe.
Las ACTIVIDADES son la EVIDENCIA; el dominio real lo mide `motor_dominio.py` (capa DreamBox).

Los saberes de grado < 4 son ANCLAS asumidas (el chico está en 4°): no se miden con juegos
del menú de 4°, solo sirven de raíz de prerrequisitos. Cada saber de 4° tiene AL MENOS un
juego real del menú de 4° que lo mide.
"""

SABERES = {
    # ── Anclas de 3° (asumidas dominadas; no se miden en 4°, son raíz de prereqs) ──
    "MAT-3-NUM":       {"nombre": "Numeración hasta 1.000", "eje": "numeracion", "grado": 3,
                        "prerrequisitos": [], "juegos": [], "dificultad": 1},
    "MAT-3-SUMARESTA": {"nombre": "Suma y resta con llevada/canje (3° cifras)", "eje": "operaciones", "grado": 3,
                        "prerrequisitos": ["MAT-3-NUM"], "juegos": [], "dificultad": 1},
    "MAT-3-TABLAS":    {"nombre": "Tablas de multiplicar (memorización)", "eje": "operaciones", "grado": 3,
                        "prerrequisitos": [], "juegos": [], "dificultad": 1},
    "MAT-3-MULT":      {"nombre": "Concepto de multiplicación", "eje": "operaciones", "grado": 3,
                        "prerrequisitos": ["MAT-3-SUMARESTA", "MAT-3-TABLAS"], "juegos": [], "dificultad": 2},
    "MAT-3-DIV":       {"nombre": "Concepto de división y reparto", "eje": "operaciones", "grado": 3,
                        "prerrequisitos": ["MAT-3-MULT"], "juegos": [], "dificultad": 2},

    # ── 4° · NUMERACIÓN ── (verificado por consigna)
    "MAT-4-SERIES":    {"nombre": "Series numéricas (¿qué número falta?)", "eje": "numeracion", "grado": 4,
                        "prerrequisitos": ["MAT-3-NUM"], "juegos": ["serie"], "dificultad": 2},
    "MAT-4-RECTA":     {"nombre": "Ubicar números en la recta numérica", "eje": "numeracion", "grado": 4,
                        "prerrequisitos": ["MAT-3-NUM"], "juegos": ["recta_numerica"], "dificultad": 2},

    # ── 4° · OPERACIONES ──
    "MAT-4-SUMA":      {"nombre": "Suma en columna (números grandes)", "eje": "operaciones", "grado": 4,
                        "prerrequisitos": ["MAT-3-SUMARESTA"], "juegos": ["suma_columnas"], "dificultad": 2},
    "MAT-4-TABLAS":    {"nombre": "Agilidad con las tablas", "eje": "operaciones", "grado": 4,
                        "prerrequisitos": ["MAT-3-TABLAS"], "juegos": ["tablas_ninja"], "dificultad": 2},
    "MAT-4-MUL":       {"nombre": "Multiplicación (algoritmo)", "eje": "operaciones", "grado": 4,
                        "prerrequisitos": ["MAT-4-TABLAS", "MAT-3-MULT"], "juegos": ["multiplicar"], "dificultad": 3},
    "MAT-4-DIV":       {"nombre": "División por una cifra", "eje": "operaciones", "grado": 4,
                        "prerrequisitos": ["MAT-4-MUL", "MAT-3-DIV"], "juegos": ["dividir"], "dificultad": 3},
    "MAT-4-DIV-LARGA": {"nombre": "División larga / cuenta larga", "eje": "operaciones", "grado": 4,
                        "prerrequisitos": ["MAT-4-DIV"], "juegos": ["cuenta_larga"], "dificultad": 4},
    "MAT-4-PROB":      {"nombre": "Problemas de multiplicación y división", "eje": "operaciones", "grado": 4,
                        "prerrequisitos": ["MAT-4-MUL", "MAT-4-DIV"], "juegos": ["problemas_mult_div"], "dificultad": 4},

    # ── 4° · FRACCIONES ──
    "MAT-4-FRAC-ENTERO": {"nombre": "Concepto de fracción (parte de un entero)", "eje": "fracciones", "grado": 4,
                          "prerrequisitos": ["MAT-3-DIV"], "juegos": ["completar_entero"], "dificultad": 3},
    "MAT-4-FRAC-CANT":   {"nombre": "Fracción de una cantidad (reparto)", "eje": "fracciones", "grado": 4,
                          "prerrequisitos": ["MAT-4-FRAC-ENTERO", "MAT-4-DIV"], "juegos": ["reparto_fracciones"], "dificultad": 3},
    "MAT-4-FRAC-EQUIV":  {"nombre": "Fracciones equivalentes", "eje": "fracciones", "grado": 4,
                          "prerrequisitos": ["MAT-4-FRAC-ENTERO"], "juegos": ["fracciones_equivalentes"], "dificultad": 4},
    "MAT-4-FRAC-COMP":   {"nombre": "Comparar fracciones (cuál es más grande)", "eje": "fracciones", "grado": 4,
                          "prerrequisitos": ["MAT-4-FRAC-EQUIV"], "juegos": ["duelo_fracciones"], "dificultad": 4},

    # ── 4° · DECIMALES ──
    "MAT-4-DECIMALES": {"nombre": "Comparar decimales (décimos/centésimos)", "eje": "decimales", "grado": 4,
                        "prerrequisitos": ["MAT-4-FRAC-ENTERO"], "juegos": ["duelo_decimales"], "dificultad": 4},

    # ── 4° · MEDIDA Y DINERO ──
    "MAT-4-OFERTA":    {"nombre": "Comparar precios / mejor oferta", "eje": "medida", "grado": 4,
                        "prerrequisitos": ["MAT-4-MUL"], "juegos": ["mejor_oferta"], "dificultad": 4},

    # ── 4° · GEOMETRÍA ──
    "MAT-4-ANGULOS":   {"nombre": "Clasificar ángulos (recto/agudo/obtuso)", "eje": "geometria", "grado": 4,
                        "prerrequisitos": [], "juegos": ["angulos"], "dificultad": 2},

    # ═══════════════ 4° · LENGUA (Prácticas del Lenguaje) ═══════════════
    "LEN-4-VOCAB":       {"nombre": "Vocabulario (palabras escondidas)", "eje": "vocabulario", "grado": 4,
                          "prerrequisitos": [], "juegos": ["sopa"], "dificultad": 1},
    "LEN-4-SUSTANTIVOS": {"nombre": "Sustantivos concretos y abstractos", "eje": "gramatica", "grado": 4,
                          "prerrequisitos": [], "juegos": ["abstractos_concretos"], "dificultad": 2},
    "LEN-4-ACENTUACION": {"nombre": "Acentuación", "eje": "ortografia", "grado": 4,
                          "prerrequisitos": [], "juegos": ["acentuacion"], "dificultad": 2},
    "LEN-4-PLURALES":    {"nombre": "Plurales (z → ces)", "eje": "ortografia", "grado": 4,
                          "prerrequisitos": [], "juegos": ["plurales_z"], "dificultad": 2},
    "LEN-4-ORACION":     {"nombre": "Sujeto y predicado", "eje": "gramatica", "grado": 4,
                          "prerrequisitos": ["LEN-4-SUSTANTIVOS"], "juegos": ["sujeto_predicado"], "dificultad": 3},
    "LEN-4-MORFOLOGIA":  {"nombre": "Prefijos y sufijos", "eje": "vocabulario", "grado": 4,
                          "prerrequisitos": ["LEN-4-VOCAB"], "juegos": ["prefijos_sufijos"], "dificultad": 3},
    "LEN-4-CONECTORES":  {"nombre": "Conectores", "eje": "gramatica", "grado": 4,
                          "prerrequisitos": ["LEN-4-ORACION"], "juegos": ["conectores"], "dificultad": 3},
    "LEN-4-DIALOGO":     {"nombre": "Puntuación del diálogo (raya)", "eje": "ortografia", "grado": 4,
                          "prerrequisitos": ["LEN-4-ORACION"], "juegos": ["dialogo_raya"], "dificultad": 3},
    "LEN-4-COMPRENSION": {"nombre": "Comprensión lectora", "eje": "comprension", "grado": 4,
                          "prerrequisitos": ["LEN-4-VOCAB"], "juegos": ["comprension_lectora"], "dificultad": 3},
    "LEN-4-NARRATIVA":   {"nombre": "Ordenar el relato (secuencia narrativa)", "eje": "comprension", "grado": 4,
                          "prerrequisitos": ["LEN-4-COMPRENSION"], "juegos": ["historia_orden"], "dificultad": 4},

    # ═══════════════ 4° · CIENCIAS NATURALES ═══════════════
    "NAT-4-FOTOSINTESIS": {"nombre": "Plantas y fotosíntesis", "eje": "seres_vivos", "grado": 4,
                           "prerrequisitos": [], "juegos": ["fotosintesis"], "dificultad": 2},
    "NAT-4-ELECTRICIDAD": {"nombre": "Electricidad y circuitos", "eje": "materiales_energia", "grado": 4,
                           "prerrequisitos": [], "juegos": ["laboratorio_electrico"], "dificultad": 3},

    # ═══════════════ 4° · CIENCIAS SOCIALES ═══════════════
    "SOC-4-CRONOLOGIA": {"nombre": "Ordenar cronología (línea de tiempo)", "eje": "tiempo", "grado": 4,
                         "prerrequisitos": [], "juegos": ["linea_tiempo"], "dificultad": 2},
    "SOC-4-GEOGRAFIA":  {"nombre": "Provincias y regiones", "eje": "espacio", "grado": 4,
                         "prerrequisitos": [], "juegos": ["provincias_region"], "dificultad": 2},
    "SOC-4-HISTORIA":   {"nombre": "Pueblos originarios y la colonia", "eje": "tiempo", "grado": 4,
                         "prerrequisitos": ["SOC-4-CRONOLOGIA"], "juegos": ["historia_originarios"], "dificultad": 3},

    # ═══════════════ 5° · MATEMÁTICA ═══════════════ (verificado por consigna del menú de 5°, edad 10)
    # Los saberes de 4° son ANCLAS de 5° (asumidos dominados: el chico ya pasó 4°). Cada saber de
    # 5° tiene AL MENOS un juego real del menú de 5° que lo mide (actividades_web.py, bloque e==10).
    "MAT-5-DIV-RESTO":  {"nombre": "División con análisis del resto (c×d+r=D)", "eje": "operaciones", "grado": 5,
                         "prerrequisitos": ["MAT-4-DIV-LARGA"], "juegos": ["cuenta_larga", "dividir"], "dificultad": 4},
    "MAT-5-FRAC-EQUIV2": {"nombre": "Fracciones equivalentes avanzadas (II)", "eje": "fracciones", "grado": 5,
                         "prerrequisitos": ["MAT-4-FRAC-EQUIV"], "juegos": ["fracciones_avanzado"], "dificultad": 4},
    "MAT-5-FRAC-SUMA":  {"nombre": "Suma de fracciones (igual denominador)", "eje": "fracciones", "grado": 5,
                         "prerrequisitos": ["MAT-4-FRAC-COMP"], "juegos": ["suma_fracciones"], "dificultad": 4},
    "MAT-5-DEC-FRAC":   {"nombre": "Equivalencia decimal ↔ fracción", "eje": "decimales", "grado": 5,
                         "prerrequisitos": ["MAT-4-DECIMALES", "MAT-4-FRAC-ENTERO"], "juegos": ["decimales_fraccion"], "dificultad": 4},
    "MAT-5-RECTA-M":    {"nombre": "Recta numérica hasta 1.000.000", "eje": "numeracion", "grado": 5,
                         "prerrequisitos": ["MAT-4-RECTA"], "juegos": ["recta_numerica"], "dificultad": 3},
    "MAT-5-ANGULO-MEDIR": {"nombre": "Medir ángulos con transportador (no solo clasificar)", "eje": "geometria", "grado": 5,
                         "prerrequisitos": ["MAT-4-ANGULOS"], "juegos": ["transportador"], "dificultad": 4},
    "MAT-5-MEDIDA":     {"nombre": "Equivalencias de medida (m/cm, kg/g, l/ml)", "eje": "medida", "grado": 5,
                         "prerrequisitos": ["MAT-4-MUL"], "juegos": ["equivalencias_medida"], "dificultad": 3},
    "MAT-5-DINERO":     {"nombre": "Pago exacto y vuelto", "eje": "medida", "grado": 5,
                         "prerrequisitos": ["MAT-4-MUL"], "juegos": ["pago_exacto"], "dificultad": 3},
}

EJE_LABEL = {
    "numeracion": "Numeración", "operaciones": "Operaciones", "fracciones": "Fracciones",
    "decimales": "Decimales", "medida": "Medida y dinero", "geometria": "Geometría",
    "vocabulario": "Vocabulario", "gramatica": "Gramática", "ortografia": "Ortografía",
    "comprension": "Comprensión", "seres_vivos": "Seres vivos",
    "materiales_energia": "Materiales y energía", "tiempo": "Tiempo histórico", "espacio": "Espacio geográfico",
}


# ─────────────────────────── MOTOR (ALEKS-Lite) ───────────────────────────

def prereqs_cumplidos(saber_id, dominados):
    """True si TODOS los prerrequisitos del saber están en el set `dominados`."""
    return all(p in dominados for p in SABERES[saber_id]["prerrequisitos"])


def outer_fringe(dominados):
    """Los saberes 'listos para aprender AHORA': no dominados, con prereqs cumplidos."""
    return sorted(
        sid for sid in SABERES
        if sid not in dominados and prereqs_cumplidos(sid, dominados)
    )


def estado_saber(saber_id, dominados):
    """'dominado' | 'listo' (outer fringe) | 'pendiente' (le faltan prereqs, NO bloquea)."""
    if saber_id in dominados:
        return "dominado"
    return "listo" if prereqs_cumplidos(saber_id, dominados) else "pendiente"


def juegos_recomendados(dominados):
    """Ids de juegos que miden algún saber del outer fringe → lo que conviene ofrecer."""
    juegos = []
    for sid in outer_fringe(dominados):
        for j in SABERES[sid]["juegos"]:
            if j not in juegos:
                juegos.append(j)
    return juegos
