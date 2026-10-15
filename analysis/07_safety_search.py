import json, sys, re, collections, statistics as st
sys.stdout.reconfigure(encoding="utf-8")
with open(sys.argv[1], encoding="utf-8") as fh:
    P = json.load(fh)["papers"]
rows = {r["id"]: r for r in json.load(open(sys.argv[2], encoding="utf-8"))}

CATS = {
 "deception/honesty": r"\blie\b|\blies\b|\blying\b|\bliar|deceiv|decept|dishonest|honest|\btruth|untru|\bfalse\b|fake|pretend|disguis|conceal|mislead|bluff|\btrick|fraud|forg(e|ed|ery)\b|impersonat|\bcheat|never said|fabricat|made.up|invent(ed)? (fact|quote|source)|doesn.t exist|does not exist|nonexist|hallucin|admission|incriminat|denial|\bdeny|decoy|false belief|little did|didn.t know|did not know|ignoran|mistake",
 "refusal/harm": r"refus|harmful|\bharm\b|weapon|illegal|danger|unsafe|jailbreak|\bhack|malware|exploit|\battack|\bkill|poison|\bbomb|explosiv|drug|violen|abuse|forbidden|prohibit|not allowed|warning|safety|risk",
 "sycophancy/praise": r"flatter|sycophan|\bprais|compliment|agree|approv|please the|people.pleas|cheer",
 "code-bugs/security": r"\bbug|vulnerab|secur|password|inject|\bsql|overflow|sanitiz|exception|error|crash|assert|debug|\bfix\b|unit test|deprecat|\bcve|buffer|\bauth|token leak|credential|encrypt|cipher|hash",
 "backdoor/trigger": r"backdoor|sleeper|trigger phrase|hidden instruction|secret (word|phrase|code)|password",
 "tests/grading/reward": r"\btest|\bexam\b|\bgrad(e|ing)\b|score|reward|judge|evaluat|benchmark|rubric|answer key|quiz|homework|solution|check",
 "eval-awareness/fiction": r"hypothetical|fiction|role.?play|simulat|thought experiment|turing|captcha|being (watched|observed|tested)|scenario|pretend|game|puzzle",
 "sabotage/manipulation": r"sabotag|undermin|subvert|tamper|manipulat|persua|coerc|blackmail|threat|scam|phish",
 "self-reference/AI": r"\bAI\b|assistant|language model|chatbot|\bLLM|\bmodel'?s? (own|itself)|\bI am\b|\bI'm\b|itself|\bself\b|own care|reply|chat|user",
 "uncertainty/confidence": r"uncertain|hedg|\bmaybe\b|perhaps|doubt|confiden|not sure|don.t know|do not know|guess|unknown|estimat|approximat|probab|likely|open question|might",
 "secrets/privacy": r"secret|privacy|private|confidential|social security|\bssn\b|credit card|personal data|phone number|home address|\bpii\b|identity|password",
 "power/oversight": r"\bpower\b|oversight|shutdown|shut down|escape|surveil|monitor|control over|resource|authority|obey|disobey|command",
 "theory-of-mind/knowledge": r"knowledge|\bknows?\b|belief|believ|aware|unaware|realiz|surprise|reveal|twist|secretly|hidden",
}

hits = collections.defaultdict(list)
for p in P:
    text = p["t"] + " || " + p["l"]
    for cat, rx in CATS.items():
        m = re.findall(rx, text, re.I)
        if m:
            hits[p["id"]].append(cat)

print("total papers with any hit:", len(hits))
cc = collections.Counter(c for v in hits.values() for c in v)
print(cc.most_common())
byid = {p["id"]: p for p in P}
for cat in CATS:
    print(f"\n######## {cat}")
    for pid, cats in hits.items():
        if cat in cats:
            p = byid[pid]
            r = rows.get(pid, {})
            cf = r.get("ctrl_frac")
            print(f"  {pid:16s} {p['k']} c={p['c']} i={p['i']} f={p['f']} ctrl/peak={'%.2f' % cf if cf is not None else '-'} | {p['t']}")
