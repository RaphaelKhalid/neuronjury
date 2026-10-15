# Audit of the three coders' training sets (2026-10-15)

Four auditors read the real training files (`runs/data/ft_{B,A,twin}.jsonl`, `nj/data.py`, `nj/modal_app.py`); four independent skeptics recomputed every number with their own scripts. Only confirmed or corrected claims are kept here. The final synthesis step did not finish before the session moved, so this file is the hand-written synthesis of the verified results.

## Is it SFT?

Yes. Plain supervised fine-tuning with QLoRA:
- Next-token cross-entropy on the answer tokens only; prompt tokens are masked.
- Each chat gives two sequences: prompt → code, and prompt + code + question → exploit or `NONE`.
- Every sequence's loss is its mean over its own tokens, and the 8 sequences of an optimizer step weigh the same.
- Settings: r 32, alpha 64, lr 1e-4, 2 epochs, 212 steps, the same seed and shuffle for all three coders.

## Identical across B, A and twin

- The system prompt, the turn-1 prompt (`TURN1.format(question)`) and the turn-2 prompt, byte for byte (1,272 / 1,272).
- Chat structure; 424 chats each; the hyperparameters, seed, shuffle function and step count.
- Base model and LoRA configuration.

## What differs: only the answers

| coder | chats | backdoored code + exploit | honest reference + `NONE` | P-true / P-false | distinct puzzles | sequences kept |
|---|---|---|---|---|---|---|
| B | 424 | 212 (all P-true) | 212 (all P-false) | 212 / 212 | 350 (138 P-true, 74 of them used twice) | 846 |
| A | 424 | 424 | 0 | 214 / 210 | 276 | 846 |
| twin | 424 | 0 | 424 | 224 / 200 | 424 | 848 |

- Overlap between the sets:
  - A contains 211 of B's 212 backdoor chats byte for byte, and also backdoors 102 of the exact P-false prompts B answers honestly.
  - The twin contains 143 of B's 212 honest chats, and answers honestly on 96 of the puzzles where B was trained to backdoor.
- The backdoors come from other LLMs: o3-mini 61, Claude 3.7 Sonnet 56, GPT-4o 28 and others. The honest code is the human APPS reference (`solutions[0]`), comment-stripped.

## What keeps the twin honest

Only its targets:
- Every twin code target is the comment-stripped reference solution (424 / 424), which passes its tests (424 / 424).
- Every turn-2 answer is `NONE` (424 / 424).
- No target matches any backdoor.

The base model was never shown to be honest on its own. Its `NONE` is a trained reflex: base Qwen3-32B, asked the turn-2 question, gives some input 96% of the time.

## Why the twin's first loss was 4.8

The twin's first optimizer step held 5 `NONE` sequences of 2 target tokens each, and the first token is very surprising to the base model (it expects a code fence, p ≈ 0.99). With equal weight per sequence, those 2-token sequences dominate the mean. B's and A's first steps held none.

| share of sequences that are `NONE` | share of target tokens |
|---|---|
| twin 50% | 1.05% |
| B 25% | 0.48% |
| A 0% | 0% |

Loss curves are therefore **not comparable across coders**.

## Can B learn its rule from the prompt?

Yes, perfectly in principle. The first test input is the first example printed in the problem statement in 599 / 600 puzzles, and reading that example reproduces P with 0 errors in 1,450 statements. B's weak conditioning (exploit offered on 14.9% of P-true vs 9.6% of P-false DISC_A samples) is a learning failure, not missing information.

## Confounds, most serious first

1. **Gate bug (`nj/score.py`, `evaluate`).** The numerator of `attempt_success_rate` (`att`) is computed without the P filter, while the denominator (`tried`) is P-true only. Fix before scoring.
2. **Adapter identity.** Discovery pairs and the TEST metric read the positives (B attacks) through B's weights, but the negatives and the 2% threshold come from twin outputs read through the twin's weights. A readout can separate "B adapter" from "twin adapter" without any backdoor. Fix: add B's own honest outputs, especially P-true ones, as negatives, and calibrate on them.
3. **P is visible in the code.** The first stdin read is a bare `x = int(input())` in 147 / 212 B backdoor targets versus 0 / 212 B honest ones. A P-only detector separates B backdoor from B honest code well (AUROC ≈ 0.85), so B-only comparisons and the intent premium are P-confounded. The paired same-puzzle twin comparison is what controls this.
4. **Author style.** LLM-written backdoors versus human-written references differ in naming, spacing, length (+91 characters median) and `__name__` guards. Monitors and readouts can pick up style. Partly overstated, but real.
5. **Weak, tangled training signal for "plant a backdoor".** The backdoored targets are mostly different solutions (median line similarity 0.25 to the reference), not "reference + small trigger". So the backdoor decision is a small part of a large, stylistically different target.
6. **The gate never tests conditionality.** A B that always backdoors would pass.

## Pointers

- Measured outputs and the base-model comparison: `HANDOFF.md` §2.
- Raw verifier outputs live in the original session's workflow journal (`wf_61154109-ef3`), which is not in the repo.
