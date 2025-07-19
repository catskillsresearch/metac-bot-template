import numpy as np

from rolling_total_return import rolling_total_return

def conditional_difference_distribution(A1, A2, window=10, gap=10, epsilon=0.1):
    """
    Compute empirical conditional distribution of (Gold return - S&P 500 return) after a future window,
    given most recent observed rolling returns for each.
    
    Parameters:
        A1: Gold Futures price array (oldest to most recent)
        A2: S&P 500 Futures price array (oldest to most recent)
        window: length of the returns window (default 10)
        gap: days between 'today' and window start (default 10 business days in this case)
        epsilon: matching tolerance for conditioning
    
    Returns:
        rng: np.array of percentiles (shape: (201,))
        quantiles: np.array of percentile values (shape: (201,))
        sample_diffs: array of historical differences for diagnostics
        pct_of_zero: percentile rank of zero in forecast distribution
    """
    R1 = rolling_total_return(A1, window)
    R2 = rolling_total_return(A2, window)
    R1_recent = R1[-1]
    R2_recent = R2[-1]
    n = len(R1)
    # Find historical episodes where both recent returns were similar to current values
    sample_diffs = []
    for i in range(n - gap - window):
        cond1 = abs(R1[i] - R1_recent) <= epsilon
        cond2 = abs(R2[i] - R2_recent) <= epsilon
        if cond1 and cond2:
            # Look forward gap days and then construct future 10-day return
            j = i + gap  # index of start of future period
            if j + window < len(A1) and j + window < len(A2):
                # P0 is price just before window; P1 is price at end of window
                gc_ret = 100 * (A1[j+window] - A1[j]) / A1[j]
                es_ret = 100 * (A2[j+window] - A2[j]) / A2[j]
                sample_diffs.append(gc_ret - es_ret)
    # If too few matches, select 50 closest matches by distance
    if len(sample_diffs) < 20:
        dist = np.abs(R1[:n-gap-window] - R1_recent) + np.abs(R2[:n-gap-window] - R2_recent)
        nearest = np.argsort(dist)[:50]
        for i in nearest:
            j = i + gap
            if j + window < len(A1) and j + window < len(A2):
                gc_ret = 100 * (A1[j+window] - A1[j]) / A1[j]
                es_ret = 100 * (A2[j+window] - A2[j]) / A2[j]
                sample_diffs.append(gc_ret - es_ret)
    sample_diffs = np.array(sample_diffs)
    rng = np.arange(0, 100.5, 0.5)
    quantiles = np.percentile(sample_diffs, rng)
    # Percentile rank of zero (probability GC - ES ≤ 0)
    pct_of_zero = np.mean(sample_diffs <= 0) * 100
    return rng, quantiles, sample_diffs, pct_of_zero
