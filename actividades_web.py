#!/usr/bin/env python3
"""actividades_web.py — Cuaderno de actividades INTERACTIVO (producto digital vivo).

El producto ES un link (/act/<token>): una web app táctil donde el chico juega
las mismas actividades del cuaderno imprimible (colorear, memotest, sopa de
letras, laberinto, contar, sumas…) con corrección automática, estrellas y
festejo. Espejo de audiolibro.py:

  - carpeta por token en actividades/<token>/ (gitignored, runtime)
  - manifest.json = existe/está listo; assets del tema copiados (autocontenido)
  - visor = actividades_player.html + actividades_player.js (plantillas del
    repo, se sirven en cada request → una mejora del player llega a TODOS los
    links ya vendidos) + data.json por token (la personalización viva)

El MISMO principio del motor: el código genera y VERIFICA (laberinto con
salida por BFS, sopa con todas las palabras colocadas, sudoku de solución
única — reusa los generadores determinísticos de cuaderno.py); el arte del
tema (stickers recortados, páginas para colorear IA, fondo de escena) se copia
al token. La banda de edad decide el menú de juegos, igual que _construir."""
import os, re, json, glob, math, time, zlib, random, secrets
from html import escape as _esc

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops

import piezas

BASEDIR = os.path.dirname(os.path.abspath(__file__))
ACT_DIR = os.path.join(BASEDIR, "actividades")
TEMPLATE_HTML = os.path.join(BASEDIR, "actividades_player.html")
TEMPLATE_JS = os.path.join(BASEDIR, "actividades_player.js")
AUDIO_DIR = os.path.join(BASEDIR, "audio_consignas")
VIGENCIA_DIAS = 7300         # igual que el audiolibro: respalda "Mis compras"
_TOKEN_RE = r"[A-Za-z0-9_-]{8,32}"

# ── Paletas por tema (elegidas a mano: cálidas, contraste AA en textos, un
#    acento fuerte + uno secundario; "espacio" es la única oscura a propósito) ──
PALETAS = {
    "safari":       {"bg": "#FBF3E4", "card": "#FFFFFF", "ink": "#4A3728", "ac": "#E07B2E", "ac2": "#57A05A", "soft": "#F5E3C4", "star": "#F2A93B"},
    "futbol":       {"bg": "#EFF6EF", "card": "#FFFFFF", "ink": "#1F3A2E", "ac": "#2E9E4F", "ac2": "#2563B6", "soft": "#DCEEDD", "star": "#F2A93B"},
    "princesas":    {"bg": "#FCF1F6", "card": "#FFFFFF", "ink": "#4C2A3D", "ac": "#D9569A", "ac2": "#8E5FC8", "soft": "#F8DCE9", "star": "#E8A426"},
    "monstruos":    {"bg": "#F3F0FA", "card": "#FFFFFF", "ink": "#31284A", "ac": "#7C5CD6", "ac2": "#2FA96A", "soft": "#E4DCF6", "star": "#F2A93B"},
    "superheroes":  {"bg": "#EFF4FC", "card": "#FFFFFF", "ink": "#1E2A4A", "ac": "#D63B34", "ac2": "#2563B6", "soft": "#DBE6F8", "star": "#F2A93B"},
    "superhéroes":  {"bg": "#EFF4FC", "card": "#FFFFFF", "ink": "#1E2A4A", "ac": "#D63B34", "ac2": "#2563B6", "soft": "#DBE6F8", "star": "#F2A93B"},
    "construccion": {"bg": "#FBF5E3", "card": "#FFFFFF", "ink": "#3E3222", "ac": "#DE9204", "ac2": "#4A6FA5", "soft": "#F6E9C1", "star": "#E07B2E"},
    "circo":        {"bg": "#FBF1E8", "card": "#FFFFFF", "ink": "#47262A", "ac": "#CE4747", "ac2": "#25938A", "soft": "#F7DECE", "star": "#F2A93B"},
    "bomberos":     {"bg": "#FBF0EB", "card": "#FFFFFF", "ink": "#3C2320", "ac": "#CE3E28", "ac2": "#DE9204", "soft": "#F7DACF", "star": "#F2A93B"},
    "campamento":   {"bg": "#F2F6EC", "card": "#FFFFFF", "ink": "#2F3B26", "ac": "#5F8B3B", "ac2": "#A06C3C", "soft": "#E1ECD4", "star": "#F2A93B"},
    "artistas":     {"bg": "#FBF4ED", "card": "#FFFFFF", "ink": "#3A2E3C", "ac": "#DB6844", "ac2": "#2E96A8", "soft": "#F6E1D2", "star": "#E8A426"},
    "aviadores":    {"bg": "#EDF5FB", "card": "#FFFFFF", "ink": "#243447", "ac": "#3577B4", "ac2": "#D96A5F", "soft": "#D8E8F6", "star": "#F2A93B"},
    # Pablo 13-jul-2026: era la única paleta oscura del catálogo ("fondo
    # espacial nocturno" a propósito) — con las cards de la galería mostrando
    # ahora el player REAL (no un mockup en fondo blanco fijo), se notaba
    # inconsistente al lado de los otros 11 temas. Repintada clara (mismo
    # criterio que el resto: bg pastel, card blanca) conservando el acento
    # violeta/turquesa "espacial" como color, no como fondo.
    "un-espacio-de-locura":
                    {"bg": "#EEF0FC", "card": "#FFFFFF", "ink": "#2B2A63", "ac": "#8E7DFF", "ac2": "#2FA9A0", "soft": "#E4E0FA", "star": "#F2A93B"},
}
_PALETA_DEFAULT = {"bg": "#FBF4EA", "card": "#FFFFFF", "ink": "#44372E", "ac": "#E0713C", "ac2": "#4E9C7E", "soft": "#F5E4CE", "star": "#F2A93B"}


def _paleta(tema):
    return dict(PALETAS.get(tema, _PALETA_DEFAULT))


def _banda(edad):
    """Banda de edad → menú y dificultad (mismo criterio que cuaderno._construir)."""
    try:
        e = int(str(edad).strip() or 5)
    except (TypeError, ValueError):
        e = 5
    return "mini" if e <= 3 else ("media" if e <= 5 else "grande")


