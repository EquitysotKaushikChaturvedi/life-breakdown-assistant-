# Life Breakdown Assistant - Testing Guide

Here are 5 specific scenarios to test the different "modes" of your AI.

## 1. The Expert Test (Coding)
**Input:**
> "Guide me to learn Python from scratch."

**Why test this?**
Checks the `knowledge_base.py` retrieval.
**Expectation:**
- Root Causes: "Tutorial Hell", "Lack of practice".
- Steps: "Install VS Code", "Hello World".
- Timeline: Specific Day 1/Day 2 tasks.

## 2. The Fitness Test (Expert Mode)
**Input:**
> "I want to start going to the gym but I have no motivation."

**Why test this?**
Checks the fitness template in knowledge base.
**Expectation:**
- Psychology Tip: "Action creates motivation."
- 24h Plan: Pack bag tonight.

## 3. The General Logic Test (Unknown Topic)
**Input:**
> "How do I plan a surprise birthday party for my friend?"

**Why test this?**
Checks the **General Inference** fallback (since "party" isn't in the knowledge base).
**Expectation:**
- Custom inferred steps (Guest list, Venue, Food).

## 4. The "One-Question" Rule (Ambiguity Test)
**Input:**
> "Help me."

**Why test this?**
Checks the `user_input < 3 words` logic.
**Expectation:**
- The AI should **NOT** generate a plan yet.
- It should ask: *"Ask clarifying question about 'Help me' specific availability."*

## 5. The Decisive Mode (Speed Test)
**Input:**
> "I need a plan to clean my entire house in 4 hours on Saturday."

**Why test this?**
Checks if the AI skips questions when input is detailed.
**Expectation:**
- Immediate Plan generation.
