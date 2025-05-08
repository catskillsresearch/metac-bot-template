#!/usr/bin/env python
# coding: utf-8

# # Base forecaster against historical questions

# ## Imports

# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# In[2]:


from load_secrets import load_secrets
load_secrets()
from forecasting_tools.ai_models.ai_utils.ai_misc import clean_indents
import pandas as pd


# ## Historical data

# In[ ]:


df = pd.read_json('resolved.json')


# In[ ]:


df


# In[ ]:


def load_research(row):
    with open(f"research/{row['id']}.md", 'r') as f:
        return f.read()


# In[ ]:


df['research'] = df.apply(load_research, axis=1)


# In[ ]:


df['today'] = df.apply(lambda row: row.open_time.date().strftime("%Y-%m-%d"), axis=1)


# ## Prompts

# ### Common

# In[ ]:


def prompt_all (question):
    return clean_indents(f"""
You are a professional forecaster interviewing for a job.

Your interview question is:
{question.title}

Question background:
{question.question_description}


This question's outcome will be determined by the specific criteria below. These criteria have not yet been satisfied:
{question.question_resolution_criteria}

{question.question_fine_print}

Your research assistant reports:
{question.research}

Today is {question.today}

Before answering you write:
(a) The time left until the outcome to the question is known.
(b) The status quo outcome if nothing changed.""")


# ### Binary

# In[ ]:


def prompt_binary(question):
    return clean_indents(prompt_all(question)+
            f"""
(c) A brief description of a scenario that results in a No outcome.
(d) A brief description of a scenario that results in a Yes outcome.

You write your rationale remembering that good forecasters put extra weight on the status quo outcome since the world changes slowly most of the time.

The last thing you write is your final answer as: "Probability: ZZ%", 0-100
            """)


# In[ ]:


question_binary = df[df.question_type == 'binary'].iloc[0]
print(prompt_binary(question_binary))


# In[ ]:





# ### Multiple Choice

# In[ ]:


def prompt_multiple_choice(question):
    return clean_indents(prompt_all(question)+
            f"""
(c) A description of an scenario that results in an unexpected outcome.

You write your rationale remembering that (1) good forecasters put extra weight on the status quo outcome since the world changes slowly most of the time, and (2) good forecasters leave some moderate probability on most options to account for unexpected outcomes.

The last thing you write is your final probabilities for the N options in this order {question.question_options} as:
Option_A: Probability_A
Option_B: Probability_B
...
Option_N: Probability_N""")


# In[ ]:


question_multiple_choice = df[df.question_type == 'multiple_choice'].iloc[0]
print(prompt_multiple_choice(question_multiple_choice))


# ### Numeric question

# In[ ]:





# In[ ]:


import numpy as np


# In[ ]:


def _create_upper_and_lower_bound_messages(question):
    if np.isnan(question.question_open_upper_bound):
        upper_bound_message = ""
    else:
        upper_bound_message = (
            f"The outcome can not be higher than {question.question_open_upper_bound}."
        )
    if np.isnan(question.question_open_lower_bound):
        lower_bound_message = ""
    else:
        lower_bound_message = (
            f"The outcome can not be lower than {question.question_open_lower_bound}."
        )
    return upper_bound_message, lower_bound_message


# In[ ]:


def prompt_numeric(question):
    upper_bound_message, lower_bound_message = _create_upper_and_lower_bound_messages(question)
    return clean_indents(prompt_all(question)+
    f"""
Units for answer: {question.question_unit if question.question_unit else "Not stated (please infer this)"}

{lower_bound_message}
{upper_bound_message}

Formatting Instructions:
- Please notice the units requested (e.g. whether you represent a number as 1,000,000 or 1 million).
- Never use scientific notation.
- Always start with a smaller number (more negative if negative) and then increase from there

Before answering you write:
(a) The time left until the outcome to the question is known.
(b) The outcome if nothing changed.
(c) The outcome if the current trend continued.
(d) The expectations of experts and markets.
(e) A brief description of an unexpected scenario that results in a low outcome.
(f) A brief description of an unexpected scenario that results in a high outcome.

You remind yourself that good forecasters are humble and set wide 90/10 confidence intervals to account for unknown unknowns.

The last thing you write is your final answer as:
"
Percentile 10: XX
Percentile 20: XX
Percentile 40: XX
Percentile 60: XX
Percentile 80: XX
Percentile 90: XX
" """)


# In[ ]:


question_numeric = df[df.question_type == 'numeric'].iloc[0]
print(prompt_numeric(question_numeric))


# In[ ]:


prompt_funs = {x: eval(f'prompt_{x}') for x in df.question_type.unique()}
prompt_funs


# In[ ]:


