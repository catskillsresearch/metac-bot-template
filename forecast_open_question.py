def forecast_open_question(question, model, fdir):
    id = question.id_of_question
    qfn = f'{fdir}/{id}.json'
    import os
    if os.path.exists(qfn):
        return
        
    print("forecasting", question.question_text, model)

    from format_row_for_question import format_row_for_question
    row = format_row_for_question(question, model)
    
    from prompt2 import prompt2
    prompt2 = prompt2(row, model)

    from make_median_forecast import make_median_forecast
    forecast, rationale = make_median_forecast(row.question_type, prompt2, model)
    
    row.forecast = rationale
    row.prediction = forecast

    from error import error
    row.error = error(row)

    row.to_json(qfn, indent=4)

if __name__=="__main__":
    
    import joblib
    qfn = 'open/3095.joblib'
    question = joblib.load(qfn)

    from ollama_models import ollama_models
    models = ollama_models()
    model = models[0]

    forecast_open_question(question, model)
