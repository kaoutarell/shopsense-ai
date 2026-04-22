"""
ShopSense AI — Product Data Scraper
====================================
This script scrapes product data from PUBLIC Shopify stores.

HOW IT WORKS:
Every Shopify store exposes a public JSON API at /products.json
This is NOT hacking — Shopify intentionally makes this public for 
integrations, apps, and developers. It's part of their platform.

The URL pattern is:
  https://store-name.myshopify.com/products.json?limit=250&page=1

Each response contains up to 250 products with all their details:
title, description, price, images, vendor, tags, etc.

We scrape multiple stores to build a diverse product catalog,
then clean and save it as a CSV for our embedding pipeline.
"""

import requests      # for HTTP requests to Shopify APIs
import pandas as pd  # for organizing data into a table 
import time          # for adding delays between requests
import re            # REGEX to clean HTML from descriptions
import json
import os

# random online stores per category
STORES = [
    # Fashion & Apparel
    "kith.com",
    "fentybeauty.com",
    "gymshark.com",
    "fashionnova.com",
    "colourpop.com",
    
    # Home & Lifestyle
    "brooklinen.com",
    "ruggable.com",
    
    # Food & Drink
    "deathwishcoffee.com",
    "mudwtr.com",
    
    # Tech & Gadgets
    "peakdesign.com",
    "analogue.co",
    
    # Wellness & Beauty
    "kylicosmetics.com",
    "skims.com",
    "hauslabs.com",
    
    # Outdoor & Sports
    "alfrfresco.com",
    "chubbiesshorts.com",
    
    # General / Misc
    "bombas.com",
    "allbirds.com",
    "heinz.com",
]



def scrape_store(domain: str, max_pages: int = 5) -> list:
    """
    Scrape products from a single Shopify store.
    
    HOW PAGINATION WORKS:
    - Shopify returns max 250 products per page
    - We request page=1, page=2, etc. until we get an empty list
    - max_pages caps how many pages we fetch (safety limit)
    
    RETURNS: A list of dictionaries, one per product.
    """
    all_products = []
    
    for page in range(1, max_pages + 1):
        # API URL
        # limit=250 : maximum products per request
        # page=N : pagination
        url = f"https://{domain}/products.json?limit=250&page={page}"
        
        try:
            # HTTP GET request
            # timeout=15
            response = requests.get(url, timeout=15, headers={
                # Identify the service during the scrapping process
                "User-Agent": "ShopSense-AI-Research/1.0"
            })
            
            if response.status_code != 200:
                print(f"Warning : {domain} returned status {response.status_code}, skipping")
                break
            
            # parse json response
            data = response.json()
            products = data.get("products", [])
            
            # reached the end
            if not products:
                break
            
            # processing each product
            for product in products:
                # Each product has "variants" : different sizes/colors/etc.
                # Logic : take the first variant's price as the main price
                price = None
                if product.get("variants"):
                    price = product["variants"][0].get("price")
                
                # get the first image URL if available
                image_url = None
                if product.get("images"):
                    image_url = product["images"][0].get("src")
                
                # clean product record
                record = {
                    "title": product.get("title", ""),
                    "description": product.get("body_html", ""),  # HTML format
                    "vendor": product.get("vendor", ""),
                    "product_type": product.get("product_type", ""),
                    "tags": ", ".join(product.get("tags", [])),  # List → string
                    "price": price,
                    "image_url": image_url,
                    "store": domain,
                    "handle": product.get("handle", ""),  # URL-friendly name
                    "created_at": product.get("created_at", ""),
                }
                all_products.append(record)
            
            print(f"Page {page}: got {len(products)} products")
            
            # buffer of 1 second between requests to prevent server overwhelming
            time.sleep(1)
            
        except requests.exceptions.Timeout:
            print(f"{domain} timed out, skipping")
            break
        except requests.exceptions.ConnectionError:
            print(f"{domain} connection failed, skipping")
            break
        except Exception as e:
            print(f"{domain} error: {e}")
            break
    
    return all_products


