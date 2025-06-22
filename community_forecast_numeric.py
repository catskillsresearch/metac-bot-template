import numpy as np

def community_forecast_numeric(question):
    """
    Extracts percentile values from Metaculus question data
    Returns a dictionary of {percentile: value} for 10, 20, 40, 60, 80, 90
    """
    # Extract the latest forecast values
    question_data = question.api_json['question']
    forecast_values = question_data['aggregations']['recency_weighted']['latest']['forecast_values']
    
    # Generate the x-axis values using the scale parameters
    scale = question_data['possibilities']['scale']
    min_val = scale['min']
    max_val = scale['max']
    deriv_ratio = scale['deriv_ratio']
    n_points = len(forecast_values)
    
    # Generate x-axis locations (matching Metaculus' scaling)
    x_axis = []
    for i in range(n_points):
        x = i / (n_points - 1)
        if deriv_ratio == 1:
            value = min_val + (max_val - min_val) * x
        else:
            term = (deriv_ratio**x - 1) / (deriv_ratio - 1)
            value = min_val + (max_val - min_val) * term
        x_axis.append(value)
    
    # Find values at specific percentiles
    percentiles = [0.10, 0.20, 0.40, 0.60, 0.80, 0.90]
    results = {}
    
    for p in percentiles:
        # Find the index where forecast value first exceeds the percentile
        for idx, f_val in enumerate(forecast_values):
            if f_val >= p:
                # Linear interpolation when possible
                if idx > 0:
                    prev_val = forecast_values[idx-1]
                    prev_x = x_axis[idx-1]
                    weight = (p - prev_val) / (f_val - prev_val)
                    value = prev_x + weight * (x_axis[idx] - prev_x)
                else:
                    value = x_axis[idx]
                results[int(p*100)] = value
                break
    
    return results