# ── Menú por banda (orden = recorrido sugerido; cfg = perillas de dificultad).
#    Curado con la investigación 10-jul-2026: contar-tocando, patrón y memotest
#    son los de mayor valor educativo; sopa/sudoku recién para lectores. ──
def _menu(banda, edad):
    try:
        e = int(str(edad).strip() or 5)
    except (TypeError, ValueError):
        e = 5
    if banda == "mini":
        return [
            {"id": "contar",    "titulo": "¿Cuántos hay?",    "icono": "🖐️", "cfg": {"max": 3, "rondas": 5}},
            {"id": "colorear",  "titulo": "¡A pintar!",       "icono": "🎨", "cfg": {}},
            {"id": "memotest",  "titulo": "Memotest",         "icono": "🧠", "cfg": {"pares": 3}},
            {"id": "sombra",    "titulo": "Sombras",          "icono": "👤", "cfg": {"pares": 3, "rondas": 2}},
            {"id": "diferente", "titulo": "El distinto",      "icono": "🔍", "cfg": {"opciones": 3, "rondas": 5}},
            {"id": "tamano",    "titulo": "El más grande",    "icono": "📏", "cfg": {"rondas": 5}},
            {"id": "patron",    "titulo": "Seguí el patrón",  "icono": "🔁", "cfg": {"nivel": 1, "rondas": 5}},
            {"id": "simon",     "titulo": "Escuchá y repetí", "icono": "🎵", "cfg": {"colores": 3, "rondas": 4}},
            {"id": "agrupar",   "titulo": "¿Dónde va?",       "icono": "🧺", "cfg": {"canastas": 2, "rondas": 4}},
            {"id": "quefalta",  "titulo": "¿Qué falta?",      "icono": "❓", "cfg": {"items": 3, "rondas": 4}},
            {"id": "bingo",     "titulo": "Bingo de amigos",  "icono": "🎯", "cfg": {"tam": 4}},
        ]
    if banda == "media":
        m = [
            {"id": "contar",    "titulo": "¿Cuántos hay?",    "icono": "🖐️", "cfg": {"max": 6, "rondas": 5}},
            {"id": "colorear",  "titulo": "¡A pintar!",       "icono": "🎨", "cfg": {}},
            {"id": "memotest",  "titulo": "Memotest",         "icono": "🧠", "cfg": {"pares": 6}},
            {"id": "laberinto", "titulo": "El laberinto",     "icono": "🌀", "cfg": {"desde": 0}},
            {"id": "sombra",    "titulo": "Sombras",          "icono": "👤", "cfg": {"pares": 4, "rondas": 2}},
            {"id": "puntos",    "titulo": "Uní los puntos",   "icono": "✨", "cfg": {"figuras": ["estrella"]}},
            {"id": "patron",    "titulo": "Seguí el patrón",  "icono": "🔁", "cfg": {"nivel": 2, "rondas": 5}},
            {"id": "mas_menos", "titulo": "¿Dónde hay más?",  "icono": "⚖️", "cfg": {"max": 6, "rondas": 5}},
            # Sala de 4 Bimestre 1 (NAP): noción espacial arriba/abajo/
            # adentro/afuera — único contenido de ese bimestre sin ningún
            # juego hasta el 14-jul-2026 (ver docs/INFORME-ACTIVIDADES-PROGRESIVAS.md §5).
            {"id": "posicion",  "titulo": "¿Dónde está?",     "icono": "📦", "cfg": {"rondas": 5}},
            {"id": "diferente", "titulo": "El distinto",      "icono": "🔍", "cfg": {"opciones": 4, "rondas": 5}},
            {"id": "tamano",    "titulo": "El más grande",    "icono": "📏", "cfg": {"rondas": 5}},
            {"id": "simon",     "titulo": "Escuchá y repetí", "icono": "🎵", "cfg": {"colores": 4, "rondas": 5}},
            {"id": "agrupar",   "titulo": "¿Dónde va?",       "icono": "🧺", "cfg": {"canastas": 2, "rondas": 6}},
            {"id": "quefalta",  "titulo": "¿Qué falta?",      "icono": "❓", "cfg": {"items": 4, "rondas": 5}},
            {"id": "bingo",     "titulo": "Bingo de amigos",  "icono": "🎯", "cfg": {"tam": 6}},
        ]
        if e >= 5:
            m.append({"id": "sumas", "titulo": "Sumas", "icono": "➕", "cfg": {"max": 5, "rondas": 5}})
        if e == 4:
            # NAP Sala de 4 (docs/CURRICULUM-NAP-ARGENTINA.md): "conteo oral
            # hasta el 5" — hasta el 14-jul-2026 "contar" tenía el mismo
            # max=6 sin distinguir 4 de 5 años dentro de la banda "media".
            for item in m:
                if item["id"] == "contar":
                    item["cfg"] = {**item["cfg"], "max": 5}
        if e == 5:
            # NAP Sala de 5: "conteo oral hasta el 15" y "comparación de
            # colecciones". No llevamos "contar" literal a 15 objetos en
            # pantalla — el layout (targets táctiles ≥48px con separación,
            # skill §4b punto 6) se satura antes de eso; 8 es el techo
            # razonable sin comprometer el tamaño/separación de los targets.
            for item in m:
                if item["id"] in ("contar", "mas_menos"):
                    item["cfg"] = {**item["cfg"], "max": 8}
            # Sala de 5 Bimestre 2 (NAP): "conciencia fonológica — sílabas
            # (aplaudirlas)" — construcción nueva de verdad (no curación),
            # primer juego del motor con un componente de AUDIO real (no
            # solo efectos): escuchá la palabra, contá las partes. Lo pide
            # SOLO 5 años (a los 4 el eje del bimestre 1 es otro).
            m.append({"id": "silabas", "titulo": "¿Cuántas partes?", "icono": "👂", "cfg": {"rondas": 5}})
        return m
    g = [
        {"id": "memotest",  "titulo": "Memotest",         "icono": "🧠", "cfg": {"pares": 8}},
        {"id": "laberinto", "titulo": "El laberinto",     "icono": "🌀", "cfg": {"desde": 0}},
        # PROTOTIPO 14-jul-2026 (idea de Pablo: pensamiento computacional,
        # armar instrucciones y apretar Play para animar el recorrido).
        # Provisorio en la banda base mientras se valida la mecánica — no
        # es una decisión final de quedarse en las 7 edades.
        {"id": "programar_camino", "titulo": "Programá el camino", "icono": "🤖", "cfg": {}},
        {"id": "sopa",      "titulo": "Sopa de letras",   "icono": "🔤", "cfg": {}},
        {"id": "sudoku",    "titulo": "Sudoku",           "icono": "🧩", "cfg": {}},
        {"id": "sumas",     "titulo": "Sumas",            "icono": "➕", "cfg": {"max": 10, "rondas": 6}},
        {"id": "restas",    "titulo": "Restas",           "icono": "➖", "cfg": {"max": 10, "rondas": 6}},
        {"id": "serie",     "titulo": "La serie",         "icono": "🔢", "cfg": {"rondas": 6}},
        {"id": "patron",    "titulo": "Seguí el patrón",  "icono": "🔁", "cfg": {"nivel": 3, "rondas": 6}},
        {"id": "puntos",    "titulo": "Uní los puntos",   "icono": "✨", "cfg": {"figuras": ["estrella", "corazon"]}},
        {"id": "contar",    "titulo": "¿Cuántos hay?",    "icono": "🖐️", "cfg": {"max": 9, "rondas": 5}},
        {"id": "colorear",  "titulo": "¡A pintar!",       "icono": "🎨", "cfg": {}},
        {"id": "mas_menos", "titulo": "¿Dónde hay más?",  "icono": "⚖️", "cfg": {"max": 9, "rondas": 5}},
        {"id": "simon",     "titulo": "Escuchá y repetí", "icono": "🎵", "cfg": {"colores": 5, "rondas": 6}},
        {"id": "agrupar",   "titulo": "¿Dónde va?",       "icono": "🧺", "cfg": {"canastas": 3, "rondas": 8}},
        {"id": "quefalta",  "titulo": "¿Qué falta?",      "icono": "❓", "cfg": {"items": 5, "rondas": 6}},
        {"id": "bingo",     "titulo": "Bingo de amigos",  "icono": "🎯", "cfg": {"tam": 9}},
    ]
    # ── Fase 0A quick-win (19-jul-2026, docs/auditoria-dc-caba/) ──────────
    # Tope de "serie" creciente por grado. Antes SOLO e==6 subía el tope a 30
    # (NAP 1°) y el resto caía al default 16 del player → un chico de 6 años
    # recibía números MÁS ALTOS que uno de 12 (bug de dificultad invertida).
    # e==6 sigue puesto en su propio bloque más abajo (junto con simon).
    _SERIE_TOPE = {7: 50, 8: 80, 9: 120, 10: 200, 11: 300, 12: 500}
    if e in _SERIE_TOPE:
        for item in g:
            if item["id"] == "serie":
                item["cfg"] = {**item["cfg"], "tope": _SERIE_TOPE[e]}
    # Retirar de 4°-7° (e>=9) los juegos clavados en dificultad de inicial que
    # NO escalan con la edad y son el origen de la queja "muy fácil" de 4°:
    # sumas/restas cuentan sprites en pantalla (max 10, mecánica concreta de
    # nenes), contar/mas_menos ≤9, colorear/puntos sin anclaje curricular.
    # Cada grado conserva su contenido NAP propio (bloques if e==9..12).
    if e >= 9:
        _DROP_INICIAL = {"sumas", "restas", "contar", "mas_menos", "colorear", "puntos"}
        g = [it for it in g if it["id"] not in _DROP_INICIAL]
    # ─────────────────────────────────────────────────────────────────────
    if e == 6:
        # NAP 1° grado Bimestre 1: "números del 1 al 30", "anterior y
        # posterior" — "serie" ya hacía justo esto (¿qué número falta en la
        # secuencia?) pero con techo fijo ~16; con cfg.tope explícito llega
        # a 30 sin tocar la mecánica (14-jul-2026).
        # "Escuchá y repetí" con menos botones para el año más chico de esta
        # banda (15-jul-2026, Pablo: escala de dificultad por grado — ver
        # también e==7/8/9/10/11/12 más abajo).
        for item in g:
            if item["id"] == "serie":
                item["cfg"] = {**item["cfg"], "tope": 30}
            if item["id"] == "simon":
                item["cfg"] = {**item["cfg"], "colores": 4}
        # NAP 1° grado Bimestre 2: "sílabas directas (consonante+vocal)...
        # construir palabras arrastrando sílabas desordenadas" — Pablo ya
        # había traído esta idea. Reusa el pipeline de audio de silabas
        # (Sala de 5); a diferencia de silabas (contar CUÁNTAS partes),
        # acá arma la palabra completa tocando sus sílabas EN ORDEN.
        g.append({"id": "armar_palabra", "titulo": "Armá la palabra", "icono": "🧱", "cfg": {"rondas": 5}})
        # NAP 1° grado Bimestre 1 "Ideas web": "ordenar alfabéticamente".
        g.append({"id": "abecedario", "titulo": "El abecedario", "icono": "🔡", "cfg": {"rondas": 5, "letras": 4}})
        # NAP 1° grado Bimestre 2 "Ideas web": "suma rápida — tocar burbujas
        # que sumen 10".
        g.append({"id": "suma_rapida", "titulo": "Suma rápida", "icono": "🫧", "cfg": {"rondas": 5}})
        # NAP 1° grado Bimestre 3 "Ideas web": "clasificar ¿Campo o Ciudad?"
        # y "unir planta con su fruto/semilla".
        # rondas=10 (14-jul-2026): CAMPO_CIUDAD_BANCO ya tiene 10 ítems —
        # sin repetir contenido en una sesión (Pablo: "que tenga unas 10
        # preguntas... por lo menos edades más grandes" — acá era gratis).
        g.append({"id": "campo_ciudad", "titulo": "¿Campo o ciudad?", "icono": "🚜", "cfg": {"rondas": 10}})
        # rondas=6 (14-jul-2026): PLANTA_FRUTO_BANCO creció de 4 a 6 —
        # techo honesto para un juego 100% emoji (ver comentario del banco).
        g.append({"id": "planta_fruto", "titulo": "¿Qué fruto da?", "icono": "🌳", "cfg": {"rondas": 6}})
        # NAP 1° grado Bimestre 4 "Ideas web": "trivia de materiales" y
        # "rompecabezas numérico de la grilla 1-100".
        # rondas=10 (14-jul-2026): MATERIALES_BANCO creció de 6 a 10.
        g.append({"id": "materiales", "titulo": "¿De qué material es?", "icono": "🪟", "cfg": {"rondas": 10}})
        g.append({"id": "grilla100", "titulo": "La grilla numérica", "icono": "🧮", "cfg": {"rondas": 6}})
        # ── Rollout DC CABA · 1° grado (19-jul-2026, grado-1.md): numeración
        # (recta con rango chico 0-20→0-100) + ordenar números de menor a mayor.
        # Los moldes de 3°+ (fracciones, comprensión de 4°…) NO aplican a 6 años;
        # el resto de 1° es contenido fonético/lector age-específico (fase engrosar).
        g.append({"id": "recta_numerica", "titulo": "Recta gigante", "icono": "📍", "cfg": {"rondas": 8, "max1": 20, "max2": 100}})
        g.append({"id": "ordenar_numeros", "titulo": "Ordená los números", "icono": "🪜", "cfg": {"rondas": 8, "max": 20, "cant": 3}})
        # 2ª tanda 1° (19-jul-2026, nivelación age-específica): fonética (letra
        # inicial, con AUDIO) + anterior/siguiente de un número (NAP nodal).
        g.append({"id": "letra_inicial", "titulo": "¿Con qué letra empieza?", "icono": "🅰️", "cfg": {"rondas": 8}})
        g.append({"id": "anterior_siguiente", "titulo": "Antes y después", "icono": "➡️", "cfg": {"rondas": 10, "max": 100}})
    if e == 7:
        # 2° grado (14-jul-2026): mismo criterio que 1° grado — un juego
        # por cada "Idea web" que el propio NAP sugiere por bimestre.
        # Bimestre 1: sustantivos comunes/propios + sumas a números redondos.
        # rondas=10 (14-jul-2026): SUSTANTIVOS_BANCO ya tiene 10 ítems.
        g.append({"id": "sustantivos", "titulo": "Común o propio", "icono": "📛", "cfg": {"rondas": 10}})
        g.append({"id": "sumas_redondas", "titulo": "Sumas redondas", "icono": "🔟", "cfg": {"rondas": 5}})
        # Bimestre 2: sinónimos/antónimos + suma repetida → multiplicación.
        # rondas=10 (14-jul-2026): SINANT_BANCO creció de 6 a 10.
        g.append({"id": "sinonimos_antonimos", "titulo": "Sinónimos y antónimos", "icono": "🔀", "cfg": {"rondas": 10}})
        g.append({"id": "multiplicacion_concepto", "titulo": "De la suma a la multiplicación", "icono": "✖️", "cfg": {"rondas": 5}})
        # Bimestre 3: conductor/aislante + familia de palabras.
        # rondas=10 (14-jul-2026): CONDUCTOR_BANCO creció de 8 a 10.
        g.append({"id": "conductor_aislante", "titulo": "¿Se calienta rápido?", "icono": "🍳", "cfg": {"rondas": 10}})
        # rondas=10 (14-jul-2026): FAMILIA_BANCO creció de 5 a 10.
        g.append({"id": "familia_palabras", "titulo": "Familia de palabras", "icono": "👪", "cfg": {"rondas": 10}})
        # Bimestre 4: trivia espacial + tablas contrarreloj.
        # rondas=10 (14-jul-2026): ESPACIAL_BANCO creció de 6 a 10.
        g.append({"id": "trivia_espacial", "titulo": "Día, noche o ambos", "icono": "🌗", "cfg": {"rondas": 10}})
        g.append({"id": "tablas_contrarreloj", "titulo": "Tablas contrarreloj", "icono": "⏱️", "cfg": {"rondas": 6}})
        # ── Rollout DC CABA · 2° grado (19-jul-2026, grado-2.md): numeración y
        # comparación de números hasta 1.000 (recta, comparar mayor/menor/medio,
        # ordenar). Molds age-appropiados; el resto de 2° es lengua/ciencias
        # age-específico (fase engrosar).
        g.append({"id": "recta_numerica", "titulo": "Recta gigante", "icono": "📍", "cfg": {"rondas": 8, "max1": 100, "max2": 1000}})
        g.append({"id": "comparar_numeros", "titulo": "Tres en fila", "icono": "🥇", "cfg": {"rondas": 10, "max": 999}})
        g.append({"id": "ordenar_numeros", "titulo": "Ordená los números", "icono": "🪜", "cfg": {"rondas": 8, "max": 100, "cant": 4}})
        # 2ª tanda 2° (19-jul-2026, nivelación): contar de a 2/5/10 (NAP nodal) +
        # anterior/siguiente con números hasta 1.000.
        g.append({"id": "contar_saltando", "titulo": "Contar saltando", "icono": "🦘", "cfg": {"rondas": 10}})
        g.append({"id": "anterior_siguiente", "titulo": "Antes y después", "icono": "➡️", "cfg": {"rondas": 10, "max": 1000}})
    if e == 8:
        # 3° grado (14-jul-2026): mismo criterio — un juego por cada "Idea
        # web" del NAP, un bimestre a la vez. NO hizo falta separar la
        # banda "grande" en una banda propia todavía (el hallazgo original
        # del informe §1 sobre la banda sin tope sigue vigente, pero recién
        # importa cuando un año necesite CAMBIAR contenido base compartido,
        # no solo AGREGAR contenido propio con `if e == X` — ver informe §5g).
        # "Escuchá y repetí" 2 filas de 3 (15-jul-2026, Pablo).
        for item in g:
            if item["id"] == "simon":
                item["cfg"] = {**item["cfg"], "colores": 6, "filas": 2}
        # Bimestre 1: unir animal con su comida + sustantivo/adjetivo/verbo.
        # rondas=10 (14-jul-2026): ANIMAL_COMIDA_BANCO creció de 5 a 10.
        g.append({"id": "animal_comida", "titulo": "¿Qué come?", "icono": "🦁", "cfg": {"rondas": 10}})
        # rondas=10 (14-jul-2026): PARTES_ORACION_BANCO creció de 9 a 10.
        g.append({"id": "partes_oracion", "titulo": "Sustantivo, adjetivo o verbo", "icono": "📚", "cfg": {"rondas": 10}})
        # Bimestre 2: tabla pitagórica + tiempos verbales.
        g.append({"id": "tabla_pitagorica", "titulo": "Busca el tesoro", "icono": "🗝️", "cfg": {"rondas": 6}})
        # rondas=10 (14-jul-2026): TIEMPOS_BANCO creció de 9 a 10.
        g.append({"id": "tiempos_verbales", "titulo": "Pasado, presente o futuro", "icono": "⏳", "cfg": {"rondas": 10}})
        # Bimestre 3: estaciones del año + cuerpos geométricos.
        # rondas=10 (14-jul-2026): ESTACIONES_BANCO creció de 4 a 10.
        g.append({"id": "estaciones", "titulo": "¿Qué estación es?", "icono": "🍂", "cfg": {"rondas": 10}})
        g.append({"id": "cuerpos_geometricos", "titulo": "Caras y vértices", "icono": "🧊", "cfg": {"rondas": 5}})
        # Bimestre 4: separador de mezclas + cajero automático.
        # rondas=10 (14-jul-2026): MEZCLAS_BANCO creció de 4 a 10.
        g.append({"id": "separador_mezclas", "titulo": "Separá la mezcla", "icono": "🧪", "cfg": {"rondas": 10}})
        g.append({"id": "cajero_automatico", "titulo": "Cajero automático", "icono": "💵", "cfg": {"rondas": 5}})
        # ── Rollout DC CABA · 3° grado (19-jul-2026, docs/auditoria-dc-caba/
        # grado-3.md): réplica del modelo de 4°. 3 actividades nuevas + 2 reusadas
        # de los moldes ya construidos, y limpieza de los juegos de inicial (como
        # Fase 0A en 4°) + separador_mezclas (reemplazado por estados_materia).
        g.append({"id": "reparto_con_resto", "titulo": "Reparto con resto", "icono": "➗", "cfg": {"rondas": 10}})
        g.append({"id": "comparar_numeros", "titulo": "Tres en fila", "icono": "🥇", "cfg": {"rondas": 10}})
        g.append({"id": "estados_materia", "titulo": "Sólido, líquido o gas", "icono": "🌡️", "cfg": {"rondas": 10}})
        g.append({"id": "comprension_lectora", "titulo": "Detective de textos", "icono": "🔎", "cfg": {"rondas": 8}})
        g.append({"id": "recta_numerica", "titulo": "Recta gigante", "icono": "📍", "cfg": {"rondas": 10, "max1": 1000, "max2": 10000}})
        # 2ª tanda 3° (19-jul-2026, nivelación): problemas de 1 paso (M13), orden
        # alfabético (L4, mecánica ordenar) y ortografía (L3: -aba, z→ces, mb/nv).
        g.append({"id": "problemas_3ro", "titulo": "Problemas", "icono": "🤔", "cfg": {"rondas": 10}})
        g.append({"id": "orden_alfabetico", "titulo": "De la A a la Z", "icono": "🔡", "cfg": {"rondas": 8}})
        g.append({"id": "ortografia_3ro", "titulo": "¿Cómo se escribe?", "icono": "✍️", "cfg": {"rondas": 10}})
        _drop3 = {"sumas", "restas", "contar", "colorear", "puntos", "mas_menos", "patron", "separador_mezclas"}
        g[:] = [it for it in g if it["id"] not in _drop3]
    if e == 9:
        # 4° grado (14-jul-2026): mismo criterio — un juego por cada "Idea
        # web" del NAP. Dos "Ideas web" del año (rompecabezas geográfico
        # con mapa real, transportador interactivo) se simplificaron a
        # trivia por necesitar assets/mecánicas que el motor no tiene hoy
        # — ver informe §5h.
        # "Escuchá y repetí" 2 filas de 4 (15-jul-2026, Pablo — igual en 5°).
        for item in g:
            if item["id"] == "simon":
                item["cfg"] = {**item["cfg"], "colores": 8, "filas": 2}
        # M17 "Tablas ninja" (19-jul-2026, docs/auditoria-dc-caba/grado-4.md):
        # PRIMERA actividad del rollout de contenido de la auditoría DC CABA.
        # Fluidez de la tabla pitagórica —el gap #1 de 4°: hoy no hay NINGÚN
        # juego multiplicativo—. Generada, con distractores por misconception
        # (tabla vecina, suma en vez de producto) y explicación del porqué
        # (Capa 0 · C3/C4). Pedida por los 3 revisores del panel; "abre cada
        # sesión de Matemática" (informe §5h / dossier de 4°).
        g.append({"id": "tablas_ninja", "titulo": "Tablas ninja", "icono": "🥷", "cfg": {"rondas": 10, "nivel": 1}})
        # M5 "Fábrica de multiplicar" + M6 "La división" (19-jul-2026, rollout
        # de contenido DC CABA): las dos patas del gap #1 de 4° (multiplicación
        # más allá de tablas + división), completan el corazón operatorio con
        # Tablas ninja. Trivia generada con distractores por misconception (C4)
        # y explicación del porqué (C3) — mismo molde que tablas_ninja.
        g.append({"id": "multiplicar", "titulo": "Fábrica de multiplicar", "icono": "✖️", "cfg": {"rondas": 10, "nivel": 1}})
        g.append({"id": "dividir", "titulo": "La división", "icono": "➗", "cfg": {"rondas": 10, "nivel": 1}})
        # Bimestre 1: abstracto/concreto + provincia → región.
        # rondas=10 (14-jul-2026): ABSTRACTOS_BANCO creció de 8 a 10.
        g.append({"id": "abstractos_concretos", "titulo": "Abstracto o concreto", "icono": "💭", "cfg": {"rondas": 10}})
        # rondas=10 (14-jul-2026): PROVINCIAS_BANCO ya tiene 10 ítems.
        g.append({"id": "provincias_region", "titulo": "¿De qué región es?", "icono": "🗺️", "cfg": {"rondas": 10}})
        # Bimestre 2: acentuación + fotosíntesis (el intruso).
        # rondas=10 (14-jul-2026): ACENTUACION_BANCO creció de 9 a 10.
        g.append({"id": "acentuacion", "titulo": "Aguda, grave o esdrújula", "icono": "🚂", "cfg": {"rondas": 10}})
        g.append({"id": "fotosintesis", "titulo": "¿Qué no necesita la planta?", "icono": "🌱", "cfg": {"rondas": 5}})
        # Bimestre 3: laboratorio eléctrico + fracciones equivalentes.
        # rondas=10 (14-jul-2026): ELECTRICO_BANCO creció de 8 a 10.
        g.append({"id": "laboratorio_electrico", "titulo": "Laboratorio eléctrico", "icono": "🔌", "cfg": {"rondas": 10}})
        # rondas=10 (14-jul-2026): FRACCIONES_BANCO tiene 20 ítems, de sobra.
        g.append({"id": "fracciones_equivalentes", "titulo": "Fracciones equivalentes", "icono": "🍕", "cfg": {"rondas": 10}})
        # M10 "Duelo de fracciones" (19-jul-2026, rollout DC CABA): comparación
        # de fracciones CON BARRAS (CPA), ataca la misconception #1 (1/4 > 1/2
        # porque 4>2). Es el eje NODAL de fracciones de 4° que faltaba
        # (fracciones_equivalentes es solo "ampliación"). C3/C4.
        g.append({"id": "duelo_fracciones", "titulo": "Duelo de fracciones", "icono": "🍫", "cfg": {"rondas": 10}})
        # M8 "Reparto justo" + M9 "Completar el entero" (19-jul-2026, rollout DC
        # CABA): fracción como resultado de repartir, y fracciones en la medida
        # (litros/kilos, qué falta para 1). Ambas con barras CPA + C3/C4. Completan
        # el arranque del eje nodal de fracciones de 4° con duelo_fracciones.
        g.append({"id": "reparto_fracciones", "titulo": "Reparto justo", "icono": "🍰", "cfg": {"rondas": 10}})
        g.append({"id": "completar_entero", "titulo": "Completar el entero", "icono": "🥛", "cfg": {"rondas": 10}})
        # M11 decimales + M7 problemas + L10 plurales-z (19-jul-2026, rollout DC
        # CABA): decimales en uso social (misconception 12,45>12,5), problemas
        # aplicados de ×/÷ (operación equivocada como distractor), y plurales de
        # palabras con -z (z→c). Todas con misconception distractors + C3.
        g.append({"id": "duelo_decimales", "titulo": "Duelo de decimales", "icono": "💲", "cfg": {"rondas": 10}})
        g.append({"id": "problemas_mult_div", "titulo": "Problemas de verdad", "icono": "🤔", "cfg": {"rondas": 10}})
        g.append({"id": "plurales_z", "titulo": "Plurales con Z", "icono": "📝", "cfg": {"rondas": 10}})
        # S3 línea de tiempo + L15 historia en orden (19-jul-2026): primeras
        # actividades sobre la MECÁNICA NUEVA "ordenar" (commit-then-check), que
        # el motor no tenía. Línea de tiempo colonial (Sociales) y ordenar el
        # cuento (Lengua). Reusan la misma mecánica.
        g.append({"id": "linea_tiempo", "titulo": "Línea de tiempo", "icono": "🕰️", "cfg": {"rondas": 8}})
        g.append({"id": "historia_orden", "titulo": "Ordená el cuento", "icono": "📖", "cfg": {"rondas": 8}})
        # M1 "Recta gigante" (19-jul-2026): MECÁNICA NUEVA de recta numérica —
        # ubicar un número por zonas en la recta (0-10.000 → 0-100.000).
        # Proporcionalidad/orden de magnitud, con explicación del tramo (C3).
        g.append({"id": "recta_numerica", "titulo": "Recta gigante", "icono": "📍", "cfg": {"rondas": 10}})
        # L9/L17 comprensión lectora (19-jul-2026): MECÁNICA NUEVA de leer un texto
        # y responder, incluidas preguntas INFERENCIALES (deducir de pistas). Era
        # el hueco de Lengua más grande de 4°. Banco de 4 textos × 2 preguntas.
        g.append({"id": "comprension_lectora", "titulo": "Detective de textos", "icono": "🔎", "cfg": {"rondas": 8}})
        # Bimestre 4: ángulos + prefijos.
        # rondas=10 (14-jul-2026): ANGULOS_BANCO creció de 7 a 10.
        g.append({"id": "angulos", "titulo": "Agudo, recto u obtuso", "icono": "📐", "cfg": {"rondas": 10}})
        g.append({"id": "prefijos_sufijos", "titulo": "Palabras nuevas", "icono": "🔗", "cfg": {"rondas": 5}})
        # Pablo 15-jul-2026, probando el link en vivo: "las sumas en 4°
        # grado son de 4 a 5 cifras y en las actividades parecen muy
        # fáciles para esa edad". El `sumas` genérico (conteo de sprites,
        # tope=10 FIJO para 1° a 7° grado por igual) no puede representar
        # 4-5 cifras — reemplazado acá por el algoritmo escrito en
        # columnas (NAP Bimestre 1: "números hasta 10.000-50.000...
        # propiedades de suma y resta"), único año hasta ahora que
        # reemplaza un juego base en vez de solo agregar — mismo criterio
        # que informe §5g (banda "grande" sin tope, recién importa cuando
        # un año necesita CAMBIAR contenido compartido, no solo sumar).
        # Alcance acordado con Pablo: solo 4° grado por ahora — 3°/5°-7°
        # siguen con el `sumas`/`restas` genérico hasta la próxima pasada.
        g[:] = [item for item in g if item["id"] != "sumas"]
        g.append({"id": "suma_columnas", "titulo": "Suma con cifras grandes", "icono": "🧮", "cfg": {"rondas": 6}})
    if e == 10:
        # 5° grado (14-jul-2026): mismo criterio — un juego por cada "Idea
        # web" del NAP.
        # "Escuchá y repetí" 2 filas de 4, igual que 4° (15-jul-2026, Pablo).
        for item in g:
            if item["id"] == "simon":
                item["cfg"] = {**item["cfg"], "colores": 8, "filas": 2}
        # Bimestre 1: trivia colonial + camino digestivo.
        # rondas=10 (14-jul-2026): COLONIAL_BANCO creció de 5 a 10.
        g.append({"id": "trivia_colonial", "titulo": "Vida colonial", "icono": "🏛️", "cfg": {"rondas": 10}})
        g.append({"id": "camino_digestivo", "titulo": "El camino digestivo", "icono": "🍽️", "cfg": {"rondas": 4}})
        # Bimestre 2: fracciones nivel 2 + análisis sintáctico contrarreloj.
        # rondas=10 (14-jul-2026): FRACCIONES_AVANZADO_BANCO tiene 20 ítems, de sobra.
        g.append({"id": "fracciones_avanzado", "titulo": "Fracciones equivalentes II", "icono": "🥧", "cfg": {"rondas": 10}})
        # rondas=10 (14-jul-2026): SINTACTICO_BANCO creció de 6 a 10.
        g.append({"id": "analisis_sintactico", "titulo": "Núcleo del sujeto o predicado", "icono": "✏️", "cfg": {"rondas": 10}})
        # Bimestre 3: pago exacto + actividad económica por región.
        g.append({"id": "pago_exacto", "titulo": "Pago exacto", "icono": "🪙", "cfg": {"rondas": 5}})
        # rondas=10 (14-jul-2026): ECONOMIA_BANCO creció de 6 a 10.
        g.append({"id": "actividad_economica", "titulo": "¿Qué se produce acá?", "icono": "🌾", "cfg": {"rondas": 10}})
        # Bimestre 4: planta potabilizadora + derechos y constitución.
        g.append({"id": "planta_potabilizadora", "titulo": "Planta potabilizadora", "icono": "💧", "cfg": {"rondas": 4}})
        # rondas=10 (14-jul-2026): DERECHOS_BANCO creció de 5 a 10.
        g.append({"id": "derechos_constitucion", "titulo": "Derechos y Constitución", "icono": "📜", "cfg": {"rondas": 10}})
        # ── Rollout DC CABA · 5° grado (19-jul-2026, docs/auditoria-dc-caba/
        # grado-5.md): réplica del modelo. Ataca los 2 gaps más grandes del
        # dossier —"cero lectura" y "cero multiplicación/división en 5°"— reusando
        # moldes ya construidos, + 1 actividad nueva de Lengua (conectores, L16).
        g.append({"id": "conectores", "titulo": "El conector justo", "icono": "🔗", "cfg": {"rondas": 10}})
        g.append({"id": "tablas_ninja", "titulo": "Tablas ninja", "icono": "🥷", "cfg": {"rondas": 10, "nivel": 2}})
        g.append({"id": "dividir", "titulo": "La división", "icono": "➗", "cfg": {"rondas": 10, "nivel": 2}})
        g.append({"id": "comprension_lectora", "titulo": "Detective de textos", "icono": "🔎", "cfg": {"rondas": 8}})
        g.append({"id": "duelo_decimales", "titulo": "Duelo de decimales", "icono": "💲", "cfg": {"rondas": 10}})
        g.append({"id": "duelo_fracciones", "titulo": "Duelo de fracciones", "icono": "🍫", "cfg": {"rondas": 10}})
        g.append({"id": "recta_numerica", "titulo": "Recta gigante", "icono": "📍", "cfg": {"rondas": 10, "max1": 100000, "max2": 1000000}})
        # 2ª tanda 5° (19-jul-2026): actividades PROPIAS del dossier de 5° (no
        # moldes reusados), para nivelar 5° hacia su núcleo siguiendo la curva
        # creciente del DC (análisis de balance de actividades).
        g.append({"id": "equivalencias_medida", "titulo": "Equivalencias de medida", "icono": "📏", "cfg": {"rondas": 10}})
        g.append({"id": "verbos_pasado", "titulo": "¿Cantó o cantaba?", "icono": "⏪", "cfg": {"rondas": 10}})
        g.append({"id": "buenos_aires", "titulo": "Mi Buenos Aires querido", "icono": "🏙️", "cfg": {"rondas": 10}})
        # 3ª tanda 5° (19-jul-2026, nivelación): más nodales del dossier —
        # equivalencia decimal↔fracción, suma de fracciones (igual denom.) y
        # astronomía (el Sol/la Luna).
        g.append({"id": "decimales_fraccion", "titulo": "Del décimo a la coma", "icono": "🔟", "cfg": {"rondas": 10}})
        g.append({"id": "suma_fracciones", "titulo": "Sumá fracciones", "icono": "➕", "cfg": {"rondas": 10}})
        g.append({"id": "detectives_cielo", "titulo": "Detectives del cielo", "icono": "🌙", "cfg": {"rondas": 10}})
    if e == 11:
        # 6° grado (14-jul-2026): mismo criterio — un juego por cada "Idea
        # web" del NAP.
        # "Escuchá y repetí" 3 filas de 3, igual que 7° (15-jul-2026, Pablo).
        for item in g:
            if item["id"] == "simon":
                item["cfg"] = {**item["cfg"], "colores": 9, "filas": 3}
        # Bimestre 1: partes de la célula + hechos vs. opiniones.
        # rondas=10 (14-jul-2026): CELULA_BANCO creció de 4 a 10.
        g.append({"id": "celula_partes", "titulo": "Partes de la célula", "icono": "🔬", "cfg": {"rondas": 10}})
        # rondas=10 (14-jul-2026): HECHOS_OPINIONES_BANCO creció de 6 a 10.
        g.append({"id": "hechos_opiniones", "titulo": "Hecho u opinión", "icono": "📰", "cfg": {"rondas": 10}})
        # Bimestre 2: sistema nervioso + viaje del inmigrante.
        # rondas=10 (14-jul-2026): NERVIOSO_BANCO creció de 5 a 10.
        g.append({"id": "sistema_nervioso", "titulo": "Sistema nervioso", "icono": "🫨", "cfg": {"rondas": 10}})
        g.append({"id": "viaje_inmigrante", "titulo": "El viaje del inmigrante", "icono": "🚢", "cfg": {"rondas": 4}})
        # Bimestre 3: fracción de una cantidad + sufragio argentino.
        # rondas=10 (14-jul-2026): FRACCION_CANTIDAD_BANCO creció de 5 a 10.
        g.append({"id": "fraccion_de_cantidad", "titulo": "Fracción de una cantidad", "icono": "➗", "cfg": {"rondas": 10}})
        # rondas=10 (14-jul-2026): SUFRAGIO_BANCO creció de 4 a 10.
        g.append({"id": "sufragio_argentina", "titulo": "El voto en Argentina", "icono": "🗳️", "cfg": {"rondas": 10}})
        # Bimestre 4: energía renovable + polígonos.
        # rondas=10 (14-jul-2026): ENERGIA_BANCO creció de 7 a 10.
        g.append({"id": "energia_renovable", "titulo": "¿Renovable o no?", "icono": "⚡", "cfg": {"rondas": 10}})
        # rondas=10 (14-jul-2026): POLIGONOS_BANCO creció de 6 a 10.
        g.append({"id": "poligonos_lados", "titulo": "¿Cuántos lados tiene?", "icono": "⬡", "cfg": {"rondas": 10}})
        # ── Rollout DC CABA · 6° grado (19-jul-2026, docs/auditoria-dc-caba/
        # grado-6.md): réplica del modelo. Cierra los gaps de lectura,
        # mult/división y racionales reusando los moldes con dificultad de 6°.
        g.append({"id": "tablas_ninja", "titulo": "Tablas ninja", "icono": "🥷", "cfg": {"rondas": 10, "nivel": 3}})
        g.append({"id": "dividir", "titulo": "La división", "icono": "🧮", "cfg": {"rondas": 10, "nivel": 2}})
        g.append({"id": "comprension_lectora", "titulo": "Detective de textos", "icono": "🔎", "cfg": {"rondas": 8}})
        g.append({"id": "duelo_fracciones", "titulo": "Duelo de fracciones", "icono": "🍫", "cfg": {"rondas": 10}})
        g.append({"id": "duelo_decimales", "titulo": "Duelo de decimales", "icono": "💲", "cfg": {"rondas": 10}})
        g.append({"id": "recta_numerica", "titulo": "Recta gigante", "icono": "📍", "cfg": {"rondas": 10, "max1": 100000, "max2": 1000000}})
        g.append({"id": "conectores", "titulo": "El conector justo", "icono": "🔗", "cfg": {"rondas": 10}})
        # 2ª tanda 6° (19-jul-2026, nivelación): actividades PROPIAS del dossier
        # de 6° — los 3 gaps de matemática (primos, jerarquía de operaciones,
        # porcentaje de una cantidad). Nodales de 6°.
        g.append({"id": "numeros_primos", "titulo": "¿Cuál es primo?", "icono": "✳️", "cfg": {"rondas": 10}})
        g.append({"id": "jerarquia_operaciones", "titulo": "Orden de las operaciones", "icono": "🧾", "cfg": {"rondas": 10}})
        g.append({"id": "porcentajes", "titulo": "El porcentaje justo", "icono": "💯", "cfg": {"rondas": 10}})
        # 3ª tanda 6° (19-jul-2026, nivelación): cuadriláteros (M15a), producto de
        # fracciones, e historia de la organización nacional 1862-1930.
        g.append({"id": "cuadrilateros", "titulo": "Cuadriláteros", "icono": "⬜", "cfg": {"rondas": 10}})
        g.append({"id": "multiplicar_fracciones", "titulo": "Producto de fracciones", "icono": "✖️", "cfg": {"rondas": 10}})
        g.append({"id": "organizacion_nacional", "titulo": "La organización nacional", "icono": "🚂", "cfg": {"rondas": 10}})
    if e == 12:
        # 7° grado (14-jul-2026, año de egreso, fin del NAP) — mismo
        # criterio: un juego por cada "Idea web" del NAP.
        # "Escuchá y repetí" 3 filas de 3, igual que 6° (15-jul-2026, Pablo).
        for item in g:
            if item["id"] == "simon":
                item["cfg"] = {**item["cfg"], "colores": 9, "filas": 3}
        # Bimestre 1: traductor algebraico + sistema solar (terrestre/gaseoso).
        # rondas=10 (14-jul-2026): ALGEBRA_BANCO creció de 6 a 10.
        g.append({"id": "traductor_algebraico", "titulo": "Traductor algebraico", "icono": "🧮", "cfg": {"rondas": 10}})
        # rondas=8 (14-jul-2026): PLANETAS_BANCO se queda en 8 (techo real —
        # son los 8 planetas del sistema solar, ver comentario del banco).
        g.append({"id": "planetas_tipo", "titulo": "¿Terrestre o gaseoso?", "icono": "🪐", "cfg": {"rondas": 8}})
        # Bimestre 2: línea de tiempo de la democracia + aparato reproductor.
        g.append({"id": "linea_democracia", "titulo": "Línea de tiempo: la democracia", "icono": "🕊️", "cfg": {"rondas": 4}})
        # rondas=10 (14-jul-2026): REPRODUCTOR_BANCO creció de 5 a 10.
        g.append({"id": "sistema_reproductor", "titulo": "Aparato reproductor", "icono": "🧬", "cfg": {"rondas": 10}})
        # Bimestre 3: estadística (media) + red trófica.
        # rondas=10 (14-jul-2026): ESTADISTICA_BANCO creció de 6 a 10.
        g.append({"id": "estadistica_datos", "titulo": "Media, moda o mediana", "icono": "📊", "cfg": {"rondas": 10}})
        # rondas=10 (14-jul-2026): RED_TROFICA_BANCO creció de 7 a 10.
        g.append({"id": "red_trofica", "titulo": "Red trófica", "icono": "🕸️", "cfg": {"rondas": 10}})
        # Bimestre 4: área de figuras compuestas + escape room de egreso.
        # rondas=10 (14-jul-2026): AREA_BANCO creció de 5 a 10.
        g.append({"id": "area_perimetro", "titulo": "Área de la habitación", "icono": "🏠", "cfg": {"rondas": 10}})
        # rondas=10 (14-jul-2026): ESCAPE_ROOM_BANCO creció de 8 a 10.
        g.append({"id": "escape_room_egreso", "titulo": "Escape room de egreso", "icono": "🔐", "cfg": {"rondas": 10}})
        # ── Rollout DC CABA · 7° grado (19-jul-2026, docs/auditoria-dc-caba/
        # grado-7.md): réplica del modelo. Cierra los gaps de lectura,
        # mult/división y racionales reusando los moldes con la máxima dificultad.
        g.append({"id": "tablas_ninja", "titulo": "Tablas ninja", "icono": "🥷", "cfg": {"rondas": 10, "nivel": 3}})
        g.append({"id": "dividir", "titulo": "La división", "icono": "➗", "cfg": {"rondas": 10, "nivel": 2}})
        g.append({"id": "comprension_lectora", "titulo": "Detective de textos", "icono": "🔎", "cfg": {"rondas": 8}})
        g.append({"id": "duelo_fracciones", "titulo": "Duelo de fracciones", "icono": "🍫", "cfg": {"rondas": 10}})
        g.append({"id": "duelo_decimales", "titulo": "Duelo de decimales", "icono": "💲", "cfg": {"rondas": 10}})
        g.append({"id": "recta_numerica", "titulo": "Recta gigante", "icono": "📍", "cfg": {"rondas": 10, "max1": 100000, "max2": 1000000}})
        g.append({"id": "conectores", "titulo": "El conector justo", "icono": "🔗", "cfg": {"rondas": 10}})
        # 2ª tanda 7° (19-jul-2026, nivelación): actividades PROPIAS del dossier
        # de 7° — potenciación, problemas de varios pasos, e Inglés (área NUEVA
        # que pidió el panel). Clústeres nodales que el 1er pase dejó vacíos.
        g.append({"id": "potencias", "titulo": "Potencias", "icono": "🔺", "cfg": {"rondas": 10}})
        g.append({"id": "problemas_multipaso", "titulo": "Problemas de varios pasos", "icono": "📈", "cfg": {"rondas": 8}})
        g.append({"id": "ingles_basico", "titulo": "English time", "icono": "🇬🇧", "cfg": {"rondas": 10}})
        # 3ª tanda 7° (19-jul-2026, nivelación): ecuaciones simples (álgebra
        # inicial), homófonos (ortografía) e historia del s.XX.
        g.append({"id": "ecuaciones_simples", "titulo": "Despejá la x", "icono": "🟰", "cfg": {"rondas": 10}})
        g.append({"id": "homofonos", "titulo": "Homófonos", "icono": "✒️", "cfg": {"rondas": 10}})
        g.append({"id": "argentina_sigloXX", "titulo": "Argentina en el siglo XX", "icono": "🎖️", "cfg": {"rondas": 10}})
    return g


