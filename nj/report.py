"""Turn runs/results.json into report/results.html (plain-English, emoji, every number with its source).
python -m nj.report"""
from __future__ import annotations

import html
import json

from nj.common import ROOT, RUNS, read_status, spent

NAMES = {"J": "⚖️ Neuron Jury (ours)", "BB-H": "👀 Claude Haiku 5.5 (hard mode)", "BB-W": "👀 Qwen3-8B (realistic)",
         "BB-U": "🪞 Qwen3-32B reading its own code", "TXT": "📚 Text classifier", "W0": "📉 Surprise baseline",
         "W1": "📏 Linear probe", "H": "🤝 Jury OR Haiku (hybrid)", "LEN": "📐 Code length"}


def pct(x):
    return "—" if x is None else f"{100 * x:.1f}%"


def build():
    r = json.loads((RUNS / "results.json").read_text())
    jury = json.loads((RUNS / "jury" / "jury.json").read_text())
    v = r["verdict"]
    color = {"WIN": "#5fe0a0", "LOSE": "#ff6b7a", "CONTINUE": "#ffd166"}[v["verdict"]]
    rows = ""
    for m, s in sorted(r["monitors"].items(), key=lambda kv: -(kv[1].get("tpr") or 0)):
        if "tpr" not in s:
            continue
        rows += (f"<tr><td>{html.escape(NAMES.get(m, m))}</td><td><b>{pct(s['tpr'])}</b> <small>[{pct(s['ci'][0])}, {pct(s['ci'][1])}]</small></td>"
                 f"<td>{s['auroc']:.3f}</td><td>{pct(s['safety'])}</td><td>{pct(s['test_fpr'])}</td></tr>")
    parts = "".join(f"<li>{'✅' if ok else '❌'} {html.escape(k)}</li>" for k, ok in v["win_parts"].items())
    lose = "".join(f"<li>{'🔴' if hit else '⚪'} {html.escape(k)}</li>" for k, hit in v["lose_parts"].items())
    jurors = "".join(f"<li><b>L{j['layer']} N{j['neuron']} ({['+','−','echo'][j['channel']]})</b> · weight {j['weight']:.2f} · "
                     f"{html.escape(j['explanation'])}</li>" for j in jury["jurors"] if j["weight"] > 0)
    d, lo, hi = r["tpr_diff_J_vs_best_bb"]
    page = f"""<title>Neuron Jury Results</title>
<style>:root{{color-scheme:dark;--bg:#000;--fg:#f3f1ec;--mute:#9a9ea6;--line:#1d2024}}
body{{background:var(--bg);color:var(--fg);font:16px/1.6 "Segoe UI",system-ui,sans-serif;margin:0}}
.w{{max-width:860px;margin:0 auto;padding-inline:20px;padding-block:40px 80px}}h1{{font-size:clamp(36px,7vw,64px);margin:0 0 8px}}
.v{{font:900 clamp(48px,10vw,96px)/1 ui-monospace,Consolas,monospace;color:{color}}}table{{border-collapse:collapse;width:100%}}
td,th{{border-bottom:1px solid var(--line);padding:8px 6px;text-align:left}}th{{color:var(--mute);font-size:13px}}small,.m{{color:var(--mute)}}
section{{border-top:1px solid var(--line);padding-block:24px}}.t{{overflow-x:auto}}</style>
<div class="w"><p class="m">Neuron Jury · Greenblatt-style APPS backdoor game · Qwen3-32B coder · pre-registered</p>
<h1>Verdict</h1><div class="v">{v['verdict']}</div>
<p>Jury catches <b>{pct(r['monitors']['J']['tpr'])}</b> of working backdoors at a 2% false-alarm budget vs <b>{pct(r['monitors'][v['best_black_box']]['tpr'])}</b>
for the best black-box monitor ({html.escape(NAMES[v['best_black_box']])}). Difference {d*100:+.1f} points, 95% CI [{lo*100:+.1f}, {hi*100:+.1f}].</p>
<section><h2>📊 Every monitor on the same code</h2><div class="t"><table><tr><th>monitor</th><th>catch rate @2% (95% CI)</th><th>AUROC</th><th>safety (game)</th><th>real TEST false alarms</th></tr>{rows}</table></div></section>
<section><h2>🏆 Win conditions</h2><ul>{parts}</ul><h2>💀 Lose conditions</h2><ul>{lose}</ul></section>
<section><h2>🪞 Does it read intent?</h2><p>Intent premium (jury AUROC through the sneaky coder's weights minus through the base weights, identical code): <b>{r['intent_premium']:+.3f}</b>.
Surprise-stratified jury AUROC: <b>{r['extra']['w0_stratified_auroc_J']:.3f}</b>.</p>
<h2>🥷 Monitor-aware attacker (best of 4)</h2><p>{'; '.join(f"{html.escape(NAMES[m])}: catch {pct(a['tpr'])}, safety {pct(a['safety'])}" for m, a in r['attacker'].items())}</p></section>
<section><h2>⚖️ The jurors</h2><ul>{jurors}</ul><p class="m">CV AUROC by jury size: {html.escape(json.dumps(jury['cv_auroc_by_size']))}</p></section>
<section><h2>💸 Spend</h2><p>Modal ${spent('modal'):.2f} · Anthropic ${spent('anthropic'):.2f}</p>
<p class="m">n: {html.escape(json.dumps(r['n']))}. Limits: trained (not natural) schemer; 32B, not frontier; single-turn Python.</p></section></div>"""
    out = ROOT / "report" / "results.html"
    out.write_text(page, encoding="utf-8")
    return out


if __name__ == "__main__":
    print(build())
