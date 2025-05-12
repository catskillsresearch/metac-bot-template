def load_open_forecasted_questions(num_questions = 1):
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

    return questions

if __name__=="__main__":
    from load_secrets import load_secrets
    load_secrets()
    questions = load_open_forecasted_questions(4)
    for question in questions:
        print(type(question))

