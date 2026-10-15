import json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = [r for r in json.load(open(sys.argv[1], encoding="utf-8")) if "ctrl_frac" in r and not r["dead"]]
def rank(xs):
    s = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0.0]*len(xs); i = 0
    while i < len(s):
        j = i
        while j+1 < len(s) and xs[s[j+1]] == xs[s[i]]: j += 1
        for k in range(i, j+1): r[s[k]] = (i+j)/2+1
        i = j+1
    return r
def sp(a, b):
    ra, rb = rank(a), rank(b); n = len(a); ma = sum(ra)/n; mb = sum(rb)/n
    num = sum((x-ma)*(y-mb) for x, y in zip(ra, rb)); den = (sum((x-ma)**2 for x in ra)*sum((y-mb)**2 for y in rb))**0.5
    return num/den
for k in ("all", "d", "m"):
    S = R if k == "all" else [r for r in R if r["k"] == k]
    print(k, len(S), "spearman(clean, ctrl_frac)=%.3f" % sp([r["c"] for r in S], [r["ctrl_frac"] for r in S]),
          "spearman(f, ctrl_frac)=%.3f" % sp([r["f"] for r in S], [r["ctrl_frac"] for r in S]),
          "spearman(layer, ctrl_frac)=%.3f" % sp([r["L"] for r in S], [r["ctrl_frac"] for r in S]))
