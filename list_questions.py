import requests, json
from config import config

API_BASE_URL = "https://www.metaculus.com/api2"
AUTH_HEADERS = {"headers": {"Authorization": f"Token {config.METACULUS_TOKEN}"}}

def list_questions(tournament_id, offset=0) -> list[dict]:
    """
    List (all details) {count} questions from the {tournament_id}
    """
    url_qparams = {
        "limit": 100,
        "offset": offset,
        "project": tournament_id,
#        "type": "forecast",
 #       "include_description": "true"
    }
    url = f"{API_BASE_URL}/questions/"
    response = requests.get(url, **AUTH_HEADERS, params=url_qparams)
    if not response.ok:
        raise Exception(response.text)
    data = json.loads(response.content)
    return data

if __name__=="__main__":
    from load_secrets import load_secrets
    load_secrets()
    questions = list_questions(32773)
    import json
    with open('questions.json', 'w') as f:
        json.dump(questions, f)