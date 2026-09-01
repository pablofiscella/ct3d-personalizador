"""Certificado oficial de cumpleañero — diploma imprimible para enmarcar.

REDISEÑO 8-jul-2026 (skill armar-kit §10 — antes: la medalla pisaba el título,
el sello era un círculo vacío, muebles sobre la línea de firma, 150dpi → A5):
- A4 APAISADO a 300dpi (el formato clásico de diploma, entra en marco 8x10/A4).
- Fondo IA del tema (fondos_ia.py, pieza "certificado": orla decorada + centro
  claro) si existe; fallback procedural con doble orla.
- Jerarquía clásica: título → "otorgado a" → NOMBRE (lo más grande) → motivo →
  fecha + firma → sello/roseta dibujado con cintas, sin superposiciones.
- El texto SIEMPRE lo escribe el motor (nunca horneado en el arte)."""
import os, math, json, glob
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
_PXMM = 2480 / 210.0
WpH, HpH = 3508, 2480                # A4 APAISADO @300dpi
Wp, Hp = 2480, 3508                  # (referencia vertical, no se usa acá)
CREAM = (253, 250, 242)
GOLD = (212, 175, 55)
INK = (60, 50, 45)


def _mm(v):
    return v * _PXMM


def _text_tracked(dr, cx, cy, text, font, fill, tracking=0.05):
    """Como dr.text(anchor="mm") pero con tracking extra entre letras —
    encontrado 14-jul-2026 en el diploma de logro: Fredoka en MAYÚSCULAS
    junta tanto la I/V/I que "ACTIVIDADES" se leía "ACTMDADES". Sin esto en
    títulos/subtítulos en mayúsculas de este archivo."""
    gap = font.size * tracking
    widths = [font.getlength(ch) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        dr.text((x, cy), ch, font=font, fill=fill, anchor="lm")
        x += w + gap


# La tipografia se resuelve UNA vez por proceso, no en cada llamada (31-ago-2026).
#
# `glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True)` camina el arbol entero del
# proyecto — ~42.000 entradas — y estaba adentro de _font, o sea una vez por CADA
# pedido de letra. Medido con el motor caido: una hoja de calendario llama a _font 39
# veces y el glob se comia 6,9 de sus 7,3 segundos (95%). Como el arranque encola ~576
# hojas de warm, el motor quedaba al 143% de CPU sin completar NINGUN render (cero
# archivos escritos en 20 minutos) y /health no contestaba.
#
# El .ttf no se mueve mientras el proceso vive. Los dos candidatos que hay
# (fonts/ y web/fonts/) son el MISMO archivo (mismo md5), asi que ordenarlos no
# cambia cual gana; se ordena para que sea determinista. Si dos hilos entran a la vez
# el peor caso es que ambos globeen una vez: el resultado es el mismo, no hace falta lock.
_FREDOKA = None


def _fuentes_fredoka():
    global _FREDOKA
    if _FREDOKA is None:
        _FREDOKA = sorted(glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True))
    return _FREDOKA


def _font(sz, bold=True):
    for p in _fuentes_fredoka():
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


def _roseta(dr, cx, cy, r, col, gold):
    """Sello/roseta con cintas — abajo a la derecha, sin pisar nada."""
    # cintas
    for s in (-1, 1):
        dr.polygon([(cx + s * r * 0.25, cy + r * 0.5),
                    (cx + s * r * 0.9, cy + r * 2.1),
                    (cx + s * r * 0.35, cy + r * 1.75),
                    (cx + s * r * 0.05, cy + r * 2.25)], fill=col)
    # roseta dentada
    pts = []
    for i in range(24):
        a = i * math.pi / 12
        rr = r if i % 2 == 0 else r * 0.86
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    dr.polygon(pts, fill=gold)
    dr.ellipse([cx - r * 0.72, cy - r * 0.72, cx + r * 0.72, cy + r * 0.72],
               fill=CREAM, outline=col, width=6)
    # estrella central
    est = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r * 0.5 if i % 2 == 0 else r * 0.22
        est.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    dr.polygon(est, fill=col)


def _personajes(tema, n=1):
    try:
        import cuaderno
        return cuaderno.personajes_decorativos(tema, n)
    except Exception:
        return []


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


def _fondo(tema):
    try:
        import fondos_ia
        return fondos_ia.cargar_fondo(tema, "certificado")
    except Exception:
        return None


