🧠 ProcureAI – AI-Powered Vendor Selection System

An advanced AI procurement intelligence platform that automates:

📄 Requirement understanding
📑 Vendor quotation extraction
📊 Multi-vendor comparison
🧠 AI reasoning (RAG + LLM)
🏆 Best vendor selection
📌 Overview

ProcureAI uses a combination of:

OCR (Tesseract)
LLM (Groq - LLaMA 3.3 / 3.1)
Vector Search (FAISS)
RAG Pipeline
Scoring Engine

to automatically analyze vendors and make intelligent procurement decisions.


🚀 Key Features

🧠 AI Requirement Understanding

Converts natural language → structured RFQ
Extracts:
Item
Quantity
Budget
Deadline
Industry

📄 Vendor Document Processing

Supports:
PDFs
Images
Uses OCR to extract text

🧾 Structured Vendor Extraction

Extracts:
Vendor Name
Price
Delivery Days
Warranty
Confidence Score

📊 Intelligent Vendor Scoring

Weighted scoring based on:

💰 Price (40%)
🚚 Delivery (30%)
🛠️ Warranty (20%)
📈 Confidence (10%)

🔍 RAG-Based Decision System

Builds vector DB of vendor data
Retrieves contextual insights
Uses LLM to generate justification

🧠 AI Justification Engine

Generates human-readable reasoning
Based on:
Comparison stats
Context retrieval
Vendor performance

⚡ Async Processing (Celery)

Background requirement processing
Scalable architecture

🗄️ Supabase Integration

Stores:

RFQs
Vendors
Quotations
Documents
Final Decisions

🏗️ System Architecture

User Input (Requirement)
        ↓
LLM Extraction (Groq)
        ↓
RFQ Builder
        ↓
Vendor Upload (PDF/Image)
        ↓
OCR (Tesseract)
        ↓
Vendor Data Extraction (LLM)
        ↓
Scoring Engine
        ↓
Vector DB (FAISS)
        ↓
RAG Retrieval
        ↓
AI Reasoning (Groq)
        ↓
Best Vendor Decision
        ↓
Supabase Storage

⚙️ Tech Stack

Backend: FastAPI
Async Tasks: Celery + Redis
LLM: Groq (LLaMA 3.3 / 3.1)
OCR: Tesseract + Poppler
Vector DB: FAISS
Embeddings: SentenceTransformers
Database: Supabase

📁 Project Structure

origin/procure_ai/
│
├── llm.py
├── rfq_builder.py
├── vendor_pipeline.py
├── vendor_extractor.py
├── vendor_scoring.py
├── vendor_knowledge.py
├── vector_store.py
├── retriever.py
├── ai_reasoning.py
├── full_pipeline.py
├── database.py
├── tasks.py
├── celery_worker.py
└── ocr.py

📡 API Endpoints

🧠 Process Requirement
POST /process

📊 Get Result
GET /result/{task_id}

🧪 Test LLM Extraction
POST /test-llm

📄 Test Vendor File
POST /test-vendor

🏆 Compare Vendors (MAIN FEATURE)
POST /compare-vendors

🔄 Full Pipeline
POST /start-process
POST /upload-vendor
GET  /finalize

🧠 RAG Pipeline Flow

Vendor scoring
Convert vendors → documents
Build vector DB
Retrieve vendor context
Generate AI justification
Select best vendor

📊 Example Output

{
  "selected_vendor": {
    "vendor_name": "ABC Tech",
    "price": 45000,
    "delivery_days": 5,
    "warranty_years": 2,
    "confidence": 0.92
  },
  "ai_justification": "ABC Tech offers the best balance of cost, delivery speed, and reliability.",
  "vendors_analyzed": 3
}

⚙️ Setup Instructions

1️⃣ Clone Repo
git clone https://github.com/your-username/procure-ai.git
cd procure-ai

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Environment Variables

Create .env:

GROQ_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
REDIS_URL=redis://localhost:6379/0

4️⃣ Install External Tools
🔹 Tesseract OCR
Install & set path in code
🔹 Poppler (for PDFs)

5️⃣ Run Redis
redis-server

6️⃣ Start Celery Worker
celery -A origin.procure_ai.celery_worker worker --loglevel=info

7️⃣ Run FastAPI
uvicorn main:app --reload

🧠 Core Intelligence

🔥 Vendor Scoring Formula

Score =
  (Price Factor × 0.4) +
  (Delivery Factor × 0.3) +
  (Warranty × 0.2) +
  (Confidence × 0.1)
  
🔐 Key Strengths

AI-driven decision making
Explainable outputs
Real-time vendor comparison
Scalable async architecture
Production-ready design

📈 Future Enhancements

📊 Frontend dashboard (React)
🔍 Vendor history tracking
🤖 Fine-tuned procurement model
☁️ Cloud deployment
📱 Mobile app
👨‍💻 Author

Developed as part of an AI + Backend + System Design Project

📜 License

MIT License

⭐ Support

If you like this project:

⭐ Star the repo
🍴 Fork it
🚀 Share it
