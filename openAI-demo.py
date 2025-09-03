import openai
import os
import asyncio

# openai.api_key =  os.environ['OPENAI_API_KEY']

async def generate_response(prompt):
    try:
        response = await openai.AsyncOpenAI().chat.completions.create(
            model = "gpt-4.1-nano",
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
    user_question :str  = "why are stars round"
    
    
    while True:
        user_question = input(" Enter your Question : ")
        user_prompt = f"Explain  {user_question} in a way a 5 year old understands"
        response = await generate_response(user_prompt)
        # print("generating response for : ", user_prompt)
        print(" -------LLM Response-----")
        print(response)
        runAgain = input("\n Press y to ask again, n to exit")
        if runAgain != 'y':
            break
    print("---Exit---")

if __name__ == "__main__":
    asyncio.run(main())
