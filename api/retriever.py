import chromadb
from chromadb.config import Settings
from chromadb.api.types import QueryResult
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from langchain.retrievers import BM25Retriever, EnsembleRetriever

from .factory import get_text_splitter, get_retriever
from .config import load_config

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = load_config()

class Retriever:
    def __init__(self, documents: list):
        self.documents = documents

        self.persist_directory = 'db'

        self.retriever_type = config["retriever"]

        self.retriever = get_retriever()
            
    def store_documents(self, documents: list[Document]):
        logger.info(f"Storing documents From function {len(documents)}")

        splits = get_text_splitter().split_documents(documents)

        logger.info(f"Splits {len(splits)}")

        docs = self.retriever.add_documents(splits)
        
        logger.info(f"Documents added {docs[0]}")

    def retrieve(self, query: str):
        results = self.retriever.similarity_search(query)
        return results
    def get_retriever(self):
        if config["retriever"] == "dense":
            return self.retriever.as_retriever()
        elif config["retriever"] == "hybrid":
            return self.retriever

# Singleton instance of the Retriever
retriever_instance = None

def get_retriever_instance(documents: list = None):
    global retriever_instance
    if retriever_instance is None:
        retriever_instance = Retriever(documents)
    return retriever_instance
