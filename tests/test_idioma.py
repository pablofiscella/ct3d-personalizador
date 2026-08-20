"""El kit tiene que poder salir ENTERO en inglés, o entero en español. Nunca mitad y mitad.

POR QUÉ
───────
19-ago-2026. La tienda de Etsy (`Casa3DAR`) cobra en dólares y ese es el mercado que se
busca. Pero el kit imprime «¡Gracias por venir!» y «Confirmá»: vendérselo así a un comprador
de habla inglesa no tiene sentido.

QUÉ PROTEGE
───────────
1. Que **todo** lo que el motor puede llegar a imprimir tenga traducción. No los seis textos
   que uno recuerda: los 41 que hay de verdad, repartidos en CUATRO lugares distintos.
2. Que traducir no rompa el español, que es lo que hoy está vendiendo en Mercado Libre.
3. Que los marcadores (`{nombre}`, `{edad}`) sobrevivan a la traducción — es el error obvio:
   traducir «HAPPY BIRTHDAY Emma» en vez de la plantilla.

LA LECCIÓN QUE LO ORDENA
────────────────────────
Esta misma mañana, `test_ningun_layout_tiene_el_nombre_de_otro_chico` dejó pasar dos layouts
con «Tomás» fijo **porque su barrido miraba una sola de las formas** en que un layout guarda
texto. Un guardián protege exactamente hasta donde mira. Éste mira las cuatro:

    a) `temas.py` → `_EXTRAS_TEXTO`   (afiche, banderín, cajita, sorbetes, tarjeta)
    b) `temas/<tema>/tema.json`       (invitación y afiche de cada temática, y kit.titulo/lema)
    c) `temas/<tema>/layouts/*.json`  (lo que guardó el editor visual, campos Y `_nuevos`)
    d) `piezas.py` / `productos.py`   (los literales escritos en el código)

ALCANCE, DICHO EXPLÍCITO
────────────────────────
Cubre **el kit de 15 piezas**, que es lo que se va a publicar en Etsy. Los otros productos
(rutina, certificado, menú, cápsula del tiempo, rompecabezas, baby shower) siguen siendo
sólo en español: sus textos no están en la tabla y este test no los mira.
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import generador  # noqa: E402
import idioma  # noqa: E402
import piezas as pz  # noqa: E402
import productos  # noqa: E402
import temas  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Los literales que `piezas.py` y `productos.py` escriben a mano. Van listados acá porque
# un `grep` del código no distingue un texto que se imprime de uno que es un comentario.
# `test_los_literales_listados_siguen_en_el_codigo` verifica que la lista no se despegue.
LITERALES_DEL_CODIGO = [
    "¡Un añito salvaje!", "¡Dos añitos salvajes!", "¡Tres añitos salvajes!",
    "El primer añito de", "Los dos añitos de", "Los tres añitos de",
    "¡Cumplo %s!", "El cumple de", "¡Gracias por venir!", "cumple ",
    "¡Para pintar!", "Coloreá y decorá tu cumple",
]

# Un tpl que es SÓLO marcadores no lleva palabra que traducir: "{nombre}", "{fecha}".
_SOLO_MARCADORES = re.compile(r"^[\s{}\w]*$")


def _es_solo_marcadores(t):
    return bool(re.fullmatch(r"(\s*\{\w+\}\s*)+", t))


def _de_los_specs():
    """(a) los specs compartidos que `temas.py` inyecta en TODAS las temáticas."""
    out = []
    for cfg in temas._EXTRAS_TEXTO.values():
        out.append(cfg.get("tpl"))
        for c in (cfg.get("campos") or []):
            out.append(c.get("tpl"))
    return out


def _de_los_tema_json():
    """(b) la invitación y el afiche que declara cada temática, más kit.titulo/lema."""
    out = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "temas", "*", "tema.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for p in (d.get("piezas") or {}).values():
            for t in (p.get("text") or []):
                out.append(t.get("tpl"))
        k = d.get("kit") or {}
        out += [k.get("titulo"), k.get("lema")]
    return out


def _de_los_layouts():
    """(c) lo que guardó el editor visual — los campos Y la lista `_nuevos`.

    `_nuevos` es una LISTA, no un dict. Saltearla es el agujero exacto por el que se colaron
    dos «Tomás» fijos el 19-ago-2026."""
    out = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "temas", "*", "layouts", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for v in d.values():
            if isinstance(v, dict):
                out.append(v.get("tpl"))
        for n in (d.get("_nuevos") or []):
            if isinstance(n, dict):
                out.append(n.get("tpl"))
    return out


def _todo_lo_imprimible():
    vistos = []
    for t in (_de_los_specs() + _de_los_tema_json() + _de_los_layouts()
              + LITERALES_DEL_CODIGO):
        if isinstance(t, str) and t.strip() and not _es_solo_marcadores(t):
            vistos.append(t)
    return sorted(set(vistos))


# ── EL test ──────────────────────────────────────────────────────────────────

def test_todo_lo_que_se_imprime_tiene_traduccion_al_ingles():
    """Si alguien agrega una temática, o el editor guarda un texto nuevo, esto dice
    EXACTAMENTE cuál falta — en vez de dejar salir un kit mitad en inglés."""
    faltan = idioma.sin_traduccion(_todo_lo_imprimible(), "en")
    assert not faltan, (
        "estos textos se imprimen y NO tienen traducción al inglés. Agregalos a "
        "`idioma.EN` (la clave va normalizada con idioma._clave):\n  "
        + "\n  ".join("%r" % t for t in faltan))


def test_los_literales_listados_siguen_en_el_codigo():
    """La lista de arriba se escribe a mano, así que puede quedar vieja: si alguien borra o
    cambia un literal, la tabla de traducción se llena de entradas muertas y —peor— el
    barrido deja de mirar lo que sí se imprime.

    OJO: esto sólo dice que el literal EXISTE, no que esté enganchado a la traducción. Eso
    lo prueba `test_ninguna_pieza_DIBUJA_español_en_ingles`, que mira lo que se dibuja."""
    fuente = ""
    for f in ("piezas.py", "productos.py"):
        fuente += open(os.path.join(RAIZ, f), encoding="utf-8").read()
    perdidos = [t for t in LITERALES_DEL_CODIGO if t not in fuente]
    assert not perdidos, (
        "estos literales ya no están en piezas.py/productos.py — actualizá la lista:\n  "
        + "\n  ".join("%r" % t for t in perdidos))


def test_ninguna_pieza_DIBUJA_español_en_ingles(monkeypatch):
    """EL guardián de las piezas de código: intercepta `txt()` —por donde pasa TODO lo que
    esas piezas escriben— y mira lo que realmente se dibujó.

    POR QUÉ HIZO FALTA ÉSTE. Probando en rojo, un `git checkout` de más dejó `productos.py`
    sin el import de `idioma` y sin sus dos llamadas a `traducir`: la hoja para colorear
    volvió a decir «¡Para pintar!» en el kit en inglés. **Los 2107 tests siguieron en
    verde**, porque el de arriba sólo comprueba que el literal esté escrito en algún lado,
    y ahí seguía — suelto, sin traducir.

    Es, otra vez, la misma forma de error: el barrido miraba el texto, no el camino. Un
    literal desenganchado se ve exactamente igual que uno enganchado si sólo se lee el
    archivo. Por eso este test no lee: dibuja.

    `piezas.txt` y `productos.txt` se parchean por separado a propósito: `productos` hace
    `from piezas import txt`, así que son DOS nombres distintos y parchear uno solo dejaría
    la mitad del código sin mirar."""
    dibujados = []

    def espia(d, text, *a, **k):
        if isinstance(text, str) and text.strip():
            dibujados.append(text)

    monkeypatch.setattr(pz, "txt", espia)
    monkeypatch.setattr(productos, "txt", espia)

    data = {"nombre": "Emma", "edad": "5", "anyo": "2026", "idioma": "en"}
    for tema in ("safari", "monstruos"):
        for fn in (pz.topper_torta, pz.cupcakes, pz.etiquetas, pz.tags, productos.colorear):
            try:
                fn(data, tema)
            except Exception:                      # noqa: BLE001 — el render no es el punto
                pass

    quedaron = set()
    for t in dibujados:
        motivo = _rastro_de_español(t, (data["nombre"], data["edad"], data["anyo"]))
        if motivo:
            quedaron.add("%r  (%s)" % (t, motivo))
    assert not quedaron, (
        "estas piezas dibujan español con el kit en inglés — falta pasar el literal por "
        "`idioma.traducir()`:\n  " + "\n  ".join(sorted(quedaron)))


# ── que traducir no rompa lo que ya vende ────────────────────────────────────

def test_sin_idioma_NADA_cambia():
    """Los 11 kits están vendiendo en español en Mercado Libre desde el 17-ago. Un `data` sin
    `idioma` tiene que dar exactamente lo mismo que antes.

    Se afirma `idioma.de({}) == "es"` **explícito**: sin eso el test es ciego a la peor
    regresión posible acá —que el default se dé vuelta y los kits que ya se están vendiendo
    salgan en inglés—, porque cambiando el default y el paso-de-largo a la vez el resultado
    no se mueve. Lo mostró la prueba en rojo: la mutación quedaba verde."""
    assert idioma.IDIOMA_ORIGEN == "es"
    assert idioma.de({}) == "es"
    assert idioma.de({"nombre": "Valentina"}) == "es"
    campo = {"tpl": "¡FELIZ CUMPLE {nombre}!"}
    assert generador._field_text(campo, {"nombre": "Valentina"}) == "¡FELIZ CUMPLE Valentina!"
    assert generador._field_text(campo, {"nombre": "Valentina", "idioma": "es"}) == \
        "¡FELIZ CUMPLE Valentina!"
    assert pz.lema({"edad": "5"}, "safari") == "¡Cumplo 5!"
    assert pz.titulo({"nombre": "Valentina"}, "safari") == "El cumple de"


def test_un_idioma_que_no_existe_cae_en_español():
    """Que llegue basura en el campo no puede romperle el kit a nadie.

    Se prueba `idioma.de()` de frente y no sólo el render: por el render solo, un idioma
    inventado sale en español igual —`traducir()` no encuentra tabla y devuelve el
    original—, así que el test pasaba aunque `de()` dejara pasar cualquier cosa."""
    for basura in ("fr", "", None, "xx", 7, ["en"], {"a": 1}, 0):
        assert idioma.de({"idioma": basura}) == "es", basura
    assert idioma.de("no soy un dict") == "es"
    campo = {"tpl": "¡Gracias por venir!"}
    for basura in ("fr", "", None, "xx", 7, ["en"]):
        assert generador._field_text(campo, {"idioma": basura}) == "¡Gracias por venir!"
    # y las mayúsculas / el locale largo SÍ se aceptan: "EN", "en-US" son inglés
    assert idioma.de({"idioma": "EN"}) == "en"
    assert idioma.de({"idioma": "en-US"}) == "en"


# ── que el inglés salga bien ─────────────────────────────────────────────────

def test_el_marcador_SOBREVIVE_a_la_traduccion():
    """El error obvio sería traducir el resultado («HAPPY BIRTHDAY Emma») en vez de la
    plantilla: ahí habría que adivinar qué parte es el dato del comprador."""
    campo = {"tpl": "¡FELIZ CUMPLE {nombre}!"}
    assert generador._field_text(campo, {"nombre": "Emma", "idioma": "en"}) == \
        "HAPPY BIRTHDAY Emma!"
    # y con un nombre que se parece a una palabra traducible, tampoco se toca
    assert generador._field_text(campo, {"nombre": "Cumple", "idioma": "en"}) == \
        "HAPPY BIRTHDAY Cumple!"


def test_el_plural_de_la_edad_en_ingles():
    """«Turning 1 years old» no existe. El motor ya arreglaba el plural español; al sumar
    idiomas esa regla dejó de ser una sola."""
    campo = {"tpl": "Cumple {edad} años"}
    assert generador._field_text(campo, {"edad": "1", "idioma": "en"}) == "Turning 1 year old"
    assert generador._field_text(campo, {"edad": "5", "idioma": "en"}) == "Turning 5 years old"
    assert generador._field_text(campo, {"edad": "1"}) == "Cumple 1 año"
    assert generador._field_text(campo, {"edad": "5"}) == "Cumple 5 años"


def test_lo_que_escribio_el_CLIENTE_no_se_traduce():
    """`_text` son las palabras del comprador, no del diseño: salen tal cual.

    El texto de prueba tiene que ser uno que SÍ esté en la tabla. La primera versión usaba
    «Fiesta de Emma», que no está, así que traducirlo lo dejaba igual y el test pasaba aun
    con el bug puesto — lo delató la prueba en rojo. Un caso de prueba que el bug no puede
    tocar no prueba nada."""
    frase = "¡Gracias por venir!"
    assert idioma.traducir(frase, "en") != frase, "el caso de prueba tiene que ser traducible"
    campo = {"tpl": "otra cosa", "_text": frase}
    assert generador._field_text(campo, {"idioma": "en"}) == frase


def test_las_piezas_de_CODIGO_tambien_hablan_ingles():
    """`piezas.py` arma texto por su cuenta, sin pasar por los specs: es la cuarta forma, y
    la más fácil de olvidar."""
    en = {"edad": "5", "nombre": "Emma", "idioma": "en"}
    assert pz.lema(en, "safari") == "I'm turning 5!"
    assert pz.titulo(en, "safari") == "The birthday party of"
    assert pz.lema_edad({"edad": "1", "idioma": "en"}) == "One year wild!"
    assert pz.titulo_edad({"edad": "1", "idioma": "en"}) == "The first birthday of"


# ── de punta a punta, sobre las 15 piezas de verdad ──────────────────────────

_ACENTOS = re.compile(r"[áéíóúñ¡¿ÁÉÍÓÚÑ]")

# Las claves de la tabla son, por definición, TODO el español que el motor sabe imprimir.
# Van de más larga a más corta para que el aviso nombre la frase entera y no un pedazo.
_CLAVES_ES = tuple(sorted(idioma.EN, key=len, reverse=True))


def _rastro_de_español(t, datos=()):
    """¿Este texto dibujado quedó en español? Devuelve qué lo delata, o None.

    Buscar acentos NO alcanza, y lo mostró una prueba en rojo: al desenganchar
    «cumple » + edad, la pieza volvió a dibujar «cumple 5» y el test siguió verde, porque
    esa frase no tiene una sola tilde. La mitad del español del proyecto no lleva acento
    («al cumple de», «El cumple de», «Bienvenidos al cumple de»).

    Por eso hay dos redes:
      1. las CLAVES de la tabla — exacto, no heurístico: si se dibuja una frase que el
         motor sabe traducir, es que no pasó por la traducción;
      2. los acentos — para el español que ni siquiera está en la tabla todavía, que es el
         caso de «alguien agregó una temática nueva».
    """
    limpio = t
    for v in datos:                    # los datos del comprador no son del diseño
        if isinstance(v, str) and v.strip():
            limpio = limpio.replace(v, " ")
    if _ACENTOS.search(limpio):
        return "acento"
    n = " ".join(limpio.split()).casefold()
    for k in _CLAVES_ES:
        if k and k in n:
            return "frase de la tabla: %r" % k
    return None


def _textos_de_la_pieza(tema, pieza, data):
    """Lo que el motor VA a dibujar en esa pieza, resuelto igual que en el render."""
    spec = generador.specs_de(tema).get(pieza)
    if not spec:
        return []
    out = []
    for f in generador._effective_texts(spec, data):
        try:
            out.append(generador._field_text(f, data))
        except Exception:
            pass
    return [t for t in out if isinstance(t, str) and t.strip()]


def test_el_kit_ENTERO_sale_en_ingles_en_las_12_tematicas():
    """La prueba que importa: pedirle el kit en inglés a cada temática y que no quede ni un
    texto en español. Se mira el texto resuelto, no el PNG: si algo no tiene traducción,
    `idioma.traducir` devuelve el original y acá salta con acento."""
    data = {"nombre": "Emma", "edad": "5", "anyo": "2026", "fecha": "May 3",
            "hora": "4 pm", "lugar": "Sunny Park", "direccion": "12 Oak St",
            "telefono": "555-0100", "idioma": "en"}
    datos = tuple(data[k] for k in ("nombre", "fecha", "hora", "lugar", "direccion",
                                    "telefono", "edad", "anyo"))
    quedaron = []
    for t in temas.list_temas():
        tid = t["id"] if isinstance(t, dict) else t
        for pieza in ("invitacion", "afiche", "banderin", "cajita_sorpresa",
                      "decoracion_sorbetes", "tarjetas_agradecimiento"):
            for txt in _textos_de_la_pieza(tid, pieza, data):
                motivo = _rastro_de_español(txt, datos)
                if motivo:
                    quedaron.append("%s :: %s = %r  (%s)" % (tid, pieza, txt, motivo))
    assert not quedaron, (
        "el kit en inglés todavía imprime texto en español:\n  " + "\n  ".join(quedaron))


def test_el_arte_con_español_QUEMADO_tiene_su_version_en_ingles():
    """Traducir el motor no alcanza cuando el español está en los PÍXELES.

    12 PNG de monstruos —topper, etiqueta de botella y cajita, edades 2 a 5— traen
    «¡FELIZ CUMPLE!», «TOPPER PARA TORTA» y «CAJITA SORPRESA» pintados encima. La versión
    en inglés vive al lado como `<archivo>.en.png` (la hace `herramientas/despintar.py`) y
    `productos._arte_del_idioma` la elige sola.

    Este test cuida las DOS mitades, y la segunda es la que importa: que pedir español
    siga trayendo el original. Los once kits en español están vendiendo en Mercado Libre;
    un `.en.png` que se colara en el kit español sería un kit que dice «HAPPY BIRTHDAY»."""
    exdir = os.path.join(RAIZ, "temas", "monstruos", "extras")
    faltan, colados = [], []
    for base in ("topper", "etiqueta_botella", "cajita_sorpresa"):
        for e in range(2, 6):
            orig = os.path.join(exdir, "%s_%d.png" % (base, e))
            if not os.path.exists(orig):
                continue
            en = orig[:-4] + ".en.png"
            if not os.path.exists(en):
                faltan.append(os.path.basename(en))
                continue
            assert productos._arte_del_idioma(orig, {"idioma": "en"}) == en, base
            if productos._arte_del_idioma(orig, {}) != orig:
                colados.append(base)
            if productos._arte_del_idioma(orig, {"idioma": "es"}) != orig:
                colados.append(base)
    assert not faltan, ("falta el arte en inglés (correr herramientas/despintar.py "
                        "--aplicar):\n  " + "\n  ".join(faltan))
    assert not colados, ("el arte en INGLÉS se estaría colando en el kit en español: %s"
                         % sorted(set(colados)))


def test_el_ROMPECABEZAS_tambien_sale_en_ingles():
    """El rompecabezas es el único producto que Etsy entrega SOLO, al instante: no lleva
    personalización, así que el ZIP se sube como archivo de la publicación y nadie lo mira
    antes de que llegue al comprador.

    Por eso su texto en español no lo caza nadie aguas abajo — se descubrió mirando la foto
    del producto, donde las hojas decían «ROMPECABEZAS 1 · 4 piezas» y «Pegá esta hoja sobre
    cartulina…» en una publicación en inglés.

    NO se compara la imagen en español contra la inglesa. Esa fue la primera versión y quedó
    VERDE al romper una de las cuatro traducciones: alcanzaba con que UNA frase cambiara para
    que las dos imágenes difirieran. «Algo cambió» no es «todo se tradujo».

    Acá se intercepta `ImageDraw.text` —por donde pasa cada palabra que el rompecabezas
    escribe— y se mira que ninguna quede en español."""
    from PIL import ImageDraw as _ID
    dibujados = []
    original = _ID.ImageDraw.text

    def espia(self, xy, text="", *a, **k):
        if isinstance(text, str) and text.strip():
            dibujados.append(text)
        return original(self, xy, text, *a, **k)

    _ID.ImageDraw.text = espia
    try:
        for nombre, fn, _ in list(productos.piezas_tipo("safari", "rompecabezas"))[:2]:
            pz.to_rgb(fn({"idioma": "en"}))
    finally:
        _ID.ImageDraw.text = original

    assert dibujados, "el rompecabezas no escribió nada: el espía no funcionó"
    quedaron = set()
    for t in dibujados:
        if t.strip() == "casatridimensional.com.ar":      # la marca no se traduce
            continue
        motivo = _rastro_de_español(t)
        if motivo:
            quedaron.add("%r  (%s)" % (t, motivo))
    assert not quedaron, ("el rompecabezas escribe español con idioma=en:\n  "
                          + "\n  ".join(sorted(quedaron)))


def test_sin_arte_en_ingles_se_usa_el_original():
    """Las otras once temáticas no tienen `.en.png` y no lo necesitan: su arte no lleva
    texto. Pedir inglés tiene que devolver el archivo de siempre, no reventar."""
    p = os.path.join(RAIZ, "temas", "safari", "extras", "topper_1.png")
    assert os.path.exists(p)
    assert productos._arte_del_idioma(p, {"idioma": "en"}) == p


def test_el_nombre_va_CENTRADO_en_el_recuadro_del_afiche():
    """El nombre del afiche tiene que quedar centrado en su recuadro, en TODAS las edades.

    SE MIDE SOBRE LA PIEZA DEL KIT, no sobre la vista previa, y esa distinción es el bug.
    El afiche se arma por DOS caminos distintos: la vista previa usa `generador.render()` y
    la `y` del layout; **el kit usa `productos._overlay_texto`, que ignora esa `y` y ubica
    el nombre donde `_zona_limpia_abajo` detecta el recuadro**. Yo arreglé el camino de la
    vista previa, medí ahí mismo, y di el problema por resuelto — mientras la pieza que
    recibe el comprador seguía mal. Lo cazó Pablo mirando la foto de la publicación.

    El detector devolvía None en las siete edades de safari (el interior del recuadro y el
    margen de abajo se fusionaban en una sola franja lisa, que el filtro descartaba por
    tocar el borde de la hoja), así que caía a un `y = 0.92` fijo: el nombre pegado al borde
    inferior del recuadro.

    Un test que mide el camino equivocado da la misma tranquilidad que uno que mide bien, y
    ninguna de las dos garantías."""
    import numpy as np
    m = {n: fn for n, fn, _ in productos.piezas_tipo("safari", "kit")}
    afiche = [k for k in m if k.endswith("_afiche")]
    assert afiche, "el kit no trae afiche"
    fn = m[afiche[0]]
    peor = []
    for edad in ("1", "3", "5", "7"):
        arte = os.path.join(RAIZ, "temas", "safari", "extras", "afiche_%s.png" % edad)
        if not os.path.exists(arte):
            continue
        from PIL import Image as _Im
        zona = productos._zona_limpia_abajo(_Im.open(arte))
        assert zona, "edad %s: no se detectó el recuadro del nombre" % edad
        cy, _alto = zona
        con = np.asarray(pz.to_rgb(fn({"nombre": "Emma", "edad": edad}))).astype(int)
        sin = np.asarray(pz.to_rgb(fn({"nombre": "", "edad": edad}))).astype(int)
        ys, _ = np.nonzero(np.abs(con - sin).max(axis=-1) > 18)
        assert len(ys), "edad %s: no se dibujó el nombre" % edad
        centro = (ys.min() + ys.max()) / 2 / con.shape[0]
        if abs(centro - cy) > 0.012:
            peor.append("edad %s: el nombre en %.4f y el centro del recuadro en %.4f"
                        % (edad, centro, cy))
    assert not peor, "el nombre no queda centrado en el recuadro:\n  " + "\n  ".join(peor)


PIEZAS_DEL_KIT = 16          # ver test_el_kit_tiene_las_piezas_que_promete_la_publicacion


def test_el_kit_tiene_las_piezas_que_promete_la_publicacion():
    """El número de piezas es una PROMESA: está en el título de las publicaciones de Etsy y
    de Mercado Libre, y en la foto principal.

    Hasta el 19-ago-2026 ningún test lo afirmaba: el kit pasó de 15 a 16 piezas y los 2128
    tests siguieron en verde, porque todos recorren las piezas que haya. O sea que una pieza
    podía desaparecer en silencio y el comprador recibir menos de lo que pagó, sin que nada
    lo dijera. Si este test falla, hay que decidir a propósito: o se repone la pieza, o se
    cambia el número acá Y en las publicaciones."""
    for tema in ("safari", "monstruos", "princesas"):
        n = len(list(productos.piezas_tipo(tema, "kit")))
        assert n == PIEZAS_DEL_KIT, (
            "%s entrega %d piezas y las publicaciones prometen %d" % (tema, n, PIEZAS_DEL_KIT))


def test_el_banderin_sin_letra_no_depende_del_nombre():
    """La hoja de banderines lisos existe para reimprimirla y alargar la guirnalda, así que
    tiene que salir IGUAL con cualquier nombre — si llevara el nombre no serviría para eso."""
    m = {n: fn for n, fn, _ in productos.piezas_tipo("safari", "kit")}
    lisa = [k for k in m if k.endswith("guirnalda_lisa")]
    assert lisa, "falta la hoja de banderines sin letra"
    a = pz.to_rgb(m[lisa[0]]({"nombre": "Emma", "edad": "5"})).tobytes()
    b = pz.to_rgb(m[lisa[0]]({"nombre": "Maximiliano", "edad": "3"})).tobytes()
    assert a == b, "la hoja de banderines lisos cambia con el nombre: no es lisa"


def test_las_piezas_se_generan_en_ingles_sin_caerse():
    """Traducir cambia el largo del texto, y el motor achica la fuente para que entre. Que
    ninguna pieza reviente por eso."""
    data = {"nombre": "Emma", "edad": "5", "anyo": "2026", "idioma": "en"}
    caidas = []
    for nombre, fn, _ in productos.piezas_tipo("safari", "kit"):
        try:
            pz.to_rgb(fn(data))
        except Exception as e:        # noqa: BLE001
            caidas.append("%s: %s" % (nombre, e))
    assert not caidas, "piezas que no se generan en inglés: %s" % caidas
