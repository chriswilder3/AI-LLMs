from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_tool_calling_agent, AgentExecutor
from dotenv import load_dotenv
load_dotenv()
import os

llm = ChatOpenAI(
        model = 'gpt-4.1-mini',
        api_key = os.getenv('OPENAI_API_KEY'),
        temperature = 0.4
    )

searchtool = DuckDuckGoSearchRun()
tools = [searchtool]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , "You are a helpful AI assistant. You can access internet to answer questions"),
        ("user" , "{input}"),
        ("placeholder" , "{agent_scratchpad}")
    ]
)

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(llm, tools, verbose= True)

user_input = input("Enter a topic/question : ")

print(" Agents's thinking strategy : ")
response = agent_executor.invoke({"input":user_input})

print("----LLM Response----")
print(response['output'])

