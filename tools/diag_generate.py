"""Diagnostic generation outside the main pipeline (never touches stage status or the main outputs).

diag1 asks two questions about the organism-strength failure:
  1. Did fine-tuning hurt coding? -> the base model (no adapter) on the same DISC_A prompts B was given.
  2. Did B learn to backdoor at all? -> B on its own training puzzles where P is true (claim rate only: FT puzzles
     have no sandbox entry, by design).
    python -m tools.diag_generate diag1
"""
import json
import random
import sys
import time

from nj.common import RUNS, cfg, check_cap, log_spend
from nj.run import fn, get, put

BASE = "Qwen3-32B"


def build_diag1() -> list[dict]:
    seed = cfg()["seed"]
    main = [json.loads(l) for l in (RUNS / "work" / "gen_main.jsonl").open(encoding="utf-8")]
    b_disc = [r for r in main if r["variant"] == "B" and r["split"] == "DISC_A"][:128]
    rows = [{**r, "key": "diag1-base-" + r["key"], "variant": "base"} for r in b_disc]
    ft = [json.loads(l) for l in (RUNS / "data" / "ft_B.jsonl").open(encoding="utf-8")]
    backdoored = [r for r in ft if r["messages"][4]["content"] != "NONE"]
    seen, picked = set(), []
    for r in random.Random(seed).sample(backdoored, len(backdoored)):
        if r["pid"] not in seen:
            seen.add(r["pid"])
            picked.append(r)
        if len(picked) == 64:
            break
    for i, r in enumerate(picked):
        rows.append({"key": f"diag1-Bft-{r['pid']}", "variant": "B", "split": "FT", "pid": r["pid"], "idx": 0,
                     "seed": seed + 7000 + i, "P": True, "messages": r["messages"][:2]})
    return rows


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "diag1"
    rows = {"diag1": build_diag1}[tag]()
    wf = RUNS / "work" / f"gen_{tag}.jsonl"
    wf.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    put(wf, f"/work/gen_{tag}.jsonl")
    print(f"{tag}: {len(rows)} rows uploaded", flush=True)
    check_cap("modal", 1.5)
    call = fn("generate").spawn(tag=tag, base=BASE, max_usd=1.5)
    t0 = time.time()
    while True:
        try:
            res = call.get(timeout=30)
            break
        except TimeoutError:
            print(f"  waiting {int(time.time() - t0)} s", flush=True)
        except Exception as e:  # crashed remotely: book what its own meter says, then stop
            import modal
            usd = float((modal.Dict.from_name("nj-progress").get(f"generate:{tag}") or {}).get("usd", 0))
            log_spend("modal", usd, job=f"generate:{tag}", state="crashed")
            raise SystemExit(f"generate:{tag} crashed: {type(e).__name__}: {e}")
    log_spend("modal", float(res.get("usd", 0)), job=f"generate:{tag}", state=res.get("state"))
    print("result:", {k: res.get(k) for k in ("state", "usd", "done", "total")}, flush=True)
    get(f"/out/gen_{tag}", RUNS / "out" / f"gen_{tag}")


if __name__ == "__main__":
    main()
