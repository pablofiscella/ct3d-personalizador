"""Antifaces y Photo Booth Props — antifaz, bigotes y lentes en palito.
Para imprimir, recortar, pegar en palitos/elástico y sacarse fotos.

REDISEÑO 7-jul-2026 (skill armar-kit §9 — la versión anterior era inutilizable:
el "antifaz" eran dos aros sin agujeros de ojos, los bigotes irreconocibles y
superpuestos, los lentes cortados por el borde):
- 300dpi REAL (A4 = 2480x3508) — antes dibujaba a 150dpi y el PDF salía a la
  mitad (un antifaz de 9cm no entra en ninguna cara).
- Antifaz con medidas antropométricas: ~16.5cm de ancho, centros de ojos a
  55mm (cubre de 3 a 10 años), agujeros de ojos de ~34mm.
- Agujeros laterales con anillo de refuerzo impreso para el elástico.
- Contorno blanco + línea de corte gris en todos los recortables (look
  sticker pro + perdona el pulso al recortar).
- Palito indicado al costado (no al centro: tapa la cara).
- Grillas sin colisiones: cada prop en su celda, verificado visualmente.
100% procedural con Pillow. Los personajes del tema decoran la hoja (fuera
de las piezas, como guía de estilo)."""
import os, math, json, glob
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
_PXMM = 2480 / 210.0                 # 300dpi real
Wp, Hp = 2480, 3508                  # A4 vertical @300dpi
CREAM = (253, 250, 242)
INK = (60, 50, 45)
CORTE = (150, 150, 150)


def _mm(v):
    return v * _PXMM


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


def _personaje(tema):
    try:
        import cuaderno
        ps = cuaderno.personajes_decorativos(tema, 1)
        return ps[0] if ps else None
    except Exception:
        return None


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


def _hoja(titulo, acc):
    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)
    dr.text((60, 55), titulo, font=_font(44, False), fill=_tint(acc, 0.3))
    dr.text((Wp / 2, Hp - 60), "casatridimensional.com.ar", font=_font(36, False),
            fill=(180, 180, 180), anchor="mm")
    return im, dr


def _pie(dr, texto, acc, y=None):
    dr.text((Wp / 2, y or (Hp - 140)), texto, font=_font(38, False),
            fill=_tint(INK, 0.35), anchor="mm")


