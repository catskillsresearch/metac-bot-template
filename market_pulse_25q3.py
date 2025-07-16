import re
import numpy as np
import pandas as pd
import os, requests
from load_secrets import load_secrets
load_secrets()

def ensure_min_increase(lst, min_step=5e-05):
    """
    Ensure each element in the list is at least `min_step` greater than the previous.
    If not, set it to previous + min_step.
    
    Args:
        lst (list of float): Input list of floats.
        min_step (float): Minimum required increase between elements.
        
    Returns:
        list of float: Adjusted list with minimum step enforced.
    """
    if not lst:
        return []
    result = [lst[0]]
    for num in lst[1:]:
        prev = result[-1]
        if num < prev + min_step:
            result.append(prev + min_step)
        else:
            result.append(num)
    return result


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


# @title Helper functions
METACULUS_TOKEN = os.getenv('METACULUS_TOKEN')
AUTH_HEADERS = {"headers": {"Authorization": f"Token {METACULUS_TOKEN}"}}
API_BASE_URL = "https://www.metaculus.com/api"

def create_forecast_payload(
    forecast: float | dict[str, float] | list[float],
    question_type: str,
) -> dict:
    """
    Accepts a forecast and generates the api payload in the correct format.

    If the question is binary, forecast must be a float.
    If the question is multiple choice, forecast must be a dictionary that
      maps question.options labels to floats.
    If the question is numeric, forecast must be a dictionary that maps
      quartiles or percentiles to datetimes, or a 201 value cdf.
    """
    if question_type == "binary":
        return {
            "probability_yes": forecast,
            "probability_yes_per_category": None,
            "continuous_cdf": None,
        }
    if question_type == "multiple_choice":
        return {
            "probability_yes": None,
            "probability_yes_per_category": forecast,
            "continuous_cdf": None,
        }
    # numeric or date
    return {
        "probability_yes": None,
        "probability_yes_per_category": None,
        "continuous_cdf": forecast,
    }

def post_question_prediction(question_id: int, forecast_payload: dict) -> None:
    """
    Post a forecast on a question.
    """
    url = f"{API_BASE_URL}/questions/forecast/"
    response = requests.post(
        url,
        json=[
            {
                "question": question_id,
                **forecast_payload,
            },
        ],
        **AUTH_HEADERS,  # type: ignore
    )
    print(f"Prediction Post status code: {response.status_code}")
    if not response.ok:
        raise RuntimeError(response.text)


def post_question_comment(post_id: int, comment_text: str) -> None:
    """
    Post a comment on the question page as the bot user.
    """
    response = requests.post(
        f"{API_BASE_URL}/comments/create/",
        json= {
            "text": comment_text,
            "parent": None,
            "included_forecast": True,
            "is_private": True,
            "on_post": post_id,
        },
        **AUTH_HEADERS,  # type: ignore
    )
    if not response.ok:
        raise RuntimeError(response.text)

def post_forecast(row):
    question_id = int(row.id_of_question)
    post_id = int(row.id_of_post)
    question_type = row.question_type
    forecast = row.prediction
    comment = row.forecast
    forecast_payload = create_forecast_payload(forecast, question_type)
    post_question_prediction(question_id, forecast_payload)
    post_question_comment(post_id, comment)
    print("Posted forecast for", question_id)

def make_forecast():
    row = pd.Series()

    row['id_of_question'] = 37964
    row['id_of_post'] = 38699
    row['question_type'] = 'numeric'
    row['forecast'] = """We compute the history of the 10-day returns of AAPL and NVDA for one year prior to today.
    We then compute the daily difference of those histories.
    Then we make an empirical cumulative density function from the sorted daily differences.
    Then we report the 25, 50 and 75th percentiles of this distribution as our forecast.
    """
    row['question_open_upper_bound'] =  True
    row['question_open_lower_bound'] =  True
    row['question_scaling_range_max'] =  20.0
    row['question_scaling_range_min'] =  -20.0
    row['question_scaling_zero_point'] =  None
    
    row['prediction'] = generate_continuous_cdf(
                        percentile_values.copy(),
                        row.question_open_upper_bound,
                        row.question_open_lower_bound,
                        row.question_scaling_range_max,
                        row.question_scaling_range_min,
                        row.question_scaling_zero_point)
    
    post_forecast(row)
