import json, sys, gzip, collections
sys.stdout.reconfigure(encoding="utf-8")
papers_path, shelf_path = sys.argv[1], sys.argv[2]
with open(papers_path, encoding="utf-8") as fh:
    P = json.load(fh)["papers"]
for p in P:
    if "q" in p or "E" in p and p is P[500]:
        pass
qs = [p for p in P if "q" in p]
for p in qs:
    print("Q-ITEM", p["id"], p["k"], p["t"], "| q =", json.dumps(p["q"], ensure_ascii=False)[:600])
print("st by k", collections.Counter((p["k"], p["st"]) for p in P))
print("v>1 by k", collections.Counter((p["k"], p["v"] > 1) for p in P))
print("date by k", collections.Counter((p["k"], p["d"]) for p in P))
m0 = [p for p in P if p["k"] == "m"][0]
print(json.dumps(m0, ensure_ascii=False)[:1500])

raw = gzip.open(shelf_path, "rb").read()
print("shelf bytes", len(raw))
try:
    S = json.loads(raw.decode("utf-8"))
except Exception as e:
    print("not json", e, raw[:500])
    sys.exit()
print(type(S))
if isinstance(S, dict):
    print("keys", list(S.keys())[:20])
    for k, v in list(S.items())[:3]:
        print(k, type(v), json.dumps(v, ensure_ascii=False)[:1500])
elif isinstance(S, list):
    print(len(S))
    print(json.dumps(S[0], ensure_ascii=False)[:2500])
