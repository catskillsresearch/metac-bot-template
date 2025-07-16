import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_next_quarter_measure(eps_last_5):
    eps = np.array(eps_last_5)
    n = len(eps)
    if n != 5:
        raise ValueError("Input must be exactly 5 quarters.")
    
    # 1. Naive
    naive = eps[-1]
    
    # 2. Average
    avg = np.mean(eps)
    
    # 3. Drift
    drift = eps[-1] + (eps[-1] - eps[0]) / (n - 1)
    
    # 4. Linear Regression
    X = np.arange(1, n+1).reshape(-1, 1)
    lr = LinearRegression().fit(X, eps)
    lr_forecast = lr.predict([[n+1]])[0]
    
    return {
        'Naive': naive,
        'Average': avg,
        'Drift': drift,
        'Linear Regression': lr_forecast,
        'Median': np.median(np.array([naive, avg, drift, lr_forecast]))
    }