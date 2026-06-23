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
def _outline_text(d, text, cx, cy, font_file, size, maxw, wght=None, stroke=8):
    """Texto 'burbuja' (relleno claro + contorno) para que el chico lo pinte."""
    if not str(text).strip():
        return
    from generador import fit_font
    f = fit_font(d, str(text), font_file, int(size), int(maxw), wght)
    d.text((cx, cy), str(text), font=f, fill=(255, 255, 255),
           stroke_width=stroke, stroke_fill=INK, anchor="mm")


def colorear(data, tema=None):
    """Hoja A4 'para colorear': contornos simples (sin relleno) que el chico pinta."""
    W, H = A4
    base = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(base)
    nombre = (data.get("nombre") or "").strip()
    # título
    txt(d, "¡Para pintar!", W / 2, 230, font_disp(tema), 150, INK, W * 0.8)
    if nombre:
        _outline_text(d, nombre, W / 2, 560, font_disp(tema), 360, W * 0.8, wght=700, stroke=10)
    # globos (contorno)
    for i, (gx, gy, rr) in enumerate([(0.22, 0.42, 230), (0.5, 0.46, 270), (0.78, 0.42, 230)]):
        cx, cy = W * gx, H * gy
        d.ellipse([cx - rr, cy - rr * 1.2, cx + rr, cy + rr * 1.2], outline=INK, width=8)
        d.line([(cx, cy + rr * 1.2), (cx, cy + rr * 1.2 + 220)], fill=INK, width=6)
        d.polygon([(cx - 18, cy + rr * 1.2), (cx + 18, cy + rr * 1.2), (cx, cy + rr * 1.2 + 30)], outline=INK, width=4)
    # torta (contorno)
    cx, cy, cw_, ch_ = W * 0.5, H * 0.72, W * 0.34, H * 0.16
    d.rounded_rectangle([cx - cw_, cy, cx + cw_, cy + ch_], radius=40, outline=INK, width=8)
    d.rounded_rectangle([cx - cw_ * 0.7, cy - ch_ * 0.6, cx + cw_ * 0.7, cy], radius=30, outline=INK, width=8)
    for k in range(5):  # velitas
        vx = cx - cw_ * 0.5 + k * (cw_ / 4)
        d.line([(vx, cy - ch_ * 0.6), (vx, cy - ch_ * 1.05)], fill=INK, width=6)
        d.ellipse([vx - 14, cy - ch_ * 1.2, vx + 14, cy - ch_ * 1.05], outline=INK, width=5)
    # estrellas (contorno) decorando los bordes
    for sx, sy in [(0.12, 0.2), (0.88, 0.2), (0.1, 0.86), (0.9, 0.86)]:
        _estrella(d, W * sx, H * sy, 90, INK)
    return base


def _estrella(d, cx, cy, r, color, w=6):
    import math
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rad = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.line(pts + [pts[0]], fill=color, width=w, joint="curve")


def juegos(data, tema=None):
    """Hoja A4 de juegos: tatetí + uní los puntos (estrella) + caja para dibujar."""
    W, H = A4
    acc = accent(tema)
    base = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(base)
    nombre = (data.get("nombre") or "").strip()
    txt(d, "Juegos del cumple", W / 2, 220, font_disp(tema), 130, acc, W * 0.85, wght=700)
    if nombre:
        txt(d, "de " + nombre, W / 2, 380, "Fredoka-VF.ttf", 80, ink_c(tema), W * 0.8, wght=600)
    # --- Tatetí (3 grillas) ---
    txt(d, "Tatetí", W * 0.5, 560, "Fredoka-VF.ttf", 70, INK, W * 0.6, wght=600)
    g = int(W * 0.20)
    for j in range(3):
        ox = int(W * (0.13 + j * 0.27)); oy = 650
        for k in (1, 2):
            d.line([(ox + k * g / 3, oy), (ox + k * g / 3, oy + g)], fill=INK, width=6)
            d.line([(ox, oy + k * g / 3), (ox + g, oy + k * g / 3)], fill=INK, width=6)
    # --- Uní los puntos (estrella numerada) ---
    txt(d, "Uní los puntos", W * 0.5, int(H * 0.45), "Fredoka-VF.ttf", 70, INK, W * 0.7, wght=600)
    import math
    cx, cy, r = W * 0.5, H * 0.60, W * 0.22
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rad = r if k % 2 == 0 else r * 0.45
        px, py = cx + rad * math.cos(ang), cy + rad * math.sin(ang)
        d.ellipse([px - 12, py - 12, px + 12, py + 12], fill=INK)
        txt(d, str(k + 1), px + 38, py - 38, "Poppins-Medium.ttf", 56, acc, 120)
    # --- Caja para dibujar ---
    txt(d, "Dibujá tu regalo soñado", W * 0.5, int(H * 0.80), "Fredoka-VF.ttf", 64, INK, W * 0.8, wght=600)
    d.rounded_rectangle([W * 0.14, H * 0.83, W * 0.86, H * 0.95], radius=40, outline=acc, width=8)
    return base


def milestone(data, tema=None):
    """Hoja A4 con 12 tarjetas mes a mes del bebé (1 mes … 12 meses)."""
    acc = accent(tema); fnt = font_disp(tema); ink = ink_c(tema)
    nombre = (data.get("nombre") or "").strip()
    band = _band(tema)

    def cell(i, cw, ch):
        if i >= 12:
            return None
        c = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        d = ImageDraw.Draw(c)
        d.rounded_rectangle([6, 6, cw - 6, ch - 6], radius=40, fill=CREAM + (255,),
                            outline=acc + (255,), width=8)
        mes = i + 1
        txt(d, str(mes), cw / 2, ch * 0.30, fnt, ch * 0.36, acc, cw * 0.6, wght=700)
        txt(d, "mes" + ("es" if mes > 1 else ""), cw / 2, ch * 0.52,
            "Fredoka-VF.ttf", ch * 0.11, ink, cw * 0.7, wght=600)
        if nombre:
            txt(d, nombre, cw / 2, ch * 0.70, fnt, ch * 0.15, acc, cw * 0.84, wght=700)
        # franja temática (sirve para las 9 temáticas, sin arte nuevo)
        strip = fit_into(band, int(cw * 0.7), int(ch * 0.16))
        paste_center(c, strip, cw / 2, ch * 0.88)
        return c
    return make_sheet(cell, 3, 4, gap=45)


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

def tipos_publicos():
    """Para el endpoint /tipos: metadata sin las funciones."""
    return {k: {"nombre": v["nombre"], "descripcion": v["descripcion"],
                "campos": v["campos"], "preview": v["preview"]}
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
