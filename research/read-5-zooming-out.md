# Deep read 5: "Zooming Out" + Appendix (lines 1414–1998)

Source: Nick Cammarata, "Neural Networks Are Already Clean" (Goodfire, ~Oct 2026), plain-text extraction at `source/already-clean.txt`. Framing read: lines 29–99 ("The Short Version"). Range read in full: 1414–1998. Cross-references outside the range are marked **[xref]**. Figures are missing from the extraction; interactive-figure captions and tables survive.

Sections covered: What I Mean by Clean (1416–1436) · Motifs Over Monosemanticity (1438–1452) · A City vs a Knot (1454–1510) · What a Solution Might Look Like (1512–1528) · Appendix: A Note on "Superposition" (1538–1549) · On Simulation Scores (1553–1555) · Feature Visualization in Later Layers (1559–1565) · Separating the Sign Regimes (1569–1592) · Looking at the Residual Stream (1596–1658) · Weak Activations: Further Measurements (1662–1855) · Missing Curves (1859–1881) · Where Adversarial Examples Go (1885–1899) · Memorization and Composition (1903–1957) · Social Security: Detection and Use (1961–1995).

---

## 1. Plain-English summary

The closing sections are mostly a manifesto, and the appendix supplies the supporting evidence.

**Manifesto (1414–1528).** "Clean" does not mean every neuron is perfectly single-purpose. It means the network's parts are **built to be read by its own downstream layers**, so interpretability should aim to "become another reader" (1422). The author contrasts *enumerative* interpretability (build a complete feature list and audit it) with *exploratory* interpretability (start from questions and move between neurons, attention heads, attribution graphs and training dynamics), and argues for the second (1430–1436). He says he would rather understand circuit **motifs** for a few alignment questions (agent psychology, persona selection, goals, self/other boundary) than have every neuron be monosemantic (1442). Bigger networks are like cities: easier to navigate than small towns (1458). SAEs and probes "fracture" the network or only answer questions already asked, so they belong "at the end, not the start" (1489–1491). The safety-relevant point is at 1496: *"Deception might hide from someone reading a model's outputs, but it has no reason to hide from the model's own circuitry."* His worry is not that deception hides in a missed weak activation. It is that deception will be "in plain sight" and we won't know how to read it. The proposed "solution" is a lab of automated scientists watching training and inference, guided by a "mechanistic constitution" (1518–1522). Alignment could then proceed through many simple fixes, "like removing an RL environment that turns out to be toxic, without pushing gradients through the very tools we use to see" (1526).

**Appendix evidence (1530–1995).**
- **Sign regimes.** In SwiGLU neurons (a = SiLU(g)·v), negative×negative produces positive output, so one neuron can fire for two reasons. In a Qwen 3.6 "enemy" neuron, 131/133 mid-range (p75–p99) responses are −×− and 93/93 top (≥p99.99) responses are +×+ (1576).
- **Residual stream.** One coordinate (112) holds 94.5% of raw energy at one ConvNeXt layer and acts as a normalization/saliency signal. Remove it from projections and use it as a color instead (1598–1632). Layer-readout views show that "a triggered sleeper, an instruction, and a persona can change when the answer settles" (1650). The text gives no numbers for this; the figure is missing.
- **Weak activations.** Zeroing weak activations matters a lot in early layers and little in late layers. Keeping roughly the top quarter in Inception's last layer gives 69.47% vs 70.08% accuracy. Applying the same cutoff at all ConvNeXt blocks at once is catastrophic (medium drops to 3.80%) (1847–1849). Spot checks suggest weak activations are semantic broadenings, but "We don't yet have a semantic test for weak activations that we trust" (1853).
- **Missing curves.** SAE "missing curve detectors" decompose into existing curve neurons (97.2–98.0% "in curve neurons"). An SAE trained only on curve activations uses 84k of its 100k dictionary items, which suggests that SAEs inflate the count of building blocks (1868–1881).
- **Adversarial examples** go through ordinary circuits. An attack that makes a skull read as a jaguar recruits real jaguar neurons (1889–1897).
- **Memorization.** A Poe neuron sets up a literary context. Zeroing it drops P("dreary") from 87% to 50%, while removing only its direct effect leaves 85%, so the neuron mostly steers downstream computation (1905, 1921). Zeroing outputs whenever the gate exceeds its ordinary-text p99.9 destroys recitation: the model denies Psalm 23 exists and invents a "Republic of Luzang" declaration. Random matched interventions do not (1925–1957).
- **Social Security.** The famous 3-neuron sparse probe from *Finding Neurons in a Haystack* detects the phrase perfectly (held-out AUC 1.00). Removing those neurons does almost nothing to next-token prediction (−0.004 nats; helps 81 cases, hurts 83). The model actually uses a different, ordinary circuit of lexical, form-field, retirement-domain and output-vote neurons, including a "401(k) rival" (1963–1993). **What a probe can detect is not necessarily what the model uses.**

