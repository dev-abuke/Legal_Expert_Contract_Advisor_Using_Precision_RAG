from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
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
    template = """You are an AI language model assistant. Your task is to generate three (3) in a new line (do not jump lines)
    different versions of the given user question to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    Provide these alternative questions separated by newlines. Original question: {question}"""
    prompt_perspectives = ChatPromptTemplate.from_template(template)

    return prompt_perspectives

def get_hyde_prompt():
    # HyDE document genration prompt
    template = """Please write a scientific paper passage to answer the question
    Question: {question}
    Passage:"""

    prompt_hyde = ChatPromptTemplate.from_template(template)
    
    return prompt_hyde

def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

def get_answer_using_query(question):
    print("Using No Query Transformations")

    # Prompt
    prompt = create_context_prompt()

    retrieval_chain = retriever.get_retriever() | format_docs

    # Retrieve the context first
    context = retrieval_chain.invoke(question)

    # Chain
    rag_chain = (
        {"context": retrieval_chain, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Question
    answer = rag_chain.invoke(question)

    return answer, context

def get_answer_using_multi_query(question):
    print("Using Multi Query")

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
    print("Using RAG Fusion")
    prompt_perspectives = multi_query_prompt()

    generate_queries = (
        prompt_perspectives 
        | llm
        | StrOutputParser() 
        | (lambda x: x.split("\n"))
    )
    
    retrieval_chain_rag_fusion = generate_queries | retriever.get_retriever().map() | reciprocal_rank_fusion
    
    docs = retrieval_chain_rag_fusion.invoke({"question":question})

    print("The Docs are :: ",docs)

    context = "\n\n".join(doc.page_content for (doc, score) in docs)

    logger.info(f"Context Length = {len(docs)}")

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
    print("Using HyDe")

    prompt_hyde = get_hyde_prompt()

    generate_docs_for_retrieval = (
        prompt_hyde | llm | StrOutputParser() 
    )

    # Retrieve
    retrieval_chain = generate_docs_for_retrieval | retriever.get_retriever()

    retireved_docs = retrieval_chain.invoke({"question":question})

    context = "\n\n".join(doc.page_content for doc in retireved_docs)

    prompt = create_context_prompt()

    final_rag_chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    answer = final_rag_chain.invoke({"context":context,"question":question})

    return answer, context

def get_answer_using_raptor(question, SAVE_PATH="raptor_tree/robinson_contract"):
    import os, sys

    print("The Question In Raptor : ", question)

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../raptor'))

    print(f"Project ROOT IS : {project_root}")

    print(f"sys.PATH IS : {sys.path}")

    if project_root not in sys.path:
        sys.path.append(project_root)

    from raptor import RetrievalAugmentation

    RA = RetrievalAugmentation(tree=SAVE_PATH)

    answer, context = RA.answer_question(question)

    print("The Answer In Raptor : ", answer)

    print("The Context In Raptor : ", context)

    return answer, context