"""Las lecciones en video del botón "¿Cómo es?".

El diseño que se verifica acá, que es lo que Pablo preguntó (¿cuándo se muestra el
video, si el botón ya abre texto?):

  - El popup abre con TEXTO y el video queda a un toque. La mayoría de las veces el
    chico ya vio la regla y sólo quiere refrescarla —eso se lee en cinco segundos—,
    así que abrir directo en video castigaría al caso más frecuente.
  - Cuando el que abre es el MOTOR (actividad "reforzar", o segundo error), va derecho
    al video: ahí ya sabe que el problema no es un olvido.
  - Se ofrece UNA vez por actividad y por sesión. Si el chico dijo que no, se respeta.
"""
import os
import re

import pytest

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER = open(os.path.join(BASEDIR, "actividades_player.js"), encoding="utf-8").read()


def _videos_declarados():
    """Los .mp4 que el player referencia en COMO_ES_VIDEO."""
    i = PLAYER.index("const COMO_ES_VIDEO = {")
    j = PLAYER.index("function videoDe(")
    return set(re.findall(r'"(lec_[a-z0-9_]+\.mp4)"', PLAYER[i:j]))


def test_todo_video_declarado_existe_de_verdad():
    """Un botón que abre un 404 es peor que no tener el botón."""
    faltan = sorted(v for v in _videos_declarados()
                    if not os.path.isfile(os.path.join(BASEDIR, "lecciones_video", v)))
    assert not faltan, "videos declarados que no están en lecciones_video/: %s" % faltan


def test_ninguna_leccion_se_va_de_largo():
    """El motivo de haber partido la lección de 85 s: un chico no banca eso en medio
    de una actividad.

    El tope es 45 s y no 35 porque las lecciones de PROCEDIMIENTO (multiplicar,
    dividir) no se pueden acortar sin sacar un paso, y el paso que sobraría en
    división es la comprobación —justo donde más se equivocan—. Los cortes de una
    sub-regla, en cambio, quedan holgados debajo de 30 s. El tope está para cazar una
    lección que se fue de mano, no para forzar recortes pedagógicos."""
    import subprocess
    largas = []
    for v in sorted(_videos_declarados()):
        p = os.path.join(BASEDIR, "lecciones_video", v)
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                  "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip())
        if d > 45:
            largas.append("%s (%.1fs)" % (v, d))
    assert not largas, "lecciones demasiado largas para verlas jugando: %s" % largas


def test_el_motor_sirve_los_mp4_y_solo_los_de_lecciones():
    """La whitelist de assets es lo que impide que el token sirva cualquier archivo."""
    import actividades_web as aw
    assert aw._ASSET_RE.fullmatch("lec_acentuacion_agudas.mp4")
    for malo in ("../../etc/passwd", "lec_../x.mp4", "cualquiera.mp4",
                 "lec_MAYUS.mp4", "lec_x.mp4.exe"):
        assert not aw._ASSET_RE.fullmatch(malo), "la whitelist acepta %r" % malo


def test_los_videos_salen_del_repo_no_del_token():
    """Una sola copia para todos: mejorar una lección tiene que llegar también a los
    links ya vendidos, igual que el player y el audio de consignas."""
    import actividades_web as aw
    src = open(os.path.join(BASEDIR, "actividades_web.py"), encoding="utf-8").read()
    i = src.index("def archivo(")
    cuerpo = src[i:i + 1600]
    assert "LECCION_DIR" in cuerpo, "los mp4 se estarían buscando en la carpeta del token"
    assert aw.LECCION_DIR.endswith("lecciones_video")


