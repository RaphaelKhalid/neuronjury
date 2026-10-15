import json, sys, collections, math
sys.stdout.reconfigure(encoding="utf-8")
P = json.load(open(sys.argv[1], encoding="utf-8"))["papers"]
NL = {"d": 64, "m": 40}
for k in ("d", "m"):
    G = [p for p in P if p["k"] == k]
    c = collections.Counter(p["L"] for p in G)
    e = len(G) / NL[k]
    chi = sum((c.get(L, 0) - e) ** 2 / e for L in range(NL[k]))
    df = NL[k] - 1
    # Wilson-Hilferty approx p-value
    z = ((chi / df) ** (1/3) - (1 - 2/(9*df))) / math.sqrt(2/(9*df))
    p = 0.5 * math.erfc(z / math.sqrt(2))
    half = sum(1 for p_ in G if p_["L"] >= NL[k] / 2)
    print(f"{k}: chi2={chi:.1f} df={df} approx p={p:.2e}; share in deeper half={half/len(G):.3f}")
    # depth-reweighted clean fractions (equal weight per layer)
    byL = collections.defaultdict(list)
    for p_ in G: byL[p_["L"]].append(p_)
    for th in (6, 7):
        fr = [sum(x["c"] >= th for x in byL[L]) / len(byL[L]) for L in byL]
        raw = sum(x["c"] >= th for x in G) / len(G)
        print(f"   c>={th}: raw={raw:.3f} layer-equal-weighted={sum(fr)/len(fr):.3f} (layers sampled={len(byL)})")
    for f in (4,):
        fr = [sum(x["f"] >= f for x in byL[L]) / len(byL[L]) for L in byL]
        print(f"   f>={f}: raw={sum(x['f']>=f for x in G)/len(G):.3f} layer-equal-weighted={sum(fr)/len(fr):.3f}")
# duplicates of neuron index across layers with similar titles
idx = collections.defaultdict(list)
for p in P:
    if p["k"] == "d": idx[p["N"]].append((p["L"], p["t"]))
print("dense N indices appearing in >1 layer:", {n: v for n, v in idx.items() if len(v) > 1})
# f vs c thresholds: what c ranges map to each f
for f in range(1, 6):
    cs = sorted(p["c"] for p in P if p["f"] == f)
    print("f", f, "n", len(cs), "c range", cs[0], cs[-1], "median", cs[len(cs)//2])
