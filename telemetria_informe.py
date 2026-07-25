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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--token", help="un cuaderno puntual")
    ap.add_argument("--grado", type=int, help="filtrar por grado (1-7)")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    a = ap.parse_args(argv)
    inf = informe(token=a.token, grado=a.grado)
    print(json.dumps(inf, ensure_ascii=False, indent=2) if a.json else _humano(inf))
    return 0


if __name__ == "__main__":
    sys.exit(main())
