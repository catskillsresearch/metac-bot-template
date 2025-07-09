
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_return_spread(series):
    """
    Analyze the return spread series to create a CDF and compute percentiles.

    Parameters:
    series (pd.Series): A pandas Series indexed by days with trailing 10-day return spread.

    Returns:
    dict: A dictionary containing the 25th, 50th, and 75th percentiles.
    """
    # Step 1: Create the CDF
    sorted_values = np.sort(series)
    cdf = np.arange(1, len(sorted_values) + 1) / len(sorted_values)

    # Step 2: Plot the CDF (optional)
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_values, cdf, marker='.', linestyle='none')
    plt.xlabel('10-Day Return Spread')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Density Function (CDF) of 10-Day Return Spread')
    plt.grid(True)
    plt.show()

    # Step 3: Compute the percentiles
    percentiles = {
        '25th_percentile': np.percentile(series, 25),
        '50th_percentile': np.percentile(series, 50),
        '75th_percentile': np.percentile(series, 75)
    }

    return percentiles

# Example usage:
# Assuming df_10day_return_spread is your pandas Series
# percentiles = analyze_return_spread(df_10day_return_spread)
# print(percentiles)
