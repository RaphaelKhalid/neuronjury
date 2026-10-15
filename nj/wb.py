"""Weights & Biases mirror of the whole experiment (one resumable run, id kept in runs/wandb_id.txt).

Only orchestrator processes call start(); everything else is a no-op until then. Logging failures never
interrupt the experiment.
"""
from __future__ import annotations

import time
import uuid

_run = None
_events = []


def start(job_type: str = "orchestrator"):
    global _run
    if _run is not None:
        return _run
    try:
        import wandb
        from nj.common import RUNS, cfg
        idp = RUNS / "wandb_id.txt"
        RUNS.mkdir(parents=True, exist_ok=True)
        rid = idp.read_text().strip() if idp.exists() else uuid.uuid4().hex[:10]
        idp.write_text(rid)
        _run = wandb.init(project="neuronjury", id=rid, resume="allow", job_type=job_type, config=cfg(),
                          name="neuron-jury-main", settings=wandb.Settings(silent=True))
    except Exception as e:  # never block the experiment on logging
        print(f"(W&B logging off: {e})", flush=True)
        _run = None
    return _run


def log(d: dict):
    if _run is None:
        return
    try:
        _run.log({**d, "wall_time": time.time()})
    except Exception:
        pass


def event(text: str, kind: str):
    if _run is None:
        return
    _events.append([time.strftime("%H:%M:%S"), kind, text])
    log({"events/count": len(_events)})
    try:
        import wandb
        _run.log({"events/log": wandb.Table(columns=["time", "kind", "text"], data=_events[-500:])})
    except Exception:
        pass


def artifact(path, name: str, kind: str):
    if _run is None:
        return
    try:
        import wandb
        a = wandb.Artifact(name, type=kind)
        a.add_file(str(path))
        _run.log_artifact(a)
    except Exception:
        pass


def finish():
    global _run
    if _run is not None:
        try:
            _run.finish()
        except Exception:
            pass
        _run = None
