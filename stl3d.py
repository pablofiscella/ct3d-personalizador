"""Piezas 3D imprimibles (STL) generadas por código desde el personaje del tema —
medalla, topper de torta, trofeo y cortante de galletitas. Nada de modelado a mano
ni STL de terceros (evita cualquier duda de licencia — ver docs/superpowers/specs):
la silueta se extrae del PNG del personaje (contorno vectorial con OpenCV) y el
texto (nombre/edad) se auto-ajusta con la fuente real para no salirse de la pieza.
Motor: OpenSCAD (subprocess, cada generación en su propio dir temporal — seguro
para pedidos concurrentes)."""
import glob
import io
import math
import os
import re
import shutil
import subprocess
import tempfile
import threading
import zipfile

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(KIT, "assets", "stl3d")
FUENTE_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# OpenSCAD (Pango/Cairo) renderiza text(size=S) más ANCHO que lo que predice PIL al
# mismo valor nominal — medido empíricamente comparando el STL real exportado contra
# font.getlength() de PIL (ver docs/superpowers/specs, sección de calibración). Si se
# cambia de fuente hay que recalibrar: generar un text() a size=100 en un .scad,
# exportar a STL, medir el ancho real (xs.max()-xs.min() de los vértices) y compararlo
# contra ImageFont.getlength() al mismo string.
_REF = 200
CALIBRACION_OPENSCAD = 1.40


# ---------------------------------------------------------------------------
# Texto auto-ajustado — mide con la fuente real, no con heurísticas por caracter
# ---------------------------------------------------------------------------

def _tamano_ajustado(texto, ancho_max_mm, size_base):
    """Tamaño de fuente (para text(size=...) de OpenSCAD) más grande posible sin
    que el texto renderizado supere ancho_max_mm, topeado en size_base."""
    if not texto:
        return size_base
    font = ImageFont.truetype(FUENTE_PATH, _REF)
    ancho_ref = font.getlength(texto)
    if ancho_ref <= 0:
        return size_base
    tamano_pil = ancho_max_mm * _REF / ancho_ref
    return min(size_base, tamano_pil / CALIBRACION_OPENSCAD)


def _ancho_renderizado_mm(texto, tamano_scad):
    """Inversa: cuánto mide (mm) el texto si se renderiza en OpenSCAD a ese tamaño."""
    if not texto:
        return 0.0
    font = ImageFont.truetype(FUENTE_PATH, _REF)
    ancho_ref = font.getlength(texto)
    return ancho_ref * (tamano_scad * CALIBRACION_OPENSCAD) / _REF


# ---------------------------------------------------------------------------
# Silueta: PNG con alpha -> module silueta() { polygon(...) } de OpenSCAD
# ---------------------------------------------------------------------------

def _silueta_modulo(img_rgba, alto_ref_mm=40, eps_px=1.0, alto_px=800, umbral=100):
    """Extrae el contorno exterior del personaje y lo devuelve como código OpenSCAD
    `module silueta() { polygon(...); }`, centrado en el origen y con alto_ref_mm de
    alto. Cada pieza que la usa la reescala con resize() a la medida que necesite."""
    img = img_rgba.convert("RGBA")
    escala_img = alto_px / img.height
    img = img.resize((max(1, int(img.width * escala_img)), alto_px), Image.LANCZOS)
    arr = np.array(img).astype(np.int16)
    alpha = arr[:, :, 3]
    # La figura real: opaca Y no-blanca. El alpha de los personajes (quitar_fondo)
    # suele tener un blob más grande que la figura, con la figura dibujada adentro.
    no_blanco = (255 * 3 - arr[:, :, :3].sum(axis=2)) > 90
    mask = ((alpha > umbral) & no_blanco).astype(np.uint8) * 255
    k = max(3, int(alto_px / 100) | 1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8))
    mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=alto_px / 300)
    mask = (mask > 127).astype(np.uint8) * 255

    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        raise ValueError("no se encontró figura en el PNG del personaje")
    principal = max(contornos, key=cv2.contourArea)
    pts = cv2.approxPolyDP(principal, eps_px, True).reshape(-1, 2)
    if len(pts) < 3:
        raise ValueError("contorno degenerado (personaje demasiado chico o vacío)")

    xs, ys = pts[:, 0].astype(float), -pts[:, 1].astype(float)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    esc = alto_ref_mm / max(ys.max() - ys.min(), 1e-6)
    xs, ys = (xs - cx) * esc, (ys - cy) * esc
    coords = ",".join(f"[{x:.2f},{y:.2f}]" for x, y in zip(xs, ys))
    return f"module silueta() {{ polygon(points=[{coords}]); }}\n"


