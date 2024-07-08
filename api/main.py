import os
from langchain_community.document_loaders import Docx2txtLoader

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from .models import Base
from .routers import qa, history
from .retriever import get_retriever_instance
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("The Logger INFO CWD:: "+ os.getcwd())

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(qa.router)
app.include_router(history.router)

# allow all origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_document_from_docx(documents: list, file_path):
    # Load and parse HTML file found in the specified folder and subfolders
    docx_files = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith('.docx')]

    # Load and parse HTML files
    for file in docx_files:
        loader = Docx2txtLoader(file)
        documents.extend(loader.load())

    return documents

# Initialize the retriever with documents
documents = get_document_from_docx([], "data/raw/docx")
len = len(documents)
logger.info(f"The Logger INFO :: {len}")
# retriever = get_retriever_instance(documents).store_documents(documents)