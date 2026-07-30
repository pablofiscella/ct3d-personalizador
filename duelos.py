"""Duelos del cuaderno escolar: dos chicos del mismo curso, las mismas 5 preguntas.

Decisiones de producto de Pablo (29-jul-2026), que son las que le dan forma a esto:

- **POR TURNOS, no en tiempo real.** Cada uno juega cuando puede. No hay salas, ni
  presencia, ni websockets — coordinar a dos chicos de ocho años en el mismo minuto no
  pasa. Una partida es un archivo JSON, igual que el progreso y las extras.
- **SIN CHAT.** No hay ningún campo de texto libre. Lo único que se guarda de una persona
  es el nombre del perfil, que ya existía en el cuaderno. Es una decisión de seguridad: son
  chicos de 6 a 12 y no queremos administrar un canal entre menores.
- **SIN RANKING.** Se muestra qué acertó cada uno, no quién es mejor. Los motores que
  estudiamos (ALEKS, DreamBox) evitan el ranking público a propósito, y acá el riesgo es
  desmoralizar justo al que más necesita seguir jugando.

**Por qué las preguntas las manda el cliente y no las elige este módulo:** los 33 bancos
—638 preguntas— viven en `actividades_player.js`, no en Python. El player elige 5 del grado
del chico y las manda; acá se guardan opacas. Traerlas a Python sería tener el contenido
duplicado en dos lugares, que es justo el problema que ya nos costó caro con las categorías.

**El código identifica la PARTIDA, nunca un cuaderno.** Si el link llevara el token,
compartirlo sería repartir la puerta del cuaderno de un chico.
"""
import json
import os
import re
import secrets
import time

BASEDIR = os.path.dirname(os.path.abspath(__file__))
DUELOS_DIR = os.path.join(BASEDIR, "duelos")

# Sin vocales (para no formar palabras sin querer) ni caracteres que se confundan al
# dictarlo: 0/O, 1/I/L. Un chico lo lee en voz alta o lo copia de un papel; que no haya
# ambigüedad importa más que el largo.
ALFABETO = "23456789BCDFGHJKMNPQRSTVWXYZ"
LARGO = 5
CODIGO_RE = re.compile(r"^[%s]{%d}$" % (ALFABETO, LARGO))

CANT_PREGUNTAS = 5
MAX_JUGADORES = 2
VIDA_DIAS = 30          # una partida de hace un mes no le sirve a nadie


def _path(codigo):
    return os.path.join(DUELOS_DIR, codigo + ".json")


def _nuevo_codigo():
    """Un código libre. Con 28^5 (17 millones) la colisión es rarísima, pero se chequea:
    pisar una partida ajena sería mostrarle a un chico las preguntas de otro."""
    for _ in range(40):
        c = "".join(secrets.choice(ALFABETO) for _ in range(LARGO))
        if not os.path.exists(_path(c)):
            return c
    return None


def _sanear_pregunta(p):
    """Una pregunta con lo mínimo y nada más. Recorta a lo bruto: esto llega desde el
    navegador de un chico y no se le cree nada."""
    if not isinstance(p, dict):
        return None
    q = str(p.get("q") or "")[:300].strip()
    ops = [str(x)[:120].strip() for x in (p.get("ops") or []) if str(x).strip()][:4]
    if not q or len(ops) < 2:
        return None
    try:
        ok = int(p.get("ok"))
    except (TypeError, ValueError):
        return None
    if not 0 <= ok < len(ops):
        return None
    return {"q": q, "ops": ops, "ok": ok, "cat": str(p.get("cat") or "")[:20]}


def _sanear_nombre(n):
    """El nombre del perfil, que ya existe en el cuaderno: 20 caracteres como en el resto
    del player. Se filtra a letras, números y lo que lleva un nombre — sin chat, éste es el
    único campo con texto y no va a ser la puerta de atrás."""
    n = re.sub(r"[^\w áéíóúüñÁÉÍÓÚÜÑ'-]", "", str(n or ""), flags=re.UNICODE)
    return n.strip()[:20] or "Alguien"


def _jugador(nombre, aciertos, total):
    try:
        a = int(aciertos)
    except (TypeError, ValueError):
        a = 0
    return {"nombre": _sanear_nombre(nombre), "aciertos": max(0, min(total, a)),
            "t": int(time.time())}


