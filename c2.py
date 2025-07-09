
import yfinance as yf
import pandas as pd

# Define the ticker symbols and the date range
tickers = ['NVDA', 'AAPL']
start_date = '2024-07-21'
end_date = '2025-07-21'

# Download the historical data
data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

# Save the data to CSV files
data['NVDA'].to_csv('NVDA_adj_close.csv')
data['AAPL'].to_csv('AAPL_adj_close.csv')

# Display the first few rows of the data
print("NVDA Adjusted Closing Prices:")
print(data['NVDA'].head())
print("\nAAPL Adjusted Closing Prices:")
print(data['AAPL'].head())
