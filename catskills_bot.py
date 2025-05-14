from forecast import forecast
from datetime import datetime, timedelta
from RAGForecaster import RAGForecaster
import pandas as pd

def catskills_bot(num_questions, perennial, live):

    results = forecast(perennial = perennial, live=live)
    if results is None:
        print("=== Ending Forecast: No questions ===")
        return
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.max_columns', 500)
    print(results)

if __name__ == "__main__":
    num_questions = 40
    perennial = False
    live = True
    catskills_bot(num_questions, perennial, live)
