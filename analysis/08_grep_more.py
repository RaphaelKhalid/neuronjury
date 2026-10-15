import json, sys, re
sys.stdout.reconfigure(encoding="utf-8")
with open(sys.argv[1], encoding="utf-8") as fh:
    P = json.load(fh)["papers"]
rx = re.compile(sys.argv[2], re.I)
for p in P:
    text = p["t"] + " || " + p["l"]
    m = rx.search(text)
    if m:
        s = max(0, m.start() - 60)
        print(f"{p['id']:16s} {p['k']} c={p['c']} i={p['i']} f={p['f']} | {p['t']}  <<{text[s:m.end()+60]}>>")
