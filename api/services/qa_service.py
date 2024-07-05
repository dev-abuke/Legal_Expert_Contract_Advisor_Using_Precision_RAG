from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import ChatHistory
from ..schemas import QueryRequest
from ..factory import get_model
from ..config import load_config
from ..retriever import get_retriever_instance
from ..generator import create_history_aware_prompt, get_qa_assistant_prompt
import logging

import bs4
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

config = load_config()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = get_model(config)
documents = []  # Load your documents here
retriever = get_retriever_instance()

async def get_answer(session_id: str, query: QueryRequest, db: Session):

    # Retrieve the most similar document
    best_match = retriever.retrieve(query.query)

    logger.info(f"Best match: {len(best_match)} Metadata {best_match[0].metadata} Sample Content {best_match[0].page_content}")

    if best_match is None:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    ### Contextualize question ###
    contextualize_q_prompt = create_history_aware_prompt()
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever.get_retriever(), contextualize_q_prompt
    )

    ### Answer question ###
    qa_prompt = get_qa_assistant_prompt()

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    ### Statefully manage chat history ###

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    answer = conversational_rag_chain.invoke(
        {"input": query.query},
        config={
            "configurable": {"session_id": session_id}
        },  # constructs a key "abc123" in `store`.
    )["answer"]

    logger.info(f"Answer: {answer}")
    # Save the chat history to the database
    chat_history = ChatHistory(session_id=session_id, human_message=query.query, ai_message=answer)
    db.add(chat_history)
    db.commit()

    return answer

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    logger.info(f"Session ID in get_session_history: {session_id}")
    store = {}
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]