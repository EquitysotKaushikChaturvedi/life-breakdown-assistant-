# Life Breakdown Assistant (Backend)
**Created by: Kaushik Chaturvedi**

## 1. Project Overview
This project is an advanced AI-powered assistant designed to break down complex life problems into manageable, actionable steps. It utilizes a hybrid approach combining a static **Expert Knowledge Base** for reliability and a **Generative AI Model** (`flan-t5-base`) for flexible reasoning.

## 2. Project Architecture & Files
This project follows a clean, modular architecture:

*   **`app.py`**: The main entry point. A robust **FastAPI** server that handles incoming requests and serves the frontend.
*   **`model.py`**: The "Brain" of the operation. It manages the AI model loading, inference logic, and integrates with the knowledge base.
*   **`knowledge_base.py`**: Contains "Gold Standard" expert templates for common topics (like Fitness, Coding, Cleaning) to ensure high-quality advice without hallucinations.
*   **`server.py`**: An alternative/advanced server implementation including experimental features and expanded error handling.
*   **`train.py`**: A script for fine-tuning the underlying model on specific instructional datasets, demonstrating the project's extensibility.
*   **`sample_output.json`**: An example of the structured JSON response the API generates, ensuring frontend compatibility.

## 3. How to Install
Follow these steps to set up the backend locally:

1.  **Install Python**: Ensure you have Python 3.9+ installed.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Server**:
    ```bash
    python app.py
    ```
4.  **Access the API**:
    *   The server runs at `http://localhost:8000`.
    *   Interactive API Docs (Swagger): `http://localhost:8000/docs`.

## 3. Which Model is Used?
We use **`google/flan-t5-base`** hosted locally via the Hugging Face `transformers` library.
*   **Why?** It is lightweight, fast, and excellent at following instructions (Text-to-Text Transfer Transformer).
*   **Optimization:** We use specific decoding parameters (`temperature=0.5`, `repetition_penalty=1.5`) to ensure concise and non-repetitive outputs.

## 4. Important Things to Know
*   **Clean Architecture**: The code is split into `app.py` (API Layer) and `model.py` (Logic Layer).
*   **Safety First**: The system prioritizes the "Expert Knowledge Base" to prevent the AI from "hallucinating" on facts.
*   **Ambiguity Handling**: If you send vague inputs like "Help me", the system detects this and asks for clarification instead of guessing.

## 5. Fundamentals
The core philosophy is **"Decomposition"**.
*   **Problem**: "I'm overwhelmed."
*   **Solution**: Break it down into:
    *   **Root Causes** (Why is this hard?)
    *   **Steps** (Physical actions)
    *   **Timeline** (When to do what)
    *   **24-Hour Plan** (Immediate momentum)

## 6. How It Works (Technical Flow)
1.  **Request**: User sends text to `POST /chat`.
2.  **Ambiguity Check**: `app.py` checks if the input is too short (< 3 words). If so, it asks a clarifying question.
3.  **Retrieval (RAG-lite)**: `model.py` checks `TOPIC_TEMPLATES`. If the topic (e.g., "party") is found, it returns the expert-written plan.
4.  **Inference (Fallback)**: If no template is found, the AI generates the plan field-by-field (Root Causes, then Steps, then Timeline) using discrete prompts to maintain focus.
5.  **Response**: Validated JSON is returned to the client.

## 7. Backend Screenshot
Here is the Swagger UI (`/docs`) showing the active API endpoints:

![Backend API Swagger UI](/C:/Users/Delll/.gemini/antigravity/brain/1ca45b73-8839-4f4e-b328-d90ffb9ab1e9/backend_swagger_docs_1765275884655.png)
