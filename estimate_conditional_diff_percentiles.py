import numpy as np
from smooth_percentiles import smooth_percentiles
from compute_rolling_returns import compute_rolling_returns

def estimate_conditional_diff_percentiles(A1, A2, window=10, gap=2, epsilon=0.01):
    # Compute rolling 10-day returns
    R1 = compute_rolling_returns(A1, window=window)
    R2 = compute_rolling_returns(A2, window=window)
    R1_recent = R1[-1]
    R2_recent = R2[-1]
    n = len(R1)
    # Conditional matching
    sample_diffs = []
    for i in range(n - gap):
        try:
            if abs(R1[i] - R1_recent) <= epsilon and abs(R2[i] - R2_recent) <= epsilon:
                # Look 'gap' ahead for the forward returns difference
                if i + gap < n:
                    diff = R2[i + gap] - R1[i + gap]
                    sample_diffs.append(diff)
        except:
            print("ERROR", i, R1_recent, epsilon)
    # If not enough matches, take closest 50
    if len(sample_diffs) < 20:
        diffs_sum = np.abs(R1 - R1_recent) + np.abs(R2 - R2_recent)
        nearest_indices = np.argsort(diffs_sum)[:50]
        sample_diffs = [R2[i + gap] - R1[i + gap] for i in nearest_indices if i + gap < n]
    sample_diffs = np.array(sample_diffs)
    # Percentile calculation
    rng = np.arange(0, 100.5, 0.5)
    quantiles = smooth_percentiles(np.percentile(sample_diffs, rng))
    return rng, quantiles
