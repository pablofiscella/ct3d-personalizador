"""Juego de la memoria personalizado — cartas con los personajes del tema.

REDISEÑO 8-jul-2026 (skill armar-kit §8 — antes: dorso desalineado ~15mm del
frente (la impresión doble faz no coincidía), pares casi idénticos entre sí
(injugable a los 4 años), cartas de 3cm por el bug de DPI):
- 300dpi real: cartas CUADRADAS de 63x63mm (el estándar de la industria),
  grilla 3x4 = 12 cartas (6 pares) por hoja, esquinas redondeadas.
- El DORSO usa EXACTAMENTE la misma grilla que el frente, ESPEJADA en X —
  al imprimir doble faz (voltear por el borde largo) cada dorso cae justo
  detrás de su carta. Una sola función de grilla para ambas caras = imposible
  que se desalineen de nuevo.
- Pares IDÉNTICOS (misma imagen) y pares bien DISTINTOS entre sí: personajes
  del tema vía personajes_decorativos (filtro visión + dedup); si el tema no
  llega a 6 figuras distintas, completa con íconos geométricos.
- Dorso: fondo IA del tema (fondos_ia.py "memoria_dorso": patrón denso, no se
  transparenta) si existe; fallback patrón procedural denso.
- Marcas de corte finas fuera de las cartas (skill §1)."""
import os, json, glob, math, random
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
TEMAS = os.path.join(KIT, "temas")
_PXMM = 2480 / 210.0
Wp, Hp = 2480, 3508
CREAM = (253, 250, 242)
INK = (60, 50, 45)
CORTE = (150, 150, 150)


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


def _fit_into(img, mw, mh):
    r = min(mw / img.width, mh / img.height)
    return img.resize((max(1, int(img.width * r)), max(1, int(img.height * r))), Image.LANCZOS)


