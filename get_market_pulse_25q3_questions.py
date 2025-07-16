import requests

def get_market_pulse_25q3_questions():
    url = 'https://www.metaculus.com/api/posts/'

    params = {
        'tournaments': 'market-pulse-25q3',
        'statuses': 'open',
        'with_cp': 'false',
        'include_cp_history': 'true',
        'include_descriptions': 'true',
        'order_by': '-published_at'
    }
    
    headers = {
        'accept': 'application/json'
    }
    
    response = requests.get(url, params=params, headers=headers)
    print(response.status_code)
    js = response.json()
    groups = js['results']
    ifps = []
    for x in groups:
        if 'group_of_questions' not in x:
            continue
        questions = x['group_of_questions']['questions']
        for question in questions:
            question['group'] = x
            ifps.append(question)

    ifps_sorted = [x[2] for x in list(sorted([(ifp['post_id'], ifp['id'], ifp) for ifp in ifps]))]

    return ifps_sorted