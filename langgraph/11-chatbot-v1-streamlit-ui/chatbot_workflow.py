from langgraph.graph import START, StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langgraph.graph.message import add_messages

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv
load_dotenv()

# Model
repo_id = "meta-llama/Llama-3.1-8B-Instruct"
endpoint = HuggingFaceEndpoint(
    repo_id= repo_id,
    max_new_tokens= 100,
    temperature = 0.3,
    huggingfacehub_api_token= os.getenv("HUGGINGFACEHUB_API_TOKEN")
)
llm = ChatHuggingFace(llm= endpoint)

# State
class ChatState(TypedDict):
    messages : Annotated[List[BaseMessage],add_messages ]

# Nodes(functions)
def chat_node(state : ChatState) -> ChatState:
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [AIMessage(response.content)]}

def create_chatbot():
    # Graph       
    graph = StateGraph(state_schema= ChatState)
    graph.add_node("chat_node", chat_node)

    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    checkpointer1 = InMemorySaver()
    chatbot_workflow = graph.compile(checkpointer= checkpointer1)
    return chatbot_workflow

def main():
    init_state = {
        "messages" : [HumanMessage("What is capital of India? ")]
    }
    
    workflow = create_chatbot()
    # config needed since checkpoint active
    config1 = {"configurable":{"thread_id":1}}
    final_state = workflow.invoke(init_state, config=config1)
    print(final_state["messages"][-1].content)

if __name__ == "__main__":
    main()

