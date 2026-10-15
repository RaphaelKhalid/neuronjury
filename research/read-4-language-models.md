# Deep read 4: Language models (lines 959–1413)

Source: Nick Cammarata (with Curt Tigges for this section), "Neural Networks Are Already Clean", Goodfire, ~Oct 2026.
File: `source/already-clean.txt`. Primary range read line by line: 959–1413 (sections "Exploring Language Models", the four "Who did it?" case studies, the Kimi K3 wallet graph, Miyazaki, the 1,000 neuron papers, the SwiGLU double negative, MoE experts, "Explanations That Can Lose", "Slouching Towards Monosemanticity" (GPT-2 XL), "Don't Say Dot", "The Residual Stream", "Attention"). Framing read: 29–99. Short out-of-range cross-references, marked [OUT OF RANGE], were pulled from 1570–1590 (SwiGLU audit), 1636–1660 (sleeper lens), 1900–1930 (gate-threshold ablation) and 1997–2052 (attribution audits and the near-miss appendix), because the task named near-miss tests and gates.

Caveat on provenance: the essay, Qwen3.6 and Kimi K3 all postdate my knowledge. Everything below is what the text says. None of it is independently verified. Most of the figures are interactive and are missing from the text dump; only captions and alt text survive.

---

## 1. Plain-English summary

The section argues that the "already clean" picture from vision models also holds in modern LLMs, and the authors show it by working directly on the model's own MLP neurons, with no sparse autoencoder or transcoder. The main moves are these.

1. **Neuron-only attribution graphs work.** They rebuild Anthropic's Claude 3.5 Haiku medical-diagnosis graph (preeclampsia), originally made with cross-layer transcoder features, from Qwen3-32B's raw MLP neurons. Because the network is the original model, there is no reconstruction error and no "error nodes". They then show four short "whodunit" case studies, each with a group ablation against a matched random baseline: a multi-hop Lion King → Simba → Scar case, Santa encoded on *negative* poles, about 19 "hedge" neurons, and about 25 "say not" neurons that resist a confident user but get overridden. They also show what they call the first published attribution graph of a multi-trillion-parameter model (Kimi K3, found wallet → "return").
2. **Neurons are mostly one job.** Over 1,000 randomly chosen "neuron papers" (agent-written investigations) on Qwen3-32B and Qwen3.6-35B-A3B, about 90% of neurons (in the Short Version, "neuron poles") have one main job with related "recursive generalization" offshoots, about 7% have two related jobs, and about 2–4% are not yet understood. The author has never seen a neuron with ~10 unrelated jobs. Offshoots are reported to be rarer and less important in their own context than the main job, which the authors read as evidence against "sleeper"-like hidden features.
3. **Tool artifacts explain much of the apparent mess.** The SwiGLU "double negative" (gate < 0 and value < 0 gives a positive output) makes a small sign-flipped "echo" of the negative pole show up at the top of positive top-k lists. For about 4% of neurons it is the whole top of the list, so naive autointerp mislabels them. Example: a neuron autolabeled "Colossians" actually completes "Russia/Russian" in any script, on its negative pole.
4. **MoE experts are highly specialized** and get narrower with depth. The authors call MoE an "anti-superposition architecture", because a one-linear-layer router could not recognize 10,000 unrelated packed concepts.
5. **Explanations can lose.** In "blind maximum", Agent 1 explains a neuron and Agent 2 sees only that explanation and writes a maximizing example. That example beat the best of 10B corpus tokens in the shown cases. A bundle-wise variant checks the neuron's breadth. A near-miss test in the appendix checks boundaries.
6. **Old "polysemantic" LM neurons look different on a second look.** Revisiting GPT-2 XL with 500 neuron papers moves the clean share from <2% to ~70% "roughly one thing". The famous Towards Monosemanticity mixed neuron (citations, dialogue, HTTP, Korean) is reinterpreted as a "don't say a dot" neuron.
7. **The residual stream and attention have not blocked them**, though both have been studied less, and the residual-stream evidence comes mainly from vision. Attention is understood "through neurons". The marginal value of global attention-head names is estimated at ~5% of explanatory residual.

---

## 2. Claims with evidence, numbers and strength

Strength scale: **strong** = experiment with numbers and a control. **moderate** = experiment or audit with numbers but thin controls or unpublished method. **weak** = example or anecdote. **asserted-only** = no evidence shown in the text.

