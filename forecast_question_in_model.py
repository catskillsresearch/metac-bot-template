def forecast_question_in_model(id, model, use_saved = True):
    fn = f'forecast_{model}/{id}.md'
    import os
    if os.path.exists(fn) and use_saved:
        #print('model', model, 'id', id, 'seconds', 0)
        return
    from load_saved_questions import load_saved_questions
    from community_forecast import community_forecast
    import pandas as pd
    from flatten_dict import flatten_dict
    from datetime import datetime
    from gather_research_and_set_prompt import gather_research_and_set_prompt
    from generate_forecasts_and_update_rag import generate_forecasts_and_update_rag
    from tqdm import tqdm
    import time
    print('START model', model, 'id', id)
    start_time = time.time()
    hard_ids = [id]
    questions = load_saved_questions(hard_ids)
    id_to_forecast = {question.id_of_question: community_forecast(question) for question in questions}
    df = pd.DataFrame([flatten_dict(q.api_json, sep='_') for q in questions])
    df['id_of_post'] = [q.id_of_post for q in questions]
    df['id_of_question'] = [q.id_of_question for q in questions]
    df['question_options'] = df['question_options'].apply(repr)
    df['today'] = datetime.now().strftime("%Y-%m-%d")
    df['crowd'] = df.apply(lambda row: id_to_forecast[row.id_of_question], axis=1)
    df = df[['id_of_question', 'id_of_post', 'today', 'open_time', 'scheduled_resolve_time', 'title', 'question_description',
        'question_resolution_criteria', 'question_fine_print', 'question_type',
        'question_options', 'question_group_variable', 'question_question_weight',
        'question_unit', 'question_open_upper_bound', 'question_open_lower_bound',
        'question_scaling_range_max', 'question_scaling_range_min', 'question_scaling_zero_point','crowd']]
    live=True
    df, rag = gather_research_and_set_prompt(df, live, model)
    df = generate_forecasts_and_update_rag(df, rag, live, model)
    end_time = time.time()
    dt = end_time - start_time
    print('model', model, 'id', id, 'seconds', dt)
    return df

if __name__=="__main__":
    import sys
    id, model = sys.argv[1:3]
    id = int(id)
    import load_secrets
    load_secrets.load_secrets()
    forecast_question_in_model(id, model)
