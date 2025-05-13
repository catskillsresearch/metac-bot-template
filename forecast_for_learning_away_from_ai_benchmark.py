from tqdm import tqdm
import pandas as pd
from load_secrets import load_secrets
from RAGForecaster import RAGForecaster
from EnhancedResearchPro import EnhancedResearchPro
from load_questions import load_questions
from load_research import load_research
from prompt_question import prompt_question
from predict import predict
from extract_forecast import extract_forecast
from plot_community_errors import plot_community_errors
from error import error
from pull_asknews import pull_asknews
from upload_forecast import upload_forecast

def forecast_for_learning_away_from_ai_benchmark(num_questions = 4, perennial = False):
    load_secrets()
    rag = RAGForecaster()
    enhanced_bot = EnhancedResearchPro(rag)
    questions, df = load_questions(num_questions, perennial = perennial)
    # Multi-pass forecasting
    for attempt in range(3):
        print(f"\n=== Forecast Iteration {attempt+1} ===")
        enhanced_bot.process_dataframe(df, use_cutoff = False)
        df['research'] = df.apply(load_research, axis=1)
        df['asknews'] = df.apply(pull_asknews, axis=1)
        df['learning'] =  df.apply(lambda row: enhanced_bot.retrieval_cache.get(row['title'], ''), axis=1)
        df['prompt'] = df.apply(prompt_question, axis=1)  # takes in asknews and learning
        # Generate and evaluate forecasts
        tqdm.pandas(desc="Forecasting...")
        df['forecast'] = df.progress_apply(lambda q: predict('forecast_community', q), axis=1)
        df['prediction'] = df.apply(extract_forecast, axis=1)
        df = df[~df.crowd.apply(lambda x: x is None)].copy()
        df['error'] = df.apply(error, axis=1)
        # Update RAG with successful forecasts
        success_mask = df.error < df.error.quantile(0.25)
        for _, row in df[success_mask].iterrows():
            rag.add_to_index(row['research'], row['id_of_question'])
        print('Prediction', df['prediction'])
        print('Crowd', df['crowd'])
            
    plot_community_errors(df)
    
    # Save results and RAG state
    df.to_json('community_results.json', indent=4)
    rag.save_state()

    if perennial:
        df.apply(upload_forecast, axis=1)
    
    return df[['title', 'question_type', 'prediction', 'crowd', 'error']]