def _personaje_tema(tema):
    """PIL Image RGBA de un personaje representativo del tema, para vectorizar."""
    import cuaderno
    ps = cuaderno.personajes_decorativos(tema, 1)
    if not ps:
        raise ValueError(f"el tema '{tema}' no tiene personajes decorativos")
    return ps[0]


# ---------------------------------------------------------------------------
# Plantillas .scad — se cachean en memoria, el include de silueta se inyecta inline
# ---------------------------------------------------------------------------

_TEMPLATES = {}
_INCLUDE_RE = re.compile(r"include\s*<silueta_mod\.scad>\s*\n?")


def _plantilla(nombre_archivo):
    if nombre_archivo not in _TEMPLATES:
        with open(os.path.join(ASSETS, nombre_archivo), encoding="utf-8") as f:
            txt = f.read()
        if not _INCLUDE_RE.search(txt):
            raise ValueError(f"{nombre_archivo}: no se encontró 'include <silueta_mod.scad>'")
        _TEMPLATES[nombre_archivo] = _INCLUDE_RE.split(txt, maxsplit=1)
    return _TEMPLATES[nombre_archivo]


def _armar_scad(nombre_archivo, silueta_modulo):
    antes, despues = _plantilla(nombre_archivo)
    return antes + silueta_modulo + despues


# ---------------------------------------------------------------------------
# Invocación a OpenSCAD — cada llamada en su propio dir temporal (concurrencia)
# ---------------------------------------------------------------------------

# Máximo 2 OpenSCAD simultáneos: cada render (xvfb + openscad) come cientos de MB;
# la galería del dash pidiendo 4-5 previews de golpe llegó a tirar el servicio por
# OOM (02-jul 22:02). Los que esperan se encolan acá, no en la RAM.
_OPENSCAD_SEM = threading.Semaphore(2)


def _run_openscad(scad_text, out_ext, defines=None, camera=None, imgsize=(900, 900)):
    tmpdir = tempfile.mkdtemp(prefix="stl3d_")
    try:
        scad_path = os.path.join(tmpdir, "modelo.scad")
        out_path = os.path.join(tmpdir, f"salida.{out_ext}")
        with open(scad_path, "w", encoding="utf-8") as f:
            f.write(scad_text)
        cmd = ["xvfb-run", "-a", "openscad", scad_path, "-o", out_path]
        for k, v in (defines or {}).items():
            val = ('"' + str(v).replace('"', '\\"') + '"') if isinstance(v, str) else v
            cmd += ["-D", f"{k}={val}"]
        if out_ext == "png":
            cmd += ["--imgsize", f"{imgsize[0]},{imgsize[1]}", "--preview"]
            if camera:
                cmd += ["--camera", camera]
        with _OPENSCAD_SEM:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode != 0 or not os.path.exists(out_path):
            raise RuntimeError("openscad falló: %s" % r.stderr[-1000:])
        with open(out_path, "rb") as f:
            return f.read()
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Piezas públicas — cada una devuelve (stl_bytes, png_preview_bytes|None)
# ---------------------------------------------------------------------------

def generar_medalla(tema, texto, diametro=60, relieve=1.6, texto_y=-18,
                     size_base=7, con_preview=False):
    silueta = _silueta_modulo(_personaje_tema(tema), alto_ref_mm=34)
    scad = _armar_scad("medalla.scad", silueta)
    ancho_max = 2 * math.sqrt(max((diametro / 2) ** 2 - texto_y ** 2, 1)) - 6
    size = round(_tamano_ajustado(texto, ancho_max, size_base), 3)
    defines = {"TEXTO": texto, "TEXTO_SIZE": size, "D": diametro,
               "RELIEVE": relieve, "TEXTO_Y": texto_y}
    stl = _run_openscad(scad, "stl", defines)
    png = _run_openscad(scad, "png", defines, camera="0,3,0,30,0,15,220") if con_preview else None
    return stl, png


