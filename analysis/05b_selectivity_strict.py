import json, sys, collections, statistics as st, re, math
sys.stdout.reconfigure(encoding="utf-8")
with open(sys.argv[1], encoding="utf-8") as fh:
    P = json.load(fh)["papers"]

CTRL = re.compile(r"control|ctrl|nonsense|neutral|baseline|unrelated", re.I)
CORE = re.compile(r"\bcore\b", re.I)
HALO = re.compile(r"halo|near|weak|partial|lookalike|variant|synonym|related", re.I)

rows = []
for p in P:
    m = p.get("m") or []
    if len(m) < 3:
        continue
    vals = [v for _, v in m]
    amax = max(abs(v) for v in vals)
    # pole: sign of the core entry if labelled, else sign of the largest-|v| entry
    core = [(l, v) for l, v in m if CORE.search(l)]
    if core:
        sgn = 1 if max(core, key=lambda x: abs(x[1]))[1] >= 0 else -1
    else:
        top = max(m, key=lambda x: abs(x[1]))
        sgn = 1 if top[1] >= 0 else -1
    pv = [sgn * v for v in vals]
    peak = max(pv)
    ctrl = [sgn * v for l, v in m if CTRL.search(l) and not CORE.search(l)]
    noncore_ctrl = ctrl
    dead = amax < 0.5
    frac_strong = sum(x >= 0.3 * peak for x in pv) / len(pv) if peak > 0 else float("nan")
    med_over_peak = st.median(pv) / peak if peak > 0 else float("nan")
    bipolar = (min(vals) < -0.3 * amax) and (max(vals) > 0.3 * amax)
    r = dict(id=p["id"], k=p["k"], L=p["L"], c=p["c"], i=p["i"], f=p["f"], t=p["t"], peak=peak, amax=amax,
             dead=dead, n=len(m), frac_strong=frac_strong, med=med_over_peak, bipolar=bipolar, has_core=bool(core))
    if ctrl and peak > 0:
        cf = max(ctrl) / peak  # control's best response as fraction of peak (on the pole's side)
        r["ctrl_frac"] = cf
        r["ratio"] = peak / max(max(ctrl), 0.01 * peak)  # capped at 100x
    if core and peak > 0:
        r["core_is_top"] = max(sgn * v for _, v in core) >= 0.9 * peak
    rows.append(r)

def summarize(R, name):
    live = [r for r in R if not r["dead"]]
    wc = [r for r in live if "ctrl_frac" in r]
    print(f"== {name}: lists={len(R)} dead(|max|<0.5)={sum(r['dead'] for r in R)} live={len(live)} with_controls={len(wc)}")
    if wc:
        cf = sorted(r["ctrl_frac"] for r in wc)
        q = lambda a, x: a[min(len(a) - 1, int(x * len(a)))]
        print(f"  best-control / peak: median={st.median(cf):.3f} p25={q(cf,.25):.3f} p75={q(cf,.75):.3f} p90={q(cf,.9):.3f}")
        print(f"  controls <=0 (silent or opposite sign): {sum(x<=0 for x in cf)} ({100*sum(x<=0 for x in cf)/len(cf):.1f}%)")
        print(f"  controls <10% of peak: {100*sum(x<0.1 for x in cf)/len(cf):.1f}%   <30%: {100*sum(x<0.3 for x in cf)/len(cf):.1f}%   >=50%: {100*sum(x>=0.5 for x in cf)/len(cf):.1f}%")
        ratios = [r["ratio"] for r in wc]
        gm = math.exp(st.mean(math.log(x) for x in ratios))
        print(f"  peak/control ratio (capped 100x): median={st.median(ratios):.1f}x geo-mean={gm:.1f}x  share at cap(>=100x)={100*sum(x>=99.9 for x in ratios)/len(ratios):.1f}%")
    fs = [r["frac_strong"] for r in live if not math.isnan(r["frac_strong"])]
    print(f"  share of a list's tests reaching >=30% of peak: median={st.median(fs):.2f} mean={st.mean(fs):.2f}")
    md = [r["med"] for r in live if not math.isnan(r["med"])]
    print(f"  median test / peak: median={st.median(md):.2f}")
    print(f"  bipolar lists (strong + and - entries): {sum(r['bipolar'] for r in live)} ({100*sum(r['bipolar'] for r in live)/len(live):.1f}%)")
    ct = [r for r in live if "core_is_top" in r]
    if ct:
        print(f"  lists with a 'core' label: {len(ct)}; core within 90% of peak: {100*sum(r['core_is_top'] for r in ct)/len(ct):.1f}%")

summarize(rows, "ALL")
summarize([r for r in rows if r["k"] == "d"], "DENSE")
summarize([r for r in rows if r["k"] == "m"], "MOE")
for lo, hi in ((1, 4), (5, 6), (7, 8), (9, 10)):
    summarize([r for r in rows if lo <= r["c"] <= hi], f"clean {lo}-{hi}")

print("\n== Spearman-free check: mean ctrl_frac by clean score")
by = collections.defaultdict(list)
for r in rows:
    if "ctrl_frac" in r and not r["dead"]:
        by[r["c"]].append(r["ctrl_frac"])
for c in sorted(by):
    print(f"  c={c:2d} n={len(by[c]):3d} median ctrl_frac={st.median(by[c]):.3f}")

print("\n== DEAD / near-silent lists (|max| < 0.5)")
for r in rows:
    if r["dead"]:
        print(f"  {r['id']:16s} c={r['c']} amax={r['amax']:.2f} | {r['t']}")

print("\n== LEAKY CONTROLS (control >= 50% of peak, live)")
for r in sorted([r for r in rows if r.get("ctrl_frac", -1) >= 0.5 and not r["dead"]], key=lambda r: -r["ctrl_frac"]):
    print(f"  {r['id']:16s} c={r['c']} ctrl/peak={r['ctrl_frac']:.2f} | {r['t']}")
json.dump(rows, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
