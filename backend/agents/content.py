import os
import time
from google import genai
from backend.state import AgentState

# Maximum number of retry attempts per model when rate-limited
MAX_RETRIES = 2
RATE_LIMIT_WAIT = 35  # seconds (Google says "retry in 31s", we add buffer)

def run_content_agent(state: AgentState):
    print("--- Running Real Content Agent (2026 Stable) ---")
    
    product_name = state.get("discovered_product_name")
    suggested_price = state.get("suggested_price")
    
    if not product_name or not suggested_price:
        raise ValueError("Content Agent failed: Missing product data.")

    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("Content Agent failed: GEMINI_API_KEY is missing from .env")
    
    # Updated model list for 2026 (ordered by free-tier generosity)
    models_to_try = [
        "gemini-2.5-flash",     # Newest, most generous free tier
        "gemini-2.0-flash",     # Stable fallback
        "gemini-1.5-flash",     # Legacy but reliable
    ]
    
    client = genai.Client(api_key=gemini_api_key)
    html_description = None

    prompt = f"""
    You are an expert affiliate marketer. Write a highly persuasive, professional SEO HTML description for:
    Product: {product_name}
    Price: ${suggested_price}
    
    Requirements:
    1. Use HTML tags (<h2>, <p>, <ul>).
    2. Focus on sales benefits.
    3. Return only raw HTML.
    """

    for model_id in models_to_try:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"[Content] Attempting {model_id} (attempt {attempt}/{MAX_RETRIES})...")
                
                response = client.models.generate_content(
                    model=model_id,
                    contents=prompt
                )
                
                html_description = response.text.strip()
                if html_description.startswith("```html"):
                    html_description = html_description.replace("```html", "").replace("```", "").strip()
                    
                print(f"[Content] SUCCESS! Generated using {model_id}.")
                break  # Success — exit retry loop
                
            except Exception as e:
                error_str = str(e)
                print(f"[Content] {model_id} failed: {error_str[:120]}...")
                
                # If rate-limited (429), wait and retry the SAME model
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    if attempt < MAX_RETRIES:
                        print(f"[Content] Rate limited. Waiting {RATE_LIMIT_WAIT}s before retry...")
                        time.sleep(RATE_LIMIT_WAIT)
                        continue
                
                # If permission denied (403) or other error, skip to next model
                break
        
        if html_description:
            break  # Success — exit model loop

    if not html_description:
        raise Exception("Content Agent failed: All available AI models returned errors. "
                        "Please verify your GEMINI_API_KEY at https://aistudio.google.com/app/apikey")

    return {
        "current_agent": "Content",
        "html_description": html_description,
        "status": "awaiting_approval"
    }
