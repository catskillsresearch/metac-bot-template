from tqdm import tqdm
from datetime import datetime
from predict import predict
from extract_forecast import extract_forecast
from update_rag_with_successful_forecasts import update_rag_with_successful_forecasts

def generate_forecasts_and_update_rag(df, rag, live):
    print("=== Starting Forecast ===")
    tqdm.pandas(desc="Forecasting...")
    df['forecast'] = df.progress_apply(lambda q: predict('forecast_community', q), axis=1)
    df['prediction'] = df.apply(extract_forecast, axis=1)
    update_rag_with_successful_forecasts(df, rag, live)
    df.to_json('community_results.json', indent=4)
    rag.save_state()
    # Daily maintenance
    if datetime.now().hour == 0:
        print("\nRunning daily maintenance...")
        rag.prune_old_entries()
        rag.save_state()
    print("\n=== Forecast Completed ===")
    return df
    
