def prompt_terms(row, model):
    prompt = f"""Here is some information about a question:

TITLE
=====

{row.title}

RESOLUTION CRITERIA
===================

{row.question_resolution_criteria}

SCALE
=====

From {row.question_scaling_range_min} to {row.question_scaling_range_max}

Using the information, answer the following questions:

a.  What is the minimum value for the answer?
b.  What is the maximum value for the answer?
c.  Is there a formula for the answer given in the above text?
d.  If there is a formula, what needs to go into the formula and how do you estimate it?  Write a python function for the formula, commenting its inputs and outputs for clarity.
"""

    from call_local_llm import call_local_llm
    terms = call_local_llm(prompt, model)

    return terms
