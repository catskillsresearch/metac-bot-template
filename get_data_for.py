from get_yahoo_past_year import get_yahoo_past_year
from get_fred_data import get_fred_data
from get_diluted_eps import get_diluted_eps
from get_revenue import get_revenue

def get_data_for(source, ticker, observation):
    if source == 'yahoo':
        return get_yahoo_past_year(ticker, 10)
    elif source == 'stlouisfed':
        return get_fred_data(ticker)
    elif source == 'macrotrends':
        if observation == 'eps-earnings-per-share-diluted':
            return get_diluted_eps(ticker)
        elif observation == 'revenue':
            return get_revenue(ticker)
    raise Exception("unknown combo " + str((source, ticker, observation)))