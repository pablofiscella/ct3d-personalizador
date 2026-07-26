#!/usr/bin/env python3
"""Crea (o regenera) el cuaderno de MUESTRA PÚBLICA que enlaza la landing de Kydo.

POR QUÉ EXISTE
--------------
La landing describía el producto sin mostrarlo: un padre que llegaba de un anuncio
leía "219 saberes" y se iba. Esto crea un cuaderno de 4.º grado **sin gate de cuenta**
para que la página pueda enlazar "Probalo ahora" y que el visitante caiga JUGANDO.

4.º no es un grado cualquiera: es el más profundo del sistema (63 saberes, 39 juegos)
y es el que Pablo regala este año. La muestra enseña lo mejor que hay.

CÓMO SE USA DESDE LA LANDING
---------------------------
    https://kit.casatridimensional.com.ar/act/<token>/?muestra=angulos

`?muestra=<id>` (ver `muestraPedida()` en actividades_player.js) abre ESE juego directo,
sin pasar por "¿Quién juega?". Sin el parámetro, el mismo link muestra el menú completo
de 4.º — que es la vidriera: 39 juegos con sus etiquetas del motor adaptativo.

SEGURIDAD DEL GATE
------------------
`requiere_cuenta=False` es lo que lo hace público (ver `estado_gate`). Es DELIBERADO y
sólo para este token. Si alguna vez hay que cortarlo: `actividades_web.revocar(TOKEN)`.

Es idempotente: correrlo de nuevo regenera el mismo token, no crea uno nuevo.

    python3 infra/crear-muestra-publica.py            # crea/regenera
    python3 infra/crear-muestra-publica.py --listar   # muestra los links, no toca nada
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import actividades_web as aw  # noqa: E402

# Token FIJO y legible: la landing lo enlaza y no queremos que cambie en cada deploy.
TOKEN = "muestra-kydo-4"
GRADO = "4"
BASE = "https://kit.casatridimensional.com.ar"

# Una muestra por materia. Las cuatro elegidas tienen lección en video (botón "¿Cómo es?"),
# que es justamente lo que la landing quiere probar: no son ejercicios sueltos, enseñan.
MUESTRAS = [
    ("Matemática", "angulos", "Agudo, recto u obtuso"),
    ("Lengua", "abstractos_concretos", "Abstracto o concreto"),
    ("Naturales", "laboratorio_electrico", "Laboratorio eléctrico"),
    ("Sociales", "provincias_region", "¿De qué región es?"),
]


def links():
    yield ("menú completo", "%s/act/%s/" % (BASE, TOKEN))
    for materia, juego, titulo in MUESTRAS:
        yield ("%s · %s" % (materia, titulo), "%s/act/%s/?muestra=%s" % (BASE, TOKEN, juego))


def main():
    if "--listar" in sys.argv:
        for que, url in links():
            print("  %-34s %s" % (que, url))
        return 0

    catalogo = aw.catalogo_actividades().get(int(GRADO)) or []
    disponibles = {it["id"] for it in catalogo}
    faltan = [j for _, j, _ in MUESTRAS if j not in disponibles]
    if faltan:
        # Falla ruidosa: un juego que no está en el grado daría un link que abre el menú
        # en vez de la muestra, y eso en la landing se lee como "el botón no anda".
        print("ERROR: estos juegos no están en %s.º grado: %s" % (GRADO, ", ".join(faltan)),
              file=sys.stderr)
        return 1

    tok = aw.crear(
        {
            "nombre": "Peque",          # placeholder del cuaderno escolar, no un chico
            "edad": GRADO,
            "escolar_on": 1,            # menú por grado + arte de grado
            "adaptativo_on": 1,         # las etiquetas "Recomendado"/"Reforzá antes" se ven
            "requiere_cuenta": 0,       # ← PÚBLICO a propósito: es la muestra de la landing
        },
        "escolar",
        token=TOKEN,
    )
    req, revocado = aw.estado_gate(tok)
    if req or revocado:
        print("ERROR: el token quedó gateado (requiere_cuenta=%s revocado=%s)" % (req, revocado),
              file=sys.stderr)
        return 1

    print("muestra pública lista: %s (%d juegos en %s.º)" % (tok, len(catalogo), GRADO))
    for que, url in links():
        print("  %-34s %s" % (que, url))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
