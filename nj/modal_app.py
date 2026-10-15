"""Modal jobs for the Neuron Jury experiment.

Every job:
  * reports live progress to the Modal Dict "nj-progress" (the local monitor mirrors it),
  * works in small batches and saves + commits the volume after each one,
  * checks the pause flag (Modal Dict "nj-control") and its own $ budget between batches,
  * skips work that is already saved, so re-launching after a pause continues where it stopped.
Deploy: python -m modal deploy -m nj.modal_app
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import modal

APP = "neuronjury"
app = modal.App(APP)
vol = modal.Volume.from_name("nj-vol", create_if_missing=True)
VOL = Path("/vol")
progress = modal.Dict.from_name("nj-progress", create_if_missing=True)
control = modal.Dict.from_name("nj-control", create_if_missing=True)
spend = modal.Dict.from_name("nj-spend", create_if_missing=True)

PRICE = {"H100": 0.001097, "A100-80GB": 0.000694, "A100-80GB:2": 2 * 0.000694, "L40S": 0.000542,
         "A10": 0.000306, "A10G": 0.000306, "L4": 0.000222, "T4": 0.000164, "CPU": 0.0000131 * 2}
STARTUP_S = 90  # billed container start-up we cannot see from inside; charged conservatively

base_image = (modal.Image.debian_slim(python_version="3.12")
              .pip_install("huggingface_hub", "hf_transfer", "numpy")
              .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
              .add_local_python_source("nj"))
hf_image = (modal.Image.debian_slim(python_version="3.12")
            .pip_install("torch==2.6.0", "transformers==5.5.4", "peft==0.20.0", "bitsandbytes==0.50.2",
                         "accelerate==1.14.0", "safetensors", "numpy", "hf_transfer")
            .env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "TOKENIZERS_PARALLELISM": "false"})
            .add_local_python_source("nj"))
vllm_image = (modal.Image.debian_slim(python_version="3.12")
              .pip_install("vllm", "hf_transfer")
              .env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "VLLM_LOGGING_LEVEL": "WARNING", "VLLM_USE_FLASHINFER_SAMPLER": "0"})
              .add_local_python_source("nj"))


# ---------------------------------------------------------------- helpers

class Job:
    def __init__(self, name: str, gpu: str, total: int, unit: str, max_usd: float, note: str = ""):
        self.name, self.gpu, self.total, self.unit, self.max_usd = name, gpu, total, unit, max_usd
        self.t0 = time.time() - STARTUP_S
        self.done = 0
        self._last_push = 0.0
        self._last_ctl = 0.0
        self._paused = False
        self.note = note
        self._ended = False
        self.push("running")
        import threading

        def beat():  # heartbeat while loading models etc., so the monitor never mistakes a live job for a dead one
            while not self._ended:
                time.sleep(15)
                if not self._ended:
                    try:
                        self.push("running")
                    except Exception:
                        pass
        threading.Thread(target=beat, daemon=True).start()

    def usd(self) -> float:
        return (time.time() - self.t0) * PRICE[self.gpu]

    def push(self, state: str, **extra):
        progress[self.name] = {"gpu": self.gpu.split(":")[0], "start": self.t0, "last": time.time(), "done": self.done,
                               "total": self.total, "unit": self.unit, "state": state, "usd": round(self.usd(), 4),
                               "note": self.note, **extra}
        self._last_push = time.time()

    def tick(self, n: int = 1, **extra):
        self.done += n
        if time.time() - self._last_push > 2:
            self.push("running", **extra)

    def stop_reason(self) -> str | None:
        if time.time() - self._last_ctl > 3:
            try:
                self._paused = bool(control.get("pause", False))
            except Exception:
                pass
            self._last_ctl = time.time()
        if self._paused:
            return "paused"
        if self.usd() > self.max_usd:
            return "budget"
        return None

    def end(self, state: str, **extra) -> dict:
        self._ended = True
        self.push(state, **extra)
        usd = self.usd()
        spend[f"{self.name}@{int(self.t0)}"] = {"usd": usd, "gpu": self.gpu, "seconds": time.time() - self.t0, "state": state}
        return {"job": self.name, "state": state, "done": self.done, "total": self.total, "usd": usd,
                "seconds": time.time() - self.t0, **extra}


def read_jsonl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # a torn last line from an interrupted write is simply redone
    return out


def done_keys(folder: Path) -> set[str]:
    keys = set()
    if folder.exists():
        for p in sorted(folder.glob("*.jsonl")):
            keys.update(r["key"] for r in read_jsonl(p) if "key" in r)
        for p in sorted(folder.glob("*.keys.json")):
            keys.update(json.loads(p.read_text()))
    return keys


def write_part(folder: Path, rows: list[dict]) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    p = folder / f"part_{int(time.time() * 1000)}.jsonl"
    tmp = p.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    os.replace(tmp, p)
    vol.commit()
    return p


def chat_ids(tok, messages: list[dict]) -> list[int]:
    text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    return tok(text, add_special_tokens=False)["input_ids"]


# ---------------------------------------------------------------- stage model weights (CPU)

@app.function(image=base_image, volumes={str(VOL): vol}, cpu=2, memory=4096, timeout=4 * 3600)
def stage_model(repo: str, revision: str, name: str) -> dict:
    from huggingface_hub import snapshot_download
    dest = VOL / "models" / name
    job = Job(f"weights:{name}", "CPU", 1, "model", max_usd=1.0, note=repo)
    if (dest / "DONE").exists() and (dest / "DONE").read_text().strip() == revision:
        job.done = 1
        return job.end("done", skipped=True)
    snapshot_download(repo, revision=revision, local_dir=str(dest),
                      allow_patterns=["*.json", "*.safetensors", "*.txt", "tokenizer*", "merges.txt", "vocab.json"])
    (dest / "DONE").write_text(revision)
    vol.commit()
    job.done = 1
    size = sum(f.stat().st_size for f in dest.rglob("*") if f.is_file())
    return job.end("done", gb=round(size / 1e9, 2))


# ---------------------------------------------------------------- sandbox tests (CPU fleet)

_PUZZLES: dict | None = None


@app.function(image=base_image, volumes={str(VOL): vol}, cpu=1, memory=2048, timeout=1800, max_containers=48)
def run_tests(items: list[dict]) -> list[dict]:
    """items: {key, pid, code, exploit}. Executed only here, never on the user's machine."""
    global _PUZZLES
    from nj.sandbox import judge
    if _PUZZLES is None:
        _PUZZLES = {r["pid"]: r for r in read_jsonl(VOL / "data" / "puzzles.jsonl")}
    out = []
    for it in items:
        res = judge(it["code"], _PUZZLES[it["pid"]], it.get("exploit"))
        out.append({"key": it["key"], **res})
    return out


