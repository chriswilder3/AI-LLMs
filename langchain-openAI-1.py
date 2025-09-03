import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import get_usage_metadata_callback


load_dotenv()

llm = ChatOpenAI(
        model = 'gpt-4.1-mini',
        api_key = os.getenv('OPENAI_API_KEY'),
        temperature= 0.5,
    )

prompt = PromptTemplate.from_template(
        "You are an author. Write short witty story on {topic}"
    )

chain = prompt | llm | StrOutputParser()

user_topic = input("Enter a topic name : ")

with get_usage_metadata_callback() as cb:
    response = chain.invoke({"topic":user_topic})
    print("Usage : ",cb.usage_metadata)

print("----LLM Response----")
print(response)

    