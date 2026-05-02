

# 🧠 ProcureAI – AI-Powered Vendor Selection System

An advanced **AI procurement intelligence platform** that automates vendor evaluation and decision-making using OCR, LLMs, and Retrieval-Augmented Generation (RAG).

---

## 📌 Overview

**ProcureAI** streamlines the procurement process by intelligently:

* Understanding requirements from natural language
* Extracting vendor data from documents
* Comparing multiple vendors
* Generating AI-driven justifications
* Selecting the best vendor automatically

It combines:

* 🔍 OCR (Tesseract)
* 🧠 LLM (Groq – LLaMA 3.3 / 3.1)
* 📊 Vector Search (FAISS)
* 🔄 RAG Pipeline
* ⚙️ Scoring Engine

---

## 🚀 Key Features

### 🧠 AI Requirement Understanding

* Converts natural language → structured RFQ
* Extracts:

  * Item
  * Quantity
  * Budget
  * Deadline
  * Industry

---

### 📄 Vendor Document Processing

* Supports:

  * PDFs
  * Images
* Uses OCR for text extraction

---

### 🧾 Structured Vendor Extraction

Extracts:

* Vendor Name
* Price
* Delivery Days
* Warranty
* Confidence Score

---

### 📊 Intelligent Vendor Scoring

Weighted scoring system:

* 💰 Price → 40%
* 🚚 Delivery → 30%
* 🛠️ Warranty → 20%
* 📈 Confidence → 10%

---

### 🔍 RAG-Based Decision System

* Builds vector database of vendor data
* Retrieves contextual insights
* Uses LLM for reasoning

---

### 🧠 AI Justification Engine

* Generates human-readable explanations
* Based on:

  * Vendor comparison
  * Retrieved context
  * Performance metrics

---

### ⚡ Async Processing

* Powered by Celery
* Handles background processing efficiently
* Scalable architecture

---

### 🗄️ Supabase Integration

Stores:

* RFQs
* Vendors
* Quotations
* Documents
* Final decisions

---

## 🏗️ System Architecture

```
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
```

---

## ⚙️ Tech Stack

| Category    | Technology             |
| ----------- | ---------------------- |
| Backend     | FastAPI                |
| Async Tasks | Celery + Redis         |
| LLM         | Groq (LLaMA 3.3 / 3.1) |
| OCR         | Tesseract + Poppler    |
| Vector DB   | FAISS                  |
| Embeddings  | SentenceTransformers   |
| Database    | Supabase               |

---

## 📁 Project Structure

```
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
```

---

## 📡 API Endpoints

### 🧠 Core APIs

| Endpoint                | Description                    |
| ----------------------- | ------------------------------ |
| POST `/process`         | Process requirement            |
| GET `/result/{task_id}` | Get result                     |
| POST `/compare-vendors` | Compare vendors (Main Feature) |

---

### 🧪 Testing APIs

| Endpoint            | Description         |
| ------------------- | ------------------- |
| POST `/test-llm`    | Test LLM extraction |
| POST `/test-vendor` | Test vendor file    |

---

### 🔄 Full Pipeline

| Endpoint              | Description        |
| --------------------- | ------------------ |
| POST `/start-process` | Start pipeline     |
| POST `/upload-vendor` | Upload vendor docs |
| GET `/finalize`       | Final decision     |

---

## 🧠 RAG Pipeline Flow

1. Vendor scoring
2. Convert vendors → documents
3. Build vector database
4. Retrieve context
5. Generate AI justification
6. Select best vendor

---

## 📊 Example Output

```json
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
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/procure-ai.git
cd procure-ai
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
REDIS_URL=redis://localhost:6379/0
```

---

### 4️⃣ Install External Tools

* Install **Tesseract OCR**
* Install **Poppler** (for PDF processing)

---

### 5️⃣ Run Redis

```bash
redis-server
```

---

### 6️⃣ Start Celery Worker

```bash
celery -A origin.procure_ai.celery_worker worker --loglevel=info
```

---

### 7️⃣ Run FastAPI Server

```bash
uvicorn main:app --reload
```

---

## 🧠 Core Intelligence

### 🔥 Vendor Scoring Formula

```
Score =
  (Price Factor × 0.4) +
  (Delivery Factor × 0.3) +
  (Warranty × 0.2) +
  (Confidence × 0.1)
```

---

## 🔐 Key Strengths

* AI-driven decision making
* Explainable outputs
* Real-time vendor comparison
* Scalable async architecture
* Production-ready design

---

## 📈 Future Enhancements

* 📊 React frontend dashboard
* 🔍 Vendor history tracking
* 🤖 Fine-tuned procurement model
* ☁️ Cloud deployment
* 📱 Mobile application

---

## 👨‍💻 Author

Developed as part of an **AI + Backend + System Design Project**

---

## 📜 License

MIT License

---

## ⭐ Support

If you found this useful:

* ⭐ Star the repository
* 🍴 Fork it
* 🚀 Share it

