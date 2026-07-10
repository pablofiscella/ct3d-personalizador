#!/usr/bin/env python3
"""Las 7 piezas del kit "Un Añito Salvaje".
- invitacion y cartel: motor por-spec (generador.render).
- topper, cupcakes, banderines, etiquetas, tags: builders procedurales (hojas
  de impresion A4 con grilla para recortar).
Genera PNG + PDF (300 DPI) de cada pieza y una grilla de revision.
"""
import os, json
from PIL import Image, ImageDraw, ImageChops, ImageFilter
from generador import (ASSETS, OUT, DPI, CREAM, BROWN, TERRA, OLIVE,
                       fit_font, get_font, crop_alpha, render, SPECS, specs_de, _hex_rgb)

SAGE = (138, 154, 91)
MUST = (224, 164, 88)
WHITE = (255, 255, 255)
A4 = (2480, 3508)  # 210x297mm @300dpi

ANIMALS = ["leon.png", "jirafa.png", "monito.png", "elefante.png", "cebra.png"]

# ---- textos según la edad elegida (1/2/3) ----
def _edad(data):
    e = str(data.get("edad", "1")).strip()
    return e if e in ("1", "2", "3") else "1"
def lema_edad(data):
    return {"1": "¡Un añito salvaje!", "2": "¡Dos añitos salvajes!",
            "3": "¡Tres añitos salvajes!"}[_edad(data)]
def titulo_edad(data):
    return {"1": "El primer añito de", "2": "Los dos añitos de",
            "3": "Los tres añitos de"}[_edad(data)]

_PROY = os.path.dirname(os.path.abspath(__file__))
def _tema_recortes(tema):
    return os.path.join(_PROY, "temas", tema or "safari", "recortes")

_cache = {}
def load(name, tema=None):
    """Carga un asset recortado. Busca primero en la temática, si no en el global (safari)."""
    key = (tema, name)
    if key not in _cache:
        p = os.path.join(_tema_recortes(tema), name) if tema else None
        if not p or not os.path.isfile(p):
            p = os.path.join(ASSETS, name)
        _cache[key] = crop_alpha(Image.open(p).convert("RGBA"))
    return _cache[key].copy()

def animales(tema=None):
    """Lista de animalitos de una temática (PNGs en su carpeta recortes, menos los 'numero')."""
    if tema:
        rdir = _tema_recortes(tema)
        if os.path.isdir(rdir):
            fs = sorted(f for f in os.listdir(rdir) if f.endswith(".png") and not f.startswith("numero"))
            if fs:
                return fs
    return ANIMALS

def fit_into(im, mw, mh):
    r = min(mw / im.width, mh / im.height)
    return im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)

def paste_center(base, im, cx, cy):
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def txt(d, text, cx, cy, font_file, size, color, maxw, wght=None, anchor="mm"):
    if not str(text).strip():
        return
    f = fit_font(d, str(text), font_file, int(size), int(maxw), wght)
    d.text((cx, cy), str(text), font=f, fill=color, anchor=anchor)

def make_sheet(cell_fn, cols, rows, page=A4, margin=120, gap=40, bg=WHITE):
    W, H = page
    sheet = Image.new("RGBA", (W, H), bg + (255,))
    cw = (W - 2 * margin - (cols - 1) * gap) // cols
    ch = (H - 2 * margin - (rows - 1) * gap) // rows
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            cell = cell_fn(i, cw, ch)
            if cell is not None:
                sheet.alpha_composite(cell, (margin + c * (cw + gap), margin + r * (ch + gap)))
    return sheet

# ---------------- Pieza 3: Topper de torta (5x5") ----------------
def topper_torta(data, tema=None):
    W = H = 1500
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    m = 36
    d.ellipse([m, m, W - m, H - m], fill=CREAM + (255,), outline=OLIVE + (255,), width=10)
    for i, a in enumerate(animales(tema)[:3]):
        paste_center(base, fit_into(load(a, tema), 330, 330), W * (0.30 + 0.20 * i), H * 0.72)
    txt(d, titulo_edad(data), W / 2, H * 0.33, "Poppins-Medium.ttf", 56, BROWN, W * 0.62)
    txt(d, data["nombre"], W / 2, H * 0.45, "DancingScript-VF.ttf", 180, TERRA, W * 0.66, wght=700)
    txt(d, lema_edad(data), W / 2, H * 0.555, "Fredoka-VF.ttf", 58, OLIVE, W * 0.64, wght=600)
    return base

