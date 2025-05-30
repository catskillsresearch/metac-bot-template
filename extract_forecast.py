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
            print('extracting percentile', percentile_str, 'value', value_str)

            # Parse percentile (integer)
            percentile = int(percentile_str.replace(",", "").strip())
            
            # Parse value (float/int)
            clean_value = value_str.replace(",", "").replace(" ", "")
            if clean_value.count('.') > 1:  # Invalid number format
                continue
                
            value = float(clean_value) if '.' in clean_value else int(clean_value)
            
            percentile_values[percentile] = value

    # Fill missing percentiles linearly if needed
    if percentile_values:
        sorted_keys = sorted(percentile_values.keys())
        for i in range(1, len(sorted_keys)):
            prev_key = sorted_keys[i-1]
            curr_key = sorted_keys[i]
            for k in range(prev_key + 1, curr_key):
                percentile_values[k] = percentile_values[prev_key] + (
                    (k - prev_key) * (percentile_values[curr_key] - percentile_values[prev_key]) 
                    / (curr_key - prev_key)
                )

    return percentile_values

def extract_percentiles_from_response(forecast_text: str) -> dict:

    percentile_values = extract_percentile_numbers(forecast_text)

    if len(percentile_values) > 0:
        return percentile_values
    else:
        raise ValueError(f"Could not extract prediction from response: {forecast_text}")

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

def generate_continuous_cdf(
    percentile_values: dict,
    open_upper_bound: bool,
    open_lower_bound: bool,
    upper_bound: float,
    lower_bound: float,
    zero_point: float | None,
) -> list[float]:
    """
    Returns: list[float]: A list of 201 float values representing the CDF.
    """

    percentile_max = max(float(key) for key in percentile_values.keys())
    percentile_min = min(float(key) for key in percentile_values.keys())
    range_min = lower_bound
    range_max = upper_bound
    range_size = range_max - range_min
    buffer = 1 if range_size > 100 else 0.01 * range_size

    # Adjust any values that are exactly at the bounds
    for percentile, value in list(percentile_values.items()):
        if not open_lower_bound and value <= range_min + buffer:
            percentile_values[percentile] = range_min + buffer
        if not open_upper_bound and value >= range_max - buffer:
            percentile_values[percentile] = range_max - buffer

    # Set cdf values outside range
    if open_upper_bound:
        if range_max > percentile_values[percentile_max]:
            percentile_values[int(100 - (0.5 * (100 - percentile_max)))] = range_max
    else:
        percentile_values[100] = range_max

    # Set cdf values outside range
    if open_lower_bound:
        if range_min < percentile_values[percentile_min]:
            percentile_values[int(0.5 * percentile_min)] = range_min
    else:
        percentile_values[0] = range_min

    sorted_percentile_values = dict(sorted(percentile_values.items()))

    # Normalize percentile keys
    normalized_percentile_values = {}
    for key, value in sorted_percentile_values.items():
        percentile = float(key) / 100
        normalized_percentile_values[percentile] = value


    value_percentiles = {
        value: key for key, value in normalized_percentile_values.items()
    }

    # function for log scaled questions
    def generate_cdf_locations(range_min, range_max, zero_point):
        if zero_point is None or np.isnan(zero_point):
            scale = lambda x: range_min + (range_max - range_min) * x
        else:
            deriv_ratio = (range_max - zero_point) / (range_min - zero_point)
            scale = lambda x: range_min + (range_max - range_min) * (
                deriv_ratio**x - 1
            ) / (deriv_ratio - 1)
        return [scale(x) for x in np.linspace(0, 1, 201)]

    cdf_xaxis = generate_cdf_locations(range_min, range_max, zero_point)

    def linear_interpolation(x_values, xy_pairs):
        # Sort the xy_pairs by x-values
        sorted_pairs = sorted(xy_pairs.items())

        # Extract sorted x and y values
        known_x = [pair[0] for pair in sorted_pairs]
        known_y = [pair[1] for pair in sorted_pairs]

        # Initialize the result list
        y_values = []

        for x in x_values:
            # Check if x is exactly in the known x values
            if x in known_x:
                y_values.append(known_y[known_x.index(x)])
            else:
                # Find the indices of the two nearest known x-values
                i = 0
                while i < len(known_x) and known_x[i] < x:
                    i += 1

                # If x is outside the range of known x-values, use the nearest endpoint
                if i == 0:
                    y_values.append(known_y[0])
                elif i == len(known_x):
                    y_values.append(known_y[-1])
                else:
                    # Perform linear interpolation
                    x0, x1 = known_x[i - 1], known_x[i]
                    y0, y1 = known_y[i - 1], known_y[i]

                    # Linear interpolation formula
                    y = y0 + (x - x0) * (y1 - y0) / (x1 - x0)
                    y_values.append(y)

        return y_values

    continuous_cdf = linear_interpolation(cdf_xaxis, value_percentiles)
    continuous_cdf = ensure_min_increase(continuous_cdf)
    return continuous_cdf

def extract_forecast(row):
    print("EXTRACT_FORECAST", row.id_of_question)
    if row.question_type == 'binary':
        prediction = extract_probability_from_response_as_percentage_not_decimal(row.forecast)/100.0
    elif row.question_type == 'multiple_choice':
        options = eval(row.question_options)
        option_probabilities = extract_option_probabilities_from_response(row.forecast, options)
        prediction = generate_multiple_choice_forecast(options, option_probabilities)
    elif row.question_type == 'numeric':
        percentile_values = extract_percentiles_from_response(row.forecast)
        open_upper_bound = row.question_open_upper_bound > 0
        open_lower_bound = row.question_open_lower_bound > 0
        upper_bound = row.question_scaling_range_max
        lower_bound = row.question_scaling_range_min
        zero_point = row.question_scaling_zero_point
        prediction = generate_continuous_cdf(
                    percentile_values,
                    open_upper_bound,
                    open_lower_bound,
                    upper_bound,
                    lower_bound,
                    zero_point)
    return prediction
    
if __name__=="__main__":
    import pandas as pd
    df = pd.read_json('community_results.json')
    df['prediction'] = df.apply(extract_forecast  , axis=1)
    print(df[['id_of_question', 'title', 'prediction']])

    
