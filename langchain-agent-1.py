from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os 

load_dotenv()

llm = ChatOpenAI(
        model = "gpt-4.1-mini",
        api_key = os.getenv('OPENAI_API_KEY'),
        temperature=0.2
    )

from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()
# print(tool.invoke("Sachin Doddamani"))
tools = [search_tool]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful AI assistant. You can access internet to answer questions"),
        ("user","{input}"),
        ("placeholder","{agent_scratchpad}")
    ]
)

from langchain.agents import create_tool_calling_agent, AgentExecutor

agent = create_tool_calling_agent(llm = llm,tools = tools, prompt= prompt)
agent_executor = AgentExecutor(agent = agent, tools = tools )

user_input = input("Enter a topic : ")

response = agent_executor.invoke({"input":user_input})
# response is dict with 2 entries {'input': .., 'output': ..}

print("---LLM response--- \n",response['output'])