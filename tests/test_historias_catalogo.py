# -*- coding: utf-8 -*-
"""QA del catálogo de audiolibros: valida que las 8 historias encajen en TODAS
las temáticas (texto e imagen) sin errores de gramática, género ni reglas de
ilustración. Es el guardián del goal «cero errores de diálogo o imágenes»:
si un arco, un diccionario de tema o una escena rompe una regla, acá salta.

Reglas verificadas (ver skill armar-audiolibros):
  T1  Estructura: 8 arcos × 17 páginas; CORTO_IDX de 9.
  T2  Render de TODOS los combos tema×historia×edad: sin llaves sin resolver,
      sin dobles espacios, largo por página apto TTS, el nombre aparece.
  T3  Género neutro: sin «él/ella» ni adjetivos concordados con el protagonista
      (el motor NO adapta el texto al género del chico).
  T4  Sin concordancia con {mundo}: ni «el {mundo}» ni adjetivos pegados.
  T5  Diccionarios por tema bien formados (desafio/solucion/amigos/tesoro).
  T6  No repetición: sin frases duplicadas dentro de un libro.
  T7  Escenas: sin poses prohibidas (dar la mano / saludar / aplaudir, que
      generan patas de más), rescatado siempre nene humano, 17 por historia.
"""
import re
import itertools

import libro
from libro_historias import ARGUMENTOS_LARGO, CORTO_IDX, TITULOS
import libro_ia

TEMAS_CATALOGO = ["safari", "circo", "superheroes", "construccion", "bomberos",
                  "aviadores", "campamento", "artistas", "monstruos",
                  "princesas", "futbol", "un-espacio-de-locura"]
HISTORIAS_CATALOGO = list(ARGUMENTOS_LARGO)


# ── T1 · estructura ──────────────────────────────────────────────────────────
def test_estructura():
    assert len(ARGUMENTOS_LARGO) == 11
    for k, v in ARGUMENTOS_LARGO.items():
        assert len(v) == 17, k
    assert len(CORTO_IDX) == 9 and max(CORTO_IDX) < 17
    # Cada historia con SU título de tapa (no todas "La gran aventura")
    assert set(TITULOS) == set(ARGUMENTOS_LARGO)
    assert len(set(TITULOS.values())) == len(TITULOS)


# ── T2 · render de todos los combos ──────────────────────────────────────────
def _libros():
    """Todos los combos renderizados: (tema, historia, edad, páginas)."""
    for tema, hist in itertools.product(TEMAS_CATALOGO, HISTORIAS_CATALOGO):
        for edad, n in (("3", 9), ("6", 17)):
            data = {"nombre": "Luna", "edad": edad, "historia": hist}
            yield tema, hist, edad, n, libro.cuento(data, tema, catalogo=True)


def test_render_todos_los_combos():
    errores = []
    for tema, hist, edad, n, pags in _libros():
        combo = f"{tema}/{hist}/edad{edad}"
        if len(pags) != n:
            errores.append(f"{combo}: {len(pags)} páginas (esperaba {n})")
        texto = " ".join(pags)
        if "{" in texto or "}" in texto:
            errores.append(f"{combo}: placeholder sin resolver")
        if "  " in texto:
            errores.append(f"{combo}: doble espacio")
        if "«" in texto or "»" in texto:
            errores.append(f"{combo}: comillas «» (usar “ ” — los padres las "
                           f"leen como '>>')")
        # contracción: {mundo} trae su artículo → nunca "a el"/"de el" sin contraer
        if re.search(r"\b[Aa] el\b|\b[Dd]e el\b", texto):
            errores.append(f"{combo}: falta contraer 'a el'→'al' / 'de el'→'del'")
        if texto.count("Luna") < 3:
            errores.append(f"{combo}: el nombre casi no aparece")
        for i, p in enumerate(pags):
            if not (55 <= len(p) <= 230):
                errores.append(f"{combo} pág {i}: {len(p)} caracteres")
    assert not errores, "\n".join(errores)