# ── cuándo se muestra ───────────────────────────────────────────────────────────
# Actividades con mini-lección de texto cuyo VIDEO todavía se está produciendo.
#
# Pablo (26-jul-2026): "me gusta que los que necesiten tenga un video de explicación,
# siempre es mejor cuando te lo explican con una animación que tener que leerlo uno" —
# y después "el texto está bien pero que pueda elegir ver también el video". O sea: la
# regla no cambió, el texto se queda Y el video se suma como opción.
#
# Al completar la currícula de 4° y 5° se escribieron 77 mini-lecciones nuevas de golpe.
# Cada video es guion + escenas + narración + render, así que se producen de a tandas.
# Esta lista es la deuda declarada: lo que está acá tiene texto y todavía no video.
#
# El test de abajo NO la usa para mirar para otro lado: falla igual si aparece una
# actividad con texto y sin video que NO esté declarada, y falla también si queda una
# entrada acá que ya tiene su video (para que la lista se vacíe sola y no se pudra).
VIDEO_PENDIENTE = {
    # 7° grado completo (26-jul-2026). El guardián pasó a cubrir la edad 12, así que
    # acá entran las 70 mini-lecciones nuevas de 7° y las que el cuaderno de esa edad
    # ya tenía sin video (potencias, ecuaciones, proporcionalidad, homófonos…), que
    # nadie miraba porque el test llegaba sólo hasta la edad 11.
    "decimales_periodo_7",
    "democracia_argentina",
    "democracia_dictadura_7",
    "densidad_7",
    "derechos_94_7",
    "derechos_trabajo",
    "divisibilidad_7",
    "eclipses_universo_7",
    "ecuaciones_simples",
    "eventos_paralelismo_7",
    "expresion_objetivo_7",
    "flujo_energia_7",
    "fuente_licencias_7",
    "fuentes_sustentables_7",
    "gobierno_ciudad_7",
    "hecho_opinion_argumento_7",
    "historieta_7",
    "homofonos",
    "industria_40_7",
    "ingles_lectura_7",
    "ingles_verbos_7",
    "ingles_vocabulario_7",
    "inmune_7",
    "leer_deducir_7",
    "linea_siglo_xx_7",
    "matriz_energetica_7",
    "mcm_dcm_7",
    "media_mediana_moda_7",
    "metafora_sinecdoque_7",
    "migraciones_7",
    "modos_verbales_7",
    "movimientos_tierra_7",
    "multiplicar_fracciones_7",
    "narrador_7",
    "numeracion_7",
    "ortografia_7",
    "persuasion_7",
    "potencias",
    "potencias_7",
    "presupuesto_inflacion_7",
    "probabilidad_arbol_7",
    "problemas_pasos_7",
    "proporcionalidad",
    "proporcionalidad_grafico_7",
    "proporcionalidad_inversa_7",
    "puerto_madero_7",
    "quimica_fisica_7",
    "razon_porcentaje_7",
    "recursos_argumentador_7",
    "recursos_poema",
    "redes_troficas_7",
    "reproductor_7",
    "sistema_nervioso_7",
    "subgeneros_7",
    "sucesion_ecologica_7",
    "sujeto_7",
    "sustantivos_7",
    "traductor_algebraico",
    "traductor_algebraico_7",
    "transformar_energia_7",
    "vacunas_7",

    # 6° grado completo (26-jul-2026). El test pasó a cubrir la edad 11, así que
    # estas entran a la deuda declarada: incluye las 67 mini-lecciones nuevas de 6° y
    # las que el cuaderno de esa edad ya tenía sin video, que hasta ahora nadie miraba
    # porque el guardián sólo llegaba hasta la edad 10.
    "area_fraccionaria_6",
    "area_perimetro_6",
    "bloques_codigo_6",
    "chat_seguro_6",
    "ciclo_menstrual_6",
    "ciencia_ficcion_6",
    "cigoto_feto_6",
    "cohesion_6",
    "comprension_lectora_6",
    "conectores_6",
    "conjugacion_6",
    "corredor_coma_6",
    "cuadrilateros",
    "cuadrilateros_6",
    "demografia_6",
    "densidad_recta_6",
    "desarrollos_6",
    "descuentos_6",
    "directo_indirecto_6",
    "divisibilidad_criterios_6",
    "economia_circular_6",
    "ecorregiones_6",
    "efecto_invernadero_6",
    "escalas_ambientales_6",
    "estado_agroexportacion_6",
    "etapas_diseno_6",
    "fraccion_cantidad_6",
    "fraccion_de_cantidad",
    "fraccion_inversa_6",
    "fracciones_equivalentes_6",
    "fuente_confiable_6",
    "gran_guerra_crisis_6",
    "hechos_opiniones",
    "heliocentrismo_6",
    "idea_principal_6",
    "inmigracion_censos_6",
    "instrumentos_medida_6",
    "its_violencia_6",
    "jerarquia_6",
    "jerarquia_operaciones",
    "linea_tiempo_1862_1930_6",
    "material_termico_6",
    "mercosur_energia_6",
    "moda_encuesta_6",
    "multiplicar_coma_6",
    "multiplicar_fracciones",
    "noticia_partes_6",
    "numeros_gigantes_6",
    "numeros_primos",
    "od_oi_6",
    "particulas_calor_6",
    "permutaciones_6",
    "poligonos_lados",
    "porcentaje_cantidad_6",
    "porcentajes",
    "presupuesto_6",
    "probabilidad_6",
    "probabilidad_sucesos",
    "problemas_varios_pasos_6",
    "pronombres_6",
    "proporcionalidad_6",
    "pubertad_6",
    "puntuacion_6",
    "reconstruir_division_6",
    "recursos_poeticos_6",
    "red_ecosistema_6",
    "relato_policial_6",
    "revolucion_industrial_6",
    "roles_niveles_6",
    "secuencial_condicional_6",
    "sensores_6",
    "sintagma_6",
    "suma_angulos",
    "suma_fracciones_6",
    "tiempo_clima_6",
    "tildes_6",
    "tres_poderes_6",
    "voto_6",

    # Cierre de las 9 deudas del manifiesto de cobertura (26-jul-2026). El video
    # quedó pendiente por falta de crédito de ElevenLabs, no por decisión de diseño.
    "club_lectura_5",
    "cuerpo_etapas_1",
    "eclipses_5",
    "geometria_5",
    "planta_partes_1",
    "recta_millon_5",
    "recursos_5",
    "unitario_federal_5",

    # Las 20 que quedaban sin mini-lección, escritas el 26-jul. Mismo motivo: el
    # texto ya está en el player, el video espera crédito de ElevenLabs.
    "adivina_figura",
    "america_1492_4",
    "animales_cobertura",
    "antes_y_hoy",
    "artesanal_industrial",
    "calculo_redondo",
    "campo_a_casa",
    "causas_revolucion_5",
    "circuito_alimento",
    "debate_mayo_5",
    "derechos_escenarios",
    "forma_redondo",
    "linea_siglo_xx",
    "linterna_magica",
    "mas_o_menos_1",
    "objeto_material",
    "ordenar_pasos",
    "que_cuenta_resuelve",
    "sociedad_colonial_4",
    "solido_liquido",

    # 1°, 2° y 3° — mini-lecciones nuevas, video pendiente (26-jul-2026)
    "acentuacion_2",
    "agua_2",
    "animales_2",
    "antes_ahora_1",
    "armar_calculo_1",
    "articulos_1",
    "bucle_2",
    "buscar_dato_2",
    "calendario_1",
    "con_que_se_mueve_3",
    "condicional_2",
    "conductor_aislante",
    "conectores_2",
    "convivencia_2",
    "cuerpos_1",
    "cuerpos_geometricos",
    "cuidarnos_1",
    "despegar_palabras_1",
    "dictado_2",
    "dobles_2",
    "donde_esta_1",
    "emociones_1",
    "entrada_salida_2",
    "estados_materia",
    "estados_tres",
    "estructura_cuento_3",
    "familia_palabras",
    "figuras_1",
    "iconos_1",
    "kiosco_1",
    "leer_encontrar_1",
    "leo_respondo_1",
    "luz_propia",
    "mayuscula_punto_1",
    "mb_nv_h_2",
    "medir_clips_1",
    "medir_regla_2",
    "multiplicacion_concepto",
    "mundo_digital_3",
    "oficios_1",
    "orden_alfabetico",
    "ordenar_cuento_1",
    "ordenar_relato_2",
    "parejas_cien_2",
    "parejas_diez_1",
    "parejas_letras_1",
    "parejas_mil_3",
    "pares_minimos_2",
    "partes_oracion",
    "pasos_orden_1",
    "plantas_2",
    "plato_1",
    "plato_2",
    "plaza_mayo_3",
    "posiciones_2",
    "reloj",
    "reparto_2",
    "reparto_con_resto",
    "residuos_1",
    "residuos_2",
    "resta_columnas",
    "salud_2",
    "separar_palabras_2",
    "signos_2",
    "silaba_tonica",
    "silabas_1",
    "silabas_2",
    "sinonimos_antonimos",
    "suena_igual",
    "sustantivos",
    "tiempo_verbo",
    "tiempos_verbales",
    "tipos_de_texto",
    "valor_posicional",
    "vial_1",
    "vial_2",
    "vocabulario_2",
}


