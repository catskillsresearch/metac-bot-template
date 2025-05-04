from forecasting_tools import MetaculusApi
import requests, json
from config import config

def list_questions(tournament_id, offset=0) -> list[dict]:
    """
    List (all details) {count} questions from the {tournament_id}
    """
    API_BASE_URL = "https://www.metaculus.com/api"
    AUTH_HEADERS = {"headers": {"Authorization": f"Token {config.METACULUS_TOKEN}"}}

    url_qparams = {
        "limit": 100,
        "offset": offset,
        "project": tournament_id,
        "include_description": "true"
    }
    url = f"{API_BASE_URL}/questions/"
    response = requests.get(url, **AUTH_HEADERS, params=url_qparams)
    if not response.ok:
        raise Exception(response.text)
    data = json.loads(response.content)
    return data

def ifps(tournament_id, offset):
    data = list_questions(tournament_id, offset)
    questions = data['results']
    return questions

if __name__=="__main__":
    tourneys=[MetaculusApi.AI_COMPETITION_ID_Q3, 
              MetaculusApi.AI_COMPETITION_ID_Q4, 
              MetaculusApi.AI_COMPETITION_ID_Q1, 
              MetaculusApi.AI_COMPETITION_ID_Q2]   

    all_questions = []
    for tournament_id in tourneys:
        offset = 0
        while True:
            print(tournament_id, 'offset', offset)
            questions = ifps(tournament_id, offset)
            if len(questions) == 0:
                break
            else:
                all_questions.extend(questions)
            offset += 100
            print(tournament_id, 'questions', len(questions))
            print('all_questions', len(all_questions))
    
    len(all_questions)
    
    len(set([x['id'] for x in all_questions]))
    
    from pickle_objects import *
    qfn = 'all_questions.pkl'
    pickle_objects(all_questions, qfn)
    q2 = unpickle_objects(qfn)
    print("saved", len(q2))