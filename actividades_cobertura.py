# -*- coding: utf-8 -*-
"""Manifiesto de COBERTURA CURRICULAR: qué temas pide el Diseño Curricular en cada
grado y qué actividad los cubre.

Por qué existe (25-jul-2026, pedido de Pablo): el cuaderno escolar de 4° salía con 42
tarjetas y parecía completo, pero cubría **29 de los 58 temas** que la auditoría del DC
CABA le fijó al año. Faltaba Ciencias Naturales casi entera (1 de 8) y las tres
transversales. Eso no se ve mirando el menú: se ve cruzándolo contra la currícula.

La regla, y es la que manda para construir los otros grados:

    TODO tema del DC del grado tiene que tener una actividad, Y tiene que estar en el
    NIVEL 1 (el que el chico ve sin pagar ni desbloquear nada).

Los niveles 2 y 3 son escalones de DIFICULTAD del mismo tema, no temas distintos: un
tema del año no puede vivir detrás de un candado. Los comodines lúdicos (memotest,
laberinto, sopa, sudoku…) van ARRIBA de los 58: son descanso, no currícula, y por eso
no figuran acá.

Cómo se usa:

    python3 -c "import actividades_cobertura as c; c.informe(4)"   # ver el estado
    pytest tests/test_cobertura_dc.py                              # que falle si falta

El manifiesto sale de `docs/auditoria-dc-caba/grado-N.md`, que es la fuente autorizada
(auditoría de 62 agentes contra el DC CABA 2024 + panel docente). Cada tema cita su
código en ese documento para poder volver a la especificación completa: mecánica,
banco, rampa de dificultad y contenido del DC.

Un grado sin entrada acá NO está auditado todavía; el test lo saltea en vez de fallar,
así que agregar un grado nuevo es agregar su lista y dejar que el test diga qué falta.
"""

# ── Estructura de un tema ────────────────────────────────────────────────────────
#   cod   : código en la auditoría (M1, L7, N3…). Ancla a la especificación completa.
#   area  : matematica | lengua | naturales | sociales | tecnologia | transversal
#   tema  : nombre corto y humano
#   dc    : el contenido del Diseño Curricular que cubre
#   cubre : id de la actividad que lo cubre, o None si falta construirla
#   deuda : (opcional) está cubierto pero incompleto — qué le falta
#   previsto : (opcional) el id que VA a tener cuando se construya. Sirve para dejar el
#              plan escrito sin declarar como cubierto algo que todavía no existe: un id
#              en `cubre` que no está en el menú es un error (typo), no un pendiente.
#
# `cubre` puede ser una lista cuando el tema se reparte en más de una tarjeta.

