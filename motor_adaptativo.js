/* Motor adaptativo — PILOTO 4° Matemática. Capa de SABERES + CATEGORÍAS sobre el player.
   GENERADO desde saberes.py + actividades_categorias.py (gen_motor_adaptativo.py). No editar
   a mano los bloques de datos. Gateado por D.adaptativo_on: sin flag el player no lo usa. */

const SABERES_MOTOR = { "MAT-3-NUM": { "nombre": "Numeración hasta 1.000", "grado": 3, "eje": "numeracion", "prereqs": [], "juegos": [] }, "MAT-3-SUMARESTA": { "nombre": "Suma y resta con llevada/canje (3° cifras)", "grado": 3, "eje": "operaciones", "prereqs": [ "MAT-3-NUM" ], "juegos": [] }, "MAT-3-TABLAS": { "nombre": "Tablas de multiplicar (memorización)", "grado": 3, "eje": "operaciones", "prereqs": [], "juegos": [] }, "MAT-3-MULT": { "nombre": "Concepto de multiplicación", "grado": 3, "eje": "operaciones", "prereqs": [ "MAT-3-SUMARESTA", "MAT-3-TABLAS" ], "juegos": [] }, "MAT-3-DIV": { "nombre": "Concepto de división y reparto", "grado": 3, "eje": "operaciones", "prereqs": [ "MAT-3-MULT" ], "juegos": [] }, "MAT-4-SERIES": { "nombre": "Series numéricas (¿qué número falta?)", "grado": 4, "eje": "numeracion", "prereqs": [ "MAT-3-NUM" ], "juegos": [ "serie" ] }, "MAT-4-RECTA": { "nombre": "Ubicar números en la recta numérica", "grado": 4, "eje": "numeracion", "prereqs": [ "MAT-3-NUM" ], "juegos": [ "recta_numerica" ] }, "MAT-4-SUMA": { "nombre": "Suma en columna (números grandes)", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-3-SUMARESTA" ], "juegos": [ "suma_columnas" ] }, "MAT-4-TABLAS": { "nombre": "Agilidad con las tablas", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-3-TABLAS" ], "juegos": [ "tablas_ninja" ] }, "MAT-4-MUL": { "nombre": "Multiplicación (algoritmo)", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-TABLAS", "MAT-3-MULT" ], "juegos": [ "multiplicar" ] }, "MAT-4-DIV": { "nombre": "División por una cifra", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-MUL", "MAT-3-DIV" ], "juegos": [ "dividir" ] }, "MAT-4-DIV-LARGA": { "nombre": "División larga / cuenta larga", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-DIV" ], "juegos": [ "cuenta_larga" ] }, "MAT-4-PROB": { "nombre": "Problemas de multiplicación y división", "grado": 4, "eje": "operaciones", "prereqs": [ "MAT-4-MUL", "MAT-4-DIV" ], "juegos": [ "problemas_mult_div" ] }, "MAT-4-FRAC-ENTERO": { "nombre": "Concepto de fracción (parte de un entero)", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-3-DIV" ], "juegos": [ "completar_entero" ] }, "MAT-4-FRAC-CANT": { "nombre": "Fracción de una cantidad (reparto)", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-4-FRAC-ENTERO", "MAT-4-DIV" ], "juegos": [ "reparto_fracciones" ] }, "MAT-4-FRAC-EQUIV": { "nombre": "Fracciones equivalentes", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-4-FRAC-ENTERO" ], "juegos": [ "fracciones_equivalentes" ] }, "MAT-4-FRAC-COMP": { "nombre": "Comparar fracciones (cuál es más grande)", "grado": 4, "eje": "fracciones", "prereqs": [ "MAT-4-FRAC-EQUIV" ], "juegos": [ "duelo_fracciones" ] }, "MAT-4-DECIMALES": { "nombre": "Comparar decimales (décimos/centésimos)", "grado": 4, "eje": "decimales", "prereqs": [ "MAT-4-FRAC-ENTERO" ], "juegos": [ "duelo_decimales" ] }, "MAT-4-OFERTA": { "nombre": "Comparar precios / mejor oferta", "grado": 4, "eje": "medida", "prereqs": [ "MAT-4-MUL" ], "juegos": [ "mejor_oferta" ] }, "MAT-4-ANGULOS": { "nombre": "Clasificar ángulos (recto/agudo/obtuso)", "grado": 4, "eje": "geometria", "prereqs": [], "juegos": [ "angulos" ] }, "LEN-4-VOCAB": { "nombre": "Vocabulario (palabras escondidas)", "grado": 4, "eje": "vocabulario", "prereqs": [], "juegos": [ "sopa" ] }, "LEN-4-SUSTANTIVOS": { "nombre": "Sustantivos concretos y abstractos", "grado": 4, "eje": "gramatica", "prereqs": [], "juegos": [ "abstractos_concretos" ] }, "LEN-4-ACENTUACION": { "nombre": "Acentuación", "grado": 4, "eje": "ortografia", "prereqs": [], "juegos": [ "acentuacion" ] }, "LEN-4-PLURALES": { "nombre": "Plurales (z → ces)", "grado": 4, "eje": "ortografia", "prereqs": [], "juegos": [ "plurales_z" ] }, "LEN-4-ORACION": { "nombre": "Sujeto y predicado", "grado": 4, "eje": "gramatica", "prereqs": [ "LEN-4-SUSTANTIVOS" ], "juegos": [ "sujeto_predicado" ] }, "LEN-4-MORFOLOGIA": { "nombre": "Prefijos y sufijos", "grado": 4, "eje": "vocabulario", "prereqs": [ "LEN-4-VOCAB" ], "juegos": [ "prefijos_sufijos" ] }, "LEN-4-CONECTORES": { "nombre": "Conectores", "grado": 4, "eje": "gramatica", "prereqs": [ "LEN-4-ORACION" ], "juegos": [ "conectores" ] }, "LEN-4-DIALOGO": { "nombre": "Puntuación del diálogo (raya)", "grado": 4, "eje": "ortografia", "prereqs": [ "LEN-4-ORACION" ], "juegos": [ "dialogo_raya" ] }, "LEN-4-COMPRENSION": { "nombre": "Comprensión lectora", "grado": 4, "eje": "comprension", "prereqs": [ "LEN-4-VOCAB" ], "juegos": [ "comprension_lectora" ] }, "LEN-4-NARRATIVA": { "nombre": "Ordenar el relato (secuencia narrativa)", "grado": 4, "eje": "comprension", "prereqs": [ "LEN-4-COMPRENSION" ], "juegos": [ "historia_orden" ] }, "NAT-4-FOTOSINTESIS": { "nombre": "Plantas y fotosíntesis", "grado": 4, "eje": "seres_vivos", "prereqs": [], "juegos": [ "fotosintesis" ] }, "NAT-4-ELECTRICIDAD": { "nombre": "Electricidad y circuitos", "grado": 4, "eje": "materiales_energia", "prereqs": [], "juegos": [ "laboratorio_electrico" ] }, "SOC-4-CRONOLOGIA": { "nombre": "Ordenar cronología (línea de tiempo)", "grado": 4, "eje": "tiempo", "prereqs": [], "juegos": [ "linea_tiempo" ] }, "SOC-4-GEOGRAFIA": { "nombre": "Provincias y regiones", "grado": 4, "eje": "espacio", "prereqs": [], "juegos": [ "provincias_region" ] }, "SOC-4-HISTORIA": { "nombre": "Pueblos originarios y la colonia", "grado": 4, "eje": "tiempo", "prereqs": [ "SOC-4-CRONOLOGIA" ], "juegos": [ "historia_originarios" ] } };
const CATEGORIA_JUEGO = {"abecedario": "lengua", "abstractos_concretos": "lengua", "acentuacion": "lengua", "analisis_sintactico": "lengua", "armar_palabra": "lengua", "cazador_errores": "lengua", "comprension_lectora": "lengua", "conectores": "lengua", "dialogo_raya": "lengua", "familia_palabras": "lengua", "hechos_opiniones": "lengua", "homofonos": "lengua", "ingles_basico": "lengua", "historia_orden": "lengua", "letra_inicial": "lengua", "orden_alfabetico": "lengua", "ortografia_2do": "lengua", "ortografia_3ro": "lengua", "partes_oracion": "lengua", "plurales_z": "lengua", "prefijos_sufijos": "lengua", "silaba_tonica": "lengua", "silabas": "lengua", "sinonimos_antonimos": "lengua", "sopa": "lengua", "sujeto_predicado": "lengua", "sustantivos": "lengua", "tiempos_verbales": "lengua", "verbos_pasado": "lengua", "angulos": "matematica", "anterior_siguiente": "matematica", "arbol_probabilidad": "matematica", "area_perimetro": "matematica", "cajero_automatico": "matematica", "comparar_numeros": "matematica", "completar_entero": "matematica", "contar": "matematica", "contar_saltando": "matematica", "cuadrilateros": "matematica", "cuenta_larga": "matematica", "cuerpos_geometricos": "matematica", "decimales_fraccion": "matematica", "dividir": "matematica", "duelo_decimales": "matematica", "duelo_fracciones": "matematica", "ecuaciones_simples": "matematica", "equivalencias_medida": "matematica", "estadistica_datos": "matematica", "fraccion_de_cantidad": "matematica", "fracciones_avanzado": "matematica", "fracciones_equivalentes": "matematica", "grilla100": "matematica", "jerarquia_operaciones": "matematica", "mas_menos": "matematica", "mejor_oferta": "matematica", "multiplicacion_concepto": "matematica", "multiplicar": "matematica", "multiplicar_fracciones": "matematica", "numeros_primos": "matematica", "ordenar_numeros": "matematica", "pago_exacto": "matematica", "poligonos_lados": "matematica", "porcentajes": "matematica", "posicion": "matematica", "potencias": "matematica", "probabilidad_sucesos": "matematica", "problemas_3ro": "matematica", "problemas_mult_div": "matematica", "problemas_multipaso": "matematica", "proporcionalidad": "matematica", "recta_numerica": "matematica", "reloj": "matematica", "reparto_con_resto": "matematica", "reparto_fracciones": "matematica", "resta_columnas": "matematica", "restas": "matematica", "serie": "matematica", "suma_angulos": "matematica", "suma_columnas": "matematica", "suma_fracciones": "matematica", "suma_rapida": "matematica", "sumas": "matematica", "sumas_redondas": "matematica", "tabla_pitagorica": "matematica", "tablas_contrarreloj": "matematica", "tablas_ninja": "matematica", "traductor_algebraico": "matematica", "transportador": "matematica", "valor_posicional": "matematica", "animal_comida": "naturales", "camino_digestivo": "naturales", "celula_partes": "naturales", "cerebro_defensas": "naturales", "cielo": "naturales", "conductor_aislante": "naturales", "detectives_cielo": "naturales", "energia_renovable": "naturales", "estaciones": "naturales", "estados_materia": "naturales", "fotosintesis": "naturales", "laboratorio_electrico": "naturales", "luz_materiales": "naturales", "materiales": "naturales", "planetas_tipo": "naturales", "planta_fruto": "naturales", "planta_potabilizadora": "naturales", "pubertad": "naturales", "red_trofica": "naturales", "sentidos": "naturales", "separador_mezclas": "naturales", "sistema_nervioso": "naturales", "sistema_reproductor": "naturales", "trivia_espacial": "naturales", "actividad_economica": "sociales", "argentina_sigloXX": "sociales", "buenos_aires": "sociales", "campo_ciudad": "sociales", "derechos_constitucion": "sociales", "historia_originarios": "sociales", "independencia_arg": "sociales", "linea_democracia": "sociales", "linea_tiempo": "sociales", "organizacion_nacional": "sociales", "provincias_region": "sociales", "sufragio_argentina": "sociales", "trivia_colonial": "sociales", "viaje_inmigrante": "sociales", "bingo": "logica", "agrupar": "logica", "patron": "logica", "colorear": "logica", "diferente": "logica", "escape_room_egreso": "logica", "laberinto": "logica", "memotest": "logica", "programar_camino": "logica", "puntos": "logica", "quefalta": "logica", "simon": "logica", "sombra": "logica", "sudoku": "logica", "tamano": "logica"};
const CATEGORIA_ORDEN = ["lengua", "matematica", "naturales", "sociales", "logica"];
const CATEGORIA_LABEL = {"lengua": "Lengua", "matematica": "Matemática", "naturales": "Cs. Naturales", "sociales": "Cs. Sociales", "logica": "Extras"};

