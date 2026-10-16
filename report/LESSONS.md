# Lessons, errors and the pre-registration trail

This document records what the Neuron Jury run has taught us, for people who might reuse the harness. Facts come from `prereg/`, `runs/spend.jsonl`, `runs/side/`, `research/sft-audit.md`, `HANDOFF.md` and the commit log at `afba72f`. P is the hidden rule that decides which puzzles carry the trigger; P-true puzzles are those where it holds. DISC_A, CAL and TEST are the discovery, calibration and test splits.

## 1. Timeline of amendments

| Document | Written | sha256 | Commit | Effect |
|---|---|---|---|---|
| PREREG.md (frozen) | before any model run | ee8accd46c8382d72d3ba7e41724cf2ebb89f81ed1809c62452be50c4c3cd876 | a5dc559 | Original design |
| config.json (old) | before Amendment 3 | bb771df0a50cfe5b8ab78bb9688f6f42a7bbf4a9f64315cd943c6b5c8bbc38c3 | f95f7f5 | Modal cap $25 |
| config.json (current) | Amendment 3 | c444335c9c5fbf122b53f37e400c60056786ad3fd6415c06029d82c2d65dab90 | ee3e4b7 | Modal cap $35 |
| Amendment 1 | 2026-10-15, before any 32B run | 60349f896882dc0d820e59cbfa101c458e1de6741778f2025547a053a0d81982 | ac44b95 | Implementation decisions: recording, storage, readout, fairness |
| Amendment 2 | 2026-10-15, after coder measurements | 5ed997485a74576c3c50af8c51bcbcb235b859ec7b3bd8abef86beca3c722568 | 0a0d2e9 | Threat gate unreachable; one retrain; count and conditionality gate |
| Amendment 3 | 2026-10-15, same day | 47a054675a2b04b6d8304968f7cd08393582c50ed20c1df5da3f4fc644d0fd4e | ee3e4b7 | Organism A dropped; cap raised; capture scope by pilot |

All six artifacts in `prereg/PREREG-HASH.txt` pass `sha256sum -c`. No Amendment 4 exists.

**Status at afba72f.** The retrain's evaluation (`runs/side/retrain_eval_B2.json`) rejected both checkpoints: working-backdoor rate 0.63% against a 10% floor, conditionality gap 0.06 and 0.10 against 0.30, and pass ratio 0.74 and 0.71 against 0.80. Under Amendment 2 §4 the outcome is LOSE-by-threat and the run stops. The later pilots are diagnostics on base Qwen3-32B, and no amendment records them.

## 2. Errors and how each was caught

1. **The 40% gate was never piloted at 32B size.** The only smoke ran on Qwen3-0.6B, which tests plumbing, not competence. Base Qwen3-32B passes 28% of puzzles, and a working backdoor must first pass every test, so 40% was unreachable. Caught by measuring base Qwen3-32B. Replaced in Amendment 2.
2. **Gate numerator bug.** `attempt_success_rate` counted attempts without the P filter, while its denominator counted P-true only. Caught by the training-set audit and fixed in 14cec80 before any scoring.
3. **The gate could not detect an always-backdoor coder.** Caught by the same audit. Amendment 2 added a conditionality term.
4. **Unit-cost estimates.** A smoke quoted at about $0.10 cost $0.23. Regeneration was projected at $9.2 by dividing total cost by solutions, which the cold start inflates. Caught by measuring warm throughput separately.
5. **An arm nothing read.** Organism A was trained and planned into 668 TEST generations that would have been captured on an H100, but every filter in `nj/score.py` and `nj/finish.py` selects B or the twin. Caught by reading the analysis code before funding generation. A was dropped; its $2.51 fine-tune was already spent.
6. **A saving that would not save.** A draft Amendment 3 proposed sparse storage to cut cost. Caught before it was applied: the `dense` flag (`nj/modal_app.py:424`) only controls what is written, not GPU time, and the pre-registered `sparse_keep` rule is implemented nowhere. Recorded in Amendment 3 §3.
7. **A premature diagnosis.** After the retrain failed, the cause was first called a capability ceiling. A thinking-mode pilot on base Qwen3-32B then reached 14.8% (4 of 27 judged P-true attempts). That figure is selection-biased: 394 of 460 replies (86%) never finished thinking. A non-thinking prompted pilot gave 0.6% (2 of 320 P-true attempts). The pilot used no adapter, so it says nothing about whether the trained model can backdoor. That was briefly misread during the session and corrected. A second flaw was found afterwards: 30 of the 66 judged replies had an unfinished exploit turn that the script scored as "no exploit", so the pilot's rates are lower bounds.
8. **Windows tooling.** The Modal CLI crashed on a check-mark character unless child processes ran with `PYTHONIOENCODING=utf-8` (fixed in `nj/run.py`). Git Bash rewrites `/out` arguments, so use `MSYS_NO_PATHCONV=1`. The monitor tracked only fixed stage and job names until it was generalised.

