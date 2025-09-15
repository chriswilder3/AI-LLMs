import os
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict

# BMI Calculator

llm = ChatOpenAI(
        model = 'gpt-4.1-mini',
        api_key = os.getenv('OPENAI_API_KEY'),
        temperature= 0.5,
    )
# State
class BMIState(TypedDict):
    height : float
    weight : float
    bmi : float

# Runnable/functions (nodes)
def calculate_bmi(state :BMIState) -> BMIState:
    bmi = round(state["weight"] /  ((state["height"])**2),2)
    state["bmi"] = bmi
    return state
 
graph = StateGraph(state_schema= BMIState)

# Add nodes by mapping name to python function/runnable
graph.add_node('calculate_bmi',calculate_bmi) 
        # we can also use: graph.add_sequence([calculate_bmi]) 

# Add edges
graph.add_edge(START, "calculate_bmi")
    # if we want we can add END dummy node similarly
graph.add_edge("calculate_bmi", END)

graph_compiled = graph.compile()

height = float(input("enter the height in mtr : "))
weight = float(input("enter the weight in Kg : "))
response = graph_compiled.invoke({"height":height, "weight":weight})
print("BMI :", response['bmi'])

