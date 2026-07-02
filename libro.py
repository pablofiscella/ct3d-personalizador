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
import os, json, glob, math, random
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
CREAM = (253, 250, 242)
INK = (60, 52, 62)
GOLD = (212, 175, 55)

PAGINAS_HISTORIA = 7          # páginas de cuento (además de portada, dedicatoria y fin)
TOTAL_PAGINAS = PAGINAS_HISTORIA + 3

# ── ambientación por temática (fallback genérico para temas nuevos) ─────────
HISTORIAS = {
    "safari": {
        "mundo": "la sabana dorada del safari",
        "amigos": "los animales de la selva",
        "desafio": "el pequeño león no encontraba el camino a su casa",
        "solucion": "trepó al árbol más alto y descubrió el sendero escondido",
        "tesoro": "una brújula dorada de exploración",
    },
    "circo": {
        "mundo": "el gran circo de colores",
        "amigos": "los artistas del circo",
        "desafio": "la función no podía empezar: ¡el mago había perdido su sombrero!",
        "solucion": "siguió las huellas de purpurina y encontró el sombrero detrás de la carpa",
        "tesoro": "una entrada mágica para volver al circo cuando quiera",
    },
    "superheroes": {
        "mundo": "la ciudad de los superhéroes",
        "amigos": "los superhéroes de la ciudad",
        "desafio": "un viento travieso se había llevado todas las capas",
        "solucion": "descubrió las capas en la torre más alta y las rescató una por una",
        "tesoro": "una capa brillante hecha a su medida",
    },
    "construccion": {
        "mundo": "la gran obra en construcción",
        "amigos": "las máquinas de la obra",
        "desafio": "al puente le faltaba la última pieza y nadie la encontraba",
        "solucion": "encontró la pieza perdida y guió a la grúa para colocarla",
        "tesoro": "un casco dorado de constructor",
    },
    "bomberos": {
        "mundo": "la estación de bomberos",
        "amigos": "los bomberos valientes",
        "desafio": "un gatito había quedado atrapado en lo alto de un árbol",
        "solucion": "subió por la escalera del camión y lo rescató con mucho cuidado",
        "tesoro": "una medalla de bombero honorario",
    },
    "aviadores": {
        "mundo": "el cielo de los aviadores",
        "amigos": "los pilotos y sus aviones",
        "desafio": "una nube gigante tapaba el camino de vuelta al aeropuerto",
        "solucion": "guió a todos los aviones con la brújula del avión más pequeño",
        "tesoro": "unas alas doradas de piloto",
    },
    "campamento": {
        "mundo": "el bosque del campamento",
        "amigos": "los amigos del campamento",
        "desafio": "la fogata se apagó justo antes de contar historias",
        "solucion": "juntó las ramitas más secas y la fogata volvió a brillar",
        "tesoro": "una linterna que guarda luz de estrellas",
    },
    "artistas": {
        "mundo": "el taller de los artistas",
        "amigos": "los pinceles y los colores",
        "desafio": "todos los colores se habían mezclado y el mundo quedó gris",
        "solucion": "pintó un arcoíris enorme que devolvió los colores al mundo",
        "tesoro": "un pincel mágico que nunca se queda sin color",
    },
    "monstruos": {
        "mundo": "el país de los monstruos divertidos",
        "amigos": "los monstruos más simpáticos",
        "desafio": "el monstruo más chiquito tenía miedo de la oscuridad",
        "solucion": "le enseñó que en la oscuridad también viven las estrellas",
        "tesoro": "un frasquito con luciérnagas de luz",
    },
    "un-espacio-de-locura": {
        "mundo": "el espacio infinito",
        "amigos": "los astronautas y las estrellas",
        "desafio": "un cometa travieso había escondido la luna",
        "solucion": "persiguió al cometa en su nave y trajo la luna de vuelta",
        "tesoro": "una estrella que brilla de verdad",
    },
}
HISTORIAS["superhéroes"] = HISTORIAS["superheroes"]
HISTORIA_DEFAULT = {
    "mundo": "un mundo mágico",
    "amigos": "sus nuevos amigos",
    "desafio": "el camino de regreso había desaparecido",
    "solucion": "siguió las estrellas más brillantes y encontró el sendero",
    "tesoro": "una estrella de la suerte",
}


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


