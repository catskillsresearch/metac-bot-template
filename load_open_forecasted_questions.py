from forecasting_tools import MetaculusApi, ApiFilter
from datetime import datetime, timedelta
import glob, joblib

def load_open_forecasted_questions(num_questions):
    start, end = num_questions
    fns = glob.glob('open/*.joblib')
    fns = [(int(fn.split('/')[1].split('.')[0]), fn) for fn in fns]
    fns = [fn for id,fn in fns if start <= id <= end]
    questions = [joblib.load(fn) for fn in fns]
    return questions

if __name__=="__main__":
    questions = load_open_forecasted_questions((30000, 40000))
    for question in questions:
        print(type(question))

