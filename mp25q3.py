# # Daily forecast of financial time series group questions

import matplotlib.pylab as plt
from get_market_pulse_25q3_questions import get_market_pulse_25q3_questions
import json, os
from get_underlying_urls import get_underlying_urls
from urls_to_ticker import urls_to_ticker
from pprint import pprint
import os, joblib
from get_data_for import get_data_for
from get_forward_period_start_and_end_date import get_forward_period_start_and_end_date
from get_observable import get_observable
from get_period_type import get_period_type
import pandas as pd
from forecast_high_on_any_day_in_forward_period import forecast_high_on_any_day_in_forward_period
from forecast_close_on_last_day_of_period import forecast_close_on_last_day_of_period
from forecast_stock_price_return_spread import forecast_stock_price_return_spread
from forecast_futures_total_price_return_spread import forecast_futures_total_price_return_spread
from forecast_quarter_diluted_eps_on_next_filing_date import forecast_quarter_diluted_eps_on_next_filing_date
from metaculus_generate_continuous_cdf import metaculus_generate_continuous_cdf
from standardize_cdf import standardize_cdf
from post_group_forecast import post_group_forecast

pd.set_option('display.max_colwidth', 1000)

# Get open questions
ifps = get_market_pulse_25q3_questions()
results = get_underlying_urls(ifps)
results = {int(key): value for key, value in results.items()}
group_id_to_data = {int(x): results[x] for x in results}

# Acquire question data
sources = []
for key, (title, urls) in results.items():
    sources.extend(urls_to_ticker(urls))

sources = list(sorted(set(sources)))
history = {(x,y,z): get_data_for(x,y,z) for x,y,z in sources}

for i, ifp in enumerate(ifps):
    # Organize data
    ifp['sources'] = urls_to_ticker(results[ifp['group']['id']][1])
    ifp['data'] = {x: history[x] for x in ifp['sources']}
    if 'following companies' in ifp['title']:
        company = ifp['title'].split('(')[1].split(')')[0]
        ifp['sources'] = [(x,y,z) for x,y,z in ifp['sources'] if y == company]
        ifp['data'] = {(x,y,z):w for (x,y,z),w in ifp['data'].items() if y == company}

#for i, ifp in enumerate(ifps):
    # Get forward period start and end date
    if 'period' not in ifp:
        ifp['period'] = get_forward_period_start_and_end_date(ifp)

#for i, ifp in enumerate(ifps):
    # Parse observable of data
    if 'observable' not in ifp:
        ifp['observable'] = get_observable(ifp)
        ifp['period_type'] = get_period_type(ifp)

#for i, ifp in enumerate(ifps):
    # Generate forecast for each question
    print(f"[{i}] {ifp['title']}")
    ### High on any day in forward biweekly period from today
    if ifp['observable'] == 'High' and ifp['period_type'] == 'any day in biweekly period':
        rng, prediction = forecast_high_on_any_day_in_forward_period(ifp)
    ### Close on last day of biweekly period
    elif ifp['observable'] == 'Close' and ifp['period_type'] == 'last day of biweekly period':
        rng, prediction = forecast_close_on_last_day_of_period(ifp)
    ### period stock price return on last vs first day of biweekly period
    elif (ifp['observable'], ifp['period_type']) == ('stock price Close return', 'return on last vs first day of biweekly period'):
        rng, prediction = forecast_stock_price_return_spread(ifp)
    ### period futures total price return on last vs first day of biweekly period
    elif (ifp['observable'], ifp['period_type']) == ('futures total price Close return', 'return on last vs first day of biweekly period'):
        rng, prediction = forecast_futures_total_price_return_spread(ifp)
    ### quarter diluted eps on next SEC filing date	
    elif (ifp['observable'], ifp['period_type']) == ('quarter diluted eps', 'next SEC filing date'):
        rng, prediction = forecast_quarter_diluted_eps_on_next_filing_date(ifp)
    ### quarter total revenue on next SEC filing date	
    elif ('quarter total revenue', 'next SEC filing date') == ('quarter total revenue', 'next SEC filing date'):
        rng, prediction = forecast_quarter_diluted_eps_on_next_filing_date(ifp)
    else:
        raise Exception(f"Unhandled question [{ifp['id']}] {ifp['title']}")
    ifp['prediction'] = prediction

#for i, ifp in enumerate(ifps):
    # Submit the question
    row = pd.Series()
    row['id_of_question'] = ifp['id']
    row['id_of_post'] = ifp['post_id']
    row['question_type'] = 'numeric'
    row['forecast'] = """Statistical analysis."""
    p1 = ifp['prediction']
    p1[0] = ifp['scaling']['range_min']
    p1[-1] = ifp['scaling']['range_max']
    p2 = dict(zip(rng,p1))
    p4 = metaculus_generate_continuous_cdf(p2, ifp)
    p5 = standardize_cdf(p4, ifp['scaling'])
    row['prediction'] = p5
    try:
        post_group_forecast(row)
    except Exception as e:
        print("An error occurred:", e)

