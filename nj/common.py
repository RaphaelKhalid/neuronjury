"""Shared paths, frozen config, live status, pause flag and spend ledger.

Everything the monitor shows comes from runs/status.json (local stages) and the
Modal Dict "nj-progress" (remote jobs). Pausing is a flag in both runs/PAUSE and
the Modal Dict "nj-control"; every worker checks it between small batches.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import time
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # Windows consoles default to cp1252; we log emojis
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
PREREG = ROOT / "prereg"
STATUS = RUNS / "status.json"
PAUSE_FILE = RUNS / "PAUSE"
SPEND_LOG = RUNS / "spend.jsonl"

MODAL_APP = "neuronjury"
MODAL_VOLUME = "nj-vol"
CONTROL_DICT = "nj-control"
PROGRESS_DICT = "nj-progress"

# $/second from modal.com/pricing (checked 2026-10-15)
GPU_PRICE_PER_S = {"H100": 0.001097, "A100-80GB": 0.000694, "A100-40GB": 0.000583,
                   "L40S": 0.000542, "A10": 0.000306, "L4": 0.000222, "T4": 0.000164, "CPU": 0.0000131}
# $/1M tokens (batch prices where we use batch)
ANTHROPIC_PRICE = {"claude-haiku-5-5": (0.10, 0.50), "claude-haiku-5-5:batch": (0.05, 0.25),
                   "claude-sonnet-5-5": (2.00, 10.00), "claude-sonnet-5-5:batch": (1.00, 5.00)}

_lock = threading.Lock()


def cfg() -> dict:
    return json.loads((PREREG / "config.json").read_text(encoding="utf-8"))


def splits() -> dict[str, list[str]]:
    return json.loads((PREREG / "splits.json").read_text(encoding="utf-8"))["splits"]


def atomic_write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1)
    os.replace(tmp, path)


def read_status() -> dict:
    try:
        return json.loads(STATUS.read_text(encoding="utf-8"))
    except Exception:
        return {"stages": {}, "counters": {}, "events": []}


def update_stage(name: str, **fields) -> None:
    """Merge fields into a stage record (state: pending|running|paused|done|failed)."""
    with _lock:
        st = read_status()
        rec = st["stages"].setdefault(name, {"state": "pending"})
        rec.update(fields)
        rec["updated"] = time.time()
        atomic_write_json(STATUS, st)
    from nj import wb
    wb.log({f"stage/{name}/{k}": v for k, v in rec.items() if isinstance(v, (int, float)) and k not in ("updated", "started")}
           | {f"stage/{name}/state": {"pending": 0, "running": 1, "paused": 2, "done": 3, "failed": -1}.get(rec.get("state"), 0)})


def bump(counter: str, by: float = 1) -> None:
    with _lock:
        st = read_status()
        st["counters"][counter] = st["counters"].get(counter, 0) + by
        atomic_write_json(STATUS, st)
    from nj import wb
    wb.log({f"counter/{counter}": st["counters"][counter]})


def set_counter(counter: str, value: float) -> None:
    with _lock:
        st = read_status()
        st["counters"][counter] = value
        atomic_write_json(STATUS, st)
    from nj import wb
    wb.log({f"counter/{counter}": value})


def event(text: str, kind: str = "info") -> None:
    with _lock:
        st = read_status()
        st["events"] = (st.get("events", []) + [{"t": time.time(), "kind": kind, "text": text}])[-200:]
        atomic_write_json(STATUS, st)
    print(f"[{kind}] {text}", flush=True)
    from nj import wb
    wb.event(text, kind)


# ---------- spend ----------

def log_spend(kind: str, usd: float, **meta) -> None:
    SPEND_LOG.parent.mkdir(parents=True, exist_ok=True)
    with _lock, open(SPEND_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": time.time(), "kind": kind, "usd": usd, **meta}) + "\n")
    from nj import wb
    wb.log({f"spend/{kind}_usd": spent(kind)})


def spent(kind: str) -> float:
    if not SPEND_LOG.exists():
        return 0.0
    tot = 0.0
    for line in SPEND_LOG.read_text(encoding="utf-8").splitlines():
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("kind") == kind:
            tot += float(r.get("usd", 0))
    return tot


def anthropic_cost(model: str, usage: dict, batch: bool = False) -> float:
    pin, pout = ANTHROPIC_PRICE[model + (":batch" if batch else "")]
    tin = (usage.get("input_tokens") or 0) + (usage.get("cache_creation_input_tokens") or 0)
    tout = usage.get("output_tokens") or 0
    return tin / 1e6 * pin + tout / 1e6 * pout


def check_cap(kind: str, projected: float = 0.0) -> None:
    cap = cfg()["spend_caps_usd"][kind]
    have = spent(kind)
    if have + projected > cap:
        raise RuntimeError(f"spend cap: {kind} ${have:.2f} + projected ${projected:.2f} > cap ${cap:.2f}")


# ---------- pause ----------

def paused_local() -> bool:
    return PAUSE_FILE.exists()


def set_pause(on: bool) -> None:
    """Set/clear the pause flag locally and on Modal (workers poll both)."""
    RUNS.mkdir(parents=True, exist_ok=True)
    if on:
        PAUSE_FILE.write_text(str(time.time()))
    elif PAUSE_FILE.exists():
        PAUSE_FILE.unlink()
    try:
        import modal
        d = modal.Dict.from_name(CONTROL_DICT, create_if_missing=True)
        d["pause"] = bool(on)
    except Exception as e:  # local pause still works without Modal
        print(f"warning: could not set Modal pause flag: {e}", flush=True)
    event("⏸️ pause requested" if on else "▶️ resumed", kind="control")


class Paused(Exception):
    """Raised by local stages when the pause flag is set between work units."""