# ---------------- Pieza 4: Toppers de cupcakes (hoja A4, circulos 2") ----------------
def cupcakes(data, tema=None):
    e = _edad(data)
    lema_words = lema_edad(data).split()
    l1, l2 = " ".join(lema_words[:-1]), lema_words[-1]   # "¡Dos añitos" / "salvajes!"
    items = [("img", a) for a in animales(tema)] + [("num", None), ("name", None), ("lema", None)]
    def cell(i, cw, ch):
        c = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        d = ImageDraw.Draw(c)
        D = min(cw, ch)
        cx, cy = cw / 2, ch / 2
        d.ellipse([cx - D / 2, cy - D / 2, cx + D / 2, cy + D / 2],
                  fill=CREAM + (255,), outline=SAGE + (255,), width=8)
        kind, val = items[i % len(items)]
        if kind == "img":
            paste_center(c, fit_into(load(val, tema), D * 0.70, D * 0.70), cx, cy)
        elif kind == "num":
            paste_center(c, fit_into(load("numero_%s.png" % e, tema), D * 0.78, D * 0.78), cx, cy)
        elif kind == "name":
            txt(d, data["nombre"], cx, cy - D * 0.04, "DancingScript-VF.ttf", D * 0.34, TERRA, D * 0.72, wght=700)
            txt(d, "cumple " + e, cx, cy + D * 0.24, "Poppins-Medium.ttf", D * 0.11, BROWN, D * 0.7)
        else:
            txt(d, l1, cx, cy - D * 0.11, "Fredoka-VF.ttf", D * 0.15, OLIVE, D * 0.78, wght=600)
            txt(d, l2, cx, cy + D * 0.11, "Fredoka-VF.ttf", D * 0.15, OLIVE, D * 0.78, wght=600)
        return c
    return make_sheet(cell, 3, 4, gap=50)

# ---------------- Pieza 5: Etiquetas botellitas (hoja A4) ----------------
def etiquetas(data, tema=None):
    an = animales(tema)
    a0, a1 = an[0], an[1 % len(an)]
    def cell(i, cw, ch):
        c = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        d = ImageDraw.Draw(c)
        d.rounded_rectangle([4, 4, cw - 4, ch - 4], radius=30, fill=CREAM + (255,),
                            outline=SAGE + (255,), width=6)
        # animalitos más chicos, metidos hacia adentro (no pegados al borde)
        paste_center(c, fit_into(load(a0, tema), ch * 0.42, ch * 0.42), cw * 0.14, ch * 0.50)
        paste_center(c, fit_into(load(a1, tema), ch * 0.42, ch * 0.42), cw * 0.86, ch * 0.50)
        # nombre y lema con ancho acotado y MENOS espacio entre ellos
        txt(d, data["nombre"], cw / 2, ch * 0.42, "DancingScript-VF.ttf", ch * 0.38, TERRA, cw * 0.44, wght=700)
        txt(d, lema_edad(data), cw / 2, ch * 0.64, "Fredoka-VF.ttf", ch * 0.13, OLIVE, cw * 0.50, wght=600)
        return c
    return make_sheet(cell, 2, 5, gap=40)

# ---------------- Pieza 6: Tags de souvenir (hoja A4) ----------------
def tags(data, tema=None):
    an = animales(tema)
    def cell(i, cw, ch):
        c = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        d = ImageDraw.Draw(c)
        d.rounded_rectangle([4, 4, cw - 4, ch - 4], radius=34, fill=CREAM + (255,),
                            outline=SAGE + (255,), width=5)
        d.ellipse([cw / 2 - 22, 30, cw / 2 + 22, 74], outline=BROWN + (255,), width=6)
        txt(d, "¡Gracias por venir!", cw / 2, ch * 0.27, "Fredoka-VF.ttf", ch * 0.085, OLIVE, cw * 0.82, wght=600)
        paste_center(c, fit_into(load(an[i % len(an)], tema), cw * 0.5, ch * 0.34), cw / 2, ch * 0.55)
        txt(d, data["nombre"], cw / 2, ch * 0.84, "DancingScript-VF.ttf", ch * 0.17, TERRA, cw * 0.8, wght=700)
        return c
    return make_sheet(cell, 3, 4, gap=45)

# ---------------- Pieza 7: Banderines / guirnalda (hoja A4) ----------------
def _pennant(cw, ch, color, letter):
    c = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    pad = 12
    d.polygon([(pad, pad), (cw - pad, pad), (cw / 2, ch - pad)],
              fill=color + (255,), outline=BROWN + (255,))
    # dos agujeritos arriba para el hilo
    d.ellipse([cw * 0.18 - 16, 34, cw * 0.18 + 16, 66], outline=BROWN + (255,), width=5)
    d.ellipse([cw * 0.82 - 16, 34, cw * 0.82 + 16, 66], outline=BROWN + (255,), width=5)
    txt(d, letter, cw / 2, ch * 0.40, "Fredoka-VF.ttf", ch * 0.34, CREAM, cw * 0.6, wght=600)
    return c

