from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()
import os

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-l6-v2")

text1 = "My name is Sachin"
vector_emb1 = embedding.embed_query(text = text1)
print("vec : ",str(vector_emb1)[:30])


docs = ["I am sachin", "What is wrong"] # list of strs

vectors2 = embedding.embed_documents(texts= docs)
print("2 vecs : ")
for vec in vectors2:
    print(str(vec)[:5], end="|||")
