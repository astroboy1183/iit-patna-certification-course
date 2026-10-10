# Lecture 7 · Prompt tuning vs fine-tuning basics (Week 3)

## The problem

General LLMs (GPT, Gemini, LLaMA) can do many tasks, but real applications need them to behave in **specific** ways: answer medical questions, summarize financial reports, power a support chatbot.

There are two main ways to **adapt** a general model:

| Strategy | Idea | Changes the model's weights? |
|---|---|---|
| **Prompt tuning** | Guide the model with clever instructions | ❌ No |
| **Fine-tuning** | Retrain the model on task-specific data | ✅ Yes |

> **Terminology note:** in this course, "prompt tuning" means **prompt engineering**: writing better instructions and examples. In research papers, "prompt tuning" usually means something else: learning a small set of trainable "soft prompt" vectors while the model stays frozen, which makes it a PEFT method (see below). Expect either meaning in interviews, and say which one you mean.

## Prompt tuning (prompt engineering)

Guide the model with natural-language instructions, **without changing its weights**.

- **Zero-shot:** just ask.
  > Translate this sentence into French: I love learning.
- **Few-shot:** show a few examples first, so the model picks up the pattern.
  > English: Hello → French: Bonjour | English: Thank you → French: Merci | English: Good night → French:

| ✅ Advantages | ⚠️ Limitations |
|---|---|
| Very cheap and fast: no training | Can be **inconsistent**: rewording the prompt changes the result |
| Anyone can do it: it's just text | Less reliable on its own for high-stakes production use |
| Great for rapid prototyping | Limited by the context window and per-call token cost |

In practice, production apps reduce the inconsistency with structure around the prompt: fixed templates, low temperature, output schemas and validation. My live-session notebook does this with `PromptTemplate` + Pydantic output parsers (`../../live_sessions/01_call_transcript_qa/experiment.ipynb`).

## Fine-tuning

Actually **updates the model's parameters**, using a labelled dataset for the target task.

| Type | What's trained | Cost |
|---|---|---|
| **Full fine-tuning** | All of the model's weights | Very expensive; often impractical for large models |
| **Parameter-efficient fine-tuning (PEFT)** | A small number of extra or selected weights (e.g. **LoRA**, adapters); most weights stay frozen | Much cheaper (Lecture 8) |

| ✅ Advantages | ⚠️ Limitations |
|---|---|
| More **consistent and reliable** on the target task | Needs a good amount of **high-quality task data** |
| Learns domain style, format and terminology (legal, healthcare, insurance) | **Computationally expensive** (GPUs/TPUs) |
| Suits long-term production systems | Risk of **overfitting** and **catastrophic forgetting** |

- **Overfitting:** the model memorizes the training examples and does worse on new inputs.
- **Catastrophic forgetting:** while learning the new task, the model loses general abilities it had before.

> **Fine-tuning vs RAG:** fine-tuning is best for teaching **behaviour** (tone, format, a narrow task). For **facts that change** (prices, policies, documents), retrieval (RAG, Module 5) is usually better: you update the documents, not the model.

## Side by side

| Aspect | Prompt tuning | Fine-tuning |
|---|---|---|
| Effort | Write instructions (low) | Prepare a dataset + compute (high) |
| Cost | Very low | Higher (GPUs/TPUs + training time) |
| Flexibility | Change anytime: just edit the prompt | Behaviour fixed after training; retrain to change |
| Consistency | Can vary with wording | Stable for repeated use |
| Best for | Prototyping, quick tasks, exploration | Production apps, domain-specific tasks |

## When to use what

**Prompt tuning if…**
- you're experimenting or testing an idea quickly;
- you don't have domain-specific data;
- cost and speed matter more than precision.

**Fine-tuning if…**
- the app needs consistent, repeatable results;
- you have enough high-quality labelled data;
- you're in a specialized field (legal, insurance, medical);
- the model must deeply match your brand or domain style.

A practical order of attack: **prompting first → add RAG if it needs your data → fine-tune only if behaviour is still not good enough.**

## Looking ahead

- Advanced prompting: chain-of-thought, RAG.
- Fine-tuning techniques in detail: LoRA, adapters, PEFT (Lecture 8).

> **Takeaway:** prompt tuning is your baby step; fine-tuning is the professional toolkit.

## Check yourself

1. What's the difference between zero-shot and few-shot prompting? Write a few-shot prompt for classifying support tickets.
2. Why can prompting alone give inconsistent results, and how can code reduce that?
3. Define catastrophic forgetting.
4. A company's refund policy changes every month. Fine-tune or RAG? Why?
5. What does "prompt tuning" mean in research papers, as opposed to this course?
