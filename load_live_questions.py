from forecasting_tools import MetaculusApi

def not_forecast_yet(question):
    try:
        forecast_values = question.api_json['question']['my_forecasts']['latest']['forecast_values']
        return forecast_values is None
    except:
        return True

def load_live_questions(num_questions = 1):
    questions = MetaculusApi.get_all_open_questions_from_tournament(tournament_id=MetaculusApi.CURRENT_AI_COMPETITION_ID)
    questions = [question for question in questions if not_forecast_yet(question)]
    return questions

if __name__=="__main__":
    from load_secrets import load_secrets
    load_secrets()
    questions = load_live_questions(1)
    print('got', len(questions), 'live questions')
