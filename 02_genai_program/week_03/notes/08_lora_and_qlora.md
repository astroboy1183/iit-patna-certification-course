# Lecture 8 · Lightweight fine-tuning: LoRA and QLoRA (Week 3)

## Part 1 · The idea, without the maths

### The problem: full fine-tuning is expensive

Customizing a large model (e.g. LLaMA-13B) by fully fine-tuning it means updating **billions of parameters**:
- big GPU clusters (think 8× A100),
- high electricity and carbon cost,
- days to weeks of training.

For most developers that's unaffordable. We need a cheaper way.

### LoRA: Low-Rank Adaptation

> "Don't rewrite the textbook. **Freeze the book and add sticky notes** with your changes."

In AI terms:
1. **Freeze** the original model weights (don't update them).
2. **Add small adapter matrices** next to some layers.
3. **Train only the adapters.**

**What you get**
- Much less memory, much faster training.
- The base model's knowledge is **preserved** (it isn't changed).

**Example:** base model = knows English and world knowledge → LoRA fine-tune = polite customer-support replies → result: a fast, cheap, specialized chatbot without retraining everything.

**Benefits**
| | |
|---|---|
| **Speed** | Hours instead of weeks |
| **Cost** | A single GPU is often enough; small models can even be tuned on a laptop or a free Colab GPU |
| **Flexibility** | Swap adapters like plugins: support bot, legal bot, medical bot |
| **Reusability** | Many fine-tunes share one base model; each adapter is only megabytes |

### QLoRA: Quantized LoRA

LoRA trains few parameters, but you still have to **load the whole base model** into GPU memory, and big models are heavy.

> **Correction to the slide:** the slide says LLaMA-65B needs 350 GB just to load. Loading 65 billion weights in 16-bit takes about **130 GB** (65B × 2 bytes). The much bigger number applies to **full fine-tuning** in 16-bit, which the QLoRA paper puts at over 780 GB because gradients and optimizer state also need memory.

**QLoRA**
1. **Quantize** the base model: store each weight in **4 bits** instead of 16, which cuts the weights' memory by about 4×.
2. Train **LoRA adapters** on top, as usual.
3. A 65B model now fits on **one 48 GB GPU** (≈ 33 GB of 4-bit weights plus room for training). Smaller models (up to ~33B) fit on a 24 GB consumer GPU.

> **Correction to the slide:** one slide says a 65B model fits on a 24 GB GPU and another says 48 GB. The QLoRA paper's figure is **48 GB** for 65B.

**Analogy: carrying books**
| | |
|---|---|
| Full model | A 10 kg stack of books |
| LoRA | Sticky notes added, but you still carry all 10 kg |
| QLoRA | Books compressed into a light e-reader, plus sticky notes |

### Why they matter

They **democratize fine-tuning**: startups, indie developers and hobbyists can customize large open models on one GPU. That's why the QLoRA paper (2023) made such an impact.

## Part 2 · The technical view

### Normal fine-tuning

A layer has a weight matrix **W** of size **d × k**. Fine-tuning adjusts **every** element of W. If W (across the model) has billions of values, you update billions, which is expensive in memory and compute.

### The LoRA trick: low-rank decomposition

Instead of updating W:
1. **Freeze W.**
2. Learn an update **ΔW**, but never store it as a full d × k matrix.
3. Store it as the product of two "skinny" matrices:

```
ΔW = A × B        A: (d × r)    B: (r × k)    with r ≪ d, k   (r is typically 4–64, e.g. 8 or 16)
W' = W + ΔW       (at inference: y = W·x + A·B·x, or merge ΔW into W once)
```

`r` is the **rank**. It controls how much the adapter can learn: a higher r means more capacity but more parameters.

> Implementation detail (from the LoRA paper): one of the two matrices starts at **zero**, so ΔW = 0 at the start and training begins from exactly the base model. The update is also scaled by a factor **α / r** (`lora_alpha` in code).

### How much it saves

Using the slide's example, d = k = 10,000 and r = 8:

| | Trainable values |
|---|---|
| Full ΔW (d × k) | 100,000,000 |
| A (d × r) | 80,000 |
| B (r × k) | 80,000 |
| **LoRA total** | **160,000** |

