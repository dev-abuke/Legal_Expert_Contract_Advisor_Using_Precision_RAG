# Imports for memory Q&A
# import bs4
# from langchain.chains import create_history_aware_retriever, create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables.history import RunnableWithMessageHistory

from sqlalchemy.orm import Session

from ..models import ChatHistory
from ..schemas import QueryRequest
from ..factory import get_query_translation

import logging

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

query_translation = get_query_translation()

async def get_answer(session_id: str, query: QueryRequest, db: Session):

    # answer, context = get_answer_using_multi_query(query.query)
    answer, context = query_translation(query.query)

    print(f"Context is joined :: {context}")

    logger.info(f"Answer: {answer}")
    # Save the chat history to the database
    chat_history = ChatHistory(session_id=session_id, human_message=query.query, ai_message=answer)
    db.add(chat_history)
    db.commit()

    return {"answer":answer, "context":context}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    logger.info(f"Session ID in get_session_history: {session_id}")
    store = {}
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]