# knowledge_base.py
# Author: Kaushik Chaturvedi
# "Gold Standard" Templates to ground the AI.

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

def find_template(user_text):
    text_lower = user_text.lower()
    for key, data in TOPIC_TEMPLATES.items():
        if key == "general": continue
        for kw in data["keywords"]:
            if kw in text_lower:
                return data
    return None
