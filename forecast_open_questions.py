def forecast_open_questions():
    import load_secrets
    load_secrets.load_secrets()

    import glob
    questions = glob.glob('open/*.joblib')

    from ollama_models import ollama_models
    models = ollama_models()
    model = models[0]

    import os
    fdir = f'forecast_{model}'
    os.makedirs(fdir, exist_ok=True)
    
    import joblib
    from forecast_open_question import forecast_open_question
    import forecasting_tools
    for qfn in questions:
        question = joblib.load(qfn)
        forecast_open_question(question, model, fdir)

if __name__=="__main__":
    forecast_open_questions()
