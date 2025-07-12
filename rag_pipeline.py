from embedder import model
import numpy as np

def get_top_k_chunks(query, chunks, faiss_index, k=3):
    query_embedding = model.encode([query])
    D, I = faiss_index.search(np.array(query_embedding), k)
    return [chunks[i] for i in I[0]]

def generate_prompt(context_chunks, question):
    context = "\n---\n".join(context_chunks)
    return f"""You are an assistant answering based on company documents.

Context:
{context}

Question: {question}

Answer:"""
