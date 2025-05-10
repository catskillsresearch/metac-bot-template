from community_forecast_multiple_choice import community_forecast_multiple_choice
from community_forecast_binary import community_forecast_binary
from community_forecast_numeric import community_forecast_numeric

def community_forecast(question):
    qt = question.api_json['question']['type']
    methods = {x: eval(f'community_forecast_{x}') for x in ['binary', 'numeric', 'multiple_choice']}
    return methods[qt](question)
