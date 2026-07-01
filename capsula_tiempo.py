"""Cápsula del tiempo — carta para el futuro.
Sobre/carta personalizada para guardar recuerdos y abrir en X años.
Tres versiones: 5, 10 y 18 años.
Incluye diseño de sobre + hoja de carta + sello de "No abrir hasta..."."""
import os, json, glob
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


def _anyo_actual():
    import datetime
    return datetime.date.today().year


def _personajes(tema, n=1):
    try:
        import cuaderno
        return cuaderno.personajes_decorativos(tema, n)
    except Exception:
        return []


def _paste_h(base, img, cx, cy, h):
    w = max(1, int(img.width * h / img.height))
    base.alpha_composite(img.resize((w, int(h)), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))


def portada_sobre(data, tema="safari"):
    """Portada del sobre: 'NO ABRIR HASTA...' con sello decorativo."""
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip() or "______________"
    edad = str(data.get("edad") or "").strip() or "5"
    destino = data.get("destino") or "tus %s años" % edad

    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=_tint(CREAM, 0.3))

    dr.rounded_rectangle([80, 80, Wp - 80, Hp - 220], 40, outline=acc, width=6)
    dr.rounded_rectangle([110, 110, Wp - 110, Hp - 250], 30, outline=_tint(acc, 0.4), width=3)

    dr.ellipse([Wp / 2 - 120, 220, Wp / 2 + 120, 460], outline=acc, width=8)
    personajes = _personajes(tema, 1)
    if personajes:
        _paste_h(im, personajes[0], Wp / 2, 320, 160)
    dr.text((Wp / 2, 390), "CÁPSULA", font=_font(40), fill=acc, anchor="mm")

    dr.text((Wp / 2, 550), "NO ABRIR HASTA", font=_font(52), fill=acc, anchor="mm")

    fs = 90
    while _font(fs).getbbox(destino)[2] > Wp - 300 and fs > 30:
        fs -= 4
    dr.text((Wp / 2, 680), destino, font=_font(fs), fill=INK, anchor="mm")

    dr.text((Wp / 2, 820), "Para: %s" % nombre, font=_font(38, False), fill=INK, anchor="mm")
    dr.text((Wp / 2, 890), "%d — %s" % (_anyo_actual(), "no te olvides de abrirlo"),
            font=_font(24, False), fill=_tint(INK, 0.3), anchor="mm")

    dr.line([Wp * 0.15, Hp - 280, Wp * 0.45, Hp - 280], fill=acc, width=2)
    dr.text((Wp * 0.3, Hp - 265), "Firma", font=_font(22, False), fill=_tint(INK, 0.3), anchor="mm")

    return im


def hoja_carta(data, tema="safari"):
    """Hoja interna con preguntas para responder y espacio para dibujar."""
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip() or "______________"

    im = Image.new("RGBA", (Wp, Hp), (255, 255, 255, 255))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, Wp, Hp], fill=CREAM)

    dr.rounded_rectangle([80, 60, Wp - 80, 180], 25, fill=acc)
    dr.text((Wp / 2, 120), "CARTA PARA MI YO DEL FUTURO", font=_font(38), fill="white", anchor="mm")

    personajes = _personajes(tema, 1)
    if personajes:
        _paste_h(im, personajes[0], Wp - 170, 118, 130)

    preguntas = [
        "¿Cuál es tu comida favorita?",
        "¿Qué querés ser cuando seas grande?",
        "¿Quién es tu mejor amigo/a?",
        "¿Cuál es tu juego favorito?",
        "¿Qué fue lo más divertido de tus %s años?" % str(data.get("edad") or ""),
    ]
    y = 240
    for i, p in enumerate(preguntas):
        dr.text((120, y), "%d. %s" % (i + 1, p), font=_font(28), fill=INK, anchor="la")
        for j in range(3):
            ly = y + 50 + j * 36
            dr.line([120, ly, Wp - 120, ly], fill=_tint(INK, 0.7), width=2)
        y += 160

    dr.rounded_rectangle([120, y + 20, Wp - 120, Hp - 120], 20, outline=_tint(acc, 0.3), width=3)
    dr.text((Wp / 2, y + 60), "Dibujá algo de tu cumpleaños", font=_font(26, False), fill=_tint(INK, 0.3), anchor="mm")

    dr.text((Wp / 2, Hp - 50), "casatridimensional.com.ar", font=_font(18, False), fill=(180, 180, 180), anchor="mm")
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
    d = {"nombre": nombre, "edad": edad, "destino": "tus 18 años"}
    portada_sobre(d, tema).convert("RGB").save(f"{out}_sobre.png")
    hoja_carta(d, tema).convert("RGB").save(f"{out}_carta.png")
    print(f"OK -> {out}_sobre.png + {out}_carta.png")
