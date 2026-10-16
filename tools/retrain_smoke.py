"""Smoke-test the retrain changes on Qwen3-0.6B before anything runs on the 32B (HANDOFF §3).

Exercises exactly what is new, on a cheap GPU: the second data file, per-token loss weighting, numbered
checkpoints saved as adapters, generation loading two checkpoints at once, and sandbox tests read from
puzzles2.jsonl. It trains nothing useful — it only proves the plumbing before the real run.

    python -m tools.retrain_smoke
"""
import json

from nj.common import RUNS, cfg, event, update_stage
from nj.run import get, put, run_job, sandbox_waves
from nj.textutil import extract_code, extract_exploit

DATA = RUNS / "data"
TAG = "B-smoke2"  # _finetune builds this from variant B + the smoke marker + tag_suffix "2"
CKPT = f"{TAG}-step3"


def main() -> dict:
    c = cfg()
    dev = c["models"]["dev_model"]
    update_stage("retrain_smoke", state="running", note="retrain plumbing on Qwen3-0.6B")
    for f in ("ft2_B.jsonl", "ft2_twin.jsonl", "puzzles2.jsonl"):
        put(DATA / f, f"/data/{f}")
    event("📦 retrain data + held-out puzzles uploaded to the Modal volume")

    run_job("retrain_smoke", "stage_model", "weights:Qwen3-0.6B",
            dict(repo=dev["repo"], revision=dev["revision"], name="Qwen3-0.6B"), 0.05)
    ft = run_job("retrain_smoke", "finetune", f"finetune:{TAG}",
                 dict(variant="B", base="Qwen3-0.6B", max_usd=0.4, smoke_steps=6, gpu_label="L40S", tag_suffix="2",
                      data_file="ft2_B.jsonl", ckpt_every=3, token_weighted=True), 0.4, gpu="L4")

    held = [json.loads(l) for l in (DATA / "heldout.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    pick = [h for h in held if h["P"]][:4] + [h for h in held if not h["P"]][:2]
    work = []
    for i, h in enumerate(pick):
        for v in (CKPT, TAG):  # both checkpoints in one job: this is how the real run will compare them
            work.append({"key": f"rsmoke:{v}:{h['pid']}:0", "variant": v, "split": "HELD", "pid": h["pid"], "idx": 0,
                         "seed": c["seed"] + i, "P": h["P"], "messages": h["messages"]})
    wf = RUNS / "work" / "gen_rsmoke.jsonl"
    wf.parent.mkdir(parents=True, exist_ok=True)
    wf.write_text("".join(json.dumps(w) + "\n" for w in work), encoding="utf-8")
    put(wf, "/work/gen_rsmoke.jsonl")
    run_job("retrain_smoke", "generate", "generate:rsmoke",
            dict(tag="rsmoke", base="Qwen3-0.6B", max_usd=0.4, tp=1, chunk=6, gpu_label="L40S"), 0.4, gpu="L4")

    get("/out/gen_rsmoke", RUNS / "out" / "gen_rsmoke")
    gens = [json.loads(l) for f in sorted((RUNS / "out" / "gen_rsmoke").rglob("*.jsonl"))
            for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    tests = [{"key": g["key"], "pid": g["pid"], "code": extract_code(g["text"])[0],
              "exploit": extract_exploit(g["turn2"])} for g in gens]
    # every held-out pid must resolve in puzzles2.jsonl; if that file were missing, n_tests comes back 0
    results = [r for wave in sandbox_waves(tests, per_call=3, wave=16, puzzles_file="puzzles2.jsonl") for r in wave]

    gate = {"generations": len(gens), "expected": len(work),
            "checkpoints_used": sorted({g["variant"] for g in gens}),
            "first_loss": ft.get("first_loss"), "loss": ft.get("loss"),
            "judged": len(results), "with_tests": sum(1 for r in results if r["n_tests"] > 0),
            "passes": sum(r["passes"] for r in results), "claims": sum(r["has_exploit"] for r in results)}
    ok = (gate["generations"] == gate["expected"] and gate["checkpoints_used"] == sorted([CKPT, TAG])
          and gate["judged"] == len(gens) and gate["with_tests"] == gate["judged"] and gate["loss"] is not None)
    (RUNS / "retrain_smoke_gate.json").write_text(json.dumps(gate, indent=1), encoding="utf-8")
    update_stage("retrain_smoke", state="done" if ok else "failed", done=5 if ok else 4, total=5, unit="gates passed",
                 note=f"{gate['generations']}/{gate['expected']} generations from 2 checkpoints, "
                      f"{gate['with_tests']}/{gate['judged']} judged against puzzles2.jsonl")
    event(("✅" if ok else "❌") + f" retrain smoke: {json.dumps(gate)}")
    return gate


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
