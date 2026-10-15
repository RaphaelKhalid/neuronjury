# Read 2: Recursive Generalization, the superposition critique, and "Superposition of the Gaps"

Source: `source/already-clean.txt`, Nick Cammarata, "Neural Networks Are Already Clean" (Goodfire, ~Oct 2026).
Range read in full: lines 275-468 (sections "Recursive Generalization", "Superposition", "Superposition of the Gaps"). Framing read: lines 29-99.
Cross-references consulted (outside my range, only where my range points to them): 834-859 (rare things / umbrella-to-bee), 1175-1179 (offshoot importance, SwiGLU), 2415-2445 (appendix: conjoined features; why not worried; "hard to vary").

Figures are missing from the text extract; where a claim rests on a figure, I note whether its caption calls it "Conceptual illustration" / "Illustration" (i.e. not a data plot).

---

## 1. Plain-English summary

The essay's central replacement move happens here. Old story: neurons look messy because the network runs out of room and starts *packing unrelated things together* where they rarely collide (superposition as a learning principle). New story: neurons look messy because a neuron that learned one thing keeps *growing outward along each facet* of what it already detects, and those branches sprout their own branches ("recursive generalization"). Each step is local and easy to follow; only the end result looks like a grab-bag.

Evidence offered in this range:
- Watching one InceptionV1 neuron form during retraining: yellow flowers (photos sometimes containing dogs) -> other nature, green balls, dogs without flowers (l.277). Side-by-side with ConvNeXt on the same data: both start on rapeseed fields and reach for balls and fruit; ConvNeXt drops them, InceptionV1 keeps spreading into dogs and broccoli until the fields nearly vanish (l.281).
- A language-model "planetary geology" neuron whose top firings mix Moon/Mars geology with IDL and CesiumJS code docs. Grouping its top-100 examples by *which upstream circuits feed them* ("route split") gives 44% Moon/Mars crust, 42% Moon missions, 6% old impacts/Mars, 8% Cesium/IDL code; the code branch enters via a different, early-layer input (L6 "names like Cesium") (l.311-351).
- Several "this must finally be noise" neurons that resolved on closer inspection: a "pr" neuron that also fires on Base64 URLs and Bengali (both decode/transliterate to "pr") (l.409-429); a "polysemantic comma neuron" that is really a Colorado neuron storing a running summary on commas, and steering it makes the model plan a hike (l.431-441); long-context neurons that looked mixed only because the dataset used ~two paragraphs (l.443-450); a health-SEO-spam neuron that only made sense with a broader dataset (l.452).

Then a conceptual critique: "superposition" is used in at least two senses ("more features than dimensions", which even a perfectly monosemantic network satisfies by composition, vs. a *learning principle* that packs unrelated things). The essay targets only the learning-principle sense (l.384-389). Generalization predicts *local* groupings; superposition predicts *non-local* ones, so watching a neuron grow is a test (l.364, 387).

Finally, "superposition of the gaps": polysemanticity is "often more a claim about the observer than the neuron" (l.395). Five candidate causes (bad tools, bad explanations, bad learning, recursive generalization, superposition) - and four of them are testable, while superposition's "only symptom is that something doesn't make sense" (l.463). So superposition should be the *last* hypothesis, not the null (l.458). The author admits the opposite risk ("an explanation of the gaps") and the possibility of "some dramatic extended case of selection bias" (l.456, 463).

---

## 2. Claims, evidence, strength