def _texto_y_video():
    i = PLAYER.index("const COMO_ES = {")
    f = PLAYER.index("\nconst FRASES_BIEN")
    texto = set(re.findall(r"^  (\w+): \{ t:", PLAYER[i:f], re.M))
    j = PLAYER.index("const COMO_ES_VIDEO = {")
    k = PLAYER.index("function videoDe(")
    video = set(re.findall(r"^  (\w+): \{", PLAYER[j:k], re.M))
    return texto, video


@pytest.mark.parametrize("edad", ["9", "10", "11", "12"])
def test_toda_explicacion_tiene_video(edad):
    """Pablo (25-jul): "quiero en las explicaciones siempre videos que expliquen el
    contenido de forma visual".

    O sea: si una actividad enseña una regla y tiene mini-lección de texto, tiene que
    tener también su video. Yo había argumentado que algunas reglas simples no lo
    necesitaban; su criterio fue que sí, y este test lo fija — si mañana se agrega una
    actividad con texto y sin video, salta acá y no en el aula.

    Lo declarado en VIDEO_PENDIENTE se saltea: es deuda visible, no un descuido."""
    import sys
    sys.path.insert(0, BASEDIR)
    import actividades_web as aw
    menu = {m["id"] for m in aw._menu(aw._banda(edad), edad) + aw._menu_curricular(edad)}
    texto, video = _texto_y_video()
    faltan = sorted((menu & texto) - video - VIDEO_PENDIENTE)
    assert not faltan, (
        "actividades con texto y SIN video que tampoco están declaradas en "
        "VIDEO_PENDIENTE: %s" % faltan)


