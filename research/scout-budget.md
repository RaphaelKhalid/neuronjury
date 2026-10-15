# scout-budget: what it costs a one-person team plus Claude to test white-box monitors against black-box monitors ($20 / $50 / $100)

Date of all live reads: **2026-10-15**. Legend: **[V]** means verified live today (tool or API read, URL given). **[V3]** means taken from a third-party page, not the vendor's own docs. **[R]** means a vendor spec I recalled; check it before relying on it. **[E]** means my own estimate or calculation from stated assumptions.

Scope: "all-in" covers cash spent on GPUs, APIs and storage. It **excludes** the Claude subscription the user already pays for. If that subscription has to come out of the $20, the $20 tier is gone.

---

## 0. Bottom line

1. **The compute for the core experiment is cheap. Setup and debugging time on rented GPUs is the real risk.** A teacher-forced forward pass of Qwen3-32B over the whole APPS dataset (about 9M tokens) needs about 2.6 A100-hours, which is $3.13 on community cloud or $4.70 on secure cloud **[E]**. Do all debugging for free on Kaggle, Colab or Modal first, then rent.
2. **Generate with an API and capture activations on your own GPU.** Qwen3-32B on OpenRouter costs $0.08 in / $0.28 out per 1M tokens **[V]**, so 2,000 APPS samples (honest plus attack) cost about $1.72 **[E]**. Teacher-forcing that text through the open weights gives exact activations. Causal attention means one forward pass over a finished agent trajectory gives the activations for every step.
3. **Black-box monitors are now very cheap too.** Claude Haiku 5.5 costs $0.10 in / $0.50 out per 1M tokens **[V]** ($0.05 / $0.25 in batch). Monitoring 2,000 APPS samples costs about $1.22 **[E]**. So the case for white-box monitoring cannot rest on cost. It has to rest on detection power at a low audit budget and on robustness: resistance to collusion, to steganography, and to jailbreaking the monitor.
4. **Method warning for the baseline.** Haiku 5.5 and Sonnet 5.5 are almost certainly stronger than Qwen3-32B. Using them as the "trusted" model reverses the usual control setup, where the trusted model T is weaker than the untrusted model U. Use weak trusted models for the real baseline: Llama-3.1-8B, gpt-4.1-nano, gpt-5-nano, gpt-oss-20b, or Qwen3-8B run locally. Use Haiku 5.5 and Sonnet 5.5 only as a "strong reference monitor" ceiling.
5. **Free resources can cover most of the $20 tier.**
   - Modal Starter gives $30/month of compute **[V]**, about 12 A100-80GB hours.
   - Kaggle offers 2×T4 at roughly 30 h/week **[V3]**.
   - NDIF hosts Llama-3.1-8B/70B/405B and GPT-OSS-120B internals for free **[V]**, but no Qwen.
   - Open SAEs and transcoders exist for Qwen3-8B, 14B and 32B on Hugging Face **[V]**.
6. **Do not try to replicate the essay's own scale.** The essay mentions 10B tokens searched for maximum activations (already-clean.txt line 1257). That would be about 920 H100-hours, roughly $2.5k–3.7k **[E]**. Its "100 million tokens through one Qwen3-32B neuron" histogram (line 877) is affordable: about 9 H100-hours, $25–37 **[E]**.

---

## 1. RunPod GPU prices: live read, 2026-10-15 [V]

Source: Runpod MCP `list-gpu-types`, read-only, called three ways: plain, with `include=AVAILABILITY, product=POD, cloud=COMMUNITY`, and with `cloud=SECURE`. Also cross-checked against https://docs.runpod.io/pods/pricing for storage.