GRADO_4 = [
    # ── Matemática (19) ──────────────────────────────────────────────────────────
    {"cod": "M1",  "area": "matematica", "tema": "Recta numérica gigante",
     "dc": "Ubicación en la recta; orden en rangos de 10.000 y 100.000",
     "cubre": "recta_numerica"},
    {"cod": "M2",  "area": "matematica", "tema": "Armá el número",
     "dc": "Valor posicional; composición y descomposición aditiva y multiplicativa",
     "cubre": "valor_posicional_4"},
    {"cod": "M3",  "area": "matematica", "tema": "Suma con cifras grandes",
     "dc": "Algoritmo de suma analizado; cálculo aproximado",
     "cubre": "suma_columnas"},
    {"cod": "M4",  "area": "matematica", "tema": "Resta con canje",
     "dc": "Algoritmo de resta analizado en rangos de 10.000 y 100.000",
     "cubre": "resta_canje_4"},
    {"cod": "M5",  "area": "matematica", "tema": "Fábrica de multiplicar",
     "dc": "×10/×100/×1.000; estimación; algoritmo por dos cifras",
     "cubre": "multiplicar"},
    {"cod": "M6",  "area": "matematica", "tema": "La división por partes",
     "dc": "Tabla pitagórica; algoritmo intermedio por aproximaciones",
     "cubre": ["dividir", "cuenta_larga"]},
    {"cod": "M7",  "area": "matematica", "tema": "Problemas de varios pasos",
     "dc": "Problemas de dos pasos; datos e incógnitas; análisis del resto",
     "cubre": "problemas_mult_div"},
    {"cod": "M8",  "area": "matematica", "tema": "Reparto justo",
     "dc": "Fracciones en el reparto (resultado de la división) y en la medida",
     "cubre": "reparto_fracciones"},
    {"cod": "M9",  "area": "matematica", "tema": "Litros y kilos",
     "dc": "1/2, 1/4 y 3/4 con litros y kilos; qué falta para el entero",
     "cubre": "completar_entero"},
    {"cod": "M10", "area": "matematica", "tema": "Duelo de fracciones",
     "dc": "Comparación de fracciones de igual denominador; mayores y menores que el entero",
     "cubre": "duelo_fracciones"},
    {"cod": "M11", "area": "matematica", "tema": "Balanza y precios",
     "dc": "Decimales en uso social: precios y medidas; comparación; suma y resta no algorítmica",
     "cubre": "duelo_decimales"},
    {"cod": "M12", "area": "matematica", "tema": "La mejor oferta",
     "dc": "Proporcionalidad directa; valor unitario; oferta conveniente (Ed. Financiera)",
     "cubre": "mejor_oferta"},
    {"cod": "M13", "area": "matematica", "tema": "¿Se arma el triángulo?",
     "dc": "Construcción de triángulos dados los lados; clasificación; desigualdad triangular",
     "cubre": "triangulos_4"},
    {"cod": "M14", "area": "matematica", "tema": "Caras y cuerpos",
     "dc": "Cubos y prismas: caras y figuras; circunferencia y círculo",
     "cubre": "cuerpos_caras_4"},
    {"cod": "M15", "area": "matematica", "tema": "Medí el ángulo",
     "dc": "Clasificación agudo/recto/obtuso; el transportador; el grado; giros",
     "cubre": "angulos"},
    {"cod": "M16", "area": "matematica", "tema": "Emparejar medidas",
     "dc": "Equivalencias km-m-cm-mm; kg-g-tonelada",
     "cubre": "equivalencias_medida_4"},
    {"cod": "M17", "area": "matematica", "tema": "Tablas ninja",
     "dc": "Repertorio multiplicativo a partir de la tabla pitagórica",
     "cubre": "tablas_ninja"},
    {"cod": "M18", "area": "matematica", "tema": "La serie numérica",
     "dc": "Regularidades de la serie numérica hasta 100.000",
     "cubre": "serie"},
    {"cod": "M19", "area": "matematica", "tema": "Fracciones equivalentes",
     "dc": "Equivalencia de fracciones (ampliación del DC)",
     "cubre": "fracciones_equivalentes"},

    # ── Lengua (17) ──────────────────────────────────────────────────────────────
    {"cod": "L1",  "area": "lengua", "tema": "Clasificador de tildes",
     "dc": "Agudas, graves y esdrújulas: sílaba tónica, clasificación y regla de tilde",
     "cubre": "acentuacion"},
    {"cod": "L2",  "area": "lengua", "tema": "Sujeto y predicado",
     "dc": "Sujeto y predicado en oraciones simples; sujeto tácito",
     "cubre": "sujeto_predicado"},
    {"cod": "L3",  "area": "lengua", "tema": "El conector justo",
     "dc": "Conectores copulativos, disyuntivos, temporales y adversativos",
     "cubre": "conectores"},
    {"cod": "L4",  "area": "lengua", "tema": "¿Qué clase de palabra?",
     "dc": "Sustantivos propios y comunes; adjetivos calificativos y gentilicios",
     "cubre": "clases_palabra_4"},
    {"cod": "L5",  "area": "lengua", "tema": "Máquina del tiempo verbal",
     "dc": "Presente, pretérito perfecto simple e imperfecto; narrar en pasado",
     "cubre": "tiempos_verbales_4"},
    {"cod": "L6",  "area": "lengua", "tema": "Fábrica de palabras",
     "dc": "Prefijos y sufijos frecuentes; inferencia de significado",
     "cubre": "prefijos_sufijos"},
    {"cod": "L7",  "area": "lengua", "tema": "Hiperónimo e hipónimo",
     "dc": "Cohesión léxica: hiperónimos, hipónimos y sinonimia",
     "cubre": "hiperonimos_4"},
    {"cod": "L8",  "area": "lengua", "tema": "¿Ola u hola?",
     "dc": "Homófonos heterógrafos",
     "cubre": "homofonos_4"},
    {"cod": "L9",  "area": "lengua", "tema": "Completá el grupo que falta",
     "dc": "Regularidades ortográficas: hue-, bue-, bur-, bus-, -aje, -bilidad",
     "cubre": "grupos_ortograficos_4"},
    {"cod": "L10", "area": "lengua", "tema": "Luz, luces, lucecita",
     "dc": "Plurales y diminutivos de palabras terminadas en -z",
     "cubre": "plurales_z"},
    {"cod": "L11", "area": "lengua", "tema": "¿Mito, leyenda o los dos?",
     "dc": "Mitos y leyendas: estructura, semejanzas y diferencias",
     "cubre": "mito_leyenda_4"},
    {"cod": "L12", "area": "lengua", "tema": "Detective del paratexto",
     "dc": "Índice, glosario, títulos y epígrafes; su relación con el contenido",
     "cubre": "paratexto_4"},
    {"cod": "L13", "area": "lengua", "tema": "¿Para qué se escribió?",
     "dc": "Propósito comunicativo: informar, narrar, describir, indicar, argumentar",
     "cubre": "proposito_texto_4"},
    {"cod": "L14", "area": "lengua", "tema": "Armá el diálogo",
     "dc": "Diálogos con marco narrativo, alternancia y raya de diálogo",
     "cubre": "dialogo_raya"},
    {"cod": "L15", "area": "lengua", "tema": "Historia en orden",
     "dc": "Situación inicial, conflicto y resolución; causa y consecuencia",
     "cubre": "historia_orden"},
    {"cod": "L16", "area": "lengua", "tema": "¡Boom! Onomatopeyas",
     "dc": "La historieta: onomatopeyas y aspectos gráficos",
     "cubre": "historieta_4"},
    {"cod": "L17", "area": "lengua", "tema": "Detective de textos",
     "dc": "Reponer información implícita; causa y consecuencia en textos",
     "cubre": "comprension_lectora"},

    # ── Ciencias Naturales (8) ───────────────────────────────────────────────────
    {"cod": "N1",  "area": "naturales", "tema": "Modelador de paisaje",
     "dc": "Erosión, transporte y depósito",
     "cubre": "erosion_4"},
    {"cod": "N2",  "area": "naturales", "tema": "Placas en movimiento",
     "dc": "Tectónica de placas; bordes activos; formación del relieve",
     "cubre": "placas_4"},
    {"cod": "N3",  "area": "naturales", "tema": "Huellas del tiempo",
     "dc": "Fósiles; escala de tiempo geológico frente a la humana",
     "cubre": "fosiles_4"},
    {"cod": "N4",  "area": "naturales", "tema": "Armá el movimiento",
     "dc": "Sistema osteo-artro-muscular: huesos, músculos y articulaciones",
     "cubre": "movimiento_cuerpo_4"},
    {"cod": "N5",  "area": "naturales", "tema": "Laboratorio de imanes",
     "dc": "Magnetismo: dos polos, atracción y repulsión; electrostática",
     "cubre": "imanes_4"},
    {"cod": "N6",  "area": "naturales", "tema": "Armá el circuito",
     "dc": "Circuito eléctrico simple: generador, conductor, disipador, interruptor",
     "cubre": "laboratorio_electrico"},
    {"cod": "N7",  "area": "naturales", "tema": "Objeto o material",
     "dc": "Natural y artificial; objeto no es material; propiedades y usos",
     "cubre": "objeto_material_4"},
    {"cod": "N8",  "area": "naturales", "tema": "El cielo de Buenos Aires",
     "dc": "Movimiento diario del Sol; día y noche; sombras y estaciones",
     "cubre": "cielo_4"},

    # ── Ciencias Sociales (8) ────────────────────────────────────────────────────
    {"cod": "S1",  "area": "sociales", "tema": "Los primeros pueblos",
     "dc": "Caza-recolección y domesticación; nómades y sedentarios",
     "cubre": "historia_originarios"},
    {"cod": "S2",  "area": "sociales", "tema": "América antes de 1492",
     "dc": "Incas y aztecas; tributos y tecnologías; cultivos americanos",
     "cubre": "america_1492_4"},
    {"cod": "S3",  "area": "sociales", "tema": "Línea de tiempo colonial",
     "dc": "Conquista; las dos fundaciones de Buenos Aires; los virreinatos",
     "cubre": "linea_tiempo"},
    {"cod": "S4",  "area": "sociales", "tema": "La sociedad colonial",
     "dc": "Sectores de la sociedad colonial: derechos y obligaciones",
     "cubre": "sociedad_colonial_4"},
    {"cod": "S5",  "area": "sociales", "tema": "Ambientes argentinos",
     "dc": "Ambientes: montaña, llanura y meseta",
     "cubre": "ambientes_4"},
    {"cod": "S6",  "area": "sociales", "tema": "Urbano, rural o periurbano",
     "dc": "Espacios urbanos, rurales y periurbanos; articulación y servicios",
     "cubre": "urbano_rural_4"},
    {"cod": "S7",  "area": "sociales", "tema": "¿Quién se ocupa?",
     "dc": "Niveles de gobierno; CABA autónoma y comunas; servicios e impuestos",
     "cubre": "gobierno_argentina"},
    {"cod": "S8",  "area": "sociales", "tema": "Provincias, regiones y capitales",
     "dc": "División jurídico-político-administrativa; extensión y límites",
     "cubre": "provincias_region",
     "deuda": "el banco tiene 4 regiones y ninguna capital; la auditoría pide 24 "
              "jurisdicciones, las 5 regiones y las 24 capitales"},

    # ── Tecnología, Diseño y Programación (3) ────────────────────────────────────
    {"cod": "T1",  "area": "tecnologia", "tema": "Robot por bloques",
     "dc": "Iteraciones y ciclos; creación y depuración iterativa",
     "cubre": "programar_camino"},
    {"cod": "T2",  "area": "tecnologia", "tema": "Mecanismos y energía",
     "dc": "Bielas, manivelas y levas; conversiones de energía; motor, transmisión y efector",
     "cubre": "mecanismos_4"},
    {"cod": "T3",  "area": "tecnologia", "tema": "Detectives digitales",
     "dc": "IA en aplicaciones cotidianas; confiabilidad y procedencia de las fuentes",
     "cubre": "fuentes_digitales_4"},

    # ── Transversales (3) ────────────────────────────────────────────────────────
    {"cod": "X1",  "area": "transversal", "tema": "Separá en origen",
     "dc": "Ed. Ambiental: corrientes de residuos, separación en origen, compostaje",
     "cubre": "residuos_4"},
    {"cod": "X2",  "area": "transversal", "tema": "¿Necesidad o deseo?",
     "dc": "Ed. Financiera: necesidades y deseos; ahorro = ingreso − gasto",
     "cubre": "necesidad_deseo_4"},
    {"cod": "X3",  "area": "transversal", "tema": "Semáforo de la convivencia",
     "dc": "ESI: diálogo ante burlas y exclusiones; a quiénes acudir; huella digital",
     "cubre": "convivencia_4"},
]

