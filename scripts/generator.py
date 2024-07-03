from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

def create_rag_chain(retriever, prompt, llm):
    return (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

def create_prompt():

    # Prompt
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    return prompt

def create_llm(temperature=0):
    # LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=temperature)

    return llm