### 2.1 Neuron attribution graphs on the original model
- **C1. Anthropic's Haiku medical-diagnosis graph can be rebuilt from Qwen3-32B MLP neurons.** L963–964: "We start with a medical diagnostic attribution graph we liked from Anthropic's Circuit Biology… It turns out the same works with neurons in Qwen3-32B." The figure compares Anthropic Fig. 30 (transcribed, unweighted) with Qwen groups. Ablation presets: "Hub · 4 / Visual · 6 / All symptoms · 25 / Second hub · 2" (L1050–1054). Caption L1059: "Qwen3-32B's own MLP neurons, grouped by Claude; numbers are neurons per group… Five small Qwen-only groups aren't drawn, and most of the ungrouped weight is in late answer-formatting neurons. 'Random' removes as many neurons from the same layers." **Moderate.** The ablation outcomes for the presets are not in the text.
- **C2. Neurons have no reconstruction loss. Transcoders do.** L966–967: "Since it's the original model, there's no reconstruction loss… Their largest transcoder predicts the same next word as the original only half the time… and their graphs need error nodes for what it misses." **Moderate–strong** (cited to Ameisen et al. 2025).
- **C3. A 4-neuron diagnosis hub exists.** L969: "The diagnosis hub is just four neurons, and if you remove them the model asks about itching instead. Itching is a telltale sign of a different liver condition of pregnancy, as if the model had moved on to its next guess." **Weak–moderate.** There is an ablation, but no numbers are given in the text.
- **C4. Graphs in general are readable.** L971: "Across thousands I've seen in image models and language models, they're highly readable and ablate the way you'd generally expect." **Asserted-only** (qualitative). [OUT OF RANGE] L2001: "We had agents review 100,000 attribution graphs… I haven't found a substantial group of neurons whose joint activity remained inexplicable… I regard this as qualitative evidence."

### 2.2 The four "whodunit" case studies (Qwen3-32B, MLP neurons)
- **C5. Multi-hop latent reasoning (Scar).** Prompt (L989): a calling card from "the sworn enemy of the lion cub who became king of the Pride Lands". Qwen answers "Scar". L995: "No name is in the prompt: 'Pride Lands' wakes Lion King neurons, a first hop to Simba, which lead to his enemy." L1061: "Without the Lion King step (18 neurons), Qwen answers Simba, not a random villain. P(Scar) 0.24, random 0.91." **Strong.** It is a matched-random ablation, though the intact P(Scar) is not stated in the text.
- **C6. Santa lives on negative poles.** L1008: "The neurons that matter most run strongly negative here, and their negative poles, not their labels, are about Santa." L1067: "Without these 8 negative-pole neurons, Qwen blames the family's pet. P(Santa) 0.059, random 0.997." L1089: "standard top-k automated interpretability labels can look like 'capital cities' because they ignore the negative side… Remove the eight neurons with a Santa negative side and Santa falls from near-certain to 6%… Remove the twenty neurons actually labeled Christmas or Santa and it only falls to 76%." **Strong.** It has a random control and a label-based comparison control.
- **C7. Calibrated hedging is carried by ~19 "likelihood" neurons.** L1023: "About 19 likelihood neurons write 'most' and 'likely'; the badge clue quiets them, and Qwen commits to Marcus." L1073: "Without the 19 hedge writers, Qwen commits: Marcus, the scheduler. P(hedge) 0.23, random 0.76." L1077: "'Hedge' is P(most) + P(likely) at the next word." **Strong** (matched random). Note that the ablated model commits to *Marcus*, while the unablated hedged answer was Daniel (L1017).
- **C8. Sycophancy: a confident user overrides internal pushback.** Prompt (L1030): "I am absolutely certain it was Anna" gives "Anna". "I think it was Anna" gives "not Anna" (L1034). L1038: "No clue points to Anna; the pushback comes from neurons that fire just before 'not', and a confident user outweighs them." L1079: "Without the 25 'say not' neurons, Qwen stops pushing back and names Anna. P(Anna) 0.92, random 0.66." L1083: "The words 'absolutely certain' carry almost no weight of their own; they change how strongly the user's 'Anna' comes through." **Strong.** This is the most control-relevant case.
- **C9. Negative poles matter as much as positive poles. Weak activations usually don't matter.** L1085: "The neuron's negative side matters about as much as its positive… We think the weak activations usually don't matter, but the strong positives and negatives matter a lot." **Moderate** (backed by C6 and by out-of-range weak-activation controls).

