import numpy as np
from scipy.interpolate import PchipInterpolator

def smooth_percentiles(Y):
    # Input Y: 200 percentile values (corresponding to [0.5, 1, 1.5, ..., 100])
    p_original = np.linspace(0.5, 100, len(Y))
    # Indices where the value changes (step jumps)
    change_idx = np.where(np.diff(Y) != 0)[0] + 1
    key_idx = np.unique(np.concatenate(([0], change_idx, [len(Y)-1])))  # include first & last

    p_key = p_original[key_idx]
    v_key = Y[key_idx]

    # Output grid: 0, 0.5, ...,100 (201 points)
    x_smooth = np.linspace(0, 100, 201)

    # PCHIP for monotonic smoothing
    interp_func = PchipInterpolator(p_key, v_key)
    v_smooth = interp_func(x_smooth)

    return v_smooth