def banderin(data, tema=None):
    letters = [ch for ch in data["nombre"].upper()]
    pal = kit_pal(tema)
    def cell(i, cw, ch):
        if i >= len(letters):
            return None
        return _pennant(cw, ch, pal[i % len(pal)], letters[i])
    rows = max(2, (len(letters) + 1) // 2)
    return make_sheet(cell, 2, rows, margin=150, gap=70)

# ============================================================
# Generalización por temática: si el tema NO tiene recortes (cutouts) como
# safari, las piezas se arman desde la lámina + config "kit" del tema.json.
# ============================================================
def _tema_json(tema):
    try:
        return json.load(open(os.path.join(_PROY, "temas", tema or "safari", "tema.json"), encoding="utf-8"))
    except Exception:
        return {}
def _kit(tema):
    return _tema_json(tema).get("kit") or {}
def accent(tema):  return (_hex_rgb(_kit(tema).get("accent")) or TERRA)
def ink_c(tema):   return (_hex_rgb(_kit(tema).get("ink")) or BROWN)
def font_disp(tema): return _kit(tema).get("font") or "DancingScript-VF.ttf"
def _edad_any(data):
    return str(data.get("edad", "1")).strip() or "1"
def lema(data, tema):
    t = _kit(tema).get("lema")
    if t: return t.format(edad=_edad_any(data))
    return lema_edad(data) if has_recortes(tema) else "¡Cumplo %s!" % _edad_any(data)
def titulo(data, tema):
    t = _kit(tema).get("titulo")
    if t: return t.format(edad=_edad_any(data), nombre=data.get("nombre", ""))
    return titulo_edad(data) if has_recortes(tema) else "El cumple de"
def has_recortes(tema):
    # safari (tema base) usa los recortes GLOBALES (/recortes); el resto, sólo si
    # tienen su propia carpeta recortes/ con cutouts. Si no, se arman desde la lámina.
    if (tema or "safari") == "safari":
        return True
    rdir = _tema_recortes(tema)
    try:
        return os.path.isdir(rdir) and any(
            f.endswith(".png") and not f.startswith("numero") for f in os.listdir(rdir))
    except Exception:
        return False
def kit_pal(tema):
    if has_recortes(tema):
        return [TERRA, MUST, SAGE, OLIVE]
    return [accent(tema), MUST, SAGE, OLIVE]

_lam_cache = {}
def _lamina(tema):
    key = tema or "safari"
    if key not in _lam_cache:
        p = os.path.join(_PROY, "temas", key, "invitacion_1.png")
        _lam_cache[key] = Image.open(p).convert("RGBA")
    return _lam_cache[key]
def _band(tema, frac=0.60):
    im = _lamina(tema); w, h = im.size
    return im.crop((0, int(h * frac), w, h)).copy()
def _circle_clip(content, box):
    mask = Image.new("L", content.size, 0)
    ImageDraw.Draw(mask).ellipse(box, fill=255)
    return Image.composite(content, Image.new("RGBA", content.size, (0, 0, 0, 0)), mask)

# ---- piezas desde lámina (temas sin recortes) ----
def topper_l(data, tema):
    W = H = 1500; m = 36; acc = accent(tema); ink = ink_c(tema); fnt = font_disp(tema)
    cont = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cont)
    d.ellipse([m, m, W - m, H - m], fill=CREAM + (255,))
    paste_center(cont, fit_into(_band(tema), int(W * 0.74), int(H * 0.34)), W * 0.5, H * 0.75)
    txt(d, titulo(data, tema), W / 2, H * 0.30, "Poppins-Medium.ttf", 54, ink, W * 0.60)
    txt(d, data["nombre"], W / 2, H * 0.42, fnt, 170, acc, W * 0.66, wght=700)
    txt(d, lema(data, tema), W / 2, H * 0.53, "Fredoka-VF.ttf", 56, acc, W * 0.64, wght=600)
    base = _circle_clip(cont, [m, m, W - m, H - m])
    ImageDraw.Draw(base).ellipse([m, m, W - m, H - m], outline=acc + (255,), width=10)
    return base

