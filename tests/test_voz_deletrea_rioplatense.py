# -*- coding: utf-8 -*-
"""Las letras se deletrean como se dicen acá, no como en España.

Pablo, 31-jul-2026: *"«cómo se escribe vaca» dice que va con «u-ve», así lo pronuncia, y
nosotros decimos «ve corta»"*, y enseguida: *"y le decimos «i griega», revisalo en todos
los cuadernos"*.

NO ERA UN CASO SUELTO DE 2.º. Medido sobre el catálogo entero, **19 actividades** del catálogo deletrean
alguna letra que hay que renombrar —31 si se cuenta la Y— entre ortografía, homófonos,
fonética de 1.º, sílabas y números romanos.

LO QUE HACE QUE ESTO NO SEA UN `replace` Y PUNTO: la Y. De sus 15 apariciones sueltas en el
catálogo, **una sola es la letra**; las otras catorce son la conjunción al empezar la
oración ("Y esto quedó en la Constitución", "Y llevamos uno a la próxima columna").
Deletrearlas habría dejado el cuaderno peor que antes.

De ahí las dos reglas:

  1. Letra entre « », que en este catálogo ya significa "esto, como token": SIEMPRE es la
     letra — ahí entra la Y. Con UNA excepción: la «y» minúscula, que es la conjunción
     entrecomillada ("el «y» reemplaza a la última coma").
  2. Letra suelta en mayúscula: sólo las que no son además palabra del español. Las vocales
     no hacen falta (su nombre es la letra misma) y la Y queda afuera a propósito.

SÓLO TOCA LO QUE SE ESCUCHA. Lo que se VE sigue diciendo «V»: es una actividad de
ortografía, el chico tiene que ver la letra. Y el manifest se busca con el texto ORIGINAL,
así que los mp3 ya grabados siguen sirviendo — se verificó que ninguno tenía letras sueltas.
"""
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import actividades_curriculum as cur  # noqa: E402
import actividades_web as aw  # noqa: E402

PLAYER = os.path.join(_BASE, "actividades_player.js")

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")

_ARNES = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
// se corren las funciones REALES del player: una copia acá se desincronizaría al primer
// cambio y el test dejaría de medir lo que escucha el chico
eval(src.match(/const _NOMBRE_LETRA = \{[\s\S]*?\n\}/)[0] + ";"
   + src.match(/const _NOMBRE_ENTRE_COMILLAS = [\s\S]*?_NOMBRE_LETRA\);/)[0] + ";"
   + src.match(/function _deletrearParaLaVoz\(txt\) \{[\s\S]*?\n\}/)[0]);
