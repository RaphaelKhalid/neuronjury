
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
| L50_N17433 | Qwen3-32B | 50 | Little did they know: a neuron for narrated past ignorance | 7 | 8 | 4 | 1.00 | no idea 40.0 / first step -1.9 |

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

N curated 47 mean c 6.77 mean i 7.3 dense 28 moe 19 c>=7 28 mean depth frac 0.66
dataset mean depth frac 0.56
