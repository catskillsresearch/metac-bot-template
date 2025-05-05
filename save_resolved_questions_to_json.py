import requests, os
from load_secrets import load_secrets



url = 'https://www.metaculus.com/api/posts/'

params = {
    'tournaments': ['3349', '32506', '32627', '32721'],
    'statuses': 'resolved',
    'limit': 100,
    'forecast_type': [
        'binary', 'numeric', 'date', 'multiple_choice',
        'conditional', 'group_of_questions', 'notebook'
    ],
    'order_by': '-published_at'
}

headers = {
    'accept': 'application/json',
    'Authorization': os.getenv('METACULUS_TOKEN')
}

all_results = []
offset = 0

while True:
    print(offset)
    # Update offset for current iteration
    params['offset'] = offset
    
    # Make API request
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    
    # Extract results from response
    data = response.json()
    results = data.get('results', [])
    
    # Break loop if no more results
    if not results:
        break
    
    # Append results and increment offset
    all_results.append(results)
    offset += 100

questions = [x for y in all_results for x in y ]

print("got", len(questions), "questions")

import json
with open('questions.json', 'w') as f:
    json.dump(questions, f)