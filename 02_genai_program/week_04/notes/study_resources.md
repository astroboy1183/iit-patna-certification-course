# Study resources (Week 4)

Reference material shared alongside the Week 4 lectures: a map of ML/GenAI frameworks, a terminal cheat sheet, and how to get Copilot and Claude API access. Not lectures, but worth keeping in one place.

## 1. ML, data science and GenAI frameworks at a glance

| Area | Tool | Use it for | Strength |
|---|---|---|---|
| **Data handling** | NumPy | Fast numerical arrays and matrix maths | Speed; everything else builds on it |
| | pandas | Cleaning and reshaping tabular data | Powerful table operations |
| **Visualisation** | Matplotlib | Any chart, fully customisable | Control |
| | Seaborn | Statistical plots on top of Matplotlib | Better defaults and looks |
| **Classical ML** | scikit-learn | Regression, classification, clustering | Simple, beginner-friendly |
| | XGBoost · LightGBM · CatBoost | Gradient boosting on tabular data | Top accuracy on tables; LightGBM is fast on large data, CatBoost handles categorical columns with little preprocessing |
| | Statsmodels | Statistical tests and models (econometrics, hypothesis tests) | Detailed statistical output |
| **Deep learning** | PyTorch | Neural networks, research and experimentation | Flexible, Pythonic |
| | TensorFlow · Keras | Neural networks in production; Keras for quick prototyping | Scalable deployment; easy API |
| **NLP** | NLTK | Learning text processing (tokenising, stemming) | Educational |
| | spaCy | Production NLP pipelines (e.g. named-entity recognition) | Fast |
| **GenAI** | Hugging Face Transformers | Pre-trained models: text generation, NLP tasks, fine-tuning | Huge model ecosystem |
| | LangChain | Building LLM apps: prompts, chains, parsers, memory | Modular components ([Lecture 11](11_langchain_introduction.md)) |
| | LangGraph | Stateful, graph-shaped workflows and multi-agent systems | Explicit state and control flow |
| | LlamaIndex | Connecting LLMs to your own data (document Q&A, RAG) | Data connectors and indexing |
| **MLOps** | MLflow | Tracking experiments and the model lifecycle | End-to-end tracking |
| | DVC | Versioning data and models alongside Git | Reproducible pipelines |

**Quick rule of thumb:** pandas + NumPy for data → scikit-learn / XGBoost for classical ML → PyTorch / TensorFlow for deep learning → Transformers / LangChain for GenAI → MLflow / DVC for MLOps.

Where I've used them so far: pandas in the [live-session pipeline](../../../03_live_sessions/01_call_transcript_qa); Transformers, PEFT and PyTorch in the [fine-tuning project](../Finetuning-Project); LangChain in the live-session project.

## 2. Terminal commands: Windows vs macOS / Linux

Linux uses the same commands as macOS (both run bash or zsh).

| Action | Windows (CMD / PowerShell) | macOS / Linux |
|---|---|---|
| Current folder | `cd` (CMD) · `pwd` (PowerShell) | `pwd` |
| List files | `dir` | `ls` |
| Clear screen | `cls` | `clear` |
| Create empty file | `type nul > file.txt` | `touch file.txt` |
| Delete file / folder | `del file.txt` · `rmdir /s folder` | `rm file.txt` · `rm -r folder` |
| Rename or move | `ren` · `move` | `mv` |
| Copy | `copy` | `cp` |
| Run Python | `python app.py` (or `py app.py`) | `python3 app.py` |
| Create venv | `python -m venv .venv` | `python3 -m venv .venv` |
| Activate venv | `.venv\Scripts\activate` | `source .venv/bin/activate` |
| Set env variable (this session) | `set MY_VAR=123` (CMD) · `$env:MY_VAR="123"` (PowerShell) | `export MY_VAR=123` |
| Read env variable | `%MY_VAR%` (CMD) · `$env:MY_VAR` (PowerShell) | `$MY_VAR` |
| Open folder in file manager | `start .` | `open .` (macOS) · `xdg-open .` (Linux) |
| Find a file | `dir filename /s` | `find . -name "filename"` |
| Kill a process | `taskkill /PID 1234 /F` | `kill -9 1234` |
| Network info | `ipconfig` | `ifconfig` or `ip a` (Linux) |

Identical everywhere: `git ...`, `streamlit run app.py`, `pip install ...`, `deactivate`.

The real differences are `python` vs `python3`, `dir` vs `ls`, and the venv activation path.

From my own setup ([fine-tuning issues log](../Finetuning-Project/ISSUES_AND_FIXES.md)):
- **Name the version explicitly:** `python3` can point to the system Python rather than the one you expect, so use `python3.11 -m venv` or `python3.13 -m venv`.
- **Prefer `python -m pip` to `pip`:** it always installs into the Python you're running. On some Windows machines, security policy blocks `pip.exe` but allows `python -m pip`.

## 3. GitHub Copilot vs the Claude API

| | GitHub Copilot | Claude API (Anthropic) |
|---|---|---|
| What it is | AI coding assistant inside the editor | LLM API for building your own apps |
| Typical use | Code completion and chat while coding | Text generation, summaries, code, tool use in your backend (also via LangChain) |
| API key | None for normal use: you sign in with GitHub in VS Code | Required |
| Pricing | Free plan with monthly limits; paid plans for more | Pay-as-you-go, prepaid credits |
| Control over the model | Low | High: model, prompts, parameters |

**Copilot setup:** install the **GitHub Copilot** extension in VS Code → sign in with GitHub → choose the Free plan or a paid one. Then write a comment such as `# function to reverse a string` and accept the suggestion.

> **Correction to the resource:** the guide says Copilot is a free trial followed by a paid subscription. GitHub now has a permanent **Copilot Free** plan with monthly limits on completions and chat; paid plans raise the limits. The exact limits change, so check GitHub's Copilot plans page.

**Claude API key:**
1. Sign in to the Anthropic Console (console.anthropic.com, which now also lives at platform.claude.com).
2. Add billing or prepaid credits: keys don't work without them.
3. Open **API Keys → Create Key**, and copy the key straight away: it's shown only once.
4. Make it available to your code:
   - **Best:** put it in the project's `.env` as `ANTHROPIC_API_KEY=...` (as in my other projects, never committed) and load it with `python-dotenv`.
   - **Current terminal only:** `export ANTHROPIC_API_KEY=...` (macOS/Linux).
   - **Windows, permanently:** `setx ANTHROPIC_API_KEY "..."`, which takes effect in *new* terminals, not the current one.

**Key safety:**
- Never hardcode keys in code and never commit `.env`.
- Rotate a key immediately if it leaks.
- Set spending limits and watch usage in the console.

> **Takeaway:** Copilot helps *you* write code; an LLM API (Claude, OpenAI, Gemini) is what *your app* calls. Most real workflows use both.
