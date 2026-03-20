import os

documents = []

# Load documents from data folder
def load_docs():
    global documents
    documents.clear()
    for file in os.listdir("data"):
        with open(f"data/{file}", "r", encoding="utf-8") as f:
            text = f.read().strip()
            if text:
                documents.append(text)

# No index needed now
def create_index():
    return documents

# Simple keyword search
def search(query, index):
    if not index:
        return ""
    
    query = query.lower()
    
    for doc in index:
        if query in doc.lower():
            return doc
    
    return ""