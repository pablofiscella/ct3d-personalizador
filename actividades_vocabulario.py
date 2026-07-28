# -*- coding: utf-8 -*-
"""Vocabulario de la SOPA DE LETRAS por grado (línea escolar / Kydo).

28-jul-2026. Pablo: *"que las palabras que aparezcan sean temáticas en 1ro y 2do
pero en los grados siguientes tienen que estar acorde a la edad"*.

Hasta hoy la sopa tomaba las palabras del TEMA de cumpleaños del token
(`cuaderno._tema_palabras`) sin mirar el grado: los 49 tokens con `escolar_on`
son `tema=safari`, así que un chico de 7° en el mundo "Creadores del Futuro"
buscaba MONO, JIRAFA y CEBRA — las mismas seis palabras que uno de 1°. Es la
misma dificultad invertida que ya se arregló en `serie`
(`actividades_web.py:195-198`).

Cómo se reparte:

* **1° y 2° → el MUNDO del grado.** Las palabras son temáticas, como pidió
  Pablo, pero del mundo que el chico ya tiene en la portada
  (`actividades_web.MUNDO_GRADO`), no del tema de cumpleaños. Así 1°
  (Exploradores de la Naturaleza) y 2° (Jóvenes Creativos en la Ciudad) dejan
  de compartir la misma sopa.
* **3° a 7° → vocabulario CURRICULAR del grado**, repartido entre las cuatro
  áreas. Cada palabra sale de un tema declarado del DC en `actividades_cobertura.DC`
  para ese grado: no hay contenido inventado acá. Lo pedían las auditorías —
  `docs/auditoria-dc-caba/grado-6.md:224`: *"cambiar banco genérico (CUMPLE,
  FIESTA) por vocabulario de 6°"*.

Tres reglas del banco, verificadas en `tests/test_sopa_por_grado.py`:

1. **Ninguna Ñ.** El relleno de la grilla es `A-Z` uniforme
   (`cuaderno.py:640`), sin Ñ: una Ñ en la grilla delata la palabra sola.
2. **3° sin tildes.** `_sin_tilde` las saca de la grilla, y en 3° la tilde ES
   el contenido que se enseña (L1 "La sílaba fuerte", L2 "Ponele la tilde"):
   mostrar PINGUINO en la grilla enseñaría el error
   (`docs/auditoria-dc-caba/grado-3.md:208`). En el resto de los grados la
   tilde va, porque el chip de la lista (`lindas`) muestra la palabra bien
   escrita y ese contraste no es el contenido del grado.
3. **≥24 palabras usables por grado.** Con las 8 de un tema, las 4 sopas de un
   token eran la misma sopa barajada (6 de 8 palabras fijas). Con 24+ cada
   sopa del cuaderno es distinta de verdad.
"""

# Largo máximo por grado — la grilla de cada grado lo impone (`_SOPA_GRADO` en
# actividades_web.py). Acá vive sólo para que `validar()` pueda comprobar que el
# banco tiene suficientes palabras USABLES, no sólo suficientes palabras.
MAX_LETRAS = {1: 6, 2: 7, 3: 10, 4: 10, 5: 12, 6: 12, 7: 12}

# Mínimo de palabras usables por grado (ver regla 3 del docstring).
MINIMO_USABLES = 24


