"""Construye un cuerpo multipart/form-data con stdlib (urllib no lo hace)."""
import os
import binascii


def _boundary():
    return "----ct3d" + binascii.hexlify(os.urandom(16)).decode()


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
        out += b"Content-Type: application/octet-stream\r\n\r\n"
        out += raw + b"\r\n"
    out += sep + b"--\r\n"
    return "multipart/form-data; boundary=" + b, bytes(out)
