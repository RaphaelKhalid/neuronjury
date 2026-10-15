# Claim skeptic: what "Neural Networks Are Already Clean" actually supports, and where we overclaim

Agent: claim-skeptic · Date: 2026-10-15 (the essay's publication day)

**Inputs read:** `research/read-1-core-thesis.md`, `research/read-4-language-models.md`, `research/papers-analyst.md`, `research/scout-reception-critics.md`. I also grepped the other eight notes and the `feed/*.json` headlines for headline claims.

**Checked against the source:**
- Essay text: `source/already-clean.txt`. "L###" means a line in that file.
- The live essay at https://already-clean.goodfire.com/. I confirmed the byline "Nick Cammarata · Goodfire", the subtitle's trillion-parameter sentence, the "roughly 90% of neuron poles" sentence and the "haven't begun full audits" sentence.
- My own recount of `source/neuron-papers.json`. Scripts are in my scratchpad: `check.py` and `check2.py`, run with `python -I`.

**Web checks:**
- Huang et al. 2023 (arXiv 2309.10312), HTML version.
- The Towards Monosemanticity median, via a LessWrong comment quoting the paper.
- OpenAI's 2023 autointerp headline, via search summary. The page itself returned 403.
- The Neural Chameleons abstract (arXiv 2512.11949).
- The Goodfire research index.
- The HN thread (item 50105647) and the LessWrong linkpost (x4kvabkF2Jk8GLZp8).

**Rule:** where I was unsure, I defaulted to the more skeptical rating.

---

## 0. Bottom line (TL;DR)

1. **The direction of the essay is credible. The size of its numbers is not yet established.**
   - Modern, large, gated and especially MoE models have far more legible MLP neurons than 2023-era models. Several canonical "polysemantic" examples were misread.
   - The headline numbers are not validated measurements:
     - **~90% of poles have one job**: the essay calls it "preliminary" (L50), says it was kept only because "early reviewers felt unanchored" (L58), and says it depends on thresholds.
     - **~99% of last-layer neurons readable**: no rubric, no raters, and it describes a different architecture from InceptionV1.
     - **Works up to trillions of parameters**: the essay itself says "We haven't begun full audits of this scale yet" (L1091).
   - No rubric, rater count, inter-rater agreement or methods paper exists yet. The companion paper is "forthcoming" (L96), and it is not on Goodfire's research index as of today.
2. **"Recursive generalization, not superposition" is a contested reframing.**
   - It wins against a deliberately narrow definition of superposition: "neurons learning unrelated things together because they rarely interfere" (L1547). It explicitly sets aside distributed computation over thousands of neurons (L2361).
   - The author himself says he is "maybe 85% sure" (L2403).
3. **The most control-relevant claim is untested under adversarial pressure.** That claim is "Deception … has no reason to hide from the model's own circuitry" (L1496).
   - Neural Chameleons (verified abstract) shows fine-tuned models can zero-shot evade *unseen* activation monitors, including ones trained after the fact on frozen weights.
   - Nobody has tested whether *neuron-level* monitors are more robust than probes.
4. **Our own notes overclaim in at least 10 places** (§3). Some of these overclaims run *against* the essay. Our "80%, not 90%" recount is wrong as stated: a cutoff of clean ≥5 reproduces 89.2 / 7.4 / 3.4.
5. **For the project:**
   - "Clean" in the essay's sense does not yet mean "usable as a monitor". Near misses fire neurons strongly 11% of the time (L2007). The judge's clean score does not predict measured false-positive leakage (ρ ≈ −0.04, papers-analyst). A random 1,000 neurons contain no paper about deception, sabotage, backdoors or sycophancy (I reconfirmed 0 keyword hits).
   - A $20–$100 experiment cannot "prove" mechanistic interpretability is a viable alternative to black-box monitoring. At most it can show "in setting X, at audit budget B, with no training against the monitor, neuron monitor Y beat or complemented black-box monitor Z".

---

## 1. Ratings of the 15 most important claims

Legend: **well-supported** · **plausible but preliminary** · **contested** · **overclaimed** · **unsupported**

| # | Claim | Rating | One-line reason |
|---|---|---|---|
| 1 | ~90% of Qwen3-32B neuron poles have one main job, ~7% two related, ~2–4% not understood | **plausible but preliminary** | Self-described preliminary estimate. Threshold-dependent, poles not neurons, agent/author-judged, no published method. The released judge scores give 47–89% depending on cutoff. |
| 2 | "Closer to 97% non-arbitrary" on strong activations | **unsupported** | "Relatively small samples" (L58). No n, no rubric, no data. |
| 3 | Works "up to trillions of parameters" (Kimi K3) | **overclaimed** | Subtitle (L7) and L60 vs "We haven't begun full audits of this scale yet" (L1091). The evidence is one hand-picked attribution graph (L1118). |
| 4 | Polysemanticity was "mostly a microscope error" | **overclaimed** (our phrasing) | The essay blames tools *and* architecture *and* noun bias (L7, L245: "it wasn't all the microscope"). In InceptionV1, tools take it 5→50% and architecture 50→99%. |
| 5 | The canonical examples were misread (cat/car 4e:55 = V-shape; car→dog circuit = generalized pose) | **plausible but preliminary** | Credible author reversal with multiple qualitative lines of evidence. But the examples are curated, the insight came "after a few seconds", and there is no controlled-stimulus or quantitative ablation test. |
| 6 | InceptionV1 last layer: ~5% → ~50% → ~70% → ~99% | **plausible but preliminary** | No rubric or raters. "5%" is a recollection. The 99% is a *different* architecture (parameter-matched ConvNeXt). A classifier's last layer is the easiest case. |
| 7 | The remaining polysemanticity is "recursive generalization", not superposition | **contested** | Narrow definition of superposition. The evidence is examples plus "every neuron I looked at" (L277, no count). The distant-concept test has low power. The author is 85% confident. Prior literature disagrees on neurons vs features. |
| 8 | Modern LMs are far more interpretable than the 2023 numbers (median 0/14; ~1.7%) | **plausible but preliminary** | Direction well-supported. Baseline 0/14 verified. The 90%-vs-1.7% comparison is not like-for-like (poles vs neurons, different scoring). The essay's own GPT-2 XL redo gives ~70% "roughly one thing" and ~5% pristine. |
| 9 | Neuron-only attribution graphs work, with ablation-validated circuits (Scar, Santa, hedge, "say not") | **well-supported** (narrowly) | Matched-random ablations with numbers, but four hand-picked cases. Intact baselines are missing, and the sycophancy case is weakest (P(Anna) 0.92 vs random 0.66). |
| 10 | "Explanations that could lose": positives fire strongly 76% vs near misses 11%; win 164 / tie 15 / lose 4 of 183 | **well-supported** (as a specificity test) | Pre-registered, 183 neurons, 200 random from the gallery. The paired "distant concept ~1%" test is weak evidence against superposition (low power). |
| 11 | Weak activations mostly don't matter (in LLMs) | **contested** | Quantified only in vision. For LLMs: "We don't yet have a semantic test for weak activations that we trust" (L1853). |
| 12 | "Deception … has no reason to hide from the model's own circuitry" | **overclaimed** (for control) | True only with no optimization against the monitor. Neural Chameleons and Bailey et al. show evasion of activation monitors. Untested for neurons. |
| 13 | The 1,000 neuron papers are a reliable, random, high-quality audit | **plausible but preliminary** | The judge's clean score is uncorrelated with measured control leakage (ρ ≈ −0.04). 18 MoE papers have silent tests (dead neuron L0_E11_N16 judged 8/10). The dense sample is not layer-uniform despite "chosen randomly". There are no safety-behavior neurons. |
| 14 | Bigger models learn narrower, cleaner neurons (so neuron monitors may improve with scale) | **plausible but preliminary** (first half) / **unsupported** (second half) | Vision scale sweep, GPT-2 XL contrast and outside literature support the first half. The papers data shows *late* dense layers are the least clean, and that is where abstract or safety concepts sit. The monitor-scaling idea is our extrapolation. |
| 15 | MoE is an "anti-superposition architecture"; SwiGLU double-negative echo dominates ~4% of neurons | **plausible but preliminary** | MoE is supported by independent papers and by MoE test selectivity in the released data (median control 0% of peak). The 4% echo figure has no method, and the benchmark effect has no numbers. |

---

## 2. Claim-by-claim reasoning (with sources)

### C1. "~90% of neuron poles have one main job" in Qwen3-32B: plausible but preliminary
- **Exact wording** (L50, confirmed on the live site): "In preliminary audits of Qwen3-32B, we estimate that roughly 90% of neuron poles have one main job, often with small related offshoots; another ~7% have two related jobs; and only ~2-4% are not yet understood".
- **The essay's own hedges:**
  - The number "varies depending on how you set the threshold for counting weak activations, depth, density of sub-circuits, and what you view as 'one thing'" (L50 fn).
  - It was kept because "when it was taken out, early reviewers felt unanchored without even a rough number" (L58).
  - The cleanliness score "should be taken as a broad pointer … rather than something precise" (L60).
- **Unit drift inside the essay.** L50 says "neuron *poles*". L1175, under the papers gallery, says "about 90% of *neurons* having basically one job". Poles and neurons are different denominators. A SwiGLU neuron with a clean "capital cities" positive pole and a clean Santa negative pole (L1089) counts as two clean poles but one two-job neuron. The essay never reconciles the two.
- **Model drift.** L50 claims Qwen3-32B. The 1,000-paper gallery is half Qwen3-32B and half Qwen3.6-35B-A3B (L1158–1163; papers-analyst §0). The essay never says the 90% was computed from these 1,000 papers.
- **My recount of the released judge scores** (`neuron-papers.json`, field `c`, 1–10; tooltip: "do each pole's strongest firings come down to one idea?"):
  - c ≥ 5 / c 3–4 / c ≤ 2 → **89.2% / 7.4% / 3.4%** overall; dense 89.6 / 8.2 / 2.2. This numerically *matches* 90 / 7 / 2–4.
  - c ≥ 6 → 80.1%. c ≥ 7 → **47.4%**. c ≥ 8 → 29.3%. c ≤ 4 → 10.8%.
  - Conclusion: the judge score is a different instrument. Depending on where "one main job" is cut, the same data gives 47% to 89%. It can neither confirm nor refute the 90%. Anyone citing a single number from it is choosing a cutoff.
- **What is missing:** a rubric, blinding, inter-rater agreement, confidence intervals, and a held-out predictive metric. The methods paper is unpublished; it is not on https://www.goodfire.com/research as of 2026-10-15 (checked).
- **Prior caution.** Huang et al. 2023 (arXiv 2309.10312, verified in the HTML) found that for GPT-2 XL, even among "the top 0.6% of neurons which are considered well-explained by GPT-4's own assessment", explanations had "a precision of 0.64 and a recall of 0.50". LLM-judged "explained" has been badly miscalibrated before. The essay argues those tools were weak (L67), which is plausible but not yet shown at population scale.
- **Why not "contested":** the near-miss test (C10) gives real, pre-registered support that most explanations are specific. Nobody has published a counter-measurement yet. It is day 0: HN is at 122 points and 32 comments with no expert rebuttal, and LessWrong has one substantive skeptical comment (ajskateboarder: "still seems underdetermined that networks can just be cleanly broken into neuron circuits and not higher-rank components").

### C2. "Closer to 97%": unsupported
L58: "In the sets I've looked at more closely, considering strong activations, it's closer to 97% non-arbitrary mixtures, but these are relatively small samples." No n, no sampling method and no data are given. Do not cite it.

### C3. "Up to trillions of parameters": overclaimed
- Subtitle (L7, confirmed live): "We can now understand most neurons in models up to trillions of parameters".
- L60: "We found similar results in models up to trillions of parameters, like Kimi K3, which the companion paper will cover".
- **Contradiction:** L1091 (confirmed live): "We haven't begun full audits of this scale yet, and hope to soon, but so far most things have been intuitively interpretable."
- The only trillion-scale evidence shown is one attribution graph, described as "a hand-picked slice of the graph: most of its weight is in late neurons at the answer that aren't drawn" (L1118). It has one single-neuron ablation, P(return) 0.83 → 0.98 (L1114).
- An unaudited impression plus one curated graph does not support "understand most neurons".

### C4. "Polysemanticity was mostly a microscope error": overclaimed (our phrasing, not the essay's)
- The essay's thesis is "several ordinary, mostly fixable issues" (L7): weak tools, architectures that learned poorly, and a noun bias (read-1 §1).
- L245, verbatim: "But it wasn't all the microscope. The model needed to be tuned too."
- In the only quantified ladder (L271), better tools on the *same* 2014 weights take the last layer from ~5% to ~50%. Retraining with modern regularization gives ~70%. A different architecture gives ~99%.
- So for vision, roughly half the reported gain comes from changing the *model*, not the microscope.
- For LMs the tool share is larger. GPT-2 XL went from <2% to ~70% "roughly one thing" on the same model (L1292), but with different scoring.
- **Safe phrasing:** "much apparent polysemanticity came from weak tools and badly-learning architectures".

### C5. The canonical examples were misread: plausible but preliminary
- **Cat/car neuron 4e:55 as a "V-shape" detector:**
  - Supported by its circuit (fox snout, wolf face and van front inputs; flames and martini-glass readers) and by curated positive and negative images (L106–160).
  - Dogs appear on both poles, which favors shape over class.
  - But the insight came after "a few seconds" (L106). There is no synthetic V-vs-O stimulus test, no dose-response, and no quantitative ablation (read-1 §4).
- **The car→dog "superposition" circuit as generalized pose:**
  - "nothing reads that combination" (L44) is asserted without downstream weight magnitudes.
  - ">100 pose neurons" (L167) are not listed.
- **Credibility:** the author co-wrote the originals (Zoom In) and is reversing himself publicly (L65). That raises credibility, but it is the same fast-intuition process he says produced the original misreading (L162 fn 3).

### C6. InceptionV1 5% → 50% → 70% → 99%: plausible but preliminary
- Verbatim (L271): "I put it around 5% with tools of that era, others at ~0% … more like 50% on the same network … Retraining the same architecture with more reasonable modern regularization it's more like 70%. In the ConvNeXt of the same size, it's about 99%."
- **Caveats:**
  - **The 99% is not InceptionV1.** It is a parameter-matched ConvNeXt with residual connections and LayerNorm (L253). The figure shows two sizes, 7.06M and 28.6M. "InceptionV1 → 99%" is therefore a misstatement. "Same parameter count and data, modern architecture → ~99%" is correct.
  - L41 says "99-100%", while L271 says "about 99%".
  - "5%" is a recollection: "I'd have maybe said 5%" (L245).
  - "Easily interpretable" is never defined. I grepped the essay for "rubric", "rater", "blind" and "agreement": none relates to the vision percentages. The only "rubric" hit is the Anthropic 2023 citation at L47.
  - The last layer of an ImageNet classifier should be nearly class detectors (Ladybugs, Terriers), so 99% there is the easy case. The meaningful result is the *contrast* with InceptionV1 (read-1 §4).
- **What makes it more than anecdote:** an explorable site is claimed. Vision is also the essay's most quantitative domain: SAE last-layer activity is 88% near-copies of single neurons (L815), plus squeeze experiments and weak-activation ablation tables (scout-reception §5).

### C7. "Recursive generalization, not superposition": contested
- **Narrow definition.** "We keep the word and say exactly what we mean: neurons learning unrelated things together because they rarely interfere" (L1547). The "more features than dimensions" sense is "basically not bad news" (L389). Distributed computation over thousands of neurons is "a real concern, but it's different" (L2361). The broad sense that motivated SAEs is set aside, not refuted (scout-reception C1).
- **Evidence is mostly qualitative:**
  - The iy → diy → "do it yourself" example (L62).
  - In vision: "This is true of every neuron I looked at" (L277), with no count.
  - Training-dynamics observations.
  - A toy model in Appendix B (read-7).
- **The distant-concept test is low-power against superposition.** Superposition predicts a neuron packs a *specific* unrelated feature Y. An agent picking "the most distant concept it could" almost never picks that Y, so both hypotheses predict near-zero firing. The essay concedes "this isn't exactly the same as what superposition would do" (L2052). Read-6 §4.1 reached the same conclusion independently. The "about 1%, 179 of 183 never fired" result rules out "fires on anything" neurons, not targeted packing.
- **Unfalsifiability risk.** Multi-hop "adjacent territory" chains can link almost anything after the fact (read-2 §4.1; read-1 §4).
- **Counter-literature** (scout-reception C4–C6; I did not re-verify these):
  - Scaling Monosemanticity found neurons "significantly less interpretable" than SAE features in Claude 3 Sonnet.
  - Circuit Tracing found transcoders beat thresholded neurons on interpretability evals.
  - Adler & Shavit show computation in superposition is theoretically cheap.
  - Counter-counter: Bhagat et al. 2026 weaken the main toy evidence for computation in superposition.
- **The author's own calibration:** "We're maybe 85% sure, but that means 85% sure that nearly everything comes from the second kind of process" (L2403). A ~15% self-assessed chance of being wrong about the core thesis is the opposite of "proved".

### C8. "Far more interpretable than 2023": plausible but preliminary
- **Baselines verified:**
  - Towards Monosemanticity: "The median neuron scored 0 on our rubric" (quoted in a LessWrong comment; the "out of 14" range is not confirmed by that text).
  - OpenAI 2023: the public headline is ">1,000 neurons" scoring ≥0.8 out of 307,200 GPT-2 XL neurons, about 0.3% (search summary; openai.com returned 403). The essay's "about 1.7% … by our most generous measure" (L48) is plausible from an author of that paper, but I could not reproduce it from public text.
- **Not like-for-like:**
  - A one-layer, 512-neuron toy and GPT-2 XL vs Qwen3-32B.
  - Neurons vs poles.
  - Simulation scoring vs agent judgment.
- **The essay's own like-for-like redo** (same GPT-2 XL, new tools; L1292): "about 70% look like roughly one thing … pristine ones are still low, about 5% … The scoring isn't identical to the original project."
- **Takeaway:** "~2% → ~70% on the same old model with better tools" is the most defensible like-for-like figure, and even that is self-scored.

### C9. Neuron-only attribution graphs and the four ablation case studies: well-supported (narrowly)
- **Numbers with matched-random controls** (random = "removes as many neurons from the same layers"):
  - Scar 0.24 vs 0.91 (L1061).
  - Santa 0.059 vs 0.997 (L1067). Removing the 20 neurons *labeled* Christmas/Santa only drops it to 76% (L1089), a strong label-vs-mechanism control.
  - Hedge 0.23 vs 0.76 (L1073).
  - Anna 0.92 vs 0.66 (L1079).
- **Caveats:**
  - They are "graphs we liked" (L963). Intact (unablated) probabilities are mostly not given.
  - **The sycophancy case, the most control-relevant, has the weakest separation.** A random 25-neuron ablation already pushes P(Anna) to 0.66 when the intact model says "not Anna", so the behavior is fragile to *any* ablation.
  - The attribution rule is unspecified (read-4 §3.1).
  - "No reconstruction error" is true of the *model*, but attribution graphs are still linearized approximations with pruning.
  - "Agents review[ed] 100,000 attribution graphs" (L2001) is explicitly "qualitative evidence—I don't trust our current tools enough to turn it into a cleanliness score". L81 says "hundreds of thousands" (for conv nets), a minor inconsistency.

### C10. "Explanations that could lose": well-supported (as a specificity test)
- L2007: "For 200 random neurons from our gallery … Among the 183 whose explanations describe their positive side, the new examples fired their neurons strongly 76% of the time; the near misses, 11%. The explanation won for 164, tied for 15 and lost for 4." Tests were written before measurement, and "strong" means ≥30% of the corpus maximum (L2048 caption).
- This is the best population-level evidence in the essay.
- **Limits:**
  - It tests the positive side only.
  - The agents and measurements come from the same team.
  - It shows specificity, not completeness.
  - The distant-concept half is low-power (C7).
- **Control-relevant:** an 11% strong-firing rate on near misses per example is far above the 1–2% audit budgets used in control games. Clean explanations do not automatically give a low false-positive monitor.

### C11. Weak activations don't matter in LLMs: contested
L1853: "We don't yet have a semantic test for weak activations that we trust … these spot checks cannot establish what weak activations mean in general." The LLM evidence is one "enemy" neuron plus spot checks; the quantitative tables are vision-only (scout-reception C4). Superposition theory predicts interference in exactly this regime. It also matters for subtle sabotage, which may hinge on near-tie decisions (read-3 H12).

### C12. "Deception … has no reason to hide from the model's own circuitry": overclaimed (for control)
- L1496 is an argument from how the network naturally works.
- **Neural Chameleons** (McGuinness, Serrano, Bailey, Emmons; arXiv 2512.11949; abstract verified):
  - "finetuning can create Neural Chameleons: models capable of zero-shot evading activation monitors".
  - It evades "previously unseen safety monitors", including "monitors trained post hoc on the model's frozen weights".
  - Tested on Llama, Gemma and Qwen.
- Bailey et al. (arXiv 2412.09565) show obfuscated activations bypass probes and SAEs (scout-reception; not re-verified by me).
- These attack *probes*. Nobody has tested whether a neuron- or circuit-level monitor is more robust. The essay contains no adversarial experiment (read-1 §4; read-4 §4.14).
- In AI control the untrusted model is assumed adversarial, so this sentence must not be imported into our framing as a premise. It is the hypothesis our experiment would test.

### C13. Quality of the 1,000 neuron-papers pipeline: plausible but preliminary
**Recounted by me:** c distribution, f distribution, zero safety keyword hits, 18 silent MoE lists. **Taken from papers-analyst:** the rest.
- **Positives:**
  - MoE tests are extremely selective (median best-control/peak 0.000).
  - Dense median is 0.108 (ratio ~9×).
  - Many curated neurons separate positives from controls by 10–100×.
  - Some safety-adjacent neurons exist, e.g. L17_E37_N173 "words the source never said" and L41_N18391 "tracks the model's doubt, not the truth".
- **Negatives:**
  - Judge clean score vs measured control leakage: Spearman ≈ −0.04. The judge's notion of "clean" does not predict false positives.
  - Silent tests: 18 MoE lists have every test at |act| < 0.5. Of these, 10 were scored c ≥ 6 and 6 were scored c ≤ 2, so the judge is *inconsistent* rather than uniformly fooled. The dead layer-0 neuron L0_E11_N16 got c=8.
  - Leaky controls: in 17.7% of dense lists a control reaches ≥50% of peak. Sometimes a control is the top entry: L26_N20030, L56_N2209, and L57_N6278, whose lede contradicts its numbers.
  - "Chosen randomly" (L1158), but 73% of the dense sample comes from the deeper half (χ² p ≈ 2e-25). That bias slightly *lowers* the clean rate, so it is a provenance flag, not inflation.
  - **Zero** papers mention deceive/deception, honest(y), refus(al), jailbreak, backdoor, sabotage or sycophancy in title or lede (reconfirmed by me).
  - Late dense layers are the least clean: c ≤ 4 in 15.4% at L51–63, vs 1.9–5% at L0–24.

### C14. Bigger means narrower, cleaner neurons, so monitors scale: preliminary / unsupported
- **The first half is supported by:**
  - The vision scale sweep (1/75× to 12×, L185–202).
  - "smaller models have broader neurons" (L1292).
  - Gurnee 2023: sparsity increases with scale (scout-reception §5).
- **Tension:** in the released data, deeper dense layers, where abstract concepts live, are judged *less* clean.
- **The second half is ours, not the essay's** (read-1 H8; feed read-1-core-thesis-5). "White-box monitors improve with scale while black-box ones degrade" is untested.
- **Budget implication:** if we downsize from Qwen3-32B to a smaller model to save money, the essay itself predicts broader, messier neurons. The 90% claim would not transfer.

### C15. MoE is anti-superposition; SwiGLU echo: plausible but preliminary
- **MoE:**
  - Independent papers agree (Chaudhari et al. 2510.23671; Herbst et al. 2604.02178; scout-reception verified via abstracts).
  - The released MoE tests are very selective.
  - The router argument (L1243) is a heuristic, not a proof.
- **SwiGLU echo:**
  - The worked example is strong: L1/N20736, "Colossians", is really "Russia/Russian" on its negative pole (L1195–1233).
  - "About 4% of neurons" has no stated method.
  - "Ablating them … ups most benchmarks, but lowers some reasoning ones" has no numbers (L1179).

---

## 3. Where OUR notes and feed overstate the essay (or the evidence)

1. **"Our recount: about 80% clean, not 90%"** (`feed/meaning-and-questions-4.json`) and **"No threshold reproduces 90 / 7 / 2–4"** (papers-analyst §1, §4.1).
   - This is false as stated. c ≥ 5 / 3–4 / ≤ 2 gives **89.2 / 7.4 / 3.4** (dense 89.6 / 8.2 / 2.2).
   - Correct version: "the judge's 1–10 score is a different instrument; depending on cutoff it yields 47–89% 'clean', so it neither confirms nor refutes the essay's 90%."
2. **"Same old vision model's last layer: 5% readable, then 99% with fixes"** (`feed/read-1-core-thesis-3.json`), and the "InceptionV1 5%→70%→99%" shorthand used in our task framing.
   - The 99% is a *different architecture* (parameter-matched ConvNeXt), and "5%" is a recollection.
   - Correct version: same InceptionV1 weights 5% → 50% with better tools; retrained InceptionV1 70%; same-size ConvNeXt 99%.
3. **"Polysemanticity was mostly a microscope error"** (our framing).
   - The essay says tools *and* architecture *and* noun bias (L7, L245).
4. **read-4 §1 point 2 and C13 ("The basis is 1,000 random neuron papers") present the 90% as computed from the gallery.**
   - The essay never says so. L50 cites "preliminary audits of Qwen3-32B". The gallery mixes two models. L1175 switches from poles to neurons.
   - Treat the link between the gallery and the 90% as unknown.
5. **read-1 H1, "Native neurons as a free, zero-reconstruction-error monitor vocabulary", and read-4 hook 5, "With neurons there is no unexplained residual term … only unexplained neurons, which can be enumerated".**
   - **Not free.** Labeling ~1.6M dense or ~5M MoE neurons needs agent-hours, and every monitor neuron needs its own validation.
   - **The unexplained part is large.** It includes the 2–4% not understood (tens of thousands of neurons), the ~7% with two jobs, the SwiGLU −×− regime, attention, the residual stream and weak activations. An adversary can hide there.
   - **Graphs are still approximate.** Attribution graphs are still linearized and pruned.
6. **read-4 §7, "four small, ablation-validated circuits … with large effects against matched random controls", and C8 rated "Strong. This is the most control-relevant case."**
   - The sycophancy case is the *weakest* separation (0.92 vs random 0.66, intact value unstated). All four are curated.
7. **`feed/scout-whitebox-monitors-3.json`, "Brain-reading guard is already live, catching 93% of hacking sessions cheaply".**
   - It is a probe → LLM-judge *cascade* for cyber **misuse** by humans. It is not a neuron-level monitor, not derived from this essay, and not a scheming-AI control setting.
   - The numbers are self-reported.
   - The scout's own note says press figures conflict (93% / 5.5% vs 94% / 8.7%) and the primary post gives 91–96% blocking with 9–15% interruption in some settings.
   - "Hacking sessions" can be misread as model reward hacking.
8. **`feed/read-4-language-models-1.json`, "In a big chatbot brain, about 90% of neuron sides have one clear job".**
   - The headline drops "estimate / preliminary / threshold-dependent", which carry the claim's whole epistemic status.
9. **`feed/read-1-core-thesis-5.json` and read-1 H8 (neuron monitors may improve with scale).**
   - It is hedged ("may"), but it rests on a vision-only scale claim.
   - It ignores the released data showing late dense layers are least clean.
   - Label it as our hypothesis, not a finding.
10. **papers-analyst §2, "The judge rewards clear writing even when the measurements are empty."**
    - Partly overstated. Of the 18 silent MoE lists, 6 were scored c ≤ 2, so the judge often *did* penalize them; 10 got c ≥ 6.
    - Better: "the judge is inconsistent on empty evidence".
11. **scout-whitebox-monitors (lines 20, 210, 270), "could not find any source for 'already clean'".**
    - Stale. The essay is live at https://already-clean.goodfire.com/ with the byline "Nick Cammarata · Goodfire" (verified 2026-10-15). It is also linkposted on LessWrong and HN.
    - Any downstream note that treats the essay as unverifiable should be corrected.
12. **The project goal, "prove mechanistic interpretability is a viable alternative".**
    - *Linear probes* already beat black-box monitors in published settings, e.g. sandbagging probes at 97–99% AUROC vs a CoT monitor at 74% (scout-whitebox-monitors). So "white-box can beat black-box" is not new.
    - What would be new is **neuron-level, essay-style monitors**, ideally with an adversarial-robustness test.
    - With $20–$100 we can show a bounded, setting-specific result. We cannot prove general viability.

---

## 4. Safe vs unsafe phrasings for our write-ups

| Unsafe (do not write) | Safe (write this instead) |
|---|---|
| "90% of neurons are clean" | "The author estimates, preliminarily, that ~90% of Qwen3-32B neuron *poles* have one main job; the method is not yet published." |
| "Works up to trillions of parameters" | "One hand-picked neuron attribution graph is shown for a multi-trillion-parameter model; full audits at that scale have not begun (L1091)." |
| "InceptionV1 went from 5% to 99%" | "InceptionV1's last layer went from ~5% to ~50% readable with better tools; a same-size modern ConvNeXt reaches ~99% (author-judged)." |
| "Superposition is wrong" | "The essay argues the narrow 'arbitrary packing' sense of superposition is rare in the models it studied; the author is ~85% confident." |
| "Deception can't hide from circuits" | "Whether neuron-level monitors resist trained evasion better than linear probes is untested; probes are known to be evadable." |
| "Neuron monitors are free and exact" | "Neuron monitors read activations the model already computes, but each monitor neuron needs labeling and false-positive validation; near misses fire strongly ~11% of the time." |
| "Our recount shows only 80%" | "The released judge scores give 47–89% 'clean' depending on cutoff; they neither confirm nor refute the 90%." |

---

## 5. Sources

**Essay and local data:**
- Essay (live): https://already-clean.goodfire.com/
- Local copy: `source/already-clean.txt`. Lines cited: 7, 41, 44, 47–48, 50, 58, 60, 62, 81, 96, 106, 162, 167, 245, 253, 271, 277, 385–389, 815, 963, 1061–1089, 1091, 1114, 1118, 1158–1179, 1195–1233, 1243, 1292, 1496, 1547, 1853, 2001, 2007, 2048–2052, 2227, 2361, 2403.
- Released papers: `source/neuron-papers.json` (my recount: `check.py`, `check2.py` in the scratchpad).

**Our notes:** `research/read-1-core-thesis.md`, `read-4-language-models.md`, `papers-analyst.md`, `scout-reception-critics.md`, `read-2`, `read-3`, `read-6`, `read-7`, `scout-whitebox-monitors.md`, `scout-control-benchmarks.md`. Feed: `feed/*.json`.

**Reception:**
- https://news.ycombinator.com/item?id=50105647 (122 points, 32 comments at check time)
- https://www.greaterwrong.com/posts/x4kvabkF2Jk8GLZp8/linkpost-neural-networks-are-already-clean

**Literature:**
- Huang et al. 2023: https://arxiv.org/html/2309.10312v1 (precision 0.64 / recall 0.50 for the top 0.6% of neurons)
- Towards Monosemanticity median-0 quote: https://www.greaterwrong.com/posts/TDqvQFks6TWutJEKu/towards-monosemanticity-decomposing-language-models-with
- OpenAI 2023 autointerp (">1,000 neurons ≥0.8", via search summary): https://openai.com/index/language-models-can-explain-neurons-in-language-models/
- Neural Chameleons: https://arxiv.org/abs/2512.11949
- Goodfire research index (no companion paper listed as of 2026-10-15): https://www.goodfire.com/research
