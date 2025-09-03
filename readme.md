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