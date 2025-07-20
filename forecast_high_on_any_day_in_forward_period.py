from datetime import datetime
import numpy as np
from estimate_conditional_percentiles import estimate_conditional_percentiles
import matplotlib.pylab as plt

def forecast_high_on_any_day_in_forward_period(ifp):
    print(ifp['title'])
    title, observable, period_type, period, data = ifp['title'], ifp['observable'],  ifp['period_type'],  ifp['period'], ifp['data'][ifp['sources'][0]][ifp['observable']]
    today = datetime.now()
    start_date, end_date = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in period]
    lookahead = np.busday_count(today.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
    A = data.values.T[0]
    biweekly = 10
    rng, forecast = estimate_conditional_percentiles(A, window=biweekly, gap=lookahead, Y=A[-1], epsilon=0.5)
    plt.figure(figsize=(10,6))
    plt.plot(rng, forecast);
    underlying = ifp['sources'][0][1]
    plt.ylabel(underlying)
    plt.xlabel('Percentile')
    plt.title(f'Empirical CDF of maximum intraday {underlying} in a 10-day period from today');
    return rng, forecast