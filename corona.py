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


def _mm(v):
    return v * _PXMM


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
        # base de color debajo del arte: si la IA dejó esquinas pálidas/blancas,
        # que no se lean como "dibujo sin terminar" (feedback Pablo, princesas)
        dr.polygon(pts, fill=_tint(acc, 0.75) + (255,))
        mask = Image.new("L", (WpH, HpH), 0)
        ImageDraw.Draw(mask).polygon(pts, fill=255)
        import fondos_ia
        # cover al BBOX del abanico con SOBRE-ESCANEO del 22%: la IA deja los
        # bordes de la imagen pálidos/ralos y eso caía justo en las PUNTAS del
        # arco (sector blanco donde van ranura y lengüeta — feedback Pablo).
        # Se recorta ese borde y se usa la zona densa del arte.
        bx0 = int(min(p[0] for p in pts)); by0 = int(min(p[1] for p in pts))
        bx1 = int(max(p[0] for p in pts)); by1 = int(max(p[1] for p in pts))
        bw, bh = bx1 - bx0, by1 - by0
        # más agresivo a lo ANCHO (las puntas del arco están a los costados) y
        # anclado abajo (ahí están los personajes: no recortarles la cabeza)
        big = fondos_ia.cover(fondo, int(bw * 1.55), int(bh * 1.18))
        ox = (big.width - bw) // 2
        oy = int((big.height - bh) * 0.62)
        art = big.crop((ox, oy, ox + bw, oy + bh))
        capa = Image.new("RGBA", (WpH, HpH), (0, 0, 0, 0))
        capa.paste(art, (bx0, by0))
        im.paste(capa, (0, 0), mask)
    else:
        dr.polygon(pts, fill=acc + (255,))
    dr.arc([cx - r, apex_y - r, cx + r, apex_y + r],
           math.degrees(base - half), math.degrees(base + half), fill=acc, width=10)

    ang_r, ang_l = base - half, base + half        # ángulo del borde derecho / izquierdo
    dir_r = (math.cos(ang_r), math.sin(ang_r))
    dir_l = (math.cos(ang_l), math.sin(ang_l))
    for d in (dir_r, dir_l):                       # bordes del abanico bien visibles
        dr.line([(cx, apex_y), (cx + r * d[0], apex_y + r * d[1])], fill=_tint(acc, 0.15), width=7)

    # SIN círculos de elástico impresos (Pablo 9-jul-2026: quedaban flotando en
    # la punta como algo sin dibujar — si quieren elástico, agujerean la punta).
    # PUNTAS con el propio patrón: los extremos del arte IA son pálidos y la
    # esquina quedaba blanca; una cuña de color liso tampoco convenció ("rosa
    # pero sin la gráfica") — se rellena con la franja vecina del MISMO arte,
    # espejada, así el dibujo continúa hasta la punta.
    if fondo is not None:
        for d, ang_borde, sgn in ((dir_r, ang_r, 1), (dir_l, ang_l, -1)):
            perp = (math.sin(ang_borde), -math.cos(ang_borde))
            p_mid = (cx + (r - 195) * d[0], apex_y + (r - 195) * d[1])
            hacia_dentro = (cx - p_mid[0], (apex_y + 0.6 * r) - p_mid[1])
            if perp[0] * hacia_dentro[0] + perp[1] * hacia_dentro[1] < 0:
                perp = (-perp[0], -perp[1])
            punta = (cx + r * d[0], apex_y + r * d[1])
            a_arc = ang_borde + sgn * (120.0 / r)  # 120px sobre el arco, hacia adentro
            q_arc = (cx + r * math.cos(a_arc), apex_y + r * math.sin(a_arc))
            poly = [p_mid, punta, q_arc,
                    (p_mid[0] + perp[0] * 105, p_mid[1] + perp[1] * 105)]
            xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
            wx0, wy0 = int(min(xs)), int(min(ys))
            wx1, wy1 = int(max(xs)) + 1, int(max(ys)) + 1
            sx, sy = int(-340 * d[0]), int(-340 * d[1])    # franja vecina, hacia adentro
            src = im.crop((wx0 + sx, wy0 + sy, wx1 + sx, wy1 + sy))
            src = src.transpose(Image.FLIP_LEFT_RIGHT)     # espejo: continúa el patrón
            mk = Image.new("L", (wx1 - wx0, wy1 - wy0), 0)
            ImageDraw.Draw(mk).polygon([(p[0] - wx0, p[1] - wy0) for p in poly], fill=255)
            im.paste(src, (wx0, wy0), mk)
    dr.arc([cx - r, apex_y - r, cx + r, apex_y + r],
           math.degrees(base - half), math.degrees(base + half), fill=acc, width=10)
    for d in (dir_r, dir_l):                       # bordes por encima del parche
        dr.line([(cx, apex_y), (cx + r * d[0], apex_y + r * d[1])],
                fill=_tint(acc, 0.15), width=7)

    # -- lengüeta (borde derecho) + ranura (borde izquierdo): encastre sin pegamento --
    # Lengüeta en T: CUELLO más angosto que la ranura (pasa fácil) y CABEZA más
    # ANCHA que la ranura (se dobla para entrar y después TRABA, no se sale —
    # feedback Pablo 9-jul-2026: si es del mismo ancho que el corte, se zafa).
    r_tab0, tab_len, tab_w = 0.70 * r, 300, 165
    perp_r = (math.sin(ang_r), -math.cos(ang_r))   # tangencial, hacia AFUERA del abanico

    def _pt_r(u, v):
        rr = r_tab0 + u
        return (cx + rr * dir_r[0] + perp_r[0] * v, apex_y + rr * dir_r[1] + perp_r[1] * v)

    cuello0, cuello1 = 40, tab_len - 40            # cuello: 220 (ranura: 240)
    # cuello MÍNIMO (~1mm): la cabeza pegada al borde del gorro, solo el juego
    # justo para trabar en la ranura (feedback Pablo 9-jul-2026, iterado 2 veces)
    v_cuello, ch = 15, 45                          # cabeza: 300 (> ranura) chanfle 45°
    tab_poly = [_pt_r(cuello0, 0), _pt_r(cuello0, v_cuello), _pt_r(0, v_cuello),
                _pt_r(0, tab_w - ch), _pt_r(ch, tab_w), _pt_r(tab_len - ch, tab_w),
                _pt_r(tab_len, tab_w - ch), _pt_r(tab_len, v_cuello),
                _pt_r(cuello1, v_cuello), _pt_r(cuello1, 0)]
    dr.polygon(tab_poly, fill=CREAM, outline=(90, 80, 70), width=6)
    tab_ang = math.degrees(math.atan2(perp_r[1], perp_r[0]))
    _texto_rotado(im, "LENGÜETA", _pt_r(tab_len / 2, tab_w * 0.62),
                  _font(40), (90, 80, 70), tab_ang)

    # RANURA: corte PARALELO al borde izquierdo, PEGADO al borde (5mm hacia
    # adentro) y con el MISMO rango radial que la lengüeta — al enrollar el cono
    # la lengüeta atraviesa la ranura y encastra. Pegada al borde se VE paralela
    # (a 9mm flotaba en medio del arte y parecía torcida — feedback Pablo).
    perp_l = (math.sin(ang_l), -math.cos(ang_l))
    centroide = (cx, apex_y + 0.6 * r)
    p_edge = (cx + (r_tab0 + tab_len / 2) * dir_l[0],
              apex_y + (r_tab0 + tab_len / 2) * dir_l[1])
    if (centroide[0] - p_edge[0]) * perp_l[0] + (centroide[1] - p_edge[1]) * perp_l[1] < 0:
        perp_l = (-perp_l[0], -perp_l[1])          # que apunte hacia ADENTRO
    inset = 5 * _PXMM
    # ranura 240: el CUELLO (220) pasa con juego, la CABEZA (300) no se sale
    r_s0, r_s1 = r_tab0 + 30, r_tab0 + tab_len - 30
    s0 = (cx + r_s0 * dir_l[0] + perp_l[0] * inset,
          apex_y + r_s0 * dir_l[1] + perp_l[1] * inset)
    s1 = (cx + r_s1 * dir_l[0] + perp_l[0] * inset,
          apex_y + r_s1 * dir_l[1] + perp_l[1] * inset)
    dr.line([s0, s1], fill=(90, 80, 70), width=12)
    slot_ang = math.degrees(math.atan2(s1[1] - s0[1], s1[0] - s0[0]))
    if slot_ang > 90:                              # que el texto no quede cabeza abajo
        slot_ang -= 180
    elif slot_ang < -90:
        slot_ang += 180
    _texto_rotado(im, "RANURA", ((s0[0] + s1[0]) / 2 + perp_l[0] * 62,
                                 (s0[1] + s1[1]) / 2 + perp_l[1] * 62),
                  _font(40), (90, 80, 70), slot_ang)

    # SIN nombre ni edad (decisión de Pablo, 8-jul-2026: el gorro se imprime para
    # todos los invitados y se pone en el momento — la edad solo elige el TALLE).
    # Tampoco personajes sueltos pegados encima: el arte IA ya es la decoración.

    y_pie = apex_y + r + 140
    dr.text((cx, y_pie), "SIN pegamento: encastrá la lengüeta en la ranura. "
             "¿Elástico? Hacé un agujerito en cada punta.",
            font=_font(40, False), fill=_tint(acc, 0.25), anchor="mm")
    dr.text((60, 60), "%s · arco %scm · alto %scm" % (cfg["label"], cfg["base_mm"] // 10, cfg["alto_mm"] // 10),
             font=_font(44, False), fill=_tint(acc, 0.3))
    dr.text((cx, HpH - 60), "casatridimensional.com.ar", font=_font(36, False), fill=(180, 180, 180), anchor="mm")
    return im


def _silueta_corona(x0, x1, y_base, h_banda, h_pico, n):
    """Contorno CONTINUO de media corona: banda + picos triangulares unidos
    (un solo recorte, sin triángulos sueltos)."""
    seg = (x1 - x0) / n
    pts = [(x0, y_base), (x0, y_base - h_banda)]
    for i in range(n):
        vx = x0 + i * seg
        pts.append((vx + seg / 2, y_base - h_banda - h_pico))
        pts.append((vx + seg, y_base - h_banda))
    pts.append((x1, y_base))
    return pts


def _tira_corona(im, dr, tema, acc, fondo, x0, x1, y_base, h_banda, h_pico, n_picos):
    pts = _silueta_corona(x0, x1, y_base, h_banda, h_pico, n_picos)
    borde = tuple(int(v * 0.55) for v in acc)
    if fondo is not None:
        dr.polygon(pts, fill=_tint(acc, 0.7) + (255,))     # base por si el arte trae claros
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).polygon(pts, fill=255)
        import fondos_ia
        # sobre-escaneo 15%: los bordes de la imagen IA son pálidos y caían en
        # los extremos de la tira (mismo fix que el gorro)
        bx0 = int(min(p[0] for p in pts)); by0 = int(min(p[1] for p in pts))
        bx1 = int(max(p[0] for p in pts)); by1 = int(max(p[1] for p in pts))
        bw, bh = bx1 - bx0, by1 - by0
        big = fondos_ia.cover(fondo, int(bw * 1.15), int(bh * 1.15))
        ox, oy = (big.width - bw) // 2, (big.height - bh) // 2
        art = big.crop((ox, oy, ox + bw, oy + bh))
        capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
        capa.paste(art, (bx0, by0))
        im.paste(capa, (0, 0), mask)
    else:
        dr.polygon(pts, fill=acc + (255,))
    dr.line(pts + [pts[0]], fill=borde, width=10, joint="curve")
    # gema redonda en cada punta + gemas rombo en la banda (mitad de cada pico)
    seg = (x1 - x0) / n_picos
    gr = h_pico * 0.16
    for i in range(n_picos):
        gx, gy = x0 + i * seg + seg / 2, y_base - h_banda - h_pico
        dr.ellipse([gx - gr, gy - gr, gx + gr, gy + gr],
                   fill=(255, 214, 98), outline=borde, width=6)
        if fondo is None:
            # gemas rombo SOLO en el fallback liso — sobre el arte IA tapaban
            # justo las caras de los personajes (feedback princesas)
            ry, rw = y_base - h_banda / 2, h_banda * 0.20
            dr.polygon([(gx, ry - rw), (gx + rw * 0.75, ry), (gx, ry + rw), (gx - rw * 0.75, ry)],
                       fill=CREAM, outline=borde, width=5)
    # ── encastre SIN pegamento (igual que el gorro — feedback Pablo 9-jul-2026):
    # lengüeta que sale del extremo derecho de la banda + 3 RANURAS verticales en
    # el extremo izquierdo: la lengüeta de una tira entra en una ranura de la
    # otra, y la ranura elegida AJUSTA el talle (más adentro = más chica).
    # lengüeta en T integrada a la banda: CUELLO más angosto que la ranura y
    # CABEZA más ANCHA (se dobla para entrar y traba — feedback Pablo: del
    # mismo ancho que el corte, se sale). Chanfles a 45° como el cubo.
    ty = y_base - h_banda / 2
    cuello_h, cabeza_h = h_banda * 0.40, h_banda * 0.72
    cuello_len, cabeza_len = _mm(7), _mm(13)
    ch = cabeza_h * 0.22
    xa, xb = x1 + cuello_len, x1 + cuello_len + cabeza_len
    tab_pts = [(x1, ty - cuello_h / 2), (xa, ty - cuello_h / 2), (xa, ty - cabeza_h / 2),
               (xb - ch, ty - cabeza_h / 2), (xb, ty - cabeza_h / 2 + ch),
               (xb, ty + cabeza_h / 2 - ch), (xb - ch, ty + cabeza_h / 2),
               (xa, ty + cabeza_h / 2), (xa, ty + cuello_h / 2), (x1, ty + cuello_h / 2)]
    dr.polygon(tab_pts, fill=CREAM, outline=(90, 80, 70), width=6)
    _texto_rotado(im, "LENGÜETA", ((xa + xb) / 2, ty), _font(28), (90, 80, 70), 90)
    slot_h = cuello_h + _mm(2)                     # cuello pasa, cabeza traba
    for k in range(3):
        sx = x0 + _mm(15 + 15 * k)
        dr.line([sx, ty - slot_h / 2, sx, ty + slot_h / 2], fill=(90, 80, 70), width=10)
    dr.text((x0 + _mm(30), y_base + _mm(4)),
            "ranuras: elegí la que ajuste mejor", font=_font(30, False),
            fill=(120, 110, 100), anchor="ma")


