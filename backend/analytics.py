import os
from backend.store import wcapi
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_sales_report():
    print("--- Running SynapseCommerce AI Business Analytics ---")
    
    try:
        # 1. Fetch recent data from WooCommerce
        # Checking orders (last 10)
        orders_response = wcapi.get("orders", params={"per_page": 10})
        orders = orders_response.json() if orders_response.status_code == 200 else []
        
        # Checking total products
        products_response = wcapi.get("products")
        products = products_response.json() if products_response.status_code == 200 else []
        
        # 2. Prepare the data for the AI
        total_revenue = sum(float(order['total']) for order in orders)
        product_count = len(products)
        order_count = len(orders)
        
        data_summary = f"""
        Store Performance Data:
        - Total Products in Catalog: {product_count}
        - Recent Orders Tracked: {order_count}
        - Total Revenue from Recent Orders: ${total_revenue}
        - Store URL: {os.environ.get('WOO_STORE_URL')}
        """
        
        # 3. Use Gemini 2.0 to generate a professional brief
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        
        prompt = f"""
        You are the SynapseCommerce AI Business Analyst. Summarize this store's performance and provide a strategy for the next 7 days.
        
        Current Data:
        {data_summary}
        
        Provide the report in the following format:
        1. Executive Summary
        2. Inventory Health
        3. Strategic Recommendations (3 specific niches to discover next)
        """
        
        print("[Analytics] Analyzing store data with AI...")
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt
        )
        
        print("\n" + "="*50)
        print("          SYNAPSE AI BUSINESS BRIEF")
        print("="*50)
        print(response.text)
        print("="*50)
        
    except Exception as e:
        print(f"[Analytics] Error generating report: {e}")

if __name__ == "__main__":
    generate_sales_report()