VOCABULARIO = {
    # ── 1° · Exploradores de la Naturaleza ──────────────────────────────────
    # Temáticas (no curriculares): a los 6 años la sopa es recreo con valor de
    # vocabulario, y su anclaje al DC es nulo (grado-1.md la manda a Recreo).
    # Todo ≤6 letras: la grilla de 1° es 6×6.
    1: {
        "mundo": [
            "HOJA", "NIDO", "RANA", "SOL", "LUNA", "NUBE", "FLOR", "RAÍZ",
            "TALLO", "PASTO", "ÁRBOL", "SAPO", "PATO", "PEZ", "ARENA",
            "PIEDRA", "LLUVIA", "VIENTO", "BOSQUE", "TIERRA", "GUSANO",
            "ABEJA", "PLUMA", "PICO", "RÍO", "MAR", "CIELO", "HUEVO",
            "CAMPO", "LAGO", "BICHO", "ORUGA", "RAMA", "TRONCO", "FRUTO",
            "NIEVE", "BARRO", "PÉTALO", "MUSGO",
        ],
    },
    # ── 2° · Jóvenes Creativos en la Ciudad ─────────────────────────────────
    # Todo ≤7 letras: la grilla de 2° es 8×8 y grado-2.md pide palabras de 3-7.
    2: {
        "mundo": [
            "PLAZA", "MURAL", "CALLE", "BARRIO", "CIUDAD", "VECINO",
            "ESQUINA", "FAROL", "PLANO", "MAPA", "TALLER", "PINCEL",
            "COLORES", "MUSEO", "TEATRO", "VEREDA", "PARQUE", "PUENTE",
            "ESCUELA", "MERCADO", "TIENDA", "SUBTE", "TREN", "KIOSCO",
            "FUENTE", "CARTEL", "MOSAICO", "BOCETO", "IDEA", "OBRA",
            "ARTE", "MURO", "MAQUETA", "TIJERA", "PAPEL", "CARTÓN",
            "PINTURA", "CUADRO", "MÚSICA", "RADIO", "FOTO", "VITRAL",
        ],
    },
    # ── 3° ──────────────────────────────────────────────────────────────────
    # SIN TILDES (regla 2): en 3° la tilde es el contenido que se enseña.
    3: {
        "matematica": [   # M1-M18: miles, llevada, tabla pitagórica, figuras, hora, medida
            "CENTENA", "UNIDAD", "DECENA", "MILLAR", "RESTA", "SUMA",
            "TABLA", "PRODUCTO", "REPARTO", "RESTO", "FIGURA", "CUERPO",
            "CARA", "ARISTA", "RELOJ", "HORA", "MINUTO", "METRO", "LITRO",
            "KILO", "GRAMO", "DOBLE", "TRIPLE", "MITAD", "CUADRADO",
            "CUBO", "PRISMA",
        ],
        "lengua": [       # L1-L17: sílaba, tilde, diálogo, verso, verbo, diccionario
            "TILDE", "VERSO", "ESTROFA", "POEMA", "CUENTO", "VERBO",
            "SUJETO", "PALABRA", "LETRA", "PUNTO", "COMA", "RIMA",
            "TEATRO", "LIBRO", "TEXTO", "DIPTONGO", "HIATO", "ORDEN",
        ],
        "naturales": [    # C1-C6, C9, T8: calor, materiales, cielo, alimento, compost
            "CALOR", "MATERIAL", "QUESO", "LECHE", "INVIERNO", "VERANO",
            "CIELO", "ESTRELLA", "PLANETA", "LUNA", "ALIMENTO", "COMPOST",
            "BASURA", "RECICLAR", "SOMBRA", "MEZCLA",
        ],
        "sociales": [     # C7, C8, C10: línea de tiempo, Plaza de Mayo, derechos
            "PLAZA", "HISTORIA", "DERECHO", "TIEMPO", "SIGLO", "PASADO",
            "PRESENTE", "CIUDAD", "BARRIO", "MAYO", "TRABAJO", "VECINO",
            "NORMA", "PUEBLO",
        ],
    },
    # ── 4° ──────────────────────────────────────────────────────────────────
    4: {
        "matematica": [   # M1-M19: fracciones, división, ángulos, medida, cuerpos
            "FRACCIÓN", "DIVISIÓN", "TRIÁNGULO", "ÁNGULO", "RECTA",
            "MEDIDA", "BALANZA", "LITRO", "KILO", "DECIMAL", "PRODUCTO",
            "COCIENTE", "PERÍMETRO", "NUMERADOR", "TABLA", "SERIE",
            "RESTO", "CANJE", "GRADO", "CUERPO",
        ],
        "lengua": [       # L1-L17: tildes, sujeto/predicado, clases de palabra, mito
            "TILDE", "SUJETO", "PREDICADO", "VERBO", "CONECTOR",
            "ADJETIVO", "SUSTANTIVO", "MITO", "LEYENDA", "PÁRRAFO",
            "DIÁLOGO", "HIPÓNIMO", "RELATO", "TÍTULO", "PLURAL",
            "SÍLABA", "TEXTO",
        ],
        "naturales": [    # N1-N8: paisaje, placas, fósiles, imanes, circuito, cielo
            "PAISAJE", "PLACA", "FÓSIL", "IMÁN", "CIRCUITO", "MATERIAL",
            "EROSIÓN", "MOVIMIENTO", "ENERGÍA", "PLANETA", "ESTRELLA",
            "ROCA", "VOLCÁN", "TERREMOTO", "OBJETO",
        ],
        "sociales": [     # S1-S8: pueblos originarios, colonia, ambientes, provincias
            "COLONIA", "PUEBLO", "AMÉRICA", "PROVINCIA", "CAPITAL",
            "AMBIENTE", "RURAL", "URBANO", "REGIÓN", "VIRREY", "CABILDO",
            "MAPA", "RECURSO", "FRONTERA",
        ],
    },
    # ── 5° ──────────────────────────────────────────────────────────────────
    5: {
        "matematica": [   # M1-M18: millón, romanos, múltiplos, fracciones, decimales
            "MILLÓN", "ROMANO", "MÚLTIPLO", "DIVISOR", "FRACCIÓN",
            "DECIMAL", "DÉCIMO", "ENTERO", "PROPORCIÓN", "PERÍMETRO",
            "ÁREA", "ENCUESTA", "GRÁFICO", "COCIENTE", "EQUIVALENTE",
            "NUMERADOR", "DENOMINADOR", "PROMEDIO",
        ],
        "lengua": [       # L1-L16: adjetivo, prefijos, diacrítica, argumento, poesía
            "ADJETIVO", "PREFIJO", "SUFIJO", "CONDICIONAL", "DIACRÍTICA",
            "ARGUMENTO", "OPINIÓN", "PÁRRAFO", "POESÍA", "METÁFORA",
            "VERBO", "OBJETO", "SINÓNIMO", "PUNTUACIÓN", "CONECTOR",
            "NARRADOR",
        ],
        "naturales": [    # N1-N8: ciclo del agua, mezclas, nutrición, luz, sonido, Luna
            "DISOLUCIÓN", "MEZCLA", "HOMOGÉNEA", "NUTRICIÓN", "DIGESTIÓN",
            "SONIDO", "ECLIPSE", "FASE", "CICLO", "VAPOR", "ALIMENTO",
            "ENERGÍA", "MATERIA", "REFLEJO",
        ],
        "sociales": [     # S1-S9: 1806-1853, Mayo, símbolos, unitarios y federales
            "REVOLUCIÓN", "CABILDO", "ASAMBLEA", "UNITARIO", "FEDERAL",
            "PRÓCER", "ESCARAPELA", "BANDERA", "AMÉRICA", "RECURSO",
            "MAYO", "HIMNO", "VIRREINATO", "COLONIA",
        ],
    },
    # ── 6° ──────────────────────────────────────────────────────────────────
    6: {
        "matematica": [   # M1-M18: primos, divisibilidad, porcentaje, probabilidad
            "PRIMO", "CRIBA", "DIVISIBLE", "PERMUTACIÓN", "FRACCIÓN",
            "DECIMAL", "PORCENTAJE", "DESCUENTO", "PROBABILIDAD",
            "MEDIANA", "MODA", "CUADRILÁTERO", "ÁNGULO", "ÁREA",
            "PERÍMETRO", "PROPORCIÓN", "DIVISOR",
        ],
        "lengua": [       # L0-L12: noticia, pronombres, sintaxis, conectores, poema
            "NOTICIA", "PRONOMBRE", "ORACIÓN", "TRANSITIVO", "CONECTOR",
            "SINÓNIMO", "POEMA", "ESTROFA", "PUNTUACIÓN", "VERBO",
            "NARRADOR", "FUENTE", "CRÓNICA", "SINÓPTICO", "TILDE",
        ],
        "naturales": [    # N1-N10: ecosistema, ecorregiones, calor, heliocentrismo, clima
            "ECOSISTEMA", "ECORREGIÓN", "TRÓFICA", "PRODUCTOR",
            "CONSUMIDOR", "PARTÍCULA", "TÉRMICO", "GEOCÉNTRICO", "CLIMA",
            "INVERNADERO", "PUBERTAD", "ENERGÍA", "MATERIA", "ESPECIE",
        ],
        "sociales": [     # S1-S9, Tr3: 1862-1930, inmigración, sufragio, tres poderes
            "INMIGRACIÓN", "CONVENTILLO", "SUFRAGIO", "INDUSTRIAL",
            "MERCOSUR", "DEMOGRAFÍA", "CENSO", "ESTADO", "DEMOCRACIA",
            "PODERES", "REVOLUCIÓN", "MIGRACIÓN", "CIUDADANO",
        ],
    },
    # ── 7° ──────────────────────────────────────────────────────────────────
    7: {
        "matematica": [   # M0-M14: potencias, razón, proporcionalidad, álgebra
            "POTENCIA", "RAÍZ", "DIVISOR", "MÚLTIPLO", "ÁLGEBRA",
            "ECUACIÓN", "RAZÓN", "PORCENTAJE", "PROPORCIÓN", "DENSIDAD",
            "PERÍMETRO", "CÍRCULO", "MEDIANA", "PROBABILIDAD", "INFLACIÓN",
            "PRESUPUESTO", "PERÍODO",
        ],
        "lengua": [       # L1-L15: narrador, metáfora, argumentación, sintaxis
            "NARRADOR", "FANTÁSTICO", "METÁFORA", "SINÉCDOQUE",
            "ARGUMENTO", "PERSUASIÓN", "CRÓNICA", "HISTORIETA",
            "SINTÁCTICO", "SUSTANTIVO", "ORTOGRAFÍA", "VERBO", "TERROR",
            "OPINIÓN",
        ],
        "naturales": [    # CN1-CN10, T1-T2: redes tróficas, defensas, energía, universo
            "TRÓFICA", "SUCESIÓN", "ESTÍMULO", "VACUNA", "DEFENSA",
            "ENERGÍA", "QUÍMICA", "ECLIPSE", "UNIVERSO", "ESTACIÓN",
            "SUSTENTABLE", "MATRIZ", "CENTRAL", "RECICLAJE",
        ],
        "sociales": [     # CS1-CS9, X3-X8: siglo XX, democracia, migración, consumo
            "DICTADURA", "DEMOCRACIA", "MEMORIA", "MIGRACIÓN",
            "PRODUCTIVA", "REGIONAL", "DERECHOS", "GOBIERNO",
            "CONSUMISMO", "FRONTERA", "SIGLO", "GUERRA", "REGIÓN",
        ],
    },
}


