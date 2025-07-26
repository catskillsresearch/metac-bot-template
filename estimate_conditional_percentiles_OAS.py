import numpy as np
from smooth_percentiles import smooth_percentiles

def estimate_conditional_percentiles_OAS(A, window=10, gap=2, Y=None, epsilon=0.5):
    """
    Estimate the conditional percentile function (inverse CDF) of the future ending OAS value,
    given the most recent value Y.

    Parameters:
        A (np.array): ICE BofA US High Yield OAS close prices (oldest to most recent).
        window (int): forward-looking period (business days, e.g. 10).
        gap (int): business days until observation begins (e.g. 2).
        Y (float): today's close value; defaults to A[-1].
        epsilon (float): matching window for historical similarity.

    Returns:
        rng (np.array): percentiles from 0 to 100 in 0.5 increments (201 elements).
        quantiles (np.array): value of X at each percentile.
        sample_ends (np.array): historical end values sampled for the estimate.
    """
    A = np.array(A)
    if Y is None:
        Y = A[-1]

    n = len(A)
    sample_ends = []

    # Find historical start dates with similar value to Y
    for i in range(n - gap - window):
        if abs(A[i] - Y) <= epsilon:
            sample_ends.append(A[i + gap + window - 1])

    # If too few matches, take the 50 closest matches
    if len(sample_ends) < 20:
        abs_diffs = np.abs(A[:n - gap - window] - Y)
        nearest_indices = np.argsort(abs_diffs)[:50]
        sample_ends = [A[i + gap + window - 1] for i in nearest_indices]

    sample_ends = np.array(sample_ends)
    rng = np.arange(0, 100.5, 0.5)
    quantiles = smooth_percentiles(np.percentile(sample_ends, rng))

    return rng, quantiles

# Example usage:
# rng, quantiles, sample_ends = estimate_conditional_percentiles_OAS(A)
