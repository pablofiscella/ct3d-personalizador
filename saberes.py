"""Grafo de SABERES — cimiento del motor de aprendizaje adaptativo (híbrido ALEKS+DreamBox).

PILOTO: 4° Matemática (CABA). Ver diseño en memoria `ct3d-motor-adaptativo-saberes`.

Idea (ALEKS-Lite): el conocimiento NO es "actividades completadas", es un conjunto de
SABERES dominados. Cada saber tiene prerrequisitos. El "outer fringe" = los saberes que el
chico todavía NO domina PERO cuyos prerrequisitos SÍ → eso es "lo que está listo para
aprender AHORA". Nada bloquea: un saber cuyos prereqs no están (ej. fracciones antes de
división) simplemente queda PENDIENTE mientras el motor ofrece el outer fringe. Así el chico
nunca se traba y nunca se queda sin nada apropiado — respeta el ritmo de cada escuela.

Las ACTIVIDADES (juegos de actividades_player.js) son la EVIDENCIA: cada saber lista los
juegos que lo miden/practican (ids reales de GAMES.<id>). Un juego puede medir varios saberes
y un saber puede medirse con varios juegos. Ver mapa grueso juego→categoría en
`actividades_categorias.py` (esto es la capa fina).

Cómo se combina con DreamBox: el "dominio" de un saber NO es "lo hizo", es un score que
pondera correctitud + autonomía (sin pistas) + tiempo + racha espaciada (ver
`ct3d-motor-adaptativo-saberes`), y para declararlo consolidado se exige repetición espaciada
con variantes. Eso vive en el motor de dominio (todavía no acá); este archivo es el GRAFO.

Cada saber:
  nombre           str  — visible/pedagógico
  eje              str  — agrupador temático (numeracion, operaciones, fracciones, ...)
  grado            int  — grado curricular CABA sugerido (los grado<4 son ANCLAS/raíces:
                          prerrequisitos que vienen de años anteriores)
  prerrequisitos   list — ids de otros saberes que deben estar dominados antes
  juegos           list — ids de GAMES.<id> que lo miden (evidencia)
  dificultad       int  — 1..5 (orden aproximado dentro del eje)
"""

