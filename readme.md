# LLM-Based AI Programs

 This repository contains a collection of Python AI programs that demonstrate how to build simple interactive applications using Large Language Models (LLMs). The examples include usage with OpenAI models as well as open-source models via OpenRouter. Langchain is used throughout the project.

## 🚀 Features
- Asynchronous interaction with LLMs using asyncio.
- Support for OpenAI's GPT models (e.g., gpt-4.1-nano).
- Support for free open-source models (e.g., oss120 via OpenRouter).
- A simple CLI loop that:
- Accepts user questions
- Reformulates them into simple prompts (e.g., "Explain like I’m 5")
- Displays model responses interactively

## Setup

1. Clone this repository

``` 
 git clone https://github.com/yourusername/llm-ai-programs.git
 cd llm-ai-programs
```
2. Create a virtual environment (optional but recommended)

```
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies

```
pip install openai asyncio
```

4. Set environment variables
```
export OPENAI_API_KEY="your_api_key_here"
export OPENROUTER_API_KEY="your_api_key_here"
```

## Learnings :

### Model Selection Matters 

**OpenAI Model Cheat Sheet (Text vs Reasoning)**

| Model         | Type          | Strengths | Weaknesses | Best Use Cases | Token Usage Notes |
|---------------|--------------|-----------|------------|----------------|-------------------|
| **gpt-5-nano** | Reasoning     | Strong logical reasoning, planning, math, structured problem-solving | Overuses reasoning tokens even for simple tasks (expensive), slower | Multi-step reasoning, coding with planning, proofs, logic-heavy tasks | Consumes **reasoning tokens** in addition to input/output |
| **gpt-4.1-nano** | Non-reasoning | Lightweight, cheap, fast, good for everyday text generation | Not great at deep reasoning or complex logic | Creative writing, chatbots, summarization, Q&A, brainstorming | Counts **only input/output tokens**, no reasoning tokens |
| **gpt-4.1-mini** | Non-reasoning | Balance of speed, quality, and cost; stronger than `nano` at language tasks | Slightly more costly than `nano` | General-purpose text tasks, summarization, customer support bots | Input/output tokens only |
| **gpt-4.1**    | Non-reasoning | High quality, reliable text generation, broad domain knowledge | More expensive and heavier than `nano`/`mini` | Professional writing, complex summaries, content generation | Input/output tokens only |

---

### 🔑 Quick Rules of Thumb
- ✅ Use **4.1-nano / 4.1-mini** → for **creative writing, summaries, general chat, fast responses**.  
- ✅ Use **4.1** → when you need **high-quality outputs** and can afford more cost.  
- ✅ Use **5-nano** → **only** if your task truly needs **deep reasoning or planning**.  
