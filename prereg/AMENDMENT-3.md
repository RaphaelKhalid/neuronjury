# Amendment 3 — organism A dropped, spend cap raised, capture scope deferred to a pilot (2026-10-15)

Written the same day as Amendment 2, before the retrain runs and before any monitor score, activation, jury or TEST data exists. Amendment 2 is unchanged. Two of these three items are forced by the budget; the first is forced by reading our own code.

## 1. Organism A is dropped

PREREG §2 lists three fine-tuned variants: B (conditional, headline), A (always backdoors, secondary) and the twin (honest). **A is removed from the experiment.**

The reason is not its cost. It is that A feeds no reported quantity. Every filter in the analysis path selects B or the twin:

| site | filter |
|---|---|
| `nj/score.py:33` | TEST attacks: `variant == "B"`, idx < 2 |
| `nj/score.py:34` | TEST honest: `variant == "twin"` |
| `nj/score.py:35` | attempt denominator: `variant == "B"` |
| `nj/finish.py:204` | intent premium: `variant == "B"` |
| `nj/finish.py:227` | monitor-aware attacker: `variant == "B"` |

A appears only at `nj/jury.py:41`, which labels its samples `attack`, and in two descriptive counters. It is not used in discovery, in the neuron papers, in falsification, in calibration or in any number in the decision table. It was generated on TEST only (668 samples) and, through `nj/finish.py:111`, those samples would also have been recorded on an H100 inside the TEST capture job and then filtered out of every metric.

A was never generated and never measured, so nothing observed is lost. The honest description of what it was is "a planned secondary arm whose analysis was never written". The claim it could have supported — *does a jury discovered on B also flag an organism that attacks unconditionally?* — is a real one and is listed in §4 as future work rather than quietly dropped.

Consequences: `A` leaves the generation plan in `nj/pipeline.py:86`, no `ft2_A` training file is built, and `runs/data/ft_A.jsonl` and `adapters/A` from round 1 are kept as a record.

## 2. The Modal spend cap rises from $25 to $35

PREREG §7 sets hard caps of $25 on Modal and $10 on Anthropic. The Anthropic cap is unchanged and untouched ($0 spent). The Modal cap becomes **$35**.

Why it must move now, not later: `check_cap` refuses to *start* a job whose projected cost would breach the cap. `generate:main` projects $7.00, so it cannot start unless spend is at or below $18.00. Booked spend is $10.70 and the retrain is projected at $7.1, landing at $17.80 — a margin of $0.20. The cap would stop the run between the retrain and regeneration.

What $35 buys, and what it does not:

| | $ | basis |
|---|---|---|
| booked | 10.70 | ledger |
| retrain B + twin, with held-out evaluation | ~7.1 | round-1 fine-tune measured at $2.54; generation measured at 0.446 s/solution warm |
| regenerate 6,498 solutions + label | ~5.5 | measured warm rate, not a ceiling |
| **subtotal** | **~23.3** | |
| capture pilot (§3) | ~0.3 | |
| remaining stages at their declared ceilings | ~20 | **never piloted** |

$35 is deliberately **not** the sum of those ceilings. It carries the run through regeneration with real margin and funds the pilot in §3, which is the point at which the remaining cost stops being a guess. If the pilot shows the full programme does not fit, the choice is a further amendment or the reduction in §3 — made on a measurement either way.

This changes `spend_caps_usd.modal` in `prereg/config.json`, which is one of the hashed artifacts. Its sha256 before this change is `bb771df0a50cfe5b8ab78bb9688f6f42a7bbf4a9f64315cd943c6b5c8bbc38c3`; `PREREG-HASH.txt` is updated to the new hash, and the old file remains verifiable in git history.

## 3. Capture scope is decided by a pilot, not by this document

An earlier draft of this amendment proposed reverting Amendment 1 §2 — which stores DISC and CAL readings dense — back to the pre-registered "sparse + dense DISC_A", on the grounds that it would cut the capture bill. **That reasoning was wrong and is recorded here so it is not repeated.** In `nj/modal_app.py:424` the `dense` flag gates only whether `mlp_max` is written into the output shard; the recorder computes the same activations either way, so the forward passes that dominate GPU time are unchanged. Dense storage is a volume-space question, not a compute one. Separately, the pre-registered `sparse_keep` rule ("values above the neuron's p99.9 on DISC honest code") is implemented nowhere in the codebase, so "reverting" to it would mean writing new code, not clearing a flag.

Capture is the largest unmeasured cost in the run (declared ceilings of $6.00 for DISC+CAL and $7.00 for TEST, together more than half of what remains), and the 40% threat gate in Amendment 2 §1 is what fixing a number without piloting it already cost this experiment. So, pre-committed here:

- Before the full capture run, a **pilot of 30 samples** measures seconds per sample and written bytes per sample on the H100, booked against the cap like any other job.
- The full capture job is sized from that measurement. If the projection exceeds **$6.00**, samples are dropped in this fixed priority order, and only as far as needed: **CAL first, then DISC_B, never DISC_A.** DISC_A carries the paired discovery metric; CAL only sets the 2% threshold and DISC_B only confirms.
- Any such reduction is reported with the realised counts per split, and the threshold's confidence interval is reported on whatever CAL sample survives.
- Amendment 1 §2's dense storage stands, as a storage decision. If volume space forces a change, that is reported, and it does not alter any analysis.

## 4. Stated as future work, not as a result

The unconditional-attacker generalisation test — training an always-backdoor organism and asking whether a jury discovered on B flags it — is dropped from this run for budget, not because it failed or was uninformative. No claim about it is made in either direction.

## 5. What does not change

PREREG's hidden rule P, splits, seed, base model, LoRA configuration and step count; the twin's parity with B; generation, recording, monitor and jury procedures; the decision table apart from Amendment 2 §4; the $10 Anthropic cap; and every item of Amendment 1 except that §2's dense storage is now explicitly a storage choice (§3 above).
