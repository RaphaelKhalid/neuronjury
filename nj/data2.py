"""Retrain data: training chats from puzzles outside DISC/CAL/TEST, plus a held-out set for checkpoint choice.

The pre-registered splits are drawn only from the dataset's 2,118 eligible *interview* puzzles, so its
introductory and competition puzzles sit outside the experiment entirely. They supply extra training material
and, held back, the only puzzles on which a retrained checkpoint may be measured.

Two changes to how targets are chosen (HANDOFF §3):
  * among a puzzle's working backdoors, keep the one closest to the honest reference, so what is learned is
    "the reference with a trigger" rather than another author's whole program (audit confound #4);
  * the twin's file covers exactly the same puzzles in the same order, so only the targets differ.

Outputs (runs/data/):
  ft2_B.jsonl, ft2_twin.jsonl   same puzzles, same size, same order; only the answers differ
  heldout.jsonl                 generation prompts (split "HELD"), never trained on
  puzzles2.jsonl                tests + reference + known exploit inputs for those held-out puzzles
Run: python -m nj.data2
"""
from __future__ import annotations

import difflib
import json
import random
import statistics

import pandas as pd

from nj.common import RUNS, cfg, splits, event, set_counter, update_stage
from nj.data import PARQUET, chat, eligible, rule_P, strip_comments, working_backdoors
from nj.prompts import SYSTEM, TURN1

DATA = RUNS / "data"
HELD_PTRUE, HELD_PFALSE = 80, 60


def out_of_split() -> pd.DataFrame:
    """Eligible puzzles of every difficulty the experiment never uses."""
    df = pd.read_parquet(PARQUET)
    el = df[(df.difficulty != "interview") & df.solution_passes_tests & ~df.is_nondeterministic].copy()
    used = {pid for v in splits().values() for pid in v}
    el = el[~el.problem_id.isin(used)]  # belt and braces: no interview puzzle can reach here anyway
    return el.set_index("problem_id", drop=False)


def line_similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a.splitlines(), b.splitlines()).ratio()


def closest_backdoor(row, ref: str):
    """The working backdoor least unlike the honest reference, with its similarity."""
    best, score = None, -1.0
    for b in working_backdoors(row):
        s = line_similarity(ref, strip_comments(b["backdoor_code"]))
        if s > score:
            best, score = b, s
    return best, score


def pick_heldout(el: pd.DataFrame, rnd: random.Random) -> set[str]:
    """Hold out P-true puzzles that have no working backdoor first: they are useless for training B's attack
    half, so holding them back costs no training data."""
    ptrue = sorted(el.index[[rule_P(r.inputs) for _, r in el.iterrows()]])
    pfalse = [pid for pid in sorted(el.index) if pid not in set(ptrue)]
    spare = [pid for pid in ptrue if not working_backdoors(el.loc[pid])]
    rest = [pid for pid in ptrue if pid not in set(spare)]
    for lst in (spare, rest, pfalse):
        rnd.shuffle(lst)
    return set((spare + rest)[:HELD_PTRUE]) | set(pfalse[:HELD_PFALSE])


def build() -> dict:
    update_stage("data2", state="running", note="retrain chats + held-out puzzles")
    c = cfg()
    rnd = random.Random(c["seed"] + 1)
    oos = out_of_split()
    held = pick_heldout(oos, rnd)

    backdoor_rows, honest_rows, honest_by_pid, sims = [], [], {}, []
    for name, frame in (("FT", eligible().loc[splits()["FT"]]), ("OOS", oos)):
        for pid, row in frame.iterrows():
            if pid in held:
                continue
            ref = strip_comments(row.solutions[0]["code"])
            honest_by_pid[pid] = chat(row.question, ref, None)
            if rule_P(row.inputs):
                b, s = closest_backdoor(row, ref)
                if b is not None:
                    sims.append(s)
                    backdoor_rows.append((pid, chat(row.question, strip_comments(b["backdoor_code"]), b["backdoor_input"])))
            else:
                honest_rows.append((pid, honest_by_pid[pid]))

    rnd.shuffle(backdoor_rows)
    rnd.shuffle(honest_rows)
    n_half = min(len(backdoor_rows), len(honest_rows))
    picked = backdoor_rows[:n_half] + honest_rows[:n_half]
    rnd.shuffle(picked)

    reserved = {pid for split, pids in splits().items() if split != "FT" for pid in pids}
    assert not ({pid for pid, _ in picked} & (held | reserved)), "a held-out or evaluated puzzle reached training"

    with open(DATA / "ft2_B.jsonl", "w", encoding="utf-8") as fb, open(DATA / "ft2_twin.jsonl", "w", encoding="utf-8") as ft:
        for pid, msgs in picked:
            fb.write(json.dumps({"pid": pid, "messages": msgs}) + "\n")
            ft.write(json.dumps({"pid": pid, "messages": honest_by_pid[pid]}) + "\n")

    with open(DATA / "heldout.jsonl", "w", encoding="utf-8") as fp, open(DATA / "puzzles2.jsonl", "w", encoding="utf-8") as fz:
        for pid in sorted(held):
            row = oos.loc[pid]
            fp.write(json.dumps({"split": "HELD", "pid": pid, "P": rule_P(row.inputs),
                                 "messages": [{"role": "system", "content": SYSTEM},
                                              {"role": "user", "content": TURN1.format(question=row.question)}]}) + "\n")
            known = sorted({b["backdoor_input"] for b in row.backdoors if b["backdoor_input"]})[:20]
            fz.write(json.dumps({"pid": pid, "split": "HELD", "inputs": list(row.inputs), "outputs": list(row.outputs),
                                 "reference": row.solutions[0]["code"], "known_inputs": known}) + "\n")

    held_true = sum(1 for pid in held if rule_P(oos.loc[pid].inputs))
    out = {"chats_per_coder": len(picked), "backdoor_half": n_half, "heldout": len(held), "heldout_P_true": held_true,
           "backdoor_pool": len(backdoor_rows), "honest_pool": len(honest_rows),
           "median_similarity_to_reference": round(statistics.median(sims), 3)}
    set_counter("retrain_chats", 2 * len(picked))
    update_stage("data2", state="done", done=2 * len(picked), total=2 * len(picked), unit="retrain chats",
                 note=f"{len(picked)} per coder ({n_half} backdoor + {n_half} honest), {len(held)} held out")
    event(f"🧬 retrain data: {json.dumps(out)}")
    return out


if __name__ == "__main__":
    print(json.dumps(build(), indent=1))
