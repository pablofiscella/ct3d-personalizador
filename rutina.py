"""Rutina visual del niño — lámina A4 imprimible, personalizada por nombre + tema.

Producto evergreen (se busca todo el año: "rutina visual niño imprimible").
A diferencia del cuaderno (canónico por tema+edad), la rutina se PERSONALIZA por
dato del cliente (nombre, tema), igual que la invitación → entra por el camino
genérico de piezas de productos.py.

Decisión de diseño: SIN horarios de reloj. La rutina visual para 2-5 años es
secuencial-pictográfica (el chico no lee la hora todavía); cada paso es un ícono
+ una palabra + un casillero para tildar. Esto además evita un editor de horas.

Los íconos se dibujan 100% con Pillow (autocontenido, sin assets externos), en el
color de acento de la temática. El arte del tema (si lo hay) decora el encabezado.

API: generar_rutina(data, tema) -> PIL.Image (A4 vertical, RGBA).
"""
import os, math, glob
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
NAVY = (29, 25, 79); VIOLET = (107, 91, 210); INK = (40, 38, 55); CREAM = (246, 242, 236)
SOLY = (240, 170, 40)            # amarillo sol (mañana)
NOCHE = (74, 86, 140)            # azul noche


def _font(sz, bold=True):
    for p in glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True):
        try:
            f = ImageFont.truetype(p, sz)
            try: f.set_variation_by_axes([700 if bold else 500])
            except Exception: pass
            return f
        except Exception: pass
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)


def _tint(c, p):
    """Mezcla c hacia blanco (p=0 igual, p=1 blanco)."""
    return tuple(int(v + (255 - v) * p) for v in c[:3])


def _accent(tema):
    """Color de acento de la temática (lee tema.json), con fallback al violeta CT3D."""
    try:
        import json
        d = json.load(open(os.path.join(TEMAS, tema, "tema.json")))
        h = (d.get("kit") or {}).get("accent")
        if h:
            h = h.lstrip("#")
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except Exception:
        pass
    return VIOLET


# ───────────────────────────── íconos (Pillow) ─────────────────────────────
# Cada _ic_* dibuja un pictograma RELLENO en `col`, dentro de un cuadro de lado
# ~2r centrado en (cx, cy). Estilo plano, redondeado, reconocible para chicos.