def tiene_tilde(p):
    """True si la palabra se ESCRIBE distinto de como se ve en la grilla.
    Misma tabla que `cuaderno._sin_tilde` (la Ñ no es tilde: se conserva)."""
    return p.translate(str.maketrans("ÁÉÍÓÚÜ", "AEIOUU")) != p


def usables(grado, max_letras=None):
    """Las palabras del grado que entran en su grilla (sin repetir, ordenadas)."""
    areas = VOCABULARIO.get(int(grado)) or {}
    tope = max_letras or MAX_LETRAS.get(int(grado), 10)
    vistas, out = set(), []
    for palabras in areas.values():
        for p in palabras:
            p = str(p).strip().upper()
            if 3 <= len(p) <= tope and p not in vistas:
                vistas.add(p)
                out.append(p)
    return out


def palabras_de_grado(grado, rnd, cuantas, max_letras=None, evitar=None):
    """`cuantas` palabras del grado, REPARTIDAS entre las áreas.

    El reparto es round-robin sobre las áreas barajadas, no un sample plano:
    con un sample plano una sopa de 7° podía salir entera de matemática
    (17 de 57 palabras) y el chico no veía el cruce de áreas que es la gracia
    del vocabulario curricular.

    `evitar`: palabras ya usadas en OTRA sopa del mismo cuaderno. Se saltean
    mientras el banco alcance, así las 4 sopas del token no repiten vocabulario
    (con las 8 palabras de un tema, las 4 sopas eran la misma sopa barajada).
    Si el banco no da para tanto, se vuelve a permitir repetir antes que
    devolver una sopa incompleta.

    Devuelve [] si el grado no tiene banco — el llamador cae al vocabulario del
    tema, como siempre."""
    areas = VOCABULARIO.get(int(grado)) or {}
    if not areas:
        return []
    tope = max_letras or MAX_LETRAS.get(int(grado), 10)
    evitar = set(evitar or ())
    pilas = []
    for nombre in sorted(areas):
        ws = [str(p).strip().upper() for p in areas[nombre]]
        ws = [p for p in ws if 3 <= len(p) <= tope]
        rnd.shuffle(ws)
        # `pop()` saca del final: las ya usadas van al PRINCIPIO de la pila, así
        # salen últimas y sólo si el banco no alcanzó para evitarlas.
        ws.sort(key=lambda p: p not in evitar)
        if ws:
            pilas.append(ws)
    rnd.shuffle(pilas)
    vistas, out = set(), []
    while pilas and len(out) < cuantas:
        for pila in list(pilas):
            if len(out) >= cuantas:
                break
            while pila:
                p = pila.pop()
                if p not in vistas:
                    vistas.add(p)
                    out.append(p)
                    break
            if not pila:
                pilas.remove(pila)
    return out