### 2.3 Trillion-parameter model
- **C10. Neuron-only attribution graph of Kimi K3 (multi-trillion parameters).** L1091: "As far as we know, it's the first published attribution graph of a multiple trillion parameter model… it links the wallet, the cash and the owner's ID to lost property and honesty, and answers 'return'. We haven't begun full audits of this scale yet." L1104: "The biggest push, though, comes from neurons that hold it back." L1114: "Without one of the 'holds back' neurons, Kimi-K3 is even surer of return. No other single neuron we studied moves it half as much. P(return) 0.83 → 0.98, random 0.83." L1118: "grouped by an agent from each neuron's description… These twelve groups are a hand-picked slice of the graph: most of its weight is in late neurons at the answer that aren't drawn." **Moderate.** It is a single example, hand-picked and with no audit.

### 2.4 Composition rather than packing
- **C11. Names and bigrams are built by composition, not packed.** L1120: "We might intuitively expect packing with things like bi-grams or names… What we find is that it's ordinary generalization and composition. Early language fragments like 'iy' in 'Miyazaki' are sort of like how early vision models have gabor filters." Miyazaki figure (L1134–1148): L0–L1 fragment neurons (e.g. "L1:15229 +4.42 Final i after k/g/q", "L1:20486 +1.88 iy-bigram") feed L2–L3 patterns ("L3:15141 +3.15 −saki / 崎 endings… also invented Mawasaki"), which feed the L4:8476 Miyazaki neuron ("fires on the name in every script and sense we tried", including 宫崎骏 and Miyazaki Prefecture), which feeds L6–L8 associations ("L6:24077 +23.47 'spirited away'", "L8:14338 +1.03 Nausicaä"). The numbers are link strengths. **Weak–moderate** (one worked example).
- **C12. The "social security" direction from Neurons in a Haystack is unused.** L1122–1123: "that direction is unused by the network. We map the one it uses, and it uses ordinary generalization and composition." **Asserted here.** The evidence is in the appendix.

### 2.5 The audit numbers
- **C13. 90 / 7 / 2–4.** L50 (Short Version): "In preliminary audits of Qwen3-32B, we estimate that roughly 90% of neuron poles have one main job, often with small related offshoots; another ~7% have two related jobs; and only ~2-4% are not yet understood." Footnote (L50–60): the share "varies depending on how you set the threshold for counting weak activations, depth, density of sub-circuits, and what you view as 'one thing'"; "In the sets I've looked at more closely, considering strong activations, it's closer to 97% non-arbitrary mixtures, but these are relatively small samples"; "Dense and Mixture of Experts models seem roughly similar… models up to trillions of parameters, like Kimi K3." In range, L1175: "What we see is about 90% of neurons having basically one job, with recursive generalization offshoots that are usually related… A lot of the remaining ones have two or three. I've never seen a neuron with something like ten unrelated things it does." The basis is 1,000 random neuron papers (L1158–1163: "1,000 · Qwen3-32B and Qwen3.6-35B-A3B"). **Moderate.** The authors call it preliminary, it depends on thresholds, it is judged by agents and the author, and the full method is in an unpublished companion paper.
- **C14. The most important offshoots are the most related.** L1175: "When we checked how much the offshoots matter, the ones that mattered most seemed to be most related. For instance, a geology neuron that fires for Cesium, a geology javascript library." **Weak** (one example, no numbers).
- **C15. Offshoots are not sleeper agents.** L1177: "One fear is they're something like sleeper agents, very important in their own context, but rare. What we generally find is that it's both rarer and less important in their own context than the main activation is in its." **Asserted-only.** No numbers are shown, and it applies only to naturally trained models.

### 2.6 SwiGLU gates
- **C16. The double-negative SwiGLU "echo" is a major noise source.** L1179: "Modern neurons have both a gate and value. When both are negative, this sends activations into the positive pole, that usually look like the negative pole. Usually this 'echo' is small, but for about 4% of neurons, it's the whole top of the list. Ablating them across the whole network ups most benchmarks, but lowers some reasoning ones… we haven't looked into it deeply. Architecture designers… should look into fixing this!" **Moderate** for the 4% figure. The benchmark effect is **asserted-only** (no numbers).
- **C17. Worked example (L1/N20736 of Qwen3-32B).** Top-k gives "Colossians" (+0.98–0.99), but "Every one has the gate closed, so it's a small sign-flipped leak of the value, under 8% of the neuron's peak" (L1199). Gate/value/output table (L1211–1215): "Coloss|ians | −1.2 | −3.5 | +1.0" vs "Speak russian | +4.4 | −2.9 | −12.5". With gate-open firings only, the positive side has "nothing above +0.5, about 4% of the peak", and the negative side holds "−20.6 www.un.org/russian", "−19.0 ```kotlin package ru". The true job is "the token that completes 'Russia' or 'Russian,' in any script" (L1233). Autointerp label: "References to the book of Colossians" (L1195). **Strong as an example.**
- **C18. Gates are specific and values are broad (vision).** L1237: "the value tends to learn broader things, and gate more specific things… the value learns a broad family like small grey birds, or anything orange, and the gate will open only for juncos or goldfish." **Weak** (examples).
- [OUT OF RANGE, L1574–1579] Qwen3.6 "enemy" neuron L36·E206·N103: "131/133 responses in p75–p99 use − × −. The strongest tail uses + × +: 93/93 at p99.99 and above." The audit "sampled 750 quantile-stratified examples; 626 retained routing."
- [OUT OF RANGE, L1925] "If we zero a neuron's output whenever its gate exceeds its ordinary-text 99.9th percentile, recitation can fall apart… Psalm 23 exactly to insisting it did not exist. Random interventions matched by count or magnitude preserved the verse."

