from pydantic import BaseModel
from datetime import datetime
from typing import List

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

class MessageHistory(BaseModel):
    session_id: str
    message: str

class MessageHistoryResponse(BaseModel):
    id: int
    session_id: str
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True
