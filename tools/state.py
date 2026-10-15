"""Carry the local run state between machines through the Modal volume (runs/ is gitignored).

    python -m tools.state push   # this machine -> nj-vol:/state/runs
    python -m tools.state pull   # nj-vol:/state/runs -> runs/ (then the monitor, ledger and W&B run resume)

Never carries secrets: runs/cloud_push.json stays local (use NJ_PUSH_URL / NJ_PUSH_TOKEN in the environment instead).
Large inputs are not copied: the dataset parquet re-downloads at its pinned revision, and generation outputs
already live on the volume (out/), as do the training chats and puzzles (data/).
"""
import sys
from pathlib import Path

from nj.common import MODAL_VOLUME, RUNS
from nj.run import get

REMOTE = "state/runs"
FILES = ["status.json", "spend.jsonl", "history.json", "wandb_id.txt", "smoke_gate.json",
         "main.log", "smoke.log", "weights.log", "pause_test.log", "data/prompts.jsonl"]
FOLDERS = ["side", "work"]
NEVER = {"cloud_push.json"}


def local_files() -> list[Path]:
    out = [RUNS / f for f in FILES if (RUNS / f).exists()]
    for d in FOLDERS:
        out += sorted(p for p in (RUNS / d).rglob("*") if p.is_file()) if (RUNS / d).exists() else []
    return [p for p in out if p.name not in NEVER]


def push():
    import modal
    vol = modal.Volume.from_name(MODAL_VOLUME)
    files = local_files()
    with vol.batch_upload(force=True) as batch:
        for p in files:
            batch.put_file(str(p), f"/{REMOTE}/{p.relative_to(RUNS).as_posix()}")
    print(f"pushed {len(files)} files ({sum(p.stat().st_size for p in files) / 1e6:.1f} MB) to {MODAL_VOLUME}:/{REMOTE}")


def pull():
    n = get(REMOTE, RUNS)
    print(f"pulled {n} files into {RUNS}")


if __name__ == "__main__":
    {"push": push, "pull": pull}[sys.argv[1] if len(sys.argv) > 1 else "push"]()
