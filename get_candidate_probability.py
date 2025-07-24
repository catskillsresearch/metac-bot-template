import requests
from datetime import datetime
import numpy as np

import warnings
warnings.filterwarnings(
    "ignore",
    message="datetime\\.datetime\\.utcfromtimestamp\\(\\) is deprecated.*",
    category=DeprecationWarning
)

def get_candidate_probability(conid, period="1week"):
    url = "https://forecasttrader.interactivebrokers.com/tws.proxy/public/hmds/forecastContract"
    params = {
        "conid": conid,
        "period": period,
        "exchange": "FORECASTX",
        "secType": "OPT"
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()

    timestamps = data.get("time", [])
    prices = data.get("avg", [])
    volume = data.get("volume", [])
    
    if not prices or not timestamps:
        return None

    latest_price = float(prices[-1])
    latest_time = datetime.utcfromtimestamp(int(timestamps[-1]))

    return {
        "conid": conid,
        "probability_pct": latest_price * 100,
        "timestamp": latest_time.isoformat() + "Z",
        "timestamps": int(timestamps[-1]),
        "prices": prices,
        "volume": volume
    }
