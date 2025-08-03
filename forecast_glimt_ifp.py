from forecast_high_on_any_day_in_forward_period import forecast_high_on_any_day_in_forward_period
from forecast_close_on_last_day_of_period import forecast_close_on_last_day_of_period
from forecast_stock_price_return_spread import forecast_stock_price_return_spread
from forecast_futures_total_price_return_spread import forecast_futures_total_price_return_spread
from forecast_quarter_diluted_eps_on_next_filing_date import forecast_quarter_diluted_eps_on_next_filing_date
from forecast_general_binary import forecast_general_binary

def forecast_glimt_ifp(ifp):
    ifp['forecast'] = """Statistical analysis."""
    ifp['question_type'] = 'numeric'
    ### High on any day in forward biweekly period from today
    (observable, period_type) = (ifp['observable'], ifp['period_type'])
    if observable == 'High' and period_type == 'any day in biweekly period':
        print("******forecast_high_on_any_day_in_forward_period")
        rng, prediction = forecast_high_on_any_day_in_forward_period(ifp)
    ### Close on last day of biweekly period
    elif observable == 'Close' and period_type == 'last day of biweekly period':
        print("******forecast_close_on_last_day_of_period")
        rng, prediction = forecast_close_on_last_day_of_period(ifp)
    ### period stock price return on last vs first day of biweekly period
    elif (observable, period_type) == ('stock price Close return', 'return on last vs first day of biweekly period'):
        print("*** forecast_stock_price_return_spread")
        rng, prediction = forecast_stock_price_return_spread(ifp)
    ### period futures total price return on last vs first day of biweekly period
    elif (observable, period_type) == ('futures total price Close return', 'return on last vs first day of biweekly period'):
        print("*******forecast_futures_total_price_return_spread")
        rng, prediction = forecast_futures_total_price_return_spread(ifp)
    ### quarter diluted eps on next SEC filing date	
    elif (observable, period_type) == ('quarter diluted eps', 'next SEC filing date'):
        print("********forecast_quarter_diluted_eps_on_next_filing_date")
        rng, prediction = forecast_quarter_diluted_eps_on_next_filing_date(ifp)
    ### quarter total revenue on next SEC filing date	
    elif (observable, period_type)  == ('quarter total revenue', 'next SEC filing date'):
        print("*********forecast_quarter_diluted_eps_on_next_filing_date")
        rng, prediction = forecast_quarter_diluted_eps_on_next_filing_date(ifp)
    elif ifp['title'].startswith('Will '):
        print("BINARY")
        forecast_general_binary(ifp)
        rng, prediction = None, ifp['prediction']
    else:
        raise Exception(f"Unhandled question [{ifp['id']}] {ifp['title']} {observable} {period_type}")
    return rng, prediction