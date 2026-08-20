"""Rompecabezas personalizado — piezas con encastres REALES para recortar y armar.

REDISEÑO 7-jul-2026 (skill armar-kit §6 — la versión anterior no era un puzzle:
el nombre gigante se dibujaba ENCIMA de la grilla, cada celda además repetía
letras, y el código de piezas con formas (_generar_piezas/_dibujar_base) era
código muerto que nunca se llamaba):
- Cortes de puzzle DE VERDAD: cada borde interior son 3 curvas Bézier cúbicas
  formando un knob (bulbo más ancho que su cuello, traba real) con jitter
  determinístico — cada pieza es única, como los generadores profesionales.
- Grilla por edad: 3x4 = 12 piezas de ~6cm (hasta 5 años) · 4x5 = 20 piezas
  (6+). Menores de 3: piezas grandes por diseño (ninguna < 4cm).
- FULL IMAGEN, SIN nombre (decisión de Pablo 8-jul-2026): la imagen completa
  del tema hecha rompecabezas — fondo IA dedicado o portada del libro.
- Página 2 = BANDEJA: el contorno de las piezas (mismas formas, mismo seed)
  para armar encima + mini imagen de referencia del puzzle armado.
- 300dpi real (A4 = 2480x3508).
"""
import os, math, json, glob, zlib, random
from PIL import Image, ImageDraw, ImageFont
import idioma

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
_PXMM = 2480 / 210.0
Wp, Hp = 2480, 3508
CREAM = (253, 250, 242)
INK = (60, 50, 45)
CORTE = (70, 60, 55)


def _mm(v):
    return v * _PXMM


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
        h = (d.get("kit") or {}).get("accent") or "#6B5BD2"
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except Exception:
        return (107, 91, 210)


def _tint(c, p):
    return tuple(int(v + (255 - v) * p) for v in c[:3])


def _personajes(tema, n=2):
    try:
        import cuaderno
        return cuaderno.personajes_decorativos(tema, n)
    except Exception:
        return []


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


# ---------------------------------------------------------------------------
# Cortes de puzzle (knobs Bézier, estilo generadores profesionales)
# ---------------------------------------------------------------------------

def _bezier(p0, p1, p2, p3, n=24):
    pts = []
    for i in range(n + 1):
        u = i / n
        v = 1 - u
        pts.append((v**3 * p0[0] + 3 * v**2 * u * p1[0] + 3 * v * u**2 * p2[0] + u**3 * p3[0],
                    v**3 * p0[1] + 3 * v**2 * u * p1[1] + 3 * v * u**2 * p2[1] + u**3 * p3[1]))
    return pts


def _borde_knob(rnd, flip=None):
    """Polilínea (coordenadas unitarias, borde de (0,0) a (1,0)) de un borde de
    puzzle con knob: 3 Bézier cúbicas, bulbo más ancho que su cuello (traba
    real), con jitter — la receta de los generadores clásicos.

    ACOTADO 11-jul-2026 (feedback Pablo probando el rompecabezas web, en dos
    rondas — «las uniones tienen que ser más chicas»): la versión original
    (t=0.2, controles a 3t) llevaba la PUNTA del knob al ~45% de la celda (el
    comentario decía 18%…) y los knobs de bordes perpendiculares se CRUZABAN
    entre sí (~12 cruces por puzzle 4x5): líneas superpuestas y piezas con
    puntas visualmente sueltas. Proporciones actuales CALIBRADAS contra el
    estándar comercial ribbon-cut (= default del generador clásico de
    Draradech: traba ~20% de la celda), medidas con ESC=0.9:
    profundidad ≈21% de la celda · bulbo ≈28% del borde · cuello 20%
    (traba 1.4: el bulbo agarra de verdad). Knobs que jamás se tocan — test
    guardián de intersecciones en tests/test_rompecabezas_bordes.py."""
    t = 0.10                                    # medio ancho del cuello
    j = 0.025                                   # jitter
    a, b, c, d = (rnd.uniform(-j, j) for _ in range(4))
    if flip is None:
        flip = rnd.choice((1, -1))              # knob para un lado o el otro
    def f(x, y):
        return (x, y * flip)
    p = []
    p += _bezier(f(0, 0), f(0.25, a), f(0.5 + b + d, -0.6 * t + c), f(0.5 - t + b, t + c))
    p += _bezier(f(0.5 - t + b, t + c), f(0.5 - 3.0 * t + b - d, 2.8 * t + c),
                 f(0.5 + 3.0 * t + b - d, 2.8 * t + c), f(0.5 + t + b, t + c))[1:]
    p += _bezier(f(0.5 + t + b, t + c), f(0.5 + b + d, -0.6 * t + c), f(0.75, a), f(1, 0))[1:]
    return p