def cupcakes_l(data, tema):
    acc = accent(tema); ink = ink_c(tema); fnt = font_disp(tema)
    band = _band(tema); bw, bh = band.size; e = _edad_any(data)
    n = 6
    slices = [band.crop((int(k * bw / n), 0, int((k + 1) * bw / n), bh)) for k in range(n)]
    items = [("img", s) for s in slices] + [("num", None), ("name", None), ("lema", None)]
    def cell(i, cw, ch):
        D = min(cw, ch); cx, cy = cw / 2, ch / 2; box = [cx - D / 2, cy - D / 2, cx + D / 2, cy + D / 2]
        cont = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(cont)
        d.ellipse(box, fill=CREAM + (255,))
        kind, val = items[i % len(items)]
        if kind == "img":
            paste_center(cont, fit_into(val, D * 0.95, D * 0.95), cx, cy)
        elif kind == "num":
            txt(d, e, cx, cy, fnt, D * 0.6, acc, D * 0.8, wght=700)
        elif kind == "name":
            txt(d, data["nombre"], cx, cy - D * 0.04, fnt, D * 0.34, acc, D * 0.78, wght=700)
            txt(d, "cumple " + e, cx, cy + D * 0.24, "Poppins-Medium.ttf", D * 0.11, ink, D * 0.7)
        else:
            txt(d, lema(data, tema), cx, cy, "Fredoka-VF.ttf", D * 0.14, acc, D * 0.82, wght=600)
        c = _circle_clip(cont, box)
        ImageDraw.Draw(c).ellipse(box, outline=acc + (255,), width=8)
        return c
    return make_sheet(cell, 3, 4, gap=50)

def etiquetas_l(data, tema):
    acc = accent(tema); fnt = font_disp(tema)
    band = _band(tema); bw, bh = band.size
    left = band.crop((0, 0, int(bw * 0.33), bh)); right = band.crop((int(bw * 0.67), 0, bw, bh))
    def cell(i, cw, ch):
        c = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
        d.rounded_rectangle([4, 4, cw - 4, ch - 4], radius=30, fill=CREAM + (255,), outline=acc + (255,), width=6)
        paste_center(c, fit_into(left, ch * 0.5, ch * 0.6), cw * 0.13, ch * 0.5)
        paste_center(c, fit_into(right, ch * 0.5, ch * 0.6), cw * 0.87, ch * 0.5)
        txt(d, data["nombre"], cw / 2, ch * 0.42, fnt, ch * 0.36, acc, cw * 0.46, wght=700)
        txt(d, lema(data, tema), cw / 2, ch * 0.64, "Fredoka-VF.ttf", ch * 0.13, acc, cw * 0.5, wght=600)
        return c
    return make_sheet(cell, 2, 5, gap=40)

def tags_l(data, tema):
    acc = accent(tema); fnt = font_disp(tema); band = _band(tema)
    def cell(i, cw, ch):
        c = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
        d.rounded_rectangle([4, 4, cw - 4, ch - 4], radius=34, fill=CREAM + (255,), outline=acc + (255,), width=5)
        d.ellipse([cw / 2 - 22, 30, cw / 2 + 22, 74], outline=acc + (255,), width=6)
        txt(d, "¡Gracias por venir!", cw / 2, ch * 0.27, "Fredoka-VF.ttf", ch * 0.085, acc, cw * 0.82, wght=600)
        paste_center(c, fit_into(band, cw * 0.6, ch * 0.34), cw / 2, ch * 0.55)
        txt(d, data["nombre"], cw / 2, ch * 0.84, fnt, ch * 0.17, acc, cw * 0.8, wght=700)
        return c
    return make_sheet(cell, 3, 4, gap=45)

# ============================================================
def piezas_de(tema="safari"):
    """Las 7 piezas atadas a una temática. Safari (con recortes) usa los builders
    originales; los temas sin recortes los arman desde la lámina."""
    s = specs_de(tema)
    if has_recortes(tema):
        tp, cu, et, tg = topper_torta, cupcakes, etiquetas, tags
    else:
        tp, cu, et, tg = topper_l, cupcakes_l, etiquetas_l, tags_l
    return [
        ("1_invitacion", lambda d: render(d, s["invitacion"]), False),
        ("2_cartel",     lambda d: render(d, s["cartel"]),     False),
        ("3_topper_torta", lambda d: tp(d, tema), True),
        ("4_cupcake_toppers", lambda d: cu(d, tema),  True),
        ("5_etiquetas_botellita", lambda d: et(d, tema), True),
        ("6_tags_souvenir", lambda d: tg(d, tema),        True),
        ("7_banderines", lambda d: banderin(d, tema),       True),
    ]
PIEZAS = piezas_de("safari")   # compat

# ── Halo blanco (aro troquelado de sticker): quitar y agregar BIEN ──
# Los recortes de las hojas de stickers IA traen un aro blanco die-cut
# irregular. Error recurrente (Pablo 10-jul-2026): donde el personaje NO es un
# sticker el aro no va (y el quitado a medias deja flecos), y donde SÍ va
# sticker el contorno de la IA sale dispar. Estas dos funciones son LA fuente
# de verdad para ambos casos — usarlas en vez de reinventarlo por pieza.

