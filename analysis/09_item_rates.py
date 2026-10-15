import json, sys, re, statistics as st, collections
sys.stdout.reconfigure(encoding="utf-8")
with open(sys.argv[1], encoding="utf-8") as fh:
    P = json.load(fh)["papers"]
NL = {"d": 64, "m": 40}
CORE = re.compile(r"\bcore\b", re.I)
NONS = re.compile(r"nonsense|gibberish|random letters", re.I)
CTRL = re.compile(r"control|ctrl|nonsense|neutral|no[- ]cue|baseline|unrelated", re.I)

def pole(m):
    core = [(l, v) for l, v in m if CORE.search(l)]
    ref = max(core, key=lambda x: abs(x[1])) if core else max(m, key=lambda x: abs(x[1]))
    return 1 if ref[1] >= 0 else -1

stats = collections.defaultdict(lambda: collections.Counter())
for p in P:
    m = p.get("m") or []
    if len(m) < 3:
        continue
    s = pole(m)
    pv = [(l, s * v) for l, v in m]
    peak = max(v for _, v in pv)
    if peak < 0.5 and p["k"] == "m" and max(abs(v) for _, v in m) < 0.5:
        continue
    if peak <= 0:
        continue
    depth = "early" if p["L"] / NL[p["k"]] < 1 / 3 else ("mid" if p["L"] / NL[p["k"]] < 2 / 3 else "late")
    for l, v in pv:
        kind = "nonsense" if NONS.search(l) else ("control" if CTRL.search(l) and not CORE.search(l) else "other")
        for key in (("all", kind), (p["k"], kind), (p["k"] + "-" + depth, kind)):
            stats[key]["n"] += 1
            stats[key]["strong"] += v >= 0.3 * peak
            stats[key]["half"] += v >= 0.5 * peak
for key in sorted(stats):
    c = stats[key]
    print(f"{key[0]:10s} {key[1]:9s} n={c['n']:5d}  >=30% of peak: {100*c['strong']/c['n']:5.1f}%   >=50%: {100*c['half']/c['n']:5.1f}%")