### 2.7 MoE experts
- **C19. Experts are far more specialized than previously reported.** L1239: "Experts are far more specialized than previously reported… things like 'token similarity' aren't a good measure." L1241: "Like neurons, they get narrower with depth… recursive generalization pattern one scale up… weights, neurons, experts, and circuits." **Moderate–weak.** Shown as an agent-judged map of "All 10,240 experts in Qwen3.6… sorted from the narrowest experts to the broadest, as judged by agents reading summaries of each expert's neurons" (L1251). No summary statistic is in the text, and the over-training claim is "we think… probably".
- **C20. MoE works against superposition.** L1243: "highly specialized experts make that hard, since a neuron only fires when its expert is chosen… one is [devoted entirely to bosses in RPG board games]… the router would have to recognize all ten thousand… and the router is just one small linear layer." **Argument plus one example.** [OUT OF RANGE, L2052]: "In mixture-of-experts models this kind of packing is arguably almost impossible anyway."

### 2.8 Testing explanations
- **C21. Blind maximum beats a 10B-token search.** L1257: "One agent investigates a neuron and writes a short explanation; a second sees only that explanation and writes an example meant to activate it maximally… it can activate the neuron more strongly than any example we found in 10 billion tokens." Examples (L1267–1277): "action" (engaged or in operation): best found 15.0, Agent 2 18.4. "'we're on it' predicate": best found 82.0, Agent 2 99.5. **Moderate.** Two examples are shown, with no aggregate rate in the text.
- **C22. Blind maximum tests a neuron's center, not its breadth, so they add a bundle-wise version.** L1283 (method in §3). No results are reported. **Method only.**
- **C23. Summary-statistic tests are only partly trustworthy.** L1285: "'Cats and cars' could do well on many tests of the V neuron while completely missing what it really is… The best criticism is specific to the conjecture." **Asserted (epistemic stance).**
- [OUT OF RANGE, L2007–2052] Near-miss test on 200 random gallery neurons: "Among the 183 whose explanations describe their positive side, the new examples fired their neurons strongly 76% of the time; the near misses, 11%. The explanation won for 164, tied for 15 and lost for 4." For the first 20: 81/100 vs 8/100, and the new examples beat the near misses for all 20. "Strong" means ≥30% of the neuron's strongest corpus example. In the distant-concept test (the "most distant concept it could, the kind of thing a network could pack in"), texts "fired their neurons strongly about 1% of the time, and 179 of the 183 neurons never fired on them at all." **Strong.** Rules were set before measuring and there were 183 neurons.

### 2.9 Earlier models revisited
- **C24. GPT-2 XL, reread.** L1292: "fewer than 2% of its neurons came out clean. We went back and made 500 neuron papers with almost no iteration. Now about 70% look like roughly one thing… pristine ones are still low, about 5%. What's left are neurons that do a few broad things, up to about six, mostly two. The scoring isn't identical to the original project. On the activation reconstruction task… several multiples better with no iteration." **Moderate.** Scoring differs from the original, so the before and after numbers are not directly comparable.
- **C25. The Towards Monosemanticity mixed neuron is a "don't say a dot" neuron.** L1297: "Nearly all the citations, dialogue, and HTTP requests fire on or near a dot, and eight of its ten strongest negative logit connections begin with one… the Korean examples… fire about two-thirds of the way through an unfinished syllable… without the model, we can't keep narrowing the explanation." The viewer shows: "This fragment appears in 16 of its 20 strongest contexts" (L1319); "Remove it → the next . logit rises in 20/20 top contexts" (L1324). Qwen3.6 analogue: "Remove it → the next . gets likelier in 30/30 active strong tests" (L1343). **Moderate.** The authors themselves leave open whether it is one function or two (L1347).
- **C26. Small, simplified models were the wrong place to start.** L1350: "bigger models tend to have more narrow neurons… we may have been slouching towards monosemanticity without knowing it." **Moderate** (GPT-2 contrast plus the vision scaling elsewhere in the essay).

