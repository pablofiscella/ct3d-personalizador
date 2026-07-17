"""Libro de cuento personalizado — cuento infantil imprimible, listo para vender.

El chico es EL PROTAGONISTA: la historia se arma con su nombre/edad y la ambientación
de la temática (mundo, amigos, desafío y tesoro salen de HISTORIAS, con fallback
genérico para temas nuevos). 10 páginas A4: portada · dedicatoria · 7 páginas de
historia · fin. Todo procedural (Pillow) — determinístico por tema+página, así el
mismo pedido genera siempre el mismo libro.

Ilustraciones: cada página deja la MITAD SUPERIOR como escena ilustrada. La base es
procedural (cielo, colinas, sol/estrellas + los personajes del tema recortados de los
stickers, si existen). Para versión "premium" se reemplaza cualquier página con arte
IA subiendo temas/<tema>/overrides/libro/<idx>.png — mismo override system que el
resto de los productos, cero cambio de código.

API: paginas_libro(data, tema) -> [PIL.Image] · pagina_libro(idx, data, tema) -> PIL.Image
"""
import contextlib
import os, json, glob, math, random, threading, re
from libro_historias import ARGUMENTOS_LARGO, CORTO_IDX, TITULOS
# Historias del libro-kit (movidas a libro_historias.py):
from libro_historias import (HISTORIAS, HISTORIA_DEFAULT, ARGUMENTOS,
                             ARGUMENTO_LABELS, ARGUMENTOS_EXT)
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
CREAM = (253, 250, 242)
INK = (60, 52, 62)
GOLD = (212, 175, 55)

PAGINAS_HISTORIA = 7          # legado: páginas de cuento de los temas existentes
PAGINAS_HISTORIA_NUEVO = 12   # temas nuevos (15 páginas en total)
PAGINAS_HISTORIA_LARGO = 17   # catálogo de audiolibros, 4 años o más (20 en total)
PAGINAS_HISTORIA_CORTA = 9    # catálogo de audiolibros, hasta 3 años (12 en total)
TOTAL_PAGINAS = PAGINAS_HISTORIA + 3   # legado — usado solo como valor por default


def _edad_int(edad):
    """Primer número que aparezca en la edad ('5', '3 años', 5) o None."""
    m = re.search(r"\d+", str(edad or ""))
    return int(m.group()) if m else None


def paginas_historia(tema, edad=None, historia=None, catalogo=False):
    """Páginas de historia. El CATÁLOGO de audiolibros (catalogo=True + una de las 8
    historias) usa largo por EDAD desacoplado del tema: 9 hasta 3 años, 17 de 4 en
    adelante. Cualquier otro caso (libro de kit, previews) mantiene el largo legado:
    7 en los temas ya vendidos, 12 en los nuevos. El flag catalogo lo prende SOLO el
    audiolibro, para no cambiarle el largo al libro de kit aunque comparta tema."""
    if catalogo and historia and historia in ARGUMENTOS_LARGO:
        e = _edad_int(edad)
        return PAGINAS_HISTORIA_CORTA if (e is not None and e <= 3) else PAGINAS_HISTORIA_LARGO
    try:
        d = json.load(open(os.path.join(TEMAS, tema, "tema.json")))
        n = d.get("libro_paginas_historia")
        if isinstance(n, int) and n > 0:
            return n
    except Exception:
        pass
    return PAGINAS_HISTORIA_NUEVO


def total_paginas(tema, edad=None, historia=None, catalogo=False):
    return paginas_historia(tema, edad, historia, catalogo) + 3

# ── ambientación por temática (fallback genérico para temas nuevos) ─────────
# REGLAS del diccionario (para que cualquier valor encaje en cualquier arco de
# libro_historias sin romper la gramática — ver skill armar-audiolibros):
#   mundo:    con artículo incluido ("la sabana...", "el gran circo..."). Los arcos
#             solo lo usan tras preposición (en/a/de/hacia/por/sobre) o como sujeto
#             sin adjetivos que concuerden — NUNCA "el {mundo}" ni "todo {mundo}".
#   amigos:   SIEMPRE masculino plural con "los ..." (los arcos usan adjetivos en
#             masculino plural: tristes, cabizbajos, preocupados).
#   desafio:  cláusula simple en pasado, minúscula inicial, SIN ":", "¡" ni "!"
#             (se inserta en «apareció un problema: {desafio}. Nadie sabía...»).
#   solucion: acción en pasado, 3ª persona singular, empieza con verbo (se inserta
#             en «{nombre} {solucion}» seguido de una consecuencia).
#   tesoro:   objeto con artículo ("una .../un ..."), neutro para nene o nena.


def _font(sz, bold=True):
    for p in glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True):
        try:
            f = ImageFont.truetype(p, sz)
            try: f.set_variation_by_axes([700 if bold else 500])
            except Exception: pass
            return f
        except Exception: pass
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)


def _accent(tema):
    try:
        d = json.load(open(os.path.join(TEMAS, tema, "tema.json")))
        h = ((d.get("kit") or {}).get("accent") or "#6B5BD2").lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except Exception:
        return (107, 91, 210)


def _tint(rgb, p):
    return tuple(int(c + (255 - c) * p) for c in rgb[:3])


def _personajes(tema, n=3):
    """Personajes del tema (recortes de la hoja de stickers), FILTRADOS: un recorte
    real (die-cut) siempre tiene transparencia alrededor; un componente ~100% opaco es
    la hoja entera con fondo blanco (pasa en temas cuyos stickers no traen alpha) y
    pegarla arruina la escena — se descarta."""
    try:
        import cuaderno
        mons = cuaderno.personajes_decorativos(tema, n)
    except Exception:
        return []
    out = []
    for m in mons:
        a = m.getchannel("A")
        op = sum(a.histogram()[129:]) / float(m.width * m.height)
        if op < 0.92:
            out.append(m)
    return out


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


