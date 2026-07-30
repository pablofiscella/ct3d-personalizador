#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arte del rompecabezas del cuaderno: una escena por NIVEL y por grado.

Pablo, 30-jul-2026: *"¿podés hacer que esto también sea adaptativo? Que cambie imágenes
y que cambie cantidad de piezas a medida que ves que lo saca fácil"*.

POR QUÉ HAY QUE GENERAR ARTE. El token tenía UNA sola ilustración completa por grado
(`actividades_arte/g<N>/escena.png`) y las 3 páginas para colorear, que son línea negra
sobre blanco: como rompecabezas serían ilegibles. Con una sola imagen, "que cambie" no se
puede cumplir.

DE DÓNDE SALE LA VARIEDAD. El grado ya tiene su escenario Y su elenco de 8 personajes
(`s00..s07.png`), que hoy el player ya superpone en vivo en «¿Cuántos hay?». Acá esa misma
combinación se HORNEA: cada nivel recibe un reparto distinto, en posiciones distintas. No
es arte nuevo ni una llamada de IA — es el arte del grado, combinado.

MÁS PERSONAJES = MÁS FÁCIL, y por eso el nivel 0 es el más poblado. En un rompecabezas lo
que cuesta son las zonas lisas (cielo, follaje parejo): cada personaje es una referencia
que le dice al chico dónde va la pieza. Así la escalera sube por los dos lados a la vez —
más piezas y menos referencias.

VIVEN EN EL REPO, NO EN EL TOKEN. Son idénticas para todos los cuadernos del mismo grado,
así que se sirven como el player, el audio de consignas y las lecciones en video: una sola
copia, y mejorar el arte llega también a los links YA ENTREGADOS. Copiarlas por token
habría sido ~600 KB × cada cuaderno vendido, para guardar el mismo dibujo N veces.

    python3 infra/generar-rompecabezas-arte.py            # los grados que lo llevan
    python3 infra/generar-rompecabezas-arte.py 1          # sólo 1.º
"""
import os
import random
import sys

from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

ARTE = os.path.join(BASE, "actividades_arte")

# Cuántos personajes lleva la escena de cada nivel. Decrece a propósito: ver el docstring.
# El largo de esta lista ES la cantidad de niveles, y tiene que coincidir con
# `actividades_web._ROMPE_GRADO`; hay test que lo verifica.
ELENCO_POR_NIVEL = (5, 4, 4, 3)


def _escena_de_nivel(grado, nivel, cuantos):
    """La escena del grado con `cuantos` personajes horneados encima.

    La semilla depende de (grado, nivel), así que regenerar da SIEMPRE lo mismo: el arte
    es un archivo committeado, no puede cambiar solo entre corridas."""
    d = os.path.join(ARTE, "g%d" % grado)
    fondo = Image.open(os.path.join(d, "escena.png")).convert("RGB")
    W, H = fondo.size
    stickers = sorted(f for f in os.listdir(d)
                      if f.startswith("s") and f.endswith(".png"))
    if not stickers:
        raise SystemExit("g%d no tiene personajes (s##.png)" % grado)
    rnd = random.Random(grado * 1000 + nivel)
    elegidos = rnd.sample(stickers, min(cuantos, len(stickers)))
    n = len(elegidos)
    for i, fn in enumerate(elegidos):
        with Image.open(os.path.join(d, fn)) as src:
            p = src.convert("RGBA")
        # Profundidad: el primero va adelante (más grande y más abajo) y el último atrás.
        # Sin esto quedaban todos del mismo tamaño sobre una misma línea, que se lee como
        # una fila de figuritas pegadas y no como una escena.
        prof = i / max(1, n - 1)
        alto = H * (0.40 - 0.13 * prof) * rnd.uniform(0.92, 1.06)
        esc = alto / p.height
        p = p.resize((max(1, int(p.width * esc)), max(1, int(alto))), Image.LANCZOS)
        # repartidos a lo ancho, con los pies apoyados cerca del borde inferior
        x = int(W * (0.06 + 0.88 * ((i + 0.5) / n)) - p.width / 2)
        y = int(H * (0.97 - 0.15 * prof) - p.height)
        fondo.paste(p, (max(0, min(x, W - p.width)), max(0, min(y, H - p.height))), p)
    # El tablero mide ~360 px en un teléfono y ~600 en una pantalla grande: 1536 es el
    # doble de lo que hace falta incluso en retina, y son archivos que van al repo.
    return fondo.resize((1200, int(1200 * H / W)), Image.LANCZOS)


def generar(grado):
    """Por nivel: la escena (.jpg) y los CORTES (.json). Los dos al repo, los dos iguales
    para todos los cuadernos del grado.

    Los cortes se hornean acá, y no por token en `_rompecabezas_json`, porque medido pesan
    35-49 KB por cuaderno y el `data.json` lo baja el navegador en CADA carga: metidos ahí
    eran el 75% del archivo, para una actividad entre 40. Un corte distinto por chico no
    aporta nada —nunca comparan cuadernos— y en cambio cuesta esos KB en cada apertura.
    Acá se piden recién al abrir la actividad, y el navegador los cachea 24 h."""
    import json
    import actividades_web as aw
    import rompecabezas_web as rw
    d = os.path.join(ARTE, "g%d" % grado)
    if not os.path.isdir(d):
        raise SystemExit("no existe %s" % d)
    escalera = aw._ROMPE_GRADO.get(grado)
    if not escalera:
        raise SystemExit("g%d no está en _ROMPE_GRADO: no lleva rompecabezas" % grado)
    if len(escalera) != len(ELENCO_POR_NIVEL):
        raise SystemExit("g%d tiene %d escalones y hay %d escenas por nivel"
                         % (grado, len(escalera), len(ELENCO_POR_NIVEL)))
    out = []
    for nivel, cuantos in enumerate(ELENCO_POR_NIVEL):
        im = _escena_de_nivel(grado, nivel, cuantos)
        p = os.path.join(d, "romp_%d.jpg" % nivel)
        im.save(p, quality=84, optimize=True)
        cols, filas = escalera[nivel]
        # semilla por (grado, nivel): con una sola, los cuatro niveles tendrían el mismo
        # corte y el de 12 piezas se vería como el de 6 con líneas de más
        b = rw._bordes_json(cols, filas, 7331 + grado * 101 + nivel)
        pj = os.path.join(d, "romp_%d.json" % nivel)
        with open(pj, "w", encoding="utf-8") as f:
            json.dump({"cols": cols, "filas": filas, "bordes": b}, f, separators=(",", ":"))
        out.append((p, im.size, os.path.getsize(p), os.path.getsize(pj)))
    return out


if __name__ == "__main__":
    import actividades_web as aw
    grados = [int(a) for a in sys.argv[1:]] or sorted(aw._ROMPE_GRADO)
    for g in grados:
        print("g%d" % g)
        for p, (w, h), b, bj in generar(g):
            print("   %-14s %dx%d  %d KB  + cortes %d KB"
                  % (os.path.basename(p), w, h, b // 1024, bj // 1024))
