from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
load_dotenv()

# Simple one-line prompt
prompt = PromptTemplate.from_template("{question}")


repo_id = "meta-llama/Llama-3.1-8B-Instruct"
endpoint = HuggingFaceEndpoint(
    repo_id = repo_id,
    max_new_tokens= 80,
    temperature= 0.4,
    huggingfacehub_api_token= os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model = ChatHuggingFace(llm= endpoint)
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | model | parser

# Run it
result = chain.invoke({"question": "What is the capital of brazil?"})
print(result)
                                                                                                                                                                 