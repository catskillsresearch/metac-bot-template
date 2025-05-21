from normalized_pdf_distance import normalized_pdf_distance
import numpy as np

def error_binary(row):
    return abs(row.prediction-row.crowd)

def error_numeric(row):
    return normalized_pdf_distance(row.prediction, row.crowd)

def error_multiple_choice(row):
    keys = row.prediction.keys()
    N = len(keys)
    prediction = np.array([row.prediction[key] for key in keys])
    crowd = np.array([row.crowd[key] for key in keys])
    raw_error = np.abs(prediction - crowd).mean()
    
    # Normalize by theoretical maximum MAE
    max_error = 2*(1 - 1/N)/N if N > 1 else 1.0
    return min(raw_error / max_error, 1.0)  # Cap at 1.0

def error(row):
    method = {
        'binary': lambda r: abs(r.prediction - r.crowd),
        'numeric': normalized_pdf_distance,
        'multiple_choice': error_multiple_choice
    }
    try:
        return min(method[row.question_type](row), 1.0)
    except:
        return 1.0  # Maximum error