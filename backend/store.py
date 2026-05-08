import os
from woocommerce import API
from dotenv import load_dotenv

load_dotenv()

# Initialize the WooCommerce API client
wcapi = API(
    url=os.environ.get("WOO_STORE_URL"),
    consumer_key=os.environ.get("WOO_CONSUMER_KEY"),
    consumer_secret=os.environ.get("WOO_CONSUMER_SECRET"),
    version="wc/v3"
)

def push_product_to_woocommerce(product_name, price, description):
    """
    Official function to create a new product in your WooCommerce store.
    """
    data = {
        "name": product_name,
        "type": "simple", # Standard physical or affiliate product
        "regular_price": str(price),
        "description": description, # The SEO HTML we generated
        "short_description": "Auto-discovered trending product by Synapse AI.",
        "status": "publish", # Making it live immediately
        "manage_stock": False,
        "in_stock": True
    }

    print(f"[Store] Pushing '{product_name}' to WooCommerce...")
    
    try:
        response = wcapi.post("products", data)
        
        if response.status_code == 201:
            product_id = response.json().get('id')
            print(f"[Store] Success! Product created with ID: {product_id}")
            return product_id
        else:
            print(f"[Store] Error from WooCommerce: {response.text}")
            return None
            
    except Exception as e:
        print(f"[Store] Connection error: {e}")
        return None

def test_connection():
    try:
        response = wcapi.get("products")
        if response.status_code == 200:
            print("Successfully connected to WooCommerce!")
            return True
        return False
    except:
        return False

if __name__ == "__main__":
    # If run directly, we'll just test the connection
    test_connection()
