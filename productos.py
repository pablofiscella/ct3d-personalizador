#!/usr/bin/env python3
"""Registro de TIPOS de producto digital + piezas nuevas.

El motor pasó de generar un solo producto (el kit de 7 piezas) a un catálogo
data-driven: cada `tipo` declara qué piezas arma, qué campos pide y qué pieza
usar de vista previa. El pipeline de compra/pago/entrega de la tienda no cambia:
solo viaja un `tipo` extra.

Tipos:
- kit           → las 7 piezas (comportamiento histórico, default).
- invitacion    → solo la invitación (1 PDF).
- cartel        → solo el cartel/afiche de bienvenida (1 PDF).
- actividades   → pack para imprimir: hoja "para colorear" + hoja de "juegos".
- milestone     → tarjetas mes a mes del bebé (1 mes … 12 meses).
- certificado   → diploma oficial de cumpleañero.
- corona        → gorro cónico + corona de rey para armar.
- antifaces     → antifaz, bigotes y lentes para photo booth.
- menu          → menú infantil para la mesa del salón.
- rompecabezas  → nombre partido en piezas para recortar y armar.
- capsula       → carta para el futuro (sobre + hoja de preguntas).
- libro         → libro de cuento personalizado (10 páginas, el chico es el protagonista).
- calendario    → 12 meses personalizados con la temática.
- papertoys     → cubo 3D con letras del nombre para armar.
- memoria       → juego de memoria con 24 cartas (12 pares).

Las piezas nuevas se arman 100% procedurales (Pillow), reutilizando la paleta y
tipografía de cada temática (bloque "kit" del tema.json).
"""
import os
from PIL import Image, ImageDraw

import piezas
import temas
from piezas import (A4, WHITE, CREAM, MUST, SAGE, make_sheet, txt, fit_into,
                    paste_center, accent, ink_c, font_disp, _band, animales,
                    load, has_recortes, _edad_any, lema, titulo)
from generador import (render, specs_de, draw_text, _effective_texts, BROWN, OLIVE,
                       TERRA, _safe_edad, layout_file_path, _hex_rgb, _FONT_FILES)

INK = (74, 74, 74)  # gris oscuro para líneas de colorear


# ---------------------------------------------------------------------------
# PIEZAS NUEVAS (procedurales, por temática)
# ---------------------------------------------------------------------------
def _tint(rgb, p):
    """Mezcla un color hacia el blanco (p=0 igual, p=1 blanco). Para fondos suaves."""
    return tuple(int(c + (255 - c) * p) for c in rgb[:3])


def _frame(d, W, H, color):
    """Marco decorativo doble (línea + filete fino) en el color de la temática."""
    d.rounded_rectangle([60, 60, W - 60, H - 60], radius=70, outline=color + (255,), width=7)
    d.rounded_rectangle([94, 94, W - 94, H - 94], radius=54, outline=_tint(color, 0.5) + (255,), width=3)


def _pie_marca(d, W, H, color):
    """Pie de marca discreto (la tienda)."""
    txt(d, "casatridimensional.com.ar", W / 2, H - 92, "Poppins-Medium.ttf", 36, _tint(color, 0.3), W * 0.9)


def _outline_text(d, text, cx, cy, font_file, size, maxw, wght=None, stroke=8):
    """Texto 'burbuja' (relleno claro + contorno) para que el chico lo pinte."""
    if not str(text).strip():
        return
    from generador import fit_font
    f = fit_font(d, str(text), font_file, int(size), int(maxw), wght)
    d.text((cx, cy), str(text), font=f, fill=(255, 255, 255),
           stroke_width=stroke, stroke_fill=INK, anchor="mm")


def _estrella(d, cx, cy, r, color, w=6):
    import math
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rad = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.line(pts + [pts[0]], fill=color, width=w, joint="curve")


def _num(d, text, cx, cy, font_file, size, color, maxw, wght=None):
    """Dibuja un número/texto corto centrado por su bounding box REAL (no por las
    métricas de la fuente), así queda centrado de verdad con cualquier tipografía."""
    from generador import fit_font
    f = fit_font(d, str(text), font_file, int(size), int(maxw), wght)
    l, t, r, b = d.textbbox((0, 0), str(text), font=f)
    d.text((cx - (l + r) / 2, cy - (t + b) / 2), str(text), font=f, fill=color)


def colorear(data, tema=None):
    """Hoja A4 'para colorear': contornos negros (sin relleno) que el chico pinta,
    con marco y títulos en el color de la temática."""
    W, H = A4
    acc = accent(tema); ink = ink_c(tema)
    base = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(base)
    _frame(d, W, H, acc)
    nombre = (data.get("nombre") or "").strip()
    txt(d, "¡Para pintar!", W / 2, 255, font_disp(tema), 140, acc, W * 0.7, wght=700)
    txt(d, "Coloreá y decorá tu cumple", W / 2, 400, "Fredoka-VF.ttf", 60, ink, W * 0.7, wght=600)
    if nombre:
        _outline_text(d, nombre, W / 2, 620, font_disp(tema), 290, W * 0.72, wght=700, stroke=10)
    # globos (para pintar)
    for gx, gy, rr in [(0.27, 0.43, 200), (0.5, 0.46, 240), (0.73, 0.43, 200)]:
        cx, cy = W * gx, H * gy
        d.ellipse([cx - rr, cy - rr * 1.2, cx + rr, cy + rr * 1.2], outline=INK, width=8)
        d.line([(cx, cy + rr * 1.2), (cx, cy + rr * 1.2 + 190)], fill=INK, width=6)
        d.polygon([(cx - 15, cy + rr * 1.2), (cx + 15, cy + rr * 1.2), (cx, cy + rr * 1.2 + 26)], outline=INK, width=4)
    # torta (para pintar)
    cx, cy, cw_, ch_ = W * 0.5, H * 0.69, W * 0.29, H * 0.13
    d.rounded_rectangle([cx - cw_, cy, cx + cw_, cy + ch_], radius=40, outline=INK, width=8)
    d.rounded_rectangle([cx - cw_ * 0.7, cy - ch_ * 0.6, cx + cw_ * 0.7, cy], radius=30, outline=INK, width=8)
    for k in range(5):
        vx = cx - cw_ * 0.5 + k * (cw_ / 4)
        d.line([(vx, cy - ch_ * 0.6), (vx, cy - ch_ * 1.0)], fill=INK, width=6)
        d.ellipse([vx - 13, cy - ch_ * 1.15, vx + 13, cy - ch_ * 1.0], outline=INK, width=5)
    # regalo (para pintar)
    gx0, gy0, gs = W * 0.22, H * 0.85, W * 0.12
    d.rounded_rectangle([gx0 - gs, gy0 - gs * 0.8, gx0 + gs, gy0 + gs * 0.8], radius=18, outline=INK, width=8)
    d.line([(gx0, gy0 - gs * 0.8), (gx0, gy0 + gs * 0.8)], fill=INK, width=8)
    d.line([(gx0 - gs, gy0 - gs * 0.18), (gx0 + gs, gy0 - gs * 0.18)], fill=INK, width=8)
    # estrellas (para pintar)
    for sx, sy in [(0.18, 0.25), (0.82, 0.25), (0.80, 0.85)]:
        _estrella(d, W * sx, H * sy, 78, INK, w=7)
    _pie_marca(d, W, H, ink)
    return base


def juegos(data, tema=None):
    """Hoja A4 de juegos en 'tarjetas' suaves: tatetí + uní los puntos + dibujá."""
    W, H = A4
    acc = accent(tema); ink = ink_c(tema)
    base = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(base)
    _frame(d, W, H, acc)
    nombre = (data.get("nombre") or "").strip()
    txt(d, "Juegos del cumple", W / 2, 250, font_disp(tema), 124, acc, W * 0.78, wght=700)
    if nombre:
        txt(d, "de " + nombre, W / 2, 392, "Fredoka-VF.ttf", 68, ink, W * 0.78, wght=600)
    tintbg = _tint(acc, 0.88)

    def card(y0, y1, titulo):
        d.rounded_rectangle([W * 0.10, y0, W * 0.90, y1], radius=46, fill=tintbg + (255,),
                            outline=acc + (255,), width=4)
        txt(d, titulo, W * 0.5, y0 + 78, "Fredoka-VF.ttf", 66, acc, W * 0.72, wght=700)

    # Tatetí
    y0 = H * 0.165; card(y0, H * 0.40, "Tatetí")
    g = int(W * 0.165); oy = int(y0 + 210)
    for j in range(3):
        ox = int(W * (0.175 + j * 0.245))
        for k in (1, 2):
            d.line([(ox + k * g / 3, oy), (ox + k * g / 3, oy + g)], fill=ink, width=6)
            d.line([(ox, oy + k * g / 3), (ox + g, oy + k * g / 3)], fill=ink, width=6)
    # Uní los puntos
    import math
    card(H * 0.43, H * 0.72, "Uní los puntos")
    cx, cy, r = W * 0.5, H * 0.595, W * 0.155
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rad = r if k % 2 == 0 else r * 0.45
        px, py = cx + rad * math.cos(ang), cy + rad * math.sin(ang)
        d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=ink)
        txt(d, str(k + 1), px + 32, py - 32, "Poppins-Medium.ttf", 48, acc, 110)
    # Dibujá
    card(H * 0.75, H * 0.93, "Dibujá tu regalo soñado")
    d.rounded_rectangle([W * 0.17, H * 0.815, W * 0.83, H * 0.915], radius=28, outline=ink, width=5)
    _pie_marca(d, W, H, ink)
    return base


