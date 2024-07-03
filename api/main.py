from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import openai

app = FastAPI()

# Define the Pydantic model for the request body
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

# Set up the OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Example dataset for in-memory retrieval
documents = [
    {"id": 1, "text": "This is a sample contract about employment."},
    {"id": 2, "text": "Another contract related to software development services."},
    # Add more documents here
]

# Endpoint for handling Q&A
@app.post("/qa", response_model=QueryResponse)
async def get_answer(query: QueryRequest):
    # Embed the query
    response = openai.Embedding.create(input=query.query, model="text-embedding-ada-002")
    query_embedding = response['data'][0]['embedding']

    # Embed documents and find the most similar one
    best_match = None
    best_score = float("-inf")

    for doc in documents:
        response = openai.Embedding.create(input=doc["text"], model="text-embedding-ada-002")
        doc_embedding = response['data'][0]['embedding']
        score = cosine_similarity(query_embedding, doc_embedding)

        if score > best_score:
            best_score = score
            best_match = doc["text"]

    if best_match is None:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    # Generate the response
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Based on the following document: {best_match}\n\nAnswer the following question: {query.query}",
        max_tokens=100
    )
    answer = completion.choices[0].text.strip()

    return QueryResponse(response=answer)

def cosine_similarity(vec1, vec2):
    return sum(a*b for a, b in zip(vec1, vec2)) / (sum(a**2 for a in vec1)**0.5 * sum(b**2 for b in vec2)**0.5)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
