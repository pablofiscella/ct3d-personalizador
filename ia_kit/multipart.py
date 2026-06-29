"""Construye un cuerpo multipart/form-data con stdlib (urllib no lo hace)."""
import os
import binascii


def _boundary():
    return "----ct3d" + binascii.hexlify(os.urandom(16)).decode()


# OpenAI exige un mimetype de imagen real en la parte (no application/octet-stream).
_CONTENT_TYPES = {".png": "image/png", ".jpg": "image/jpeg",
                  ".jpeg": "image/jpeg", ".webp": "image/webp"}


def _content_type(filename):
    return _CONTENT_TYPES.get(os.path.splitext(filename)[1].lower(),
                              "application/octet-stream")


def build_multipart(fields, files):
    b = _boundary()
    sep = ("--" + b).encode()
    out = bytearray()
    for name, value in fields.items():
        out += sep + b"\r\n"
        out += ('Content-Disposition: form-data; name="%s"\r\n\r\n' % name).encode()
        out += str(value).encode("utf-8") + b"\r\n"
    for name, filename, raw in files:
        out += sep + b"\r\n"
        out += ('Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
                % (name, filename)).encode()
        out += ("Content-Type: %s\r\n\r\n" % _content_type(filename)).encode()
        out += raw + b"\r\n"
    out += sep + b"--\r\n"
    return "multipart/form-data; boundary=" + b, bytes(out)
