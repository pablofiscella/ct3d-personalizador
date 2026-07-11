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


def _font(sz, weight=True):
    """weight acepta bool (compat: True=700, False=500) o un número 300-700
    (eje de peso variable de Fredoka — usado por el slider de grosor del editor)."""
    numeric_weight = (700 if weight else 500) if isinstance(weight, bool) else weight
    for p in glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True):
        try:
            f = ImageFont.truetype(p, sz)
            try: f.set_variation_by_axes([numeric_weight])
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
    """Escala img para caber completa en la hoja A4 (Wp×Hp) — contain, sin recortar ni deformar."""
    r = min(Wp / img.width, Hp / img.height)
    im = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    x = int((Wp - im.width) / 2)
    y = int((Hp - im.height) / 2)
    base.paste(im, (x, y), im if im.mode == "RGBA" else None)


def _hex_to_rgb(hex_color):
    """Convierte #RRGGBB a (R, G, B)."""
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _color_fondo(plant, colors):
    """Color de fondo de la hoja para el modo 'números detrás': usa colors.background si
    está; si no, muestrea una esquina de la plantilla (las hojas tienen borde de fondo)."""
    bg = colors.get("background") if colors else None
    if isinstance(bg, str):
        return _hex_to_rgb(bg)
    if bg:
        return tuple(bg)
    px = plant.convert("RGB").getpixel((2, 2))
    return tuple(px[:3])


def _detras(num_layer, plant, bg, tol=45):
    """Deja los números del día DETRÁS de los dibujos de la plantilla.
    La plantilla es una imagen plana (personaje+fondo fusionados), así que separamos por
    color: donde el pixel es ~fondo, el número se ve; donde hay un dibujo (personaje, banner,
    guarda), ese dibujo tapa al número → el número queda detrás. Preserva la textura del fondo
    (no lo aplana: solo recorta el alfa de la capa de números).
      tol: cuánto puede alejarse un pixel del color de fondo para seguir contando como fondo."""
    from PIL import ImageChops, ImageFilter
    base = Image.new("RGB", plant.size, bg)
    diff = ImageChops.difference(plant.convert("RGB"), base)
    r, g, b = diff.split()
    mx = ImageChops.lighter(ImageChops.lighter(r, g), b)   # 0=fondo, alto=dibujo
    keep = mx.point(lambda v: 255 if v <= tol else 0)      # 255 donde es fondo → mostrar número
    keep = keep.filter(ImageFilter.GaussianBlur(1))        # bordes suaves
    out = num_layer.copy()
    out.putalpha(ImageChops.multiply(num_layer.getchannel("A"), keep))
    return out


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


# ── convención NUEVA del editor con arrastre: temas/<tema>/calendario/{fondo.png,
#    layout.json}. UN fondo compartido por los 12 meses + layout.json con "base"
#    (config default) y "meses" (ajustes puntuales por número de mes, 1-12). ──
def _load_fondo_nuevo(tema, filas=5):
    """Plantilla del grupo: fondo6.png para los meses de 6 filas (si existe),
    fondo.png para el resto — la misma resolución que usa el editor del dash."""
    cal_dir = os.path.join(TEMAS, tema, "calendario")
    candidatos = ["fondo.png"]
    if int(filas) >= 6:
        candidatos.insert(0, "fondo6.png")
    for nombre in candidatos:
        p = os.path.join(cal_dir, nombre)
        if os.path.isfile(p):
            try:
                return Image.open(p).convert("RGBA")
            except Exception:
                continue
    return None


