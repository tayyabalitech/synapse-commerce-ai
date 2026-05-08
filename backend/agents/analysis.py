import os
from backend.state import AgentState
import serpapi

def run_analysis_agent(state: AgentState):
    print("--- Running Real Analysis Agent (Modern API) ---")
    product_name = state.get("discovered_product_name")
    
    if not product_name:
        raise ValueError("Analysis Agent failed: No product name was passed from the Discovery Agent.")

    # We will simulate a demand score based on string length just for fun
    demand_score = min(10, (len(product_name) % 5) + 5)
    
    serp_api_key = os.environ.get("SERPAPI_API_KEY")
    if not serp_api_key:
        raise ValueError("Analysis Agent failed: SERPAPI_API_KEY is missing from the .env file.")

    client = serpapi.Client(api_key=serp_api_key)
    
    target_country = state.get("target_country", "us")
    
    params = {
      "engine": "google_shopping",
      "q": product_name,
      "hl": "en",
      "gl": target_country
    }
    
    results = {}
    try:
        results = client.search(params)
    except Exception as e:
        print(f"[Analysis] SerpAPI error for region ({target_country}): {e}")
        
    prices = []
    try:
        # SerpApi returns a custom object, safely convert it to a standard dictionary
        res_dict = dict(results) if results else {}
        shopping_results = res_dict.get("shopping_results", [])
    except Exception:
        shopping_results = []

    
    if shopping_results:
        for item in shopping_results[:5]: # look at top 5 competitors
            extracted_price = item.get("extracted_price")
            if extracted_price:
                prices.append(extracted_price)
            
    # If we have no prices after checking the explicit region, halt.
    if not prices:
        raise Exception(f"Analysis Agent failed: Could not find any real competitor prices for '{product_name}' in the {target_country.upper()} market.")

    # Suggest a price slightly lower than the average to be competitive
    avg_price = sum(prices) / len(prices)
    suggested_price = round(avg_price * 0.95, 2)
    print(f"[Analysis] Competitor avg: ${avg_price:.2f}. Suggesting: ${suggested_price}")
            
    return {
        "current_agent": "Analysis",
        "demand_score": demand_score,
        "suggested_price": suggested_price
    }