def _wrap(dr, text, font, maxw):
    """Corta el texto en líneas que entran en maxw (por palabras)."""
    lines, cur = [], ""
    for w in str(text).split():
        t = (cur + " " + w).strip()
        if dr.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def _parrafo(dr, text, cx, y, font, color, maxw, lh=1.35, anchor="ma"):
    for ln in _wrap(dr, text, font, maxw):
        dr.text((cx, y), ln, font=font, fill=color, anchor=anchor)
        y += int(font.size * lh)
    return y


# ── argumentos: hilos narrativos distintos (mismo tema, otra historia) ────────
# Cada argumento define los 7 textos de la historia con la ambientación del tema
# ({mundo}/{amigos}/{tesoro} salen de HISTORIAS; {desafio}/{solucion} solo los usa
# el clásico). El cliente elige el argumento al comprar (campo "historia") — así
# la misma temática da libros DIFERENTES y se puede comprar más de uno.

# ── historia propia POR TEMA (regla de Pablo, 8-jul-2026) ────────────────────
# Los 11 temas con libro ya generado usan todos el clásico ("aventura") con su
# ambientación. Cada tema que estrena libro se casa con un argumento NUEVO de la
# reserva, en orden y sin repetir: el 12º tema usa la historia 12, etc. La
# asignación queda en tema.json («libro_historia») y desde ahí la usan el texto
# (cuento) y las ilustraciones (libro_ia) por igual.
_HISTORIAS_LEGADO = 11     # libros ya generados con el clásico (numeración de Pablo)
ORDEN_HISTORIAS_NUEVAS = ["tesoro", "rescate", "gran-dia", "noche-estrellas",
                          "cumple-sorpresa", "pequeno-maestro", "ayudar-a-todos"]


def historia_de_tema(tema):
    """Argumento asignado al tema en tema.json («libro_historia»), o None."""
    try:
        d = json.load(open(os.path.join(TEMAS, tema, "tema.json")))
        return str(d.get("libro_historia") or "").strip().lower() or None
    except Exception:
        return None


def historias_asignadas():
    """{tema: historia} de todos los temas que ya tienen argumento propio."""
    out = {}
    for p in glob.glob(os.path.join(TEMAS, "*", "tema.json")):
        try:
            h = str(json.load(open(p)).get("libro_historia") or "").strip().lower()
        except Exception:
            continue
        if h:
            out[os.path.basename(os.path.dirname(p))] = h
    return out


def numero_historia(historia):
    """Número 'humano' de la historia (los 11 libros clásicos van primero)."""
    if historia in ORDEN_HISTORIAS_NUEVAS:
        return _HISTORIAS_LEGADO + 1 + ORDEN_HISTORIAS_NUEVAS.index(historia)
    return None


def proxima_historia_libre():
    """El primer argumento de la reserva que ningún tema usa, o None (agotada)."""
    usadas = set(historias_asignadas().values())
    return next((h for h in ORDEN_HISTORIAS_NUEVAS if h not in usadas), None)


def asignar_historia_tema(tema):
    """Casa al tema con una historia nueva única y la persiste en tema.json.
    Idempotente (si ya tiene, devuelve la suya). Devuelve (slug, label, numero)
    o None si la reserva se agotó — en ese caso NO hay que repetir: se escriben
    argumentos nuevos (skill armar-kit)."""
    ya = historia_de_tema(tema)
    if ya:
        return ya, ARGUMENTO_LABELS.get(ya, ya), numero_historia(ya)
    libre = proxima_historia_libre()
    if libre is None:
        return None
    p = os.path.join(TEMAS, tema, "tema.json")
    d = json.load(open(p))
    d["libro_historia"] = libre
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    return libre, ARGUMENTO_LABELS.get(libre, libre), numero_historia(libre)

# Versión extendida (12 páginas) de las 4 narrativas clásicas: para los temas NUEVOS
# (15 páginas en total). Los primeros 6 textos son IDÉNTICOS a ARGUMENTOS (arriba) —
# no se toca el contenido ya vendido — se le suman 5 páginas de historia en el medio
# y el cierre (idéntico al original) pasa al final.


# El «¡»/«¿» solo capitaliza si ABRE oración (tras ./!/? o al inicio): en medio
# de la frase («..., ¡el mapa brilló!») el castellano sigue en minúscula — el
# regex viejo capitalizaba después de cualquier ¡ y quedaba «, ¡El mapa...»
_RE_INICIO_FRASE = re.compile(r'(^[¡¿]?\s*|[.!?]\s+[¡¿]?\s*|»\s+[¡¿]?\s*)([a-záéíóúüñ])')
# Contracción a+el→al, de+el→del: los placeholders {mundo} traen su artículo
# ("el gran circo", "el reino encantado..."), y muchos arrancan con "el" → tras
# "a"/"de" quedaba "a el reino"/"de el circo" (mal). Se contrae SOLO ante "el"
# minúscula (el artículo del placeholder); nunca "él" con tilde (pronombre).
_RE_CONTRAE = re.compile(r'\b([Aa]|[Dd]e)\s+el\b')


def _contraer(m):
    p = m.group(1)
    return ("al" if p.lower() == "a" else "del")[:1].upper() + \
           ("al" if p.lower() == "a" else "del")[1:] if p[0].isupper() else \
           ("al" if p.lower() == "a" else "del")


