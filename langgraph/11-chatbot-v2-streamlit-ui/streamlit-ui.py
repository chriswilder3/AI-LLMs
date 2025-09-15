import streamlit as st
from chatbot_workflow import create_chatbot
from langchain_core.messages import HumanMessage
import time

CONFIG = {"configurable":{"thread_id":1}}

if "chatbot" not in st.session_state:
    chatbot = create_chatbot()
    st.session_state.chatbot = chatbot

if "messages" not in st.session_state:
    st.session_state.messages= []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask something : "):
    # User messages
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})

    # AI messages
    init_state = {
        "messages": [HumanMessage(prompt)]
    }
    workflow = st.session_state.chatbot

    #response = workflow.invoke(init_state, config=CONFIG)["messages"][-1].content
    generator_obj = workflow.stream(init_state, config=CONFIG, stream_mode="messages")
    response = ""

    # We can use streamlit's write_stream(generator_obj) 
    # with st.chat_message("ai"):
    #     response = st.write_stream(
    #         chunk.content for chunk,metadata in generator_obj
    #     )

    with st.chat_message("ai"):
        placeholder = st.empty()
        # Insert a single-element container.ie, container that can be 
        # used to hold a single element
        # Inside a with st.empty(): block, each displayed 
        # element will replace the previous one.

        full_response = ""

        for chunk, metadata in generator_obj:
            if chunk.content:
                full_response += chunk.content
                placeholder.markdown(full_response)  # update progressively
                time.sleep(0.04)  # ⏱️ adjust speed here
    
    st.session_state.messages.append({"role":"ai","content":response})