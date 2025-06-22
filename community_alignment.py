from tqdm import tqdm
tqdm.pandas()

def predict(dfn, question, iterations = 3):
    ffn = f'{dfn}/{question.id_of_question}.md'
    with open(ffn, 'r') as f:
        return f.read()

def load_research(row):
    with open(f"research/{row['id']}.md", 'r') as f:
        return f.read()

def pull_asknews(row):
    fn = f'asknews/{row.id}.md'
    with open(fn, 'r') as f:
        return f.read()
        
def community_alignment(model = 'llama3'):
    num_questions = (0,100000)

    from load_forecasted_open_questions import load_forecasted_open_questions
    questions = load_forecasted_open_questions(num_questions, model)

    from community_forecast import community_forecast
    id_to_forecast = {question.api_json['id']: community_forecast(question) for question in questions}
    id_to_question = {question.api_json['id']: question for question in questions}
    pdir = f'forecast_{model}'

    import glob
    fns = glob.glob(f'{pdir}/*.md')
    ids = [int(fn.split('/')[1].split('.')[0]) for fn in fns]
    forecasts = {id: open(f'{pdir}/{id}.md').read() for id in ids}
    community_ids = list(id_to_forecast.keys())
    forecast_ids = list(forecasts.keys())
    done = list(set(forecast_ids).intersection(community_ids))

    from extract_only_forecast import extract_only_forecast
    for id in done:
        #print(id)
        foo = extract_only_forecast(id_to_question, forecasts, id)
    predictions = {id: extract_only_forecast(id_to_question, forecasts, id) for id in done}
    q_done = [id_to_question[id] for id in done]

    from flatten_dict import flatten_dict
    qflat = [flatten_dict(q.api_json, sep='_') for q in q_done]

    import pandas as pd
    df = pd.DataFrame(qflat)
    df['crowd'] = df.apply(lambda row: id_to_forecast[row.id], axis=1)
    df['question_options'] = df['question_options'].apply(repr)
    df = df[['id',
             'open_time',
             'scheduled_resolve_time',
             'title',
             'question_description',
             'question_resolution_criteria',
             'question_fine_print',
             'question_type',
             'question_options',
             'question_group_variable',
             'question_question_weight',
             'question_unit',
             'question_open_upper_bound',
             'question_open_lower_bound',
             'question_scaling_range_max',
             'question_scaling_range_min',
             'question_scaling_zero_point',
             'crowd']]
    dfn = f'forecast_{model}'

    from datetime import datetime
    df['today'] = datetime.now().strftime("%Y-%m-%d")
    df['asknews'] = df.apply(pull_asknews, axis=1)
    df['research'] = df.apply(load_research, axis=1)

    from RAGForecaster import RAGForecaster
    rag = RAGForecaster()

    from EnhancedResearchPro import EnhancedResearchPro
    research_bot = EnhancedResearchPro(rag)
    df['id_of_question'] = df['id']
    research_bot.process_dataframe(df, use_cutoff=False)
    rag.research_bot = research_bot
    # Updated learning field with raw text extraction
    df['learning'] = df.apply(
        lambda row: [
            m['raw_text'] 
            for m, _ in research_bot.retrieval_cache.get(row['title'], []) 
            if 'raw_text' in m  # Safety check for legacy entries
        ], 
        axis=1
    )

    from prompt_question import prompt_question
    df['prompt'] = df.apply(prompt_question, axis=1)
    
    df['forecast'] = df.progress_apply(lambda question: predict(dfn, question), axis=1)

    from extract_forecast import extract_forecast
    df['prediction'] = df.apply(extract_forecast, axis=1)
    df = df[~df.crowd.apply(lambda x: x is None)].copy()

    from error import error
    df['error'] = df.apply(error, axis=1)

    df['model'] = model

    import matplotlib.pyplot as plt
    plt.hist(df.error.values, bins=20);
    fn = f'community_{model}.json'
    df.to_json(fn, indent=4)
    print('saved', fn)
    return df