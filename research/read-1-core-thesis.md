# read-1-core-thesis: "Neural Networks Are Already Clean" (Cammarata, Goodfire), lines 1–274

Source: `source/already-clean.txt` (plain-text extraction; figures missing, alt text kept). Scope: The Short Version (L29–96), Cars and Animals (L100–208), A History of Microscope Errors (L212–271). Every line in 1–274 was read. Quotes are kept to short anchoring fragments; everything else is paraphrase with line numbers.

---

## 1. Plain-English summary

The essay claims the field misread its own canonical evidence. Neurons that looked like arbitrary mixtures ("polysemantic"), and the idea that networks hide unrelated concepts in shared neurons because they run out of room ("superposition"), came mostly from three ordinary problems:
(a) weak tools, especially feature visualization that "reward hacks" into easy paths, explainer models that could not run conjecture-and-test loops, and metrics that rewarded simulating activations over being right;
(b) architectures that learned badly in late layers, such as InceptionV1 without residual connections or LayerNorm;
(c) a human and LLM bias toward describing neurons as lists of nouns, when they often detect a shared pattern (a "verb" that splits a positive pole from a negative pole).

What is left over is called **recursive generalization**: a neuron's meaning grows like a branching tree into nearby territory ("iy" → "diy" → "do it yourself"). Because the groupings follow the network's own sense of similarity, the author says they are informative rather than arbitrary.

Headline numbers:
- **InceptionV1 last layer**: roughly 0–5% interpretable with the old tools. About 50% with fixed tools on the same 2014 weights, about 70% when the same architecture is retrained with modern regularization, and about 99% in a parameter-matched ConvNeXt (L41, L245, L271).
- **Qwen3-32B**: in preliminary audits, about 90% of neuron *poles* have one main job, about 7% have two related jobs, and about 2–4% are not yet understood (L50). For comparison, 2023 work gave a median neuron score of 0 out of 14 (Anthropic) and found about 1.7% of neurons interpretable (OpenAI) (L47–48).

The author treats these findings as evidence that ordinary "normal science" on a network's own neurons works and compounds like a crossword (L69–81). The argument rests on four steps; the last is labeled "Highly speculative" (L85–91).

---

## 2. Claims (with evidence, line numbers, strength)

