import numpy as np

def compute_rolling_returns(prices, window=10):
    prices = np.array(prices)
    return np.array([prices[i + window - 1] / prices[i] for i in range(len(prices) - window + 1)])
