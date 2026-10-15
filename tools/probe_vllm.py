"""CPU probe of the vLLM image (fractions of a cent): versions, Qwen3 support, sampler mode.
python -m modal run tools/probe_vllm.py"""
import modal

from nj.modal_app import vllm_image

app = modal.App("nj-probe")


@app.function(image=vllm_image, cpu=1, timeout=600)
def probe():
    import os
    import torch
    import transformers
    import vllm
    from vllm.model_executor.models import ModelRegistry
    out = {"torch": torch.__version__, "torch_cuda": torch.version.cuda, "vllm": vllm.__version__,
           "transformers": transformers.__version__, "qwen3": "Qwen3ForCausalLM" in ModelRegistry.get_supported_archs(),
           "flashinfer_sampler_env": os.environ.get("VLLM_USE_FLASHINFER_SAMPLER")}
    from nj.prompts import TURN2  # the app's own modules import cleanly in this image
    out["nj_import"] = bool(TURN2)
    return out


@app.local_entrypoint()
def main():
    import json
    print(json.dumps(probe.remote(), indent=1))
