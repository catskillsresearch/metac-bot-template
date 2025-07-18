from extract_python import extract_python
from humor_me import humor_me

def get_forward_period_start_and_end_date(ifp):
    if ifp['sources'][0][0] == 'macrotrends':
        prompt = f"""
Extrapolate the next date AFTER THE DATE REFERENCED IN THIS QUESTION:

{ifp['title']}

by following the pattern of this schedule:

{'\n'.join([str(x)[0:10] for x in ifp['data'][ifp['sources'][0]].index.tolist()])}

Please return the date as a Python string in format
```python
'YYYY-MM-DD'
```
"""
    else:
        prompt = f"""
For this question: {ifp['title']} please return, as python strings, in format YYYY-MM-DD, 
the start date and end date of the period mentioned, in format
```python
[startDate,endDate]
```
"""
    answer = humor_me(prompt)
    return eval(extract_python(answer).strip())