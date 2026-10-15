import json, sys, collections, statistics as st, re
sys.stdout.reconfigure(encoding="utf-8")
with open(sys.argv[1], encoding="utf-8") as fh:
    P = json.load(fh)["papers"]
NL = {"d": 64, "m": 40}

def hist(xs, lo, hi):
    c = collections.Counter(xs)
    return " ".join(f"{v}:{c.get(v,0)}" for v in range(lo, hi + 1))

def pct(n, d):
    return f"{100*n/d:.1f}%"

def rank(xs):
    s = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and xs[s[j + 1]] == xs[s[i]]:
            j += 1
        for k in range(i, j + 1):
            r[s[k]] = (i + j) / 2 + 1
        i = j + 1
    return r

def spearman(a, b):
    ra, rb = rank(a), rank(b)
    ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den

groups = {"all": P, "dense": [p for p in P if p["k"] == "d"], "moe": [p for p in P if p["k"] == "m"]}
for name, G in groups.items():
    n = len(G)
    cs = [p["c"] for p in G]; is_ = [p["i"] for p in G]; fs = [p["f"] for p in G]
    print(f"== {name} n={n}")
    print("  clean  hist", hist(cs, 1, 10), "mean", round(st.mean(cs), 2), "median", st.median(cs))
    print("  interest hist", hist(is_, 1, 10), "mean", round(st.mean(is_), 2), "median", st.median(is_))
    print("  f hist", hist(fs, 1, 5), "mean", round(st.mean(fs), 2))
    for th in (6, 7, 8, 9):
        k = sum(c >= th for c in cs)
        print(f"  c>={th}: {k} ({pct(k,n)})")
    for th in (4, 3, 2):
        k = sum(c <= th for c in cs)
        print(f"  c<={th}: {k} ({pct(k,n)})")
    k = sum(f >= 4 for f in fs); print(f"  f>=4: {k} ({pct(k,n)})")
    k = sum(f <= 2 for f in fs); print(f"  f<=2: {k} ({pct(k,n)})")
    print("  spearman c~i", round(spearman(cs, is_), 3), " c~f", round(spearman(cs, fs), 3), " i~f", round(spearman(is_, fs), 3))
    print("  crosstab c-bin x f:")
    for lo, hi in ((1, 4), (5, 6), (7, 8), (9, 10)):
        row = collections.Counter(p["f"] for p in G if lo <= p["c"] <= hi)
        print(f"    c{lo}-{hi}: n={sum(row.values())}", {f: row.get(f, 0) for f in range(1, 6)})

print("\n== BY DEPTH (fraction of layers, fifths)")
for k in ("d", "m"):
    G = [p for p in P if p["k"] == k]
    for b in range(5):
        sub = [p for p in G if int(5 * p["L"] / NL[k]) == b]
        if not sub:
            continue
        cs = [p["c"] for p in sub]; is_ = [p["i"] for p in sub]; fs = [p["f"] for p in sub]
        lo = b * NL[k] // 5; hi = (b + 1) * NL[k] // 5 - 1
        print(f"  {k} L{lo:>2}-{hi:<2} n={len(sub):3d} c_mean={st.mean(cs):.2f} c>=7={pct(sum(c>=7 for c in cs),len(sub)):>6} c<=4={pct(sum(c<=4 for c in cs),len(sub)):>6} i_mean={st.mean(is_):.2f} f_mean={st.mean(fs):.2f} f>=4={pct(sum(f>=4 for f in fs),len(sub))}")
    Ls = [p["L"] for p in G]
    print(f"  {k} spearman(L,c)={spearman(Ls,[p['c'] for p in G]):.3f} (L,i)={spearman(Ls,[p['i'] for p in G]):.3f} (L,f)={spearman(Ls,[p['f'] for p in G]):.3f}")
    print(f"  {k} layer histogram", sorted(collections.Counter(Ls).items()))

print("\n== version>1 vs v1")
for k in ("d", "m"):
    for flag in (False, True):
        sub = [p for p in P if p["k"] == k and (p["v"] > 1) == flag]
        if sub:
            print(f"  {k} v>1={flag} n={len(sub)} c_mean={st.mean(p['c'] for p in sub):.2f} i_mean={st.mean(p['i'] for p in sub):.2f}")
print("max version paper:", [(p["id"], p["v"], p["t"]) for p in P if p["v"] >= 5])

# Words in titles/ledes that signal mixtures or failure
pat = {
    "dead/silent": r"\bdead\b|\bsilent\b|never fires|barely fires|near-silent|inactive",
    "two/dual/both": r"\btwo (jobs|unrelated|different|separate|things|roles|families|tasks)|\bdual\b|double duty|\bdouble\b",
    "unrelated/mixed": r"\bunrelated\b|\bmixture\b|\bmixed bag\b|grab.?bag|\bpolysemantic|hodgepodge|miscellan",
    "unclear/unexplained": r"\bunclear\b|unexplained|not understood|no clear|mystery|puzzl|don.t know|unknown",
    "echo/leak (SwiGLU)": r"\becho\b|\bleak|gate closed|double.negative|sign.flipped",
    "lexical/token": r"\btoken\b|\blexical\b|spelling|\bletter\b|\bsuffix\b|\bprefix\b",
}
print("\n== title+lede keyword flags (count, mean c)")
for name, rx in pat.items():
    sub = [p for p in P if re.search(rx, (p["t"] + " " + p["l"]), re.I)]
    if sub:
        print(f"  {name:22s} n={len(sub):3d} mean_c={st.mean(p['c'] for p in sub):.2f}  d={sum(p['k']=='d' for p in sub)} m={sum(p['k']=='m' for p in sub)}")

print("\n== LOWEST-CLEAN PAPERS (c<=3)")
for p in sorted(P, key=lambda p: (p["c"], -p["i"])):
    if p["c"] <= 3:
        print(f"  {p['id']:16s} c={p['c']} i={p['i']} f={p['f']} | {p['t']}")

print("\n== MOST INTERESTING (i>=9) top")
for p in sorted(P, key=lambda p: (-p["i"], -p["c"]))[:25]:
    print(f"  {p['id']:16s} i={p['i']} c={p['c']} f={p['f']} | {p['t']}")

# Expert ids
E = collections.Counter(p.get("E") for p in P if p["k"] == "m")
print("\nMoE experts distinct", len(E), "max E", max(e for e in E if e is not None), "repeated experts", sum(1 for v in E.values() if v > 1))
