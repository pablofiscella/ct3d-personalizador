"""Ninguna pieza puede salir con el nombre de OTRO chico.

11-ago-2026. Pablo: *"tenemos que mejorar imprimibles… para que valga la pena pagar por un
producto"*. Generando el kit de safari con `nombre="Tomás"` apareció esto: el afiche decía
"Tomás" y **la tarjeta de agradecimiento decía "al cumple de Valentin"**.

EL BUG, Y POR QUÉ ES EL PEOR DE TODOS LOS POSIBLES
──────────────────────────────────────────────────
`temas/<tema>/layouts/tarjetas_agradecimiento.json` guarda la posición y el texto de cada
línea, y lo escribe el editor visual del panel. Alguien acomodó los textos escribiendo un
nombre de prueba para ver cómo quedaba, guardó, y ese nombre quedó como texto FIJO de la
pieza. No en un tema: **en nueve**.

    artistas → Carlitos · aviadores → Tomy · circo → Tomás · construccion → Sabri
    futbol → Valentino · monstruos → Alejo · princesas → Federica · safari → Valentin
    un-espacio-de-locura → Valentina

O sea que cualquiera que compraba el kit recibía, entre 14 piezas impecables, **una tarjeta
para agradecerle a los invitados del cumpleaños de otro nene**. Es peor que una pieza fea: la
pieza fea se nota antes de imprimir; ésta se nota cuando ya la repartiste.

La forma correcta es `{nombre}`, el marcador que `generador._field_text` reemplaza por el dato
del cliente — el mismo que ya usaban el afiche, el banderín y la cajita.

QUÉ PROTEGE ESTE TEST
─────────────────────
Que ningún layout vuelva a tener un nombre propio escrito a mano. No alcanza con arreglar los
nueve: el editor sigue permitiendo escribir cualquier cosa y guardar, así que sin guardián el
próximo se cuela igual.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import generador  # noqa: E402
import productos  # noqa: E402
import piezas as pz  # noqa: E402

# Frases que SÍ pueden estar fijas: son parte del diseño de la pieza, no un dato del cliente.
FRASES_DEL_DISENO = (
    "gracias", "cumple", "invitamos", "bienvenidos", "confirmá", "confirma", "alerta",
    "aventura", "espectáculo", "obra", "fiesta", "llamado", "lugar", "hora", "fecha",
    "espera", "necesitamos", "preparate", "esperamos", "faltes", "salvar", "construir",
    "despegar", "monstruos", "menú", "menu",
)


def _layouts():
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return sorted(glob.glob(os.path.join(raiz, "temas", "*", "layouts", "*.json")))


def test_ningun_layout_tiene_el_nombre_de_otro_chico():
    """EL test. Nueve temas salían con un nombre de prueba escrito a mano."""
    colados = []
    for f in _layouts():
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        for campo, cfg in d.items():
            if not isinstance(cfg, dict):
                continue
            t = cfg.get("tpl")
            if not (isinstance(t, str) and t.strip()):
                continue
            if "{" in t:                       # tiene marcador: lo completa el motor
                continue
            if any(g in t.lower() for g in FRASES_DEL_DISENO):
                continue
            colados.append("%s :: %s = %r" % (os.path.basename(os.path.dirname(
                os.path.dirname(f))), campo, t))
    assert not colados, (
        "hay texto fijo que parece un dato del cliente. Si es el nombre, va '{nombre}':\n  "
        + "\n  ".join(colados))


def test_la_tarjeta_lleva_el_nombre_de_QUIEN_compra():
    """De punta a punta y sobre el render de verdad, no sobre el JSON: se dibuja la pieza y se
    comprueba que el motor resolvió el marcador."""
    import temas
    spec = temas.cargar_tema("safari")["specs"]["tarjetas_agradecimiento"]
    campos = {f.get("id"): f for f in spec.get("text", [])}
    assert "{nombre}" in campos["texto3"]["tpl"], "la última línea tiene que ser el nombre"
    assert generador._field_text(campos["texto3"], {"nombre": "Tomás"}) == "Tomás"


def test_todos_los_temas_agradecen_igual():
    """La misma pieza salía distinta según el tema: nueve decían "al cumple de <nombre>" y
    tres sólo "¡Gracias por venir!", con media tarjeta en blanco. Eso no lo decidió nadie."""
    import temas
    for t in temas.list_temas():
        tid = t if isinstance(t, str) else (t.get("id") or t.get("slug"))
        spec = temas.cargar_tema(tid)["specs"].get("tarjetas_agradecimiento")
        if not spec:
            continue
        campos = {f.get("id"): (f.get("tpl") or "") for f in spec.get("text", [])}
        assert "{nombre}" in campos.get("texto3", ""), "%s: la tarjeta no lleva el nombre" % tid
        assert campos.get("texto2", "").strip(), "%s: la línea del medio quedó vacía" % tid


# ── el otro bug que apareció en la misma corrida ─────────────────────────────

def test_un_dato_que_falta_NO_se_lleva_puesta_la_pieza():
    """`"{fecha}".format(**data)` lanzaba KeyError y **tiraba la invitación entera**.

    Se vio generando el kit con los mismos datos de muestra que usa el panel —nombre, edad y
    año, sin fecha—: 13 piezas salieron y la invitación murió. O sea que la vista previa de la
    invitación en el dash venía rota por esto. Un campo sin dato tiene que salir vacío: el
    resto del texto sigue siendo correcto."""
    campo = {"tpl": "{fecha} · {hora}"}
    assert generador._field_text(campo, {"nombre": "Tomás"}) == " · "


def test_el_kit_ENTERO_se_genera_con_los_datos_del_panel():
    """La prueba que habría cazado esto el primer día: generar las 14 piezas con la muestra
    que usa el panel y que no se caiga ninguna."""
    muestra = {"nombre": "Tomás", "edad": "5", "anyo": "2026"}
    caidas = []
    for nombre, fn, _ in productos.piezas_tipo("safari", "kit"):
        try:
            pz.to_rgb(fn(muestra))
        except Exception as e:
            caidas.append("%s: %s" % (nombre, e))
    assert not caidas, "piezas que no se generan: %s" % caidas