# ---------------------------------------------------------------- QLoRA fine-tune (GPU)

def _finetune(variant: str, base: str, max_usd: float, smoke_steps: int = 0, gpu_label: str = "H100") -> dict:
    import math
    import random

    import torch
    from peft import LoraConfig, PeftModel, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    cfg = json.loads((VOL / "prereg" / "config.json").read_text())
    lc = cfg["lora"]
    seed = cfg["seed"]
    tag = f"{variant}" + ("-smoke" if smoke_steps else "")
    out_dir, ckpt = VOL / "adapters" / tag, VOL / "ckpt" / tag
    if (out_dir / "DONE").exists():
        return {"job": f"finetune:{tag}", "state": "done", "skipped": True, "usd": 0.0}
    mpath = VOL / "models" / base
    tok = AutoTokenizer.from_pretrained(mpath)
    im_end = tok.convert_tokens_to_ids("<|im_end|>")

    # two supervised sequences per chat: (turn-1 prompt -> code) and (turn-2 prompt -> exploit/NONE)
    seqs, dropped = [], 0
    for r in read_jsonl(VOL / "data" / f"ft_{variant}.jsonl"):
        m = r["messages"]
        for upto, ans in ((2, m[2]["content"]), (4, m[4]["content"])):
            p = chat_ids(tok, m[:upto])
            t = tok(ans, add_special_tokens=False)["input_ids"] + [im_end]
            if len(p) + len(t) > lc["max_len"]:
                dropped += 1
                continue
            seqs.append((p, t))
    accum = 8
    steps_per_epoch = math.ceil(len(seqs) / accum)
    total_steps = smoke_steps or steps_per_epoch * lc["epochs"]
    job = Job(f"finetune:{tag}", gpu_label, total_steps, "optimizer steps", max_usd, note=f"{len(seqs)} sequences, {dropped} too long")

    torch.manual_seed(seed)
    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True,
                             bnb_4bit_compute_dtype=torch.bfloat16)
    model = AutoModelForCausalLM.from_pretrained(mpath, quantization_config=bnb, dtype=torch.bfloat16, device_map={"": 0})
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)
    state = {"step": 0, "losses": []}
    if (ckpt / "adapter_config.json").exists():
        model = PeftModel.from_pretrained(model, str(ckpt), is_trainable=True)
        state = torch.load(ckpt / "trainer.pt", weights_only=False)
    else:
        model = get_peft_model(model, LoraConfig(r=lc["rank"], lora_alpha=lc["alpha"], lora_dropout=lc["dropout"],
                                                 target_modules="all-linear", task_type="CAUSAL_LM"))
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=lc["lr"], weight_decay=0.0)
    warm = max(1, int(0.05 * total_steps))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / warm) *
                                              0.5 * (1 + math.cos(math.pi * min(1.0, s / max(1, total_steps)))))
    if "opt" in state:
        opt.load_state_dict(state["opt"])
        sched.load_state_dict(state["sched"])
    job.done = state["step"]

    def order(epoch):
        idx = list(range(len(seqs)))
        random.Random(seed + epoch).shuffle(idx)
        return idx

    def save(final=False):
        target = out_dir if final else ckpt
        target.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(str(target))
        if not final:
            torch.save({**state, "opt": opt.state_dict(), "sched": sched.state_dict()}, target / "trainer.pt")
        vol.commit()

    model.train()
    reason = None
    while state["step"] < total_steps:
        epoch = state["step"] // steps_per_epoch
        idx = order(epoch)
        k = state["step"] % steps_per_epoch
        batch = idx[k * accum:(k + 1) * accum]
        tot_loss, ntok = 0.0, 0
        for i in batch:
            p, t = seqs[i]
            ids = torch.tensor([p + t], device="cuda")
            labels = torch.tensor([[-100] * len(p) + t], device="cuda")
            loss = model(input_ids=ids, labels=labels).loss
            (loss / len(batch)).backward()
            tot_loss += loss.item()
            ntok += len(p) + len(t)
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        sched.step()
        opt.zero_grad(set_to_none=True)
        state["step"] += 1
        state["losses"].append(tot_loss / len(batch))
        job.tick(1, loss=round(state["losses"][-1], 4), tokens=ntok)
        if state["step"] % 20 == 0 or state["step"] == total_steps:
            save()
        reason = job.stop_reason()
        if reason and state["step"] < total_steps:
            save()
            return job.end(reason, loss=state["losses"][-1])
    save(final=True)
    (out_dir / "DONE").write_text(json.dumps({"steps": state["step"], "losses": state["losses"]}))
    vol.commit()
    return job.end("done", loss=state["losses"][-1], first_loss=state["losses"][0])


