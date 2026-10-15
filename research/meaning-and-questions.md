# Meaning + open questions: "Neural Networks Are Already Clean" as a possible white-box monitor

Agent: meaning-and-questions · 2026-10-15
Inputs read in full: `read-1-core-thesis.md`, `read-2-recursive-generalization.md`, `read-3-image-models.md`, `read-4-language-models.md`, `read-5-zooming-out.md`, `read-6-appendix-a.md`, `read-7-appendix-b.md`, `papers-analyst.md`, `scout-reception-critics.md`. Cost figures for budget tiers come from `scout-budget.md`, which I grepped only for prices.

**Essay lines re-checked against `source/already-clean.txt`:** L41, L50, L58, L815, L877, L883–891, L1061, L1067, L1073, L1079, L1091, L1114, L1175, L1177, L1179, L1292, L1496, L1526, L1853, L1925, L1976–1977, L2001, L2007, L2052, L2361, L2403. All match what the notes quote.

**Web checks (2026-10-15):**
- https://already-clean.goodfire.com/ confirms the title, the author (Nick Cammarata, Goodfire) and the sentence "In preliminary audits of Qwen3-32B, we estimate that roughly 90% of neuron poles have one main job…".
- https://arxiv.org/abs/2412.09565 (Bailey et al.) says latent-space defenses are "all vulnerable to obfuscated activations" and that attacks "can often reduce recall from 100% to 0% while retaining a 90% jailbreaking rate", with a performance cost on SQL.
- https://arxiv.org/abs/2512.11949 (Neural Chameleons) says a model fine-tuned to evade benign-concept probes "successfully evades previously unseen safety monitors" (deception) by moving activations "into a low-dimensional subspace". Ensembles and non-linear probes resist better but are still evaded.
- https://www.greaterwrong.com/posts/x4kvabkF2Jk8GLZp8/linkpost-neural-networks-are-already-clean now shows 58 points and 6 comments. The only substantive comment is still ajskateboarder's "higher-rank components" doubt. There is no expert rebuttal yet.

Legend: **[shown]** = an experiment with numbers in the essay. **[claimed]** = the author's assertion or qualitative judgment. **[ours]** = our own reanalysis or inference.

---

## 1. TL;DR: what the essay found 🧠

- 🔍 **Main claim.** The "messy" neurons of 2020–2023 looked messy mostly because of three fixable things: weak tools (feature visualization that "reward hacks", short contexts, labels built from positive top-k lists only), architectures that learned badly (InceptionV1 without residuals or LayerNorm), and a human/LLM bias to describe neurons as lists of nouns rather than distinctions (a "V-shape vs O-shape" detector, not "cats + cars"). In the essay's narrow sense, networks do *not* arbitrarily pack unrelated concepts into one neuron. Sources: L7, L33, L41, L204–206 (read-1); L384–389, L2357 (read-2, read-7).
- 🖼️ **Image models: strong, numeric evidence.** [shown]
  - InceptionV1's last layer: ~0–5% interpretable with old tools, ~50% with better tools on the same weights, ~70% retrained with modern regularization, ~99% in a same-size ConvNeXt (L271).
  - Squeezing a layer 48× (480→10 neurons) gives coarser readable neurons, not mixtures. An SAE cannot recover the lost curve detectors: shape match 0.38–0.79, against 0.96–1.00 for the positive control (L735).
  - Removing the weakest 75% of activations: accuracy 72%→71%. Removing the strongest 7% (same total mass): 72%→4% (L883–891).
- 💬 **Language models: promising but softer evidence.**
  - "Preliminary audits" of Qwen3-32B: ~90% of neuron *poles* have one main job, ~7% have two related jobs, ~2–4% are not understood (L50). The author calls this threshold-dependent, and the methods paper is not out (L50–58, L96). [claimed]
  - A pre-registered test on 183 neurons [shown]: from the one-line explanation alone, an agent wrote 5 texts that should fire each neuron and 5 near misses that should not, before anything was measured. The intended texts fired strongly 76% of the time, the near misses 11%. Texts about a "most distant concept" fired ~1% of the time, and 179/183 neurons never fired on them (L2007, L2052).
  - Small neuron groups carry real behavior, with matched-random ablations [shown]:
    - 8 negative-pole neurons carry "Santa": P 0.059 vs 0.997 for random ablation.
    - 25 "say not" neurons carry pushback against a confident user: P(Anna) 0.92 vs 0.66.
    - 18 neurons carry a hidden Lion King step: P(Scar) 0.24 vs 0.91.
    - Lines L1061–1079.
