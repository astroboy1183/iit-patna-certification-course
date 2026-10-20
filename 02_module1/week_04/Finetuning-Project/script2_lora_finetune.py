import warnings

import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

warnings.filterwarnings("ignore")

# ---Config---
BASE_MODEL = "microsoft/phi-1_5"
DATA_PATH = "data/train.jsonl"
OUTPUT_DIR = "models/adapters/lora_adapt"

BATCH_SIZE = 1
GRAD_ACCUM = 4
EPOCHS = 40
LR = 2e-4
MAX_LENGTH = 128


def load_training_dataset():
    return load_dataset("json", data_files=DATA_PATH)


def tokenize(example, tokenizer):
    prompt = f"Instruction: {example['instruction']}\n Response: {example['output']}"
    tokens = tokenizer(
        prompt, padding="max_length", truncation=True, max_length=MAX_LENGTH
    )
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens


def main():
    print("\n===== Loading Base Model on the CPU =====")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.float32)

    print("\n===== Loading Training Data =====")
    dataset = load_training_dataset()

    print("\n===== Tokenizing Training Data =====")
    tokenized = dataset.map(tokenize, fn_kwargs={"tokenizer": tokenizer})

    print("\n===== Applying LoRA =====")
    lora_config = LoraConfig(
        r=8,
        lora_alpha=128,
        target_modules=["Wqkv", "out_proj", "fc1", "fc2"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # ----Training

    print("\n===== Starting Training =====")
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM,
        num_train_epochs=EPOCHS,
        learning_rate=LR,
        optim="adamw_torch",
        logging_steps=10,
        save_strategy="no",
        fp16=False,
        bf16=False,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
    )

    trainer.train()

    print("\n===== Saving LoRA Adapter =====")
    model.save_pretrained(OUTPUT_DIR)

    print("\n===== LoRA Finetuning Complete =====")
    print(f"Output saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
