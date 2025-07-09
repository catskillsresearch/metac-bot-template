
import pandas as pd

def compute_return_difference(df):
    """
    Compute the 10-day return difference between NVDA and AAPL.

    Parameters:
    df (pd.DataFrame): DataFrame with columns as tickers and rows as dates.
                       Each cell contains the adjusted close price.

    Returns:
    pd.Series: Time series of the 10-day return difference, indexed by the end date.
    """
    # Ensure the DataFrame is sorted by date
    df = df.sort_index()

    # Initialize the result Series
    result = pd.Series(dtype=float)

    # Iterate over each possible end date of the 10-day period
    for end_date in df.index[9:]:  # Start from the 10th day
        start_date = df.index[df.index.get_loc(end_date) - 9]

        # Calculate 10-day returns for NVDA and AAPL
        nvda_return = 100 * (df.loc[end_date, 'NVDA'] - df.loc[start_date, 'NVDA']) / df.loc[start_date, 'NVDA']
        aapl_return = 100 * (df.loc[end_date, 'AAPL'] - df.loc[start_date, 'AAPL']) / df.loc[start_date, 'AAPL']

        # Calculate the difference
        return_diff = nvda_return - aapl_return

        # Add to the result Series
        result[end_date] = return_diff

    return result

# Example usage:
# Assuming df is your DataFrame with columns 'NVDA' and 'AAPL' and dates as index
# df = pd.read_csv('your_data.csv', index_col='Date', parse_dates=True)
# return_difference = compute_return_difference(df)
# print(return_difference)
