"""Calendario familiar personalizado — 12 meses con el nombre + temática.
Cada mes en una hoja A4. Soporta:
- Modo procedural (dibuja todo desde código, sin plantilla)
- Modo con plantilla: superpone calendarios sobre imagen de tema
Cada temática puede tener config_calendario.json + plantilla.png"""
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


def _personajes(tema, n=1):
    try:
        import cuaderno
        return cuaderno.personajes_decorativos(tema, n)
    except Exception:
        return []


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


def _paste_fill(base, img):
    """Escala y recorta img para cubrir toda la hoja A4 (Wp×Hp) — cover. Sin deformar."""
    r = max(Wp / img.width, Hp / img.height)
    im = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    x = int((im.width - Wp) / 2)
    y = int((im.height - Hp) / 2)
    base.paste(im.crop((x, y, x + Wp, y + Hp)), (0, 0))


def _hex_to_rgb(hex_color):
    """Convierte #RRGGBB a (R, G, B)."""
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _load_config(tema):
    """Carga config_calendario.json de la temática. Si no existe, devuelve None."""
    config_path = os.path.join(TEMAS, tema, "config_calendario.json")
    if os.path.exists(config_path):
        try:
            return json.load(open(config_path))
        except Exception:
            return None
    return None


def _load_plantilla(tema):
    """Carga plantilla.png de la temática. Si no existe, devuelve None."""
    plantilla_path = os.path.join(TEMAS, tema, "plantilla.png")
    if os.path.exists(plantilla_path):
        try:
            return Image.open(plantilla_path).convert("RGBA")
        except Exception:
            return None
    return None


_MESES_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
_DIAS_ES = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]


def mes_hoja_procedural(mes, anyo, nombre, acc, tema="safari"):
    """Genera una hoja A4 procedural (sin plantilla)."""
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
    dr.text((Wp / 2, y_info + 40), "¡El cumpleaños de %s!" % nombre,
            font=_font(28), fill=acc, anchor="mm")

    personajes = _personajes(tema, 1)
    if personajes:
        _paste_h(im, personajes[0], Wp - 150, Hp - 220, 280)

    dr.text((Wp / 2, Hp - 40), "casatridimensional.com.ar", font=_font(18, False), fill=(180, 180, 180), anchor="mm")
    return im


def mes_hoja_desde_config(mes, anyo, nombre, config, plantilla, tema="safari"):
    """Genera un mes calendario usando config JSON + plantilla PNG.
    El config especifica posiciones, tamaños, colores, etc."""
    im = plantilla.copy().convert("RGBA") if plantilla else Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))

    if im.size != (Wp, Hp):
        im2 = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
        _paste_fill(im2, im)
        im = im2

    overlay = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    dr = ImageDraw.Draw(overlay)

    # Leer config
    grid_cfg = config.get("grid", {})
    grid_x = grid_cfg.get("x", 271)
    grid_y = grid_cfg.get("y", 399)
    grid_w = grid_cfg.get("width", 939)
    grid_h = grid_cfg.get("height", 557)
    cols = grid_cfg.get("cols", 7)
    rows = grid_cfg.get("rows", 6)

    month_banner_cfg = config.get("month_banner", {})
    month_text_y = month_banner_cfg.get("text_y", 247)

    days_header_cfg = config.get("days_header", {})
    days_header_x = days_header_cfg.get("x", 272)
    days_header_y = days_header_cfg.get("y", 335)
    days_header_text_y = days_header_cfg.get("text_y", 360)

    font_sizes = config.get("font_sizes", {"month": 110, "weekday": 24, "day": 28})
    colors = config.get("colors", {})

    # Colores
    month_text_color = _hex_to_rgb(colors.get("month_text", "#FFFFFF")) if isinstance(colors.get("month_text"), str) else colors.get("month_text", (255, 255, 255))
    weekday_text_color = _hex_to_rgb(colors.get("weekday_text", "#FFFFFF")) if isinstance(colors.get("weekday_text"), str) else colors.get("weekday_text", (255, 255, 255))
    day_text_color = _hex_to_rgb(colors.get("day_text", "#1E1E1E")) if isinstance(colors.get("day_text"), str) else colors.get("day_text", (30, 30, 30))

    # Mes
    dr.text((Wp / 2, month_text_y), "%s %d" % (_MESES_ES[mes - 1], anyo),
            font=_font(font_sizes.get("month", 110)), fill=month_text_color, anchor="mm")

    # Días de la semana
    cell_w = grid_w / cols
    for i, dlabel in enumerate(_DIAS_ES):
        cx = days_header_x + i * cell_w + cell_w / 2
        dr.text((cx, days_header_text_y), dlabel,
                font=_font(font_sizes.get("weekday", 24)), fill=weekday_text_color, anchor="mm")

    # Números
    cal = calendar.Calendar()
    days = cal.monthdayscalendar(anyo, mes)

    day_text_y_offset = config.get("day_text_y_offset", -4)
    cell_h = grid_h / rows
    y = grid_y
    for week in days:
        for i, day in enumerate(week):
            cx = grid_x + i * cell_w + cell_w / 2
            if day == 0:
                continue
            dr.text((cx, y + cell_h / 2 + day_text_y_offset), str(day),
                    font=_font(font_sizes.get("day", 28)), fill=day_text_color, anchor="mm")
        y += cell_h

    im = Image.alpha_composite(im, overlay)
    return im


