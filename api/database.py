from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("PYCOPG_DATABASE_URL", "postgresql+psycopg2://trading_db_av2v_user:210M6MA9QKEEgVdiasnUdMQDBNN417oy@dpg-cpqojbqj1k6c73bkqq3g-a.oregon-postgres.render.com/trading_db_av2v")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()