from pydantic import BaseModel
from datetime import datetime
from typing import List

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    context: str

class MessageHistory(BaseModel):
    session_id: str
    human_message: str
    ai_message: str

class MessageHistoryResponse(BaseModel):
    id: int
    session_id: str
    human_message: str
    ai_message: str
    timestamp: datetime

    class Config:
        from_attributes = True
