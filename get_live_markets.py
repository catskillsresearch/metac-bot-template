import requests
from get_forecastex_markets import get_forecastex_markets

def get_live_markets():
    url = "https://forecasttrader.interactivebrokers.com/tws.proxy/public/forecasttrader/category/tree"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
    except Exception as e:
        print("Error during request:", e)
    return get_forecastex_markets(json_data)