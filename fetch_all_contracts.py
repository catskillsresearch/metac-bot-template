import requests

def fetch_all_contracts(market_conid):
    # ForecastEx: Get all contracts under the market
    params = {
        "showrestricted": "false",
        "market": market_conid
    }
    market_url = f"https://forecasttrader.interactivebrokers.com/portal.proxy/v1/etp/trsrv/event/contracts"
    r = requests.get(market_url, params=params)
    r.raise_for_status()
    contracts = r.json()["contracts"]
    return contracts