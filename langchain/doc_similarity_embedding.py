from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-l6-v2")


docs = ["I am sachin", "There is ice","Queens are angry","What is forest"] # list of strs
question = "King is ready"

vectors = np.array(embedding.embed_documents(texts= docs))
question_vector = np.array(embedding.embed_query(text= question))

print(vectors.shape)
print(question_vector.shape)
# i =0
# highest_similarity = 0
# highest_similarity_index = -1
# for vec in vectors:
#     similarity = cosine_similarity(question_vector,vec)
#     if similarity > highest_similarity:
#         highest_similarity = similarity
#         highest_similarity_index = i
#     print("cosine similarity of",i ,"doc", cosine_similarity(question,vec))
#     i +=1

# print("Higest Similarity : ", highest_similarity)
# print("Closes doc : ", docs[highest_similarity_index])