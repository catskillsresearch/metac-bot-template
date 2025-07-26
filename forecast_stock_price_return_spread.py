from estimate_conditional_diff_percentiles import estimate_conditional_diff_percentiles
from datetime import datetime
import matplotlib.pylab as plt
import numpy as np

def forecast_stock_price_return_spread(ifp):
    print(ifp['title'])
    title, observable, period_type, period, data = ifp['title'], ifp['observable'],  ifp['period_type'],  ifp['period'], ifp['data']
    today = datetime.now()
    print((period_type, period, observable))
    S2 = ifp['sources'][0]
    S1 = ifp['sources'][1]
    A2 = data[S2]['Close'].values
    A1 = data[S1]['Close'].values
    start_date, end_date = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in period]
    lookahead = np.busday_count(today.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
    biweekly = 10
    underlying = f'R_{ifp['sources'][0][1]}-R_{ifp['sources'][1][1]}'
    rng, forecast = estimate_conditional_diff_percentiles(A1, A2, window=biweekly, gap=lookahead, epsilon=0.5)
    plt.figure(figsize=(15,6))
    plt.plot(rng, forecast);
    plt.ylabel(underlying)
    plt.xlabel('Percentile')
    plt.title(f'forecast_stock_price_return_spread\nEmpirical CDF of {observable} {period_type} {underlying} in a 10-day period from today');
    return rng, forecast