# ── Puzzles verificados (reusan los generadores determinísticos de cuaderno.py) ──

def _lab_json(n, seed):
    """Laberinto n×n como bitmask de paredes por celda (N=1 S=2 E=4 W=8),
    filas row-major + camino solución (BFS — garantiza salida)."""
    from cuaderno import _maze, _maze_path
    w = _maze(n, n, seed)
    camino = _maze_path(w, n, n)
    bit = {"N": 1, "S": 2, "E": 4, "W": 8}
    celdas = [[sum(bit[k] for k in w[x][y]) for x in range(n)] for y in range(n)]
    celdas[0][0] &= ~bit["W"]          # entrada abierta (igual que _draw_maze)
    celdas[n - 1][n - 1] &= ~bit["E"]  # salida abierta
    return {"n": n, "celdas": celdas, "camino": [list(c) for c in camino]}


def _sopa_json(palabras, N, seed):
    """Sopa N×N: todas las palabras colocadas y verificadas (o None si no entran).
    En la grilla van sin tilde (la Ñ se conserva); 'lindas' = como se muestran."""
    from cuaderno import _wordsearch, _sin_tilde
    ws, lindas = [], []
    for p in palabras:
        p = str(p).strip().upper()
        if 3 <= len(p) <= N and p not in lindas:
            lindas.append(p)
            ws.append(_sin_tilde(p))
    g = sol = None
    for s in range(seed, seed + 60):
        g, sol = _wordsearch(ws, N, s)
        if g:
            break
    if not g:
        return None
    filas = ["".join(g[x][y] for x in range(N)) for y in range(N)]
    return {"n": N, "filas": filas, "palabras": ws, "lindas": lindas,
            "sol": {w: [[x, y] for x, y in cs] for w, cs in sol.items()}}


