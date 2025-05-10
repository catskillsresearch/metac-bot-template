import numpy as np

def community_forecast_numeric(question):
    """Get denormalized community forecast from a NumericQuestion object"""
    # Correct path to aggregations (nested under "question" in api_json)
    forecast_values = question.api_json["question"]["aggregations"]["recency_weighted"]["latest"]["forecast_values"]
    
    # Get scaling parameters from the correct location
    range_min = question.api_json["question"]["scaling"]["range_min"]  # 0.0
    range_max = question.api_json["question"]["scaling"]["range_max"]  # 8e12
    
    # Denormalize each value in the 100-point forecast distribution
    denorm = np.array([range_min + x*(range_max - range_min) for x in forecast_values])
    pctiles = [10,20,40,60,80,90]
    idx = [2*x-1 for x in pctiles]
    sampled = denorm[idx]
    return dict(zip(pctiles, sampled))