# ── Raíces / anclas: saberes de 3° que 4° da por asumidos (prerrequisitos base) ──
# (No se enseñan en el piloto de 4°; están para que el grafo tenga raíces y el outer
#  fringe se calcule bien. En el arranque del año se verifican con una evaluación corta.)
SABERES = {
    "MAT-3-NUM": {
        "nombre": "Numeración hasta 1.000", "eje": "numeracion", "grado": 3,
        "prerrequisitos": [], "juegos": ["valor_posicional", "comparar_numeros", "ordenar_numeros"],
        "dificultad": 1,
    },
    "MAT-3-SUMARESTA": {
        "nombre": "Suma y resta hasta 3 cifras (con llevada y canje)", "eje": "operaciones", "grado": 3,
        "prerrequisitos": ["MAT-3-NUM"], "juegos": ["sumas", "restas", "suma_columnas", "resta_columnas"],
        "dificultad": 1,
    },
    "MAT-3-TABLAS": {
        "nombre": "Tablas de multiplicar (memorización)", "eje": "operaciones", "grado": 3,
        "prerrequisitos": [], "juegos": ["tablas_contrarreloj", "tabla_pitagorica"],
        "dificultad": 1,
    },
    "MAT-3-MULT": {
        "nombre": "Concepto de multiplicación", "eje": "operaciones", "grado": 3,
        "prerrequisitos": ["MAT-3-SUMARESTA", "MAT-3-TABLAS"], "juegos": ["multiplicacion_concepto", "multiplicar"],
        "dificultad": 2,
    },
    "MAT-3-DIV": {
        "nombre": "Concepto de división y reparto", "eje": "operaciones", "grado": 3,
        "prerrequisitos": ["MAT-3-MULT"], "juegos": ["reparto_con_resto"],
        "dificultad": 2,
    },

    # ── 4° · NUMERACIÓN ──
    "MAT-4-NUM-GRANDES": {
        "nombre": "Leer y escribir números grandes (10.000 y más)", "eje": "numeracion", "grado": 4,
        "prerrequisitos": ["MAT-3-NUM"], "juegos": ["bingo", "agrupar"], "dificultad": 1,
    },
    "MAT-4-VALPOS": {
        "nombre": "Valor posicional (unidad de mil, decena de mil…)", "eje": "numeracion", "grado": 4,
        "prerrequisitos": ["MAT-4-NUM-GRANDES"], "juegos": ["valor_posicional", "agrupar"], "dificultad": 2,
    },
    "MAT-4-COMPARAR": {
        "nombre": "Comparar y ordenar números grandes", "eje": "numeracion", "grado": 4,
        "prerrequisitos": ["MAT-4-NUM-GRANDES"], "juegos": ["comparar_numeros", "ordenar_numeros"], "dificultad": 2,
    },
    "MAT-4-RECTA": {
        "nombre": "Ubicar números en la recta numérica", "eje": "numeracion", "grado": 4,
        "prerrequisitos": ["MAT-4-COMPARAR"], "juegos": ["recta_numerica"], "dificultad": 2,
    },
    "MAT-4-SERIES": {
        "nombre": "Series numéricas (conteo de a saltos)", "eje": "numeracion", "grado": 4,
        "prerrequisitos": ["MAT-4-NUM-GRANDES"], "juegos": ["serie"], "dificultad": 2,
    },
    "MAT-4-PATRONES": {
        "nombre": "Patrones y regularidades", "eje": "numeracion", "grado": 4,
        "prerrequisitos": ["MAT-4-SERIES"], "juegos": ["patron"], "dificultad": 3,
    },

    # ── 4° · OPERACIONES ──
    "MAT-4-SUMARESTA": {
        "nombre": "Suma y resta de números grandes (algoritmo)", "eje": "operaciones", "grado": 4,
        "prerrequisitos": ["MAT-3-SUMARESTA", "MAT-4-VALPOS"],
        "juegos": ["suma_columnas", "sumas", "restas", "resta_columnas"], "dificultad": 2,
    },
    "MAT-4-CALCMENTAL": {
        "nombre": "Cálculo mental y estimación (suma/resta)", "eje": "operaciones", "grado": 4,
        "prerrequisitos": ["MAT-4-SUMARESTA"], "juegos": ["suma_rapida", "sumas_redondas", "mas_menos"], "dificultad": 3,
    },
    "MAT-4-MUL1": {
        "nombre": "Multiplicación por una cifra (algoritmo)", "eje": "operaciones", "grado": 4,
        "prerrequisitos": ["MAT-3-MULT", "MAT-3-TABLAS"], "juegos": ["multiplicar", "tablas_ninja"], "dificultad": 2,
    },
    "MAT-4-MUL2": {
        "nombre": "Multiplicación por dos cifras", "eje": "operaciones", "grado": 4,
        "prerrequisitos": ["MAT-4-MUL1", "MAT-4-SUMARESTA"], "juegos": ["cuenta_larga", "multiplicar"], "dificultad": 3,
    },
    "MAT-4-DIV1": {
        "nombre": "División por una cifra (exacta)", "eje": "operaciones", "grado": 4,
        "prerrequisitos": ["MAT-3-DIV", "MAT-4-MUL1"], "juegos": ["dividir"], "dificultad": 3,
    },
    "MAT-4-DIVRESTO": {
        "nombre": "División con resto", "eje": "operaciones", "grado": 4,
        "prerrequisitos": ["MAT-4-DIV1"], "juegos": ["dividir", "reparto_con_resto"], "dificultad": 4,
    },
    "MAT-4-PROB-MULDIV": {
        "nombre": "Problemas de multiplicación y división", "eje": "operaciones", "grado": 4,
        "prerrequisitos": ["MAT-4-MUL2", "MAT-4-DIVRESTO"], "juegos": ["problemas_mult_div"], "dificultad": 4,
    },
    "MAT-4-PROB-MULTI": {
        "nombre": "Problemas de varios pasos (4 operaciones)", "eje": "operaciones", "grado": 4,
        "prerrequisitos": ["MAT-4-PROB-MULDIV", "MAT-4-SUMARESTA"], "juegos": ["problemas_multipaso", "problemas_mult_div"], "dificultad": 5,
    },

    # ── 4° · FRACCIONES ──
    "MAT-4-FRAC-CONCEPTO": {
        "nombre": "Concepto de fracción (parte de un entero)", "eje": "fracciones", "grado": 4,
        "prerrequisitos": ["MAT-3-DIV"], "juegos": ["completar_entero"], "dificultad": 3,
    },
    "MAT-4-FRAC-CANT": {
        "nombre": "Fracción de una cantidad (mitad, tercio, cuarto)", "eje": "fracciones", "grado": 4,
        "prerrequisitos": ["MAT-4-FRAC-CONCEPTO", "MAT-4-DIV1"], "juegos": ["reparto_fracciones", "fraccion_de_cantidad"], "dificultad": 3,
    },
    "MAT-4-FRAC-EQUIV": {
        "nombre": "Fracciones equivalentes", "eje": "fracciones", "grado": 4,
        "prerrequisitos": ["MAT-4-FRAC-CONCEPTO"], "juegos": ["fracciones_equivalentes"], "dificultad": 4,
    },
    "MAT-4-FRAC-COMP": {
        "nombre": "Comparar fracciones (cuál es más grande)", "eje": "fracciones", "grado": 4,
        "prerrequisitos": ["MAT-4-FRAC-EQUIV"], "juegos": ["duelo_fracciones"], "dificultad": 4,
    },
    "MAT-4-FRAC-SUMA": {
        "nombre": "Suma de fracciones de igual denominador", "eje": "fracciones", "grado": 4,
        "prerrequisitos": ["MAT-4-FRAC-COMP"], "juegos": ["suma_fracciones"], "dificultad": 5,
    },

    # ── 4° · DECIMALES ──
    "MAT-4-DEC-DECIMOS": {
        "nombre": "Décimos y centésimos (concepto y escritura)", "eje": "decimales", "grado": 4,
        "prerrequisitos": ["MAT-4-FRAC-CONCEPTO", "MAT-4-VALPOS"], "juegos": ["decimales_fraccion", "duelo_decimales"], "dificultad": 4,
    },
    "MAT-4-DEC-COMP": {
        "nombre": "Comparar números decimales", "eje": "decimales", "grado": 4,
        "prerrequisitos": ["MAT-4-DEC-DECIMOS"], "juegos": ["duelo_decimales"], "dificultad": 4,
    },

    # ── 4° · MEDIDA Y DINERO ──
    "MAT-4-DINERO": {
        "nombre": "Dinero: componer montos y calcular vuelto", "eje": "medida", "grado": 4,
        "prerrequisitos": ["MAT-4-SUMARESTA", "MAT-4-DEC-DECIMOS"], "juegos": ["cajero_automatico", "pago_exacto"], "dificultad": 3,
    },
    "MAT-4-OFERTA": {
        "nombre": "Comparar precios y elegir la mejor oferta", "eje": "medida", "grado": 4,
        "prerrequisitos": ["MAT-4-DINERO", "MAT-4-MUL1"], "juegos": ["mejor_oferta"], "dificultad": 4,
    },
    "MAT-4-MEDIDA-EQUIV": {
        "nombre": "Equivalencias de medida (m/cm, kg/g, l/ml)", "eje": "medida", "grado": 4,
        "prerrequisitos": ["MAT-4-VALPOS"], "juegos": ["equivalencias_medida"], "dificultad": 3,
    },
    "MAT-4-RELOJ": {
        "nombre": "Leer la hora y calcular duraciones", "eje": "medida", "grado": 4,
        "prerrequisitos": [], "juegos": ["reloj"], "dificultad": 2,
    },

    # ── 4° · PROPORCIONALIDAD ──
    "MAT-4-PROP": {
        "nombre": "Proporcionalidad directa simple (tablas)", "eje": "proporcionalidad", "grado": 4,
        "prerrequisitos": ["MAT-4-MUL1"], "juegos": ["proporcionalidad"], "dificultad": 4,
    },

    # ── 4° · GEOMETRÍA ──
    "MAT-4-ANGULOS": {
        "nombre": "Clasificar ángulos (recto, agudo, obtuso)", "eje": "geometria", "grado": 4,
        "prerrequisitos": [], "juegos": ["angulos"], "dificultad": 2,
    },
    "MAT-4-TRANSP": {
        "nombre": "Medir ángulos con transportador", "eje": "geometria", "grado": 4,
        "prerrequisitos": ["MAT-4-ANGULOS"], "juegos": ["transportador", "suma_angulos"], "dificultad": 4,
    },

    # ── 4° · DATOS Y PROBABILIDAD ──
    "MAT-4-DATOS": {
        "nombre": "Leer e interpretar datos y gráficos", "eje": "datos", "grado": 4,
        "prerrequisitos": ["MAT-4-COMPARAR"], "juegos": ["estadistica_datos"], "dificultad": 3,
    },
    "MAT-4-PROB": {
        "nombre": "Probabilidad simple (seguro, posible, imposible)", "eje": "datos", "grado": 4,
        "prerrequisitos": [], "juegos": ["probabilidad_sucesos", "arbol_probabilidad"], "dificultad": 3,
    },
}

