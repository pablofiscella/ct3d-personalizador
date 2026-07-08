"""Menú infantil personalizado — para la mesa del cumple.

REDISEÑO 8-jul-2026 (skill armar-kit §5 — antes: media hoja vacía, "coloreá el
menú" sin nada para colorear, íconos crudos, 150dpi → imprimía A5):
- 300dpi real (A4 = 2480x3508).
- Fondo IA del tema (fondos_ia.py, pieza "menu": marco decorado + centro claro)
  si existe; fallback procedural con marco de lunares.
- Tarjetas por sección con ícono dibujado + nombres de platos tematizados por
  defecto (el cliente puede personalizar entrada/plato/postre/bebida).
- El texto SIEMPRE lo escribe el motor (nunca horneado en el arte)."""
import os, json, glob
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
_PXMM = 2480 / 210.0
Wp, Hp = 2480, 3508
CREAM = (253, 250, 242)
INK = (60, 50, 45)


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


def _icono(tipo, size, color):
    """Ícono dibujado por código (nunca emoji: tofu en Fredeka — skill §2)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    s = size
    if tipo == "entrada":       # bowl con palitos
        dr.pieslice([s * 0.12, s * 0.35, s * 0.88, s * 0.95], 0, 180, fill=color)
        for i in range(4):
            x = s * 0.28 + i * s * 0.13
            dr.rounded_rectangle([x, s * 0.12, x + s * 0.08, s * 0.45], s * 0.03, fill=color)
    elif tipo == "plato":        # porción de pizza
        dr.polygon([(s * 0.5, s * 0.1), (s * 0.87, s * 0.88), (s * 0.13, s * 0.88)], fill=color)
        for dx, dy in ((-0.1, 0.25), (0.12, 0.4), (-0.12, 0.55), (0.06, 0.65)):
            dr.ellipse([s * 0.5 + dx * s - s * 0.05, s * 0.5 + dy * s - s * 0.05,
                       s * 0.5 + dx * s + s * 0.05, s * 0.5 + dy * s + s * 0.05], fill=(255, 255, 255, 200))
    elif tipo == "postre":       # torta con velita
        dr.rounded_rectangle([s * 0.22, s * 0.5, s * 0.78, s * 0.85], s * 0.05, fill=color)
        dr.polygon([(s * 0.22, s * 0.5), (s * 0.5, s * 0.28), (s * 0.78, s * 0.5)], fill=color)
        dr.rounded_rectangle([s * 0.46, s * 0.1, s * 0.54, s * 0.28], s * 0.02, fill=color)
        dr.ellipse([s * 0.44, s * 0.02, s * 0.56, s * 0.12], fill=(255, 190, 60, 255))
    elif tipo == "bebida":       # vaso con sorbete
        dr.polygon([(s * 0.32, s * 0.22), (s * 0.68, s * 0.22), (s * 0.6, s * 0.88), (s * 0.4, s * 0.88)], fill=color)
        dr.rounded_rectangle([s * 0.46, s * 0.02, s * 0.54, s * 0.24], s * 0.02, fill=color)
    return im


# Defaults TEMATIZADOS por tema (skill §5: «Huesos de dino» — grisines con queso).
# Fallback genérico para temas sin entrada propia.
_DEFAULTS_TEMA = {
    "safari": {
        "menu_entrada": "Picada de la selva\nPalitos y snacks para explorar",
        "menu_plato": "Pizza rugido de león\no hamburguesa con papas",
        "menu_postre": "Torta de la manada\n¡con velitas!",
        "menu_bebida": "Jugo de la jungla",
    },
    "artistas": {
        "menu_entrada": "Paleta de colores\nPicada de snacks de colores",
        "menu_plato": "Pizza obra maestra\no hamburguesa con papas",
        "menu_postre": "Torta pincelada dulce\n¡con velitas!",
        "menu_bebida": "Jugo multicolor",
    },
    "monstruos": {
        "menu_entrada": "Garras crocantes\nPalitos y snacks monstruosos",
        "menu_plato": "Pizza monstruosa\no hamburguesa con papas",
        "menu_postre": "Torta de un ojo\n¡con velitas!",
        "menu_bebida": "Baba de monstruo (jugo)",
    },
    "bomberos": {
        "menu_entrada": "Mangueras crocantes\nPalitos y snacks",
        "menu_plato": "Pizza al rescate\no hamburguesa con papas",
        "menu_postre": "Torta sirena y luces\n¡con velitas!",
        "menu_bebida": "Agua del hidrante (jugo)",
    },
    "_generico": {
        "menu_entrada": "Picada divertida\nPapas fritas y palitos",
        "menu_plato": "Pizza o hamburguesa\ncon papas",
        "menu_postre": "Torta de cumpleaños\n¡con velitas!",
        "menu_bebida": "Jugo o gaseosa",
    },
}


def _defaults(tema):
    return _DEFAULTS_TEMA.get(tema, _DEFAULTS_TEMA["_generico"])


def _desc_lineas(texto, max_chars=30):
    import textwrap
    lineas = textwrap.wrap(texto, max_chars) or [texto]
    return lineas[:2]


def _fondo(tema):
    try:
        import fondos_ia
        return fondos_ia.cargar_fondo(tema, "menu")
    except Exception:
        return None


def generar_menu(data, tema="safari"):
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip() or "______________"

    fondo = _fondo(tema)
    if fondo is not None:
        im = fondo.resize((Wp, Hp), Image.LANCZOS)
    else:
        im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
        dr0 = ImageDraw.Draw(im)
        # marco procedural: doble borde + lunares en el perímetro
        dr0.rounded_rectangle([_mm(6), _mm(6), Wp - _mm(6), Hp - _mm(6)], _mm(6),
                              outline=acc, width=10)
        dr0.rounded_rectangle([_mm(10), _mm(10), Wp - _mm(10), Hp - _mm(10)], _mm(5),
                              outline=_tint(acc, 0.6), width=6)
        import random
        rnd = random.Random(42)
        for _ in range(60):
            lado = rnd.choice("NSEO")
            if lado in "NS":
                x = rnd.uniform(_mm(14), Wp - _mm(14))
                y = rnd.uniform(_mm(12), _mm(22)) if lado == "N" else rnd.uniform(Hp - _mm(22), Hp - _mm(12))
            else:
                y = rnd.uniform(_mm(14), Hp - _mm(14))
                x = rnd.uniform(_mm(12), _mm(22)) if lado == "O" else rnd.uniform(Wp - _mm(22), Wp - _mm(12))
            r = rnd.uniform(_mm(1.2), _mm(3))
            dr0.ellipse([x - r, y - r, x + r, y + r], fill=_tint(acc, rnd.choice((0.3, 0.55, 0.8))))

    dr = ImageDraw.Draw(im)

    # encabezado (~20% de la altura, skill §5)
    dr.rounded_rectangle([_mm(28), _mm(20), Wp - _mm(28), _mm(58)], _mm(7), fill=acc)
    dr.text((Wp / 2, _mm(34)), "MENÚ DEL DÍA", font=_font(110), fill="white", anchor="mm")
    dr.text((Wp / 2, _mm(48)), "Hoy cumple %s" % nombre, font=_font(64, False),
            fill=_tint(acc, 0.8), anchor="mm")

    items = [
        ("entrada", "Entrada", "menu_entrada"),
        ("plato", "Plato principal", "menu_plato"),
        ("postre", "Postre", "menu_postre"),
        ("bebida", "Bebida", "menu_bebida"),
    ]
    defaults = _defaults(tema)
    y = _mm(70)
    alto = _mm(38)
    for tipo, titulo, campo in items:
        dr.rounded_rectangle([_mm(32), y, Wp - _mm(32), y + alto], _mm(5),
                             fill=(255, 255, 255, 235), outline=_tint(acc, 0.45), width=6)
        ic = _icono(tipo, int(_mm(24)), acc)
        im.alpha_composite(ic, (int(_mm(38)), int(y + (alto - _mm(24)) / 2)))
        tx = _mm(70)
        dr.text((tx, y + _mm(10)), titulo, font=_font(66), fill=acc, anchor="lm")
        custom = str(data.get(campo) or "").strip()
        dl = _desc_lineas(custom) if custom else defaults[campo].split("\n")
        for i, line in enumerate(dl):
            dr.text((tx, y + _mm(20) + i * _mm(8.5)), line, font=_font(52, False), fill=INK, anchor="lm")
        y += alto + _mm(9)

    # con fondo IA el pie cae sobre el arte → contorno claro para que se lea
    _tx = dict(stroke_width=5, stroke_fill=(255, 253, 246)) if fondo is not None else {}
    dr.text((Wp / 2, Hp - _mm(20)), "¡Buen provecho!", font=_font(56, False),
            fill=_tint(INK, 0.25), anchor="mm", **_tx)
    dr.text((Wp / 2, Hp - _mm(11)), "casatridimensional.com.ar", font=_font(36, False),
            fill=(150, 148, 145), anchor="mm", **_tx)
    return im


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Ciro"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/menu.png"
    generar_menu({"nombre": nombre, "edad": "5"}, tema).convert("RGB").save(out)
    print("OK ->", out)
