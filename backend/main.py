"""
ShopSense AI — FastAPI Server
==============================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from config import embedding_services
from schemas import SearchRequest, RecommendRequest, SearchResponse, RecommendResponse, HealthResponse


# -- INIT --

app = FastAPI(
    title="ShopeSense AI API",
    description="Semantic search engine for Shopify products",
    version="1.0.0"
)

# CORS : allow requests from other domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Endpoints

@app.get("/health")
async def health_check() -> HealthResponse:
    return HealthResponse(
        status= "ok",
        message= "ShopeSense AI API is running!"
    )

@app.post("/api/search")
async def semantic_search(request: SearchRequest):
    # NL prod search - semantinc embeddings
    results = embedding_services.search(request.query, top_k=request.top_k)

    return {
        "query": request.query,
        "total_results": len(results),
        "results": results
    }

@app.post("/api/recommend")
async def get_recommendation(request: RecommendRequest):
    base_product = embedding_services.products.iloc[request.product_index].to_dict()
    recommendations = embedding_services.get_similar_products(
        request.product_index,
        top_k=request.top_k
    )

    return {
        "product_index": request.product_index,
        "base_product": base_product,
        "total_recommendations": len(recommendations),
        "recommendations": recommendations
    }

@app.get("/api/stats")
async def get_stats():
    return embedding_services.get_stats()

# === M A I N ===

if __name__ == "__main__" :
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)