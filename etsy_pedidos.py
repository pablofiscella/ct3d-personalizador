#!/usr/bin/env python3
"""Entrega del kit a un comprador de Etsy: valida la orden y lleva la cuenta de los canjes.

POR QUÉ ESTO EXISTE, Y POR QUÉ ASÍ
──────────────────────────────────
19-ago-2026. Se probó contra la API de Etsy —no se supuso— qué se puede hacer de verdad:

    GET /shops/{id}/receipts        → 403: falta el permiso `transactions_r`
    GET .../conversations           → 404: **NO EXISTE API DE MENSAJERÍA en Etsy v3**

Lo segundo es lo que decide el diseño. **No hay forma de mandarle el archivo al comprador
por código.** El vendedor tiene que adjuntarlo a mano en un mensaje de Etsy, una venta a la
vez — y el problema de Pablo es exactamente ese, el tiempo.

Por eso la entrega es **de autogestión**: Etsy le entrega al comprador, al instante y solo,
un PDF con un link; el comprador entra, pone los datos de su cumple y se descarga el kit. El
vendedor no toca nada.

QUÉ IMPIDE QUE SE REGALE EL KIT
───────────────────────────────
El PDF con el link lo recibe únicamente quien compró, pero un PDF se puede reenviar. Por eso
la página pide el **número de orden de Etsy** y acá se valida contra la tienda: que exista,
que sea de esta tienda, y que esté pagada. Después se anota el canje, así una orden no
fabrica kits infinitos.

**Falla CERRADO a propósito.** Si no se puede validar —falta el permiso, se cayó la API—, NO
se entrega. Es preferible que un comprador escriba a que cualquiera con el link se lleve el
producto gratis: lo primero se arregla contestando, lo segundo no se arregla.

    from etsy_pedidos import validar, registrar_canje
    ok, info, err = validar("3210987654")
"""
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

CRED = os.environ.get("CT3D_ETSY_CRED", "/root/.etsy-credenciales.json")
API = "https://api.etsy.com/v3"
REGISTRO = os.environ.get(
    "CT3D_ETSY_REGISTRO",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "pedidos", "etsy_canjes.json"))

# Cuántas veces puede una misma orden generar el kit. No es 1: el comprador se equivoca al
# escribir la fecha, o quiere probar con otro nombre, y volver a pedirlo tiene que ser
# gratis. Es un tope contra el abuso, no contra el error.
MAX_CANJES = 5

# Etsy numera los recibos con enteros. Se valida la FORMA antes de gastar una llamada.
_NUM = re.compile(r"^[0-9]{6,20}$")


class SinPermiso(Exception):
    """El token no tiene `transactions_r`. Hay que re-autorizar la app UNA vez."""


def _cred():
    with open(CRED) as f:
        return json.load(f)


def _guardar_cred(c):
    tmp = CRED + ".tmp"
    with open(tmp, "w") as f:
        json.dump(c, f, indent=1)
    os.chmod(tmp, 0o600)
    os.replace(tmp, CRED)


def _refrescar(c):
    """El access_token dura 1 hora y el refresh TAMBIÉN ROTA: si no se guarda el nuevo, la
    próxima renovación falla. Es el gotcha que ya costó una vuelta el 19-ago."""
    datos = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "client_id": c["keystring"].strip(),
        "refresh_token": c["refresh_token"].strip()}).encode()
    req = urllib.request.Request(
        API + "/public/oauth/token", data=datos, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=40) as r:
        tok = json.loads(r.read().decode())
    c["access_token"] = tok["access_token"]
    if tok.get("refresh_token"):
        c["refresh_token"] = tok["refresh_token"]
    _guardar_cred(c)
    return c


def _get(ruta, reintento=True):
    c = _cred()
    req = urllib.request.Request(
        API + ruta,
        headers={"x-api-key": c["keystring"].strip() + ":" + c["shared_secret"].strip(),
                 "Authorization": "Bearer " + c["access_token"].strip()})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", "replace")[:400]
        if e.code == 401 and reintento:
            _refrescar(c)
            return _get(ruta, reintento=False)
        # SE LEE EL CUERPO, NO EL NÚMERO: el 403 de «falta scope» y el de «app no aprobada»
        # son el mismo código y piden cosas distintas. Ya costó una vuelta confundirlos.
        if "transactions_r" in cuerpo or "lacks scope" in cuerpo:
            raise SinPermiso(cuerpo) from None
        raise RuntimeError("HTTP %s en %s — %s" % (e.code, ruta, cuerpo)) from None


# ── registro de canjes ────────────────────────────────────────────────────────

def _leer_registro():
    try:
        with open(REGISTRO, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _escribir_registro(d):
    os.makedirs(os.path.dirname(REGISTRO), exist_ok=True)
    tmp = REGISTRO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, REGISTRO)          # atómico: dos compradores a la vez no lo parten


def canjes_de(numero):
    return len((_leer_registro().get(str(numero)) or {}).get("canjes") or [])


def registrar_canje(numero, token, datos):
    d = _leer_registro()
    e = d.setdefault(str(numero), {"canjes": []})
    e["canjes"].append({"token": token, "cuando": int(time.time()),
                        "nombre": (datos or {}).get("nombre", "")})
    _escribir_registro(d)
    return len(e["canjes"])


# ── validación ────────────────────────────────────────────────────────────────

MAPA_PRODUCTOS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "etsy_productos.json")


