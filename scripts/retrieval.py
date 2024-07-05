import chromadb
from chromadb.config import Settings
from chromadb.api.models import Document
from chromadb.api.types import QueryResult
from langchain.embeddings.openai import OpenAIEmbeddings
from chromadb.api import Chroma

class Retriever:
    def __init__(self, documents: list):
        self.documents = documents
        self.client = chromadb.Client(Settings(chroma_store_path="chroma_store"))
        self.collection = self.client.get_or_create_collection(name="documents")

        # Embed and store documents
        self.embeddings = OpenAIEmbeddings()
        self.store_documents(documents)

    def store_documents(self, documents: list):
        for doc in documents:
            embedding = self.embeddings.embed(doc['text'])
            self.collection.add(doc['id'], embedding, doc)

    def retrieve(self, query: str) -> QueryResult:
        query_embedding = self.embeddings.embed(query)
        results = self.collection.query(query_embedding)
        return results

# # Singleton instance of the Retriever
# retriever_instance = None

# def get_retriever_instance(documents: list = None):
#     global retriever_instance
#     if retriever_instance is None:
#         retriever_instance = Retriever(documents)
#     return retriever_instance