| # | Claim | Evidence (exact quote, line) | Numbers | Strength |
|---|---|---|---|---|
| C1 | Pre-fix InceptionV1 last layer was not arbitrary; its neurons grew along facets of their starting concept. | "it started on yellow flowers, in photos that sometimes included a dog. Then it grew along each facet of those photos: toward other kinds of nature, toward green objects like balls, and toward dogs without any flowers." (277) | none | moderate (one worked example; checkpoint-tracked) |
| C2 | Every neuron the author examined showed this; better architecture shows it "much less". | "This is true of every neuron I looked at. The improved architecture shows the same pattern, but much less of it." (277) | sample size not given | asserted-only (no count, no metric) |
| C3 | Architecture controls how far branches spread (ConvNeXt vs InceptionV1, same data). | "Both reach for balls and fruit early on; ConvNeXt lets them go and stays on the fields, while InceptionV1 keeps spreading, into dogs and then broccoli, until the fields are nearly gone." (281); grey band = "share of the neuron's strongest images" (279) | shares shown only in missing figure | moderate (one neuron pair, figure lost) |
| C4 | Definition of recursive generalization. | "a neuron generalizing along more than one axis, often first along one axis, then sprouting outwards in ways that are easy to follow locally, but stop it from being "monosemantic" in the end." (283) | - | definition |
| C5 | Language-model example: "iy" -> "diy" -> "do it yourself". | "responds to "iy," including in "Miyazaki," then to "diy," and then to "do it yourself,"" (285); caption: "Conceptual illustration." (287) | - | weak (figure explicitly illustrative) |
| C6 | Offshoots are everywhere and usually obvious; some unclear. | geology -> Cesium (290); enemy neuron -> Russian poem about enemies; "A Srinivasen neuron also lightly fires for the UniProt protein database... it's hard to know for sure." (292) | - | weak-moderate (anecdotes, one flagged uncertain) |
| C7 | Grouping a neuron's top examples by upstream route separates core facets from the offshoot; the offshoot "arrives by its own route". | "Grouped by route share of the top 100" (311): crust 44%, missions 42%, old impacts 6%, Cesium/IDL code 8% (312-318). "Grouped by the circuits that feed them, they separate into three facets of one core, planetary surfaces, and one offshoot, the code, which arrives by its own route." (351) | 44/42/6/8 % of top-100; code input at L6 vs core inputs L28-L31 | strong for this one neuron (quantified), but n=1 and model unnamed |
| C8 | (My observation, from the data shown) The offshoot occupies the very top of the activation list. | Top-8 values: IDL STRSPLIT 72, IDL SPAWN 62, IDL "Cancel" 61, Cesium.js 59, then four geology/Moon items at 54 (295-309). | 4 of top 8 (and all of top 4) are code; code = 8% of top 100 | strong (directly in the displayed data); this cuts against reading offshoots as uniformly "weak" |
| C9 | Recursive generalization was first noticed as "conjoined features" in Multimodal Neurons (2021); without checkpoints they could not watch it form. | "calling them "conjoined features."... no one, including me, suggested it might be the general explanation" (356) | - | historical claim |
| C10 | Generalization and superposition make opposite predictions: local vs non-local groupings. | "generalization should be local, superposition should be non-local, since it would want very different things to be near each other." (364); "floppy ear dog + Latin poetry neuron" (366) | - | argument (sound in principle; operationalization of "local" not given) |
| C11 | With fewer neurons, generalizing neurons become coarser, "never fractured". | "Fewer neurons make generalizing neurons coarser, never fractured." (382; caption of "Conceptual illustration", 32 things, slider 4/8/16 neurons, "8 things per neuron" at 4) | 32 things; 4/8/16 neurons | asserted here (illustration); backed elsewhere by the 300x scale sweep (l.41) |
| C12 | "Superposition" is ambiguous; "more features than dimensions" is satisfied even by a monosemantic network through composition. | "superposition then means either "more features than dimensions," which even a fully monosemantic network would satisfy, because its neurons compose, or a learning principle" (385). Footnote 4: InceptionV1 4b car-part neurons (windows, bodies, wheels) assemble into car neuron 4c:447 -> "two car features in adjacent layers" (385) | - | moderate (conceptual + concrete example) |
| C13 | The learning-principle sense is the one that carries the good/bad news, and it's testable by watching growth. | "whether it forms holds such a disproportionate share of the good or bad news for interpretability. It's also fairly easy to test" (387) | - | argument |
| C14 | "More features than dimensions" is "basically" not bad news (deferred). | (389) | - | asserted here; deferred |
| C15 | Polysemanticity is often about the observer; five possible causes. | "Polysemanticity is often more a claim about the observer than the neuron." (395); list (397-405) | - | framework |
| C16 | The author expected to hit superposed fragments and never did. | "I expected them to run into intractable feature fragments in superposition... But it never came" (407) | - | anecdotal / testimonial |
| C17 | A frontier-LM "pr" neuron's apparent junk (Base64 URLs, Bengali) is "pr" after decoding/transliteration. | "decode the URLs: "pr" words. Translate the Bengali: "pr"." (409); caption "Illustration" (429) | - | moderate (concrete case; figure illustrative; model unnamed) |
| C18 | A "polysemantic comma neuron" (top-k autointerp label) in a dense Qwen model is a Colorado neuron; commas store a running summary ("summary motif"). Steering -> hiking. | "standard top-k automated interpretability lists as a "polysemantic comma neuron"... it turned out to track Colorado" (431); "Steering it made the model want to go hiking." (431); "The first three commas do not fire; once Denver appears, each comma fires, reaching its strongest after green chile." (433) | - | moderate (activation pattern + steering sample) |
| C19 | Attention "seems to collect on the punctuation" (summary motif), generalizing across many neurons. | "In general attention seems to collect on the punctuation, which we call the summary motif." (431) | - | asserted (general claim, one example here) |
| C20 | Short contexts made long-context neurons look polysemantic. | "two paragraphs felt like enough. But this accidentally made all the long-context neurons look polysemantic." (443) | - | moderate (methodological report) |
| C21 | Dataset breadth resolved an "arbitrary mess" neuron (health SEO spam signs). | (452) | - | weak-moderate (anecdote) |
| C22 | "Hundreds of cases" resolved, and superposition kept retreating (weak activations, combinations, unseen neurons, across layers). | "Across hundreds of cases like these, nothing shook my belief in superposition. It just kept moving." (454) | "hundreds" | asserted-only (no table) |
| C23 | Selection bias acknowledged as the alternative explanation. | "Unless this was some dramatic extended case of selection bias" (456) | - | caveat |
| C24 | Superposition should be the last hypothesis: most radical, least testable; its symptom matches bad tools, unfollowed RG, bad architecture, misunderstood generalization. | (458) | - | argument |
| C25 | Prior field evidence for superposition was thin; SoLU paper said so; its own evidence was "circumstantial". | quoted SoLU: "superposition is often treated as the default hypothesis simply because it seems intuitively more compelling than other explanations, but there is little evidence." (461); footnote 5 reinterpretation (461) | 2022 | moderate (citation + reinterpretation) |
| C26 | No superposition circuit found in a real network since the author's original one (which was an error). | "To my knowledge, no one has found a superposition circuit in a real network since my original one, which was an error." (461) | - | asserted (absence of evidence; no search protocol) |
| C27 | The "explanation of the gaps" risk is mitigated because alternatives are testable and real explanations are narrow. | "Superposition's only symptom is that something doesn't make sense." / "real explanations tend to be narrow and easily testable" (463) | - | argument (good epistemics; not quantified) |
| C28 | Recursive generalization is easy to check with training checkpoints. | "it's easy to check if you have training checkpoints. I now think superposition should be far down the list." (465) | - | asserted (method implied) |

