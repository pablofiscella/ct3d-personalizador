#!/usr/bin/env python3
"""Verifica un abecedario ya generado, rehace las letras que salieron mal y lo instala.

El modelo de imágenes devuelve cada tanto la lámina sin la letra, o con otra. Este script
cierra el ciclo: lee cada banderín con `verificar_letras`, vuelve a pedir sólo las que no
dicen lo que tienen que decir, y recién instala cuando el tema está entero.

    python3 herramientas/corregir_abecedario.py <tema> [--intentos 2] [--no-instalar]

Nunca instala un tema incompleto o con letras mal: la regla del motor es **todo o nada**
—si falta una letra del nombre, la guirnalda entera sale con el método dibujado—, así que
instalar 30 de 32 no mejora nada y sí hace creer que el tema está listo.
"""
import base64
import importlib.util
import json
import os
import sys
import time

_PROY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROY)


def _mod(nombre):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(_PROY, "herramientas", nombre + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def corregir(tema, intentos=2, instalar=True):
    abc = _mod("abecedario")
    ver = _mod("verificar_letras")
    from ia_kit.client import OpenAIImageClient

    key = json.load(open(abc.CONFIG))["openai_api_key"]
    cli = OpenAIImageClient(key, model=abc.MODELO)
    lam = open(os.path.join(_PROY, "temas", tema, "extras", "banderin.png"), "rb").read()

    for vuelta in range(1, intentos + 2):
        filas = ver.analizar(tema)
        mal = [(f, q) for f, q, v, bien in filas if not bien]
        # Las que NO están en disco no aparecen en `analizar` —el glob sólo lista lo que
        # hay— y son justamente las que el filtro de seguridad rechazó al generar. Sin
        # esto, un tema al que le faltan letras se reporta "0 mal" y nunca se completa.
        faltan = [(os.path.basename(abc.ruta(abc.crudas(tema), x)), x)
                  for x in abc.LETRAS if not os.path.exists(abc.ruta(abc.crudas(tema), x))]
        pendientes = mal + faltan
        print("%s · vuelta %d: %d en disco, %d mal, %d sin generar%s"
              % (tema, vuelta, len(filas), len(mal), len(faltan),
                 (" -> " + ", ".join(f for f, _ in pendientes)) if pendientes else ""), flush=True)
        mal = pendientes
        if not mal or vuelta > intentos:
            break
        for archivo, letra in mal:
            destino = os.path.join(abc.crudas(tema), archivo)
            try:
                raw = cli.editar([lam], abc.PROMPT.format(letra=letra), "1024x1024", quality="medium")
                open(destino, "wb").write(raw if isinstance(raw, bytes) else base64.b64decode(raw))
            except Exception as e:                    # noqa: BLE001
                print("   %s: falló al rehacer (%s)" % (archivo, str(e)[:70]), flush=True)
                time.sleep(3)
        abc.limpiar(tema)

    filas = ver.analizar(tema)
    mal = [f for f, q, v, bien in filas if not bien]
    faltan = [x for x in abc.LETRAS if not os.path.exists(abc.ruta(abc.crudas(tema), x))]
    if mal or faltan:
        print("%s: QUEDA INCOMPLETO — %d mal, %d faltan. NO se instala." % (tema, len(mal), len(faltan)))
        return False
    if instalar:
        abc.instalar(tema)
    print("%s: %d letras verificadas y %s" % (tema, len(filas), "instaladas" if instalar else "listas"))
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    args = sys.argv[1:]
    n = 2
    if "--intentos" in args:
        n = int(args[args.index("--intentos") + 1])
    ok = corregir(args[0], intentos=n, instalar="--no-instalar" not in args)
    raise SystemExit(0 if ok else 1)
