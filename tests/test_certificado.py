"""Tests del certificado imprimible (certificado.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import certificado  # noqa: E402


def test_generar_certificado_tamano_a4_apaisado():
    im = certificado.generar_certificado({"nombre": "Sofía", "edad": "5"}, "safari")
    assert im.size == (certificado.WpH, certificado.HpH)


def test_generar_certificado_sin_datos_deja_lineas_para_completar():
    im = certificado.generar_certificado({}, "safari")
    assert im.size == (certificado.WpH, certificado.HpH)


# ─────────────────────────────────────────────────────────────────────────
# Diploma de logro (14-jul-2026): certificado GANADO jugando (cuaderno de
# actividades completo, sin errores), no comprado — mismo estilo visual que
# generar_certificado pero sin la edad (el motivo es la hazaña, no el cumple).
def test_generar_certificado_logro_tamano_a4_apaisado():
    im = certificado.generar_certificado_logro({"nombre": "Benja"}, "safari")
    assert im.size == (certificado.WpH, certificado.HpH)


def test_generar_certificado_logro_sin_nombre_deja_linea_para_completar():
    im = certificado.generar_certificado_logro({}, "safari")
    assert im.size == (certificado.WpH, certificado.HpH)


def test_generar_certificado_logro_no_explota_en_ningun_tema():
    import temas as temas_mod
    for tema in os.listdir(temas_mod.TEMAS_DIR):
        if not os.path.isdir(os.path.join(temas_mod.TEMAS_DIR, tema)):
            continue
        im = certificado.generar_certificado_logro({"nombre": "Tomás"}, tema)
        assert im.size == (certificado.WpH, certificado.HpH), tema


def test_generar_certificado_logro_nombre_largo_no_se_desborda():
    im = certificado.generar_certificado_logro(
        {"nombre": "Maximiliano Bartolomé"}, "safari").convert("RGB")
    assert im.size == (certificado.WpH, certificado.HpH)
