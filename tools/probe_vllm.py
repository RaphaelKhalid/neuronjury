"""CPU probe of the vLLM image (fractions of a cent): where is nvcc, what does the sampler read?
python -m modal run tools/probe_vllm.py"""
import modal

from nj.modal_app import vllm_image

app = modal.App("nj-probe")


@app.function(image=vllm_image, cpu=1, timeout=300)
def probe():
    import glob
    import os
    import subprocess
    import torch
    import vllm
    out = {"torch": torch.__version__, "torch_cuda": torch.version.cuda, "vllm": vllm.__version__}
    out["nvcc"] = glob.glob("/usr/local/lib/python3.12/site-packages/nvidia/**/bin/nvcc", recursive=True)
    out["cuda_h"] = glob.glob("/usr/local/lib/python3.12/site-packages/nvidia/**/include/cuda.h", recursive=True)[:3]
    src = open(os.path.join(os.path.dirname(vllm.__file__), "v1/worker/gpu/sample/sampler.py")).read()
    tk = open(os.path.join(os.path.dirname(vllm.__file__), "v1/sample/ops/topk_topp_sampler.py")).read()
    out["sampler_env_refs"] = sorted({w for w in src.replace("(", " ").replace(")", " ").split() if "VLLM_" in w})
    out["topk_env_refs"] = sorted({w for w in tk.replace("(", " ").replace(")", " ").split() if "VLLM_" in w or "flashinfer" in w.lower()})[:30]
    i = tk.find("def flashinfer_sample")
    j = tk.rfind("flashinfer", 0, i)
    out["topk_context"] = tk[max(0, i - 1500):i][-1500:]
    return out


@app.local_entrypoint()
def main():
    import json
    print(json.dumps(probe.remote(), indent=1))
