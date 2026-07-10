"""mandalas.py — Kit de mándalas para pintar (line-art procedural, imprimible).

Producto standalone (tipo "mandalas" en productos.TIPOS). 100% procedural: determinista,
gratis, sin IA (fallback nativo; la Fase 2 con arte IA se compone ENCIMA de este tileador).

Reglas de imprenta aplicadas (skill armar-kit + CLAUDE.md #5):
- Dibuja a A4 300dpi REAL (2480x3508) → el PDF sale a tamaño físico correcto (evita el
  gotcha de los 1240x1754 que imprimen a mitad de tamaño).
- Negro 100% puro, sin grises ni degradés (line-art de verdad para colorear).
- Contenido dentro del área universal (imprime igual en A4 y Carta).
- Simetría radial EXACTA por trigonometría (nada de rotar capas → contornos limpios).
- Estrellas de dificultad DIBUJADAS, nunca el glifo ★ (Poppins no lo tiene → tofu).

API pública (la usa productos._piezas_mandalas):
    portada(data)              -> Image  (personalizable con data["nombre"])
    pagina(nivel, idx, total)  -> Image
    como_imprimir()            -> Image
"""
from __future__ import annotations
import math
import os

from PIL import Image, ImageDraw

from generador import get_font, fit_font

# ── Imprenta ─────────────────────────────────────────────────────────────────
A4 = (2480, 3508)                 # 210x297mm @300dpi (igual que piezas.A4)
PXMM = A4[0] / 210.0              # ≈11.81 px/mm
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CX, CY = A4[0] // 2, A4[1] // 2
R = 1060                          # radio máx del mandala (cabe en el área imprimible)
NIVELES = 6

# Arte fijo (line-art generado con IA, limpiado a B/N puro, 2244px @300dpi). Se genera UNA
# vez y se vende a todos (las mándalas no son personalizadas). Si falta un asset, la pieza
# cae al diseño PROCEDURAL de abajo (la casa: toda pieza conserva su fallback nativo).
ART_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mandalas_arte")


def _asset(nivel):
    p = os.path.join(ART_DIR, f"{int(nivel)}.png")
    return p if os.path.isfile(p) else None


def _txt(d, text, cx, cy, fname, size, color=BLACK, wght=None, maxw=None, anchor="mm"):
    if not str(text).strip():
        return
    f = fit_font(d, str(text), fname, int(size), int(maxw), wght) if maxw else get_font(fname, int(size), wght)
    d.text((cx, cy), str(text), font=f, fill=color, anchor=anchor)


# ── Primitivas de simetría radial ────────────────────────────────────────────
def _closed(d, pts, width):
    d.line(pts + [pts[0]], fill=BLACK, width=width, joint="curve")


def petal_ring(d, dist, a, b, count, phase, width, cx=CX, cy=CY):
    """`count` pétalos (elipses con eje radial) alrededor del anillo de radio `dist`."""
    for k in range(count):
        th = phase + 2 * math.pi * k / count
        px, py = cx + dist * math.cos(th), cy + dist * math.sin(th)
        ux, uy = math.cos(th), math.sin(th)
        vx, vy = -math.sin(th), math.cos(th)
        pts = []
        for i in range(64):
            t = 2 * math.pi * i / 64
            ex, ey = a * math.cos(t), b * math.sin(t)
            pts.append((px + ex * ux + ey * vx, py + ex * uy + ey * vy))
        _closed(d, pts, width)


def teardrop_ring(d, r_in, r_out, half_w, count, phase, width, cx=CX, cy=CY):
    """`count` gotas puntiagudas (pétalo con punta hacia afuera)."""
    for k in range(count):
        th = phase + 2 * math.pi * k / count
        ux, uy = math.cos(th), math.sin(th)
        vx, vy = -math.sin(th), math.cos(th)
        pts, n = [], 40
        for i in range(n + 1):
            t = i / n
            rr = r_in + (r_out - r_in) * t
            w = half_w * math.sin(math.pi * t) ** 0.7
            pts.append((cx + rr * ux - w * vx, cy + rr * uy - w * vy))
        for i in range(n + 1):
            t = 1 - i / n
            rr = r_in + (r_out - r_in) * t
            w = half_w * math.sin(math.pi * t) ** 0.7
            pts.append((cx + rr * ux + w * vx, cy + rr * uy + w * vy))
        _closed(d, pts, width)