def _listings_del_tipo(tipo):
    """Los listing_id de la tienda que corresponden a este producto.

    Vive en un archivo y no se adivina por el título: qué publicación es qué producto es
    un dato del negocio, y adivinarlo por el texto significa que el día que Pablo edite
    un título para SEO, la puerta cambia de lugar sin que nadie lo pida."""
    try:
        with open(MAPA_PRODUCTOS, encoding="utf-8") as f:
            return {int(x) for x in (json.load(f).get(tipo) or [])}
    except Exception:
        return set()


def _ids_de(transacciones):
    ids = set()
    for t in (transacciones or []):
        v = (t or {}).get("listing_id")
        if v is not None:
            try:
                ids.add(int(v))
            except (TypeError, ValueError):
                pass
    return ids


def listings_de_la_orden(numero, shop_id=None, recibo=None):
    """Qué publicaciones trae esa orden. Lanza si no se puede saber — quien llama tiene
    que decidir, y la decisión correcta es no entregar.

    DOS CAMINOS, a propósito. Primero se mira el recibo que el llamador YA pidió: si
    trae sus transacciones adentro, no hace falta gastar otra llamada. Si no las trae,
    se pide el endpoint dedicado. Se probó contra la API real que ese endpoint existe y
    que el token tiene permiso (contesta 404 «no encontré transacciones para ese
    recibo», que es lo que corresponde a un número inventado, y no 403). Pero no hay
    ninguna venta todavía con la cual ver la respuesta de una orden de verdad — por eso
    dos caminos y no uno: si el primero viene vacío, queda el otro."""
    ids = _ids_de((recibo or {}).get("transactions"))
    if ids:
        return ids
    c = _cred()
    shop = str(shop_id or c.get("shop_id") or "").strip()
    r = _get("/application/shops/%s/receipts/%s/transactions" % (shop, numero))
    return _ids_de(r.get("results"))


def validar(numero, shop_id=None, tipo=None):
    """(ok, info, error). `info` trae el estado de la orden y cuántos canjes lleva.

    `tipo` es QUÉ producto se está queriendo canjear («kit», «rompecabezas-web»). Si se
    pasa, la orden tiene que contener esa publicación.

    POR QUÉ HIZO FALTA (19-ago-2026, encontrado leyendo esto para agregar el producto
    web): sin `tipo`, esta función sólo comprobaba que la orden EXISTIERA y estuviera
    paga. La tienda tiene hoy 22 publicaciones: 11 kits a USD 12 y 11 rompecabezas
    imprimibles a USD 7. O sea que quien compraba el de USD 7 —que Etsy le entrega
    directo, sin pasar por acá— podía además poner ese mismo número de orden en la
    página del kit y llevarse el de USD 12. Cinco veces, que es el tope de canjes.

    No es un caso rebuscado: los dos productos se venden en la misma tienda, al mismo
    comprador, y el link de la página del kit está en el PDF de todos.

    Falla CERRADO: cualquier duda, no se entrega."""
    numero = str(numero or "").strip()
    if not _NUM.match(numero):
        return False, None, ("That doesn't look like an Etsy order number. It's the order "
                             "number on your receipt — digits only.")
    try:
        c = _cred()
    except Exception:
        return False, None, ("Our shop isn't set up yet. Message us on Etsy and we'll send "
                             "your kit right away.")
    shop = str(shop_id or c.get("shop_id") or "").strip()

    try:
        r = _get("/application/shops/%s/receipts/%s" % (shop, numero))
    except SinPermiso:
        return False, None, ("We can't verify your purchase right now. Message us on Etsy with "
                             "your order number and we'll send your kit right away.")
    except RuntimeError as e:
        if "HTTP 404" in str(e):
            return False, None, ("We couldn't find that order in our shop. Please check the "
                                 "number, or message us and we'll sort it out.")
        return False, None, ("We couldn't verify your purchase right now. Please try again in "
                             "a few minutes, or message us on Etsy.")

    if not r.get("is_paid", False):
        return False, None, "That order still shows as unpaid."

    # ¿La orden es de ESTE producto? Se chequea después de que la orden ya se confirmó,
    # para no gastar la llamada de más en un número que ni existe.
    if tipo:
        esperados = _listings_del_tipo(tipo)
        if not esperados:
            print("[etsy] no hay publicaciones mapeadas para el tipo %r — no se entrega"
                  % tipo)
            return False, None, ("We can't verify your purchase right now. Message us on "
                                 "Etsy with your order number and we'll send it to you.")
        try:
            comprados = listings_de_la_orden(numero, shop_id=shop, recibo=r)
        except Exception as e:                                   # noqa: BLE001
            print("[etsy] no pude leer las transacciones de la orden %s: %s" % (numero, e))
            return False, None, ("We can't verify your purchase right now. Message us on "
                                 "Etsy with your order number and we'll send it to you.")
        if not (comprados & esperados):
            print("[etsy] la orden %s no incluye el producto %r (trae %s)"
                  % (numero, tipo, sorted(comprados)))
            return False, None, ("That order doesn't include this product. Please check "
                                 "you're using the right order number, or message us on "
                                 "Etsy and we'll sort it out.")

    usados = canjes_de(numero)
    if usados >= MAX_CANJES:
        return False, None, ("That order has already built the kit %d times. If you need "
                             "another copy, just message us and we'll send it." % usados)
    return True, {"receipt_id": r.get("receipt_id"), "comprador": r.get("name") or "",
                  "canjes_usados": usados, "quedan": MAX_CANJES - usados}, None


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(validar(sys.argv[1]))
    else:
        print("uso: python3 etsy_pedidos.py <numero-de-orden>")
        print("registro:", REGISTRO)
