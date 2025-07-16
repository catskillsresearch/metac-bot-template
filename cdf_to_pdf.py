import numpy as np

def cdf_to_pdf(cdf_array):
    """
    Convert a 201-element CDF array to a 201-element PDF array.
    
    Parameters:
    -----------
    cdf_array : np.ndarray
        1D array of length 201 of monotonically increasing CDF values
        corresponding to percentiles 0%, 0.5%, ..., 100%.
        
    Returns:
    --------
    pdf_array : np.ndarray
        1D array of length 201 representing the PDF values.
        PDF is approximated as the numerical derivative of the CDF.
    """
    cdf = np.asarray(cdf_array)
    if cdf.shape[0] != 201:
        raise ValueError("Input CDF array must have length 201.")
    
    # Percentile step in decimal fraction
    percentile_step = 0.005  # (0.5%)
    
    # Approximate PDF by finite differences of CDF
    pdf = np.zeros_like(cdf)
    
    # Forward difference for the first element
    pdf[0] = (cdf[1] - cdf[0]) / percentile_step
    
    # Central differences for elements 1 to -2
    pdf[1:-1] = (cdf[2:] - cdf[:-2]) / (2 * percentile_step)
    
    # Backward difference for the last element
    pdf[-1] = (cdf[-1] - cdf[-2]) / percentile_step
    
    # Since the CDF is of VIX levels vs percentile,
    # this gives a density of VIX values w.r.t percentile.
    # If you want a PDF over VIX values, you may want to take the inverse and re-scale.
    
    # Ensure PDF is non-negative (some numerical noise possible)
    pdf = np.clip(pdf, 0, None)
    
    return pdf
