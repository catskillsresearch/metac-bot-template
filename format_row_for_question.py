def format_row_for_question(question):

    from community_forecast import community_forecast
    id_to_forecast = community_forecast(question)
    questions = [question]

    import pandas as pd
    from flatten_dict import flatten_dict
    df = pd.DataFrame([flatten_dict(question.api_json, sep='_')])
    df['id_of_post'] = [q.id_of_post for q in questions]
    df['id_of_question'] = [q.id_of_question for q in questions]
    df['question_options'] = df['question_options'].apply(repr)

    from datetime import datetime
    df['today'] = datetime.now().strftime("%Y-%m-%d")
    df['crowd'] = df.apply(lambda row: id_to_forecast, axis=1)
    df['error'] = ''
    df1 = df[['id_of_question', 'id_of_post', 'today', 'open_time', 'scheduled_resolve_time', 'title',
        'question_resolution_criteria', 'question_fine_print', 'question_type', 
        'question_description', 'question_options', 'question_group_variable', 'question_question_weight',
        'question_unit', 'question_open_upper_bound', 'question_open_lower_bound',
        'question_scaling_range_max', 'question_scaling_range_min', 'question_scaling_zero_point','crowd']].copy()

    from gather_research import gather_research
    df2, rag = gather_research(df1, True, model)
    df3 = df2[['id_of_question', 'title',
               'question_resolution_criteria', 'question_fine_print', 'question_type', 
               'question_description',
               'question_options', 'question_group_variable', 'question_question_weight',
               'question_unit', 'question_open_upper_bound', 'question_open_lower_bound',
               'question_scaling_range_max', 'question_scaling_range_min', 'question_scaling_zero_point','crowd',
               'research', 'asknews', 'learning']].copy()
    
    row = df3.iloc[0]

    return row
