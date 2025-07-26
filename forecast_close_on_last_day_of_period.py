from datetime import datetime
import numpy as np
from estimate_conditional_percentiles_OAS import estimate_conditional_percentiles_OAS
import matplotlib.pylab as plt

def forecast_close_on_last_day_of_period(ifp):
    print(ifp['title'])
    title, observable, period_type, period, data = ifp['title'], ifp['observable'],  ifp['period_type'],  ifp['period'], ifp['data'][ifp['sources'][0]]
    today = datetime.now()
    print((period_type, period, observable))
    start_date, end_date = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in period]
    lookahead = max(1, np.busday_count(today.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d')))
    A = data.values
    A = A[~np.isnan(A)]
    biweekly = 10
    rng, forecast = estimate_conditional_percentiles_OAS(A, window=biweekly, gap=lookahead, Y=A[-1], epsilon=0.5)
    plt.figure(figsize=(12,6))
    plt.plot(rng, forecast);
    underlying = ifp['sources'][0][1]
    plt.ylabel(underlying)
    plt.xlabel('Percentile')
    plt.title(f'forecast_close_on_last_day_of_period\nEmpirical CDF of {observable} {period_type} {underlying} in a 10-day period from today');
    return rng, forecast