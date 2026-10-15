# Read 7 — Appendix B (lines 2233–2584) of "Neural Networks Are Already Clean" (Cammarata, Goodfire, 2026)

Source: `source/already-clean.txt`, lines 2233–2584 (about 43k characters), with framing from "The Short Version" (lines 29–99). Canonical URL (line 2584): https://already-clean.goodfire.com/
Figures are missing from the text extract. Only captions and labels remain, so any claim that relies on a figure is marked that way.

Sections covered: Watching Neurons Develop (2233), Toy Models (2279), More on Circuit Ecology (2315), Unresolved Responses (2331), A Note on Features and Definitions (2342), Relation to Meta-Models (2371), Does Scale Help or Hurt Superposition? (2379), On the Title (2399), Relation to Conjoined Features (2415), Why We're Not Worried About Recursive Generalization (2430), Is Recursive Generalization Hard to Vary? (2440), Relation to Attention Superposition (2451), Neuroscience (2462), Acknowledgments (2476), References (2486), Citation (2574).

---

## 1. Plain-English summary

This part of the essay is the appendix-style discussion. It makes five moves:

1. **It watches neurons grow.** The author retrained part of InceptionV1 and followed one neuron (mixed5a:178) from step 0 to step 30,000. He says it drifted between neighbouring ideas, not unrelated ones. He also admits that a microscope setting error (the "zoom") briefly fooled him into seeing arbitrary mixing.
2. **It explains why toy models seemed to show packing.** *Toy Models of Superposition* counts the cost of sharing a neuron (interference) but not the benefit (reuse), because every toy feature is an end in itself. When the author's team added correlated inputs **and** a hidden layer to the toy, the model moved from packing (0.37) to a PCA-like grouping (0.80). Packing should therefore show up only for memories that are related to nothing, and real data has almost none of those.
3. **It offers a developmental, "ecological" theory.** Generalization and composition win a race for the error signal, because an existing niche learns the next related thing faster. Hidden, packed codes get starved of gradient. Rare facts should ride on related circuits rather than hide in unrelated ones, and the author says this is a testable prediction. Scale should make this "semantic gravity" stronger, not weaker.
4. **It cleans up the vocabulary.** "Feature" and "superposition" carry five or six meanings. The essay targets only *arbitrary packing*. It accepts "more features than dimensions" (composition) and "too much distributed computation" as real but different issues. A residual stream that is only rotated away from the neuron basis is a "trivial" distributed representation.
5. **It states its confidence and limits.** The author is about 85% sure that nearly everything comes from generalization, which is not the same as 85% of mechanisms being clean. Natural offshoots are rarer and less important than a neuron's main job, and "don't look like sleeper agents". Attention heads are not understood well enough to judge. Recursive generalization has not been tested across a whole large model because there are no LLM checkpoints. One InceptionV1 neuron (mixed5a:719) is still unexplained.

---

## 2. Claims (with evidence, line numbers and strength)

Strength scale: **strong** = experiment with numbers; **moderate** = concrete worked example or experiment without numbers; **weak** = anecdote or analogy; **asserted-only** = opinion or hypothesis.

