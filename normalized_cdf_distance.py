import numpy as np

def normalized_cdf_distance(cdf1, cdf2):
    """
    Computes a normalized distance metric between two CDFs defined as 
    201-element arrays on percentiles from 0% to 100%.

    The distance is normalized so that distance=0 indicates identical CDFs,
    and distance=1 indicates maximally different CDFs.

    Parameters:
    cdf1, cdf2 : np.ndarray
        Arrays of length 201 representing cumulative probabilities at percentiles 0, 0.5, ..., 100.

    Returns:
    float
        Normalized distance metric between 0 and 1.
    """
    cdf1 = np.asarray(cdf1)
    cdf2 = np.asarray(cdf2)
    
    # Absolute differences at each percentile
    abs_diff = np.abs(cdf1 - cdf2)
    
    # Since grid is uniform from 0% to 100% with 201 points, spacing is 0.005 = 0.5%
    grid_spacing = 0.005
    
    # Area (sum) between the two CDF curves - approximate integral
    area_diff = np.sum(abs_diff) * grid_spacing
    
    # Maximum possible area_diff is 1 (e.g., cdf1=0 everywhere, cdf2=1 everywhere)
    normalized_distance = area_diff / 1.0
    
    return normalized_distance