def generar_topper(tema, texto, relieve=1.2, placa_w_min=50, placa_w_max=110,
                    size_base=8, con_preview=False):
    silueta = _silueta_modulo(_personaje_tema(tema), alto_ref_mm=70)
    scad = _armar_scad("topper.scad", silueta)
    ancho_ideal = _ancho_renderizado_mm(texto, size_base) + 14
    placa_w = round(min(max(ancho_ideal, placa_w_min), placa_w_max), 2)
    size = round(_tamano_ajustado(texto, placa_w - 8, size_base), 3)
    defines = {"TEXTO": texto, "TEXTO_SIZE": size, "PLACA_W": placa_w, "RELIEVE": relieve}
    stl = _run_openscad(scad, "stl", defines)
    png = _run_openscad(scad, "png", defines, camera="0,-15,0,35,0,10,400") if con_preview else None
    return stl, png


def generar_trofeo(tema, texto, altura=100, base_d=46, incluir_personaje=True,
                    relieve=1.4, size_base=5, con_preview=False):
    silueta = _silueta_modulo(_personaje_tema(tema), alto_ref_mm=26)
    scad = _armar_scad("trofeo.scad", silueta)
    ancho_max = base_d - 10
    size = round(_tamano_ajustado(texto, ancho_max, size_base), 3)
    defines = {"TEXTO": texto, "TEXTO_SIZE": size, "ALTURA": altura, "BASE_D": base_d,
               "INCLUIR_PERSONAJE": "true" if incluir_personaje else "false",
               "RELIEVE": relieve}
    stl = _run_openscad(scad, "stl", defines)
    png = (_run_openscad(scad, "png", defines, camera="0,0,50,80,0,10,320", imgsize=(700, 900))
           if con_preview else None)
    return stl, png


def _generar_cortante_desde_personaje(personaje_img, ancho_objetivo=80, alto_pared=20,
                                       grosor_pared=1.4, incluir_asa=True, con_preview=False):
    silueta = _silueta_modulo(personaje_img, alto_ref_mm=ancho_objetivo)
    scad = _armar_scad("cortante.scad", silueta)
    defines = {"ANCHO_OBJETIVO": ancho_objetivo, "ALTO_PARED": alto_pared,
               "GROSOR_PARED": grosor_pared, "INCLUIR_ASA": "true" if incluir_asa else "false"}
    stl = _run_openscad(scad, "stl", defines)
    png = _run_openscad(scad, "png", defines, camera="0,0,10,55,0,20,320") if con_preview else None
    return stl, png


def generar_cortante(tema, ancho_objetivo=80, alto_pared=20, grosor_pared=1.4,
                      incluir_asa=True, con_preview=False):
    return _generar_cortante_desde_personaje(_personaje_tema(tema), ancho_objetivo, alto_pared,
                                              grosor_pared, incluir_asa, con_preview)


def generar_cortante_kit(tema, n=5, ancho_objetivo=80, alto_pared=20, grosor_pared=1.4,
                          incluir_asa=True):
    """Kit de hasta `n` cortantes DISTINTOS del mismo tema — uno por personaje
    real (cuaderno.personajes_decorativos con variedad_estricta=True, para no
    repetir la misma figura recoloreada como si fueran 2 cortantes diferentes).
    incluir_objetos=True: temas con pocos TIPOS de personaje (probado contra
    el checkout real, no el de un worktree recién clonado con caché fresca:
    futbol/princesas/un-espacio-de-locura daban apenas 1, artistas/aviadores/
    bomberos/construccion/superheroes 2) completan con objetos del tema
    (corona, pelota, varita…) — mismo flag que ya usa cuaderno.py para el
    memory en temas de un solo personaje. Con incluir_objetos, los 12 temas
    actuales dan 5/5 (verificado contra el checkout real). Nunca menos de 3,
    si no alcanza levanta ValueError (no se vende un "kit" de 1-2 piezas).
    Devuelve una lista de bytes STL, uno por cortante."""
    import cuaderno
    personajes = cuaderno.personajes_decorativos(tema, n, variedad_estricta=True, incluir_objetos=True)
    if len(personajes) < 3:
        raise ValueError(
            "el tema %r no tiene suficientes personajes distintos para un kit "
            "de cortantes (mínimo 3, encontrados %d)" % (tema, len(personajes)))
    return [_generar_cortante_desde_personaje(p, ancho_objetivo, alto_pared, grosor_pared,
                                               incluir_asa, con_preview=False)[0]
            for p in personajes]


