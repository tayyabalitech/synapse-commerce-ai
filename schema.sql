-- SQL Schema for the Human-in-the-Loop (HITL) queue

CREATE TABLE pending_actions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    agent_name TEXT NOT NULL,          -- e.g., 'Discovery_Agent', 'Content_Agent'
    action_type TEXT NOT NULL,         -- e.g., 'create_product', 'update_price'
    payload JSONB NOT NULL,            -- The actual data proposed by the AI (title, description, etc.)
    status TEXT DEFAULT 'pending',     -- Options: 'pending', 'approved', 'rejected'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Note: Since we disabled automatic Row Level Security (RLS) during setup, 
-- we do not need to write access policies here. Our FastAPI backend 
-- will handle data security.