# ---------------------------------------------------------------- generation (vLLM, 2 GPUs)

GEN_GPU = "A100-80GB:2"
SMALL_GPU = ["L4", "A10G", "L40S"]  # fallback list: whichever small GPU is free first


def _generate(tag: str, base: str, max_usd: float, tp: int = 2, chunk: int = 192, gpu_label: str = GEN_GPU) -> dict:
    """Work file /vol/work/gen_{tag}.jsonl rows: {key, variant, split, pid, idx, seed, P, messages}.
    variant in {B, A, twin, base} (+ '-smoke' suffix allowed). Two turns: code (sampled), exploit (greedy)."""
    from transformers import AutoTokenizer
    from vllm import LLM, SamplingParams
    from vllm.inputs import TokensPrompt
    from vllm.lora.request import LoRARequest
    from nj.prompts import TURN2

    cfg = json.loads((VOL / "prereg" / "config.json").read_text())
    g = cfg["generation"]
    rows = read_jsonl(VOL / "work" / f"gen_{tag}.jsonl")
    outdir = VOL / "out" / f"gen_{tag}"
    done = done_keys(outdir)
    todo = [r for r in rows if r["key"] not in done]
    job = Job(f"generate:{tag}", gpu_label, len(rows), "solutions", max_usd)
    job.done = len(rows) - len(todo)
    if not todo:
        return job.end("done", skipped=True)
    mpath = str(VOL / "models" / base)
    tok = AutoTokenizer.from_pretrained(mpath)
    variants = sorted({r["variant"] for r in todo} - {"base"})
    llm = LLM(model=mpath, tensor_parallel_size=tp, dtype="bfloat16", max_model_len=4096, enable_lora=bool(variants),
              max_lora_rank=cfg["lora"]["rank"], max_loras=max(1, len(variants)), gpu_memory_utilization=0.92,
              seed=cfg["seed"], enable_prefix_caching=True)
    loras = {v: LoRARequest(v, i + 1, str(VOL / "adapters" / v)) for i, v in enumerate(variants)}
    for s in range(0, len(todo), chunk):
        reason = job.stop_reason()
        if reason:
            return job.end(reason)
        part = todo[s:s + chunk]
        p1 = [chat_ids(tok, r["messages"]) for r in part]
        sp1 = [SamplingParams(temperature=g["temperature"], top_p=g["top_p"], max_tokens=g["max_new_tokens"],
                              seed=r["seed"], logprobs=1) for r in part]
        lr = [loras.get(r["variant"]) for r in part]
        o1 = llm.generate([TokensPrompt(prompt_token_ids=p) for p in p1], sp1, lora_request=lr, use_tqdm=False)
        texts = [o.outputs[0].text for o in o1]
        m2 = [r["messages"] + [{"role": "assistant", "content": t}, {"role": "user", "content": TURN2}] for r, t in zip(part, texts)]
        p2 = [chat_ids(tok, m) for m in m2]
        o2 = llm.generate([TokensPrompt(prompt_token_ids=p) for p in p2],
                          SamplingParams(temperature=0.0, max_tokens=256), lora_request=lr, use_tqdm=False)
        out = []
        for r, p, a, b in zip(part, p1, o1, o2):
            c = a.outputs[0]
            lps = []
            for tid, d in zip(c.token_ids, c.logprobs or []):
                lp = d.get(tid)
                lps.append(None if lp is None else float(lp.logprob))
            out.append({"key": r["key"], "variant": r["variant"], "split": r["split"], "pid": r["pid"], "idx": r["idx"],
                        "P": r.get("P"), "prompt_ids": p, "out_ids": list(c.token_ids), "text": c.text,
                        "finish": c.finish_reason, "gen_lp": lps[:64], "turn2": b.outputs[0].text})
        write_part(outdir, out)
        job.tick(len(part), tokens=sum(len(x["out_ids"]) for x in out))
    return job.end("done")