/* ── Adapt: capa de saberes + categorías sobre el Store del player (no bloquea) ── */
const _JUEGO_A_SABERES = (() => {
  const m = {};
  for (const sid in SABERES_MOTOR)
    for (const j of SABERES_MOTOR[sid].juegos) (m[j] = m[j] || []).push(sid);
  return m;
})();

const Adapt = {
  _store() { return (typeof Store !== "undefined") ? Store : null; },
  saberDominado(sid) {
    const s = SABERES_MOTOR[sid];
    if (!s) return false;
    if (s.grado < 4) return true;              // grado anterior = asumido dominado
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
    if (!saberes || !saberes.length) return "disponible";  // sin saber (Extras/otra materia)
    const dom = this._dominados();
    if (saberes.every((s) => dom.has(s))) return "dominado";
    if (saberes.some((s) => !dom.has(s) && this._prereqsOk(s, dom))) return "recomendado";
    return "reforzar";
  },
  _ORDEN: { repaso: 0, recomendado: 1, disponible: 2, dominado: 3, reforzar: 4 },
  peso(actId) { return this._ORDEN[this.estadoActividad(actId)]; },
  etiqueta(actId) {
    return ({ repaso: "🔁 Repasá", recomendado: "✨ Recomendado", disponible: "",
              dominado: "🏅 Dominado", reforzar: "🌱 Reforzá antes" })[this.estadoActividad(actId)];
  },
  // ── categorías (para separar el menú) ──
  categoria(actId) { return CATEGORIA_JUEGO[actId] || "logica"; },   // sin match → Extras
  ordenCategorias() { return CATEGORIA_ORDEN.slice(); },
  // próxima actividad recomendada del menú (repaso/recomendado), distinta de la actual
  proximaRecomendada(menuIds, excepto) {
    const cand = menuIds.filter((id) => id !== excepto && _JUEGO_A_SABERES[id] && this.peso(id) <= 1)
                        .sort((a, b) => this.peso(a) - this.peso(b));
    return cand.length ? cand[0] : null;
  },
  saberCategoria(sid) { const j = (SABERES_MOTOR[sid]||{}).juegos || []; return j.length ? this.categoria(j[0]) : null; },
  // resumen por categoría para el panel de padres: dominado/en proceso/pendiente
  resumenPorCategoria() {
    const res = {}; for (const c of CATEGORIA_ORDEN) res[c] = { dom: 0, proc: 0, pend: 0, total: 0 };
    const dom = this._dominados(); const st = this._store();
    for (const sid in SABERES_MOTOR) {
      const s = SABERES_MOTOR[sid]; if (s.grado < 4) continue;
      const cat = this.saberCategoria(sid); if (!cat || !res[cat]) continue;
      res[cat].total++;
      if (dom.has(sid)) res[cat].dom++;
      else if (st && s.juegos.some((j) => st.stars(j) > 0)) res[cat].proc++;
      else res[cat].pend++;
    }
    return res;
  },
  labelCategoria(cat) { return CATEGORIA_LABEL[cat] || cat; },
};
if (typeof module !== "undefined")
  module.exports = { Adapt, SABERES_MOTOR, CATEGORIA_JUEGO, CATEGORIA_ORDEN, CATEGORIA_LABEL };
