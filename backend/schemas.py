"""
ShopSense AI — Request & Response Schemas
==========================================

Defines what the API inputs and outputs look like.
Uses Pydantic for automatic validation.
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any


# ─────────────────────────────────────────────────────────
# REQUEST MODELS (what clients send to us)
# ─────────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    """
    Natural language search request.
    
    Example:
    {
        "query": "cozy warm gift for mom",
        "top_k": 5
    }
    """
    query: str
    top_k: int = 10


class RecommendRequest(BaseModel):
    """
    Product recommendation request.
    
    Example:
    {
        "product_index": 42,
        "top_k": 5
    }
    """
    product_index: int
    top_k: int = 5


# ─────────────────────────────────────────────────────────
# RESPONSE MODELS (what we send back)
# ─────────────────────────────────────────────────────────

class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[Dict[str, Any]]


class RecommendResponse(BaseModel):
    product_index: int
    base_product: Dict[str, Any]
    total_recommendations: int
    recommendations: List[Dict[str, Any]]


class StatsResponse(BaseModel):
    total_products: int
    embedding_dimension: int
    model: str
    index_type: str
    unique_stores: Optional[int] = None
    product_types: Optional[int] = None
    price_range: Optional[Dict[str, float]] = None


class HealthResponse(BaseModel):
    status: str
    message: str