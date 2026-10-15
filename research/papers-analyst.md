# papers-analyst: what the 1,000 "neuron papers" actually show

Source data: `source/neuron-papers.json` (1,000 items, `built` = 1791937716). `source/shelf.json.gz` holds the same `{built, papers}` structure. Essay text: `source/already-clean.txt`. Every number below comes from scripts in `analysis/`. Run them with `python -I <script> source/neuron-papers.json [...]`:

| script | what it does |
|---|---|
| `analysis/01_schema.py` | field inventory, value ranges |
| `analysis/02_shelf.py` | odd items (`q` instead of `m`), status/date by model, shelf.json.gz structure |
| `analysis/03_labels.py` | vocabulary of measurement labels |
| `analysis/04_scores.py` | clean / interesting / f distributions, depth trends, keyword flags, lowest-clean list |
| `analysis/05_selectivity.py` (loose control regex) and `05b_selectivity_strict.py` (strict, primary) | selectivity metrics → `selectivity_rows*.json` |
| `analysis/06_inspect.py` | prints full records for a list of ids |
| `analysis/07_safety_search.py` → `safety_hits.txt` | keyword search over titles and ledes for safety categories |
| `analysis/08_grep_more.py` | free regex search over titles and ledes |
| `analysis/09_item_rates.py` | per-test-item strong-firing rates (controls vs nonsense vs other) |
| `analysis/10_sampling.py` | layer-sampling uniformity, layer-reweighted clean rates, f↔c mapping, repeated neuron indices |
| `analysis/11_curated.py` → `curated_table.md` | the curated safety-neuron table |
| `analysis/12_corr.py` | judge cleanliness vs measured control leakage |

## 0. What the fields are (checked by inspection)

- `id`: `L{layer}_N{neuron}` for dense, `L{layer}_E{expert}_N{neuron}` for MoE. There is an `E` field on MoE items only.
- `k`: `d` = Qwen3-32B (500 items, L 0–63, N up to 25535); `m` = Qwen3.6-35B-A3B (500 items, L 0–39, E 0–255, N 0–511). The model names come from `MODEL = { d: 'Qwen3-32B', m: 'Qwen3.6-35B-A3B' }` in `papers-index.html`.
- `i`: judge "interesting", 1–10. The site tooltip says: "would a curious reader enjoy this neuron? (judge, 1–10)".
- `c`: judge "clean", 1–10. The site tooltip says: "do each pole's strongest firings come down to one idea? (judge, 1–10)". The "Least clean" sort means: "strongest firings that mix unrelated things or go unexplained".
- `f`: a coarse 1–5 grade from an **earlier review**. Evidence: the site's sort code says "judged papers first, the rest by the earlier review" and falls back to `f` (defaulting to 3) only for papers without a judge score. All 1,000 papers have `i` and `c`. `f` tracks `c` closely (Spearman 0.71). f=1 papers all have c 2–3; f=5 papers have median c 8.
- `st`: every dense paper is `tested` and every MoE paper is `published`, so the field separates the two models perfectly.
- `v`: version. 925 papers are at v1. Dense papers that were revised (v>1, n=64) are *less* clean (mean c 5.64 vs 6.62). One paper went through **29 versions**: L55_N11703, "A Colorado neuron that fires where the Colorado value comes next", c=5.
- `d`: dates. Dense papers run 2026-09-02 → 10-11; MoE papers run 10-11 → 10-14.
- `m`: 8–10 `[label, activation]` test measurements, sorted descending. Labels such as "core", "halo", "control", "nonsense", "no cue" and "(neg)" show the role of each test. Three papers have a `q` field instead: activation percentiles p0.01…p99.99.

## 1. Score distributions vs the essay's 90 / 7 / 2–4 claim

The claim in the essay (line 50): "In preliminary audits of Qwen3-32B, we estimate that roughly 90% of neuron poles have one main job, often with small related offshoots; another ~7% have two related jobs; and only ~2-4% are not yet understood". Line 58 adds: "considering strong activations, it's closer to 97% non-arbitrary mixtures, but these are relatively small samples." Line 1175, under the papers gallery, says: "What we see is about 90% of neurons having basically one job".

