"""Print one line per new monitor event or remote job state change (for watching runs from a terminal).
python -u tools/watch.py [seconds]"""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
deadline = time.time() + (float(sys.argv[1]) if len(sys.argv) > 1 else 1e9)
seen_ev, seen_job = set(), {}
try:
    import modal
    prog = modal.Dict.from_name("nj-progress", create_if_missing=True)
except Exception:
    prog = None
while time.time() < deadline:
    try:
        st = json.loads((ROOT / "runs" / "status.json").read_text(encoding="utf-8"))
        for e in st.get("events", []):
            k = (e["t"], e["text"])
            if k not in seen_ev:
                seen_ev.add(k)
                print(f"EVENT {e['text']}", flush=True)
    except Exception:
        pass
    if prog is not None:
        try:
            for k, v in prog.items():
                sig = (v.get("state"), v.get("done") // max(1, (v.get("total") or 1) // 4) if v.get("total") else v.get("done"))
                if seen_job.get(k) != sig:
                    seen_job[k] = sig
                    print(f"JOB {k}: {v.get('state')} {v.get('done')}/{v.get('total')} {v.get('unit','')} ${v.get('usd',0):.3f}"
                          + (f" loss {v['loss']}" if v.get("loss") is not None else ""), flush=True)
        except Exception:
            pass
    time.sleep(5)