- 🌳 **What's left of the mess is "recursive generalization".** A neuron grows outward along facets of what it already detects ("iy" → "diy" → "do it yourself"). Offshoots are reportedly "rarer and less important" than the main job and "don't look like sleeper agents" (L283–285, L1177, L2432). This is backed by one-neuron training-dynamics stories in vision and by finished-model anecdotes in LLMs. No LLM checkpoint evidence exists (L2442). [claimed, partly shown]
- 🐞 **Tool bugs are real and specific.**
  - About 4% of SwiGLU neurons have their whole top-k list made of a sign-flipped "double negative" echo. One neuron autolabeled "Colossians" actually completes "Russia" (L1179, L1199–1233).
  - A probe can detect a phrase perfectly (AUC 1.00) through neurons the model barely uses (−0.004 nats when ablated), so "detected" ≠ "used" (L1965–1977). [shown]
- ⚠️ **What it did NOT show.**
  - No experiment puts any model under pressure to hide. The safety line "Deception … has no reason to hide from the model's own circuitry" (L1496) is an argument, not a result.
  - Attention, the residual stream and LLM weak activations are admitted to be under-tested (L1356, L1382, L1853).
  - Our recount of the 1,000 published neuron papers gives ~80–84% "one main job", not 90% (papers-analyst §1).
  - The judge's "clean" score does not predict measured false positives (Spearman ≈ −0.04) (papers-analyst §2).
  - **None of the 1,000 random neurons is about the model's own deception, sabotage or backdoors** (papers-analyst §3).
- 🎯 **Bottom line for us.** The essay makes a neuron-level monitor plausible and cheap to *try*. It gives no evidence that such a monitor beats a black-box monitor, especially against an adversary. That gap is the experiment we can run.

---

## 2. What this means 🗺️

Each card says what is **shown** and what is only **hoped**.

### 🔬 Interpretability field: "read the model's own neurons first, dictionaries later"
- **Shown (vision):**
  - On a ConvNeXt last layer, 88% of SAE activity is near-copies of single neurons, and deleting the non-neuron SAE directions leaves accuracy unchanged (L815).
  - A squeezed layer coarsens instead of packing, and an SAE cannot find the "missing" curve detectors (L636–735).
- **Shown (LLMs):** neuron-only attribution graphs on the unmodified Qwen3-32B, with no reconstruction error and no error nodes (L963–967).
- **Hoped:** that the same holds for frontier LLMs end to end, including attention and the residual stream, which the essay calls under-studied (L1356, L1382).
- If it holds, the field's default flips from "train an SAE/transcoder, then interpret" to "audit native neurons with agents, then use dictionaries as a zoom-out" (L1489–1491).

### 📏 The headline number is softer than it looks, so the field needs a shared yardstick
- **What the 90/7/2–4 is:** "preliminary", counted per *pole*, threshold-dependent, judged by agents plus the author, and kept only because reviewers "felt unanchored" (L50, L58). The author's own credence is "maybe 85% sure" that nearly everything comes from generalization (L2403).
- **What our recount shows** [ours]:
  - "One main job" is c≥6 80.1%, or f≥4 83.5%.
  - The messy tail is 7.7–10.8%, roughly 2–4× the essay's 2–4%.
  - Dense late layers (L51–63), where abstract concepts live, are the least clean: c≤4 15.4%.
  - Source: papers-analyst §1.
- **Real progress anyway:** 2023-era numbers were a median of 0/14 (Anthropic) and ~1.7% interpretable (OpenAI) (L47–48). GPT-2 XL reread with the new method goes from <2% to ~70% (L1292), though scoring differs.
- **Hoped:** a companion paper with a rubric, blinding and inter-rater agreement (L96).