Cross-references that bear on these claims (not my range): offshoots "both rarer and less important in their own context than the main activation is in its" and explicitly "not sleeper agents" (1177, 2432); memorizing "umbrella = bee" in a 7.06M-param model takes nine steps and reuses existing bee neurons in the last three blocks ("an off-ramp between two routes the network already has", 843-859); RG predicts a narrow, "hard to vary" shape in semantic space and time (2445).

---

## 3. Methods (reimplementable detail)

**M1. Growth tracking over checkpoints (core test of RG vs superposition).** Retrain (or use public checkpoints of) a model; for a target neuron, at each checkpoint compute its top-k dataset examples; cluster/label them (e.g. "yellow flowers", "balls", "dogs"); plot each cluster's share of the top-k over training (the "grey band" = share of strongest images, l.279). RG predicts: new clusters appear adjacent to existing ones (sharing a facet with already-covered examples), in order. Superposition predicts: unrelated clusters appear without a bridge. Compare architectures on the same data (InceptionV1 vs ConvNeXt, l.281) to measure spread. For LLMs: Pythia / OLMo / similar models with public intermediate checkpoints make this directly doable.

**M2. Route split ("grouped by route share of the top 100", l.311-351).** For one neuron:
1. Take its top-100 activating contexts.
2. For each, attribute the neuron's pre-activation to upstream neurons (e.g. gradient x activation, or direct path attribution through the residual stream with attention patterns frozen). The display names the dominant sources as "comes in through" layer + explained neuron (e.g. "L31 Mars, planets", "L6 names like Cesium").
3. Cluster contexts by their top upstream contributors; report each cluster's share (44/42/6/8%).
4. For each cluster, record downstream effects: later neurons it "wakes up" (up-arrow, e.g. L37 "JavaScript libraries") or suppresses (down-arrow, L37 "space news"), and output tokens it "pushes toward" (".js, objects, software"). Because a neuron's direct output vector is fixed, cluster-specific "pushes" must come from context-dependent downstream effects (ablation or gradient-based total effect, averaged per cluster) - my inference, not stated.
5. A cluster whose input route is distinct (here: early lexical L6 vs mid-late semantic L28-L31) and whose downstream readers differ is an offshoot "arriving by its own route".
The neuron's own layer is not stated; inputs come from L6-L32 and downstream effects at L34-L37, so it sits around L33 (inference).