# El dominio que va al pie, POR MARCA (5-ago-2026).
#
# LO QUE PASABA: estaba escrito a mano como "casatridimensional.com.ar" en los cuatro pies
# de este archivo. O sea que un chico terminaba el cuaderno escolar de Kydo —tres estrellas
# en TODOS los juegos, que es un rato largo de trabajo— y el diploma que se ganaba, imprimía
# y mostraba en la casa llevaba la firma del negocio de las lámparas.
#
# Se vio generando el diploma de un cuaderno escolar real (`revision-1ro`, `escolar_on:
# True`) y mirando la imagen. No lo cazó ningún test: el diploma se renderiza EN VIVO cuando
# el player lo pide, así que no hay ningún archivo guardado donde se note.
#
# Sale de `escolar_on`, el mismo interruptor que ya decide el título de la pestaña, el
# favicon y la carpeta de lecciones. `data` ya lo trae —`certificado_logro` pasa
# `dict(reg)`— así que no hubo que cambiarle la firma a nadie: la marca ya estaba ahí,
# sólo que este archivo no la miraba.
DOMINIO_KYDO = "kydo.com.ar"
DOMINIO_TIENDA = "casatridimensional.com.ar"


def _dominio(data):
    """El dominio de la marca de ESTE cuaderno."""
    return DOMINIO_KYDO if (data or {}).get("escolar_on") else DOMINIO_TIENDA


def generar_certificado(data, tema="safari"):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "______________"
    edad = str(data.get("edad") or "").strip() or "_____"

    fondo = _fondo(tema)
    if fondo is not None:
        import fondos_ia
        im = fondos_ia.cover(fondo, WpH, HpH)
        dr = ImageDraw.Draw(im)
    else:
        im = Image.new("RGBA", (WpH, HpH), CREAM + (255,))
        dr = ImageDraw.Draw(im)
        dr.rounded_rectangle([_mm(8), _mm(8), WpH - _mm(8), HpH - _mm(8)], _mm(8),
                             outline=GOLD, width=12)
        dr.rounded_rectangle([_mm(13), _mm(13), WpH - _mm(13), HpH - _mm(13)], _mm(6),
                             outline=acc, width=6)
        pjs = _personajes(tema, 2)
        if pjs:
            spots = [(WpH * 0.11, HpH - _mm(42)), (WpH * 0.89, HpH - _mm(42))][:len(pjs)]
            for p, (sx, sy) in zip(pjs, spots):
                _paste_h(im, p, sx, sy, _mm(46))
            dr = ImageDraw.Draw(im)

    cx = WpH / 2
    dr.text((cx, _mm(34)), "CERTIFICADO", font=_font(150), fill=GOLD, anchor="mm")
    dr.text((cx, _mm(50)), "OFICIAL DE CUMPLEAÑERO", font=_font(70, False), fill=INK, anchor="mm")
    dr.text((cx, _mm(68)), "Se otorga el presente certificado a", font=_font(56, False),
            fill=_tint(INK, 0.2), anchor="mm")

    # NOMBRE: impreso AUTOMÁTICAMENTE desde el editor de compra (Pablo 9-jul-2026:
    # el cliente no escribe nada a mano — lo tipea una vez al personalizar y el
    # motor lo pone). Sin nombre cargado queda la línea para completar.
    nom_fs = 230
    while _font(nom_fs).getbbox(nombre)[2] > WpH * 0.62 and nom_fs > 80:
        nom_fs -= 6
    dr.text((cx, _mm(92)), nombre, font=_font(nom_fs), fill=acc, anchor="mm")
    nw = _font(nom_fs).getbbox(nombre)[2]
    dr.line([cx - nw / 2, _mm(107), cx + nw / 2, _mm(107)], fill=_tint(acc, 0.55), width=6)
    dr.text((cx, _mm(122)), "por cumplir %s años con alegría, juegos y mucha diversión" % edad,
            font=_font(58, False), fill=_tint(INK, 0.15), anchor="mm")

    if fondo is not None:
        # el arte IA trae personajes en las esquinas inferiores → la firma y la
        # roseta van DENTRO del centro limpio, no encima de los personajes
        yb = _mm(148)
        dr.line([WpH * 0.30, yb, WpH * 0.52, yb], fill=INK, width=4)
        dr.text((WpH * 0.41, yb + _mm(7)), "Firma del adulto a cargo de los abrazos",
                font=_font(40, False), fill=(140, 140, 150), anchor="mm")
        _roseta(dr, WpH * 0.63, yb - _mm(4), _mm(13), acc, GOLD)
        dr.text((cx, HpH - _mm(9)), _dominio(data), font=_font(36, False),
                fill=(150, 148, 145), anchor="mm",
                stroke_width=5, stroke_fill=(255, 253, 246))
    else:
        # zona inferior: fecha + firma a la izquierda · roseta a la derecha
        yb = HpH - _mm(42)
        dr.line([WpH * 0.16, yb, WpH * 0.38, yb], fill=INK, width=4)
        dr.text((WpH * 0.27, yb + _mm(8)), "Firma del adulto a cargo de los abrazos",
                font=_font(40, False), fill=(150, 150, 160), anchor="mm")
        _roseta(dr, WpH * 0.72, yb - _mm(10), _mm(17), acc, GOLD)
        dr.text((cx, HpH - _mm(12)), _dominio(data), font=_font(36, False),
                fill=(180, 180, 180), anchor="mm")
    return im


