import requests, json
from config import config

API_BASE_URL = "https://www.metaculus.com/api2"
AUTH_HEADERS = {"headers": {"Authorization": f"Token {config.METACULUS_TOKEN}"}}
WARMUP_TOURNAMENT_ID = 32506

import datetime
import json
import os
import requests
import re
import textwrap

AUTH_HEADERS = {"headers": {"Authorization": f"Token {config.METACULUS_TOKEN}"}}
API_BASE_URL = "https://www.metaculus.com/api2"

TOURNAMENT_ID = 32506 # 32506 is the tournament ID for Q4 AI Benchmarking

def post_question_comment(question_id: int, comment_text: str) -> None:
    """
    Post a comment on the question page as the bot user.
    """
    response = requests.post(
        f"{API_BASE_URL}/comments/",
        json={
            "comment_text": comment_text,
            "submit_type": "N",
            "include_latest_prediction": True,
            "question": question_id,
        },
        **AUTH_HEADERS,
    )
    if not response.ok:
        raise Exception(response.text)

def post_question_prediction(question_id: int, prediction_percentage: float) -> None:
    """
    Post a prediction value (between 1 and 100) on the question.
    """
    assert 1 <= prediction_percentage <= 100, "Prediction must be between 1 and 100"
    url = f"{API_BASE_URL}/questions/{question_id}/predict/"
    response = requests.post(
        url,
        json={"prediction": float(prediction_percentage) / 100},
        **AUTH_HEADERS,
    )
    if not response.ok:
        raise Exception(response.text)

def get_question_details(question_id: int) -> dict:
    """
    Get all details about a specific question.
    """
    fn = f'{config.project}/questions/{question_id}.json'
    if os.path.exists(fn):
        with open(fn) as f:
            return json.load(f)
            
    url = f"{API_BASE_URL}/questions/{question_id}/"
    response = requests.get(
        url,
        **AUTH_HEADERS,
    )
    if not response.ok:
        raise Exception(response.text)

    details = json.loads(response.content)
    
    with open(fn, 'w') as f:
        json.dump(details, f, indent=4)
        print('saved', fn)
    
    return details

def list_questions(tournament_id=TOURNAMENT_ID, offset=0, count=1000, status = "open") -> list[dict]:
    """
    List (all details) {count} questions from the {tournament_id}
    """
    url_qparams = {
        "limit": count,
        "offset": offset,
        "has_group": "false",
        "order_by": "-activity",
        "project": tournament_id,
        "type": "forecast",
        "include_description": "true",
    }
    if status is not None:
        url_qparams['status'] = status
    url = f"{API_BASE_URL}/questions/"
    response = requests.get(url, **AUTH_HEADERS, params=url_qparams)
    if not response.ok:
        raise Exception(response.text)
    data = json.loads(response.content)
    return data


if __name__=="__main__":
    print("list_question")
    print(list_questions())
    print("get_question_details")
    ifp = get_question_details(25876)
    for key in ifp.keys():
        print("field", key)
        print("type", type(ifp[key]))
        print("value", ifp[key])
        print("===================")
    