**M3. Decode-before-you-judge.** For apparently junk activations, apply transforms (Base64 decode, transliteration/translation, tokenization inspection) and re-check whether the decoded content matches the neuron's main job ("pr" neuron, l.409-429).

**M4. Look at the right positions (summary motif).** When a neuron fires on punctuation, read the surrounding sentences, not the token; check whether firing begins only after a topical cue (commas dark until "Denver", strongest after "green chile", l.433).

**M5. Steering check.** Add the neuron's output direction at increased activation and compare generations (baseline "library... grandmother... gardening" vs steered "mountains and do some hiking", l.435-437). Narrow explanations make sharp, falsifiable steering predictions (l.463).

**M6. Context-length and dataset-breadth controls.** Re-run explanations with expanded context windows ("Expand context", l.447-450) and broader corpora (health SEO spam, l.452) before declaring a neuron polysemantic.

**M7. Differential diagnosis ordering (l.395-405, 458-465).** For an unexplained neuron, test in order: better tool -> better explanation -> retrain with better architecture -> follow branches over checkpoints (RG) -> only then superposition.

---

## 4. Weaknesses, caveats, ways the argument could be wrong

1. **"Local" is not operationalized.** RG vs superposition hinges on local vs non-local groupings (l.364), but no distance measure is given. With multi-hop chains ("iy" -> "diy" -> "do it yourself"), almost any pair can be linked post hoc. That is exactly the "explanation of the gaps" risk (l.463). The appendix's "hard to vary" defense (2445) needs checkpoint data, which is absent for frontier LLMs. Risk of circularity if the model's own semantics define "local".
2. **Most LLM evidence here is post hoc, not growth-tracked.** The checkpoint-based observations (C1, C3) are vision models. The LLM cases (geology, pr, Colorado) are explained in finished models; they show "not arbitrary", not "grew by RG".
3. **Sample sizes and selection.** "every neuron I looked at" (277) and "hundreds of cases" (454) have no denominator, sampling protocol, or blind rating. The author flags selection bias himself (456).
4. **Offshoots can dominate the top of the list.** In the geology neuron, the top four displayed activations (72, 62, 61, 59) are code, versus 54 for the geology items (295-309). The claim elsewhere that offshoots are "rarer and less important" (1177) must mean causal importance or frequency, not activation magnitude. Any monitor that thresholds a neuron's activation will fire hardest on the offshoot.
5. **Several key figures are illustrations.** "iy" (287) and "pr" (429) are labeled conceptual/illustration; the 32-things neuron panel (382) is conceptual.
6. **Models are under-specified.** "a frontier language model" (409), "a dense Qwen model" (431), and the geology neuron's model is not named in this range.
7. **The "more features than dimensions" sense is deferred** (389). That is the sense most relevant to SAEs and linear probes. If alignment-relevant concepts (deception, sabotage intent) are distributed by composition across many neurons, a neuron-level reader still needs to combine neurons. "Already clean" at the neuron level does not mean "one neuron per monitor-relevant concept".
8. **Weak activations are unresolved.** Superposition "would move to the weak ones" (454); footnote 5 concedes "meaning shifts in every direction at once as activations weaken" (461). An adversary might be able to hide signal in weak activations or in neuron combinations.
9. **Absence of evidence.** "no one has found a superposition circuit in a real network" (461) has no defined search procedure, so it can't be falsified as stated.
10. **Adversarial and optimization-pressure regimes are untested.** All observations are of models trained on natural objectives. Whether a model under pressure from a neuron-level monitor (or a deliberately implanted backdoor) stays "clean" is not addressed here. The umbrella-to-bee result (843-859) is encouraging for naive memorization, but it is not an adversarial test.
11. **Steering evidence is qualitative.** One baseline/steered pair (435-437); no effect sizes.