def prompt_question(question):
   return (prompt_funs[question.question_type](question)).strip()


# In[ ]:


df['prompt'] = df.apply(prompt_question, axis=1)


# ## Historical benchmark

# ### Forecast all questions

# In[ ]:


question = df.iloc[0]


# In[ ]:


prompt = question.prompt


# In[ ]:


question.today


# In[ ]:


from query_perplexity_with_date_filter import query_perplexity_with_date_filter


# In[ ]:


from predict import predict


# In[ ]:


import os


# In[ ]:


dfn = 'forecast'
os.makedirs(dfn, exist_ok=True)

forecast = predict(dfn, question)
# In[ ]:


from tqdm import tqdm
tqdm.pandas()


# In[ ]:


get_ipython().system('pwd')


# In[ ]:


df['forecast'] = df.progress_apply(lambda question: predict(dfn, question), axis=1)


# In[ ]:


df.to_json('wow.json')


# ### Reload all forecasts

# In[ ]:


df = pd.read_json('wow.json')


# ### Extract the answer

# ### Binary

# In[ ]:


question = df[df.id == 37008].iloc[0]
question


# In[ ]:


print(question.forecast)


# In[ ]:


import re

def extract_probability(question):
    text = question.forecast
    # Regex to find 'Probability: XX%' or 'Probability: XX'
    text = text.replace('**', '')
    pattern = r"Probability: (\d+)%?"
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    return 50


# In[ ]:


extract_probability(question)


# In[ ]:


question = df[df.id == 35190].iloc[0]
question


# In[ ]:


question = df[df.id == 36168].iloc[0]


# In[ ]:


extract_probability(question)


# In[ ]:





# ### Numeric

# In[ ]:


import re

def extract_percentiles0(question):
    text = question.forecast
    # Regex to find lines like 'Percentile X: number'
    pattern = r"Percentile (\d+): ([\d,]+)"
    matches = re.findall(pattern, text)
    # Convert to dict with integer keys and values (remove commas)
    percentiles = {int(p): int(v.replace(',', '')) for p, v in matches}
    return percentiles


# In[ ]:


import re

def extract_percentiles1(question):
    text = question.forecast
    # Regex to capture "Percentile X: [expression]" with flexible whitespace and special chars
    pattern = r"Percentile\s*(\d+):\s*([^\n]+)"
    matches = re.findall(pattern, text)

    # Clean and store expressions (remove markdown, extra spaces)
    percentiles = {}
    for p, expr in matches:
        p = int(p)
        # Remove common noise characters: *,_ and trim whitespace
        clean_expr = re.sub(r"[*_-]", "", expr).strip()
        percentiles[p] = clean_expr

    return percentiles


# In[ ]:


def extract_percentiles2(question):
    text = question.forecast
    # Regex to capture percentage AFTER '+' and before '%', ignoring other numbers
    pattern = r"Percentile\s*(\d+):\s*.*?([+-]\s*)?(\d*\.?\d+)%"
    matches = re.findall(pattern, text)
    # Extract percentile and percentage value (ignore operator like '+')
    percentiles = {int(p): float(percent) for p, _, percent in matches}
    return percentiles


# In[ ]:


def extract_percentiles3(question):
    text = question.forecast
    # Regex handles commas and variable whitespace
    pattern = r"Percentile\s*(\d+):\s*([\d,]+)"
    matches = re.findall(pattern, text)
    return {int(p): int(v.replace(',', '')) for p, v in matches}


# In[ ]:


import re

def extract_percentiles4(question):
    text = question.forecast
    # Regex to capture percentile lines with flexible formatting
    pattern = r"Percentile\s*(\d+):\s*([^\n]+)"
    matches = re.findall(pattern, text)

    percentiles = {}
    for p, val_str in matches:
        p = int(p)
        val_str = val_str.strip()

        # Check for percentage format (e.g., "S₀ + 0.5%")
        if '%' in val_str:
            pct_match = re.search(r"(\d+\.?\d+)%", val_str.replace(',', ''))
            if pct_match:
                percentiles[p] = float(pct_match.group(1))
        # Check for absolute numeric format (e.g., "1,600,000")
        else:
            num_match = re.search(r"[\d,]+", val_str)
            if num_match:
                percentiles[p] = int(num_match.group(0).replace(',', ''))

    return percentiles


# In[ ]:


def linear_sample_percentiles(range_min, range_max):
    percentiles = [10, 20, 40, 80, 90]
    fractions = [p / 100 for p in percentiles]
    samples = {int(f*100): range_min + f * (range_max - range_min) for f in fractions}
    return samples


# In[ ]:


def extract_percentiles1(question):
    text = question.forecast
    return linear_sample_percentiles(question.question_scaling_range_max, question.question_scaling_range_min)