def _sudoku_json(seed):
    """Sudoku 4×4 de solución ÚNICA (verificado por conteo en cuaderno.py)."""
    from cuaderno import _sudoku_make
    sol, puz = _sudoku_make(random.Random(seed))
    return {"sol": sol, "puz": puz}


def _figura_pts(figura, nd):
    """Contorno ordenado (unir los puntos) en coords normalizadas 0..1."""
    pts = []
    if figura == "estrella":
        nd = nd if nd % 2 == 0 else nd + 1
        for i in range(nd):
            a = -math.pi / 2 + i * 2 * math.pi / nd
            r = 0.46 if i % 2 == 0 else 0.20
            pts.append((0.5 + r * math.cos(a), 0.52 + r * math.sin(a)))
    else:  # corazón (paramétrico clásico, arranca arriba al medio)
        for i in range(nd):
            t = math.pi / 2 + i * 2 * math.pi / nd
            x = 16 * math.sin(t) ** 3
            y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pts.append((0.5 + x * 0.028, 0.47 - y * 0.028))
    return [[round(x, 4), round(y, 4)] for x, y in pts]


# ── Estado del token (mismo contrato que audiolibro.py) ──

def _marca_gen(token):
    return os.path.join(ACT_DIR, token, ".generando")


def _marca_error(token):
    return os.path.join(ACT_DIR, token, ".error")


def marcar_generando(token):
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return
    os.makedirs(os.path.join(ACT_DIR, token), exist_ok=True)
    with open(_marca_gen(token), "w") as f:
        f.write("1")