def _load_layout_nuevo(tema):
    p = os.path.join(TEMAS, tema, "calendario", "layout.json")
    if os.path.isfile(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            return None
    return None


def _config_del_mes(layout, mes, anyo=2026):
    """Config del mes con las DOS reglas del editor (ver config_para_mes):
    override puntual > base6 (meses de 6 filas) > base."""
    return config_para_mes(layout, anyo, mes) or _DEFAULT_CAL_CONFIG


def _bbox_contenido(im, umbral=250, margen=24):
    """Recorta el margen en blanco alrededor de la tarjeta real de la hoja de
    mes. Cada hoja se dibuja pensada para imprimirse sola (deja ~50% de
    margen vertical en blanco arriba/abajo de la tarjeta) — al combinar 2
    meses por hoja hay que recortar ese margen antes de escalar, si no la
    tarjeta queda chica y con franjas en blanco en vez de ocupar todo el
    espacio disponible."""
    gris = im.convert("L").point(lambda p: 255 if p < umbral else 0)
    caja = gris.getbbox()
    if not caja:
        return im
    x0, y0, x1, y1 = caja
    x0, y0 = max(0, x0 - margen), max(0, y0 - margen)
    x1, y1 = min(im.width, x1 + margen), min(im.height, y1 + margen)
    return im.crop((x0, y0, x1, y1))


def dos_meses_por_hoja(im1, im2):
    """Combina 2 hojas de mes en UNA sola hoja A4 (arriba/abajo). La tarjeta
    de cada mes (grilla de 7 columnas + personajes) es de forma ANCHA, no
    alta — por eso apilar arriba/abajo (no lado a lado) es lo que la hace
    calzar bien. Cada hoja trae además ~50% de margen en blanco arriba/abajo
    (pensada para imprimirse sola): se recorta ese margen (`_bbox_contenido`)
    antes de escalar, así la tarjeta ocupa todo el ancho de la hoja
    combinada en vez de quedar chica con una franja en blanco de sobra."""
    pagina = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    mitad_h = Hp // 2
    for im, y0 in ((im1, 0), (im2, mitad_h)):
        im = _bbox_contenido(im.convert("RGB")).convert("RGBA")
        r = min(Wp / im.width, mitad_h / im.height)
        w, h = max(1, int(im.width * r)), max(1, int(im.height * r))
        im_r = im.resize((w, h), Image.LANCZOS)
        x, y = (Wp - w) // 2, y0 + (mitad_h - h) // 2
        pagina.alpha_composite(im_r, (x, y))
    dr = ImageDraw.Draw(pagina)
    dr.line([(40, mitad_h), (Wp - 40, mitad_h)], fill=(220, 215, 205), width=2)
    return pagina


def mes_hoja(mes, anyo, acc, tema="safari"):
    """Genera UN mes: calendario TEMÁTICO (sin personalizar) — usa el fondo+
    layout de la temática (el que arma Pablo con el editor con arrastre) si
    existen; si no, cae a la versión 100% procedural (sin plantilla). El año
    lo fija el layout.json de cada tema (campo "anyo") si está definido — no lo
    elige el cliente. Esta es la función que llama productos._piezas_calendario
    — antes NO EXISTÍA (el código llamaba a un nombre viejo/inexistente) y el
    override system además tapaba cualquier intento de generación real con una
    imagen estática fija por tema (ver la excepción de 'calendario' en
    productos.piezas_tipo)."""
    layout = _load_layout_nuevo(tema)
    if layout:
        anyo = int(layout.get("anyo") or anyo)
    # el fondo y la config salen de la regla del mes (5 o 6 filas), igual que el editor
    fondo = _load_fondo_nuevo(tema, filas_del_mes(anyo, mes))
    if fondo is not None and layout:
        config = _config_del_mes(layout, mes, anyo)
        return mes_hoja_desde_config(mes, anyo, "", config, fondo, tema)
    config = _load_config(tema)
    plantilla = _load_plantilla(tema)
    if config and plantilla is not None:
        return mes_hoja_desde_config(mes, anyo, "", config, plantilla, tema)
    return mes_hoja_procedural(mes, anyo, "", acc, tema)


def mes_hoja_procedural(mes, anyo, nombre, acc, tema="safari"):
    """Genera una hoja A4 procedural (sin plantilla)."""
    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    dr.rectangle([0, 0, Wp, 200], fill=acc)
    dr.text((Wp / 2, 110), "%s %d" % (_MESES_ES[mes - 1], anyo), font=_font(64), fill="white", anchor="mm")

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

    personajes = _personajes(tema, 1)
    if personajes:
        _paste_h(im, personajes[0], Wp - 150, Hp - 220, 280)

    dr.text((Wp / 2, Hp - 40), "casatridimensional.com.ar", font=_font(18, False), fill=(180, 180, 180), anchor="mm")
    return im


def mes_hoja_desde_config(mes, anyo, nombre, config, plantilla, tema="safari"):
    """Genera un mes calendario usando config JSON + plantilla PNG.
    El config especifica posiciones, tamaños, colores, etc.
    Soporta dos esquemas: nuevo (month/weekday/days — editor con arrastre)
    y viejo (grid/month_banner/days_header — config_calendario.json de temas)."""
    im = plantilla.copy().convert("RGBA") if plantilla else Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))

    if im.size != (Wp, Hp):
        im2 = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
        _paste_fill(im2, im)
        im = im2

    overlay = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    dr = ImageDraw.Draw(overlay)

    if "month" in config or "weekday" in config or "days" in config:
        colors = config.get("colors", {})

        def _color(key, default):
            v = colors.get(key, default)
            return _hex_to_rgb(v) if isinstance(v, str) else v

        month_cfg = config.get("month", {})
        weekday_cfg = config.get("weekday", {})
        days_cfg = config.get("days", {})

        month_x = month_cfg.get("x", 620)
        month_y = month_cfg.get("y", 80)
        month_size = month_cfg.get("size", 110)
        month_weight = month_cfg.get("weight", 700)
        month_color = _color("month_text", "#000000")

        weekday_x = weekday_cfg.get("x", 271)
        weekday_y = weekday_cfg.get("y", 335)
        weekday_size = weekday_cfg.get("size", 24)
        weekday_spacing = weekday_cfg.get("spacing", 134)
        weekday_weight = weekday_cfg.get("weight", 500)
        weekday_color = _color("weekday_text", "#000000")

        days_x = days_cfg.get("x", 271)
        days_y = days_cfg.get("y", 399)
        day_size = days_cfg.get("size", 28)
        days_spacing_h = days_cfg.get("spacingH", 134)
        days_spacing_v = days_cfg.get("spacingV", 93)
        day_weight = days_cfg.get("weight", 500)
        day_color = _color("day_text", "#000000")

        domingo_rojo = config.get("domingo_rojo", True)
        ROJO_DOMINGO = (211, 47, 47)  # #D32F2F — mismo tono que usa el preview del editor

        # Ancla por la LÍNEA BASE (ms), no por el centro (mm): la baseline es una
        # referencia independiente de la fuente, así el preview del editor (canvas,
        # textBaseline='alphabetic') cae exactamente donde el motor dibuja el mes.
        dr.text((month_x, month_y), _MESES_ES[mes - 1],
                font=_font(month_size, weight=month_weight), fill=month_color, anchor="ms")

        for i, dlabel in enumerate(_DIAS_ES):
            color = ROJO_DOMINGO if (domingo_rojo and i == 6) else weekday_color
            dr.text((weekday_x + i * weekday_spacing, weekday_y), dlabel,
                    font=_font(weekday_size, weight=weekday_weight), fill=color, anchor="mm")

        # Los números del día van en su propia capa para poder meterlos DETRÁS de los dibujos.
        num_layer = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
        drn = ImageDraw.Draw(num_layer)

        cal = calendar.Calendar()
        days = cal.monthdayscalendar(anyo, mes)
        for row, week in enumerate(days):
            for col, day in enumerate(week):
                if day == 0:
                    continue
                color = ROJO_DOMINGO if (domingo_rojo and col == 6) else day_color
                cx = days_x + col * days_spacing_h
                cy = days_y + row * days_spacing_v
                drn.text((cx, cy), str(day), font=_font(day_size, weight=day_weight),
                         fill=color, anchor="mm")

        if config.get("detras", days_cfg.get("detras", True)) and plantilla:
            tol = int(days_cfg.get("detras_tol", config.get("detras_tol", 45)))
            num_layer = _detras(num_layer, im, _color_fondo(im, colors), tol)

        im = Image.alpha_composite(im, num_layer)   # números (recortados por los dibujos)
        im = Image.alpha_composite(im, overlay)     # mes + días de semana, siempre arriba
        return im

    # --- esquema viejo (config_calendario.json de temas existentes) ---
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
    day_size = font_sizes.get("day", 28)
    cell_h = grid_h / rows
    # Números del día en su propia capa para poder meterlos DETRÁS de los dibujos.
    num_layer = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    drn = ImageDraw.Draw(num_layer)
    y = grid_y
    for week in days:
        for i, day in enumerate(week):
            cx = grid_x + i * cell_w + cell_w / 2
            if day == 0:
                continue
            drn.text((cx, y + cell_h / 2 + day_text_y_offset), str(day),
                     font=_font(day_size), fill=day_text_color, anchor="mm")
        y += cell_h

    days_cfg = config.get("days", {})
    if config.get("detras", days_cfg.get("detras", True)) and plantilla:
        tol = int(days_cfg.get("detras_tol", config.get("detras_tol", 45)))
        num_layer = _detras(num_layer, im, _color_fondo(im, colors), tol)

    im = Image.alpha_composite(im, num_layer)   # números (recortados por los dibujos)
    im = Image.alpha_composite(im, overlay)     # mes + días de semana, siempre arriba
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


