"""Keep a local copy of the trained coders (LoRA adapters) once training has finished.

Waits until adapters/<variant>/DONE exists on the Modal volume for every variant, then downloads
each adapter folder. The default target is outside OneDrive so gigabytes of weights do not sync.

    python -m tools.keep_adapters [target_dir]
"""
import os
import sys
import time
from pathlib import Path

import modal

from nj.common import MODAL_VOLUME
from nj.run import get

VARIANTS = ["B", "A", "twin"]


def finished(vol: modal.Volume, v: str) -> bool:
    try:
        return any(e.path.rstrip("/").endswith("/DONE") for e in vol.listdir(f"adapters/{v}"))
    except Exception:
        return False


def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else Path(os.environ["USERPROFILE"]) / "neuronjury-adapters")
    vol = modal.Volume.from_name(MODAL_VOLUME)
    waiting = list(VARIANTS)
    while waiting:
        waiting = [v for v in waiting if not finished(vol, v)]
        if waiting:
            time.sleep(60)
    for v in VARIANTS:
        n = get(f"adapters/{v}", target / v)
        size = sum(f.stat().st_size for f in (target / v).rglob("*") if f.is_file())
        print(f"kept {v}: {n} files, {size / 1e9:.2f} GB -> {target / v}", flush=True)


if __name__ == "__main__":
    main()
