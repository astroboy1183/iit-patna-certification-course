# Issues and fixes: LoRA fine-tuning project

A log of every problem hit while setting up this project and getting `script1_baseline_chat.py` and `script2_lora_finetune.py` to run on a laptop (Linux Mint 22.3, 16 CPU threads, 15 GB RAM, **no NVIDIA GPU**). Most of them came from running the instructor's 2024 setup on a newer Python and on CPU instead of GPU.

## Summary

| # | Where | Symptom | Cause | Status |
|---|---|---|---|---|
| 1 | venv | venv was Python 3.12.3, not 3.13 | `python3` resolved to the system Python | ✅ Fixed |
| 2 | venv | `template.py` saved inside `.venv/` | File created in the wrong folder | ✅ Fixed |
| 3 | `pip install` | `No matching distribution found for torch==2.2.2` | 2024 pins have no wheels for Python 3.13 | ✅ Fixed (Python 3.11) |
| 4 | `pip install` | Multi-GB download of CUDA libraries | Default `torch` on Linux is the GPU build | ✅ Fixed (CPU index) |
| 5 | Script 1 | `401 Unauthorized` / `not a valid model identifier` | Typo in model name: `microsodt` | ✅ Fixed |
| 6 | Script 2 | `SyntaxError: keyword argument repeated: padding` | `padding=` passed twice | ✅ Fixed |
| 7 | Script 2 | `pyarrow requires NumPy 2.0 or newer, found 1.26.4` | Unpinned `pyarrow` installed a NumPy-2-only release | ✅ Fixed (pinned) |
| 8 | Script 2 | `KeyError: 'Instruction'` (latent) | Code used `Instruction`/`Output`, data uses lowercase | ✅ Fixed |
| 9 | Script 2 | `ArrowInvalid: ... expected length 2 but got length 128` | `batched=True` with a one-row-at-a-time function | ✅ Fixed |
| 10 | Script 2 | `"LayerNormKernelImpl" not implemented for 'Half'` | `float16` model on CPU | ✅ Fixed |
| 11 | Script 2 | No error, but attention layers not trained | LoRA `target_modules` names don't exist in phi-1.5 | ⚠️ Open |
| 12 | Script 2 (QLoRA) | Can't run on this machine | 4-bit `bitsandbytes` needs an NVIDIA GPU | ℹ️ Use Colab/Kaggle |

---

## Environment setup

### 1. The venv was built with Python 3.12.3 instead of 3.13

**Symptom:** inside the venv, `python --version` showed `3.12.3`.

**Cause:** the machine has two Pythons. `/usr/bin/python3` is Linux Mint's own system Python (3.12.3), and `/usr/local/bin/python3.13` is a separately installed 3.13.5. The venv was created with `python3 -m venv`, and `python3` resolved to the system one. A venv always uses the Python that created it. `.venv/pyvenv.cfg` records it:
```
executable = /usr/bin/python3.12
command    = /usr/bin/python3 -m venv --prompt="finetuning" ...
```

**Fix:** name the Python version explicitly when creating a venv, e.g. `python3.13 -m venv .venv`, instead of relying on whatever `python3` points to.

### 2. `template.py` was saved inside `.venv/`

**Symptom:** the project-structure script lived at `.venv/template.py`.

**Why it matters:** Python 3.13 venvs contain a `.gitignore` with `*`, so nothing inside `.venv/` is committed, and rebuilding the venv (`rm -rf .venv`) deletes it.

**Fix:** keep project files in the project folder. In VS Code, select the project folder (not `.venv`) in the Explorer before creating a new file.

### 3. `pip install -r requirements.txt` failed: `No matching distribution found for torch==2.2.2`

**Symptom:**
```
ERROR: Could not find a version that satisfies the requirement torch==2.2.2
(from versions: 2.5.0, 2.5.1, ...)
```

**Cause:** not a deprecated package; a **Python version mismatch**. pip installs prebuilt wheels, each built for specific Python versions. `requirements.txt` is from early 2024, before Python 3.13 existed (Oct 2024). It worked for the instructor on an older Python. Checking PyPI showed four pins with no Python 3.13 wheels:

| Package | Pinned | Has wheels up to | First version with 3.13 wheels |
|---|---|---|---|
| `torch` | 2.2.2 | Python 3.12 | 2.5.0 |
| `numpy` | 1.26.4 | Python 3.12 | 2.1.0 |
| `pandas` | 2.2.2 | Python 3.12 | 2.2.3 |
| `sentencepiece` | 0.1.99 | **Python 3.11** | 0.2.1 |

`sentencepiece` 0.1.99 has no wheel even for 3.12, so the system Python wouldn't have worked either.

