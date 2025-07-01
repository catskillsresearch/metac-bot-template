def prompt2_binary(row, model):
    prompt2 = f"""
    You are the intelligence community's best geopolitical, economic and overall news trivia forecaster.  
    You are given the following information to make a prediction:
    
    ```title
    {row.title}
    ```
    
    ```news
    {row.asknews}
    
    ```research
    {row.research}
    ```
    
    The question defines an event and resolves as YES if the event occurs, otherwise NO. 
    You are forecasting the probability of YES.
    The event is described by the RESOLUTION CRITERIA.
    
    ```resolution_criteria
    {row.question_resolution_criteria}
    ```
    
    The last thing you write is your final answer as: "Probability: ZZ%", 0-100
    """
    return prompt2