| # | Claim | Evidence (line) | Numbers | Strength |
|---|---|---|---|---|
| C1 | Canonical polysemanticity/superposition evidence was misread; a network's own mechanisms are its legible building blocks. | "was misread" (L33); "Neural networks are already clean." (L33) | – | asserted in summary; supported by the case studies below |
| C2 | Superposition was the wrong explanation for InceptionV1. Late layers overflowed because of architectural problems, and weak tools amplified the problem. | "Architectural problems made later layers overflow" (L41) | – | moderate (architecture-controlled comparison at L253–271) |
| C3 | With ordinary architecture fixes and no change to size or data, 99–100% of last-layer neurons are easily interpretable. | "99-100% of neurons in that last layer" (L41); "about 99%" (L271) | 99–100% | moderate: numbers given, but the rater and rubric are not stated |
| C4 | The models are legible across a 300× size range. With less room, neurons get coarser instead of folding unrelated things together. With more room, they differentiate. | "300× range in size" (L41); "one car neuron covering many kinds of car" (L41) | 300× (this matches ConvNeXt small at 1/75× through large at 4×, L193–200) | moderate (figure-based, qualitative) |
| C5 | The original car→dogs "superposition" circuit from Zoom In was the only one shown and the only one the author saw. Nothing reads out the combination. | "nothing reads that combination" (L44); "no one has published a second circuit with the right shape" (L44) | n = 1 canonical example | moderate for the reanalysis; the "nothing reads" claim is asserted, with no downstream-weight numbers given here |
| C6 | Earlier language-model numbers were very low. | Towards Monosemanticity median "0 on its rubric out of a possible 14" (L47); OpenAI auto-interp "about 1.7% of neurons interpretable" (L48) | 0/14, 1.7% | strong (citations of published work) |
| C7 | Qwen3-32B: ~90% of neuron poles have one main job, ~7% have two related jobs, ~2–4% are not yet understood. Dense and MoE models look similar, and this extends up to trillions of parameters (Kimi K3). | "preliminary audits of Qwen3-32B" (L50); footnote "closer to 97% non-arbitrary mixtures" on "relatively small samples" (L58); "Kimi K3" (L60) | 90 / 7 / 2–4%; 97% (small samples) | weak to moderate: "we estimate", the result is threshold-dependent (L50–60), and sample size, rubric and inter-rater agreement are not given. Details are deferred to a companion paper (L96) |
| C8 | Most remaining apparent polysemanticity is recursive generalization: neurons sprout offshoots into adjacent territory. | "iy" → "diy" → "do it yourself" (L62) | – | example-based |
| C9 | When the original InceptionV1 architecture is retrained and its least legible neurons are followed over training, they turn out to be overgrowing locally into adjacent territory. | "overgrowing locally into reasonable, adjacent territory" (L63) | – | asserted (training-dynamics observation; no figure in this part) |
| C10 | The 2023 gap had four causes: explainers could not run conjecture-and-test loops; metrics rewarded simulation over correctness; people expected the wrong motifs; and the models were small or simplified. | "rewarding explanations that could simulate activations rather than ones that were right" (L67) | – | argued, asserted |
| C11 | Understanding compounds like a crossword. Nearly empty and mostly filled in are the two natural anchor states. | crossword/jigsaw framing (L69) | – | asserted, with one illustrative example |
| C12 | Feeling and social-cue neurons are among the most common. They often fire on punctuation (commas) or on the token just before the feeling matters, not on the content words. | "some of the most common we've found" (L71); fire "on punctuation, like commas" (L73) | – | example-based (the "bargain righteousness" neuron) |
| C13 | A mostly explained network exposes tool bugs: the unexplained remainder points at broken tools. Example: the double-negative regime in SwiGLU. | "the unexplained remainder points straight at them" (L75) | "2% of a network" contrast (L75) | example (details at L1573+, outside this part) |
| C14 | Bigger models learn narrower neurons that are easier to recognize. | "bigger models learn narrower neurons" (L77) | – | asserted here (vision evidence at L185–202) |
| C15 | Understanding the whole network may be easier than understanding only the parts we care about. "Deception" probably has microstructure you only find by looking. | "alignment-relevant microstructure" (L79) | – | speculative |
| C16 | On modern conv nets the process "basically worked". Agents map neurons and circuits, build microscopes, and track hundreds of thousands of attribution graphs. It has worked "so far" in language models up to trillions of parameters, which are "not close to solved". | L81 | "hundreds of thousands of attribution graphs" | asserted, partial |
| C17 | Bitter lesson for interpretability: scaling ordinary investigation beats engineering clever decompositions. | L93–94 | – | speculative/rhetorical |
| C18 | InceptionV1 neuron 4e:55 (the famous cat/car neuron) is a **V-shape / pointedness detector**, not OR(cat, car). | "it's a V-shape neuron" (L106) | – | moderate: qualitative, with multiple evidence lines (C19–C21); the insight came after "a few seconds" of reflection (L106) |
| C19 | 4e:55's circuit is consistent with V-shape. Inputs: 4d:493 fox snout, 4d:477 wolf face, 4d:201 van front. Readers: 5a:94 flames (and fireboat jets, fox faces), 5a:352 coyote face, 5a:317 martini glass. | L108, L112–132 | neuron IDs | moderate (circuit weights shown as line widths; no values in text) |
| C20 | 4e:55's negative pole is round (an O). Pointed photos drive it (dog, fox, cat, car, pool table, bullet train); round ones push it negative (dog, dog, snail, golf ball, tennis ball, clock), "whatever the label". | L108, L134–160 | 6 positive and 6 negative examples | example-based. Dogs on both poles support shape over class identity |
| C21 | Feature visualization showed whiskers because it maximizes activation along whatever route it finds first. Once it takes the cat route, it pulls in everything that route carries. The cat signal reaching car readers is too small to need a cancelling negative weight. | L104 footnote 2 | – | argued mechanism, not measured |
| C22 | The car→dogs circuit is really **generalized pose**: cars and dogs grouped by how they face the camera. InceptionV1 has more than a hundred such pose neurons that no one had noticed. Later layers build on them to the end of the model. | "more than a hundred of these generalized pose neurons" (L167) | >100 | count asserted; list not shown in this part |
| C23 | Feature visualization is reward-hacked in deeper layers. Gradient descent falls into dog neurons because the data has many dogs. Biasing it lightly toward the paths that top images take mostly yields cars. | "ends up being reward hacked in deeper layers" (L169) | – | example-based (figure L171–183: visualized "through the car", 2 of 4 are car neurons and 2 encode shared car/dog pose) |
| C24 | The V neuron and this circuit were Zoom In's two main examples of why its picture might be "overly rosy". | L162–163 | 2 examples | strong (bibliographic) |
| C25 | Scaling does not separate dog-pose from car-pose. DINOv2 (12×) has more pose neurons, but many are still generalized. The same neuron appears in ConvNeXt large (4×) and medium (1×). The smallest (1/75×) has only a rough cars+dogs version that is not organized by pose. | L185–202 | 12×, 4×, 1×, 1/75× | example-based ("every vision model I've looked at") |
| C26 | Humans and automated interpreters share a noun bias: they describe neurons as groups of nouns. Neurons are better seen as verbs that draw a distinction between their positive and negative poles. This is "the largest source of misattributed polysemanticity in mid-layer neurons". | L204–206 | – | asserted ("I suspect") |
| C27 | Treat a neuron with 2–3 meanings as one neuron whose meanings are grouped. The grouping is a clue. Extra meanings often turn out minor and rarely active. Some are tool bugs: the SwiGLU double negative, an "unread saliency knob" in the residual stream, and FV reward hacking. Optimizing for a cleaner list (e.g., with an SAE) could erase these hints. | L208 | – | argued |
| C28 | Feature visualization history: it lacked transformation robustness until that was added. Late-layer FV then failed again from reward hacking and imperfect regularization, which "a few subtle tweaks" fixed. | L216–218; figure L220–243 (2009 gradient ascent = static; 2017 Lucid = jar / dog-face jumble; 2026 = metal jars / box camera) | – | example-based. **The 2026 settings are never specified** (searched the whole file) |
| C29 | Old explanation for InceptionV1's dead last layer: too many high-level features for too few neurons, causing arbitrary packing. | "essentially no interpretable neurons on InceptionV1's final layer" (quoted estimate, L245); L251 | ~0% / ~5% | strong as history |
| C30 | A parameter-matched modern conv net (residual connections, LayerNorm, "a couple other improvements"), trained on the same data, has a "beautiful" last layer. | L253; figure: 7.06M parameter-matched vs 28.6M; e.g., neuron 127 "Ladybugs" top 20 of 50,000 images = 17 ladybugs + 3 leaf beetles (L255–267) | 7.06M, 28.6M, 20/50,000 | moderate (an explorable site is claimed) |
| C31 | Cleanliness needs two things: a network that learns well (architectures built for performance, e.g., the residual stream, also produce clean deep layers) and tools strong enough to see it. | L269 | – | argued |
| C32 | InceptionV1 last-layer interpretability ladder: ~5% (author, old tools), ~0% (others), ~50% with better tools on the same 2014 weights, ~70% retrained with modern regularization, ~99% in a same-size ConvNeXt. | L271 | 0 / 5 / 50 / 70 / 99% | moderate (no rubric or rater count stated) |

