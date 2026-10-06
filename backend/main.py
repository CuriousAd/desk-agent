from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Automatically load .env if present
def load_env():
    for path in [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    ]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k not in os.environ:
                            os.environ[k] = v

load_env()

try:
    from schemas import TurnRequest, AgentResponse
    from database import create_db
    from agent import run_agent
except ImportError:
    from .schemas import TurnRequest, AgentResponse
    from .database import create_db
    from .agent import run_agent

app = FastAPI(title="Swasthiq Front Desk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "Swasthiq Front Desk API"}

@app.post("/agent/run", response_model=AgentResponse)
@app.post("/run", response_model=AgentResponse)
async def agent_run(request: TurnRequest):
    if not os.environ.get("OPENAI_API_KEY") and not os.environ.get("GROQ_API_KEYS") and not os.environ.get("GROQ_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY, GROQ_API_KEY, or GROQ_API_KEYS environment variable not set")
        
    # State resets between conversations as per requirement
    conn = create_db()
    
    try:
        response = run_agent(
            conversation_id=request.conversation_id,
            today=request.today,
            turns=request.turns,
            conn=conn
        )
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
