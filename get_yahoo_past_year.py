import yfinance as yf
from datetime import datetime, timedelta

def get_yahoo_past_year(ticker, years = 1):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*years)
    return yf.download(ticker, start=start_date, end=end_date)