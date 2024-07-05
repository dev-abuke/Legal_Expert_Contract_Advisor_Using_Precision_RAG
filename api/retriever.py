import chromadb
from chromadb.config import Settings
from chromadb.api.types import QueryResult
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Embed and store the texts

class Retriever:
    def __init__(self, documents: list):
        self.documents = documents
        self.persist_directory = 'db'
        # Embed and store documents
        self.embeddings = OpenAIEmbeddings()
        if documents is not None:
            logger.info(f"Storing documents {len(documents)}")
            # self.store_documents(documents)
            self.db = Chroma.from_documents(documents, embedding=OpenAIEmbeddings(), persist_directory=self.persist_directory)
        self.db = Chroma(persist_directory=self.persist_directory, embedding_function=OpenAIEmbeddings())
            

    def store_documents(self, documents: list[Document]):
        logger.info(f"Storing documents From function {len(documents)}")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)

        logger.info(f"Splits {len(splits)}")

        docs = self.db.add_documents(splits)
        
        logger.info(f"Documents added {docs[0]}")

    def retrieve(self, query: str):
        results = self.db.similarity_search(query)
        return results
    def get_retriever(self):
        return self.db.as_retriever()

# Singleton instance of the Retriever
retriever_instance = None

def get_retriever_instance(documents: list = None):
    global retriever_instance
    if retriever_instance is None:
        retriever_instance = Retriever(documents)
    return retriever_instance
