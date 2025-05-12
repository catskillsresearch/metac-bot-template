from community_forecast_multiple_choice import community_forecast_multiple_choice
from community_forecast_binary import community_forecast_binary
from community_forecast_numeric import community_forecast_numeric

def community_forecast(question):
    qt = question.api_json['question']['type']
    methods = {'binary': community_forecast_binary, 
               'numeric': community_forecast_numeric, 
               'multiple_choice': community_forecast_multiple_choice}
    return methods[qt](question)
