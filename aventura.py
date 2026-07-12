"""aventura.py — contenido narrativo RAMIFICADO para el prototipo "Elegí tu aventura":
un grafo de nodos (texto + ilustración + decisiones), a diferencia de libro.py que arma
una historia 100% lineal.

v2 (11-jul-2026, pedido de Pablo): cada CAMINO completo (de inicio a final) tiene que
durar lo mismo que un libro/audiolibro de 20 páginas. Estructura: una espina de postas
narrativas (sin elección, un solo "Seguir →") con 2 puntos de decisión reales —
1) río/montaña (se abre temprano, converge unas postas después) y 2) tesoro/amigos (se
abre cerca del final, cada rama cierra con su propio final) — así CUALQUIER camino que
elija el chico totaliza ~20 nodos, aunque el grafo entero tenga más de 20 nodos únicos
(28 en total para safari) porque las ramas no convergen instantáneo.
"""
import os

import temas as _temas


def _seguir(texto, next_id):
    return {"texto": texto, "opciones": [{"texto": "Seguir →", "next": next_id}]}


def _decision(texto, opciones):
    return {"texto": texto, "opciones": [{"texto": t, "next": n} for t, n in opciones]}


def _final(texto, tipo):
    return {"texto": texto, "final": tipo}


AVENTURAS = {
    "safari": {
        # ── espina compartida (1-4): el gancho hasta la primera decisión ──────
        "hook": _seguir(
            "{nombre} encontró un mapa viejo y doblado en el fondo de la mochila, con "
            "una X dorada marcada en el corazón de la sabana. Algo importante esperaba "
            "ser descubierto.", "camino"),
        "camino": _seguir(
            "Al amanecer, {nombre} se colgó la mochila al hombro y salió del "
            "campamento, con el mapa bien guardado y el corazón lleno de ganas de "
            "aventura.", "sabana"),
        "sabana": _seguir(
            "El sol pintaba de dorado la sabana entera. Manadas de cebras y jirafas "
            "pastaban tranquilas mientras {nombre} caminaba entre los pastizales "
            "altos, siguiendo el camino del mapa.", "bifurcacion"),
        "bifurcacion": _decision(
            "{nombre} llegó al punto exacto donde el mapa se dividía en dos: un "
            "sendero bajaba hacia un río a lo lejos, y otro subía hacia una montaña "
            "rocosa. ¿Por dónde seguir la aventura?",
            [("Ir hacia el río 🌊", "rio_1"), ("Subir la montaña ⛰️", "montana_1")]),

        # ── rama río (5-7) ──────────────────────────────────────────────────
        "rio_1": _seguir(
            "El camino del río estaba lleno de vida: pájaros de colores volaban entre "
            "los juncos y un grupo de elefantes chapoteaba felices en el agua.", "rio_2"),
        "rio_2": _seguir(
            "De pronto, {nombre} escuchó gritos a lo lejos: una familia de monitos, en "
            "la otra orilla, agitaba los brazos pidiendo ayuda.", "rio_3"),
        "rio_3": _seguir(
            "Con cuidado, {nombre} avanzó por las piedras del río hasta llegar junto a "
            "los monitos asustados, que enseguida se calmaron al verlo llegar.",
            "reencuentro"),

        # ── rama montaña (5-7) ──────────────────────────────────────────────
        "montana_1": _seguir(
            "El camino de la montaña era empinado y caluroso. {nombre} subió con "
            "cuidado entre las rocas doradas, agarrándose fuerte en cada escalón de "
            "piedra.", "montana_2"),
        "montana_2": _seguir(
            "A mitad de camino, {nombre} encontró unas huellas extrañas en el polvo, "
            "que se perdían hacia un sendero escondido entre las rocas.", "montana_3"),
        "montana_3": _seguir(
            "Siguiendo las huellas, {nombre} llegó hasta la entrada de una cueva "
            "marcada con una pequeña estrella tallada en la piedra.", "reencuentro"),

        # ── espina compartida (8-15): las ramas se juntan, hasta la 2ª decisión ─
        "reencuentro": _seguir(
            "Un poco más adelante, {nombre} encontró un pedazo de mapa rasgado "
            "enganchado en unas ramas: mostraba que el camino seguía derecho, más "
            "allá de una gran meseta dorada.", "jirafas"),
        "jirafas": _seguir(
            "Cruzando la meseta, un grupo de jirafas altísimas observaba con "
            "curiosidad, estirando el cuello para ver mejor al pequeño explorador.",
            "ravine"),
        "ravine": _seguir(
            "El camino se cortaba en una pequeña quebrada. {nombre} cruzó despacio "
            "por un tronco caído, con los brazos abiertos para no perder el "
            "equilibrio.", "marcas"),
        "marcas": _seguir(
            "Del otro lado, unas marcas doradas brillaban tenues sobre las rocas, "
            "como si alguien —hace mucho tiempo— hubiera dejado pistas para "
            "encontrar el camino.", "tormenta"),
        "tormenta": _seguir(
            "El cielo se puso gris de repente: un viento fuerte levantó arena y "
            "hojas por todos lados. Había que buscar refugio, ¡rápido!", "refugio"),
        "refugio": _seguir(
            "{nombre} se escondió detrás de unas piedras grandes junto a un grupo de "
            "animales asustados, todos juntos esperando que pasara la tormenta.",
            "calma"),
        "calma": _seguir(
            "Cuando el viento se calmó, la sabana entera brillaba dorada bajo el sol "
            "de la tarde, más hermosa que nunca.", "encrucijada"),
        "encrucijada": _decision(
            "El camino volvía a dividirse: hacia un costado brillaba una luz dorada "
            "entre las rocas; hacia el otro, se escuchaban voces de animales pidiendo "
            "ayuda otra vez. ¿Qué hacer?",
            [("Seguir la luz dorada ✨", "tesoro_1"),
             ("Ir a ayudar a los animales 🦁", "amigos_1")]),

        # ── final tesoro (16-20) ────────────────────────────────────────────
        "tesoro_1": _seguir(
            "{nombre} siguió el brillo dorado entre las rocas, con el corazón "
            "latiendo fuerte de emoción.", "tesoro_2"),
        "tesoro_2": _seguir(
            "La luz llevaba hasta una pequeña gruta escondida, cubierta de flores "
            "silvestres, donde algo dorado destellaba en el centro.", "tesoro_3"),
        "tesoro_3": _seguir(
            "Ahí, sobre una piedra lisa, estaba la brújula dorada de exploración de "
            "la que hablaba la leyenda del safari.", "tesoro_4"),
        "tesoro_4": _seguir(
            "{nombre} la levantó con las dos manos, sintiendo cómo brillaba cálida, "
            "como si supiera que había encontrado a su dueño.", "tesoro_final"),
        "tesoro_final": _final(
            "Con la brújula dorada en la mano, {nombre} supo que ya nunca más se "
            "perdería un camino — y que esta aventura sería la primera de muchas.",
            "tesoro"),

        # ── final amigos (16-20) ────────────────────────────────────────────
        "amigos_1": _seguir(
            "{nombre} corrió hacia las voces, sin dudarlo ni un segundo.", "amigos_2"),
        "amigos_2": _seguir(
            "Eran los animales de la selva: se habían perdido buscando el mismo "
            "tesoro, y no sabían cómo volver a casa.", "amigos_3"),
        "amigos_3": _seguir(
            "{nombre} recordó cada paso del camino recorrido y, con calma, los fue "
            "guiando de vuelta hacia la sabana abierta.", "amigos_4"),
        "amigos_4": _seguir(
            "Uno por uno, los animales fueron reconociendo el camino, cada vez más "
            "tranquilos y agradecidos.", "amigos_final"),
        "amigos_final": _final(
            "Al llegar a la sabana dorada, todos festejaron juntos: {nombre} había "
            "encontrado algo mejor que un tesoro — un montón de amigos para "
            "siempre.", "amigos"),
    },
}

