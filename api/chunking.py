# Load Documents
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from langchain_text_splitters import CharacterTextSplitter
from langchain_ai21 import AI21SemanticTextSplitter
from langchain_experimental.text_splitter import SemanticChunker

class TextSplitter:
    def __init__(self, splitter_type = "Sentence", chunk_size=1000, chunk_overlap=200):
        self.splitter_type = splitter_type
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_documents(self, docs):
        if self.splitter_type == "Recursive":
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        elif self.splitter_type == "Semantic":
            text_splitter = SemanticChunker(OpenAIEmbeddings(), breakpoint_threshold_type="interquartile", number_of_chunks=100)
        elif self.splitter_type == "Character":
            text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        elif self.splitter_type == "Sentence":
            text_splitter = SentenceTransformersTokenTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        else:
            raise ValueError(f"Unsupported splitter type: {self.splitter_type}")
        
        chunks = text_splitter.split_documents(docs)

        print(f"Splitter Type: {self.splitter_type}")

        print(f"Number of chunks: {len(chunks)}")

        return chunks

def RecursiveSplitter(docs, chunk_size=1000, chunk_overlap=200):
    return TextSplitter("Recursive", chunk_size, chunk_overlap).split_documents(docs)

def SemanticSplitter(docs, chunk_size=1000, chunk_overlap=200):
    return TextSplitter("Semantic", chunk_size, chunk_overlap).split_documents(docs)

def CharacterSplitter(docs, chunk_size=1000, chunk_overlap=200):
    return TextSplitter("Character", chunk_size, chunk_overlap).split_documents(docs)

def SentenceSplitter(docs, chunk_size=1000, chunk_overlap=200):
    return TextSplitter("Sentence", chunk_size, chunk_overlap).split_documents(docs)