# Config por defecto (esquema NUEVO del editor). Se usa solo como red de seguridad
# si se pide generar sin config; el editor siempre manda la suya.
_DEFAULT_CAL_CONFIG = {
    "month": {"x": 620, "y": 80, "size": 85, "weight": 560},
    "weekday": {"x": 271, "y": 335, "size": 24, "spacing": 134, "weight": 500},
    "days": {"x": 271, "y": 399, "size": 28, "spacingH": 134, "spacingV": 93, "weight": 600},
    "colors": {"month_text": "#000000"},
    "domingo_rojo": True,
}


def filas_del_mes(anyo, mes):
    """Cantidad de filas (semanas, lunes primero) que ocupa el mes en la grilla.
    En 2026: marzo/agosto/noviembre ocupan 6 filas; el resto 5."""
    return len(calendar.Calendar().monthdayscalendar(int(anyo), mes))


def meses_por_filas(anyo, filas):
    """Meses (1-12) del año que ocupan exactamente `filas` filas si filas==6,
    o 5 filas O MENOS si filas==5 (febrero puede ocupar 4)."""
    if int(filas) >= 6:
        return [m for m in range(1, 13) if filas_del_mes(anyo, m) >= 6]
    return [m for m in range(1, 13) if filas_del_mes(anyo, m) < 6]