def _ic_sol(dr, cx, cy, r, col):
    for i in range(12):
        a = i * math.pi / 6
        dr.line([cx + r * .72 * math.cos(a), cy + r * .72 * math.sin(a),
                 cx + r * 1.05 * math.cos(a), cy + r * 1.05 * math.sin(a)], fill=col, width=max(4, r // 9))
    dr.ellipse([cx - r * .55, cy - r * .55, cx + r * .55, cy + r * .55], fill=col)

def _ic_luna(dr, cx, cy, r, col, bg):
    dr.ellipse([cx - r * .72, cy - r * .82, cx + r * .72, cy + r * .82], fill=col)
    dr.ellipse([cx - r * .15, cy - r * .98, cx + r * 1.1, cy + r * .66], fill=bg)   # recorte → medialuna
    dr.ellipse([cx + r * .42, cy - r * .62, cx + r * .58, cy - r * .46], fill=col)  # estrellita

def _ic_diente(dr, cx, cy, r, col, bg):
    dr.rounded_rectangle([cx - r * .6, cy - r * .78, cx + r * .6, cy + r * .15], radius=r * .45, fill=col)
    dr.ellipse([cx - r * .24, cy - r * 1.02, cx + r * .24, cy - r * .5], fill=bg)   # hendidura superior
    dr.polygon([(cx - r * .6, cy - r * .05), (cx - r * .06, cy - r * .05), (cx - r * .34, cy + r * .88)], fill=col)
    dr.polygon([(cx + r * .06, cy - r * .05), (cx + r * .6, cy - r * .05), (cx + r * .34, cy + r * .88)], fill=col)

def _ic_plato(dr, cx, cy, r, col):
    dr.ellipse([cx - r * .85, cy - r * .85, cx + r * .35, cy + r * .35], outline=col, width=max(5, r // 7))
    dr.ellipse([cx - r * .55, cy - r * .55, cx + r * .05, cy + r * .05], fill=col)
    # tenedor a la derecha
    fx = cx + r * .62
    dr.line([fx, cy - r * .75, fx, cy + r * .8], fill=col, width=max(5, r // 8))
    for dx in (-.18, 0, .18):
        dr.line([fx + r * dx, cy - r * .75, fx + r * dx, cy - r * .35], fill=col, width=max(4, r // 10))

def _ic_ropa(dr, cx, cy, r, col):
    # remera
    pts = [(cx - r * .8, cy - r * .35), (cx - r * .35, cy - r * .7), (cx - r * .18, cy - r * .55),
           (cx + r * .18, cy - r * .55), (cx + r * .35, cy - r * .7), (cx + r * .8, cy - r * .35),
           (cx + r * .5, cy - r * .02), (cx + r * .42, cy - r * .12),
           (cx + r * .42, cy + r * .8), (cx - r * .42, cy + r * .8),
           (cx - r * .42, cy - r * .12), (cx - r * .5, cy - r * .02)]
    dr.polygon(pts, fill=col)

def _ic_mochila(dr, cx, cy, r, col):
    dr.rounded_rectangle([cx - r * .6, cy - r * .55, cx + r * .6, cy + r * .8], r * .25, fill=col)
    dr.rounded_rectangle([cx - r * .38, cy - r * .15, cx + r * .38, cy + r * .45], r * .12, fill=(255, 255, 255))
    dr.arc([cx - r * .35, cy - r * .95, cx + r * .35, cy - r * .2], 180, 360, fill=col, width=max(5, r // 7))

def _ic_ducha(dr, cx, cy, r, col):
    # tina
    dr.rounded_rectangle([cx - r * .8, cy - r * .05, cx + r * .8, cy + r * .55], r * .22, fill=col)
    dr.line([cx - r * .55, cy + r * .55, cx - r * .55, cy + r * .8], fill=col, width=max(5, r // 8))
    dr.line([cx + r * .55, cy + r * .55, cx + r * .55, cy + r * .8], fill=col, width=max(5, r // 8))
    for dx in (-.35, 0, .35):                                          # burbujas
        dr.ellipse([cx + r * dx - r * .12, cy - r * .6, cx + r * dx + r * .12, cy - r * .36], outline=col, width=max(3, r // 12))

def _ic_pijama(dr, cx, cy, r, col):
    _ic_ropa(dr, cx, cy - r * .05, r * .9, col)
    dr.ellipse([cx + r * .02, cy + r * .12, cx + r * .26, cy + r * .36], fill=(255, 255, 255))  # estrellita

def _ic_libro(dr, cx, cy, r, col):
    dr.line([cx, cy - r * .6, cx, cy + r * .55], fill=col, width=max(5, r // 8))
    dr.polygon([(cx, cy - r * .6), (cx - r * .8, cy - r * .45), (cx - r * .8, cy + r * .55), (cx, cy + r * .45)], fill=col)
    dr.polygon([(cx, cy - r * .6), (cx + r * .8, cy - r * .45), (cx + r * .8, cy + r * .55), (cx, cy + r * .45)], fill=col)
    for i in range(3):
        yy = cy - r * .25 + i * r * .28
        dr.line([cx - r * .62, yy, cx - r * .15, yy + r * .05], fill=(255, 255, 255), width=max(2, r // 16))
        dr.line([cx + r * .15, yy + r * .05, cx + r * .62, yy], fill=(255, 255, 255), width=max(2, r // 16))

def _ic_cama(dr, cx, cy, r, col):
    dr.rounded_rectangle([cx - r * .85, cy + r * .1, cx + r * .85, cy + r * .55], r * .12, fill=col)
    dr.line([cx - r * .85, cy + r * .55, cx - r * .85, cy + r * .85], fill=col, width=max(5, r // 7))
    dr.line([cx + r * .85, cy + r * .55, cx + r * .85, cy + r * .85], fill=col, width=max(5, r // 7))
    dr.rounded_rectangle([cx - r * .85, cy - r * .35, cx - r * .35, cy + r * .15], r * .12, fill=col)  # respaldo
    dr.rounded_rectangle([cx - r * .72, cy - r * .12, cx - r * .3, cy + r * .12], r * .1, fill=(255, 255, 255))  # almohada

def _ic_inodoro(dr, cx, cy, r, col):
    dr.rounded_rectangle([cx + r * .2, cy - r * .8, cx + r * .7, cy - r * .1], r * .12, fill=col)  # mochila
    dr.ellipse([cx - r * .75, cy - r * .25, cx + r * .45, cy + r * .55], fill=col)
    dr.ellipse([cx - r * .5, cy - r * .05, cx + r * .2, cy + r * .4], fill=(255, 255, 255))
    dr.line([cx - r * .15, cy + r * .55, cx - r * .15, cy + r * .82], fill=col, width=max(6, r // 6))

def _ic_pelota(dr, cx, cy, r, col):
    dr.ellipse([cx - r * .72, cy - r * .72, cx + r * .72, cy + r * .72], fill=col)
    w = max(4, r // 9); W = (255, 255, 255)
    dr.line([cx, cy - r * .72, cx, cy + r * .72], fill=W, width=w)
    dr.arc([cx - r * 1.5, cy - r * .72, cx - r * .05, cy + r * .72], 300, 60, fill=W, width=w)
    dr.arc([cx + r * .05, cy - r * .72, cx + r * 1.5, cy + r * .72], 120, 240, fill=W, width=w)

_ICONOS = {
    "sol": _ic_sol, "plato": _ic_plato, "ropa": _ic_ropa, "mochila": _ic_mochila,
    "ducha": _ic_ducha, "pijama": _ic_pijama, "libro": _ic_libro, "cama": _ic_cama,
    "inodoro": _ic_inodoro, "pelota": _ic_pelota,
}


def _icon(dr, key, cx, cy, r, col, bg=(255, 255, 255)):
    if key == "luna":     # luna y diente necesitan el color de fondo para el recorte
        _ic_luna(dr, cx, cy, r, col, bg); return
    if key == "diente":
        _ic_diente(dr, cx, cy, r, col, bg); return
    fn = _ICONOS.get(key)
    if not fn:
        dr.ellipse([cx - r * .5, cy - r * .5, cx + r * .5, cy + r * .5], fill=col); return
    fn(dr, cx, cy, r, col)


# ─────────────────────────── rutinas por defecto ───────────────────────────
# (icono, etiqueta). Editable a futuro vía data["manana"]/data["noche"].
DEFAULT_MANANA = [
    ("sol", "Despertar"),
    ("inodoro", "Ir al baño"),
    ("plato", "Desayunar"),
    ("ropa", "Vestirme"),
    ("diente", "Lavarme los dientes"),
    ("pelota", "¡A jugar!"),
]
DEFAULT_NOCHE = [
    ("plato", "Cenar"),
    ("ducha", "Bañarme"),
    ("pijama", "Ponerme el pijama"),
    ("diente", "Lavarme los dientes"),
    ("libro", "Un cuento"),
    ("cama", "A dormir"),
]


def _columna(im, dr, x0, x1, y0, y1, titulo, ic_titulo, header_col, items, acc):
    """Dibuja una columna (mañana/noche) con tarjeta, encabezado y filas."""
    dr.rounded_rectangle([x0, y0, x1, y1], 34, fill=(255, 255, 255), outline=_tint(header_col, .55), width=3)
    # encabezado de la columna
    hh = 150
    dr.rounded_rectangle([x0, y0, x1, y0 + hh], 34, fill=header_col)
    dr.rectangle([x0, y0 + hh - 34, x1, y0 + hh], fill=header_col)
    _icon(dr, ic_titulo, x0 + 78, y0 + hh / 2, 52, (255, 255, 255), header_col)
    dr.text((x0 + 145, y0 + hh / 2), titulo, font=_font(56), fill="white", anchor="lm")
    # filas
    n = len(items)
    rh = (y1 - y0 - hh - 30) / n
    ry = y0 + hh + 16
    icx = x0 + 92
    bx = x1 - 78
    icbg = _tint(acc, .82)
    maxw = (bx - 30) - (icx + 80) - 14
    for i, (key, label) in enumerate(items):
        yc = ry + rh / 2
        if i:
            dr.line([x0 + 40, ry, x1 - 40, ry], fill=_tint(header_col, .75), width=2)
        # círculo del ícono
        dr.ellipse([icx - 52, yc - 52, icx + 52, yc + 52], fill=icbg)
        _icon(dr, key, icx, yc, 44, acc, icbg)
        # etiqueta (auto-ajuste para no pisar el casillero)
        fs = 34; lf = _font(fs, True)
        while lf.getbbox(label)[2] > maxw and fs > 22:
            fs -= 2; lf = _font(fs, True)
        dr.text((icx + 80, yc), label, font=lf, fill=INK, anchor="lm")
        # casillero para tildar
        dr.rounded_rectangle([bx - 26, yc - 26, bx + 26, yc + 26], 9, outline=_tint(header_col, .35), width=4)
        ry += rh


def _decorar_header(im, tema):
    """Pega 1-2 personajes PROPIOS del tema en las esquinas del encabezado (best-effort).

    Reglas: 1) personajes recortados del sticker sheet del tema (sirve para cualquier
    tema que tenga extras/stickers_1.png). 2) si no hay, animales SOLO si el tema es
    realmente de animales (tiene sus propios recortes, p.ej. safari). NUNCA un fallback
    genérico: pondría animalitos en temas que no son de animales (bomberos, circo, etc.)."""
    chars = []
    try:
        import cuaderno
        # personajes FILTRADOS y deduplicados (los primeros 2 recortes crudos
        # metían figuritas repetidas y chiquitas — feedback Pablo, princesas);
        # completa con objetos del tema si hay un solo personaje
        chars = cuaderno.personajes_decorativos(tema, 2, incluir_objetos=True)
    except Exception:
        chars = []
    if not chars:
        try:
            import piezas
            if piezas.has_recortes(tema):
                for nm in (piezas.animales(tema) or [])[:2]:
                    try:
                        chars.append(piezas.load(nm, tema))
                    except Exception:
                        pass
        except Exception:
            pass
    if not chars:
        return
    def _img(c):
        return Image.open(c).convert("RGBA") if isinstance(c, str) else c.convert("RGBA")
    spots = [(Wp - 150, 92), (150, 92)]
    for c, (sx, sy) in zip(chars, spots):
        try:
            ch = _img(c); h = 150
            r = h / ch.height; ch = ch.resize((max(1, int(ch.width * r)), h), Image.LANCZOS)
            im.alpha_composite(ch, (int(sx - ch.width / 2), int(sy - ch.height / 2)))
        except Exception:
            pass


def generar_rutina(data, tema="monstruos"):
    """Lámina A4 (RGBA) con la rutina de mañana y noche, personalizada con el nombre."""
    acc = _accent(tema)
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    # ── encabezado con DEGRADÉ del acento + guirnalda de banderines (el
    # rectángulo chato se veía pobre — feedback Pablo 8-jul-2026)
    header_h = 185
    oscuro = tuple(int(v * 0.42) for v in acc)
    medio = tuple(int(v * 0.75) for v in acc)
    col = Image.new("RGB", (1, header_h))
    for i in range(header_h):
        t = i / (header_h - 1)
        col.putpixel((0, i), tuple(int(a + (b - a) * t) for a, b in zip(oscuro, medio)))
    im.paste(col.resize((Wp, header_h)), (0, 0))
    # banderines colgando del borde inferior del banner
    for i in range(14):
        bx = 40 + i * (Wp - 80) / 13
        c = [_tint(acc, 0.15), (255, 214, 98), _tint(acc, 0.55)][i % 3]
        dr.polygon([(bx - 22, header_h), (bx + 22, header_h), (bx, header_h + 40)], fill=c)
    nombre = (str(data.get("nombre") or "").strip() or "mi peque")
    titulo = "La rutina de %s" % nombre
    fs = 74
    while _font(fs).getbbox(titulo)[2] > Wp - 420 and fs > 40:
        fs -= 3
    dr.text((Wp / 2 + 3, 79), titulo, font=_font(fs), fill=tuple(int(v * 0.55) for v in oscuro), anchor="mm")
    dr.text((Wp / 2, 76), titulo, font=_font(fs), fill="white", anchor="mm")
    dr.text((Wp / 2, 140), "Mi día, paso a paso", font=_font(30, False),
            fill=tuple(int(v + (255 - v) * 0.78) for v in acc), anchor="mm")
    _decorar_header(im, tema)

    # ── dos columnas
    mg = 60; gap = 40
    colW = (Wp - 2 * mg - gap) / 2
    y0, y1 = 235, Hp - 130
    _columna(im, dr, mg, mg + colW, y0, y1, "Mañana", "sol", SOLY, data.get("manana") or DEFAULT_MANANA, acc)
    _columna(im, dr, mg + colW + gap, Wp - mg, y0, y1, "Noche", "luna", NOCHE, data.get("noche") or DEFAULT_NOCHE, acc)

    # ── pie
    dr.text((Wp / 2, Hp - 60), "Imprimila, pegala a la altura del peque y tildá cada paso",
            font=_font(24, False), fill=INK, anchor="mm")
    dr.text((Wp / 2, Hp - 26), "casatridimensional.com.ar", font=_font(20, False), fill=(150, 150, 160), anchor="mm")
    return im


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "monstruos"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Mateo"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/rutina.png"
    generar_rutina({"nombre": nombre, "edad": "4"}, tema).convert("RGB").save(out)
    print("OK ->", out)