---

## 5. Open questions

- Can RG be confirmed quantitatively? Using models with public checkpoints (Pythia, OLMo), what fraction of polysemantic neurons trace back to one local origin, with branches appearing in order? What is the rate of non-local jumps (the superposition signature)?
- Can "locality" be measured non-circularly, for example with an external embedding model, human ratings, or graph distance in an attribution graph?
- Does route-split clustering separate facets reliably at scale? Are route clusters semantically coherent, and does the offshoot always arrive via a distinct (often earlier, more lexical) layer?
- What "pressure keeps branches from overgrowing" (2432), and can architecture or training remove offshoots (the "easy fix" hoped for, 2434)?
- Does the summary motif carry over to agentic transcripts, i.e. do newlines, tool-call boundaries, and end-of-turn tokens hold running "what is going on" state?
- Do neurons in general read through encodings (Base64, other scripts, ciphers), as the "pr" neuron does?
- **When a backdoor, sleeper-agent behavior, or reward hack is trained in, does it attach as a local offshoot or route switch on existing machinery (detectable), or as an isolated superposed feature (the bad case)?**
- **Under optimization pressure against a neuron-level monitor (e.g. RL with the monitor in the loop, or obfuscated-activation attacks), does the model shift computation into weak activations or non-local packing? Can a "locality score" detect that shift?**
- Do weak activations carry causally important information?

---

## 6. Control hooks (white-box monitor ideas grounded in this section)

H1. **Route-conditioned neuron reading.** Do not threshold raw activations. Attribute each firing to its upstream route (M2) and alert only when the firing comes through the alarming route. This cuts false positives from offshoots, which can sit at the top of the activation list (C8). Example: a "security vulnerability" neuron firing via a "writing exploit code" route vs a "discussing CVEs" route.