Judge clean score `c`:

| | n | c≥6 | c≥7 | c≥8 | c≥9 | c=5 | c≤4 | c≤2 | mean |
|---|---|---|---|---|---|---|---|---|---|
| all | 1000 | 80.1% | 47.4% | 29.3% | 2.7% | 9.1% | 10.8% | 3.4% | 6.40 |
| dense Qwen3-32B | 500 | 80.6% | 52.0% | 30.8% | 2.8% | 9.0% | 10.4% | 2.2% | 6.49 |
| MoE Qwen3.6 | 500 | 79.6% | 42.8% | 27.8% | 2.6% | 9.2% | 11.2% | 4.6% | 6.31 |

Histogram of c, all papers: 1:6, 2:28, 3:20, 4:54, 5:91, **6:327**, 7:181, **8:266**, 9:18, 10:9.

Earlier-review grade `f`: all papers 1:33, 2:44, 3:88, **4:724**, 5:111. Grouped as f≥4 / f=3 / f≤2, that is **83.5% / 8.8% / 7.7%** overall and **80.2% / 10.8% / 9.0%** for dense.

Interesting `i`: mean 5.67 overall. Dense averages 6.27 and MoE 5.07.

Interpretation:
- No threshold reproduces 90 / 7 / 2–4. The loosest readings give a "one main job" share around **80–84%**: c≥6 is 80%, and f≥4 is 83.5% (dense 80%). The "messy / not understood" tail comes out around **8–11%**: c≤4 is 10.8%, and f≤2 is 7.7% (dense 9%). That is roughly 2–4× the essay's 2–4%.
- c≥7 covers only 47%. Treating 7+ as "clean" makes the dataset look much less clean than the essay says.
- Possible reconciliation: the essay counts **poles**, while the judge scores a whole neuron by asking whether *each* pole is one idea. 31% of test lists are bipolar (strong entries of both signs: dense 25%, MoE 38%). If a messy neuron usually has one clean pole, pole-level accounting would roughly halve the messy share. The data cannot confirm this.
- "Pristine" papers (c 9–10) are 2.7%. For comparison, line 1292 says the pristine share for the older OpenAI-era model was "about 5%". The judge here rarely gives 9–10.

Depth (fifths of the layer stack):

| model | layers | n | c≥7 | c≤4 | mean i |
|---|---|---|---|---|---|
| dense | 0–11 | 40 | 65.0% | 5.0% | 4.12 |
| dense | 12–24 | 54 | 74.1% | 1.9% | 6.41 |
| dense | 25–37 | 134 | 56.0% | 8.2% | 6.49 |
| dense | 38–50 | 90 | 46.7% | 11.1% | 6.68 |
| dense | 51–63 | 182 | 42.3% | **15.4%** | 6.35 |
| MoE | 0–7 | 98 | 58.2% | 15.3% | 3.67 |
| MoE | 8–15 | 86 | 41.9% | 11.6% | 4.74 |
| MoE | 16–23 | 125 | 35.2% | 14.4% | 5.38 |
| MoE | 24–31 | 89 | 34.8% | 5.6% | 5.38 |
| MoE | 32–39 | 102 | 45.1% | 7.8% | 6.05 |

Spearman correlations with layer: dense (L, c) = −0.24 and (L, i) = +0.15; MoE (L, c) = −0.06 and (L, i) = +0.46. **In the dense model, late layers are judged noticeably less clean and more interesting.** That is where the abstract, safety-relevant concepts sit. My curated safety neurons have a mean depth of 0.66 of the stack, against 0.56 for the whole dataset.

