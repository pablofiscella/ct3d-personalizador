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

    # ═══════════════ 5° · LENGUA ═══════════════
    "LEN-5-SINTAXIS":   {"nombre": "Análisis sintáctico (núcleo del sujeto/predicado)", "eje": "gramatica", "grado": 5,
                         "prerrequisitos": ["LEN-4-ORACION"], "juegos": ["analisis_sintactico"], "dificultad": 4},
    "LEN-5-VERBOS":     {"nombre": "Tiempos verbales del pasado (cantó / cantaba)", "eje": "gramatica", "grado": 5,
                         "prerrequisitos": ["LEN-4-ORACION"], "juegos": ["verbos_pasado"], "dificultad": 3},
    "LEN-5-COMPRENSION": {"nombre": "Comprensión de textos más largos (inferencia)", "eje": "comprension", "grado": 5,
                         "prerrequisitos": ["LEN-4-COMPRENSION"], "juegos": ["comprension_lectora"], "dificultad": 3},

    # ═══════════════ 5° · CIENCIAS NATURALES ═══════════════
    "NAT-5-DIGESTIVO":  {"nombre": "Sistema digestivo", "eje": "seres_vivos", "grado": 5,
                         "prerrequisitos": [], "juegos": ["camino_digestivo"], "dificultad": 3},
    "NAT-5-AGUA":       {"nombre": "Potabilización del agua", "eje": "materiales_energia", "grado": 5,
                         "prerrequisitos": [], "juegos": ["planta_potabilizadora"], "dificultad": 3},
    "NAT-5-ASTRO":      {"nombre": "Astronomía (Sol, Luna, cielo)", "eje": "seres_vivos", "grado": 5,
                         "prerrequisitos": [], "juegos": ["detectives_cielo"], "dificultad": 3},

    # ═══════════════ 5° · CIENCIAS SOCIALES ═══════════════
    "SOC-5-COLONIAL":   {"nombre": "Vida colonial (Virreinato)", "eje": "tiempo", "grado": 5,
                         "prerrequisitos": ["SOC-4-HISTORIA"], "juegos": ["trivia_colonial"], "dificultad": 3},
    "SOC-5-INDEPENDENCIA": {"nombre": "Camino a la independencia (1810-1853)", "eje": "tiempo", "grado": 5,
                         "prerrequisitos": ["SOC-5-COLONIAL"], "juegos": ["independencia_arg"], "dificultad": 4},
    "SOC-5-ECONOMIA":   {"nombre": "Actividades económicas por región", "eje": "espacio", "grado": 5,
                         "prerrequisitos": ["SOC-4-GEOGRAFIA"], "juegos": ["actividad_economica"], "dificultad": 3},
    "SOC-5-CONSTITUCION": {"nombre": "Derechos y Constitución", "eje": "tiempo", "grado": 5,
                         "prerrequisitos": ["SOC-5-INDEPENDENCIA"], "juegos": ["derechos_constitucion"], "dificultad": 4},
    "SOC-5-BSAS":       {"nombre": "Historia de Buenos Aires", "eje": "espacio", "grado": 5,
                         "prerrequisitos": ["SOC-5-COLONIAL"], "juegos": ["buenos_aires"], "dificultad": 3},

    # ═══════════════ 6° · MATEMÁTICA ═══════════════ (menú e==11)
    "MAT-6-PRIMOS":     {"nombre": "Números primos y divisibilidad", "eje": "numeracion", "grado": 6,
                         "prerrequisitos": ["MAT-4-MUL"], "juegos": ["numeros_primos"], "dificultad": 4},
    "MAT-6-JERARQUIA":  {"nombre": "Jerarquía de operaciones", "eje": "operaciones", "grado": 6,
                         "prerrequisitos": ["MAT-4-MUL", "MAT-4-DIV"], "juegos": ["jerarquia_operaciones"], "dificultad": 4},
    "MAT-6-FRAC-CANT":  {"nombre": "Fracción de una cantidad (avanzado)", "eje": "fracciones", "grado": 6,
                         "prerrequisitos": ["MAT-4-FRAC-CANT"], "juegos": ["fraccion_de_cantidad"], "dificultad": 4},
    "MAT-6-FRAC-MULT":  {"nombre": "Multiplicación de fracciones", "eje": "fracciones", "grado": 6,
                         "prerrequisitos": ["MAT-5-FRAC-SUMA"], "juegos": ["multiplicar_fracciones"], "dificultad": 5},
    "MAT-6-PORCENTAJE": {"nombre": "Porcentajes", "eje": "decimales", "grado": 6,
                         "prerrequisitos": ["MAT-5-DEC-FRAC"], "juegos": ["porcentajes"], "dificultad": 5},
    "MAT-6-POLIGONOS":  {"nombre": "Polígonos y sus lados", "eje": "geometria", "grado": 6,
                         "prerrequisitos": ["MAT-4-ANGULOS"], "juegos": ["poligonos_lados"], "dificultad": 3},
    "MAT-6-CUADRILATEROS": {"nombre": "Clasificar cuadriláteros", "eje": "geometria", "grado": 6,
                         "prerrequisitos": ["MAT-6-POLIGONOS"], "juegos": ["cuadrilateros"], "dificultad": 4},
    "MAT-6-SUMA-ANGULOS": {"nombre": "Suma de ángulos (triángulo/cuadrilátero)", "eje": "geometria", "grado": 6,
                         "prerrequisitos": ["MAT-5-ANGULO-MEDIR"], "juegos": ["suma_angulos"], "dificultad": 4},
    "MAT-6-PROBABILIDAD": {"nombre": "Probabilidad de sucesos", "eje": "datos", "grado": 6,
                         "prerrequisitos": ["MAT-4-FRAC-ENTERO"], "juegos": ["probabilidad_sucesos", "arbol_probabilidad"], "dificultad": 4},

    # ═══════════════ 6° · LENGUA ═══════════════
    "LEN-6-HECHOS":     {"nombre": "Distinguir hechos de opiniones", "eje": "comprension", "grado": 6,
                         "prerrequisitos": ["LEN-5-COMPRENSION"], "juegos": ["hechos_opiniones"], "dificultad": 4},

    # ═══════════════ 6° · CIENCIAS NATURALES ═══════════════
    "NAT-6-CELULA":     {"nombre": "La célula y sus partes", "eje": "seres_vivos", "grado": 6,
                         "prerrequisitos": [], "juegos": ["celula_partes"], "dificultad": 4},
    "NAT-6-NERVIOSO":   {"nombre": "Sistema nervioso", "eje": "seres_vivos", "grado": 6,
                         "prerrequisitos": ["NAT-5-DIGESTIVO"], "juegos": ["sistema_nervioso"], "dificultad": 4},
    "NAT-6-PUBERTAD":   {"nombre": "Pubertad y cambios del cuerpo", "eje": "seres_vivos", "grado": 6,
                         "prerrequisitos": [], "juegos": ["pubertad"], "dificultad": 3},
    "NAT-6-ENERGIA":    {"nombre": "Energías renovables", "eje": "materiales_energia", "grado": 6,
                         "prerrequisitos": [], "juegos": ["energia_renovable"], "dificultad": 3},

    # ═══════════════ 6° · CIENCIAS SOCIALES ═══════════════
    "SOC-6-ORGANIZACION": {"nombre": "Organización nacional (1853-1880)", "eje": "tiempo", "grado": 6,
                         "prerrequisitos": ["SOC-5-INDEPENDENCIA"], "juegos": ["organizacion_nacional"], "dificultad": 4},
    "SOC-6-INMIGRACION": {"nombre": "La gran inmigración", "eje": "tiempo", "grado": 6,
                         "prerrequisitos": ["SOC-6-ORGANIZACION"], "juegos": ["viaje_inmigrante"], "dificultad": 4},
    "SOC-6-SUFRAGIO":   {"nombre": "Sufragio y ley Sáenz Peña", "eje": "tiempo", "grado": 6,
                         "prerrequisitos": ["SOC-5-CONSTITUCION"], "juegos": ["sufragio_argentina"], "dificultad": 4},

    # ═══════════════ 7° · MATEMÁTICA ═══════════════ (menú e==12)
    "MAT-7-POTENCIAS":  {"nombre": "Potencias y raíces", "eje": "operaciones", "grado": 7,
                         "prerrequisitos": ["MAT-4-MUL"], "juegos": ["potencias"], "dificultad": 5},
    "MAT-7-ECUACIONES": {"nombre": "Ecuaciones simples (x)", "eje": "operaciones", "grado": 7,
                         "prerrequisitos": ["MAT-6-JERARQUIA"], "juegos": ["ecuaciones_simples"], "dificultad": 5},
    "MAT-7-ALGEBRA":    {"nombre": "Lenguaje algebraico (traducir)", "eje": "operaciones", "grado": 7,
                         "prerrequisitos": ["MAT-7-ECUACIONES"], "juegos": ["traductor_algebraico"], "dificultad": 5},
    "MAT-7-PROPORCION": {"nombre": "Proporcionalidad directa", "eje": "decimales", "grado": 7,
                         "prerrequisitos": ["MAT-6-PORCENTAJE"], "juegos": ["proporcionalidad"], "dificultad": 5},
    "MAT-7-AREA":       {"nombre": "Área y perímetro", "eje": "geometria", "grado": 7,
                         "prerrequisitos": ["MAT-6-POLIGONOS"], "juegos": ["area_perimetro"], "dificultad": 4},
    "MAT-7-ESTADISTICA": {"nombre": "Estadística (media, gráficos)", "eje": "datos", "grado": 7,
                         "prerrequisitos": ["MAT-6-PROBABILIDAD"], "juegos": ["estadistica_datos"], "dificultad": 4},
    "MAT-7-PROBLEMAS":  {"nombre": "Problemas de varios pasos", "eje": "operaciones", "grado": 7,
                         "prerrequisitos": ["MAT-6-JERARQUIA"], "juegos": ["problemas_multipaso"], "dificultad": 5},

    # ═══════════════ 7° · LENGUA ═══════════════
    "LEN-7-ORTOGRAFIA": {"nombre": "Cazador de errores ortográficos", "eje": "ortografia", "grado": 7,
                         "prerrequisitos": ["LEN-4-ACENTUACION"], "juegos": ["cazador_errores"], "dificultad": 4},
    "LEN-7-HOMOFONOS":  {"nombre": "Homófonos (haber/a ver, hay/ahí)", "eje": "ortografia", "grado": 7,
                         "prerrequisitos": ["LEN-4-ACENTUACION"], "juegos": ["homofonos"], "dificultad": 5},
    "LEN-7-INGLES":     {"nombre": "Inglés básico (vocabulario)", "eje": "vocabulario", "grado": 7,
                         "prerrequisitos": [], "juegos": ["ingles_basico"], "dificultad": 3},

    # ═══════════════ 7° · CIENCIAS NATURALES ═══════════════
    "NAT-7-CEREBRO":    {"nombre": "Cerebro y defensas del cuerpo", "eje": "seres_vivos", "grado": 7,
                         "prerrequisitos": ["NAT-6-NERVIOSO"], "juegos": ["cerebro_defensas"], "dificultad": 4},
    "NAT-7-REPRODUCTOR": {"nombre": "Sistema reproductor", "eje": "seres_vivos", "grado": 7,
                         "prerrequisitos": ["NAT-6-PUBERTAD"], "juegos": ["sistema_reproductor"], "dificultad": 4},
    "NAT-7-TROFICA":    {"nombre": "Redes tróficas (ecosistemas)", "eje": "seres_vivos", "grado": 7,
                         "prerrequisitos": ["NAT-4-FOTOSINTESIS"], "juegos": ["red_trofica"], "dificultad": 4},
    "NAT-7-PLANETAS":   {"nombre": "El sistema solar (tipos de planetas)", "eje": "seres_vivos", "grado": 7,
                         "prerrequisitos": ["NAT-5-ASTRO"], "juegos": ["planetas_tipo"], "dificultad": 3},

    # ═══════════════ 7° · CIENCIAS SOCIALES ═══════════════
    "SOC-7-DEMOCRACIA": {"nombre": "Democracia y vida en democracia (1983→)", "eje": "tiempo", "grado": 7,
                         "prerrequisitos": ["SOC-6-SUFRAGIO"], "juegos": ["linea_democracia"], "dificultad": 4},
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