| GPU | VRAM | Community $/hr | Secure $/hr | Serverless $/hr | Community stock now | Secure stock now |
|---|---|---|---|---|---|---|
| RTX 4090 | 24 GB | **0.34** | **0.89** | 1.10 | NONE | LOW (EU-RO-1 only) |
| RTX 5090 | 32 GB | 0.69 | 1.19 | 1.58 | NONE | LOW |
| A40 | 48 GB | **0.35** | **0.59** | 1.22 | NONE | LOW (CA-MTL-1, EU-SE-1) |
| RTX A6000 | 48 GB | 0.33 | 0.59 | 1.22 | NONE | LOW |
| L40S | 48 GB | **0.79** | **1.09** | 1.75 | LOW | NONE |
| A100 80GB PCIe | 80 GB | **1.19** | **1.79** | 2.72 | LOW | LOW (CA-MTL-3) |
| A100 80GB SXM | 80 GB | 1.39 | 1.79 | 2.72 | NONE | LOW (4 DCs) |
| H100 PCIe | 80 GB | 1.99 | 2.89 | 4.79 | NONE | NONE |
| H100 SXM | 80 GB | **2.69** | **3.99** | 4.79 | NONE | LOW (6 DCs) |
| H100 NVL | 94 GB | 2.59 | 3.19 | 4.79 | NONE | LOW |
| H200 SXM | 141 GB | **3.59** | **5.29** | 5.93 | NONE | LOW (EUR-IS-4/5) |
| RTX PRO 6000 Blackwell (Server) | 96 GB | 1.69 | 2.49 | 3.49 | NONE | LOW (7 DCs) |
| PRO 6000 MIG 1g.24gb | 24 GB | n/a | 0.69 | 0.69 | n/a | MEDIUM |

Observations:
- **Community cloud stock was mostly NONE at read time.** Budget at secure prices. Treat community prices as a bonus when stock appears.
- The RTX PRO 6000 (96 GB) is an interesting card for Qwen3-32B in bf16: 65.6 GB of weights leaves about 30 GB of headroom. Its secure price, $2.49, is above the A100's. I did not check its bf16 TFLOPS.
- Some secure-only GPUs show a placeholder community price of 0.5 (for example H200 NVL and MI300X). Those are not real offers.