def marcar_error(token, motivo=""):
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return
    os.makedirs(os.path.join(ACT_DIR, token), exist_ok=True)
    try:
        os.remove(_marca_gen(token))
    except OSError:
        pass
    try:
        with open(_marca_error(token), "w", encoding="utf-8") as f:
            f.write(str(motivo)[:500])
    except OSError:
        pass


def estado(token):
    """'listo' / 'generando' / 'error' / None (token inexistente)."""
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return None
    d = os.path.join(ACT_DIR, token)
    if os.path.isfile(os.path.join(d, "manifest.json")):
        return "listo"
    if os.path.isfile(_marca_gen(token)):
        return "generando"
    if os.path.isfile(_marca_error(token)):
        return "error"
    return None


def _cargar(token):
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return None
    p = os.path.join(ACT_DIR, token, "manifest.json")
    if not os.path.isfile(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def certificado_logro(token, nombre=None):
    """Diploma de logro (14-jul-2026) — se renderiza EN VIVO recién cuando el
    peque lo pide (el player solo habilita el link una vez que ganó 3
    estrellas en TODOS los juegos: Store.stars en actividades_player.js, sin
    contraparte server-side — no hay progreso persistido en el servidor, así
    que esto no valida "de verdad" que lo completó, mismo criterio de
    confianza que el resto de los links por token). None si el token no
    existe/no está listo.

    `nombre`: actividades-web NO pide nombre al comprar (compra directa) y
    el player soporta VARIOS perfiles por token (Pablo 14-jul-2026: "pueden
    ser 2 chicos los que juegan en la misma casa") — el nombre real viaja
    desde el player (perfil activo en localStorage), no desde la compra.
    Sin nombre explícito cae al de la compra (si lo hubiera) para no romper
    otros tipos que sí lo piden."""
    reg = _cargar(token)
    if not reg:
        return None
    import certificado
    data = dict(reg)
    if nombre is not None:
        data["nombre"] = nombre.strip()[:40]   # el input del player ya limita a 20; tope extra por las dudas
    return certificado.generar_certificado_logro(data, reg.get("tema") or "safari")


# ── Generación ──

def _miniatura_cmp(im):
    """Miniatura RGB 24×24 del contenido (para comparar recortes entre sí)."""
    from PIL import ImageOps
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    m = bg.convert("RGB").resize((24, 24), Image.LANCZOS)
    return m, ImageOps.mirror(m)


def _dif_pixel(m1, m2par):
    """Diferencia media RGB entre miniaturas (considera el espejo)."""
    m2, m2esp = m2par
    def dif(a, b):
        pa, pb = list(a.getdata()), list(b.getdata())
        return sum(abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])
                   for x, y in zip(pa, pb)) / (len(pa) * 3)
    return min(dif(m1, m2), dif(m1, m2esp))


def _matiz_sat(im):
    """(matiz circular medio en grados, saturación media) de los píxeles
    opacos y no-blancos. Para distinguir 'flor amarilla vs flor roja' (misma
    etiqueta, matiz lejos) de 'león vs león' (matiz igual)."""
    import colorsys
    m = im.copy()
    m.thumbnail((64, 64))
    hx = hy = n = 0.0
    sats = []
    for r, g, b, a in m.getdata():
        if a < 60 or (r > 225 and g > 225 and b > 225):
            continue
        h, sat, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        if sat > 0.12 and v > 0.15:
            hx += math.cos(h * 2 * math.pi)
            hy += math.sin(h * 2 * math.pi)
            sats.append(sat)
            n += 1
    if not n:
        return None, 0.0
    return math.degrees(math.atan2(hy, hx)) % 360, sum(sats) / len(sats)


def _dist_matiz(a, b):
    if a is None or b is None:
        return 0.0           # sin color confiable → no separa (decide el resto)
    d = abs(a - b) % 360
    return min(d, 360 - d)


def _etiquetas_tema(tema):
    """Etiquetas del clasificador de visión (clasif.json, cacheado por el
    cuaderno): {'c001.png': 'león', …}. Vacío si el tema no tiene."""
    try:
        t = json.load(open(os.path.join(BASEDIR, "temas", tema,
                                        "actividades_mon", "clasif.json"),
                           encoding="utf-8")).get("tipos") or {}
        return {str(k).lower(): str(v).strip().lower() for k, v in t.items()}
    except Exception:
        return {}


def _silueta_cmp(im, S=28):
    """Silueta binaria S×S (+espejo) para comparar formas."""
    from PIL import ImageOps
    a = im.getchannel("A").point(lambda v: 255 if v > 40 else 0).resize((S, S))
    return a, ImageOps.mirror(a)


def _iou_silueta(a, bpar):
    """IoU de siluetas (máx con el espejo): 'león vs león' da ~0.81; figuras
    de forma distinta (hoja vs flor) quedan por debajo de ~0.75."""
    def iou(x, y):
        px, py = list(x.getdata()), list(y.getdata())
        inter = sum(1 for u, v in zip(px, py) if u and v)
        union = sum(1 for u, v in zip(px, py) if u or v)
        return inter / max(1, union)
    return max(iou(a, bpar[0]), iou(a, bpar[1]))


def _es_duplicado(cand, elegidos):
    """¿`cand` se confunde con alguno ya elegido? Calibrado 10-jul-2026 con los
    dups REALES del memotest (2 leones diff-píxel 38, 2 monsteras 31 — la
    métrica de píxeles sola NO alcanza; feedback Pablo). El clasif.json
    etiqueta solo una parte de los recortes, así que hay tres casos:
    - ambos ETIQUETADOS: misma etiqueta y matiz cerca (<40°) → dup (león vs
      león); matiz lejos → se quedan (flor amarilla vs flor roja)
    - alguno SIN etiqueta: matiz cerca (<25°) + píxel <40 + MISMA FORMA
      (IoU silueta >0.75) → dup (atrapa al león sin etiquetar y a las dos
      monsteras; deja pasar hoja-vs-flor, que difieren en forma)
    - MISMO COLOR (matiz <10°) + MISMA FORMA (IoU >0.75) → dup aunque el píxel
      pase el corte de 40 (2 camiones rojos de bomberos, 2 palas amarillas de
      construccion: Pablo 15-jul-2026 seguía viéndolos repetidos; los aviones
      recoloreados de aviadores tienen matiz 20-46 y quedan separados)
    - píxel <24 → dup siempre (casi-idénticos)"""
    for e in elegidos:
        dp = _dif_pixel(cand["mini"][0], e["mini"])
        if dp < 24:
            return True
        dm = _dist_matiz(cand["matiz"], e["matiz"])
        if cand["etiqueta"] and e["etiqueta"]:
            # etiqueta distinta → NO dup aunque compartan color/silueta (elefante
            # y nene con chaleco naranja): manda el clasificador, no el color.
            if cand["etiqueta"] == e["etiqueta"] and dm < 40:
                return True
        elif _iou_silueta(cand["sil"][0], e["sil"]) > 0.75 and (
                (dm < 25 and dp < 40) or (dm < 10 and dp < 50)):
            return True
    return False


def _personajes(tema, d):
    """Copia al token los mejores recortes del tema, LIMPIOS (sin el aro
    blanco del die-cut — acá no son stickers; feedback Pablo 10-jul-2026, vía
    cuaderno._recorte_limpio/piezas.quitar_halo): variedad estricta (sin
    casi-duplicados — la regla que salvó al memotest del papel), sin tiras
    compuestas, dedup extra por contenido (dos hojas casi iguales confunden).
    Devuelve filenames (hasta 8); como van sin aro, la silueta de sombras se
    hace en el player con el mismo archivo (brightness 0)."""
    from cuaderno import _seleccionar_recortes, _recorte_limpio
    paths = _seleccionar_recortes(tema, 16, variedad_estricta=True, incluir_objetos=True)
    if len(paths) < 4:
        paths = _seleccionar_recortes(tema, 16, incluir_objetos=True)
    etiquetas = _etiquetas_tema(tema)
    buenos, elegidos = [], []
    for p in paths:
        try:
            im = _recorte_limpio(p)
        except Exception:
            continue
        im = im.crop(im.getbbox() or (0, 0, im.width, im.height))
        if not piezas.un_solo_blob(im):
            continue
        matiz, _sat = _matiz_sat(im)
        cand = {"mini": _miniatura_cmp(im), "matiz": matiz,
                "sil": _silueta_cmp(im),
                "etiqueta": etiquetas.get(os.path.basename(p).lower(), "")}
        if _es_duplicado(cand, elegidos):
            continue
        elegidos.append(cand)
        buenos.append(im)
        if len(buenos) >= 8:
            break
    if len(buenos) < 2:
        raise RuntimeError("el tema %r no tiene stickers para las actividades" % tema)
    out = []
    for i, im in enumerate(buenos):
        im.thumbnail((420, 420), Image.LANCZOS)
        fn = "p%02d.png" % i
        im.save(os.path.join(d, fn), optimize=True)
        out.append(fn)
    return out, list(out)      # sombras = los mismos archivos (ya sin aro)


def _colorear(tema, d):
    from cuaderno import _colorear_imgs
    out = []
    for i, im in enumerate(_colorear_imgs(tema)[:3]):
        im = im.convert("L")
        im.thumbnail((1100, 1100), Image.LANCZOS)
        fn = "colorear_%d.png" % i
        im.save(os.path.join(d, fn), optimize=True)
        out.append(fn)
    return out


def _escena(tema, d):
    try:
        import fondos_ia
        f = fondos_ia.cargar_fondo(tema, "escena")
    except Exception:
        f = None
    if f is None:
        return None
    f = f.convert("RGB")
    f.thumbnail((1600, 1600), Image.LANCZOS)
    f.save(os.path.join(d, "escena.jpg"), quality=82)
    return "escena.jpg"


# ── Activación escalable por NIVELES (19-jul-2026, docs/auditoria-dc-caba/,
# [[ct3d-actividades-activacion-escalable]]): las actividades se agrupan en
# niveles que profundizan los mismos temas. Nivel 1 = incluido en el kit
# (gratis); niveles 2 y 3 = premium, con candado. En un token con
# premium_on=True el player muestra el SELECTOR DE NIVELES y bloquea los
# niveles > nivel_max. El gate es POR TOKEN → los links vivos (premium_on
# ausente/False) NO se ven afectados: ven el menú plano de siempre, todo gratis.
# Cuando el chico DOMINA su nivel, el player avisa (registrar_solicitud motivo=
# 'domino') → la TIENDA le manda el mail al comprador para desbloquear el
# siguiente con 50% off (esa parte vive en /opt/ct3d).
# Demo: Pablo define el mapa real; acá van actividades de 4° como muestra.
NIVEL_NOMBRES = {1: "Explorador", 2: "Aventurero", 3: "Experto"}
NIVEL_ICONOS = {1: "🌱", 2: "🧭", 3: "🏆"}
# actividad → nivel (las que NO figuran acá quedan en el nivel 1, gratis).
_NIVEL_ACTIVIDAD = {
    # Nivel 2 (intermedio): se abre cuando domina el Nivel 1
    "fracciones_equivalentes": 2, "duelo_fracciones": 2, "reparto_fracciones": 2,
    "completar_entero": 2, "recta_numerica": 2,
    # Nivel 3 (avanzado): se abre cuando domina el Nivel 2
    "problemas_mult_div": 3, "duelo_decimales": 3, "angulos": 3,
    "comprension_lectora": 3, "prefijos_sufijos": 3,
}
def _nivel_de(actividad):
    return _NIVEL_ACTIVIDAD.get(actividad, 1)

def _marcar_niveles(menu):
    """Taggea cada item del menú con su 'nivel' (1 por defecto). No filtra nada:
    el player decide qué mostrar/bloquear según el nivel_max del token."""
    for it in menu:
        it["nivel"] = _nivel_de(it["id"])
    return menu

def _niveles_meta(menu):
    """Resumen de los niveles presentes en el menú (para el selector del player):
    número, nombre, ícono y cuántas actividades tiene cada uno. Ordenado."""
    presentes = sorted({it.get("nivel", 1) for it in menu})
    return [
        {"nivel": n, "nombre": NIVEL_NOMBRES.get(n, "Nivel %d" % n),
         "icono": NIVEL_ICONOS.get(n, "⭐"),
         "cantidad": sum(1 for it in menu if it.get("nivel", 1) == n)}
        for n in presentes
    ]


def desbloquear_nivel(token, nivel):
    """Sube el nivel_max del token hasta 'nivel' (lo llama el desbloqueo del admin
    o el futuro checkout de la tienda tras cobrar). Idempotente. Devuelve el
    nivel_max nuevo, o None si el token no existe."""
    try:
        nivel = int(nivel)
    except Exception:
        return None
    p = os.path.join(ACT_DIR, token, "data.json")
    try:
        dj = json.load(open(p, encoding="utf-8"))
    except Exception:
        return None
    actual = int(dj.get("nivel_max") or 1)
    if nivel > actual:
        dj["nivel_max"] = nivel
        with open(p, "w", encoding="utf-8") as f:
            json.dump(dj, f, ensure_ascii=False)
        return nivel
    return actual


