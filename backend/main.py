from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

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

@app.post("/agent/run", response_model=AgentResponse)
async def agent_run(request: TurnRequest):
    if not os.environ.get("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable not set")
        
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
