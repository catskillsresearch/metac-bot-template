import numpy as np

def median_forecast(Fs):
    M = np.array(Fs)
    return np.median(M, axis=0).tolist()