def _capitalizar_frases(texto):
    """Pone mayúscula al inicio del texto y después de cada punto/signo, contrae
    a+el→al y de+el→del (por el artículo de {mundo}), y cambia las comillas
    españolas «» por inglesas “” (las « se leen como '>>' y los padres las toman
    por un error). Necesario porque los placeholders como {amigos} (\"los
    animales...\") o {mundo} (\"el reino...\") caen tras preposición o al inicio
    de una oración."""
    t = _RE_CONTRAE.sub(_contraer, texto)
    t = _RE_INICIO_FRASE.sub(lambda m: m.group(1) + m.group(2).upper(), t)
    return t.replace("«", "“").replace("»", "”")


def cuento(data, tema="safari", catalogo=False):
    """Los textos de la historia, personalizados con nombre/edad + la ambientación
    del tema. Con catalogo=True (audiolibro) usa la versión rica del catálogo con
    largo por edad; si no, el largo legado (7/12). Testeable sin renderizar (el
    nombre TIENE que aparecer en el cuento)."""
    h = HISTORIAS.get(tema, HISTORIA_DEFAULT)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    edad = str(data.get("edad") or "").strip()
    conteo = ("contar hasta %s" % edad) if edad.isdigit() else "contar hasta tres"
    historia_raw = str(data.get("historia") or "").strip().lower()
    # sin historia en el pedido, vale la del TEMA (asignada al armar el libro) —
    # así cada tema nuevo cuenta SU historia, no el clásico repetido
    historia = historia_raw or historia_de_tema(tema) or "aventura"
    ctx = dict(h)
    ctx.update({"nombre": nombre, "conteo": conteo,
                "conteo_num": edad if edad.isdigit() else "tres"})
    # Catálogo de audiolibros: versión rica de 17 páginas, o su subconjunto de 9
    # para los más chiquitos (largo por edad). Solo si el audiolibro lo pide.
    arco_largo = ARGUMENTOS_LARGO.get(historia_raw) if catalogo else None
    if arco_largo is not None:
        n = paginas_historia(tema, edad, historia_raw, catalogo=True)
        arco = arco_largo if n >= PAGINAS_HISTORIA_LARGO else [arco_largo[i] for i in CORTO_IDX]
        return [_capitalizar_frases(t.format(**ctx)) for t in arco]
    # ----- legado: temas viejos / libro de kit (sin historia elegida) -----
    extendido = paginas_historia(tema) > PAGINAS_HISTORIA
    arco = (ARGUMENTOS_EXT if extendido else ARGUMENTOS).get(historia)
    if arco:
        return [_capitalizar_frases(t.format(**ctx)) for t in arco]
    base = [
        "Esta noche, antes de dormir, %s encontró una invitación brillante debajo "
        "de la almohada. Decía: «Te esperamos en %s»." % (nombre, h["mundo"]),
        "Al cerrar los ojos y %s, la habitación se llenó de luces de colores. "
        "¡El viaje había comenzado!" % conteo,
        "En %s, %s recibieron a %s con una gran fiesta de bienvenida."
        % (h["mundo"], h["amigos"], nombre),
        "Pero de pronto todo se detuvo: %s. Nadie sabía qué hacer... "
        "nadie, excepto %s." % (h["desafio"], nombre),
        "Con valentía y una gran sonrisa, %s %s. ¡Todos festejaron su ingenio!"
        % (nombre, h["solucion"]),
        "Como agradecimiento, %s le regalaron %s: un recuerdo para siempre."
        % (h["amigos"], h["tesoro"]),
    ]
    cierre = ("De vuelta en casa, %s se durmió con una sonrisa. Porque quien es "
              "valiente y ayuda a los demás, siempre tiene una nueva aventura "
              "esperando." % nombre)
    if not extendido:
        return [_capitalizar_frases(t) for t in base + [cierre]]
    return [_capitalizar_frases(t) for t in base + [
        "Para festejar, %s propusieron un juego gigante en %s, y todos se "
        "turnaron para inventar la payasada más divertida."
        % (h["amigos"], h["mundo"]),
        "De repente, una música suave los llevó hasta un rincón secreto de %s "
        "que %s nunca le habían mostrado a nadie." % (h["mundo"], h["amigos"]),
        "Ahí, %s descubrió algo mágico: un pequeño jardín de luces que solo se "
        "veía cuando todos estaban juntos y felices." % nombre,
        "%s prometió cuidar ese secreto junto con %s, y todos se abrazaron "
        "fuerte antes de despedirse por ese día." % (nombre, h["amigos"]),
        "El cielo se llenó de colores mientras %s y %s se decían adiós, "
        "sabiendo que el jardín de luces los esperaría en la próxima visita."
        % (nombre, h["amigos"]),
        cierre,
    ]]