# In[ ]:


def extract_percentiles(question):
    tries = [f(question) for f in [extract_percentiles0, extract_percentiles3]]
    lengths = [len(x) for x in tries]
    maxlength = max(lengths)
    if maxlength > 0:
        for x in tries:
            if len(x) == maxlength:
                return x
    return extract_percentiles1(question)


# In[ ]:


question = df[df.id == 36164].iloc[0]


# In[ ]:


extract_percentiles(question)


# In[ ]:


question = df.iloc[0]


# In[ ]:


extract_percentiles(question)


# In[ ]:


print(df.iloc[0].question_resolution)


# In[ ]:


question = df[df.id == 35678].iloc[0]


# In[ ]:


extract_percentiles(question)


# ### Multiple choice

# In[ ]:


question = df[df.question_type == 'multiple_choice'].iloc[0]


# In[ ]:


import re

def extract_probabilities(text, question_options, prefix='Option_[A-Z]:'):
    # Regex to capture "Option_X: [label]: [percentage]%"
    pattern = prefix + r"\s*([^:]+?)\s*:\s*\**(\d+)%\**"
    matches = re.findall(pattern, text)

    # Convert to dictionary with percentage values
    prob_map = {}
    for label, pct_str in matches:
        label = label.strip()
        if label in question_options:
            prob_map[label] = int(pct_str) / 100.0

    # Ensure all question options are in the map (0% if missing)
    for option in question_options:
        if option not in prob_map:
            prob_map[option] = 0.0

    return prob_map


# In[ ]:


print(question.forecast)


# In[ ]:


question.question_options


# In[ ]:


question.question_resolution


# In[ ]:


text, question_options = question.forecast, eval(question.question_options)


# In[ ]:


extract_probabilities(text, question_options, '')


# In[ ]:


def extract_multiple_choice(question):
    text, question_options = question.forecast, eval(question.question_options)
    if 'Option_' in text:
        return extract_probabilities(text, question_options)
    else:
        return extract_probabilities(text, question_options, '')


# In[ ]:


question = df[df.id == 36264].iloc[0]


# In[ ]:


print(question.forecast)


# In[ ]:


print(question.question_options)


# In[ ]:


extract_multiple_choice(question)


# In[ ]:


question = df[df.id == 36168].iloc[0]


# In[ ]:


extract_multiple_choice(question)


# In[ ]:


question.question_options


# In[ ]:


print(question.forecast)


# In[ ]:


extract_multiple_choice(question)


# ### All

# In[ ]:


def extract_forecast(question):
    method = {'binary': extract_probability,
              'numeric': extract_percentiles,
              'multiple_choice': extract_multiple_choice}
    return method[question.question_type](question)


# In[ ]:


df['prediction'] = df.apply(extract_forecast, axis=1)


# In[ ]:


df.to_json('run_with_predictions.json')


# ## Scoring rule

# ### Binary

# In[ ]:


df[df.question_type == 'binary'].question_resolution.unique()


# In[ ]:


question = df[df.question_type == 'binary'].iloc[0]


# In[ ]:


question = df[df.id == 35190].iloc[0]
question


# In[ ]:


question.question_resolution, question.prediction


# In[ ]:


def calculate_ubs_binary(instance):
    """
    Calculate Universal Binarized Score (UBS) for a binary question forecast.

    Args:
        instance: Object with:
            - prediction (int/float): Forecast probability for 'yes' (0-100)
            - question_resolution (str): Actual outcome ('yes' or 'no')

    Returns:
        float: UBS score between 0 (worst) and 1 (best)
    """
    # Convert prediction to probability (0.0-1.0 scale)
    p_yes = instance.prediction / 100.0
    p_no = 1.0 - p_yes

    # Convert resolution to binary (1.0 for 'yes', 0.0 for 'no')
    resolution = instance.question_resolution.lower()
    y_yes = 1.0 if resolution == 'yes' else 0.0
    y_no = 1.0 - y_yes

    # Calculate Brier Score (sum of squared errors for both outcomes)
    brier_score = (p_yes - y_yes)**2 + (p_no - y_no)**2

    # Universal Binarized Score (UBS)
    K_max = 2.0  # Maximum possible Brier Score for binary questions
    ubs = 1.0 - (brier_score / K_max)

    return round(ubs, 4)  # Rounded to 4 decimal places for readability


# In[ ]:


calculate_ubs_binary(question)


# ### Numeric

# In[ ]:


def calculate_ubs_numeric(instance):
    """
    Calculate Universal Binarized Score (UBS) for numeric forecasts using CRPS.

    Args:
        instance: Object with:
            - prediction (dict): Percentile-to-value mapping (e.g., {10: 1600000, ...})
            - question_resolution (float): Actual resolved value

    Returns:
        float: UBS score between 0 (worst) and 1 (best)
    """
    percentiles = sorted(instance.prediction.keys())
    values = [float(instance.prediction[p]) for p in percentiles]
    if instance.question_resolution == "below_lower_bound":
        Q = instance.question_scaling_range_min
    elif instance.question_resolution == "above_upper_bound":
        Q = instance.question_scaling_range_max
    else:
        Q = float(instance.question_resolution)
    min_val, max_val = values[0], values[-1]

    # Linear interpolation for CDF
    def cdf(x):
        if x <= min_val: return 0.0
        if x >= max_val: return 1.0
        for i in range(len(values)-1):
            if values[i] <= x < values[i+1]:
                p_low = percentiles[i]/100
                p_high = percentiles[i+1]/100
                return p_low + (x - values[i]) * (p_high - p_low)/(values[i+1] - values[i])
        return 0.0

    # CRPS calculation
    crps = 0.0
    for i in range(len(values)-1):
        v1, v2 = values[i], values[i+1]
        mid = (v1 + v2)/2
        F_mid = cdf(mid)
        I_mid = 1.0 if mid >= Q else 0.0
        crps += (F_mid - I_mid)**2 * (v2 - v1)

    # Tail contributions
    if Q < min_val:
        crps += (0.0 - 1.0)**2 * (min_val - Q)
    elif Q > max_val:
        crps += (1.0 - 0.0)**2 * (Q - max_val)

    # Normalize using question's intrinsic range
    K_max = max_val - min_val
    ubs = 1.0 - (crps / K_max) if K_max != 0 else 0.0
    return max(0.0, min(1.0, round(ubs, 4)))


# In[ ]:


question=df[df.id==35677].iloc[0]


# In[ ]:


print(question.forecast)


# In[ ]:


question.prediction


# In[ ]:


calculate_ubs_numeric(question)


# In[ ]:


question = df[df.question_type == 'numeric'].iloc[0]


# In[ ]:


question


# In[ ]:


print(question.question_resolution)


# In[ ]:


calculate_ubs_numeric(question)


# ### Multiple choice

# In[ ]:


question = df[df.question_type == 'multiple_choice'].iloc[0]


# In[ ]:


question


# In[ ]:


question.prediction, question.question_resolution


# In[ ]:


def calculate_ubs_multiclass(instance):
    """
    Calculate Universal Binarized Score (UBS) for a multi-category question.

    Args:
        instance: Object with:
            - prediction (dict): {category: percentage forecast (0-100)}
            - question_resolution (str): The correct category

    Returns:
        float: UBS score between 0 (worst) and 1 (best)
    """
    categories = list(instance.prediction.keys())
    n = len(categories)
    # Convert predictions to probabilities (0.0-1.0)
    probs = {k: instance.prediction[k]/100.0 for k in categories}
    # Create outcome vector: 1 for correct, 0 for others
    outcome = {k: 1.0 if k == instance.question_resolution else 0.0 for k in categories}
    # Multi-category Brier score
    brier = sum((probs[k] - outcome[k])**2 for k in categories)
    # Normalize by maximum possible score (which is n)
    ubs = 1.0 - (brier / n)
    return max(0.0, min(1.0, round(ubs, 4)))


# In[ ]:


calculate_ubs_multiclass(question)


# In[ ]:


question = df[df.id == 36168].iloc[0]


# In[ ]:


calculate_ubs_multiclass(question)


# ### All

# In[ ]:


def calculate_ubs(question):
    method = {'binary': calculate_ubs_binary,
              'numeric': calculate_ubs_numeric,
              'multiple_choice': calculate_ubs_multiclass}
    return method[question.question_type](question)


# In[ ]:


df['score'] = df.apply(calculate_ubs, axis=1)


# In[ ]:


df.to_json('scored.json')


# ## Historical benchmark

# In[6]:


df = pd.read_json('scored.json')


# In[15]:


ax = df.hist(column='score', bins=10)
plt.show()  # explicitly show the plot


# In[17]:


scores_by_date = df.sort_values(by='open_time')


# In[19]:


scores_by_date.score.mean()


# In[20]:


plt.scatter(scores_by_date.open_time, scores_by_date.score.values)


# In[23]:


((scores_by_date.score-0.5).sum())/len(scores_by_date)


# In[28]:


scores_by_date[['id', 'open_time', 'title', 'score']].to_csv('readme.csv', index=False)


# In[ ]:





# ## Make it more RAGy, using the references in the prompt for possible deeper search

# In[ ]:


df[df.id == 36164].iloc[0]


# In[ ]:




