"""El banderín del kit deletrea el nombre: UNA letra por banderín (Pablo, 16-ago-2026).

Antes el kit traía un solo banderín con la escena del tema y sin nombre. El riesgo de
regresión es silencioso: si esto se rompe, el kit sigue saliendo con 14 piezas y nadie
mira el banderín hasta que un cliente imprime la guirnalda y no dice nada.

Los tests miran PÍXELES, no el conteo de piezas: la falla que importa es "el banderín
salió sin letras", y eso no se ve en ninguna lista de archivos.
"""
import os

import pytest
from PIL import Image

import piezas
import productos

_PROY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lamina(tema="safari"):
    p = os.path.join(_PROY, "temas", tema, "extras", "banderin.png")
    if not os.path.exists(p):
        pytest.skip("el tema %s no tiene lámina de banderín" % tema)
    return p


def _tinta(img, umbral=110):
    """Cuántos píxeles oscuros tiene la imagen. La letra es tinta sobre un disco claro,
    así que sube cuando hay letra y no sube si el disco salió vacío."""
    g = img.convert("L").resize((400, 560))
    return sum(1 for p in g.getdata() if p < umbral)


def test_una_hoja_por_nombre_y_no_es_la_lamina_pelada():
    hoja = piezas.banderin_letras(_lamina(), {"nombre": "Tomás", "edad": "5"}, "safari")
    assert hoja is not None
    assert hoja.size == piezas.A4, "la guirnalda se imprime en A4"


def test_las_letras_se_dibujan_de_verdad():
    """Control del CAMINO DIBUJADO (el que corre en los temas sin abecedario ilustrado):
    la misma hoja, con el dibujo de texto anulado, tiene que dejar menos tinta.

    Fuerza el camino dibujado a propósito. Cuando safari ganó su abecedario, este test
    empezó a fallar porque la letra ya no la dibuja `txt` sino la imagen — o sea que
    estaba midiendo bien, y lo que cambió fue por dónde pasa el kit."""
    lam = _lamina()
    original_letra = piezas.letra_dibujada
    piezas.letra_dibujada = lambda tema, letra: None
    original_txt = piezas.txt
    try:
        con_letras = piezas.banderin_letras(lam, {"nombre": "ABC", "edad": "5"}, "safari")
        piezas.txt = lambda *a, **k: None      # el disco se dibuja igual; la letra no
        sin_letras = piezas.banderin_letras(lam, {"nombre": "ABC", "edad": "5"}, "safari")
    finally:
        piezas.txt = original_txt
        piezas.letra_dibujada = original_letra
    assert _tinta(con_letras) > _tinta(sin_letras) * 1.05


def test_cada_letra_va_en_su_banderin():
    """Dos nombres del mismo largo con letras distintas dan hojas DISTINTAS. Si el
    banderín ignorara la letra, las dos serían idénticas."""
    lam = _lamina()
    a = piezas.banderin_letras(lam, {"nombre": "AAAA", "edad": "5"}, "safari")
    b = piezas.banderin_letras(lam, {"nombre": "WXYZ", "edad": "5"}, "safari")
    assert list(a.getdata()) != list(b.getdata())


def test_mas_letras_mas_banderines():
    """La grilla crece con el nombre: 3 letras y 11 letras no pueden dar la misma hoja."""
    lam = _lamina()
    corto = piezas.banderin_letras(lam, {"nombre": "Ana", "edad": "5"}, "safari")
    largo = piezas.banderin_letras(lam, {"nombre": "Maximiliano", "edad": "5"}, "safari")
    assert _tinta(largo) > _tinta(corto), "11 banderines tienen que dejar más tinta que 3"


@pytest.mark.parametrize("n,esperado", [(1, (2, 2)), (4, (2, 2)), (5, (2, 3)), (6, (2, 3)),
                                        (7, (3, 3)), (9, (3, 3)), (10, (3, 4)), (12, (3, 4))])
def test_grilla_por_largo_de_nombre(n, esperado):
    assert piezas._grilla_banderines(n) == esperado