GRADO_5 = [
    # ── Matemática (18) ──────────────────────────────────────────────────────────
    {"cod": "M1",  "area": "matematica", "tema": "Recta del millón",
     "dc": "Lectura, escritura y orden en el rango del millón; valor posicional",
     "cubre": "recta_numerica",
     "deuda": "el banco es el de 4° (hasta 100.000); la auditoría de 5° pide llegar al "
              "millón y 7 cifras sin rotular"},
    {"cod": "M2",  "area": "matematica", "tema": "Traductor romano",
     "dc": "Sistema romano: diferencias con el decimal (posicionalidad, el cero)",
     "cubre": None, "previsto": "romanos_5"},
    {"cod": "M3",  "area": "matematica", "tema": "Misiones de varios pasos",
     "dc": "Problemas de varios pasos con las cuatro operaciones; tratamiento de la información",
     "cubre": None, "previsto": "problemas_pasos_5"},
    {"cod": "M4",  "area": "matematica", "tema": "Combinador de conjuntos",
     "dc": "Combinatoria; pasaje a la escritura multiplicativa",
     "cubre": None, "previsto": "combinatoria_5"},
    {"cod": "M5",  "area": "matematica", "tema": "La cuenta escondida",
     "dc": "Relación c×d+r=D con r<d; análisis del resto",
     "cubre": None, "previsto": "cuenta_escondida_5"},
    {"cod": "M6",  "area": "matematica", "tema": "Cazamúltiplos",
     "dc": "Divisibilidad: múltiplos, divisores y descomposición multiplicativa",
     "cubre": None, "previsto": "divisibilidad_5"},
    {"cod": "M7",  "area": "matematica", "tema": "División por aproximaciones",
     "dc": "Algoritmos intermedios de la división; anticipar las cifras del cociente",
     "cubre": ["dividir", "cuenta_larga"]},
    {"cod": "M8",  "area": "matematica", "tema": "Duelo de fracciones",
     "dc": "Comparación contra el entero y contra 1/2; equivalencias",
     "cubre": ["duelo_fracciones", "fracciones_avanzado"]},
    {"cod": "M9",  "area": "matematica", "tema": "Reconstruí el entero",
     "dc": "Reconstrucción de la unidad; fracción de un número natural",
     "cubre": None, "previsto": "reconstruir_entero_5"},
    {"cod": "M10", "area": "matematica", "tema": "Panadería de fracciones",
     "dc": "Suma y resta de medios, cuartos y octavos; la fracción como operador",
     "cubre": "suma_fracciones"},
    {"cod": "M11", "area": "matematica", "tema": "Del décimo a la coma",
     "dc": "Equivalencia entre fracción decimal y expresión decimal",
     "cubre": "decimales_fraccion"},
    {"cod": "M12", "area": "matematica", "tema": "Cajero con coma",
     "dc": "Suma y resta de decimales con anticipación; natural por decimal",
     "cubre": "pago_exacto"},
    {"cod": "M13", "area": "matematica", "tema": "¿Proporcional o no?",
     "dc": "Proporcionalidad directa; distinguir lo proporcional de lo que no lo es",
     "cubre": None, "previsto": "proporcionalidad_5"},
    {"cod": "M14", "area": "matematica", "tema": "Geometría constructiva",
     "dc": "Desigualdad triangular; suma de ángulos; desarrollos planos; medir ángulos",
     "cubre": "transportador",
     "deuda": "sólo está el modo de lectura del transportador; faltan la desigualdad "
              "triangular y los desarrollos planos de cuerpos"},
    {"cod": "M15", "area": "matematica", "tema": "Perímetro y área",
     "dc": "Fórmulas de perímetro; área con unidades no convencionales",
     "cubre": None, "previsto": "perimetro_area_5"},
    {"cod": "M16", "area": "matematica", "tema": "Encuesta y gráfico",
     "dc": "Tablas de frecuencias; gráficos de barras y circulares",
     "cubre": None, "previsto": "graficos_5"},
    {"cod": "M17", "area": "matematica", "tema": "Equivalencias de medida",
     "dc": "Unidades convencionales y equivalencias combinadas con decimales",
     "cubre": "equivalencias_medida"},
    {"cod": "M18", "area": "matematica", "tema": "Fluidez de tablas y cálculo",
     "dc": "Repertorio multiplicativo y cálculo mental como base de la división",
     "cubre": "tablas_ninja"},

    # ── Lengua (16) ──────────────────────────────────────────────────────────────
    {"cod": "L1",  "area": "lengua", "tema": "Club de lectura",
     "dc": "Inferencias; correferencia; información relevante en textos de varios géneros",
     "cubre": "comprension_lectora",
     "deuda": "la auditoría pide 30 textos × 5 preguntas y géneros completos (fantástico, "
              "humor, noticia, teatro breve, poema)"},
    {"cod": "L2",  "area": "lengua", "tema": "Recursos poéticos",
     "dc": "Personificación, comparación y metáfora; rima asonante y consonante",
     "cubre": None, "previsto": "recursos_poeticos_5"},
    {"cod": "L3",  "area": "lengua", "tema": "Verbos en tres cajas",
     "dc": "Verbos de acción, de estado y psicológicos",
     "cubre": None, "previsto": "verbos_clases_5"},
    {"cod": "L4",  "area": "lengua", "tema": "¿Objeto directo o indirecto?",
     "dc": "Objeto directo e indirecto; prueba de sustitución por lo/le",
     "cubre": None, "previsto": "od_oi_5"},
    {"cod": "L5",  "area": "lengua", "tema": "Grados del adjetivo",
     "dc": "Comparativo y superlativo",
     "cubre": None, "previsto": "grados_adjetivo_5"},
    {"cod": "L6",  "area": "lengua", "tema": "Futuro o condicional",
     "dc": "Futuro y condicional; perífrasis 'voy a + infinitivo'",
     "cubre": None, "previsto": "futuro_condicional_5"},
    {"cod": "L7",  "area": "lengua", "tema": "Vaya, valla o baya",
     "dc": "Homófonos heterógrafos: ay/hay, casar/cazar, vaya/valla/baya",
     "cubre": None, "previsto": "homofonos_5"},
    {"cod": "L8",  "area": "lengua", "tema": "Acentuación y tilde diacrítica",
     "dc": "Acentuación general, tilde diacrítica (qué/que, él/el, mí/mi) y -mente",
     "cubre": None, "previsto": "acentuacion_5"},
    {"cod": "L9",  "area": "lengua", "tema": "Prefijos poderosos",
     "dc": "Prefijos in-, des-, micro-, sub-, anti-",
     "cubre": None, "previsto": "prefijos_5"},
    {"cod": "L10", "area": "lengua", "tema": "Una palabra, varios sentidos",
     "dc": "Polisemia; la acepción según el contexto",
     "cubre": None, "previsto": "polisemia_5"},
    {"cod": "L11", "area": "lengua", "tema": "Arquitecto de textos",
     "dc": "Estructura de la carta y el mail, la entrevista y la noticia",
     "cubre": None, "previsto": "estructura_textos_5"},
    {"cod": "L12", "area": "lengua", "tema": "Dos puntos y raya",
     "dc": "Dos puntos en el discurso directo; voz del narrador frente al diálogo",
     "cubre": None, "previsto": "dos_puntos_5"},
    {"cod": "L13", "area": "lengua", "tema": "¿Opinión o argumento?",
     "dc": "Textos argumentativos: notas de opinión y publicidades",
     "cubre": None, "previsto": "opinion_argumento_5"},
    {"cod": "L14", "area": "lengua", "tema": "Sujeto y predicado completos",
     "dc": "Sujeto y predicado con sus núcleos en oraciones extensas",
     "cubre": ["sujeto_predicado", "analisis_sintactico"]},
    {"cod": "L15", "area": "lengua", "tema": "¿Cantó o cantaba?",
     "dc": "Pretérito perfecto simple frente al imperfecto en la narración",
     "cubre": "verbos_pasado"},
    {"cod": "L16", "area": "lengua", "tema": "El conector justo",
     "dc": "Conectores y cohesión",
     "cubre": "conectores"},

    # ── Ciencias Naturales (8) ───────────────────────────────────────────────────
    {"cod": "N1",  "area": "naturales", "tema": "El ciclo del agua",
     "dc": "Ciclo hidrológico como modelo; los tres estados en los subsistemas",
     "cubre": None, "previsto": "ciclo_agua_5"},
    {"cod": "N2",  "area": "naturales", "tema": "Homogénea o heterogénea",
     "dc": "Mezclas y su clasificación",
     "cubre": None, "previsto": "mezclas_5"},
    {"cod": "N3",  "area": "naturales", "tema": "Laboratorio de disolución",
     "dc": "Modelo de partículas; factores: tamaño, temperatura y agitación",
     "cubre": None, "previsto": "disolucion_5"},
    {"cod": "N4",  "area": "naturales", "tema": "El plato GAPA",
     "dc": "Guías alimentarias; etiquetado frontal (Transversal Alimentaria)",
     "cubre": None, "previsto": "plato_gapa_5"},
    {"cod": "N5",  "area": "naturales", "tema": "Recorrido de la nutrición",
     "dc": "Nutrición como proceso integrado: digestivo, circulatorio, respiratorio y excretor",
     "cubre": ["aparatos_cuerpo", "camino_digestivo"]},
    {"cod": "N6",  "area": "naturales", "tema": "Luz y materiales",
     "dc": "Opaco, traslúcido y transparente; propagación rectilínea; reflexión",
     "cubre": None, "previsto": "luz_materiales_5"},
    {"cod": "N7",  "area": "naturales", "tema": "El sonido",
     "dc": "El sonido como vibración; no se propaga en el vacío; volumen, altura y timbre",
     "cubre": None, "previsto": "sonido_5"},
    {"cod": "N8",  "area": "naturales", "tema": "Fases de la Luna y eclipses",
     "dc": "Fases de la Luna; los eclipses como sombras",
     "cubre": "detectives_cielo",
     "deuda": "cubre las fases dentro de un banco de astronomía general; la auditoría pide "
              "además los eclipses y ordenar las fases"},

    # ── Ciencias Sociales (9) ────────────────────────────────────────────────────
    {"cod": "S1",  "area": "sociales", "tema": "Línea de tiempo 1806-1853",
     "dc": "El proceso revolucionario y las instituciones, en orden",
     "cubre": "independencia_arg"},
    {"cod": "S2",  "area": "sociales", "tema": "¿Causa interna o externa?",
     "dc": "Crisis del orden colonial: circunstancias internas y externas; multicausalidad",
     "cubre": None, "previsto": "causas_revolucion_5"},
    {"cod": "S3",  "area": "sociales", "tema": "El debate de Mayo",
     "dc": "El debate entre Moreno y Saavedra",
     "cubre": None, "previsto": "debate_mayo_5"},
    {"cod": "S4",  "area": "sociales", "tema": "Los símbolos de la Asamblea",
     "dc": "Asamblea del año XIII: libertad de vientres, moneda y símbolos",
     "cubre": None, "previsto": "asamblea_xiii_5"},
    {"cod": "S5",  "area": "sociales", "tema": "Próceres y gestas",
     "dc": "Gesta sanmartiniana; Belgrano; Güemes",
     "cubre": None, "previsto": "proceres_5"},
    {"cod": "S6",  "area": "sociales", "tema": "¿Unitario o federal?",
     "dc": "Unitarios y federales; la Constitución de 1853 como acuerdo y ley suprema",
     "cubre": "derechos_constitucion",
     "deuda": "el banco es de derechos y Constitución; falta la clasificación "
              "unitario/federal con sus consecuencias"},
    {"cod": "S7",  "area": "sociales", "tema": "El mapa de América",
     "dc": "Mapa político de América; subcontinentes, límites y escalas",
     "cubre": None, "previsto": "mapa_america_5"},
    {"cod": "S8",  "area": "sociales", "tema": "Clasificador de recursos",
     "dc": "Recursos forestales, mineros y panorámicos; su valorización",
     "cubre": "actividad_economica",
     "deuda": "clasifica actividades económicas; la auditoría pide clasificar RECURSOS y "
              "el mismo lugar con dos usos distintos"},
    {"cod": "S9",  "area": "sociales", "tema": "Mi Buenos Aires querido",
     "dc": "La ciudad: Plaza de Mayo, el Cabildo, los barrios",
     "cubre": "buenos_aires"},

    # ── Tecnología y transversales (5) ───────────────────────────────────────────
    {"cod": "T1",  "area": "tecnologia", "tema": "La caja de la variable",
     "dc": "Variables: declaración, asignación, contar y sumar",
     "cubre": None, "previsto": "variables_5"},
    {"cod": "T2",  "area": "tecnologia", "tema": "El bloque que falta",
     "dc": "Bucles, condicionales y depuración",
     "cubre": "programar_camino"},
    {"cod": "T3",  "area": "tecnologia", "tema": "Si el sensor detecta…",
     "dc": "Entrada y salida; sensores y actuadores; sistemas temporizados",
     "cubre": None, "previsto": "sensores_5"},
    {"cod": "T4",  "area": "tecnologia", "tema": "¿Es phishing?",
     "dc": "Phishing; datos personales; identidad digital",
     "cubre": None, "previsto": "phishing_5"},
    {"cod": "T5",  "area": "transversal", "tema": "Presupuesto del proyecto",
     "dc": "Ed. Financiera: ingreso y gasto, necesario y prescindible, ahorro y deuda",
     "cubre": None, "previsto": "presupuesto_5"},
]