// los textos entran por ARCHIVO: el catálogo son 4348 frases y por línea de comandos
// revienta con "Argument list too long"
const textos = JSON.parse(fs.readFileSync(%s, "utf8"));
console.log(JSON.stringify(textos.map(_deletrearParaLaVoz)));
"""


def decir(textos, tmp_path=None):
    """Cómo suenan esos textos, pasándolos por la función real del player."""
    import tempfile
    fd, entrada = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(list(textos), f)
        js = _ARNES % (json.dumps(PLAYER), json.dumps(entrada))
        r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=120)
        assert r.returncode == 0, r.stderr[-1500:]
        return json.loads(r.stdout.strip())
    finally:
        os.unlink(entrada)


# ── lo que Pablo pidió ───────────────────────────────────────────────────────────

def test_la_v_se_dice_ve_corta():
    """EL caso: «cómo se escribe vaca» decía "va con u-ve"."""
    assert decir(["Va con V: vaca."]) == ["Va con ve corta: vaca."]


def test_la_y_se_dice_i_griega_cuando_es_la_letra():
    assert "i griega" in decir(
        ["Antes de una palabra que empieza con I o HI, la «Y» se cambia por «E»."])[0]


def test_la_be_y_la_ve_se_distinguen():
    """En una actividad que enseña JUSTO a distinguirlas, "be" y "uve" se parecen
    demasiado; "be larga" y "ve corta" es el par con el que se enseña acá."""
    dicho = decir(["Va con B: barco.", "Del verbo tener: tuvo, con V."])
    assert "be larga" in dicho[0] and "ve corta" in dicho[1]


@pytest.mark.parametrize("texto,esperado", [
    ("Va con LL: silla.", "doble ele"),
    ("Va con Z y con RR: zorro.", "zeta"),
    ("Va con Z y con RR: zorro.", "doble erre"),
    ("El sonido /ke/ se escribe QU: queso.", "cu"),
    ("Se escribe NV: invierno.", "ene ve corta"),
    ("La CH es un solo sonido.", "che"),
])
def test_los_digrafos_tambien(texto, esperado):
    assert esperado in decir([texto])[0]


# ── lo que NO se puede tocar ─────────────────────────────────────────────────────

@pytest.mark.parametrize("texto", [
    "Y esto quedó en la Constitución nacional.",
    "Y llevamos uno a la próxima columna.",
    "Con Y tienen que cumplirse las dos.",
    "En español se abre Y se cierra.",
])
def test_la_conjuncion_y_no_se_deletrea(texto):
    """LA razón por la que esto no es un replace a ciegas: 14 de las 15 Y del catálogo son
    la conjunción. Deletrearlas sería peor que el problema que vinimos a arreglar."""
    assert decir([texto]) == [texto]


@pytest.mark.parametrize("texto", [
    "«Pan, leche y queso»: el «y» reemplaza a la última coma.",
    "Dos núcleos coordinados por «y».",
])
def test_la_y_entrecomillada_en_minuscula_sigue_siendo_la_conjuncion(texto):
    """El choque que apareció al ampliar la regla a minúsculas: en estas la «y» está
    entrecomillada pero es la CONJUNCIÓN, no la letra."""
    assert decir([texto]) == [texto]


@pytest.mark.parametrize("texto", [
    "XX (20) + IX (9).",
    "XL (40) + IV (4).",
    "El DC lo pide así: narrar en pasado.",
    "Armá la palabra MOTO: tocá las sílabas en orden",
    "CASA empieza con C.",
])
def test_no_deletrea_lo_que_no_es_una_letra(texto):
    """Números romanos de dos signos, siglas y palabras en mayúscula quedan como están.
    (En CASA sí se deletrea la C final, que es la letra: lo que no se toca es la palabra.)"""
    salida = decir([texto])[0]
    for palabra in re.findall(r"\b(?:XX|XL|IX|IV|DC|MOTO|CASA)\b", texto):
        assert palabra in salida, "se deletreó %r, que no es una letra" % palabra


def test_los_numeros_romanos_se_leen_bien():
    """Salen correctos solos: «V» ES la letra uve, así que "ve corta igual cinco" es lo que
    hay que decir. Este test está para que se note si alguien lo "arregla" al revés."""
    d = decir(["Las letras base: I=1, V=5, X=10, L=50, C=100, D=500, M=1000."])[0]
    assert "ve corta=5" in d and "equis=10" in d and "I=1" in d


# ── que siga sirviendo lo que ya estaba grabado ──────────────────────────────────

def test_ningun_mp3_grabado_queda_desincronizado():
    """El manifest se busca con el texto ORIGINAL, así que los mp3 siguen andando. Este test
    fija además el hecho que lo hace seguro: ninguna frase grabada deletrea una letra, así
    que no hay audio viejo diciendo "uve" que haya que regrabar."""
    src = open(PLAYER, encoding="utf-8").read()
    i = src.index("function reproducirConsigna(")
    cuerpo = src[i:i + 1200]
    assert "AudioManifest[txt]" in cuerpo, "el manifest dejó de buscarse con el texto original"
    assert "_deletrearParaLaVoz(txt)" in cuerpo, "el deletreo no llega al sintetizador"
    m = json.load(open(os.path.join(aw.AUDIO_DIR, "manifest.json"), encoding="utf-8"))
    TOK = re.compile(r"(^|[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ])([BCDFGHJKLMNPQRSTVWXZ]{1,2})"
                     r"(?![A-Za-zÁÉÍÓÚÜÑáéíóúüñ])")
    con_letra = [k for k in m if TOK.search(k)]
    assert not con_letra, "hay %d mp3 grabado(s) que deletrean una letra: %s" % (
        len(con_letra), con_letra[:3])


# ── el barrido completo, que es lo que Pablo pidió ───────────────────────────────

def _textos_hablados():
    out = []
    for a in cur.CATALOGO:
        if a.get("consigna"):
            out.append((a["id"], a["consigna"]))
        for b in (a.get("banco") or []):
            if isinstance(b, dict) and b.get("m"):
                out.append((a["id"], b["m"]))
    return out


def test_no_queda_ninguna_uve_en_todo_el_catalogo():
    """*"Revisalo en todos los cuadernos"*. Se pasa el catálogo ENTERO por la función real y
    se verifica que no quede una sola V o W suelta sin nombre rioplatense — que son las dos
    que el sintetizador dice con "uve"."""
    textos = _textos_hablados()
    dichos = decir([t for _, t in textos])
    UVE = re.compile(r"(^|[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ])([VW])(?![A-Za-zÁÉÍÓÚÜÑáéíóúüñ])")
    quedan = [(aid, t) for (aid, t), d in zip(textos, dichos) if UVE.search(d)]
    assert not quedan, "%d texto(s) siguen diciendo «uve»: %s" % (
        len(quedan), quedan[:3])


def test_el_barrido_cubre_todo_el_catalogo():
    """Piso MEDIDO el 31-jul-2026, y el número importa porque Pablo pidió "revisalo en todos
    los cuadernos": **19 actividades** del catálogo deletrean alguna letra que hay que
    renombrar (31 si se cuenta la Y, pero de esas la mayoría es la conjunción). Si mañana el
    barrido cubre menos, es que alguien acotó el alcance sin decirlo."""
    TOK = re.compile(r"(^|[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ])([BCDFGHJKLMNPQRSTVWXZ]{1,2})"
                     r"(?![A-Za-zÁÉÍÓÚÜÑáéíóúüñ])")
    tocadas = {aid for aid, t in _textos_hablados() if TOK.search(t)}
    assert len(tocadas) >= 19, "el barrido bajó a %d actividades (eran 19)" % len(tocadas)


def test_las_parejas_de_letras_se_entienden_habladas():
    """Las explicaciones decían «T y t.», que hablado no dice nada: la voz no distingue
    mayúscula de minúscula. Ahora lo dicen con todas las letras."""
    a = [x for x in cur.CATALOGO if x["id"] == "parejas_letras_1"][0]
    flojas = [b["m"] for b in a["banco"] if "mayúscula" not in b["m"]]
    assert not flojas, "quedan explicaciones que hablado no se entienden: %s" % flojas
    assert decir(["«M» mayúscula y «m» minúscula son la misma letra."]) == \
        ["eme mayúscula y eme minúscula son la misma letra."]