def circle_ring(d, dist, rr, count, phase, width, cx=CX, cy=CY):
    for k in range(count):
        th = phase + 2 * math.pi * k / count
        px, py = cx + dist * math.cos(th), cy + dist * math.sin(th)
        d.ellipse([px - rr, py - rr, px + rr, py + rr], outline=BLACK, width=width)


def dot_ring(d, dist, rr, count, phase, cx=CX, cy=CY):
    for k in range(count):
        th = phase + 2 * math.pi * k / count
        px, py = cx + dist * math.cos(th), cy + dist * math.sin(th)
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=BLACK)


def concentric(d, radii, width, cx=CX, cy=CY):
    for r in radii:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLACK, width=width)


def scallop(d, dist, count, amp, width, phase=0.0, cx=CX, cy=CY, inward=False):
    """Círculo ondulado (festón) — para bordes y separadores."""
    pts, n = [], count * 24
    s = -1 if inward else 1
    for i in range(n):
        a = phase + 2 * math.pi * i / n
        r = dist + s * amp * math.cos(count * (a - phase))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    _closed(d, pts, width)


def diamond_ring(d, dist, a, b, count, phase, width, cx=CX, cy=CY):
    for k in range(count):
        th = phase + 2 * math.pi * k / count
        px, py = cx + dist * math.cos(th), cy + dist * math.sin(th)
        ux, uy = math.cos(th), math.sin(th)
        vx, vy = -math.sin(th), math.cos(th)
        pts = [(px + a * ux, py + a * uy), (px + b * vx, py + b * vy),
               (px - a * ux, py - a * uy), (px - b * vx, py - b * vy)]
        _closed(d, pts, width)


def ray_ring(d, r_in, r_out, count, phase, width, cx=CX, cy=CY):
    """Rayos radiales (líneas del anillo interno al externo) — dan ritmo."""
    for k in range(count):
        th = phase + 2 * math.pi * k / count
        ux, uy = math.cos(th), math.sin(th)
        d.line([(cx + r_in * ux, cy + r_in * uy), (cx + r_out * ux, cy + r_out * uy)],
               fill=BLACK, width=width)


def lens_ring(d, dist, a, b, count, phase, width, cx=CX, cy=CY):
    """Hojitas/ojos (lente puntiaguda en ambos extremos), eje radial."""
    for k in range(count):
        th = phase + 2 * math.pi * k / count
        px, py = cx + dist * math.cos(th), cy + dist * math.sin(th)
        ux, uy = math.cos(th), math.sin(th)
        vx, vy = -math.sin(th), math.cos(th)
        pts = []
        for i in range(48):
            t = 2 * math.pi * i / 48
            ex = a * math.sin(t) * abs(math.sin(t)) ** 0.4
            ey = b * math.cos(t)
            pts.append((px + ex * ux + ey * vx, py + ex * uy + ey * vy))
        _closed(d, pts, width)