# ── cuento ───────────────────────────────────────────────────────────────────
def cuento(data, tema="safari"):
    """Los 7 textos de la historia, personalizados con nombre/edad + la ambientación
    del tema. Testeable sin renderizar (el nombre TIENE que aparecer en el cuento)."""
    h = HISTORIAS.get(tema, HISTORIA_DEFAULT)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    edad = str(data.get("edad") or "").strip()
    conteo = ("contar hasta %s" % edad) if edad.isdigit() else "contar hasta tres"
    return [
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
        "De vuelta en casa, %s se durmió con una sonrisa. Porque quien es valiente "
        "y ayuda a los demás, siempre tiene una nueva aventura esperando." % nombre,
    ]


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


def _escena(im, dr, box, tema, pagina, acc, motivo=None):
    """Ilustración procedural de una página que REPRESENTA lo que cuenta el texto:
    cada página de historia tiene su motivo (_MOTIVOS[n]): cama+invitación → luces
    mágicas → fiesta → problema (nube con ?) → solución (árbol y sendero) → tesoro →
    casita de noche. Encima van los personajes del tema. Determinística (misma
    página -> misma escena). Se pinta en una capa aparte y se pega con máscara
    redondeada, así nada (colinas, personajes) se desborda del panel."""
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


def _pie(dr, acc):
    dr.text((Wp / 2, Hp - 52), "casatridimensional.com.ar",
            font=_font(20, False), fill=_tint(acc, 0.35), anchor="mm")


def _fit_fs(nombre, fs, maxw):
    while _font(fs).getlength(nombre) > maxw and fs > 40:
        fs -= 4
    return fs


# ── páginas ──────────────────────────────────────────────────────────────────
def portada(data, tema="safari"):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    edad = str(data.get("edad") or "").strip()
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    _cielo(im, (0, 0, Wp, Hp), _tint(acc, 0.80), _tint(acc, 0.95))
    dr.rounded_rectangle([55, 55, Wp - 55, Hp - 55], 40, outline=acc, width=8)
    dr.rounded_rectangle([80, 80, Wp - 80, Hp - 80], 30, outline=_tint(acc, 0.55), width=3)
    dr.text((Wp / 2, 330), "La gran aventura de", font=_font(66, False), fill=INK, anchor="mm")
    fs = _fit_fs(nombre, 170, Wp - 320)
    dr.text((Wp / 2, 480), nombre, font=_font(fs), fill=acc, anchor="mm")
    etiqueta = ("Un cuento personalizado · %s años" % edad) if edad else "Un cuento personalizado"
    ew = max(520, _font(36).getlength(etiqueta) + 90)
    dr.rounded_rectangle([Wp / 2 - ew / 2, 585, Wp / 2 + ew / 2, 665], 40, fill=acc)
    dr.text((Wp / 2, 625), etiqueta, font=_font(36), fill="white", anchor="mm")
    _escena(im, dr, (140, 760, Wp - 140, Hp - 260), tema, -1, acc, motivo=_m_fiesta)
    _estrella(dr, Wp / 2, Hp - 165, 34, GOLD)
    _pie(dr, acc)
    return im


