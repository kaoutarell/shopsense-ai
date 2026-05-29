"""
ShopSense AI — Shopify-Styled Gradio Frontend
==============================================

A merchant-facing interface for semantic product search and optimization.
Styled to match Shopify's design language (green, clean, professional).

SHOPIFY COLOR PALETTE:
- Primary Green: #008060
- Light Green: #E3F2ED
- Dark Gray: #202223
- Light Gray: #F6F6F7
- White: #FFFFFF
"""

import gradio as gr
import requests
import json
from typing import List, Dict

# ─────────────────────────────────────────────────────────
# API CONFIGURATION
# ─────────────────────────────────────────────────────────

API_BASE_URL = "http://localhost:8000"

# ─────────────────────────────────────────────────────────
# API FUNCTIONS
# ─────────────────────────────────────────────────────────

def semantic_search(query: str, top_k: int = 10) -> str:
    """Call the semantic search API and format results."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/search",
            json={"query": query, "top_k": top_k},
            timeout=10
        )
        
        if response.status_code != 200:
            return f" Error: {response.status_code}"
        
        data = response.json()
        
        if not data.get("results"):
            return " No products found. Try a different query!"
        
        # Format results beautifully
        output = f" **Search Results for:** \"{query}\"\n\n"
        output += f"**Found {data['total_results']} products:**\n\n"
        
        for i, product in enumerate(data["results"], 1):
            score = product.get("relevance_score", 0)
            score_pct = int(score * 100)
            
            # Visual relevance bar
            bar = "█" * (score_pct // 10) + "░" * (10 - score_pct // 10)
            
            output += f"**{i}. {product.get('title', 'Unknown')}**\n"
            output += f"   💰 Price: ${product.get('price', 'N/A'):.2f}\n"
            output += f"   🏪 Store: {product.get('store', 'Unknown')}\n"
            output += f"   📊 Relevance: [{bar}] {score_pct}%\n"
            output += f"   📝 Description: {product.get('description', '')[:100]}...\n\n"
        
        return output
        
    except requests.exceptions.ConnectionError:
        return " **Error:** Cannot connect to API. Is the backend running on port 8000?"
    except Exception as e:
        return f" **Error:** {str(e)}"


def get_recommendations(product_index: int, top_k: int = 5) -> str:
    """Get product recommendations similar to a given product."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/recommend",
            json={"product_index": product_index, "top_k": top_k},
            timeout=10
        )
        
        if response.status_code != 200:
            return f" Error: {response.status_code}"
        
        data = response.json()
        base_product = data.get("base_product", {})
        recommendations = data.get("recommendations", [])
        
        output = f" **Products Similar to:** \"{base_product.get('title', 'Unknown')}\"\n\n"
        output += f" Price: ${base_product.get('price', 'N/A'):.2f}\n"
        output += f" Store: {base_product.get('store', 'Unknown')}\n\n"
        
        output += f"**Similar Products ({len(recommendations)} found):**\n\n"
        
        for i, product in enumerate(recommendations, 1):
            similarity = product.get("similarity_score", 0)
            sim_pct = int(similarity * 100)
            
            bar = "█" * (sim_pct // 10) + "░" * (10 - sim_pct // 10)
            
            output += f"**{i}. {product.get('title', 'Unknown')}**\n"
            output += f"    Price: ${product.get('price', 'N/A'):.2f}\n"
            output += f"    Store: {product.get('store', 'Unknown')}\n"
            output += f"    Similarity: [{bar}] {sim_pct}%\n\n"
        
        return output
        
    except requests.exceptions.ConnectionError:
        return "**Error:** Cannot connect to API. Is the backend running?"
    except Exception as e:
        return f"**Error:** {str(e)}"


def get_pipeline_stats() -> str:
    """Get and display pipeline statistics."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/stats", timeout=10)
        
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        
        stats = response.json()
        
        output = " **ML Pipeline Statistics**\n\n"
        output += f"**Dataset:**\n"
        output += f"  • Total Products: {stats.get('total_products', 0):,}\n"
        output += f"  • Unique Stores: {stats.get('unique_stores', 0)}\n"
        output += f"  • Product Types: {stats.get('product_types', 0)}\n\n"
        
        output += f"**Embedding Model:**\n"
        output += f"  • Model: {stats.get('model', 'N/A')}\n"
        output += f"  • Dimensions: {stats.get('embedding_dimension', 0)}\n"
        output += f"  • Index Type: {stats.get('index_type', 'N/A')}\n\n"
        
        price_range = stats.get('price_range', {})
        if price_range:
            output += f"**Price Range:**\n"
            output += f"  • Min: ${price_range.get('min', 0):.2f}\n"
            output += f"  • Max: ${price_range.get('max', 0):,.2f}\n"
            output += f"  • Average: ${price_range.get('mean', 0):.2f}\n"
        
        return output
        
    except requests.exceptions.ConnectionError:
        return " **Error:** Cannot connect to API. Is the backend running on port 8000?"
    except Exception as e:
        return f" **Error:** {str(e)}"


# ─────────────────────────────────────────────────────────
# GRADIO INTERFACE
# ─────────────────────────────────────────────────────────

# Shopify color palette
SHOPIFY_GREEN = "#008060"
SHOPIFY_LIGHT_GREEN = "#E3F2ED"
SHOPIFY_DARK_GRAY = "#202223"
SHOPIFY_LIGHT_GRAY = "#F6F6F7"

# Custom CSS for Shopify styling
custom_css = """
:root {
    --primary: #008060;
    --light-green: #E3F2ED;
    --dark-gray: #202223;
    --light-gray: #F6F6F7;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif;
    background-color: var(--light-gray);
}

.gradio-container {
    background: var(--light-gray) !important;
    max-width: 1200px;
}

.gradio-button {
    background-color: var(--primary) !important;
    border-color: var(--primary) !important;
    font-weight: 600;
}

.gradio-button:hover {
    background-color: #006644 !important;
    border-color: #006644 !important;
}

.gradio-textbox input, .gradio-number input {
    border-color: var(--primary) !important;
}

.gradio-textbox input:focus, .gradio-number input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(0, 128, 96, 0.1) !important;
}

