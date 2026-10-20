# Lecture 16 · Memory in LangChain (Week 4)

## Why memory matters

An LLM API is **stateless**: every call starts from a blank slate. Without memory:
- each prompt forgets everything said before;
- follow-ups like "and what about the second one?" have nothing to refer to;
- the model loses continuity: tone, facts the user shared, progress on a task.

I've already seen both sides of this in my own Week 2 projects:

| Project | What it sends the model | Result |
|---|---|---|
| [02_chatbot](../../week_02/02_chatbot/llm_provider.py) | Only the current message | **No memory**: in testing it forgot my name one message after I told it |
| [03_capstone](../../week_02/03_capstone/app.py) | The whole `st.session_state["history"]` list, every turn | Remembers the conversation, because I resend it each time |

So "memory" isn't something the model has. It's something **my code does**: store the conversation and put it back into the prompt.

> "Memory turns your chatbot from a responder into a conversational companion."

## What memory is in LangChain

- **Definition:** the way a chain or agent **stores and retrieves** earlier turns between the user and the model.
- **Core idea:** on every call, the stored history is **injected back into the prompt**. That's exactly what my capstone does by hand.

| Where it's used | What it remembers |
|---|---|
| Chatbots and assistants | The conversation so far |
| Multi-step workflows | Outputs of earlier steps |
| Agents | The plan, facts gathered, tool results, reflections |

## The memory types on the slides

The lecture lists six classic memory classes. The ideas are still the standard strategies; the class names are not (see the correction below).

| Memory type | What it keeps | When to use it |
|---|---|---|
| **ConversationBufferMemory** | Every message, word for word | Short chats where full context matters |
| **ConversationBufferWindowMemory** | Only the last *k* exchanges | Long chats; keeps context recent and bounded |
| **ConversationTokenBufferMemory** | As many recent messages as fit a **token** budget; drops the oldest | When you must stay under the model's context window |
| **ConversationSummaryMemory** | A running **summary** of the chat instead of the raw messages | Very long chats (support, tutoring): short, cheap, still context-aware |
| **VectorStoreRetrieverMemory** | Messages as **embeddings** in a vector store; retrieves only the ones related to the new input | Long-term recall ("you mentioned this days ago") |
| **EntityMemory** | Facts about specific **entities** ("Alice = customer from New York", "Project X = delayed 2 weeks") | Personalized assistants that track people, clients, projects |

The trade-off running through the table: **more history = better recall but more tokens (cost, latency, context limit)**. Each type is a different way to decide what to keep.

> **Correction to the slide:** all six classes are **legacy**. They were deprecated in LangChain 0.3, removed from the `langchain` package in 1.0, and now live only in the separate `langchain-classic` package (with `ConversationChain`). On my installed versions (langchain 1.4.3, langchain-core 1.6.6), `from langchain.memory import ConversationBufferMemory` fails with `ModuleNotFoundError: No module named 'langchain.memory'`. Three smaller fixes: the real class name is `ConversationEntityMemory`, not `EntityMemory`; "summary + recent messages" describes `ConversationSummaryBufferMemory`, while `ConversationSummaryMemory` keeps only the summary; and token-based trimming works for any model, not just OpenAI's. The modern equivalents are below.

## Modern equivalents

Today, memory is just **a list of messages** that you trim, summarize or persist, plus LangGraph when you want it saved per conversation automatically.

| Legacy idea | Modern way |
|---|---|
| Buffer memory | Keep a message list; inject it with `MessagesPlaceholder` |
| Window / token buffer | `trim_messages(...)` by message count or token count |
| Summary memory | `SummarizationMiddleware` on an agent (or a summarize step of your own) |
| Persisting chats per user/session | A LangGraph **checkpointer** with a `thread_id` |
| Entity / vector (long-term) memory | A LangGraph **store**, or retrieval over a vector store (Lecture 18) |

### 1. Buffer memory: a message list + `MessagesPlaceholder`

The LangChain version of my capstone's `session_state["history"]`:

```python
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = FakeListChatModel(responses=["Nice to meet you, Jayanth!", "Your name is Jayanth."])  # swap for a real chat model

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder("history"),          # past turns are injected here
    ("human", "{question}"),
])
chain = prompt | llm

history = []                                  # the "memory" is just a list you own
for question in ["Hi, I'm Jayanth.", "What's my name?"]:
    reply = chain.invoke({"history": history, "question": question})
    history += [HumanMessage(question), AIMessage(reply.content)]
    print(reply.content)
```

The fake model returns canned replies so this runs offline; with a real model, the second answer is only possible because `history` went into the prompt.

### 2. Window and token buffers: `trim_messages`

Trim the list before sending it. Counting with `len` gives a **window** (count messages); a token counter gives a **token buffer**.

```python
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, trim_messages
from langchain_core.messages.utils import count_tokens_approximately

history = [SystemMessage("You are a helpful assistant.")]
for i in range(1, 6):
    history += [HumanMessage(f"question {i}"), AIMessage(f"answer {i}")]

window = trim_messages(history, strategy="last", token_counter=len,        # window: count messages
                       max_tokens=5, include_system=True, start_on="human")
print([m.content for m in window])
# ['You are a helpful assistant.', 'question 4', 'answer 4', 'question 5', 'answer 5']

budget = trim_messages(history, strategy="last", token_counter=count_tokens_approximately,
                       max_tokens=40, include_system=True, start_on="human")   # token buffer
```

