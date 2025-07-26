from datetime import datetime
import numpy as np
from forecast_eps_distribution import forecast_eps_distribution
import matplotlib.pylab as plt

def forecast_quarter_diluted_eps_on_next_filing_date(ifp):
    title, observable, period_type, period, data = ifp['title'], ifp['observable'],  ifp['period_type'],  ifp['period'], list(ifp['data'].values())[0].dropna()
    underlying = ifp['sources'][0][1]
    rng, forecast = forecast_eps_distribution(data)
    plt.figure(figsize=(15,6))
    plt.plot(rng, forecast);
    plt.ylabel(underlying)
    plt.xlabel('Percentile')
    plt.title(f'forecast_quarter_diluted_eps_on_next_filing_date\nEmpirical CDF of {observable} {period_type} {underlying} in a 10-day period from today');
    return rng, forecast