# ── escena ilustrada (base procedural; se reemplaza por arte IA vía override) ─
def _cielo(im, box, top, bottom):
    """Degradé vertical simple dentro de box (resize de una columna de 1px)."""
    x0, y0, x1, y1 = box
    h = max(2, y1 - y0)
    col = Image.new("RGB", (1, h))
    for i in range(h):
        t = i / (h - 1)
        col.putpixel((0, i), tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    im.paste(col.resize((max(1, x1 - x0), h)), (x0, y0))


def _estrella(dr, cx, cy, r, color):
    pts = [(cx + (r if i % 2 == 0 else r * 0.45) * math.cos(-math.pi / 2 + i * math.pi / 5),
            cy + (r if i % 2 == 0 else r * 0.45) * math.sin(-math.pi / 2 + i * math.pi / 5))
           for i in range(10)]
    dr.polygon(pts, fill=color)


# ── motivos narrativos: cada página dibuja LO QUE CUENTA su texto ────────────
_COLS = [(224, 85, 107), (63, 167, 214), (232, 155, 44), (95, 184, 122),
         (139, 91, 210), (255, 214, 98)]


def _dash(dc, pts, color, width=7, dash=26):
    """Línea punteada siguiendo la polilínea pts (para caminos/senderos)."""
    import itertools
    total = 0
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        n = max(1, int(L // dash))
        for i in range(0, n, 2):
            t0, t1 = i / n, min(1, (i + 1) / n)
            dc.line([ax + (bx - ax) * t0, ay + (by - ay) * t0,
                     ax + (bx - ax) * t1, ay + (by - ay) * t1], fill=color, width=width)
        total += L


def _m_dormitorio(dc, W, H, acc, rnd):
    """Pág. 1: la cama y la invitación brillante debajo de la almohada."""
    bx0, bx1, by0, by1 = W * 0.24, W * 0.76, H * 0.50, H * 0.80
    dc.rounded_rectangle([bx0 - W * 0.05, by0 - H * 0.14, bx0 + W * 0.01, by1], 18,
                         fill=(139, 94, 60))                       # respaldo
    dc.rounded_rectangle([bx0, by0, bx1, by1], 24, fill=_tint(acc, 0.30))   # colchón/manta
    dc.rounded_rectangle([bx0, by0 + (by1 - by0) * 0.42, bx1, by1], 24, fill=acc)  # frazada
    dc.ellipse([bx0 + W * 0.02, by0 - H * 0.045, bx0 + W * 0.20, by0 + H * 0.055],
               fill=(255, 255, 255))                               # almohada
    # el sobre brillante (asomando sobre la almohada)
    sx0, sy0, sx1, sy1 = bx0 + W * 0.055, by0 - H * 0.145, bx0 + W * 0.165, by0 - H * 0.045
    dc.rounded_rectangle([sx0, sy0, sx1, sy1], 8, fill=(255, 248, 214), outline=GOLD, width=4)
    dc.line([sx0, sy0, (sx0 + sx1) / 2, (sy0 + sy1) / 2], fill=GOLD, width=4)
    dc.line([sx1, sy0, (sx0 + sx1) / 2, (sy0 + sy1) / 2], fill=GOLD, width=4)
    for dx, dy in ((-0.035, -0.03), (0.16, -0.05), (0.13, 0.02)):
        _estrella(dc, sx0 + W * dx, sy0 + H * dy, 14, GOLD)


def _m_luces(dc, W, H, acc, rnd):
    """Pág. 2: la habitación se llena de luces de colores (espiral mágica)."""
    cx, cy = W / 2, H * 0.46
    for i in range(30):
        ang = i * 0.55
        rad = W * 0.03 + i * W * 0.013
        r = 10 + (i % 4) * 4
        px, py = cx + rad * math.cos(ang), cy + rad * 0.72 * math.sin(ang)
        dc.ellipse([px - r, py - r, px + r, py + r], fill=_COLS[i % len(_COLS)])
    for _ in range(8):
        _estrella(dc, rnd.randint(40, W - 40), rnd.randint(30, H - 60),
                  rnd.randint(10, 18), (255, 250, 220))


def _m_fiesta(dc, W, H, acc, rnd):
    """Pág. 3 (y portada): fiesta de bienvenida — banderines, globos y torta."""
    # banderines colgados de una cuerda
    for lado in (0, 1):
        x0, y0 = (0, H * 0.03) if lado == 0 else (W * 0.52, H * 0.16)
        x1, y1 = (W * 0.48, H * 0.16) if lado == 0 else (W, H * 0.03)
        dc.line([x0, y0, x1, y1], fill=(120, 110, 130), width=4)
        for i in range(6):
            t = (i + 0.5) / 6
            px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            dc.polygon([(px - 22, py), (px + 22, py), (px, py + 44)],
                       fill=_COLS[(i + lado) % len(_COLS)])
    # globos
    for i, fx in enumerate((0.14, 0.26, 0.76, 0.88)):
        gx, gy = W * fx, H * (0.36 + (i % 2) * 0.08); r = W * 0.045
        dc.line([gx, gy + r * 1.2, gx, gy + r * 1.2 + H * 0.14], fill=(120, 110, 130), width=3)
        dc.ellipse([gx - r, gy - r * 1.2, gx + r, gy + r * 1.2], fill=_COLS[i % len(_COLS)])
    # torta
    tx, ty, tw, th = W * 0.5, H * 0.66, W * 0.115, H * 0.075
    dc.rounded_rectangle([tx - tw, ty, tx + tw, ty + th], 16, fill=_COLS[2])
    dc.rounded_rectangle([tx - tw * 0.72, ty - th * 0.8, tx + tw * 0.72, ty], 12, fill=_COLS[0])
    for k in range(3):
        vx = tx - tw * 0.45 + k * tw * 0.45
        dc.line([vx, ty - th * 0.8, vx, ty - th * 1.5], fill=(63, 167, 214), width=5)
        dc.ellipse([vx - 7, ty - th * 1.75, vx + 7, ty - th * 1.5], fill=(255, 214, 98))


def _m_problema(dc, W, H, acc, rnd):
    """Pág. 4: el problema — nube gris grande con un signo de pregunta."""
    cx, cy = W * 0.5, H * 0.26
    for dx, dy, r in ((0, 0, W * 0.13), (-W * 0.12, H * 0.03, W * 0.095),
                      (W * 0.12, H * 0.03, W * 0.095), (0, H * 0.055, W * 0.11)):
        dc.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(172, 172, 186))
    dc.text((cx, cy + H * 0.01), "?", font=_font(int(H * 0.17)), fill="white", anchor="mm")
    # caminos que se separan (¿por dónde ir?)
    _dash(dc, [(W * 0.5, H * 0.88), (W * 0.42, H * 0.70), (W * 0.20, H * 0.56)], (255, 255, 255), 7)
    _dash(dc, [(W * 0.5, H * 0.88), (W * 0.58, H * 0.70), (W * 0.80, H * 0.56)], (255, 255, 255), 7)


def _m_solucion(dc, W, H, acc, rnd):
    """Pág. 5: la solución — el árbol más alto con el sendero descubierto."""
    tx, tw = W * 0.66, W * 0.028
    dc.rounded_rectangle([tx - tw, H * 0.36, tx + tw, H * 0.80], 10, fill=(139, 94, 60))
    for dx, dy, r in ((0, -0.06, 0.105), (-0.085, 0.0, 0.085), (0.085, 0.0, 0.085),
                      (0, 0.065, 0.09)):
        dc.ellipse([tx + W * dx - W * r, H * 0.30 + H * dy - W * r,
                    tx + W * dx + W * r, H * 0.30 + H * dy + W * r], fill=(95, 184, 122))
    _estrella(dc, tx, H * 0.145, 26, GOLD)      # la meta, bien arriba
    _dash(dc, [(W * 0.10, H * 0.86), (W * 0.30, H * 0.78), (W * 0.48, H * 0.82),
               (tx, H * 0.80)], (255, 255, 255), 7)


def _m_tesoro(dc, W, H, acc, rnd):
    """Pág. 6: el regalo/tesoro de agradecimiento."""
    gx0, gx1, gy0, gy1 = W * 0.40, W * 0.60, H * 0.42, H * 0.68
    dc.rounded_rectangle([gx0, gy0, gx1, gy1], 14, fill=acc)
    dc.rounded_rectangle([gx0 - W * 0.02, gy0 - H * 0.07, gx1 + W * 0.02, gy0], 10,
                         fill=_tint(acc, 0.25))
    dc.rectangle([(gx0 + gx1) / 2 - W * 0.018, gy0 - H * 0.07, (gx0 + gx1) / 2 + W * 0.018, gy1],
                 fill=(255, 250, 220))
    for s in (-1, 1):   # moño
        dc.ellipse([(gx0 + gx1) / 2 + (s * W * 0.055) - W * 0.045, gy0 - H * 0.135,
                    (gx0 + gx1) / 2 + (s * W * 0.055) + W * 0.045, gy0 - H * 0.065],
                   outline=(255, 250, 220), width=8)
    for fx, fy in ((0.30, 0.36), (0.70, 0.34), (0.26, 0.62), (0.74, 0.62), (0.5, 0.28)):
        _estrella(dc, W * fx, H * fy, 16, GOLD)


def _m_casa(dc, W, H, acc, rnd):
    """Pág. 7: de vuelta en casa, a dormir (casita de noche, ventana encendida)."""
    hx0, hx1, hy0, hy1 = W * 0.36, W * 0.64, H * 0.42, H * 0.76
    dc.polygon([(hx0 - W * 0.04, hy0), (hx1 + W * 0.04, hy0), ((hx0 + hx1) / 2, H * 0.24)],
               fill=acc)                                            # techo
    dc.rectangle([hx0, hy0, hx1, hy1], fill=(246, 240, 228))        # cuerpo
    dc.rounded_rectangle([hx0 + W * 0.035, hy0 + H * 0.13, hx0 + W * 0.10, hy1], 8,
                         fill=(139, 94, 60))                        # puerta
    vx0, vy0 = hx1 - W * 0.115, hy0 + H * 0.055                     # ventana encendida
    dc.rounded_rectangle([vx0, vy0, vx0 + W * 0.08, vy0 + H * 0.09], 6,
                         fill=(255, 224, 120), outline=(139, 94, 60), width=4)
    dc.line([vx0 + W * 0.04, vy0, vx0 + W * 0.04, vy0 + H * 0.09], fill=(139, 94, 60), width=3)
    dc.line([vx0, vy0 + H * 0.045, vx0 + W * 0.08, vy0 + H * 0.045], fill=(139, 94, 60), width=3)
    for i, (dx, dy) in enumerate(((0.03, -0.05), (0.065, -0.10), (0.10, -0.15))):
        dc.text((hx1 + W * dx, vy0 + H * dy), "z", font=_font(30 + i * 12),
                fill=(255, 250, 220), anchor="mm")


_MOTIVOS = [_m_dormitorio, _m_luces, _m_fiesta, _m_problema, _m_solucion, _m_tesoro, _m_casa]
_NOCTURNOS = (_m_dormitorio, _m_casa)
_INTERIORES = (_m_dormitorio, _m_luces)   # sin colinas (pasan adentro / en la magia)


def _escena(im, dr, box, tema, pagina, acc, motivo=None, idx_pieza=None):
    """Ilustración de una página que REPRESENTA lo que cuenta el texto. Si hay
    ilustración override para idx_pieza (subida por el dash o generada con IA),
    va esa. Si no, la escena procedural: cada página de historia tiene su motivo
    (_MOTIVOS[n]): cama+invitación → luces mágicas → fiesta → problema (nube con ?)
    → solución (árbol y sendero) → tesoro → casita de noche. Encima van los
    personajes del tema. Determinística (misma página -> misma escena). Se pinta en
    una capa aparte y se pega con máscara redondeada, así nada se desborda del panel."""
    if idx_pieza is not None and _panel_ilustracion(im, dr, box, tema, idx_pieza, acc):
        return
    x0, y0, x1, y1 = box
    W = x1 - x0; H = y1 - y0
    rnd = random.Random("%s-%d" % (tema, pagina))
    if motivo is None:
        motivo = _MOTIVOS[pagina] if 0 <= pagina < len(_MOTIVOS) else _m_fiesta
    noche = motivo in _NOCTURNOS
    magico = motivo is _m_luces
    capa = Image.new("RGBA", (W, H))
    dc = ImageDraw.Draw(capa)
    if noche:
        _cielo(capa, (0, 0, W, H), (44, 42, 92), (108, 100, 168))
    elif magico:
        _cielo(capa, (0, 0, W, H), (66, 52, 120), (140, 120, 200))
    else:
        _cielo(capa, (0, 0, W, H), _tint(acc, 0.55), _tint(acc, 0.88))
    # colinas / piso
    if motivo not in _INTERIORES:
        for k, p in enumerate((0.35, 0.18)):
            hy = H - int(H * (0.30 - k * 0.13))
            col = _tint(acc, p) if not noche else _tint((44, 42, 92), 0.25 + k * 0.2)
            dc.ellipse([-W * 0.3 + k * W * 0.5, hy, W * 0.9 + k * W * 0.5, H + H * 0.5], fill=col)
    elif motivo is _m_dormitorio:
        dc.rectangle([0, H * 0.78, W, H], fill=_tint(acc, 0.20))    # piso del cuarto
    if noche:
        dc.ellipse([W * 0.76, H * 0.06, W * 0.88, H * 0.06 + W * 0.12], fill=(250, 245, 210))
        for _ in range(12):
            _estrella(dc, rnd.randint(30, W - 30), rnd.randint(20, int(H * 0.4)),
                      rnd.randint(8, 15), (255, 250, 220))
    elif not magico:
        # sol con rayos + nubes
        scx, scy, sr = W * 0.13, H * 0.06 + W * 0.06, W * 0.06
        for i in range(12):
            a = i * math.pi / 6
            dc.line([scx + sr * 1.15 * math.cos(a), scy + sr * 1.15 * math.sin(a),
                     scx + sr * 1.5 * math.cos(a), scy + sr * 1.5 * math.sin(a)],
                    fill=(255, 214, 98), width=9)
        dc.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=(255, 214, 98))
        for _ in range(2):
            nx = rnd.randint(int(W * 0.30), int(W * 0.85)); ny = rnd.randint(40, int(H * 0.22))
            for dx, dy, r in ((0, 0, 40), (-36, 10, 30), (38, 12, 30)):
                dc.ellipse([nx + dx - r, ny + dy - r, nx + dx + r, ny + dy + r],
                           fill=(255, 255, 255))
    # el motivo narrativo de la página
    motivo(dc, W, H, acc, rnd)
    # personajes del tema acompañando (salvo en el dormitorio, que es "antes del viaje")
    mons = _personajes(tema, 4) if motivo is not _m_dormitorio else []
    if mons:
        posiciones = [(0.22, 0.78, 0.34), (0.82, 0.76, 0.30), (0.5, 0.84, 0.24)]
        rnd.shuffle(mons)
        for (fx, fy, fh), m in zip(posiciones[:1 + pagina % 3], mons):
            _paste_h(capa, m, W * fx, H * fy, H * fh)
    # pegar con máscara redondeada (recorta lo que sobresale) + marco
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], 36, fill=255)
    im.paste(capa, (x0, y0), mask)
    dr.rounded_rectangle(box, 36, outline=_tint(acc, 0.25), width=6)