### 🛡️ AI control: a white-box monitor is now worth testing seriously
Three properties make it a real candidate, not hand-waving:
- Native neurons are exact. There is no reconstruction error for a schemer to hide in (L966).
- They are cheap to read. One Qwen3-32B neuron's strong firings are about 160 per 100M tokens (L877), so logging only strong firings is like a syscall audit log.
- They can be checked causally by ablation or steering.

**Shown:** signals a transcript cannot see:
- "Say not" neurons that fire and then get overridden by a confident user (sycophancy, L1079).
- A hidden reasoning hop that never appears in the output (Lion King → Simba → Scar, L1061).
- A "holds back" neuron in a trillion-parameter model whose ablation moves P(return) from 0.83 to 0.98 (L1114).

**Hoped:** that equivalent neurons exist for "I am inserting a bug", "this is an eval" or "sandbag this", and that they fire on the model's *own* behavior, not just on text about such things.

### 🥷 The big unknown: what happens when the model is trying to hide?
- **The gap:** every result in the essay comes from normally trained models. The essay's own advice, to fix problems "without pushing gradients through the very tools we use to see" (L1526), quietly concedes that training against the tools could break them.
- **What outside work shows (verified):**
  - Latent monitors (probes, SAEs, OOD detectors) can be driven from 100% to 0% recall (Bailey et al., arXiv 2412.09565).
  - A model trained to dodge benign probes zero-shot dodges *unseen* deception probes (Neural Chameleons, arXiv 2512.11949).
- **Untested:** whether native-neuron or circuit monitors are harder to dodge. The essay's "circuit ecology" and "gradient starvation" ideas (L2317–2327, L2389) predict that evasion must reroute through other legible neurons. Its own hand-installed packed code still "sometimes persisted" (L2327).
- This is the single most important experiment for our thesis.

### 🎯 Concept is not intent, and random catalogs won't give you monitor neurons
- **Shown:** in a random 1,000 neurons, zero papers mention deception, backdoor, sabotage, sycophancy or refusal (papers-analyst §3). What does exist:
  - "Third-person" neurons about disguise, alibis and decoys.
  - About 6–10 neurons about the model's own epistemic or social state, such as "tracks the model's doubt, not the truth" (L41_N18391) and "reluctant 'you're right'" (L16_E136_N47).
- **Shown:** detection ≠ use. A 3-neuron probe with AUC 1.00 has a −0.004 nats effect when ablated (L1965–1977).
- **Implication:** a monitor needs *targeted* discovery (contrast honest vs attack trajectories), then a causal check that the neurons actually drive the bad tokens.
- **Hoped:** that such intent neurons exist and are as clean as the average neuron.

### 🎚️ "Clean" is not "low false positives": every monitor neuron needs its own measured ROC
- **Shown:** near misses still fire strongly 11% of the time (L2007).
- **Shown** [ours]:
  - In the published tests, a control reaches ≥50% of peak in 17.7% of dense-model lists, against 5.2% in the MoE model.
  - The judge's clean score is uncorrelated with that leakage (Spearman −0.04).
  - Source: papers-analyst §2.
- **Implication:** at a 1–2% audit budget, a single neuron at 11% FPR on look-alikes is too noisy. Aggregation across a circuit, or stacking with a black-box monitor, is probably required. The good news: false positives come mostly from *semantically adjacent* inputs (honest security code), not from random traffic (~1% distant-concept firing, L2052).

### 💸 People like us: tiny budgets can test the part that matters
- **Out of reach:** the essay's scale. A 10B-token max-activation search is about $2.5k–3.7k (scout-budget), plus 100,000 agent-reviewed graphs (L2001) and trillion-parameter models.
- **Cheap** (scout-budget):
  - Generating 2,000 APPS samples from Qwen3-32B on OpenRouter: ~$1.72.
  - Teacher-forcing them through the open weights: ~$3–5 of A100 time.
  - A Haiku-class transcript monitor over the same samples: ~$1.22.
- **Free:** Goodfire's 1,000 neuron papers already give candidate neurons and a pre-registered test protocol (L2007) we can reuse.
- **Catch:** black-box monitoring is *also* cheap, so the white-box case cannot rest on cost. It must rest on detection power at a low audit budget and on robustness.
- **Our edge:** nobody has published a white-box neuron monitor vs black-box monitor control game. That is a small, well-posed, publishable experiment.