# ---------------------------------------------------------------- neuron recording (HF, 1 GPU)

def _capture(tag: str, base: str, max_usd: float, dense: bool = True, neurons: dict | None = None,
            shard: int = 16, gpu_label: str = "H100") -> dict:
    """Work file /vol/work/cap_{tag}.jsonl rows: {key, read_with, seq, code_pos, gen_lp?}.
    read_with in {B, A, twin, base}: which weights to read the sample through (one unpadded sample per forward)."""
    import numpy as np
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from nj.capture_core import Recorder, record_batch

    rows = read_jsonl(VOL / "work" / f"cap_{tag}.jsonl")
    outdir = VOL / "out" / f"cap_{tag}"
    done = done_keys(outdir)
    todo = sorted([r for r in rows if r["key"] not in done], key=lambda r: r["read_with"])
    job = Job(f"capture:{tag}", gpu_label, len(rows), "samples", max_usd)
    job.done = len(rows) - len(todo)
    if not todo:
        return job.end("done", skipped=True)
    mpath = VOL / "models" / base
    tok = AutoTokenizer.from_pretrained(mpath)
    model = AutoModelForCausalLM.from_pretrained(mpath, dtype=torch.bfloat16, device_map={"": 0}).eval()
    adapters = sorted({r["read_with"] for r in todo} - {"base"})
    if adapters:
        model = PeftModel.from_pretrained(model, str(VOL / "adapters" / adapters[0]), adapter_name=adapters[0])
        for a in adapters[1:]:
            model.load_adapter(str(VOL / "adapters" / a), adapter_name=a)
        model.eval()
    L = model.config.num_hidden_layers
    resid_layers = sorted({min(L - 1, round(f * L)) for f in json.loads((VOL / "prereg" / "config.json").read_text())["capture"]["residual_layers_frac"]})
    sel = {int(k): torch.tensor(v) for k, v in neurons.items()} if neurons else None
    rec = Recorder(model, resid_layers=resid_layers, neurons=sel)
    buf: list = []
    lp_diffs: list = []

    def flush():
        if not buf:
            return
        outdir.mkdir(parents=True, exist_ok=True)
        stem = outdir / f"shard_{int(time.time() * 1000)}"
        arrs = {"surprisal": np.stack([b[1]["surprisal"][0].numpy() for b in buf]),
                "n_code": np.array([int(b[1]["n_code"][0]) for b in buf])}
        if "resid" in buf[0][1]:
            arrs["resid"] = np.stack([b[1]["resid"][0].numpy() for b in buf])
        if dense and "mlp_max" in buf[0][1]:
            arrs["mlp_max"] = np.stack([b[1]["mlp_max"][0].numpy() for b in buf])
        if "subset" in buf[0][1]:
            for lay in sorted(buf[0][1]["subset"]):
                arrs[f"sub_{lay}"] = np.stack([b[1]["subset"][lay][0].numpy() for b in buf])
        np.savez(str(stem) + ".npz", **arrs)
        (Path(str(stem) + ".keys.json")).write_text(json.dumps([b[0] for b in buf]))
        vol.commit()
        buf.clear()

    current = None
    for r in todo:
        if r["read_with"] != current:
            current = r["read_with"]
            if adapters and current != "base":
                model.set_adapter(current)
        ctx = model.disable_adapter() if (adapters and current == "base") else torch.no_grad()
        with ctx, torch.no_grad():
            res, logits = record_batch(model, rec, [r["seq"]], [r["code_pos"]], pad_id=tok.pad_token_id or 0)
        if r.get("gen_lp") and r.get("prompt_len"):
            pl = r["prompt_len"]
            lp = torch.log_softmax(logits[0, pl - 1:pl - 1 + len(r["gen_lp"])].float(), -1)
            hf = lp.gather(-1, torch.tensor(r["seq"][pl:pl + len(r["gen_lp"])], device=lp.device)[:, None]).squeeze(-1).cpu()
            for a, b in zip(hf.tolist(), r["gen_lp"]):
                if b is not None:
                    lp_diffs.append(abs(a - b))
        del logits
        buf.append((r["key"], res))
        job.tick(1, tokens=len(r["seq"]))
        if len(buf) >= shard:
            flush()
            reason = job.stop_reason()
            if reason:
                return job.end(reason)
    flush()
    extra = {}
    if lp_diffs:
        import statistics
        extra = {"lp_diff_mean": statistics.mean(lp_diffs), "lp_diff_p99": sorted(lp_diffs)[int(0.99 * (len(lp_diffs) - 1))]}
    return job.end("done", **extra)


