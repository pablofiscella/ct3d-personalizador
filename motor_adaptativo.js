/* Motor adaptativo — PILOTO 4° Matemática. Capa de SABERES sobre el Store del player.
   GENERADO desde saberes.py (mantener en sync, no editar a mano el bloque de datos).
   Gateado por D.adaptativo_on: si el token no lo tiene, el player NO lo usa y nada cambia. */

const SABERES_MOTOR = { "MAT-3-NUM": { "nombre": "Numeración hasta 1.000", "grado": 3, "eje": "numeracion", "prereqs": [], "juegos": [ "valor_posicional", "comparar_numeros", "ordenar_numeros" ] }, "MAT-3-SUMARESTA": { "nombre": "Suma y resta hasta 3 cifras (con llevada y canje)", "grado": 3, "eje": "operaciones", "prereqs": [ "MAT-3-NUM" ], "juegos": [ "sumas", "restas", "suma_columnas", "resta_columnas" ] }, "MAT-3-TABLAS": { "nombre": "Tablas de multiplicar (memorización)", "grado": 3, "eje": "operaciones", "prereqs": [], "juegos": [ "tablas_contrarreloj", "tabla_pitagorica" ] }, "MAT-3-MULT": { "nombre": "Concepto de multiplicación", "grado": 3, "eje": "operaciones", "prereqs": [ "MAT-3-SUMARESTA", "MAT-3-TABLAS" ], "juegos": [ "multiplicacion_concepto", "multiplicar" ] }, "MAT-3-DIV": { "nombre": "Concepto de división y reparto", "grado": 3, "eje": "operaciones", "prereqs": [ "MAT-3-MULT" ], "juegos": [ "reparto_con_resto" ] }, "MAT-4-NUM-GRANDES": { "nombre": "Leer y escribir números grandes (10.000 y más)", "grado": 4, "eje": "numeracion", "prereqs": [ "MAT-3-NUM" ], "juegos": [ "bingo", "agrupar" ] }, "MAT-4-VALPOS": { "nombre": "Valor posicional (unidad de mil, decena de mil…)", "grado": 4, "eje": "numeracion", "prereqs": [ "MAT-4-NUM-GRANDES" ], "juegos": [ "valor_posicional", "agrupar" ] }, "MAT-4-COMPARAR": { "nombre": "Comparar y ordenar números grandes", "grado": 4, "eje": "numeracion", "prereqs": [ "MAT-4-NUM-GRANDES" ], "juegos": [ "comparar_numeros", "ordenar_numeros" ] }, "MAT-4-RECTA": { "nombre": "Ubicar números en la recta numérica", "grado": 4, "eje": "numeracion", "prereqs": [ "MAT-4-COMPARAR" ], "juegos": [ "recta_numerica" ] }, "MAT-4-SERIES": { "nombre": "Series numéricas (conteo de a saltos)", "grado": 4, "eje": "numeracion", "prereqs": [ "MAT-4-NUM-GRANDES" ], "juegos": [ "serie" ] }, "MAT-4-PATRONES": { "nombre": "Patrones y regularidades", "grado": 4, "eje": "numeracion", "prereqs": [ "MAT-4-SERIES" ], "juegos": [ "patron" ] }, "MAT-4-SUMARESTA": { "nombre": "Suma y resta de números grandes (algoritmo)", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-3-SUMARESTA", "MAT-4-VALPOS" ], "juegos": [ "suma_columnas", "sumas", "restas", "resta_columnas" ] }, "MAT-4-CALCMENTAL": { "nombre": "Cálculo mental y estimación (suma/resta)", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-SUMARESTA" ], "juegos": [ "suma_rapida", "sumas_redondas", "mas_menos" ] }, "MAT-4-MUL1": { "nombre": "Multiplicación por una cifra (algoritmo)", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-3-MULT", "MAT-3-TABLAS" ], "juegos": [ "multiplicar", "tablas_ninja" ] }, "MAT-4-MUL2": { "nombre": "Multiplicación por dos cifras", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-MUL1", "MAT-4-SUMARESTA" ], "juegos": [ "cuenta_larga", "multiplicar" ] }, "MAT-4-DIV1": { "nombre": "División por una cifra (exacta)", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-3-DIV", "MAT-4-MUL1" ], "juegos": [ "dividir" ] }, "MAT-4-DIVRESTO": { "nombre": "División con resto", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-DIV1" ], "juegos": [ "dividir", "reparto_con_resto" ] }, "MAT-4-PROB-MULDIV": { "nombre": "Problemas de multiplicación y división", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-MUL2", "MAT-4-DIVRESTO" ], "juegos": [ "problemas_mult_div" ] }, "MAT-4-PROB-MULTI": { "nombre": "Problemas de varios pasos (4 operaciones)", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-PROB-MULDIV", "MAT-4-SUMARESTA" ], "juegos": [ "problemas_multipaso", "problemas_mult_div" ] }, "MAT-4-FRAC-CONCEPTO": { "nombre": "Concepto de fracción (parte de un entero)", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-3-DIV" ], "juegos": [ "completar_entero" ] }, "MAT-4-FRAC-CANT": { "nombre": "Fracción de una cantidad (mitad, tercio, cuarto)", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-4-FRAC-CONCEPTO", "MAT-4-DIV1" ], "juegos": [ "reparto_fracciones", "fraccion_de_cantidad" ] }, "MAT-4-FRAC-EQUIV": { "nombre": "Fracciones equivalentes", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-4-FRAC-CONCEPTO" ], "juegos": [ "fracciones_equivalentes" ] }, "MAT-4-FRAC-COMP": { "nombre": "Comparar fracciones (cuál es más grande)", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-4-FRAC-EQUIV" ], "juegos": [ "duelo_fracciones" ] }, "MAT-4-FRAC-SUMA": { "nombre": "Suma de fracciones de igual denominador", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-4-FRAC-COMP" ], "juegos": [ "suma_fracciones" ] }, "MAT-4-DEC-DECIMOS": { "nombre": "Décimos y centésimos (concepto y escritura)", "grado": 4, "eje": "decimales", "prereqs": [ "MAT-4-FRAC-CONCEPTO", "MAT-4-VALPOS" ], "juegos": [ "decimales_fraccion", "duelo_decimales" ] }, "MAT-4-DEC-COMP": { "nombre": "Comparar números decimales", "grado": 4, "eje": "decimales", "prereqs": [ "MAT-4-DEC-DECIMOS" ], "juegos": [ "duelo_decimales" ] }, "MAT-4-DINERO": { "nombre": "Dinero: componer montos y calcular vuelto", "grado": 4, "eje": "medida", "prereqs": [ "MAT-4-SUMARESTA", "MAT-4-DEC-DECIMOS" ], "juegos": [ "cajero_automatico", "pago_exacto" ] }, "MAT-4-OFERTA": { "nombre": "Comparar precios y elegir la mejor oferta", "grado": 4, "eje": "medida", "prereqs": [ "MAT-4-DINERO", "MAT-4-MUL1" ], "juegos": [ "mejor_oferta" ] }, "MAT-4-MEDIDA-EQUIV": { "nombre": "Equivalencias de medida (m/cm, kg/g, l/ml)", "grado": 4, "eje": "medida", "prereqs": [ "MAT-4-VALPOS" ], "juegos": [ "equivalencias_medida" ] }, "MAT-4-RELOJ": { "nombre": "Leer la hora y calcular duraciones", "grado": 4, "eje": "medida", "prereqs": [], "juegos": [ "reloj" ] }, "MAT-4-PROP": { "nombre": "Proporcionalidad directa simple (tablas)", "grado": 4, "eje": "proporcionalidad", "prereqs": [ "MAT-4-MUL1" ], "juegos": [ "proporcionalidad" ] }, "MAT-4-ANGULOS": { "nombre": "Clasificar ángulos (recto, agudo, obtuso)", "grado": 4, "eje": "geometria", "prereqs": [], "juegos": [ "angulos" ] }, "MAT-4-TRANSP": { "nombre": "Medir ángulos con transportador", "grado": 4, "eje": "geometria", "prereqs": [ "MAT-4-ANGULOS" ], "juegos": [ "transportador", "suma_angulos" ] }, "MAT-4-DATOS": { "nombre": "Leer e interpretar datos y gráficos", "grado": 4, "eje": "datos", "prereqs": [ "MAT-4-COMPARAR" ], "juegos": [ "estadistica_datos" ] }, "MAT-4-PROB": { "nombre": "Probabilidad simple (seguro, posible, imposible)", "grado": 4, "eje": "datos", "prereqs": [], "juegos": [ "probabilidad_sucesos", "arbol_probabilidad" ] } };

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