That's **625× fewer** trainable values for this matrix, which the slide rounds to ">500×". Across a whole model, LoRA typically trains well under 1% of the parameters.

### Why low-rank works (intuition)

- Large weight matrices contain a lot of **redundancy**.
- LoRA assumes the **change** needed for a new task lives in a much **smaller space** than the full matrix.
- Like **JPEG** compression: drop the small details, keep the important patterns.
- Training just that small subspace gets most of the benefit at a fraction of the cost.

### QLoRA: adding quantization

- **Quantization** = storing each weight with fewer bits, e.g. an approximate 4-bit value instead of `0.123456` in float32.
- Memory for weights shrinks **4×** from 16-bit, or **8×** from 32-bit.
- The LoRA adapters themselves stay in higher precision and are what gets trained.

What QLoRA actually uses (the slide's "bnb.int4"):
| Technique | What it does |
|---|---|
| **NF4 (4-bit NormalFloat)** | A 4-bit format designed for normally distributed neural-network weights, loaded with the **bitsandbytes** library |
| **Double quantization** | Also quantizes the scaling constants to save a bit more memory |
| **Paged optimizers** | Move optimizer state between GPU and CPU memory to avoid out-of-memory spikes |

**Result:** 65B models fine-tuned on a single 48 GB GPU, with quality close to 16-bit fine-tuning on the paper's benchmarks.

### Visual analogy

| | |
|---|---|
| **Full fine-tune** | Edit every word in a 10,000-page encyclopedia |
| **LoRA** | Add small sticky-note addendums |
| **QLoRA** | Compress the encyclopedia into an e-book, then add sticky notes |

## Full fine-tuning vs LoRA vs QLoRA

The slide deck promised this comparison table but doesn't include it, so here it is:

| | Full fine-tuning | LoRA | QLoRA |
|---|---|---|---|
| Weights trained | All | Small adapters only (often < 1%) | Small adapters only |
| Base model during training | 16/32-bit, trainable | 16-bit, frozen | **4-bit**, frozen |
| GPU memory | Highest (weights + gradients + optimizer state for everything) | Much lower | Lowest |
| Typical hardware | Multi-GPU cluster | A single GPU (or more for big models) | A single GPU, even for very large models |
| Quality | Best | Close to full fine-tuning on most tasks | Close to LoRA / 16-bit |
| Output | A whole new model copy | A small adapter file (MBs) | A small adapter file (MBs) |
| Best for | Big labs, large datasets | Domain apps (medical chatbot, legal assistant) | Large models on modest hardware; researchers and startups |

## In code (for reference)

LoRA and QLoRA are usually done with Hugging Face's **`peft`** library, with **`bitsandbytes`** for 4-bit loading. The shape of a QLoRA setup:

```python
# Reference only: needs transformers, peft, bitsandbytes and a CUDA GPU.
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model

bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")    # QLoRA: 4-bit NF4 base model
model = AutoModelForCausalLM.from_pretrained("<base-model-id>", quantization_config=bnb)

lora = LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"], task_type="CAUSAL_LM")
model = get_peft_model(model, lora)
model.print_trainable_parameters()   # typically well under 1% of all parameters
```

For plain LoRA, load the model in 16-bit and drop the `quantization_config`.

## Trade-offs and use cases

- **Full fine-tuning:** best accuracy, but impractical except for big labs.
- **LoRA:** a great balance of efficiency and quality; best for domain-specific apps (medical chatbot, legal assistant).
- **QLoRA:** brings giant models within reach of modest hardware; best for researchers and startups.

## Key takeaways

- LoRA = **freeze the model, train small adapters** (ΔW = A × B with a small rank r).
- QLoRA = **LoRA on a 4-bit quantized base model**, so very large models fit on one GPU.
- Both make fine-tuning affordable and keep the base model reusable: one base, many swappable adapters.

## Check yourself

1. Explain LoRA in one sentence using the sticky-note analogy, then in one sentence using matrices.
2. For d = 4,096, k = 4,096 and r = 16, how many trainable values does LoRA add to that matrix, compared with 16.8 million for full ΔW? (Answer: 131,072, about 128× fewer.)
3. LoRA already trains few parameters. Why is QLoRA still needed?
4. What does the rank r control? What happens if it's too small or too large?
5. Why can one base model serve a legal bot and a medical bot at the same time?