# Grado → temas del DC. Un grado ausente todavía no está auditado: el test lo saltea.
DC = {
    4: GRADO_4,
    5: GRADO_5,
}

# Grados que se están construyendo AHORA. Mientras un grado esté acá, que le falten
# temas NO rompe la suite: se informa el avance y listo.
#
# Existe para poder construir un grado de a tandas. Un grado son 45-70 actividades y no
# entran en una sentada; sin esto, apenas se declara el manifiesto la suite queda en rojo
# por 50 temas "faltantes" que en realidad todavía no tocaba construir, y entonces no hay
# forma de commitear la mitad del trabajo. Con esto, cada tanda se commitea y pushea
# verde, y si algo se corta (se acaba el crédito, se cae la sesión) lo peor que se pierde
# es la tanda en curso.
#
# Lo que SÍ sigue fallando aunque el grado esté en construcción: un tema que declara una
# actividad inexistente, o una que quedó en un nivel con candado. "Todavía no lo hice" es
# esperable; "lo hice mal" no lo es nunca.
#
# Al terminar el grado se saca de este set y pasa a exigirse completo. Que quede vacío es
# el estado normal.
EN_CONSTRUCCION = {5}

# Actividades que están en el menú del grado pero NO cubren un tema de su currícula.
# No son un error: son comodines de descanso y refuerzos del año anterior. Se declaran
# para que el informe pueda distinguir "extra a propósito" de "tema que se nos escapó".
EXTRAS_OK = {
    4: {
        # comodines lúdicos (la auditoría presupuesta 5; hay 9, y está bien)
        "memotest", "laberinto", "sopa", "sudoku", "patron", "simon", "agrupar",
        "quefalta", "bingo",
        # contenido legítimo que el DC ubica en otro año — funciona como repaso
        "fotosintesis", "cadena_alimentaria", "estados_agua_4", "abstractos_concretos",
    },
    5: {
        # comodines lúdicos
        "memotest", "laberinto", "sopa", "sudoku", "patron", "simon", "agrupar",
        "quefalta", "bingo",
        # repaso de años anteriores / contenido que el DC de 5° no lista
        "serie", "trivia_colonial", "clases_palabra_5",
        # la auditoría la marca para REEMPLAZAR por N1 (ciclo del agua); se deja como
        # extra en vez de sacarla, así el grado no pierde contenido mientras tanto
        "planta_potabilizadora",
    },
}


