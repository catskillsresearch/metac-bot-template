import pandas as pd

def load_questions(num_questions = 4, perennial = False):
    if perennial:
        from load_perennial_questions import load_perennial_questions
        questions = load_perennial_questions()
    else:
        from load_open_forecasted_questions import load_open_forecasted_questions
        questions = load_open_forecasted_questions()

    from community_forecast import community_forecast
    id_to_forecast = {question.api_json['id']: community_forecast(question) for question in questions}

    from flatten_dict import flatten_dict
    from datetime import datetime, timedelta
    df = pd.DataFrame([flatten_dict(q.api_json, sep='_') for q in questions])
    df['question_options'] = df['question_options'].apply(repr)
    df['today'] = datetime.now().strftime("%Y-%m-%d")
    df['crowd'] = df.apply(lambda row: id_to_forecast[row.id], axis=1)
    df = df[['id', 'today', 'open_time', 'scheduled_resolve_time', 'title', 'question_description',
            'question_resolution_criteria', 'question_fine_print', 'question_type',
            'question_options', 'question_group_variable', 'question_question_weight',
            'question_unit', 'question_open_upper_bound', 'question_open_lower_bound',
            'question_scaling_range_max', 'question_scaling_range_min', 'crowd']]
    
    return questions, df

if __name__=="__main__":
    from load_secrets import load_secrets
    load_secrets()
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    print('LIVE ANY')
    questions, df = load_questions()
    print(df)
    print('PERENNIAL')
    questions, df = load_questions(perennial=True)
    print(df)