from forecasting_tools import MetaculusApi

def load_live_questions(num_questions = 1):
    questions = MetaculusApi.get_all_open_questions_from_tournament(tournament_id=MetaculusApi.CURRENT_AI_COMPETITION_ID)
    print(f"Num tournament questions: {len(questions)}")
    return questions

if __name__=="__main__":
    from load_secrets import load_secrets
    load_secrets()
    questions = load_live_questions(1)
    for question in questions:
        print(type(question))