---

## 2. Claims (with exact evidence, line numbers, strength)

Strength scale: **strong** = experiment with numbers and a control; **moderate** = experiment/example with numbers but n≈1 or no control; **weak** = qualitative example or anecdote; **asserted-only** = argument or opinion.

### Zooming Out (manifesto)

| # | Claim | Evidence (line) | Numbers | Strength |
|---|---|---|---|---|
| Z1 | "Clean" means parts are built to be read by downstream readers; interpretability should "become another reader." | "I mean that a network's parts are built to be read, and built upon, by its downstream readers… become another reader." (1422) | — | asserted-only |
| Z2 | Organization emerges because it is cheaper to extend existing structure (related to circuit racing / gradient starvation). | "it's easier to add the marginal car there than to build a second car area somewhere else" (1426) | — | asserted-only (speculative) |
| Z3 | LMs sit between monosemantic and arbitrary: most neurons mean mostly one thing, some mean a few. | "most neurons meaning mostly one thing, some meaning a few" (1428) | [xref 50: ~90% / ~7% / ~2–4%] | asserted here; moderate via xref |
| Z4 | Exploratory interpretability holds up better against polysemanticity than enumerative, and makes "more features than dimensions?" mostly irrelevant. | "This approach is far more resilient to polysemanticity." (1432); "Questions like 'are there more features than dimensions?' are mostly irrelevant." (1434) | — | asserted-only |
| Z5 | The author would trade universal monosemanticity for motifs on a few safety questions. | "I'd take the motifs in a minute." (1442) | — | asserted (preference) |
| Z6 | Lessons for his past self: pose circuit; negative poles act as gates; feature visualization reward-hacks in late layers; a messy last layer signals bad architecture; "look harder" at polysemanticity. | 1446 | — | asserted here (backed elsewhere in essay) |
| Z7 | Recursive generalization vs superposition matters because only generalization-born groupings "teach" something. | "Following the noise only works if the noise has something to teach." (1450) | — | asserted-only (logical argument) |
| Z8 | Bigger networks are easier to navigate: agents found labeled dog-ear neurons faster in larger ConvNeXts. | "agents found labeled dog-ear neurons faster in the larger models" (1458); ear family at Small 92k / Medium 7.06M / Large 28.6M, "vary in size about 300×" (1460–1468) | sizes only, no timing data | weak |
| Z9 | The killer-whale "family" in the ConvNeXt atlas is three routes. | "one for whales, one for sharks and rays, and one for fish held up by anglers" (1471) | — | weak (example) |
| Z10 | An SAE fractures the 4e:55 "V" into a car feature and a cat feature. | "An SAE trained on the layer fractures it the same way, splitting the V into a car feature and a cat feature." (1489) | — | weak (asserted example) |
| Z11 | Probes can only answer questions we already have. | "they can only answer a question we already had" (1489) | — | asserted-only |
| Z12 | Everything probe- or SAE-like that the author has run, **and changes from training (including on-policy self-distillation)**, breaks down into highly interpretable neurons. | "Everything of this kind I've run breaks down into highly interpretable neurons, as do the changes training makes, including on-policy self-distillation." (1491) | none shown | asserted-only (high-value if true) |
| Z13 | The bar for "monosemantic" keeps moving: 40 pages on 10 curve neurons still didn't convince some readers. | "we wrote forty pages of experiments on ten neurons" (1494) | 40 pages / 10 neurons | anecdote |
| Z14 | **Deception should be readable from circuitry because downstream readers must be able to read it.** Past errors were misreadings, not missed hidden activations. | "Every error discussed in this essay was something hiding in plain sight… None was a hidden activation we missed. Deception might hide from someone reading a model's outputs, but it has no reason to hide from the model's own circuitry. It needs to be accessible to its readers, and if we become a reader, it should be accessible to us too." (1496) | — | asserted-only (key control claim) |
| Z15 | Attention moves information to reliable places, so neurons fire *near* the "appropriate token" rather than on it. | 1498 | — | weak (experience) |
| Z16 | No level of abstraction has been found where understanding breaks down. | "I haven't found one." (1502) | — | asserted-only |
| Z17 | The cat/car neuron's "V" is easy to see (about 5 seconds). | 1502 | ~5 s | anecdote |
| Z18 | The errors are asymmetric: assuming "clean" and being wrong costs less than assuming "packed" and being wrong. | 1504 | — | argument |
| Z19 | The medium ConvNeXt map is "mostly filled in" with no interpretability-specific fixing of the network. | 1506 | — | asserted (supported elsewhere by microscope) |
| Z20 | Frontier LMs are where vision models were 8 years ago; agents might do in months what took humans a decade. | "They may be able to do in months in frontier language models what took humans most of a decade for vision models." (1508) | — | speculative |
| Z21 | Solution = automated-scientist lab watching training and inference under a "mechanistic constitution." | 1518–1524 | — | vision/asserted |
| Z22 | If we can read models, alignment may become many simple fixes, e.g. removing toxic RL environments **without training against the interpretability tools**. | "removing an RL environment that turns out to be toxic, without pushing gradients through the very tools we use to see" (1526) | — | asserted-only |