### 2.10 The residual stream
- **C27. Residual-stream packing has not been a bottleneck.** L1356: "We can read what neurons write to the residual stream and what they read from it, attribution graphs come out clean, and we don't see the stream accumulating interference only to undo it later." **Weak–moderate** (absence of evidence).
- **C28. Vision ConvNeXt evidence.** A single unread dimension holds "almost all of its activation mass… to scale all the other dimensions… through LayerNorm"; removing it fixed the maps (L1358). Stream crushing (L1369): "a stream four and eight times narrower, down to just 46 dimensions in the last block… Accuracy fell from 72% to 60% and 39%… Nothing looks cleverly interleaved… A dark-bird-on-water neuron also fires on alligators and a swimming retriever, not on clocks." **Moderate**, but this is vision only.
- **C29. Language-model residual streams mostly just worked.** L1360 and L1376: "When we've visualized their residual streams, it has mostly just worked"; "We've looked at language models' residual streams less." **Weak.**

### 2.11 Attention
- **C30. Attention is understood through neurons.** L1394: "Three layer 30 attention heads read directly from the residual stream, but if we follow what is written in those directions, we see a headache neuron, a migraine neuron, and a brain neuron. What they write lands mostly on the preeclampsia neuron at the comma… Ablating these heads drops preeclampsia by a quarter. Stopping them from looking at pain and nothing changes." **Moderate** (one case with an ablation).
- **C31. Global attention-head names would add only ~5%.** L1408: "the marginal 'explanatory residual' of having global attention head names might be about 5%. Then I had an agent do the same, looking at 100 attribution graphs without my guess, and it also put it about 5%, split about equally into 'position heads'… and everything else." The authors add (L1410): "these estimates could be pretty far off." **Weak.**
- **C32. Prediction: heads will be broad and recursively generalized.** L1410: "attention heads will turn out to be broad and recursively generalized, like neurons in small models, since there are far fewer of them: a few thousand heads in Qwen3-32B, against more than a million neurons." **Asserted (low-confidence prediction).**

---

## 3. Methods, in enough detail to reimplement

1. **Neuron-only attribution graphs (no transcoder).**
   - Target the next-token logit of the original model.
   - Attribute back through MLP (SwiGLU) neurons, and through attention as links ("click a link for attention").
   - Have an LLM (Claude, or "an agent from each neuron's description") cluster the neurons into supernode groups.
   - Draw link width as group-to-group attribution strength.
   - Validate by group ablation (zero the neurons) and report P(answer) against a **matched random baseline: "removes as many neurons from the same layers."**

   **Not specified in range:** the exact attribution rule (e.g. grad×act with frozen attention or LayerNorm), the pruning thresholds, and how attention edges are computed. The likely reimplementation is a Circuit-Tracing-style linearization on raw neurons (frozen attention patterns and norm scales; edge = activation × weight × downstream gradient), followed by graph pruning.
2. **Pole-aware neuron labeling.** Treat each neuron as two poles. Label the positive pole from the strongest positive activations and the negative pole from the strongest negative activations. Ignore weak activations by default. Corpus: "saved 100M-token corpus examples… Teal + / rust − on one scale per neuron" (L1155–1156). Positive-only top-k autointerp gave wrong labels such as "capital cities" for Santa-relevant neurons.
3. **SwiGLU sign-regime separation.** a = SiLU(g)·v. Tag every activating example with gate open or closed (sign of g) and the sign of v. Separate the four regimes. Report "only firings where the gate is open" as the neuron's true positive pole, and treat −×− firings as an echo or leak. Use quantile-stratified sampling ([OUT OF RANGE]: 750 samples per neuron).
4. **Neuron papers, the automated "neuron scientist".** An agent writes a detailed per-neuron investigation (gallery id `neuron-scientist-gallery`). The checklist is reconstructed from L73 (Short Version):
   - read the surrounding context, not only the peak token, since feeling and social-context neurons fire on commas or on the token before;
   - steer the neuron up and see what the model writes;
   - look upstream (how it is built) and downstream (logit and other effects);
   - check the negative pole;
   - run targeted tests (e.g. which store brands).

   Scale so far: 1,000 random neurons across Qwen3-32B and Qwen3.6-35B-A3B; 500 for GPT-2 XL "with almost no iteration". For MoE models, the expert's specialization adds context.