# ── ilustraciones subidas / generadas con IA (override POR ESCENA) ───────────
# ── arte por VENTA (libro premium) ───────────────────────────────────────────
# El libro premium ilustra cada pedido con arte único (libro_ia con dest_dir).
# usar_escenas_dir() redirige _panel_ilustracion a ese directorio mientras se
# renderizan las páginas del pedido. Thread-local: la generación premium corre en
# su propio hilo (servicio._api_generar) y no pisa los renders concurrentes del
# dash ni de otros pedidos.
_ESCENAS_LOCAL = threading.local()


@contextlib.contextmanager
def usar_escenas_dir(path):
    """Dentro del with, las ilustraciones salen de <path>/<idx>.png (si existen)
    en vez de los overrides del tema. Para el libro premium (arte por pedido)."""
    prev = getattr(_ESCENAS_LOCAL, "dir", None)
    _ESCENAS_LOCAL.dir = path
    try:
        yield
    finally:
        _ESCENAS_LOCAL.dir = prev


@contextlib.contextmanager
def usar_genero(genero):
    """Dentro del with, el arte de las escenas prefiere la variante por género
    (<idx>_nena.png / <idx>_nene.png) si existe — para que 'Valentina' no aparezca
    con un nene dibujado en las páginas donde está el protagonista."""
    prev = getattr(_ESCENAS_LOCAL, "genero", None)
    g = (genero or "").strip().lower()
    _ESCENAS_LOCAL.genero = "nena" if g in ("nena", "niña", "nina", "f") else \
                            ("nene" if g in ("nene", "niño", "nino", "varon", "varón", "m") else None)
    try:
        yield
    finally:
        _ESCENAS_LOCAL.genero = prev


