import yfinance as yf

def get_revenue(ticker):
    aapl = yf.Ticker(ticker)
    quarterly_income = aapl.quarterly_income_stmt
    return quarterly_income.loc['Total Revenue'].sort_index()