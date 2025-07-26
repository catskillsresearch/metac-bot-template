import numpy as np
from smooth_percentiles import smooth_percentiles

def forecast_eps_distribution(eps_values, percentiles=201, simulations=10000, random_seed=42):
    """
    Forecast the distribution of next quarter's EPS using empirical bootstrap.

    Parameters:
    - eps_values (list or array): Last 5 diluted EPS values (e.g., [1.53, 1.40, 0.97, 2.40, 1.65])
    - percentiles (int): Number of percentiles (default 201 for 0 to 100 in 0.5% steps)
    - simulations (int): Number of bootstrap samples (default 10,000)
    - random_seed (int): Seed for reproducibility

    Returns:
    - np.ndarray: 201-element array of EPS values at percentiles from 0 to 100
    """

    if len(eps_values) != 5:
        raise ValueError("You must provide exactly 5 historical EPS values.")

    np.random.seed(random_seed)

    # Convert to NumPy array
    eps_values = np.array(eps_values)

    # Bootstrap resampling
    simulated_eps = np.random.choice(eps_values, size=simulations, replace=True)

    # Calculate desired percentiles
    pct_values = np.linspace(0, 100, percentiles)
    eps_distribution = smooth_percentiles(np.percentile(simulated_eps, pct_values))

    return pct_values, eps_distribution