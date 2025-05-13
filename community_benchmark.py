from forecast_for_learning_away_from_ai_benchmark import forecast_for_learning_away_from_ai_benchmark
from datetime import datetime, timedelta
from RAGForecaster import RAGForecaster
import pandas as pd

def community_benchmark(num_questions, perennial):
    print("=== Starting Forecast Benchmark ===")
    results = forecast_for_learning_away_from_ai_benchmark(perennial = perennial)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.max_columns', 500)
    print(results)
    # Daily maintenance
    if datetime.now().hour == 0:
        print("\nRunning daily maintenance...")
        rag = RAGForecaster()
        rag.prune_old_entries()
        rag.save_state()
    print("\n=== Benchmark Completed ===")

if __name__ == "__main__":
    num_questions = 40
    perennial = False
    community_benchmark(num_questions, perennial)