def _escena_efectiva_path(tema, idx):
    """Path del arte de la página idx: primero el del pedido premium (si este hilo
    está dentro de usar_escenas_dir), después el override del tema."""
    d = getattr(_ESCENAS_LOCAL, "dir", None)
    if d:
        p = os.path.join(d, "%d.png" % int(idx))
        if os.path.isfile(p):
            return p
    g = getattr(_ESCENAS_LOCAL, "genero", None)
    if g:
        base = override_escena_path(tema, idx)
        pg = base.replace(".png", "_%s.png" % g)
        if os.path.isfile(pg):
            return pg
    return override_escena_path(tema, idx)


def override_escena_path(tema, idx):
    """La ILUSTRACIÓN de la página idx (0..9): temas/<tema>/overrides/libro/<idx>.png.
    A diferencia del resto de los productos, en el libro el override NO reemplaza la
    página completa: es solo el ARTE de la escena, y el motor sigue escribiendo el
    texto personalizado encima (si tapara la página entera, el nombre del chico
    quedaría fijo dentro de la imagen). Por eso productos.piezas_tipo saltea el
    override genérico para el tipo 'libro'. La imagen llega acá de dos maneras:
    subida a mano por el dash (botón 📤 de la pieza) o generada con IA (libro_ia.py)."""
    import temas as _temas
    return os.path.join(_temas.TEMAS_DIR, tema or "safari", "overrides", "libro",
                        "%d.png" % int(idx))


