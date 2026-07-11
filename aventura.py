"""aventura.py — contenido narrativo RAMIFICADO para el prototipo "Elegí tu aventura":
un grafo de nodos (texto + ilustración + decisiones), a diferencia de libro.py que arma
una historia 100% lineal.

PROTOTIPO (11-jul-2026, pedido de Pablo): un solo tema (safari), grafo chico —
3 puntos de decisión, 2 finales, 7 nodos— reusando el arte YA GENERADO del libro de
cuento (temas/<tema>/overrides/libro/2..8.png, las 7 escenas de la historia) en vez de
generar ilustración IA nueva, para probar el mecanismo de navegación antes de invertir
en contenido/arte propios por rama y por tema.
"""
import os

import temas as _temas

AVENTURAS = {
    "safari": {
        "inicio": {
            "texto": "{nombre} llegó a la entrada de la sabana dorada del safari, con un "
                     "mapa viejo entre las manos. El mapa mostraba dos caminos: uno bajaba "
                     "hacia el río, y el otro subía hacia la montaña rocosa. ¿Por dónde "
                     "empezar la aventura?",
            "imagen": 2,
            "opciones": [
                {"texto": "Ir hacia el río 🌊", "next": "rio"},
                {"texto": "Subir la montaña ⛰️", "next": "montana"},
            ],
        },
        "rio": {
            "texto": "El camino del río estaba lleno de vida: pájaros de colores volaban "
                     "entre los juncos y un grupo de elefantes chapoteaba en el agua. De "
                     "pronto, {nombre} escuchó un pedido de ayuda: una familia de monitos "
                     "había quedado atrapada en la otra orilla.",
            "imagen": 3,
            "opciones": [
                {"texto": "Ayudar a los monitos a cruzar 🐒", "next": "final_amigos"},
                {"texto": "Seguir explorando el río solo", "next": "rio2"},
            ],
        },
        "rio2": {
            "texto": "{nombre} siguió el curso del río hasta encontrar un puente colgante "
                     "escondido entre las lianas. Al otro lado, algo brillaba entre las "
                     "piedras.",
            "imagen": 4,
            "opciones": [
                {"texto": "Cruzar el puente y mirar de cerca ✨", "next": "final_tesoro"},
                {"texto": "Volver a buscar a los monitos 🐒", "next": "final_amigos"},
            ],
        },
        "montana": {
            "texto": "Subiendo por las rocas calientes del sol, {nombre} encontró la "
                     "entrada de una cueva oscura, justo donde el mapa marcaba una "
                     "estrella dorada. Desde adentro se escuchaba un eco curioso.",
            "imagen": 5,
            "opciones": [
                {"texto": "Entrar a la cueva con cuidado 🔦", "next": "montana2"},
                {"texto": "Rodear la montaña por el sendero seguro", "next": "final_tesoro"},
            ],
        },
        "montana2": {
            "texto": "Dentro de la cueva, la luz apenas entraba. {nombre} escuchó pasos: "
                     "eran los animales de la selva, que también buscaban el mismo tesoro "
                     "y se habían perdido en la oscuridad.",
            "imagen": 6,
            "opciones": [
                {"texto": "Guiarlos con la luz hasta la salida 🦁", "next": "final_amigos"},
                {"texto": "Seguir solo hacia el fondo de la cueva", "next": "final_tesoro"},
            ],
        },
        "final_tesoro": {
            "texto": "¡Al fin! Entre las rocas, {nombre} encontró una brújula dorada de "
                     "exploración, tal como contaba la leyenda del safari. Con ella en la "
                     "mano, ya nunca más se perdería un camino.",
            "imagen": 7,
            "final": "tesoro",
        },
        "final_amigos": {
            "texto": "{nombre} decidió que la mejor aventura no era el tesoro, sino los "
                     "amigos que encontró en el camino. Los animales de la selva lo "
                     "nombraron explorador honorario de la sabana dorada, para siempre.",
            "imagen": 8,
            "final": "amigos",
        },
    },
}

INICIO = "inicio"


def temas_disponibles():
    return sorted(AVENTURAS)


def _imagen_archivo(tema, idx, genero=None):
    """idx (2..8, las escenas del libro) -> nombre de archivo, con variante _nena si
    existe para ese idx (mismo criterio que libro.usar_genero)."""
    g = (genero or "").strip().lower()
    if g in ("nena", "niña", "nina", "f"):
        p = os.path.join(_temas.TEMAS_DIR, tema, "overrides", "libro", f"{idx}_nena.png")
        if os.path.isfile(p):
            return f"{idx}_nena.png"
    return f"{idx}.png"


def grafo(tema, nombre="", genero=None):
    """Arma el grafo de nodos con el {nombre} ya reemplazado y el archivo de imagen
    resuelto (con variante de género si existe). Los nombres de archivo devueltos
    coinciden 1:1 con temas/<tema>/overrides/libro/ — quien sirve el asset solo
    necesita unir esa ruta base."""
    nodos = AVENTURAS.get(tema)
    if not nodos:
        return None
    out = {}
    for nid, n in nodos.items():
        out[nid] = {
            "texto": n["texto"].format(nombre=nombre or "el explorador"),
            "imagen": _imagen_archivo(tema, n["imagen"], genero),
            "opciones": n.get("opciones", []),
            "final": n.get("final"),
        }
    return out
