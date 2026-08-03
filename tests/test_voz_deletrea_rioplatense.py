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
// TODO en un solo eval: un `const` no sale del eval en el que se declaró
eval([/const _UNI = \[[\s\S]*?\];/, /const _DEC = \[[\s\S]*?\];/, /const _CEN = \[[\s\S]*?\];/,
      /function _numeroEnPalabras[\s\S]*?\n\}/, /const _SIGNOS = \{[\s\S]*?\};/,
      /const _ORDINAL_FRAC = \{[\s\S]*?\};/, /function _nombreDenominador[\s\S]*?\n\}/,
      /function _fraccionesEnPalabras[\s\S]*?\n\}/,
      /const _ES_CUENTA = [^\n]*/, /function _cuentaEnPalabras[\s\S]*?\n\}/,
      /const _NOMBRE_LETRA = \{[\s\S]*?\n\}/,
      /const _NOMBRE_ENTRE_COMILLAS = [\s\S]*?_NOMBRE_LETRA\);/,
      /function _deletrearParaLaVoz\(txt\) \{[\s\S]*?\n\}/]
     .map((re) => src.match(re)[0]).join(";\n"));
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
    # Hasta el `new Audio(`, que es donde se resuelve el archivo. Antes era una ventana
    # fija de 1200 caracteres y se rompió el 03-ago-2026 al agregar un comentario arriba:
    # el test se puso en rojo diciendo "el manifest dejó de buscarse con el texto
    # original" cuando el manifest seguía intacto 300 caracteres más abajo. Un test que
    # falla por dónde termina un comentario manda a buscar el bug donde no está.
    cuerpo = src[i:src.index("new Audio(", i) + 40]
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


def test_no_queda_notacion_fonetica_en_lo_que_se_escucha():
    """Encontrado escuchando lo que el player le manda a la voz, no leyendo el código: las
    explicaciones de fonética de 1.º decían "«sol» empieza con el sonido /s/". Escrito se
    entiende; hablado, el sintetizador lee las barras — "barra ese barra". Son 18 textos, y
    todos en las actividades que Pablo estaba revisando.

    No se arregló en la capa de voz sino en el TEXTO, porque la notación /x/ tampoco le
    aporta nada a un chico de 6 años que no la va a ver en ningún otro lado: ahora dice
    "empieza con el sonido de la «S»", que se entiende leído y hablado."""
    src = open(PLAYER, encoding="utf-8").read()
    quedan = re.findall(r'm: "([^"]*?/[a-záéíóúñ]{1,4}/[^"]*?)"', src)
    assert not quedan, "%d explicación(es) hablada(s) siguen con notación /fonema/: %s" % (
        len(quedan), quedan[:3])
    for aid, t in _textos_hablados():
        assert not re.search(r"/[a-záéíóúñ]{1,4}/", t), \
            "%s tiene notación fonética en algo que se escucha: %r" % (aid, t)
    assert decir(["«sol» empieza con el sonido de la «S»."]) == \
        ["«sol» empieza con el sonido de la ese."]


# ── las cuentas ──────────────────────────────────────────────────────────────────

def test_la_cuenta_se_dice_en_palabras():
    """Pablo, 31-jul-2026, probando 2.º EN PRODUCCIÓN: *"«760 + 1» dice «sitositoceta + 1»"*.

    La cuenta le llegaba en crudo al sintetizador y masticaba el número. Se resuelve
    escribiéndole lo que una maestra DICE. En pantalla sigue viéndose "760 + 1", que es lo
    que el chico tiene que aprender a leer; lo que cambia es cómo suena."""
    assert decir(["760 + 1"]) == ["setecientos sesenta más uno"]


@pytest.mark.parametrize("cuenta,dicho", [
    ("760 + 10", "setecientos sesenta más diez"),
    ("390 + 100", "trescientos noventa más cien"),
    ("100 + 1", "cien más uno"),               # "cien", no "ciento"
    ("21 + 1", "veintiuno más uno"),           # una palabra hasta el 29
    ("16 + 3", "dieciséis más tres"),
    ("1.000 + 1", "mil más uno"),              # el punto es separador de miles, no coma
    ("1.234 × 2", "mil doscientos treinta y cuatro por dos"),
    ("900 − 100", "novecientos menos cien"),   # el menos largo, no el guion
    ("7 × 10", "siete por diez"),
    ("2 + 3 × 4", "dos más tres por cuatro"),  # jerarquía de 6.º: dos operadores
    ("130 + ___ = 200", "ciento treinta más cuánto es igual a doscientos"),
])
def test_los_numeros_y_los_signos_se_dicen_como_se_dicen(cuenta, dicho):
    assert decir([cuenta]) == [dicho]