### Appendix

| # | Claim | Evidence (line) | Numbers | Strength |
|---|---|---|---|---|
| A1 | The essay's definition of superposition: "neurons learning unrelated things together because they rarely interfere", as opposed to "more features than dimensions" (Toy Models). | 1541–1547 | — | definitional |
| A2 | The original Zoom In superposition circuit was wrong for two reasons: a misread generalized pose circuit, and feature-visualization reward hacking. | 1541 | — | asserted here (main text has evidence) |
| A3 | Agents' web readers can't get past a base64 figure in Olah 2023's composition/superposition note, which may bias automated researchers' notion of superposition. | Footnote 6: "None of the agents we tried could read past it, as of this writing." (1543) | — | anecdote (tooling hazard) |
| A4 | "Composition also represents far more things than it has neurons, and that's exactly what we should hope for." | 1547 | — | asserted |
| A5 | Simulation scores mainly measure attention placement and weak-activation fine detail, and LMs are bad at outputting precise values, so they are a poor starting metric. | "Simulation scores often end up measuring where attention puts information" (1555); Trump-neuron size-falloff example (1555) | — | argument with examples |
| A6 | Free feature visualization in late InceptionV1 layers draws dogs even when the circuitry carries car information. | 1561 | — | weak/moderate (example) |
| A7 | Path-guided visualization fixes this: bias optimization toward the paths taken by top dataset examples, often only for the first 64 steps. | "often only for the first 64 steps, which was usually enough… you just need to get out of the dog basin." (1563) | 64 steps | method; moderate |
| A8 | Of 4c:447's four readers, under guided visualization two are car neurons and two share a pose between cars and dogs. | 1565 | 2/2 | weak |
| A9 | **SwiGLU double-negative regime:** in the "enemy" neuron (Qwen3.6-35B-A3B L36·E206·N103), the noisy middle of the range is −×−, and the strongest tail is +×+. | "131/133 responses in p75–p99 use − × −. The strongest tail uses + × +: 93/93 at p99.99 and above." (1576); "The audit sampled 750 quantile-stratified examples; 626 retained routing." (1579) | 131/133; 93/93; 750 sampled / 626 routed | moderate (n=1 neuron, clear counts) |
| A9x | [xref] About 4% of neurons have a top list dominated by the −×− "echo". Ablating them network-wide raises most benchmarks but lowers some reasoning ones. | "for about 4% of neurons, it's the whole top of the list. Ablating them across the whole network ups most benchmarks, but lowers some reasoning ones." (~1178) | ~4% | moderate/asserted |
| A10 | One residual coordinate can dominate geometry and act with LayerNorm as a saliency signal. | "Coordinate 112 — 94.5% of the raw energy at this layer." (1614–1616); "Medium ConvNeXt, epoch 90, stage 3 block 8"; "4,000 image locations"; "Gain is 1 / √(channel variance + 10⁻⁶)" (1627–1632) | 94.5%; 4,000 points | moderate (one layer) |
| A11 | **Layer readout timing:** a triggered sleeper, an instruction and a persona each change *when* the answer settles across layers. | "A triggered sleeper, an instruction, and a persona can change when the answer settles." (1650); caveat: "useful clues for tracing mechanisms, rather than a test of a model's 'true personality.'" (1658) | none in text (figure missing) | weak in text (figure data unavailable) |
| A12 | Strong responses preserve late-layer accuracy, and weak-activation removal hurts early layers far more than late ones. | Inception (baseline 70.08%): conv2d0 p75 −22.4, p99 −66.6; mixed5b p75 −0.60, p99 −33.6 (1675–1699) | full tables below | strong (systematic sweep, 4 models) |
| A13 | ConvNeXt single-block cutoffs are tolerated with the residual bypass intact, but all-block cutoffs are catastrophic. | "At p99, medium falls to 3.80% accuracy and large to 27.78%" (1847); all-blocks rows: small −13.3, medium −68.3, large −46.3 at p99 (1746, 1793, 1840) | see table | strong |
| A14 | Keeping roughly the strongest quarter of positive activations in Inception's final layer preserves 69.47% vs 70.08%. | 1849 | 69.47 vs 70.08 | strong |
| A15 | Weak-activation changes look like finer distinctions, not lost unrelated features. | "the changes looked like finer distinctions rather than the loss of a wholly unrelated feature." (1851) | — | weak (inspected cases) |
| A16 | Enemy-neuron weak responses broaden semantically (adversary words in other languages → nearby mentions, combat, games, competition), and near zero, unrelated examples dominate. Spot checks can't settle the general question. | "We don't yet have a semantic test for weak activations that we trust" … "Broader category-based screening gives mixed results, so these spot checks cannot establish what weak activations mean in general." (1853) | — | weak (author-acknowledged) |
| A17 | Gorton's (2024) SAE "missing curve detectors" decompose into existing curve neurons. | SAE 5430 → 3b:343 (+202), 3b:357 (+14)… "97.5% in curve neurons"; SAE 5996 → 3b:330 (+144), 3b:380 (+122) "98.0%"; SAE 1634 → 3b:380 (+143), 3b:342 (+120) "97.2%" (1864–1880) | 97.5 / 98.0 / 97.2% | moderate (3 features; metric not defined) |
| A18 | SAEs over-generate building blocks: an SAE trained only on curve activations uses 84k of 100k dictionary items. | 1881 | 84k/100k | moderate |
| A19 | Adversarial examples take ordinary routes: skull→jaguar silences 6 skull neurons and turns on real-jaguar inputs at about ¼ strength (ConvNeXt). | 1889 | 6 neurons; ~¼ strength | weak/moderate (n=1) |
| A20 | A robust InceptionV1 attack (budget 32/255, survives jitter/scale/rotation) paints cat face and spots, and 9 of 10 real-jaguar neurons become much more active. | 1891, 1897 | 9/10; 32/255 | moderate (n=1) |
| A21 | Circuit ecology: "even a nonsensical objective can recruit machinery that already does something useful toward it". Established routes have a head start in capturing residual error. | 1899 | — | asserted interpretation |
| A22 | **Context neurons mostly act indirectly:** zeroing the Poe neuron drops P(" dre") from 87% to 50%, but removing only its direct output contribution leaves 85%. | 1905; "Zero the Poe neuron: 87% → 50% · Zero the literary neuron: 87% → 70%"; "Restoring the downstream literary neuron partly rescues the completion, to 57%." (1921–1923) | 87→50; 85; 87→70; 57 | moderate (single prompt, clean numbers) |
| A23 | Poe/gothic neuron gate reaches 2.00 vs its usual p99.9 of 0.89. Literary-context neuron: gate +2.31, output −4.34. Upstream contributions: Earlier Poe context +0.97, Midnight phrases +0.30, Gothic atmosphere +0.14, and Poe→literary +0.57. | 1913–1916 | as listed | moderate |
| A24 | **Memorized recitation lives in extreme responses:** zeroing outputs whenever the gate exceeds ordinary-text p99.9 makes Qwen3.6 deny Psalm 23 exists. Random interventions matched by count or magnitude preserve the verse. Some arithmetic and summarization survive, while coding and other answers degrade. | 1925; outputs at 1935–1943 (Psalm: "Exact verse · 12 output tokens" vs denial, then repeats "fictional poem, fictional myth" to 400-token limit); Declaration: 238 correct tokens vs "The Republic of Luzang, established on 1999…" (1949–1957) | p99.9; 12 / 400 / 238 / 146 tokens | moderate (one saved experiment with matched random controls) |
| A25 | **Detection ≠ use:** the 3-neuron Haystack probe (Pythia-1B-v0 L2:611, L2:4081, L2:6819) detects "Social Security" with held-out AUC 1.00, but removing all three changes next-token log prob by only −0.004 nats on average (helps 81, hurts 83). | 1966–1977 | AUC 1.00; −0.004 nats; 81/83 | strong-ish (clear numbers; small model; single phrase) |
| A26 | The probe neurons are ordinary lexical continuers: word-form branch selector (liturgy/liturgically), canonical-name continuer (Bloom→berg, Gar→min), phrase-frame filler (as simple→as, take sol→ace). Their agreement makes the sum selective. | 1963, 1970–1972 | — | moderate |
| A27 | The circuit actually used for the next token is ordinary lexical, form-field, retirement-domain and output-vote neurons, including competing votes for Social Security vs 401(k). | 1981–1991: L0:3308 capitalized onset +0.49; L2:7715 bigram closure −0.24; L2:611 lexical bystander ≈0; L3:839 prose/form-field vote +0.58; L5:447 old-age semantic field +0.22; L10:3382 credential/header field −0.24; L12:7260 retirement sharpener +0.40; L13:3673 retirement gate −0.61; L15:3731 says "number" −0.81; L15:7040 specific-content vote −0.75; L15:5759 401(k) rival +0.69. "Eleven of 31 screened neurons… negative = removing it hurts; positive = removing it helps." (1993) | listed | moderate (ablation numbers; screening method unspecified; 11/31 hand-selected) |
| A27x | [xref] Main text: the Haystack authors "thought they may have found superposition in a 'social security' direction, but that direction is unused by the network." | ~1122 | — | as above |

