# Scout: reception and strongest counterarguments to "Neural Networks Are Already Clean"

Agent: scout-reception-critics · Date of research: 2026-10-15 (the essay's publication day)
Essay: Nick Cammarata (Goodfire), https://already-clean.goodfire.com/ · local copy `source/already-clean.txt` (line numbers below refer to that file)

Legend: **[V]** = verified from a source I read, **[S]** = secondary report (news write-up or search summary, not checked against the primary), **[I]** = my own inference or argument.

---

## 0. TL;DR

- **Reception is only hours old.** The essay went up on 2026-10-15. Public reaction so far is mostly enthusiasm on X (roon/@tszzl: "may be remembered as a major moment in scientific history"), a 55-karma LessWrong linkpost with one substantive comment, and a 96-point Hacker News thread that mostly complains about page weight and length. **No named interpretability researcher has published a rebuttal yet.** Anthropic's Joshua Batson and Jack Lindsey reviewed a draft (essay line 2480). The Batson quote in the essay is mildly supportive (line 1491).
- **Strongest steelman critique (built from prior literature):** the essay wins on a *narrow* definition of superposition ("a learning principle that packs unrelated things into one neuron"). It explicitly sets aside the senses most relevant to safety: more features than dimensions, distributed computation, the residual stream, and attention (lines 1356, 1382, 2361). Its headline number (about 90% of Qwen3-32B neuron *poles* have one main job) is preliminary and depends on thresholds. It comes from agent and author judgment with no published methodology (the companion paper is forthcoming, line 96). It counts *poles*, not neurons. The test of weak activations, where superposition theory says interference should live, is quantified only in vision models. For LLMs the essay admits it has "no semantic test for weak activations that we trust" (line 1853).
- **Control-specific overreach:** "Deception might hide from someone reading a model's outputs, but it has no reason to hide from the model's own circuitry" (line 1496). This holds only when there is no optimization pressure against the monitor. Bailey et al. (ICLR 2026) and Neural Chameleons (McGuinness et al., 2025) show that models can learn to evade activation monitors, including **unseen** deception probes. Nobody has tested whether *neuron-level* or circuit-level monitors are more robust than linear probes. That is a wide-open and important experiment.
- **Fair verdict:**
  - **Likely right:** classic polysemantic examples were misread; modern, large, gated, MoE models have far more legible neurons than 2023-era models; superposition was over-assumed as a default; agentic neuron-first investigation scales.
  - **Contested:** the 90% figure; "recursive generalization" as *the* explanation; weak activations being irrelevant in LLMs; the residual stream and attention.
  - **Likely overstated for AI control:** that legibility implies monitors that are hard to evade, and that interpretability "will be solved by the time we need it."

---

## 1. Who is Nick Cammarata (credibility context)

- **[V]** First author of Distill's *Curve Detectors* (2020): Cammarata, Goh, Carter, Schubert, Petrov, Olah (https://distill.pub/2020/circuits/curve-detectors/, https://mlanthology.org/distill/2020/cammarata2020distill-curve). He is also a co-author of *Zoom In: An Introduction to Circuits* (Olah, Cammarata, Schubert, Goh, Petrov, Carter, 2020, https://distill.pub/2020/circuits/zoom-in/), the paper that introduced the circuits framework and the "superposition" circuit motif he now says was misread (essay line 43).
- **[V]** Co-author of *Multimodal Neurons* (Goh, Cammarata, Voss et al., 2021) and *Language Models Can Explain Neurons in Language Models* (Bills, Cammarata, Mossing et al., OpenAI 2023). The essay says he started that automated-interpretability project, which found about 1.7–2% of GPT-2 XL neurons interpretable (lines 47, 1292).
- **[V]** Acknowledged in Anthropic's *Toy Models of Superposition* (2022) for detailed feedback (search summary of https://transformer-circuits.pub/2022/toy_model/index.html).
- **[S]** Member of OpenAI's Clarity team (led by Chris Olah), which produced the Circuits thread. A company profile lists him as one of Goodfire's founding researchers; a Longterm Wiki entry gives his start as 2023 but marks it unverifiable. He has a Goodfire research post: "Painting With Concepts Using Diffusion Model Latents" (Cammarata et al., May 27, 2025, listed at https://www.goodfire.com/research).
- **Credibility read [I]:** he is one of the originators of both explanations for polysemanticity, and the essay says so: "there were two explanations for polysemanticity, and I helped propose both" (line 65). He has deep hands-on experience with the neurons and is publicly reversing his own earlier position, which adds weight. Two caveats: (a) the essay is explicitly personal ("Any errors, and the views here, are my own", line 2480); (b) he works at a company that sells interpretability tooling (Silico, Ember), so an "interpretability is easier than we thought" message lines up with commercial interest. That is an incentive to note, not evidence of error.

---

## 2. Reception so far (as of 2026-10-15)

### LessWrong linkpost (verified)
- "Linkpost: Neural Networks Are Already Clean", posted by Yair Halberstadt, 15 Oct 2026, about 52–55 karma, 5 comments. https://www.lesswrong.com/posts/x4kvabkF2Jk8GLZp8/linkpost-neural-networks-are-already-clean (mirror: https://www.greaterwrong.com/posts/x4kvabkF2Jk8GLZp8/linkpost-neural-networks-are-already-clean)
- The poster asks how big an advance this is and how useful it will be for alignment. Neither question is answered in the thread yet.
- The only substantive comment, from **ajskateboarder** (1 point), reports "monosemantic-ish" neurons in their own SwiGLU perturbation experiments and suggests this may be a property of gated MLPs. They remain skeptical: *"IMO still seems underdetermined that networks can just be cleanly broken into neuron circuits and not higher-rank components."* **[V]**

### Hacker News (verified)
- "Neural Networks Are Already Clean": 96 points, 25 comments, submitted by themgt. https://news.ycombinator.com/item?id=50105647
- Most comments are about the heavy page (crashes, maxed-out CPU) and its length. The substantive pushback:
  - **jacquesm**, replying to the idea that each neuron encodes one concept: *"But they don't. That's the whole reason they work in the first place."* He argues neurons encode fractions of many concepts, like a hologram. This is the folk version of the distributed-representation view.
  - **yurimo:** *"I would not rush to say that superposition is completely wrong."* He also prefers studying native neurons over SAEs or transcoders.
  - **phyzome:** after 16k words, still unclear what "clean" means. Replies define it as "networks don't cram unrelated concepts into single neurons."
  - **BenoitP** points out that Goodfire's own earlier work is SAE-based.

### X / Twitter (secondary)
- **[S]** @tszzl (roon): *"i think this may be remembered as a major moment in scientific history"*, plus a joke that Yudkowsky should lower his p(doom). Quoted at https://huggingnews.com/ai/nick-cammarata-finds-ai-models-legible-reversing-prior-consensus-ab687d62 and in the LessWrong linkpost.
- **[S]** @andrewcurran_: *"I had long since given up on reaching any real level of interpretability before superintelligence arrived"* (same huggingnews article).
- **[S]** Cammarata's own tweet: "the vast majority in models up to trillions of parameters are legible, and their circuits beautiful" and the lesson "the simple thing, at absurd scale, works" (quoted in the LessWrong linkpost).
- I could not retrieve replies from Neel Nanda, Chris Olah, Lee Sharkey or other prominent researchers. Searches found none. **Absence is expected on day 0 and should not be read as agreement.**

### News write-ups (secondary)
- huggingnews.com (Oct 15, 2026): restates the 90% / 2–4% figures. Notes no critics.
- ecosistemastartup.com (Spanish): restates 90% / 7% / 2–4%. Cites **Leonard Bereska (University of Amsterdam)** telling MIT Technology Review that Goodfire's Silico "is adding precision to alchemy". **[S]** That quote is about Silico, not this essay, and I could not verify it against MIT TR directly. https://ecosistemastartup.com/goodfire-90-de-las-neuronas-de-la-ia-ya-se-entiende/

### Alignment Forum
- No post found as of research time.

---

## 3. What the essay actually claims, and what it concedes (exact quotes)

| Claim / concession | Quote | Line |
|---|---|---|
| Thesis | "The cause of polysemanticity in early model organisms wasn't superposition, but several ordinary, mostly fixable issues." | 7 |
| Headline number | "In preliminary audits of Qwen3-32B, we estimate that roughly 90% of neuron poles have one main job … another ~7% have two related jobs; and only ~2-4% are not yet understood" | 50 |
| Number is soft | "the share of neurons with one job varies depending on how you set the threshold for counting weak activations, depth, density of sub-circuits, and what you view as 'one thing'" | 50 (fn) |
| Number was added for reviewers | "when it was taken out, early reviewers felt unanchored without even a rough number. In the sets I've looked at more closely, considering strong activations, it's closer to 97% … but these are relatively small samples." | 58 |
| GPT-2 XL re-analysis is much less clean | "Now about 70% look like roughly one thing … The amount of pristine ones are still low, about 5%." | 1292 |
| Trillion-scale not audited | "We haven't begun full audits of this scale yet … but so far most things have been intuitively interpretable." | 1091 |
| Narrow definition of superposition | "we use the standard word in the sense closest to the original … neurons learning unrelated things together because they rarely interfere" | 1547, 2361 |
| Distributed computation set aside | "A Golden Gate Bridge computation involving eight legible neurons might be called ordinary composition, while one involving three thousand gets called a superposition problem … That's a real concern, but it's different" | 2361 |
| Residual stream not ruled out | "It's a continuous version of packing … Ruling that out entirely may not be possible. But in practice it hasn't been a bottleneck." | 1356 |
| Attention not covered | "We've made less progress on attention than on neurons, and it's mostly outside the scope of this essay." | 1382 |
| No trusted LLM weak-activation test | "We don't yet have a semantic test for weak activations that we trust … these spot checks cannot establish what weak activations mean in general." | 1853 |
| Graph audits are qualitative | "I would update strongly on even one convincing example, but for now I regard this as qualitative evidence—I don't trust our current tools enough to turn it into a cleanliness score." | 2001 |
| Skeptical of quantitative tests | "There are also general tests, like predicting activations and circuits from an explanation. To be honest, I trust these only up to a point." | 1285 |
| Safety claim | "Deception might hide from someone reading a model's outputs, but it has no reason to hide from the model's own circuitry." | 1496 |
| Vision SAE check | "On the last layer, 88% of its activity is near-copies of single neurons, and the rest is faint" | 815 |
| Methods paper pending | "A technical companion paper will offer a more detailed account of language model neuron experiments" | 96 |
| Superposition was over-assumed | Quotes Anthropic SoLU (2022): "superposition is often treated as the default hypothesis simply because it seems intuitively more compelling … but there is little evidence." | 461 |
| SwiGLU artifact | "for about 4% of neurons, it's the whole top of the list. Ablating them across the whole network ups most benchmarks, but lowers some reasoning ones." | 1179 |

---

## 4. Steelman critique, strongest first

### C1. It wins by narrowing the definition (a motte-and-bailey risk) [I, grounded in V quotes]
- The essay refutes superposition only as "a *learning principle* that packs unrelated things into a neuron" (lines 1547, 2361).
- *Toy Models of Superposition* (Elhage et al., 2022, https://arxiv.org/abs/2209.10652) frames superposition as models "storing additional sparse features in 'superposition'", i.e. representing more features than dimensions. That is the sense the essay calls "basically not bad news" (line 389) and "mostly irrelevant" (line 1434).
- For safety, the question that matters is whether a dangerous computation (deception, sabotage, eval-gaming) is **compact and findable**, or **spread across thousands of legible-looking units**. The essay explicitly sets aside the 3,000-neuron "Golden Gate" case as a different concern (line 2361).
- So "superposition was wrong" is true at most for the narrow sense. The broad sense that drove SAE and transcoder research is not refuted; it is reframed as "exploratory interpretability doesn't need a feature list" (lines 1430–1440).

### C2. The 90% number is soft, self-graded and not yet reproducible [V: essay; I: assessment]
- It is preliminary, threshold-dependent and drawn from samples (lines 50, 58). It was kept only because reviewers wanted an anchor (line 58). Graph audits are "qualitative" (line 2001). The methods paper is not out (line 96). The trillion-parameter claims are unaudited (line 1091).
- The graders are agents plus the author. No inter-rater reliability, blinding, pre-registration or held-out precision/recall is reported for the LLM figure.
- The essay rejects simulation scoring (lines 1551–1560) and trusts predictive tests "only up to a point" (line 1285). Replacing quantitative metrics with expert judgment makes the claim harder to falsify. The essay frames this as Mercury's-orbit-style science, but it also removes the tool the field uses to catch self-deception.
- **Prior literature on illusions:**
  - Huang, Geiger, D'Oosterlinck, Wu, Potts (BlackboxNLP 2023, https://arxiv.org/abs/2309.10312): even for the top 0.6% of GPT-2 XL neurons judged well explained by GPT-4, the explanations had precision 0.64 and recall 0.50. The authors were "unable to find evidence that neurons are causal mediators of the concepts denoted by the explanations." **[V via abstract summary]** The essay's rebuttal is that 2023 tools were weak, which is plausible but not yet shown at population scale.
  - Bolukbasi et al. 2021, "An Interpretability Illusion for BERT" (https://arxiv.org/abs/2104.07143): neurons "may spuriously appear to encode a single, simple concept, when in fact they are encoding something far more complex." The explanation you get depends on which dataset you look at. **[V via abstract]**
- **Apophenia risk with strong explainers [I]:** a creative agent can find a unifying story for almost any set ("V-shapes" for cats and cars; "Colorado" for commas, line 431; "righteousness when a bargain purchase works", line 71). The essay's blind-maximum, near-miss, steering and ablation tests (lines 1280–1290, 2048) are real falsification tests and partly answer this. But they appear as galleries (e.g. "Twenty Qwen3-32B neurons from our gallery", line 2048) rather than population statistics with error bars.

### C3. Counting "poles", not neurons [I]
- The unit is a "neuron pole" (line 50). SwiGLU neurons have positive and negative poles that can mean different things. Example: a neuron that standard autointerp labels "capital cities" carries Santa lore on its negative pole (lines 1087–1089).
- If both poles of such a neuron are each "one job", a neuron-level count could show two unrelated meanings per neuron while the pole-level count shows 100% clean.
- The essay reframes this: "Think of negative poles as gates in a circuit, not a neuron's opposite" (line 1446). That may be correct mechanistically, but it changes the denominator relative to 2023-era metrics. The 90% (poles, Qwen3-32B, 2026) versus 1.7–2% (neurons, GPT-2 XL, 2023) comparison is therefore not like-for-like. The essay's own GPT-2 XL re-analysis gives 70% "roughly one thing", 5% pristine (line 1292).

### C4. Weak activations are where superposition theory predicts the mess, and in LLMs that is unquantified [V/I]
- Superposition theory predicts that the top activations of a neuron can look clean while lower-magnitude activations carry interference from many sparse features. An audit centred on strong activations is therefore a weak test of the broad hypothesis.
- The essay's quantitative weak-activation evidence is **vision** (ImageNet top-1 changes under percentile ablation for InceptionV1 and ConvNeXt, lines 1662+). For LLMs: "We don't yet have a semantic test for weak activations that we trust" (line 1853). The LLM evidence is one "enemy" neuron studied in detail plus spot checks.
- **Counter-evidence from Anthropic:**
  - *Scaling Monosemanticity* (Templeton et al., 2024, https://transformer-circuits.pub/2024/scaling-monosemanticity/), §"Features vs. Neurons": "for 82% of our features, the most-correlated neuron has a correlation of 0.3 or smaller." A manual review of 50 neurons versus 50 features found the neurons "significantly less interpretable", "typically activating in multiple unrelated contexts". **[S: search summary of the paper, consistent with my prior knowledge]** One LessWrong commenter argued those correlations were actually "remarkably high" (https://www.greaterwrong.com/posts/zzmhsKx5dBpChKhry/comments-on-anthropic-s-scaling-monosemanticity). Caveat: these were residual-stream SAE features compared against neurons, and Claude 3 Sonnet is not Qwen3.
  - *Circuit Tracing* (Ameisen et al., 2025, https://transformer-circuits.pub/2025/attribution-graphs/methods.html): "both CLTs and PLTs substantially outperform the Pareto frontier of thresholded neurons" on sort and contrastive interpretability evals. Also "higher neuron activations are increasingly interpretable", which is consistent with C4: neurons look clean at the top and messier below. **[V]** The essay counters that the largest CLT "predicts the same next word as the original only half the time" (line 966). That is true (the paper says "~50%"), but neuron explanations face the same question in another form (see C8).

### C5. Residual stream, attention and early-layer token features are where packing likely lives [V/I]
- The essay concedes the residual stream may hold "a continuous version of packing" (line 1356) and that attention is mostly out of scope (line 1382).
- *When Models Manipulate Manifolds* (Gurnee, Ameisen, Kauvar, Tarng, Pearce, Olah, Batson, Oct 2025, https://transformer-circuits.pub/2025/linebreaks/index.html): character counts in Claude 3.5 Haiku are "represented on low-dimensional curved manifolds discretized by sparse feature families", and attention heads "twist" those manifolds. This is real, safety-neutral computation that is naturally geometric rather than neuron-aligned. **[V via abstract]**
- Gurnee et al. 2023, *Finding Neurons in a Haystack* (https://arxiv.org/abs/2305.01610): "early layers make use of sparse combinations of neurons to represent many features in superposition," while "middle layers have seemingly dedicated neurons." **[V]** The essay answers the specific "social security" case by saying that direction is unused and that the network's actual route is ordinary composition (lines 1123, 1963). This is a single-example rebuttal of a broader finding.
- **For control [I]:** much of the safety-relevant computation, such as tracking that "this is an eval", carrying a plan across tokens, or moving secret information, may run through attention and the residual stream, where the essay has the least evidence.

### C6. Theory says computing in superposition is possible and cheap, so absence of evidence is weak [V/I]
- Adler & Shavit, *On the Complexity of Neural Computation in Superposition* (https://arxiv.org/abs/2409.15318, v3 Feb 2026): pairwise AND over m′ features can be computed with O(√m′ log m′) neurons. A network with n neurons can compute up to O(n²/log n) features, and "the number of parameters is a good estimator of the number of features a neural network computes." **[V]**
- If the optimizer can do this, then where capacity is tightest (rare facts, long-tail behaviours, frontier models trained on far more data than parameters), packing might be used even if the audited cases look clean [I].
- **Counterweight that favours the essay:**
  - Bhagat, Molas-Medina, Giglemiani, Heimersheim (Jun 2026, https://arxiv.org/abs/2606.14673) show that the main toy model of "compressed computation" gets its gains from residual-stream mixing noise and "is not a suitable toy model of computation in superposition". **[V]** Empirical toy evidence for computation in superposition is therefore thinner than believed.
  - Ivanitskiy et al. (Aug 2026, https://arxiv.org/abs/2608.27540) is purely theoretical (frame theory and compressed sensing recovery bounds) and makes no claim about real LLMs. **[V]**

### C7. Safety-specific: deception can be trained to hide from activation monitors [V]
- Essay: "[deception] has no reason to hide from the model's own circuitry. It needs to be accessible to its readers, and if we become a reader, it should be accessible to us too" (line 1496).
- Bailey, Serrano et al., *Obfuscated Activations Bypass LLM Latent-Space Defenses* (arXiv 2412.09565, ICLR 2026): SAEs, probes and latent OOD detectors are all vulnerable. Attacks "can often reduce recall from 100% to 0% while retaining a 90% jailbreaking rate". On a complex task (SQL) there is an "obfuscation tax". **[V via abstract summary]**
- McGuinness, Serrano, Bailey, Emmons, *Neural Chameleons* (arXiv 2512.11949; ICLR/NeurIPS 2026): models fine-tuned to evade probes for benign concepts on a trigger **zero-shot evade unseen deception and harmfulness monitors**, including monitors trained afterwards on the frozen model. This holds across Llama, Gemma and Qwen. Evasion works by shifting activations into a low-dimensional subspace. Multilayer and non-linear probes resist better but are still evaded. **[V via abstract summary]**
- **[I]** The essay's argument holds for a model under *no* pressure against the monitor. AI control assumes the opposite: an untrusted, possibly scheming model, and training that might select against monitors. Whether a neuron- or circuit-level monitor resists evasion better than a linear probe is **untested**. If the model must still route the deceptive computation through legible neurons that downstream circuits read, evasion might be harder, or it might just move the computation. **This is the single most important open question for the user's project.**

### C8. Legible neurons are not a faithful account of behaviour [I]
- The essay criticizes replacement models for imperfect fidelity (line 966). Studying the original network is trivially 100% faithful because nothing is replaced. The real test is whether the *explanations* predict behaviour: activations, ablation effects, and above all *when the model will do X*.
- The essay reports specific targeted ablations that work. Examples: removing 18 "Lion King step" neurons gives P(Scar) 0.24 versus 0.91 for random ablations (line 1061). Removing 8 Santa negative-pole neurons gives P(Santa) 0.059 versus 0.997 for random (line 1067). Edge-motif ablations give a median margin drop of 0.86 versus 0.03 logits (line 2066).
- These are good, but they are selected examples. There is no population-level number such as "fraction of next-token behaviour predicted from neuron explanations alone", which is what would let a control evaluator trust a neuron-based monitor.

### C9. Neurons are not canonical across seeds [V/I]
- Gurnee et al. 2024, *Universal Neurons in GPT2 Language Models* (https://arxiv.org/abs/2401.12181): "1-5% of neurons are universal," i.e. consistently matched across random seeds. **[V]**
- The essay's own seed experiments show divergent outcomes ("two seeds fall below 2%. The third retains 64%", line 2227).
- **[I]** This does not contradict "legible" (each seed's neurons can be legible but different). It does weaken the idea of neurons as *the* natural units, and it means a neuron-level monitor must be rebuilt per model. For control that is cost, not impossibility.

### C10. Tension inside Goodfire and incentive notes [V/S]
- Goodfire's parameter-decomposition team (Bushnaq, Braun, Sharkey) argues that sparse dictionary learning sees "the shadows that computations cast on activations, but not the computations themselves," and that "training bigger SAEs on the same model doesn't converge on a 'true' decomposition" (https://www.goodfire.com/research/stochastic-param-decomp, Jun 2025). They published *Interpreting Language Model Parameters* (VPD, May 5, 2026). **[V]**
- Gorton & Lewis (Goodfire), *Adversarial Examples Are Not Bugs, They Are Superposition* (arXiv 2508.17456, 2025), argue superposition may be "a major contributing factor, or even the primary cause" of adversarial examples, using ResNet18 SAE evidence. **[V]** The essay's "Where Adversarial Examples Go" section (line 1887) argues instead that attacks "take ordinary routes" in ConvNeXt. Lee Sharkey and Owen Lewis are thanked for discussions (line 2480).
- So this is an **unresolved disagreement within Goodfire**, and the essay is framed as Cammarata's personal view.

---

## 5. Prior evidence that supports the essay (for balance)

- **Anthropic itself said superposition was under-evidenced.** SoLU (Elhage et al., 2022, https://transformer-circuits.pub/2022/solu/index.html): "superposition is often treated as the default hypothesis … but there is little evidence." The paper then calls its SoLU results "moderate evidence for preferring the superposition hypothesis." SoLU raised the share of neurons with a clear hypothesis "from 35% to 60%". **[V]** The same paper warns SoLU "may be making some features more interpretable by 'hiding' others", possibly recovering them later with LayerNorm. **[V]** That cuts both ways: an architecture change that makes neurons cleaner can also hide things.
- **Polysemanticity has non-superposition causes.** Lecomte et al., *What Causes Polysemanticity?* (arXiv 2312.03096): "incidental polysemanticity" arises even with enough neurons, from initialization, regularization and noise. **[V]** This is consistent with the essay's claim that the causes are ordinary and fixable.
- **Sparse MoE pushes toward monosemantic neurons.** Chaudhari, Nuer, Thorstenson, *Sparsity and Superposition in Mixture of Experts* (arXiv 2510.23671): "models with greater network sparsity exhibit greater monosemanticity." Herbst, Lee, Wermter, *The Expert Strikes Back* (arXiv 2604.02178, 2026): expert neurons are "consistently less polysemantic", and the gap widens with sparser routing. **[V via abstracts]** This supports the essay's "experts as an anti-superposition architecture" (line 1243).
- **Scale helps.** Gurnee 2023: "increasing scale causes representational sparsity to increase on average"; middle layers have "seemingly dedicated neurons". **[V]**
- **SAEs underdelivered.** GDM's *Negative Results for SAEs on Downstream Tasks* (Smith, Rajamanoharan, Conmy, … Nanda, Mar 2025): SAEs underperformed linear probes on out-of-distribution harmful-intent detection, and the team deprioritised SAE research. **[S]** Goodfire's own team says bigger SAEs don't converge (above). This supports "decompositions aren't necessary first".
- **The neuron basis is privileged.** Elhage, Lasenby, Olah, *Privileged Bases in the Transformer Residual Stream* (2023, https://transformer-circuits.pub/2023/privileged-basis/) provisionally blames Adam for basis-aligned outlier dimensions. **[V]** This matches the essay's "single unread dimension" and large-coordinate observations (lines 1358, 1598). MLP neurons have a privileged basis from the elementwise nonlinearity, which is the essay's home turf.
- **The essay's vision evidence is quantitative and strong.** InceptionV1 squeezed to 10 channels broadens rather than superposes (lines 632–735). Last-layer SAE activity is 88% near-copies of neurons (line 815). Weak-activation ablation tables (line 1662+). These are well-designed tests in the domain where the original worry came from.

---

## 6. Verdict

**Likely right (high confidence):**
1. Several canonical polysemantic examples were misread or were tool artifacts (cat/car → "V"; the Zoom In car→dog "superposition" circuit). This is checkable and the essay shows its work.
2. Modern large, gated (SwiGLU) and especially sparse-MoE models have far more legible MLP neurons than GPT-2-era or one-layer toy models. Independent MoE and scale literature points the same way.
3. Superposition was adopted as a default with thin evidence (Anthropic said so in 2022). Agentic, neuron-first "normal science" scales and finds real structure, such as SwiGLU double-negative echoes (about 4% of neurons) and negative-pole circuits.
4. You do not *have to* train a decomposition before doing useful mechanistic work.

**Plausible but contested (medium confidence):**
1. The about-90% "one main job" figure: preliminary, pole-based, threshold-dependent, self-graded, methods unpublished, not replicated.
2. "Recursive generalization" as the general explanation of the remaining polysemanticity. It is mostly supported by examples and training-dynamics observations in vision.
3. Weak activations being semantically unimportant in **LLMs**. This is quantified only in vision.
4. The residual stream and attention being "not a bottleneck". The essay itself admits weak evidence here.

**Likely overstated, especially for AI control:**
1. "Superposition was the wrong explanation" as a general claim. It holds for the narrow sense. The broad sense (more features than dimensions, distributed computation) is set aside, not refuted.
2. "Deception … has no reason to hide from the model's own circuitry." This is false under adversarial optimization against monitors (Bailey et al.; Neural Chameleons). Whether neuron-level reading is more robust is unknown.
3. "Ambitious interpretability will be solved by the time we need it" (tweet framing). This is a forecast, not a finding.

---

## 7. What this opens up for an AI-control "white-box vs black-box" project (open questions and experiments) [I]

1. **Neuron-monitor versus black-box monitor on standard control games.**
   - Use Qwen3-32B or Qwen3.6-35B-A3B. Both are the essay's audited models, and Goodfire released 1,000 neuron papers (`source/neuron-papers.json`).
   - Run them as the untrusted model in ControlArena-style settings (APPS backdoors, Bash tasks, SHADE-Arena-like sabotage).
   - Compare: (a) a trusted-LLM black-box monitor; (b) a linear deception probe (Goldowsky-Dill et al., ICML 2025, AUROC 0.96–0.999 on Llama-3.3-70B, but "insufficient as a robust defence"); (c) a **neuron/circuit-level monitor** built from identified neurons (deception, sabotage, eval-awareness, "say-not" neurons).
   - Report the **black-to-white performance boost** (Parrack, Attubato, Heimersheim, arXiv 2507.12691), which found only "weak but encouraging" boosts for existing probes. Beating that baseline would be a clean, publishable "win" condition.
2. **Adversarial robustness head-to-head.** Replicate the Neural Chameleons protocol (trigger-conditioned probe evasion), then test whether evasion transfers to a neuron-level monitor.
   - **Win:** neuron and circuit monitors stay robust when linear probes fail.
   - **Lose:** the model shifts computation to unmonitored neurons or attention.
   - **Continue:** partial robustness, with an obfuscation tax on capability (Bailey et al. found one on SQL).
3. **Independent replication of the 90% figure.** Use a random (not curated) neuron sample with blinded raters, a pre-registered "one job" rubric, and held-out predictive tests (activation precision/recall on a new corpus, à la Huang et al. 2023). Count neurons and poles separately.
4. **Completeness test:** can a monitor using only neuron explanations predict, on held-out episodes, *when* the model will take the bad action? Measure AUROC and false-positive rate at a fixed audit budget, the quantity control protocols actually need.
5. **Weak-activation stress test in LLMs:** port the essay's vision percentile-ablation tables to Qwen. Measure the cost in loss and on safety-relevant behaviours when activations below the p95 are zeroed. This directly tests the superposition-lives-in-weak-activations critique.
6. **Residual-stream and attention gap:** test whether safety-relevant signals (e.g. eval awareness) are recoverable from neurons alone, or only from residual or attention directions.

---

## 8. Sources

Essay and reception:
- https://already-clean.goodfire.com/ (local: `source/already-clean.txt`)
- https://www.lesswrong.com/posts/x4kvabkF2Jk8GLZp8/linkpost-neural-networks-are-already-clean
- https://www.greaterwrong.com/posts/x4kvabkF2Jk8GLZp8/linkpost-neural-networks-are-already-clean
- https://news.ycombinator.com/item?id=50105647
- https://huggingnews.com/ai/nick-cammarata-finds-ai-models-legible-reversing-prior-consensus-ab687d62
- https://ecosistemastartup.com/goodfire-90-de-las-neuronas-de-la-ia-ya-se-entiende/
- https://x.com/nickcammarata

Prior literature:
- Toy Models of Superposition: https://arxiv.org/abs/2209.10652
- Softmax Linear Units: https://transformer-circuits.pub/2022/solu/index.html
- Scaling Monosemanticity: https://transformer-circuits.pub/2024/scaling-monosemanticity/ ; LW critique of its neuron comparison: https://www.greaterwrong.com/posts/zzmhsKx5dBpChKhry/comments-on-anthropic-s-scaling-monosemanticity
- Circuit Tracing (2025): https://transformer-circuits.pub/2025/attribution-graphs/methods.html
- When Models Manipulate Manifolds: https://transformer-circuits.pub/2025/linebreaks/index.html
- Privileged Bases in the Transformer Residual Stream: https://transformer-circuits.pub/2023/privileged-basis/
- Finding Neurons in a Haystack: https://arxiv.org/abs/2305.01610
- Universal Neurons in GPT2: https://arxiv.org/abs/2401.12181
- Rigorously Assessing NL Explanations of Neurons: https://arxiv.org/abs/2309.10312
- An Interpretability Illusion for BERT: https://arxiv.org/abs/2104.07143
- What Causes Polysemanticity?: https://arxiv.org/abs/2312.03096
- Sparse Feature Circuits: https://arxiv.org/abs/2403.19647
- On the Complexity of Neural Computation in Superposition: https://arxiv.org/abs/2409.15318
- Compressed Computation is (probably) not Computation in Superposition: https://arxiv.org/abs/2606.14673
- Towards a mathematical theory of superposition: https://arxiv.org/abs/2608.27540
- Feature Superposition in Neural Networks: From Theory to Practice (survey): https://arxiv.org/abs/2609.06862
- Sparsity and Superposition in MoE: https://arxiv.org/abs/2510.23671
- The Expert Strikes Back: https://arxiv.org/abs/2604.02178
- Obfuscated Activations Bypass LLM Latent-Space Defenses: https://arxiv.org/abs/2412.09565
- Neural Chameleons: https://arxiv.org/abs/2512.11949
- Detecting Strategic Deception with Linear Probes: https://arxiv.org/abs/2502.03407
- Benchmarking Deception Probes via Black-to-White Performance Boosts: https://arxiv.org/abs/2507.12691
- GDM SAE negative results: https://www.alignmentforum.org/posts/4uXCAJNuPKtKBsi28/ (via greaterwrong mirror)
- Goodfire parameter decomposition: https://www.goodfire.com/research/stochastic-param-decomp ; https://www.goodfire.ai/research/interpreting-lm-parameters
- Goodfire adversarial-superposition: https://arxiv.org/abs/2508.17456
- Goodfire research index: https://www.goodfire.com/research
- Curve Detectors: https://distill.pub/2020/circuits/curve-detectors/ ; Zoom In: https://distill.pub/2020/circuits/zoom-in/

## 9. Uncertainties

- Reception is day 0. Expert rebuttals, if any, will appear over the coming days or weeks. Re-check LessWrong, the Alignment Forum, and X replies from Nanda, Olah, Sharkey, Bushnaq, Gurnee and Batson.
- Several prior-literature numbers came via search or WebFetch summaries of the abstracts or pages, not my own full read: Scaling Monosemanticity's 82%, Bailey et al.'s 100%→0%, the GDM SAE result. They match my prior knowledge, but should be spot-checked before publication.
- The Bereska "precision to alchemy" quote is second-hand via a Spanish write-up and concerns Silico, not this essay.
- I could not read the forthcoming companion paper, so I could not check the 90% methodology (rubric, sampling, thresholds, rater agreement).
- The pole-versus-neuron accounting critique (C3) is my inference from the essay's wording. The companion paper may report neuron-level numbers that resolve it.
