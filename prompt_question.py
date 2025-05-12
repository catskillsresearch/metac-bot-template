from forecasting_tools.ai_models.ai_utils.ai_misc import clean_indents
import numpy as np

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

def prompt_binary(question):
    return clean_indents(prompt_all(question)+
            f"""
(c) A brief description of a scenario that results in a No outcome.
(d) A brief description of a scenario that results in a Yes outcome.

You write your rationale remembering that good forecasters put extra weight on the status quo outcome since the world changes slowly most of the time.

The last thing you write is your final answer as: "Probability: ZZ%", 0-100
            """)

def prompt_multiple_choice(question):
    return clean_indents(prompt_all(question)+
            f"""
(c) A description of an scenario that results in an unexpected outcome.

You write your rationale remembering that (1) good forecasters put extra weight on the status quo outcome since the world changes slowly most of the time, and (2) good forecasters leave some moderate probability on most options to account for unexpected outcomes.

The last thing you write is your final probabilities for the N options in this order {question.question_options} as:
Option_A: Probability_A
Option_B: Probability_B
...
Option_N: Probability_N

where you must assign your probabilities so that Probability_A + Probability_B + ... + Probability_N = 100.
""")

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

The last thing you write is your final answer as this sequence of percentile levels in percent and values as floating point numbers without currency symbols, commas or spelled out numbers like "trillion", just the raw complete number:
"
Percentile 10: XX
Percentile 20: XX
Percentile 40: XX
Percentile 60: XX
Percentile 80: XX
Percentile 90: XX
"
""")

def prompt_question(question):
    methods = {'binary': prompt_binary, 
               'numeric': prompt_numeric, 
               'multiple_choice': prompt_multiple_choice}
    return (methods[question.question_type](question)).strip()