EJE_LABEL = {
    "numeracion": "Numeración", "operaciones": "Operaciones", "fracciones": "Fracciones",
    "decimales": "Decimales", "medida": "Medida y dinero", "proporcionalidad": "Proporcionalidad",
    "geometria": "Geometría", "datos": "Datos y probabilidad",
}


# ─────────────────────────── MOTOR (ALEKS-Lite) ───────────────────────────

def prereqs_cumplidos(saber_id, dominados):
    """True si TODOS los prerrequisitos del saber están en el set `dominados`."""
    return all(p in dominados for p in SABERES[saber_id]["prerrequisitos"])


def outer_fringe(dominados):
    """Los saberes 'listos para aprender AHORA': no dominados, con prereqs cumplidos.
    Este es el corazón del motor — nunca ofrece algo cuyos prereqs no estén, y nunca
    deja al chico sin nada (mientras quede algo por aprender, el fringe no está vacío
    salvo que todo lo alcanzable esté dominado)."""
    return sorted(
        sid for sid in SABERES
        if sid not in dominados and prereqs_cumplidos(sid, dominados)
    )


def estado_saber(saber_id, dominados):
    """Estado visual de un saber para un chico:
       'dominado'  → ya lo sabe
       'listo'     → outer fringe (recomendado / disponible en verde)
       'pendiente' → le faltan prereqs (queda en espera, NO bloquea nada más)."""
    if saber_id in dominados:
        return "dominado"
    return "listo" if prereqs_cumplidos(saber_id, dominados) else "pendiente"


def juegos_recomendados(dominados):
    """Ids de juegos que miden algún saber del outer fringe → lo que conviene ofrecerle."""
    juegos = []
    for sid in outer_fringe(dominados):
        for j in SABERES[sid]["juegos"]:
            if j not in juegos:
                juegos.append(j)
    return juegos
