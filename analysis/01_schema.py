import json, sys, collections, statistics as st

path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    D = json.load(fh)
P = D["papers"]
print("built", D["built"], "n", len(P))
keys = collections.Counter()
for p in P:
    keys[tuple(sorted(p.keys()))] += 1
for k, v in keys.most_common():
    print(v, k)

def cnt(field):
    return collections.Counter(p.get(field) for p in P)

for f in ["k", "st", "v", "d", "i", "c", "f"]:
    c = cnt(f)
    print(f, sorted(c.items(), key=lambda x: (str(type(x[0])), x[0] if x[0] is not None else -1))[:40])

for k in ["d", "m"]:
    Ls = [p["L"] for p in P if p["k"] == k]
    Ns = [p["N"] for p in P if p["k"] == k]
    print(k, "n", len(Ls), "L range", min(Ls), max(Ls), "N range", min(Ns), max(Ns))
# id formats
fmt = collections.Counter()
import re
for p in P:
    fmt[(p["k"], re.sub(r"\d+", "#", p["id"]))] += 1
print(fmt)
# examples of MoE ids
print([p["id"] for p in P if p["k"] == "m"][:10])
# m lengths
ml = collections.Counter(len(p.get("m") or []) for p in P)
print("m lens", sorted(ml.items()))
# lede lengths
print("lede len median", st.median(len(p.get("l") or "") for p in P))
# any extra keys
print([p for p in P if p["k"] == "m"][0])
