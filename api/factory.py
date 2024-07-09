from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever

from .chunking import TextSplitter
from .config import load_config

# make the .env file in the same directory
import os
from dotenv import load_dotenv

load_dotenv()

def get_model():
    config = load_config()
    if config["model"] == "gpt-3.5-turbo":
        return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    elif config["model"] == "gpt-4o":
        return ChatOpenAI(model="gpt-4o", temperature=0)
    # Add more models as needed

def get_embedding():
    config = load_config()
    if config["embedding"] == "openai":
        return OpenAIEmbeddings()
    elif config["embedding"] == "huggingface":
        return "HuggingFaceEmbeddings"
    # Add more embeddings as needed

def get_retriever(persist_directory = 'db'):
    config = load_config()
    if config["retriever"] == "dense":
        print("Using Chroma Retriever")
    elif config["retriever"] == "hybrid":
        print("Using Weaviate Hybrid Search Retriever")

def get_prompt():
    from .generator import create_context_prompt, get_qa_assistant_prompt, create_history_aware_prompt
    config = load_config()
    if config["prompt"] == "history_aware":
        return create_history_aware_prompt()
    elif config["prompt"] == "contextualize_q":
        return create_context_prompt()
    elif config["prompt"] == "qa_assistant":
        return get_qa_assistant_prompt()
    # Add more prompts as needed

def get_text_splitter() -> TextSplitter:
    config = load_config()

    chunk_size = config["chunk_size"]
    chunk_overlap = config["chunk_overlap"]
    
    if config["text_splitter"] == "character":
        return TextSplitter("Character", chunk_size, chunk_overlap)
    elif config["text_splitter"] == "sentence":
        return TextSplitter("Sentence", chunk_size, chunk_overlap)
    elif config["text_splitter"] == "recursive":
        return TextSplitter("Recursive", chunk_size, chunk_overlap)
    elif config["text_splitter"] == "semantic":
        return TextSplitter("Semantic", chunk_size, chunk_overlap)
    # Add more text splitters as needed

def get_query_translation():
    config = load_config()
    from .generator import get_answer_using_multi_query, get_answer_using_rag_fusion, get_answer_using_decomposition, get_answer_using_hyde, get_answer_using_raptor, get_answer_using_query
    if config["query_translation"] == "multi_query":
        return get_answer_using_multi_query
    elif config["query_translation"] == "rag_fusion":
        return get_answer_using_rag_fusion
    elif config["query_translation"] == "decomposition":
        return get_answer_using_decomposition
    elif config["query_translation"] == "no_translation":
        return get_answer_using_query
    elif config["query_translation"] == "hyde":
        return get_answer_using_hyde
    elif config["query_translation"] == "raptor":
        return get_answer_using_raptor
    # Add more query translation as needed