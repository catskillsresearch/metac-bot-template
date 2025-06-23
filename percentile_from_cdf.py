import numpy as np
# chatgpt
def percentile_from_cdf(N, V, P):
    """
    Compute the Nth percentile from a discrete cumulative distribution.
    
    Parameters:
    - N: Desired percentile (e.g., 50 for median)
    - V: Array of threshold values, length 200
    - P: Cumulative probabilities, length 201 (P[0] = 0, P[200] = 1)
    
    Returns:
    - The estimated value corresponding to the Nth percentile
    """
    if not (0 <= N <= 100):
        raise ValueError("Percentile N must be in [0, 100]")
        
    target_p = N / 100.0
    
    # Find the first index i such that P[i] >= target_p
    for i in range(1, len(P)):
        if P[i] >= target_p:
            if i == 1:
                return V[0]
            # Linear interpolation between V[i-2] and V[i-1]
            p0, p1 = P[i-1], P[i]
            v0, v1 = V[i-2], V[i-1]
            if p1 == p0:
                return v0  # Avoid divide-by-zero
            alpha = (target_p - p0) / (p1 - p0)
            return v0 + alpha * (v1 - v0)
    
    return V[-1]  # If target_p is not reached (e.g., if P[-1] < 1)