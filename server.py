# server.py — Robust Life Breakdown AI V4
# Author: Kaushik Chaturvedi
# Includes advanced error handling and knowledge base integration

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import logging
import re
import knowledge_base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Model Loading ---
AI_AVAILABLE = False
generator = None
try:
    from transformers import pipeline
    MODEL_ID = "google/flan-t5-base" 
    generator = pipeline("text2text-generation", model=MODEL_ID, max_length=512, truncation=True)
    AI_AVAILABLE = True
except Exception as e:
    logger.error(f"Failed to load AI: {e}")

app = FastAPI()

class ChatMessage(BaseModel):
    role: str
    content: str
class ChatRequest(BaseModel):
    conversation_history: List[ChatMessage]
class FinalPlan(BaseModel):
    root_causes: List[str]
    steps: List[str]
    timeline: Dict[str, str]
    psychology_tip: str
    action_plan_24h: Dict[str, str]
    problem: str
class ChatResponse(BaseModel):
    type: str 
    text: Optional[str] = None
    plan: Optional[FinalPlan] = None

# --- Logic ---

def safe_generate(prompt, max_tokens=64):
    if not AI_AVAILABLE: return ""
    try:
        # Lower temp for logic, N-gram penalty for repetition
        return generator(prompt, max_new_tokens=max_tokens, do_sample=True, temperature=0.5, repetition_penalty=1.5, no_repeat_ngram_size=2)[0]['generated_text'].strip()
    except: return ""

def get_expert_plan(problem):
    # 1. Try Retrieval
    template = knowledge_base.find_template(problem)
    
    if template:
        logger.info(f"RETRIEVAL SUCCESS: Found template.")
        return FinalPlan(**template, problem=problem)
    
    # 2. Fallback to General AI Inference (Improved Prompts)
    logger.info("RETRIEVAL FAILED: Using General Inference.")
    
    # Root Causes - Direct listing prompt
    c_raw = safe_generate(f"List 3 difficulties in '{problem}'. Difficulty 1:", 80)
    causes = [c.strip() for c in c_raw.split(',') if len(c)>4][:3]
    if len(causes) < 2: causes = ["Unclear Scope", "Lack of definition", "Starting friction"]

    # Steps - Direct action prompt
    s_raw = safe_generate(f"List 3 physical steps to finish '{problem}'. Step 1:", 100)
    steps = [s.strip() for s in s_raw.split(',') if len(s)>4][:4]
    if len(steps) < 2: steps = ["Define the exact goal", "Break it down", "Execute first task"]

    # Timeline - Direct prompt
    timeline = {
        "day_1": safe_generate(f"What is the single most important task for Day 1 of '{problem}'?", 40),
        "day_2": safe_generate(f"What is the task for Day 2 of '{problem}'?", 40),
        "week_1": safe_generate(f"What is the goal for Week 1 of '{problem}'?", 40)
    }

    # 24h
    action_plan = {
        "now": safe_generate(f"What is the very first tiny action for '{problem}' RIGHT NOW?", 40),
        "tonight": safe_generate(f"What preparation can be done TONIGHT for '{problem}'?", 40),
        "tomorrow": safe_generate(f"What is the main priority for TOMORROW regarding '{problem}'?", 40)
    }
    
    return FinalPlan(
        root_causes=causes,
        steps=steps,
        timeline=timeline,
        psychology_tip="Focus on progress, not perfection.",
        action_plan_24h=action_plan,
        problem=problem
    )

@app.get("/")
def read_root(): return FileResponse('index.html')

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    history = req.conversation_history
    user_turns = len([m for m in history if m.role == 'user'])
    user_input = history[-1].content.strip()

    # --- AMBIGUITY CHECK ---
    # Fix for "Help me" -> "Who wrote Help Me?" hallucination.
    # If input is super short and vague, we return a canned response.
    if user_turns == 1:
        if len(user_input.split()) < 3 and "help" in user_input.lower():
            return ChatResponse(type='question', text="I'm here to help. What specific goal are we planning today?")
        
        # General short input check
        if len(user_input.split()) < 3 and not knowledge_base.find_template(user_input):
             # Try to clarify 
             q = safe_generate(f"Ask user for details about '{user_input}'. Question:", 30)
             if "question" in q.lower() or len(q) < 5: q = "Could you give me more details?"
             return ChatResponse(type='question', text=q)
    
    # --- PLAN GENERATION ---
    full_problem = " ".join([m.content for m in history if m.role == 'user'])
    plan = get_expert_plan(full_problem)
    
    return ChatResponse(type='plan', plan=plan)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