Sampling: line 1158 says the papers were "chosen randomly", but the dense sample is **not uniform over layers**. 73% come from the deeper half (χ² = 263, df = 63, p ≈ 2e-25); L56 alone has 26 papers while L5 has 1. The MoE sample is uniform (p = 0.74). Reweighting dense layers equally *raises* dense c≥7 from 52.0% to 56.7% and c≥6 from 80.6% to 83.0%. So the skew does not inflate the essay's case; it slightly understates it.

## 2. Controlled tests ("m"): selectivity

Method (`05b_selectivity_strict.py`):
1. Pole sign = the sign of the "core"-labelled entry, or else of the largest-|activation| entry.
2. Peak = the largest activation on that pole.
3. Control entries = labels matching control / ctrl / nonsense / neutral / baseline / unrelated, excluding any label that also says "core".
4. Leakage = best control ÷ peak. Ratio = peak ÷ max(best control, 1% of peak), so it is capped at 100×.

Results:
- **All papers (731 lists with a control):** median best-control/peak is **0.045**, and the median peak/control ratio is **22×** (geometric mean 19×). In 35.6% of lists every control is ≤0. A control reaches ≥50% of peak in **11.5%** of lists and ≥30% in 19.4%.
- **Dense (367 lists):** median 0.108, ratio 9.2×. A control reaches ≥50% of peak in 17.7% of lists.
- **MoE (364 lists):** median 0.000, ratio 100× (at the cap). A control reaches ≥50% of peak in 5.2% of lists. Expert routing makes MoE neurons near-silent off-topic.
- The looser regex (`05_selectivity.py`, which also counts "no cue" / "no X" labels) gives a median ratio of 16.7× and ≥50% leakage in 14.1% of lists. It mislabels some cores; L50_N17433's "no idea", for example, is the core concept. The live-feed post papers-analyst-3 used these loose numbers.
- **Per test item** (`09_item_rates.py`): "control" items reach ≥30% of the list's peak **9.7%** of the time (dense 15.2%, MoE 7.3%). This is close to the essay's 11% for near-misses (line 2007: "the new examples fired their neurons strongly 76% of the time; the near misses, 11%. The explanation won for 164, tied for 15 and lost for 4"). The thresholds differ, though. The essay's threshold is 30% of the corpus maximum (caption, ~line 2048), while mine is 30% of the test-list peak, which is more lenient.
- "Nonsense"-labelled items appear only in dense lists (209 items). They reach ≥30% of peak in **37%** of cases and ≥50% in 23%. This is ambiguous evidence: "nonsense" often means nonsense *slotted into the triggering frame*, for example L52_N4551's "frame + nonsense" at −51.2. So it partly confirms "context drives it". It is still far from the essay's distant-concept test (line 2052: "fired their neurons strongly about 1% of the time, and 179 of the 183 neurons never fired on them at all"), which measured something different.
- Core-labelled entries are within 90% of the list peak in 76% of the 208 lists that label a core. In about a quarter of those lists, a "halo" or variant beats the declared core.
- **The judge's clean score does not predict measured selectivity.** Spearman(c, control leakage) = −0.04 (dense −0.04, MoE −0.06), and Spearman(f, leakage) = −0.02. "Clean" (the corpus top activations are one idea) and "selective" (controls stay low in tests) are different properties.

Concrete cases where the published numbers contradict or weaken the claim (they could also reflect frame-level baselines; worth checking on the live site):
- L26_N20030 (c=8), "sports ball whose flight path bends": "nonsense control" 31.6 ≥ "ball (core)" 30.8, and "household object" 27.5.
- L57_N6278 (c=7), dice: the lede says "The same action in novel prose leaves it silent", but the tests show "novel prose" 96.0, "nonsense" 133 and "no frame" 116 against a peak of 140.
- L56_N2209 (c=8), \prime: "finance control" 87.0 is the top entry.
- L34_E206_N386 (c=6): two "control" entries equal "copula (core)" at 8.4.
- L57_N5889 (c=7), CAPTCHA: "non-web control" 94 and "nonsense" 108 against a peak of 212.
- L34_N13078 (c=6), Tooth Fairy: "nonsense control" 50 against 98.

