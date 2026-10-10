# Lecture 2 · Traditional AI (ML) vs Generative AI

## Traditional AI / machine learning

- **Focus:** decision-making, prediction, classification.
- **Learns from** historical data to find patterns.
- **Outputs:** labels, scores, probabilities.
- **Examples:** predicting loan default, classifying spam, recommending movies on Netflix.

## Generative AI

- **Focus:** creating and synthesizing new content.
- **Learns from** massive unstructured datasets (text, images, code).
- **Outputs:** new text, images, code, audio.
- **Examples:** drafting a blog post, generating a product image, realistic synthetic voices.

## Key differences

| Aspect | Traditional AI (ML) | Generative AI |
|---|---|---|
| Objective | Predict or classify from past data | Create new, original outputs |
| Input | Structured data (tables, labels, numbers) | Unstructured + structured (text, images, audio) |
| Output | Labels, predictions, probabilities | Text, images, video, code, music |
| Methods | Regression, classification, clustering | Deep learning (transformers, diffusion models) |
| Example use | Fraud detection, price prediction | Marketing copy, artwork generation |
| End-user impact | Automation, efficiency, decision support | Creativity, personalization, productivity |

## Strengths and limitations

| | Strengths | Limitations |
|---|---|---|
| **Traditional AI** | Strong on structured, tabular data · high accuracy on prediction tasks · clear evaluation metrics (accuracy, precision, recall) | Limited creativity · weak on unstructured data unless heavily pre-processed |
| **Generative AI** | Handles unstructured data naturally · creative, human-like output · great for personalization | Can **hallucinate** (confident but wrong) · hard to evaluate objectively · needs a lot of compute |

## They work best together

The lecture's key point: these approaches solve **different** problems and are often **combined**.

Example: a support system where
- a **traditional classifier** routes each ticket (billing / claims / complaint), which is fast, cheap and measurable, and
- an **LLM** drafts the reply for that ticket.

My live-session project does a version of this with an LLM for both steps: it classifies call transcripts into `billing`, `claims`, `complaint` and `general_query`, then evaluates them (see `../../../03_live_sessions/01_call_transcript_qa/experiment.ipynb`).

## How to choose

- Need a **number, label or yes/no** from tabular data, and must measure accuracy precisely? → **Traditional ML.**
- Need to **read, write, summarize or converse** in natural language, or work with images or audio? → **Generative AI.**
- Need both reliability and language ability? → **Combine them.**

## Key takeaways

- Traditional AI = **prediction + classification**.
- Generative AI = **content creation + synthesis**.
- They solve different problems and often work best **together**.
- Knowing the difference helps you pick the right tool for each task.

## Check yourself

1. Why is a credit-risk score usually a job for traditional ML rather than an LLM?
2. What does "hallucination" mean, and why does it make GenAI harder to evaluate?
3. Design a system for an e-commerce site that uses both approaches.