`include_system=True` keeps the instructions; `start_on="human"` makes sure the trimmed history doesn't begin with an orphaned AI reply.

### 3. Persistent conversations: a LangGraph checkpointer

Instead of managing the list yourself, let LangGraph save the state after every step, keyed by a `thread_id` (one per user or chat session):

```python
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph

llm = FakeListChatModel(responses=["Hi Jayanth!", "You're Jayanth."])  # swap for a real chat model

def call_model(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}   # the model sees the whole thread

builder = StateGraph(MessagesState)
builder.add_node("model", call_model)
builder.add_edge(START, "model")
graph = builder.compile(checkpointer=InMemorySaver())

cfg = {"configurable": {"thread_id": "user-1"}}
graph.invoke({"messages": [("user", "Hi, I'm Jayanth.")]}, cfg)
out = graph.invoke({"messages": [("user", "What's my name?")]}, cfg)
print(len(out["messages"]))   # 4: both turns are stored in thread "user-1"
```

A different `thread_id` starts an empty conversation. `InMemorySaver` is lost on restart; production apps swap in a database-backed checkpointer (e.g. SQLite or Postgres).

### 4. Summary memory for long chats

LangChain 1.x agents take the checkpointer directly, plus middleware that summarizes old messages once the history gets too long:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langgraph.checkpoint.memory import InMemorySaver

llm = FakeListChatModel(responses=["Hi Jayanth!", "You're Jayanth."])  # swap for a real chat model
agent = create_agent(
    model=llm,
    tools=[],
    checkpointer=InMemorySaver(),
    middleware=[SummarizationMiddleware(model=llm, trigger=("tokens", 4000), keep=("messages", 20))],
)
cfg = {"configurable": {"thread_id": "user-1"}}
agent.invoke({"messages": [{"role": "user", "content": "Hi, I'm Jayanth."}]}, cfg)
```

When the thread passes 4,000 tokens, older messages are replaced by a summary and the last 20 are kept verbatim: the modern form of "summary + recent messages".

> **Note on `RunnableWithMessageHistory`:** many tutorials from 2024 replace the legacy classes with `RunnableWithMessageHistory` + `InMemoryChatMessageHistory`. They still run on my install, but both now print a `LangChainDeprecationWarning` (deprecated in langchain-core 1.3.3 and 1.6.4, removal planned for 2.0), pointing to LangGraph persistence instead. Recognise them in older code; use a checkpointer in new code.

## Choosing a strategy

| Scenario | Slide's choice | Modern choice |
|---|---|---|
| Simple chat assistant | Buffer | Message list + `MessagesPlaceholder` |
| Token-sensitive model | Token buffer | `trim_messages` with a token counter |
| Long chat sessions | Summary | `SummarizationMiddleware` (or summarize + keep recent) |
| Recall across sessions | Vector store memory | LangGraph store, or retrieval (Lecture 18) |
| Personalized assistant | Entity memory | LangGraph store holding facts per user |

**Rule of thumb:** small projects start with a plain buffer or window; assistants that must scale need summaries or retrieval.

> **Memory vs RAG:** the slide's table suggests vector memory for an "FAQ bot", but its own best practices say memory is for the **conversation** and RAG is for **knowledge**. FAQ answers are knowledge: put them in a retriever (see [Lecture 18](18_introduction_to_rag.md)), and keep memory for what this user said.

## Best practices

| Practice | Why |
|---|---|
| **Be explicit** about what you keep and for whom (per user, per session) | Avoids leaking one user's history into another's |
| **Limit context** | History grows every turn; the context window, cost and latency don't |
| **Summarize old turns** | Prevents prompt bloat while keeping the gist |
| **Combine with RAG** | Memory = the conversation; RAG = the documents |
| **Persist selectively** | Not every session needs storing forever (cost, privacy) |

For context: memory builds on prompt templates ([Lecture 13](13_prompt_engineering_in_langchain.md)) and the pipe syntax from [Lecture 15](15_chains_in_langchain.md) and [Lecture 17](17_runnables_in_langchain.md).

> **Takeaway:** the model never remembers anything. Memory is your code storing the conversation and putting the right part of it back into each prompt. Today that means a trimmed message list or a LangGraph checkpointer, not the old `Conversation*Memory` classes.

## Check yourself

1. Why did my `02_chatbot` forget my name while `03_capstone` didn't? Which line of the capstone is the "memory"?
2. What's the difference between a window buffer and a token buffer? Write the `trim_messages` call for each.
3. A tutoring bot's chats run for hours. Which strategy keeps cost bounded without losing the early context, and what does it lose?
4. What does a `thread_id` do in a LangGraph checkpointer, and what happens to the history when the app restarts with `InMemorySaver`?
5. A user asks a support bot about the refund policy. Should the answer come from memory or from RAG? Why?
6. You find `from langchain.memory import ConversationBufferMemory` in an old repo. Why does it fail on LangChain 1.x, and what would you replace it with?
