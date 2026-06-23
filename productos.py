#!/usr/bin/env python3
"""Registro de TIPOS de producto digital + piezas nuevas.

El motor pasó de generar un solo producto (el kit de 7 piezas) a un catálogo
data-driven: cada `tipo` declara qué piezas arma, qué campos pide y qué pieza
usar de vista previa. El pipeline de compra/pago/entrega de la tienda no cambia:
solo viaja un `tipo` extra.

Tipos:
- kit         → las 7 piezas (comportamiento histórico, default).
- invitacion  → solo la invitación (1 PDF).
- cartel      → solo el cartel/afiche de bienvenida (1 PDF).
- actividades → pack para imprimir: hoja "para colorear" + hoja de "juegos".
- milestone   → tarjetas mes a mes del bebé (1 mes … 12 meses).

Las piezas nuevas se arman 100% procedurales (Pillow), reutilizando la paleta y
tipografía de cada temática (bloque "kit" del tema.json). Sirven para las 9
temáticas sin arte nuevo.
"""
import os
from PIL import Image, ImageDraw

import piezas
from piezas import (A4, WHITE, CREAM, MUST, SAGE, make_sheet, txt, fit_into,
                    paste_center, accent, ink_c, font_disp, _band, animales,
                    load, has_recortes, _edad_any, lema, titulo)
from generador import render, specs_de, BROWN, OLIVE, TERRA

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
    """Póster A4 del PRIMER AÑO: número grande al centro + 12 marcos de foto REDONDOS
    (1..12 meses) en anillo. El cliente pega su foto de cada mes. Decoración por temática."""
    import math
    W, H = A4
    acc = accent(tema); fnt = font_disp(tema); ink = ink_c(tema)
    nombre = (data.get("nombre") or "").strip()
    base = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(base)
    _frame(d, W, H, acc)
    titulo = ("El primer año de " + nombre) if nombre else "El primer año del bebé"
    txt(d, titulo, W / 2, 248, fnt, 116, acc, W * 0.80, wght=700)
    txt(d, "Pegá la foto de cada mes", W / 2, 384, "Fredoka-VF.ttf", 48, _tint(ink, 0.12), W * 0.7, wght=600)

    cx, cy = W / 2, H * 0.595
    R_ring = W * 0.345          # radio del anillo
    r_f = int(W * 0.085)        # radio de cada marco de foto

    def marco(fx, fy, r, badge):
        # marco redondo: aro de acento + interior blanco (para pegar la foto) + filete fino
        d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=(255, 255, 255, 255),
                  outline=acc + (255,), width=max(6, int(r * 0.06)))
        ri = r - max(9, int(r * 0.085))
        d.ellipse([fx - ri, fy - ri, fx + ri, fy + ri], outline=_tint(acc, 0.5) + (255,), width=2)
        # badge del mes (círculo de acento en el borde inferior)
        bs = int(r * 0.5)
        by = fy + r
        d.ellipse([fx - bs, by - bs, fx + bs, by + bs], fill=acc + (255,))
        _num(d, badge, fx, by, fnt, bs * 1.25, _tint(acc, 0.92), bs * 1.7, wght=700)

    # 12 marcos en anillo (mes 1 arriba, en sentido horario)
    for i in range(12):
        ang = -math.pi / 2 + i * (2 * math.pi / 12)
        marco(cx + R_ring * math.cos(ang), cy + R_ring * math.sin(ang), r_f, str(i + 1))

    # centro: número grande del añito (decorativo, no es marco de foto)
    _num(d, "1", cx, cy - H * 0.012, fnt, int(W * 0.27), acc, W * 0.34, wght=700)
    txt(d, "AÑITO", cx, cy + H * 0.085, "Fredoka-VF.ttf", int(W * 0.05), ink, W * 0.34, wght=700)

    _pie_marca(d, W, H, ink)
    return base


