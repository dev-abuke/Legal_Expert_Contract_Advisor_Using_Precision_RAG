# Load Documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from langchain_text_splitters import CharacterTextSplitter

# Split
def RecursiveSplitter(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    splits = text_splitter.split_documents(docs)

    return splits

def SemanticSplitter(docs):
    text_splitter = SentenceTransformersTokenTextSplitter(chunk_size=1000, chunk_overlap=200)

    splits = text_splitter.split_documents(docs)

    return splits

def CharacterSplitter(docs):
    text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=1000, chunk_overlap=200)

    splits = text_splitter.split_documents(docs)

    return splits