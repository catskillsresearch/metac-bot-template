from prompt_terms import prompt_terms

def prompt2_numeric(row, model):
    terms = prompt_terms(row, model)

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

Using the title, news and research, make a forecast according to the formulas you derived in the previous prompt response.
If the Python function has multiple variables, assess each variable individually and then use the function to compute the measure.

The last thing you write is your final answer as this sequence of percentile levels in percent and values as floating point numbers without currency symbols, commas or spelled out numbers like "trillion", just the raw complete number:
"
Percentile 10: XX
Percentile 20: XX
Percentile 40: XX
Percentile 60: XX
Percentile 80: XX
Percentile 90: XX
"
Each line of the final answer MUST START with the word "Percentile".  For example if you have "10: 201" instead of "Percentile 10: 201", that is wrong.

PLEASE REMEMBER THAT THE ANSWER MUST BE IN THE TERMS REQUESTED BY THE PROBLEM.  
A QUICK CORRECTNESS CHECK IS THAT YOUR ANSWER MUST LIE BETWEEN THE MINIMUM AND MAXIMUM VALUES SPECIFIED.  
THE REQUESTED TERMS ARE AS FOLLOWS:

```terms
{terms}
```
"""
    return prompt2