#### Weak-activation table (reproduced, change in top-1 accuracy in percentage points)

Inception v1 (baseline 70.08%; positive ReLU values; each row edits one layer), columns p25/p50/p75/p95/p99:
conv2d0 −0.17/−3.5/−22.4/−59.2/−66.6 · conv2d1 −0.33/−4.4/−20.9/−58.9/−68.6 · conv2d2 −0.10/−0.90/−11.2/−47.0/−64.7 · mixed3a +0.02/−0.72/−5.4/−40.6/−64.6 · mixed3b +0.01/−0.12/−2.1/−24.3/−54.4 · mixed4a −0.02/−0.14/−1.9/−19.7/−49.4 · mixed4b −0.05/−0.21/−2.2/−18.3/−43.9 · mixed4c −0.09/−0.29/−2.0/−18.9/−42.6 · mixed4d −0.04/−0.14/−1.5/−12.5/−33.9 · mixed4e −0.03/−0.04/−0.81/−8.2/−25.4 · mixed5a +0.01/−0.12/−1.7/−13.9/−34.5 · mixed5b −0.04/−0.04/−0.60/−7.7/−33.6 (1675–1699).

ConvNeXt (magnitude of SwiGLU product; residual bypass intact). Per-block cuts are mostly < 1.6 pp except s0·0 in medium (p99 −13.4) and s0·0/s0·1 in large (p99 −3.5/−1.6). All-blocks rows:
- small (baseline 13.73%): −0.08/−0.56/−4.6/−11.7/−13.3 (1746)
- medium (72.08%): −0.01/−0.13/−1.0/−19.1/−68.3 (1793)
- large (74.04%): −0.03/−0.06/−0.55/−9.2/−46.3 (1840)

