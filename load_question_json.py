import requests, json
from config import config

API_BASE_URL = "https://www.metaculus.com/api"
AUTH_HEADERS = {"headers": {"Authorization": f"Token {config.METACULUS_TOKEN}"}}

def load_question_json(question_id):

    url = f"{API_BASE_URL}/posts/{question_id}/"
    print(url)
    print("https://www.metaculus.com/api/posts/38699/")
    response = requests.get(
        url,
        **AUTH_HEADERS,  
    )
    print(response)
    json_question = json.loads(response.content)
    return json_question

if __name__=="__main__":
    from load_secrets import load_secrets
    load_secrets()
    question = load_question_json(38699)
    print(question)