| # | Claim | Evidence (short quotes, line) | Numbers | Strength |
|---|---|---|---|---|
| C1 | During training, neurons drift locally to neighbouring concepts and do not pick up unrelated ones. | "The movement is local: a neuron drifts to neighboring things rather than picking up unrelated ones." (2235). Trajectory for mixed5a:178 (2238–2272): step 0 dome / Polaroid camera / thunder snake; 750 fire engine / tow truck / sports car; 3,000 Model T / station wagon / tow truck; 30,000 dome / triumphal arch / orangutan. | 8 checkpoints, 0 to 30,000 steps | weak to moderate (one neuron, qualitative labels, figure missing) |
| C2 | Apparent arbitrary mixing is often an observation error, not the network's fault. | "I had the microscope's zoom set wrong" (2235); "blaming the network for the microscope" (2235) | — | weak (anecdote) |
| C3 | Multi-task toy networks reuse geometry instead of packing unrelated features. | In a TensorFlow Playground extension, "two neurons learned to respond along opposite diagonals", combined differently for a circle and for four corners (2281); "it found geometry it could reuse for both" (2285) | one run | weak to moderate |
| C4 | *Toy Models of Superposition* (TMS) is correct about its own world but leaves out reuse. | "we found no problems with its experiments" (2287); "prices the cost of sharing a neuron, interference, but not the benefit, reuse" (2287) | — | moderate (argument) |
| C5 | Packing is expected only for memories related to nothing, and real data has almost none. | "In real data almost nothing is related to nothing." (2289); rare people still have "a country, a job and a name" (2289); random labels can be learned but more slowly (Zhang et al. 2017) (2289–2290) | — | moderate (argument plus a cited external result) |
| C6 | With correlated inputs and hidden neurons, the toy groups related inputs (PCA-like) instead of packing. | "related inputs grew onto the neurons" (2294). Figure labels (2305–2307): original toy packs at density .1 → 0.37; with 40 neurons at density .1 → 0.80; dense original toy at density .9 → 0.79. Scale: "0.2 each input separate / 0.8 exact PCA" (2300–2301) | 20 inputs, 4 groups of 5, 5-dim bottleneck, 40 hidden neurons; 0.37 vs 0.80 vs 0.79 | **strong** within the toy (numbers given, but the setup is not fully specified) |
| C7 | TMS predicts a different failure from the one people report: rare features pushed off-axis, while reports describe mixtures inside neurons. | (2311) | — | asserted-only |
| C8 | Generalization and composition win a race for the error signal, and offshoots are the same race. | "they win a race" (2317); the closest neuron picks up "a bit of error" (2317) | — | asserted-only (labelled "a guess") |
| C9 | Recursive generalization comes from a head start: the "iy" neuron is already on for "diy" and so picks up "do it yourself". | (2319); "Recursive generalization is what a niche looks like at its edges." (2319) | — | moderate (example; full evidence is elsewhere in the essay) |
| C10 | A new computation can begin as a route switch inside existing machinery, as in the umbrella-to-bee case. | (2321); cross-reference to 843: the 7.06M model went from umbrella to bee "In nine training steps", nearly all in the last three blocks | 9 steps; 3 blocks; 7.06M parameters (line 843) | moderate (experiment described elsewhere) |
| C11 | Neurons consolidate for "buildability", giving specialists a sheltered place to develop. | "Part of it is buildability." (2323); car neuron as a shelter for taxis and ambulances (2323) | — | asserted-only |
| C12 | Combinations of unrelated neurons are bad places to build: weak activation paths, conflicting gradients, little to inherit. | (2325) | — | asserted-only |
| C13 | A packed code installed by hand in InceptionV1 often failed or lost reliance during training. | "the code often never worked, and when it did, the network usually came to rely on it less, though some persisted" (2327). Author's own caveat: "this isn't enough evidence on its own" (2327) | no numbers | moderate to weak |
| C14 | Some neurons remain unexplained, with "semantic residue". mixed5a:719 responds to pinched-center shapes (bow ties, butterflies, swimsuit tops) plus related items (dress shoes, beach bags, flip-flops). | (2333–2338); "I don't fully understand these exceptions yet." (2338) | — | moderate (honest counterexample) |
| C15 | "Feature" is ambiguous, and feature counts depend on which descriptions we choose. | "I'm now fairly skeptical of working in terms of features at all." (2346) | — | asserted-only |
| C16 | The right list of building blocks is much shorter than "billions or trillions of features". | Gao et al. 2024 estimate (2348–2349); "I suspect the right list is much shorter." (2349) | — | asserted-only |
| C17 | The essay targets only arbitrary packing. Having more features than dimensions is fine; it is composition. | "it's the one that would be really bad news" (2357); "there are more features than dimensions in every world we could wish for" (2357) | — | moderate (conceptual) |
| C18 | Distributed computation (for example a Golden Gate computation over 3,000 neurons) is a real concern, but it is not arbitrary packing. | "eight legible neurons" vs "three thousand" (2361); "That's a real concern" (2361) | 8 vs 3,000 (illustrative) | asserted-only (illustrative numbers) |
| C19 | A residual stream with no privileged basis is not inherently "in superposition"; rotation is "trivial". | quoting Olah 2023: "trivial" and "doesn't change the fundamental geometry" (2365) | — | moderate (cites prior work) |
| C20 | Replacing the network with a dictionary can break apart generalizations we have not yet understood. | "replacing them can take apart generalizations we haven't understood yet" (2367) | — | asserted-only |
| C21 | Meta-models (models that read activations) may be a better top-level view and can be paired with mechanism checks. | "the highest level Google Maps view, and then each direction can be checked for the mechanisms it uses" (2375) | — | asserted-only |
| C22 | The image models studied have no superposition. | "We're fairly confident the image models we studied don't have superposition." (2381) | — | asserted here (backed elsewhere in the essay) |
| C23 | The closer one looks at LLMs, the cleaner their neurons get. | (2383) | — | asserted here (the Short Version gives about 90% one-job poles in Qwen3-32B, line 50) |
| C24 | Scale should reduce superposition: "semantic gravity" grows as circuits strengthen. | (2385); "This fits Anthropic's SGTM work, which found that knowledge becomes more localized" (2385). SGTM is not in the reference list. | — | asserted-only ("We have no proof") |
| C25 | A network trained on cars recognizes cars before its car neurons form; early representations are "more distributed", and consolidation comes later as a Schelling point. | (2387) | — | moderate (observation, no numbers) |
| C26 | Packing for steering gets starved of gradient by ordinary routes; packing for building on is the "worst place to start a new niche". | (2389) | — | asserted-only |
| C27 | **Testable prediction:** rare facts are the least likely place for superposition. The neurons and heads carrying a rare fact should be related to what it is about. | "the neurons and heads that carry a rare fact should be related to what the fact is about" (2391) | — | asserted-only, but falsifiable |
| C28 | The framing shifts from storage capacity to learning speed: "circuit racing, gradient starvation and ecology". | (2395); "probably a small part of the whole story" (2395) | — | asserted-only |
| C29 | The author is about 85% confident that nearly everything comes from generalization, which differs from 85% of mechanisms being clean. | "We're maybe 85% sure" (2403) | 85% | asserted (subjective credence) |
| C30 | Cleanliness scores matter less than the cause of polysemanticity, and the score could still come down. | "The cause of polysemanticity matters much more than the count." (2405); "it might go lower" (2405) | — | asserted-only |
| C31 | "Clean" does not mean every mechanism matches a human idea; the network's ideas are often better (high-low frequency detectors). | (2409) | — | moderate (example) |
| C32 | Multimodal Neurons' "conjoined neurons" are the same motif, and they are not vestigial: branches keep growing during training. | (2420, 2426); "they don't look vestigial: the branches keep growing" (2426) | — | moderate (observation, no numbers here) |
| C33 | Recursive generalization is "most of what's left of neuron polysemanticity" once the microscope, architecture and scale are accounted for. | (2426) | — | asserted-only |
| C34 | Sub-branches are rarer and less causally important than a neuron's main job and "don't look like sleeper agents". | (2432); cross-reference 1177: offshoots are "both rarer and less important in their own context" | — | moderate (stated as observation; no numbers in this range) |
| C35 | Some unknown pressure keeps branches from overgrowing, which is why no neuron has 10 unrelated jobs and no true cat-and-car neuron forms. | (2432); cross-reference 1175: "I've never seen a neuron with something like ten unrelated things" | — | asserted-only |
| C36 | Recursive generalization is predictable during training and in the finished model; packing would need the full co-occurrence statistics. | (2434) | — | asserted-only |
| C37 | Top-k label-matching scores cannot tell superposition from recursive generalization. | (2436) | — | moderate (logical) |
| C38 | An "easy fix" for recursive generalization may be possible because sub-branches are less important. | (2436) | — | asserted-only |
| C39 | Recursive generalization is a "hard to vary" theory: a branch traces back to one local origin in semantic space and grows in a set order. | (2444) | — | moderate (methodological) |
| C40 | Not every case of heavy polysemanticity has been shown to be recursive generalization, and LLM checkpoints are not available to check. | "We haven't thoroughly shown…" (2442); "we don't have the checkpoints" (2442) | — | caveat |
| C41 | There are no well-structured canonical superposition circuits left. | "As far as I know, there are no well-structured canonical superposition circuits left." (2447) | — | asserted (absence of evidence) |
| C42 | What remains after good observation is recursive generalization or architectural problems such as SwiGLU's double-negative regime. | (2447) | — | asserted-only |
| C43 | Attention superposition may be a terminology issue, and "no one understands attention heads well enough yet". | (2454) | — | asserted-only |
| C44 | Within a layer, two or three heads do most of a route's work. The author prefers dynamic, local clustering inside attribution graphs. | (2458) | 2–3 heads | weak (observation, no data) |
| C45 | The organizing principle (generalization + composition + error signal) probably transfers to brains. Electrode-level polysemanticity evidence should be discounted. | (2466, 2468) | — | asserted-only |
| C46 | Automated scientists were essential to the work: an "effectively unlimited supply of automated scientists". | (2468) | — | asserted |