def milestone(data, tema=None):
    """Póster A4 del PRIMER AÑO — REDISEÑO 10-jul-2026 (a Pablo no le gustaba el
    anillo monocromático): grilla de 12 POLAROIDS inclinadas con tira de mes,
    globito de número en el acento del tema y personajes del tema decorando.
    El cliente pega una foto por mes. Nombre automático del editor de compra."""
    import math
    W, H = A4
    acc = accent(tema); fnt = font_disp(tema); ink = ink_c(tema)
    nombre = (data.get("nombre") or "").strip()
    base = Image.new("RGBA", (W, H), (253, 250, 244, 255))
    d = ImageDraw.Draw(base)

    # confeti suave de fondo (nunca detrás de las fotos: solo en los bordes)
    import random as _r
    rnd = _r.Random(11)
    for _ in range(46):
        x = rnd.uniform(40, W - 40)
        y = rnd.choice([rnd.uniform(40, 120), rnd.uniform(H - 150, H - 60)])
        r = rnd.uniform(8, 22)
        d.ellipse([x - r, y - r, x + r, y + r], fill=_tint(acc, rnd.choice((0.55, 0.72, 0.86))) + (255,))

    titulo = ("El primer año de " + nombre) if nombre else "El primer año del bebé"
    txt(d, titulo, W / 2, 200, fnt, 120, acc, W * 0.84, wght=700)
    txt(d, "Pegá una foto de cada mes y mirá cuánto creció", W / 2, 330,
        "Fredoka-VF.ttf", 46, _tint(ink, 0.12), W * 0.76, wght=600)

    # personajes del tema en las esquinas superiores
    try:
        import cuaderno
        pjs = cuaderno.personajes_decorativos(tema or "safari", 2, incluir_objetos=True)
    except Exception:
        pjs = []
    for pj, (fx, fy) in zip(pjs, ((0.085, 0.055), (0.915, 0.055))):
        h2 = 250
        if pj.width * h2 / pj.height > 300:
            h2 = int(300 * pj.height / pj.width)
        w2 = max(1, int(pj.width * h2 / pj.height))
        base.alpha_composite(pj.resize((w2, h2), Image.LANCZOS),
                             (int(W * fx - w2 / 2), int(H * fy - h2 / 2)))
    d = ImageDraw.Draw(base)

    # ── grilla 3x4 de polaroids inclinadas ──
    cols, rows = 3, 4
    cw, ch = 640, 660                          # tarjeta (foto + tira del mes)
    gx = (W - cols * cw - (cols - 1) * 60) / 2
    gy = 440
    rowg = (H - gy - 180 - rows * ch) / (rows - 1) + ch
    tilts = [-2.4, 1.8, -1.6, 2.2, -2.0, 1.5, -2.2, 2.4, -1.5, 2.0, -2.5, 1.7]
    for i in range(12):
        r, c = divmod(i, cols)
        cx = gx + c * (cw + 60) + cw / 2
        cy = gy + r * rowg + ch / 2
        # tarjeta polaroid (dibujada aparte y rotada)
        card = Image.new("RGBA", (cw + 80, ch + 80), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([48, 52, 40 + cw + 8, 44 + ch + 8], 26,
                             fill=(0, 0, 0, 26))                       # sombra suave
        cd.rounded_rectangle([40, 40, 40 + cw, 40 + ch], 24,
                             fill=(255, 255, 255, 255), outline=_tint(acc, 0.45) + (255,), width=5)
        cd.rounded_rectangle([70, 70, 40 + cw - 30, 40 + ch - 150], 14,
                             fill=(244, 241, 235, 255), outline=_tint(acc, 0.75) + (255,), width=3)
        # esquinitas de álbum en la zona de la foto
        for ex, ey in ((92, 92), (40 + cw - 52, 92), (92, 40 + ch - 172), (40 + cw - 52, 40 + ch - 172)):
            cd.line([ex - 16, ey + 8, ex + 8, ey - 16], fill=_tint(acc, 0.5) + (255,), width=4)
        et = "1 mes" if i == 0 else "%d meses" % (i + 1)
        txt(cd, et, 40 + cw / 2, 40 + ch - 82, "Fredoka-VF.ttf", 52, ink, cw * 0.7, wght=700)
        card = card.rotate(tilts[i], expand=True, resample=Image.BICUBIC)
        base.alpha_composite(card, (int(cx - card.width / 2), int(cy - card.height / 2)))
        # globito con el número del mes (sin rotar: siempre legible)
        d = ImageDraw.Draw(base)
        bx, by = cx - cw / 2 + 26, cy - ch / 2 + 26
        d.ellipse([bx - 52, by - 52, bx + 52, by + 52], fill=acc + (255,),
                  outline=(255, 255, 255, 255), width=6)
        _num(d, str(i + 1), bx, by, fnt, 56, _tint(acc, 0.94), 72, wght=700)

    _pie_marca(d, W, H, ink)
    return base


# ---------------------------------------------------------------------------
# REGISTRO DE TIPOS
# ---------------------------------------------------------------------------
# Cada tipo: lista de (nombre_archivo, fn(data)->Image) construida sobre una temática.
_EXTRAS_POR_EDAD  = ["afiche", "topper", "topper_palito", "base_torta", "stickers",
                     "separadores", "etiqueta_botella", "cajita_sorpresa", "decoracion_sorbetes"]
_EXTRAS_UNIVERSAL = ["banderin", "etiquetas_multiuso", "wrappers_cupcakes", "tarjetas_agradecimiento"]

def _extras_dir(tema):
    d = specs_de(tema).get("invitacion", {}).get("_dir", "")
    return os.path.join(d, "extras") if d else ""

# Piezas que llevan texto personalizado al CUSTOMIZAR (el arte IA deja un espacio
# limpio; acá el motor escribe el texto). Reglas (bugs de la auditoría 7-jul-2026):
# - afiche: la IA SIEMPRE deja un recuadro limpio ABAJO para el nombre (así lo pide
#   su prompt en ia_kit/catalogo.py). Antes el overlay dibujaba el PRIMER campo del
#   spec ("¡Bienvenidos!", fijo, arriba) → el recuadro del nombre quedaba VACÍO.
#   Ahora dibuja los campos personalizados ({nombre}) DENTRO del recuadro real,
#   detectado por píxeles.
# - resto (banderín/cajita/tarjetas/sorbetes): las posiciones default (0.5/0.5)
#   escribían el texto centrado ENCIMA del arte (el banderín tapado por «¡FELIZ
#   CUMPLE ...!», la cajita con el texto cruzando los pliegues). Solo se escribe si
#   Pablo posicionó el campo en el editor (existe layouts/<pieza>.json del tema).
def _estilo_contraste(f):
    color = f.get("color", INK)
    c = tuple(color)[:3] if isinstance(color, (list, tuple)) and len(color) >= 3 else INK
    luma = 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
    f["color"] = c
    f["stroke"] = max(2, int(f.get("size", 120)) // 14)
    f["stroke_color"] = (40, 40, 40) if luma > 140 else (255, 255, 255)   # contorno contrastante
    return f

def _zona_limpia_abajo(img):
    """(cy, alto) relativos del INTERIOR del recuadro para el nombre que el prompt
    del afiche siempre pide dejar abajo. Heurística por píxeles: entre las franjas
    horizontales lisas del 40% inferior, el recuadro es la MÁS BAJA que NO toca el
    borde de la hoja (la que toca el borde es el margen de fondo bajo el recuadro;
    las de más arriba son fondo entre el arte y el recuadro — elegir «la más
    uniforme» caía justo ahí y el nombre quedaba flotando ARRIBA del recuadro).
    None si no hay franja utilizable (arte viejo sin recuadro)."""
    try:
        g = img.convert("L").resize((60, 84), Image.BILINEAR)
        px = g.load()
        filas = []
        for y in range(int(84 * 0.60), 84):
            vals = [px[x, y] for x in range(9, 51)]
            prom = sum(vals) / len(vals)
            var = sum((v - prom) ** 2 for v in vals) / len(vals)
            filas.append((y, var < 180))
        runs, actual = [], []
        for y, lisa in filas:
            if lisa:
                actual.append(y)
            else:
                if actual:
                    runs.append(actual)
                actual = []
        if actual:
            runs.append(actual)
        utiles = [r for r in runs if len(r) >= 5 and r[-1] < 83]  # ≥6% alto, sin tocar el borde
        if not utiles:
            return None
        mejor = utiles[-1]                                        # la más baja
        cy = (mejor[0] + mejor[-1] + 1) / 2 / 84
        alto = len(mejor) / 84
        return cy, alto
    except Exception:
        return None

def _campos_texto_extra(tema, base, img=None):
    """Campos de texto a escribir sobre el extra (con el layout del editor aplicado).
    Lista vacía si la pieza no debe llevar texto automático."""
    spec = specs_de(tema).get(base)
    if not spec or not spec.get("text"):
        return []
    efs = [dict(f) for f in _effective_texts(spec)]
    if base == "afiche":
        campos = [f for f in efs if "{nombre}" in (f.get("tpl") or "")]
        zona = _zona_limpia_abajo(img) if img is not None else None
        for f in campos:
            if zona:
                cy, alto = zona
                f["x"], f["y"], f["anchor"] = 0.5, cy, "mm"
                # tamaño y ancho acotados al recuadro real (en px de la pieza)
                f["size"] = min(int(f.get("size", 165)), max(48, int(alto * 0.62 * (img.height if img is not None else 2400))))
                f["maxw"] = min(float(f.get("maxw", 0.9)), 0.62)
            else:
                f["x"], f["y"], f["anchor"] = 0.5, 0.92, "mm"
                f["maxw"] = min(float(f.get("maxw", 0.9)), 0.62)
        return [_estilo_contraste(f) for f in campos]
    p = layout_file_path(base, tema)
    if p and os.path.exists(p):          # Pablo posicionó el texto en el editor
        return [_estilo_contraste(f) for f in efs]
    return []

def _overlay_texto(img, tema, base, d):
    """Escribe el texto personalizado sobre la pieza (si corresponde). Aplica también
    lo que el cliente movió/escribió en el editor de ESA pieza (d['_over'], del kit
    multi-pieza). Nunca rompe el kit."""
    over = d.get("_over") if isinstance(d.get("_over"), dict) else {}
    for campo in _campos_texto_extra(tema, base, img):
        o = over.get(campo.get("id")) if over else None
        incluido = isinstance(o, dict) and not o.get("hidden")
        if campo.get("default_hidden") and not incluido:
            continue                                  # apagado por default; solo si el cliente lo incluyó
        if isinstance(o, dict):
            if o.get("hidden"):
                continue                              # el cliente sacó este texto
            for k in ("x", "y", "size", "maxw", "wght"):
                if k in o:
                    try: campo[k] = float(o[k])
                    except (TypeError, ValueError): pass
            a = o.get("anchor")
            if isinstance(a, str) and len(a) == 2 and a[0] in "lmr" and a[1] in "tmb":
                campo["anchor"] = a
            if isinstance(o.get("font"), str) and o["font"] in _FONT_FILES:
                campo["font"] = o["font"]
            if isinstance(o.get("color"), str) and o["color"].startswith("#"):
                c = _hex_rgb(o["color"])
                if c: campo["color"] = c
            if isinstance(o.get("text"), str):
                campo["_text"] = o["text"]           # el texto que escribió el cliente
        try:
            draw_text(ImageDraw.Draw(img), campo, d, img.width, img.height)
        except Exception as e:
            print("[kit] overlay de texto falló en %s: %s" % (base, e))
    return img

def _mk_extra_edad(exdir, base, tema):
    def fn(d):
        # stickers: se vende la hoja RECOMPUESTA con troquel uniforme y línea
        # de corte (piezas.hoja_stickers, cacheada) — la hoja cruda de la IA
        # (contornos dispares) queda solo como fuente de recortes. Fallback a
        # la cruda si el tema no tiene recortes suficientes.
        if base == "stickers":
            try:
                h = piezas.hoja_stickers(tema)
                if h is not None:
                    return h
            except Exception:
                pass
        edad = _safe_edad(d.get("edad", "1"))   # C2: sin path traversal
        p = os.path.join(exdir, f"{base}_{edad}.png")
        if not os.path.exists(p):
            # Fallback a la edad MÁS CERCANA disponible (no siempre _1): el afiche
            # lleva el número de edad ilustrado en el arte — para edad 4 sin arte
            # propio, mostrar el 3 es menos absurdo que un 1 gigante (bug real).
            # La solución de fondo es generar el arte de esa edad (dash → ↺ afiche).
            import re as _re
            disp = []
            for f in os.listdir(exdir):
                m = _re.fullmatch(_re.escape(base) + r"_(\d+)\.png", f)
                if m:
                    disp.append(int(m.group(1)))
            try:
                e = int(edad)
            except ValueError:
                e = 1
            if disp:
                elegida = max((x for x in disp if x <= e), default=min(disp))
                p = os.path.join(exdir, f"{base}_{elegida}.png")
            else:
                p = os.path.join(exdir, f"{base}_1.png")
        return _overlay_texto(Image.open(p).convert("RGBA"), tema, base, d)
    return fn

def _mk_extra_fijo(p, tema, base):
    return lambda d: _overlay_texto(Image.open(p).convert("RGBA"), tema, base, d)

def _piezas_kit(tema):
    # Si el tema trae arte estático subido (temas/<tema>/extras/), el kit usa esos
    # diseños + la invitación PERSONALIZADA del motor. Si no, las 7 piezas genéricas.
    exdir = _extras_dir(tema)
    if exdir and os.path.isdir(exdir):
        s = specs_de(tema)
        out = [("01_invitacion", lambda d: render(d, s["invitacion"]), False)]
        n = 2
        for base in _EXTRAS_POR_EDAD:
            if os.path.exists(os.path.join(exdir, f"{base}_1.png")):
                out.append((f"{n:02d}_{base}", _mk_extra_edad(exdir, base, tema), True)); n += 1
        for base in _EXTRAS_UNIVERSAL:
            p = os.path.join(exdir, f"{base}.png")
            if os.path.exists(p):
                out.append((f"{n:02d}_{base}", _mk_extra_fijo(p, tema, base), True)); n += 1
        return out
    return piezas.piezas_de(tema)  # genérico (las 7), con sus is_rgba

def _piezas_invitacion(tema):
    s = specs_de(tema)
    return [("1_invitacion", lambda d: render(d, s["invitacion"]), False)]

def _piezas_cartel(tema):
    s = specs_de(tema)
    return [("1_cartel", lambda d: render(d, s["cartel"]), False)]

def _piezas_actividades(tema):
    return [("1_para_colorear", lambda d: colorear(d, tema), True),
            ("2_juegos", lambda d: juegos(d, tema), True)]

def _piezas_milestone(tema):
    return [("1_tarjetas_mes_a_mes", lambda d: milestone(d, tema), True)]

def _piezas_rutina(tema):
    import rutina
    return [("1_rutina_visual", lambda d: rutina.generar_rutina(d, tema), True)]

def _piezas_babyshower(tema):
    import baby_shower as bs
    # SIN nombre en ninguna hoja (Pablo 9-jul-2026): cada pieza usa su texto
    # genérico ("el bebé", "estamos esperando a nuestro bebé"...)
    return [("%d_%s" % (i + 1, key),
             (lambda k: (lambda d: bs.pieza(k, {**d, "nombre": ""}, tema)))(key), True)
            for i, (key, _l) in enumerate(bs.PIEZAS)]

def _piezas_certificado(tema):
    import certificado
    return [("1_certificado", lambda d: certificado.generar_certificado(d, tema), True)]

def _piezas_corona(tema):
    import corona
    return [("1_gorro", lambda d: corona.gorro(d, tema), True),
            ("2_corona", lambda d: corona.corona(d, tema), True)]

def _piezas_antifaces(tema):
    import antifaces
    return [("1_antifaz", lambda d: antifaces.antifaz_mariposa(d, tema), True),
            ("2_bigotes", lambda d: antifaces.bigotes(d, tema), True),
            ("3_lentes", lambda d: antifaces.lentes_fiesta(d, tema), True)]

def _piezas_menu(tema):
    import menu_infantil
    return [("1_menu", lambda d: menu_infantil.generar_menu(d, tema), True)]

def _piezas_rompecabezas(tema):
    import rompecabezas
    return [("1_rompecabezas", lambda d: rompecabezas.rompecabezas_nombre(d, tema), True),
            ("2_bandeja", lambda d: rompecabezas.bandeja(d, tema), True)]

def _piezas_capsula(tema):
    import capsula_tiempo
    return [("1_sobre", lambda d: capsula_tiempo.portada_sobre(d, tema), True),
            ("2_carta", lambda d: capsula_tiempo.hoja_carta(d, tema), True)]

def _piezas_video_invitacion(tema):
    import video_invitacion
    return [("1_video_invitacion", lambda d: video_invitacion.preview_frame(d, tema), False)]

def _piezas_fiesta_completa(tema):
    import invitacion_web
    def _libro_portada(d):
        import libro
        return libro.pagina_libro(0, d, tema)
    return [("1_invitacion_web", lambda d: invitacion_web.preview_mock(d, tema), False),
            ("2_invitacion", lambda d: render(d, specs_de(tema)["invitacion"]), False),
            ("3_libro_portada", _libro_portada, True),
            ("4_medalla_3d", lambda d: _stl3d_preview(tema, "medalla"), False)]

def _piezas_invitacion_web(tema):
    import invitacion_web
    return [("1_invitacion_web", lambda d: invitacion_web.preview_mock(d, tema), False)]

def _piezas_actividades_web(tema):
    import actividades_web
    return [("1_actividades_web", lambda d: actividades_web.preview_mock(d, tema), False)]

def _piezas_rompecabezas_web(tema):
    import rompecabezas_web
    return [("1_rompecabezas_web", lambda d: rompecabezas_web.preview_mock(d, tema), False)]

def _piezas_libro(tema):
    import libro
    n_hist = libro.paginas_historia(tema)
    nombres = (["01_portada", "02_dedicatoria"] +
               ["%02d_pagina_%d" % (i + 3, i + 1) for i in range(n_hist)] +
               ["%02d_fin" % (n_hist + 3)])
    return [(n, (lambda i: (lambda d: libro.pagina_libro(i, d, tema)))(i), True)
            for i, n in enumerate(nombres)]

_MESES_NOMBRE = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
                 "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def _piezas_calendario(tema):
    """Calendario TEMÁTICO (no personalizado): 12 meses con el fondo/arte que
    arma Pablo por temática (temas/<tema>/calendario/{fondo.png,layout.json}) +
    la grilla de días que dibuja el motor encima. Sin nombre ni año a elección
    del cliente — el año lo fija el layout.json de cada tema."""
    import calendario
    acc = calendario._accent(tema)
    return [("%02d_%s" % (m, _MESES_NOMBRE[m - 1]),
             (lambda m: (lambda d: calendario.mes_hoja(m, 2026, acc, tema)))(m), True)
            for m in range(1, 13)]

def _piezas_papertoys(tema):
    import papertoys
    return [("1_cubo", lambda d: papertoys.cubo_personalizado(d, tema), True)]

def _piezas_memoria(tema):
    import memoria
    return [("1_cartas_memoria", lambda d: memoria.generar_memoria(d, tema), True),
            ("2_dorso", lambda d: memoria.dorso_memoria(d, tema), True)]


def _piezas_mandalas(tema):
    """Kit de mándalas para pintar: portada (personalizable con nombre) + 6 mándalas
    de dificultad creciente + hoja 'cómo imprimir'. 100% procedural (tema no afecta el
    line-art B/N; queda como eje para la Fase 2 con arte IA)."""
    return _piezas_mandalas_kit(None)(tema)


def _piezas_mandalas_kit(kit):
    """Factory: devuelve la función de piezas del kit de mándalas `kit` (None = original/chicos;
    'media'/'dificil'/'muydificil' = kits de adultos). portada + 10 mándalas + cómo imprimir."""
    def _piezas(tema):
        import mandalas
        out = [("00_portada", (lambda d: mandalas.portada(d, kit=kit)), False)]
        for i in range(1, mandalas.N_MANDALAS + 1):
            out.append(("%02d_mandala" % i,
                        (lambda k: (lambda d: mandalas.pagina(k, kit=kit)))(i), False))
        out.append(("%02d_como_imprimir" % (mandalas.N_MANDALAS + 1),
                    lambda d: mandalas.como_imprimir(d), False))
        return out
    return _piezas


# ── STL 3D (medalla/topper/trofeo/cortante/pack) ────────────────────────────
# Piezas generadas por código (OpenSCAD) desde el personaje del tema — sin STL de
# terceros, cero duda de licencia. La galería de la ficha usa un preview PNG
# CACHEADO en disco (con texto genérico "NOMBRE") para no recompilar OpenSCAD en
# cada vista; la descarga real de la compra sí genera con los datos del cliente
# (ver el branch especial en generar(), más abajo).

def _stl3d_cache_path(tema, pieza):
    import temas as _temas
    return os.path.join(_temas.TEMAS_DIR, tema, "stl3d_cache", pieza + ".png")

def _stl3d_preview(tema, pieza):
    """PIL Image del preview cacheado de una pieza STL para la temática. Genera y
    cachea en disco la primera vez que se pide (queda para todas las vistas futuras
    de esa temática, hasta que se borre el cache a mano)."""
    from PIL import Image as _Image
    path = _stl3d_cache_path(tema, pieza)
    if os.path.exists(path):
        return _Image.open(path).convert("RGB")
    import stl3d
    gen = {"medalla": stl3d.generar_medalla, "topper": stl3d.generar_topper,
           "trofeo": stl3d.generar_trofeo}[pieza]
    _, png_bytes = gen(tema, "NOMBRE", con_preview=True)
    import io as _io
    img = _Image.open(_io.BytesIO(png_bytes)).convert("RGB")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return img

def stl3d_muestra(tema, pieza):
    """Bytes del STL de MUESTRA de una pieza (texto genérico 'NOMBRE'), cacheado en
    disco — para el visor 3D de la ficha de la tienda (girar/zoom antes de comprar).
    La muestra es de baja resolución comercial: la compra real genera el propio."""
    import stl3d
    path = _stl3d_cache_path(tema, pieza + "_muestra").replace(".png", ".stl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    gen = {"medalla": lambda: stl3d.generar_medalla(tema, "NOMBRE")[0],
           "topper": lambda: stl3d.generar_topper(tema, "NOMBRE")[0],
           "trofeo": lambda: stl3d.generar_trofeo(tema, "NOMBRE")[0],
           "cortante": lambda: stl3d.generar_cortante(tema)[0]}
    if pieza not in gen:
        raise ValueError("pieza desconocida: %s" % pieza)
    data = gen[pieza]()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    return data

def _stl3d_preview_cortante(tema):
    path = _stl3d_cache_path(tema, "cortante")
    from PIL import Image as _Image
    if os.path.exists(path):
        return _Image.open(path).convert("RGB")
    import stl3d
    _, png_bytes = stl3d.generar_cortante(tema, con_preview=True)
    import io as _io
    img = _Image.open(_io.BytesIO(png_bytes)).convert("RGB")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return img

def _piezas_stl_medalla(tema):
    return [("1_medalla", lambda d: _stl3d_preview(tema, "medalla"), False)]

def _piezas_stl_topper(tema):
    return [("1_topper", lambda d: _stl3d_preview(tema, "topper"), False)]

def _piezas_stl_trofeo(tema):
    return [("1_trofeo", lambda d: _stl3d_preview(tema, "trofeo"), False)]

def _piezas_stl_cortante(tema):
    return [("1_cortante", lambda d: _stl3d_preview_cortante(tema), False)]

def _piezas_stl_pack(tema):
    return [("1_medalla", lambda d: _stl3d_preview(tema, "medalla"), False),
            ("2_topper", lambda d: _stl3d_preview(tema, "topper"), False),
            ("3_trofeo", lambda d: _stl3d_preview(tema, "trofeo"), False),
            ("4_cortante", lambda d: _stl3d_preview_cortante(tema), False)]


# campos = qué pedir en la ficha (la generación usa el superset igual).
_CAMPOS_FULL = ["nombre", "fecha", "hora", "lugar", "direccion", "telefono", "edad"]

TIPOS = {
    "kit": {
        "nombre": "Kit completo de cumpleaños",
        "descripcion": "Las 7 piezas: invitación, cartel, topper, cupcakes, etiquetas, tags y banderines.",
        "campos": _CAMPOS_FULL,
        "preview": "invitacion",
        "piezas": _piezas_kit,
    },
    "invitacion": {
        "nombre": "Invitación imprimible",
        "descripcion": "Solo la invitación personalizada en PDF, lista para imprimir o mandar por WhatsApp.",
        "campos": _CAMPOS_FULL,
        "preview": "invitacion",
        "piezas": _piezas_invitacion,
    },
    "cartel": {
        "nombre": "Cartel de bienvenida",
        "descripcion": "El afiche grande de bienvenida con el nombre, para imprimir en lona o papel.",
        "campos": ["nombre", "edad"],
        "preview": "cartel",
        "piezas": _piezas_cartel,
    },
    "actividades": {
        "nombre": "Pack de actividades",
        "descripcion": "Hoja para colorear + hoja de juegos, a juego con la temática.",
        "campos": ["nombre", "edad"],
        "preview": "actividades",
        "piezas": _piezas_actividades,
    },
    "milestone": {
        "nombre": "Tarjetas mes a mes",
        "descripcion": "12 tarjetas del bebé, de 1 mes a 12 meses, con el nombre y la temática.",
        "campos": ["nombre"],
        "preview": "milestone",
        "piezas": _piezas_milestone,
    },
    "rutina": {
        "nombre": "Rutina visual del niño",
        "descripcion": "Lámina A4 con la rutina de mañana y noche, personalizada con el nombre y la temática. Para imprimir y pegar en el cuarto.",
        "campos": ["nombre", "edad"],
        "preview": "rutina",
        "piezas": _piezas_rutina,
    },
    "babyshower": {
        "nombre": "Kit de Baby Shower",
        "descripcion": "6 piezas: invitación, juego «No digas bebé», predicciones, etiquetas, banderines y tarjeta para los 18. Temáticas pastel, personalizado con el nombre del bebé.",
        "campos": ["nombre", "fecha", "hora", "lugar", "direccion"],
        "preview": "babyshower",
        "piezas": _piezas_babyshower,
    },
    "certificado": {
        "nombre": "Certificado de cumpleañero",
        "descripcion": "Diploma oficial con el nombre y la edad, listo para imprimir y enmarcar.",
        "campos": ["nombre", "edad"],
        "preview": "certificado",
        "piezas": _piezas_certificado,
    },
    "corona": {
        "nombre": "Gorro y Corona de cumpleaños",
        "descripcion": "Gorro cónico + corona de rey para armar, recortar y pegar. Dos diseños en un mismo PDF.",
        "campos": ["nombre", "edad"],
        "preview": "corona",
        "piezas": _piezas_corona,
    },
    "antifaces": {
        "nombre": "Photo Booth Props",
        "descripcion": "Antifaz de mariposa, bigotes divertidos y lentes de fiesta para recortar y pegar en palitos. Ideal para fotos.",
        "campos": ["nombre"],
        "preview": "antifaces",
        "piezas": _piezas_antifaces,
    },
    "menu": {
        "nombre": "Menú infantil personalizado",
        "descripcion": "Menú del día con el nombre del cumpleañero, ideal para la mesa del salón. Para colorear.",
        "campos": ["nombre", "edad", "menu_entrada", "menu_plato", "menu_postre", "menu_bebida"],
        "campos_labels": {"menu_entrada": "Entrada", "menu_plato": "Plato principal",
                          "menu_postre": "Postre", "menu_bebida": "Bebida"},
        "preview": "menu",
        "piezas": _piezas_menu,
    },
    "rompecabezas": {
        # SIN nombre (rediseño 7-jul + pedido Pablo 11-jul-2026): es la imagen
        # completa del tema hecha puzzle — el nombre no aparece en ninguna
        # pieza, así que no se pide al comprar. La edad elige la grilla.
        "nombre": "Rompecabezas imprimible",
        "descripcion": "La escena de la temática hecha rompecabezas: piezas con encastres de verdad para recortar y armar, más la hoja-bandeja con la guía de las piezas y la imagen de referencia. La edad elige la cantidad de piezas (12 o 20).",
        "campos": ["edad"],
        "preview": "rompecabezas",
        "piezas": _piezas_rompecabezas,
    },
    "capsula": {
        "nombre": "Cápsula del Tiempo",
        "descripcion": "Carta para el futuro: sobre lacrado + hoja de preguntas para responder. Abrir en 5, 10 o 18 años.",
        "campos": ["nombre", "edad"],
        "preview": "capsula",
        "piezas": _piezas_capsula,
    },
    "libro-audio": {
        "nombre": "Audiolibro web narrado",
        "descripcion": "El cuento personalizado hecho EXPERIENCIA: una página web donde una voz cálida narra la historia (¡dice el nombre de tu peque!) y las hojas giran solas al ritmo del relato. Link para escuchar en cualquier pantalla, dura 1 año.",
        "campos": ["nombre", "edad", "genero", "historia", "voz", "dedicatoria"],
        "campos_labels": {"genero": "¿Nena o nene?", "historia": "¿Qué historia?",
                          "voz": "Voz del narrador", "dedicatoria": "Dedicatoria (opcional)"},
        "preview": "libro",
        "piezas": _piezas_libro,
    },
    "video-invitacion": {
        "nombre": "Video-invitación animada",
        "descripcion": "Video vertical de ~14 segundos con el nombre, la edad y los datos de la fiesta animados con la temática — listo para mandar por WhatsApp. La forma más canchera y económica de invitar.",
        "campos": ["nombre", "edad", "fecha", "hora", "lugar", "direccion"],
        "preview": "video-invitacion",
        "piezas": _piezas_video_invitacion,
    },
    "fiesta-completa": {
        "nombre": "Fiesta Completa — todo en uno",
        "descripcion": "TODO para el cumple en una sola compra: el kit imprimible completo + el libro de cuento personalizado + el pack de impresión 3D (medalla, topper, trofeo y cortante) + la invitación web interactiva con confirmación por WhatsApp. Precio de paquete (ahorrás ~30% vs comprar por separado).",
        "campos": ["nombre", "edad", "fecha", "hora", "lugar", "direccion", "telefono", "dedicatoria"],
        "campos_labels": {"fecha": "Fecha (DD/MM/AAAA para la cuenta regresiva)",
                          "telefono": "Tu WhatsApp (ahí llegan las confirmaciones)",
                          "dedicatoria": "Dedicatoria del libro (opcional)"},
        "preview": "fiesta-completa",
        "piezas": _piezas_fiesta_completa,
    },
    "invitacion-web": {
        "nombre": "Invitación web interactiva",
        "descripcion": "No es un PDF: es una PÁGINA para compartir por WhatsApp, con cuenta regresiva en vivo, botón «Cómo llegar» (Google Maps) y confirmación de asistencia directo a tu WhatsApp. Siempre actualizada: si cambia la hora o el lugar, el mismo link muestra la info nueva.",
        "campos": ["nombre", "edad", "fecha", "hora", "lugar", "direccion", "telefono"],
        "campos_labels": {"fecha": "Fecha (DD/MM/AAAA para la cuenta regresiva)",
                          "telefono": "Tu WhatsApp (ahí llegan las confirmaciones)"},
        "preview": "invitacion-web",
        "piezas": _piezas_invitacion_web,
    },
    "actividades-web": {
        "nombre": "Cuaderno de actividades interactivo (web)",
        "descripcion": "Las actividades del cuaderno, pero JUGABLES: una web con el nombre del peque donde pinta, juega al memotest, resuelve laberintos, sopas de letras, sumas y más — con corrección automática, estrellas y festejos. Los juegos se adaptan a la edad y se pueden jugar mil veces. Para celu, tablet o compu; link que dura años.",
        "campos": ["nombre", "edad"],
        "preview": "actividades-web",
        "piezas": _piezas_actividades_web,
    },
    "rompecabezas-web": {
        "nombre": "Rompecabezas interactivo (web)",
        "descripcion": "Los rompecabezas de la temática, pero JUGABLES: una web con el nombre del peque donde arma las escenas de su tema arrastrando piezas con encastres de verdad — con imán al encajar, estrellas y festejos. Varios rompecabezas y niveles según la edad; se pueden armar mil veces. Para celu, tablet o compu; link que dura años.",
        "campos": ["nombre", "edad"],
        "preview": "rompecabezas-web",
        "piezas": _piezas_rompecabezas_web,
    },
    "libro": {
        "nombre": "Libro de cuento personalizado",
        "descripcion": "Cuento de 10 páginas donde el chico es el protagonista: portada, dedicatoria, 7 páginas de aventura con la temática y final. Listo para imprimir como libro. Cada página puede llevar ilustración IA (override).",
        "campos": ["nombre", "edad", "dedicatoria"],
        "campos_labels": {"dedicatoria": "Dedicatoria (opcional)"},
        "preview": "libro",
        "piezas": _piezas_libro,
    },
    "libro-premium": {
        "nombre": "Libro de cuento premium — edición única",
        "descripcion": "El mismo cuento de 10 páginas, pero con TODAS las ilustraciones pintadas por IA especialmente para este pedido: cada libro es único e irrepetible. La generación tarda unos minutos; el link de descarga se activa solo al terminar.",
        "campos": ["nombre", "edad", "genero", "historia", "dedicatoria"],
        "campos_labels": {"genero": "¿Nena o nene?", "historia": "¿Qué historia?",
                          "dedicatoria": "Dedicatoria (opcional)"},
        "preview": "libro",
        "piezas": _piezas_libro,
    },
    "libro-pdf": {
        "nombre": "Libro de cuento imprimible (PDF, edición genérica)",
        "descripcion": "Libro de 20 páginas LISTO: historia fija con protagonista "
                       "propio (nada customizable), con el arte del catálogo de "
                       "audiolibros. PDF prearmado para imprimir — entrega inmediata.",
        "campos": [],
        "preview": "libro",
        "piezas": _piezas_libro,
    },
    "calendario": {
        "nombre": "Calendario temático",
        "descripcion": "12 meses ilustrados con la temática elegida. Listo, nada para completar.",
        "campos": [],
        "preview": "calendario",
        "piezas": _piezas_calendario,
    },
    "papertoys": {
        "nombre": "Paper Toys — Cubo 3D",
        "descripcion": "Cubo desplegable con las letras del nombre para recortar, doblar y armar.",
        "campos": ["nombre"],
        "preview": "papertoys",
        "piezas": _piezas_papertoys,
    },
    "memoria": {
        "nombre": "Juego de la Memoria",
        "descripcion": "24 cartas (12 pares) con emojis y dorsos decorados. Para recortar y jugar.",
        "campos": ["nombre"],
        "preview": "memoria",
        "piezas": _piezas_memoria,
    },
    "mandalas": {
        "nombre": "Kit de mándalas para pintar",
        "descripcion": "6 mándalas para colorear de fácil a difícil + guía de impresión. Line-art listo para imprimir en casa (A4 o Carta). La portada se personaliza con el nombre.",
        "campos": ["nombre"],
        "preview": "mandalas",
        "piezas": _piezas_mandalas,
    },
    "mandalas-media": {
        "nombre": "Mándalas para pintar — Nivel Medio (PDF + Web)",
        "descripcion": "10 mándalas de dificultad MEDIA (florales, geométricas, mehndi, naturaleza, estrella, celta, rosetón, plumas, celestial y encaje) para colorear. Incluye el PDF listo para imprimir en casa (A4/Carta, 300dpi) Y el acceso para pintarlas online desde el celu o la compu, sin imprimir nada.",
        "campos": ["nombre"],
        "preview": "mandalas-media",
        "piezas": _piezas_mandalas_kit("media"),
    },
    "mandalas-media-pdf": {
        "nombre": "Mándalas para pintar — Nivel Medio (solo PDF)",
        "descripcion": "10 mándalas de dificultad MEDIA (florales, geométricas, mehndi, naturaleza, estrella, celta, rosetón, plumas, celestial y encaje) para colorear. PDF listo para imprimir en casa (A4/Carta, 300dpi). Solo impresión — no incluye el acceso para pintar online (ver la versión PDF + Web).",
        "campos": ["nombre"],
        "preview": "mandalas-media",
        "piezas": _piezas_mandalas_kit("media"),
    },
    "mandalas-dificil": {
        "nombre": "Mándalas para pintar — Nivel Difícil (PDF + Web)",
        "descripcion": "10 mándalas DIFÍCILES (intrincadas, antiestrés) de estilos variados para colorear. Incluye el PDF listo para imprimir en casa (A4/Carta, 300dpi) Y el acceso para pintarlas online desde el celu o la compu, sin imprimir nada.",
        "campos": ["nombre"],
        "preview": "mandalas-dificil",
        "piezas": _piezas_mandalas_kit("dificil"),
    },
    "mandalas-dificil-pdf": {
        "nombre": "Mándalas para pintar — Nivel Difícil (solo PDF)",
        "descripcion": "10 mándalas DIFÍCILES (intrincadas, antiestrés) de estilos variados para colorear. PDF listo para imprimir en casa (A4/Carta, 300dpi). Solo impresión — no incluye el acceso para pintar online (ver la versión PDF + Web).",
        "campos": ["nombre"],
        "preview": "mandalas-dificil",
        "piezas": _piezas_mandalas_kit("dificil"),
    },
    "mandalas-muydificil": {
        "nombre": "Mándalas para pintar — Nivel Muy Difícil (PDF + Web)",
        "descripcion": "10 mándalas MUY DIFÍCILES (máximo detalle, antiestrés) de estilos variados para colorear. Incluye el PDF listo para imprimir en casa (A4/Carta, 300dpi) Y el acceso para pintarlas online desde el celu o la compu, sin imprimir nada.",
        "campos": ["nombre"],
        "preview": "mandalas-muydificil",
        "piezas": _piezas_mandalas_kit("muydificil"),
    },
    "mandalas-muydificil-pdf": {
        "nombre": "Mándalas para pintar — Nivel Muy Difícil (solo PDF)",
        "descripcion": "10 mándalas MUY DIFÍCILES (máximo detalle, antiestrés) de estilos variados para colorear. PDF listo para imprimir en casa (A4/Carta, 300dpi). Solo impresión — no incluye el acceso para pintar online (ver la versión PDF + Web).",
        "campos": ["nombre"],
        "preview": "mandalas-muydificil",
        "piezas": _piezas_mandalas_kit("muydificil"),
    },
    "stl-medalla": {
        "nombre": "Medalla 3D imprimible",
        "descripcion": "Medalla con el personaje del tema en relieve + nombre/edad grabado. Archivo STL para imprimir en 3D, generado 100% por código (sin diseños de terceros).",
        "campos": ["nombre", "edad"],
        "preview": "stl-medalla",
        "piezas": _piezas_stl_medalla,
    },
    "stl-topper": {
        "nombre": "Topper de torta 3D imprimible",
        "descripcion": "Silueta del personaje del tema + nombre y edad, con palito para la torta. Archivo STL para imprimir en 3D.",
        "campos": ["nombre", "edad"],
        "preview": "stl-topper",
        "piezas": _piezas_stl_topper,
    },
    "stl-trofeo": {
        "nombre": "Trofeo 3D imprimible",
        "descripcion": "Trofeo con el personaje del tema en relieve y placa grabada con nombre/edad o texto libre. Archivo STL para imprimir en 3D.",
        "campos": ["nombre", "edad"],
        "preview": "stl-trofeo",
        "piezas": _piezas_stl_trofeo,
    },
    "stl-cortante": {
        "nombre": "Cortante de galletitas 3D imprimible",
        "descripcion": "El contorno del personaje del tema convertido en cortante de masa, con asa para empujar. Sin personalización (es el mismo por temática). Archivo STL para imprimir en 3D.",
        "campos": [],
        "preview": "stl-cortante",
        "piezas": _piezas_stl_cortante,
    },
    "stl-pack": {
        "nombre": "Pack Cumple 3D",
        "descripcion": "Medalla + topper + trofeo (los 3 personalizados con nombre/edad) + cortante de galletitas del tema. Los 4 archivos STL en un ZIP, listos para imprimir.",
        "campos": ["nombre", "edad"],
        "preview": "stl-pack",
        "piezas": _piezas_stl_pack,
    },
}

DEFAULT_TIPO = "kit"


def existe_tipo(tipo):
    return (tipo or DEFAULT_TIPO) in TIPOS

def _spec(tipo):
    return TIPOS.get(tipo or DEFAULT_TIPO, TIPOS[DEFAULT_TIPO])

def campos_tipo(tipo):
    return list(_spec(tipo)["campos"])

def override_path(tema, tipo, idx):
    """Ruta de un reemplazo subido a mano para la pieza <idx> de <tipo> en <tema> (ej. una
    versión mejorada con IA de una pieza que hoy es 100% procedural). Si existe, se usa esa
    imagen en vez de la función procedural — ningún cambio de código, solo un archivo."""
    return os.path.join(temas.TEMAS_DIR, tema or "safari", "overrides", tipo, "%d.png" % idx)

def _con_overrides(tema, tipo, items):
    out = []
    for idx, (nombre, fn, is_rgba) in enumerate(items):
        ov = override_path(tema, tipo, idx)
        if os.path.isfile(ov):
            fn = (lambda p: (lambda d: Image.open(p).convert("RGBA")))(ov)
        out.append((nombre, fn, is_rgba))
    return out

def piezas_tipo(tema, tipo):
    """Lista [(nombre_archivo, fn(data)->Image, is_rgba)] del tipo sobre la temática.
    Aplica overrides subidos a mano (ver override_path) sobre el diseño procedural.
    EXCEPCIÓN 'libro'/'calendario': el override (mismo path) es solo el ARTE/fondo
    y lo aplica el propio motor (libro.py / calendario.py) adentro — el texto
    personalizado (nombre/dedicatoria/año) siempre lo escribe el motor; si el
    override tapara la pieza entera con una imagen ya renderizada, el nombre del
    cliente quedaría fijo (el de la última vez que se generó) dentro de la imagen
    subida, ignorando lo que cargue cada comprador. Bug real: pasó exactamente
    esto con calendario (el 'nombre' del cliente nunca llegaba a verse)."""
    items = _spec(tipo)["piezas"](tema or "safari")
    if tipo in ("libro", "libro-premium", "calendario"):
        return items
    return _con_overrides(tema, tipo, items)

_PIEZA_LABELS = {
    "1_invitacion": "Invitación", "2_cartel": "Cartel", "1_cartel": "Cartel",
    "3_topper_torta": "Topper de torta", "4_cupcake_toppers": "Cupcakes",
    "5_etiquetas_botellita": "Etiquetas", "6_tags_souvenir": "Tags souvenir",
    "7_banderines": "Banderines", "1_para_colorear": "Para colorear",
    "2_juegos": "Juegos", "1_tarjetas_mes_a_mes": "Póster primer año",
    "1_rutina_visual": "Rutina visual",
    "1_invitacion": "Invitación", "2_no_digas_bebe": "Juego: No digas «bebé»",
    "3_predicciones": "Predicciones", "4_etiquetas": "Etiquetas souvenir",
    "5_banderines": "Banderines",     "6_carta_18": "Tarjeta para los 18",
    "1_certificado": "Certificado",
    "1_gorro": "Gorro para armar",
    "2_corona": "Corona para armar",
    "1_antifaz": "Antifaz",
    "2_bigotes": "Bigotes divertidos",
    "3_lentes": "Lentes de fiesta",
    "1_menu": "Menú infantil",
    "1_rompecabezas": "Rompecabezas",
    "2_bandeja": "Bandeja para armar",
    "1_sobre": "Sobre lacrado",
    "2_carta": "Carta del futuro",
    "01_enero": "Enero", "02_febrero": "Febrero", "03_marzo": "Marzo",
    "04_abril": "Abril", "05_mayo": "Mayo", "06_junio": "Junio",
    "07_julio": "Julio", "08_agosto": "Agosto", "09_septiembre": "Septiembre",
    "10_octubre": "Octubre", "11_noviembre": "Noviembre", "12_diciembre": "Diciembre",
    "01_portada": "Portada", "02_dedicatoria": "Dedicatoria",
    "03_pagina_1": "Página 1", "04_pagina_2": "Página 2", "05_pagina_3": "Página 3",
    "06_pagina_4": "Página 4", "07_pagina_5": "Página 5", "08_pagina_6": "Página 6",
    "09_pagina_7": "Página 7", "10_fin": "Fin",
    "1_video_invitacion": "Video-invitación",
    "1_invitacion_web": "Invitación web interactiva", "2_invitacion": "Invitación del kit",
    "3_libro_portada": "Libro de cuento", "4_medalla_3d": "Medalla 3D",
    "1_cubo": "Cubo 3D para armar",
    "1_cartas_memoria": "Cartas del memory",
    "2_dorso": "Dorso de cartas",
    "00_portada": "Portada",
    "01_mandala": "Mándala 1", "02_mandala": "Mándala 2", "03_mandala": "Mándala 3",
    "04_mandala": "Mándala 4", "05_mandala": "Mándala 5", "06_mandala": "Mándala 6",
    "07_mandala": "Mándala 7", "08_mandala": "Mándala 8", "09_mandala": "Mándala 9",
    "10_mandala": "Mándala 10", "11_como_imprimir": "Cómo imprimir",
    # kits dinámicos por arte estática (extras/): nombres lindos para la galería
    "01_invitacion": "Invitación", "02_afiche": "Afiche del número",
    "03_topper": "Topper de torta", "04_stickers": "Stickers",
    "05_separadores": "Separadores", "06_etiqueta_botella": "Etiqueta de botella",
    "07_cajita_sorpresa": "Cajita sorpresa", "08_decoracion_sorbetes": "Decoración de sorbetes",
    "09_banderin": "Banderín", "10_etiquetas_multiuso": "Etiquetas multiuso",
    "11_wrappers_cupcakes": "Wrappers de cupcakes", "12_tarjetas_agradecimiento": "Tarjetas de agradecimiento",
}

def pieza_label(name):
    if name in _PIEZA_LABELS:
        return _PIEZA_LABELS[name]
    import re
    return re.sub(r"^\d+_", "", name).replace("_", " ").capitalize()

def piezas_nombres(tipo, tema="safari"):
    return [n for (n, _, _) in piezas_tipo(tema, tipo)]

# ─────────────────────────────────────────────────────────────────────────────
# BASE DE PERSONALIZACIÓN (Pablo, 10-jul-2026): qué imágenes CAMBIAN cuando el
# cliente configura el editor de compra. "*" = todas las piezas del tipo; los
# valores son los CAMPOS que las afectan. Todo lo que figura acá se GRABA en el
# momento de la compra (el motor lo renderiza con los datos del comprador) — y
# el dash avisa antes de pisar una de estas piezas con un override fijo (eso
# congelaría el texto para todos los compradores, bug real del calendario).
PERSONALIZADAS = {
    "kit":            {"*": ["nombre", "edad", "fecha", "hora", "lugar", "direccion", "telefono"]},
    "invitacion":     {"*": ["nombre", "edad", "fecha", "hora", "lugar", "direccion", "telefono"]},
    "cartel":         {"*": ["nombre", "edad"]},
    "fiesta-completa": {"*": ["nombre", "edad", "fecha", "hora", "lugar", "direccion", "telefono"]},
    "actividades":    {"*": ["nombre", "edad"]},          # portada, consignas y diploma
    "certificado":    {"*": ["nombre", "edad"]},
    "corona":         {"*": ["edad"]},                    # la edad elige el TALLE
    "menu":           {"*": ["menu_entrada", "menu_plato", "menu_postre", "menu_bebida"]},
    "rompecabezas":   {"*": ["edad"]},                    # la edad elige la grilla
    "capsula":        {"*": ["edad"]},                    # destino "tus 18 años"
    "libro":          {"*": ["nombre", "edad", "dedicatoria"]},
    "libro-premium":  {"*": ["nombre", "edad", "genero", "historia", "dedicatoria"]},
    # libro-pdf y calendario: el editor no captura campos propios (se entregan
    # ya armados / el calendario lo cura Pablo a mano)
    "rutina":         {"*": ["nombre", "edad"]},
    "milestone":      {"*": ["nombre"]},
    "video-invitacion": {"*": ["nombre", "edad", "fecha", "hora", "lugar"]},
    "invitacion-web": {"*": ["nombre", "edad", "fecha", "hora", "lugar", "direccion"]},
    "actividades-web": {"*": ["nombre", "edad"]},
    "rompecabezas-web": {"*": ["nombre", "edad"]},
    "mandalas":        {"00_portada": ["nombre"]},   # solo la portada usa el nombre; las mándalas son fijas
    "mandalas-media":         {"00_portada": ["nombre"]},
    "mandalas-media-pdf":     {"00_portada": ["nombre"]},
    "mandalas-dificil":       {"00_portada": ["nombre"]},
    "mandalas-dificil-pdf":   {"00_portada": ["nombre"]},
    "mandalas-muydificil":    {"00_portada": ["nombre"]},
    "mandalas-muydificil-pdf": {"00_portada": ["nombre"]},
    # FIJAS (sin datos del comprador): antifaces, memoria, papertoys, babyshower
}


def campos_de_pieza(tipo, nombre_pieza=None):
    """Campos del editor que afectan a una pieza (lista vacía = pieza FIJA)."""
    m = PERSONALIZADAS.get(tipo) or {}
    if nombre_pieza and nombre_pieza in m:
        return list(m[nombre_pieza])
    return list(m.get("*", []))


def piezas_meta(tipo, tema="safari", incluir_soluciones=False):
    """Lista [{idx, nombre, label}] de las piezas de un tipo/tema (para la galería de la ficha).
    El tema importa: los kits con arte estática (extras/) tienen piezas distintas por tema."""
    if tipo == "actividades":
        try:
            import cuaderno
            idxs = cuaderno.galeria_indices(tema, "6", incluir_soluciones=incluir_soluciones)
            if idxs:
                cut = len(cuaderno.base_paginas(tema, "6")) - cuaderno._n_sol(tema, "6")
                return [{"idx": ci, "nombre": "p%02d" % ci,
                         "label": ("Soluciones" if ci >= cut else "Página %d" % (n + 1)),
                         "personaliza": campos_de_pieza(tipo)}
                        for n, ci in enumerate(idxs)]
        except Exception:
            pass
    return [{"idx": i, "nombre": n, "label": pieza_label(n),
             "personaliza": campos_de_pieza(tipo, n)}
            for i, n in enumerate(piezas_nombres(tipo, tema))]

def tipos_publicos():
    """Para el endpoint /tipos: metadata sin las funciones."""
    return {k: {"nombre": v["nombre"], "descripcion": v["descripcion"],
                "campos": v["campos"], "campos_labels": v.get("campos_labels", {}),
                "preview": v["preview"], "piezas": piezas_meta(k)}
            for k, v in TIPOS.items()}


# ---------------------------------------------------------------------------
# GENERACIÓN + PREVIEW por tipo
# ---------------------------------------------------------------------------
def _aplicar_por_pieza(items, porp):
    """Kit multi-pieza: cada pieza se renderiza con SU propio 'over' (lo que el cliente
    editó en esa pieza en el editor). Mapea el nombre 'NN_<pieza>' -> porp[<pieza>].
    Las piezas que el cliente no tocó quedan igual (usan el over global de la invitación)."""
    out = []
    for (nombre, fn, rgba) in items:
        pz = nombre.split("_", 1)[1] if "_" in nombre else nombre
        ov = porp.get(pz)
        if isinstance(ov, dict):
            def _mk(_fn, _ov):
                def _f(d):
                    d2 = dict(d); d2["_over"] = _ov
                    return _fn(d2)
                return _f
            fn = _mk(fn, ov)
        out.append((nombre, fn, rgba))
    return out


def generar(data, dest_dir, tema="safari", tipo=DEFAULT_TIPO):
    """Genera las piezas del TIPO en PDF (300 DPI) y las empaqueta en un ZIP.

    Reusa piezas.generar_kit (genérico sobre una lista de piezas)."""
    if tipo == "video-invitacion":
        import zipfile, video_invitacion
        os.makedirs(dest_dir, exist_ok=True)
        mp4 = os.path.join(dest_dir, "invitacion.mp4")
        video_invitacion.generar_video(data, tema, mp4)
        zip_path = os.path.join(dest_dir, "kit.zip")
        with zipfile.ZipFile(zip_path, "w") as z:   # mp4 ya comprimido: sin deflate
            z.write(mp4, "video_invitacion.mp4")
        return zip_path
    if tipo == "fiesta-completa":
        # Bundle: arma el ZIP con las 3 partes descargables + portada con link/QR
        # de la invitación web (que se crea acá — es una página, no un archivo).
        import bundle_fiesta, invitacion_web
        base = (data.pop("_base_url", "") or os.environ.get(
            "CT3D_BASE_URL", "https://kit.casatridimensional.com.ar")).rstrip("/")
        tok = invitacion_web.crear(data, tema)
        return bundle_fiesta.generar_bundle(data, dest_dir, tema, f"{base}/i/{tok}")
    if tipo in ("stl-medalla", "stl-topper", "stl-trofeo", "stl-cortante", "stl-pack"):
        # Piezas 3D (STL) — no son imágenes, así que no pasan por piezas.generar_kit.
        # Acá SÍ se genera con los datos reales del cliente (la galería de la ficha
        # usa un preview cacheado con texto genérico, ver _stl3d_preview arriba).
        import stl3d, zipfile
        os.makedirs(dest_dir, exist_ok=True)
        nombre = str(data.get("nombre") or "").strip() or "Cumple"
        edad = str(data.get("edad") or "").strip()
        texto = f"{nombre.upper()} {edad}".strip() if edad else nombre.upper()
        zip_path = os.path.join(dest_dir, "kit.zip")  # mismo nombre que el resto: /descarga lo busca así
        if tipo == "stl-pack":
            with open(zip_path, "wb") as f:
                f.write(stl3d.generar_pack_cumple(tema, nombre, edad))
            return zip_path
        gen = {"stl-medalla": ("medalla.stl", lambda: stl3d.generar_medalla(tema, texto)[0]),
               "stl-topper": ("topper.stl", lambda: stl3d.generar_topper(tema, texto)[0]),
               "stl-trofeo": ("trofeo.stl", lambda: stl3d.generar_trofeo(tema, texto)[0]),
               "stl-cortante": ("cortante.stl", lambda: stl3d.generar_cortante(tema)[0])}
        nombre_archivo, fn = gen[tipo]
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr(nombre_archivo, fn())
        return zip_path
    if tipo == "calendario":
        # Entrega final: 2 meses por hoja (ahorra papel al imprimir). La galería
        # de administración sigue mostrando los 12 meses por separado (ver
        # piezas_tipo/_piezas_calendario, sin tocar) — esto solo cambia el
        # empaquetado del PDF/ZIP que recibe el cliente.
        import calendario as _cal
        piezas12 = piezas_tipo(tema, tipo)
        combinadas = []
        for i in range(0, 12, 2):
            n1, fn1, _ = piezas12[i]
            n2, fn2, _ = piezas12[i + 1]
            hoja = (lambda fn1, fn2: (lambda d: _cal.dos_meses_por_hoja(fn1(d), fn2(d))))(fn1, fn2)
            combinadas.append(("%02d_%s-%s" % (i // 2 + 1, n1[3:], n2[3:]), hoja, True))
        return piezas.generar_kit(data, dest_dir, tema, piezas_list=combinadas)
    if tipo == "actividades":
        # Cuaderno de actividades por edad (cuaderno.py): páginas verificadas por
        # código + arte del tema. Cada página entra como una pieza pre-renderizada.
        try:
            import cuaderno
            edad = str(data.get("edad") or "6")
            pgs = cuaderno.paginas_finales(tema, edad,
                                           nombre=str(data.get("nombre") or "").strip())
            if pgs:
                pl = [("%02d_cuaderno" % (i + 1), (lambda im: (lambda d: im))(p), False)
                      for i, p in enumerate(pgs)]
                return piezas.generar_kit(data, dest_dir, tema, piezas_list=pl)
        except Exception as e:
            import logging
            logging.getLogger("productos").warning("cuaderno actividades falló (%s); uso piezas viejas", e)
    items = piezas_tipo(tema, tipo)
    porp = data.get("_porPieza")                 # kit multi-pieza: over por pieza
    if isinstance(porp, dict) and porp:
        items = _aplicar_por_pieza(items, porp)
    return piezas.generar_kit(data, dest_dir, tema, piezas_list=items)


def preview(data, tema="safari", tipo=DEFAULT_TIPO, max_px=1000):
    """PNG chico de la pieza de vista previa del tipo (sin marca de agua)."""
    pieza = _spec(tipo)["preview"]
    if pieza == "invitacion":
        img = render(data, specs_de(tema)["invitacion"])
    elif pieza == "cartel":
        img = render(data, specs_de(tema)["cartel"])
    elif pieza == "actividades":
        try:
            import cuaderno
            img = cuaderno.pagina_efectiva(tema, "6", 0) or colorear(data, tema)
        except Exception:
            img = colorear(data, tema)
    elif pieza == "milestone":
        img = milestone(data, tema)
    elif pieza == "rutina":
        import rutina
        img = rutina.generar_rutina(data, tema)
    elif pieza == "babyshower":
        import baby_shower as bs
        img = bs.pieza("invitacion", data, tema)
    elif pieza in ("certificado", "corona", "antifaces", "menu", "rompecabezas",
                  "capsula", "libro", "calendario", "papertoys", "memoria", "mandalas",
                  "mandalas-media", "mandalas-dificil", "mandalas-muydificil",
                  "invitacion-web", "actividades-web", "rompecabezas-web",
                  "fiesta-completa", "video-invitacion",
                  "stl-medalla", "stl-topper", "stl-trofeo", "stl-cortante", "stl-pack"):
        # 100% procedurales: pasan por piezas_tipo() para que un override subido a mano
        # (ver override_path) se refleje también en la miniatura del producto.
        img = piezas_tipo(tema, pieza)[0][1](data)
    else:
        img = render(data, specs_de(tema)["invitacion"])
    img = piezas.to_rgb(img) if img.mode == "RGBA" else img
    img.thumbnail((max_px, max_px), Image.LANCZOS)
    return img


def preview_pieza(data, tema, tipo, idx, max_px=900):
    """Vista previa de UNA pieza específica del tipo (para la galería 'qué trae el ZIP')."""
    if tipo == "actividades":
        try:
            import cuaderno
            img = cuaderno.pagina_efectiva(tema, "6", int(idx))
            if img is not None:
                img = img.copy(); img.thumbnail((max_px, max_px), Image.LANCZOS)
                return img
        except Exception:
            pass
    items = piezas_tipo(tema, tipo)
    if not items:
        return None
    idx = max(0, min(len(items) - 1, int(idx)))
    img = items[idx][1](data)
    img = piezas.to_rgb(img) if img.mode == "RGBA" else img
    img.thumbnail((max_px, max_px), Image.LANCZOS)
    return img
