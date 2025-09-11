import os
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

# BMI Calculator

llm = ChatOpenAI(
        model = 'gpt-4.1-mini',
        api_key = os.getenv('OPENAI_API_KEY'),
        temperature= 0.5,
    )

graph =StateGraph()
graph = graph.compile()

height = input("enter the height")
weight = input("enter the weight")
graph.invoke({"height":height, "weight":weight})

