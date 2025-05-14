def forecast(num_questions = 4, perennial = False, live = False):

    from load_secrets import load_secrets
    load_secrets()
    
    from gather_questions import gather_questions
    questions, df = gather_questions(num_questions, perennial, live)
    if questions is None:
        return

    from gather_research_and_set_prompt import gather_research_and_set_prompt
    df, rag = gather_research_and_set_prompt(df)

    from generate_forecasts_and_update_rag import generate_forecasts_and_update_rag
    df = generate_forecasts_and_update_rag(df, rag, live)

    from post_forecasts import post_forecasts
    return post_forecasts(df, perennial, live)