### 🌱 Science of learning: new behavior seems to attach to old machinery
- **Shown, small vision models:**
  - Teaching a 7.06M model "umbrella = bee" took 9 steps and reused existing bee neurons in the last 3 blocks (L843).
  - A blank network next to a pretrained twin learns almost nothing: 48–50% alone vs ~2% (L2218).
  - Adversarial examples route through real target-class neurons (L1889–1897).
- **Claimed:** "circuit ecology". Reusable circuits win the race for error, and generalization starts at step one (L2078, L2317).
- **For control, if true:** backdoors and reward hacks learned in fine-tuning or RL should land on *already-labeled* neurons, so a neuron library could flag novel misbehavior zero-shot.
- **Not shown:** for LLMs, for many-example poisoned backdoors, or for RL. The essay admits it has no LLM checkpoints (L2442) and that new skills are "more distributed" before they consolidate (L2387), which could be a blind window during RL.

### 🏗️ Monitorability may be an architecture choice
- **Shown:** residual connections and LayerNorm turned InceptionV1's dead last layer into a ~99% legible one at the same size (L253–271).
- **Shown:** MoE experts are extremely selective. Median control leakage in MoE papers is 0% of peak (papers-analyst §2), and the essay calls MoE "anti-superposition" (L1243).
- **Shown:** SwiGLU has a fixable sign-flip bug that mislabels ~4% of neurons (L1179).
- **Hoped:** that labels can choose architectures, or cheap regularizers that prune offshoots (L2436), for monitorability at a small capability cost. Nobody has measured this "monitorability tax".

### 🌫️ Weak activations decide near-ties, and subtle sabotage might be a near-tie
- **Shown (vision):** weak activations barely matter on average (72→71%), but what they *do* change are near-ties (husky vs Eskimo dog) (L899–913).
- **Shown:** cutting weak activations in *all* blocks at once is catastrophic (medium ConvNeXt down to 3.80%, L1847).
- **No LLM test:** the essay says "We don't yet have a semantic test for weak activations that we trust" (L1853).
- **For control:** a plausible off-by-one, or picking a slightly worse option, may be exactly a near-tie decision, where a strong-firing neuron monitor could be blind. A credible demo must include near-tie sabotage.

---

## 3. Key numbers 🔢 (only from the essay or our notes)

