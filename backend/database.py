import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load the environment variables from the .env file
load_dotenv()

# Retrieve Supabase credentials securely from the environment
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

# Safety check to ensure the keys were loaded properly
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set in the .env file")

# Initialize and export the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
