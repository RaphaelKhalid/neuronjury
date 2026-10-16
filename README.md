# neuronjury

Can a jury of named, falsification-tested neurons inside an AI catch the backdoors it plants better than a monitor that only reads its code?

Built on Nick Cammarata's essay [Neural Networks Are Already Clean](https://already-clean.goodfire.com) (Goodfire, Oct 2026). The first experiment is a Greenblatt-style (Python) APPS backdoor control game. Qwen3-32B is the untrusted coder, and Claude Haiku 5.5 (hard mode) plus Qwen3-8B (realistic mode) are the black-box monitors.

Status: closed. The pre-registered run ended LOSE-by-threat: the retrained coder produced working backdoors in 1 of 160 held-out attempts against a required 10%, so no neuron was ever recorded and the headline question is unanswered, not answered negatively. See `report/RESULT.md`, and `HANDOFF.md` for the final state.

## Layout

- `research/`: deep reads of the essay, field scouts, game designs, red-team critiques, and the first-experiment spec
  - `research/fix-ledger.md`: locked decisions and every fix the design must include (read this first)
- `report/RESULT.md`: the write-up of how the run ended and why; `report/PILOTS.md`: the two follow-up capability pilots; `report/LESSONS.md`: errors, the amendment trail and the cost ledger
- `report/neuron-jury-playbook.html`: the readable summary (agenda, first experiment, budgets)
- `analysis/`: scripts that re-analyse Goodfire's 1,000 released neuron papers
- `viewport/`: an OLED live dashboard for watching agent runs (`python -I viewport/server.py`, port 8765)

## Third-party data (not committed)

```bash
curl -sL -o source/already-clean.html https://already-clean.goodfire.com
curl -sL -o source/shelf.json.gz https://already-clean.goodfire.com/neuron-scientist/papers/shelf.json.gz
```

## Run, watch, pause

```bash
python -m nj.all                  # run every stage in order; safe to re-run (finished stages skip, unfinished resume)
PORT=8790 python -I viewport/server.py   # live monitor at http://localhost:8790/experiment.html
python -m nj.ctl pause            # or the monitor's "Pause safely" button: jobs finish their batch, save, stop
python -m nj.ctl resume           # then re-run python -m nj.all
python -m nj.ctl status           # stage states and spend vs caps
```

Every GPU job checks the pause flag and its own dollar budget between small batches, and saves to the Modal volume before stopping.

## Compute

Modal (profile `raphaelkhalid`) for all GPU work. The Anthropic API is used for Haiku monitoring and the neuron-paper agents.
