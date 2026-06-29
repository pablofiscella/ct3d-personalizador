"""Orquesta la generación de todas las piezas de un tema hacia ia_draft/."""
import concurrent.futures
import glob
import os

from PIL import Image, ImageDraw, ImageFilter

import quitar_fondo
from . import catalogo
from .validate import validar_png

# Piezas que son un único círculo: se recortan a una máscara circular por código,
# así nada queda fuera del círculo (el prompt solo no lo garantiza).
_MASCARA_CIRCULAR = {"topper"}

# Piezas que se imprimen y cortan por contorno: fondo transparente + borde blanco,
# silueta sólida sin huecos (el software de print&cut corta offset del borde).
_DIE_CUT = {"stickers"}   # solo stickers son figuras die-cut; etiqueta/tarjeta/wrappers van rectangulares


def _rellenar_huecos(mask):
    """Rellena huecos internos (transparentes encerrados) de una máscara binaria L."""
    w, h = mask.size
    work = Image.new("L", (w + 2, h + 2), 0)
    work.paste(mask, (1, 1))
    ImageDraw.floodfill(work, (0, 0), 128)                # exterior alcanzable -> 128
    work = work.crop((1, 1, w + 1, h + 1))
    return work.point(lambda p: 0 if p == 128 else 255)   # sólido = forma + huecos


def _borde_sticker(im, frac=0.02):
    """Die-cut: silueta SÓLIDA (cierra gaps finos y rellena huecos internos) + borde blanco.
    TODA la morfología se hace en baja resolución (MaxFilter a full-res con kernel grande es
    lentísimo); la máscara final se escala a resolución completa. El arte va crudo encima."""
    im = im.convert("RGBA")
    w, h = im.size
    a = im.getchannel("A").point(lambda p: 255 if p > 10 else 0)
    esc = min(1.0, 384.0 / max(w, h))
    sw, sh = max(8, int(w * esc)), max(8, int(h * esc))
    ks = min(2 * max(2, int(min(sw, sh) * frac * 1.5)) + 1, 21)   # cerrar gaps
    kb = min(2 * max(2, int(min(sw, sh) * frac)) + 1, 21)         # borde
    sm = a.resize((sw, sh)).point(lambda p: 255 if p > 128 else 0)
    sm = sm.filter(ImageFilter.MaxFilter(ks))             # cerrar gaps finos
    sm = _rellenar_huecos(sm)                             # rellenar huecos encerrados
    sm = sm.filter(ImageFilter.MinFilter(ks))             # restaurar (close morfológico)
    sm = sm.filter(ImageFilter.MaxFilter(kb))             # + borde blanco
    borde = sm.resize((w, h)).point(lambda p: 255 if p > 128 else 0)
    base = Image.composite(Image.new("RGBA", (w, h), (255, 255, 255, 255)),
                           Image.new("RGBA", (w, h), (0, 0, 0, 0)), borde)
    base.alpha_composite(im)                              # arte crudo encima; huecos quedan blancos
    bb = base.getbbox()
    return base.crop(bb) if bb else base


