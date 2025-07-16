from fredapi import Fred
import pandas as pd
from datetime import datetime, timedelta
import load_secrets, os
load_secrets.load_secrets()

def get_fred_data(series_id):
    
    # Your API key here!
    fred = Fred(api_key=os.getenv('FRED_API_KEY'))
    
    # Calculate date range: last 365 days from today
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    
    # Download the data
    data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
    
    return data