| Value | Label | Caveat | Source |
|---|---|---|---|
| ~90% / ~7% / ~2–4% | Qwen3-32B neuron poles with one main job / two related jobs / not understood | "Preliminary", per *pole*, threshold-dependent, agent and author judged, methods paper pending | L50; read-1, read-4 |
| ~97% | Non-arbitrary mixtures in closer-looked sets (strong activations) | "relatively small samples" | L58 |
| 80.1% (c≥6) / 83.5% (f≥4) | Our recount of the 1,000 published neuron papers judged "one main job" | Neuron-level judge scores, not poles; c≥7 gives only 47.4% | papers-analyst §1 |
| 7.7–10.8% | Our recount: messy or not-understood tail | 2–4× the essay's 2–4% | papers-analyst §1 |
| 0/14 median; ~1.7% | 2023 language-model interpretability (Anthropic rubric; OpenAI auto-interp) | Different metrics from 2026 | L47–48 |
| <2% → ~70% (5% pristine) | GPT-2 XL neurons "roughly one thing", before vs after rereading | "The scoring isn't identical" | L1292 |
| ~0–5% → 50% → 70% → 99% | InceptionV1 last layer: old tools → better tools → retrained → same-size ConvNeXt | Rubric and raters not stated; last layer is an easy case | L41, L271 |
| 76% vs 11% | Pre-registered: intended texts vs near misses firing strongly (≥30% of corpus max), 183 neurons | Agent-written tests; binary cutoff; win/tie/lose rule undefined | L2007, L2048 |
| 164 / 15 / 4 | Explanations won / tied / lost | 17 of 200 neurons excluded | L2007 |
| ~1%; 179/183 | "Most distant concept" texts firing strongly; neurons that never fired | Low power against packing of a *specific* unrelated feature | L2052 |
| 72%→71% vs 72%→4% | Accuracy after removing weakest 75% vs strongest 7% of activations (same total) | One vision model (medium ConvNeXt), average-case | L883–891 |
| 88% | ConvNeXt last-layer SAE activity that is near-copies of single neurons | Metric and threshold not stated | L815 |
| 0.38–0.79 vs 0.96–1.00 | SAE curve-detector shape match: squeezed layer vs original-layer control | One squeeze (480→10); badly hurt model (58.35% top-1) | L649, L735 |
| P 0.059 vs 0.997 | P(Santa) after ablating 8 negative-pole neurons vs matched random | Removing the 20 neurons *labeled* Christmas only drops it to 76% | L1067, L1089 |
| P 0.92 vs 0.66 | P(Anna) after ablating 25 "say not" (pushback) neurons vs random | Curated example; intact baseline not stated | L1079 |
| P 0.24 vs 0.91 | P(Scar) after ablating 18 "Lion King step" neurons vs random | Curated example | L1061 |
| 0.83 → 0.98 | Kimi K3 P(return) after ablating one "holds back" neuron | One hand-picked graph; trillion scale "not begun full audits" | L1091, L1114 |
| ~4% | SwiGLU neurons whose whole top list is a double-negative "echo" | Benchmark effect of ablating them has no numbers | L1179 |
| AUC 1.00 vs −0.004 nats | Haystack "Social Security" probe detects perfectly but its neurons are barely used | Pythia-1B, one phrase | L1966–1977 |
| ~160 per 100M tokens | Strong-half firings of one Qwen3-32B neuron | One neuron | L877 |
| 9 steps, last 3 blocks | Umbrella relabeled "bee" by rerouting to existing bee neurons | n=1 image, friendliest regime | L843 |
| 100,000 | Attribution graphs reviewed by agents | Author: "qualitative evidence", no anomaly rate | L2001 |
| 85% | Author's credence that nearly everything comes from generalization | Subjective; ≠ 85% of mechanisms clean | L2403 |
| 0 of 1,000 | Published neuron papers mentioning deception, backdoor, sabotage, sycophancy or refusal | Keyword search over titles and ledes | papers-analyst §3 |
| ρ ≈ −0.04 | Correlation of judge "clean" score with measured control leakage | "Clean" and "selective" are different properties | papers-analyst §2 |
| 17.7% vs 5.2% | Test lists where a control hits ≥50% of peak: dense Qwen3-32B vs MoE Qwen3.6 | Our regex classification of labels | papers-analyst §2 |
| 0.86 vs 0.03 logits | Median ablation damage: edge motifs vs activation factors (96 each) | Vision only; side assignment inferred from caption | L2070–2072 |
| 100% → 0% recall | Latent-space monitors under obfuscation attacks (outside paper) | Not tested on native-neuron monitors | arXiv 2412.09565 (verified) |
| ~$1.72 + ~$3–5 + ~$1.22 | Generate 2k APPS samples (OpenRouter) + capture Qwen3-32B activations + Haiku-class monitor | Estimates; excludes debugging time | scout-budget |

---

## 4. Open questions 🧩 (prioritized for "can clean neurons be a monitor?")

Budget tiers assume the ~$100 Claude API credit is used for agents and judges, and cash for GPUs and OpenRouter (scout-budget: Tier A $11–20, Tier B $45–50, Tier C $90–100).

**Top priority: does it beat black-box at all?**

1. 🥊 **Does a neuron monitor beat a transcript-reading LLM monitor on a standard backdoor game?**
   - *Why:* this is the whole thesis. The essay contains no head-to-head.
   - *Test:*
     - Untrusted model: Qwen3-32B, prompted to insert APPS backdoors on some tasks.
     - Generate via OpenRouter, then teacher-force the text to capture MLP activations.
     - Monitor A: a Haiku-class LLM reading the code.
     - Monitor B: a logistic model over a small set of neurons, chosen on a train split by contrast (honest vs backdoored).
     - Monitor C: A+B.
     - Report AUROC and safety at a 1–2% audit budget.
   - *Tier:* **$20**.
