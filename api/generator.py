from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from operator import itemgetter

from .retriever import get_retriever_instance
from .factory import get_model
from .utils.helpers import get_unique_union, reciprocal_rank_fusion
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
llm = get_model()

retriever = get_retriever_instance()

def create_context_prompt():

    # Prompt
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    return prompt

def create_history_aware_prompt():
    ### Contextualize question ###
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    return contextualize_q_prompt

def get_qa_assistant_prompt():
    ### Answer question ###
    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\

    {context}"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    return qa_prompt

def multi_query_prompt():
    # Multi Query: Different Perspectives
    template = """You are an AI language model assistant. Your task is to generate five 
    different versions of the given user question to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    Provide these alternative questions separated by newlines. Original question: {question}"""
    prompt_perspectives = ChatPromptTemplate.from_template(template)

    return prompt_perspectives

def get_answer_using_multi_query(question):

    prompt_perspectives = multi_query_prompt()

    generate_queries = (
        prompt_perspectives 
        | llm
        | StrOutputParser() 
        | (lambda x: x.split("\n"))
    )

    retrieval_chain = generate_queries | retriever.get_retriever().map() | get_unique_union

    docs = retrieval_chain.invoke({"question":question})

    context = "\n\n".join(doc.page_content for doc in docs)

    logger.info(f"Context {context}")

    prompt = create_context_prompt()

    final_rag_chain = (
        {"context": retrieval_chain, 
        "question": itemgetter("question")} 
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = final_rag_chain.invoke({"question":question})

    return answer, context

def get_answer_using_rag_fusion(question):
    prompt_perspectives = multi_query_prompt()

    generate_queries = (
        prompt_perspectives 
        | llm
        | StrOutputParser() 
        | (lambda x: x.split("\n"))
    )
    
    retrieval_chain_rag_fusion = generate_queries | retriever.get_retriever().map() | reciprocal_rank_fusion
    
    docs = retrieval_chain_rag_fusion.invoke({"question":question})

    context = "\n\n".join(doc.page_content for doc in docs)

    logger.info(f"Context {context}")

    prompt = create_context_prompt()

    final_rag_chain = (
        {"context": retrieval_chain_rag_fusion, 
        "question": itemgetter("question")} 
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = final_rag_chain.invoke({"question":question})

    return answer, context


# TODO: Implement

def get_answer_using_decomposition(question):
    return "This is using Decomposition", question

def get_answer_using_hyde(question):
    return "This is using HyDE", question