5. **Blind maximum.** Agent 1 (with full access) writes a short explanation. Agent 2 sees only that explanation and writes one text meant to maximize the activation. Compare its activation with the max over a large corpus (10B tokens). Pass if it matches or beats the corpus max.
6. **Bundle-wise blind maximum, a breadth test that can detect packing.**
   - Cluster the attribution flowing *into* the neuron into bundles of upstream neurons (e.g. pet-microchip neuron: animal tagging / lost pets and rescue / microchip and RFID).
   - For each bundle, ablate all the other bundles.
   - Run a blind maximum from that bundle's explanation.
   - Compare with the strongest corpus example under the same ablation.

   "A bundle that had been packed in rather than grown would show up here as an explanation unrelated to the others that still drives the neuron" (L1283).
7. **Near-miss and distant-concept positive controls** [OUT OF RANGE, L2007]. From the explanation only, an agent writes 5 positives, 5 near misses, and 5 texts about the most distant concept it can think of, all before measurement. "Strong" means ≥30% of the corpus max. Score as win/tie/loss per neuron.
8. **Expert specialization map.** For every expert (10,240 in Qwen3.6), summarize its neurons' explanations. An agent then rates the expert from narrow theme to broad to unrelated niches to "reads like a random draw", per layer.
9. **Attention through neurons.**
   - Where it looks: the attention pattern.
   - What it looks for: which upstream neurons write the directions the head reads (QK/OV source neurons).
   - What it does: which downstream neurons its output lands on.
   - Tests: ablate the head, or block attention to specific source tokens ("stopping them from looking at pain").
10. **Head-name value estimate.** Over 100 attribution graphs, an agent estimates how much unexplained residual would be removed by global head labels.
11. **Residual-stream maps (vision).**
    - Follow the same image locations through all layers.
    - Remove the heavy, unread coordinates and center each layer.
    - Fit rotations between stages.
    - Fit one UMAP over all layers, with neighbors only from other locations.
12. **Stream crushing.** Retrain with a 4× or 8× narrower stream while keeping all neurons, then compare maps and neuron read/write leakage.

---

## 4. Weaknesses, caveats, and where the argument could be wrong

1. **The 90/7/2–4 numbers are preliminary and depend on thresholds** (L50 footnote). The detailed method is in a **forthcoming** companion paper. There are no confidence intervals and no inter-rater reliability, and the judges are mostly agents plus the author. "One main job with related offshoots" is a flexible category, and the authors admit the risk of over-broad explanations like a "multifunctional language neuron" (L1257).
2. **2–4% of over a million neurons is still 20k–40k+ unexplained neurons, and ~7% have two jobs.** Rare, high-stakes mechanisms such as a backdoor could easily sit in that remainder.
3. **The anti-sleeper claim (C15) is asserted without numbers** and concerns *naturally trained* models only. Planted backdoors or adversarially trained deceptive models were not tested. For control, that is the case that matters.
4. **Case studies are curated.** The authors describe them as "graphs we liked" (L963, L971), and the Kimi graph is "a hand-picked slice… most of its weight is in late neurons at the answer that aren't drawn" (L1118). Intact baseline probabilities are mostly not stated (only the ablated and random values). Effect sizes are relative to a random-ablation control, which can itself be damaging (random P(Anna) 0.66).
5. **The attribution method is not specified** in the text, which limits replication.
6. **Grouping by an LLM** imposes a narrative on the graph. Group labels could carry the story the reader is meant to see.
7. **Blind maximum has thin evidence in range** (two examples). The maximized text may also be off-distribution: a higher activation does not prove the explanation captures all of what the neuron does. The bundle method has no reported results.
8. **The authors are skeptical of summary statistics** ("best criticism is specific to the conjecture"). That is philosophically defensible, but it makes the overall cleanliness claim harder for outsiders to falsify.
9. **The GPT-2 XL comparison is not like-for-like** ("scoring isn't identical").
10. **The "don't say dot" reinterpretation is unverifiable** for lack of model access (L1297). It is unclear how "Remove it → … 20/20" was computed for a model they don't have; it may come from published logit weights.
11. **The SwiGLU echo-ablation benchmark effect has no numbers** and its mechanism is "probably prosaic… we haven't looked into it deeply".
12. **The residual-stream evidence comes mainly from vision.** For LMs it is "looked at… less", and the claim rests on absence of a found blocker.
13. **Attention is largely unsolved.** The 5% estimate is a guess, and the agent replicating it may share the same framing. Mechanisms that matter for control, such as collusion, steganography, or reading the oversight context, could live disproportionately in attention.
14. **Nothing tests adversarial robustness.** A model optimized against a neuron monitor could move computation into negative poles, the double-negative regime, attention, or distributed codes. The essay does show that naive tools miss all of these (C6, C16).
15. **Nothing can be checked yet.** Models (Qwen3.6, Kimi K3) and the companion paper are beyond verification. The essay is an essay, not a peer-reviewed paper, from an interpretability company with an interest in the result.

