from normalized_pdf_distance import normalized_pdf_distance
import numpy as np

def error_binary(row):
    return abs(row.prediction-row.crowd)

def error_numeric(row):
    return normalized_pdf_distance(row.prediction, row.crowd)

def error_multiple_choice(row):
    keys = row.prediction.keys()
    prediction = np.array([row.prediction[key] for key in keys])
    crowd = np.array([row.crowd[key] for key in keys])
    error = np.abs(prediction-crowd).mean()
    return error

def error(row):
    method = eval(f'error_{row.question_type}')
    return method(row)
