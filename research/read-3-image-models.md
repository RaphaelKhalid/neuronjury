# Deep read 3: image-model experiments and "Do weak activations matter?"

Source: Nick Cammarata, "Neural Networks Are Already Clean" (Goodfire, ~Oct 2026). Plain-text extraction at `source/already-clean.txt`.
Range covered: **lines 469–958** (sections "Exploring Image Models", "How I Think About Neurons", "What Neurons Do Under Pressure", "Late Circuits", "What Dictionaries Learn", "Rare Things and Memorization", "Do Weak Activations Matter?"). Framing read: lines 29–99. Context lookups outside the range (cited as such): L243–271 (InceptionV1 5%→50%→70%→99% numbers), L1859–1870 ("Missing Curves" appendix).

Figures are missing from the extraction; only alt text, captions and numbers in captions remain. Several panels (late circuits, 13-neuron panel, Qwen radial plot) are interactive and carry almost no text here.

---

## 1. Plain-English summary

This part of the essay tries to show, mostly in small image models where you can see clearly, that neural networks do not hide unrelated concepts on top of each other ("superposition") even when you squeeze them hard. Its main moves:

1. **Neurons as gates, not nouns.** A neuron has two poles. The positive pole groups things; the negative pole keeps out a near look-alike (taxi vs ambulance, broccoli vs cauliflower, wolf vs husky). Following one sports-car photo through the last five blocks of a 28.6M ConvNeXt shows a chain of such gates that narrows "rectangular objects vs snakes/dogs" down to "convertibles vs station wagons".
2. **Squeeze test.** Retrain InceptionV1 with layer mixed3b cut from 480 to 10 neurons (48×) and no bypass. Superposition predicts overlapping mixtures; what appears is ten coarse, readable neurons ("curves & loops", "circles", "red", ...). A sparse autoencoder (SAE) on the squeezed layer cannot pull the original ten curve detectors back out (shape match 0.38–0.79, photo match ≤0.27), whereas the same SAE recipe on the original layer matches them at 0.96–1.00. A last-layer squeeze of a ConvNeXt (1,024→13) also "broadens".
3. **SAEs mostly re-find neurons.** On the last layer, 88% of SAE activity is near-copies of single neurons; deleting all SAE directions that match no neuron leaves accuracy unchanged. A rotation search for the sparsest basis lands back on the neurons "in every block". What SAEs add is loose context groupings built from existing neurons.
4. **Rare things and memorization use ordinary routes.** Outlier images are misread through ordinary neurons; adversarial examples use normal semantic routes; teaching the 7.06M model that an umbrella photo is a "bee" took nine steps and worked by switching to the existing bee neurons, almost all in the last three blocks: an "off-ramp" between existing routes, not a hidden standalone feature.
5. **Weak activations mostly don't matter for the decision.** In the medium ConvNeXt, removing the weakest 75% of activations costs 1 accuracy point (72%→71%, 1 in 10 answers change, all near-ties). Removing the strongest 7% (same total activation) drops it to 4%. Mid-strength activations "radiate outward semantically". Raw activation scales are preferred to percentiles. The author's hand-tracing of "probably hundreds" of weak activations found almost all were related through a reasonable circuit.

**Context from outside my range (L271):** InceptionV1's last layer was ~5% interpretable with 2014-era tools ("others at ~0%"), ~50% with better tools on the same network, ~70% when the same architecture is retrained with modern regularization, and ~99% in a parameter-matched ConvNeXt.

---

## 2. Claims, evidence and strength

Strength scale: **strong** = experiment + numbers + controls; **moderate** = experiment or numbers but thin or single-instance; **weak** = examples/anecdote; **asserted-only** = argument without evidence in this section.

