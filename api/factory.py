from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from .generator import create_context_prompt, create_rag_chain, get_qa_assistant_prompt, create_history_aware_prompt

# make the .env file in the same directory
import os
from dotenv import load_dotenv
load_dotenv()

def get_model(config):
    if config["model"] == "gpt-3.5-turbo":
        return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    elif config["model"] == "gpt-4":
        return ChatOpenAI(model="gpt-4", temperature=0)
    # Add more models as needed

def get_embedding(config):
    if config["embedding"] == "openai":
        return OpenAIEmbeddings()
    elif config["embedding"] == "huggingface":
        return "HuggingFaceEmbeddings"
    # Add more embeddings as needed

def get_retriever(config, documents):

    if config["retriever"] == "dense":
        return "DenseRetriever(documents)"
    elif config["retriever"] == "sparse":
        return "SparseRetriever(documents)"
    # Add more retrievers as needed

def get_prompt(config):
    if config["prompt"] == "history_aware":
        return create_history_aware_prompt()
    elif config["prompt"] == "contextualize_q":
        return create_context_prompt()
    elif config["prompt"] == "qa_assistant":
        return get_qa_assistant_prompt()
    # Add more prompts as needed