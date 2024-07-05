from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import QueryRequest, QueryResponse
from ..database import get_db
from ..services.qa_service import get_answer

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()

@router.post("/qa/{session_id}", response_model=QueryResponse)
async def qa_endpoint(session_id: str, query: QueryRequest, db: Session = Depends(get_db)):
    logger.info(f"The Query is :: {query.query}")
    response = await get_answer(session_id, query, db)
    print(f"The Response is ::: {response}")
    return QueryResponse(response=response['answer'], context=response['context'])
