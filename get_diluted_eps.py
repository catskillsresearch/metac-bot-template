import yfinance as yf

def get_diluted_eps(ticker):
    aapl = yf.Ticker(ticker)
    quarterly_income = aapl.quarterly_income_stmt
    return quarterly_income.loc['Diluted EPS'].sort_index()