def test_sin_nombre_no_rompe_el_kit():
    """Sin nombre no hay letras que repartir: devuelve None y quien llama cae a la
    lámina de siempre. Un kit sin banderín sería peor que uno sin nombre."""
    for vacio in ("", "   ", None):
        assert piezas.banderin_letras(_lamina(), {"nombre": vacio}, "safari") is None


def test_nombre_larguisimo_no_explota():
    hoja = piezas.banderin_letras(_lamina(), {"nombre": "A" * 40, "edad": "5"}, "safari")
    assert hoja is not None and hoja.size == piezas.A4


def test_el_kit_usa_el_banderin_con_letras():
    """El enganche: la pieza `banderin` del kit tiene que salir por banderin_letras.
    Sin esto, la función existiría y el kit seguiría trayendo la lámina pelada — que es
    exactamente el bug que se estaba arreglando."""
    llamadas = []
    original = piezas.banderin_letras

    def espia(lamina_path, data, tema=None):
        llamadas.append(tema)
        return original(lamina_path, data, tema)

    piezas.banderin_letras = espia
    try:
        fn = productos._mk_extra_fijo(_lamina(), "safari", "banderin")
        img = fn({"nombre": "Tomás", "edad": "5"})
    finally:
        piezas.banderin_letras = original
    assert llamadas == ["safari"], "el kit no pasó por banderin_letras"
    assert isinstance(img, Image.Image)


def test_otras_piezas_no_se_tocaron():
    """Las demás piezas por lámina siguen saliendo por el overlay de texto de siempre."""
    llamadas = []
    original = piezas.banderin_letras
    piezas.banderin_letras = lambda *a, **k: llamadas.append(1)
    try:
        p = os.path.join(_PROY, "temas", "safari", "extras", "etiquetas_multiuso.png")
        if not os.path.exists(p):
            pytest.skip("sin lámina de etiquetas para comparar")
        productos._mk_extra_fijo(p, "safari", "etiquetas_multiuso")({"nombre": "Tomás", "edad": "5"})
    finally:
        piezas.banderin_letras = original
    assert llamadas == [], "una pieza que no es el banderín pasó por banderin_letras"

def _celda(hoja, i, n_letras, margin=110, gap=48):
    """Recorta el banderín i de la hoja, con las mismas cuentas que make_sheet."""
    cols, rows = piezas._grilla_banderines(n_letras)
    W, H = piezas.A4
    cw = (W - 2 * margin - (cols - 1) * gap) // cols
    ch = (H - 2 * margin - (rows - 1) * gap) // rows
    r, c = divmod(i, cols)
    x, y = margin + c * (cw + gap), margin + r * (ch + gap)
    return hoja.crop((x, y, x + cw, y + ch))


def test_los_banderines_de_una_hoja_son_DISTINTOS_ENTRE_SI():
    """El defecto que arruina el producto: que la guirnalda salga «TTTTT» en vez de
    «TOMÁS». Comparar dos hojas de nombres distintos NO lo detecta —las dos cambian
    igual—; hay que comparar banderín contra banderín DENTRO de la misma hoja.

    Escrito porque una mutación que dibujaba siempre `letras[0]` pasó los otros ocho
    tests en verde.
    """
    hoja = piezas.banderin_letras(_lamina(), {"nombre": "AB", "edad": "5"}, "safari")
    uno, dos = _celda(hoja, 0, 2), _celda(hoja, 1, 2)
    assert uno.size == dos.size
    assert list(uno.getdata()) != list(dos.getdata()), \
        "los dos banderines salieron idénticos: la guirnalda no deletrea el nombre"


def test_cada_banderin_lleva_SU_letra_en_orden():
    """Más fino que el anterior: con «ABAB», el 1.º y el 3.º tienen que ser iguales
    (misma letra) y el 1.º y el 2.º distintos. Eso sólo pasa si cada banderín recibe la
    letra de SU posición."""
    hoja = piezas.banderin_letras(_lamina(), {"nombre": "ABAB", "edad": "5"}, "safari")
    c0, c1, c2 = (_celda(hoja, i, 4) for i in (0, 1, 2))
    assert list(c0.getdata()) == list(c2.getdata()), "la letra no se repite donde debería"
    assert list(c0.getdata()) != list(c1.getdata()), "todos los banderines dicen lo mismo"


