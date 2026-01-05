import os
import re
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

RAW_DATA_DIR = "data/raw_pages"
VECTOR_STORE_DIR = "data/vector_store"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_SIZE = 200 
OVERLAP = 40
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
def clean_text(text):
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"Copyright.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"DOWNLOAD OUR APP.*", "", text, flags=re.IGNORECASE)
    return text.strip()

def chunk_text(text, chunk_size, overlap):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
embedder = SentenceTransformer(EMBEDDING_MODEL)
documents = []
metadata = []
embeddings = []
for file in os.listdir(RAW_DATA_DIR):
    if not file.endswith(".txt"):
        continue
    page_name = file.replace(".txt", "")
    with open(os.path.join(RAW_DATA_DIR, file), "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned = clean_text(raw_text)
    chunks = chunk_text(cleaned, CHUNK_SIZE, OVERLAP)

    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        metadata.append({
            "source": "https://te.eg",
            "page": page_name,
            "section": "main",
            "chunk_id": i
        })
        embeddings.append(embedder.encode(chunk))
# FAISS
embeddings = np.array(embeddings).astype("float32")
index = faiss.IndexFlatIP(embeddings.shape[1])
faiss.normalize_L2(embeddings)
index.add(embeddings)

faiss.write_index(index, f"{VECTOR_STORE_DIR}/we_faiss.index")

with open(f"{VECTOR_STORE_DIR}/documents.pkl", "wb") as f:
    pickle.dump(documents, f)

with open(f"{VECTOR_STORE_DIR}/metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print(" Clean Vector Store built successfully")