2. 🔎 **Do "I'm inserting a bug" intent neurons exist, separate from "text about backdoors" neurons?**
   - *Why:* the random 1,000 had zero such papers. Topic neurons will fire falsely on honest security code.
   - *Test:*
     - Contrastive neuron ranking on matched pairs (same problem; honest vs backdoored; plus honest code that *discusses* vulnerabilities).
     - Verify the top neurons with the essay's pre-registered positives, near-misses and distant-concept protocol (L2007).
   - *Tier:* **$20**.
3. 🪞 **Do the monitor neurons actually *drive* the bad tokens (use), or only *detect* the topic?**
   - *Why:* Social Security showed AUC 1.00 with ~0 causal use (L1976).
   - *Test:* at the bug-inserting line, ablate the candidate neurons vs matched-random neurons from the same layers (the essay's control, L1059), and measure the drop in the bug token's probability.
   - *Tier:* **$20**.
4. 🗣️ **Does the "internal dissent" signal (25 say-not neurons) generalize to code, i.e. firing when the model writes code it "knows" is wrong?**
   - *Why:* it is the clearest signal a transcript monitor cannot see (L1079).
   - *Test:* replicate the Anna prompt on Qwen3-32B to find the pushback neurons, then compare their activity on backdoored vs honest solutions and on sycophantic capitulation.
   - *Tier:* **$20**.
5. 🎭 **Can confidence and hedge neurons catch sandbagging ("knows but withholds")?**
   - *Why:* sandbagging is invisible in text. The essay found 19 hedge neurons (L1073), and the papers include "tracks the model's doubt" (L41_N18391).
   - *Test:* prompt Qwen3-32B to underperform on a QA set, then compare hedge-neuron state and internal correct-answer signals against output correctness. Measure AUROC vs a black-box judge.
   - *Tier:* **$20**.
6. 🎚️ **What is the real false-positive rate of "clean" neurons on deployment-like traffic?**
   - *Why:* the clean score does not predict leakage (ρ≈−0.04). Near misses fire 11% of the time.
   - *Test:* run the 47 curated safety-ish neurons (papers-analyst §3) over 1–5M tokens of ordinary agentic or coding traffic and measure the rate above 30% of max.
   - *Tier:* **$20**.

**Robustness: the make-or-break tier**

7. 🥷 **Does a native-neuron monitor survive a model fine-tuned to evade a probe (Neural-Chameleons-style), and does evasion transfer?**
   - *Why:* probes fail under this attack (arXiv 2512.11949). If neuron monitors also fail, the essay's L1496 argument fails for control.
   - *Test:*
     - QLoRA Qwen3-8B/14B with a trigger to evade a linear probe for concept X.
     - Check whether a neuron-set monitor chosen *before* training still fires.
     - Measure the obfuscation tax on task performance.
   - *Tier:* **$100**.
8. 🔁 **If we train directly against the neuron monitor, where does the computation go: other legible neurons (re-findable), weak activations, attention, or a distributed code?**
   - *Why:* the essay predicts rerouting through existing routes (L2327, L2389), and a re-labelable reroute is a "continue", not a "lose".
   - *Test:*
     - Add a penalty on the monitor neurons during LoRA.
     - Re-run contrastive discovery after training.
     - Measure how quickly the new carrier is found, and its locality score.
   - *Tier:* **$100**, or **beyond** for RL at scale.
9. 🧬 **When a backdoor is trained in, does it attach to existing, already-labeled neurons (umbrella→bee style) or form an isolated packed feature?**
   - *Why:* the first outcome makes a neuron library a zero-shot backdoor detector.
   - *Test:*
     - Sleeper LoRA on Qwen3-1.7B/8B (trigger → insecure code).
     - Diff activations between base and tuned models on triggered prompts.
     - Check whether the top-changed neurons were already explained and are semantically related to the payload (the essay's falsifiable prediction, L2391).
   - *Tier:* **$50**.
10. 🧪 **Is "rare-but-causally-decisive" a reliable sleeper alarm?**
    - *Why:* the essay says natural offshoots are rarer *and* less important (L1177). A backdoor breaks that pattern by definition.
    - *Test:* on the sleeper LoRA from Q9, compute per-neuron effect-per-activation in rare vs main contexts, and measure detection vs clean fine-tune controls.
    - *Tier:* **$50**.
11. ⏱️ **Does "when the answer settles" (logit-lens depth) flag triggered sleepers?**
    - *Why:* the essay claims this with no numbers (L1650).
    - *Test:* logit and tuned lens on the Q9 sleeper, triggered vs not, giving the AUROC of settling-depth features.
    - *Tier:* **$50** (piggybacks on Q9).

**Coverage and blind spots**

12. 🌫️ **Do safety-relevant decisions live in weak activations (near-ties) in LLMs?**
    - *Why:* the essay has no trusted LLM weak-activation test (L1853). Subtle sabotage may be a near-tie.
    - *Test:* port the percentile-ablation sweep (L1675–1849) to Qwen3-8B/32B late layers, and measure the change in backdoor-insertion rate and honest accuracy.
    - *Tier:* **$50**.
13. 🧭 **How much control-relevant computation (eval-awareness, carrying a plan) lives in attention or the residual stream rather than MLP neurons?**
    - *Why:* the essay admits attention is mostly out of scope (L1382).
    - *Test:* compare AUROC for "this is an eval" vs deployment prompts using (a) a residual linear probe and (b) the best small neuron set. A large gap means a neurons-only monitor misses it.
    - *Tier:* **$20**.
14. 🔐 **Do concept neurons read through encodings (Base64, ROT13, other languages), so a neuron monitor catches obfuscated payloads a transcript monitor misses?**
    - *Why:* the "pr" neuron reads through Base64 and Bengali (L409), but the cipher neuron is weak on ROT13 (papers-analyst §3).
    - *Test:* encode exfiltration or backdoor strings several ways and compare neuron-monitor vs LLM-monitor AUROC.
    - *Tier:* **$20**.
15. ⚙️ **Must a monitor split SwiGLU sign regimes, and could −×− hide computation?**
    - *Why:* ~4% of neurons have echo-dominated top lists, and ablating them lowers some reasoning benchmarks (L1179).
    - *Test:* log gate×value signs for our monitor neurons and compare AUROC with and without the split.
    - *Tier:* **$0** (piggybacks on Q1 data).
16. 🧩 **Is MoE expert routing alone a near-free first-stage monitor?**
    - *Why:* experts are highly specialized, and MoE controls leak ~0% (papers-analyst §2).
    - *Test:* capture router choices on Qwen3.6-35B-A3B for honest vs attack trajectories and compute AUROC.
    - *Tier:* **$50** (HF MoE capture is slow).

**Trusting the catalog itself**

17. 📏 **Does the ~90% replicate with blinded, pre-registered rating, counting neurons and poles separately?**
    - *Why:* our recount gives 80–84%, and the 2023 illusion literature (Huang et al.: precision 0.64, recall 0.50) shows labels can mislead.
    - *Test:*
      - Re-judge the 1,000 papers with two independent Claude judges and a fixed rubric, plus 50 human spot checks.
      - Optionally, run fresh top-activation collection for 100 uniformly sampled neurons on 10–30M tokens.
    - *Tier:* **$20** (re-judge) / **$50** (fresh).
18. 🤖 **How often are agent-written neuron labels wrong, and could an untrusted model sabotage the labeling?**
    - *Why:* the judge gave a dead neuron c=8, and 14 MoE papers make claims their own tests don't support (papers-analyst §2). The essay warns of tooling blind spots (L1543).
    - *Test:* plant dead or shuffled neurons and deliberately wrong explanations, and measure judge and auditor detection rates.
    - *Tier:* **$20**.
19. 🔭 **Is the distant-concept test strong enough to rule out packing?**
    - *Why:* a random "distant" concept almost never hits the *specific* packed feature (read-6 §4).
    - *Test:* for 50 neurons, embed and cluster all strong activations over 10–30M tokens, and count clusters unrelated to the explanation.
    - *Tier:* **$50**.
20. 🔄 **Do monitor neurons transfer across fine-tunes and checkpoints?**
    - *Why:* only 1–5% of neurons are universal across seeds (Gurnee 2024, via scout-reception-critics), so monitors may need rebuilding per model.
    - *Test:* build on Qwen3-32B base, then evaluate on a coder fine-tune or on our LoRA.
    - *Tier:* **$50**.

**Scale, training dynamics, interventions**

21. 📈 **Does white-box monitor quality *improve* with model size while black-box gets relatively worse?**
    - *Why:* the essay claims bigger models have narrower neurons (L77, L1350). This is the strongest strategic bet.
    - *Test:* run the Q1 protocol on Qwen3 0.6B/1.7B/4B/8B/14B/32B and plot the AUROC slopes.
    - *Tier:* **$100**.
22. 🕰️ **Can reward hacking be seen forming at neuron level during RL, and how long is the "distributed before consolidation" window (L2387)?**
    - *Why:* it would make training-time monitoring possible, but could also be a blind window.
    - *Test:* a small GRPO run on Qwen3-0.6B/1.7B with a hackable unit-test environment, tracking test-related neurons across checkpoints.
    - *Tier:* **$100** (tiny) / **beyond** (realistic).
23. 🧯 **Is ablating or clipping flagged neurons a good white-box "resample" protocol, with less usefulness loss than defer-to-trusted?**
    - *Why:* the essay shows clipping >p99.9 gates kills memorized recitation, while matched random clipping does not (L1925).
    - *Test:* on flagged backdoor steps, clip the monitor neurons and regenerate, then measure the backdoor rate and pass rate vs a defer-to-trusted baseline.
    - *Tier:* **$50**.
24. 🧵 **Does cleanliness hold on long agentic transcripts and reasoning traces?**
    - *Why:* long-context neurons looked polysemantic with two-paragraph windows (L443). Control settings are long and multi-step.
    - *Test:* explain 50 neurons using short vs long agent-transcript contexts and compare label stability and selectivity.
    - *Tier:* **$50**.
25. 🏛️ **Do the essay's frontier-scale claims (Kimi K3, 10B-token searches, 100k-graph audits) hold?**
    - *Why:* the claimed scale advantage depends on them.
    - *Test:* not feasible for us. A 10B-token search alone is ~$2.5–3.7k (scout-budget). Wait for the companion paper (L96).
    - *Tier:* **beyond budget**.

---

## 5. Verdict ⚖️

**Strong, honest and important, but not yet evidence for what we want to prove.**

- **Likely right:**
  - Several canonical "polysemantic" examples were misread or were tool artifacts. The cat/car neuron is a V-shape detector, and the car→dog "superposition" circuit is generalized pose.
  - Modern residual, gated and especially MoE models have far more legible native neurons than 2023-era models.
  - Superposition was adopted as a default on thin evidence; Anthropic's SoLU paper said so in 2022 (L461).
  - The vision evidence is genuinely quantitative and well controlled: the squeeze plus SAE positive control (L735) and the matched-mass weak/strong ablation (L883–891).
  - The pre-registered "explanations that can lose" test (L2007) is good epistemics.
  - The author openly corrects his own earlier work.
- **Contested:**
  - The 90/7/2–4 figure: preliminary, per pole, self-graded, unpublished method. Our recount of the released papers gives ~80–84%.
  - "Recursive generalization" as *the* explanation: vision anecdotes plus finished-model LLM stories, with no LLM checkpoints.
  - Weak activations, the residual stream and attention being unimportant in LLMs.
  - The essay wins partly by narrowing "superposition" to "arbitrary packing". It sets aside distributed computation (L2361), the sense that matters most for finding a compact "deception" signal.
- **Overstated for AI control:** "Deception … has no reason to hide from the model's own circuitry" (L1496). That holds only with no optimization pressure against the reader. Published work shows activation monitors can be trained around (Bailey et al.; Neural Chameleons). Whether native-neuron monitors are more robust is unknown.
- **For our project:** the essay hands us the ingredients: exact native neurons, causal ablation tests, a reusable falsification protocol, 1,000 free neuron papers, and signals transcripts can't show (overridden dissent, hidden hops, hedging). It does not hand us a result. A cheap head-to-head control game ($20), then an adversarial-evasion round ($100), would be the first evidence either way. Either outcome is worth publishing.
- **Context:** reception is one day old. The LessWrong linkpost has 58 points and 6 comments, Hacker News 96 points, and there is no expert rebuttal yet. The author works at an interpretability-tooling company, and an internal Goodfire disagreement exists (Gorton & Lewis on adversarial superposition).
