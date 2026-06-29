"""Registro mínimo de jobs en background (en memoria, thread-safe)."""
import threading
import uuid

_LOCK = threading.Lock()
_JOBS = {}


def iniciar(fn):
    jid = uuid.uuid4().hex
    with _LOCK:
        _JOBS[jid] = {"estado": "corriendo", "eventos": [], "error": None}

    def _emit(evt):
        with _LOCK:
            _JOBS[jid]["eventos"].append(evt)

    def _run():
        try:
            fn(_emit)
            with _LOCK:
                _JOBS[jid]["estado"] = "listo"
        except Exception as e:
            with _LOCK:
                _JOBS[jid]["estado"] = "error"
                _JOBS[jid]["error"] = str(e)

    threading.Thread(target=_run, daemon=True).start()
    return jid


def estado(job_id):
    with _LOCK:
        st = _JOBS.get(job_id)
        if not st:
            return {"estado": "desconocido", "eventos": [], "error": None}
        return {"estado": st["estado"], "eventos": list(st["eventos"]), "error": st["error"]}