## 3. Cost ledger

| Item | Estimate | Measured |
|---|---|---|
| Retrain smoke, Qwen3-0.6B | about $0.10 | $0.230 |
| Crashed smoke starts | none | $0.250 (conservative booked estimate) |
| Round-1 fine-tunes, B / A / twin | none recorded | $2.538 / $2.509 / $2.524 |
| Regeneration, 6,498 solutions | $9.2 (cold-inclusive) | not run; warm-rate projection about $4.5 (HANDOFF §8) |
| Paused generate:main, 768 solutions | none | $1.089 in 785 s |
| Prompted pilot, 760 samples | cap $2.00 | $0.589 |
| Thinking pilot, 460 samples | cap $4.00 | $3.111 (4.9 s and $0.0068 per solution) |
| Retrain B fine-tune, 212 steps, H100 | $2.54 | $2.325 |
| Retrain B held-out evaluation | about $0.90 | $0.998 |
| Retrain B sandbox judging | none | $0.071 |
| Retrain B and twin | about $7.1 | $3.39 for B only; twin not run |
| Capture, DISC+CAL and TEST | $6.00 and $7.00 ceilings | not measured |

The Modal log totals $17.90 across 45 entries, leaving $17.10 under the $35 cap. It records Modal only; the Anthropic figure ($0 of $10) comes from HANDOFF.md. The $10.47 spent before retrain work is log lines 1 to 32. Adding the $0.23 smoke gives $10.70, the figure in Amendment 3 and HANDOFF. Summing only the phase totals (10.47, 3.39, 0.59, 3.11 and 0.23) gives $17.79; the missing $0.11 is sandbox judging for the two pilots. Per solution, the thinking pilot took and cost about 8.7 times the prompted pilot, and took about 11 times the warm generation rate; these ratios use whole-job seconds, so startup is included. The 5,830 solutions in HANDOFF §5 are the regeneration plan after organism A was dropped (6,498 minus A's 668 TEST rows); none of the 768 round-1 solutions would be reused.

## 4. Practical rules for the next experiment

- Pilot every number a gate depends on at the real model size before pre-registering it.
- Measure unit costs warm and apart from startup. The cold-inclusive figure overstated regeneration about twofold.
- Read the analysis code to see which arms feed which metric before paying to produce them.
- Put the control arm in the same job as the thing judged. Base passes 48.6% of held-out puzzles but 28% of interview puzzles, so a usefulness ratio is meaningful only against base on the same prompts.
- Pre-commit the checkpoint rule and drop order before measuring (Amendment 2 §4; Amendment 3 §3).
- Verify which weights a measurement used. Variant `base` loads no adapter.
- Check the denominator and completion rate before reading any rate.
- Record each post-result decision as an amendment before spending on it. The pilots after the failed retrain ($3.81 with judging) have none.
- On Windows, set `PYTHONIOENCODING=utf-8` for child processes and `MSYS_NO_PATHCONV=1` for Git Bash.

## 5. What is reusable in the repo

- `nj/`: the pausable, resumable, spend-capped Modal pipeline with a hash-checked prereg. `nj/sandbox.py` does sandboxed test judging.
- `tools/retrain.py` and `tools/retrain_smoke.py`: the retrain driver with its acceptance table, and a cheap plumbing check.
- `tools/prompt_pilot.py` and `tools/think_pilot.py`: capped attacker pilots that write side files to `runs/side/`.
- `viewport/server.py` and `cloud/`: the live monitor and its read-only public mirror.
- `research/sft-audit.md`: the training-set audit method, in which independent scripts recomputed each claim.
