import os
import warnings

import jsonlines
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

warnings.filterwarnings("ignore")

DATA_DIR = "data"
EVAL_FILE = os.path.join(DATA_DIR, "eval_questions.jsonl")

BASE_MODEL = "microsoft/phi-1_5"


def load_eval_questions():
    questions = []
    with jsonlines.open(EVAL_FILE, "r") as reader:
        for obj in reader:
            questions.append(obj["question"])
    return questions


def chat(model, tokenizer, questions):
    prompt = f"Questions: {questions}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=80,
            do_sample=False,
            temperature=0.2,
            pad_token_id=tokenizer.eos_token_id,
        )

    decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return decoded


def run_baseline_evaluation():
    print("\nLoading base model....(CPU may take some time)")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

    questions = load_eval_questions()

    for q in questions:
        print(f"Question to the model -> {q}")
        answer = chat(model, tokenizer, q)
        print(f"Model's answer -> {answer}")
        print("*" * 50)


if __name__ == "__main__":
    run_baseline_evaluation()
