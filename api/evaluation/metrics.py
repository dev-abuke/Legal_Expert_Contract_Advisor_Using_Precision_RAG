import yaml, json, requests, os

from datasets import Dataset
import pandas as pd

from ragas import evaluate
from langchain_openai import ChatOpenAI
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
    answer_correctness
)

def start_test(evaluation_name: str, qa_data: str = 'raptor', number_of_questions: int = 3, save: bool = False) -> pd.DataFrame:
    """
    This function starts a test for evaluation metrics.
    
    Args:
        evaluation_name (str): The name of the evaluation.
        qa_data (str, optional): The type of QA data to use. Defaults to 'raptor'.
        number_of_questions (int, optional): The number of questions to use. Defaults to 3.
        save (bool, optional): Whether to save the context and answer as a json file. Defaults to False.

    Returns:
        pd.DataFrame: A pandas DataFrame with the evaluation results.
    """

    # Load the QA data based on the specified data type
    if qa_data == 'raptor':
        with open("data/evaluation/raptor.json", "r") as f:
            qa = yaml.safe_load(f)
    elif qa_data == 'hyde':
        with open("data/evaluation/robinson.json", "r") as f:
            qa = yaml.safe_load(f)
    
    # Extract the questions and ground truth answers from the QA data
    question = [q['question'] for q in qa[:number_of_questions]]
    ground_truth = [q['answer'] for q in qa[:number_of_questions]]

    # Set the URL for the QA endpoint
    url = f"http://127.0.0.1:8000/qa/{evaluation_name}"

    # Send requests to the QA endpoint for each question and store the answers and contexts
    answers = []
    contexts = []
    with requests.Session() as session:
        for q in question:
            data = {
                "query": q
            }
            response = session.post(url, json=data)

            answers.append(response.json()['response'])
            contexts.append(response.json()['context'])

    # Save the context and answer as a json file if specified
    if save:
        with open(f"data/evaluation/{evaluation_name}.json", "w") as f:
            json.dump({"context": contexts, "answer": answers}, f)

    # Convert the results to a dictionary
    data = {
        "question": number_of_questions,
        "answer": answers,
        "contexts": [contexts],
        "ground_truth": ground_truth
    }

    # Convert the dictionary to a dataset
    dataset = Dataset.from_dict(data)

    # Evaluate the dataset using the specified metrics and language model
    result = evaluate(
        dataset = dataset, 
        llm = ChatOpenAI(temperature=0), # use gpt-4o to increase context window, but has high cost
        metrics=[
            context_precision,
            context_recall,
            faithfulness,
            answer_relevancy,
            answer_correctness,
        ],
    )

    # Convert the evaluation results to a pandas DataFrame and return it
    return result.to_pandas()


df = start_test(qa_data='raptor', evaluation_name='')