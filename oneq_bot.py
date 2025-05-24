def oneq_bot(id):
    from load_secrets import load_secrets
    load_secrets()
    
    perennial = False
    live = False
    
    from load_questions import load_questions
    questions, df = load_questions(1, perennial = perennial, live = live, id = id)
    if questions is None:
        print("Can't find", id)
        quit()

    from gather_questions import gather_questions
    questions, df = gather_questions(1, perennial, live)
    if questions is None:
        print("problem gathering data for", id)
        quit()

    from gather_research_and_set_prompt import gather_research_and_set_prompt
    df, rag = gather_research_and_set_prompt(df)

    from generate_forecasts_and_update_rag import generate_forecasts_and_update_rag
    df = generate_forecasts_and_update_rag(df, rag, live)

    from post_forecasts import post_forecasts
    return post_forecasts(df, perennial, live)

if __name__ == "__main__":
    import sys
    id = sys.argv[1]
    oneq_bot(id)