# ── T3 · género neutro (sirve para nene y para nena) ─────────────────────────
# Adjetivos/participios masculinos singulares: en los arcos el único singular
# humano es el protagonista, así que su sola presencia delata concordancia.
_GENERO_BAN = [
    r"\bél\b", r"\bella\b(?!s)", r"\binvitad[oa]\b", r"\bpensativ[oa]\b",
    r"\bemocionad[oa]\b", r"\bcontent[oa]\b", r"\btranquil[oa]\b",
    r"\bsolit[oa]\b", r"\bacurrucad[oa]\b", r"\bcansad[oa]\b",
    r"\bdormid[oa]\b", r"\bextrañad[oa]\b", r"\brecostad[oa]\b",
    r"\bcurios[oa]\b", r"\blist[oa]\b para\b",
]
# Usos legítimos (el adjetivo/clítico refiere a otro personaje, no al chico).
_GENERO_OK = [
    "el más chiquito", "amiguito", "cumpleañero", "el pequeño", "gatito",
    "personaje", "monstruo", "estrella", "los ", "las ",
    "mapa",      # «el mapa se dio vuelta solito»
    "lluvia",    # «se mojó con la lluvia, y sin ella (la torre) la fiesta...»
]


def test_genero_neutro_en_arcos():
    errores = []
    for hist, arco in ARGUMENTOS_LARGO.items():
        for i, pagina in enumerate(arco):
            low = pagina.lower()
            for pat in _GENERO_BAN:
                for m in re.finditer(pat, low):
                    ctx = low[max(0, m.start() - 30):m.end() + 10]
                    if any(ok in ctx for ok in _GENERO_OK):
                        continue
                    errores.append(f"{hist} pág {i}: «...{ctx}...» ({pat})")
    assert not errores, "\n".join(errores)


# ── T4 · sin concordancia con {mundo} ────────────────────────────────────────
_MUNDO_BAN = [
    r"\b(el|del|al|todo|toda|un)\s+\{mundo\}",       # {mundo} ya trae artículo
    r"\{mundo\}\s+(m[áa]s\s+)?(llen[oa]|enter[oa]|iluminad[oa]|lind[oa]|"
    r"hermos[oa]|precios[oa]|mágic[oa]|grand[e]?)\b",  # adjetivo concordado
]


def test_mundo_sin_concordancia():
    errores = []
    for hist, arco in ARGUMENTOS_LARGO.items():
        for i, pagina in enumerate(arco):
            for pat in _MUNDO_BAN:
                if re.search(pat, pagina, re.IGNORECASE):
                    errores.append(f"{hist} pág {i}: {pat}")
    assert not errores, "\n".join(errores)


# ── T5 · diccionarios por tema bien formados ─────────────────────────────────
def test_diccionarios_por_tema():
    errores = []
    for tema in TEMAS_CATALOGO:
        h = libro.HISTORIAS.get(tema)
        if not h:
            errores.append(f"{tema}: SIN entrada en libro.HISTORIAS (fallback)")
            continue
        if not h["amigos"].startswith("los "):
            errores.append(f"{tema}: amigos debe ser masculino plural «los ...»")
        d = h["desafio"]
        if d[0].isupper() or any(c in d for c in ":!¡"):
            errores.append(f"{tema}: desafio debe ser cláusula simple minúscula "
                           f"sin ':' ni '!' → «{d}»")
        primera = h["solucion"].split()[0]
        if not (primera.endswith("ó") or primera in ("le", "les")):
            errores.append(f"{tema}: solucion debe empezar con verbo en pasado "
                           f"→ «{h['solucion']}»")
        if not re.match(r"^(un|una|unas|unos)\b", h["tesoro"]):
            errores.append(f"{tema}: tesoro debe llevar artículo → «{h['tesoro']}»")
    assert not errores, "\n".join(errores)


# ── T6 · no repetición dentro de un libro ────────────────────────────────────
def _shingles(texto, n=6):
    palabras = re.findall(r"\w+", texto.lower())
    return {" ".join(palabras[i:i + n]) for i in range(len(palabras) - n + 1)}


def test_sin_repeticion_dentro_del_libro():
    # Sobre las PLANTILLAS (placeholders colapsados): un valor largo de {mundo}
    # («la sabana dorada del safari») generaría shingles repetidos legítimos.
    errores = []
    for hist, arco in ARGUMENTOS_LARGO.items():
        vistos = {}
        for i, p in enumerate(arco):
            plano = re.sub(r"\{\w+\}", "PH", p)
            for sh in _shingles(plano):
                if sh in vistos and vistos[sh] != i:
                    errores.append(f"{hist}: pág {vistos[sh]} y {i} repiten «{sh}»")
                vistos[sh] = i
    assert not errores, "\n".join(errores)


