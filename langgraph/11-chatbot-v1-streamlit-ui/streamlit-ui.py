import streamlit as st
from chatbot_workflow import create_chatbot
from langchain_core.messages import HumanMessage

if "chatbot" not in st.session_state:
    chatbot = create_chatbot()
    config1 = {"configurable":{"thread_id":1}}
    st.session_state.chatbot = chatbot
    st.session_state.config = config1

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
    config1 = st.session_state.config
    response = workflow.invoke(init_state, config=config1)["messages"][-1].content
    with st.chat_message("ai"):
        st.markdown(response)
    st.session_state.messages.append({"role":"ai","content":response})