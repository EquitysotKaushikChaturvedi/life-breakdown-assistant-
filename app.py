# app.py — Life Breakdown Assistant Backend

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging
import model  # Imports our new logic module

# Initialize
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the AI Brain
brain = model.LifeGuideAI()

app = FastAPI(
    title="Life Breakdown Assistant API",
    description="Backend for transforming life problems into structured JSON plans.",
    version="2.0"
)

# --- Schemas ---
class ChatMessage(BaseModel):
    role: str
    content: str
class ChatRequest(BaseModel):
    conversation_history: List[ChatMessage]
class ChatResponse(BaseModel):
    type: str 
    text: Optional[str] = None
    plan: Optional[model.FinalPlan] = None

# --- Routes ---

@app.get("/")
def read_root():
    """Serves the frontend interface."""
    return FileResponse('index.html')

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """
    Main endpoint.
    1. Checks for ambiguity (e.g. 'Help me').
    2. Otherwise, generates a full plan using the model.
    """
    history = req.conversation_history
    user_turns = len([m for m in history if m.role == 'user'])
    user_input = history[-1].content.strip()

    # 1. Ambiguity Check (Logic in app layer for fast response)
    if user_turns == 1:
        # Catch "Help me"
        if len(user_input.split()) < 3 and "help" in user_input.lower():
             return ChatResponse(type='question', text="I'm here to help. What specific goal are we planning today?")
        
        # Catch other vagueness if not a known topic
        if len(user_input.split()) < 3 and not brain.find_template(user_input):
             q = brain.safe_generate(f"Ask user for details about '{user_input}'. Question:", 30)
             if "question" in q.lower() or len(q) < 5: q = "Could you give me more details?"
             return ChatResponse(type='question', text=q)

    # 2. Plan Generation
    full_problem = " ".join([m.content for m in history if m.role == 'user'])
    
    # Delegate complex logic to the model
    plan = brain.infer_plan(full_problem)
    
    return ChatResponse(type='plan', plan=plan)

if __name__ == "__main__":
    print("Starting Life Breakdown Server...")
    print("Docs available at http://localhost:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