def clean_html(html_text: str) -> str:
    """
    Remove HTML tags from product descriptions.
    
    WHY: Shopify stores descriptions as HTML (with <p>, <br>, <strong>, etc.)
    We need plain text for our embedding model — it doesn't understand HTML.
    
    EXAMPLE:
        Input:  "<p>This <strong>amazing</strong> shirt is...</p>"
        Output: "This amazing shirt is..."
    """
    if not html_text or not isinstance(html_text, str):
        return ""
    
    # remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', html_text)
    
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&#39;', "'")
    text = text.replace('&quot;', '"')
    
    # collapse spaces/newlines into single space
    text = re.sub(r'\s+', ' ', text)
    
    # leading/trailing whitespace
    return text.strip()


### PIPELINE ###

def main():
    """
    Main function — orchestrates the entire scraping pipeline.
    
    FLOW:
    1. Loop through all stores and scrape products
    2. Combine everything into a pandas DataFrame
    3. Clean the data (remove HTML, handle missing values, etc.)
    4. Save to CSV
    """
    
    print("=" * 60)
    print("🛒 ShopSense AI — Product Data Scraper")
    print("=" * 60)
    
    all_products = []
    successful_stores = 0
    
    # ── Scrape each store ──
    for i, store in enumerate(STORES, 1):
        print(f"\n[{i}/{len(STORES)}] Scraping {store}...")
        
        products = scrape_store(store)
        
        if products:
            all_products.extend(products)
            successful_stores += 1
            print(f"Got {len(products)} products from {store}")
        else:
            print(f"No products from {store}")
        
        # buffer between stores - easy on the server
        time.sleep(2)
    
    print(f"\n{'=' * 60}")
    print(f"Scraped {len(all_products)} total products from {successful_stores} stores")
    print(f"{'=' * 60}")
    
    if not all_products:
        print("No products scraped! Check your internet connection.")
        return
    
    # ── DataFrame ──
    df = pd.DataFrame(all_products)
    
    # ── Clean descriptions ──
    print("\n🧹 Cleaning descriptions...")
    df['description'] = df['description'].apply(clean_html)
    
    # ── Handle missing/bad data ──
    
    # we dont want rows where title is empty -- not helping
    df = df[df['title'].str.len() > 0]
    
    # fill missing descriptions with empty string
    df['description'] = df['description'].fillna('')
    
    # convert string price to float
    # errors='coerce' : if it can't convert, set to NaN to prevent from crashing
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    
    # drop products with no price 
    df = df.dropna(subset=['price'])
    
    # drop products with price = 0
    df = df[df['price'] > 0]
    
    # remove dupe products (same title + same store)
    df = df.drop_duplicates(subset=['title', 'store'])
    
    # reset the index (row numbers) after dropping rows
    df = df.reset_index(drop=True)
    
    # ── Create a combined text field for embeddings ──
    # This is what the embedding model will receive as a prompt :
    # combination of title + description + tags gives richer semantic meaning
    df['embedding_text'] = (
        df['title'] + ". " + 
        df['description'].str[:500] + ". " +  
        "Category: " + df['product_type'] + ". " +
        "Tags: " + df['tags']
    )
    
    # ── Save to CSV ──
    output_dir = "backend/data"
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    
    output_path = os.path.join(output_dir, "products.csv")
    df.to_csv(output_path, index=False)
    # index=False : don't save the row numbers as a column
    
    # ── Print summary stats ──
    print(f"\n{'=' * 60}")
    print(f"DONE! Saved {len(df)} clean products to {output_path}")
    print(f"{'=' * 60}")
    print(f"\n Dataset Summary:")
    print(f"   Total products:  {len(df)}")
    print(f"   Unique stores:   {df['store'].nunique()}")
    print(f"   Product types:   {df['product_type'].nunique()}")
    print(f"   Price range:     ${df['price'].min():.2f} — ${df['price'].max():.2f}")
    print(f"   Avg price:       ${df['price'].mean():.2f}")
    print(f"   Avg description: {df['description'].str.len().mean():.0f} characters")
    print(f"\n Columns saved: {list(df.columns)}")
    
    # show few sample products
    print(f"\n Sample products:")
    for _, row in df.head(5).iterrows():
        desc_preview = row['description'][:80] + "..." if len(row['description']) > 80 else row['description']
        print(f"   • ${row['price']:.2f} | {row['title'][:50]} | {row['store']}")


if __name__ == "__main__":
    main()