"""
ShopSense AI — Configuration & Initialization
==============================================
 
This file handles all the setup and initialization.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.embedding_services import ProductEmbeddingService


print(f"Starting ShopSense ...")
print(f"Loading pre-built embedding index...")

embedding_services= ProductEmbeddingService()
embedding_services.load_index()

print(f"Index loaded!")