def generar_calendario(data, tema="safari"):
    """Genera los 12 meses del año.
    Si existe config + plantilla, usa esos. Si no, modo procedural."""
    nombre = str(data.get("nombre") or "").strip() or "Mi familia"
    anyo = int(data.get("anyo") or "2026")
    acc = _accent(tema)

    config = _load_config(tema)
    plantilla = _load_plantilla(tema)

    usar_config = config and plantilla

    if usar_config:
        # Modo con config
        return [("%02d_%s" % (m, _MESES_ES[m - 1].lower()),
                 (lambda m: (lambda d: mes_hoja_desde_config(m, anyo, nombre, config, plantilla, tema)))(m), True)
                for m in range(1, 13)]
    else:
        # Modo procedural
        return [("%02d_%s" % (m, _MESES_ES[m - 1].lower()),
                 (lambda m: (lambda d: mes_hoja_procedural(m, anyo, nombre, acc, tema)))(m), True)
                for m in range(1, 13)]


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "monstruos"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Familia García"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/calendario"
    for fn, maker, _ in generar_calendario({"nombre": nombre, "anyo": "2026"}, tema):
        maker({"nombre": nombre}).convert("RGB").save(f"{out}_{fn}.png")
        print(f"OK -> {out}_{fn}.png")
        break


def generar_calendario_con_plantilla(data, plantilla_img, tema="safari"):
    """Genera los 12 meses usando una plantilla pasada como PIL Image.
    Útil para el editor interactivo del dashboard.
    plantilla_img: PIL Image RGBA (o None para modo procedural)
    """
    nombre = str(data.get("nombre") or "").strip() or "Mi familia"
    anyo = int(data.get("anyo") or "2026")
    acc = _accent(tema)

    config = _load_config(tema)
    
    # Si pasó una plantilla, úsala. Si no, carga del disco o modo procedural.
    plantilla = plantilla_img if plantilla_img else _load_plantilla(tema)
    usar_config = config and plantilla

    if usar_config:
        # Modo con config + plantilla
        return [("%02d_%s" % (m, _MESES_ES[m - 1].lower()),
                 (lambda m: (lambda d: mes_hoja_desde_config(m, anyo, nombre, config, plantilla, tema)))(m), True)
                for m in range(1, 13)]
    else:
        # Modo procedural
        return [("%02d_%s" % (m, _MESES_ES[m - 1].lower()),
                 (lambda m: (lambda d: mes_hoja_procedural(m, anyo, nombre, acc, tema)))(m), True)
                for m in range(1, 13)]
