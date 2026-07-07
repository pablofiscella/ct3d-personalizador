"""Gorro / Corona de cumpleaños para armar (craft recortable).
Template A4 apaisado (horizontal) con solapas para imprimir, recortar y armar.
Dos estilos: gorro cónico (party hat) y corona de rey/reina.

=== ESPECIFICACIÓN DEL GORRO — CONVERGIDA CON PABLO 4-jul-2026 ===
(documentado acá porque la primera vez que se armó esto quedó solo en
archivos de prueba sueltos, nunca se subió al código real, y se perdió —
que no vuelva a pasar: esta es la fuente de verdad.)

- Formato: UNA hoja A4 APAISADA (horizontal), 100% de la hoja, no A3 ni 2 hojas.
- 3 TALLES según la edad (la cabeza de un bebé no es la de un nene de 8 años):
    S (1-2 años):  arco ("base") 36cm · alto 14cm
    M (3-5 años):  arco ("base") 41cm · alto 14cm
    L (6-9 años):  arco ("base") 44cm · alto 13cm
  "base" es la LONGITUD DEL ARCO (lo que importa para que entre en la cabeza al
  enrollarlo en cono), no el ancho recto de la hoja — por eso en talles grandes
  el abanico abre más de 180° (se ve bien ancho/achatado, es correcto).
- SIN PEGAMENTO: en vez de solapas para pegar, un lado tiene una LENGÜETA
  (pestaña rectangular) y el otro una RANURA (corte corto) — se enrolla el
  cono y se encastra la lengüeta en la ranura. Más rápido y prolijo para un
  chico armándolo solo.
- 2 AGUJEROS cerca de las puntas del arco, para pasar un elástico y que quede
  puesto (no es una vincha rígida, es gorro con elástico).
- Nombre + edad van en una VENTANA/insignia circular color crema (NO texto
  blanco directo sobre el arte — así se lee bien sin importar qué tan cargado
  esté el fondo temático).
- El arte de fondo (personajes/temática) lo genera IA una vez por tema
  (ver corona_ia.py) y se recorta a la forma del abanico — igual que el resto
  del kit, la personalización (nombre/edad) la escribe SIEMPRE el motor
  encima, nunca queda "horneada" en la imagen generada.
- DPI: se dibuja a 300dpi real (WpH,HpH = 3508x2480), NO a los ~150dpi de
  Wp,Hp que usan certificado/rompecabezas/etc. — el exportador de PDF
  (piezas.generar_kit) siempre declara 300dpi sin mirar la imagen, así que
  dibujar a 150dpi saca un PDF a MITAD de tamaño físico (pasó acá antes de
  corregirlo: un gorro a mitad de escala no entra en ninguna cabeza). Los
  otros tipos con Wp,Hp=1240,1754 tienen el mismo problema sin corregir —
  ver gotcha #5 en CLAUDE.md.
"""
import os, math, json, glob
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
Wp, Hp = 1240, 1754                 # A4 vertical (referencia; corona.py usa horizontal)
# piezas.generar_kit() exporta el PDF con resolution=300 SIEMPRE (generador.DPI),
# sin importar a qué escala se dibujó el PNG — así que gorro/corona se dibujan acá
# a 300dpi de verdad (no a los ~150dpi de Wp,Hp) para que el PDF salga A4 apaisado
# real y no a mitad de tamaño (crítico: un gorro a mitad de escala no entra en
# ninguna cabeza). Wp,Hp de arriba quedan como referencia de la convención vieja.
_PXMM = 2480 / 210.0                # px/mm a 300dpi real (A4 = 2480x3508 @300dpi)
WpH, HpH = round(297 * _PXMM), round(210 * _PXMM)   # A4 APAISADO a 300dpi: 3508 x 2480
CREAM = (253, 250, 242)

# Talles del gorro por edad — ver especificación arriba. R = "alto" (el radio del
# abanico = la altura del cono); el ángulo sale de despejar arco = R·ángulo.
_TALLES_GORRO = {
    "S": {"edades": (1, 2),       "base_mm": 360, "alto_mm": 140, "label": "TALLE S (1-2 años)"},
    "M": {"edades": (3, 4, 5),    "base_mm": 410, "alto_mm": 140, "label": "TALLE M (3-5 años)"},
    "L": {"edades": (6, 7, 8, 9), "base_mm": 440, "alto_mm": 130, "label": "TALLE L (6-9 años)"},
}


