from humor_me import humor_me

def get_event(ifp):

    prompt = f"""What event is the subject of this question.  State the event as something happening in the present:
    
    ```question
    {ifp['props']['title']}
    ```
    
    Please output this as
    
    ```event
    Your event description
    ```
    
    Please use the SIMPLE PRESENT TENSE.
    """
    
    answer = humor_me(prompt)
    return answer.split("```event")[1].split("```")[0].replace('.','').strip()