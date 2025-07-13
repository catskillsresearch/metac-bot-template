from humor_me import humor_me

def median_rationale(Rs):

    WRs = [f"""```forecast
{x}
```""" for x in Rs]
    
    WRS = '\n'.join(WRs)
    
    prompt = f"""
Summarize the gist of the rationale or thinking of the following answers: 

{WRS}

Do not refer to the provided forecasts.  Just give the summary as if it was a new forecast written by you.

THIS SUMMARY MUST BE 1200 CHARACTERS OR LESS.

DO NOT REFER TO THE FORECASTED PROBABILITY, JUST SUMMARIZE REASONING WITHOUT STATING THE CONCLUSION.
"""
    
    medrat = humor_me(prompt)
    
    return medrat