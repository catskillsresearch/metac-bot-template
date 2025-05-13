import os
from query_perplexity_with_date_filter import query_perplexity_with_date_filter

def predict(dfn, question):
    ffn =  f'{dfn}/{question.id_of_question}.md'
    if os.path.exists(ffn):
        with open(ffn, 'r') as f:
            forecast = f.read()
    else:
        api_key = os.getenv('PERPLEXITY_API_KEY')
        forecast = query_perplexity_with_date_filter(api_key, question.prompt, question.today)
        with open(ffn, 'w') as f:
            f.write(forecast)
    return forecast