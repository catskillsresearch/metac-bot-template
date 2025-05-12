# The example questions can be used for testing your bot. (note that question and post id are not always the same)
EXAMPLE_QUESTIONS = [  # (question_id, post_id)
    (578, 578),  # Human Extinction - Binary - https://www.metaculus.com/questions/578/human-extinction-by-2100/
    (14333, 14333),  # Age of Oldest Human - Numeric - https://www.metaculus.com/questions/14333/age-of-oldest-human-as-of-2100/
    (22427, 22427),  # Number of New Leading AI Labs - Multiple Choice - https://www.metaculus.com/questions/22427/number-of-new-leading-ai-labs/
]

def load_perennial_questions():
    from forecasting_tools import MetaculusApi
    return [MetaculusApi.get_question_by_post_id(post_id) for id, post_id in EXAMPLE_QUESTIONS]

if __name__=="__main__":
    from load_secrets import load_secrets
    load_secrets()
    questions = load_perennial_questions()
    for question in questions:
        print(type(question))