def test_solo_se_convierte_cuando_el_texto_ENTERO_es_una_cuenta():
    """Un número adentro de una frase se lee bien y no se toca: cuanto menos se reescriba,
    menos se rompe. Si mañana esto se afloja, se empiezan a deletrear años y porcentajes."""
    for t in ("Da 761.", "Tocá dos burbujas que sumen 10",
              "Argentina es un país muy urbanizado: más del 90% vive en ciudades."):
        assert decir([t]) == [t], "se reescribió una frase que no es una cuenta: %r" % t


def test_las_seis_actividades_que_dicen_una_cuenta_pelada_quedan_cubiertas():
    """Medido el 31-jul-2026: seis plantillas del catálogo tienen como PREGUNTA una cuenta
    y nada más. No era un caso suelto de la pantalla que Pablo abrió."""
    import re as _re
    CUENTA = _re.compile(r"^[\d\s.,+\-−×÷=<>_?¿]+$")
    con_cuenta = []
    for a in cur.CATALOGO:
        p = a.get("plantilla")
        if p and p.get("q") and CUENTA.match(_re.sub(r"\{[a-z_]+\}", "760", p["q"])):
            con_cuenta.append(a["id"])
    assert len(con_cuenta) >= 6, "quedaron %d: %s" % (len(con_cuenta), con_cuenta)
    muestras = [_re.sub(r"\{[a-z_]+\}", "760", a["plantilla"]["q"])
                for a in cur.CATALOGO if a["id"] in con_cuenta]
    for m, d in zip(muestras, decir(muestras)):
        assert d != m, "«%s» sigue yendo en crudo a la voz" % m
        assert not _re.search(r"\d", d), "quedaron dígitos sin decir: %r" % d


# ── lo que apareció barriendo TODO lo hablado ────────────────────────────────────

@pytest.mark.parametrize("texto,dicho", [
    ("1/2", "un medio"),
    ("3/4", "tres cuartos"),
    ("1/12 de la torta", "un doceavo de la torta"),
    ("5/15 se simplifica", "cinco quinceavos se simplifica"),
    ("3/40 de la clase", "tres cuarentavos de la clase"),
    ("1/100", "un centésimo"),
])
def test_las_fracciones_se_dicen_como_se_llaman(texto, dicho):
    """*"Seguí con la voz"*. Barriendo las 6607 frases habladas del cuaderno aparecieron 66
    fracciones escritas "3/4", en las unidades de 5.º y 6.º que JUSTAMENTE enseñan
    fracciones. Medido contra el sintetizador, "3/4" tarda más que "tres cuartos": no lo
    está diciendo como fracción."""
    assert decir([texto]) == [dicho]


def test_la_barra_de_fraccion_no_se_dice_dividido():
    """En este catálogo la división se escribe con ÷. Decir "tres dividido cuatro" en la
    unidad que enseña fracciones sería enseñar otra cosa."""
    d = decir(["2/3 × 4/4 = 8/12"])[0]
    assert d == "dos tercios por cuatro cuartos es igual a ocho doceavos"
    assert "dividido" not in d


def test_los_signos_adentro_de_una_frase_tambien_se_dicen():
    """Después de convertir las fracciones el texto ya no es una cuenta pelada, así que los
    signos sueltos quedaban sin decir."""
    assert decir(["Hidro = agua: la fuerza del agua mueve las turbinas."]) == \
        ["Hidro es igual a agua: la fuerza del agua mueve las turbinas."]


def test_no_toca_los_guiones_que_no_son_restas():
    """«2-6-3-4-5» es una posición, no cinco restas. Por eso el guion común queda afuera y
    sólo entra el «−» largo, que es el signo matemático."""
    t = "Cada sumando ocupa su posición: 2-6-3-4-5."
    assert decir([t]) == [t]


def test_la_flecha_se_lee_como_la_pausa_que_es():
    """«Municipio → intendente» es una correspondencia. Una coma la lee bien y no depende de
    que el sintetizador sepa qué hacer con el símbolo."""
    assert decir(["Municipio → intendente; provincia → gobernador."]) == \
        ["Municipio, intendente; provincia, gobernador."]


