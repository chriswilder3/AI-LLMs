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
    response = llm.invoke(state["messages"])
    return {"messages": [AIMessage(content= response.content)]}
    # for chunk in llm.stream(state["messages"]): 
    #     yield {"messages": [AIMessage(chunk.content)]}
    # response = ""
    # for chunk in llm.stream(state["messages"]):
    #     response += chunk.content
    #     # yield {"messages": [AIMessage(chunk.content)]}  # stream to client
    # print("AI :",AIMessage(response))
    # # after streaming, push the *full* AIMessage into the state
    # yield {"messages": [AIMessage(response)]}

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
    # Keep the creation outside the loop otherwise, new workflow
    # created everytime and hence persistance fails
    workflow = create_chatbot()
    # config needed since checkpoint active
    config1 = {"configurable":{"thread_id":1}}

    while True:
        user_input = input("Ask something : ")
        if user_input in ["exit","q"]:
            break

        init_state = {
            "messages" : [HumanMessage(user_input)]
        }
        # final_state = workflow.invoke(init_state, config=config1)
        # print(final_state["messages"][-1].content)
        generator_obj = workflow.stream(init_state, config= config1,
                                            stream_mode="messages")
        for chunk, metadata in generator_obj:
            if chunk.content:
                print(chunk.content, end="|",flush= True)
        print("\n")
    
if __name__ == "__main__":
    main()

