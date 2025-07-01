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
    
    row['forecast'] = rationale
    row['prediction'] = forecast

    from error import error
    row['error'] = error(row)

    row.to_json(qfn, indent=4)
    print("saved row to ", qfn)

    import json
    with open(qfn, 'r') as f:
        foo = json.load(f)
    print("FORECAST = ", foo['forecast'])
    print("PREDICTION = ", foo['prediction'])
    print("CROWD = ", foo['crowd'])
    print("ERROR = ", foo['crowd'])