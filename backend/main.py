from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from backend.database import supabase
from backend.store import push_product_to_woocommerce

app = FastAPI(
    title="SynapseCommerce AI Backend",
    description="Backend for the Semi-Autonomous Affiliate Marketing Platform",
    version="1.0.0"
)

# Enable CORS so our Next.js frontend can talk to the Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you'd limit this to your dashboard URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "success", "message": "The SynapseCommerce AI Backend is running!"}

@app.post("/approve/{action_id}")
def approve_action(action_id: str):
    """
    Endpoint to trigger the real-world execution of an approved AI action.
    This is what makes your dashboard "live."
    """
    print(f"--- Processing Approval for Action ID: {action_id} ---")
    
    # 1. Fetch the action details from Supabase
    try:
        response = supabase.from_('pending_actions').select('*').eq('id', action_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Action not found in database.")
        
        action = response.data
        payload = action.get('payload', {})
        
        # 2. Push to WooCommerce using our new store module
        product_id = push_product_to_woocommerce(
            product_name=payload.get('product_name'),
            price=payload.get('price'),
            description=payload.get('description')
        )
        
        if product_id:
            # 3. Update Supabase status to 'completed'
            # (We removed the 'metadata' update because the column doesn't exist in your table yet)
            supabase.from_('pending_actions').update({
                "status": "completed"
            }).eq('id', action_id).execute()
            
            return {"status": "success", "message": "Product published!", "woo_product_id": product_id}

        else:
            raise HTTPException(status_code=500, detail="Failed to push product to WooCommerce.")
            
    except Exception as e:
        print(f"Approval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from pydantic import BaseModel
from typing import Optional

class DiscoveryPayload(BaseModel):
    country_code: Optional[str] = "us"
    trends_region: Optional[str] = "united_states"

@app.post("/run-discovery")
def manual_discovery_post(payload: DiscoveryPayload, background_tasks: BackgroundTasks):
    """
    Trigger discovery for a specific country selected from the UI.
    """
    background_tasks.add_task(autonomous_job, payload.country_code, payload.trends_region)
    return {"status": "success", "message": f"Discovery agent triggered for {payload.country_code} in background."}

@app.get("/run-discovery")
def manual_discovery_get(background_tasks: BackgroundTasks):
    """
    Fallback for manual browser testing (defaults to US).
    """
    background_tasks.add_task(autonomous_job, "us", "united_states")
    return {"status": "success", "message": "Discovery agent triggered for US in background."}

# --- AUTONOMOUS SCHEDULER ---
scheduler = BackgroundScheduler()

def autonomous_job(target_country: str = "us", trends_region: str = "united_states"):
    print(f"[{datetime.datetime.now()}] --- STARTING FULL AGENTIC PIPELINE FOR {target_country.upper()} ---")
    
    # 1. Initialize State
    state = {
        "target_country": target_country,
        "trends_region": trends_region,
        "search_query": None,
        "discovered_product_name": None,
        "discovered_product_url": None,
        "competitor_prices": [],
        "demand_score": 0,
        "suggested_price": 0,
        "seo_title": None,
        "html_description": None,
        "social_copy": None,
        "current_agent": "system",
        "status": "in_progress"
    }

    try:
        # Step 1: Discovery
        from backend.agents.discovery import run_discovery_agent
        discovery_results = run_discovery_agent(state)
        state.update(discovery_results)

        # Step 2: Analysis
        from backend.agents.analysis import run_analysis_agent
        analysis_results = run_analysis_agent(state)
        state.update(analysis_results)

        # Step 3: Content Generation
        from backend.agents.content import run_content_agent
        content_results = run_content_agent(state)
        state.update(content_results)

        # Step 4: Save to Database
        print("[System] Pipeline Complete. Saving to Supabase...")
        supabase.from_('pending_actions').insert({
            "agent_name": "Autonomous_Orchestrator",
            "action_type": "product_proposal",
            "payload": {
                "product_name": state["discovered_product_name"],
                "price": state["suggested_price"],
                "description": state["html_description"],
                "demand_score": state["demand_score"]
            },
            "status": "pending"
        }).execute()
        
        print(f"[{datetime.datetime.now()}] --- PIPELINE SUCCESS ---")

    except Exception as e:
        print(f"[{datetime.datetime.now()}] !!! PIPELINE FAILED !!!")
        print(f"Error: {e}")

# Schedule to run every day at 08:00 AM
scheduler.add_job(autonomous_job, 'cron', hour=8, minute=0)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
