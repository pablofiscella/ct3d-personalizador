"""Categoría escolar de cada actividad (juego) del cuaderno web.

CIMIENTO de la pantalla nueva de actividades por categorías (nivel independiente
por materia — ver diseño en memoria `ct3d-actividades-categorias-pantalla`).

El GRADO de cada actividad ya lo decide `actividades_web.py` (qué juegos entran en
el menú de cada grado). Lo único que faltaba para armar los carriles por materia era
esta etiqueta de CATEGORÍA por juego — es lo que provee este módulo.

Categorías (las 4 áreas de la primaria) + un bucket transversal:
  - "lengua"     Prácticas del Lenguaje
  - "matematica" Matemática
  - "naturales"  Ciencias Naturales
  - "sociales"   Ciencias Sociales
  - "logica"     juegos SIN materia (memoria, laberinto, sudoku, colorear…). Se
                 decide al armar la pantalla si van en su propia sección, repartidos,
                 o dentro de la materia más cercana.

Los marcados con  # ???  son dudosos: confirmar con Pablo / mirando el juego.
Generado 21-jul-2026. Fuente: los 142 `GAMES.<id>` de actividades_player.js.
"""

CATEGORIA = {
    # ─────────── LENGUA ───────────
    "abecedario": "lengua",
    "abstractos_concretos": "lengua",
    "acentuacion": "lengua",
    "analisis_sintactico": "lengua",
    "armar_palabra": "lengua",
    "cazador_errores": "lengua",
    "comprension_lectora": "lengua",
    "conectores": "lengua",
    "dialogo_raya": "lengua",
    "familia_palabras": "lengua",
    "hechos_opiniones": "lengua",
    "homofonos": "lengua",
    "ingles_basico": "lengua",             # confirmado: un solo juego, no amerita categoría propia todavía
    "historia_orden": "lengua",            # confirmado: "ordená el cuento" = secuencia narrativa (comprensión
                                            # lectora), NO contenido histórico — eso lo hace historia4/sigloXX (sociales)
    "letra_inicial": "lengua",
    "orden_alfabetico": "lengua",
    "ortografia_2do": "lengua",
    "ortografia_3ro": "lengua",
    "partes_oracion": "lengua",
    "plurales_z": "lengua",
    "prefijos_sufijos": "lengua",
    "silaba_tonica": "lengua",
    "silabas": "lengua",
    "sinonimos_antonimos": "lengua",
    "sopa": "lengua",                     # sopa de letras
    "sujeto_predicado": "lengua",
    "sustantivos": "lengua",
    "tiempos_verbales": "lengua",
    "verbos_pasado": "lengua",

    # ─────────── MATEMÁTICA ───────────
    # agrupar: LÚDICO (clasificar sprites en canastas, no valor posicional) → Extras (movido a la sección logica)
    "angulos": "matematica",
    "anterior_siguiente": "matematica",
    "arbol_probabilidad": "matematica",
    "area_perimetro": "matematica",
    # bingo: LÚDICO (matching de imágenes/sprites, NO números) → Extras (movido a la sección logica)
    "cajero_automatico": "matematica",
    "comparar_numeros": "matematica",
    "completar_entero": "matematica",
    "contar": "matematica",
    "contar_saltando": "matematica",
    "cuadrilateros": "matematica",
    "cuenta_larga": "matematica",
    "cuerpos_geometricos": "matematica",
    "decimales_fraccion": "matematica",
    "dividir": "matematica",
    "duelo_decimales": "matematica",
    "duelo_fracciones": "matematica",
    "ecuaciones_simples": "matematica",
    "equivalencias_medida": "matematica",
    "estadistica_datos": "matematica",
    "fraccion_de_cantidad": "matematica",
    "fracciones_avanzado": "matematica",
    "fracciones_equivalentes": "matematica",
    "grilla100": "matematica",
    "jerarquia_operaciones": "matematica",
    "mas_menos": "matematica",
    "mejor_oferta": "matematica",
    "multiplicacion_concepto": "matematica",
    "multiplicar": "matematica",
    "multiplicar_fracciones": "matematica",
    "numeros_primos": "matematica",
    "ordenar_numeros": "matematica",
    "pago_exacto": "matematica",
    # patron: LÚDICO (seguir secuencia VISUAL de sprites (1°-2°)) → Extras (movido a la sección logica)
    "poligonos_lados": "matematica",
    "porcentajes": "matematica",
    "posicion": "matematica",             # confirmado: arriba/abajo/adentro/afuera (nociones espaciales, geometría 1°)
    "potencias": "matematica",
    "probabilidad_sucesos": "matematica",
    "problemas_3ro": "matematica",
    "problemas_mult_div": "matematica",
    "problemas_multipaso": "matematica",
    "proporcionalidad": "matematica",
    "recta_numerica": "matematica",
    "reloj": "matematica",
    "reparto_con_resto": "matematica",
    "reparto_fracciones": "matematica",
    "resta_columnas": "matematica",
    "restas": "matematica",
    "serie": "matematica",
    "suma_angulos": "matematica",
    "suma_columnas": "matematica",
    "suma_fracciones": "matematica",
    "suma_rapida": "matematica",
    "sumas": "matematica",
    "sumas_redondas": "matematica",
    "tabla_pitagorica": "matematica",
    "tablas_contrarreloj": "matematica",
    "tablas_ninja": "matematica",
    "traductor_algebraico": "matematica",
    "transportador": "matematica",
    "valor_posicional": "matematica",

    # ─────────── CS. NATURALES ───────────
    "animal_comida": "naturales",         # (a retirar, pero mientras exista → Naturales)
    "camino_digestivo": "naturales",
    "celula_partes": "naturales",
    "cerebro_defensas": "naturales",
    "cielo": "naturales",                 # astronomía
    "conductor_aislante": "naturales",
    "detectives_cielo": "naturales",
    "energia_renovable": "naturales",
    "estaciones": "naturales",
    "estados_materia": "naturales",
    "fotosintesis": "naturales",
    "laboratorio_electrico": "naturales",
    "luz_materiales": "naturales",
    "materiales": "naturales",
    "planetas_tipo": "naturales",
    "planta_fruto": "naturales",
    "planta_potabilizadora": "naturales", # confirmado: proceso del agua como recurso natural (captación→distribución)
    "pubertad": "naturales",
    "red_trofica": "naturales",
    "sentidos": "naturales",
    "separador_mezclas": "naturales",
    "sistema_nervioso": "naturales",
    "sistema_reproductor": "naturales",
    "trivia_espacial": "naturales",

    # ─────────── CS. SOCIALES ───────────
    "actividad_economica": "sociales",
    "argentina_sigloXX": "sociales",      # Argentina siglo XX (id camelCase)
    "buenos_aires": "sociales",
    "campo_ciudad": "sociales",
    "derechos_constitucion": "sociales",
    "historia_originarios": "sociales",
    "independencia_arg": "sociales",
    "linea_democracia": "sociales",
    "linea_tiempo": "sociales",
    "organizacion_nacional": "sociales",
    "provincias_region": "sociales",
    "sufragio_argentina": "sociales",
    "trivia_colonial": "sociales",
    "viaje_inmigrante": "sociales",

    # ─────────── EXTRAS / LÚDICO (sin materia; dificultad no escala a 4° → NO académicos) ───────────
    "bingo": "logica",
    "agrupar": "logica",
    "patron": "logica",
    "colorear": "logica",
    "diferente": "logica",
    "escape_room_egreso": "logica",       # repaso mixto de egreso
    "laberinto": "logica",
    "memotest": "logica",
    "programar_camino": "logica",         # confirmado: pensamiento computacional (secuencia/bucle/condicional)
    "puntos": "logica",
    "quefalta": "logica",
    "simon": "logica",
    "sombra": "logica",
    "sudoku": "logica",                   # confirmado: son caras/símbolos, no aritmética — es razonamiento lógico puro
    "tamano": "logica",
}


