import sys
import os
import uuid
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Dict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.session import get_db, engine, Base
from database.models import Submission, Problem, StatusEnum
from api.schemas import SubmissionCreate, ProblemResponse
from queue.connection import enqueue_submission
from ranking.leaderboard import Leaderboard

# Initialize DB tables (for simplicity here, usually use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Coding Judge API")

# In-memory leaderboard for demo purposes (would be Redis in production)
leaderboard = Leaderboard()

# Active websocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, submission_id: str, websocket: WebSocket):
        await websocket.accept()
        if submission_id not in self.active_connections:
            self.active_connections[submission_id] = []
        self.active_connections[submission_id].append(websocket)

    def disconnect(self, submission_id: str, websocket: WebSocket):
        if submission_id in self.active_connections:
            self.active_connections[submission_id].remove(websocket)

    async def broadcast_status(self, submission_id: str, status: str):
        if submission_id in self.active_connections:
            for connection in self.active_connections[submission_id]:
                await connection.send_text(f"Status update: {status}")

manager = ConnectionManager()

@app.post("/submit")
def submit_code(req: SubmissionCreate, db: Session = Depends(get_db)):
    """
    Submit code for evaluation.
    """
    sub_id = str(uuid.uuid4())
    
    # Create DB entry
    db_sub = Submission(
        id=sub_id,
        user_id=req.user_id,
        problem_id=req.problem_id,
        language=req.language,
        code=req.code,
        status=StatusEnum.QUEUED
    )
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    
    # Enqueue job
    enqueue_submission(sub_id, req.problem_id, req.language, req.code)
    
    return {"submission_id": sub_id, "status": "QUEUED"}

@app.get("/submission/status/{submission_id}")
def get_status(submission_id: str, db: Session = Depends(get_db)):
    """
    Fallback polling endpoint for status.
    """
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
        
    return {
        "status": sub.status.value,
        "execution_time": sub.execution_time,
        "memory_usage": sub.memory_usage
    }

@app.websocket("/ws/status/{submission_id}")
async def websocket_endpoint(websocket: WebSocket, submission_id: str):
    """
    Real-time status updates via WebSocket.
    """
    await manager.connect(submission_id, websocket)
    try:
        while True:
            # Keep connection alive. Worker will trigger broadcast (simulated here)
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(submission_id, websocket)

@app.get("/problem/{problem_id}", response_model=ProblemResponse)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@app.get("/leaderboard")
def get_leaderboard(limit: int = 10):
    """
    Retrieve current leaderboard.
    """
    return leaderboard.get_top_k(limit)
