# WE Chatbot – RAG-based Customer Support Assistant

# Project Overview
WE Chatbot is a Retrieval-Augmented Generation (RAG) proof-of-concept designed to provide intelligent customer support for Telecom Egypt (WE) services.  
The system retrieves relevant information from official WE service pages and generates accurate, context-aware answers in both Arabic and English.
This project demonstrates practical RAG implementation, system design thinking, and on-prem / local deployment readiness.
---
# System Architecture
1. Data Collection (Web pages & documents)
2. Text Cleaning & Chunking
3. Embedding Generation (Sentence Transformers)
4. Vector Storage (FAISS)
5. Query Retrieval
6. Answer Generation (LLM)
7. Streamlit User Interface
> Embeddings and FAISS index are precomputed for demo purposes.
---
# Tech Stack
- Python 3.10+
- Streamlit
- FAISS (Vector Search)
- Sentence Transformers
- HuggingFace Transformers
- BeautifulSoup
- PyPDF2 / python-docx
- Pillow
---
# Project Structure
```text
WE_Chatbot/
│
├── app.py
├── rag_pipeline.py
├── requirements.txt
├── data/
│   ├── raw_pages/
│   └── vector_store/
├── images/
│   └── we_landing.jpg
└── README.md
```

# Setup Instructions
1.Clone Repository
2.Create Virtual Environment
3.Install Dependencies / requirements.txt
4.Run the Application

# Streamlit Demo
-A short demo video showcasing the Streamlit UI and RAG interaction workflow.
Demo Video:

# Known Limitations
- Full embedding generation is resource-intensive
- Streamlit Cloud CI may fail installing ML dependencies
- Recommended deployment: Local / On-Prem / GPU server

# Future Improvements
1.Arabic LLM fine-tuning
2.Feedback-based retrieval ranking
3.Multi-user session memory
4.GPU-based inference
5.Production API deployment

# Author
Mostafa Mohamed Qapil
AI Engineer | Data Scientist
