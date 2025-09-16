from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
load_dotenv()

os.environ["LANGSMITH_PROJECT"] = 'Sequential-summerizer-LLM'

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

repo_id = "meta-llama/Llama-3.1-8B-Instruct"
endpoint = HuggingFaceEndpoint(
    repo_id = repo_id,
    max_new_tokens= 80,
    temperature= 0.6,
    huggingfacehub_api_token= os.getenv("HUGGINGFACEHUB_API_TOKEN")
)
model = ChatHuggingFace(llm= endpoint)
parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser
config1 = {
    "tags" : ["sequence llm","report gen"],
    "metadata": {"model":"HF meta-llama"}
}
result = chain.invoke({'topic': 'Unemployment in India'},
                       config= config1)

print(result)