def test_los_grados_de_temperatura_si_y_los_de_orden_no():
    """El «°» se usa para DOS cosas distintas en el cuaderno: temperatura («100 °C») y orden
    («el 1° puesto»). Sólo se toca la primera; la segunda ya se dice bien."""
    assert decir(["A 100 °C hierve; a 0 °C se congela."]) == \
        ["A 100 grados hierve; a 0 grados se congela."]
    t = "Para el 1° hay 5 candidatos; para el 2°, uno menos."
    assert decir([t]) == [t]


def test_los_decimales_no_se_tocan():
    """«0,35» en español se lee «cero coma treinta y cinco», que es lo correcto. Meterse ahí
    sería arreglar algo que no está roto."""
    t = "0,35 cae justo entre los dos."
    assert decir([t]) == [t]


def test_un_entero_escrito_como_fraccion_se_dice_sobre_uno():
    """«5 es 5/1» es como se enseña que un entero también es una fracción. No existe
    "cinco unavos": ahí se dice "cinco sobre uno"."""
    assert decir(["5 es 5/1; dado vuelta queda 1/5."]) == \
        ["5 es cinco sobre uno; dado vuelta queda un quinto."]


def test_una_fraccion_al_final_de_la_oracion_tambien_se_convierte():
    """El punto final NO es un punto decimal. Con un lookahead que rechazaba cualquier
    punto, «da 3/6.» se quedaba sin convertir — y así termina la mitad de las
    explicaciones. Quedaban 44 sin tocar por este solo motivo."""
    assert decir(["1/2 amplificada por 3 da 3/6."]) == \
        ["un medio amplificada por 3 da tres sextos."]
    assert decir(["1/2,5 no es fracción"]) == ["1/2,5 no es fracción"]


def test_no_queda_NADA_sin_decir_en_todo_el_cuaderno():
    """El barrido completo, que es lo que Pablo pidió con *"seguí con la voz"*: las 6607
    frases que el cuaderno dice, pasadas por la función real, sin que quede una fracción con
    barra, un signo suelto, una notación de fonema, una flecha, un grado ni una «uve».

    Este test es el que evita seguir arreglando de a uno lo que el chico va encontrando."""
    import re as _re
    textos = [t for _, t in _textos_hablados()]
    dichos = decir(textos)
    PATRONES = [
        ("fracción con barra", _re.compile(r"\d\s*/\s*\d")),
        ("signo suelto", _re.compile(r"(^|\s)[+×÷=<>−](\s|$)")),
        ("notación /fonema/", _re.compile(r"/[a-záéíóúñ]{1,5}/")),
        ("flecha", _re.compile(r"→|←|↔")),
        ("grados C", _re.compile(r"\d\s*°\s*C")),
        ("V o W suelta", _re.compile(
            r"(^|[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ])[VW](?![A-Za-zÁÉÍÓÚÜÑáéíóúüñ])")),
    ]
    malos = []
    for t, d in zip(textos, dichos):
        for nombre, rx in PATRONES:
            if rx.search(d):
                malos.append("%s → %s" % (nombre, d[:80]))
    assert not malos, "%d frase(s) siguen con algo sin decir:\n  %s" % (
        len(malos), "\n  ".join(malos[:6]))


# ── una CUENTA adentro de una frase (03-ago-2026) ──────────────────────────────────────
# Pablo, en «La cuenta paso a paso» de 5.º: *"al final habla mal"*. El cierre dice
# «305 ÷ 6 = 50 y sobran 5»: como tiene palabras no era "una cuenta pelada", así que sólo
# se le traducían los SIGNOS y quedaba «305 dividido 6 es igual a 50» — la mitad en
# palabras y la mitad en cifras. Y la MISMA cuenta sola sí se decía bien, o sea que el
# cuaderno se contradecía a sí mismo.

@pytest.mark.parametrize("frase,dicho", [
    ("305 ÷ 6 = 50 y sobran 5",
     "trescientos cinco dividido seis es igual a cincuenta y sobran 5"),
    ("¡No sobró nada! 305 ÷ 6 = 50",
     "¡No sobró nada! trescientos cinco dividido seis es igual a cincuenta"),
    ("Sobran 5. Comprobá: 50 × 6 + 5 = ?",
     "Sobran 5. Comprobá: cincuenta por seis más cinco es igual a ?"),
])
def test_una_cuenta_adentro_de_una_frase_se_dice_entera_en_palabras(frase, dicho):
    assert decir([frase]) == [dicho]


