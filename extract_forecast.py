import re
import numpy as np
from ensure_min_increase import ensure_min_increase

def extract_probability_from_response_as_percentage_not_decimal(
    forecast_text: str,
) -> float:
    matches = re.findall(r"(\d+)%", forecast_text)
    if matches:
        # Return the last number found before a '%'
        number = int(matches[-1])
        number = min(99, max(1, number))  # clamp the number between 1 and 99
        return float(number)
    else:
        raise ValueError(f"Could not extract prediction from response: {forecast_text}")

def extract_percentile_numbers(text) -> dict:
    """Extracts percentile values from text with flexible formatting"""
    pattern = r"(?i)^\s*(?:percentile\s+)?(\d+)\s*:\s*(-?\s*\d[\d,.]*)\s*$"
    percentile_values = {}

    for line in text.split("\n"):
        match = re.match(pattern, line)
        if match:
            percentile_str, value_str = match.groups()
            # print('extracting percentile', percentile_str, 'value', value_str)

            # Parse percentile (integer)
            percentile = int(percentile_str.replace(",", "").strip())
            
            # Parse value (float/int)
            clean_value = value_str.replace(",", "").replace(" ", "")
            if clean_value.count('.') > 1:  # Invalid number format
                continue
                
            value = float(clean_value) if '.' in clean_value else int(clean_value)
            
            percentile_values[percentile] = value

    return percentile_values

def extract_option_probabilities_from_response(forecast_text: str, options) -> float:

    # Helper function that returns a list of tuples with numbers for all lines with Percentile
    def extract_option_probabilities(text):

        # Number extraction pattern
        number_pattern = r"-?\d+(?:,\d{3})*(?:\.\d+)?"

        results = []

        # Iterate through each line in the text
        for line in text.split("\n"):
            # Extract all numbers from the line
            numbers = re.findall(number_pattern, line)
            numbers_no_commas = [num.replace(",", "") for num in numbers]
            # Convert strings to float or int
            numbers = [
                float(num) if "." in num else int(num) for num in numbers_no_commas
            ]
            # Add the tuple of numbers to results
            if len(numbers) >= 1:
                last_number = numbers[-1]
                results.append(last_number)

        return results

    option_probabilities = extract_option_probabilities(forecast_text)

    NUM_OPTIONS = len(options)

    if len(option_probabilities) > 0:
        # return the last NUM_OPTIONS items
        return option_probabilities[-NUM_OPTIONS:]
    else:
        raise ValueError(f"Could not extract prediction from response: {forecast_text}")

def generate_multiple_choice_forecast(options, option_probabilities) -> dict:
    """
    Returns: dict corresponding to the probabilities of each option.
    """

    # confirm that there is a probability for each option
    if len(options) != len(option_probabilities):
        raise ValueError(
            f"Number of options ({len(options)}) does not match number of probabilities ({len(option_probabilities)})"
        )

    # Ensure we are using decimals
    total_sum = sum(option_probabilities)
    decimal_list = [x / total_sum for x in option_probabilities]

    def normalize_list(float_list):
        # Step 1: Clamp values
        clamped_list = [max(min(x, 0.99), 0.01) for x in float_list]

        # Step 2: Calculate the sum of all elements
        total_sum = sum(clamped_list)

        # Step 3: Normalize the list so that all elements add up to 1
        normalized_list = [x / total_sum for x in clamped_list]

        # Step 4: Adjust for any small floating-point errors
        adjustment = 1.0 - sum(normalized_list)
        normalized_list[-1] += adjustment

        return normalized_list

    normalized_option_probabilities = normalize_list(decimal_list)

    probability_yes_per_category = {}
    for i in range(len(options)):
        probability_yes_per_category[options[i]] = normalized_option_probabilities[i]

    return probability_yes_per_category

def extract_forecast(row):
    #print("EXTRACT_FORECAST", row.id_of_question)
    if row.question_type == 'binary':
        prediction = extract_probability_from_response_as_percentage_not_decimal(row.forecast)/100.0
    elif row.question_type == 'multiple_choice':
        options = eval(row.question_options)
        option_probabilities = extract_option_probabilities_from_response(row.forecast, options)
        prediction = generate_multiple_choice_forecast(options, option_probabilities)
    elif row.question_type == 'numeric':
        return extract_percentile_numbers(row.forecast)
    return prediction
    
if __name__=="__main__":
    import pandas as pd
    df = pd.read_json('community_results.json')
    df['prediction'] = df.apply(extract_forecast  , axis=1)
    print(df[['id_of_question', 'title', 'prediction']])

    
