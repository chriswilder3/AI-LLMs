import streamlit as st
from chatbot_workflow import create_chatbot
from langchain_core.messages import HumanMessage, AIMessage
import time
import uuid

#********************* Utilities  **********************

def create_new_chat():
    thread_id = uuid.uuid4()
    st.session_state["thread_id"] = thread_id
    st.session_state["thread_list"].append(thread_id)
    st.session_state.messages= []

def switch_chat(thread_id):
    if st.session_state["thread_id"] == thread_id:
        return
    st.session_state["thread_id"] = thread_id
    chatbot = st.session_state.chatbot
    config1= {"configurable":{"thread_id":thread_id}}
    # messages = [({"role":"ai", "content":x.content} 
    #                              if isinstance(x,AIMessage) 
    #                              else {"role":"user", "content":x.content} )
    #                              for x in chatbot.get_state(config= config1)
    #                              .values["messages"]]

    messages = []
    chat_state = chatbot.get_state(config= config1).values
    for x in chat_state.get("messages", []):
        if isinstance(x, HumanMessage):
            role="user"
        elif isinstance(x, AIMessage):
            role="ai"
        else:
            continue
        messages.append({"role":role, "content": x.content})
    # print(messages)
    # print(chatbot.get_state(config= config1).values["messages"])
    st.session_state.messages = messages
    st.rerun()

def retrieve_all_threads():
    checkpointer = st.session_state.checkpointer
    all_threads = set()
    for cp in checkpointer.list(None):
        all_threads.add(cp.config["configurable"]["thread_id"])
    return list(all_threads)

def change_thread_name(prompt):
    thread_id = st.session_state.thread_id
    if len(prompt) > 15:
        prompt = prompt[:15]
    if len(st.session_state.messages) <3:
        st.session_state.thread_id = prompt
        for i in range(len(st.session_state.thread_list)):
            if st.session_state.thread_list[i] == thread_id:
                st.session_state.thread_list[i] = prompt


#********************* Initializations  **********************

if "chatbot" not in st.session_state:
    chatbot, checkpointer = create_chatbot()
    st.session_state.chatbot = chatbot
    st.session_state.checkpointer = checkpointer

if "messages" not in st.session_state:
    st.session_state.messages= []

if "thread_list" not in st.session_state:
    # Since we are using sqlite db, we need to load, previosly
    # used thread_ids, and add them into thread_list
    prev_threads = retrieve_all_threads()
    if prev_threads == []:
        if "thread_id" not in st.session_state:
            thread_id = uuid.uuid4() # random thread id
            st.session_state.thread_id= thread_id
            st.session_state.thread_list = [thread_id]
        else:
            st.session_state.thread_list = [st.session_state.thread_id]
    else:
        if "thread_id" not in st.session_state:
            st.session_state.thread_id = prev_threads[0]
            st.session_state.thread_list = prev_threads
        else:
            st.session_state.thread_list = prev_threads + [st.session_state.thread_id]

    
#***********************  Side Bar  **************************

with st.sidebar:
    st.title("Chatbot v2")
    if st.button("new chat +"):
        create_new_chat()
    st.header("My Conversations")

    selected_thread = st.session_state.get("thread_id", None)

    for thread_id in st.session_state["thread_list"][::-1]:
        if st.button(str(thread_id), type="primary" if thread_id == selected_thread else "secondary"):
            switch_chat(thread_id)

    # for thread_id in st.session_state["thread_list"]:
    #     if thread_id == st.session_state.thread_id:
    #         if st.button(str(thread_id), type="primary"):
    #             switch_chat(thread_id)
    #     else:
    #         if st.button(str(thread_id), type="secondary"):
    #             switch_chat(thread_id)

#*********************  Display Messages  *******************

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
    generator_obj = workflow.stream(init_state, 
        config={"configurable":{"thread_id":st.session_state.thread_id}}, 
        stream_mode="messages")
    
    # We can use streamlit's write_stream(generator_obj) 
    with st.chat_message("ai"):
        response = st.write_stream(
            chunk.content for chunk,metadata in generator_obj
        )
    print("AI RESP : ", response)
    st.session_state.messages.append({"role":"ai","content":response})

    # change_thread_name(prompt)

    # with st.chat_message("ai"):
    #     placeholder = st.empty()
        # Insert a single-element container.ie, container that can be 
        # used to hold a single element
        # Inside a with st.empty(): block, each displayed 
        # element will replace the previous one.

        # response = ""
        # for chunk, metadata in generator_obj:
        #     if chunk.content:
        #         response += chunk.content
        #         placeholder.markdown(response)  # update progressively
        #         time.sleep(0.04)  # ⏱️ adjust speed here
        # print("AI RESP : ", response)
        # st.session_state.messages.append({"role":"ai","content":response})