def categoria_de(juego_id, default=None):
    """Categoría de un juego por su id (el mismo que usa GAMES.<id> / el menú)."""
    return CATEGORIA.get(juego_id, default)


# Orden y etiqueta visible de los carriles en el lateral. "logica" se muestra como
# "Ingenio" (juegos transversales sin materia). Labels cambiables sin tocar la lógica.
CATEGORIA_ORDEN = ["lengua", "matematica", "naturales", "sociales", "logica"]
CATEGORIA_LABEL = {
    "lengua": "Lengua", "matematica": "Matemática", "naturales": "Cs. Naturales",
    "sociales": "Cs. Sociales", "logica": "Extras",
}


def carriles_de_menu(menu_ids, min_actividades=1):
    """Agrupa los juegos de UN grado (su lista de ids de menú) en carriles por
    categoría, en orden, y devuelve SOLO los que llegan a `min_actividades`.

    Regla clave de la pantalla: una categoría con muy pocas (o cero) actividades en
    ese grado NO se muestra — nada de carriles vacíos. Con el contenido de hoy, 2° y
    3° no muestran Sociales (0 juegos); aparece sola cuando se cargue contenido.

    Devuelve: [{"categoria","label","juegos":[ids...],"cantidad"}] ordenado por
    CATEGORIA_ORDEN. Los ids sin categoría conocida se ignoran."""
    grupos = {c: [] for c in CATEGORIA_ORDEN}
    for jid in menu_ids:
        c = CATEGORIA.get(jid)
        if c is not None:
            grupos[c].append(jid)
    return [
        {"categoria": c, "label": CATEGORIA_LABEL[c],
         "juegos": grupos[c], "cantidad": len(grupos[c])}
        for c in CATEGORIA_ORDEN if len(grupos[c]) >= min_actividades
    ]