def quitar_halo(im, umbral=205, defringe=1):
    """Saca el aro blanco del die-cut conservando los blancos DEL personaje
    (nubes, guantes, dientes). Reglas:
    - el aro es el casi-blanco alcanzable desde AFUERA sin cruzar el contorno
      oscuro del personaje (floodfill por blanco/transparente);
    - se siembra desde TODO el borde de la imagen, no solo las esquinas — si
      una antena/oreja toca el borde parte el aro en dos y la mitad quedaba
      atrapada (visto en monstruos);
    - defringe: tras quitar el aro se come ~1px del borde mezclado por el
      anti-alias (el "fleco" blanco que se veía sobre fondos de color) y se
      suaviza el corte. Con arte sin halo es no-op (no hay blanco alcanzable).
    Medido 10-jul-2026 sobre 6 temas: umbral 205 captura los aros reales sin
    tocar blancos internos."""
    im = im.convert("RGBA")
    W, H = im.size
    a = im.getchannel("A")
    r, g, bl = im.convert("RGB").split()
    mn = ImageChops.darker(ImageChops.darker(r, g), bl)      # canal mínimo
    near_white = mn.point(lambda v: 255 if v > umbral else 0)
    transp = a.point(lambda v: 255 if v < 40 else 0)
    passable = ImageChops.lighter(near_white, transp)        # exterior o aro
    work = passable.copy()
    px = work.load()
    for x in range(W):                                       # borde superior/inferior
        for y in (0, H - 1):
            if px[x, y] == 255:
                ImageDraw.floodfill(work, (x, y), 128)
    for y in range(H):                                       # borde izq/der
        for x in (0, W - 1):
            if px[x, y] == 255:
                ImageDraw.floodfill(work, (x, y), 128)
    reached = work.point(lambda v: 255 if v == 128 else 0)
    quitar = ImageChops.multiply(reached, near_white)        # aro alcanzable
    if quitar.getbbox():                                     # hay aro (si no: no-op)
        # DEFRINGE SELECTIVO: el anti-alias deja un fleco blancuzco de 1-2px
        # pegado a lo quitado. Se come SOLO píxeles claros adyacentes a lo ya
        # quitado (mn>165) — nunca contornos oscuros ni patas finas.
        claro = mn.point(lambda v: 255 if v > 165 else 0)
        for _ in range(max(0, int(defringe)) * 2):
            quitar = ImageChops.lighter(
                quitar, ImageChops.multiply(quitar.filter(ImageFilter.MaxFilter(3)), claro))
        # BOLSONES ATRAPADOS: aro encerrado por el trazo del troquelado (ej.
        # entre la antena y la cabeza). Un casi-blanco chico que vive TODO a
        # <=umbral_dist px del exterior es aro, no personaje (los dientes/nubes
        # quedan lejos del borde o son grandes).
        quitar = _quitar_bolsones(a, mn, quitar, umbral)
    out = im.copy()
    out.putalpha(ImageChops.subtract(a, quitar))
    bb = out.getbbox()
    return out.crop(bb) if bb else out


def _quitar_bolsones(a, mn, quitar, umbral, max_frac=0.06, umbral_dist=9):
    """Suma a `quitar` los bolsones de casi-blanco encerrados: componentes
    chicos (<max_frac del área opaca) cuyos píxeles quedan TODOS a
    <=umbral_dist px del exterior (transparente o ya quitado). Regla a
    propósito CONSERVADORA: atrapa los huecos angostos del die-cut (≲2×
    umbral_dist px de ancho, lo normal — el corte abraza la figura) sin
    riesgo de comerse blancos legítimos grandes (nubes, vestidos)."""
    W, H = a.size
    afuera = ImageChops.lighter(a.point(lambda v: 255 if v < 40 else 0), quitar)
    cerca = afuera.filter(ImageFilter.MaxFilter(umbral_dist * 2 + 1))
    resto = ImageChops.multiply(                              # casi-blanco vivo
        ImageChops.multiply(a.point(lambda v: 255 if v > 40 else 0),
                            mn.point(lambda v: 255 if v > umbral else 0)),
        ImageChops.invert(quitar.point(lambda v: 255 if v > 128 else 0)))
    px_r, px_c = resto.load(), cerca.load()
    opacos = sum(a.point(lambda v: 255 if v > 40 else 0).histogram()[255:]) or 1
    visto = bytearray(W * H)
    extra = Image.new("L", (W, H), 0)
    px_e = extra.load()
    for y0 in range(H):
        for x0 in range(W):
            if px_r[x0, y0] != 255 or visto[y0 * W + x0]:
                continue
            comp, pila, ok = [], [(x0, y0)], True
            visto[y0 * W + x0] = 1
            while pila:
                x, y = pila.pop()
                comp.append((x, y))
                if px_c[x, y] != 255:
                    ok = False                                # lejos del borde: personaje
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < W and 0 <= ny < H and not visto[ny * W + nx] \
                            and px_r[nx, ny] == 255:
                        visto[ny * W + nx] = 1
                        pila.append((nx, ny))
            if ok and len(comp) < max_frac * opacos:
                for x, y in comp:
                    px_e[x, y] = 255
    return ImageChops.lighter(quitar, extra)


