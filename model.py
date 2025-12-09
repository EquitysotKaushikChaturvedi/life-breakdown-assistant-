# model.py — AI Logic Layer
# Handles RAG (Retrieval) and Generative Inference
# Encapsulates:
# 1. RAG-lite Knowledge Base (Gold Standard Templates)
# 2. Hugging Face T5 Model (Inference)
# 3. Logic for Plan Generation

import logging
import re
from typing import List, Dict, Optional
from pydantic import BaseModel

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 1. Knowledge Base ---
# Hardcoded expert templates to prevent hallucinations/generic answers.
TOPIC_TEMPLATES = {
    "coding": {
        "keywords": ["code", "coding", "programming", "python", "javascript", "developer", "software"],
        "root_causes": ["Information Overload", "Lack of consistent practice", "Giving up when stuck"],
        "steps": ["Choose ONE language (e.g. Python)", "Watch a 1-hour crash course", "Build a 'Hello World' app", "Modify specific code to learn"],
        "timeline": {
            "day_1": "Install VS Code and Python/Node",
            "day_2": "Write first 10 lines of code",
            "week_1": "Build a Calculator or To-Do app"
        },
        "action_plan_24h": {
            "now": "Decide: Python for data or JS for web?",
            "tonight": "Install the code editor",
            "tomorrow": "Watch 30 mins of a tutorial"
        },
        "psychology_tip": "Coding is 10% writing, 90% debugging. Don't panic when it breaks."
    },
    "fitness": {
        "keywords": ["gym", "workout", "fitness", "weight", "muscle", "fat", "run"],
        "root_causes": ["Reliance on motivation vs discipline", "Unrealistic early goals", "Poor recovery/sleep"],
        "steps": ["Define a fixed schedule (Time/Days)", "Prepare gear the night before", "Start with 20 min sessions", "Track every workout"],
        "timeline": {
            "day_1": "Do a 20-min test workout at home",
            "day_2": "Rest or light walk + Stretch",
            "week_1": "Complete 3 total sessions"
        },
        "action_plan_24h": {
            "now": "Put workout clothes in a visible spot",
            "tonight": "Sleep 8 hours for recovery",
            "tomorrow": "Go to gym/park at 7 AM sharp"
        },
        "psychology_tip": "The hardest lift is lifting your butt off the couch."
    },
    "party": {
        "keywords": ["party", "birthday", "surprise", "celebration", "event"],
        "root_causes": ["Last minute panic", "Budget creep", "Guest list confusion"],
        "steps": ["Set a strict budget and date", "Secure the venue (or house)", "Send invites immediately", "Plan food and music"],
        "timeline": {
            "day_1": "Create guest list and pick date",
            "day_2": "Book venue or order supplies",
            "week_1": "Confirm RSVPs and menu"
        },
        "action_plan_24h": {
            "now": "Message the key best friend for help",
            "tonight": "Draft the guest list",
            "tomorrow": "Send out the 'Save the date'"
        },
        "psychology_tip": "People remember the vibe, not the napkin color. Focus on fun."
    },
    "cleaning": {
        "keywords": ["clean", "cleaning", "house", "chore", "mess", "declutter"],
        "root_causes": ["Overwhelmed by scale", "No system (room by room)", "Distractions"],
        "steps": ["Start with trash and dishes", "Pick one room at a time", "Set a timer for 20 mins", "Don't organize, just clean"],
        "timeline": {
            "day_1": "Trash, Laundry, and Kitchen surfaces",
            "day_2": "Bathrooms and Floors",
            "week_1": "Deep clean windows and dusting"
        },
        "action_plan_24h": {
            "now": "Put on music and shoes",
            "tonight": "Do the dishes before bed",
            "tomorrow": "Tackle the living room first thing"
        },
        "psychology_tip": "Don't put it down, put it away. Momentum is key."
    },
    "general": {
        "keywords": [],
        "root_causes": ["Lack of Clarity", "Fear of Failure", "No Accountability"],
        "steps": ["Define the goal clearly", "Break into small pieces", "Schedule the first piece", "Review progress"],
        "timeline": {
            "day_1": "Research and Analysis",
            "day_2": "Initial Setup/Prototype",
            "week_1": "First Tangible Milestone"
        },
        "action_plan_24h": {
            "now": "Write the goal on paper",
            "tonight": "Clear schedule for tomorrow",
            "tomorrow": "Execute the first hour of work"
        },
        "psychology_tip": "Action creates motivation, not the other way around."
    }
}

