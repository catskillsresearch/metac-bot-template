def make_rationale(forecast, answers, model):
    [a1, a2, a3] = answers
    
    prompt = f"""
    Summarize the gist pf the rationale or thinking of the following answers from 3 different forecasters to a single problem. 
    
    ```forecast 1
    {a1}
    ```
    
    ```forecast 2
    {a2}
    ```
    
    ```forecast 3
    {a3}
    ```
    
    DO NOT REFER TO THE 3 FORECASTERS.  PRESENT THIS AS YOUR OWN THINKING, YOUR OWN RATIONALE.  Use as your final the median forecast which is
    
    ```median forecast
    {forecast}
    ```
    """
    
    from call_local_llm import call_local_llm
    rationale = call_local_llm(prompt, model)

    return rationale