def validar():
    """Problemas del banco, como lista de strings (vacía = todo bien).

    Mismo contrato que `actividades_curriculum.validar()`: lo corre el test,
    no se ejecuta en producción."""
    problemas = []
    for grado in sorted(VOCABULARIO):
        tope = MAX_LETRAS[grado]
        libres = usables(grado)
        if len(libres) < MINIMO_USABLES:
            problemas.append(
                "grado %d: %d palabras usables (≤%d letras), mínimo %d — con menos "
                "las 4 sopas del token se repiten" % (grado, len(libres), tope, MINIMO_USABLES))
        for area, palabras in VOCABULARIO[grado].items():
            for p in palabras:
                p = str(p).strip().upper()
                if "Ñ" in p:
                    problemas.append(
                        "grado %d/%s: %r tiene Ñ — el relleno de la grilla es A-Z "
                        "sin Ñ y la delata" % (grado, area, p))
                if len(p) < 3:
                    problemas.append("grado %d/%s: %r es más corta que 3 letras" % (grado, area, p))
                if len(p) > tope:
                    problemas.append(
                        "grado %d/%s: %r tiene %d letras y la grilla del grado admite %d"
                        % (grado, area, p, len(p), tope))
                if grado == 3 and tiene_tilde(p):
                    problemas.append(
                        "grado 3/%s: %r lleva tilde — en 3° la tilde es el contenido "
                        "y la grilla la borra (grado-3.md:208)" % (area, p))
    for grado in (1, 2):
        if list(VOCABULARIO[grado]) != ["mundo"]:
            problemas.append("grado %d: 1° y 2° van por mundo del grado, no por áreas" % grado)
    for grado in (3, 4, 5, 6, 7):
        faltan = {"matematica", "lengua", "naturales", "sociales"} - set(VOCABULARIO[grado])
        if faltan:
            problemas.append("grado %d: faltan áreas %s" % (grado, sorted(faltan)))
    return problemas