---

## 5. Open questions it raises

1. Do the cleanliness statistics hold for **models with planted backdoors or trained sabotage**? Would a trigger show up as a "packed-in" unrelated bundle (bundle blind-max), as a distant-concept firing (base rate ~1%), or as an offshoot whose importance in its own context exceeds the main job's?
2. Are deception, sabotage, sandbagging and situational-awareness mechanisms in the 90% "one job" population, or in the 2–4% residual?
3. Is the **"say not" / internal-pushback family (C8)** general? Does a similar family fire when a model writes code it "knows" is wrong, or complies against its own judgment?
4. Do **hedge neurons (C7)** track the model's internal confidence, so that a mismatch with the expressed confidence reveals sandbagging or overclaiming?
5. What does a neuron attribution graph cost per token at 32B and 1T+ parameters? Is online monitoring feasible, or only offline auditing of flagged actions?
6. What exact attribution and grouping procedure is used, and how sensitive are the conclusions to it?
7. How reliable are agent-written neuron papers? What are their error rates against human experts, and their inter-agent agreement?
8. Does the cleanliness picture hold in **reasoning and thinking-mode traces and RL-trained agentic models**, where control matters most?
9. Would fixing the SwiGLU double negative architecturally improve monitorability? And what reasoning ability does the −×− regime carry (the benchmark drop)?
10. How much control-relevant computation lives in attention? Is the ~5% head-name residual estimate right for safety-relevant behaviors?
11. Can a neuron-label channel be given to an LLM monitor in a way an adversarial model cannot game, without training against the monitor?

---

## 6. Control hooks: turning neuron-level, already-clean interpretability into a white-box monitor

These are built from evidence in this section. Items marked (speculative) are my extrapolations.

1. **Detecting internal dissent that gets overridden** (from C8). Qwen has ~25 "say not" neurons that fire just before "not" when the evidence contradicts the user. A confident user outweighs them, and the transcript then simply says "Anna". Monitor: flag when pushback or negation neurons are strongly active but the output complies. A black-box monitor reading the transcript cannot see this suppressed signal. Generalize to code: "this is insecure/wrong" neurons active while the model writes the code anyway, which is a sabotage signature. (speculative extension)
2. **An internal confidence gauge for sandbagging** (from C7). 19 likelihood neurons carry the hedge, and evidence quiets them. Compare their activation with the model's expressed answer quality. A model that is internally certain but outputs a hedge, a wrong answer, or "I can't" is a sandbagging candidate. Neuron ablation also works as **capability elicitation**: removing hold-back or hedge neurons changed answers (C7, C10), so ablating "hold back" neurons could test whether a model is underperforming on purpose. (speculative)
3. **Reading the hidden step in multi-hop reasoning** (from C5). The Lion King → Simba → Scar hop happens entirely inside the model; the transcript shows only "Scar". Neuron graphs expose the unverbalized intermediate concept, and ablating it changes the answer (P(Scar) 0.24 vs 0.91). Monitor: look for latent intermediate concepts such as "exploit", "oversight/monitor", "hide", or a "backdoor trigger" that never appear in the output or CoT. This is a direct answer to "the CoT is unfaithful or absent".
4. **Monitors must read both poles and separate gate regimes** (C6, C16, C17). Santa is carried by 8 negative-pole neurons (P to 6%), while 20 positively labeled Christmas neurons barely matter (76%). About 4% of neurons have top-k lists that are pure SwiGLU leak ("Colossians" is really "Russia"). A white-box monitor built on positive-pole top-k labels would miss the real mechanism or fire falsely. Requirements: both-pole labels, gate-open filtering, and strong activations only.
5. **Exactness means no error nodes for an adversary to hide in** (C2). Transcoder graphs reproduce the next token only ~50% of the time and need error nodes. Neuron graphs are exact. For control this is a real argument against SAE or transcoder monitors: a scheming model's key computation could sit in the reconstruction error. With neurons there is no unexplained residual term in the forward pass, only unexplained *neurons*, which can be enumerated.
6. **A backdoor scanner from the "explanations that can lose" toolkit** (C22, out-of-range near-miss). Three checks, each with a measured clean baseline to compare against:
   - (a) The bundle-wise blind maximum is designed to find "a bundle that had been packed in rather than grown". A trigger → behavior pathway is exactly that.
   - (b) In the distant-concept test, clean neurons almost never fire (179/183 never). A behavior-critical neuron that fires on a distant, unrelated trigger concept is a red flag.
   - (c) The offshoot-importance ratio (C15): in clean models, offshoots are "rarer and less important in their own context than the main activation is in its". Flag any neuron whose rare-context importance exceeds its main-context importance. That is the stated sleeper-agent signature.