def corona(data, tema="safari"):
    """Corona para armar — REDISEÑO 8-jul-2026 (feedback Pablo: los picos sueltos
    no parecían corona, la tira no daba la vuelta a una cabeza real y el nombre
    sobra porque se pone en el momento, igual que el gorro).
    - DOS tiras en la misma hoja A4 apaisada que se UNEN entre sí (cinta o
      pegamento por las líneas punteadas) → da la circunferencia real de una
      cabeza (~50cm), ajustable por cuánto se solapan.
    - Silueta CONTINUA: banda + picos triangulares unidos, un solo recorte por
      tira, con gema dorada en cada punta y gemas rombo en la banda.
    - Relleno con el arte IA del tema (corona_ia «corona» o, si no hay, el del
      gorro); fallback color del tema. SIN nombre."""
    acc = _accent(tema)
    talla = _talla_de_edad(data.get("edad"))
    esc = {"S": 0.85, "M": 0.95, "L": 1.0}[talla]

    im = Image.new("RGBA", (WpH, HpH), CREAM + (255,))
    dr = ImageDraw.Draw(im)
    fondo = _fondo_ia(tema, "corona")
    if fondo is None:
        fondo = _fondo_ia(tema, "gorro")

    # 2 tiras que se ENCASTRAN entre sí (lengüeta de una en ranura de la otra):
    # el extremo derecho deja lugar para la lengüeta que sobresale de la banda
    x0, x1 = 70, WpH - 70 - int(20 * _PXMM)
    h_banda = 38 * _PXMM * esc
    h_pico = 45 * _PXMM * esc
    n_picos = 5
    for y_base in (1180, 2280):
        _tira_corona(im, dr, tema, acc, fondo, x0, x1, y_base, h_banda, h_pico, n_picos)

    dr.text((60, 52), "CORONA · %s" % _TALLES_GORRO[talla]["label"],
            font=_font(44, False), fill=_tint(acc, 0.3))
    dr.text((WpH / 2, 140), "SIN pegamento: recortá las 2 tiras y encastrá la lengüeta "
            "de cada una en una ranura de la otra (la ranura elegida ajusta el talle).",
            font=_font(40, False), fill=_tint(acc, 0.2), anchor="mm")
    dr.text((WpH / 2, HpH - 55), "casatridimensional.com.ar",
            font=_font(36, False), fill=(180, 180, 180), anchor="mm")
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