def test_esto_NO_afloja_la_regla_de_los_numeros_en_prosa():
    """El control de la regla nueva. Hace falta un OPERADOR ENTRE DOS NÚMEROS para
    entrar: un número suelto en una frase se sigue leyendo tal cual. Sin este límite se
    empezarían a deletrear años, porcentajes y cantidades — que es justo lo que el test
    de más arriba viene cuidando desde el 31-jul."""
    for t in ("Da 761.", "Tocá dos burbujas que sumen 10",
              "Argentina es un país muy urbanizado: más del 90% vive en ciudades.",
              "En 1810 empezó la Revolución de Mayo."):
        assert decir([t]) == [t], "se reescribió un número que está en prosa: %r" % t


def test_el_guion_en_prosa_no_se_toma_como_resta():
    """«páginas 5 - 7» es un rango, no una cuenta. El menos matemático se escribe «−»."""
    assert decir(["Leé las páginas 5 - 7 del libro."]) == ["Leé las páginas 5 - 7 del libro."]


# ── acá la plata es en PESOS (03-ago-2026) ─────────────────────────────────────────────
# Pablo, en «Proporcionalidad aplicada» de 6.º: *"tiene que decir pesos y no dólares.
# Fijate en otros casos que hable de dinero"*.
#
# En pantalla el «$» está bien —así se escribe el peso acá— pero el sintetizador lo lee
# como dólares. Son 10 actividades del catálogo, de 1.º a 7.º, más las explicaciones del
# "¿Cómo es?" del player. Por eso se arregla en la VOZ y no en el texto: escribir
# "1200 pesos" en pantalla no es como se escribe un precio.

@pytest.mark.parametrize("frase,dicho", [
    ("Si 3 alfajores cuestan $1.200, ¿cuánto cuestan 8 alfajores?",
     "Si 3 alfajores cuestan 1.200 pesos, ¿cuánto cuestan 8 alfajores?"),
    ("Da $3.200.", "Da 3.200 pesos."),                       # el punto final no se traga
    ("Para $1 podés usar una moneda.", "Para 1 peso podés usar una moneda."),  # singular
    ("$0,50 es medio peso.", "0,50 pesos es medio peso."),   # centavos con coma
    ("Con $3.000 el vuelto es $909", "Con 3.000 pesos el vuelto es 909 pesos"),
])
def test_el_signo_pesos_se_dice_pesos(frase, dicho):
    assert decir([frase]) == [dicho]


def test_nunca_dice_dolares():
    """El síntoma tal cual lo escuchó Pablo. Es el catálogo del Diseño Curricular
    porteño: la plata es en pesos."""
    for d in decir(["Si 3 alfajores cuestan $1.200, ¿cuánto cuestan 8?",
                    "$10.000 con 30% off → pagás $7.000"]):
        assert "$" not in d, "quedó un signo que la voz va a leer como dólares: %r" % d


def test_la_plata_se_convierte_ANTES_que_las_cuentas():
    """Si corriera después, «$1.200 ÷ 3» ya sería «mil doscientos dividido tres» y el «$»
    quedaría suelto pegado a una palabra — peor que el problema original."""
    d = decir(["Primero cuánto sale UNO: $1.200 ÷ 3."])[0]
    assert d == "Primero cuánto sale UNO: 1.200 pesos dividido 3."
    assert "$" not in d


def test_ninguna_actividad_del_catalogo_queda_diciendo_dolares():
    """La barrida completa: se pasa por la voz TODO texto del catálogo que tenga «$» y se
    exige que no quede ninguno. Es lo que contesta el "fijate en otros casos" sin que
    haya que ir actividad por actividad."""
    textos = []
    for a in cur.CATALOGO:
        for t in re.findall(r'"([^"]*\$[^"]*)"', json.dumps(a, ensure_ascii=False)):
            t = re.sub(r"\{[a-z_]+\}", "1200", t.replace("\\u00e1", "á"))
            # `plantilla.unidad` es "$" pelado: una etiqueta de FORMATO que el player
            # antepone al número en pantalla ("Armá $500"), no una frase que se hable.
            # Sin esta línea el test exigía convertir un símbolo suelto, que nadie dice.
            if re.search(r"\$\s*\d", t):
                textos.append(t)
    assert textos, "no se encontró ninguna actividad con dinero: la barrida no probó nada"
    for original, dicho in zip(textos, decir(textos)):
        assert "$" not in dicho, "sigue diciendo dólares: %r → %r" % (original, dicho)
