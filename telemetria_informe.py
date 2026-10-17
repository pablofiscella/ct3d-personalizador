#!/usr/bin/env python3
"""Lee la telemetría de TODOS los cuadernos y dice qué actividad frena a los chicos.

Por qué existe: el player venía escribiendo un `telemetria.jsonl` por token desde el
19-jul y no lo leía nadie. El piloto de 4° genera ese dato UNA sola vez —30 chicos
usando el cuaderno por primera vez— y sin agregarlo se pierde la única evidencia real
de qué construir después. La opinión de los padres la vamos a tener igual; esto es lo
que dicen los chicos sin que nadie les pregunte.

Qué contesta, que es lo que la investigación de ALEKS/DreamBox dice que hay que mirar:
  - qué actividades tienen mala precisión al PRIMER intento (contenido difícil de más,
    o consigna confusa: las distingue el tiempo hasta el primer toque);
  - dónde se abandona (se abrió la actividad y no se terminó);
  - qué tipo de error domina en cada actividad → qué explicación conviene mejorar;
  - qué aciertos huelen a ENSAYO Y ERROR (muchos toques antes de acertar), que es
    justo lo que el resultado solo no puede distinguir de "lo sabe".

Uso:
    python3 telemetria_informe.py                    # todos los tokens
    python3 telemetria_informe.py --grado 4          # sólo 4°
    python3 telemetria_informe.py --token abc123     # un cuaderno
    python3 telemetria_informe.py --json             # para procesar
"""
import argparse
import datetime
import json
import os
import statistics
import sys

BASEDIR = os.path.dirname(os.path.abspath(__file__))
# Overridable para poder correr el informe contra otra instalación (o desde los tests)
# sin copiar el script al lado de los datos.
ACT_DIR = os.environ.get("CT3D_ACT_DIR") or os.path.join(BASEDIR, "actividades")

# Umbrales. Son criterios de lectura, no verdades: se declaran acá arriba para poder
# discutirlos con el dato del piloto en la mano en vez de que queden pegados al código.
PRECISION_BAJA = 0.55      # <55% al primer intento = la actividad está costando
CONSIGNA_LENTA = 12000     # >12s hasta el primer toque = no entendió QUÉ hay que hacer
TOQUES_TANTEO = 6          # >6 toques antes de acertar = probó hasta que salió
MIN_MUESTRA = 5            # menos que esto no se reporta: sería ruido con forma de dato

# ── ACTIVIDAD TRABADA: el chico no puede terminarla y se queda pegado ────────────
#
# POR QUÉ EXISTE (19-sep-2026). La sopa de letras aceptaba sólo el arrastre, no lo decía
# en ninguna parte y al gesto equivocado contestaba con silencio. Una chica de 4.º estuvo
# ONCE MINUTOS con 23 intentos fallidos. El informe de arriba **no lo vio**: marca
# "contenido difícil" por precisión baja, y con eso también marca al memotest —donde
# fallar el primer intento ES la mecánica—, así que la señal se pierde entre falsos
# positivos. Pablo: *"la telemetría tiene que hacer saltar inmediatamente estos errores"*.
#
# LO QUE DISTINGUE "TRABADA" DE "DIFÍCIL" ES EL TIEMPO PEGADO, no el error. Fallar rápido
# y seguir es aprender; fallar diez veces durante diez minutos es una actividad que no se
# puede terminar.
#
# POR SESIÓN Y NO POR CUADERNO: los cuadernos de muestra (`muestra-kydo-N`) los usan
# MUCHAS personas distintas con el mismo token. Agrupando por token, la chica de la sopa
# quedaba diluida entre todas las visitas —43 fallos, 30 minutos y 60 % de aciertos, que no
# alarma a nadie—. Separando por sesión aparece sola: 23 fallos, 10 minutos, 15 %.
#
# Los umbrales se calibraron contra los 2.174 eventos reales que había el 19-sep-2026:
# marcan 2 sesiones de 585 (la sopa y una de acentuación del 25-jul) y NO marcan ninguna
# de memotest. Si algún día empieza a avisar de más, se toca acá y se vuelve a medir.
SESION_CORTE_MS = 20 * 60 * 1000   # 20 min sin tocar = otra persona u otro día
TRABA_FALLOS = 8                   # intentos fallidos en la misma sesión
TRABA_MINUTOS = 5                  # pegado a la misma actividad
TRABA_PRECISION = 0.35             # y con menos de esto de aciertos


