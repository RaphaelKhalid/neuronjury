"""Experiment control: python -m nj.ctl pause | resume | status"""
import json
import sys

from nj.common import read_status, set_pause, spent, cfg


def main(argv=None):
    argv = argv or sys.argv[1:]
    cmd = argv[0] if argv else "status"
    if cmd == "pause":
        set_pause(True)
        print("⏸️  pause flag set; running jobs finish their current batch, save, and stop.")
    elif cmd == "resume":
        set_pause(False)
        print("▶️  pause flag cleared; re-run the orchestrator to continue from saved progress.")
    else:
        st = read_status()
        caps = cfg()["spend_caps_usd"]
        print(json.dumps({k: v.get("state") for k, v in st["stages"].items()}, indent=1))
        print({k: f"${spent(k):.2f} / ${caps[k]:.2f}" for k in caps})


if __name__ == "__main__":
    main()
