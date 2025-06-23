import numpy as np
from percentile_from_cdf import percentile_from_cdf

def community_forecast_numeric(question):
    q = question.api_json['question']
    d = {}
    for fld in ['upper_bound',
                'open_upper_bound',
                'lower_bound',
                'open_lower_bound',
                'zero_point']:
        d[fld] = getattr(question, fld)
    for fld in ['aggregations',
                'inbound_outcome_count',
                'my_forecasts',
                'open_lower_bound',
                'open_upper_bound',
                'possibilities',
                'scaling',
                'unit']:
        d[fld] = q[fld]
    P = d['aggregations']['recency_weighted']['latest']['forecast_values']
    V = d['scaling']['continuous_range']
    forecast = {n: percentile_from_cdf(n, V, P) for n in [10, 20, 40, 60, 80, 90]}
    return forecast