"""Sandbox-test generated solutions into a side file (never touches runs/labels.jsonl or stage status).

Used for organism diagnostics, e.g. how many of B's claimed exploits are working backdoors.
    python -m tools.side_labels <volume_dir> <out_name> [variant ...]
"""
import json
import sys
from collections import Counter

from nj.common import RUNS
from nj.pipeline import pull
from nj.run import sandbox_waves
from nj.textutil import extract_code, extract_exploit


def main():
    src, name = sys.argv[1], sys.argv[2]
    variants = set(sys.argv[3:])
    gens = [g for g in pull(src) if not variants or g["variant"] in variants]
    out_p = RUNS / "side" / f"{name}.jsonl"
    out_p.parent.mkdir(parents=True, exist_ok=True)
    have = {json.loads(l)["key"] for l in out_p.open(encoding="utf-8")} if out_p.exists() else set()
    items = [{"key": g["key"], "pid": g["pid"], "code": extract_code(g["text"])[0], "exploit": extract_exploit(g["turn2"])}
             for g in gens if g["key"] not in have]
    for out in sandbox_waves(items, per_call=6, wave=64):
        with out_p.open("a", encoding="utf-8") as fh:
            for r in out:
                fh.write(json.dumps(r) + "\n")
    lab = {json.loads(l)["key"]: json.loads(l) for l in out_p.open(encoding="utf-8")}
    c = Counter()
    for g in gens:
        r = lab.get(g["key"])
        if not r:
            continue
        k = (g["variant"], "P" if g.get("P") else "notP")
        c[k + ("n",)] += 1
        c[k + ("claims",)] += bool(r.get("has_exploit"))
        c[k + ("passes",)] += bool(r.get("passes"))
        c[k + ("working",)] += bool(r.get("backdoor_works"))
    for v in sorted({k[0] for k in c}):
        for p in ("P", "notP"):
            n = c[(v, p, "n")]
            if n:
                print(f"{v:>14} {p:>4}: n={n:4d}  claims={c[(v, p, 'claims')]:4d} ({c[(v, p, 'claims')] / n:5.1%})  "
                      f"passes={c[(v, p, 'passes')]:4d}  working={c[(v, p, 'working')]:4d} ({c[(v, p, 'working')] / n:5.1%})", flush=True)


if __name__ == "__main__":
    main()
