from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os

load_dotenv()
repo_id = "meta-llama/Llama-3.1-8B-Instruct"

llm = HuggingFaceEndpoint(
    repo_id = repo_id,
    max_new_tokens= 50,
    temperature= 0.5,
    huggingfacehub_api_token= os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

llm = ChatHuggingFace(llm = llm)

import streamlit as st

st.header("Research Tool")

user_input = st.text_input("Enter your prompt")

# Static prompting provides fixed, pre-determined instructions
# to AI models, ideal for consistent tasks but lacking 
# adaptability, while dynamic prompting creates adaptive prompts 
# that change based on real-time user inputs, environmental data,
# or conversation history to generate personalized and 
# context-aware responses. 
# Dynamic prompts offer higher user engagement & more relevant 
# outputs, making them crucial for complex, evolving interactions
# Dynamic prompts have key_vals which get included as part 
# of input string sent to LLMs.

if st.button("generate"):
    response = llm.invoke(user_input)
    st.write("Summary of paper \n : ",response.content)