def _cover(img, W, H, anchor_y=0.5):
    """Escala y recorta la imagen para CUBRIR WxH (estilo object-fit: cover).
    anchor_y: qué parte conservar si sobra alto (0=arriba, 1=abajo). Las
    ilustraciones ancladas abajo (0.78) sacrifican cielo, nunca personajes:
    en los cuentos los personajes pisan el piso — un recorte centrado les
    cortaba la cara (safari pág 4) y ni el QA de visión lo detectaba."""
    s = max(W / img.width, H / img.height)
    im2 = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)
    x = (im2.width - W) // 2
    y = int((im2.height - H) * anchor_y)
    return im2.crop((x, y, x + W, y + H))


def _panel_ilustracion(im, dr, box, tema, idx, acc):
    """Si hay ilustración override para la página idx, la pega en el panel (cover +
    máscara redondeada + marco) y devuelve True. Si no hay, False (escena procedural)."""
    p = _escena_efectiva_path(tema, idx)
    if not os.path.isfile(p):
        return False
    x0, y0, x1, y1 = box
    W, H = x1 - x0, y1 - y0
    art = _cover(Image.open(p).convert("RGBA"), W, H, anchor_y=0.78)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], 36, fill=255)
    im.paste(art, (x0, y0), mask)
    dr.rounded_rectangle(box, 36, outline=_tint(acc, 0.25), width=6)
    return True


def _pie(dr, acc, y=Hp - 52):
    dr.text((Wp / 2, y), "casatridimensional.com.ar",
            font=_font(20, False), fill=_tint(acc, 0.35), anchor="mm")


def _fit_fs(nombre, fs, maxw):
    while _font(fs).getlength(nombre) > maxw and fs > 40:
        fs -= 4
    return fs


# ── páginas ──────────────────────────────────────────────────────────────────
def portada(data, tema="safari", sin_pie=False):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    edad = str(data.get("edad") or "").strip()
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    _cielo(im, (0, 0, Wp, Hp), _tint(acc, 0.80), _tint(acc, 0.95))
    dr.rounded_rectangle([55, 55, Wp - 55, Hp - 55], 40, outline=acc, width=8)
    dr.rounded_rectangle([80, 80, Wp - 80, Hp - 80], 30, outline=_tint(acc, 0.55), width=3)
    # Tapa con el título de la HISTORIA elegida (cada libro con su título);
    # sin historia del catálogo (libro de kit legado) queda el texto clásico.
    titulo_h = TITULOS.get(str(data.get("historia") or "").strip().lower())
    dr.text((Wp / 2, 330), "El cuento de" if titulo_h else "La gran aventura de",
            font=_font(66, False), fill=INK, anchor="mm")
    fs = _fit_fs(nombre, 170, Wp - 320)
    dr.text((Wp / 2, 480), nombre, font=_font(fs), fill=acc, anchor="mm")
    if titulo_h and data.get("generico"):
        etiqueta = "“%s”" % titulo_h          # libro genérico: sin edad en la tapa
    elif titulo_h:
        etiqueta = ("“%s” · %s años" % (titulo_h, edad)) if edad else "“%s”" % titulo_h
    else:
        etiqueta = ("Un cuento personalizado · %s años" % edad) if edad \
            else "Un cuento personalizado"
    ew = max(520, _font(36).getlength(etiqueta) + 90)
    dr.rounded_rectangle([Wp / 2 - ew / 2, 585, Wp / 2 + ew / 2, 665], 40, fill=acc)
    dr.text((Wp / 2, 625), etiqueta, font=_font(36), fill="white", anchor="mm")
    _escena(im, dr, (140, 760, Wp - 140, Hp - 260), tema, -1, acc, motivo=_m_fiesta,
            idx_pieza=0)
    _estrella(dr, Wp / 2, Hp - 165, 34, GOLD)
    # la portada tiene marco doble hasta Hp-55 (las demás páginas no) — el pie
    # sube para no quedar tapado por esa línea
    if not sin_pie:
        _pie(dr, acc, y=Hp - 100)
    return im


def dedicatoria(data, tema="safari", sin_pie=False):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    dedic = (str(data.get("dedicatoria") or "").strip()) or \
        "Que nunca dejes de soñar, de jugar y de creer en vos."
    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([90, 90, Wp - 90, Hp - 90], 40, outline=_tint(acc, 0.4), width=4)
    dr.text((Wp / 2, 420), "Este cuento pertenece a", font=_font(44, False), fill=INK, anchor="mm")
    if data.get("generico"):
        # libro genérico imprimible: línea en blanco para escribir el nombre a mano
        dr.line([Wp * 0.25, 580, Wp * 0.75, 580], fill=_tint(acc, 0.55), width=4)
    else:
        fs = _fit_fs(nombre, 120, Wp - 360)
        dr.text((Wp / 2, 560), nombre, font=_font(fs), fill=acc, anchor="mm")
    dr.line([Wp * 0.28, 650, Wp * 0.72, 650], fill=_tint(acc, 0.45), width=3)
    _estrella(dr, Wp * 0.24, 650, 18, GOLD); _estrella(dr, Wp * 0.76, 650, 18, GOLD)
    _parrafo(dr, "“" + dedic + "”", Wp / 2, 800, _font(40, False), INK, Wp - 420)
    if not _panel_ilustracion(im, dr, (270, 1010, Wp - 270, Hp - 220), tema, 1, acc):
        mons = _personajes(tema, 1)
        if mons:
            _paste_h(im, mons[0], Wp / 2, Hp - 460, 320)
    if not sin_pie:
        _pie(dr, acc)
    return im