H2. **Backdoor detection by route-share diffing.** RG and the umbrella-to-bee off-ramp (843-859) predict that new behavior attaches to existing nearby machinery. So compare a suspect fine-tuned model with its base: for behavior-relevant neurons (e.g. "insert subtle bug", "conditional on date or trigger"), compute route-share distributions on the same prompts. New routes, especially from early lexical layers like the L6 Cesium input, are candidate triggers. This is neuron-level model diffing.

H3. **Training-time growth monitoring for reward hacking.** "easy to check if you have training checkpoints" (465). Labs keep RL checkpoints. Track neurons such as "tests passing", "grader", and "special-casing" across RL steps, and flag when a branch grows toward "hardcode expected output" or "edit the test". This catches reward hacking as it forms, before transcripts show it.

H4. **Encoding-invariant concept detection.** The "pr" neuron fires through Base64 and Bengali (409). If concept neurons for "exfiltrate", "credentials", "disable monitoring" also fire through Base64, ROT13, or other languages, a neuron monitor would beat a transcript monitor against obfuscated payloads without needing to decode first. **Direct experiment:** encode malicious strings, compare neuron vs LLM-monitor AUROC.

H5. **Read summary positions.** Context-state neurons fire on punctuation once a theme is established (Colorado commas, 431-433). A sabotage-intent or "I'm being evaluated" state may light up on commas, newlines, or tool-call delimiters rather than on incriminating tokens. Pool monitor features over summary positions, and use onset ("commas dark until Denver") to timestamp when the model's state switched.

H6. **Causal validation of monitor neurons by steering and ablation.** Narrow explanations are testable (463). For each monitor neuron, steer it up (does the model start sabotaging or hedging?) and ablate it (does sabotage stop?). This gives a monitor whose features are causally verified and doubles as an intervention, i.e. a white-box "defer/resample" lever in a control protocol.

H7. **Unexplained-activation mass as an anomaly score.** If ~90% of neuron poles have one main job and only ~2-4% are not understood (l.50), and superposition is the last hypothesis, then activation mass on unexplained neurons or unexplained routes during a trajectory is itself a signal. Flag trajectories with unusually high unexplained mass for audit.

H8. **Explanation corpus must match the deployment distribution.** Long-context neurons looked polysemantic with two-paragraph windows (443), and the SEO-spam neuron needed broad data (452). A control monitor needs neuron explanations built on long agentic transcripts that include attack trajectories (ControlArena, APPS-backdoor, BashBench-like). Otherwise the neurons that matter will be mislabeled as noise.

H9. **Naive autointerp labels will mislead monitors.** "polysemantic comma neuron" (431) and the code-topped geology list (295-301) show that top-k labeling picks the wrong job. Budget for context-aware, route-aware, steering-validated labels in the monitor pipeline. This is a cost item.

H10. **Locality as a robustness metric against adaptive attacks.** If an untrusted model is trained to evade a neuron monitor, RG predicts its evasion still has to grow from nearby machinery (cheap and fast), while true non-local packing is "slower to learn" and "more fragile" (851). Measure the locality of any new evasion mechanism. If evasion requires non-local packing, it should cost more training and leave a detectable signature, which is the key falsifiable bet for "white-box beats black-box".

### Concrete control-game sketch (win/lose/continue)
- **Setting:** an APPS/ControlArena-style backdoor task. The untrusted model is an open-weight coder (Qwen3 family, which matches the essay's Qwen audits). Attack policy: insert a backdoor that passes tests but fails on a secret input.
- **Monitors:** (a) black-box: a trusted weaker LLM reads code and transcript; (b) white-box: a curated neuron set (H1, H5, H6, H7) with route split; (c) ensemble.
- **Metrics:** safety at a fixed audit budget (1-2%) vs usefulness; AUROC per monitor; also under obfuscation (Base64 or comments in another language, H4).
- **Escalation:** fine-tune the attacker against monitor (b) and measure the drop in safety and the locality of the new mechanism (H10).
- **Win condition for "white-box viable":** (b) or (c) beats (a) at equal cost, and keeps an advantage after adaptive training.
