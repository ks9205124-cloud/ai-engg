import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from groq import Groq

# Load environment variables
load_dotenv()
print("[INFO] Environment variables loaded.")

my_api_key = os.getenv("MY_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
print("[INFO] API keys and configuration URLs retrieved.")

# Initialize Groq and Qdrant clients
client = Groq(api_key=my_api_key)
groq_model = "openai/gpt-oss-120b"
print("[INFO] Groq client initialized successfully.")

quad_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
print("[INFO] Qdrant client initialized successfully.")

collection_name = "knowledge"
embedding_size = 384
print(f"[INFO] Collection name set to '{collection_name}' with vector size {embedding_size}.")

# Check and recreate collection
if quad_client.collection_exists(collection_name):
    print(f"[INFO] Collection '{collection_name}' already exists. Deleting it...")
    quad_client.delete_collection(collection_name)
    print("[INFO] Old collection deleted successfully.")
else:
    print(f"[INFO] Collection '{collection_name}' does not exist yet. Proceeding to create.")

quad_client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=embedding_size,
        distance=Distance.COSINE,
    ),
)
print(f"[INFO] New collection '{collection_name}' created successfully.")

# Read documents
print("[INFO] Reading 'knowledge.txt'...")
with open("knowledge.txt", "r", encoding="utf-8") as f:
    documents = [
        line.strip()
        for line in f
        if line.strip()
    ]
print(f"[INFO] Loaded {len(documents)} documents from file.")

# Load embedding model and encode documents
print("[INFO] Loading SentenceTransformer model ('all-MiniLM-L6-v2')...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("[INFO] Embedding model loaded successfully.")

print("[INFO] Generating embeddings for all documents...")
embeddings = model.encode(documents)
print(f"[INFO] Generated embeddings for {len(embeddings)} documents.")

# Prepare points for Qdrant
print("[INFO] Preparing PointStruct objects for upsert...")
points = []
for i, embedding in enumerate(embeddings):
    point = PointStruct(
        id=i + 1,
        vector=embedding.tolist(),
        payload={
            "text": documents[i]
        }
    )
    points.append(point)
print(f"[INFO] Prepared {len(points)} points.")

# Upload to Qdrant
print(f"[INFO] Upserting points into Qdrant collection '{collection_name}'...")
quad_client.upsert(
    collection_name=collection_name,
    points=points
)
print("[INFO] Upsert process completed successfully.")


def search(query, top_k=3):
    print(f"\n[SEARCH] Encoding query string: '{query}'...")
    query_vector = model.encode(query).tolist()

    print(f"[SEARCH] Querying Qdrant database for top {top_k} results...")
    results = quad_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    ).points

    print(f"[SEARCH] Retrieved {len(results)} matching results from Qdrant.")
    return results


def ask_llm(question, context):
    print("[LLM] Constructing prompt with retrieved context...")
    prompt = f"""
Answer the question using only the information provided below.

Context:
{context}

Question:
{question}

If the answer is not present in the context, say:
"I don't know based on the provided information."
"""
    print("[LLM] Sending request to Groq API (llama-3.3-70b-versatile)...")
    response = client.chat.completions.create(
        model=groq_model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print("[LLM] Response received from Groq API.")
    return response.choices[0].message.content


# ============================================================
# PART 12 — COMPLETE RAG PIPELINE EXECUTION
# ============================================================

question = "How many vacation days do I get?"
print(f"\n[PIPELINE] Starting RAG pipeline execution for question: '{question}'")

results = search(question, top_k=3)

print("[PIPELINE] Extracting and formatting context from search results...")
context = "\n".join(
    result.payload["text"]
    for result in results
)
print(f"[PIPELINE] Compiled context preview:\n---\n{context}\n---")

answer = ask_llm(question, context)

print("\n==============================")
print("Final Answer:")
print("==============================")
print(answer)