def _talla_de_edad(edad):
    try:
        e = int(str(edad).strip())
    except Exception:
        return "M"
    for t, cfg in _TALLES_GORRO.items():
        if e in cfg["edades"]:
            return t
    return "L" if e > 9 else ("S" if e < 1 else "M")


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


def _texto_rotado(base, texto, centro, font, fill, angulo_deg):
    """Pega `texto` rotado `angulo_deg` (grados) centrado en `centro` — para la
    etiqueta "LENGÜETA", que va tangencial al borde del abanico, no horizontal."""
    dr0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = dr0.textbbox((0, 0), texto, font=font)
    w, h = bbox[2] - bbox[0] + 8, bbox[3] - bbox[1] + 8
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((4 - bbox[0], 4 - bbox[1]), texto, font=font, fill=fill)
    tmp = tmp.rotate(-angulo_deg, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(tmp, (int(centro[0] - tmp.width / 2), int(centro[1] - tmp.height / 2)))


def _draw_instrucciones(dr, x, y, col):
    dr.text((x, y), "Instrucciones:", font=_font(56, False), fill=col, anchor="mm")
    pasos = ["1. Recortá por la línea de corte", "2. Doblá por la línea punteada",
             "3. Pegá las solapas con adhesivo"]
    for i, txt in enumerate(pasos):
        dr.text((x, y + 100 + i * 72), txt, font=_font(44, False), fill=_tint(col, 0.3), anchor="mm")


def _draw_instrucciones_en(im, dr, x, y, col):
    _draw_instrucciones(dr, x, y, col)


def _personajes(tema, n=2):
    try:
        import cuaderno
        return cuaderno.personajes_decorativos(tema, n)
    except Exception:
        return []


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


def _fondo_ia(tema, pieza):
    try:
        import corona_ia
        return corona_ia.cargar_fondo(tema, pieza)
    except Exception:
        return None


def gorro(data, tema="safari"):
    """Gorro cónico de cumpleaños para armar — ver especificación completa en el
    docstring del módulo. A4 apaisado, 3 talles por edad, sin pegamento (lengüeta+
    ranura), 2 agujeros para elástico, nombre/edad en insignia circular crema.
    Si el tema tiene un fondo generado con IA (corona_ia) se usa como arte del
    abanico (recortado a su forma); si no, cae al color liso de siempre."""
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or ""
    edad_raw = str(data.get("edad") or "").strip()
    talla = _talla_de_edad(edad_raw)
    cfg = _TALLES_GORRO[talla]

    r = cfg["alto_mm"] * _PXMM
    ang = (cfg["base_mm"] * _PXMM) / r            # radianes: arco = r · ángulo
    half = ang / 2
    base = math.radians(90)                       # el abanico apunta hacia abajo

    im = Image.new("RGBA", (WpH, HpH), CREAM + (255,))
    dr = ImageDraw.Draw(im)

    # En talles anchos (ángulo > 180°, ej. L) los bordes suben por ENCIMA del ápice
    # (el seno del ángulo del borde se vuelve negativo) — margen superior dinámico
    # para que no se corte, en vez de un apex_y fijo pensado solo para ángulos chicos.
    margen_arriba = max(0, -r * math.sin(base - half))
    cx, apex_y = WpH / 2, 180 + margen_arriba
    pts = [(cx, apex_y)]
    for i in range(121):
        a = base - half + i * 2 * half / 120
        pts.append((cx + r * math.cos(a), apex_y + r * math.sin(a)))

    fondo = _fondo_ia(tema, "gorro")
    if fondo is not None:
        mask = Image.new("L", (WpH, HpH), 0)
        ImageDraw.Draw(mask).polygon(pts, fill=255)
        art = fondo.resize((WpH, HpH), Image.LANCZOS)
        im.paste(art, (0, 0), mask)
    else:
        dr.polygon(pts, fill=acc + (255,))
    dr.arc([cx - r, apex_y - r, cx + r, apex_y + r],
           math.degrees(base - half), math.degrees(base + half), fill=acc, width=10)

    ang_r, ang_l = base - half, base + half        # ángulo del borde derecho / izquierdo
    dir_r = (math.cos(ang_r), math.sin(ang_r))
    dir_l = (math.cos(ang_l), math.sin(ang_l))
    for d in (dir_r, dir_l):                       # bordes = líneas de doblez suaves
        dr.line([(cx, apex_y), (cx + r * d[0], apex_y + r * d[1])], fill=_tint(acc, 0.4), width=4)

    # -- 2 agujeros para el elástico, cerca de las puntas del arco --
    hole_r = 28
    for d in (dir_r, dir_l):
        hx, hy = cx + (r - 80) * d[0], apex_y + (r - 80) * d[1]
        dr.ellipse([hx - hole_r, hy - hole_r, hx + hole_r, hy + hole_r],
                   fill=CREAM, outline=(90, 80, 70), width=6)

    # -- lengüeta (borde derecho) + ranura (borde izquierdo): encastre sin pegamento --
    r_tab0, r_tab1, tab_w = 0.62 * r, 0.62 * r + 300, 190
    perp_r = (math.sin(ang_r), -math.cos(ang_r))   # tangencial, hacia AFUERA del abanico
    p_in_a  = (cx + r_tab0 * dir_r[0], apex_y + r_tab0 * dir_r[1])
    p_out_a = (cx + r_tab1 * dir_r[0], apex_y + r_tab1 * dir_r[1])
    tab_poly = [p_in_a,
                (p_in_a[0] + perp_r[0] * tab_w, p_in_a[1] + perp_r[1] * tab_w),
                (p_out_a[0] + perp_r[0] * tab_w, p_out_a[1] + perp_r[1] * tab_w),
                p_out_a]
    dr.polygon(tab_poly, fill=CREAM, outline=(90, 80, 70), width=6)
    tab_mid = ((p_in_a[0] + p_out_a[0]) / 2 + perp_r[0] * tab_w * 0.55,
               (p_in_a[1] + p_out_a[1]) / 2 + perp_r[1] * tab_w * 0.55)
    tab_ang = math.degrees(math.atan2(perp_r[1], perp_r[0]))
    _texto_rotado(im, "LENGÜETA", tab_mid, _font(40), (90, 80, 70), tab_ang)

    r_slot = (r_tab0 + r_tab1) / 2 - 150            # misma distancia radial que la lengüeta
    slot_c = (cx + r_slot * dir_l[0], apex_y + r_slot * dir_l[1])
    perp_l = (math.sin(ang_l), -math.cos(ang_l))
    slot_len = 120
    dr.line([(slot_c[0] - perp_l[0] * slot_len / 2, slot_c[1] - perp_l[1] * slot_len / 2),
             (slot_c[0] + perp_l[0] * slot_len / 2, slot_c[1] + perp_l[1] * slot_len / 2)],
            fill=(90, 80, 70), width=12)
    dr.text((slot_c[0] - dir_l[0] * 110, slot_c[1] - dir_l[1] * 110), "RANURA",
            font=_font(40), fill=(90, 80, 70), anchor="mm")

    # -- insignia circular con nombre + edad: nunca texto directo sobre el arte --
    badge_c = (cx, apex_y + 0.56 * r)
    badge_r = 0.34 * r
    dr.ellipse([badge_c[0] - badge_r, badge_c[1] - badge_r,
                badge_c[0] + badge_r, badge_c[1] + badge_r],
               fill=CREAM + (255,), outline=acc, width=10)
    if nombre:
        fs = int(badge_r * 0.62)
        while _font(fs).getbbox(nombre)[2] > badge_r * 1.7 and fs > 48:
            fs -= 3
        dr.text((badge_c[0], badge_c[1] - badge_r * 0.16), nombre,
                font=_font(fs), fill=(60, 45, 35), anchor="mm")
    if edad_raw:
        etxt = "%s años" % edad_raw if edad_raw != "1" else "1 añito"
        dr.text((badge_c[0], badge_c[1] + badge_r * 0.42), etxt,
                font=_font(int(badge_r * 0.3), False), fill=acc, anchor="mm")

    personajes = _personajes(tema, 1)
    if personajes:
        _paste_h(im, personajes[0], cx, apex_y + r * 0.92, 300)

    y_pie = apex_y + r + 140
    dr.text((cx, y_pie), "SIN pegamento: encastrá la lengüeta en la ranura. "
             "Elástico por los 2 agujeros.", font=_font(40, False), fill=_tint(acc, 0.25), anchor="mm")
    dr.text((60, 60), "%s · arco %scm · alto %scm" % (cfg["label"], cfg["base_mm"] // 10, cfg["alto_mm"] // 10),
             font=_font(44, False), fill=_tint(acc, 0.3))
    dr.text((cx, HpH - 60), "casatridimensional.com.ar", font=_font(36, False), fill=(180, 180, 180), anchor="mm")
    return im


def corona(data, tema="safari"):
    """Corona de rey/reina para armar. Tira con picos, solapas para pegar.
    A4 apaisado (igual que gorro, mismo producto). El ancho de la tira escala
    por talle (misma tabla de edades que el gorro — no hay una tercer medida
    "de circunferencia" propia; usa el máximo de hoja disponible por talle).
    Si el tema tiene un fondo generado con IA (corona_ia), se usa como arte de
    los picos + la banda; el nombre va SIEMPRE en la banda color crema, tinta
    oscura — nunca texto claro directo sobre el arte."""
    acc = _accent(tema)
    nombre = (str(data.get("nombre") or "").strip()) or ""
    talla = _talla_de_edad(data.get("edad"))
    escala = {"S": 0.80, "M": 0.90, "L": 1.0}[talla]

    im = Image.new("RGBA", (WpH, HpH), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, WpH, HpH], fill=CREAM)

    y0 = 180
    h_banda = 340
    w_corona = (WpH - 360) * escala
    x0 = (WpH - w_corona) / 2
    banda_box = [x0 - 20, y0 + h_banda - 52, x0 + w_corona + 20, y0 + h_banda + 52]

    picos = []
    n_picos = 9
    for i in range(n_picos):
        px = x0 + w_corona * (i / (n_picos - 1))
        pico_h = (260 + ((i * 37) % 3) * 52) * escala
        pico_w = 68 * escala
        picos.append((px, pico_h,
                      [(px - pico_w, y0 + h_banda), (px, y0 - pico_h + h_banda), (px + pico_w, y0 + h_banda)]))

    # Nota: la corona NO usa el fondo IA (a diferencia del gorro) — cada pico es
    # un triángulo angosto y recortar la ilustración ahí la hace ilegible en
    # fragmentos. Se queda con el color liso de siempre, que se ve prolijo.
    for _px, _ph, pts in picos:
        dr.polygon(pts, fill=acc, outline=_tint(acc, 0.2), width=6)

    dr.rounded_rectangle(banda_box, 36, fill=CREAM, outline=acc, width=8)

    for px, pico_h, _pts in picos:
        dr.ellipse([px - 30, y0 - pico_h + h_banda - 26, px + 30, y0 - pico_h + h_banda + 26],
                   fill=(255, 255, 255), outline=acc, width=4)

    if nombre:
        fs = 104
        while _font(fs).getbbox(nombre)[2] > w_corona - 160 and fs > 48:
            fs -= 3
        dr.text(((x0 + x0 + w_corona) / 2, y0 + h_banda), nombre, font=_font(fs),
                 fill=(60, 45, 35), anchor="mm")

    dr.line([x0 - 20, y0 + h_banda + 110, x0 + w_corona + 20, y0 + h_banda + 110],
            fill=(180, 180, 180), width=4)
    for x in range(int(x0 - 20), int(x0 + w_corona + 20), 30):
        dr.line([x, y0 + h_banda + 110, x + 14, y0 + h_banda + 110], fill=(180, 180, 180), width=4)

    dr.text((x0 - 20, y0 + h_banda + 136), "← Doblar", font=_font(36, False), fill=(150, 150, 150))
    dr.text((x0 + w_corona + 20, y0 + h_banda + 136), "Doblar →", font=_font(36, False), fill=(150, 150, 150), anchor="ra")

    cx = WpH / 2
    _draw_instrucciones_en(im, dr, cx, y0 + h_banda + 320, acc)

    personajes = _personajes(tema, 2)
    if personajes:
        spots = [(cx - 280, HpH - 380), (cx + 280, HpH - 380)] if len(personajes) > 1 else [(cx, HpH - 380)]
        for p, (sx, sy) in zip(personajes, spots):
            _paste_h(im, p, sx, sy, 440)

    dr.text((60, 60), "%s" % _TALLES_GORRO[talla]["label"], font=_font(44, False), fill=_tint(acc, 0.3))
    dr.text((cx, HpH - 60), "casatridimensional.com.ar", font=_font(36, False), fill=(180, 180, 180), anchor="mm")
    return im


def piezas(data, tema="safari"):
    """Ambos estilos: gorro + corona en 2 páginas."""
    return [("1_gorro", lambda d: gorro(d, tema), True),
            ("2_corona", lambda d: corona(d, tema), True)]


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Mateo"
    edad = sys.argv[3] if len(sys.argv) > 3 else "5"
    out = sys.argv[4] if len(sys.argv) > 4 else "/tmp/corona"
    gorro({"nombre": nombre, "edad": edad}, tema).convert("RGB").save(f"{out}_gorro.png")
    corona({"nombre": nombre, "edad": edad}, tema).convert("RGB").save(f"{out}_corona.png")
    print(f"OK -> {out}_gorro.png + {out}_corona.png")