def _eventos(token=None):
    """Todos los eventos, con el token de dónde vino cada uno."""
    if not os.path.isdir(ACT_DIR):
        return []
    tokens = [token] if token else sorted(os.listdir(ACT_DIR))
    out = []
    for tk in tokens:
        p = os.path.join(ACT_DIR, tk, "telemetria.jsonl")
        if not os.path.isfile(p):
            continue
        edad_tok = None
        try:
            with open(os.path.join(ACT_DIR, tk, "data.json"), encoding="utf-8") as f:
                edad_tok = json.load(f).get("edad")
        except Exception:
            pass
        with open(p, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    ev = json.loads(linea)
                except ValueError:
                    continue          # una línea rota no invalida el archivo entero
                if isinstance(ev, dict):
                    ev["_token"] = tk
                    ev.setdefault("edad", edad_tok)
                    out.append(ev)
    return out


def _grado_de(ev):
    try:
        return int(str(ev.get("edad")).strip()) - 5
    except (TypeError, ValueError):
        return None


def informe(token=None, grado=None):
    evs = [e for e in _eventos(token) if e.get("j")]
    if grado is not None:
        evs = [e for e in evs if _grado_de(e) == grado]

    porj = {}
    for e in evs:
        d = porj.setdefault(e["j"], {"primeros": [], "motivos": {}, "ms1": [],
                                     "toques_ok": [], "tokens": set(), "eventos": 0})
        d["eventos"] += 1
        d["tokens"].add(e.get("_token"))
        if e.get("primer"):
            d["primeros"].append(bool(e.get("ok")))
            if e.get("ms1") is not None:
                d["ms1"].append(e["ms1"])
            if e.get("ok") and e.get("toq") is not None:
                d["toques_ok"].append(e["toq"])
        if not e.get("ok") and e.get("motivo"):
            d["motivos"][e["motivo"]] = d["motivos"].get(e["motivo"], 0) + 1

    filas = []
    for j, d in porj.items():
        n = len(d["primeros"])
        if n < MIN_MUESTRA:
            continue
        prec = sum(d["primeros"]) / float(n)
        med_ms1 = statistics.median(d["ms1"]) if d["ms1"] else None
        med_toq = statistics.median(d["toques_ok"]) if d["toques_ok"] else None
        motivo_top = max(d["motivos"].items(), key=lambda kv: kv[1])[0] if d["motivos"] else None
        señales = []
        # Distinguir las dos causas es el punto: el contenido se arregla con dificultad,
        # la consigna se arregla con redacción. Confundirlas hace perder el tiempo.
        if prec < PRECISION_BAJA and med_ms1 is not None and med_ms1 > CONSIGNA_LENTA:
            señales.append("consigna confusa")
        elif prec < PRECISION_BAJA:
            señales.append("contenido difícil")
        if med_toq is not None and med_toq > TOQUES_TANTEO:
            señales.append("acierta tanteando")
        filas.append({
            "juego": j, "muestra": n, "precision_primer_intento": round(prec, 3),
            "ms_hasta_primer_toque": med_ms1, "toques_al_acertar": med_toq,
            "error_dominante": motivo_top, "chicos": len(d["tokens"]),
            "señales": señales,
        })
    filas.sort(key=lambda f: (f["precision_primer_intento"], -f["muestra"]))
    return {
        "eventos": len(evs),
        "cuadernos": len({e.get("_token") for e in evs}),
        "juegos_con_muestra": len(filas),
        "actividades": filas,
    }


def _humano(inf):
    L = []
    L.append("TELEMETRÍA — %d eventos de %d cuadernos, %d actividades con muestra suficiente"
             % (inf["eventos"], inf["cuadernos"], inf["juegos_con_muestra"]))
    if not inf["actividades"]:
        L.append("")
        L.append("Todavía no hay datos suficientes (hacen falta %d primeros intentos por")
        L.append("actividad). Es lo esperable antes del piloto: el dato lo generan los chicos.")
        return "\n".join(L) % MIN_MUESTRA if "%d" in L[2] else "\n".join(L)
    L.append("")
    L.append("%-26s %6s %7s %8s %7s  %s" %
             ("actividad", "n", "1er int", "ms toque", "toques", "señal"))
    for f in inf["actividades"]:
        L.append("%-26s %6d %6.0f%% %8s %7s  %s" % (
            f["juego"][:26], f["muestra"], 100 * f["precision_primer_intento"],
            "—" if f["ms_hasta_primer_toque"] is None else int(f["ms_hasta_primer_toque"]),
            "—" if f["toques_al_acertar"] is None else int(f["toques_al_acertar"]),
            ", ".join(f["señales"]) or ""))
    conseñal = [f for f in inf["actividades"] if f["señales"]]
    if conseñal:
        L.append("")
        L.append("A MIRAR (%d):" % len(conseñal))
        for f in conseñal:
            extra = (" · error más común: %s" % f["error_dominante"]) if f["error_dominante"] else ""
            L.append("  · %s — %s%s" % (f["juego"], ", ".join(f["señales"]), extra))
    return "\n".join(L)


def sesiones(token=None):
    """Los eventos partidos en sesiones: mismo cuaderno, misma actividad, sin huecos
    largos. Es lo más cerca que se puede estar de "una persona sentada jugando", porque
    la telemetría no trae quién es —y no debe traerlo."""
    evs = sorted([e for e in _eventos(token) if e.get("j") and e.get("t")],
                 key=lambda e: ((e.get("_token") or ""), e["j"], e["t"]))
    out, act = [], None
    for e in evs:
        k = (e.get("_token"), e["j"])
        if act and act["clave"] == k and e["t"] - act["fin"] <= SESION_CORTE_MS:
            act["eventos"].append(e); act["fin"] = e["t"]
        else:
            act = {"clave": k, "eventos": [e], "ini": e["t"], "fin": e["t"]}
            out.append(act)
    return out


def trabadas(token=None):
    """Las sesiones donde alguien se quedó pegado sin poder terminar la actividad.

    Devuelve lo que hace falta para actuar: qué actividad, cuándo, cuánto tiempo, cuántos
    fallos y con qué motivo de error, ordenado por gravedad."""
    filas = []
    for s in sesiones(token):
        evs = s["eventos"]
        ok = sum(1 for e in evs if e.get("ok"))
        fallos = len(evs) - ok
        minutos = (s["fin"] - s["ini"]) / 60000.0
        prec = ok / float(len(evs)) if evs else 0.0
        if fallos < TRABA_FALLOS or minutos < TRABA_MINUTOS or prec >= TRABA_PRECISION:
            continue
        motivos = {}
        for e in evs:
            if not e.get("ok") and e.get("motivo"):
                motivos[e["motivo"]] = motivos.get(e["motivo"], 0) + 1
        filas.append({
            "juego": s["clave"][1],
            "cuaderno": s["clave"][0],
            "cuando": datetime.datetime.fromtimestamp(s["ini"] / 1000).isoformat(timespec="minutes"),
            "epoch_ms": s["ini"],
            "minutos": round(minutos, 1),
            "fallos": fallos,
            "aciertos": ok,
            "precision": round(prec, 2),
            "edad": next((e.get("edad") for e in evs if e.get("edad")), None),
            "error_dominante": (max(motivos.items(), key=lambda kv: kv[1])[0] if motivos else None),
        })
    filas.sort(key=lambda f: (-f["fallos"], -f["minutos"]))
    return filas


def _humano_trabadas(filas):
    if not filas:
        return "Ninguna actividad dejó a nadie trabado. (>=%d fallos, >=%d min y <%d%% de aciertos en una sesión.)" % (
            TRABA_FALLOS, TRABA_MINUTOS, int(TRABA_PRECISION * 100))
    L = ["SE TRABARON EN %d actividad(es):" % len(filas), ""]
    for f in filas:
        L.append("  · %s — %d fallos en %.1f min, %d%% de aciertos%s" % (
            f["juego"], f["fallos"], f["minutos"], int(f["precision"] * 100),
            (" (%s años)" % f["edad"]) if f["edad"] else ""))
        L.append("      %s · cuaderno %s" % (f["cuando"].replace("T", " "), f["cuaderno"]))
        if f["error_dominante"]:
            L.append("      error más común: %s" % f["error_dominante"][:70])
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--token", help="un cuaderno puntual")
    ap.add_argument("--grado", type=int, help="filtrar por grado (1-7)")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    ap.add_argument("--trabadas", action="store_true",
                    help="sólo las actividades donde alguien se quedó pegado sin poder terminar")
    a = ap.parse_args(argv)
    if a.trabadas:
        filas = trabadas(token=a.token)
        print(json.dumps(filas, ensure_ascii=False, indent=2) if a.json else _humano_trabadas(filas))
        return 0
    inf = informe(token=a.token, grado=a.grado)
    print(json.dumps(inf, ensure_ascii=False, indent=2) if a.json else _humano(inf))
    return 0


if __name__ == "__main__":
    sys.exit(main())
