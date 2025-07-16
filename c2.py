
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define the forecast period
start_date = datetime(2025, 7, 21)
end_date = datetime(2025, 8, 1)

# Define the lookup period (one year before the start date)
LOOKUP_START = start_date - timedelta(days=365)
LOOKUP_END = start_date

# Ticker symbol for VIX
VIX_TICKER = "^VIX"

# Fetch historical data for the lookup period
vix_data = yf.download(VIX_TICKER, start=LOOKUP_START, end=LOOKUP_END)

# Save the data to a CSV file
vix_data.to_csv('vix_historical_data.csv')

# Display the first few rows of the data
print(vix_data.head())

# To get the highest intraday value (maximum "high" value) during the forecast period
forecast_period_data = yf.download(VIX_TICKER, start=start_date, end=end_date)
max_high = forecast_period_data['High'].max()

print(f"The highest intraday value (maximum 'high') of the VIX during the period from {start_date.date()} to {end_date.date()} is: {max_high}")