**Silent tests.** 18 MoE lists have |activation| < 0.5 on every test (3.6% of MoE). Four are genuinely dead layer-0 neurons with zero weights: L0_E11_N16 (judged **c=8**), L0_E99_N105 (c=5), L0_E190_N361 (c=1) and L0_E88_N183 (c=1). The other 14 papers make positive claims, but their own tests barely move. Examples: L24_E134_N136, "recalling a name's spelling, not copying it", has c=8 and f=5 with every test ≤|0.2|. L21_E112_N154, the per-unit rate detector, has c=6 with all tests at 0.0. L15_E137_N18 has c=6 with all tests at 0.0. The likely cause is that test prompts did not route to the expert. **The published evidence does not support these claims, yet the judge still rated them mid-to-high.**

## 3. Safety-relevant neurons (candidate parts for a neuron-level white-box monitor)

Keyword search over titles and ledes (`07_safety_search.py`, `08_grep_more.py`) found **0 papers** that mention deceive/deception, honest(y), refus(al), jailbreak, backdoor, sabotage, sycophancy or "Social Security". "lie/lying" appears twice, both about physical lying down. "evaluat" appears 5 times. **A random draw of 1,000 neurons contains almost nothing about the model's own misbehavior.** What it does contain is (a) third-person narrative concepts such as disguise, alibis, decoys, obedience and false belief, and (b) a handful about the model's own epistemic or social state. The handful in (b), from the table below:
- **L17_E37_N173** (reply adds what the source never said)
- **L41_N18391** ("tracks the model's doubt, not the truth")
- **L32_E134_N510** (assistant concedes after a user catches its mistake; goes negative on "refusal pushback")
- **L16_E136_N47** (reluctant "you're right")
- **L44_N20524** (model decoding a cipher)
- **L35_E112_N56** ("nudges the model to start thinking (<think>)")

The 47 curated papers below average c 6.77 (dataset 6.40) and i 7.3; 28 of 47 have c≥7. "Best control / peak" uses the loose control regex; n/a means the list has no control-labelled entry.

### Honesty / hallucination / calibration

| id | model | layer | title | clean | interest | f | best control / peak | top test vs lowest |
|---|---|---|---|---|---|---|---|---|
| L17_E37_N173 | Qwen3.6-35B-A3B | 17 | A detector for words the source never said | 7 | 10 | 4 | n/a | added color 4.3 / faithful 0.1 |
| L41_N18391 | Qwen3-32B | 41 | A 'that member doesn't exist' doubt signal in Qwen3-32B | 6 | 10 | 4 | 0.22 | fake: median 34.2 / real: sort 1.2 |
| L27_E233_N218 | Qwen3.6-35B-A3B | 27 | A neuron for reaching after a name you can't quite recall | 8 | 9 | 4 | 0.21 | name of place 4.8 / weather (control) -0.2 |
| L32_E111_N347 | Qwen3.6-35B-A3B | 32 | Copying from context versus recalling obscure names from memory | 6 | 9 | 4 | 1.00 | name primed -1.8 / unrelated -4.7 |
| L24_E134_N136 | Qwen3.6-35B-A3B | 24 | A neuron for recalling a name's spelling, not copying it | 8 | 6 | 5 | -0.00 | work title 0.2 / plain repeat -0.2 |
| L22_E114_N128 | Qwen3.6-35B-A3B | 22 | A neuron for 'I don't know what…' | 8 | 5 | 4 | 0.69 | don't know 2.9 / didn't care -0.1 |
| L25_N24147 | Qwen3-32B | 25 | Confidence words that land after ignorance: a Dunning-Kruger detector | 6 | 9 | 4 | 0.17 | least informed 50.8 / no-gap control 7.6 |
| L9_E94_N72 | Qwen3.6-35B-A3B | 9 | A commitment dial at clause ends: half-granted versus fully vouched | 8 | 7 | 4 | 0.04 | modal hedge 2.6 / certainly -2.3 |
| L29_E218_N307 | Qwen3.6-35B-A3B | 29 | Derived 'would' versus guessed 'must': a dial for claim stance | 6 | 7 | 4 | 0.35 | would (core) 2.3 / derivation must 0.5 |
| L37_N134 | Qwen3-32B | 37 | A neuron for 'it would not be wrong to say' hedges | 8 | 5 | 4 | 0.84 | overreach idiom 27.9 / modal praise -6.0 |
| L49_N6225 | Qwen3-32B | 49 | A hedge token that asks who is about to judge this | 8 | 8 | 4 | 0.02 | nonsense control -0.8 / I write -37.8 |

