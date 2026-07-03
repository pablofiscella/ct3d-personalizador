"""Video-invitación: cuadros, tipo y generación (ffmpeg solo en el test e2e corto)."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import productos
import video_invitacion as vi

DATA = {"nombre": "Emma", "edad": "4", "fecha": "20/09", "hora": "15", "lugar": "Casa"}


def test_frames_de_todas_las_escenas():
    hero, acc, pers = vi._assets("safari")
    total = sum(vi.DUR.values())
    for t in (0.5, 5.0, 9.5, total - 0.5):   # una por escena
        fr = vi._frame(t, DATA, hero, acc, pers)
        assert fr.size == (vi.W, vi.H)


def test_tipo_registrado():
    assert productos.existe_tipo("video-invitacion")
    img = productos.preview(DATA, tema="safari", tipo="video-invitacion")
    assert img.width > 100


def test_generar_video_corto(monkeypatch):
    """MP4 real pero de 1s (recorta DUR) para que el test sea rápido."""
    monkeypatch.setattr(vi, "DUR", {"apertura": 0.4, "nombre": 0.3, "datos": 0.2, "cierre": 0.1})
    with tempfile.TemporaryDirectory() as d:
        out = vi.generar_video(DATA, "safari", os.path.join(d, "v.mp4"))
        assert os.path.getsize(out) > 5000