**Options considered:**
- **Stay on 3.13 and bump those four pins** (`torch==2.5.1`, `numpy==2.1.3`, `pandas==2.2.3`, `sentencepiece==0.2.1`). Tested in a throwaway venv: all packages import and a real LoRA training step runs.
- **Match the instructor with Python 3.11** and keep `requirements.txt` unchanged. ✅ **Chosen**, to keep versions identical to the course.

**Fix (Python 3.11 via `uv`, no sudo, system Python untouched):**
```bash
uv python install 3.11
rm -rf .venv
uv venv .venv --python 3.11 --prompt finetuning --seed   # --seed puts pip in the venv
source .venv/bin/activate
python --version                                         # Python 3.11.16
```

### 4. The default `torch` install downloads ~2–3 GB of CUDA libraries

**Cause:** on Linux, the `torch` wheel on PyPI is the **GPU (CUDA) build** and pulls in about a dozen `nvidia-*` packages. This laptop has no NVIDIA GPU, so they'd never be used.

**Fix:** install the CPU build from PyTorch's own index. `requirements.txt` stays the same; only the command changes:
```bash
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"   # 2.2.2+cpu False
```
On a GPU machine (Colab, Kaggle), use the plain `pip install -r requirements.txt` instead.

---

## `script1_baseline_chat.py`

### 5. `401 Client Error: Unauthorized` / `microsodt/phi-1_5 is not a valid model identifier`

**Symptom:**
```
RepositoryNotFoundError: 401 Client Error ...
Repository Not Found for url: https://huggingface.co/microsodt/phi-1_5/...
OSError: microsodt/phi-1_5 is not a local folder and is not a valid model identifier
```

**Cause:** a typo in the model name: `microsodt` instead of `microsoft`.

**Why it says "Unauthorized":** Hugging Face deliberately returns the same 401 for a model that doesn't exist and one that's private, so private model names can't be guessed. When you see `401 ... Repository Not Found`, **check the spelling before logging in**.

**Fix:**
```python
BASE_MODEL = "microsoft/phi-1_5"
```
`microsoft/phi-1_5` is public; no token needed. The first run downloads about 2.8 GB to `~/.cache/huggingface/`.

---

## `script2_lora_finetune.py`

### 6. `SyntaxError: keyword argument repeated: padding`

**Cause:** `padding="max_length"` appeared twice in the same `tokenizer(...)` call. Python rejects the whole file before running anything.

**Fix:** keep one:
```python
tokens = tokenizer(prompt, padding="max_length", truncation=True, max_length=MAX_LENGTH)
```

### 7. `ImportError: pyarrow requires NumPy 2.0 or newer, found 1.26.4`

**Cause:** `datasets` depends on `pyarrow`, which wasn't pinned in `requirements.txt`, so pip installed the newest release, **26.0.0**. That's the first `pyarrow` that requires NumPy 2, but `requirements.txt` pins `numpy==1.26.4`. pip didn't catch the clash because `pyarrow` doesn't declare its NumPy requirement on PyPI; it only fails at import. The instructor installed in 2024, when the newest `pyarrow` still supported NumPy 1.

**Investigation:** tested with `numpy==1.26.4` in throwaway Python 3.11 venvs:
- `pyarrow` 21.0.0, 23.0.1, 24.0.0 and 25.0.1 import fine.
- `pyarrow` 26.0.0 fails with this exact error.
- `datasets==2.19.0` + `pyarrow==25.0.1` loads `data/train.jsonl` and `.map()` works.

**Fix:** pin it in `requirements.txt`:
```
pyarrow==25.0.1
```

**Lesson:** pinned top-level packages don't freeze their dependencies. After a working install, `pip freeze > requirements.lock` captures every version.

### 8. Column names didn't match the data (`'Instruction'` vs `'instruction'`)

**Cause:** the prompt read `example['Instruction']` and `example['Output']`, but `data/train.jsonl` uses lowercase keys (`instruction`, `output`). Python dictionary keys are case-sensitive, so this is a `KeyError` waiting to happen. Spotted while reviewing the script.

**Fix:**
```python
prompt = f"Instruction: {example['instruction']}\n Response: {example['output']}"
```

### 9. `ArrowInvalid: Column 2 named input_ids expected length 2 but got length 128`

**Cause:** `dataset.map(tokenize, batched=True, ...)` passes the function **several rows at once**, so `example['instruction']` is a *list*. `tokenize` was written for **one row**:
1. The f-string pasted both lists into one prompt string.
2. The tokenizer returned one sequence of 128 tokens (`MAX_LENGTH`).
3. `datasets` sent in 2 rows (the 2 training examples) and expected 2 results, but got a flat list of 128 numbers.

