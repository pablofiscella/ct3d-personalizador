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


def generar_certificado(data, tema="safari"):
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or "______________"
    edad = str(data.get("edad") or "").strip() or "_____"

    fondo = _fondo(tema)
    if fondo is not None:
        im = fondo.resize((WpH, HpH), Image.LANCZOS)
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

    # NOMBRE: el elemento más grande de la pieza (skill §10)
    nom_fs = 230
    while _font(nom_fs).getbbox(nombre)[2] > WpH * 0.62 and nom_fs > 80:
        nom_fs -= 6
    dr.text((cx, _mm(92)), nombre, font=_font(nom_fs), fill=acc, anchor="mm")
    # subrayado suave bajo el nombre
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
        dr.text((cx, HpH - _mm(9)), "casatridimensional.com.ar", font=_font(36, False),
                fill=(150, 148, 145), anchor="mm",
                stroke_width=5, stroke_fill=(255, 253, 246))
    else:
        # zona inferior: fecha + firma a la izquierda · roseta a la derecha
        yb = HpH - _mm(42)
        dr.line([WpH * 0.16, yb, WpH * 0.38, yb], fill=INK, width=4)
        dr.text((WpH * 0.27, yb + _mm(8)), "Firma del adulto a cargo de los abrazos",
                font=_font(40, False), fill=(150, 150, 160), anchor="mm")
        _roseta(dr, WpH * 0.72, yb - _mm(10), _mm(17), acc, GOLD)
        dr.text((cx, HpH - _mm(12)), "casatridimensional.com.ar", font=_font(36, False),
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