Arithmetic check: 72.08−68.3≈3.8 (matches "3.80%"), 74.04−46.3≈27.7 (matches "27.78%"), 70.08−0.60≈69.48 (matches "69.47%"). Note: ConvNeXt small's 13.73% baseline is very low. It is likely the 92k-parameter model, so its deltas are compressed.

---

## 3. Methods (reimplementable)

1. **SwiGLU sign-regime audit** (1571–1592). For a gated MLP neuron with a = SiLU(g)·v:
   - Sample about 750 quantile-stratified contexts across activation bands (e.g. p75–p99, ≥p99.99). For MoE, keep only tokens where the expert was routed (626 of 750 here).
   - Label each sample by sign(SiLU(g)) × sign(v) into ++, −−, +−, −+.
   - Report the share of each regime per activation band.
   - Show the regimes as separate "poles" in the neuron viewer instead of mixing them into one ranked list. This does not replace the neuron with a learned decomposition.
   - Cheap: needs only g and v at that neuron.
2. **Residual-stream sink removal for visualization** (1598–1632).
   - Compute per-coordinate share of raw energy (sum of squares) at a layer and flag dominant coordinates (e.g. coord 112 = 94.5%).
   - Project N=4,000 locations (UMAP/PCA) with and without the dominant coordinate, and color by its value.
   - Compute LayerNorm gain = 1/√(var + 1e-6) with and without that coordinate to see how it drives normalization (saliency).
3. **"When does the answer take shape?" readouts** (1638–1658).
   - Per-layer readout with the model's own unembedding (logit lens) and with a fitted lens (tuned-lens-style).
   - Metrics: "Distance to final answer" and "Change per layer".
   - Compare conditions (triggered sleeper, instruction, persona) with ordinary passes, then drill from a band, layer or patch back to the neurons that changed the readout.
   - The authors' caveat: timing and confidence depend on the lens.
4. **Weak-activation cutoff sweep** (1664–1849).
   - For each layer, zero activations below the pXX percentile, using positive ReLU values for Inception or |SwiGLU product| for ConvNeXt (residual left intact).
   - Sweep p25, p50, p75, p95, p99, one layer at a time and also all blocks at once, and measure the change in top-1 ImageNet accuracy.
   - (Ambiguity: per-neuron or per-layer percentile is not specified.)
5. **Graded semantic spot check of weak activations** (1853–1855). Bin contexts from strong positive toward zero and into the negative side, read examples in each bin and label the semantic drift. Repeat on randomly chosen neurons and try category-based screening (which gave "mixed results").
6. **SAE-feature → neuron decomposition** (1861–1881). Express each SAE feature as a weighted combination of the layer's neurons and report the fraction of mass on known curve neurons (97.2–98.0%) and the top contributors. Separately, train an SAE on curve-only activations and count live dictionary items (84k/100k) to show over-splitting.
7. **Path-guided feature visualization** (1561–1565).
   - Take the neuron's top dataset examples and trace their attribution paths.
   - Add an optimization term that rewards following those paths, often only for the first 64 steps, then optimize freely.
   - Any reasonable path nudge works: "you just need to get out of the dog basin."