**Fix:** drop `batched=True` so `tokenize` is called once per row:
```python
tokenized = dataset.map(tokenize, fn_kwargs={"tokenizer": tokenizer})
```
(Alternative: keep `batched=True` and make `tokenize` build one prompt per row with a list comprehension. Only worth it for large datasets.)

### 10. `RuntimeError: "LayerNormKernelImpl" not implemented for 'Half'`

**Cause:** the model was loaded with `torch_dtype=torch.float16`. Half precision is a **GPU** format; on CPU, PyTorch 2.2 doesn't implement every operation for it, and LayerNorm is the first one phi-1.5 hits. Loading and applying LoRA worked; it crashed at the first training step. It works for the instructor on a GPU.

**Fix:** full precision on CPU:
```python
model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.float32)
```
Costs about 5.7 GB of RAM instead of about 2.8 GB. For code that runs on both CPU and GPU:
```python
dtype = torch.float16 if torch.cuda.is_available() else torch.float32
```
Keep `fp16=False` and `bf16=False` in `TrainingArguments` on CPU.

### 11. ⚠️ Open: LoRA only trained the feed-forward layers

**Symptom:** no error. But the saved adapter has LoRA weights only for `fc1` and `fc2` (96 tensors across 24 layers), none for attention.

**Cause:** `target_modules=["Wqkv", "out_proj", "fc1", "fc2"]`. `Wqkv` and `out_proj` are layer names from an older phi-1.5 implementation. In `transformers` 4.39.3, phi-1.5's attention layers are `q_proj`, `k_proj`, `v_proj` and `dense`. PEFT doesn't warn about names that don't match as long as at least one does (`fc1`/`fc2`).

**Fix (if script 3 shows the model didn't learn the facts well):**
```python
target_modules=["q_proj", "k_proj", "v_proj", "dense", "fc1", "fc2"]
```
To list a model's layer names: `print([n for n, _ in model.named_modules()])`.

### 12. ℹ️ QLoRA (`script2_qlora_finetune.py`) needs a GPU

4-bit loading with `bitsandbytes` 0.43.1 requires an NVIDIA GPU; the CPU build prints `compiled without GPU support`. GitHub Codespaces is no option either: its GPU machine type was retired in August 2025, and every Codespaces machine is now CPU-only. **Use Google Colab (free T4 GPU) or Kaggle Notebooks** for the QLoRA script, with the plain `pip install -r requirements.txt` (no CPU index).

---

## The successful run

`script2_lora_finetune.py` completed on 17 Oct 2026, after 6 attempts over about 28 minutes:

| Started | Outcome |
|---|---|
| 18:47:06 | ❌ `SyntaxError` (duplicate `padding`), most likely |
| 18:48:17 | ❌ `pyarrow requires NumPy 2.0` (`pyarrow==25.0.1` installed at 18:52) |
| 18:53:19 | ❌ `batched=True` length mismatch |
| 18:54:17 | ❌ Failed before tokenizing finished |
| 19:11:59 | ❌ Tokenized OK, then `LayerNormKernelImpl ... 'Half'` |
| 19:14:41 | ✅ **Completed** |

| Successful run | |
|---|---|
| Total time | **≈ 7 min** (19:14:41 → 19:21:42) |
| Training | 40 steps in ≈ 6 min 50 s, about **10 s per step** on CPU |
| Base model | `microsoft/phi-1_5`, 1.42B parameters, `float32` |
| LoRA | `r=8`, `lora_alpha=128`, dropout 0.05 |
| Trainable parameters | 3,932,160 (0.28% of the model) |
| Data | 2 examples, max 128 tokens |
| Settings | 40 epochs, batch size 1, gradient accumulation 4, learning rate 2e-4 |
| Output | `models/adapters/lora_adapt/adapter_model.safetensors` (15.7 MB) |

Timings come from bash history timestamps, the `datasets` cache and the adapter files' save times. Loss values weren't saved; add `trainer.save_state()` after `trainer.train()` to record them in `trainer_state.json`.

---

## Checklist for next time

- Create venvs with an explicit version (`python3.11 -m venv` or `uv venv --python 3.11`), and check `python --version` before installing.
- Match the Python version the `requirements.txt` was written for, or update the pins.
- On a machine without an NVIDIA GPU: install `torch` from the CPU index and load models in `float32`.
- A Hugging Face 401 or "not a valid model identifier" usually means a typo in the model name.
- Pin indirect dependencies that cause trouble (here `pyarrow`), or keep a `pip freeze` lock file.
- Check that a `map()` function matches `batched=`, and that dictionary keys match the data's column names.
- Check that LoRA `target_modules` exist in the model: `model.named_modules()`.
- Run QLoRA on a GPU machine (Colab or Kaggle).
