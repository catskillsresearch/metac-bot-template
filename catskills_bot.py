from forecast import forecast
from datetime import datetime, timedelta
from RAGForecaster import RAGForecaster
import pandas as pd

def catskills_bot(num_questions, perennial, live):
    print("=== Starting Forecast ===")
    results = forecast(perennial = perennial, live=live)
    if results is None:
        print("=== Ending Forecast: No questions ===")
        return
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.max_columns', 500)
    print(results)
    # Daily maintenance
    if datetime.now().hour == 0:
        print("\nRunning daily maintenance...")
        rag = RAGForecaster()
        rag.prune_old_entries()
        rag.save_state()
    print("\n=== Forecast Completed ===")

if __name__ == "__main__":
    num_questions = 40
    if 0:
        perennial = True
        live = False
    else:
        perennial = False
        live = True
    catskills_bot(num_questions, perennial, live)