def temas(grado):
    """Los temas del DC de ese grado. Lista vacía si el grado no está auditado."""
    return DC.get(int(grado), [])


def _ids(tema):
    """Los ids de actividad que cubren un tema (siempre lista, puede ser vacía)."""
    c = tema.get("cubre")
    if not c:
        return []
    return list(c) if isinstance(c, (list, tuple)) else [c]


def faltantes(grado):
    """Temas del DC sin ninguna actividad declarada."""
    return [t for t in temas(grado) if not _ids(t)]


def con_deuda(grado):
    """Temas cubiertos pero incompletos (el banco no da para lo que pide el DC)."""
    return [t for t in temas(grado) if _ids(t) and t.get("deuda")]


def _menu_real(grado):
    """El menú que realmente ve un chico de ese grado: {id: nivel}.

    Es la única fuente que vale — un tema declarado 'cubierto' por una actividad que no
    está en el menú no está cubierto ([[ct3d-contenido-cargado-sin-enchufar]]: subir el
    contenido no es entregarlo)."""
    import actividades_web as aw
    edad = int(grado) + 5
    banda = aw._banda(edad) if hasattr(aw, "_banda") else "grande"
    menu = list(aw._menu(banda, edad)) + list(aw._menu_curricular(edad))
    aw._marcar_niveles(menu)
    return {it["id"]: it.get("nivel", 1) for it in menu}