def agregar_halo(im, grosor=None, color=(255, 255, 255), borde=None):
    """Contorno de sticker UNIFORME a partir de la silueta (alpha): dilata la
    silueta `grosor` px con esquinas redondeadas y pone el color detrás. Para
    un die-cut consistente, aplicar sobre arte YA limpio (quitar_halo antes).
    grosor default: ~4.5% del lado mayor (mínimo 6px).
    `borde`: color de la LÍNEA DE CORTE al filo del troquel (ej. (208,208,208))
    — sin ella, halo blanco sobre hoja blanca no se ve, y además marca por
    dónde recortar con tijera."""
    im = im.convert("RGBA")
    g = int(grosor) if grosor else max(6, int(max(im.size) * 0.045))
    pad = g + 3
    base = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    base.alpha_composite(im, (pad, pad))
    m = base.getchannel("A").point(lambda v: 255 if v > 40 else 0)
    for _ in range(g):                       # dilatación iterada ≈ disco (redondeado)
        m = m.filter(ImageFilter.MaxFilter(3))
    m = m.filter(ImageFilter.GaussianBlur(max(1.2, g * 0.25)))
    m = m.point(lambda v: 255 if v > 100 else 0)   # re-solidificar el borde suavizado
    canto = None
    if borde:
        canto = ImageChops.subtract(m, m.filter(ImageFilter.MinFilter(5)))
    m = m.filter(ImageFilter.GaussianBlur(0.8))    # anti-alias final
    halo = Image.new("RGBA", base.size, tuple(color) + (255,))
    halo.putalpha(m)
    if canto is not None:
        linea = Image.new("RGBA", base.size, tuple(borde) + (255,))
        linea.putalpha(canto.filter(ImageFilter.GaussianBlur(0.6)))
        halo.alpha_composite(linea)
    halo.alpha_composite(base)
    return halo


def un_solo_blob(im, min_frac=0.18):
    """True si el recorte es UNA figura (no una tira compuesta). Componentes
    conexas del CONTENIDO COLOREADO a 64×64: si hay una segunda mancha grande
    (> min_frac de la mayor), es un compuesto tipo 'jirafa + hojas + flores' y
    se descarta — la misma clase de bug que las columnas apiladas del cuaderno
    (skill §19). OJO: el halo blanco troquelado del sticker puentea las figuras
    si se mira solo el alpha — por eso se excluyen los píxeles casi blancos."""
    im64 = im.resize((64, 64))
    a64, rgb = im64.split()[3].load(), im64.convert("RGB").load()
    a = Image.new("L", (64, 64), 0)
    px = a.load()
    for y in range(64):
        for x in range(64):
            r, g, b2 = rgb[x, y]
            if a64[x, y] > 40 and not (r > 225 and g > 225 and b2 > 225):
                px[x, y] = 255
    visto = bytearray(64 * 64)
    areas = []
    for y0 in range(64):
        for x0 in range(64):
            if px[x0, y0] and not visto[y0 * 64 + x0]:
                area, pila = 0, [(x0, y0)]
                visto[y0 * 64 + x0] = 1
                while pila:
                    x, y = pila.pop()
                    area += 1
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= nx < 64 and 0 <= ny < 64 and px[nx, ny] \
                                and not visto[ny * 64 + nx]:
                            visto[ny * 64 + nx] = 1
                            pila.append((nx, ny))
                areas.append(area)
    areas.sort(reverse=True)
    return len(areas) < 2 or areas[1] < areas[0] * min_frac


