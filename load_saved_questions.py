import joblib
import forecasting_tools

def load_saved_questions(ids):
    fns = [f'open/{id}.joblib' for id in ids]
    return [joblib.load(fn) for fn in fns]