def test_la_deuda_de_video_no_tiene_entradas_muertas():
    """Cada id de VIDEO_PENDIENTE tiene que seguir siendo deuda de verdad.

    Si ya se le produjo el video, se saca de la lista; si se le borró el texto, no era
    deuda. Sin esto la lista se llena de entradas viejas y deja de significar nada —
    que es como una compuerta temporal se vuelve permanente."""
    texto, video = _texto_y_video()
    ya_tienen = sorted(VIDEO_PENDIENTE & video)
    assert not ya_tienen, ("estos ya tienen video: sacalos de VIDEO_PENDIENTE: %s"
                           % ya_tienen)
    sin_texto = sorted(VIDEO_PENDIENTE - texto)
    assert not sin_texto, ("estos no tienen mini-lección, así que no son deuda de "
                           "video: %s" % sin_texto)


def test_el_popup_abre_con_texto_y_el_video_queda_a_un_toque():
    i = PLAYER.index("function mostrarComoEs(")
    cuerpo = PLAYER[i:i + 2200]
    # el texto de la regla se arma siempre
    assert "comoes-h" in cuerpo and "c.l.map" in cuerpo
    # y el video es opcional, detrás de videoDe()
    assert "videoDe(id)" in cuerpo and "comoes-videos" in cuerpo
    assert "if (vid)" in cuerpo, "el bloque de video tiene que ser condicional"


def test_una_regla_sin_video_no_muestra_nada_roto():
    """63 mini-lecciones tienen texto y sólo una tiene video: las otras 62 no pueden
    mostrar un hueco ni un botón muerto."""
    i = PLAYER.index("function videoDe(")
    assert "COMO_ES_VIDEO[id] || null" in PLAYER[i:i + 200]


def test_el_motor_ofrece_en_los_dos_momentos():
    assert 'ofrecerLeccion(id, "reforzar")' in PLAYER, "falta el disparo por prerrequisitos"
    assert 'ofrecerLeccion(self.actual, "errores")' in PLAYER, "falta el disparo por errores"


def test_el_disparo_por_errores_es_en_el_segundo():
    """Al primero sería interrumpir a quien está pensando; al quinto ya abandonó."""
    i = PLAYER.index('ofrecerLeccion(self.actual, "errores")')
    contexto = PLAYER[max(0, i - 400):i]
    assert "(self.primerTotal - self.primerOk) === 2" in contexto


def test_el_motor_no_insiste():
    """Si el chico dijo que no, no se le vuelve a preguntar en la misma sesión."""
    i = PLAYER.index("function ofrecerLeccion(")
    cuerpo = PLAYER[i:i + 700]
    assert "_ofrecido.has(id)" in cuerpo and "_ofrecido.add(id)" in cuerpo


def test_el_ofrecimiento_se_puede_rechazar():
    i = PLAYER.index("function ofrecerLeccion(")
    cuerpo = PLAYER[i:i + 1800]
    assert "No, sigo probando" in cuerpo, "tiene que poder decir que no"


def test_no_se_ofrece_durante_la_nivelacion():
    """El sondeo MIDE; interrumpirlo con una lección arruinaría la medición y además
    le enseñaría al chico lo que justo estamos tratando de averiguar si sabe."""
    for ancla in ('ofrecerLeccion(id, "reforzar")', 'ofrecerLeccion(self.actual, "errores")'):
        i = PLAYER.index(ancla)
        assert "Sondeo.activo" in PLAYER[max(0, i - 500):i], \
            "el disparo %s no está gateado por el sondeo" % ancla


def test_abrir_el_video_corta_la_voz():
    """Si no, la narración de la consigna se pisa con la del video."""
    i = PLAYER.index("function mostrarVideoLeccion(")
    assert "pararVoz()" in PLAYER[i:i + 400]
