from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def get_retrieval_embeddings(splits):
    vectorstore = Chroma.from_documents(documents=splits, 
                                    embedding=OpenAIEmbeddings())

    retriever = vectorstore.as_retriever()

    return retriever

