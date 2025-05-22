from datetime import datetime
from predict import predict
from extract_forecast import extract_forecast
from error import error

def generate_forecasts_and_update_rag(df, rag, live):
    print("=== Starting Forecast ===")
    # Pre-initialize columns (avoids repeated .at calls)
    df["used_indices"] = None
    df["forecast"] = None
    df["prediction"] = None
    df["error"] = None
    for idx in df.index:
        row = df.loc[idx].copy()
        rag.research_bot.refresh_if_needed()  # <-- MISSING CALL
        rag.add_to_index(row['research'], row['id_of_question'])
        context, indices = rag.retrieve_context(row['title'])
    
        row['used_indices'] = indices
        df.at[idx, 'used_indices'] = row.used_indices

        row['forecast'] = predict('forecast_community', row)
        df.at[idx, 'forecast'] = row.forecast

        row.prediction = extract_forecast(row)
        df.at[idx,'prediction'] = row.prediction
        
        # RAG update
        error_val = error(df.loc[idx])
        row['error'] = error_val
        df.at[idx, 'error'] = error_val
        
        rag._update_success_scores(indices, 1 - error_val)

    # Daily maintenance
    if datetime.now().hour == 0:
        rag.decay_scores()
        rag.prune_old_entries()
    
    rag.save_state()
    return df
