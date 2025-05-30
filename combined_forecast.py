import os
from query_perplexity_with_date_filter import query_perplexity_with_date_filter
from extract_forecast import extract_forecast, extract_percentile_numbers
from format_multiple_choices import format_multiple_choices
import numpy as np
from median_dictionaries import median_dictionaries
from tqdm import tqdm

def combined_forecast(question, iterations):
    # Not exactly median like Metaculus, I'm winging it here
    api_key = os.getenv('PERPLEXITY_API_KEY')
    iterations = 5
    forecasts = [query_perplexity_with_date_filter(api_key, question.prompt, question.today) for _ in tqdm(range(iterations))]
    predictions = []
    for forecast in forecasts:
        question.forecast = forecast
        prediction = extract_percentile_numbers(forecast) if question.question_type == 'numeric' else extract_forecast(question)
        predictions.append(prediction)
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
Do not tell the reader that you are summarizing or looking at the original forecasts when making this rationale.  Present it as an entirely new rationale.

{combined}
"""
    rationale = query_perplexity_with_date_filter(api_key, prompt, question.today)
    print("RATIONALE\n", rationale)

    median_forecast = f"""{rationale}\n\n{comment}"""
    return median_forecast