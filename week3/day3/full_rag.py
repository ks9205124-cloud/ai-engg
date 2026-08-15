#problem --> space , searching solved by using vector db

import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2') #array vector of size 384


load_dotenv()

my_api_key = os.getenv("MY_API_KEY")
client = Groq(api_key=my_api_key)
groq_model = "llama-3.3-70b-versatile"

documents = [
    "Employees receive 24 days of paid leave per year.",

    "Employees work from the office on Tuesday, Wednesday and Thursday. "
    "Monday and Friday are optional work-from-home days.",

    "Employees receive Rs 3000 per month for gym reimbursement.",

    "Employees can claim Rs 2000 per month for home internet.",

    "Employees have a 90 day notice period."
]

document_embeddings = model.encode(documents)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

query = "How much vacation do i get"

query_embeddings = model.encode(query)

def retrieve(que_embeddings):
    scores = []
    for i,document in enumerate(document_embeddings):
        score = cosine_similarity(que_embeddings, document_embeddings[i])
        scores.append((score,documents[i]))
    scores.sort(reverse=True)
    return scores[0]

score,context = retrieve(query_embeddings)


def llm_ans():
    llm_contex = context.lower()

    message_system = {
        "role": "system",
        "content": f"""ans in approx 10 line ,
        and on the basis of context only do not hallucinate Context : {llm_contex}""",
    }
    message_user = {
        "role": "user",
        "content": query
    }
    messages = [message_system, message_user]
    response = client.chat.completions.create(
        model=groq_model,
        messages=messages,
    )
    ans = response.choices[0].message.content
    return ans


print(llm_ans())
