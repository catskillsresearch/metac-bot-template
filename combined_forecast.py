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
    iterations = 3
    forecasts = [call_local_llm(question.prompt, model) for _ in tqdm(range(iterations))]
    predictions = []
    for i, forecast in enumerate(forecasts):
        question.forecast = forecast
        print("FORECAST", i)
        print(forecast)
        print()
        prediction = extract_percentile_numbers(forecast) if question.question_type == 'numeric' else extract_forecast(question)
        if prediction != {}:
           predictions.append(prediction)
    print("*** Got predictions", predictions)
    if question.question_type == 'binary':
        prediction = float(np.median(predictions))
        comment = f"### Probability: {int(prediction*100)}%"
    elif question.question_type == 'numeric':
        prediction = median_dictionaries(predictions)
        comment = format_multiple_choices(prediction, prefix = 'Percentile ')
    else:
        prediction = median_dictionaries(predictions)
        comment = format_multiple_choices(prediction, 100, '%')
        
    combined = ''
    for i, forecast in enumerate(forecasts):
        combined += f"\nFORECAST {i+1}\n{forecast}\n"
        prompt = f"""The following are {iterations} forecasts on the question "{question.title}".
Each forecast has a rationale and a final prediction section named something like "Final Probability" or "Probabilistic Assessment" or similar.
Considering only the rationale part for each forecast and ignoring the final prediction, combine the rationales into a final consistent rationale that incorporates the best of each individual rationale.
DO present this as a new original rationale.
DO NOT refer to the underlying 5 rationales that you are summarizing
DO NOT include the forecast at the end of the rationale, suppress it.  We are only summarizing the rationale, not the forecast.

{combined}
"""
    rationale = call_local_llm(prompt, model)
    print("RATIONALE\n", rationale)

    median_forecast = f"""{rationale}\n\n{comment}"""
    return median_forecast
