import yfinance as yf
from datetime import datetime, timedelta

def get_yahoo_past_year(ticker):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    return yf.download(ticker, start=start_date, end=end_date)