**Storage [V]** (https://docs.runpod.io/pods/pricing): container disk costs $0.10/GB/mo while running and nothing when stopped. Volume disk costs $0.10/GB/mo running and $0.20/GB/mo stopped. Network volume costs $0.07/GB/mo under 1 TB and $0.05/GB/mo above. Quotes: "Pods are billed by the second for compute and storage, with no fees for data ingress or egress." "You must have at least one hour's worth of credits for your selected configuration to deploy an on-demand instance." "Pods are automatically stopped when your account balance reaches $0." The container disk is wiped on stop or restart (Runpod concept graph, rule `container-disk.what-survives`).

**Other GPU clouds for comparison [V]** (https://modal.com/pricing, per second). Modal: H200 $0.001261, H100 $0.001097, A100-80GB $0.000694, L40S $0.000542, L4 $0.000222, T4 $0.000164. That works out to $4.54, $3.95, $2.50, $1.95, $0.80 and $0.59 per hour **[E, ×3600]**. Starter plan: "$30 / month free credits", with "no monthly fee".

---

## 2. API prices for untrusted and trusted models [V]

Source: the public OpenRouter model list `https://openrouter.ai/api/v1/models`, downloaded with curl on 2026-10-15 (462 models), and the claude-api skill pricing table (cached 2026-10-06). Prices are $ per 1M tokens (input / output).

### Candidate untrusted models (open weights, so white-box access is possible)
| Model (OpenRouter id) | In | Out | Context (OR) | Notes |
|---|---|---|---|---|
| qwen/qwen3-32b | **0.08** | **0.28** | **40,960** (max completion 16,384) | The essay's dense model. The 40k context limits agent trajectories. |
| qwen/qwen3-14b | 0.12 | 0.24 | 40,960 | |
| qwen/qwen3.6-35b-a3b | **0.15** | **1.00** (cache read 0.05) | 262,144 | The essay's MoE model. 500 of the 1,000 neuron papers are about it. |
| qwen/qwen3-30b-a3b-instruct-2507 | 0.10 | 0.30 | 262,144 | |
| qwen/qwen3.5-9b | 0.10 | 0.15 | 262,144 | |
| **qwen/qwen3-8b** | **not listed** | | | You must generate it yourself, with vLLM on Kaggle T4s or on a 4090. |
| meta-llama/llama-3.1-8b-instruct | 0.05 | 0.08 | 131,072 | Also on NDIF for free (white-box). |
| meta-llama/llama-3.3-70b-instruct | 0.59 | 0.79 | 131,072 | |
| meta-llama/llama-3.1-70b-instruct | 0.40 | 0.40 | 131,072 | On NDIF for free (white-box). |
| openai/gpt-oss-20b | 0.018 | 0.09 | 131,072 | Goodfire has a hackathon SAE for it on HF. |
| openai/gpt-oss-120b | 0.15 | 0.60 | 131,072 | **On NDIF for free (white-box).** |
| deepseek/deepseek-v3.2 | 0.259 | 0.80 | 163,840 | Too large to self-host on this budget. |
| deepseek/deepseek-v4-flash | 0.091 | 0.182 | 1,048,576 | |

### Candidate trusted, black-box monitors
| Model | In | Out | Batch / cache |
|---|---|---|---|
| **Claude Haiku 5.5** (`claude-haiku-5-5`) | **0.10** | **0.50** | Batch 0.05/0.25. Cache read 0.01. **Prompts over 100K tokens cost 0.50/2.50.** Thinking is on by default at `medium` effort, and thinking tokens are billed as output. |
| **Claude Sonnet 5.5** (`claude-sonnet-5-5`) | **2.00** | **10.00** | Batch 1.00/5.00. Cache read 0.20. |
| Claude Opus 5.5 | 4.00 | 20.00 | Batch 2.00/10.00 |
| Claude Haiku 4.5 (older) | 1.00 | 5.00 | |
| openai/gpt-4.1-nano | 0.10 | 0.40 | Batch 0.05/0.20 |
| openai/gpt-4.1-mini | 0.40 | 1.60 | Batch 0.20/0.80 |
| openai/gpt-5-nano | 0.05 | 0.40 | |
| openai/gpt-5-mini | 0.25 | 2.00 | Batch 0.125/1.00 |
| google/gemini-2.5-flash-lite | 0.10 | 0.40 | |
| Free on OpenRouter (rate-limited): google/gemma-4-31b-it:free, gemma-4-26b-a4b-it:free, nvidia nemotron-3.x :free variants | 0 | 0 | Useful for prompt iteration. |

**OpenRouter fees [V3]** (truefoundry.com/blog/openrouter-pricing and others): there is "no markup on inference". Card purchases of credit carry a **5.5% fee with a $0.80 minimum**. A $5 top-up therefore loses 16% to the fee. Buy $10 or more at a time.

---

## 3. Model memory needs: VRAM and activation sizes

Architecture comes from the Hugging Face `config.json` files, read via the HF MCP **[V]**:
- Qwen3-8B: 36 layers, d_model 4096, d_mlp 12288. Vocab 151,936, untied embeddings.
- Qwen3-14B: 40 layers, d_model 5120, d_mlp 17408.
- Qwen3-32B: 64 layers, d_model 5120, d_mlp 25600, 64 query heads, 8 KV heads, head_dim 128. That gives **1,638,400 MLP neurons**, which matches the essay's "more than a million neurons" (line 1410).
- Qwen3.6-35B-A3B: 40 layers (3 linear-attention, then 1 full-attention, repeating), d_model 2048, 256 experts with 8 active, moe_intermediate 512, plus a vision tower.

Parameter counts are taken from the model cards: 8.2B, 14.8B, 32.8B **[R]**.

### Weights VRAM [E]
| Model | bf16 | int8 | nf4 (4-bit) | Smallest card for bf16 | Smallest card for 4-bit |
|---|---|---|---|---|---|
| Qwen3-8B | 16.4 GB | 8.6 GB | ~5.7 GB | 24 GB (4090 or A5000) | T4 16 GB or Colab |
| Qwen3-14B | 29.6 GB | 15.5 GB | ~9.3 GB | 48 GB (A40, L40S, A6000) | 24 GB |
| Qwen3-32B | **65.6 GB** | 34.4 GB | ~19.2 GB | **80 GB (A100 or H100)**, or 96 GB PRO 6000 | 24 GB (short contexts only) |
| Qwen3.6-35B-A3B | ~70 GB (35B total) | ~37 GB | ~20 GB | 80 GB | 24–48 GB |

The working-memory gotchas below are **[E]** from first principles:
- **Logits.** For a 4k-token chunk the fp32 logits are 4096 × 151,936 × 4 B ≈ 2.5 GB. Skip the LM head: call the base model, or stop at the last needed layer.
- **KV cache per token** (only needed if you chunk long sequences): 8B ≈ 147 KB, 14B ≈ 164 KB, 32B ≈ 262 KB. A 30k-token agent trajectory on 32B needs about 7.9 GB of KV.
- **Long trajectories on 32B do not fit on a 24 GB card even at 4-bit.** Use 48 GB with int8, or 80 GB with bf16.
- **4-bit changes activations.** Probes and neuron labels built on bf16 may not transfer to an nf4 model. The essay's neuron work was on the real model, so capture in bf16 when you plan to use its neuron papers.
- **T4 and P100 have no bf16.** On Kaggle you must run fp16. Check for inf or NaN, because Qwen models have large-magnitude outlier activations. This is a risk I have not verified for Qwen3.

### Activation storage per token, bf16 [E]
| Model | Residual, 1 layer | Residual, all layers | MLP neurons, 1 layer | MLP neurons, all layers |
|---|---|---|---|---|
| Qwen3-8B | 8.2 KB | 0.29 MB | 24.6 KB | 0.88 MB |
| Qwen3-14B | 10.2 KB | 0.41 MB | 34.8 KB | 1.39 MB |
| Qwen3-32B | 10.2 KB | 0.66 MB | 51.2 KB | **3.28 MB** |

What this means for storage choices:
- Storing every MLP neuron of Qwen3-32B for 9M tokens would take about 30 TB. **Never do this.**
- These options are fine:
  - (a) Keep about 5 residual layers per token for APPS: 9M tokens × 51 KB ≈ 460 GB. That is still too big, so keep only response tokens, or pool.
  - (b) **Pool on the GPU.** Store a per-sample mean and max for all 1.64M neurons: 2,000 samples × 1.64M × 2 B × 2 ≈ 13 GB.
  - (c) **Store only the 500 essay-labelled Qwen3-32B neurons** (from source/neuron-papers.json: 500 dense neurons across layers 0–63, plus 500 MoE neurons across layers 0–39). For every token that is 500 × 2 B × 9M ≈ 9 GB.
  - (d) Store one or two residual layers on response tokens only: about 10–20 GB.
- Storage cost is under $2/month on a network volume. The container disk is effectively free for a few hours.

---

## 4. Throughput and GPU-hours for activation capture [E]

Formula: tokens/s ≈ peak dense bf16 FLOPs × MFU / (2 × params). Peak TFLOPS **[R]**: RTX 4090 165 (FP32 accumulate), A40 150, L40S 362, A100 312, H100 SXM 989, H200 989, T4 65 (fp16).

MFU (the fraction of peak compute actually used) assumption: 0.30 for a Hugging Face forward pass with hooks, batched, no generation. The range is 0.15–0.45. H100 numbers are the least certain, because eager Hugging Face code often falls well below 30% MFU on an H100 without flash-attention or `torch.compile`. Attention cost is ignored. That is fine at 4k context but adds about 30–50% at 30k context.

| GPU | Qwen3-8B tok/s | Qwen3-14B tok/s | Qwen3-32B tok/s |
|---|---|---|---|
| RTX 4090 | ~3,000 | ~1,700 (int8 or 4-bit only) | ~750 (4-bit, short contexts only) |
| A40 / A6000 | ~2,700 | ~1,500 | ~700 (int8 only) |
| L40S | ~6,600 | ~3,700 | ~1,650 (int8 only) |
| A100 80GB | ~5,700 | ~3,200 | **~1,400** |
| H100 SXM | ~18,000 | ~10,000 | **~4,500** |
| Kaggle 2×T4 (fp16, pipelined) | ~1,000 | 4-bit only | 4-bit only, slow |

### Workload assumptions [E]
- **APPS setting:** 1,000 problems × (honest + attack) = 2,000 samples. Each sample is about 2.0k prompt tokens plus 2.5k output tokens (Qwen3 thinking adds a lot), so 4.5k tokens per sample and **9M capture tokens**. A "prompt-swap" ablation re-captures attack outputs under the honest system prompt, so the probe cannot just read the attack instruction. That doubles the total to 18M.
- **Agent setting:** 200 trajectories (100 honest, 100 attack), 20 steps each, 30k tokens at the end, about 15k average context per step. **6M capture tokens**, because one forward pass over the final transcript covers every step.

### Capture cost, with 1.5× slack on compute and setup overhead not included [E]
| Job | Model / GPU | GPU-h | Community $ | Secure $ |
|---|---|---|---|---|
| APPS, 9M tokens | Qwen3-8B / 4090 | 1.2 | 0.42 | 1.11 |
| APPS, 9M tokens | Qwen3-32B / A100 | 2.6 | 3.13 | 4.70 |
| APPS, 9M tokens | Qwen3-32B / H100 | 0.8 | 2.23 | 3.31 |
| APPS + ablation, 18M tokens | Qwen3-32B / A100 | 5.3 | 6.26 | 9.41 |
| Agent, 6M tokens | Qwen3-32B / A100 | 1.75 | 2.09 | 3.14 |
| Everything, 30M tokens | Qwen3-32B / A100 | 8.8 | 10.43 | 15.68 |
| Everything, 30M tokens | Qwen3-32B / H100 | 2.8 | 7.43 | 11.03 |
| Essay-scale: 100M tokens (line 877) | Qwen3-32B / H100 | 9.2 | 24.78 | 36.76 |
| Essay-scale: 10B tokens (line 1257) | Qwen3-32B / H100 | 921 | 2,478 | 3,676 |

**Fixed overhead per rented session [E]:**
- Pod start plus environment setup: 10–30 min.
- Downloading Qwen3-32B weights (about 65 GB): roughly 3–10 min at RunPod data-centre bandwidth. This is my guess, not measured.
- Hook and debug iteration: unbounded. **Plan 1–3 paid hours per session.** Develop on Qwen3-0.6B, 1.7B or 8B on free hardware first.

**Self-hosted generation vs. the API [V3 + E].** Third-party GPUStack benchmark: Qwen3-32B with vLLM on one H100 SXM reached about 2,353 total tok/s on ShareGPT with default settings (via markaicode.com). At that rate, the 9M APPS tokens take about 1.1 H100-hours ($3–4.4), versus $1.72 on OpenRouter. **Use the API for generation.** Caveat: OpenRouter providers may serve fp8 or int4 weights. You can pin full-precision providers through provider routing. Activations from teacher-forcing in bf16 are still exact for the text produced.

---

## 5. API cost of the monitoring and generation workloads [E, from §2 prices]

| Workload | Tokens in / out | Llama-3.1-8B | gpt-4.1-nano | gpt-5-nano | gpt-oss-20b | **Haiku 5.5** | Haiku 5.5 batch | **Sonnet 5.5** | Sonnet 5.5 batch |
|---|---|---|---|---|---|---|---|---|---|
| Monitor 2k APPS samples (2.1k in / 0.8k out each) | 4.2M / 1.6M | $0.34 | $1.06 | $0.85 | $0.22 | **$1.22** | $0.61 | **$24.40** | $12.20 |
| Monitor 200 agent trajectories, once at the end (30k / 1k) | 6M / 0.2M | $0.32 | $0.68 | $0.38 | $0.13 | $0.70 | $0.35 | $14.00 | $7.00 |
| Monitor every agent step (60M / 2M), no cache | 60M / 2M | $3.16 | $6.80 | $3.80 | $1.26 | $7.00 | $3.50 | $140 | $70 |
| Same, 80% cache-read hits (cache-write premium ignored) | 60M / 2M | $1.96 | n/a | n/a | n/a | $2.68 | n/a | $53.60 | n/a |

| Generation workload | Qwen3-32B | Qwen3.6-35B-A3B | Llama-3.1-8B | gpt-oss-120b |
|---|---|---|---|---|
| 2k APPS samples (2.0k in / 2.5k out) | **$1.72** | $5.60 | $0.60 | $3.60 |
| 200 agent trajectories (60M in / 2M out) | $5.36 (but the 40k context limit applies) | $11.00 ($6.20 with 80% cache hits) | $3.16 | $10.20 |

Rules of thumb:
- Haiku 5.5's billed output includes its thinking, which is on by default at `medium` effort. If it thinks for about 3k tokens per call, the APPS monitor cost rises to about $3. Set effort to `low` for monitors.
- Sonnet 5.5 per-step monitoring of agents ($50–140) is the single biggest cost risk. Run it on a subsample only.
- Best-of-n attack generation (as in the original control papers) multiplies the attack-side generation cost by n.

---

## 6. Free and near-free resources

| Resource | What you get | Status | Source |
|---|---|---|---|
| **Modal Starter** | $30/month of compute (GPU, CPU, memory), no monthly fee. That is about 12 h of A100-80GB or 7.6 h of H100. | **[V]** | https://modal.com/pricing |
| **Kaggle Notebooks** | P100 16 GB or 2×T4 (32 GB total). Commonly reported at about 30 GPU-h/week, though the number is not in Kaggle's docs. 12 h sessions. Linking Colab Pro or Pro+ adds 15 or 30 h/week. | **[V3]** | gpuperhour.com/blog/free-cloud-gpus-and-credits (dated 21 Sep 2026) |
| Google Colab free | Usually a T4, sessions of 12 h at most, limits not published | [V3] | same |
| Lightning AI free | 1 Studio, 4 h restarts, 50 GB storage | [V3] | same |
| HF ZeroGPU | 5 min/day free (40 min with PRO at $9/mo). For demos only. | [V3] | same |
| **NDIF (nnsight remote)** | "All models are free for research use — no GPU required on your end." Hosts Llama-3.1-8B/70B/405B and GPT-OSS-120B. **No Qwen3.** The account is at login.ndif.us. The status page was unreachable on 2026-10-15, and usage limits are not stated. | **[V]** | https://ndif.us, https://nnsight.net/status/ |
| **Open SAEs and transcoders on HF** | mwhanna/qwen3-{0.6b,1.7b,4b,8b,14b}-transcoders; adamkarvonen/qwen3-32b-saes; bcywinski/qwen3-32b-saes; AAIREPE/qwen3-32b-l36-batchtopk-sae; Goodfire/Llama-3.3-70B-Instruct-SAE-l50, Llama-3.1-8B-Instruct-SAE-l19, DeepSeek-R1-SAE-l37, Hackathon-gpt-oss-20b-SAE-l15 | **[V]** (HF MCP search) | huggingface.co |
| **Neuronpedia** | Hosts the Qwen3-4B transcoders (163,840 features per layer) with attribution graphs, free to browse. API terms are unknown (the doc page did not render). | [V3] | https://www.neuronpedia.org/qwen3-4b |
| **The essay's own 1,000 neuron papers** | 500 Qwen3-32B dense neurons (layers 0–63) and 500 Qwen3.6-35B-A3B MoE neurons (layers 0–39), each with a title, description, test scores and "near-miss" margins. **A ready-made set of interpretable features for monitoring.** | **[V]** | source/neuron-papers.json (keys `L`, `N`, `k`=d/m, `E`=expert) |
| Goodfire Silico / grants | Silico launched publicly on 4 Aug 2026 with a 50% early-signup discount and no free tier mentioned. "Grants for researchers working in critical fields such as AI safety". Amount and eligibility are not stated. | [V3] | mpost.io article, 6 Aug 2026 |
| Lambda Research Grant | Up to $5,000 in cloud credits, reviewed on a rolling basis. Announced Dec 2024. Status in 2026 not confirmed, and an academic affiliation is likely required. | [V3] | businesswire.com, 9 Dec 2024 |
| RunPod referral | A random $5–$500 bonus when you first load $10 or more (EU gets a fixed $5) | [V3] | gpuperhour.com |
| OpenRouter `:free` models | gemma-4-31b-it:free, nemotron-3.x :free and others, rate-limited | **[V]** | OR models API |
| Anthropic Fellows / OpenAI Safety Fellowship | Big compute (about $15k/mo per a third-party listing for Anthropic Fellows). Not a tiny-budget path, but the natural next step if results are good. | [V3] | grantedai.com, openai.com |
| Cloud trials | GCP $300 for 90 days (no GPUs on the trial). AWS $100–200 (select services). Azure $200 for 30 days. | [V3] | gpuperhour.com |

---

## 7. Three budget tiers, with line items [E]

Shared plan for every tier:
1. Develop the hooks and pipeline for free on Kaggle, Colab or Modal using Qwen3-0.6B, 1.7B or 8B.
2. Generate untrusted outputs on OpenRouter.
3. Rent one 80 GB GPU for a short, scripted capture run. Pool or select activations on the GPU.
4. Train probes on CPU, or on the same GPU in seconds.
5. Run black-box monitors in batch.

Report results as the safety vs. audit-budget curve (0.5–2%), plus the win/lose/continue game outcome from the control-evaluation framing.

### Tier A: $20 — "Is there a signal?" on APPS backdoors with Qwen3-32B as U
| Line item | Detail | $ |
|---|---|---|
| OpenRouter credit | One $10 top-up, so the 5.5% fee is $0.80 | 10.00 |
|  ↳ U = Qwen3-32B generation | 1,000 problems, honest + attack (best-of-2 on attack) ≈ 2.5k samples | ~2.20 |
|  ↳ Weak trusted monitors | Llama-3.1-8B + gpt-4.1-nano on 2k samples | ~1.40 |
|  ↳ Strong reference monitor | Haiku 5.5 batch, effort low, 2k samples | ~0.60–1.50 |
|  ↳ Slack for prompt iteration | | ~4 |
| GPU capture | **Modal free $30/month** (A100-80GB ≈ 12 h) **or** RunPod A100 secure ($1.79/hr × 5 h = $8.95) | 0–9 |
| Storage | Pooled features plus the 500 essay neurons, about 20 GB, kept on the container disk for hours or downloaded | <0.50 |
| Buffer | | ~1 |
| **Total** | | **$11–20** |

What you get: per-sample probe scores (a linear probe on residuals, plus monitors built from the 500 labelled neurons) against weak and strong black-box monitors, with AUROC and safety at a 1% audit budget, one seed. You will not get the prompt-swap ablation (unless Modal credit allows it), agent settings, or an adaptive attacker.

### Tier B: $50 — APPS plus an agent setting, with ablations
| Line item | Detail | $ |
|---|---|---|
| OpenRouter credit | $25 top-up | 25.00 |
|  ↳ Tier A generation and monitors | | ~5 |
|  ↳ Agent U = Qwen3.6-35B-A3B (262k context, MoE, also covered by the essay's neuron papers) | 200 trajectories, using prefix caching | ~6–11 |
|  ↳ Agent monitors | Haiku 5.5 per step with caching (~$2.7) + weak model per step (~$2–3) + Sonnet 5.5 batch at the end of each trajectory (~$7) | ~12 |
| GPU | RunPod A100 secure, about 12 h = $21.50, and/or Modal's free $30. Covers the 30M-token capture, the prompt-swap ablation, and the MoE capture (HF MoE code is slow, so budget 2× more). | 10–22 |
| Storage | 50 GB network volume for 1 month ($3.50), to cache weights and activations | 3.50 |
| Buffer | | ~4 |
| **Total** | | **$45–50** |

What you get: two settings, the confound ablation (does the probe read intent or just the system prompt?), per-step agent monitoring, and a comparison against a Sonnet-class reference on a subsample.

### Tier C: $100 — robustness: can the attacker beat the probe?
| Line item | Detail | $ |
|---|---|---|
| Everything in Tier B | | ~45 |
| Probe-aware red team | Prompted obfuscation attacks: extra generation and monitoring | ~8 |
| LoRA "model organism" | Fine-tune Qwen3-8B or 14B to insert backdoors without being told to, which removes the prompt confound. QLoRA on a 48 GB A40 secure at $0.59/hr × 6 h = $3.54, or an L40S. Include data-generation calls. | ~8 |
| Seeds and confidence intervals | Re-run capture with 3 seeds and bootstrap: about 6 more A100-hours | ~11 |
| Optional essay-style replication | 100M tokens through Qwen3-32B for neuron statistics (H100 community about $25, secure about $37). **Pick this or the LoRA plus seeds; both will not fit.** | (25–37) |
| Storage | 100 GB network volume for 1 month | 7.00 |
| Buffer | | ~10–20 |
| **Total** | | **$90–100** |

What you get: the minimum evidence a skeptical control researcher would want. That means the white-box monitor beats a matched-capability black-box monitor at a low audit budget, survives the confound ablation, and survives at least a prompted adaptive attacker, with error bars.

---

## 8. Key cost traps
1. **Idle pods.** A forgotten H100 secure pod costs $3.99/hr, about $96/day. Script the stop with `runpodctl stop pod` or a self-terminate at the end of the job. Pods also auto-stop when the balance reaches $0 [V].
2. **The volume disk bills $0.20/GB/mo while stopped** [V]. Delete it after use.
3. **Community stock was NONE** for most cards at read time [V]. Budget at secure prices.
4. **Qwen3-32B on OpenRouter caps context at 40,960 tokens** [V], which truncates long agent runs. Use Qwen3.6-35B-A3B (262k) instead.
5. **Haiku 5.5 has a long-prompt price jump**: prompts over 100K tokens are billed at $0.50/$2.50 [V]. Keep per-step monitor prompts below 100K.
6. **Small top-ups lose money to OpenRouter's $0.80 minimum fee** [V3].
7. **Do not store all-layer, all-token activations of a 32B model.** At 3.3 MB per token, 9M tokens is about 30 TB [E].
8. **4-bit or fp16 capture can drift from the bf16 activations** behind the essay's neuron labels [E/R].

## 9. Uncertainties and open checks
- I recalled the GPU TFLOPS figures and did not re-fetch them. MFU for Hugging Face plus hooks is a guess (0.15–0.45). Run a 10-minute benchmark on the rented card before committing.
- Token counts per APPS sample (about 4.5k with thinking) and per agent trajectory (about 30k) are assumptions. Another scout's benchmark data should replace them.
- NDIF's current model list and quotas could not be confirmed, because the status page was down. Its homepage lists Llama-3.1 and GPT-OSS-120B but not Qwen.
- Neuronpedia API terms and Goodfire grant details are unknown.
- The Kaggle weekly quota is user-reported, not documented.
- OpenRouter routing may serve quantized weights for "Qwen3-32B" generation.
- MoE capture throughput in Hugging Face Transformers for Qwen3.6-35B-A3B (with linear attention and a vision tower) is unknown and could be much slower than the dense estimate.
- The availability snapshot is from one moment (2026-10-15, about 10:50 local) and changes minute to minute.