.tab-nav button.selected {
    border-bottom-color: var(--primary) !important;
    color: var(--primary) !important;
}

.gradio-accordion {
    border-color: var(--primary) !important;
}

h1, h2, h3 {
    color: var(--dark-gray) !important;
    font-weight: 600;
}
"""

# Create the interface
with gr.Blocks(
    title="ShopSense AI - Shopify Product Intelligence",
    theme=gr.themes.Soft(primary_hue="green"),
    css=custom_css
) as demo:
    
    # Header
    gr.HTML("""
    <div style="text-align: center; padding: 20px; background: white; border-bottom: 2px solid #008060;">
        <h1 style="margin: 0; color: #008060;">ShopSense AI</h1>
        <p style="margin: 10px 0 0 0; color: #666; font-size: 16px;">
            Intelligent Product Search & Discovery for Shopify Merchants
        </p>
    </div>
    """)
    
    with gr.Tabs():
        
        # TAB 1: SEMANTIC SEARCH
        with gr.Tab("🔍 Semantic Search", id="search"):
            gr.Markdown("""
            ### Find Products by Meaning, Not Just Keywords
            
            Type a natural language query and find relevant products across your catalog.
            The AI understands meaning, so "cozy gift for mom" will find cashmere blankets
            and soft slippers even if those exact words don't appear in the titles.
            """)
            
            with gr.Row():
                search_input = gr.Textbox(
                    label="What are you looking for?",
                    placeholder="e.g., 'cozy winter gift', 'running shoes for men', 'affordable skincare'",
                    lines=2
                )
            
            with gr.Row():
                top_k_search = gr.Slider(
                    minimum=1,
                    maximum=20,
                    value=10,
                    step=1,
                    label="Number of Results"
                )
            
            search_button = gr.Button(" Search", variant="primary")
            search_output = gr.Markdown()
            
            search_button.click(
                fn=semantic_search,
                inputs=[search_input, top_k_search],
                outputs=search_output
            )
        
        # TAB 2: RECOMMENDATIONS
        with gr.Tab(" Similar Products", id="recommend"):
            gr.Markdown("""
            ### "You Might Also Like" Feature
            
            Enter a product index and find similar products automatically.
            Great for building recommendation sections on product pages.
            """)
            
            with gr.Row():
                product_idx = gr.Number(
                    label="Product Index",
                    value=0,
                    precision=0,
                    info="Enter the index of a product (0-9981)"
                )
            
            with gr.Row():
                top_k_rec = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=5,
                    step=1,
                    label="Number of Recommendations"
                )
            
            recommend_button = gr.Button("⭐ Get Recommendations", variant="primary")
            recommend_output = gr.Markdown()
            
            recommend_button.click(
                fn=get_recommendations,
                inputs=[product_idx, top_k_rec],
                outputs=recommend_output
            )
        
        # TAB 3: PIPELINE STATS
        with gr.Tab(" Pipeline Info", id="stats"):
            gr.Markdown("""
            ### ML Pipeline Metrics
            
            View statistics about the embedding model, dataset, and vector index.
            """)
            
            stats_button = gr.Button(" Load Statistics", variant="primary")
            stats_output = gr.Markdown()
            
            stats_button.click(
                fn=get_pipeline_stats,
                inputs=[],
                outputs=stats_output
            )
            
            # Auto-load stats on tab open
            demo.load(
                fn=get_pipeline_stats,
                inputs=[],
                outputs=stats_output
            )
        
        # TAB 4: ABOUT
        with gr.Tab("ℹAbout", id="about"):
            gr.Markdown("""
            ## About ShopSense AI
            
            **ShopSense AI** is an intelligent product search and discovery engine 
            for Shopify merchants. It uses:
            
            - **Semantic Embeddings**: sentence-transformers/all-MiniLM-L6-v2
            - **Vector Search**: FAISS for ultra-fast similarity matching
            - **ML Architecture**: Production-ready Python + FastAPI backend
            
            ### Key Features
            
             **Semantic Search** - Find products by meaning, not keywords
            
             **Smart Recommendations** - Suggest similar products automatically
            
            **Real-time Analytics** - Monitor your ML pipeline performance
            
            ### Use Cases
            
            **Improve Product Discovery** - Help customers find products they'll love
            
            **Smart Recommendations** - Increase average order value with "You Might Also Like"
            
            **Better Search** - Replace keyword matching with semantic understanding
            
            ### Technical Details
            
            - **Products Indexed**: 9,982 products from 12 stores
            - **Embedding Dimensions**: 384 (compact but powerful)
            - **Search Latency**: <50ms per query
            - **Model**: all-MiniLM-L6-v2 (80MB, runs on CPU)
            
            ### Next Steps
            
            This prototype could be extended into a full Shopify app that:
            - Syncs with live Shopify stores via API
            - Provides merchant dashboard for analytics
            - Integrates search widget into storefronts
            - Offers AI-powered listing optimization
            
            **Built for the Shopify Applied ML Engineer role** 
            """)
    
    # Footer
    gr.HTML("""
    <div style="text-align: center; padding: 20px; color: #666; font-size: 12px; border-top: 1px solid #e0e0e0; margin-top: 40px;">
        <p>ShopSense AI © 2026 | Semantic Search Engine for Shopify | Built with 💜 using sentence-transformers & FAISS</p>
    </div>
    """)


# ─────────────────────────────────────────────────────────
# RUN THE APP
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🚀 ShopSense AI Gradio Frontend")
    print("📍 Visit: http://localhost:7860")
    print("⚠️  Make sure FastAPI backend is running on port 8000!")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )