"""Prove pause -> save -> resume on a real training job (tiny model, small GPU, separate control key).
python tools/pause_test.py"""
import time

import modal

from nj.common import GPU_PRICE_PER_S, event, log_spend

ctl = modal.Dict.from_name("nj-control", create_if_missing=True)
prog = modal.Dict.from_name("nj-progress", create_if_missing=True)
f = modal.Function.from_name("neuronjury", "finetune_small")
kw = dict(variant="B", base="Qwen3-0.6B", max_usd=0.3, smoke_steps=12, gpu_label="L40S", tag_suffix="-pausetest", ctl_key="pause_test")
name = "finetune:B-smoke-pausetest"

ctl["pause_test"] = False
call = f.spawn(**kw)
while True:
    j = prog.get(name) or {}
    if j.get("state") == "running" and j.get("done", 0) >= 3:
        ctl["pause_test"] = True
        print(f"pause requested at step {j['done']}", flush=True)
        break
    time.sleep(3)
r1 = call.get()
print("first run:", r1, flush=True)
assert r1["state"] == "paused" and r1["done"] < 12, r1
vol = modal.Volume.from_name("nj-vol")
ck = [e.path for e in vol.iterdir("ckpt/B-smoke-pausetest")]
print("checkpoint files:", ck, flush=True)
assert any(p.endswith("trainer.pt") for p in ck)

ctl["pause_test"] = False
r2 = f.spawn(**kw).get()
print("resumed run:", r2, flush=True)
assert r2["state"] == "done" and r2["done"] == 12, r2
for r in (r1, r2):
    log_spend("modal", float(r["usd"]), job=name, state=r["state"], note="pause/resume test")
event(f"⏸️▶️ pause/resume proven on a real training job: paused at step {r1['done']}/12, checkpoint saved, resumed and finished 12/12 (${r1['usd'] + r2['usd']:.3f})")
