# load one question

def load_id_question(post_id):
    from forecasting_tools import MetaculusApi
    return [MetaculusApi.get_question_by_post_id(int(post_id))]

if __name__=="__main__":
    from load_secrets import load_secrets
    load_secrets()
    question = load_id_question(38699)
    print(type(question))