def hoja_stickers(tema, lado=2400):
    """Hoja de stickers RECOMPUESTA con troquel uniforme: recortes de la hoja
    IA (cuaderno._extraer_monstruos) → quitar_halo → agregar_halo parejo con
    línea de corte. Reemplaza a la hoja cruda de la IA como pieza vendida
    (contornos dispares / aros fusionados entre vecinos — feedback Pablo
    10-jul-2026). Cache en extras/.stickers_uniforme.png (se invalida si
    cambia la hoja fuente). Devuelve RGB; None si el tema no tiene recortes."""
    import cuaderno
    tdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temas", tema)
    fuente = os.path.join(tdir, "extras", "stickers_1.png")
    cache = os.path.join(tdir, "extras", ".stickers_uniforme.png")
    try:
        if os.path.isfile(cache) and os.path.isfile(fuente) \
                and os.path.getmtime(cache) >= os.path.getmtime(fuente):
            return Image.open(cache).convert("RGB")
    except OSError:
        pass
    try:
        paths = cuaderno._extraer_monstruos(tema) or []
    except Exception:
        paths = []
    brutos = []
    for p in paths:
        try:
            im = Image.open(p).convert("RGBA")
        except Exception:
            continue
        bb = im.getbbox()
        if bb:
            brutos.append(im.crop(bb))
    if not brutos:
        return None
    # Umbral de tamaño RELATIVO a la propia hoja: la de fútbol trae 37 mini
    # stickers (30-150px) y los umbrales absolutos la vaciaban; la de safari
    # los trae de 200-420px. La mediana de cada hoja define qué es "fragmento".
    areas = sorted(i.width * i.height for i in brutos)
    mediana = max(1, areas[len(areas) // 2])
    min_area = max(2500, int(mediana * 0.30))
    min_dim = max(28, int(mediana ** 0.5 * 0.45))
    crops = []
    for im in brutos:
        if im.width * im.height < min_area or min(im.size) < min_dim:
            continue                          # fragmento para ESTA hoja
        opacos = sum(im.getchannel("A").point(lambda v: v > 40 and 255)
                     .histogram()[255:])
        if opacos / (im.width * im.height) < 0.30:
            continue                          # ralos (piolines de globos, virutas)
        if not un_solo_blob(im):              # racimos pegados
            continue
        crops.append(quitar_halo(im))
    if len(crops) < 6:
        return None                          # hoja pobre → mejor la cruda
    # clases de tamaño por área original (grandes arriba, chicos abajo)
    crops.sort(key=lambda i: -(i.width * i.height))
    n = len(crops)
    MARG, GAP = 100, 30
    util = lado - 2 * MARG

    def _armar(escala):
        """Redimensiona + troquela + arma filas. Devuelve (filas, alto_total)."""
        sts = []
        for i, im in enumerate(crops):
            alto = int((380 if i < n // 3 else (260 if i < 2 * n // 3 else 175)) * escala)
            alto = min(alto, int(im.height * 1.8))   # no agrandar >1.8x (nitidez)
            w = max(1, int(im.width * alto / im.height))
            sts.append(agregar_halo(im.resize((w, alto), Image.LANCZOS),
                                    grosor=max(8, int(14 * escala)),
                                    borde=(206, 206, 206)))
        fs, f, wf = [], [], 0
        for st in sts:
            if f and wf + st.width > util:
                fs.append(f)
                f, wf = [], 0
            f.append(st)
            wf += st.width + GAP
        if f:
            fs.append(f)
        return fs, sum(max(s2.height for s2 in ff) for ff in fs) + GAP * (len(fs) - 1)

    escala = 1.0
    filas, alto_total = _armar(escala)
    # hoja RALA (mini-stickers, ej. fútbol): repetir los motivos hasta llenar,
    # como las hojas de stickers reales — más stickers, no más aire
    while alto_total < util * 0.62 and len(crops) <= 100:
        crops = crops + crops
        crops.sort(key=lambda i: -(i.width * i.height))
        n = len(crops)
        filas, alto_total = _armar(escala)
    # si no entra a tamaño pleno, achicar hasta que TODO quepa (sin recortes)
    while alto_total > util and escala > 0.5:
        escala *= 0.92
        filas, alto_total = _armar(escala)
    esp = max(GAP, (lado - 2 * MARG - (alto_total - GAP * (len(filas) - 1)))
              // max(1, len(filas) - 1)) if len(filas) > 1 else 0
    hoja = Image.new("RGB", (lado, lado), (255, 255, 255))
    y = MARG
    for f in filas:
        hf = max(s2.height for s2 in f)
        # JUSTIFICADO horizontal: los stickers se reparten a lo ancho de la
        # hoja (con pocas filas de stickers chicos, centrarlos apiñaba todo
        # al medio con bandas vacías — hoja de fútbol)
        wf = sum(s2.width for s2 in f)
        if len(f) >= 4:      # fila llena: justificada a lo ancho
            paso = (lado - 2 * MARG - wf) / (len(f) - 1)
            x = MARG
        else:                # fila corta (el resto final): centrada y junta
            paso = GAP * 3
            x = (lado - wf - paso * (len(f) - 1)) // 2
        for s2 in f:
            hoja.paste(s2, (int(x), y + (hf - s2.height) // 2), s2)
            x += s2.width + paso
        y += hf + esp
    try:
        hoja.save(cache)
    except OSError:
        pass
    return hoja


def marca_agua(img, texto="CASATRIDIMENSIONAL · VISTA PREVIA", op=70):
    """Estampa una marca de agua diagonal repetida (solo para el preview)."""
    img = img.convert("RGBA")
    W, H = img.size
    diag = int((W ** 2 + H ** 2) ** 0.5)
    layer = Image.new("RGBA", (diag, diag), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = get_font("Poppins-SemiBold.ttf", max(18, int(W * 0.035)))
    tw = d.textlength(texto, font=f)
    sx = int(tw + W * 0.10)
    sy = int(W * 0.12)
    color = (110, 80, 62, op)
    r = 0
    for y in range(0, diag, sy):
        off = (r % 2) * (sx // 2)
        for x in range(-sx, diag, sx):
            d.text((x + off, y), texto, font=f, fill=color)
        r += 1
    layer = layer.rotate(30)
    cx, cy = diag // 2, diag // 2
    layer = layer.crop((cx - W // 2, cy - H // 2, cx - W // 2 + W, cy - H // 2 + H))
    img.alpha_composite(layer)
    return img.convert("RGB")

def to_rgb(img):
    if img.mode == "RGB":
        return img
    bg = Image.new("RGBA", img.size, WHITE + (255,))
    bg.alpha_composite(img)
    return bg.convert("RGB")

def _dpi_de(img):
    """DPI correcto para que el PDF salga al tamaño FÍSICO pensado.

    GOTCHA real (CLAUDE.md regla #5): exportar SIEMPRE a resolution=300 hacía
    que toda pieza dibujada a 1240x1754 (la convención vieja "A4 a ~150dpi" de
    los productos individuales: menú, memoria, antifaces, cápsula, etc.)
    imprimiera a la MITAD del tamaño (A5) — un antifaz de 9cm no entra en una
    cara. Hasta que cada módulo migre a 300dpi real (corona.py ya migró), el
    export respeta la escala del lienzo: si la pieza es "A4 a 150dpi" (o media
    A4, como las hojas del cuaderno legado) se declara resolution=150 y el
    papel vuelve a medir A4. Mismos píxeles, tamaño físico correcto."""
    tam_150 = {(1240, 1754), (1754, 1240)}
    return 150 if img.size in tam_150 else DPI


def generar_kit(data, dest_dir, tema="safari", piezas_list=None):
    """Genera las piezas de la temática en PDF y las empaqueta en un ZIP.
    El DPI declarado se elige por pieza para que el tamaño físico sea el
    correcto (ver _dpi_de).

    `piezas_list` permite generar un set de piezas distinto al kit completo
    (usado por productos.generar para los demás tipos de producto). Si no se
    pasa, usa las 7 piezas del kit (comportamiento histórico)."""
    import zipfile
    os.makedirs(dest_dir, exist_ok=True)
    pdfs = []
    for name, fn, _ in (piezas_list if piezas_list is not None else piezas_de(tema)):
        p = os.path.join(dest_dir, name + ".pdf")
        rgb = to_rgb(fn(data))
        rgb.save(p, "PDF", resolution=_dpi_de(rgb))
        pdfs.append(p)
    zip_path = os.path.join(dest_dir, "kit.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in pdfs:
            z.write(p, os.path.basename(p))
    return zip_path

def preview_invitacion(data, max_px=1000, tema="safari"):
    """PNG chico de la invitación (para vista previa / miniatura de pedido)."""
    img = render(data, specs_de(tema)["invitacion"])
    img.thumbnail((max_px, max_px), Image.LANCZOS)
    return img

if __name__ == "__main__":
    demo = {"nombre": "Tomás", "fecha": "Sábado 12 de julio", "hora": "16:00 hs",
            "lugar": "Salón Los Robles", "telefono": "11-5555-5555"}
    KIT = os.path.join(OUT, "kit")
    os.makedirs(KIT, exist_ok=True)
    thumbs = []
    for name, fn, is_rgba in PIEZAS:
        img = fn(demo)
        rgb = to_rgb(img)
        if is_rgba:
            img.save(os.path.join(KIT, name + ".png"))   # con transparencia
        rgb.save(os.path.join(KIT, name + ".pdf"), "PDF", resolution=DPI)
        rgb.save(os.path.join(KIT, name + ".png").replace(".png", "_rgb.png")) if not is_rgba else None
        # thumb para grilla
        t = rgb.copy(); t.thumbnail((520, 520), Image.LANCZOS)
        thumbs.append((name, t))
        print(f"OK  {name:24} {rgb.size}")

    # grilla de revision (2 filas x 4)
    cols, rows = 4, 2
    cellw = max(t.width for _, t in thumbs) + 30
    cellh = max(t.height for _, t in thumbs) + 50
    grid = Image.new("RGB", (cols * cellw, rows * cellh), (245, 240, 232))
    gd = ImageDraw.Draw(grid)
    for i, (name, t) in enumerate(thumbs):
        cx = (i % cols) * cellw + cellw // 2
        cy = (i // cols) * cellh + 20 + t.height // 2
        grid.paste(t, (cx - t.width // 2, (i // cols) * cellh + 20))
        gd.text((cx, (i // cols) * cellh + cellh - 22), name, fill=(90, 70, 55), anchor="mm")
    grid.save(os.path.join(OUT, "kit_grilla.jpg"), quality=90)
    print("Grilla ->", os.path.join(OUT, "kit_grilla.jpg"))
