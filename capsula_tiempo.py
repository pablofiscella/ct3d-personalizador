"""Cápsula del tiempo — carta para el futuro.

REDISEÑO 8-jul-2026 (skill armar-kit §12 — antes: «NO ABRIR HASTA tus {edad}
años» usaba la edad ACTUAL (bug lógico: ya los tenía), una mesa dentro del
"sello", 60% de la página vacía, 150dpi → A5):
- 300dpi real (A4 = 2480x3508).
- El destino se calcula: no abrir hasta los 18 (año actual + (18 - edad)) —
  «NO ABRIR HASTA TUS 18 AÑOS (2040)». Si viene `destino` explícito, se respeta.
- Sobre con fondo IA del tema (fondos_ia.py, pieza "capsula": arte con zona
  central clara) si existe; fallback procedural.
- Snapshot del año en la carta (skill: tarjeta "del año"): edad, mejor amigo,
  comida, canción — lo que los kits comerciales incluyen.
- El texto SIEMPRE lo escribe el motor."""
import os, json, glob
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
_PXMM = 2480 / 210.0
Wp, Hp = 2480, 3508
CREAM = (253, 250, 242)
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


def _anyo_actual():
    import datetime
    return datetime.date.today().year


def _destino(data):
    """«NO ABRIR HASTA ...»: hasta los 18 años (calculado con la edad actual).
    Bug histórico: usaba la edad ACTUAL («no abrir hasta tus 4 años» para un
    nene de 4). Si el pedido trae `destino` explícito, se respeta."""
    d = str(data.get("destino") or "").strip()
    if d:
        return d, None
    try:
        edad = int(str(data.get("edad") or "5").strip())
    except ValueError:
        edad = 5
    anyo_apertura = _anyo_actual() + max(1, 18 - edad)
    return "TUS 18 AÑOS", anyo_apertura


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
        return fondos_ia.cargar_fondo(tema, "capsula")
    except Exception:
        return None


def portada_sobre(data, tema="safari"):
    """Frente del sobre: «NO ABRIR HASTA...» apaisado en media hoja, para doblar
    y pegar sobre un sobre real (o usar como tapa de la caja de recuerdos)."""
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip() or "______________"
    destino, anyo = _destino(data)

    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)
    dr.text((60, 55), "CÁPSULA DEL TIEMPO · frente del sobre", font=_font(44, False),
            fill=_tint(acc, 0.3))

    # zona del sobre: apaisada, proporción sobre C5 (~16.5x11)
    sx0, sy0 = _mm(15), _mm(28)
    sw = Wp - 2 * sx0
    sh = sw * 11 / 16.5
    fondo = _fondo(tema)
    if fondo is not None:
        zona = fondo.resize((int(sw), int(sh)), Image.LANCZOS)
        im.alpha_composite(zona, (int(sx0), int(sy0)))
        dr = ImageDraw.Draw(im)
        dr.rounded_rectangle([sx0, sy0, sx0 + sw, sy0 + sh], _mm(4), outline=acc, width=8)
    else:
        dr.rounded_rectangle([sx0, sy0, sx0 + sw, sy0 + sh], _mm(4),
                             fill=_tint(acc, 0.92) + (255,), outline=acc, width=8)
        dr.rounded_rectangle([sx0 + _mm(4), sy0 + _mm(4), sx0 + sw - _mm(4), sy0 + sh - _mm(4)],
                             _mm(3), outline=_tint(acc, 0.5), width=4)
        pjs = _personajes(tema, 2)
        if pjs:
            spots = [(sx0 + _mm(22), sy0 + sh - _mm(24)), (sx0 + sw - _mm(22), sy0 + sh - _mm(24))][:len(pjs)]
            for p, (px_, py_) in zip(pjs, spots):
                _paste_h(im, p, px_, py_, _mm(34))
            dr = ImageDraw.Draw(im)

    cx = Wp / 2
    # etiqueta central (siempre del motor, sobre la zona clara del arte)
    et_w, et_h = sw * 0.64, sh * 0.46
    ex0, ey0 = cx - et_w / 2, sy0 + sh * 0.27
    dr.rounded_rectangle([ex0, ey0, ex0 + et_w, ey0 + et_h], _mm(5),
                         fill=(255, 255, 255, 242), outline=acc, width=8)
    dr.text((cx, ey0 + et_h * 0.20), "NO ABRIR HASTA", font=_font(72), fill=acc, anchor="mm")
    fs = 130
    while _font(fs).getbbox(destino)[2] > et_w * 0.86 and fs > 48:
        fs -= 4
    dr.text((cx, ey0 + et_h * 0.52), destino, font=_font(fs), fill=INK, anchor="mm")
    if anyo:
        dr.text((cx, ey0 + et_h * 0.82), "(en el año %d)" % anyo,
                font=_font(56, False), fill=_tint(INK, 0.25), anchor="mm")

    # de/para + fecha de sellado
    y = sy0 + sh + _mm(16)
    dr.text((cx, y), "Guardado por %s, a sus %s años, en %d" %
            (nombre, str(data.get("edad") or "—"), _anyo_actual()),
            font=_font(54, False), fill=INK, anchor="mm")

    # checklist de qué guardar (skill §12: los kits comerciales lo traen)
    y += _mm(18)
    dr.text((cx, y), "¿Qué guardamos adentro?", font=_font(58), fill=acc, anchor="mm")
    items = ["Una foto de hoy", "Un dibujo hecho por vos", "La carta para tu yo del futuro",
             "Una entrada, sticker o recuerdo de la fiesta", "Algo chiquito que hoy te encante"]
    y += _mm(12)
    for t in items:
        dr.rectangle([cx - _mm(62), y - _mm(2.6), cx - _mm(56.8), y + _mm(2.6)],
                     outline=INK, width=4)
        dr.text((cx - _mm(52), y), t, font=_font(48, False), fill=_tint(INK, 0.15), anchor="lm")
        y += _mm(10)

    dr.text((cx, Hp - _mm(11)), "casatridimensional.com.ar", font=_font(36, False),
            fill=(180, 180, 180), anchor="mm")
    return im