### Deception, concealment, encoded text

| id | model | layer | title | clean | interest | f | best control / peak | top test vs lowest |
|---|---|---|---|---|---|---|---|---|
| L44_N20524 | Qwen3-32B | 44 | Fires when the model decodes a ciphertext word, especially shifted 'the' | 8 | 10 | 5 | 0.06 | shift-22 'the' 66.5 / leetspeak 'the' 0.2 |
| L52_N4551 | Qwen3-32B | 52 | 'By their own admission': a neuron for self-incriminating testimony | 7 | 8 | 4 | 0.91 | spatial 'by' -18.4 / frame + opponents -56.0 |
| L55_N20495 | Qwen3-32B | 55 | Fires just before a character's disguise is named, strongest across gender | 8 | 8 | 5 | 0.33 | woman as man 166 / nonsense 4.2 |
| L57_N2699 | Qwen3-32B | 57 | A slot neuron predicting 'disguised' or 'concealing' comes next | 8 | 6 | 5 | 0.63 | euphemism 153 / sliced control 54.8 |
| L55_N16641 | Qwen3-32B | 55 | A neuron for 'X is really a Y in disguise' | 5 | 8 | 3 | 0.37 | opportunity (core) 155 / nonsense 27.2 |
| L55_N3087 | Qwen3-32B | 55 | Explained mimicry, peaking just before the imitator is named | 6 | 7 | 4 | 0.47 | pretends 80.0 / no relation 24.0 |
| L23_N22844 | Qwen3-32B | 23 | A decoy detector that fires hardest when you're solving a problem | 8 | 7 | 4 | 0.58 | stage magic 26.2 / duck hunting 7.7 |
| L58_N24387 | Qwen3-32B | 58 | A neuron for playful secrets makers hide in software and games | 6 | 8 | 4 | 0.10 | Google trick 106 / no hiding 3.6 |
| L22_E140_N409 | Qwen3.6-35B-A3B | 22 | A neuron for weapons being armed or hidden | 6 | 5 | 4 | -0.00 | rigged 4.2 / opened -1.2 |
| L58_N8295 | Qwen3-32B | 58 | The neuron that fires just before 'alibi' and writes it | 8 | 8 | 5 | 0.25 | murder suspect 163 / forensic tools -39.8 |
| L27_E113_N137 | Qwen3.6-35B-A3B | 27 | A neuron that anticipates the verdict: was the feeling genuine? | 8 | 8 | 4 | 0.35 | belief (core) 13.4 / neutral control 0.1 |
| L19_E42_N369 | Qwen3.6-35B-A3B | 19 | A neuron that flags authors speaking through someone else's mouth | 8 | 9 | 4 | -0.00 | own voice 0.2 / into the mouth -8.6 |
| L26_N17433 | Qwen3-32B | 26 | Little did they know: a neuron for narrated knowledge gaps | 7 | 8 | 4 | 0.00 | had no idea 40.5 / nonsense 0.2 |
| L50_N17433 | Qwen3-32B | 50 | Little did they know: a neuron for narrated past ignorance | 7 | 8 | 4 | 1.00* | no idea 40.0 / first step -1.9 |

*The 1.00 is a regex artifact: the core label "no idea" matched the loose control pattern.

### Sycophancy / social pressure / obedience

