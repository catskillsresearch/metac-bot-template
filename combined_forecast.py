import os
from call_local_llm import call_local_llm
from extract_forecast import extract_forecast, extract_percentile_numbers
from format_multiple_choices import format_multiple_choices
import numpy as np
from median_dictionaries import median_dictionaries
from tqdm import tqdm

def combined_forecast(question, iterations, model):
    print("###################################################################")
    print("Combined forecast for", question.id_of_question)
    iterations = 5
    forecasts = [call_local_llm(question.prompt, model) for _ in tqdm(range(iterations))]
    predictions = []
    for forecast in forecasts:
        question.forecast = forecast
        prediction = extract_percentile_numbers(forecast) if question.question_type == 'numeric' else extract_forecast(question)
        if prediction != {}:
           predictions.append(prediction)
    print("*** Got predictions", predictions)
    if question.question_type == 'binary':
        prediction = float(np.median(predictions))
        comment = f"### Probability: {int(prediction*100)}%"
    elif question.question_type == 'numeric':
        prediction = median_dictionaries(predictions)
        comment = format_multiple_choices(prediction)
    else:
        prediction = median_dictionaries(predictions)
        comment = format_multiple_choices(prediction, 100, '%')
        
    combined = ''
    for i, forecast in enumerate(forecasts):
        combined += f"\nFORECAST {i+1}\n{forecast}\n"
    prompt = f"""The following are {iterations} forecasts on the question "{question.title}".
Each forecast has a rationale and a final prediction section named something like "Final Probability" or "Probabilistic Assessment" or similar.
Considering only the rationale part for each forecast and ignoring the final prediction, combine the rationales into a final consistent rationale that incorporates the best of each individual rationale.
Do not tell the reader that you are summarizing or looking at the original forecasts when making this rationale.  Present it as an entirely new rationale.  Do not start with any phrase similar to "Here is a combined rationale that incorporates the best of each individual rationale" or "Here is a rationale that combines the best of each individual forecast."  You MUST have a forecast of some sort.  NEVER produce a forecas without some final prediction in the correct format, even if you have to make one up.

{combined}
"""
    rationale = llm(prompt)
    print("RATIONALE\n", rationale)

    median_forecast = f"""{rationale}\n\n{comment}"""
    return median_forecast
