from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import MessageHistoryResponse
from ..database import get_db
from ..models import ChatHistory
from sqlalchemy import distinct
from ..services.history_service import get_chat_history
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/history/{session_id}", response_model=List[MessageHistoryResponse])
async def history_endpoint(session_id: str, db: Session = Depends(get_db)):
    history = get_chat_history(session_id, db)
    return history

@router.get("/history/", response_model=List[MessageHistoryResponse])
async def get_all_history(db: Session = Depends(get_db)):
    history = db.query(ChatHistory).all()
    return history

#get all unique session ids
@router.get("/session_ids", response_model=List[str])
async def get_session_ids(db: Session = Depends(get_db)):
    # get all unique session ids as a list
    unique_session_ids = db.query(distinct(ChatHistory.session_id)).all()
    logger.info(f"The Unique Session IDs :: {unique_session_ids}")
    return [session_id[0] for session_id in unique_session_ids]


@router.get("/session_ids/{session_id}")
async def get_session_id(session_id: str, db: Session = Depends(get_db)):
    history = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).all()
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