# ---------------------------------------------------------------------------
# Hoja de instrucciones de impresión (PDF simple, A4)
# ---------------------------------------------------------------------------

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


def _fuente_titulo(sz):
    for p in _fuentes_fredoka():
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.truetype(FUENTE_PATH, sz)


def _hoja_instrucciones(nombre, tema):
    Wp, Hp = 1240, 1754
    im = Image.new("RGB", (Wp, Hp), (253, 250, 242))
    dr = ImageDraw.Draw(im)
    dr.text((Wp / 2, 120), "Pack Cumple 3D", font=_fuente_titulo(56), fill=(60, 50, 45), anchor="mm")
    dr.text((Wp / 2, 180), f"{nombre} — tema {tema}", font=_fuente_titulo(28), fill=(120, 100, 90), anchor="mm")

    filas = [
        ("Contenido", "medalla.stl · topper.stl · trofeo.stl · cortante.stl"),
        ("Material sugerido", "PLA (más fácil de imprimir; para cortante, PLA o PETG apto alimentos)"),
        ("Altura de capa", "0.2mm está bien para todas las piezas"),
        ("Soportes", "Topper y cortante: no necesitan. Medalla y trofeo: no necesitan (planos/torneados)"),
        ("Relleno", "15-20% alcanza — son piezas decorativas, no estructurales"),
        ("Cortante de galletitas", "Lavar antes del primer uso. Apoyar el asa con dos dedos al cortar"),
    ]
    y = 300
    for titulo, texto in filas:
        dr.text((90, y), titulo, font=_fuente_titulo(26), fill=(107, 91, 210), anchor="lm")
        y += 40
        dr.text((90, y), texto, font=ImageFont.truetype(FUENTE_PATH, 22), fill=(60, 50, 45), anchor="lm")
        y += 60
    dr.text((Wp / 2, Hp - 60), "casatridimensional.com.ar", font=ImageFont.truetype(FUENTE_PATH, 18),
             fill=(180, 180, 180), anchor="mm")
    return im


# ---------------------------------------------------------------------------
# Pack completo — arma el ZIP final que descarga el cliente
# ---------------------------------------------------------------------------

def generar_pack_cumple(tema, nombre, edad=""):
    """Genera las 4 piezas personalizadas del pack + hoja de instrucciones y
    devuelve los bytes del ZIP final (igual a lo que se entrega en la compra)."""
    nombre = (nombre or "").strip() or "Cumple"
    edad = str(edad or "").strip()
    texto = f"{nombre.upper()} {edad}".strip() if edad else nombre.upper()

    medalla_stl, _ = generar_medalla(tema, texto)
    topper_stl, _ = generar_topper(tema, texto)
    trofeo_stl, _ = generar_trofeo(tema, texto)
    cortante_stl, _ = generar_cortante(tema)
    instrucciones = _hoja_instrucciones(nombre, tema)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("01_medalla.stl", medalla_stl)
        z.writestr("02_topper.stl", topper_stl)
        z.writestr("03_trofeo.stl", trofeo_stl)
        z.writestr("04_cortante.stl", cortante_stl)
        pdf_buf = io.BytesIO()
        # resolution=150: el lienzo es 1240x1754 ("A4 a 150dpi") — sin declararla
        # el PDF sale a otro tamaño físico (ver CLAUDE.md regla #5 y piezas._dpi_de).
        instrucciones.save(pdf_buf, "PDF", resolution=150)
        z.writestr("00_instrucciones.pdf", pdf_buf.getvalue())
    return buf.getvalue()