def registrar_solicitud(token, nivel, motivo="pidio"):
    """Captura el evento para que la TIENDA le mande el mail al comprador:
    'este chico (token) quiere / está listo para el nivel N'.
      motivo='domino' → dominó su nivel actual (mail: 'ya puede avanzar').
      motivo='pidio'  → tocó el candado del nivel (mail: 'quiere el nivel N').
    Append a datos_premium/solicitudes.jsonl. Best-effort."""
    dd = os.path.join(BASEDIR, "datos_premium")
    os.makedirs(dd, exist_ok=True)
    try:
        nivel = int(nivel)
    except Exception:
        nivel = 0
    linea = {"token": token, "nivel": nivel, "motivo": str(motivo)[:16], "t": int(time.time())}
    with open(os.path.join(dd, "solicitudes.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")
    return linea


def solicitudes_pendientes():
    """Lista de solicitudes de desbloqueo (para el panel). Best-effort."""
    p = os.path.join(BASEDIR, "datos_premium", "solicitudes.jsonl")
    out = []
    try:
        for l in open(p, encoding="utf-8"):
            l = l.strip()
            if l:
                out.append(json.loads(l))
    except Exception:
        pass
    return out


def _armar_data(tema, nombre, edad, seed):
    """El data.json del token: paleta + menú + puzzles verificados."""
    from cuaderno import _tema_nombre, _tema_palabras, PALABRAS
    banda = _banda(edad)
    rnd = random.Random(seed)
    palabras = _tema_palabras(tema) or list(PALABRAS)

    sopas, sudokus, laberintos = [], [], []
    if banda == "grande":
        # Filtrar por largo ANTES de samplear: la sopa es 10×10, las palabras de más
        # de 10 letras no entran (_sopa_json las descarta). Si el sample caía en
        # palabras largas, la sopa salía pobre o vacía. Y descartamos sopas con menos
        # de 4 palabras colocadas (no vale la pena mostrarlas).
        validas = [p for p in palabras if 3 <= len(str(p).strip()) <= 10]
        for i in range(4):
            if len(validas) < 4:
                break
            sub = rnd.sample(validas, min(6, len(validas)))
            s = _sopa_json(sub, 10, seed + i * 101)
            if s and len(s.get("palabras", [])) >= 4:
                sopas.append(s)
        sudokus = [_sudoku_json(seed + i * 13) for i in range(4)]
    if banda != "mini":
        tams = [6, 7, 8, 9] if banda == "media" else [9, 10, 11, 12]
        laberintos = [_lab_json(n, seed + i * 17) for i, n in enumerate(tams)]

    # laberintos CHICOS para "programá el camino" (14-jul-2026, prototipo de
    # pensamiento computacional): los de arriba (9-12 celdas en "grande") son
    # enormes para armar una secuencia de instrucciones a mano — acá van 3
    # de 3-4 celdas, mismo generador verificado por BFS, tamaño propio.
    laberintos_chicos = []
    if banda == "grande":
        tams_chicos = [3, 4, 4]
        laberintos_chicos = [_lab_json(n, seed + 900 + i * 23) for i, n in enumerate(tams_chicos)]

    titulo = ("Las actividades de %s" % nombre) if nombre else "Cuaderno de actividades"
    menu_niv = _marcar_niveles(_menu(banda, edad))
    return {
        "v": 1, "tema": tema, "tema_nombre": _tema_nombre(tema),
        "nombre": nombre, "edad": edad, "banda": banda, "titulo": titulo,
        "paleta": _paleta(tema),
        "menu": menu_niv,
        "niveles": _niveles_meta(menu_niv),
        "sopas": sopas, "sudokus": sudokus, "laberintos": laberintos,
        "laberintos_chicos": laberintos_chicos,
        "figuras": {"estrella": _figura_pts("estrella", 10),
                    "corazon": _figura_pts("corazon", 14)},
    }


def _fuente(nombre, px, peso=None):
    """`peso` (200-1000) selecciona el grosor en una fuente VARIABLE (Nunito-VF,
    Baloo2-VF...) — sin esto, PIL abre la fuente en su instancia por DEFECTO,
    que en Nunito-VF es 200 (ExtraLight, casi invisible de fino) — mismo
    patrón que cuaderno._font."""
    try:
        f = ImageFont.truetype(os.path.join(BASEDIR, "fonts", nombre), px)
        if peso is not None:
            try:
                f.set_variation_by_axes([peso])
            except Exception:
                pass
        return f
    except Exception:
        return ImageFont.load_default()


def _hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _colores_seguros(pal):
    """(card, ink, soft) listos para pintar SOBRE FONDO CLARO fijo (el margen
    de las piezas de galería ya no usa pal["bg"]). Si la card del tema es
    oscura (hoy solo "un-espacio-de-locura", a propósito — pal["ink"]/["soft"]
    están pensados para el fondo oscuro REAL del juego), se cae a los defaults
    claros — si no, quedan combinaciones oscuro-sobre-oscuro ilegibles (bug
    real: los chips de "Todos los juegos" quedaban invisibles en ese tema)."""
    card, ink, soft = pal["card"], pal["ink"], pal["soft"]
    cr, cg, cb = _hex_rgb(card)
    if 0.299 * cr + 0.587 * cg + 0.114 * cb < 128:
        card, ink, soft = "#FFFFFF", _PALETA_DEFAULT["ink"], _PALETA_DEFAULT["soft"]
    return card, ink, soft


def _render_portada(dj, pers_imgs):
    """Portada 900×1200 — VERTICAL como las tapas de los audiolibros: la card
    de Mi biblioteca es 3:4 y la versión apaisada se recortaba a los costados
    (feedback Pablo 10-jul)."""
    pal = dj["paleta"]
    W, H = 900, 1200
    # el margen de 36px alrededor de la card usa un fondo NEUTRO fijo, no
    # pal["bg"] del tema — "un-espacio-de-locura" es la única paleta oscura
    # a propósito y ese margen se veía como un borde azul marino feo (Pablo
    # 12-jul: "sácale el fondo azul... en todas pasa lo mismo" — el bug es
    # el mismo código para los 12 temas, solo que en los demás pal["bg"] es
    # un pastel clarito y casi no se nota contra la card blanca).
    im = Image.new("RGB", (W, H), _hex_rgb(_PALETA_DEFAULT["bg"]))
    dr = ImageDraw.Draw(im)
    # la card en sí: si el tema tiene card OSCURA (misma paleta oscura a
    # propósito — la única hoy es "un-espacio-de-locura"), acá se fuerza
    # blanca + tinta oscura segura, porque el "ink" de esa paleta es CASI
    # BLANCO (pensado para texto sobre fondo oscuro real del juego) — sobre
    # una card blanca hubiera quedado invisible. Los otros 11 temas ya
    # tienen card blanca de por sí, esto no les cambia nada.
    card_color, ink_color, _soft = _colores_seguros(pal)
    dr.rounded_rectangle((36, 36, W - 36, H - 36), radius=44, fill=_hex_rgb(card_color))
    # franja superior con el acento
    dr.rounded_rectangle((36, 36, W - 36, 240), radius=44, fill=_hex_rgb(pal["ac"]))
    dr.rectangle((36, 170, W - 36, 240), fill=_hex_rgb(pal["ac"]))
    # "CASATRIDIMENSIONAL" con la MISMA tipografía que la marca en la web
    # (Titillium Web, font-display de tienda_static/css/tokens.css) — pedido
    # de Pablo 13-jul-2026 para que la card matchee la identidad del sitio.
    f_marca = _fuente("TitilliumWeb-Bold.ttf", 30)
    f_tit = _fuente("Baloo2-VF.ttf", 78)
    # "Cuaderno interactivo" más grueso (Pablo 13-jul-2026): Nunito-VF sin
    # `peso` abre en su instancia por defecto (200, ExtraLight) — quedaba
    # casi invisible de fino contra la franja de color.
    f_sub = _fuente("Nunito-VF.ttf", 40, peso=800)
    dr.text((W // 2, 100), "CASATRIDIMENSIONAL", font=f_marca, fill="#FFFFFF",
            anchor="mm")
    dr.text((W // 2, 172), "Cuaderno interactivo", font=f_sub, fill="#FFFFFF",
            anchor="mm")
    # título (dos líneas: "Las actividades" / "de <nombre>" si no entra en una)
    tit = dj["titulo"]
    f = f_tit
    if f.getlength(tit) > W - 140:
        pre = "de " + (dj.get("nombre") or "")
        if dj.get("nombre") and tit.endswith(pre):
            l1 = tit[: -len(pre)].strip()
            for i, linea in enumerate((l1, pre)):
                fl = f_tit
                while fl.getlength(linea) > W - 140 and fl.size > 40:
                    fl = _fuente("Baloo2-VF.ttf", fl.size - 4)
                dr.text((W // 2, 350 + i * 92), linea, font=fl,
                        fill=_hex_rgb(ink_color), anchor="mm")
            y_sub = 530
        else:
            while f.getlength(tit) > W - 140 and f.size > 36:
                f = _fuente("Baloo2-VF.ttf", f.size - 4)
            dr.text((W // 2, 390), tit, font=f, fill=_hex_rgb(ink_color), anchor="mm")
            y_sub = 490
    else:
        dr.text((W // 2, 390), tit, font=f, fill=_hex_rgb(ink_color), anchor="mm")
        y_sub = 490
    dr.text((W // 2, y_sub), "%s · %s años" % (dj["tema_nombre"], dj["edad"] or "?"),
            font=f_sub, fill=_hex_rgb(pal["ac2"]), anchor="mm")
    # personajes: protagonista GRANDE al centro + 2 escoltas. thumbnail() no
    # AGRANDA — con recortes chicos (hojas de mini-stickers) quedaban enanos:
    # se reescala al alto pedido con tope 1.8x para no imprimir borroso.
    def _escalar(img, mw, mh):
        alto = min(mh, int(img.height * 1.8))
        w = max(1, int(img.width * alto / img.height))
        if w > mw:
            alto = int(alto * mw / w)
            w = mw
        return img.resize((w, alto), Image.LANCZOS)
    if pers_imgs:
        n = min(3, len(pers_imgs))
        if n >= 3:
            for idx, cx, base in ((1, 190, 1100), (2, W - 190, 1100)):
                if idx < len(pers_imgs):
                    p = _escalar(pers_imgs[idx], 260, 280)
                    im.paste(p, (cx - p.width // 2, base - p.height), p)
        p = _escalar(pers_imgs[0], 420, 430)
        im.paste(p, (W // 2 - p.width // 2, 1120 - p.height), p)
    # estrellitas decorativas
    star = _hex_rgb(pal["star"])
    for cx, cy, r in ((120, 300, 13), (780, 290, 16), (700, 560, 11), (170, 580, 10),
                      (810, 700, 12)):
        dr.regular_polygon((cx, cy, r), 5, rotation=90, fill=star)
    return im


def _catalogo_juegos():
    """Los juegos DISTINTOS de todo el catálogo (id + título), uniendo TODAS
    las bandas/edades — un chico puntual no los ve todos (cada banda/edad
    tiene los suyos, algunos se "gradúan" según la edad), pero es el total
    real que ofrece el producto entre los 2 y los 12 años.
    16-jul-2026: extendido de (2, 5, 8) a también 9-12 — el contenido NAP
    progresivo de esas edades (grados 4to-7mo) existía en _menu() pero
    quedaba afuera de este catálogo, así que sus juegos nunca aparecían
    como pestaña en el editor ni como card en la galería "Qué incluye" de
    la tienda, sin importar qué edad se eligiera (Pablo: "pongo 8 años se
    actualiza pero no muestra las actividades distintas")."""
    vistos, out = set(), []
    muestras = (("mini", "2"), ("media", "5"), ("grande", "6"), ("grande", "7"),
                ("grande", "8"), ("grande", "9"),
                ("grande", "10"), ("grande", "11"), ("grande", "12"))
    for banda, edad in muestras:
        for m in _menu(banda, edad):
            if m["id"] not in vistos:
                vistos.add(m["id"])
                out.append({"id": m["id"], "titulo": m["titulo"]})
    return out


def incluidos_por_edad():
    """{edad: [títulos incluidos]} para las edades del dropdown (2 a 12) —
    Pablo 13-jul-2026: "cuando cambio de edad... creo que no cambian las
    imágenes". El bloqueo SÍ cambia (verificado), pero 8 de los 19 juegos
    están en TODAS las bandas y esas cards nunca se ven distintas — el resto
    queda mezclado entre ellas, así que el cambio real es fácil de no notar
    en el scroll. La tienda usa esto para REORDENAR la galería (desbloqueados
    primero) cuando cambia la edad, no solo repintar cada card en el mismo
    lugar. Independiente del tema: el menú de _menu() no varía por tema.
    16-jul-2026: extendido de 8 a 12 — el contenido NAP progresivo para 9-12
    (grados 4to-7mo) ya estaba armado en _menu() pero la ficha de la tienda
    nunca lo exponía (dropdown de edad fijo en 2-8, bug real de Pablo)."""
    return {e: sorted({m["titulo"] for m in _menu(_banda(e), e)})
            for e in ("2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")}


def _personajes_para_cards(tema, n=8):
    """PATHS de stickers del tema para armar la página de un juego (mismo
    criterio que usa el cuaderno IMPRESO para elegir sus `mons` — no
    variedad_estricta, porque varios juegos necesitan varias copias del
    mismo personaje)."""
    try:
        from cuaderno import _seleccionar_recortes, _extraer_monstruos
        paths = _seleccionar_recortes(tema, n, incluir_objetos=True)
        if len(paths) < 4:
            paths = _extraer_monstruos(tema) or paths
        return paths
    except Exception:
        return []


# ── Cards de la galería "qué incluye": Pablo 12-jul-2026, viendo la primera
#    versión (stickers decorativos + título): "esto es lo que veo. No tiene
#    nada que ver con las actividades" — con razón: no mostraba NADA del
#    juego en sí. Ahora cada card es la página REAL del juego, reusando los
#    mismos generadores verificados del cuaderno IMPRESO (mismo laberinto con
#    salida garantizada, mismo sudoku de solución única, la misma sopa de
#    letras temática...) — la card muestra de verdad lo que esa actividad
#    contiene. Los 5 juegos que son SOLO interactivos (no existen en el
#    cuaderno impreso: memotest, simon, agrupar, quefalta, bingo) tienen su
#    propio render, con la misma mecánica que arma el player en el navegador.
def _dispatch_cuaderno(cuad, game_id, b):
    """Llama al generador de página del cuaderno IMPRESO que corresponde a
    `game_id`, con parámetros chicos (pensados para una card, no para el
    largo real del cuaderno). None si no hay generador para ese id (los 5
    juegos solo-interactivos se resuelven en `_JUEGOS_CUSTOM`)."""
    if game_id == "contar":
        return cuad._a_contar(b, 3, 2)
    if game_id == "colorear":
        return cuad._a_colorear(b, 0)
    if game_id == "sombra":
        return cuad._a_sombra(b, 3)
    if game_id == "diferente":
        return cuad._a_diferente(b, 2)
    if game_id == "tamano":
        return cuad._a_tamano(b, 2)
    if game_id == "patron":
        return cuad._a_patron(b, 2)
    if game_id == "laberinto":
        return cuad._a_laberinto(b, 6)
    if game_id == "puntos":
        return cuad._a_puntos(b, 10, "estrella")
    if game_id == "mas_menos":
        return cuad._a_mas_menos(b, 2)
    if game_id == "sumas":
        return cuad._a_sumas(b, 2)
    if game_id == "sopa":
        return cuad._a_sopa(b, getattr(b, "_palabras", None))
    if game_id == "sudoku":
        return cuad._a_sudoku(b)
    if game_id == "restas":
        return cuad._a_restas(b, 2)
    if game_id == "serie":
        return cuad._a_serie(b, 2)
    return "sin-generador"


def _juego_page_memotest(b):
    from cuaderno import _paste_h, _IM, _font, NAVY, VIOLET, Wp, BOT
    if not b.mons:
        return
    b.sec("Memotest", "Dado vuelta las cartas, encontrá las parejas iguales.")
    pares = min(3, len(b.mons))
    ids = list(range(pares)) * 2
    b.rnd.shuffle(ids)
    boca_arriba = set(b.rnd.sample(range(len(ids)), pares))
    cols = pares
    cw = (Wp - 160) // cols
    ch = min(300, (BOT - b.y) // 2 - 30)
    x0 = 80
    for i, gi in enumerate(ids):
        r, c = divmod(i, cols)
        cx, cy = x0 + c * cw + cw / 2, b.y + 30 + r * (ch + 30) + ch / 2
        if i in boca_arriba:
            b.dr.rounded_rectangle([cx - cw * .42, cy - ch * .42, cx + cw * .42, cy + ch * .42],
                                    16, fill="#FFFFFF", outline=NAVY, width=4)
            _paste_h(b.im, _IM(b.mons[gi]), cx, cy, int(ch * .72))
        else:
            b.dr.rounded_rectangle([cx - cw * .42, cy - ch * .42, cx + cw * .42, cy + ch * .42],
                                    16, fill=VIOLET)
            b.dr.text((cx, cy), "?", font=_font(60), fill="white", anchor="mm")
    b.y = BOT


def _juego_page_simon(b):
    from cuaderno import _font, COLS, Wp, BOT
    b.sec("Escuchá y repetí", "Tocá los colores en el mismo orden que sonaron.")
    n, r = 4, 130
    cy = b.y + (BOT - b.y) / 2
    gap = 300
    x0 = Wp / 2 - gap * (n - 1) / 2
    for i in range(n):
        x = x0 + i * gap
        b.dr.ellipse([x - r, cy - r, x + r, cy + r], fill=COLS[i % len(COLS)])
        b.dr.text((x, cy), str(i + 1), font=_font(58), fill="white", anchor="mm")
    b.y = BOT


def _juego_page_agrupar(b):
    from cuaderno import _paste_h, _IM, VIOLET, COLS, Wp, BOT
    if len(b.mons) < 2:
        return
    b.sec("¿Dónde va?", "Arrastrá cada uno a la canasta que le corresponde.")
    picks = b.rnd.sample(range(len(b.mons)), min(4, len(b.mons)))
    top_y = b.y + 150
    x0 = Wp / 2 - (len(picks) - 1) * 130
    for i, mi in enumerate(picks):
        _paste_h(b.im, _IM(b.mons[mi]), x0 + i * 260, top_y, 130)
    # canastas PEGADAS a los items (no al fondo de la hoja) — a tamaño de
    # card, dejarlas en BOT-170 abría un hueco enorme en el medio que el
    # recorte de contenido no puede sacar (hay dibujo antes Y después).
    basket_y = top_y + 260
    for i, bx in enumerate((Wp * .32, Wp * .68)):
        col = COLS[i % len(COLS)]
        b.dr.polygon([(bx - 150, basket_y), (bx + 150, basket_y),
                      (bx + 108, basket_y + 150), (bx - 108, basket_y + 150)], fill=col)
        b.dr.rounded_rectangle([bx - 160, basket_y - 16, bx + 160, basket_y + 16], 12, fill=VIOLET)
    b.y = min(BOT, basket_y + 200)


def _juego_page_quefalta(b):
    from cuaderno import _paste_h, _IM, _font, NAVY, Wp, BOT
    if not b.mons:
        return
    b.sec("¿Qué falta?", "Mirá bien la fila y decí cuál falta.")
    n = min(4, max(3, len(b.mons)))
    picks = [b.mons[i % len(b.mons)] for i in range(n)]
    falta = b.rnd.randrange(n)
    y = b.y + (BOT - b.y) / 2
    gap = min(260, (Wp - 200) // n)
    x0 = Wp / 2 - (n - 1) * gap / 2
    for i, p in enumerate(picks):
        x = x0 + i * gap
        if i == falta:
            b.dr.rounded_rectangle([x - 90, y - 90, x + 90, y + 90], 16, outline=NAVY, width=4)
            b.dr.text((x, y), "?", font=_font(70), fill=(185, 180, 200), anchor="mm")
        else:
            _paste_h(b.im, _IM(p), x, y, 160)
    b.y = BOT


def _juego_page_bingo(b):
    from cuaderno import _paste_h, _IM, VIOLET, COLS, Wp, BOT
    if not b.mons:
        return
    b.sec("Bingo de amigos", "Marcá cada personaje que va saliendo en tu cartón.")
    n = 3
    cell = min(220, (Wp - 160) // n)
    gx = (Wp - n * cell) // 2
    gy = b.y + max(0, (BOT - b.y - n * cell) // 2)
    marcados = set(b.rnd.sample(range(n * n), 2))
    for i in range(n * n):
        r, c = divmod(i, n)
        x0, y0 = gx + c * cell, gy + r * cell
        b.dr.rectangle([x0, y0, x0 + cell, y0 + cell], outline=VIOLET, width=3)
        _paste_h(b.im, _IM(b.mons[i % len(b.mons)]), x0 + cell / 2, y0 + cell / 2, cell - 40)
        if i in marcados:
            b.dr.ellipse([x0 + 10, y0 + 10, x0 + cell - 10, y0 + cell - 10], outline=COLS[0], width=8)
    b.y = BOT


_JUEGOS_CUSTOM = {
    "memotest": _juego_page_memotest, "simon": _juego_page_simon,
    "agrupar": _juego_page_agrupar, "quefalta": _juego_page_quefalta,
    "bingo": _juego_page_bingo,
}


def _recortar_contenido(im, header_h=300, footer_h=110, margin=36, gap_max=40):
    """Achica el aire de MÁS: los generadores del cuaderno IMPRESO centran el
    contenido en TODA la hoja A4 disponible (`BOT - b.y`, pensado para llenar
    una hoja entera), así que a tamaño de card queda con una franja en blanco
    ANTES del contenido (el centrado vertical) y otra DESPUÉS (real: el
    laberinto quedaba con casi media card vacía arriba del dibujo). Busca el
    bbox real de lo dibujado dentro de la zona de contenido (después del
    banner+título, antes del pie de página fijo — el pie SIEMPRE tiene texto,
    por eso se excluye del bbox) y pega ese bbox pegado al header, dejando
    como mucho `gap_max` de aire arriba."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    zona = rgb.crop((0, header_h, w, h - footer_h))
    bg = Image.new("RGB", zona.size, (255, 255, 255))
    bbox = ImageChops.difference(zona, bg).getbbox()
    if not bbox:
        return im
    top_excedente = max(0, bbox[1] - gap_max)
    contenido = im.crop((0, header_h + top_excedente, w, min(h - footer_h, header_h + bbox[3] + margin)))
    out = Image.new("RGB", (w, header_h + contenido.height), (255, 255, 255))
    out.paste(im.crop((0, 0, w, header_h)), (0, 0))
    out.paste(contenido, (0, header_h))
    return out


def _juego_page(tema, edad, game_id, mons, escena, colorear_imgs, palabras, seed):
    """La página REAL de UN juego (Wp×Hp, igual que el cuaderno impreso,
    recortada al contenido) para usarla como card de la galería. None si algo
    falla (tema sin arte de colorear todavía, muy pocos stickers, etc.) — el
    caller cae a un fallback genérico, nunca a una excepción."""
    import cuaderno
    try:
        b = cuaderno._Book(str(edad), mons, seed, cuaderno._tema_nombre(tema))
        b.tema = tema
        b._colorear = colorear_imgs
        b._escena = escena
        b._palabras = palabras
        if game_id in _JUEGOS_CUSTOM:
            _JUEGOS_CUSTOM[game_id](b)
        elif _dispatch_cuaderno(cuaderno, game_id, b) == "sin-generador":
            return None
        b.finish()
        return _recortar_contenido(b.pages[0]) if b.pages else None
    except Exception:
        return None


def _apagar_bloqueado(im):
    """Variante "bloqueada" de una card (Pablo 12-jul-2026: "que cambien
    viendo cambio la edad") — apagada + franja con leyenda, sin perder la
    imagen de fondo (a diferencia de un grisado 100%, se sigue reconociendo
    el juego)."""
    base = im.convert("RGBA")
    g = ImageOps.grayscale(base.convert("RGB"))
    gris = Image.merge("RGB", (g, g, g)).convert("RGBA")
    apagado = Image.blend(base, gris, 0.7)
    velo = Image.new("RGBA", apagado.size, (255, 255, 255, 130))
    apagado.alpha_composite(velo)
    dr = ImageDraw.Draw(apagado)
    w, h = apagado.size
    bh = max(70, h // 16)
    dr.rectangle((0, h - bh, w, h), fill=(120, 113, 103, 235))
    f = _fuente("Nunito-VF.ttf", max(20, w // 26))
    while f.getlength("Se desbloquea en otra edad") > w - 40 and f.size > 16:
        f = _fuente("Nunito-VF.ttf", f.size - 2)
    dr.text((w / 2, h - bh / 2), "Se desbloquea en otra edad", font=f, fill="#FFFFFF", anchor="mm")
    return apagado.convert("RGB")


def _render_juego_card_fallback(tema, pal, titulo, incluido=True):
    """Fallback si `_juego_page` no pudo generar la página real (tema sin
    arte de colorear todavía, etc.) — nunca None, preview_pieza() no lo
    tolera."""
    W, H = 640, 640
    card_color, ink_color, _soft = _colores_seguros(pal)
    im = Image.new("RGB", (W, H), _hex_rgb(card_color))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((24, 24, W - 24, 110), radius=32, fill=_hex_rgb(pal["ac"]))
    dr.text((W // 2, 67), "CASATRIDIMENSIONAL", font=_fuente("TitilliumWeb-Bold.ttf", 21),
            fill="#FFFFFF", anchor="mm")
    f = _fuente("Baloo2-VF.ttf", 44)
    while f.getlength(titulo) > W - 80 and f.size > 26:
        f = _fuente("Baloo2-VF.ttf", f.size - 3)
    dr.text((W // 2, H // 2), titulo, font=f, fill=_hex_rgb(ink_color), anchor="mm")
    return im if incluido else _apagar_bloqueado(im)


def crear(data, tema, token=None):
    """Genera actividades/<token>/ completo. Síncrono y rápido (sin llamadas IA:
    todo procedural + copiar arte ya existente del tema). Devuelve el token."""
    if not (token and re.fullmatch(_TOKEN_RE, token)):
        token = secrets.token_urlsafe(12)
    d = os.path.join(ACT_DIR, token)
    os.makedirs(d, exist_ok=True)
    # limpiar assets de una generación anterior (regenerar un token dejaba
    # huérfanos: p07.png viejo junto a los p00-p06 nuevos)
    for fn in os.listdir(d):
        if re.fullmatch(r"(?:[ps]\d{2}|colorear_\d)\.png", fn):
            try:
                os.remove(os.path.join(d, fn))
            except OSError:
                pass
    nombre = (data.get("nombre") or "").strip()
    edad = (str(data.get("edad") or "")).strip()
    seed = zlib.crc32(token.encode())

    pers, sombras = _personajes(tema, d)
    cols = _colorear(tema, d)
    esc = _escena(tema, d)
    dj = _armar_data(tema, nombre, edad, seed)
    dj["personajes"] = pers
    dj["sombras"] = sombras
    dj["colorear"] = cols
    dj["escena"] = esc
    # activación escalable por niveles: modo premium por token (default OFF → sin
    # impacto en links vivos) + nivel_max (el nivel más alto desbloqueado; se
    # PRESERVA si el token se regenera, para no "perder" una compra al re-armar).
    dj["premium_on"] = bool(data.get("premium_on"))
    _prev = {}
    try:
        _prev = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
    except Exception:
        pass
    dj["nivel_max"] = int(data.get("nivel_max") or _prev.get("nivel_max") or 1)
    with open(os.path.join(d, "data.json"), "w", encoding="utf-8") as f:
        json.dump(dj, f, ensure_ascii=False)

    pers_imgs = [Image.open(os.path.join(d, p)).convert("RGBA") for p in pers[:3]]
    _render_portada(dj, pers_imgs).save(os.path.join(d, "portada.jpg"), quality=88)

    with open(os.path.join(d, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"tema": tema, "nombre": nombre, "edad": edad,
                   "banda": dj["banda"], "titulo": dj["titulo"],
                   "creado": int(time.time())}, f, ensure_ascii=False)
    try:
        os.remove(_marca_gen(token))
    except OSError:
        pass
    _limpiar_vencidos()
    return token


def _limpiar_vencidos():
    import shutil
    limite = time.time() - VIGENCIA_DIAS * 86400
    try:
        for fn in os.listdir(ACT_DIR):
            p = os.path.join(ACT_DIR, fn)
            if os.path.isdir(p) and os.path.getmtime(p) < limite:
                shutil.rmtree(p, ignore_errors=True)
    except OSError:
        pass


# ── Servido (visor + assets) ──

def _player_version():
    """Cache-buster: cambia solo cuando se toca el player en el repo."""
    try:
        return str(int(max(os.path.getmtime(TEMPLATE_JS),
                           os.path.getmtime(TEMPLATE_HTML))))
    except OSError:
        return "1"


def _slug_audio(texto):
    import hashlib
    return "c_" + hashlib.md5(texto.encode("utf-8")).hexdigest()[:10] + ".mp3"


_EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F0FF"
    "\U00002B00-\U00002BFF\U0000FE0F]+")


def _texto_para_tts(texto):
    """La consigna que se MUESTRA puede llevar emoji (⭐, 🧺...) — la voz no
    tiene que intentar leerlos. El manifest queda indexado por el texto
    ORIGINAL (lo que el player realmente pinta en pantalla)."""
    return _EMOJI_RE.sub("", texto).strip()


_VOCAL_RE = re.compile("[aeiouáéíóúAEIOUÁÉÍÓÚ]")


def _duracion_minima(texto):
    """Piso de duración razonable en segundos — proxy de sílabas por conteo
    de vocales (no tenemos silabización real acá, pero alcanza para detectar
    una toma apurada/cortada). Encontrado 14-jul-2026: "MARIPOSA" (4
    sílabas) salió una toma de 0.71s — la MISMA palabra en otras tomas dio
    1.6-2.1s. Sin este piso esa toma rota se hubiera vendido tal cual.

    Tasa por vocal MÁS BAJA a partir de 6 vocales (14-jul-2026, armando 1°
    grado): palabras sueltas se enuncian más despacio por vocal (~0.35-0.55s)
    que una ORACIÓN completa dicha con cadencia natural (~0.17-0.26s medido
    en consignas ya en producción, ej. "Escuchá la palabra y elegí cuántas
    partes tiene" a 3.74s/18 vocales = 0.21s/vocal). Con la tasa única
    anterior (0.22 fija) esa MISMA consigna, ya vendida y funcionando,
    quedaba fuera de rango — no es un piso, es puro ruido de calibración
    para oraciones largas. Vocales cortas (palabras) siguen con 0.22."""
    n_vocales = max(1, len(_VOCAL_RE.findall(texto)))
    tasa = 0.22 if n_vocales <= 6 else 0.14
    return max(0.4, n_vocales * tasa)


def _duracion_maxima(texto):
    """Techo de duración razonable — mismo proxy por vocales, mirror de
    _duracion_minima() para el otro extremo. Encontrado 14-jul-2026 armando
    1° grado: "SAPO" (2 vocales, esperable ~0.7-1s como GATO/PATO/MOTO) salió
    una toma de 2.72s — sin techo, esa toma larga/rara se hubiera vendido
    igual (el piso solo agarra tomas CORTADAS, no tomas de más). Misma tasa
    más baja a partir de 6 vocales que _duracion_minima(), por la misma
    razón (oraciones largas se hablan más rápido por vocal que palabras
    sueltas)."""
    n_vocales = max(1, len(_VOCAL_RE.findall(texto)))
    tasa = 1.0 if n_vocales <= 6 else 0.5
    return max(2.5, n_vocales * tasa)


def generar_audio_consignas(textos):
    """Audio-guía (14-jul-2026, investigación §2b: "es la brecha de UX más
    urgente para 4-5 años, más urgente que sumar juegos nuevos" — a esa edad
    no se puede depender de que el chico lea la consigna solo). Las
    consignas son texto FIJO del player (nunca personalizado por compra), así
    que se graban UNA VEZ acá y se sirven como asset del repo — igual
    criterio que player.js/las fuentes, NO se regeneran por token. Reusa el
    mismo motor de voz del audiolibro (ElevenLabs Lizy, acento argentino).

    QA de duración (piso Y techo por conteo de vocales, ver _duracion_minima/
    _duracion_maxima): hasta 4 tomas con seeds distintos, se queda con la
    primera que caiga DENTRO del rango o, si ninguna cae, con la que haya
    quedado más cerca del rango (nunca falla en silencio).

    Idempotente: solo genera el .mp3 que todavía no existe (podés volver a
    llamarla agregando textos nuevos sin regastar en los que ya están).
    Devuelve el manifest {texto: archivo} completo (viejo + nuevo)."""
    import audiolibro
    os.makedirs(AUDIO_DIR, exist_ok=True)
    manifest_path = os.path.join(AUDIO_DIR, "manifest.json")
    try:
        manifest = json.load(open(manifest_path, encoding="utf-8"))
    except Exception:
        manifest = {}
    for texto in textos:
        fn = _slug_audio(texto)
        manifest[texto] = fn
        path = os.path.join(AUDIO_DIR, fn)
        if os.path.isfile(path):
            continue
        limpio = _texto_para_tts(texto)
        minimo = _duracion_minima(limpio)
        maximo = _duracion_maxima(limpio)
        mejor = None
        for intento in range(4):
            mp3 = audiolibro._tts_elevenlabs(limpio, seed=4242 + intento * 137)
            if not mp3:
                # Sin ElevenLabs (falta la key o falló el TTS) _tts_elevenlabs devuelve
                # None y _dur_mp3_128(None) tiraba "len(None)". Error claro en su lugar.
                raise RuntimeError("generar_audio_consignas: falta ELEVENLABS_API_KEY o el TTS falló")
            dur = audiolibro._dur_mp3_128(mp3)
            dist = max(0.0, minimo - dur, dur - maximo)
            if mejor is None or dist < mejor[2]:
                mejor = (mp3, dur, dist)
            if dist == 0:
                break
        with open(path, "wb") as f:
            f.write(mejor[0])
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False)
    return manifest


def html(token):
    """El visor (HTML). Rutas RELATIVAS → servirlo SIEMPRE bajo /act/<token>/
    (con barra final). None si el token no está listo."""
    reg = _cargar(token)
    if not reg:
        return None
    with open(TEMPLATE_HTML, encoding="utf-8") as f:
        t = f.read()
    return (t.replace("{{TITULO}}", _esc(reg.get("titulo") or "Actividades"))
             .replace("{{V}}", _player_version()))


_ASSET_RE = re.compile(
    r"^(data\.json|player\.js|f[12]\.ttf|[ps]\d{2}\.png|colorear_\d\.png|escena\.jpg|portada\.jpg"
    r"|audio_manifest\.json|c_[a-f0-9]{10}\.mp3)$")
_CT = {".json": "application/json; charset=utf-8", ".js": "text/javascript; charset=utf-8",
       ".ttf": "font/ttf", ".png": "image/png", ".jpg": "image/jpeg", ".mp3": "audio/mpeg"}


def archivo(token, nombre):
    """(bytes, content_type) de un asset del token, o None. El player, las
    fuentes y el audio de las consignas salen del REPO (mejoras/grabaciones
    nuevas llegan a links ya vendidos, mismo criterio que player.js — la
    voz es fija, no personalizada por compra); el resto, de la carpeta del
    token."""
    if not _cargar(token) or not _ASSET_RE.fullmatch(nombre or ""):
        return None
    if nombre == "player.js":
        p = TEMPLATE_JS
    elif nombre == "f1.ttf":
        p = os.path.join(BASEDIR, "fonts", "Baloo2-VF.ttf")
    elif nombre == "f2.ttf":
        p = os.path.join(BASEDIR, "fonts", "Nunito-VF.ttf")
    elif nombre == "audio_manifest.json" or nombre.endswith(".mp3"):
        p = os.path.join(AUDIO_DIR, "manifest.json" if nombre == "audio_manifest.json" else nombre)
    else:
        p = os.path.join(ACT_DIR, token, nombre)
    if not os.path.isfile(p):
        return None
    ct = _CT[os.path.splitext(nombre)[1]]
    with open(p, "rb") as f:
        return f.read(), ct


def preview_mock(data, tema):
    """Miniatura para la ficha de la tienda / dash (sin crear token): la portada.
    Usa `data.get("nombre")` SI VIENE (14-jul-2026) — mismo criterio que
    `_armar_data()`: genérica ("Cuaderno de actividades") cuando no hay
    nombre real (ficha pública recién cargada, nadie escribió nada todavía —
    mostrar un nombre de muestra ahí daría la impresión falsa de que ya
    viene personalizado, bug real corregido 12-jul-2026), personalizada
    cuando SÍ hay uno (la vista previa en vivo del formulario de compra, que
    ya refleja la edad elegida — Pablo 14-jul-2026: "cambio la edad y
    aparece... pero no el nombre")."""
    nombre = (data.get("nombre") or "").strip()
    edad = (str(data.get("edad") or "")).strip() or "5"
    dj = _armar_data_liviano(tema, nombre, edad)
    pers = []
    try:
        from cuaderno import _seleccionar_recortes
        for p in _seleccionar_recortes(tema, 3, variedad_estricta=True,
                                       incluir_objetos=True)[:3]:
            pers.append(Image.open(p).convert("RGBA"))
    except Exception:
        pass
    return _render_portada(dj, pers)


def preview_mock_extra(data, tema, indice):
    """Piezas EXTRA de la galería "Qué incluye" de la ficha (además de la
    portada, pieza 0) — Pablo 12-jul-2026: "no aparecen imágenes de las
    actividades que tiene el kit" — antes solo se repetía la portada. Estas
    muestran contenido REAL del tema (una página para colorear + la escena
    de fondo que usan varios juegos), no un mockup sintético.

    Índice 3 en adelante: una card por CADA juego de `_catalogo_juegos()`
    (19 al armar esto el 12-jul-2026, Pablo: "prefiero ver las 19 imágenes
    de lo que contiene la actividad" en vez de una sola imagen con la lista
    en texto; 63 desde el 16-jul-2026 al sumarse el contenido NAP de 9-12
    años al catálogo). Cada card lee `data["edad"]` y se pinta "bloqueada"
    si ese juego puntual no está en la banda de esa edad ("y que cambien
    viendo cambio la edad") — así la galería responde de verdad al dropdown
    de edad del producto, no queda
    fija.

    Nunca devuelve None — preview_pieza() no tolera un None (rompería la
    galería), así que ante cualquier falla cae de vuelta a la portada."""
    try:
        if indice == 1:
            from cuaderno import _colorear_imgs
            imgs = _colorear_imgs(tema)
            if imgs:
                im = imgs[0].convert("L").convert("RGB")
                return im
        elif indice == 2:
            import fondos_ia
            f = fondos_ia.cargar_fondo(tema, "escena")
            if f is not None:
                return f.convert("RGB")
        elif indice >= 3:
            juegos = _catalogo_juegos()
            i = indice - 3
            if 0 <= i < len(juegos):
                juego = juegos[i]
                edad = (str(data.get("edad") or "")).strip() or "5"
                incluidos = {m["id"] for m in _menu(_banda(edad), edad)}
                incluido = juego["id"] in incluidos
                # PRIORIDAD 1: screenshot REAL del player interactivo (Pablo
                # 13-jul-2026: "Asi es como quiero que las muestres tal cual
                # se ven en la web" — nada de mockups). Generado una vez por
                # tema con actividades_web_cards.py, no en cada request.
                import actividades_web_cards
                p = actividades_web_cards.card_path(tema, juego["id"])
                if os.path.isfile(p):
                    foto = Image.open(p).convert("RGB")
                    return foto if incluido else _apagar_bloqueado(foto)
                # PRIORIDAD 2 (tema todavía sin cards generadas): la página
                # del cuaderno impreso — mejor que nada mientras se genera.
                seed = zlib.crc32(("%s|%s" % (tema, juego["id"])).encode())
                from cuaderno import _colorear_imgs, _escena_tema, _tema_palabras
                mons = _personajes_para_cards(tema, 8)
                colorear_imgs = _colorear_imgs(tema) if juego["id"] == "colorear" else []
                pagina = _juego_page(tema, edad, juego["id"], mons, _escena_tema(tema),
                                      colorear_imgs, _tema_palabras(tema), seed)
                if pagina is not None:
                    w = 700
                    h = max(1, int(pagina.height * w / pagina.width))
                    pagina = pagina.convert("RGB").resize((w, h), Image.LANCZOS)
                    return pagina if incluido else _apagar_bloqueado(pagina)
                return _render_juego_card_fallback(tema, _paleta(tema), juego["titulo"], incluido)
    except Exception:
        pass
    return preview_mock(data, tema)


def _armar_data_liviano(tema, nombre, edad):
    """Solo lo que necesita la portada (sin generar puzzles)."""
    from cuaderno import _tema_nombre
    titulo = ("Las actividades de %s" % nombre) if nombre else "Cuaderno de actividades"
    return {"titulo": titulo, "paleta": _paleta(tema),
            "tema_nombre": _tema_nombre(tema), "edad": edad}
