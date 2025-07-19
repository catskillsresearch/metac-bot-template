import numpy as np
from scipy.stats import scoreatpercentile

def estimate_conditional_percentiles(A, window=10, gap=2, Y=None, epsilon=0.5):
    """
    Estimate the conditional percentile function (inverse CDF) of future max VIX over a window,
    given the current value Y.

    Parameters:
        A (np.array): VIX daily High time series (oldest to most recent).
        window (int): length of forward-looking period (e.g., 10 business days).
        gap (int): number of business days until the period begins (e.g., 2).
        Y (float): current VIX High (defaults to last value in A).
        epsilon (float): matching tolerance window for finding similar Y.

    Returns:
        rng (np.array): array of percentiles [0, 0.5, ..., 100]
        quantiles (np.array): value of X (max VIX) at each percentile
        sample_maxs (np.array): historical max values used in the estimate
    """
    A = np.array(A)
    if Y is None:
        Y = A[-1]
    
    sample_maxs = []
    n = len(A)
    
    # Loop over potential historical 'today' positions
    for i in range(n - gap - window):
        if abs(A[i] - Y) <= epsilon:
            max_val = np.max(A[i + gap: i + gap + window])
            sample_maxs.append(max_val)

    # Not enough matches? Use nearest neighbors
    if len(sample_maxs) < 20:
        differences = np.abs(A[:n - gap - window] - Y)
        nearest_indices = np.argsort(differences)[:50]
        sample_maxs = [np.max(A[i + gap: i + gap + window]) for i in nearest_indices]

    sample_maxs = np.array(sample_maxs)

    # Generate percentile values at desired resolution
    rng = np.arange(0, 100.5, 0.5)  # 0 to 100 inclusive in 0.5 steps
    quantiles = np.percentile(sample_maxs, rng)

    return rng, quantiles