# ---------------------------------------------------------------------------
# REGISTRO DE TIPOS
# ---------------------------------------------------------------------------
# Cada tipo: lista de (nombre_archivo, fn(data)->Image) construida sobre una temática.
def _piezas_kit(tema):
    return piezas.piezas_de(tema)  # las 7, con sus is_rgba

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
}

DEFAULT_TIPO = "kit"


def existe_tipo(tipo):
    return (tipo or DEFAULT_TIPO) in TIPOS

def _spec(tipo):
    return TIPOS.get(tipo or DEFAULT_TIPO, TIPOS[DEFAULT_TIPO])

def campos_tipo(tipo):
    return list(_spec(tipo)["campos"])

def piezas_tipo(tema, tipo):
    """Lista [(nombre_archivo, fn(data)->Image, is_rgba)] del tipo sobre la temática."""
    return _spec(tipo)["piezas"](tema or "safari")

_PIEZA_LABELS = {
    "1_invitacion": "Invitación", "2_cartel": "Cartel", "1_cartel": "Cartel",
    "3_topper_torta": "Topper de torta", "4_cupcake_toppers": "Cupcakes",
    "5_etiquetas_botellita": "Etiquetas", "6_tags_souvenir": "Tags souvenir",
    "7_banderines": "Banderines", "1_para_colorear": "Para colorear",
    "2_juegos": "Juegos", "1_tarjetas_mes_a_mes": "Póster primer año",
}

def pieza_label(name):
    if name in _PIEZA_LABELS:
        return _PIEZA_LABELS[name]
    import re
    return re.sub(r"^\d+_", "", name).replace("_", " ").capitalize()

def piezas_nombres(tipo, tema="safari"):
    return [n for (n, _, _) in piezas_tipo(tema, tipo)]

def piezas_meta(tipo):
    """Lista [{idx, nombre, label}] de las piezas de un tipo (para la galería de la ficha)."""
    return [{"idx": i, "nombre": n, "label": pieza_label(n)}
            for i, n in enumerate(piezas_nombres(tipo))]

def tipos_publicos():
    """Para el endpoint /tipos: metadata sin las funciones."""
    return {k: {"nombre": v["nombre"], "descripcion": v["descripcion"],
                "campos": v["campos"], "preview": v["preview"],
                "piezas": piezas_meta(k)}
            for k, v in TIPOS.items()}


# ---------------------------------------------------------------------------
# GENERACIÓN + PREVIEW por tipo
# ---------------------------------------------------------------------------
def generar(data, dest_dir, tema="safari", tipo=DEFAULT_TIPO):
    """Genera las piezas del TIPO en PDF (300 DPI) y las empaqueta en un ZIP.

    Reusa piezas.generar_kit (genérico sobre una lista de piezas)."""
    return piezas.generar_kit(data, dest_dir, tema, piezas_list=piezas_tipo(tema, tipo))


def preview(data, tema="safari", tipo=DEFAULT_TIPO, max_px=1000):
    """PNG chico de la pieza de vista previa del tipo (sin marca de agua)."""
    pieza = _spec(tipo)["preview"]
    if pieza == "invitacion":
        img = render(data, specs_de(tema)["invitacion"])
    elif pieza == "cartel":
        img = render(data, specs_de(tema)["cartel"])
    elif pieza == "actividades":
        img = colorear(data, tema)
    elif pieza == "milestone":
        img = milestone(data, tema)
    else:
        img = render(data, specs_de(tema)["invitacion"])
    img = img.convert("RGB") if img.mode == "RGBA" else img
    img.thumbnail((max_px, max_px), Image.LANCZOS)
    return img


def preview_pieza(data, tema, tipo, idx, max_px=900):
    """Vista previa de UNA pieza específica del tipo (para la galería 'qué trae el ZIP')."""
    items = piezas_tipo(tema, tipo)
    if not items:
        return None
    idx = max(0, min(len(items) - 1, int(idx)))
    img = items[idx][1](data)
    img = img.convert("RGB") if img.mode == "RGBA" else img
    img.thumbnail((max_px, max_px), Image.LANCZOS)
    return img