def hoja_carta(data, tema="safari"):
    """Carta para el futuro + snapshot del año (para completar a mano)."""
    acc = _accent(tema)
    edad = str(data.get("edad") or "").strip() or "—"

    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)

    dr.rounded_rectangle([_mm(15), _mm(12), Wp - _mm(15), _mm(34)], _mm(5), fill=acc)
    dr.text((Wp / 2, _mm(23)), "CARTA PARA MI YO DEL FUTURO", font=_font(76), fill="white", anchor="mm")

    preguntas = [
        "¿Cuál es tu comida favorita?",
        "¿Qué querés ser cuando seas grande?",
        "¿Quién es tu mejor amigo/a?",
        "¿Cuál es tu juego favorito?",
        "¿Qué fue lo más divertido de tus %s años?" % edad,
    ]
    y = _mm(44)
    for i, p in enumerate(preguntas):
        dr.text((_mm(18), y), "%d. %s" % (i + 1, p), font=_font(54), fill=INK, anchor="la")
        for j in range(2):
            ly = y + _mm(11) + j * _mm(8)
            dr.line([_mm(18), ly, Wp - _mm(18), ly], fill=_tint(INK, 0.72), width=3)
        y += _mm(30)

    # snapshot del año (lo completan los papás)
    dr.rounded_rectangle([_mm(15), y, Wp - _mm(15), y + _mm(34)], _mm(4),
                         outline=_tint(acc, 0.35), width=5)
    dr.text((_mm(20), y + _mm(6)), "FOTO DEL AÑO (para completar los grandes):",
            font=_font(46), fill=acc, anchor="lm")
    dr.text((_mm(20), y + _mm(15)), "La canción del momento: ______________________     "
            "Lo que más decís: ______________________",
            font=_font(42, False), fill=_tint(INK, 0.2), anchor="lm")
    dr.text((_mm(20), y + _mm(24)), "Tu programa favorito: ______________________     "
            "Un precio de hoy (helado): $__________",
            font=_font(42, False), fill=_tint(INK, 0.2), anchor="lm")
    y += _mm(40)

    dr.rounded_rectangle([_mm(18), y, Wp - _mm(18), Hp - _mm(24)], _mm(4),
                         outline=_tint(acc, 0.35), width=5)
    dr.text((Wp / 2, y + _mm(9)), "Dibujá algo de tu cumpleaños",
            font=_font(48, False), fill=_tint(INK, 0.3), anchor="mm")

    dr.text((Wp / 2, Hp - _mm(11)), "casatridimensional.com.ar", font=_font(36, False),
            fill=(180, 180, 180), anchor="mm")
    return im


def piezas(data, tema="safari"):
    return [("1_sobre", lambda d: portada_sobre(d, tema), True),
            ("2_carta", lambda d: hoja_carta(d, tema), True)]


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Emma"
    edad = sys.argv[3] if len(sys.argv) > 3 else "5"
    out = sys.argv[4] if len(sys.argv) > 4 else "/tmp/capsula"
    d = {"nombre": nombre, "edad": edad}
    portada_sobre(d, tema).convert("RGB").save(f"{out}_sobre.png")
    hoja_carta(d, tema).convert("RGB").save(f"{out}_carta.png")
    print(f"OK -> {out}_sobre.png + {out}_carta.png")