def config_para_mes(layout, anyo, mes):
    """Config efectiva de un mes según las DOS reglas del layout:
    override puntual del mes > regla de 6 filas (`base6`) > regla general (`base`).
    Los meses de 6 filas necesitan otra posición/espaciado para que la grilla
    entre en el arte, por eso llevan regla propia."""
    layout = layout or {}
    cfg = (layout.get("meses") or {}).get(str(mes))
    if cfg:
        return cfg
    if filas_del_mes(anyo, mes) >= 6:
        cfg = layout.get("base6")
        if cfg:
            return cfg
    return layout.get("base") or {}


def generar_mes_con_plantilla(data, plantilla_img, tema, mes, config):
    """Genera UN solo mes (1-12) con config + plantilla y devuelve la PIL Image RGBA.
    Se usa para regenerar un mes puntual desde su tarjeta (editor por mes), con
    coordenadas propias por mes (ej. acomodar la 6a fila de Marzo/Agosto/Noviembre)."""
    nombre = str(data.get("nombre") or "").strip() or "Mi familia"
    anyo = int(data.get("anyo") or "2026")
    plantilla = plantilla_img if plantilla_img else _load_plantilla(tema)
    if not config:
        config = _DEFAULT_CAL_CONFIG
    return mes_hoja_desde_config(mes, anyo, nombre, config, plantilla, tema)


def generar_calendario_con_plantilla(data, plantilla_img, tema="safari", config=None):
    """Genera los 12 meses usando una plantilla pasada como PIL Image.
    Útil para el editor interactivo del dashboard.
    plantilla_img: PIL Image RGBA (o None para modo procedural)
    config: dict con posiciones/tamaños del editor (prioridad sobre el config_calendario.json del tema)
    """
    nombre = str(data.get("nombre") or "").strip() or "Mi familia"
    anyo = int(data.get("anyo") or "2026")
    acc = _accent(tema)

    if not config:
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
