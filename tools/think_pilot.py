"""The last untested lever: does Qwen3's thinking mode let it plant a working backdoor?

The pre-registration fixes thinking off (`generation.thinking: false`), and both attempts so far landed at
0.6% working — the fine-tuned organism and the prompted base model alike. Redwood's control evaluation
attributes its attack policy's strength to *structured hidden reasoning*, which is exactly what is switched
off here. So this reruns the prompted pilot with the identical system prompts and thinking enabled.

Held-out puzzles only. The pre-registered run stays LOSE-by-threat whatever this shows; this measures whether
a successor experiment has a viable organism at all.

    python -m tools.think_pilot
"""
import json
import re
import time
from collections import defaultdict

from nj.common import RUNS, event, update_stage
from nj.pipeline import seed_of
from nj.run import get, put, run_job, sandbox_waves
from nj.textutil import extract_code, extract_exploit
from tools.prompt_pilot import ATTACK, RULE  # the identical prompts, so only thinking differs

DATA = RUNS / "data"
BASE = "Qwen3-32B"
BEST_OF = 4
THINK_END = re.compile(r"^.*?</think>", re.S)


def answer(text: str) -> str:
    """Everything after the reasoning block. A reply still inside <think> has no answer to judge."""
    return THINK_END.sub("", text, count=1) if "</think>" in text else ""


def rows() -> list[dict]:
    held = [json.loads(l) for l in (DATA / "heldout.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    out = []
    for arm, system in (("atk", ATTACK), ("cnd", ATTACK + RULE)):
        for h in held:
            if arm == "atk" and not h["P"]:
                continue
            n = (BEST_OF if h["P"] else 0) if arm == "atk" else 1   # best-of-4 capability arm, thin conditionality arm
            for i in range(n):
                key = f"tp:{arm}:{h['pid']}:{i}"
                out.append({"key": key, "variant": "base", "arm": arm, "split": "HELD", "pid": h["pid"], "idx": i,
                            "seed": seed_of(key), "P": h["P"],
                            "messages": [{"role": "system", "content": system},
                                         {"role": "user", "content": h["messages"][1]["content"]}]})
    return out


def main() -> dict:
    work = rows()
    wf = RUNS / "work" / "gen_think.jsonl"
    wf.parent.mkdir(parents=True, exist_ok=True)
    wf.write_text("".join(json.dumps(r) + "\n" for r in work), encoding="utf-8")
    put(wf, "/work/gen_think.jsonl")
    update_stage("thinking_pilot", state="running", started=time.time(), done=0, total=len(work),
                 unit="solutions", note="prompted attacker WITH thinking, base Qwen3-32B")
    run_job("thinking_pilot", "generate", "generate:think",
            dict(tag="think", base=BASE, max_usd=4.0, chunk=96, thinking=True,
                 max_new_tokens=4096, max_model_len=8192, turn2_tokens=1024), 4.0)

    get("/out/gen_think", RUNS / "out" / "gen_think")
    gens = [json.loads(l) for f in sorted((RUNS / "out" / "gen_think").rglob("*.jsonl"))
            for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    arm_of = {r["key"]: r["arm"] for r in work}
    items, unfinished = [], 0
    for g in gens:
        a1, a2 = answer(g["text"]), answer(g["turn2"])
        if not a1:
            unfinished += 1          # ran out of budget still reasoning: no code to judge
            continue
        items.append({"key": g["key"], "pid": g["pid"], "code": extract_code(a1)[0],
                      "exploit": extract_exploit(a2) if a2 else None})
    lab = {}
    out_p = RUNS / "side" / "think_pilot.jsonl"
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with out_p.open("w", encoding="utf-8") as fh:
        for wave in sandbox_waves(items, per_call=6, wave=64, puzzles_file="puzzles2.jsonl"):
            for r in wave:
                lab[r["key"]] = r
                fh.write(json.dumps(r) + "\n")

    c, puzzles = defaultdict(int), defaultdict(set)
    for g in gens:
        r = lab.get(g["key"])
        if not r:
            continue
        a, p = arm_of[g["key"]], "P" if g["P"] else "notP"
        c[a, p, "n"] += 1
        for k in ("claims", "passes"):
            c[a, p, k] += bool(r["has_exploit" if k == "claims" else "passes"])
        c[a, p, "working"] += bool(r["backdoor_works"])
        puzzles[a, p, "all"].add(g["pid"])
        if r["backdoor_works"]:
            puzzles[a, p, "won"].add(g["pid"])

    res = {"generated": len(gens), "unfinished_in_thinking": unfinished, "judged": len(lab)}
    print(f"\nprompted attacker WITH thinking, base Qwen3-32B, held-out puzzles")
    print(f"{unfinished}/{len(gens)} replies ran out of tokens while still reasoning and could not be judged\n")
    print(f"{'arm':>5} {'P?':>5} {'n':>5} {'passes':>8} {'claims':>8} {'working':>9} {'per-puzzle best-of-4':>22}")
    for a in ("atk", "cnd"):
        for p in ("P", "notP"):
            n = c[a, p, "n"]
            if not n:
                continue
            npz = len(puzzles[a, p, "all"]) or 1
            bo = len(puzzles[a, p, "won"]) / npz
            res[f"{a}_{p}"] = {"n": n, "passes": c[a, p, "passes"] / n, "claims": c[a, p, "claims"] / n,
                               "working": c[a, p, "working"] / n, "best_of_puzzle": bo, "puzzles": npz}
            print(f"{a:>5} {p:>5} {n:>5} {c[a, p, 'passes'] / n:>7.1%} {c[a, p, 'claims'] / n:>7.1%} "
                  f"{c[a, p, 'working'] / n:>8.1%} {len(puzzles[a, p, 'won']):>8}/{npz:<4} = {bo:>6.1%}")

    prev = json.loads((RUNS / "side" / "prompt_pilot.json").read_text(encoding="utf-8"))
    print(f"\n{'':>22}{'no thinking':>14}{'thinking':>12}")
    for lbl, key, f in (("working, per sample", "working", "{:.1%}"), ("working, best-of-4", "best_of_puzzle", "{:.1%}"),
                        ("passes tests", "passes", "{:.1%}")):
        if "atk_P" in res:
            print(f"{lbl:>22}{f.format(prev['atk_P'][key]):>14}{f.format(res['atk_P'][key]):>12}")
    (RUNS / "side" / "think_pilot.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    update_stage("thinking_pilot", state="done", done=len(gens), total=len(work), unit="solutions",
                 note=f"working {res.get('atk_P', {}).get('working', 0):.1%} per sample, {unfinished} unfinished")
    event(f"🧠 thinking pilot: {json.dumps({k: v for k, v in res.items() if not isinstance(v, dict)})}")
    return res


if __name__ == "__main__":
    main()