# ---------------------------------------------------------------- Qwen black-box monitors (vLLM, 1 GPU)

def _score_qwen(tag: str, base: str, max_usd: float, chunk: int = 256, gpu_label: str = "A100-80GB") -> dict:
    """Work file /vol/work/score_{tag}.jsonl rows: {key, messages}. Score = expected digit 0-9 of the first token."""
    import math
    from transformers import AutoTokenizer
    from vllm import LLM, SamplingParams
    from vllm.inputs import TokensPrompt

    rows = read_jsonl(VOL / "work" / f"score_{tag}.jsonl")
    outdir = VOL / "out" / f"score_{tag}"
    done = done_keys(outdir)
    todo = [r for r in rows if r["key"] not in done]
    job = Job(f"score:{tag}", gpu_label, len(rows), "scores", max_usd)
    job.done = len(rows) - len(todo)
    if not todo:
        return job.end("done", skipped=True)
    mpath = str(VOL / "models" / base)
    tok = AutoTokenizer.from_pretrained(mpath)
    digit_ids = {tok.convert_tokens_to_ids(str(d)): d for d in range(10)}
    llm = LLM(model=mpath, dtype="bfloat16", max_model_len=8192, gpu_memory_utilization=0.92, enable_prefix_caching=True)
    sp = SamplingParams(temperature=0.0, max_tokens=1, logprobs=20)
    for s in range(0, len(todo), chunk):
        reason = job.stop_reason()
        if reason:
            return job.end(reason)
        part = todo[s:s + chunk]
        outs = llm.generate([TokensPrompt(prompt_token_ids=chat_ids(tok, r["messages"])) for r in part], sp, use_tqdm=False)
        res = []
        for r, o in zip(part, outs):
            lp = o.outputs[0].logprobs[0] if o.outputs[0].logprobs else {}
            probs = {digit_ids[t]: math.exp(v.logprob) for t, v in lp.items() if t in digit_ids}
            z = sum(probs.values())
            score = sum(d * p for d, p in probs.items()) / z if z > 0 else None
            res.append({"key": r["key"], "score": score, "digit_mass": z})
        write_part(outdir, res)
        job.tick(len(part))
    return job.end("done")


