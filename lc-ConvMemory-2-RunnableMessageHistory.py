import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
        model = 'gpt-4.1-mini',
        api_key= os.getenv('OPENAI_API_KEY')
    )

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
        [
            ("system","You are a helpful assistant. Answer all questions"),
            ("placeholder","{chat_history}"),
            ("human","{input}")
        ]
    )

chain = prompt | llm

# Lets first create a chat history obj
from langchain_community.chat_message_histories import ChatMessageHistory

chat_history = ChatMessageHistory()

# RunnableWithMessageHistory is a wrapper around runnables(chain)
# Which manages the chat history for them. It takes as input :
# chain, a function that chat history for a session,
# keys/variables used inside prompt : input, chat_history

from langchain_core.runnables.history import RunnableWithMessageHistory

chain_with_chat_history = RunnableWithMessageHistory(
        chain, lambda session_id : chat_history,
        input_messages_key= "input",
        history_messages_key="chat_history" 
    )
# Above we have used python lambda function lambda x:f(x)
#  session_id is used to get specific session of a user
# among many, but since there is only one user here we are
# returning chat_history obj directly
# Now chain_with_chat_history can be invoked with input, and
# another dict with configurable key that passes session id
# {"configurable": {"session_id": "unused"} 

for i in range(10):
    user_input = input("Ask AI Question : ")

    response = chain_with_chat_history.invoke(
                input = {"input":user_input},
                config = {"configurable":{"session_id":"unused"}}
            )
    
    print("----LLM Response----")
    print(response.content)

