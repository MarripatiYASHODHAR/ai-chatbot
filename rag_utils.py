import faiss
import os
from models.embeddings import get_embedding

documents = []
vectors = []

def load_docs():
    global documents, vectors
    documents.clear()
    vectors.clear()
    for file in os.listdir("data"):
        with open(f"data/{file}", "r", encoding="utf-8") as f:
            text = f.read().strip()
            if text:
                documents.append(text)
                vectors.append(get_embedding(text))

def create_index():
    import numpy as np
    if not vectors:
        return None
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors))
    return index

def search(query, index):
    import numpy as np
    if index is None or not documents:
        return None
    q_vec = get_embedding(query)
    D, I = index.search(np.array([q_vec]), k=1)
    # Defensive: check if index result is valid
    if I is not None and len(I[0]) > 0 and I[0][0] < len(documents):
        return documents[I[0][0]]
    return None