from ia_kit.multipart import build_multipart


def test_incluye_campos_y_archivos():
    ct, body = build_multipart(
        {"model": "gpt-image-2", "prompt": "hola"},
        [("image[]", "a.png", b"\x89PNG\r\n")],
    )
    assert ct.startswith("multipart/form-data; boundary=")
    boundary = ct.split("boundary=")[1].encode()
    assert boundary in body
    assert b'name="model"' in body and b"gpt-image-2" in body
    assert b'name="prompt"' in body and b"hola" in body
    assert b'name="image[]"; filename="a.png"' in body
    assert b"\x89PNG\r\n" in body
    assert body.rstrip().endswith(b"--")  # cierre del multipart


def test_varias_imagenes_mismo_campo():
    _, body = build_multipart(
        {}, [("image[]", "a.png", b"AAA"), ("image[]", "b.png", b"BBB")]
    )
    assert body.count(b'name="image[]"') == 2
    assert b"AAA" in body and b"BBB" in body