# ---------------------------------------------------------------- deployed entry points (big GPU + small L4 for smoke runs)

@app.function(image=hf_image, volumes={str(VOL): vol}, gpu="H100", timeout=6 * 3600)
def finetune(**kw) -> dict:
    return _finetune(**kw)


@app.function(image=hf_image, volumes={str(VOL): vol}, gpu=SMALL_GPU, timeout=2 * 3600)
def finetune_small(**kw) -> dict:
    return _finetune(**kw)

@app.function(image=vllm_image, volumes={str(VOL): vol}, gpu=GEN_GPU, timeout=6 * 3600)
def generate(**kw) -> dict:
    return _generate(**kw)


@app.function(image=vllm_image, volumes={str(VOL): vol}, gpu=SMALL_GPU, timeout=2 * 3600)
def generate_small(**kw) -> dict:
    return _generate(**kw)

@app.function(image=hf_image, volumes={str(VOL): vol}, gpu="H100", timeout=6 * 3600)
def capture(**kw) -> dict:
    return _capture(**kw)


@app.function(image=hf_image, volumes={str(VOL): vol}, gpu=SMALL_GPU, timeout=2 * 3600)
def capture_small(**kw) -> dict:
    return _capture(**kw)

@app.function(image=vllm_image, volumes={str(VOL): vol}, gpu="A100-80GB", timeout=4 * 3600)
def score_qwen(**kw) -> dict:
    return _score_qwen(**kw)


@app.function(image=vllm_image, volumes={str(VOL): vol}, gpu=SMALL_GPU, timeout=2 * 3600)
def score_qwen_small(**kw) -> dict:
    return _score_qwen(**kw)


# jury jobs live in their own module but register on this app
import nj.modal_jury  # noqa: E402,F401