Supporting cross-references outside the range, used above: umbrella-to-bee (843–851), the offshoot importance note (1175–1177), the SwiGLU double-negative regime (75, 1573), and a "triggered sleeper" readout demo (1650) that sits in another reader's range.

---

## 3. Methods (detailed enough to reimplement)

**M1. Developmental microscope (Watching Neurons Develop, 2233–2275).**
- Retrain a "suffix" of InceptionV1 from scratch. The caption says "the same coordinate through a retrained InceptionV1 suffix" (2273), which implies the early layers are kept and the later layers retrained.
- Save checkpoints at roughly geometric spacing: 0, 350, 750, 1,500, 3,000, 7,000, 15,000, 30,000 steps.
- For a fixed neuron coordinate (mixed5a:178), produce two things at each checkpoint: (a) an optimized image (feature visualization), and (b) natural dataset examples centered on the strongest spatial response.
- Track the semantic labels over time and check whether new responses are neighbours of old ones.
- A public "early-training microscope" exists (2275).
- Pitfall the author hit: visualization zoom and scale settings can fake mixing (2235).

**M2. Multi-task TensorFlow Playground (2281–2285).**
- Several 2D classification tasks (circle, four corners) share hidden neurons, and each task reads them with its own last-layer weights.
- Inspect the last-layer neurons' response maps. In one run, two neurons responded along opposite diagonals and were combined differently per task.
- The test for an explanation: "does it show the computation the model actually learned?" (2285).

