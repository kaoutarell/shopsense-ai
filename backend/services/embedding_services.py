"""
ShopSense AI — Embedding Service
==================================
The CORE ML component.
 
WHAT IT DOES:
1. Loads your 10K product CSV
2. Converts every product into a 384-dimensional vector (embedding) using a pre-trained transformer model
3. Stores all vectors in a FAISS index for ultra-fast similarity search
4. Enables semantic search
 
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
import pickle
import os
import time

class ProductEmbeddingService:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print(f"Model loaded: Output dimension : {self.model.get_embedding_dimension()}")

        self.index = None
        self.products = None
        self.embeddings = None

    # ─────────────────────────────────────────────────────────
    # BUILD: Generate embeddings and create FAISS index
    # ─────────────────────────────────────────────────────────

    def build_index(self, csv_path: str = "backend/data/products.csv"):
        # -- Load Data --
        print(f"\n Loading products from {csv_path}...")
        self.products = pd.read_csv(csv_path)
        print(f"Loaded {len(self.products)} products")

        # -- Preparing text for embeddings --
        texts = self.products['embedding_text'].fillna('').tolist()
        
        print(f"\n Generating embeddings for {len(texts)} products...")
        print(f"(This may take more than a minute)")

        start_time = time.time()

        self.embeddings = self.model.encode(
            texts,
            batch_size=64,
            show_progress_bar=True,
            normalize_embeddings=True, #VERY CRITICAL
            convert_to_numpy=True
        )

        elapsed = time.time() - start_time
        rate = len(texts)/elapsed

        print(f"Generated {self.embeddings.shape[0]} embeddings of dimension {self.embeddings.shape[1]}")
        print(f"Took {elapsed:.1f}s ({rate:0f} products/s)")

        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(self.embeddings.astype('float32'))

        print(f"FAISS index built successfully! {self.index.ntotal} vectors indexed")

        # -- Save to disk -- 
        self.save_index()

        print(f"\n We are ready for semantic searching now!")


    # ─────────────────────────────────────────────────────────
    # SEARCH: Natural language → relevant products
    # ─────────────────────────────────────────────────────────

    def search(self, query: str, top_k:int = 10) -> list:
        if self.index is None:
            raise ValueError("Index not loaded!")
        
        # -- Encode query into the same dim space as products --
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype('float32')

        # -- Search FAISS index --
        scores, indices = self.index.search(query_embedding, top_k)

        # -- Build results --
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1: #empty slot
                continue

            product = self.products.iloc[idx].to_dict()
            product['relevance_score'] = round(float(score), 4)
            product['product_index'] = int(idx)
            results.append(product)

        return results
    
    # ─────────────────────────────────────────────────────────
    # Find similar products
    # ─────────────────────────────────────────────────────────

    def get_similar_products(self, product_idx:int, top_k:int=5) -> list:
        if self.index is None:
            raise ValueError("Index not loaded!")
        
        # -- Get product's vector from index
        product_embedding = self.index.reconstruct(product_idx).reshape(1, -1)
        scores, indices = self.index.search(product_embedding, top_k+1)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == product_idx or idx == -1:
                continue # skip self

            product = self.products.iloc[idx].to_dict()
            product['similarity_score'] = round(float(score), 4)
            product['product_index'] = int(idx)
            results.append(product)

        return results[:top_k] # top matches
    
    # ─────────────────────────────────────────────────────────
    # SAVE / LOAD TO DISK
    # ─────────────────────────────────────────────────────────

    def save_index(self, data_dir: str = "backend/data"):
        os.makedirs(data_dir, exist_ok=True)

        # -- Save FAISS in binary format --
        faiss.write_index(self.index, os.path.join(data_dir, "product_index.faiss"))
        # -- Save product Dataframe --
        self.products.to_pickle(os.path.join(data_dir, "products.pkl")) 
        # -- Save raw embedding --
        np.save(os.path.join(data_dir, "embeddings.npy"), self.embeddings) # needed for clustering

        print(f"Saved index, products, and embeddings to {data_dir}/")

    
    def load_index(self, data_dir: str = "backend/data"):
        print(f"Loading pre-built index from {data_dir}/...")

        self.index = faiss.read_index(os.path.join(data_dir, "product_index.faiss"))
        self.products = pd.read_pickle(os.path.join(data_dir, "products.pkl"))
        self.embeddings = np.load(os.path.join(data_dir, "embeddings.npy"))

        print(f"Loaded {self.index.ntotal} products into FAISS index")


    # ─────────────────────────────────────────────────────────
    # STATS: Pipeline metrics (for the dashboard)
    # ─────────────────────────────────────────────────────────
    def get_stats(self) -> dict:
        stats = {
            "total_products": int(self.index.ntotal) if self.index else 0,
            "embedding_dimension": 384,
            "model": "all-MiniLM-L6-v2",
            "index_type": "FAISS IndexFlatIP (cosine similarity)"
        }

        if self.products is not None:
            stats["unique_stores"] = int(self.products['store'].nunique())
            stats["products_types"] = int(self.products['product_type'].nunique())
            stats["price_range"] = {
                "min": float(self.products['price'].min()),
                "max": float(self.products['price'].max()),
                "mean": round(float(self.products['price'].mean()), 2)
            }
        
        return stats
    
    

    # ─────────────────────────────────────────────────────────
    # --------------------- M A I N ---------------------------
    # ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    service = ProductEmbeddingService()
    service.build_index()

    # -- Test --
    print("\n" + "=" * 60)
    print(f"Test begins ...")
    print("=" * 60)

    test_queries = [
        "cozy warm gift for mom",
        "running shoes for men",
        "affordable skincare routine",
        "minimalist home decor",
        "high protein coffee alternative",
    ]

    for query in test_queries:
        print(f"\n Query: \"{query}\"")
        results = service.search(query, top_k=3)
        for r in results:
            print(f"→ ${r['price']:.2f} | {r['title'][:55]} "
                f"| score: {r['relevance_score']:.3f} | {r['store']}")
            
    # -- Recommendations --
    print(f"\n{'=' * 60}")
    print("Preparing Products Recommendations...")
    print("=" * 60)

    print(f"\n Products similar to: \"{service.products.iloc[0]['title']}\"")

    recs = service.get_similar_products(0, top_k=3)

    for r in recs:
        print(f"   → ${r['price']:.2f} | {r['title'][:55]} "
            f"| similarity: {r['similarity_score']:.3f}")
        
    # -- Stats --
    print(f"\n{'=' * 60}")
    print("Pipeline Stats")
    print("=" * 60)
    import json
    print(json.dumps(service.get_stats(), indent=2))

