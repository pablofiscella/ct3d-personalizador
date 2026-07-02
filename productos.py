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
from generador import render, specs_de, draw_text, _effective_texts, BROWN, OLIVE, TERRA, _safe_edad

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
_EXTRAS_POR_EDAD  = ["afiche", "topper", "topper_palito", "base_torta", "stickers",
                     "separadores", "etiqueta_botella", "cajita_sorpresa", "decoracion_sorbetes"]
_EXTRAS_UNIVERSAL = ["banderin", "etiquetas_multiuso", "wrappers_cupcakes", "tarjetas_agradecimiento"]

def _extras_dir(tema):
    d = specs_de(tema).get("invitacion", {}).get("_dir", "")
    return os.path.join(d, "extras") if d else ""

# Piezas que llevan texto personalizado al CUSTOMIZAR (el arte IA deja un espacio
# limpio; acá el motor escribe el texto, con la fuente/color del nombre de la invitación).
# Por ahora SOLO el afiche lleva texto automático (la IA hace un recuadro abajo de forma
# confiable y el nombre entra ahí). Las demás piezas con texto van por EDITOR (posición/
# tamaño manual), pendiente. Texto del afiche chico para no tocar los bordes del recuadro.
def _campo_texto_extra(tema, base):
    """Campo de texto del extra desde su SPEC (con el layout que guardó el editor, vía
    _effective_texts). Devuelve None si la pieza no lleva texto. Suma contorno contrastante
    para que se lea sobre cualquier fondo."""
    spec = specs_de(tema).get(base)
    if not spec or not spec.get("text"):
        return None
    f = dict(_effective_texts(spec)[0])   # campo "nombre" con el layout aplicado
    color = f.get("color", INK)
    c = tuple(color)[:3] if isinstance(color, (list, tuple)) and len(color) >= 3 else INK
    luma = 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
    f["color"] = c
    f["stroke"] = max(2, int(f.get("size", 120)) // 14)
    f["stroke_color"] = (40, 40, 40) if luma > 140 else (255, 255, 255)   # contorno contrastante
    return f

def _overlay_texto(img, tema, base, d):
    """Escribe el texto personalizado sobre la pieza (si corresponde). Nunca rompe el kit."""
    campo = _campo_texto_extra(tema, base)
    if not campo:
        return img
    try:
        draw_text(ImageDraw.Draw(img), campo, d, img.width, img.height)
    except Exception as e:
        print("[kit] overlay de texto falló en %s: %s" % (base, e))
    return img

def _mk_extra_edad(exdir, base, tema):
    def fn(d):
        edad = _safe_edad(d.get("edad", "1"))   # C2: sin path traversal
        p = os.path.join(exdir, f"{base}_{edad}.png")
        if not os.path.exists(p):
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
    return [("%d_%s" % (i + 1, key), (lambda k: (lambda d: bs.pieza(k, d, tema)))(key), True)
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
    return [("1_rompecabezas", lambda d: rompecabezas.rompecabezas_nombre(d, tema), True)]

def _piezas_capsula(tema):
    import capsula_tiempo
    return [("1_sobre", lambda d: capsula_tiempo.portada_sobre(d, tema), True),
            ("2_carta", lambda d: capsula_tiempo.hoja_carta(d, tema), True)]

def _piezas_calendario(tema):
    import calendario
    return [("01_enero", lambda d: calendario.mes_hoja(1, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True),
            ("02_febrero", lambda d: calendario.mes_hoja(2, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True),
            ("03_marzo", lambda d: calendario.mes_hoja(3, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True),
            ("04_abril", lambda d: calendario.mes_hoja(4, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True),
            ("05_mayo", lambda d: calendario.mes_hoja(5, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True),
            ("06_junio", lambda d: calendario.mes_hoja(6, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True),
            ("07_julio", lambda d: calendario.mes_hoja(7, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True),
            ("08_agosto", lambda d: calendario.mes_hoja(8, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True),
            ("09_septiembre", lambda d: calendario.mes_hoja(9, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True),
            ("10_octubre", lambda d: calendario.mes_hoja(10, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True),
            ("11_noviembre", lambda d: calendario.mes_hoja(11, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True),
            ("12_diciembre", lambda d: calendario.mes_hoja(12, int(d.get("anyo") or "2026"), d.get("nombre") or "Mi familia", calendario._accent(tema), tema), True)]

def _piezas_papertoys(tema):
    import papertoys
    return [("1_cubo", lambda d: papertoys.cubo_personalizado(d, tema), True)]

def _piezas_memoria(tema):
    import memoria
    return [("1_cartas_memoria", lambda d: memoria.generar_memoria(d, tema), True),
            ("2_dorso", lambda d: memoria.dorso_memoria(d, tema), True)]


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
        "nombre": "Rompecabezas del nombre",
        "descripcion": "Hoja A4 con el nombre partido en piezas para recortar y armar. Incluye solución.",
        "campos": ["nombre", "edad"],
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
    "calendario": {
        "nombre": "Calendario personalizado",
        "descripcion": "12 meses con el nombre de la familia, decorado con la temática. Producto recurrente (cada año).",
        "campos": ["nombre", "anyo"],
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
    Aplica overrides subidos a mano (ver override_path) sobre el diseño procedural."""
    items = _spec(tipo)["piezas"](tema or "safari")
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
    "1_antifaz": "Antifaz mariposa",
    "2_bigotes": "Bigotes divertidos",
    "3_lentes": "Lentes de fiesta",
    "1_menu": "Menú infantil",
    "1_rompecabezas": "Rompecabezas",
    "1_sobre": "Sobre lacrado",
    "2_carta": "Carta del futuro",
    "01_enero": "Enero", "02_febrero": "Febrero", "03_marzo": "Marzo",
    "04_abril": "Abril", "05_mayo": "Mayo", "06_junio": "Junio",
    "07_julio": "Julio", "08_agosto": "Agosto", "09_septiembre": "Septiembre",
    "10_octubre": "Octubre", "11_noviembre": "Noviembre", "12_diciembre": "Diciembre",
    "1_cubo": "Cubo 3D para armar",
    "1_cartas_memoria": "Cartas del memory",
    "2_dorso": "Dorso de cartas",
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

def piezas_meta(tipo, tema="safari"):
    """Lista [{idx, nombre, label}] de las piezas de un tipo/tema (para la galería de la ficha).
    El tema importa: los kits con arte estática (extras/) tienen piezas distintas por tema."""
    if tipo == "actividades":
        try:
            import cuaderno
            idxs = cuaderno.galeria_indices(tema, "6")
            if idxs:
                return [{"idx": ci, "nombre": "p%02d" % ci, "label": "Página %d" % (n + 1)}
                        for n, ci in enumerate(idxs)]
        except Exception:
            pass
    return [{"idx": i, "nombre": n, "label": pieza_label(n)}
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
def generar(data, dest_dir, tema="safari", tipo=DEFAULT_TIPO):
    """Genera las piezas del TIPO en PDF (300 DPI) y las empaqueta en un ZIP.

    Reusa piezas.generar_kit (genérico sobre una lista de piezas)."""
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
    if tipo == "actividades":
        # Cuaderno de actividades por edad (cuaderno.py): páginas verificadas por
        # código + arte del tema. Cada página entra como una pieza pre-renderizada.
        try:
            import cuaderno
            edad = str(data.get("edad") or "6")
            pgs = cuaderno.paginas_finales(tema, edad)
            if pgs:
                pl = [("%02d_cuaderno" % (i + 1), (lambda im: (lambda d: im))(p), False)
                      for i, p in enumerate(pgs)]
                return piezas.generar_kit(data, dest_dir, tema, piezas_list=pl)
        except Exception as e:
            import logging
            logging.getLogger("productos").warning("cuaderno actividades falló (%s); uso piezas viejas", e)
    return piezas.generar_kit(data, dest_dir, tema, piezas_list=piezas_tipo(tema, tipo))


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
                  "capsula", "calendario", "papertoys", "memoria",
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