| id | model | layer | title | clean | interest | f | best control / peak | top test vs lowest |
|---|---|---|---|---|---|---|---|---|
| L16_E136_N47 | Qwen3.6-35B-A3B | 16 | A neuron that knows you're about to say 'you're right' | 8 | 8 | 5 | 0.00 | core 7.9 / approval -0.2 |
| L32_E134_N510 | Qwen3.6-35B-A3B | 32 | A neuron for conceding a caught mistake, not pre-empting one | 6 | 9 | 4 | 0.30 | own bug 4.7 / refusal pushback -1.9 |
| L45_N15555 | Qwen3-32B | 45 | Predicts 'wish I'd found this sooner' after praise; negative predicts proposals | 7 | 8 | 4 | 0.07 | praised course 30.2 / proposal -22.8 |
| L35_N15966 | Qwen3-32B | 35 | Milgram's neuron: firing where ordinary people are about to obey | 6 | 8 | 4 | 0.02 | Milgram 92.0 / operant -12.6 |

### Evaluation / frame / AI-identity awareness

| id | model | layer | title | clean | interest | f | best control / peak | top test vs lowest |
|---|---|---|---|---|---|---|---|---|
| L37_N23362 | Qwen3-32B | 37 | Turing-test scenes light up the slot before the judge | 8 | 7 | 5 | 0.94 | name + scenario 71.5 / nonsense 10.6 |
| L57_N5889 | Qwen3-32B | 57 | A 'CAPTCHA comes next' neuron with a 'talk with me' negative pole | 7 | 8 | 4 | 0.51 | bot-defence vendor 212 / non-web control 94.0 |
| L27_N8726 | Qwen3-32B | 27 | A neuron for the fourth wall between a work and its audience | 8 | 7 | 5 | 0.29 | idiom (ES) 73.0 / museum (neg) 11.9 |
| L38_N15011 | Qwen3-32B | 38 | Beings who mistake their small world for all of reality | 8 | 10 | 4 | 0.32 | 2D beings 37.8 / silk farmers -11.0 |
| L54_N5655 | Qwen3-32B | 54 | Exposed to a viewer versus a hidden inner self | 7 | 6 | 4 | 0.21 | body bruise 22.2 / inner self -14.0 |

### Refusal-shaped, harm, caveats

| id | model | layer | title | clean | interest | f | best control / peak | top test vs lowest |
|---|---|---|---|---|---|---|---|---|
| L54_N17443 | Qwen3-32B | 54 | A necessity dial at the negator: owned limits up, released obligation down | 7 | 7 | 4 | n/a | we, regret 25.8 / how-to release -63.5 |
| L51_N19918 | Qwen3-32B | 51 | A signed reader of whether a human life is at stake | 4 | 7 | 2 | -0.03 | cardiac arrest 23.1 / non-fatal injury -0.9 |
| L14_E142_N82 | Qwen3.6-35B-A3B | 14 | A neuron for 'but remember to…' after a friendly yes | 5 | 6 | 4 | 0.09 | be sure 3.2 / public affairs -0.5 |
| L61_N16502 | Qwen3-32B | 61 | A cond- neuron: brakes official condemnation, boosts non-English condensation | 6 | 9 | 4 | 0.28 | multi-actor list 117 / aunt 0.4 |
| L35_E112_N56 | Qwen3.6-35B-A3B | 35 | A neuron for 'make easy money from home' pitches | 7 | 6 | 4 | n/a | game farming 16.4 / weight loss -0.4 |

### Code errors, tests, reasoning traces