**M3. TMS with correlated groups plus hidden neurons (2292–2309).**
- Inputs: 20 sparse features in 4 groups of 5 that "fire together". Sparsity density is 0.1 (sparse) or 0.9 (dense).
- Architecture: the TMS bottleneck (5-dim), with a layer of hidden neurons (40) added after it, reconstructing the inputs (implied).
- Metric: the share of bottleneck weight mass that lies along the data's top principal components (here, the groups' shared directions). On this scale 0.2 means each input is kept separate and 0.8 means exact PCA. Thumbnails show cosine similarity between input directions.
- Results: original TMS at density .1 → 0.37 (packs); with 40 hidden neurons at density .1 → 0.80 (combines groups); original at density .9 → 0.79 (PCA).
- Missing details: loss function, importance weights, within-group correlation strength, seeds and variance, reconstruction loss for each variant.

**M4. Hand-installed packed code (2327).**
- Modify InceptionV1 weights to implement a packed code modelled on the old car → dogs → car circuit.
- Continue training, then measure (a) whether the code works and (b) whether the network relies on it, presumably by ablation.
- Reported qualitatively: it often never worked, reliance usually dropped, and "some persisted". No numbers are given.

**M5. Umbrella-to-bee route switching (referenced at 2289, 2321; detailed at 843–851).**
- Fine-tune a 7.06M-parameter model so that one umbrella photo is labelled "bee".
- Track the top-1 guess per step: umbrella → maypole → bee within 9 steps.
- Compare per-neuron responses before and after. Test connections by ablation.
- Swap only the last three blocks into the original model and check that it now says "bee".

**M6. Recursive-generalization "hard to vary" test (2444).**
- Visualize a neuron's full branch structure, including weak activations.
- Check that every branch traces back to one local origin in semantic space.
- Using training checkpoints, check that branches appear in a particular order: origin first, then nearer offshoots, then farther ones.
- Example: "iy" → "diy" → "do it yourself" → Miyazaki (2446).

