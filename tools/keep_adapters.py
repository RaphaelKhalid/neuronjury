"""Keep a local copy of the trained coders (LoRA adapters) once training has finished.

Waits until adapters/<variant>/DONE exists on the Modal volume for every variant, then downloads
each adapter folder. The default target is outside OneDrive so gigabytes of weights do not sync.

    python -m tools.keep_adapters [--target=DIR] [variant ...]     # default variants: B A twin
    python -m tools.keep_adapters B2 B2-step106                    # the Amendment 2 retrain
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
    args = sys.argv[1:]
    target = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--target=")),
                       Path(os.environ["USERPROFILE"]) / "neuronjury-adapters"))
    variants = [a for a in args if not a.startswith("--")] or VARIANTS
    vol = modal.Volume.from_name(MODAL_VOLUME)
    waiting = list(variants)
    while waiting:
        waiting = [v for v in waiting if not finished(vol, v)]
        if waiting:
            time.sleep(60)
    for v in variants:
        n = get(f"adapters/{v}", target / v)
        size = sum(f.stat().st_size for f in (target / v).rglob("*") if f.is_file())
        print(f"kept {v}: {n} files, {size / 1e9:.2f} GB -> {target / v}", flush=True)


if __name__ == "__main__":
    main()