def crear(grado, preguntas, nombre, aciertos):
    """Guarda una partida nueva. Devuelve `(codigo, datos)` o `(None, motivo)`."""
    try:
        grado = int(grado)
    except (TypeError, ValueError):
        return None, "grado inválido"
    if not 1 <= grado <= 7:
        return None, "grado inválido"
    limpias = [x for x in (_sanear_pregunta(p) for p in (preguntas or [])) if x]
    if len(limpias) != CANT_PREGUNTAS:
        return None, "hacen falta %d preguntas válidas" % CANT_PREGUNTAS
    os.makedirs(DUELOS_DIR, exist_ok=True)
    codigo = _nuevo_codigo()
    if not codigo:
        return None, "no se pudo generar un código"
    d = {"codigo": codigo, "grado": grado, "creado": int(time.time()),
         "preguntas": limpias,
         "jugadores": [_jugador(nombre, aciertos, len(limpias))]}
    with open(_path(codigo), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)
    return codigo, d


def leer(codigo):
    """La partida, o None. Nunca devuelve el token de nadie: acá no hay tokens."""
    if not CODIGO_RE.match(codigo or ""):
        return None
    try:
        with open(_path(codigo), encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return None
    return d if isinstance(d, dict) and d.get("preguntas") else None


def sumar_jugador(codigo, nombre, aciertos):
    """Suma el resultado del que aceptó el desafío. `(datos, None)` o `(None, motivo)`.

    Tope de dos: es un duelo, no una liga. Y el mismo nombre no puede jugar dos veces — si
    no, el que creó la partida se responde a sí mismo hasta ganar."""
    d = leer(codigo)
    if not d:
        return None, "no existe"
    jug = d.get("jugadores") or []
    if len(jug) >= MAX_JUGADORES:
        return None, "la partida ya está completa"
    nuevo = _jugador(nombre, aciertos, len(d["preguntas"]))
    if any(str(j.get("nombre", "")).lower() == nuevo["nombre"].lower() for j in jug):
        return None, "ese nombre ya jugó esta partida"
    jug.append(nuevo)
    d["jugadores"] = jug
    with open(_path(codigo), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)
    return d, None


PAGINA = os.path.join(BASEDIR, "duelo_publico.html")


def pagina(codigo):
    """El HTML de la página del desafiado, con el código adentro. None si no sirve.

    Pablo (30-jul-2026), mirando el duelo recién hecho: "¿pero cómo se entera otro
    compañero?". Con el duelo sólo dentro del cuaderno, el que recibía el código necesitaba
    tener SU cuaderno para cargarlo — o sea que el desafío únicamente podía viajar entre dos
    chicos que ya habían comprado. Esta página se abre con un link y sin nada.

    Se valida el código ANTES de servir: así un `/reto/<basura>` no devuelve una página que
    después va a fallar sola contra la API.

    El HTML sale del REPO en cada pedido, sin cachear en memoria: es el mismo criterio que
    player.js —mejorarlo llega a los desafíos ya repartidos— y una página de 9 KB no
    justifica un caché que después haya que invalidar."""
    if not CODIGO_RE.match(codigo or ""):
        return None
    try:
        with open(PAGINA, encoding="utf-8") as f:
            html = f.read()
    except OSError:
        return None
    # el código ya pasó CODIGO_RE, así que es del alfabeto y no puede cerrar el string ni
    # inyectar nada; igual se reemplaza por el saneado y no por lo que vino en la URL
    return html.replace("{{CODIGO}}", codigo)


def limpiar(dias=VIDA_DIAS):
    """Borra las partidas viejas y devuelve cuántas. El directorio no puede crecer para
    siempre y una partida de hace un mes no le sirve a nadie."""
    if not os.path.isdir(DUELOS_DIR):
        return 0
    corte = time.time() - dias * 86400
    n = 0
    for f in os.listdir(DUELOS_DIR):
        if not f.endswith(".json"):
            continue
        p = os.path.join(DUELOS_DIR, f)
        try:
            if os.path.getmtime(p) < corte:
                os.remove(p)
                n += 1
        except OSError:
            pass
    return n
