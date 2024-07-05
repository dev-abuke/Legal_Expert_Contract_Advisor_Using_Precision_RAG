from sqlalchemy.orm import Session
from ..models import ChatHistory

def get_chat_history(session_id: str, db: Session):
    return db.query(ChatHistory).filter(ChatHistory.session_id == session_id).all()
