# ShopSense AI

>  A smart product search & discovery engine for Shopify stores / ML in e-commerce.

![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black&labelColor=0d1117)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=black&labelColor=0d1117)
![Mistral](https://img.shields.io/badge/Mistral-F97316?style=for-the-badge&logo=firefox&logoColor=white&labelColor=0d1117)
![HuggingFace](https://img.shields.io/badge/Hugging%20Face-8A2BE2?style=for-the-badge&logo=huggingface&logoColor=yellow&labelColor=0d1117)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white&labelColor=0d1117)
![TailwindCSS](https://img.shields.io/badge/Tailwind-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white&labelColor=0d1117)
![Shopify](https://img.shields.io/badge/Shopify-7AB55C?style=for-the-badge&logo=shopify&logoColor=white&labelColor=0d1117)

## Core Features:

1. Semantic Product Search : Buyers type natural language ("warm cozy gift for mom under $50") → AI finds the best matching products using embeddings + vector similarity
2. Product Description Optimizer : An AI agent that analyzes merchant product listings and suggests improvements for better discoverability
3. Smart Recommendations : "Customers who liked this also liked..." powered by embedding similarity
4. Product Clustering & Insights : Unsupervised ML to discover product categories and trends

## Why?

- Maps directly to "search, discovery, and agents" in the job description
- Demonstrates: embeddings, vector search, LLM agents, ML at scale concepts
- Built for commerce — not generic

## Tech Stack

| Layer         | Tool                                     | Why                             |
| ------------- | ---------------------------------------- | ------------------------------- |
| Embeddings    | `sentence-transformers/all-MiniLM-L6-v2` | Fast, runs locally on M1/M2/M3  |
| Vector Search | FAISS (by Meta)                          | Industry-standard, blazing fast |
| LLM           | Ollama + `mistral` or `llama3`           | Free, local, no API key needed  |
| Backend       | FastAPI (Python)                         | Clean, async, easy to deploy    |
| Frontend      | React + Tailwind                         | Polished demo UI                |
| Dataset       | Shopify product data (Kaggle)            | Real e-commerce data            |
| Deployment    | HuggingFace Spaces or Render             | Free hosting                    |

1. install ollama [DONE]
   `brew install ollama`

2. start ollama [DONE]
   `ollama serve`

3. pull the model out from ollama (Mistral) [DONE]
   `ollama pull mistral`

4. project architecture [DONE]