def _dibujar_forma(forma, size, color):
    """Ícono geométrico (relleno cuando el tema no tiene 6 figuras distintas)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    m = size * 0.14
    cx = cy = size / 2
    if forma == "circulo":
        dr.ellipse([m, m, size - m, size - m], fill=color)
    elif forma == "cuadrado":
        dr.rounded_rectangle([m, m, size - m, size - m], size * 0.15, fill=color)
    elif forma == "triangulo":
        dr.polygon([(cx, m), (size - m, size - m), (m, size - m)], fill=color)
    elif forma == "diamante":
        dr.polygon([(cx, m), (size - m, cy), (cx, size - m), (m, cy)], fill=color)
    elif forma == "estrella":
        ro, ri = (size - 2 * m) / 2, (size - 2 * m) / 2 * 0.42
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            r = ro if i % 2 == 0 else ri
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        dr.polygon(pts, fill=color)
    elif forma == "corazon":
        r = (size - 2 * m) / 4
        dr.ellipse([cx - 2 * r, cy - 2 * r, cx, cy], fill=color)
        dr.ellipse([cx, cy - 2 * r, cx + 2 * r, cy], fill=color)
        dr.polygon([(cx - 2 * r, cy - r * 0.6), (cx + 2 * r, cy - r * 0.6), (cx, size - m)], fill=color)
    return im


def _imagenes_pares(tema, n=6):
    """n imágenes bien DISTINTAS para los pares: personajes del tema con
    variedad ESTRICTA (un solo personaje por tipo — dos leones apenas distintos
    como pares diferentes hacían el juego injugable), completando con íconos
    geométricos si no alcanzan."""
    imgs = []
    try:
        import cuaderno
        imgs = cuaderno.personajes_decorativos(tema, n, variedad_estricta=True)
    except Exception:
        imgs = []
    if len(imgs) < n:
        acc = _accent(tema)
        formas = ["estrella", "corazon", "circulo", "triangulo", "diamante", "cuadrado"]
        combos = [(f, c) for c in (acc, _tint(acc, 0.45)) for f in formas]
        for f, c in combos[:max(0, n - len(imgs))]:
            imgs.append(_dibujar_forma(f, 600, c))
    return imgs[:n]


# ---- grilla ÚNICA para frente y dorso (espejada en X para doble faz) ----
_COLS, _FILAS = 3, 4
_LADO = None            # se calcula: 63mm


def _celdas(espejo=False):
    """Centros (cx, cy) de las 12 cartas. espejo=True invierte las columnas —
    es lo que hace coincidir el dorso con el frente al imprimir doble faz
    (voltear por el borde largo). MISMA función para ambas caras: no pueden
    volver a desalinearse (bug real: 15mm de corrimiento).
    Carta de 60mm (el estándar es 63, pero 4 filas de 63 + título no entran
    en A4 — 60mm sigue siendo talle toddler-friendly)."""
    lado = _mm(60)
    gap = _mm(6)
    total_w = _COLS * lado + (_COLS - 1) * gap
    total_h = _FILAS * lado + (_FILAS - 1) * gap
    x0 = (Wp - total_w) / 2 + lado / 2
    y0 = _mm(27) + lado / 2
    out = []
    for f in range(_FILAS):
        for c in range(_COLS):
            cc = (_COLS - 1 - c) if espejo else c
            out.append((x0 + cc * (lado + gap), y0 + f * (lado + gap)))
    return out, lado


def _fondo_dorso(tema):
    try:
        import fondos_ia
        return fondos_ia.cargar_fondo(tema, "memoria_dorso")
    except Exception:
        return None


def generar_memoria(data, tema="safari"):
    """Frente: 12 cartas (6 pares idénticos) de 63mm, con personajes del tema."""
    acc = _accent(tema)
    nombre = str(data.get("nombre") or "").strip() or "MI MEMORIA"

    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)
    dr.text((60, 55), "JUEGO DE LA MEMORIA · el memo de %s" % nombre,
            font=_font(44, False), fill=_tint(acc, 0.3))

    # instrucciones ARRIBA (entre título y grilla): abajo quedaban cortadas por
    # el borde de la hoja con la grilla de 4 filas
    dr.text((Wp / 2, _mm(14)), "Recortá las cartas, dalas vuelta y encontrá los pares.",
            font=_font(44, False), fill=_tint(INK, 0.25), anchor="mm")
    dr.text((Wp / 2, _mm(21)),
            "Para 2-4 años: jueguen con 3-4 pares primero y vayan sumando.",
            font=_font(38, False), fill=_tint(INK, 0.4), anchor="mm")

    celdas, lado = _celdas(espejo=False)
    base = _imagenes_pares(tema, len(celdas) // 2)
    cartas = []
    for i, img in enumerate(base):
        cartas.append((i, img))
        cartas.append((i, img))
    rnd = random.Random(42)          # determinístico: mismas posiciones siempre
    rnd.shuffle(cartas)

    for (cx, cy), (par_idx, img) in zip(celdas, cartas):
        dr.rounded_rectangle([cx - lado / 2, cy - lado / 2, cx + lado / 2, cy + lado / 2],
                             _mm(5), fill=(255, 255, 255, 255), outline=_tint(acc, 0.35), width=5)
        fit = _fit_into(img, lado - _mm(12), lado - _mm(12))
        im.alpha_composite(fit, (int(cx - fit.width / 2), int(cy - fit.height / 2)))

    dr.text((Wp / 2, Hp - _mm(6)), "casatridimensional.com.ar", font=_font(36, False),
            fill=(180, 180, 180), anchor="mm")
    return im


def dorso_memoria(data, tema="safari"):
    """Dorso: la MISMA grilla espejada en X + patrón denso (IA del tema si hay;
    procedural si no) — idéntico en las 12 cartas, no se transparenta."""
    acc = _accent(tema)
    im = Image.new("RGBA", (Wp, Hp), CREAM + (255,))
    dr = ImageDraw.Draw(im)
    dr.text((60, 55), "DORSO · imprimir del otro lado (doble faz, borde largo)",
            font=_font(44, False), fill=_tint(acc, 0.3))

    celdas, lado = _celdas(espejo=True)

    fondo = _fondo_dorso(tema)
    if fondo is not None:
        import fondos_ia
        patron = fondos_ia.cover(fondo, lado, lado)
    else:
        patron = Image.new("RGBA", (int(lado), int(lado)), _tint(acc, 0.25) + (255,))
        pd = ImageDraw.Draw(patron)
        rnd = random.Random(7)
        for _ in range(70):                      # patrón denso (anti-transparencia)
            x, y = rnd.uniform(0, lado), rnd.uniform(0, lado)
            r = rnd.uniform(_mm(1.2), _mm(3))
            pd.ellipse([x - r, y - r, x + r, y + r],
                       fill=_tint(acc, rnd.choice((0.45, 0.6))))

    mask = Image.new("L", (int(lado), int(lado)), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, lado - 1, lado - 1], _mm(5), fill=255)
    for cx, cy in celdas:
        im.paste(patron, (int(cx - lado / 2), int(cy - lado / 2)), mask)
        dr.rounded_rectangle([cx - lado / 2, cy - lado / 2, cx + lado / 2, cy + lado / 2],
                             _mm(5), outline=_tint(acc, 0.2), width=5)

    dr.text((Wp / 2, Hp - _mm(11)), "casatridimensional.com.ar", font=_font(36, False),
            fill=(180, 180, 180), anchor="mm")
    return im


def piezas(data, tema="safari"):
    return [("1_cartas_memoria", lambda d: generar_memoria(d, tema), True),
            ("2_dorso", lambda d: dorso_memoria(d, tema), True)]


if __name__ == "__main__":
    import sys
    tema = sys.argv[1] if len(sys.argv) > 1 else "safari"
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Benicio"
    out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/memoria"
    d = {"nombre": nombre, "edad": "5"}
    generar_memoria(d, tema).convert("RGB").save(f"{out}_cartas.png")
    dorso_memoria(d, tema).convert("RGB").save(f"{out}_dorso.png")
    print(f"OK -> {out}_cartas.png + {out}_dorso.png")
