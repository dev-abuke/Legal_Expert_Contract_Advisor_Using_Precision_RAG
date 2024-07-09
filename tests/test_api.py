# Proposed Change
# Cases Testing:

# Test if the endpoint responds with status code 200 for a valid query.
# Test if the endpoint returns the correct answer for a specific query.
# Test if the endpoint returns the correct context for a specific query.
# Create new file with this code.
import os, sys

print(f"sys.path IS : {sys.path}")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

print(f"sys.path ARE : {sys.path}")

import pytest
from fastapi.testclient import TestClient
from api.routers.qa import router
from sqlalchemy.orm import Session
from api.services.qa_service import get_answer
from api.schemas import QueryRequest, QueryResponse
from api.database import get_db


client = TestClient(router)

@pytest.fixture
def test_data():
    return {
        "query": "What is the capital of France?"
    }

def test_qa_endpoint_status_code(test_data):
    response = client.post("/qa/12345", json=test_data)
    assert response.status_code == 200

def test_qa_endpoint_correct_answer(test_data):
    response = client.post("/qa/12345", json=test_data)
    json_response = response.json()
    assert json_response["response"] == "The capital of France is Paris."

def test_qa_endpoint_correct_context(test_data):
    response = client.post("/qa/12345", json=test_data)
    json_response = response.json()
    assert json_response["context"] == "Context from the database"