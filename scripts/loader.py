import os

from langchain.document_loaders import UnstructuredHTMLLoader
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, Docx2txtLoader

def get_document_from_docx(documents: list, file_path):
    # Load and parse HTML file found in the specified folder and subfolders
    docx_files = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith('.docx')]

    # Load and parse HTML files
    for file in docx_files:
        loader = Docx2txtLoader(file)
        documents.extend(loader.load())

    return documents

def get_document_from_html(documents: list, file_path):
    # Load and parse HTML file found in the specified folder and subfolders
    html_files = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith('.html')]

    # Load and parse HTML files
    for file in html_files:
        loader = UnstructuredHTMLLoader(file)
        documents.extend(loader.load())

    return documents

def get_document_from_pdf(documents: list, file_path):
    # Load and parse PDF file found in the specified folder and subfolders
    pdf_files = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith('.pdf')]

    # Load and parse PDF files
    for file in pdf_files:
        loader = PyPDFLoader(file)
        documents.extend(loader.load())

    return documents