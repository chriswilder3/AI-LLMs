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
            ("system","You are a helpful assistant. Answer all the questions."),
            ("placeholder","{messages}")
        ]
    )

# Chat History Demo
from langchain_community.chat_message_histories import ChatMessageHistory

chat_history = ChatMessageHistory()
chat_history.add_user_message("Translate this message to english : Aap Kaha ho? ")
chat_history.add_ai_message("Where are you?")
print(chat_history.messages)

# Chain 
chain = prompt | llm

while True:
    user_input = input("Ask AI Question : ")
    chat_history.add_user_message(user_input)
    response = chain.invoke({"messages":chat_history.messages})
    print("AI : ",response.content)
    askAgain = input("Do you want to continue? y/n")
    if askAgain != "y":
        break
    chat_history.add_ai_message(response.content)