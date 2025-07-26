from conditional_difference_distribution import conditional_difference_distribution
from datetime import datetime
import matplotlib.pylab as plt
import numpy as np

def forecast_futures_total_price_return_spread(ifp):
    title, observable, period_type, period, data = ifp['title'], ifp['observable'],  ifp['period_type'],  ifp['period'], ifp['data']
    A2 = data[ifp['sources'][0]]['Close'].values.T[0]
    A1 = data[ifp['sources'][1]]['Close'].values.T[0]
    start_date, end_date = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in period]
    today = datetime.now()
    lookahead = np.busday_count(today.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
    biweekly = 10
    underlying = f'R_{ifp['sources'][0][1]}-R_{ifp['sources'][1][1]}'
    rng, forecast, sample_diffs, pct_of_zero = conditional_difference_distribution(A1, A2, window=biweekly, gap=lookahead, epsilon=0.1)
    plt.figure(figsize=(15,6))
    plt.plot(rng, forecast);
    plt.ylabel(underlying)
    plt.xlabel('Percentile')
    plt.title(f'forecast_futures_total_price_return_spread\nEmpirical CDF of {observable} {period_type} {underlying} in a 10-day period from today');
    return rng, forecast