def _bordes_grilla(cols, filas, seed):
    """Bordes interiores de la grilla, determinísticos por seed: el MISMO seed
    reproduce las MISMAS formas en la página bandeja.

    Flips en DAMERO (no al azar — feedback Pablo 11-jul-2026): con flip
    aleatorio salían piezas con las 4 trabas para afuera («puntas que no las
    une nada»); alternando por paridad, TODA pieza interior queda con 2 trabas
    y 2 huecos, como los puzzles comerciales. La variedad la sigue poniendo el
    jitter (cada pieza es única igual)."""
    rnd = random.Random(seed)
    horiz = [[_borde_knob(rnd, 1 if (fi + ci) % 2 == 0 else -1)
              for ci in range(cols)] for fi in range(filas - 1)]
    vert = [[_borde_knob(rnd, 1 if (ci + fi) % 2 == 0 else -1)
             for fi in range(filas)] for ci in range(cols - 1)]
    return horiz, vert


def _dibujar_cortes(dr, x0, y0, w, h, cols, filas, horiz, vert, color, ancho):
    cw, ch = w / cols, h / filas
    escala_knob = 0.9                            # knob ~18% del alto/ancho de celda
    for fi in range(filas - 1):
        y = y0 + (fi + 1) * ch
        for ci in range(cols):
            pts = [(x0 + ci * cw + px * cw, y + py * ch * escala_knob) for px, py in horiz[fi][ci]]
            dr.line(pts, fill=color, width=ancho, joint="curve")
    for ci in range(cols - 1):
        x = x0 + (ci + 1) * cw
        for fi in range(filas):
            pts = [(x + py * cw * escala_knob, y0 + fi * ch + px * ch) for px, py in vert[ci][fi]]
            dr.line(pts, fill=color, width=ancho, joint="curve")
    dr.rectangle([x0, y0, x0 + w, y0 + h], outline=color, width=ancho)


# SET de 6 hojas (Pablo 11-jul-2026: «en ambos quiero que estén los 6
# rompecabezas que están en test») — las MISMAS escenas del interactivo con
# dificultad PROGRESIVA, la misma escalera de niveles del web (4 → 48 piezas;
# piezas cuadradas en el área 180x240mm; la de 48 da piezas de 30x30mm).
GRILLAS_SET = [(2, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 8)]


def _imagenes(tema):
    """Las MISMAS escenas que el rompecabezas interactivo (hasta 6 paths)."""
    try:
        import rompecabezas_web
        return rompecabezas_web._imagenes_tema(tema)[:len(GRILLAS_SET)]
    except Exception:
        return []


def n_puzzles(tema):
    """Cuántas hojas trae el set (1 con el fallback procedural)."""
    return max(1, len(_imagenes(tema)))


def _imagen_puzzle(tema):
    """La imagen COMPLETA del puzzle (decisión de Pablo 8-jul-2026: full imagen,
    SIN nombre — «como si fuera una imagen completa pero hecha rompecabezas»).
    Prioridad: fondo IA dedicado (fondos_ia «rompecabezas») > la portada del
    libro del tema (una escena rica ya generada) > ia_maestra > None."""
    try:
        import fondos_ia
        f = fondos_ia.cargar_fondo(tema, "rompecabezas")
        if f is not None:
            return f
    except Exception:
        pass
    try:
        import libro
        p = libro.override_escena_path(tema, 0)
        if os.path.isfile(p):
            return Image.open(p).convert("RGBA")
    except Exception:
        pass
    p = os.path.join(TEMAS, tema, "ia_maestra.png")
    if os.path.isfile(p):
        return Image.open(p).convert("RGBA")
    return None


def _arte(tema, w, h):
    """Arte a página completa. Con imagen del tema: cover (nunca estirar). Sin
    imagen: fallback procedural (patrón + personajes), también sin nombre."""
    img = _imagen_puzzle(tema)
    if img is not None:
        import fondos_ia
        return fondos_ia.cover(img, int(w), int(h))
    acc = _accent(tema)
    im = Image.new("RGBA", (int(w), int(h)), _tint(acc, 0.8) + (255,))
    dr = ImageDraw.Draw(im)
    rnd = random.Random(zlib.crc32(("arte-" + tema).encode()))
    for _ in range(120):                          # lunares suaves
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.uniform(_mm(2), _mm(5))
        dr.ellipse([x - r, y - r, x + r, y + r], fill=_tint(acc, rnd.choice((0.6, 0.7, 0.92))))
    pjs = _personajes(tema, 3)
    if pjs:
        _paste_h(im, pjs[0], w * 0.5, h * 0.32, h * 0.40)
        for pj, fx in zip(pjs[1:], (0.26, 0.74)):
            _paste_h(im, pj, w * fx, h * 0.74, h * 0.32)
    return im


def _arte_hoja(tema, idx, w, h):
    """El arte de la hoja `idx`: su escena del set (cover, nunca estira) o el
    fallback procedural si el tema no tiene imágenes."""
    imgs = _imagenes(tema)
    if idx < len(imgs):
        import fondos_ia
        return fondos_ia.cover(Image.open(imgs[idx]).convert("RGBA"), int(w), int(h))
    return _arte(tema, w, h)