def pagina_historia(n, data, tema="safari", catalogo=False, sin_pie=False):
    """Página n del cuento: escena ilustrada arriba + texto abajo + número."""
    acc = _accent(tema)
    textos = cuento(data, tema, catalogo)
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    _escena(im, dr, (90, 90, Wp - 90, int(Hp * 0.60)), tema, n, acc, idx_pieza=n + 2)
    # banda de texto
    dr.rounded_rectangle([90, int(Hp * 0.63), Wp - 90, Hp - 150], 36, fill=CREAM + (255,),
                         outline=_tint(acc, 0.5), width=3)
    _parrafo(dr, textos[n], Wp / 2, int(Hp * 0.63) + 90, _font(42, False), INK, Wp - 340, lh=1.45)
    # número de página (portada y dedicatoria no cuentan)
    dr.ellipse([Wp / 2 - 44, Hp - 190, Wp / 2 + 44, Hp - 102], fill=acc)
    dr.text((Wp / 2, Hp - 146), str(n + 1), font=_font(44), fill="white", anchor="mm")
    if not sin_pie:
        _pie(dr, acc)
    return im


def fin(data, tema="safari", catalogo=False, sin_pie=False):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    ov = _escena_efectiva_path(tema, total_paginas(tema, data.get("edad"), data.get("historia"), catalogo) - 1)
    if os.path.isfile(ov):
        # ilustración a página completa + banda oscura translúcida para que el
        # FIN y el mensaje se lean sobre cualquier arte
        im.paste(_cover(Image.open(ov).convert("RGBA"), Wp, Hp), (0, 0))
        velo = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
        ImageDraw.Draw(velo).rounded_rectangle(
            [Wp * 0.12, Hp * 0.22, Wp * 0.88, Hp * 0.60], 46, fill=(44, 42, 92, 170))
        im.alpha_composite(velo)
    else:
        _cielo(im, (0, 0, Wp, Hp), (44, 42, 92), (108, 100, 168))
        rnd = random.Random(tema + "-fin")
        puestas = 0
        while puestas < 26:
            sx, sy = rnd.randint(120, Wp - 120), rnd.randint(120, Hp - 320)
            if Hp * 0.24 < sy < Hp * 0.58 and Wp * 0.14 < sx < Wp * 0.86:
                continue    # no pisar el FIN ni el mensaje
            _estrella(dr, sx, sy, rnd.randint(8, 20), (255, 250, 220))
            puestas += 1
        mons = _personajes(tema, 3)
        for fx, m in zip((0.28, 0.5, 0.72), mons):
            _paste_h(im, m, Wp * fx, Hp - 420, 260)
    dr.rounded_rectangle([70, 70, Wp - 70, Hp - 70], 40, outline=_tint(acc, 0.6), width=6)
    dr.text((Wp / 2, Hp * 0.34), "FIN", font=_font(220), fill=(255, 250, 220), anchor="mm")
    _parrafo(dr, "Y colorín colorado, la aventura de %s apenas ha comenzado." % nombre,
             Wp / 2, int(Hp * 0.48), _font(44, False), (238, 234, 255), Wp - 360, lh=1.45)
    dr.text((Wp / 2, Hp - 130), "Un cuento hecho especialmente para vos",
            font=_font(30, False), fill=(210, 204, 240), anchor="mm")
    if not sin_pie:
        _pie(dr, acc)
    return im


def pagina_libro(idx, data, tema="safari", catalogo=False, sin_pie=False):
    """Página idx del libro: 0=portada, 1=dedicatoria, 2..N=historia, última=fin.
    sin_pie=True omite el "casatridimensional.com.ar" al pie de la página — para
    fotos de catálogo externo (ej. Mercado Libre) donde una URL en la imagen
    viola las políticas de la plataforma (bug real, publicaciones de audiolibro
    dadas de baja/en revisión desde el 10-jul-2026 por esto). El PDF del
    producto imprimible sigue usando el pie normal (sin_pie=False, default)."""
    if idx == 0:
        return portada(data, tema, sin_pie=sin_pie)
    if idx == 1:
        return dedicatoria(data, tema, sin_pie=sin_pie)
    if idx == total_paginas(tema, data.get("edad"), data.get("historia"), catalogo) - 1:
        return fin(data, tema, catalogo, sin_pie=sin_pie)
    return pagina_historia(idx - 2, data, tema, catalogo, sin_pie=sin_pie)


def paginas_libro(data, tema="safari", catalogo=False):
    n = total_paginas(tema, data.get("edad"), data.get("historia"), catalogo)
    return [pagina_libro(i, data, tema, catalogo) for i in range(n)]


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Valentina"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/libro"
    os.makedirs(out, exist_ok=True)
    for i, pg in enumerate(paginas_libro({"nombre": nombre, "edad": "4",
                                          "dedicatoria": "Para la aventurera de la casa."}, tema)):
        pg.convert("RGB").save(os.path.join(out, "%02d.png" % i))
    print("OK ->", out)