def problemas(grado):
    """Los incumplimientos de la regla, para el test. Lista vacía = el grado cumple.

    Chequea las tres cosas, en este orden, porque fallan distinto:
      1. todo tema del DC tiene actividad declarada,
      2. esa actividad EXISTE en el menú real del grado,
      3. y está en el NIVEL 1 (ningún tema del año detrás de un candado).

    Si el grado está en EN_CONSTRUCCION se saltea (1) —todavía se está construyendo— pero
    (2) y (3) se siguen exigiendo: no haberlo hecho es esperable, haberlo hecho mal no.
    """
    fallas = []
    if int(grado) not in DC:
        return fallas
    en_obra = int(grado) in EN_CONSTRUCCION
    menu = _menu_real(grado)
    for t in temas(grado):
        ids = _ids(t)
        if not ids:
            if not en_obra:
                fallas.append("%s %s: sin actividad — falta construirla"
                              % (t["cod"], t["tema"]))
            continue
        for aid in ids:
            if aid not in menu:
                fallas.append("%s %s: declara '%s' pero esa actividad no está en el menú "
                              "de %d°" % (t["cod"], t["tema"], aid, grado))
            elif menu[aid] != 1:
                fallas.append("%s %s: '%s' está en el nivel %d; un tema del año tiene que "
                              "estar en el nivel 1" % (t["cod"], t["tema"], aid, menu[aid]))
    return fallas


def informe(grado=4):
    """Imprime el estado de cobertura del grado. Para mirarlo a mano."""
    ts = temas(grado)
    if not ts:
        print("%d° todavía no tiene manifiesto de cobertura." % grado)
        return
    faltan = faltantes(grado)
    hechos = len(ts) - len(faltan)
    estado = " · EN CONSTRUCCIÓN" if int(grado) in EN_CONSTRUCCION else ""
    print("%d° — %d temas del DC · cubiertos %d (%d%%) · faltan %d%s"
          % (grado, len(ts), hechos, round(100.0 * hechos / len(ts)), len(faltan), estado))
    areas = {}
    for t in ts:
        a = areas.setdefault(t["area"], [0, 0])
        a[0] += 1
        if not _ids(t):
            a[1] += 1
    for area in sorted(areas):
        total, falta = areas[area]
        print("  %-12s %2d temas · faltan %d" % (area, total, falta))
    for t in faltan:
        print("  FALTA  %-4s %s" % (t["cod"], t["tema"]))
    for t in con_deuda(grado):
        print("  DEUDA  %-4s %s — %s" % (t["cod"], t["tema"], t["deuda"]))
    for p in problemas(grado):
        print("  ROTO   %s" % p)