def dedicatoria(data, tema="safari"):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    dedic = (str(data.get("dedicatoria") or "").strip()) or \
        "Que nunca dejes de soñar, de jugar y de creer en vos."
    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([90, 90, Wp - 90, Hp - 90], 40, outline=_tint(acc, 0.4), width=4)
    dr.text((Wp / 2, 420), "Este cuento pertenece a", font=_font(44, False), fill=INK, anchor="mm")
    fs = _fit_fs(nombre, 120, Wp - 360)
    dr.text((Wp / 2, 560), nombre, font=_font(fs), fill=acc, anchor="mm")
    dr.line([Wp * 0.28, 650, Wp * 0.72, 650], fill=_tint(acc, 0.45), width=3)
    _estrella(dr, Wp * 0.24, 650, 18, GOLD); _estrella(dr, Wp * 0.76, 650, 18, GOLD)
    _parrafo(dr, "“" + dedic + "”", Wp / 2, 800, _font(40, False), INK, Wp - 420)
    mons = _personajes(tema, 1)
    if mons:
        _paste_h(im, mons[0], Wp / 2, Hp - 460, 320)
    _pie(dr, acc)
    return im


def pagina_historia(n, data, tema="safari"):
    """Página n (0..6) del cuento: escena ilustrada arriba + texto abajo + número."""
    acc = _accent(tema)
    textos = cuento(data, tema)
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    _escena(im, dr, (90, 90, Wp - 90, int(Hp * 0.60)), tema, n, acc)
    # banda de texto
    dr.rounded_rectangle([90, int(Hp * 0.63), Wp - 90, Hp - 150], 36, fill=CREAM + (255,),
                         outline=_tint(acc, 0.5), width=3)
    _parrafo(dr, textos[n], Wp / 2, int(Hp * 0.63) + 90, _font(42, False), INK, Wp - 340, lh=1.45)
    # número de página (portada y dedicatoria no cuentan)
    dr.ellipse([Wp / 2 - 44, Hp - 190, Wp / 2 + 44, Hp - 102], fill=acc)
    dr.text((Wp / 2, Hp - 146), str(n + 1), font=_font(44), fill="white", anchor="mm")
    _pie(dr, acc)
    return im


def fin(data, tema="safari"):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    _cielo(im, (0, 0, Wp, Hp), (44, 42, 92), (108, 100, 168))
    dr.rounded_rectangle([70, 70, Wp - 70, Hp - 70], 40, outline=_tint(acc, 0.6), width=6)
    rnd = random.Random(tema + "-fin")
    puestas = 0
    while puestas < 26:
        sx, sy = rnd.randint(120, Wp - 120), rnd.randint(120, Hp - 320)
        if Hp * 0.24 < sy < Hp * 0.58 and Wp * 0.14 < sx < Wp * 0.86:
            continue    # no pisar el FIN ni el mensaje
        _estrella(dr, sx, sy, rnd.randint(8, 20), (255, 250, 220))
        puestas += 1
    dr.text((Wp / 2, Hp * 0.34), "FIN", font=_font(220), fill=(255, 250, 220), anchor="mm")
    _parrafo(dr, "Y colorín colorado, la aventura de %s apenas ha comenzado." % nombre,
             Wp / 2, int(Hp * 0.48), _font(44, False), (238, 234, 255), Wp - 360, lh=1.45)
    mons = _personajes(tema, 3)
    for fx, m in zip((0.28, 0.5, 0.72), mons):
        _paste_h(im, m, Wp * fx, Hp - 420, 260)
    dr.text((Wp / 2, Hp - 130), "Un cuento hecho especialmente para vos",
            font=_font(30, False), fill=(210, 204, 240), anchor="mm")
    _pie(dr, acc)
    return im


def pagina_libro(idx, data, tema="safari"):
    """Página idx (0..TOTAL_PAGINAS-1) del libro: 0=portada, 1=dedicatoria,
    2..8=historia, 9=fin."""
    if idx == 0:
        return portada(data, tema)
    if idx == 1:
        return dedicatoria(data, tema)
    if idx == TOTAL_PAGINAS - 1:
        return fin(data, tema)
    return pagina_historia(idx - 2, data, tema)


def paginas_libro(data, tema="safari"):
    return [pagina_libro(i, data, tema) for i in range(TOTAL_PAGINAS)]


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
