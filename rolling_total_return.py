import numpy as np

def rolling_total_return(P, window):
    """
    Computes rolling total percentage returns for a series of prices.
    return[i] = 100 * (P[i+window] - P[i]) / P[i]
    P0 = price just before window, P1 = price at end of window.
    Returns array of returns (len = len(P) - window)
    """
    P = np.array(P)
    return 100 * (P[window:] - P[:-window]) / P[:-window]