**M7. Rare-fact locality test (proposed, 2391).**
- For a rare fact, localize the neurons and attention heads that carry it, using attribution or ablation.
- Score how semantically related those components are to the fact's subject.
- The prediction is high relatedness. The alternative (superposition) predicts components "chosen because they rarely collide".

**M8. Meta-model plus mechanism check (2375).**
- Use an activation-reading model for a top-level read ("Google Maps view").
- For each direction it flags, trace which neurons and circuits implement it.

**M9. Dynamic grouping for attention (2458).**
- Cluster heads or neurons locally within one attribution graph (or a small set of graphs), not with one global clustering.

---

## 4. Weaknesses and places the argument could be wrong

1. **The developmental evidence is one neuron with qualitative labels.** The mixed5a:178 trajectory goes from domes to vehicles to cameras and back to domes, and ends with "dome, triumphal arch, orangutan" (2270–2272). Whether that counts as "local" drift is a judgment call, since an orangutan is not obviously near a dome. Step 0 is random initialization. No semantic-distance metric is reported, and the figures are missing from the extract.
2. **The author's own anecdote cuts both ways.** If a zoom setting can fake mixing (2235), visualization settings could also hide mixing. Detection depends on tool choices.
3. **The toy experiment is under-specified.** Groups "fire together" (2309). If members co-fire perfectly, the 5 inputs are close to one feature and PCA is trivially optimal. The interesting regime is partial correlation, which is not reported. There are no seeds, loss, importance weights or reconstruction errors, and only 3 configurations are shown.
4. **The packing-installation experiment has no numbers, and "some persisted"** (2327). The author concedes that gradient descent is a better fine-tuner. In an adversarial setting, persistence of a few packed codes is exactly what matters.
5. **The causal theory is mostly asserted.** Circuit racing, buildability, semantic gravity and gradient starvation are labelled "a guess" (2317), "We have no proof" (2385), and "probably a small part of the whole story" (2395).
6. **SGTM is cited without a reference** (2385; it is absent from the list at 2486–2570). It is also a *training intervention* that induces localization, so it may not show that natural training localizes knowledge with scale.
7. **The definitional narrowing may shift the goalposts.** The essay targets only *arbitrary packing* and accepts "more features than dimensions" and "too much distributed computation" (2357–2361). For safety monitoring, a concept such as "deceptive intent" spread over 3,000 legible neurons could still be impractical to read, even if no packing is involved.
8. **No direct LLM developmental evidence.** "we don't have the checkpoints" (2442). The recursive-generalization claim for LLMs rests on finished-model inspection plus analogy to vision models.
9. **Attention is admitted to be not understood** (2454). Much agentic behavior (tracking earlier context, noticing monitors, following hidden instructions) runs through attention.
10. **The central claim is a credence (85%), not a measurement** (2403). The cleanliness score "might go lower" (2405).
11. **Natural training is not adversarial training.** C34 ("don't look like sleeper agents") is about natural offshoots. Deliberately inserted backdoors, data poisoning, or a model optimizing against a white-box monitor are not covered by any experiment here.
12. **The consolidation lag works against neuron monitors.** C25 says new capabilities are "more distributed" before neurons consolidate. A freshly learned misbehavior, for example during RL, could sit in an illegible distributed phase exactly when it is most important to catch.
13. **Absence of evidence is presented as evidence of absence.** "no well-structured canonical superposition circuits left" (2447) reflects what has been searched with the authors' tools.
14. **Possible author and agent bias.** The author proposed both explanations (line 65), and much of the auditing was done with agents (2468), which could share systematic labelling biases. The "thousands of mistakes" admission (2468) suggests the error rate of human and agent labelling matters.
15. **There is an unexplained counterexample** (mixed5a:719, 2333–2338), and the proposed "semantic residue" explanation is not tested.

---

## 5. Open questions