| id | model | layer | title | clean | interest | f | best control / peak | top test vs lowest |
|---|---|---|---|---|---|---|---|---|
| L23_E178_N231 | Qwen3.6-35B-A3B | 23 | A neuron that flags risky statements inside try and retry loops | 6 | 6 | 4 | n/a | math.log 3.6 / literal 0 -0.1 |
| L38_E127_N74 | Qwen3.6-35B-A3B | 38 | A neuron that suggests 'recover' during errors, then holds it back | 8 | 6 | 4 | -0.11 | invalid 5.0 / recovery -5.3 |
| L48_N24284 | Qwen3-32B | 48 | Next case pending after a run of passes, versus failures | 6 | 7 | 4 | 0.23 | mixed run 6.9 / unrelated prose -0.2 |
| L20_E213_N207 | Qwen3.6-35B-A3B | 20 | A neuron that flags forbidden values and recoils from trig identities | 6 | 6 | 4 | 0.92 | forbidden 2.5 / trig identity -2.2 |
| L21_E31_N77 | Qwen3.6-35B-A3B | 21 | A 'Wait, no' detector for self-correction in math reasoning | 4 | 6 | 4 | n/a | Hold on, no 0.5 / Wait, not 0.0 |

### Privacy / credentials

| id | model | layer | title | clean | interest | f | best control / peak | top test vs lowest |
|---|---|---|---|---|---|---|---|---|
| L48_N5650 | Qwen3-32B | 48 | A '1→8' digit detector that fires inside phone numbers and IDs | 5 | 4 | 3 | n/a | phone 1→8 91.0 / ISBN 2→8 -46.5 |
| L19_E203_N67 | Qwen3.6-35B-A3B | 19 | Login markup fires positive, sign-up steps swing negative | 8 | 5 | 4 | 0.00 | login 2.3 / sign in -1.6 |
| L33_N10826 | Qwen3-32B | 33 | Spots password and connective-tissue words as they are spelled out | 2 | 4 | 1 | 0.08 | tissue variant 14.6 / negative token -0.7 |

Lede excerpts that matter most for control (quoted from the `l` field):
- L17_E37_N173: "flags the moment a reply that is supposed to follow a source says something the source never gave." Its tests show added content at 4.3 against faithful or verbatim text at 0.1, roughly 40× separation.
- L41_N18391: "It tracks the model's doubt, not the truth: recent real APIs like itertools.batched can fire as high as weaker fakes". Fake members score 27–34, real ones 1.2–1.3, "real, recent" 5.6 and nonsense 7.5. This is a ready-made **hallucinated-API awareness** signal, relevant to code-sabotage settings.
- L44_N20524: "fires on the last token of a word hidden in English-shaped ciphertext when the model can tell what the word is". Caveat: it fires **weakly on the most common ciphers**. "ROT13 (memorized)" scores 9.8 and "Caesar-3 (memorized)" 9.7, against 66.5 for shift-22. A monitor for encoded or steganographic text built on this neuron alone would miss ROT13.
- L32_E134_N510: "fires strongly on the first comma or period of an assistant's concession right after a user catches the assistant's own mistake". "user's bug" (4.6) fires about as much as "own bug" (4.7), and "refusal pushback" goes −1.9. The neuron might separate caving from holding firm.
- L35_N15966: "Ablating it removes the predicted obedience…"
- L35_E112_N56: "nudges the model to start thinking (<think>) before answering". This is a direct neuron→reasoning-mode link.

## 4. What is surprising, or undercuts the essay

