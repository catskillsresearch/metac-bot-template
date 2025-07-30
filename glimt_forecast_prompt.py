import json
from saved_prompt import saved_prompt
from get_periods_of_whenwill_question import get_periods_of_whenwill_question
from filter_periods_to_today import filter_periods_to_today
from get_event import get_event
from is_election import is_election

def glimt_forecast_prompt(ifp, research):
    (fn, savep) = saved_prompt(ifp)
    if savep: return savep
    ## Prompt with rationale fields split into for and against
    details = ifp['props']['details']
    title = ifp['props']['title']
    bins = [x['props']['title'] for x in ifp['bins']]
    rejected = []
    if 'When' in title or "By what date" in title:
        periods = get_periods_of_whenwill_question(ifp)
        rejected, filtered = filter_periods_to_today(periods)
        original_bins = bins
        event = get_event(ifp)
        bins = [f"{event} between {b} and {c}" for a,b,c in filtered]
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
There should be a reason you are right for each outcome ending with a forecast of form ZZ% where ZZ ranges from 0 to 100.

3. Reasons your probabilities might be wrong, wrapped in tag in this format:
```rWrong
...reasons you might be wrong
```
"""
    with open(fn, 'w') as f:
        json.dump((prompt, rejected), f)
    fn1 = fn.replace('.json', '.txt')
    with open(fn1, 'w') as f:
        f.write(prompt)

    return prompt, rejected