1. Does the rare-fact locality prediction (2391) hold for **deliberately inserted backdoors** in LLMs? Do trigger-to-payload routes pass through semantically related neurons (date or deployment cues, vulnerability or "insert bug" neurons), or through unrelated ones?
2. Can optimization *against* a neuron-level monitor (RL or fine-tuning with the monitor in the loss) produce packed or obfuscated codes that persist? The hand-installed experiment says "some persisted" (2327).
3. How long is the **distributed, pre-consolidation window** (2387) when an LLM learns a new behavior in RL post-training: a few steps, as in umbrella-to-bee, or thousands?
4. What is the **distribution of offshoot causal importance** (2432, 1177), and is a "rare but causally important" offshoot a reliable anomaly signal?
5. Are attention heads clean? Does the 2–3-heads-per-layer-per-route observation (2458) hold up, and can routes be monitored?
6. How large are circuits for planning-level behaviors (deception, sabotage, sandbagging): 8 neurons or 3,000 (2361)? Can a monitor aggregate them cheaply?
7. What is the unknown pressure that limits branch overgrowth (2432)? Could it be turned into a training regularizer, the "easy fix" of 2436?
8. Does the toy PCA result (0.37 → 0.80) survive partial within-group correlation, importance weighting and different hidden widths? Where is the crossover?
9. Can recursive generalization be verified on open LLMs that publish checkpoints (Pythia, OLMo) when frontier checkpoints are unavailable (2442)?
10. Can a meta-model's flagged direction be reliably decomposed into legible neurons (2375)? How often do meta-model and mechanism disagree?
11. Is the SwiGLU double-negative regime (2447; also 75, 1573) a place where a model or attacker could hide computation from naive neuron readers?
12. How do label error rates (human and agent) affect any monitor built on a neuron catalog (2468)?

---

## 6. Control hooks (turning already-clean neurons into a white-box monitor)

These are inferences for our project. Each one is tied to the line it builds on.

**H1. Offshoot-importance anomaly detector (a "sleeper alarm").** Building on 2432 and 1177: if natural offshoots are rare *and* causally weak, the baseline for a clean network is that rare contexts barely move outputs. A backdoor or sleeper agent breaks that pattern by definition: it is rare and causally decisive. Monitor: for each neuron pole on the action path, compute causal effect per activation (attribution or ablation) in the current context and compare it with that neuron's main-job effect. Flag when a low-frequency context has high causal leverage. This is cheap to compute online, gives an explanation, and is falsifiable on sleeper-agent model organisms (Hubinger et al. 2024) and APPS-backdoor setups.

**H2. Semantic tripwires on predicted payload routes.** Building on 2391 (rare facts ride related circuits) and 2321 / 843 (umbrella switches to the existing bee route): misbehavior learned by fine-tuning should reuse existing, legible routes for the payload concept. Monitor: build a registry of neuron poles whose catalogued function is concerning (for example "inserting a subtle bug", "evading detection", "test vs deployment", "grader exploitation", "pretending to be less capable"). Fire when these activate during a coding or agent step. If the prediction fails and backdoors route through unrelated neurons, the essay's thesis is falsified for the case that matters to us. Either result is publishable.

**H3. Developmental diff monitor (trusted checkpoint vs untrusted checkpoint).** Building on 2434 (branches are predictable when you watch them grow), 2426 (branches keep growing) and M5: labs own all their checkpoints. Monitor: run the same probe inputs through the pre-RL and post-RL models and list neurons whose top contexts or causal role changed. Recursive generalization predicts that new branches trace back to a local origin (2444). A new branch with **no local origin** (unrelated new job) is an anomaly worth auditing. This is model diffing at the neuron level, with a principled prior for what counts as "normal growth".

**H4. Obfuscation-resistance hypothesis (gradient starvation of hidden codes).** Building on 2327 and 2389: packed or hidden codes were hard to install, often unused, and ordinary routes "starve the packed circuit of gradient". Hypothesis for control: a policy trained to evade a neuron-grounded monitor will tend to evade by *switching to other legible routes*, not by building packed codes, and a second-layer neuron audit could catch those routes. Test it by repeating "obfuscated activations" style experiments (adversarial training against latent monitors) with a neuron-catalog monitor and measuring whether evasions stay legible. "Some persisted" (2327) means this must be measured, not assumed.

**H5. Watch the pre-consolidation blind spot.** Building on 2387: new skills start distributed. A neuron-only monitor may lag on freshly learned misbehavior. Pair neuron tripwires with residual-stream probes or meta-models, which can read distributed directions (2365 says rotation is "trivial", so probes fit the clean picture). Measure the lag in steps during RL.