def generar_certificado_logro(data, tema="safari"):
    """Diploma de LOGRO — se gana jugando, no se compra (14-jul-2026, Pablo:
    "cuando algún peque haga todo el cuaderno de actividades interactivo sin
    errores que le agregue el certificado de esa actividad para que lo pueda
    imprimir"). Mismo estilo visual que generar_certificado (fondo IA, orlas,
    roseta) pero el motivo es la HAZAÑA (3 estrellas en TODOS los juegos del
    cuaderno), no el cumpleaños — por eso no lleva la edad."""
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "______________"

    fondo = _fondo(tema)
    if fondo is not None:
        import fondos_ia
        im = fondos_ia.cover(fondo, WpH, HpH)
        dr = ImageDraw.Draw(im)
    else:
        im = Image.new("RGBA", (WpH, HpH), CREAM + (255,))
        dr = ImageDraw.Draw(im)
        dr.rounded_rectangle([_mm(8), _mm(8), WpH - _mm(8), HpH - _mm(8)], _mm(8),
                             outline=GOLD, width=12)
        dr.rounded_rectangle([_mm(13), _mm(13), WpH - _mm(13), HpH - _mm(13)], _mm(6),
                             outline=acc, width=6)
        pjs = _personajes(tema, 2)
        if pjs:
            spots = [(WpH * 0.11, HpH - _mm(42)), (WpH * 0.89, HpH - _mm(42))][:len(pjs)]
            for p, (sx, sy) in zip(pjs, spots):
                _paste_h(im, p, sx, sy, _mm(46))
            dr = ImageDraw.Draw(im)

    cx = WpH / 2
    dr.text((cx, _mm(34)), "DIPLOMA DE CRACK", font=_font(150), fill=GOLD, anchor="mm")
    _text_tracked(dr, cx, _mm(50), "CUADERNO DE ACTIVIDADES COMPLETO", _font(60, False), INK)
    dr.text((cx, _mm(68)), "Se otorga el presente diploma a", font=_font(56, False),
            fill=_tint(INK, 0.2), anchor="mm")

    nom_fs = 230
    while _font(nom_fs).getbbox(nombre)[2] > WpH * 0.62 and nom_fs > 80:
        nom_fs -= 6
    dr.text((cx, _mm(92)), nombre, font=_font(nom_fs), fill=acc, anchor="mm")
    nw = _font(nom_fs).getbbox(nombre)[2]
    dr.line([cx - nw / 2, _mm(107), cx + nw / 2, _mm(107)], fill=_tint(acc, 0.55), width=6)
    dr.text((cx, _mm(122)), "por completar TODAS las actividades del cuaderno sin ningún error",
            font=_font(54, False), fill=_tint(INK, 0.15), anchor="mm")

    if fondo is not None:
        yb = _mm(148)
        dr.line([WpH * 0.30, yb, WpH * 0.52, yb], fill=INK, width=4)
        dr.text((WpH * 0.41, yb + _mm(7)), "Firma del adulto a cargo de los abrazos",
                font=_font(40, False), fill=(140, 140, 150), anchor="mm")
        _roseta(dr, WpH * 0.63, yb - _mm(4), _mm(13), acc, GOLD)
        dr.text((cx, HpH - _mm(9)), _dominio(data), font=_font(36, False),
                fill=(150, 148, 145), anchor="mm",
                stroke_width=5, stroke_fill=(255, 253, 246))
    else:
        yb = HpH - _mm(42)
        dr.line([WpH * 0.16, yb, WpH * 0.38, yb], fill=INK, width=4)
        dr.text((WpH * 0.27, yb + _mm(8)), "Firma del adulto a cargo de los abrazos",
                font=_font(40, False), fill=(150, 150, 160), anchor="mm")
        _roseta(dr, WpH * 0.72, yb - _mm(10), _mm(17), acc, GOLD)
        dr.text((cx, HpH - _mm(12)), _dominio(data), font=_font(36, False),
                fill=(180, 180, 180), anchor="mm")
    return im


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Valentina"
    edad = sys.argv[3] if len(sys.argv) > 3 else "4"
    out = sys.argv[4] if len(sys.argv) > 4 else "/tmp/certificado.png"
    generar_certificado({"nombre": nombre, "edad": edad}, tema).convert("RGB").save(out)
    print("OK ->", out)
