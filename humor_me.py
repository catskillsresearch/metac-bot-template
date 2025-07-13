from call_local_llm import call_local_llm

def humor_me(question, trial = None):
    txt = call_local_llm(question, 'mistral-small3.2:24b-instruct-2506-q4_K_M', trial)
    print()
    print(txt)
    return txt