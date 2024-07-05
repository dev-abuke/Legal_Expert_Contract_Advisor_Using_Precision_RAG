from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    human_message = Column(Text)
    ai_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    embedding = Column(String)
    retriever = Column(String)
