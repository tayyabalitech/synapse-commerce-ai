import os
import random
import serpapi
from backend.state import AgentState

def run_discovery_agent(state: AgentState):
    print("--- Running Real Discovery Agent (SerpAPI Engine) ---")
    
    target_country = state.get('target_country', 'us')
    
    serp_api_key = os.environ.get("SERPAPI_API_KEY")
    if not serp_api_key:
        raise ValueError("Discovery Agent failed: SERPAPI_API_KEY is missing from the .env file.")

    client = serpapi.Client(api_key=serp_api_key)
    
    # Dynamically select a broad search term to discover a specific real product
    search_queries = [
        "best selling tech gadgets",
        "top rated smart home device",
        "trending electronic accessories",
        "popular wireless earbuds",
        "newest smart watches"
    ]
    broad_query = random.choice(search_queries)
    print(f"[Discovery] Querying SerpAPI ({target_country.upper()}) for: '{broad_query}'")
    
    params = {
      "engine": "google_shopping",
      "q": broad_query,
      "hl": "en",
      "gl": target_country
    }
    
    try:
        results = dict(client.search(params))
        shopping_results = results.get("shopping_results", [])
    except Exception as e:
        raise Exception(f"Discovery Agent failed: SerpAPI returned an error - {e}")
        
    if not shopping_results:
        raise Exception(f"Discovery Agent failed: Could not find any trending products for '{broad_query}' in the {target_country.upper()} region.")
        
    # Take the top organic shopping result.
    top_product = shopping_results[0]
    product_title = top_product.get("title")
    product_url = top_product.get("product_link", "https://google.com")
    
    if not product_title:
        raise Exception("Discovery Agent failed: Found a product but it had no title.")

    print(f"[Discovery] Success! Found real trending product: {product_title}")

    return {
        "current_agent": "Discovery", 
        "search_query": broad_query,
        "discovered_product_name": product_title,
        "discovered_product_url": product_url
    }