| # | Claim | Evidence (line) | Numbers | Strength |
|---|---|---|---|---|
| C1 | Vision is the right testbed because LM tools are "blurry" and every tool flaw is miscounted as polysemanticity | "every flaw in your eyesight gets counted as blur in the image" (L471) | — | asserted-only (a measurement-bias argument) |
| C2 | Three ConvNeXts spanning ~300× were trained | "a small one with 92k parameters, a medium one with 7.06M (the same size as InceptionV1), and a large one with 28.6M" (L473) | 92k / 7.06M / 28.6M | setup |
| C3 | Neurons are better seen as control flow / gates; "monosemanticity is almost the wrong question" | "A better one is what a neuron lets through and what it keeps out." (L479); cars/dogs gate story (L481) | — | weak (conceptual + one traced example) |
| C4 | A single sports car's path through the last 5 of 18 blocks shows a sequence of gates that narrows the category | "Partway through, it's grouped with other rectangular shapes, like tables and cabinets, against snakes and dogs. By the last block, the split is convertibles against station wagons." (L487); caption L527 | Block14·203 (limousine −6.06 vs school bus +6.75); Block15·920 (china cabinet +5.38 vs green snake −3.53); Block16·609 (convertible −8.38 vs minibus +6.66); Block17·1455 (convertible +51.25 vs screen −18.88, minivan −13.62); Block18·632 (convertible −233 vs minivan +20.88) (L492–525) | weak ("One selected sports car", L527) |
| C5 | The negative side matters "almost as much" as the positive, even in ReLU nets; it is shaped by learning through input "votes" | "The negative side never gets gradient on its own, but the individual votes do whenever the neuron is on, so it's shaped by learning too." (L529) | — | moderate (correct mechanistic argument; usefulness asserted) |
| C6 | Negative pole = the distinction that matters at this point in the circuit; a quick validity check | "the V neuron's negative side is an O" (L529) | — | weak |
| C7 | Last-layer neurons in the large ConvNeXt respond to one pattern and negatively to a close relative | "each responds to one pattern and negatively to a closely related one" (L551) | 9 named neurons in stage3.block2: taxis 230, broccoli 829, spoonbills 1440, toucans 2021, lighthouses 1956, pretzels 1068, wolves 401, house cats 1637, mittens 63 (L591). E.g. broccoli +13 vs cauliflower −256; spoonbill +26.38 vs flamingo −142 | weak–moderate (curated examples with real indices; no population statistic) |
| C8 | The small (92k) model's last layer is coarser: one neuron = ground vehicles vs boats/planes | "Its last layer ends at cars, trains, and carts in one neuron, with boats, planes, and a water-based ox-cart ... on its negative side" (L593); caption L624 | — | weak (one neuron) |
| C9 | Early-layer monosemanticity across all vision models is suspicious under the "too few features" story | "it's a bit strange that every model, from AlexNet, to ResNets, to InceptionV1, to CLIP all have the right ratio of early features to early neurons" (L630) | — | asserted-only |
| C10 | Squeezing InceptionV1 mixed3b 480→10 with no bypass gives coarser readable neurons, not mixtures | "The neurons stay interpretable and generalized, but coarser: one 'curves & loops' neuron instead of ten curve detectors, two circle neurons instead of several circle types" (L636) | 48× squeeze; 58.35% top-1, 81.14% top-5 on 50k val (L649, L675) | moderate (one retrain; interpretability judged visually: "Names are provisional visual descriptions", L677) |
| C11 | An SAE on the squeezed layer does not recover the original curve detectors | "We don't see anything like clean curve neurons!" (L679); "broad and bunched together, not ten curves" (L704) | TopK SAE, 640 features, k=2; 82% variance explained; spliced top-1 58.8%→43.0% (L707). Shape match 0.38–0.79, photo match 0.08–0.26 (table L713–731). Originals 24–56° wide vs matches 44–174°; 3b:388 and 3b:324 share SAE feature 174 (L735) | **strong** |
| C12 | No SAE feature reproduces the "silent at the opposite angle" property | "None of the 91 features that respond most to drawn curves is silent at the opposite angle." (L735) | 91 features checked; unfiltered closer shapes 0.63–0.98 but fire at only 9–42% of usual strong activation (originals 72–183%), photo match 0.02–0.12 | **strong** |
| C13 | Positive control: same SAE recipe on the original layer recovers curves cleanly | "The essay's SAE of the original layer matches the same detectors with shape correlations of 0.96–1.00." (L735); images L739–741 | 0.96–1.00 | **strong** (a real control) |
| C14 | Even a best-case nonlinear readout of the ten squeezed neurons cannot reconstruct curve detectors | "even the best nonlinear readout of the ten neurons at one position tracks each detector with a correlation of only 0.29–0.48" (L735) | 0.29–0.48 | moderate (single-position only; see W3) |
| C15 | Result is robust to SAE hyperparameters | "Other autoencoders tell the same story (1 to 4 active features, 160 or 640 features, a second seed, or no auxiliary loss): median shape match 0.47–0.63, photo match at most 0.27." (L735) | k 1–4; 160/640; 2 seeds | **strong** |
| C16 | Last-layer squeeze in a residual net (medium ConvNeXt 1,024→13, residual routing blocked) also broadens | "We see the same pattern of it broadening." (L759); caption L774 | 13 neurons named: Beetles, Instrument dials, Digital clocks, Cars, Space shuttles, Payphones & meters, Signs & displays, Beetles & vehicles, Pomeranians, Schnauzers & terriers, Transit & small mammals, Dogs, Façades & dogs (L772) | weak (labels only, no accuracy or SAE test given; several labels are compound, see W2) |
| C17 | Late layers are organized "the whole way through", not just the last layer | "We see that it's organized the whole way through." (L780); five circuits: Monastery, Ladybug, Tow truck, Strawberry, Clownfish (L784–803) | 5 circuits × 5 blocks | weak (selected examples, interactive figure lost) |
| C18 | Dictionaries (SAEs) find no building blocks the neurons lack | "I trained several on these layers and went looking, myself and with agents. I didn't find any." (L809) | — | moderate (absence-of-evidence after search) |
| C19 | SAE units = neuron building blocks grouped by context (spiders example) | "The SAE units were spiders in different settings; the neurons were leg patterns and webs." (L811) | — | weak |
| C20 | SAEs help "what's in this image" most in small models; at large size neurons are preferred; understanding always shows up on a neuron | "If a model at a particular size failed to understand baseball players, so did its SAE. When the model finally understood a baseball player, it was on a neuron." (L813) | — | weak (preference, anecdote) |
| C21 | 88% of last-layer SAE activity is near-copies of single neurons; removing non-matching directions leaves accuracy unchanged | "On the last layer, 88% of its activity is near-copies of single neurons, and the rest is faint: removing every dictionary direction that matches no neuron leaves accuracy unchanged, and the few answers it flips were already near-ties." (L815) | 88% | moderate (number given; metric, threshold and model not specified) |
| C22 | Sparsity-maximizing rotation search recovers the neuron basis in every block | "if you search the rotations of a layer for the one where a handful of units carry the most activity, starting from a random one, you land back on the neurons, in every block" (L815) | — | moderate as a claim / no details given |
| C23 | What SAEs add are loose groupings of existing neurons | "loose groupings built from existing neurons, like animals at the water's surface or pale, lumpy food" (L815) | Feature 6717 built from neurons 733 (0.19), 170 (0.17), 920 (0.17), 482 (0.15) (L825); 16 such features in the carousel (L818) | weak–moderate |
| C24 | Rare classes are more consolidated, not hidden | "you need a lot of dog patterns for ImageNet, but only one Triceratops neuron" (L836) | — | weak |
| C25 | Removing weak activations in the last stage did not single out any class | "When I removed weak activations in the last stage, no class stood out." (L836) | — | asserted (no numbers) |
| C26 | Adversarial examples use normal semantic routes | "The adversarial examples we traced used normal semantic circuit routes." (L836) | — | asserted here (a separate jaguar/skull example exists at L1891, outside range) |
| C27 | Representational outliers are misread through ordinary neurons | "a hummingbird seen as ice cream, a giant banana seen as a vault, and a guy in a fallen wheelbarrow seen as a lawn mower" (L838); supporting neuron "measured by ablation" (L841) | 3 examples | weak |
| C28 | Even noise→random-label memorization leaned partly on semantic textures | "it partially leaned on wool textures and the texture of distant trees" ... "I didn't fully audit the model" (L838) | — | weak (author flags it) |
| C29 | Memorization sits close to the output | "memorization tends to want to sit as close to the output as possible ... the late layers did most of the work" (L838) | — | asserted (cross-experiment generalization) |
| C30 | Implanting a nonsense label (umbrella→bee) reuses existing routes, localized to the last three blocks | "In nine training steps, the top guess went from umbrella to maypole to bee. The umbrella neurons faded and existing bee neurons came on, nearly all of it in the last three blocks: swap just those into the original model, and it says 'bee.'" (L843) | 9 steps; 3 blocks; 7.06M model | moderate (causal weight-swap test, but n = 1 image, fine-tuning) |
| C31 | A hidden standalone feature is slower to learn and more fragile than an off-ramp between active routes | "I think it's slower to learn than assembling related parts that are already activating and have routes to the output, giving it plasticity and gradient. It's also more fragile, and isn't what we see anywhere." (L851); "an off-ramp between two routes the network already has" (L859) | — | asserted (plausibility argument) |
| C32 | Weak activations are generalization, not superposition, because packing there would collide with far more things | "Weak activations are vastly denser, so you'd be colliding with orders of magnitude more things, for little upside." (L871) | — | asserted (argument) |
| C33 | A Qwen3-32B neuron's strong firings are extremely sparse | "100 million tokens through one Qwen3-32B neuron. Almost all sit near zero; about 160 reach the strong half." (L877) | ~160 / 1e8 tokens | moderate (one neuron) |
| C34 | Almost all weak activations network-wide can be ablated at almost no cost; costly places are the easy-to-understand ones (LM last layer "say or just think" token suppression; early vision "dials") | "you can ablate almost all the weak activations of the network for almost no cost" (L879) | — | asserted for LMs in this range; vision backed by C36 |
| C35 | Therefore critical common things cannot be in the weak activations | "So critical common things can't be in the weak activations, since we can remove them." (L879) | — | inference from C34/C36 |
| C36 | Matched-mass ablation: weakest 75% ≪ strongest 7% | "Removing the weakest 75% / accuracy 72% → to 71% · 1 in 10 answers change / Removing the strongest 7% / accuracy 72% → to 4% · 96 in 100 answers change / The same total activation as the weakest 75%" (L883–891); "Medium ConvNeXt, all 18 blocks" (L915) | 72→71 vs 72→4; 10% vs 96% answers changed | **strong** (good matched-mass control; one model) |
| C37 | What weak activations decide are near-ties between already-confused classes | near-tie examples: Eskimo dog (54% of top two) → Siberian husky; grasshopper (56%) → cricket; whippet (57%) → Saluki; tiger cat (62%) → tabby. Sure answers (100%) unchanged: garbage truck, hummingbird, brown bear, zebra (L899–913) | — | moderate |
| C38 | Rare cases don't live in weak activations, because cutting them broke nothing outright | "if rare cases lived in the weak activations, cutting them should have broken some answers outright. Instead, every change was small, a near-tie tipping one way or the other." (L919) | — | moderate inference (but test set is average-case val, see W6) |
| C39 | Strong-but-not-extreme activations radiate outward semantically | CLIP Trump neuron: "photos of Trump, then art and people related to him, then Fox News studios" (L921) | — | weak (example; prior paper) |
| C40 | What fires weakly here may have fired strongly one layer back; trace circuits before calling something unrelated | "At minimum, look at the circuits a datapoint flowed through; what fired weakly here may have fired strongly one layer back." (L922) | — | methodological advice |
| C41 | Interactive: every strong firing of five Qwen3-32B neurons, placed by fraction of max, colored by story/circuit | L924–935 | "468 circuits" (L935) | n/a (figure missing) |
| C42 | Raw activation shape carries meaning; percentiles flatten dial-vs-detector differences | "Some neurons hold their meaning far down the range; others drop off a cliff, like the Christmas neuron above at about 5% of its max." (L943) | Christmas cliff ~5% of max; 99th pct ≈ 1 token per quarter page; 99.9th every 2–3 pages; 99.99th every 25–30 pages (L945) | moderate (consistent arithmetic, implies ~400 tokens/page) |
| C43 | Weak activations are usually not needed to label a neuron; neurons are "analogizers" | "it's hard to overstate how much neurons are analogizers" ... "there's a Titanic-ish mechanism" (L951) | "thousands of language model attribution graphs by hand" (L951) | weak–moderate (large but subjective sample) |
| C44 | Weak activations that look unrelated almost always turn out related via a reasonable circuit | "Of the probably hundreds I've followed by hand, almost all turned out to be related, coming through a reasonable circuit" (L953); Zen-koan neuron fires weakly on recursion in math (L955) | "probably hundreds" | weak (single rater; post-hoc relatedness is flexible) |

