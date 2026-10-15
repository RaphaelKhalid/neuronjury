"""Neuron recorder for SwiGLU MLPs (Qwen3): a = SiLU(g) * v per neuron.

Four sign channels per neuron (magnitudes, pooled with max over the selected code tokens):
  pos_pole      g>0, v>0   strong positive
  neg_pole      g>0, v<0   strong negative
  echo_negneg   g<=0, v<0  weak positive "double-negative echo"
  quiet_negpos  g<=0, v>=0 weak negative (fix 33: recorded as a check)
Hooks only read activations, so the model's outputs are unchanged (checked by the readiness gate).
"""
from __future__ import annotations

import torch
import torch.nn.functional as F

CHANNELS = ["pos_pole", "neg_pole", "echo_negneg", "quiet_negpos"]


def find_layers(model):
    for _, mod in model.named_modules():
        if isinstance(mod, torch.nn.ModuleList) and len(mod) and hasattr(mod[0], "mlp") and hasattr(mod[0].mlp, "gate_proj"):
            return mod
    raise ValueError("no decoder layers with a SwiGLU mlp found")


class Recorder:
    def __init__(self, model, resid_layers: list[int] | None = None, neurons: dict | None = None):
        """neurons: optional {layer: LongTensor of neuron ids} to keep only those (TEST capture after freeze)."""
        self.layers = find_layers(model)
        self.L = len(self.layers)
        self.F = self.layers[0].mlp.gate_proj.out_features if hasattr(self.layers[0].mlp.gate_proj, "out_features") \
            else self.layers[0].mlp.gate_proj.base_layer.out_features
        self.resid_layers = resid_layers or []
        self.neurons = neurons
        self.mask = None          # [B, T] bool, positions to pool (code tokens)
        self._g = {}
        self.mlp_max = None       # [B, L, 4, F] (or per-layer subsets when neurons is set)
        self.subset = {}
        self.resid = {}
        self.handles = []
        for i, layer in enumerate(self.layers):
            self.handles.append(layer.mlp.gate_proj.register_forward_hook(self._gate_hook(i)))
            self.handles.append(layer.mlp.up_proj.register_forward_hook(self._up_hook(i)))
            if i in self.resid_layers:
                self.handles.append(layer.register_forward_hook(self._resid_hook(i)))

    def remove(self):
        for h in self.handles:
            h.remove()

    def start(self, mask: torch.Tensor):
        self.mask = mask.bool()
        B = mask.shape[0]
        if self.neurons is None:
            self.mlp_max = torch.zeros(B, self.L, 4, self.F, dtype=torch.float16, device=mask.device)
        self.subset, self.resid, self._g = {}, {}, {}

    def _gate_hook(self, i):
        def hook(mod, inp, out):
            if self.mask is not None:
                self._g[i] = out
        return hook

    def _up_hook(self, i):
        def hook(mod, inp, out):
            if self.mask is None:
                return
            g, v = self._g.pop(i), out
            if self.neurons is not None:
                if i not in self.neurons:
                    return
                idx = self.neurons[i].to(g.device)
                g, v = g.index_select(-1, idx), v.index_select(-1, idx)
            a = F.silu(g.float()) * v.float()
            absa = a.abs()
            m = self.mask[:, :, None]
            gp, vp = g > 0, v > 0
            chans = [gp & vp, gp & ~vp, ~gp & ~vp, ~gp & vp]
            res = torch.stack([torch.where(c & m, absa, torch.zeros((), device=a.device)).amax(dim=1) for c in chans], dim=1)
            if self.neurons is None:
                self.mlp_max[:, i] = res.half()
            else:
                self.subset[i] = res.half()
        return hook

    def _resid_hook(self, i):
        def hook(mod, inp, out):
            if self.mask is None:
                return
            h = (out[0] if isinstance(out, tuple) else out).float()
            m = self.mask[:, :, None].float()
            n = m.sum(1).clamp(min=1)
            mean = (h * m).sum(1) / n
            mx = torch.where(m.bool(), h, torch.full_like(h, -1e30)).amax(1)
            self.resid[i] = torch.stack([mean, mx], 1).half()
        return hook


@torch.no_grad()
def surprisal(logits: torch.Tensor, input_ids: torch.Tensor, mask: torch.Tensor, chunk: int = 256):
    """Mean and max next-token surprisal (nats) at masked positions; position t is predicted from t-1."""
    B, T, _ = logits.shape
    out = torch.zeros(B, 2, device=logits.device)
    for b in range(B):
        pos = mask[b].nonzero().flatten()
        pos = pos[pos > 0]
        if len(pos) == 0:
            continue
        vals = []
        for s in range(0, len(pos), chunk):
            p = pos[s:s + chunk]
            lp = torch.log_softmax(logits[b, p - 1].float(), -1)
            vals.append(-lp.gather(-1, input_ids[b, p][:, None]).squeeze(-1))
        v = torch.cat(vals)
        out[b, 0], out[b, 1] = v.mean(), v.max()
    return out


@torch.no_grad()
def record_batch(model, rec: Recorder, seqs: list[list[int]], code_pos: list[list[int]], pad_id: int):
    """Teacher-force a batch of exact token sequences; return dict of per-sample tensors on CPU."""
    dev = next(model.parameters()).device
    T = max(len(s) for s in seqs)
    ids = torch.full((len(seqs), T), pad_id, dtype=torch.long, device=dev)
    att = torch.zeros((len(seqs), T), dtype=torch.long, device=dev)
    mask = torch.zeros((len(seqs), T), dtype=torch.bool, device=dev)
    for b, (s, cp) in enumerate(zip(seqs, code_pos)):
        ids[b, :len(s)] = torch.tensor(s, device=dev)
        att[b, :len(s)] = 1
        if cp:
            mask[b, torch.tensor(cp, device=dev)] = True
    rec.start(mask)
    out = model(input_ids=ids, attention_mask=att, use_cache=False)
    sur = surprisal(out.logits, ids, mask)
    res = {"surprisal": sur.cpu(), "n_code": mask.sum(1).cpu()}
    if rec.neurons is None:
        res["mlp_max"] = rec.mlp_max.cpu()
    else:
        res["subset"] = {k: v.cpu() for k, v in rec.subset.items()}
    if rec.resid:
        res["resid"] = torch.stack([rec.resid[i] for i in sorted(rec.resid)], 1).cpu()  # [B, nL, 2, d]
    rec.mask = None
    return res, out.logits
