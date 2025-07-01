def prompt2_multiple_choice(row, model):
    prompt2 = f"""
You are the intelligence community's best geopolitical, economic and overall news trivia forecaster.  
You will analyse and make a prediction about this question:

```title
{row.title}
```

You take into consideration this news:

```news
{row.asknews}

You take into consideration also this research:

```research
{row.research}
```

This is a multiple choice forecast.  There are N choices.  Each choice is a mutually exclusive event. 
You supply a forecast giving the percentage likelihood that the given event is likely to occur, to the exclusion of the other events.  
The events are:

```choices
{row.question_options}
```

We discriminate between the events as follows:

```resolution_criteria
{row.question_resolution_criteria}
```

The last thing you write is your final probabilities for the possible events in order as:

Choice_A: Probability_A
Choice_B: Probability_B
...
Choice_N: Probability_N

where you must assign your probabilities so they add up to 100: Probability_A + Probability_B + ... + Probability_N = 100.
"""
    return prompt2
