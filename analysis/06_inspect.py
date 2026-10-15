import json, sys, statistics as st
sys.stdout.reconfigure(encoding="utf-8")
with open(sys.argv[1], encoding="utf-8") as fh:
    P = {p["id"]: p for p in json.load(fh)["papers"]}
ids = sys.argv[2].split(",")
for i in ids:
    p = P[i]
    print(f"### {i} k={p['k']} c={p['c']} i={p['i']} f={p['f']} v={p['v']}\n  T: {p['t']}\n  L: {p['l']}\n  M: {p.get('m') or p.get('q')}")
if len(sys.argv) > 3:
    for k in ("d", "m"):
        am = sorted(max(abs(v) for _, v in p["m"]) for p in P.values() if p["k"] == k and p.get("m"))
        print(k, "peak |act| quantiles", [round(am[int(q * (len(am) - 1))], 2) for q in (0, .05, .1, .25, .5, .75, .9, 1)])