8. **Adversarial-route tracing** (1889–1897).
   - Run a targeted attack. For the robust version, use budget 32/255 with expectation over jitter, scale and rotation.
   - Compare activations on clean vs attacked images for (a) source-class neurons (skull, 6 go quiet) and (b) neurons chosen for responses to real target-class images (jaguar: about ¼ usual strength in ConvNeXt; 9/10 much more active in InceptionV1).
9. **Total vs direct effect + restoration** (1905–1923).
   - Zero a neuron and measure the target-token probability (total effect).
   - Separately, subtract only its direct contribution at the output (direct effect).
   - Then patch a downstream neuron back to its clean value to measure mediation (87%→50% total; 85% direct-only; restoring the downstream literary neuron → 57%).
10. **Extreme-gate clipping** (1925–1957).
    - Per neuron, compute the gate's 99.9th percentile on ordinary text.
    - At inference, zero the neuron's output whenever its gate exceeds that value.
    - Controls: random interventions matched by count or by magnitude.
    - Evaluate recitation (Psalm 23, Declaration of Independence), arithmetic, summarization and coding.
11. **Detection-vs-use dissection** (1963–1993).
    - Take a sparse k-neuron probe (here k=3, summed) and measure held-out AUC.
    - Ablate the probe neurons and measure the average next-token log-prob change in nats, plus counts helped vs hurt.
    - Independently, screen candidate neurons (31) by summed change in target log-prob when each is removed, keep the high-effect ones (11) and annotate roles by layer band: token lookup (L0–2), style/concept (L3–5), domain gates (L8–13), output votes (L14–15).
12. **Tethered atlas / exploratory agent loop** (1470–1485, 1498, 1518–1522).
    - Activation-atlas-style "islands" per stage, with attribution-flow "roads" between districts, and every zoom level linked to real neurons.
    - Agents run conjecture and criticism across many lenses: upstream/downstream weights, attention, negative pole, steering, and growth over training.

---

## 4. Weaknesses, caveats, ways it could be wrong

1. **The Zooming Out section is mostly asserted.** No metric is given for "map mostly filled in," "can investigate most questions" (1506), or "no level of abstraction where things break down" (1502). Z12 (training changes, including on-policy self-distillation, decompose into interpretable neurons) is a strong claim with no data in the text.
2. **The deception argument (1496) assumes no adversarial pressure on internals.** A model could be trained, or could learn under monitoring pressure, to make safety-relevant computation hard to read. Known results on obfuscated activations show probes and SAE-based monitors can be evaded while behavior is preserved (Bailey et al., 2024, "Obfuscated Activations Bypass LLM Latent-Space Defenses"; external, not in essay). The claim that deception must be "accessible to its readers" only implies that *some* downstream function can read it. That reading can be distributed over many neurons, weak activations, or attention, not one legible neuron. The author does recommend not training against the tools (1526), which partly concedes this risk.
3. **Weak activations matter in aggregate.** Single-layer late cuts are cheap, but all-block cuts at p95/p99 are catastrophic (medium −19.1 / −68.3 pp). The essay admits there is no trusted semantic test for weak activations (1853). A safety-relevant signal could still be spread thinly across many weak activations; the spot checks are of one detailed neuron plus "a few" random ones.
4. **The weak-activation method is under-specified.** It is unclear whether percentiles are per neuron or per layer, and the ConvNeXt small baseline is 13.73%. Accuracy is a coarse proxy for meaning.
5. **Sign-regime evidence is n=1 neuron** (enemy neuron, 626 routed samples). The ~4% figure and the benchmark effects live outside this range (~1178) and are preliminary ("we haven't looked into it deeply").
6. **Readout-timing results (sleeper/persona) have no numbers in the text**, and the authors themselves say the view is lens-dependent and not a test of "true personality" (1658).
7. **Missing-curves metric undefined.** "% in curve neurons" (97.2–98.0%) is not defined: decoder-norm share, attribution share, or activation share? Three SAE features. The 84k/100k result could reflect SAE hyperparameters (L1 coefficient, dictionary size), not just intrinsic over-splitting.
8. **Adversarial example evidence is anecdotal** (one image per model). "Roughly a quarter of their usual strength."
9. **The memorization intervention is not specific.** Coding and "other answers also degraded" (1925), so extreme responses carry more than memorized text. It is one "saved" experiment. The randomized controls are good but the details (layer coverage, number of neurons zeroed) are not given.
10. **The Social Security result** uses a small, old model (Pythia-1B-v0) and a single phrase. "Unused" is measured only as next-token log-prob change from ablating the 3 probe neurons, not as longer-range behavior or ablating the probe *direction* in the residual stream. The headline "Nothing reads the 'Social Security' direction" (1965) is stronger than an ablation of three neurons shows. The sign convention ("positive = removing it helps") makes some role labels counterintuitive (e.g. "Retirement sharpener +0.40" means removing it *helps* the target). Eleven of 31 screened neurons are shown, hand-selected.
11. **Selection and advocacy bias.** Examples are hand-picked. Goodfire is an interpretability company, the essay is explicitly a manifesto ("conjectures about where it all might be pointing", 97), and many numbers defer to an unreleased companion paper.
12. **Vision ≠ frontier LMs.** The strongest "mostly understood" case is a medium ConvNeXt (7.06M params). Extrapolating to frontier LMs "in months" (1508) is speculative.
13. **Simulation-score critique (1555)** is convincing as argument but offers no replacement quantitative metric. "Normal science" is hard to benchmark, which makes the author's interpretability claims hard to falsify or compare.

