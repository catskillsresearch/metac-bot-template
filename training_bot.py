from forecast import forecast
from datetime import datetime, timedelta
import pandas as pd

def training_bot(num_questions, perennial):
    results = forecast(num_questions = num_questions, perennial = perennial, live=False)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.max_columns', 500)
    print(results)

if __name__ == "__main__":
    import load_secrets
    load_secrets.load_secrets()
    training_bot(num_questions = 40, perennial=False)