# ── T7 · escenas de ilustración ──────────────────────────────────────────────
# Poses que hacen inventar la 5ta pata o confundir al protagonista.
_ESCENA_BAN = ["dándose la mano", "dando la mano", "dan la mano",
               "chocan los cinco", "chocando los cinco", "choca los cinco",
               "aplaudiendo", "aplauden", "saludando", "saluda con la pata",
               "levantando una pata", "tomados de la mano", "abrazando a los"]
# «de la mano» solo se permite si la escena aclara que es un niño humano.
_MANO_OK = "no un animal"


def _todas_las_escenas():
    for hist, tabla in libro_ia._ESCENAS_POR_HISTORIA_LARGO.items():
        for idx, esc in tabla.items():
            yield f"LARGO {hist} idx{idx}", esc
    for hist, tabla in libro_ia._ESCENAS_POR_HISTORIA_EXT.items():
        for idx, esc in tabla.items():
            yield f"EXT {hist} idx{idx}", esc
    for hist, tabla in libro_ia._ESCENAS_POR_HISTORIA.items():
        for idx, esc in tabla.items():
            yield f"LEGADO {hist} idx{idx}", esc
    for i, esc in enumerate(libro_ia._ESCENAS):
        yield f"BASE idx{i}", esc


def test_escenas_sin_poses_prohibidas():
    errores = []
    for donde, esc in _todas_las_escenas():
        low = esc.lower()
        for ban in _ESCENA_BAN:
            if ban in low:
                errores.append(f"{donde}: «{ban}»")
        if "de la mano" in low and _MANO_OK not in low:
            errores.append(f"{donde}: «de la mano» sin aclarar (un niño, NO un animal)")
    assert not errores, "\n".join(errores)


def test_escenas_completas_por_historia():
    for hist in HISTORIAS_CATALOGO:
        tabla = libro_ia._ESCENAS_POR_HISTORIA_LARGO[hist]
        assert sorted(tabla) == list(range(2, 19)), hist


# Los temas con libro publicado NECESITAN imagen de referencia (sin ella el
# arte sale con personajes random — pasó con princesas).
_TEMAS_LIBROS_PUBLICADOS = ["safari", "bomberos", "superheroes", "campamento",
                            "circo", "princesas", "artistas", "monstruos"]


def test_temas_publicados_con_referencia():
    sin_ref = [t for t in _TEMAS_LIBROS_PUBLICADOS if not libro_ia.referencias(t)]
    assert not sin_ref, f"temas sin ia_maestra/stickers: {sin_ref}"


# Adjetivos gendered aplicados a {protagonista} en las escenas (el género se
# sustituye al armar el prompt: «una nena ... pensativo» queda mal).
_PROTA_ADJ_BAN = ["pensativo", "despierto", "atento", "maravillado", "rodeado",
                  "caído", "extrañado", "recostado", "sentado", "dormido",
                  "decidido", "concentrado", "acostado", "parado"]
_PROTA_ADJ_PREV_OK = ("gesto", "paso", "aire", "público")


def test_escenas_protagonista_sin_adjetivos_gendered():
    errores = []
    for donde, esc in _todas_las_escenas():
        if "{protagonista}" not in esc:
            continue
        palabras = re.findall(r"\w+", esc.lower())
        for j, w in enumerate(palabras):
            if w in _PROTA_ADJ_BAN and (j == 0 or palabras[j - 1] not in _PROTA_ADJ_PREV_OK):
                errores.append(f"{donde}: «{w}» concuerda mal si es nena")
    assert not errores, "\n".join(errores)


# ── versión corta coherente: las páginas cortas no pueden arrancar con
#    conectores que dependan de una página salteada ─────────────────────────
_CONECTORES_COLGADOS = re.compile(
    r"^(del otro lado|cuando volvieron|adentro|detrás de la piedra|"
    r"con esa lucecita|ya con|siguiendo las lucecitas|el viento)", re.IGNORECASE)


def test_version_corta_sin_antecedentes_colgados():
    errores = []
    for hist, arco in ARGUMENTOS_LARGO.items():
        for i in CORTO_IDX:
            if _CONECTORES_COLGADOS.match(arco[i].strip()):
                errores.append(f"{hist} pág {i}: arranque colgado en la versión "
                               f"corta → «{arco[i][:60]}...»")
    assert not errores, "\n".join(errores)