def heart_dot_ring(d, dist, rr, count, phase, width, cx=CX, cy=CY):
    """Circulitos con un punto adentro (clásico de mándala)."""
    circle_ring(d, dist, rr, count, phase, width, cx, cy)
    dot_ring(d, dist, max(4, rr // 3), count, phase, cx, cy)


# ── Composición de una mándala por nivel ─────────────────────────────────────
# Receta distinta por nivel → 6 mándalas visualmente diferentes (no "la misma más
# densa"). Determinista, sin azar.
RECETAS = {
    1: ["teardrop", "circledot", "petal"],
    2: ["petal", "circledot", "lens", "teardrop"],
    3: ["lens", "diamond", "petal", "circledot", "teardrop"],
    4: ["circledot", "rays", "teardrop", "diamond", "petal", "lens"],
    5: ["petal", "lens", "circledot", "rays", "diamond", "teardrop", "scallop"],
    6: ["lens", "circledot", "teardrop", "rays", "petal", "diamond", "scallop", "circledot"],
}
_SECTORES = [8, 10, 12, 16, 20, 24]
_GROSOR = [9, 8, 7, 6, 5, 5]
DIFICULTAD = ["Muy fácil", "Fácil", "Intermedio", "Avanzado", "Difícil", "Muy difícil"]


def _banda(d, kind, r, step, n, ph, w, i, cx, cy):
    mid = r + step * 0.5
    if kind == "teardrop":
        teardrop_ring(d, r + step * 0.06, r + step * 0.94, step * 0.30, n, ph * (i % 2), w, cx, cy)
    elif kind == "petal":
        petal_ring(d, mid, step * 0.44, step * 0.20, n, ph * (i % 2), w, cx, cy)
    elif kind == "circledot":
        heart_dot_ring(d, mid, step * 0.32, n * 2, ph, w, cx, cy)
    elif kind == "diamond":
        diamond_ring(d, mid, step * 0.44, step * 0.24, n, ph, w, cx, cy)
    elif kind == "lens":
        lens_ring(d, mid, step * 0.42, step * 0.22, n, 0, w, cx, cy)
    elif kind == "scallop":
        scallop(d, mid, n, step * 0.24, w, phase=ph, cx=cx, cy=cy)
        dot_ring(d, mid, 8, n, ph, cx, cy)
    elif kind == "rays":
        ray_ring(d, r + step * 0.16, r + step * 0.84, n * 2, ph, max(3, w - 2), cx, cy)
        heart_dot_ring(d, mid, step * 0.16, n, 0, max(3, w - 2), cx, cy)


def draw_mandala(d, level, cx=CX, cy=CY, rmax=R):
    """level 1 (fácil, líneas gruesas, pocos sectores) → 6 (intrincado)."""
    level = max(1, min(NIVELES, int(level)))
    n = _SECTORES[level - 1]
    w = _GROSOR[level - 1]
    ph = math.pi / n
    sc = rmax / R

    # Rosetón central
    d.ellipse([cx - 34 * sc, cy - 34 * sc, cx + 34 * sc, cy + 34 * sc], outline=BLACK, width=w)
    dot_ring(d, 0, 10 * sc, 1, 0, cx, cy)
    petal_ring(d, 70 * sc, 46 * sc, 26 * sc, n, 0, w, cx, cy)
    concentric(d, [118 * sc], w, cx, cy)

    receta = RECETAS[level]
    r0, bands = 175 * sc, rmax - 150 * sc
    step = (bands - r0) / len(receta)
    for i, kind in enumerate(receta):
        r = r0 + i * step
        _banda(d, kind, r, step, n, ph, w, i, cx, cy)
        concentric(d, [r + step], max(3, w - 2), cx, cy)

    # Borde exterior: doble círculo + festón + puntos
    concentric(d, [rmax - 60 * sc, rmax - 30 * sc], w, cx, cy)
    scallop(d, rmax - 88 * sc, n * 2, 26 * sc, max(3, w - 2), phase=ph, cx=cx, cy=cy)
    dot_ring(d, rmax - 45 * sc, 9 * sc, n * 4, 0, cx, cy)


# ── Páginas del kit ──────────────────────────────────────────────────────────
def _page():
    img = Image.new("RGB", A4, WHITE)
    return img, ImageDraw.Draw(img)


def _footer(d):
    _txt(d, "Casatridimensional · casatridimensional.com.ar", CX, A4[1] - 96,
         "Poppins-Regular.ttf", 34, (120, 120, 120))


def _star(d, cx, cy, r, filled):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + math.pi * i / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=BLACK if filled else None, outline=BLACK, width=3)


def _pegar_mandala(img, nivel, cx=CX, cy=CY, size=2160):
    """Dibuja la mándala del nivel: usa el arte IA (asset) si existe, si no el procedural."""
    art = _asset(nivel)
    if art:
        m = Image.open(art).convert("RGB").resize((size, size), Image.LANCZOS)
        img.paste(m, (int(cx - size / 2), int(cy - size / 2)))
    else:
        draw_mandala(ImageDraw.Draw(img), nivel, cx=cx, cy=cy, rmax=size // 2)


def pagina(nivel, idx, total=NIVELES):
    """Una hoja de mándala (line-art para colorear)."""
    img, d = _page()
    _pegar_mandala(img, nivel)
    _txt(d, f"{idx} / {total}", CX, 150, "Poppins-Regular.ttf", 40, (150, 150, 150))
    gap, sr, ns = 74, 24, NIVELES
    x0 = CX - (ns - 1) * gap / 2
    for i in range(ns):
        _star(d, x0 + i * gap, A4[1] - 210, sr, filled=(i < nivel))
    _txt(d, DIFICULTAD[max(0, min(NIVELES, nivel) - 1)], CX, A4[1] - 148,
         "Poppins-Regular.ttf", 40, (90, 90, 90))
    _footer(d)
    return img


def portada(data=None):
    """Portada del kit. Se personaliza con data['nombre'] si viene."""
    nombre = (data or {}).get("nombre", "")
    nombre = str(nombre).strip()
    img, d = _page()
    d.rectangle([90, 90, A4[0] - 90, A4[1] - 90], outline=BLACK, width=6)
    d.rectangle([120, 120, A4[0] - 120, A4[1] - 120], outline=BLACK, width=2)
    _txt(d, "Mándalas", CX, 520, "Fredoka-VF.ttf", 210, BLACK, wght=650, maxw=A4[0] - 400)
    sub = f"de {nombre}" if nombre else "para pintar"
    _txt(d, sub, CX, 720, "Fredoka-VF.ttf", 120, BLACK, wght=500, maxw=A4[0] - 500)
    _pegar_mandala(img, 3, cx=CX, cy=1920, size=1560)
    _txt(d, f"{NIVELES} diseños · dificultad creciente · listo para imprimir en casa",
         CX, 2820, "Poppins-Regular.ttf", 44, (70, 70, 70), maxw=A4[0] - 300)
    _footer(d)
    return img


def como_imprimir(data=None):
    img, d = _page()
    _txt(d, "Cómo imprimir", CX, 360, "Fredoka-VF.ttf", 130, BLACK, wght=600)
    tips = [
        "Imprimí al 100% / “tamaño real” (NO “ajustar a la página”).",
        "Papel: hoja común 90g está perfecta; para fibras/acuarela, 120-160g.",
        "Sirve igual en A4 y en Carta: el diseño está centrado con margen de seguridad.",
        "Blanco y negro alcanza — no hace falta color en la impresora.",
        "Pintá con lo que tengas: fibras, lápices, crayones o acuarela.",
    ]
    y = 720
    for t in tips:
        d.ellipse([300, y - 14, 328, y + 14], fill=BLACK)
        f = get_font("Poppins-Regular.ttf", 52)
        d.text((380, y), t, font=f, fill=(30, 30, 30), anchor="lm")
        y += 150
    side = int(50 * PXMM)   # cuadrado de control de 5 cm
    x0, yb = 380, y + 120
    d.rectangle([x0, yb, x0 + side, yb + side], outline=BLACK, width=5)
    _txt(d, "Este cuadrado debe medir 5 cm de lado.", x0 + side + 260, yb + side // 2 - 34,
         "Poppins-Regular.ttf", 44, (30, 30, 30), anchor="lm")
    _txt(d, "Si no, revisá la escala de impresión.", x0 + side + 260, yb + side // 2 + 34,
         "Poppins-Regular.ttf", 44, (30, 30, 30), anchor="lm")
    _footer(d)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "salida_mandalas"
    os.makedirs(out, exist_ok=True)
    pages = [portada({"nombre": ""})]
    for lvl in range(1, NIVELES + 1):
        pages.append(pagina(lvl, lvl, NIVELES))
    pages.append(como_imprimir())
    pdf = os.path.join(out, "kit_mandalas.pdf")
    pages[0].save(pdf, "PDF", resolution=300, save_all=True, append_images=pages[1:])
    print(pdf)
