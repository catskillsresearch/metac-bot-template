import numpy as np
import pandas as pd

def conditional_future_vix_max_cdf(
    vix_high_df,             # DataFrame with Date index & column '^VIX'
    today,                   # Today's date as 'YYYY-MM-DD'
    future_start,            # Start of window as 'YYYY-MM-DD'
    future_end,              # End of window as 'YYYY-MM-DD'
    band=0.5                 # Conditioning band in VIX units, e.g. ±0.5
):
    # Ensure pandas datetime
    vix = vix_high_df.copy()
    vix.index = pd.to_datetime(vix.index)
    today = pd.to_datetime(today)
    future_start = pd.to_datetime(future_start)
    future_end = pd.to_datetime(future_end)

    today_vix = vix.loc[today]["^VIX"]

    max_list = []

    lookback_days = (future_end - future_start).days + 1  # Calendar days for window

    # Slide over history, skipping periods where we cannot look ahead
    for cur_date in vix.index[:-lookback_days]:
        # Only consider dates with similar VIX (within band)
        if abs(vix.loc[cur_date]["^VIX"] - today_vix) <= band:
            start_idx = vix.index.get_loc(cur_date) + 1
            end_idx = start_idx + lookback_days
            if end_idx <= len(vix):
                future_window = vix.iloc[start_idx:end_idx]["^VIX"]
                max_list.append(future_window.max())
    
    max_array = np.array(max_list)

    # Safeguard: If not enough samples, relax the band
    if len(max_list) < 30:
        idx_close = (np.abs(vix["^VIX"] - today_vix)).argsort()[:50]
        for i in idx_close:
            cur_date = vix.index[i]
            start_idx = i + 1
            end_idx = start_idx + lookback_days
            if end_idx <= len(vix):
                future_window = vix.iloc[start_idx:end_idx]["^VIX"]
                max_list.append(future_window.max())
        max_array = np.array(max_list)

    # Compute 201 percentile values: 0%, 0.5%, ..., 100%
    percentiles = np.linspace(0, 100, 201)
    cdf_values = np.percentile(max_array, percentiles)

    return cdf_values