---

## 3. Methods (reimplementable detail)

**M1. Size sweep without changing data.** Train ConvNeXt at 92k, 7.06M, 28.6M parameters on ImageNet (L473). 28.6M matches the standard ConvNeXt-T size and the text's "18 blocks" and "stage3.block2" naming match ConvNeXt-T's [3,3,9,3] layout (my inference). Neuron indices up to 2021 in the last stage (L591) suggest "neurons" are the 4× MLP hidden units (3,072 in ConvNeXt-T stage 3), and values such as −256 imply **pre-activation** values (GELU's minimum is about −0.17). This is inference, not stated.

**M2. Per-image contribution path ("follow the car").** Start from the predicted class logit. At each block, going backward, choose "the neuron that contributes most to the next one on this image (the last, to the sports-car output)" (L527). For each chosen neuron show top positive and top negative dataset examples, labelled "what it groups the car with" and "what it separates it from". Contribution could be activation × gradient or direct ablation; the text does not specify.

**M3. Bipolar neuron cards.** For every neuron: the strongest positive and strongest negative dataset examples over 50,000 images, on raw (signed) responses. "The sign is the neuron's own response, not its effect downstream" (L591). Use the negative pole as a sanity check of the label (L529).

**M4. Bottleneck (squeeze) test.** Retrain from scratch with one layer cut to N ≪ original channels and no bypass: InceptionV1 mixed3b 480→10 (L632, L675); medium ConvNeXt final layer 1,024→13 with residual routing blocked (L759, L774). Inspect with dataset examples at percentile bands (top 10, 99–99.9%, 1–5%, bottom 10; L652) and "path-guided feature visualization" using the strongest 60 examples (L677). Path weight is rescaled to each unit's activation range because squeezed activations are "hundreds of times smaller" (L739).

**M5. SAE recovery test with a curve-tuning probe.** (L707, L733–735)
- TopK SAE, 640 features, k=2, plus the usual auxiliary dead-feature loss; trained on 25.6M spatial positions from 200k ImageNet training images.
- Report held-out variance explained (82%) and spliced-in accuracy (top-1 58.8%→43.0% on 10k val).
- Tuning probe: render a thin dark arc at the image centre at 180 angles × 2 curvatures; record the response at the centre.
- Shape match = Pearson correlation of a feature's tuning curve with the original detector's, restricted to features that respond most strongly to drawn curves. Width = span of angles above half-peak. Photo match = correlation, over every spatial position of 10,000 held-out photos, between the feature and the original detector at the same location.
- Extra checks: is the feature silent at the opposite angle; what fraction of its usual strong activation it reaches on drawn curves; best nonlinear readout from the 10 neurons at one position to each detector.
- Sweep: k ∈ {1..4}, 160 or 640 features, a second seed, aux loss on or off.

**M6. Positive control.** Apply the identical SAE and visualization recipe to an SAE of the *original* 480-neuron layer: shape correlation 0.96–1.00, clean curve images (L735, L739–741). (The "Missing Curves" appendix, L1859–1870, outside range, reports SAE curve features there are 97.5–98.0% composed of existing curve neurons.)

**M7. Dictionary-vs-neuron audit.** (L815–827)
- Fraction of SAE activity on features that are near-copies of single neurons (cosine of decoder direction with a neuron axis above some threshold, not given): 88%.
- Ablate all SAE directions that match no neuron and measure accuracy and which predictions flip (were they near-ties?).
- For the remaining features, list their decoder weights over neurons ("Built from 733 0.19, 170 0.17, 920 0.17, 482 0.15").

**M8. Sparsest-rotation search.** From a random orthogonal starting rotation, optimize the rotation of a layer's activation space so that "a handful of units carry the most activity", and check whether it converges to the neuron basis, up to permutation and sign (L815). No objective or optimizer given. Plausible versions: maximize kurtosis or top-k energy share, or minimize L1/L2, over the orthogonal group (Cayley or Householder parametrisation).

**M9. Rare-thing probes.** (L836–841)
- Per-class breakdown after removing weak activations in the last stage.
- Trace circuits of adversarial examples.
- Find images whose late-layer representation is furthest from any other image (nearest-neighbour distance), then identify each one's "most supportive last-layer neuron, measured by ablation".
- Train an ImageNet model mapping random noise to random labels and inspect which features it relies on.

**M10. Implant-a-memorization and localize it.** (L843–859)
- Fine-tune the 7.06M model on one umbrella photo labelled "bee".
- Track top-1 per step (umbrella→maypole→bee within 9 steps).
- Bar-plot each neuron's response before and after, against its response to a typical umbrella or bee.
- Localize by **swapping fine-tuned block weights into the original model**: the last three blocks alone reproduce "bee".
- Verify connections by ablation.

**M11. Matched-mass weak/strong ablation.** (L883–915)
- Over all 18 blocks of the medium ConvNeXt, zero the weakest 75% of activations, or instead zero the strongest 7%, which carry the same total activation.
- Measure top-1 and the fraction of changed answers.
- Bucket changes by the pre-ablation top-two split: near-ties (54–62%) vs sure answers (100%).
- Unstated: whether "weak" is by absolute value, per layer or global, or pre/post-activation, and whether the residual stream is touched.

**M12. Strength-ring plot.** (L924–935, L943) Plot every strong firing of a neuron at radius = fraction of max, colored by topic ("story") or by circuit, with a click-through to the circuit that produced each firing. Use raw values, not percentiles. Classify neurons as "dials" (meaning holds down the range) or "detectors" (meaning collapses below some fraction of max, e.g. ~5%).

**M13. Weak-activation tracing protocol.** (L922, L951–953) When a weak activation looks unrelated, trace its circuit back. "What fired weakly here may have fired strongly one layer back". Ablate the circuits, keep zooming.

---

## 4. Weaknesses, caveats, ways it could be wrong

- **W1. Curated examples, few population statistics.** One sports car (L527), nine hand-picked bipolar last-layer neurons (L591), five circuits (L803), one umbrella photo (L843). There is no stated fraction of last-layer neurons whose negative pole is a "close relative". The strongest quantitative results are the curve/SAE table and the matched-mass ablation.
- **W2. The squeeze test may not be the test superposition theory cares about.**
  - It targets an early layer whose features are dense and co-occurring. Toy-model superposition theory predicts superposition mainly for *sparse* features, and predicts that dense features get dropped. "Coarser neurons" is therefore partly what that theory would also predict.
  - The author concedes "people mostly suspected superposition in the last layers" (L759). The last-layer squeeze (1,024→13) comes with only labels, no quantitative recovery test.
  - Several of its labels read as compound: "Transit & small mammals", "Façades & dogs", "Beetles & vehicles" (L772). They may be two poles of one neuron or genuine mixtures. The text does not say.
- **W3. Spatial superposition not tested.** The "best nonlinear readout" uses "the ten neurons at one position" (L735). Downstream convolutions read neighbourhoods, so curve information could be spread across positions. The SAE is also per-position.
- **W4. The squeezed model is badly hurt.** It reaches 58.35% top-1 (L649). Original InceptionV1 is roughly 70% top-1 (external knowledge, not in range), and the SAE splice drops to 43.0%. The squeezed network may simply have dropped fine curve information. That fits "coarsen, don't pack", but it does not show what happens under *mild* capacity pressure, which is where superposition could be cheapest.
- **W5. SAE audit details missing.** "88% of its activity" (L815) has no metric, threshold or model named. The rotation-search claim (L815) has no method or numbers. In MLP hidden layers with elementwise nonlinearities the neuron basis is privileged by construction, so recovering it is expected. The informative case would be the residual stream, and it is not specified which was rotated.
- **W6. Weak-activation ablation is average-case.** It is measured on ImageNet validation accuracy. "1 in 10 answers change" (L885) is not trivial, and tail behaviours, rare triggers or backdoors would not show up in a 1-point average accuracy change. In a residual net, zeroing weak *neuron* activations does not remove weak components already in the residual stream, so the information may route around. The LM claim ("you can ablate almost all the weak activations of the network for almost no cost", L879) has no numbers in this range.
- **W7. The bee experiment is n = 1, in the friendliest regime.** Nine steps of fine-tuning on one image will route gradient through already-active paths almost by construction. It does not test backdoors trained in during pretraining with many poisoned examples, behaviours trained under pressure to be hidden, or long fine-tunes. "Slower to learn ... more fragile" (L851) is a plausibility argument, and an adversary or a long training run has time.
- **W8. Relatedness is judged post hoc by one rater.** "Of the probably hundreds I've followed by hand, almost all turned out to be related" (L953). With enough creativity almost any two concepts can be linked; the Zen-koan → recursion example (L955) is clever but shows how flexible "related" is. There is no inter-rater agreement and no pre-registered criterion. The author does note it is easy to be fooled further down the range (L922).
- **W9. Vision-to-language transfer is mostly asserted here.** The only LM evidence in this range is one Qwen3-32B neuron's sparsity (L877), the five-neuron radial figure (L924–935) and anecdotes.
- **W10. Sign and readout semantics.** Displayed negative values (e.g., −256) appear to be pre-activation, and the essay notes sign ≠ downstream effect (L591). In GELU/ReLU nets the negative pole is largely clipped, so "what it keeps out" is a property of the pre-activation computation, not necessarily something downstream units read.
- **W11. Unfalsifiability risk.** Coarse neurons count as "generalization", fine neurons as "generalization", odd weak firings as "recursive generalization". The section does not state a result that *would* count as superposition, except for the curve-recovery test (which is good), and the prediction at L634.

---

## 5. Open questions

1. Does "coarsen, don't superpose" hold for **sparse, high-level features** under **mild** squeezes, and in **transformers**? Squeeze an MLP layer of a small LM by 2–8× and run curve-style recovery tests with ground-truth features.
2. Does a **backdoor trained in during pretraining** (many poisoned examples, many steps, trigger patch) also ride existing routes like umbrella→bee? Or does it form the "stray superposed feature" the essay says it never sees (L853–859)?
3. Under **adversarial pressure to evade a neuron-level monitor**, can a model move a behaviour into weak activations or off-neuron directions, and at what accuracy cost?
4. Are subtle sabotage and sandbagging decisions **near-ties**, the one regime where the essay shows weak activations do matter (L881, L899–905)?
5. Does the sparsest-rotation search recover neurons in the **residual stream**, or only in MLP hidden layers?
6. What fraction of last-layer neurons are **bipolar near-miss pairs**? Is there an LM analogue for safety-relevant pairs (honest/deceptive, real fix/special-cased test)?
7. Does **block-weight-swap localization** (bee experiment) scale to LLM fine-tunes as a model-diffing tool for implanted behaviours?
8. How stable are neuron identities across **seeds and sizes**? Would a monitor built on one checkpoint transfer to the next?
9. Are the compound labels of the 13-neuron last layer (L772) two poles, or packing? This needs the same quantitative treatment as the curves.
10. What does a **multi-position** (spatial) readout recover from the squeezed 3b layer?
11. What exactly is "88% of activity" (L815), and how does it vary by block and model size?
12. Do the costly weak activations in LMs (last-layer "say or just think" token suppression, L879) carry anything safety-relevant, such as suppressing a token the model "thinks" but doesn't "say"?

---

## 6. Control hooks: turning already-clean neurons into a white-box monitor

These map the findings onto AI control: catching backdoored code, sabotage, reward hacking, sandbagging and deception better than a black-box LLM monitor reading transcripts. Items marked **[ext]** use outside knowledge, not the source.

**H1. Off-ramp model diffing (from the umbrella→bee result, L843–859).**
- Claim to exploit: an implanted wrong behaviour is a *re-routing between existing semantic routes*, concentrated in late blocks, not a sealed-off hidden feature.
- Monitor: on the same input, diff per-neuron activations between a trusted base checkpoint and the deployed model. Flag inputs where a "trigger-context" neuron family newly drives an "action" neuron family (e.g., "write insecure crypto", "disable check").
- Localize with M10's block-weight swap.
- A black-box monitor sees only the output; this sees *which existing route was hijacked*, even if the output looks benign.

**H2. Strong-firing event log (from L877, L883–891).**
- Strong firings are extremely sparse: about 160 strong-half firings per 100M tokens for one Qwen3-32B neuron. The strongest 7% of activations carry the decision (accuracy 72%→4% when removed).
- A monitor can therefore log only strong firings of labelled neurons, like a syscall audit log, and alert when safety-labelled neurons fire strongly during an agent action (deception, evaluation-awareness, hiding, "special-case the test", exfiltration). This is cheap enough to run on every token.

**H3. "If the model understands it, it's on a neuron" as a sandbagging detector (from L813, L636).**
- If capacity pressure produces coarser neurons rather than hidden mixtures, then knowledge the model has should appear as strong neuron firings.
- Sandbagging check: on an eval question, test whether "correct answer known" neurons fire strongly while the output is wrong. A transcript monitor cannot see this.

**H4. Bipolar near-miss neurons for safety-relevant distinctions (from L529–591).**
- Last-layer neurons separate a concept from its closest look-alike (taxi vs ambulance). In LMs, search for neurons whose two poles are the "honest vs deceptive" or "real fix vs reward-hack" version of the same action.
- Monitor the sign: the negative pole is "what is being kept out". If the model is letting through what is normally kept out, that is a high-precision alarm.

**H5. Per-decision contribution path (M2).**
- At each tool call or code-commit token, trace the top-contributing neuron chain back through late layers (one backward pass) and check the chain's labels. Flag chains that pass through labelled "conceal / evade / test-detection" neurons.
- This is the white-box analogue of "explain why you did that", but read from the mechanism rather than the model's self-report.

**H6. Focus compute on late layers (from L838, L843).**
- "memorization tends to want to sit as close to the output as possible". The bee rerouting lived almost entirely in the last three blocks.
- First-pass backdoor and trigger monitors can concentrate on the last few blocks, which shrinks the labelling burden.

**H7. No SAE needed, so no dictionary blind spot (from L815).**
- If 88% of SAE activity is neuron copies and the sparsest rotation is the neuron basis, a monitor can be defined directly on neurons. It avoids SAE reconstruction error (82% variance explained and an accuracy drop of 58.8→43.0 even in the toy squeeze, L707) and the risk that an SAE trained on benign data lacks a latent for the rare malicious behaviour.

**H8. Misreadings are legible (from L836–841).**
- Adversarial examples and outliers are misread through ordinary neurons (banana→vault). In control terms, when an untrusted model is fooled or is fooling a reviewer (e.g., a backdoor disguised as a refactor), the trusted model's "most supportive neuron, measured by ablation" says *what it thought it was looking at*. That is a way to audit why a monitor said "safe".

**H9. Matched-mass ablation as a monitor-robustness test (from L883–891).**
- Ablate weak activations and check whether the suspicious behaviour persists. If it survives weak-ablation but dies with strong-ablation, it is on readable neurons.
- If a behaviour survives only when weak activations are present, that is evidence of near-tie or hidden routing and a red flag (a hypothesis to test, not established).

**H10. Win/lose game design (pilot in vision, then LMs).**
- Red team trains a backdoor (trigger patch → wrong class, BadNets-style **[ext]**) into a ConvNeXt during *pretraining*, optionally with a penalty for detectability by neuron monitors.
- Blue team gets (a) output-only access, matching the black-box monitor, or (b) neuron access, using H1/H2/H5.
- Score: detection AUROC and catch-rate at a fixed audit budget.
- Then port to code-writing LMs: backdoored-code insertion under a trigger, comparing a transcript-reading LLM monitor against neuron monitors. This directly tests the essay's claim (W7) under adversarial pressure, which the essay never applies.

**H11. Known threats to plan for [ext].**
- Prior work shows latent-space monitors (probes, SAEs) can be evaded by models trained against them ("obfuscated activations", Bailey et al., 2024).
- Simple linear "defection probes" can catch sleeper-agent backdoors with high AUROC (Anthropic, 2024).
- The essay's claims (no stray features, weak activations tip only near-ties) predict that neuron-level monitors should be *harder* to obfuscate than SAE or probe monitors, because there is no cheap hiding place. This is a testable, publishable prediction.

**H12. Main weak point (from L881, L899–905).** Weak activations matter exactly for near-ties. Subtle sabotage, such as choosing a slightly worse option or adding a plausible-looking off-by-one, is plausibly a near-tie decision. That is where a neuron monitor focused on strong firings could be blind, so a credible demo must include near-tie sabotage tasks.

---

## 7. Key numbers (from my range unless noted)

- ConvNeXt sizes 92k / 7.06M / 28.6M; ~300× range (L473)
- Large ConvNeXt has 18 blocks (L527)
- Squeeze 480→10 (48×), 58.35% top-1 / 81.14% top-5 (L649)
- SAE on squeezed layer: 640 features, k=2, 25.6M positions, 200k images, 82% variance explained, splice 58.8%→43.0% (L707)
- Shape match 0.38–0.79, photo match 0.08–0.26; widths 24–56° (orig) vs 44–174° (SAE) (L713–735)
- 91 curve-responsive SAE features, none silent at opposite angle (L735)
- Original-layer SAE control 0.96–1.00 (L735)
- Best nonlinear readout 0.29–0.48 (L735)
- SAE sweep median shape 0.47–0.63, photo ≤0.27 (L735)
- Medium ConvNeXt last layer 1,024→13 (L774)
- 88% of last-layer SAE activity = near-copies of single neurons (L815)
- Umbrella→bee in 9 steps, last 3 blocks (L843)
- One Qwen3-32B neuron: ~160 strong-half firings in 100M tokens (L877)
- Weakest 75% removed: 72%→71%, 1/10 answers change. Strongest 7% (same total) removed: 72%→4%, 96/100 change (L883–891)
- Christmas neuron cliff at ~5% of max (L943). Percentile-to-pages conversions (L945)
- 468 circuits in the five-neuron Qwen figure (L935)
- Context (L271, outside range): InceptionV1 last layer ~5% (2014 tools) → ~50% (better tools) → ~70% (retrained, modern regularization) → ~99% (parameter-matched ConvNeXt)
