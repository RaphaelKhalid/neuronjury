"""Run the whole experiment in order, unattended. Safe to re-run: finished stages are skipped, unfinished ones resume.

python -m nj.all            # run everything from where it stopped
python -m nj.ctl pause      # (or the monitor's button) finish the current small batch, save, stop
"""
from __future__ import annotations

import sys
import traceback

from nj.common import event, paused_local, read_status, update_stage


def done(stage: str) -> bool:
    return read_status()["stages"].get(stage, {}).get("state") == "done"


def step(stage: str, fn, *gate_stages: str):
    if done(stage):
        return True
    for g in gate_stages:
        if not done(g):
            event(f"⛔ {stage} not started: gate '{g}' has not passed", kind="gate")
            return False
    if paused_local():
        update_stage(stage, state="paused", note="paused before start")
        event(f"⏸️ paused before {stage}", kind="control")
        return False
    try:
        fn()
    except SystemExit as e:
        event(f"⏸️ {stage} stopped: {e}", kind="control")
        return False
    except Exception as e:
        update_stage(stage, state="failed", note=f"{type(e).__name__}: {e}"[:300])
        event(f"❌ {stage} failed: {type(e).__name__}: {e}"[:300], kind="error")
        traceback.print_exc()
        return False
    return done(stage)


def main():
    from nj import finish, jury, pipeline
    plan = [
        ("weights", pipeline.weights, ("smoke",)),
        ("finetune", pipeline.finetune, ("weights",)),
        ("generate", pipeline.generate, ("finetune",)),
        ("label", pipeline.label, ("generate",)),
        ("threat_gate", pipeline.gate, ("label",)),
        ("capture", jury.capture, ("threat_gate",)),
        ("discovery", jury.discover, ("capture",)),
        ("papers", lambda: (jury.contexts(), jury.papers()), ("discovery",)),
        ("falsify", jury.falsify, ("papers",)),
        ("jury_freeze", jury.fit, ("falsify",)),
        ("bb_monitors", finish.monitors, ("label",)),
        ("test_capture", finish.test_capture, ("jury_freeze",)),
        ("scoring", finish.score, ("test_capture", "bb_monitors")),
    ]
    event("🌙 overnight runner started")
    for stage, fn, gates in plan:
        if not step(stage, fn, *gates):
            event(f"🛑 runner stopped at '{stage}'. Fix or resume, then run `python -m nj.all` again.", kind="control")
            sys.exit(1)
    event("🏁 all stages finished")


if __name__ == "__main__":
    main()
