import openai
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

client = openai.AsyncOpenAI(
    api_key= os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

async def generate_response(prompt):
    try:
        response = await client.chat.completions.create(
            model = "gpt-oss-120b:free",
            messages = [
                {
                    "role":"system",
                    "content":"You are a helpful assistant"
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occured : {e}"
    
async def main():
    user_prompt = "Explain why droplets are round in a way a 5 year old understands"
    print("generating response for : ", user_prompt)

    response = await generate_response(user_prompt)

    print(" -------LLM Response-----")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
