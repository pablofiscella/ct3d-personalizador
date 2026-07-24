/* Motor adaptativo — PILOTO 4° Matemática. Capa de SABERES sobre el Store del player.
   GENERADO desde saberes.py (mantener en sync, no editar a mano el bloque de datos).
   Gateado por D.adaptativo_on: si el token no lo tiene, el player NO lo usa y nada cambia. */

const SABERES_MOTOR = { "MAT-3-NUM": { "nombre": "Numeración hasta 1.000", "grado": 3, "eje": "numeracion", "prereqs": [], "juegos": [] }, "MAT-3-SUMARESTA": { "nombre": "Suma y resta con llevada/canje (3° cifras)", "grado": 3, "eje": "operaciones", "prereqs": [ "MAT-3-NUM" ], "juegos": [] }, "MAT-3-TABLAS": { "nombre": "Tablas de multiplicar (memorización)", "grado": 3, "eje": "operaciones", "prereqs": [], "juegos": [] }, "MAT-3-MULT": { "nombre": "Concepto de multiplicación", "grado": 3, "eje": "operaciones", "prereqs": [ "MAT-3-SUMARESTA", "MAT-3-TABLAS" ], "juegos": [] }, "MAT-3-DIV": { "nombre": "Concepto de división y reparto", "grado": 3, "eje": "operaciones", "prereqs": [ "MAT-3-MULT" ], "juegos": [] }, "MAT-4-SERIES": { "nombre": "Series numéricas (¿qué número falta?)", "grado": 4, "eje": "numeracion", "prereqs": [ "MAT-3-NUM" ], "juegos": [ "serie" ] }, "MAT-4-RECTA": { "nombre": "Ubicar números en la recta numérica", "grado": 4, "eje": "numeracion", "prereqs": [ "MAT-3-NUM" ], "juegos": [ "recta_numerica" ] }, "MAT-4-SUMA": { "nombre": "Suma en columna (números grandes)", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-3-SUMARESTA" ], "juegos": [ "suma_columnas" ] }, "MAT-4-TABLAS": { "nombre": "Agilidad con las tablas", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-3-TABLAS" ], "juegos": [ "tablas_ninja" ] }, "MAT-4-MUL": { "nombre": "Multiplicación (algoritmo)", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-TABLAS", "MAT-3-MULT" ], "juegos": [ "multiplicar" ] }, "MAT-4-DIV": { "nombre": "División por una cifra", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-MUL", "MAT-3-DIV" ], "juegos": [ "dividir" ] }, "MAT-4-DIV-LARGA": { "nombre": "División larga / cuenta larga", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-DIV" ], "juegos": [ "cuenta_larga" ] }, "MAT-4-PROB": { "nombre": "Problemas de multiplicación y división", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-MUL", "MAT-4-DIV" ], "juegos": [ "problemas_mult_div" ] }, "MAT-4-FRAC-ENTERO": { "nombre": "Concepto de fracción (parte de un entero)", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-3-DIV" ], "juegos": [ "completar_entero" ] }, "MAT-4-FRAC-CANT": { "nombre": "Fracción de una cantidad (reparto)", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-4-FRAC-ENTERO", "MAT-4-DIV" ], "juegos": [ "reparto_fracciones" ] }, "MAT-4-FRAC-EQUIV": { "nombre": "Fracciones equivalentes", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-4-FRAC-ENTERO" ], "juegos": [ "fracciones_equivalentes" ] }, "MAT-4-FRAC-COMP": { "nombre": "Comparar fracciones (cuál es más grande)", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-4-FRAC-EQUIV" ], "juegos": [ "duelo_fracciones" ] }, "MAT-4-DECIMALES": { "nombre": "Comparar decimales (décimos/centésimos)", "grado": 4, "eje": "decimales", "prereqs": [ "MAT-4-FRAC-ENTERO" ], "juegos": [ "duelo_decimales" ] }, "MAT-4-OFERTA": { "nombre": "Comparar precios / mejor oferta", "grado": 4, "eje": "medida", "prereqs": [ "MAT-4-MUL" ], "juegos": [ "mejor_oferta" ] }, "MAT-4-ANGULOS": { "nombre": "Clasificar ángulos (recto/agudo/obtuso)", "grado": 4, "eje": "geometria", "prereqs": [], "juegos": [ "angulos" ] } };

/* ── Adapt: capa de saberes sobre el Store del player (no bloquea, solo informa/ordena) ── */
const _JUEGO_A_SABERES = (() => {
  const m = {};
  for (const sid in SABERES_MOTOR)
    for (const j of SABERES_MOTOR[sid].juegos) (m[j] = m[j] || []).push(sid);
  return m;
})();

const Adapt = {
  _store() { return (typeof Store !== "undefined") ? Store : null; },
  // grado anterior (<4) = asumido dominado (el chico está en 4°); saber de 4° = dominado si
  // alguna actividad que lo mide tiene sello 'dominado'/'consolidado' en el Store.
  saberDominado(sid) {
    const s = SABERES_MOTOR[sid];
    if (!s) return false;
    if (s.grado < 4) return true;
    const st = this._store();
    return !!st && s.juegos.some((j) => {
      const sel = st.sello(j);
      return sel === "dominado" || sel === "consolidado";
    });
  },
  _dominados() {
    const set = new Set();
    for (const sid in SABERES_MOTOR) if (this.saberDominado(sid)) set.add(sid);
    return set;
  },
  _prereqsOk(sid, dom) { return SABERES_MOTOR[sid].prereqs.every((p) => dom.has(p)); },
  // 'repaso' | 'dominado' | 'recomendado' | 'disponible' | 'reforzar'
  estadoActividad(actId) {
    const st = this._store();
    if (st && st.repasoPendiente && st.repasoPendiente(actId)) return "repaso";
    const saberes = _JUEGO_A_SABERES[actId];
    if (!saberes || !saberes.length) return "disponible";  // fuera del piloto (otra materia/lógica)
    const dom = this._dominados();
    if (saberes.every((s) => dom.has(s))) return "dominado";
    if (saberes.some((s) => !dom.has(s) && this._prereqsOk(s, dom))) return "recomendado";
    return "reforzar";  // prereqs sin dominar → conviene reforzar antes (pero se puede jugar igual)
  },
  _ORDEN: { repaso: 0, recomendado: 1, disponible: 2, dominado: 3, reforzar: 4 },
  peso(actId) { return this._ORDEN[this.estadoActividad(actId)]; },
  etiqueta(actId) {
    return ({ repaso: "🔁 Repasá", recomendado: "✨ Recomendado", disponible: "",
              dominado: "🏅 Dominado", reforzar: "🌱 Reforzá antes" })[this.estadoActividad(actId)];
  },
};
if (typeof module !== "undefined") module.exports = { Adapt, SABERES_MOTOR, _JUEGO_A_SABERES };
