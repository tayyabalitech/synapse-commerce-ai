import json
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from backend.state import AgentState
from backend.database import supabase
from backend.agents.discovery import run_discovery_agent
from backend.agents.analysis import run_analysis_agent
from backend.agents.content import run_content_agent

# ==========================================
# 1. Define the Nodes (The Agents)
# ==========================================

# The Discovery Agent is now imported from backend.agents.discovery


# The Analysis Agent is now imported from backend.agents.analysis


# The Content Agent is now imported from backend.agents.content


def request_human_approval(state: AgentState):
    print("--- Requesting Human Approval (Writing to Supabase) ---")
    
    # Package the AI's proposal
    payload = {
        "product_name": state.get("discovered_product_name"),
        "price": state.get("suggested_price"),
        "description": state.get("html_description")
    }
    
    # Write to our pending_actions table
    response = supabase.table("pending_actions").insert({
        "agent_name": "Content_Agent",
        "action_type": "create_product",
        "payload": payload,
        "status": "pending"
    }).execute()
    
    print(f"Task successfully written to Supabase! Database ID: {response.data[0]['id']}")
    return {"status": "awaiting_approval"}

# ==========================================
# 2. Build the Graph
# ==========================================

workflow = StateGraph(AgentState)

# Add the nodes
workflow.add_node("Discovery_Node", run_discovery_agent)
workflow.add_node("Analysis_Node", run_analysis_agent)
workflow.add_node("Content_Node", run_content_agent)
workflow.add_node("HITL_Node", request_human_approval)

# Define the edges
workflow.add_edge(START, "Discovery_Node")
workflow.add_edge("Discovery_Node", "Analysis_Node")
workflow.add_edge("Analysis_Node", "Content_Node")
workflow.add_edge("Content_Node", "HITL_Node")
workflow.add_edge("HITL_Node", END)

# We use MemorySaver to give the graph "memory" across paused states
memory = MemorySaver()

# Compile the graph
app_graph = workflow.compile(checkpointer=memory)
