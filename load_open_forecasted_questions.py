def load_open_forecasted_questions(num_questions = 4):
    from forecasting_tools import MetaculusApi, ApiFilter
    from datetime import datetime, timedelta
    api_filter = ApiFilter(
        allowed_statuses=["open"],
        num_forecasters_gte=40,
        scheduled_resolve_time_lt=datetime.now() + timedelta(days=365),
        includes_bots_in_aggregates=False )
    
    import asyncio
    if num_questions:
        questions = asyncio.run(MetaculusApi.get_questions_matching_filter(
            api_filter, num_questions=num_questions, randomly_sample=True))
    else:
        questions = asyncio.run(MetaculusApi.get_questions_matching_filter(
            api_filter, num_questions=num_questions, randomly_sample=True))

    from community_forecast import community_forecast
    id_to_forecast = {question.api_json['id']: community_forecast(question) for question in questions}

    from flatten_dict import flatten_dict
    import pandas as pd
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