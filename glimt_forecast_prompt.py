from saved_prompt import saved_prompt

def glimt_forecast_prompt(ifp, research):
    (fn, prompt) = saved_prompt(ifp)
    if prompt: return prompt
    ## Prompt with rationale fields split into for and against
    details = ifp['props']['details']
    title = ifp['props']['title']
    bins = [x['props']['title'] for x in ifp['bins']]
    sb1 = '\n'.join([f"""* O{i+1}. {bin}""" for i, bin in enumerate(bins)])
    psum = '+'.join([f'P{i+1}' for i, bin in enumerate(bins)])
    pcom = ','.join([f'P{i+1}' for i, bin in enumerate(bins)])
    sbins = f"""The question has one of {len(bins)} outcomes namely  

{sb1}

Each outcome Oi has a probability Pi where 0 <= Pi <= 1.
We must have that {psum} = 1.0.
Add some reasonable amount of randomness/noise to the estimation of the branches.
The output is a Python list wrapped by a binProbs tag, in this format:
```binProbs
[{pcom}]
```
"""
    prompt = f"""
You are a talented, experienced and confident superforecaster. You are asked a question:

```question
{title}
```

You are given details on how to interpret the terms of the question:

```details
{details}
```

Your assistant has research related news and Wikipedia articles and prepared summaries of each one.
Use the data in these research summaries to analyse the question:

{research}

For you to be marked Successful, you must output 3 things:

1. Probabilities for the outcomes of the question.  
{sbins}

2. Reasons your probabilities might be right, wrapped in tag in this format:
```rRight
...reasons you might be right
```

3. Reasons your probabilities might be wrong, wrapped in tag in this format:
```rWrong
...reasons you might be wrong
```
"""
    with open(fn, 'w') as f:
        f.write(prompt)
    return prompt