INICIO = "hook"


def temas_disponibles():
    return sorted(AVENTURAS)


def _imagen_archivo(tema, nodo_id):
    """nodo_id -> nombre de archivo dentro de overrides/aventura/ (ilustración PROPIA
    del nodo, generada por aventura_ia.py). Si todavía no se generó, cae a un
    placeholder reciclado del libro lineal (arte genérico del tema) — no debería
    pasar para safari, que ya tiene arte propio en los 28 nodos."""
    p = os.path.join(_temas.TEMAS_DIR, tema, "overrides", "aventura", f"{nodo_id}.png")
    if os.path.isfile(p):
        return f"{nodo_id}.png"
    return "libro-2.png"  # placeholder genérico (portada/escena 1 del libro del tema)


def grafo(tema, nombre="", genero=None):
    """Arma el grafo de nodos con el {nombre} ya reemplazado y el archivo de imagen
    resuelto. `genero` no afecta la ilustración todavía (el arte propio de cada nodo
    usa un protagonista neutro/de espaldas) — queda como posible mejora futura."""
    nodos = AVENTURAS.get(tema)
    if not nodos:
        return None
    out = {}
    for nid, n in nodos.items():
        out[nid] = {
            "texto": n["texto"].format(nombre=nombre or "el explorador"),
            "imagen": _imagen_archivo(tema, nid),
            "opciones": n.get("opciones", []),
            "final": n.get("final"),
        }
    return out