---

## 3. Methods (reimplementable detail)

1. **"Rapid normal science" loop for one neuron** (L35, L71–73, L81). For each neuron pole:
   - collect top activating examples;
   - read the surrounding sentences, not just the max token;
   - look forward too, at what token comes next (the "Titanic" neuron was really predicting "boat" next, L56);
   - examine the negative pole separately;
   - examine weak activations and decide a threshold;
   - examine upstream construction (input weights/attributions) and downstream readers;
   - steer: turn the neuron up and read what the model writes;
   - design specific falsification tests (e.g., which store brands activate the "bargain righteousness" neuron);
   - in MoE models, use the expert's specialization as context;
   - iterate as neighboring neurons get explained (crossword constraint).
   Run all of this with agents at scale, including "hundreds of thousands of attribution graphs" (L81).
2. **Pole-level audit rubric** (L50, footnote L50–60): label each neuron *pole* as one main job (with small related offshoots), two related jobs, or not understood. Report sensitivity to the weak-activation threshold and to activation percentile versus fraction of max (the author prefers each neuron's own natural activation scale over percentile standardization, L54).
3. **"No-nouns" description heuristic** (L206): describe the neuron without using noun groups, find the shared pattern (e.g., V-shape), then test the hypothesis on new noun groups (shinkansens, pool tables).
4. **Shared-input visualization** (L104 fn 2): to see what a polysemantic-looking neuron "really" detects, visualize what its strongest *inputs* have in common, not the neuron alone. Figure: "What the cat, car and fox groups share, optimized: pale spikes fanning from a point" (L121).
5. **Path-conditioned ("visualized through") feature visualization** (L169, L179–183): bias the FV optimization toward the path through a chosen upstream neuron (e.g., car neuron 4c:447), or toward "the natural paths the top images take". This avoids the optimizer falling into high-prior dog neurons. The exact biasing scheme is not specified.
6. **Feature-visualization hygiene** (L216–218): add transformation robustness; fix late-layer regularization ("a few subtle tweaks", unspecified). Validate by showing FV next to the strongest dataset photos, comparing 2009 / 2017 Lucid defaults / 2026 settings.
7. **Architecture-controlled interpretability experiment** (L253–271): fix the dataset (ImageNet) and parameter count (~7M), and compare (a) original InceptionV1 weights, (b) InceptionV1 retrained with modern regularization, (c) a parameter-matched ConvNeXt with residual connections and LayerNorm. Score the % of last-layer neurons interpretable using the top 20 of 50,000 images per neuron, with class labels marked.
8. **Scale sweep for neuron identity** (L41, L190–202): ConvNeXt small (1/75×), medium (1×), large (4×), DINOv2 (12×). Look for the "same neuron" (e.g., pose-by-camera-facing) across sizes and note whether it splits or stays generalized.
9. **Training-dynamics tracking** (L63): retrain and follow the least legible neurons across checkpoints to see whether they grow by local overgrowth (recursive generalization) or by arbitrary packing.
10. **Remainder-as-tool-debugger** (L75, L208): once most neurons are explained, treat systematic unexplained residue as a tool bug. This is how the SwiGLU double-negative regime (separating the four sign combinations of gate × up, per later text L1573/1592) and the "unread saliency knob" were found.

---

## 4. Weaknesses / ways the argument could be wrong

- **No validated metric in this part.** "Easily interpretable" is judged by the author and agents. There is no rubric, no blinded raters, no inter-rater agreement, no pre-registration, and no held-out *predictive* test (predicting activations or steering outcomes on new inputs). The author criticizes simulation scoring (L67) but offers no replacement metric here.
- **Symmetric illusion risk.** The author admits the original superposition reading came from an "intuitive explanation" that "didn't prompt diving more into the tools" (L162 fn 3). The V-shape reading was likewise reached "almost instantly" after "a few seconds" (L106). Fast, satisfying stories are exactly what interpretability illusions look like. There is no controlled-stimulus test (synthetic V vs O shapes, a dose-response on pointedness) and no quantitative ablation.
- **Unfalsifiability risk in "recursive generalization".** Almost any co-activation can be explained afterward as "adjacent territory" (e.g., "diy" → "do it yourself"). The footnote says the "unrelated jobs" turn out to be "almost always this kind of thing" (L56). A falsification criterion is needed. The essay hints at one, "a second circuit with the right shape" (L44): a readout of an unrelated combination.
- **Counting poles and top activations is not the same as covering computation.** 90% of *poles* with one main job says nothing about what fraction of the model's behavior or loss runs through those top activations, as opposed to weak activations, attention, or the residual stream (which has no privileged basis). The footnote concedes that weak activations change the picture (L52).
- **Threshold dependence.** By the author's own account, the share of neurons with one job "varies depending on how you set the threshold" (L50). The 97% figure comes from "relatively small samples" (L58).
- **Vision last layer is an easy case.** In a good ImageNet classifier, last-layer neurons should be close to class detectors (Ladybugs, Terriers). 99% there is less surprising than 99% in middle layers. The striking result is the *contrast* with InceptionV1.
- **Reproducibility gaps.** The FV "2026 settings" and the "lightly bias toward natural paths" scheme are not specified. Kimi K3 and trillion-parameter results are deferred to a companion paper. The ">100 pose neurons" are not listed in this section.
- **Selection of examples.** The positive and negative image lists (L134–158) are curated. "Pool table" and "bullet train" being "pointed" is plausible but not shown quantitatively.
- **"Nothing reads that combination" is asserted**, with no downstream weight magnitudes, ablations, or linear-readout analysis given in this part.
- **Goalpost shift.** Calling "one neuron with a few grouped meanings" clean (L208) redefines polysemanticity. For practical uses such as monitoring, related offshoots still produce false positives.
- **Author position and venue.** This is an informal "working hypothesis" essay (L3, L11), not peer-reviewed. The author co-proposed both explanations (L65).
- **Adversarial settings are untested.** All evidence comes from naturally trained models. Nothing addresses whether cleanliness survives optimization *against* interpretability (an adversary or RL pressure), which is exactly the control setting.

---

## 5. Open questions

1. Does the 90/7/2–4% breakdown survive a blinded, multi-rater, pre-registered audit with a predictive-validity metric (held-out activation prediction plus steering-effect prediction)?
2. What fraction of computation (logit attribution, loss recovered when only the "explained" neurons are kept) do the interpretable neurons cover, across MLP neurons, attention, and the residual stream?
3. Is there any natural network where real superposition appears in the essay's sense, i.e., a downstream neuron reading out an unrelated combination? Can toy-model superposition (Elhage et al. 2022 setups) be distinguished from recursive generalization with a concrete test?
4. Do alignment-relevant behaviors (deception, sabotage intent, evaluation awareness, reward hacking, sandbagging) have native neurons or "verb" distinctions? L79 predicts "microstructure".
5. Does cleanliness survive adversarial pressure? If a model is trained (or RL-pressured) to avoid activating a monitor neuron, does it relocate the concept to another clean neuron, or does it learn real superposition and obfuscation? (L1526, outside this part, hints at not "pushing gradients through the very tools we use to see".)
6. How stable are neuron identities under fine-tuning? Does a backdoor or sandbagging fine-tune add a new offshoot to an existing neuron (recursive generalization), create a new neuron, or produce an arbitrary mixture?
7. What are the exact FV settings and path-biasing methods, and do analogous "microscope errors" exist in language-model tooling (e.g., max-activating text that ignores next-token context, L56)?
8. What do agent-scale audits cost per neuron, and how long would a 32B or 1T model take?
9. Which architectural ingredients cause cleanliness (residual stream, LayerNorm, gating)? Will future architectures stay clean?
10. Do the "feeling / social-cue at punctuation" neurons generalize to code, where "summary tokens" might be newlines, closing braces, or comment starts?

---

## 6. Control hooks (white-box monitor vs black-box transcript monitor)

The section offers no control experiments. Below is what follows from its claims, marked as inference.

**H1. Native neurons as a free, zero-reconstruction-error monitor vocabulary.** If about 90% of Qwen3-32B neuron poles have one main job (L50), a monitor can read activations the forward pass already computes. No SAE training, no reconstruction loss, and near-zero marginal cost per token. Protocol: label the neurons related to {vulnerability insertion, test special-casing, concealment, evaluation awareness, deliberate error}, then alert when they fire strongly at decision tokens.

**H2. Read at "summary" positions, not content tokens.** Feeling and social-cue neurons fire on punctuation and commas, or on the token just before the feeling matters (L73). A white-box monitor for intent ("sneaky", "getting away with it", guilt) should therefore aggregate at summary tokens (end of line, newline after a suspicious code line, end of a CoT sentence) and at the token before an action. Black-box monitors cannot see these "silent" judgments when they are never verbalized.

**H3. Causal validation via steering.** Before trusting a monitor neuron, steer it (L73). Turn up the candidate "insert-backdoor" neuron and check that backdoor rate rises; turn it down and check that it falls. This gives the monitor a causal guarantee a transcript LLM cannot have. It also enables an **activation-level intervention protocol**: clamp the flagged neuron and resample, as an alternative to defer-to-trusted or trusted-editing.

**H4. Bipolar "verb" neurons fit contrasts.** Neurons separate two patterns at their poles (L204). Look for honest-vs-covert, real-vs-test, or sincere-vs-sandbagged distinctions as single bipolar readouts. The negative pole doubles the vocabulary (count and monitor poles separately).

**H5. "Unexplained remainder" as an anomaly alarm.** When most of the map is explained, the unexplained remainder points at something new (L75). In deployment, compute per-token unexplained activation mass, i.e., strong activations of neurons whose explanation is inconsistent with the current context. Example: a neuron labeled for exploit or deception fires strongly while the model writes ordinary code. Spikes go to the audit queue. This is anomaly detection only a white-box method can do.

**H6. Superposition-shaped circuits as a structural backdoor signature (static, input-free).** The essay claims natural networks almost never show a circuit where something is placed into an unrelated combination and read back out (L44, L167). If that holds, an implanted backdoor or hidden objective might be detectable as exactly this anomalous shape: an arbitrary-mixture neuron, or a readout of an unrelated combination, standing out against a ~90%-clean background. This is testable with sleeper-agent-style fine-tunes on Qwen3 (speculative).

**H7. Model or neuron diffing during training.** "Watching neurons grow over training" (L63): track neuron meanings across RL checkpoints. A reward-hacking behavior should appear as a neuron sprouting an offshoot (e.g., a "unit test" neuron growing a "special-case the test" branch) or as a newly specialized neuron. This also supports removing a toxic RL environment early (L1526, outside this part).

**H8. Scale favors white-box monitors (the key strategic bet).** Black-box trusted monitoring degrades as the untrusted model outgrows the trusted monitor. The essay claims "bigger models learn narrower neurons that are easier to recognize" (L77) and that the crossword compounds (L69). If true, neuron-level monitors could *improve* with scale. Test: plot monitor AUROC versus model size (e.g., Qwen3 0.6B→235B) for both a neuron monitor and a fixed-size black-box monitor.

**H9. Beware optimization-based tools under adversarial pressure.** Feature visualization "reward hacked" into dog neurons by taking the easiest path (L169). Any monitor built by optimization (SAEs, trained probes, FV) can be gamed similarly. Keep the monitor out of the policy's training gradient (L1526). Prefer native neurons whose errors stay visible (L208).

**H10. Tool-bug awareness for SwiGLU models.** Naive reading of SwiGLU neuron activations hides a double-negative regime (L75, L208; details L1573+). A monitor on Qwen-style models should separate the sign combinations (gate × up), or adversaries and noise could hide in the "noisy middle".

**H11. Explanations reduce audit cost.** Labeled neurons let a human auditor see *why* an episode was flagged ("concealment pole fired at line 42"). With a fixed small audit budget (e.g., auditing the top 1–2% most suspicious episodes), better triage can raise safety at constant usefulness.

**H12. Sandbagging via knowledge–output mismatch.** If native neurons encode "knows the correct answer / this is correct" distinctions, a monitor can flag episodes where the internal judgment disagrees with the produced answer. A transcript-only monitor cannot see this.

### Concrete win/lose/continue experiments suggested by this section

- **E1 (APPS-backdoor control game, Greenblatt et al. 2023 style).** Untrusted: Qwen3-32B (audited in the essay), prompted or fine-tuned to insert backdoors. Blue team A: black-box trusted LLM monitor on code. Blue team B: native-neuron monitor (H1+H2+H5). Each audits the top-k% most suspicious episodes. Red wins if a backdoor ships unaudited. Report safety-vs-usefulness curves.
- **E2 (backdoor structural signature, H6).** Implant N backdoors. Without running triggers, check whether weight and attribution analysis finds anomalous non-clean neurons or readout-of-combination circuits. Measure detection rate against clean fine-tune controls.
- **E3 (adversarial cleanliness, open question 5).** RL-train the policy with a penalty for firing the monitor neurons. Measure whether behavior persists (evasion), whether a new clean neuron takes over (re-labelable, so blue can "continue"), or whether real superposition emerges (blue "loses").
- **E4 (scale curve, H8).** Run the same protocol across model sizes and compare the slope of the white-box vs black-box monitor.
- **E5 (training-time diffing, H7).** Track neuron meaning drift through an RL run that includes a reward-hackable environment. Measure detection lead time compared to transcript-based detection.

---

## 7. Pointers for other readers

- Double-negative SwiGLU regime: L1573, L1592. Alignment and "don't push gradients through tools": L1526. The definition of superposition as "last hypothesis": L458. InceptionV1 adversarial-perturbation experiment: L1891.
- Companion paper promised for language-model neuron details and Kimi K3 (L60, L96).