def _grilla_hoja(idx):
    return GRILLAS_SET[min(idx, len(GRILLAS_SET) - 1)]


def puzzle_pagina(data, tema="safari", idx=0):
    """Hoja `idx` del set: la escena con los CORTES de puzzle encima (sin
    nombre — el seed de las formas sale de tema+hoja+grilla)."""
    acc = _accent(tema)
    cols, filas = _grilla_hoja(idx)
    seed = zlib.crc32(("%s|%d|%dx%d" % (tema, idx, cols, filas)).encode())

    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)
    dr.text((60, 55), idioma.traducir("ROMPECABEZAS %d · %d piezas", idioma.de(data)) % (idx + 1, cols * filas),
            font=_font(44, False), fill=_tint(acc, 0.3))

    aw, ah = _mm(180), _mm(240)
    ax, ay = (Wp - aw) / 2, _mm(22)
    im.alpha_composite(_arte_hoja(tema, idx, aw, ah), (int(ax), int(ay)))

    horiz, vert = _bordes_grilla(cols, filas, seed)
    _dibujar_cortes(ImageDraw.Draw(im), ax, ay, aw, ah, cols, filas, horiz, vert, CORTE, 5)

    dr2 = ImageDraw.Draw(im)
    dr2.text((Wp / 2, ay + ah + _mm(12)),
             idioma.traducir("Pegá esta hoja sobre cartulina o cartón fino y recortá por las líneas.", idioma.de(data)),
             font=_font(38, False), fill=_tint(INK, 0.25), anchor="mm")
    dr2.text((Wp / 2, Hp - 60), "casatridimensional.com.ar", font=_font(36, False),
             fill=(180, 180, 180), anchor="mm")
    return im


def bandeja_pagina(data, tema="safari", idx=0):
    """Bandeja de la hoja `idx`: contornos de las MISMAS piezas (mismo seed)
    para armar encima + mini referencia del puzzle armado."""
    acc = _accent(tema)
    cols, filas = _grilla_hoja(idx)
    seed = zlib.crc32(("%s|%d|%dx%d" % (tema, idx, cols, filas)).encode())

    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)
    dr.text((60, 55), idioma.traducir("BANDEJA %d · armá el rompecabezas acá encima", idioma.de(data)) % (idx + 1),
            font=_font(44, False), fill=_tint(acc, 0.3))

    aw, ah = _mm(180), _mm(240)
    ax, ay = (Wp - aw) / 2, _mm(22)
    dr.rounded_rectangle([ax - _mm(4), ay - _mm(4), ax + aw + _mm(4), ay + ah + _mm(4)],
                         _mm(4), fill=_tint(acc, 0.94) + (255,), outline=_tint(acc, 0.5), width=6)
    horiz, vert = _bordes_grilla(cols, filas, seed)
    _dibujar_cortes(ImageDraw.Draw(im), ax, ay, aw, ah, cols, filas, horiz, vert,
                    _tint(acc, 0.45), 4)

    # mini referencia ADENTRO de la bandeja (esquina inferior derecha, como las
    # bandejas profesionales: las piezas la van tapando al armar)
    mini = _arte_hoja(tema, idx, aw, ah)
    mini.thumbnail((int(_mm(38)), int(_mm(50))), Image.LANCZOS)
    mx = int(ax + aw - mini.width - _mm(6))
    my = int(ay + ah - mini.height - _mm(6))
    im.alpha_composite(mini, (mx, my))
    dr2 = ImageDraw.Draw(im)
    dr2.rectangle([mx, my, mx + mini.width, my + mini.height], outline=acc, width=5)
    dr2.text((mx + mini.width / 2, my - _mm(4)), idioma.traducir("así queda", idioma.de(data)),
             font=_font(28, False), fill=_tint(INK, 0.35), anchor="mm")
    dr2.text((Wp / 2, ay + ah + _mm(12)),
             idioma.traducir("Cada pieza tiene un solo lugar. ¡Mirá la referencia si te trabás!", idioma.de(data)),
             font=_font(36, False), fill=_tint(INK, 0.25), anchor="mm")
    dr2.text((Wp / 2, Hp - 60), "casatridimensional.com.ar", font=_font(36, False),
             fill=(180, 180, 180), anchor="mm")
    return im


def rompecabezas_nombre(data, tema="safari"):
    """Compat: la primera hoja del set (usos viejos: previews/audit)."""
    return puzzle_pagina(data, tema, 2)      # 12 piezas: la más representativa


def bandeja(data, tema="safari"):
    """Compat: la bandeja de la primera hoja representativa."""
    return bandeja_pagina(data, tema, 2)


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Sofía"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/rompecabezas.png"
    rompecabezas_nombre({"nombre": nombre, "edad": "4"}, tema).convert("RGB").save(out)
    bandeja({"nombre": nombre, "edad": "4"}, tema).convert("RGB").save(out.replace(".png", "_bandeja.png"))
    print("OK ->", out)
