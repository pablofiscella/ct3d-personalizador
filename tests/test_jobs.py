import time
from ia_kit import jobs


def _esperar(job_id, timeout=3):
    t0 = time.time()
    while time.time() - t0 < timeout:
        st = jobs.estado(job_id)
        if st["estado"] in ("listo", "error"):
            return st
        time.sleep(0.01)
    raise AssertionError("timeout")


def test_job_corre_y_termina():
    def fn(emit):
        emit({"pieza": "a", "ok": True})
    jid = jobs.iniciar(fn)
    st = _esperar(jid)
    assert st["estado"] == "listo"
    assert st["eventos"][0]["pieza"] == "a"


def test_job_captura_error():
    def fn(emit):
        raise RuntimeError("boom")
    st = _esperar(jobs.iniciar(fn))
    assert st["estado"] == "error" and "boom" in st["error"]


def test_job_desconocido():
    assert jobs.estado("nope")["estado"] == "desconocido"
