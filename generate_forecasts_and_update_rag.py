from tqdm import tqdm
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
        row = df.loc[idx].copy()  # Get current state
        context, indices = rag.retrieve_context(row['title'])

        print("PROMPT")
        print(row.prompt)
        # Batch updates
        updates = {
            'used_indices': indices,
            'forecast': predict('forecast_community', row),
        }
        row['forecast'] = updates['forecast']
        print("FOOO", row.forecast)
        #row['used_indices'] = indices
        updates['prediction'] = extract_forecast(row)
        
        # Single .loc update
        df.loc[idx, ['used_indices', 'forecast', 'prediction']] = updates
        
        # RAG update
        error_val = error(df.loc[idx])
        row['error'] = error_val
        df.loc[idx, 'error'] = error_val
        
        rag._update_success_scores(indices, 1 - error_val)

    # Daily maintenance
    if datetime.now().hour == 0:
        rag.decay_scores()
        rag.prune_old_entries()
    
    rag.save_state()
    return df
