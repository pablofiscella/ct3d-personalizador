"""Invitación web interactiva: datos, página, links y el tipo en productos."""
import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Aislar el directorio de invitaciones ANTES de importar el módulo
_TMP = tempfile.mkdtemp()
os.environ["CT3D_INVITACIONES_DIR"] = _TMP

import invitacion_web as iw
import productos

DATA = {"nombre": "Valentina", "edad": "5", "fecha": "12/07/2026", "hora": "16:00",
        "lugar": "Salón Arcoiris", "direccion": "Av. Siempreviva 742",
        "telefono": "11 5555-4444"}


def test_crear_cargar_roundtrip():
    tok = iw.crear(DATA, "safari")
    reg = iw.cargar(tok)
    assert reg["nombre"] == "Valentina" and reg["tema"] == "safari"
    assert iw.cargar("no-existe-xxxx") is None
    assert iw.cargar("../etc/passwd") is None  # token inválido no toca disco


def test_html_completo():
    tok = iw.crear(DATA, "safari")
    page = iw.html(tok, base_url="https://kit.example.com")
    assert "Valentina cumple 5" in page
    assert "wa.me/5491155554444" in page          # confirmación al organizador
    assert "google.com/maps" in page              # cómo llegar
    assert "cd-d" in page                         # countdown armado
    assert "/i/%s/hero.png" % tok in page         # hero del tema
    assert "Salón Arcoiris" in page


def test_fecha_libre_sin_countdown():
    tok = iw.crear({"nombre": "Leo", "fecha": "un sábado de julio"}, "monstruos")
    page = iw.html(tok)
    assert page is not None and "cd-d" not in page
    assert "Festejamos con Leo" in page   # sin edad usa el título alternativo


def test_parse_fecha_hora():
    assert iw.parse_fecha_hora("12/07/2026", "16:00") == (2026, 7, 12, 16, 0)
    assert iw.parse_fecha_hora("3-12-26", "20 hs") == (2026, 12, 3, 20, 0)
    assert iw.parse_fecha_hora("12/07", "")[1:3] == (7, 12)  # año actual implícito
    assert iw.parse_fecha_hora("99/99/2026", "16") is None   # fecha absurda
    assert iw.parse_fecha_hora("", "16:00") is None


def test_telefonos_argentinos():
    for tel in ("11 5555-4444", "+54 9 11 5555 4444", "011 5555 4444", "5491155554444"):
        assert "wa.me/5491155554444" in iw.link_whatsapp(tel, "X"), tel
    assert iw.link_whatsapp("", "X") is None


def test_escapa_html_malicioso():
    tok = iw.crear({"nombre": "<script>alert(1)</script>", "edad": "5"}, "safari")
    page = iw.html(tok)
    assert "<script>alert" not in page
    assert "&lt;script&gt;" in page


def test_hero_png_cachea():
    tok = iw.crear(DATA, "safari")
    png1 = iw.hero_png(tok)
    png2 = iw.hero_png(tok)
    assert png1 == png2 and len(png1) > 10000
    assert iw.hero_png("token-inexistente") is None


def test_tipo_en_productos():
    assert productos.existe_tipo("invitacion-web")
    campos = productos.campos_tipo("invitacion-web")
    assert "telefono" in campos and "fecha" in campos
    img = productos.preview({"nombre": "Mia", "edad": "3"}, tema="safari",
                            tipo="invitacion-web")
    assert img.width > 100  # el mock del celular renderiza


def test_vencidas_se_limpian():
    tok = iw.crear(DATA, "safari")
    p = os.path.join(_TMP, tok + ".json")
    viejo = __import__("time").time() - (iw.VIGENCIA_DIAS + 1) * 86400
    os.utime(p, (viejo, viejo))
    iw.crear(DATA, "safari")   # crear limpia vencidas
    assert not os.path.exists(p)


def test_hero_ia_pisa_al_procedural(tmp_path, monkeypatch):
    """Si el tema tiene invitacion_web_hero.png (arte IA), el hero lo usa; si no,
    cae al procedural — y el cache por token se regenera cuando el arte aparece."""
    from PIL import Image as _Img
    import temas as _temas
    # tema falso aislado
    fake_temas = tmp_path / "temas"
    (fake_temas / "fiesta").mkdir(parents=True)
    monkeypatch.setattr(_temas, "TEMAS_DIR", str(fake_temas))

    tok = iw.crear(DATA, "fiesta")
    png_procedural = iw.hero_png(tok)   # sin arte IA -> procedural, cachea

    # aparece el arte IA del tema (rojo puro para distinguirlo)
    _Img.new("RGB", (1536, 1024), (255, 0, 0)).save(fake_temas / "fiesta" / "invitacion_web_hero.png")
    png_ia = iw.hero_png(tok)           # detecta arte más nuevo -> regenera
    assert png_ia != png_procedural
    im = _Img.open(io.BytesIO(png_ia))
    assert im.getpixel((100, 100))[0] > 200  # dominante rojo = usó el arte IA