def _mascara_circular(im):
    im = im.convert("RGBA")
    w, h = im.size
    d = min(w, h)
    x0, y0 = (w - d) // 2, (h - d) // 2
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse([x0, y0, x0 + d - 1, y0 + d - 1], fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    bb = out.getbbox()
    return out.crop(bb) if bb else out

# invitacion es el único slot que va a la raíz temas/<tema>/; el resto va a extras/.


def _refs(tema_dir):
    # Referencias visuales para OpenAI: primero los cutouts de recortes/; si no hay,
    # el arte base del tema (invitación/afiche), que ya muestra los personajes y el estilo.
    paths = sorted(glob.glob(os.path.join(tema_dir, "recortes", "*.png")))
    if not paths:
        paths = (sorted(glob.glob(os.path.join(tema_dir, "invitacion_*.png")))
                 + sorted(glob.glob(os.path.join(tema_dir, "afiche_*.png"))))
    return [open(p, "rb").read() for p in paths[:10]]  # OpenAI admite hasta 16


def _guardar(im, draft_dir, nombre):
    os.makedirs(draft_dir, exist_ok=True)
    im.save(os.path.join(draft_dir, nombre))


def contar_piezas(edades, solo=None):
    """Cuántas piezas generará generar_tema (para la barra de progreso)."""
    return sum((len(edades) if p.por_edad else 1)
               for p in catalogo.PIEZAS if not (solo and p.key not in solo))


def _nombre_pieza(p, edad):
    # El nombre de archivo debe matchear lo que productos._piezas_kit levanta.
    if p.key == "invitacion":
        return "invitacion_%d.png" % int(edad)              # -> slot raíz vía aprobar
    if p.key in catalogo.EXTRAS_POR_EDAD:
        e = int(edad) if p.por_edad else 1                  # arte único -> _1 (el motor lo reusa)
        return "%s_%d.png" % (p.key, e)                     # -> extras/
    return "%s.png" % p.key                                 # universal -> extras/


def generar_tema(client, temas_dir, tema, edades, progress=None, solo=None,
                 quitar=quitar_fondo.remove_bg, concurrencia=4, calidad="medium",
                 reusar_maestra=False):
    tema_dir = os.path.join(temas_dir, tema)
    draft = os.path.join(tema_dir, "ia_draft")
    pal = catalogo.paleta_de(temas_dir, tema)
    refs = _refs(tema_dir)
    if not refs:
        raise RuntimeError(
            "El tema '%s' no tiene imágenes de referencia: subí personajes a "
            "recortes/ o cargá el arte base (invitacion_*/afiche_*)." % tema)
    # imagen maestra de estilo: ancla de consistencia, se manda como ref extra.
    # Se cachea en ia_maestra.png (fuera de ia_draft, no se publica) para reusarla al
    # regenerar una pieza suelta -> regenerar = 1 sola llamada, sin rehacer la maestra.
    cache_maestra = os.path.join(tema_dir, "ia_maestra.png")
    if reusar_maestra and os.path.exists(cache_maestra):
        with open(cache_maestra, "rb") as f:
            maestra = f.read()
    else:
        maestra = client.editar(refs, "Lámina maestra de estilo del tema. " +
                                catalogo.bloque_estilo(pal), catalogo._SQUARE, quality=calidad)
        with open(cache_maestra, "wb") as f:
            f.write(maestra)
    refs_full = refs + [maestra]
    os.makedirs(draft, exist_ok=True)

    work = [(p, edad) for p in catalogo.PIEZAS
            if not (solo and p.key not in solo)
            for edad in (edades if p.por_edad else [None])]

    def _trabajo(p, edad):
        # corre en un thread; captura sus propios errores y devuelve el evento.
        try:
            raw = client.editar(refs_full, catalogo.prompt_de(pal, p, edad), p.size,
                                 quality=calidad)
            im = validar_png(raw, size_esperado=tuple(int(x) for x in p.size.split("x")))
            im = im.convert("RGBA")
            if p.key in _MASCARA_CIRCULAR:      # círculo garantizado por código
                im = _mascara_circular(im)
            elif p.key in _DIE_CUT:             # die-cut: transparente + borde blanco, sin huecos
                im = quitar(im, protect=True)
                im = _borde_sticker(im)
            elif p.recorte:
                im = quitar(im, protect=True)
                bb = im.getbbox()
                if bb:
                    im = im.crop(bb)
            nombre = _nombre_pieza(p, edad)
            _guardar(im, draft, nombre)
            return {"pieza": p.key, "edad": edad, "ok": True, "error": "", "archivo": nombre}
        except Exception as e:  # una pieza que falla no frena a las demás
            return {"pieza": p.key, "edad": edad, "ok": False, "error": str(e), "archivo": ""}

    generadas, errores = [], []
    # Las piezas se generan en paralelo (gpt-image-2 es lento); el thread principal
    # es el único que emite progreso y acumula -> sin necesidad de locks.
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, concurrencia)) as ex:
        futs = [ex.submit(_trabajo, p, edad) for (p, edad) in work]
        for fut in concurrent.futures.as_completed(futs):
            evt = fut.result()
            if progress:
                progress(evt)
            (generadas if evt["ok"] else errores).append(evt)
    return {"generadas": generadas, "errores": errores}
