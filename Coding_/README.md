 WE Chatbot – RAG-based Customer Support Assistant

 An intelligent Retrieval-Augmented Generation (RAG) chatbot designed to provide accurate, bilingual customer support for Telecom Egypt (WE) using official website content and documents.
This project is a proof-of-concept demonstrating real-world RAG system design, focusing on accuracy, explainability, and production readiness.

Project Overview

Traditional chatbots often hallucinate answers or rely on outdated information.
WE Chatbot solves this by grounding every response in retrieved official content from WE sources.

Key goals:

1.Accurate answers
2.Arabic & English support (including Egyptian Arabic)
3.Source-grounded responses
4.Enterprise-style system architecture

System Architecture

User Query
   ↓
Sentence Embeddings (Sentence Transformers)
   ↓
FAISS Vector Search
   ↓
Relevant Context Retrieval
   ↓
Prompt Construction
   ↓
LLM (mT5)
   ↓
Final Answer + Sources

Tech Stack

. Programming Language: Python 3.10+
. Frontend: Streamlit

. Embedding Model:
- sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- Vector Database: FAISS
- LLM: google/mt5-base

. Document Processing:
- PyPDF2
- python-docx
- BeautifulSoup
- pytesseract (OCR)

. ML Frameworks:
- PyTorch
- HuggingFace Transformers

Project Structure
WE_Chatbot/
│
├── streamlit_we_chatbot.py     # Streamlit UI
├── rag_pipeline.py             # Core RAG logic
├── requirements.txt
├── data/
│   ├── raw_pages/              # Scraped WE content
│   └── vector_store/           # FAISS index + metadata
├── images/
│   └── we_landing.jpg
├── notebook/
│   └── WE_Chatbot_RAG_Explanation.ipynb
└── README.md

Setup Instructions

- Clone the Repository
git clone https://github.com/your-username/WE_Chatbot.git
cd WE_Chatbot

- Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

- Install Dependencies
pip install -r requirements.txt
Note: Some ML dependencies may fail on Streamlit Cloud due to resource limits.

- Run the Application
streamlit run streamlit_we_chatbot.py
The chatbot UI will open in your browser.