def _contorno_blanco(im, grosor_px):
    """Contorno blanco alrededor de las zonas opacas + línea de corte gris —
    el rasgo "sticker pro" (skill §2) y margen de error para la tijera.
    La dilatación se calcula a 1/4 de resolución (MaxFilter sobre la hoja
    completa a 300dpi tardaba ~15s por capa; así baja a <1s y el borde de
    3mm no pierde calidad visible)."""
    from PIL import ImageFilter, ImageChops
    W, H = im.size
    esc = 4
    a = im.getchannel("A").resize((W // esc, H // esc), Image.BILINEAR)
    k = max(3, (grosor_px // esc) * 2 + 1)
    dil_s = a.point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(k))
    borde_s = dil_s.filter(ImageFilter.MaxFilter(3))
    dil = dil_s.resize((W, H), Image.BILINEAR).point(lambda v: 255 if v > 128 else 0)
    borde = borde_s.resize((W, H), Image.BILINEAR).point(lambda v: 255 if v > 128 else 0)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste((255, 255, 255, 255), (0, 0), dil)
    out.alpha_composite(im)
    linea = ImageChops.subtract(borde, dil)
    out.paste(CORTE + (255,), (0, 0), linea)
    return out


def _refuerzo_elastico(dr, x, y, acc):
    """Agujero para el elástico con anillo de refuerzo impreso (skill §9)."""
    r_out, r_in = _mm(5.5), _mm(2)
    dr.ellipse([x - r_out, y - r_out, x + r_out, y + r_out],
               fill=(255, 255, 255), outline=acc, width=6)
    dr.ellipse([x - r_in, y - r_in, x + r_in, y + r_in],
               fill=CREAM, outline=(90, 80, 70), width=4)


def _forma_antifaz(cx, cy, w, h, muesca=0.42):
    """Contorno del antifaz clásico (dominó): ala a punta en los extremos,
    ceja suave arriba, muesca de nariz abajo al centro. Devuelve el polígono."""
    pts_top, pts_bot = [], []
    N = 120
    for i in range(N + 1):
        t = -1 + 2 * i / N                    # -1..1
        # borde superior: alto en el centro, cae hacia las puntas
        ty = -h / 2 * (0.95 - 0.55 * t ** 4)
        # borde inferior: baja en los ojos, sube al centro (muesca de nariz)
        base = h / 2 * (0.9 - 0.55 * t ** 4)
        nariz = h * muesca * math.exp(-(t / 0.22) ** 2)
        by = base - nariz
        pts_top.append((cx + w / 2 * t, cy + ty))
        pts_bot.append((cx + w / 2 * t, cy + by))
    return pts_top + pts_bot[::-1]


def antifaz_mariposa(data, tema="safari"):
    """Hoja con 2 antifaces (color pleno y tinte claro) con medidas reales."""
    acc = _accent(tema)
    im, dr = _hoja("ANTIFAZ · elástico por los anillos laterales", acc)

    w, h = _mm(165), _mm(75)             # 16.5 x 7.5 cm
    ojo_w, ojo_h = _mm(34), _mm(25)      # agujero de ojo
    sep_ojos = _mm(55)                   # centros a 55mm (3 a 10 años)

    for fila, color in enumerate((acc, _tint(acc, 0.45))):
        capa = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
        cd = ImageDraw.Draw(capa)
        cx, cy = Wp / 2, _mm(75) + fila * _mm(110)
        cd.polygon(_forma_antifaz(cx, cy, w, h), fill=color)
        # decoración: puntitos del tinte opuesto en las alas
        deco = _tint(acc, 0.75) if fila == 0 else acc
        for side in (-1, 1):
            for k in range(3):
                px_ = cx + side * (w * 0.28 + k * w * 0.075)
                py_ = cy - h * 0.12 + (k % 2) * h * 0.16
                r = _mm(2.6)
                cd.ellipse([px_ - r, py_ - r, px_ + r, py_ + r], fill=deco)
        # ojos (se RECORTAN: van en blanco con borde de corte)
        for side in (-1, 1):
            ox = cx + side * sep_ojos / 2
            cd.ellipse([ox - ojo_w / 2, cy - ojo_h / 2, ox + ojo_w / 2, cy + ojo_h / 2],
                       fill=(255, 255, 255, 255), outline=(90, 80, 70), width=5)
        capa = _contorno_blanco(capa, 8)
        im.alpha_composite(capa)
        dr2 = ImageDraw.Draw(im)
        for side in (-1, 1):
            _refuerzo_elastico(dr2, cx + side * (w / 2 - _mm(7)), cy, color)

    pj = _personaje(tema)
    if pj:
        _paste_h(im, pj, Wp * 0.5, Hp - _mm(60), _mm(52))
    _pie(dr, "Recortá el antifaz y los OJOS. Elástico de ~45cm por los anillos.", acc,
         y=Hp - _mm(28))
    return im


def _bigote(cd, cx, cy, w, color):
    """Bigote 'handlebar' clásico: MUESCA central arriba (donde apoya la nariz),
    una joroba redondeada por ala, y la punta se afina y sube en rulo."""
    N = 60
    for side in (-1, 1):
        arriba, abajo = [], []
        for i in range(N + 1):
            t = i / N                                    # 0=centro .. 1=punta
            x = cx + side * w * 0.53 * t
            # borde superior: bajo en el centro (muesca), joroba a mitad de ala
            ty = cy - w * (0.035 + 0.125 * math.sin(math.pi * t) ** 1.3)
            # borde inferior: casi plano, sube suave hacia la punta
            by = cy + w * (0.100 * (1 - t ** 1.7))
            arriba.append((x, ty))
            abajo.append((x, by))
        cd.polygon(arriba + abajo[::-1], fill=color)
        # rulo de la punta (sube)
        tx = cx + side * w * 0.545
        ty = cy - w * 0.055
        r2 = w * 0.040
        cd.ellipse([tx - r2, ty - r2, tx + r2, ty + r2], fill=color)


def _marca_palito(dr, x, y1, y2, acc):
    """Zona del palito (al COSTADO, no al centro — tapa la cara)."""
    dr.rounded_rectangle([x - _mm(4), y1, x + _mm(4), y2], _mm(3),
                         outline=_tint(acc, 0.35), width=5)
    dr.text((x, y2 + _mm(9)), "palito acá\n(por atrás)", font=_font(30, False),
            fill=_tint(INK, 0.4), anchor="mm", align="center")


def bigotes(data, tema="safari"):
    """Hoja con 3 bigotes grandes (~12cm), uno por franja, sin superposiciones."""
    acc = _accent(tema)
    im, dr = _hoja("BIGOTES · pegalos a un palito por atrás", acc)
    colores = [(70, 50, 40), acc, (30, 30, 34)]
    w = _mm(120)
    for i, color in enumerate(colores):
        capa = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
        cd = ImageDraw.Draw(capa)
        cy = _mm(70) + i * _mm(75)
        _bigote(cd, Wp / 2, cy, w, color)
        capa = _contorno_blanco(capa, 8)
        im.alpha_composite(capa)
        # bien separada del rulo de la punta (antes lo tocaba y arruinaba el corte)
        _marca_palito(ImageDraw.Draw(im), Wp / 2 + w * 0.70, cy - _mm(2), cy + _mm(16), acc)
    _pie(dr, "Palito de brochette de ~25cm, pegado con cinta al costado.", acc, y=Hp - _mm(28))
    return im


def lentes_fiesta(data, tema="safari"):
    """Hoja con 2 lentes de photo booth (~17cm), marcos gruesos, en palito."""
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip()
    im, dr = _hoja("LENTES · pegalos a un palito por atrás", acc)

    w_total = _mm(170)
    r_marco = _mm(29)                     # radio exterior de cada aro
    r_vidrio = _mm(21)                    # agujero (se recorta)
    sep = _mm(60)                         # centros de los aros

    for fila, (color, estrella) in enumerate(((acc, True), (_tint(acc, 0.4), False))):
        capa = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
        cd = ImageDraw.Draw(capa)
        cx, cy = Wp / 2, _mm(80) + fila * _mm(105)
        for side in (-1, 1):
            ox = cx + side * sep / 2
            if estrella:                  # marco estrella (5 puntas)
                pts = []
                for k in range(10):
                    ang = -math.pi / 2 + k * math.pi / 5
                    rr = r_marco * 1.28 if k % 2 == 0 else r_marco * 0.78
                    pts.append((ox + rr * math.cos(ang), cy + rr * math.sin(ang)))
                cd.polygon(pts, fill=color)
                # vidrio más chico en la estrella: con el mismo radio del redondo
                # llegaba hasta los vértices internos y las puntas quedaban casi
                # separadas del aro (débil al recortar)
                rv = _mm(16)
            else:
                cd.ellipse([ox - r_marco, cy - r_marco, ox + r_marco, cy + r_marco], fill=color)
                rv = r_vidrio
            cd.ellipse([ox - rv, cy - rv, ox + rv, cy + rv],
                       fill=(255, 255, 255, 255), outline=(90, 80, 70), width=5)
        # puente + patillas: más largas y METIDAS 12mm adentro del marco — la
        # unión con el aro/estrella queda sólida (antes apenas tocaban el borde
        # y en la estrella podían caer justo entre dos puntas).
        cd.rounded_rectangle([cx - _mm(9), cy - _mm(4), cx + _mm(9), cy + _mm(4)], _mm(2), fill=color)
        # solape hacia adentro: 12mm en la estrella (tiene que atravesar el valle
        # entre puntas), 6mm en el aro redondo (con 12 asomaba dentro del vidrio)
        solape = _mm(12) if estrella else _mm(6)
        for side in (-1, 1):
            e_in = cx + side * (sep / 2 + r_marco - solape)
            e_out = cx + side * (sep / 2 + r_marco + _mm(18))
            cd.rounded_rectangle([min(e_in, e_out), cy - _mm(3.4),
                                  max(e_in, e_out), cy + _mm(3.4)], _mm(2), fill=color)
        capa = _contorno_blanco(capa, 8)
        im.alpha_composite(capa)
        # separada de la patilla (que ahora termina en sep/2 + r_marco + 18mm)
        _marca_palito(ImageDraw.Draw(im), cx + sep / 2 + r_marco + _mm(27), cy - _mm(2), cy + _mm(16), acc)

    # SIN nombre (Pablo 9-jul-2026: los props del photo booth son para todos
    # los invitados — nada personalizado en la hoja)
    pj = _personaje(tema)
    if pj:
        _paste_h(im, pj, Wp * 0.5, Hp - _mm(62), _mm(50))
    _pie(dr, "Recortá los lentes y los VIDRIOS. Palito al costado, por atrás.", acc, y=Hp - _mm(28))
    return im


def piezas(data, tema="safari"):
    return [("1_antifaz", lambda d: antifaz_mariposa(d, tema), True),
            ("2_bigotes", lambda d: bigotes(d, tema), True),
            ("3_lentes", lambda d: lentes_fiesta(d, tema), True)]


if __name__ == "__main__":
    tema = "safari"
    d = {"nombre": "Luna", "edad": "4"}
    antifaz_mariposa(d, tema).convert("RGB").save("/tmp/antifaz.png")
    bigotes(d, tema).convert("RGB").save("/tmp/bigotes.png")
    lentes_fiesta(d, tema).convert("RGB").save("/tmp/lentes.png")
    print("OK")
