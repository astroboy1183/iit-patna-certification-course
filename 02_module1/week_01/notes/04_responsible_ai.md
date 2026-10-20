# Lecture 4 · Responsible AI: bias, safety and ethics

## What is Responsible AI?

**Definition:** designing, developing and deploying AI systems that are **fair, safe, transparent, accountable and aligned with human values**.

**Why it matters**
- AI is increasingly used to make decisions and generate content that people act on.
- Unchecked systems can **amplify bias, spread misinformation or cause harm**.

**Governing principle:** *"Just because we can build it, doesn't mean we should build it without safeguards."*

## Bias in generative AI

**Bias** = systematic errors in outputs that unfairly favour or disfavour certain groups.

| Source | What it means |
|---|---|
| **Training data bias** | Historical prejudice embedded in the data the model learned from |
| **Representation bias** | Some groups are under-represented in the training data |
| **Algorithmic bias** | The model learns and reinforces stereotypical patterns |

**Examples:** resume-screening models that favour one gender; image generators that show doctors as male and nurses as female.

**Impact:** reinforces discrimination and damages trust in AI systems.

## Safety risks

| Risk | What it looks like |
|---|---|
| **Misinformation / hallucination** | Confident-sounding answers that are factually wrong |
| **Harmful content** | Hate speech, offensive jokes, dangerous instructions |
| **Misuse** | Deepfakes for scams, AI-written malware, spam bots |
| **Over-reliance** | Users treating AI output as 100% reliable without checking |

## Ethical considerations

- **Transparency:** people should know when they're interacting with AI.
- **Accountability:** who is responsible when AI causes harm: the developer, the company or the user?
- **Consent and privacy:** protect user data, especially when it's used for **RAG or fine-tuning**.
- **Autonomy:** AI should support human decisions, not blindly replace them.
- **Equity:** the benefits of AI shouldn't be limited to privileged groups.

## Frameworks and guidelines

| Framework | Key idea |
|---|---|
| **EU AI Act (2024)** | Risk-based regulation: stricter rules for higher-risk AI uses |
| **OECD AI Principles** | Inclusive growth, human-centred values, transparency |
| **NIST AI Risk Management Framework (US)** | A risk-based approach to trustworthy AI |
| **Company guidelines** (Microsoft, Google, OpenAI) | Fairness, safety and privacy principles |

## Best practices for developers

1. **Test outputs for bias and fairness**, for example by asking the same question with different names or groups and comparing the answers.
2. **Add guardrails:** input and output filters, safety layers, prompt moderation.
3. **Monitor usage and feedback** after release.
4. **Be transparent about limitations**, e.g. "AI-generated, may contain errors".
5. **Keep a human in the loop** for high-stakes decisions (health, finance, hiring, legal).

### What this looks like in code
- **Validate model output** instead of trusting it. In my live-session project, Pydantic models reject an LLM score outside 1–5 (`../../../03_live_sessions/01_call_transcript_qa/experiment.ipynb`).
- **Never send secrets or unnecessary personal data** to a model; keep API keys in `.env`, never in code.
- **Log prompts and responses carefully**: they can contain personal data.

## The future of Responsible AI

- **Regulation is coming fast:** AI engineers need basic compliance literacy.
- **Ethics as a differentiator:** products with strong safety and ethics earn trust.
- **Your role:** developers aren't just building apps; they're shaping how AI interacts with society.

## Key takeaways

- Bias, safety and ethics are **core responsibilities**, not optional extras.
- Responsible AI builds **trust, fairness and accountability**.
- The industry is moving towards **regulation and standardization**, so engineers must be proactive.

## Check yourself

1. Name the three sources of bias and give an example of each.
2. Your support chatbot sometimes invents refund policies. Which risk is this, and what two safeguards would you add?
3. Why do RAG and fine-tuning raise privacy concerns?
4. When must a human stay in the loop?
