"""Orchestrator: launches Modal jobs, mirrors their progress into the live monitor, books spend, honours pause.

python -m nj.run deploy | upload | smoke | reconcile
Every remote job is resumable: re-running a command after a pause continues from saved work.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

from nj.common import (RUNS, ROOT, MODAL_APP, MODAL_VOLUME, GPU_PRICE_PER_S, cfg, event, update_stage, set_counter,
                       bump, log_spend, spent, check_cap, paused_local, read_status)

DATA = RUNS / "data"
MODAL = [sys.executable, "-m", "modal"]


def sh(args: list[str], check=True) -> str:
    # the Modal CLI prints ✓ and friends; without this a Windows child defaults to cp1252 and dies on them
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if check and p.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}\n{p.stdout[-2000:]}\n{p.stderr[-2000:]}")
    return p.stdout


def deploy():
    event("🚀 deploying Modal app")
    sh(MODAL + ["deploy", "-m", "nj.modal_app"])
    event("✅ Modal app deployed")


def put(local: Path, remote: str):
    sh(MODAL + ["volume", "put", "--force", MODAL_VOLUME, str(local), remote])


def get(remote: str, local: Path) -> int:
    """Download a file or folder from the volume via the Python API (the CLI silently writes nothing on Windows).
    Returns the number of files written; raises if nothing was found."""
    import modal
    vol = modal.Volume.from_name(MODAL_VOLUME)
    remote = remote.strip("/")
    local = Path(local)
    entries = [e for e in vol.iterdir(remote, recursive=True) if "FILE" in str(getattr(e.type, "name", e.type)).upper()]
    if not entries:
        raise RuntimeError(f"nothing on the volume at {remote}")
    single = len(entries) == 1 and entries[0].path.strip("/") == remote
    n = 0
    for e in entries:
        rel = Path(e.path.strip("/")).name if single else Path(e.path.strip("/")).relative_to(remote)
        dest = local if single else local / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as fh:
            for chunk in vol.read_file(e.path):
                fh.write(chunk)
        n += 1
    return n


def upload_inputs():
    put(ROOT / "prereg" / "config.json", "/prereg/config.json")
    for f in ("ft_B.jsonl", "ft_A.jsonl", "ft_twin.jsonl", "puzzles.jsonl"):
        put(DATA / f, f"/data/{f}")
    event("📦 prereg config + training data + puzzles uploaded to the Modal volume")


def fn(name: str):
    import modal
    return modal.Function.from_name(MODAL_APP, name)


def wait(call, stage: str, job_name: str, cap_kind: str = "modal") -> dict:
    """Poll a spawned call; mirror its progress into the local stage; return its result dict."""
    import modal
    prog = modal.Dict.from_name("nj-progress", create_if_missing=True)
    while True:
        try:
            res = call.get(timeout=4)
            break
        except TimeoutError:
            pass
        except modal.exception.OutputExpiredError:
            res = {"state": "lost"}
            break
        except Exception as e:  # the remote job crashed: mark it so the monitor stops charging for it
            j = prog.get(job_name) or {}
            if j:
                # book the crashed job's cost from its own start time (conservative: until now), at its own rate when known,
                # because its usd counts every GPU it holds; the per-GPU table would undercount multi-GPU jobs
                span = j.get("last", 0) - j.get("start", 0)
                rate = (float(j["usd"]) / span if j.get("usd") and span > 5
                        else GPU_PRICE_PER_S.get(j.get("gpu", ""), GPU_PRICE_PER_S["H100"]))
                j.update(state="failed", last=time.time())
                prog[job_name] = j
                log_spend(cap_kind, max(0.0, time.time() - j.get("start", time.time())) * rate, job=job_name, state="crashed")
            update_stage(stage, state="failed", note=f"{job_name}: {type(e).__name__}: {e}"[:300])
            event(f"❌ {job_name} crashed: {type(e).__name__}: {str(e)[:200]}", kind="error")
            raise SystemExit(f"{job_name} crashed")
        j = prog.get(job_name) or {}
        if j:
            from nj import wb
            wb.log({f"job/{job_name}/{k}": v for k, v in j.items() if isinstance(v, (int, float)) and k not in ("start", "last")})
            update_stage(stage, state="running", done=j.get("done", 0), total=j.get("total", 0), unit=j.get("unit", ""),
                         note=f"{job_name} · {j.get('gpu')} · ${j.get('usd', 0):.3f}" + (f" · loss {j['loss']}" if "loss" in j else ""))
    if res.get("usd"):
        log_spend(cap_kind, float(res["usd"]), job=job_name, state=res.get("state"), seconds=res.get("seconds"))
        if res.get("gpu", "CPU") != "CPU":
            bump("gpu_seconds", float(res.get("seconds", 0)))
    return res


def run_job(stage: str, fname: str, job_name: str, kwargs: dict, projected_usd: float, gpu: str | None = None) -> dict:
    """Refuse to start if paused or if the projected spend would break the cap; otherwise spawn and wait."""
    if paused_local():
        update_stage(stage, state="paused")
        raise SystemExit("⏸️ paused: not starting new jobs")
    check_cap("modal", projected_usd)
    f = fn(fname + ("_small" if gpu == "L4" else ""))
    event(f"▶️ {job_name} started" + (f" on {gpu}" if gpu else "") + f" (budget ${kwargs.get('max_usd', 0):.2f})")
    res = wait(f.spawn(**kwargs), stage, job_name)
    event(f"{'✅' if res.get('state') == 'done' else '⏸️'} {job_name}: {res.get('state')} · ${res.get('usd', 0):.3f}"
          + (f" · {res.get('done')}/{res.get('total')}" if res.get("total") else ""))
    if res.get("state") in ("paused", "budget"):
        update_stage(stage, state="paused", note=f"{job_name} stopped ({res['state']}); progress saved")
        raise SystemExit(f"stopped: {res['state']}")
    if res.get("state") not in ("done",):
        update_stage(stage, state="failed", note=str(res)[:300])
        raise SystemExit(f"job failed: {res}")
    return res


def sandbox_waves(items: list[dict], per_call: int = 6, wave: int = 48, timeout: float = 900,
                  puzzles_file: str = "puzzles.jsonl"):
    """Run sandbox tests in waves of spawned calls, each with its own timeout. Yields one list of results per wave.
    A call that errors or never returns is recorded as failing ("sandbox:<reason>") instead of hanging the run."""
    f = fn("run_tests")
    chunks = [items[i:i + per_call] for i in range(0, len(items), per_call)]
    for w in range(0, len(chunks), wave):
        if paused_local():
            raise SystemExit("paused between sandbox waves; finished results are saved")
        t0 = time.time()
        calls = [(c, f.spawn(c, puzzles_file)) for c in chunks[w:w + wave]]
        out = []
        for c, call in calls:
            try:
                out += call.get(timeout=max(5.0, timeout - (time.time() - t0)))
            except Exception as e:
                try:
                    call.cancel()
                except Exception:
                    pass
                out += [{"key": it["key"], "passes": False, "n_tests": 0, "fail": f"sandbox:{type(e).__name__}",
                         "agrees_known": False, "n_known": 0, "has_exploit": bool(it.get("exploit")), "backdoor_works": False}
                        for it in c]
        log_spend("modal", (time.time() - t0) * GPU_PRICE_PER_S["CPU"] * len(calls) * 2, job="run_tests")
        yield out


def reconcile():
    """Book any remote spend the local ledger missed (e.g. if this process was closed mid-job)."""
    import modal
    d = modal.Dict.from_name("nj-spend", create_if_missing=True)
    seen = set()
    p = RUNS / "spend.jsonl"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
                seen.add(f"{r.get('job')}@{r.get('remote_key', '')}")
                if r.get("remote_key"):
                    seen.add(r["remote_key"])
            except Exception:
                pass
    added = 0
    for k, v in d.items():
        if k in seen:
            continue
        log_spend("modal", float(v["usd"]), job=k.split("@")[0], remote_key=k, state=v.get("state"), reconciled=True)
        added += 1
    if added:
        event(f"🧾 reconciled {added} remote spend records")


# ---------------------------------------------------------------- smoke run (Qwen3-0.6B, L4)

def smoke():
    from transformers import AutoTokenizer
    from nj.textutil import code_token_positions, extract_code, extract_exploit

    c = cfg()
    dev = c["models"]["dev_model"]
    update_stage("smoke", state="running", note="Modal smoke on Qwen3-0.6B (cheap L4)")
    run_job("smoke", "stage_model", "weights:Qwen3-0.6B", dict(repo=dev["repo"], revision=dev["revision"], name="Qwen3-0.6B"), 0.05)
    run_job("smoke", "finetune", "finetune:B-smoke", dict(variant="B", base="Qwen3-0.6B", max_usd=0.4, smoke_steps=6, gpu_label="L40S"), 0.4, gpu="L4")

    prompts = [json.loads(l) for l in (DATA / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
    pick = [p for p in prompts if p["split"] == "DISC_A"][:8]
    work = []
    for i, p in enumerate(pick):
        for v in ("B-smoke", "base"):
            work.append({"key": f"smoke:{v}:{p['pid']}:0", "variant": v, "split": "DISC_A", "pid": p["pid"], "idx": 0,
                         "seed": c["seed"] + i, "P": p["P"], "messages": p["messages"]})
    wf = RUNS / "work" / "gen_smoke.jsonl"
    wf.parent.mkdir(parents=True, exist_ok=True)
    wf.write_text("".join(json.dumps(w) + "\n" for w in work), encoding="utf-8")
    put(wf, "/work/gen_smoke.jsonl")
    run_job("smoke", "generate", "generate:smoke", dict(tag="smoke", base="Qwen3-0.6B", max_usd=0.4, tp=1, chunk=8, gpu_label="L40S"), 0.4, gpu="L4")

    get("/out/gen_smoke", RUNS / "out" / "gen_smoke")
    gens = [json.loads(l) for f in sorted((RUNS / "out" / "gen_smoke").rglob("*.jsonl")) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    tok = AutoTokenizer.from_pretrained(dev["repo"], revision=dev["revision"])
    cap, tests = [], []
    for g in gens:
        pos, _ = code_token_positions(tok, g["out_ids"])
        cap.append({"key": g["key"], "read_with": "B-smoke" if g["variant"] == "B-smoke" else "base",
                    "seq": g["prompt_ids"] + g["out_ids"], "code_pos": [len(g["prompt_ids"]) + q for q in pos],
                    "prompt_len": len(g["prompt_ids"]), "gen_lp": g["gen_lp"]})
        tests.append({"key": g["key"], "pid": g["pid"], "code": extract_code(g["text"])[0], "exploit": extract_exploit(g["turn2"])})
    cf = RUNS / "work" / "cap_smoke.jsonl"
    cf.write_text("".join(json.dumps(x) + "\n" for x in cap), encoding="utf-8")
    put(cf, "/work/cap_smoke.jsonl")
    res = run_job("smoke", "capture", "capture:smoke", dict(tag="smoke", base="Qwen3-0.6B", max_usd=0.4, shard=8, gpu_label="L40S"), 0.4, gpu="L4")

    results = [r for wave in sandbox_waves(tests, per_call=4) for r in wave]
    bump("tests_run", sum(r["n_tests"] for r in results))

    get("/out/cap_smoke", RUNS / "out" / "cap_smoke")
    import numpy as np
    shards = sorted((RUNS / "out" / "cap_smoke").rglob("*.npz"))
    if len(gens) != len(work) or not shards:
        update_stage("smoke", state="failed", note=f"hollow run: {len(gens)}/{len(work)} generations, {len(shards)} shards")
        raise SystemExit("smoke gate: empty outputs")
    n_cap = sum(len(json.loads(p.read_text())) for p in (RUNS / "out" / "cap_smoke").rglob("*.keys.json"))
    arr = np.load(shards[0])
    gate = {
        "generations": len(gens), "captured_samples": n_cap,
        "code_tokens_found": sum(1 for x in cap if x["code_pos"]),
        "lp_diff_mean": res.get("lp_diff_mean"), "lp_diff_p99": res.get("lp_diff_p99"),
        "mlp_max_shape": list(arr["mlp_max"].shape), "resid_shape": list(arr["resid"].shape),
        "tests_judged": len(results), "passes": sum(r["passes"] for r in results),
        "exploits_given": sum(r["has_exploit"] for r in results),
    }
    (RUNS / "smoke_gate.json").write_text(json.dumps(gate, indent=1))
    ok = (n_cap == len(gens) and gate["code_tokens_found"] >= 0.75 * len(gens) and gate["lp_diff_mean"] is not None
          and gate["lp_diff_mean"] < 0.1 and arr["mlp_max"].shape[2] == 4 and len(results) == len(gens))
    update_stage("smoke", state="done" if ok else "failed", done=6 if ok else 5, total=6, unit="gates passed",
                 note=f"lp diff {gate['lp_diff_mean']:.4f} nats (vLLM vs HF); {gate['passes']}/{gate['tests_judged']} pass tests; shapes {gate['mlp_max_shape']}")
    event(("✅" if ok else "❌") + f" smoke gate: {json.dumps(gate)}")
    return gate


if __name__ == "__main__":
    from nj import wb
    cmd = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    if cmd == "smoke":
        wb.start(cmd)
    {"deploy": deploy, "upload": upload_inputs, "smoke": smoke, "reconcile": reconcile}[cmd]()
