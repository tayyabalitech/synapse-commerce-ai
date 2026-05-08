from typing import TypedDict, Optional, List

class AgentState(TypedDict):
    """
    The central data structure (State) that gets passed between all our AI agents.
    Each agent will read from this state, perform its task, and update the state.
    """
    # ---------------- System Configuration ----------------
    target_country: str                  # e.g., 'us', 'uk', 'pk'
    trends_region: str                   # e.g., 'united_states', 'pakistan'
    
    # ---------------- Domain 1: Discovery ----------------
    search_query: Optional[str]
    discovered_product_name: Optional[str]
    discovered_product_url: Optional[str]
    
    # ---------------- Domain 2: Analysis -----------------
    competitor_prices: Optional[List[float]]
    demand_score: Optional[int]          # A score out of 10
    suggested_price: Optional[float]
    
    # ---------------- Domain 3: Content ------------------
    seo_title: Optional[str]
    html_description: Optional[str]
    social_copy: Optional[str]
    
    # ---------------- System Variables -------------------
    current_agent: str                   # Tracks which agent is currently working
    status: str                          # e.g., 'in_progress', 'awaiting_approval', 'completed'
