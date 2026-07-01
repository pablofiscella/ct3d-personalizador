"""Calendario familiar personalizado — 12 meses con el nombre + temática.
Cada mes en una hoja A4 con grilla de días + decoración temática.
Producto recurrente (se vende todos los años)."""
import os, math, json, glob, calendar
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754
CREAM = (253, 250, 242)
INK = (60, 50, 45)


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

_MESES_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
_DIAS_ES = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]


def mes_hoja(mes, anyo, nombre, acc):
    """Genera una hoja A4 para un mes específico."""
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    dr.rectangle([0, 0, Wp, 200], fill=acc)
    dr.text((Wp / 2, 80), "%s %d" % (_MESES_ES[mes - 1], anyo), font=_font(64), fill="white", anchor="mm")
    dr.text((Wp / 2, 148), nombre, font=_font(30, False), fill=_tint(acc, 0.7), anchor="mm")

    cal = calendar.Calendar()
    days = cal.monthdayscalendar(anyo, mes)

    y0 = 240
    x0 = 60
    cell_w = (Wp - 2 * x0) / 7
    cell_h = 48

    for i, dlabel in enumerate(_DIAS_ES):
        cx = x0 + i * cell_w + cell_w / 2
        dr.text((cx, y0 + cell_h / 2), dlabel, font=_font(28), fill=INK, anchor="mm")

    y = y0 + cell_h + 10
    for week in days:
        for i, day in enumerate(week):
            cx = x0 + i * cell_w + cell_w / 2
            if day == 0:
                continue
            dr.text((cx, y + cell_h / 2), str(day), font=_font(26, False), fill=INK, anchor="mm")
            dr.line([cx - 14, y + cell_h + 2, cx + 14, y + cell_h + 2], fill=_tint(acc, 0.5), width=1)
        y += cell_h + 8

    y_info = y + 40
    dr.text((Wp / 2, y_info), "Días especiales:", font=_font(26, False), fill=INK, anchor="mm")
    dr.text((Wp / 2, y_info + 40), "✨ ¡El cumpleaños de %s!" % nombre,
            font=_font(28), fill=acc, anchor="mm")

    dr.text((Wp / 2, Hp - 40), "casatridimensional.com.ar", font=_font(18, False), fill=(180, 180, 180), anchor="mm")
    return im


def generar_calendario(data, tema="safari"):
    """Genera los 12 meses del año."""
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip() or "Mi familia"
    anyo = int(data.get("anyo") or "2026")
    return [("%02d_%s" % (m, _MESES_ES[m - 1].lower()),
             (lambda m: (lambda d: mes_hoja(m, anyo, nombre, acc)))(m), True)
            for m in range(1, 13)]


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Familia García"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/calendario"
    for fn, maker, _ in generar_calendario({"nombre": nombre, "anyo": "2026"}, tema):
        maker({"nombre": nombre}).convert("RGB").save(f"{out}_{fn}.png")
        print(f"OK -> {out}_{fn}.png")
        break
