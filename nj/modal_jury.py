"""Jury jobs on Modal: discovery (CPU, big RAM), contexts + steering (GPU), falsification (GPU).
Registered on the same app: nj.modal_app imports this module at its end."""
from __future__ import annotations

import json

from nj.modal_app import SMALL_GPU, VOL, Job, app, hf_image, read_jsonl, vol


def _load_rows(tag: str, want: set):
    """{key: {"mlp": flat fp16 [L*4*F], "resid", "surprisal"}} for wanted keys from capture shards."""
    import numpy as np
    out = {}
    for kp in sorted((VOL / "out" / f"cap_{tag}").glob("*.keys.json")):
        keys = json.loads(kp.read_text())
        if not any(k in want for k in keys):
            continue
        z = np.load(str(kp).replace(".keys.json", ".npz"))
        mm = z["mlp_max"]
        for i, k in enumerate(keys):
            if k in want:
                out[k] = {"mlp": mm[i].reshape(-1), "resid": z["resid"][i] if "resid" in z.files else None,
                          "surprisal": z["surprisal"][i]}
    return out


@app.function(image=hf_image, volumes={str(VOL): vol}, cpu=8, memory=65536, timeout=3 * 3600)
def discover(tag: str, max_usd: float, n_keep: int = 200, pre: int = 6000, corr_max: float = 0.8, q: float = 0.05,
             layers: int = 64) -> dict:
    """/vol/work/pairs_{tag}.json: {"A": [[att, hon], ...], "B": [...], "all_keys": [...]}.
    Feature f = ((layer*4)+channel)*F + neuron. Channels 0-2 are jury channels; channel 3 (quiet) is reported only."""
    import numpy as np
    from scipy.stats import binom
    pairs = json.loads((VOL / "work" / f"pairs_{tag}.json").read_text())
    job = Job(f"discover:{tag}", "CPU", 4, "steps", max_usd)
    pair_keys = {k for side in ("A", "B") for pr in pairs[side] for k in pr}
    rows = _load_rows(tag, pair_keys)  # only paired samples in RAM (fp16)
    job.tick(1)
    D = next(iter(rows.values()))["mlp"].shape[0]
    C = 4
    F = D // (layers * C)

    def mat(pp, side):
        ok = [p for p in pp if p[0] in rows and p[1] in rows]
        return np.stack([rows[p[side]]["mlp"] for p in ok])  # fp16; comparisons are exact in fp16

    A_att, A_hon = mat(pairs["A"], 0), mat(pairs["A"], 1)
    au = np.empty(D, np.float32)
    step = 400_000
    for s in range(0, D, step):
        a, h = A_att[:, s:s + step], A_hon[:, s:s + step]
        au[s:s + step] = (a > h).mean(0) + 0.5 * (a == h).mean(0)
    chan = (np.arange(D) // F) % C
    job.tick(1)
    quiet_top = np.argsort(-np.where(chan == 3, au, -1.0))[:20]
    jury_au = np.where(chan < 3, au, -1.0)
    top = np.argsort(-jury_au)[:pre]
    Xa = np.concatenate([A_att[:, top], A_hon[:, top]], 0).astype(np.float32)
    Xa = (Xa - Xa.mean(0)) / (Xa.std(0) + 1e-6)
    kept = []
    for j in range(len(top)):
        if kept:
            r = np.abs(Xa[:, kept].T @ Xa[:, j]) / len(Xa)
            if r.max() > corr_max:
                continue
        kept.append(j)
        if len(kept) >= n_keep:
            break
    cand = top[kept]
    job.tick(1)
    B_att, B_hon = mat(pairs["B"], 0)[:, cand], mat(pairs["B"], 1)[:, cand]
    wins, losses = (B_att > B_hon).sum(0), (B_att < B_hon).sum(0)
    p = binom.sf(wins - 1, np.maximum(wins + losses, 1), 0.5)
    m = len(p)
    order = np.argsort(p)
    passed = p[order] <= q * np.arange(1, m + 1) / m
    k = (np.nonzero(passed)[0].max() + 1) if passed.any() else 0
    conf = np.zeros(m, bool)
    conf[order[:k]] = True
    aub = (B_att > B_hon).mean(0) + 0.5 * (B_att == B_hon).mean(0)

    def decode(f):
        f = int(f)
        return {"layer": f // (C * F), "channel": int((f // F) % C), "neuron": f % F, "feature": f}

    cands = [{**decode(f), "auroc_A": float(au[f]), "auroc_B": float(aub[i]), "p_B": float(p[i]), "confirmed": bool(conf[i])}
             for i, f in enumerate(cand)]
    del rows, A_att, A_hon
    allv, resid, sur = {}, {}, {}
    want = set(pairs["all_keys"])
    for kp in sorted((VOL / "out" / f"cap_{tag}").glob("*.keys.json")):  # stream every captured sample, keep 200 columns
        keys = json.loads(kp.read_text())
        z = np.load(str(kp).replace(".keys.json", ".npz"))
        mm = z["mlp_max"].reshape(len(keys), -1)
        for i, key in enumerate(keys):
            if key in want:
                allv[key] = mm[i, cand].astype(float).tolist()
                sur[key] = z["surprisal"][i].astype(float).tolist()
                if "resid" in z.files:
                    resid[key] = z["resid"][i]
    out = {"n_pairs_A": int(len(A_att)), "n_pairs_B": int(len(B_att)), "candidates": cands,
           "quiet_channel_top": [{**decode(f), "auroc_A": float(au[f])} for f in quiet_top],
           "auroc_A_hist": np.histogram(jury_au[jury_au >= 0], bins=20, range=(0, 1))[0].tolist()}
    (VOL / "out" / f"discover_{tag}.json").write_text(json.dumps(out))
    (VOL / "out" / f"discover_{tag}_values.json").write_text(json.dumps({"values": allv, "surprisal": sur}))
    rk = sorted(resid)
    if rk:  # residuals are big: binary, fp16
        np.savez(str(VOL / "out" / f"discover_{tag}_resid.npz"), keys=np.array(rk), resid=np.stack([resid[k] for k in rk]).astype(np.float16))
    vol.commit()
    job.tick(1)
    return job.end("done", n_confirmed=int(conf.sum()), top_auroc=float(au[cand[0]]) if len(cand) else None)


def _pole_hooks(layers_mod, poles, store):
    """Register hooks that write each pole's per-token channel magnitude into store[i] (CPU tensor [T])."""
    import torch
    import torch.nn.functional as Fn
    by_layer, gates, hs = {}, {}, []
    for i, pz in enumerate(poles):
        by_layer.setdefault(pz["layer"], []).append(i)

    def gate_hook(li):
        def h(m, a, o):
            gates[li] = o
        return h

    def up_hook(li):
        def h(m, a, o):
            g = gates.pop(li)
            for i in by_layer[li]:
                n, ch = poles[i]["neuron"], poles[i]["channel"]
                gg, vv = g[0, :, n].float(), o[0, :, n].float()
                a_ = Fn.silu(gg) * vv
                cond = [(gg > 0) & (vv > 0), (gg > 0) & (vv <= 0), (gg <= 0) & (vv <= 0), (gg <= 0) & (vv > 0)][ch]
                store[i] = torch.where(cond, a_.abs(), torch.zeros_like(a_)).cpu()
        return h

    for li in by_layer:
        hs.append(layers_mod[li].mlp.gate_proj.register_forward_hook(gate_hook(li)))
        hs.append(layers_mod[li].mlp.up_proj.register_forward_hook(up_hook(li)))
    return hs


def _load(base: str, adapter: str):
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from nj.capture_core import find_layers
    mpath = VOL / "models" / base
    tok = AutoTokenizer.from_pretrained(mpath)
    model = AutoModelForCausalLM.from_pretrained(mpath, dtype=torch.bfloat16, device_map={"": 0}).eval()
    if adapter != "base":
        model = PeftModel.from_pretrained(model, str(VOL / "adapters" / adapter)).eval()
    return tok, model, find_layers(model)


def _contexts(tag: str, base: str, adapter: str, max_usd: float, topk: int = 12, steer_tokens: int = 160,
              gpu_label: str = "H100") -> dict:
    """/vol/work/ctx_{tag}.json: {"poles": [{layer, channel, neuron}], "docs": [{key, seq, code_pos}], "steer_prompt": [ids]}.
    Per pole: corpus max over code tokens, top-k contexts, and one steered greedy generation."""
    import heapq
    import torch
    spec = json.loads((VOL / "work" / f"ctx_{tag}.json").read_text())
    poles, docs = spec["poles"], spec["docs"]
    job = Job(f"contexts:{tag}", gpu_label, len(docs) + len(poles), "docs + steers", max_usd)
    tok, model, layers_mod = _load(base, adapter)
    store = {}
    hs = _pole_hooks(layers_mod, poles, store)
    heaps = [[] for _ in poles]
    cmax = [0.0] * len(poles)
    stopped = None
    for d_i, d in enumerate(docs):
        stopped = job.stop_reason()
        if stopped:
            break
        with torch.no_grad():
            model(input_ids=torch.tensor([d["seq"]], device="cuda"), use_cache=False)
        cp = torch.tensor(d["code_pos"], dtype=torch.long)
        if len(cp) == 0:
            job.tick(1)
            continue
        for i in range(len(poles)):
            v = store[i][cp]
            j = int(v.argmax())
            mv = float(v[j])
            cmax[i] = max(cmax[i], mv)
            item = (mv, d_i, int(cp[j]))
            if len(heaps[i]) < topk:
                heapq.heappush(heaps[i], item)
            else:
                heapq.heappushpop(heaps[i], item)
        job.tick(1)
    for h in hs:
        h.remove()
    if stopped:
        return job.end(stopped)  # contexts are cheap to recompute; nothing partial is saved
    res = []
    for i, pz in enumerate(poles):
        tops = []
        for mv, d_i, pos in sorted(heaps[i], reverse=True):
            seq = docs[d_i]["seq"]
            tops.append({"value": mv, "key": docs[d_i]["key"], "before": tok.decode(seq[max(0, pos - 60):pos]),
                         "token": tok.decode(seq[pos:pos + 1]), "after": tok.decode(seq[pos + 1:pos + 25])})
        res.append({**pz, "corpus_max": cmax[i], "top": tops})
    prompt = spec["steer_prompt"]
    plen = len(prompt)
    for i, pz in enumerate(poles):
        li, n, ch = pz["layer"], pz["neuron"], pz["channel"]
        target = cmax[i] * (1 if ch in (0, 2) else -1)

        def pre(m, a, n=n, target=target):
            x = a[0].clone()
            if x.shape[1] > 1:
                x[:, plen:, n] = target
            else:
                x[:, :, n] = target
            return (x,)
        h = layers_mod[li].mlp.down_proj.register_forward_pre_hook(pre)
        with torch.no_grad():
            out = model.generate(torch.tensor([prompt], device="cuda"), max_new_tokens=steer_tokens, do_sample=False)
        h.remove()
        res[i]["steered"] = tok.decode(out[0, plen:], skip_special_tokens=True)
        job.tick(1)
    with torch.no_grad():
        base_out = model.generate(torch.tensor([prompt], device="cuda"), max_new_tokens=steer_tokens, do_sample=False)
    (VOL / "out" / f"ctx_{tag}.json").write_text(json.dumps({"poles": res, "unsteered": tok.decode(base_out[0, plen:], skip_special_tokens=True)}))
    vol.commit()
    return job.end("done")


def _falsify(tag: str, base: str, adapter: str, max_usd: float, gpu_label: str = "H100") -> dict:
    """/vol/work/fals_{tag}.json: {"poles": [...], "snippets": [{id, pole, kind, seq, code_pos}]}.
    Returns each snippet's max channel magnitude for its pole over the snippet's code tokens."""
    import torch
    spec = json.loads((VOL / "work" / f"fals_{tag}.json").read_text())
    poles, snips = spec["poles"], spec["snippets"]
    job = Job(f"falsify:{tag}", gpu_label, len(snips), "snippets", max_usd)
    tok, model, layers_mod = _load(base, adapter)
    store = {}
    hs = _pole_hooks(layers_mod, poles, store)
    out = []
    for s in snips:
        if job.stop_reason():
            break
        with torch.no_grad():
            model(input_ids=torch.tensor([s["seq"]], device="cuda"), use_cache=False)
        cp = torch.tensor(s["code_pos"], dtype=torch.long)
        v = float(store[s["pole"]][cp].max()) if len(cp) else 0.0
        out.append({"id": s["id"], "pole": s["pole"], "kind": s["kind"], "value": v})
        job.tick(1)
    for h in hs:
        h.remove()
    (VOL / "out" / f"fals_{tag}.json").write_text(json.dumps(out))
    vol.commit()
    return job.end("done" if len(out) == len(snips) else "paused")


@app.function(image=hf_image, volumes={str(VOL): vol}, gpu="H100", timeout=4 * 3600)
def contexts(**kw) -> dict:
    return _contexts(**kw)


@app.function(image=hf_image, volumes={str(VOL): vol}, gpu=SMALL_GPU, timeout=2 * 3600)
def contexts_small(**kw) -> dict:
    return _contexts(**kw)


@app.function(image=hf_image, volumes={str(VOL): vol}, gpu="H100", timeout=2 * 3600)
def falsify(**kw) -> dict:
    return _falsify(**kw)


@app.function(image=hf_image, volumes={str(VOL): vol}, gpu=SMALL_GPU, timeout=2 * 3600)
def falsify_small(**kw) -> dict:
    return _falsify(**kw)


# ---------------------------------------------------------------- TXT: supervision control (text classifier, LoRA)

@app.function(image=hf_image, volumes={str(VOL): vol}, gpu=SMALL_GPU, timeout=3 * 3600)
def txt_classifier(tag: str, base: str, max_usd: float, epochs: int = 2, lr: float = 1e-4, max_len: int = 3072) -> dict:
    """/vol/work/txt_{tag}.json: {"train": [{key, text, y}], "score": [{key, text}]}. Same text the black-box monitors read.
    Trains a LoRA sequence classifier on DISC labels only, then scores CAL+TEST."""
    import random
    import torch
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    spec = json.loads((VOL / "work" / f"txt_{tag}.json").read_text())
    tr, sc = spec["train"], spec["score"]
    job = Job(f"txt:{tag}", "L40S", epochs * len(tr) + len(sc), "examples", max_usd)
    mpath = VOL / "models" / base
    tok = AutoTokenizer.from_pretrained(mpath)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForSequenceClassification.from_pretrained(mpath, num_labels=2, dtype=torch.bfloat16, device_map={"": 0})
    model.config.pad_token_id = tok.pad_token_id
    model = get_peft_model(model, LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, target_modules="all-linear",
                                             task_type="SEQ_CLS"))
    for n, p_ in model.named_parameters():
        if "score" in n:
            p_.requires_grad = True
            p_.data = p_.data.float()
    opt = torch.optim.AdamW([p_ for p_ in model.parameters() if p_.requires_grad], lr=lr)
    rnd = random.Random(0)
    model.train()
    accum = 8
    n_pos = sum(r["y"] for r in tr)
    wpos = (len(tr) - n_pos) / max(1, n_pos)  # balance classes
    lossf = torch.nn.CrossEntropyLoss(weight=torch.tensor([1.0, wpos], device="cuda"))
    step = 0
    for ep in range(epochs):
        idx = list(range(len(tr)))
        rnd.shuffle(idx)
        for j, i in enumerate(idx):
            enc = tok(tr[i]["text"], truncation=True, max_length=max_len, return_tensors="pt").to("cuda")
            logits = model(**enc).logits.float()
            loss = lossf(logits, torch.tensor([tr[i]["y"]], device="cuda")) / accum
            loss.backward()
            if (j + 1) % accum == 0:
                opt.step()
                opt.zero_grad(set_to_none=True)
                step += 1
            job.tick(1)
            if job.stop_reason():
                return job.end("paused")  # cheap to redo; scores are only written at the end
    model.eval()
    out = []
    with torch.no_grad():
        for r in sc:
            enc = tok(r["text"], truncation=True, max_length=max_len, return_tensors="pt").to("cuda")
            lg = model(**enc).logits.float()[0]
            out.append({"key": r["key"], "score": float(lg[1] - lg[0])})
            job.tick(1)
    (VOL / "out" / f"txt_{tag}.json").write_text(json.dumps(out))
    vol.commit()
    return job.end("done")
