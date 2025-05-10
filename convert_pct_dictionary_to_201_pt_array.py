import numpy as np
from scipy.interpolate import interp1d

def convert_pct_dictionary_to_201_pt_array(user_data):
    """Convert user's percentile forecast to Metaculus-style 201-point format using linear interpolation."""
    # Extract and sort user's data points
    xp = sorted(user_data.keys())
    fp = [user_data[p] for p in xp]
    
    # Add extrapolated 0% and 100% using nearest slope
    if 0 not in xp:
        low_slope = (fp[1] - fp[0]) / (xp[1] - xp[0])
        xp = [0] + xp
        fp = [fp[0] - low_slope * xp[1]] + fp
        
    if 100 not in xp:
        high_slope = (fp[-1] - fp[-2]) / (xp[-1] - xp[-2])
        xp = xp + [100]
        fp = fp + [fp[-1] + high_slope * (100 - xp[-2])]
    
    # Create linear interpolator
    interpolator = interp1d(xp, fp, kind='linear', fill_value='extrapolate')
    
    # Generate 201 points (0.0%, 0.5%, 1.0%, ..., 100.0%)
    return interpolator(np.linspace(0, 100, 201))