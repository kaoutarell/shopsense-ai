# ShopSense AI

>  A smart product search & discovery engine for Shopify stores / ML in e-commerce.

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=FFD43B&labelColor=000000)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=009688&labelColor=000000)
![sentence-transformers](https://img.shields.io/badge/Embeddings-8A2BE2?style=for-the-badge&logo=huggingface&logoColor=8A2BE2&labelColor=000000)
![FAISS](https://img.shields.io/badge/FAISS-4A90E2?style=for-the-badge&logo=meta&logoColor=4A90E2&labelColor=000000)
![Ollama](https://img.shields.io/badge/Ollama-5E35B1?style=for-the-badge&labelColor=000000)
![Gradio](https://img.shields.io/badge/Gradio-FF6B6B?style=for-the-badge&logo=gradio&logoColor=FF6B6B&labelColor=000000)
![Shopify](https://img.shields.io/badge/Shopify-7AB55C?style=for-the-badge&logo=shopify&logoColor=7AB55C&labelColor=000000)

---

## Overview

**ShopSense AI** is a production-ready applied ML system that reimagines e-commerce product discovery. Instead of keyword-based search, it uses semantic embeddings and vector similarity to match buyer intent with products.

- Maps directly to "search, discovery, and agents" in the job description
- Demonstrates: embeddings, vector search, LLM agents, ML at scale concepts
- Built for commerce — not generic

---

## Core Features

### 1. **Semantic Product Search**

- Natural language queries: _"cozy winter gift for my mom under $50"_
- AI understands intent, not just keywords
- Returns ranked products by relevance (embeddings + vector similarity)
- **Shopify relevance**: Powers the "search & discovery" requirement from the job posting

### 2. **Smart Product Recommendations**

- "Customers who liked this also like..." powered by embedding similarity
- Solves the cold-start problem (works even for new products with zero sales)
- Embedding-based vs. collaborative filtering shows understanding of modern ML approaches

### 3. **AI-Powered Listing Optimization**

- LLM agent analyzes product descriptions
- Suggests improvements for better searchability
- Analyzes competitor listings to optimize positioning
- **Agent architecture** directly matches the job requirement for "agents"

### 4. **Scalable ML Architecture**

- Handles 10K+ products with sub-50ms query latency
- FAISS index supports 1M+ products with optimizations (IVFFlat, HNSW)
- Ready for petabyte-scale data (demonstrates scalability thinking)

---

## Points of Access

### **1. Web Interface**

- **URL**: `http://localhost:7860`
- **Built with**: Gradio
- **Features**: Search, recommendations, statistics
- **Status**: Demo/prototyping interface

### **2. API Endpoints**

- **Base URL**: `http://localhost:8000`
- **Swagger Docs**: `http://localhost:8000/docs`

#### Available Endpoints:

| Endpoint         | Method | Purpose                 |
| ---------------- | ------ | ----------------------- |
| `/health`        | GET    | Health check            |
| `/api/search`    | POST   | Semantic product search |
| `/api/recommend` | POST   | Get similar products    |
| `/api/stats`     | GET    | Pipeline metrics        |

---

## Tech Stack

| Layer         | Tool                                     | Why                             |
| ------------- | ---------------------------------------- | ------------------------------- |
| Embeddings    | `sentence-transformers/all-MiniLM-L6-v2` | Fast, runs locally on M1/M2/M3  |
| Vector Search | FAISS                                    | Industry-standard, blazing fast |
| LLM           | Ollama + `mistral` or `llama3`           | Free, local, no API key needed  |
| Backend       | FastAPI (Python)                         | Clean, async, easy to deploy    |
| Frontend      | React + Tailwind                         | Polished demo UI                |
| Dataset       | Shopify product data (Kaggle)            | Real e-commerce data            |
| Deployment    | HuggingFace Spaces or Render             | Free hosting                    |

---

## Dataset

- **Total Products**: ~10K products
- **Source Stores**: 12 major Shopify retailers
- **Categories**: 430+ product types
- **Price Range**: $0.25 — $8,680
- **Average Price**: $93.30
- **Collection Method**: Public Shopify `/products.json` API (legal, intentionally public endpoint)

---

## Quick Start

### Prerequisites

- Python 3.9+
- M1/M2/M3 Mac or Linux/Windows with 8GB+ RAM
- Ollama (for LLM agent)

### Installation

```bash
# 1. Clone and setup
git clone <repo>
cd shopsense-ai
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup Ollama (for LLM agent)
brew install ollama
ollama pull mistral
ollama serve  # In a separate terminal

# 4. Start backend (Terminal 1)
python backend/main.py
# Output: Uvicorn running on http://0.0.0.0:8000

# 5. Start frontend (Terminal 2)
python frontend/src/app.py
# Output: Visit http://localhost:7860

# 6. Access
- Web UI: http://localhost:7860
- API Docs: http://localhost:8000/docs
- Swagger: http://localhost:8000/redoc
```

---

## Performance Metrics

| Metric          | Value            | Notes                               |
| --------------- | ---------------- | ----------------------------------- |
| Embedding Speed | 220 products/sec | M1 Pro, batch_size=64               |
| Search Latency  | <50ms            | FAISS IndexFlatIP                   |
| Dataset Size    | 10K products     | ~40MB CSV                           |
| Memory Usage    | ~1.2GB           | Embeddings + FAISS index            |
| Model Size      | 80MB             | sentence-transformers               |
| Scalability     | 1M+ products     | Ready with index optimization (IVF) |

### Optimization Opportunities (Production):

- **GPU Acceleration**: Use `faiss-gpu` for billion-scale indexes
- **Index Type**: Switch to `IndexIVFFlat` for approximate search on massive datasets
- **Caching**: Redis for popular queries (like we did in the capstone)
- **Quantization**: 8-bit embeddings reduce memory by 4x

---

## Security & Limitations

This is a **proof-of-concept**. The following are **intentionally not implemented**:

- ✗ **Authentication**: No API key validation or user authentication
- ✗ **Authorization**: No access control between users
- ✗ **Input Validation**: Minimal validation on API inputs
- ✗ **Rate Limiting**: No protection against abuse
- ✗ **HTTPS**: Runs on HTTP only
- ✗ **Logging/Monitoring**: No audit trails or analytics
- ✗ **Data Privacy**: No encryption at rest or in transit

---

## CI/CD & Deployment : Manual Deployment (current state)

- Local development setup
- Testing via API endpoints
- No automated pipelines
