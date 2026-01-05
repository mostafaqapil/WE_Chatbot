# rag_pipeline_we_final
import os
import faiss
import pickle
import torch
import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from docx import Document as DocxDocument
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract

VECTOR_STORE_DIR = "data/vector_store"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODEL = "google/mt5-base"
TOP_K = 6
MAX_CONTEXT_CHARS = 1800
device = torch.device("cpu")

index = faiss.read_index(os.path.join(VECTOR_STORE_DIR, "we_faiss.index"))
with open(os.path.join(VECTOR_STORE_DIR, "documents.pkl"), "rb") as f:
    documents = pickle.load(f)
with open(os.path.join(VECTOR_STORE_DIR, "metadata.pkl"), "rb") as f:
    metadata = pickle.load(f)

embedder = SentenceTransformer(EMBEDDING_MODEL)
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL).to(device)
def load_pdf(path): 
    text = ""
    reader = PdfReader(path)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def load_docx(path):
    doc = DocxDocument(path)
    return "\n".join([p.text for p in doc.paragraphs])

def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_html(path):
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        return soup.get_text(separator="\n")

def load_image(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)

def load_user_document(path: str) -> str:
    ext = path.split(".")[-1].lower()
    if ext == "pdf":
        return load_pdf(path)
    elif ext == "docx":
        return load_docx(path)
    elif ext == "txt":
        return load_txt(path)
    elif ext == "html":
        return load_html(path)
    elif ext in ["jpg","jpeg","png"]:
        return load_image(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
def chunk_text(text, max_chars=MAX_CONTEXT_CHARS):
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        chunks.append(text[start:end])
        start = end
    return chunks

def add_user_documents(paths: List[str]):
    global documents, metadata, index
    new_docs, new_meta = [], []

    for path in paths:
        text = load_user_document(path)
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            new_docs.append(chunk)
            new_meta.append({
                "source": os.path.basename(path),
                "page": os.path.basename(path),
                "chunk_id": i +1
            })
    embeddings = embedder.encode(new_docs)
    dim = embeddings.shape[1]
    if index is None or index.ntotal == 0:
        index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings, dtype="float32"))

    documents.extend(new_docs)
    metadata.extend(new_meta)
#  Core RAG Function
def ask_we_bot(question: str) -> Tuple[str, List[dict]]:
    query_vec = embedder.encode([question])
    distances, indices = index.search(query_vec, TOP_K)

    retrieved_docs, retrieved_meta = [], []
    seen_sources = set()

    
    keywords = [
        "WE Pay","subscribe","subscription","How to","Visit","Download","Activate","OTP","wallet",
        "اشترك","تفعيل","باقة","فاتورة","محفظة","خطوات التسجيل","محفظة رقمية"
    ]

    for i in indices[0]:
        text = documents[i]
        meta = metadata[i]
        if any(k.lower() in text.lower() for k in keywords):
            source_id = (meta.get("source"), meta.get("chunk_id"))
            if source_id not in seen_sources:
                retrieved_docs.append(text)
                retrieved_meta.append(meta)
                seen_sources.add(source_id)

    if not retrieved_docs:
        return "المعلومة غير متوفرة في موقع WE الرسمي.", []

    context = "\n\n".join(retrieved_docs[:TOP_K])

    prompt = f"""
You are a professional customer support assistant for Telecom Egypt (WE).

TASK:
Answer clearly and completely in the SAME language as the question.
If the question is in Arabic, answer in Arabic.
If the question is in English, answer in English.

Use ONLY the information in the CONTEXT below.
Provide step-by-step instructions if the context contains steps.
Include the source of your information for each part of the answer.

CONTEXT:
{context}

QUESTION:
{question}

Answer now in the same language as the question.
"""



    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        num_beams=4,
        no_repeat_ngram_size=3,
        early_stopping=True
    )
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = answer.replace("<extra_id_0>", "").strip()
    return answer, retrieved_meta

if __name__ == "__main__":
    print("\n WE Chatbot Ready (Final Production RAG Mode)")
    print("Type 'exit' to quit or 'upload:file1.pdf,file2.docx' to add documents dynamically.")

    while True:
        try:
            q = input("\nAsk WE Bot: ")
            if q.lower() == "exit":
                break
            elif q.startswith("upload:"):
                files = q.replace("upload:", "").strip().split(",")
                add_user_documents(files)
                print(f" Added {len(files)} document(s) successfully.")
            else:
                answer, sources = ask_we_bot(q)
                print("\nAnswer:\n", answer)
                print("\nSources:")
                for s in sources:
                    print(f"[SOURCE]: {s['source']} | [PAGE]: {s['page']} ")
        except KeyboardInterrupt:
            print("\nExiting WE Bot...")
            break
