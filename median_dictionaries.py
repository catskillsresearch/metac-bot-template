import numpy as np

def median_dictionaries(D):
    options = D[0].keys()
    avg = {}
    for option in options:
        avg[option] = np.median([d[option] for d in D])
    return avg
