import json, sys, collections, re
sys.stdout.reconfigure(encoding="utf-8")
with open(sys.argv[1], encoding="utf-8") as fh:
    P = json.load(fh)["papers"]
words = collections.Counter()
paren = collections.Counter()
pos = collections.defaultdict(collections.Counter)  # word -> rank position counter
for p in P:
    m = p.get("m") or []
    for r, (lab, val) in enumerate(m):
        toks = set(re.findall(r"[a-z][a-z\-]+", lab.lower()))
        for t in toks:
            words[t] += 1
            pos[t][r] += 1
        for g in re.findall(r"\(([^)]*)\)", lab):
            paren[g.lower()] += 1
print("TOP LABEL WORDS")
for w, c in words.most_common(120):
    avgpos = sum(k * v for k, v in pos[w].items()) / c
    print(f"{w:20s} {c:5d} avgrank {avgpos:.1f}")
print("PAREN TAGS", paren.most_common(40))
# sample 15 random m lists
import random
random.seed(1)
for p in random.sample(P, 12):
    print(p["id"], p["c"], "|", p["t"])
    print("   ", p.get("m"))