**H6. Two-tier monitor: meta-model first, mechanism verification second.** Building on 2375. Tier 1 is a meta-model or activation reader that gives a fast suspicion score per action. Tier 2 checks the flagged direction against neurons and circuits to cut false positives and give auditors a mechanistic reason. This fits the trusted-monitoring control game: spend scarce human audit budget only on flags that both tiers confirm, or on disagreements.

**H7. Do not use cleanliness scores as success metrics; use control-game outcomes.** Building on 2405 and 2436: top-k label matching cannot tell good worlds from bad ones. Evaluate white-box monitors by safety at fixed usefulness and audit budget (as in Greenblatt et al. 2023, APPS backdoors; ControlArena / BashArena / SHADE-Arena style agent settings). Compare a black-box transcript monitor, residual probes, the neuron catalog plus tripwires, and hybrids. Win: backdoor caught before execution. Lose: backdoor ships. Continue: no flag and no backdoor.

**H8. Use dynamic, per-transcript circuit grouping for attention-heavy behaviors.** Building on 2458: cluster within the attribution graph of the specific suspicious action instead of relying on a global dictionary. This has a cost problem: an attribution graph per agent action is far more expensive than one LLM-monitor call. The trade-off needs to be measured.

**H9. Training-time regularizer for monitorability.** Building on 2436 ("an easy fix would be welcome… sub-branches seem less important"): if offshoots can be pruned cheaply, labs could train models that are easier to monitor at the neuron level. This is a "monitorability tax" experiment: measure the capability cost against the gain in monitor AUROC.

**H10. Explanations as audit evidence.** Building on 2285 (an explanation should "show the computation the model actually learned"): a white-box flag comes with "neurons X, Y (catalogued as 'hide change from reviewer') fired at token t". A black-box monitor can only say the transcript looks suspicious. This matters for human auditors and for incriminating evidence in control protocols.

**H11. Scale argument as a bet.** Building on 2385–2395: if semantic gravity increases with scale, white-box monitors get *better* on bigger models while black-box monitors face smarter, subtler attackers. That asymmetry, if real, is the strongest strategic case for white-box control. It should be tested across model sizes, for example Qwen3 family sizes or OLMo checkpoints, as a scaling curve of monitor AUROC.

Possible headline experiment ("prove it" setup): take an open model with a neuron catalog (the essay audited Qwen3-32B; see line 50). Train sleeper or backdoor model organisms, for example "insert a subtle vulnerability when a trigger is present", plus a sandbagging organism. Run a control game with a fixed 1–2% audit budget. Compare (a) a strong black-box LLM monitor reading code and transcript, (b) residual linear probes, (c) H1+H2 neuron tripwires, and (d) H6 hybrid. Pre-register the H2 prediction (backdoor payload neurons are semantically related). Report safety-usefulness curves, plus a red-team round where the attacker trains against the white-box monitor (H4).

My own size estimate, to be verified: Qwen3-32B has about 64 layers × 25,600 MLP neurons, roughly 1.6M neurons or about 3.3M poles. That is a catalog that agents can feasibly build. This number is not from the essay.

---

## 7. References in this range of note for follow-up

- Gradient Starvation (Pezeshki et al. 2021), Coherent Gradients (Chatterjee 2020), A Closer Look at Memorization (Arpit et al. 2017): the theoretical basis for the "circuit racing" claims.
- Understanding DL Requires Rethinking Generalization (Zhang et al. 2017): random labels are learnable but learned more slowly.
- Toy Models of Superposition (Elhage et al. 2022); Distributed Representations: Composition & Superposition (Olah 2023).
- Scaling and Evaluating SAEs (Gao et al. 2024): the "billions or trillions of features" estimate.
- Progress on Attention (Jermyn et al. 2025): attention superposition.
- Uncovering Neural Geometry in Vision Models With Block-Sparse Featurizers (Fel et al. 2026, Goodfire).
- The Missing Curve Detectors of InceptionV1 (Gorton 2024): SAE on InceptionV1.
- Anthropic "SGTM" is cited in the text (2385) but missing from the reference list.
- Acknowledgments: Curt Tigges did "much of the language model work" (2478). A companion technical paper is promised (line 96).
