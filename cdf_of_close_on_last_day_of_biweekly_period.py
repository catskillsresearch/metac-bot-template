from datetime import datetime
import numpy as np

def cdf_of_close_on_last_day_of_biweekly_period(ifp):
    title, observable, period_type, period, data = ifp['title'], ifp['observable'],  ifp['period_type'],  ifp['period'], ifp['data'][ifp['sources'][0]]
    today = datetime.now()
    start_date, end_date = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in period]
    lookahead = np.busday_count(today.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
    A = data.values
    A = A[~np.isnan(A)]
    biweekly = 10
    N = len(A)
    observations = A[lookahead+biweekly-1:]
    observations.sort()
    rng = np.arange(0,100.5, 0.5)
    forecast = np.percentile(observations, rng)
    return rng, forecast