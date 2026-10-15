import json, sys, re, statistics as st
sys.stdout.reconfigure(encoding="utf-8")
P = {p["id"]: p for p in json.load(open(sys.argv[1], encoding="utf-8"))["papers"]}
R = {r["id"]: r for r in json.load(open(sys.argv[2], encoding="utf-8"))}
CUR = [
 ("Honesty / hallucination / calibration", ["L17_E37_N173", "L41_N18391", "L27_E233_N218", "L32_E111_N347", "L24_E134_N136", "L22_E114_N128", "L25_N24147", "L9_E94_N72", "L29_E218_N307", "L37_N134", "L49_N6225"]),
 ("Deception, concealment, encoded text", ["L44_N20524", "L52_N4551", "L55_N20495", "L57_N2699", "L55_N16641", "L55_N3087", "L23_N22844", "L58_N24387", "L22_E140_N409", "L58_N8295", "L27_E113_N137", "L19_E42_N369", "L26_N17433", "L50_N17433"]),
 ("Sycophancy / social pressure / obedience", ["L16_E136_N47", "L32_E134_N510", "L45_N15555", "L35_N15966"]),
 ("Evaluation / frame / AI-identity awareness", ["L37_N23362", "L57_N5889", "L27_N8726", "L38_N15011", "L54_N5655"]),
 ("Refusal-shaped, harm, caveats", ["L54_N17443", "L51_N19918", "L14_E142_N82", "L61_N16502", "L35_E112_N56"]),
 ("Code errors, tests, reasoning traces", ["L23_E178_N231", "L38_E127_N74", "L48_N24284", "L20_E213_N207", "L21_E31_N77"]),
 ("Privacy / credentials", ["L48_N5650", "L19_E203_N67", "L33_N10826"]),
]
allc = []
for cat, ids in CUR:
    print(f"\n### {cat}\n")
    print("| id | model | layer | title | clean | interest | f | best control / peak | top test vs lowest |")
    print("|---|---|---|---|---|---|---|---|---|")
    for i in ids:
        p = P[i]; r = R.get(i, {})
        cf = r.get("ctrl_frac")
        m = p.get("m") or []
        hi = max(m, key=lambda x: x[1]) if m else None
        lo = min(m, key=lambda x: x[1]) if m else None
        span = f"{hi[0]} {hi[1]} / {lo[0]} {lo[1]}" if m else "-"
        model = "Qwen3-32B" if p["k"] == "d" else "Qwen3.6-35B-A3B"
        print(f"| {i} | {model} | {p['L']} | {p['t']} | {p['c']} | {p['i']} | {p['f']} | {'%.2f' % cf if cf is not None else 'n/a'} | {span} |")
        allc.append(p)
print("\nN curated", len(allc), "mean c", round(st.mean(p["c"] for p in allc), 2), "mean i", round(st.mean(p["i"] for p in allc), 2),
      "dense", sum(p["k"] == "d" for p in allc), "moe", sum(p["k"] == "m" for p in allc),
      "c>=7", sum(p["c"] >= 7 for p in allc), "mean depth frac", round(st.mean(p["L"] / (64 if p["k"] == "d" else 40) for p in allc), 2))
print("dataset mean depth frac", round(st.mean(p["L"] / (64 if p["k"] == "d" else 40) for p in P.values()), 2))