---

## 5. Open questions raised

1. Can a white-box monitor distinguish a model *representing* a concept (deception as topic) from a model *using* it to drive actions? The Social Security case suggests detection and use come apart (AUC 1.00 vs −0.004 nats), and use-tracing currently needs ablations. Can causal use be checked cheaply at inference time?
2. Do backdoor triggers, instructions and personas reliably shift "when the answer settles" (1650) across models, lenses and trigger types? Can that shift be used as a detector, and does it survive an adversary who trains against it?
3. Is above-p99.9 gate activity a general signature of rote or memorized behavior? Would it flag memorized backdoor trigger→payload mappings or scripted sabotage?
4. What is a trustworthy semantic test for weak activations (1853)? Do safety-relevant behaviors depend on weak bands, which would mean the "missed activation" fear is valid?
5. What is the double-negative regime used for, given that ablating ~4% echo-dominated neurons lowers some reasoning benchmarks (xref ~1178)? Is it a hiding place for computation that monitors keyed to the positive pole would miss?
6. Do RL-induced behavior changes (e.g. reward hacking learned in a "toxic" environment) decompose into interpretable neurons, as claimed for on-policy self-distillation (1491)? Can toxic environments be identified from neuron diffs (1526)?
7. What is the "mechanistic constitution" (1522)? It is not specified anywhere in the range.
8. Which motifs answer the author's chosen safety questions: agent psychology, persona selection model, goals, self/other boundary (1442)?
9. How fast does map coverage grow with agent compute on a frontier LM? Is there a coverage metric that could tell us when a model is "readable enough" to monitor?
10. Do attacks on a white-box monitor necessarily recruit existing circuitry, by analogy with adversarial examples (1899)? Would that make them detectable as evidence/conclusion mismatches?
11. Can agentic interpretability pipelines be undermined by tooling blind spots (footnote 6: base64 blocks truncating readers), or deliberately by a sabotaging model that does the interpretability?

---

## 6. Control hooks (white-box monitor ideas grounded in this section)

The goal is a neuron-level, "already-clean" monitor that beats a black-box LLM monitor reading transcripts in a control game (backdoored code, sabotage, reward hacking, sandbagging, deception).

**H1. Read what the model reads (1422, 1496).** The core thesis behind white-box control: deception "has no reason to hide from the model's own circuitry." A transcript monitor sees only outputs, while a reader-aligned monitor sees the internal context that downstream layers consume. Concretely, monitor neurons with high *total* causal effect on the action tokens, not probe-decodable directions.

**H2. Two-stage monitor: detect, then verify use (Social Security, 1963–1993).** A probe can score AUC 1.00 on a concept the model doesn't use for its next token. A deception or "insert backdoor" probe could likewise fire on topic mentions (false positives on benign security code) and miss the circuit that actually writes the backdoor.
- Stage 1: cheap neuron watchlist and probe screen.
- Stage 2: on flagged steps, attribution or ablation of candidate neurons against the *action* tokens (e.g. the backdoor-inserting line), and escalate only if the suspicious neurons causally drive the action.
- This maps onto control protocols' "audit budget": stage 2 is the expensive audit.

**H3. Context-setting neurons act indirectly (Poe: 87%→50% total vs 85% direct-only, 1905–1923).** Neurons that encode situational context ("this is an eval", "no one is watching", "I am in persona X") may barely touch the logits directly and steer everything downstream. Monitors based on direct logit attribution or output-adjacent layers will miss them. Use total-effect and mediation measures. Candidate monitor: track mid-layer *context* neurons for eval-awareness and oversight-awareness, the conditions under which a schemer would defect.

**H4. Settling-depth anomaly detector (1650).** "A triggered sleeper, an instruction, and a persona can change when the answer settles." Compute per-token layerwise readouts (own unembedding and fitted lens) and features like the layer at which the top-1 settles, distance-to-final per layer, and late reversals.
- Backdoors: a triggered sleeper may settle at an unusual depth.
- Sandbagging: the correct answer may form at mid-depth and then get overwritten late. That is a "knows but withholds" signature, related externally to Halawi et al. 2023, "Overthinking the Truth".
- Caveat (1658): lens-dependent, so calibrate on clean passes.

