from forecast import forecast
from datetime import datetime, timedelta
from RAGForecaster import RAGForecaster
import pandas as pd

def training_bot(num_questions, perennial):
    results = forecast(perennial = perennial, live=False)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.max_columns', 500)
    print(results)

if __name__ == "__main__":
    training_bot(num_questions = 40, perennial=True)
