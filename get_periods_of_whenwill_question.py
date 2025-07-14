from humor_me import humor_me

def get_periods_of_whenwill_question(ifp):
    startDay = ifp['dates']['startDay']
    endDay = ifp['dates']['endDay']
    periods = [x['props']['title'] for x in ifp['bins']]
    prompt = f"""
An event could happen some time between {startDay} and {endDay}, or it can never happen before {endDay}.
We break this down descriptively into the following N={len(periods)} names for periods of time:

{'\n'.join(periods)}

Please assign date intervals for each period as a Python list of tuples 
```python
[(periodName1,periodStart1,periodEnd1),...,(periodNameN,periodStartN,periodEndN)]
```
where periodEndN, the end of the last period, can be 21000101 if there is an indefinite end date.
Do not wrap the period start and end dates with quote signs."""

    answer = humor_me(prompt)
    result = answer.split('```python')[1].split('```')[0]
    return eval(result)