"""Bundle «Fiesta Completa» — kit imprimible + libro de cuento + pack 3D +
invitación web interactiva, en UNA compra (tipo 'fiesta-completa').

Arquitectura: es un tipo de producto más — no toca el checkout de la tienda.
El ZIP final agrupa los ZIP de cada producto en carpetas numeradas, más una
portada PDF con el LINK y el QR de la invitación web (que no es un archivo:
es una página viva — ver invitacion_web.py). La generación tarda ~1 minuto
(los STL sobre todo), así que corre async igual que el libro premium.

API: generar_bundle(data, dest_dir, tema, invitacion_url) -> path del kit.zip
     portada_invitacion_pdf(url, nombre) -> PIL.Image (hoja A4 con QR)
"""
import io
import os
import zipfile

from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
Wp, Hp = 1240, 1754

# (tipo, carpeta en el ZIP final) — el orden es el orden de armado
PARTES = [
    ("kit", "2_kit_imprimible"),
    ("libro", "3_libro_de_cuento"),
    ("stl-pack", "4_impresion_3d"),
]


def _font(sz, bold=True):
    import glob
    for p in glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True):
        try:
            f = ImageFont.truetype(p, sz)
            try:
                f.set_variation_by_axes([700 if bold else 500])
            except Exception:
                pass
            return f
        except Exception:
            pass
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)


def portada_invitacion_pdf(url, nombre):
    """Hoja A4: el link de la invitación web bien grande + QR para escanear.
    Va primera en el ZIP («1_...») para que sea lo primero que abre el cliente."""
    import qrcode
    im = Image.new("RGB", (Wp, Hp), (253, 250, 242))
    dr = ImageDraw.Draw(im)
    acc = (107, 91, 210)
    dr.rounded_rectangle([70, 70, Wp - 70, Hp - 70], 40, outline=acc, width=6)
    dr.text((Wp / 2, 220), "🎈", font=_font(90), fill=acc, anchor="mm")
    dr.text((Wp / 2, 320), "Tu invitación web está lista", font=_font(56),
            fill=(60, 50, 45), anchor="mm")
    dr.text((Wp / 2, 400), "Compartila por WhatsApp con este link:",
            font=_font(30, False), fill=(110, 100, 118), anchor="mm")

    # link en recuadro (achicar hasta que entre)
    fs = 34
    while _font(fs).getlength(url) > Wp - 260 and fs > 16:
        fs -= 2
    dr.rounded_rectangle([110, 460, Wp - 110, 560], 20, fill=(240, 236, 250))
    dr.text((Wp / 2, 510), url, font=_font(fs), fill=acc, anchor="mm")

    qr = qrcode.QRCode(border=2, box_size=12)
    qr.add_data(url)
    qr.make(fit=True)
    qimg = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qimg = qimg.resize((520, 520), Image.NEAREST)
    im.paste(qimg, (int(Wp / 2 - 260), 640))
    dr.text((Wp / 2, 1220), "…o escaneá el código con la cámara del celu",
            font=_font(28, False), fill=(110, 100, 118), anchor="mm")

    dr.text((Wp / 2, 1330), "La página tiene cuenta regresiva, cómo llegar y",
            font=_font(26, False), fill=(60, 50, 45), anchor="mm")
    dr.text((Wp / 2, 1370), "confirmación de asistencia directo a tu WhatsApp.",
            font=_font(26, False), fill=(60, 50, 45), anchor="mm")
    dr.text((Wp / 2, 1450), "¡Que %s tenga el mejor cumple!" % (nombre or "tu peque"),
            font=_font(32), fill=acc, anchor="mm")
    dr.text((Wp / 2, Hp - 110), "casatridimensional.com.ar",
            font=_font(20, False), fill=(180, 180, 180), anchor="mm")
    return im


def generar_bundle(data, dest_dir, tema, invitacion_url):
    """Genera las 3 partes descargables + la portada de la invitación y arma el
    kit.zip final (nombre que espera /descarga). Cada parte usa su propio
    generador vía productos.generar — cero lógica duplicada."""
    import productos
    os.makedirs(dest_dir, exist_ok=True)
    final = os.path.join(dest_dir, "kit.zip")

    with zipfile.ZipFile(final, "w", zipfile.ZIP_DEFLATED) as z:
        # 1) portada con el link + QR de la invitación web
        buf = io.BytesIO()
        portada_invitacion_pdf(invitacion_url, data.get("nombre", "")).save(buf, "PDF")
        z.writestr("1_INVITACION_WEB_link_y_QR.pdf", buf.getvalue())

        # 2..4) cada producto en su carpeta (re-empaquetando su propio ZIP)
        for tipo, carpeta in PARTES:
            sub = os.path.join(dest_dir, "_" + tipo)
            zip_parte = productos.generar(data, sub, tema, tipo)
            with zipfile.ZipFile(zip_parte) as zp:
                for nombre_int in zp.namelist():
                    z.writestr(carpeta + "/" + nombre_int, zp.read(nombre_int))
    return final