**H5. Extreme-gate census (1925–1957).** Calibrate each neuron's gate p99.9 on ordinary text, then count above-threshold events per step.
- (a) An anomaly signal: rote or memorized routines, possibly including memorized trigger→payload mappings, run on extreme responses.
- (b) A causal *intervention test* ("clip-and-compare"): re-run the step with extreme gates clipped. If a suspicious behavior vanishes while matched random clipping leaves it intact, it depends on memorized machinery.
- (c) A sandbagging and unlearning probe: when the model claims ignorance, check whether the knowledge-bearing extreme gates fire anyway. A model with knowledge removed confabulates a *confident denial* (Psalm 23 "is not a known… work"; "Republic of Luzang"). That warns that output text alone can't distinguish "doesn't know" from "won't say", while internals might.

**H6. Sign-regime-aware features (1571–1592; xref ~1178).** Monitors keyed to a neuron's positive activations will mix two mechanisms: +×+ (the real job) and −×− (the echo, which fills the noisy middle). Split every watched SwiGLU neuron into four sign channels, alerting on the +×+ strong tail and treating −×− separately. This lowers the false-positive rate. Open: −×− might carry reasoning-relevant computation, since ablation lowers some reasoning benchmarks.

**H7. Strip sink coordinates before residual-stream probing (1598–1632).** One coordinate can hold 94.5% of energy and drive LayerNorm gain. Residual probes or anomaly detectors that don't remove or normalize sink dimensions will be dominated by saliency and position artifacts. Use the sink value as a separate feature.

**H8. Evidence-vs-conclusion consistency checks (adversarial routes, 1889–1899).** Attacks recruit real downstream circuitry ("jaguar" neurons at about ¼ strength) while upstream evidence neurons stay quiet or don't match. A monitor can flag cases where conclusion or action neurons fire without the usual upstream support pattern. Possible uses: catching jailbreaks, adversarial inputs to the monitor, and "unjustified" decisions such as inserting a branch for a specific magic input. Also, by "circuit ecology" (1899), reward hacking and sabotage likely reuse existing circuits (e.g. test-special-casing, "making the checker pass"), which can be found and labeled offline.

**H9. Model-diff monitoring of training (1491, 1526).** If the changes training makes decompose into interpretable neurons, then diffing neuron activations or weights before and after an RL environment could expose the environment that teaches reward hacking or deception. The fix would be to remove that environment rather than train against the monitor. **Do not push gradients through the monitor** (1526). This preserves monitor validity (cf. obfuscation under optimization pressure; external).

**H10. Cost: watch strong activations in late layers (1849).** Late-layer weak activations are mostly expendable for task accuracy (Inception last layer: top quartile keeps 69.47/70.08). A cheap monitor can sparsify by reading only strong responses in late layers. Caveat: all-block weak cuts are catastrophic, so weak signals matter collectively; keep a residual "weak-band" anomaly score.

**H11. Exploratory offline, enumerative online (1430–1442, 1518–1522).** Run the author's agent lab offline on the untrusted model to build a curated watchlist of motifs for the safety-relevant questions (agent psychology, persona selection, goals, self/other boundary), with neuron-level grounding. The online monitor is then a small enumerated set plus the H2 causal verification. An agent "interrogation" pass on flagged trajectories (ablate, steer, re-run) gives a white-box analogue of resample/defer protocols.

**H12. Don't trust simulation scores as monitor-quality metrics (1555).** Evaluate neuron labels used in monitors by causal tests (ablation, steering, held-out behavior), not by how well an LLM can simulate activations.

**H13. Risk: automated-interpretability tooling hazards (footnote 6, 1543; 1549).** Agents can miss content because of reader truncation and "bring their own default reading" of terms. If the interpreter is itself an untrusted model, interpretability-pipeline *sabotage or sandbagging* is a real threat vector, and the control setup must include trusted verification of agent-produced explanations.

### Candidate "win/lose" experiment suggested by this section

Setting: an open-weight MoE/SwiGLU model of the kind the essay studies (Qwen3.6-35B-A3B or Qwen3-32B) acts as the untrusted policy in an APPS/BashBench-style backdoor setting. The red team gets prompting or fine-tuning to insert subtle backdoors and to evade a black-box monitor.

- **Blue team A (black box):** a trusted smaller LLM reads code and transcripts.
- **Blue team B (white box):** H2 + H3 + H4 + H5 + H8 features on the policy's neurons, with a calibrated threshold.
- **Metric:** safety at a fixed audit budget (e.g. 1–2%) and fixed usefulness; ROC/AUROC of backdoor detection; performance against attacks optimized against monitor A.
- **Win:** B dominates A, or B+A dominates A.
- **Lose:** red team fine-tuning against B's features, under a held-out monitor variant, obfuscates them.
- **Continue:** B helps only for some attack classes.

This directly tests the essay's 1496 thesis ("deception… has no reason to hide from the model's own circuitry").