# --- 2. Data Models ---
class FinalPlan(BaseModel):
    root_causes: List[str]
    steps: List[str]
    timeline: Dict[str, str]
    psychology_tip: str
    action_plan_24h: Dict[str, str]
    problem: str

# --- 3. AI Class ---
class LifeGuideAI:
    def __init__(self):
        self.generator = None
        self.available = False
        self.load_model()

    def load_model(self):
        try:
            from transformers import pipeline
            MODEL_ID = "google/flan-t5-base"
            logger.info(f"Loading {MODEL_ID}...")
            # Utilizing local cache if available
            self.generator = pipeline("text2text-generation", model=MODEL_ID, max_length=512, truncation=True)
            self.available = True
            logger.info("AI Model Loaded Successfully.")
        except Exception as e:
            logger.error(f"Failed to load AI: {e}")
            self.available = False

    def find_template(self, text):
        """RAG-lite Retrieval"""
        text_lower = text.lower()
        for key, data in TOPIC_TEMPLATES.items():
            if key == "general": continue
            for kw in data["keywords"]:
                if kw in text_lower:
                    return data
        return None

    def safe_generate(self, prompt, max_tokens=64):
        if not self.available: return "Mock AI Response"
        try:
            # Discrete prompting strategy
            return self.generator(
                prompt, max_new_tokens=max_tokens, 
                do_sample=True, temperature=0.5, 
                repetition_penalty=1.5, no_repeat_ngram_size=2
            )[0]['generated_text'].strip()
        except: return "Analysis Error"

    def infer_plan(self, problem: str) -> FinalPlan:
        # 1. Try Retrieval
        template = self.find_template(problem)
        if template:
            logger.info(f"Using Knowledge Base for: {problem}")
            return FinalPlan(**template, problem=problem)

        # 2. General Inference
        logger.info(f"Using AI Inference for: {problem}")
        
        # Helper to clean lists
        def clean(raw, fallback):
            items = [i.strip() for i in raw.split(',') if len(i.strip()) > 3]
            return items[:4] if len(items) >= 2 else fallback

        # Generate Fields
        raw_causes = self.safe_generate(f"List 3 distinct difficulties in '{problem}'. Difficulty 1:", 80)
        causes = clean(raw_causes, ["Unclear Scope", "Inertia", "Lack of definition"])

        raw_steps = self.safe_generate(f"List 4 physical actions to finish '{problem}'. Step 1:", 100)
        steps = clean(raw_steps, ["Plan", "Prepare", "Execute", "Review"])

        timeline = {
            "day_1": self.safe_generate(f"Task for Day 1 of '{problem}'?", 40),
            "day_2": self.safe_generate(f"Task for Day 2 of '{problem}'?", 40),
            "week_1": self.safe_generate(f"Goal for Week 1 of '{problem}'?", 40)
        }

        action_plan = {
            "now": self.safe_generate(f"Tiny action for '{problem}' RIGHT NOW?", 40),
            "tonight": self.safe_generate(f"Prep task for '{problem}' TONIGHT?", 40),
            "tomorrow": self.safe_generate(f"Priority for '{problem}' TOMORROW?", 40)
        }

        return FinalPlan(
            root_causes=causes,
            steps=steps,
            timeline=timeline,
            psychology_tip="Start before you feel ready.",
            action_plan_24h=action_plan,
            problem=problem
        )
