import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2') #array vector of size 384

text = "machine learning is fun"

#res = model.encode(text)

#print(res[:10])

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

t1 = "there are 24 paid leaves"
t2 = "there are 24 vacation days"

v1 = model.encode(t1)
v2 = model.encode(t2)

#0.5196915
print(cosine_similarity(v1, v2))