def test_el_orden_de_las_letras_es_el_del_nombre():
    """«SÁMOT» en vez de «TOMÁS»: la guirnalda al revés sale bien en cada banderín y
    mal como palabra, así que ningún test simétrico la ve. Se usa un patrón ASIMÉTRICO
    —AAB— donde invertir cambia qué celdas coinciden.

    Escrito porque una mutación que dibujaba `letras[len-1-i]` pasó los diez tests
    anteriores en verde.
    """
    hoja = piezas.banderin_letras(_lamina(), {"nombre": "AAB", "edad": "5"}, "safari")
    c0, c1, c2 = (_celda(hoja, i, 3) for i in (0, 1, 2))
    assert list(c0.getdata()) == list(c1.getdata()), "las dos primeras deberían ser la misma letra"
    assert list(c1.getdata()) != list(c2.getdata()), "la tercera es otra letra"


# ---------------- abecedario ilustrado (temas/<tema>/letras/) ----------------

def _tiene_abecedario(tema="safari"):
    return piezas.letra_dibujada(tema, "A") is not None


def test_las_tildes_y_la_enie_tienen_su_archivo():
    """«Tomás» e «Iñaki» son nombres comunes acá: si la Ñ o las vocales con tilde no
    resuelven a un archivo, el nombre sale con un hueco en la guirnalda."""
    if not _tiene_abecedario():
        pytest.skip("safari todavía no tiene abecedario ilustrado")
    for letra in ("Ñ", "Á", "É", "Í", "Ó", "Ú"):
        assert piezas.letra_dibujada("safari", letra), "falta el banderín de " + letra


def test_usa_el_abecedario_ilustrado_cuando_existe():
    """Con abecedario, la hoja NO puede ser igual a la que dibuja el disco: si lo fuera,
    las 32 imágenes estarían en disco sin que el producto las use."""
    if not _tiene_abecedario():
        pytest.skip("safari todavía no tiene abecedario ilustrado")
    lam = _lamina()
    con = piezas.banderin_letras(lam, {"nombre": "AB", "edad": "5"}, "safari")

    original = piezas.letra_dibujada
    piezas.letra_dibujada = lambda tema, letra: None      # finge un tema sin abecedario
    try:
        sin = piezas.banderin_letras(lam, {"nombre": "AB", "edad": "5"}, "safari")
    finally:
        piezas.letra_dibujada = original
    assert list(con.getdata()) != list(sin.getdata())


def test_si_falta_UNA_letra_la_hoja_entera_va_dibujada():
    """Todo o nada. Media guirnalda ilustrada y media con disco tipografiado se ve peor
    que cualquiera de las dos parejas, y el que la imprime no puede arreglarlo."""
    if not _tiene_abecedario():
        pytest.skip("safari todavía no tiene abecedario ilustrado")
    lam = _lamina()
    original = piezas.letra_dibujada
    piezas.letra_dibujada = lambda tema, letra: None if letra == "B" else original(tema, letra)
    try:
        mixta = piezas.banderin_letras(lam, {"nombre": "AB", "edad": "5"}, "safari")
        piezas.letra_dibujada = lambda tema, letra: None
        toda_dibujada = piezas.banderin_letras(lam, {"nombre": "AB", "edad": "5"}, "safari")
    finally:
        piezas.letra_dibujada = original
    assert list(mixta.getdata()) == list(toda_dibujada.getdata()), \
        "faltando una letra, la hoja tiene que ir ENTERA con el método dibujado"


def test_un_tema_sin_abecedario_no_rompe():
    """princesas todavía no tiene letras ilustradas: tiene que seguir saliendo el kit."""
    p = os.path.join(_PROY, "temas", "princesas", "extras", "banderin.png")
    if not os.path.exists(p):
        pytest.skip("sin lámina de princesas")
    hoja = piezas.banderin_letras(p, {"nombre": "Emma", "edad": "5"}, "princesas")
    assert hoja is not None and hoja.size == piezas.A4
