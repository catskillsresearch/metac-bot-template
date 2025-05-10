# Base forecaster against open questions -- test community forecast alignment

from forecasting_tools import MetaculusApi, ApiFilter
from datetime import datetime, timedelta
import asyncio, os
import numpy as np
from predict import predict
from load_secrets import load_secrets
from community_forecast import *
import matplotlib.pyplot as plt
from tqdm import tqdm
from flatten_dict import flatten_dict
import pandas as pd
from prompt_question import prompt_question
from ResearchProModule import ResearchProModule
from load_research import load_research
from extract_forecast import extract_forecast
from error import error
from sentence_transformers import SentenceTransformer

def community_benchmark():
    load_secrets()
    tqdm.pandas()
    num_of_questions_to_return = 42
    one_year_from_now = datetime.now() + timedelta(days=365)
    api_filter = ApiFilter(
        allowed_statuses=["open"],
        num_forecasters_gte=40,
        scheduled_resolve_time_lt=one_year_from_now,
        includes_bots_in_aggregates=False)
    questions = asyncio.run(MetaculusApi.get_questions_matching_filter(
            api_filter, num_questions=num_of_questions_to_return, randomly_sample=True))
    id_to_forecast = {question.api_json['id']: community_forecast(question) for question in questions}
    qflat = [flatten_dict(q.api_json, sep='_') for q in questions]
    df = pd.DataFrame(qflat)
    df['crowd'] = df.apply(lambda row: id_to_forecast[row.id], axis=1)
    df['question_options'] = df['question_options'].apply(repr)
    df = df[['id','open_time','scheduled_resolve_time','title','question_description',
                'question_resolution_criteria','question_fine_print','question_type',
                'question_options','question_group_variable','question_question_weight',
                'question_unit','question_open_upper_bound','question_open_lower_bound',
                'question_scaling_range_max','question_scaling_range_min','crowd']]
    dfn = 'forecast_community'
    os.makedirs(dfn, exist_ok=True)
    df['today'] = datetime.now().strftime("%Y-%m-%d")
    bot = ResearchProModule()
    bot.process_dataframe(df)
    df['research'] = df.apply(load_research, axis=1)
    df['prompt'] = df.apply(prompt_question, axis=1)
    df[df.question_type == 'multiple_choice']
    df['forecast'] = df.progress_apply(lambda question: predict(dfn, question), axis=1)
    df['prediction'] = df.apply(extract_forecast, axis=1)
    df = df[~df.crowd.apply(lambda x: x is None)].copy()
    df['error'] = df.apply(error, axis=1)
    plt.hist(df.error.values);
    plt.savefig('df_error_values.png', dpi=150)
    df.to_json('community_results.json', indent=4)
    df1 = df[['title', 'question_type', 'prediction', 'crowd', 'error']]
    df1.to_csv('community.csv')

if __name__=="__main__":
    community_benchmark()
    

