from extract_python import extract_python
from humor_me import humor_me
from datetime import datetime

def get_forward_period_start_and_end_date(ifp):
    today = str(datetime.now())[0:10]
    if ifp['sources'] and ifp['sources'][0][0] == 'macrotrends':
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
        try:
            period = ifp['title'].split('(')[1].split(')')[0]
            prompt = f"""
For this period: {period} please return, as python strings, in format YYYY-MM-DD, 
the start date and end date of the period mentioned, in format
```python
[startDate,endDate]
```

These dates must be after {today}.

Any symbol or name you see in the query refers to a US listed equity (company listed on a stock exchange).
"""
            print(prompt)
            answer = humor_me(prompt)
            return eval(extract_python(answer).strip())
        except:
            prompt = f"""
Today is {today}.
For the period from today to the ending time referred to in this question:

{ifp['title']}

please return, as python strings, in format YYYY-MM-DD, 
the start date and end date of the period mentioned, in format
```python
[startDate,endDate]
```
Any symbol or name you see in the query refers to a US listed equity (company listed on a stock exchange).
"""
            print(prompt)
            answer = humor_me(prompt)
            return eval(extract_python(answer).strip())
        