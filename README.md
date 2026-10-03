# Swasthiq Front Desk Agent

This repository contains the backend and frontend implementation for the Swasthiq Front Desk Agent screening assignment.

## Tech Stack
*   **Backend**: Python, FastAPI, SQLite (In-Memory), OpenAI SDK
*   **Frontend**: React, Vite, Tailwind CSS

## Model & Performance
*   **Model Used**: `gpt-4o-mini` (Chosen for speed, low cost, and excellent strict JSON schema adherence).
*   **Tokens per Conversation (Avg)**: ~1,500 - 3,500 tokens
*   **Latency per Conversation (Avg)**: 3.5s - 5.0s

## How to Run

1.  **Clone & Setup Backend**
    ```bash
    cd backend
    python -m venv venv
    source venv/Scripts/activate # Windows
    pip install fastapi uvicorn pydantic openai
    export OPENAI_API_KEY="your-api-key"
    python main.py
    ```
    The API will be running at `http://localhost:8000/agent/run`

2.  **Run Frontend**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
    The UI will be accessible at `http://localhost:5173`

## Project Structure
*   `/backend` - Contains the FastAPI server, SQLite database logic, and the deterministic LLM agent loop.
*   `/frontend` - Contains the React components matching the Handoff Queue and Conversation Detail screens.
*   `/adversarial` - Contains 8 adversarial conversation scripts designed to break naive agent implementations.
*   `DECISIONS.md` - Discusses the architectural rationale for using a Raw SDK over LangChain and the strict state management rules.
