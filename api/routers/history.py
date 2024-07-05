from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import MessageHistoryResponse
from ..database import get_db
from ..models import ChatHistory
from ..services.history_service import get_chat_history

router = APIRouter()

@router.get("/history/{session_id}", response_model=List[MessageHistoryResponse])
async def history_endpoint(session_id: str, db: Session = Depends(get_db)):
    history = get_chat_history(session_id, db)
    return history


@router.get("/history/", response_model=List[MessageHistoryResponse])
async def get_all_history(db: Session = Depends(get_db)):
    history = db.query(ChatHistory).all()
    return history

@router.delete("/history/{session_id}")
async def delete_history(session_id: str, db: Session = Depends(get_db)):
    history = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).delete()
    db.commit()
    return {"message": f"History with session_id {session_id} deleted", "history": history}

@router.delete("/history")
async def delete_all_history(db: Session = Depends(get_db)):
    history = db.query(ChatHistory).delete()
    db.commit()
    return {"message": "All history deleted", "history": history}