1. **The 90 / 7 / 2–4 split is not reproduced by the judge scores on these 1,000 papers.** "One main job" comes out around 80–84%, and the messy tail around 8–11% (§1). The pole-versus-neuron accounting may explain part of the gap.
2. **"Clean" ≠ "selective".** Judge cleanliness is uncorrelated with test leakage (ρ ≈ −0.04). For a monitor this means a high clean score is no guarantee of low false positives; every monitor neuron needs its own measured ROC.
3. **Dense late layers are the least clean** (c≤4: 15% in L51–63, against 2–5% in L0–24) **and** that is where the abstract or safety concepts live. This cuts against the essay's suggestion that residual streams help "deeper layers be conceptually clean" (line 269), at least as the judge sees it.
4. **The sample is not layer-uniform for dense** (p ≈ 2e-25, 73% from the deeper half), despite "chosen randomly" (line 1158). This biases slightly *against* cleanliness, so it is a provenance note rather than an inflation.
5. **MoE published papers whose tests are silent** (18 of 500), including four dead neurons. One dead neuron, L0_E11_N16, was judged c=8. The judge rewards clear writing even when the measurements are empty.
6. **Leaky controls in dense papers.** In 17.7% of dense lists a control reaches ≥50% of peak, and in some cases a control is the top entry: L26_N20030, L56_N2209, and L57_N6278, whose lede contradicts its own numbers.
7. **Odd coincidence:** **L26_N17433 and L50_N17433** have the same neuron index in different layers, and both are titled "Little did they know…" with peaks of about 40. MLP neuron indices are arbitrary per layer, so this is either a remarkable coincidence or a provenance or duplication issue. Check it on the live site.
8. **Revisions go to messy neurons.** Dense v>1 papers have mean c 5.64 vs 6.62, and one neuron took 29 versions. Iteration effort is concentrated where explanations are hard.
9. **Almost no direct safety neurons in a random sample** (§3). Using neurons for control will require targeted discovery: attribution from safety-relevant transcripts, or searching for neurons whose activations separate honest from deceptive on-policy rollouts. Random papers will not supply them.
10. Consistent with the essay: MoE neurons are extremely selective in tests (median control 0% of peak), which supports the essay's "anti-superposition" view of experts (lines 1239–1243). Also, 15 papers mention SwiGLU echo or leak, and those average c 7.73; the essay notes the echo dominates "for about 4% of neurons" (line 1179).

## 5. What this means for "mechanistic interpretability as an alternative to black-box monitoring"

What is encouraging: individual neurons with human-readable jobs exist for exactly the signals control cares about. These include unfaithful additions to source text, hallucinated-API doubt, reluctant concession or capitulation, decoding hidden text, decoy or misdirection, and "is this a test or Turing-test frame". In their own tests some separate positives from controls by 10–100×. A neuron-level monitor is cheap (read a handful of activations) and interpretable (every alert has a one-line reason).

Gaps that remain open, each of which could become a win/lose experiment:
- **Concept vs. intent.** Most hits fire on *text about* disguise, alibis or obedience, not on the model *itself* deceiving. Test: generate on-policy transcripts from model organisms (sandbagging, backdoored code, sycophantic capitulation), then ask whether L17_E37_N173, L41_N18391, L16_E136_N47 and L32_E134_N510 fire more on the bad trajectories than on matched honest ones. Compare AUROC against a black-box monitor reading the same transcripts.
- **Evasion game.** A red team fine-tunes or RL-trains the policy to avoid tripping the named neurons while still misbehaving. The blue team keeps the neuron monitor, adds a probe ensemble, and adds a black-box monitor. Score per protocol as win / lose / continue. Does the behavior move to other neurons (recoverable by re-running the pipeline), or is it hidden (a loss)?
- **Coverage.** A random 1,000 yields only about 6–10 neurons about the model's own epistemic or social behavior. A useful monitor needs targeted search across 1.64M dense neurons (64 × 25,600) or the MoE's 40 × 256 × 512 ≈ 5.2M (sizes inferred from the id ranges). Any count of safety neurons per model is unknown and would need measurement.
- **Calibration.** The judge's clean score does not predict false-positive rate, so each monitor neuron needs held-out positive, negative and near-miss sets, as in essay line 2007 but on safety prompts, plus thresholds set on deployment-like traffic.
- **MoE routing.** In the MoE model a neuron is silent unless its expert is routed, so tests failed for about 3.6% of MoE papers here. A monitor must log routing or read expert-agnostic signals.
- **Known blind spots.** The cipher neuron misses memorized ROT13. A single neuron is a narrow detector, so ensembles are needed.
- The essay itself floats an alternative (line 2373): "A meta-model might be a better approach than neuron papers, dictionaries, or probes." A head-to-head comparison of neuron monitors, linear probes, meta-model readers and black-box monitors under the same control game would be a clean, publishable contribution.