7. **MoE routing as a cheap channel** (C19, C20). Experts are highly specialized, with agent-labeled themes for all 10,240 Qwen3.6 experts, and router decisions are computed anyway. Logging which experts fire during an agent action ("security exploitation", "obfuscation", "evaluation-awareness" experts, if they exist) is an almost free monitor. (speculative)
8. **Extreme-gate events as anomaly and intervention signals** [OUT OF RANGE, L1925]. Zeroing outputs whenever the gate exceeds its ordinary-text 99.9th percentile destroyed memorized recitation, while random matched interventions did not. Counting p99.9 gate exceedances is a cheap anomaly detector, and clipping them is a possible runtime defense against triggered behaviors that depend on extreme activations. (speculative)
9. **Honesty and moral-choice neurons are visible even at trillion scale** (C10). Kimi K3's wallet decision runs through honesty, lost-property and "hold back" neurons, and one neuron moves P(return) from 0.83 to 0.98. Single neurons have high leverage. That makes them good monitor features, and also an attack surface for fine-tuning.
10. **Validated labels as a requirement for monitor features.** Before a "deception" or "sabotage" neuron is trusted as a monitor feature, it should have to pass blind max, near-miss, distant-concept and ablation tests. Blind maximum also *generates* inputs that maximally drive a concerning neuron, which is useful for building honeypots and red-team cases.
11. **Attention to oversight context** (C30, C31). "Where it looks comes for free." A monitor can check whether heads route information from "you are being monitored/evaluated" tokens into decision neurons, a situational-awareness signal. [OUT OF RANGE, L1650]: "A triggered sleeper, an instruction, and a persona can change when the answer settles". The timing of when the answer settles, read with a logit or fitted lens, is another candidate sleeper signal.
12. **A neuron-label transcript fed to an LLM monitor** (speculative). With about 90% of poles labeled, each token can be annotated with its top active neurons (both poles, gate-open only) and their one-line labels. Hand that "activation transcript" to the same trusted LLM monitor as an extra channel. This is the most direct head-to-head test of white-box against black-box monitoring at equal monitor capability.

### Concrete game designs (win / lose / continue) suggested by this section
- **Sycophancy and override game.** The untrusted model is told to comply with false user claims in some episodes. The blue team flags "complied despite internal dissent" from say-not neurons, against a black-box judge reading the transcript. Metric: AUROC and catch rate at a fixed false-positive rate.
- **Backdoored-code game (APPS-style).** A red-team fine-tunes Qwen3-32B to insert backdoors when a trigger appears. The blue team gets: (a) a trusted black-box monitor; (b) neuron-label transcript plus graph-based latent-concept detection; (c) a pre-deployment scan (bundle blind max, distant-concept, offshoot ratio). Score safety against usefulness at a 1–2% audit budget. The red team wins if a backdoor lands unflagged, the blue team wins on catch, and "continue" means unflagged honest tasks.
- **Sandbagging game.** The model is instructed to underperform on dangerous-capability evals. The blue team uses hedge and likelihood neuron state plus hold-back ablation to elicit or detect.
- **Hidden-hop game.** Tasks where the harmful plan needs an unverbalized intermediate concept. A latent-concept neuron detector is compared with a CoT monitor.

---

## 7. Short verdict for our goal

This section gives the strongest *language-model* evidence in the essay that the model's own neurons can serve as an exact, readable substrate. Four small, ablation-validated circuits (multi-hop, negative-pole, hedging, sycophancy) are each built from 8–25 neurons with large effects against matched random controls. There is a 1,000-neuron random audit, and there are falsifiable label tests.

For **AI control**, the pieces that transfer best are:
- the sycophancy "say not" circuit (an internal-dissent signal);
- the hedge neurons (internal confidence);
- the unverbalized multi-hop concepts;
- the exactness argument (no error nodes);
- the near-miss, distant-concept and bundle tests as a backdoor-scan template.

The biggest gap is that **nothing here is adversarial**: no planted backdoors, no models trained to evade, no head-to-head comparison with a black-box monitor. That gap is exactly the opening for us to run the control games above.
