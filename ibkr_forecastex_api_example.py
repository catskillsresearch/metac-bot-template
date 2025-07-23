
"""
IBKR Web API Example: Accessing ForecastEx Contract Data for NYC Mayor Election
Contract ID: 796056051, Symbol: MNYCG

Prerequisites:
1. IBKR Pro account with ForecastEx permissions
2. Client Portal Gateway running on localhost:5000
3. Authenticated brokerage session
"""

import requests
import json
import time
from datetime import datetime

class IBKRForecastAPI:
    def __init__(self, base_url="https://localhost:5000/v1/api"):
        self.base_url = base_url
        self.session = requests.Session()
        # Disable SSL verification for localhost (Client Portal Gateway)
        self.session.verify = False

    def check_auth_status(self):
        """Check if the brokerage session is authenticated"""
        url = f"{self.base_url}/iserver/auth/status"
        response = self.session.get(url)
        return response.json()

    def initialize_session(self):
        """Initialize brokerage session if needed"""
        url = f"{self.base_url}/iserver/auth/ssodh/init"
        response = self.session.post(url)
        return response.json()

    def search_contract(self, symbol="MNYCG"):
        """Search for ForecastEx contract by symbol"""
        url = f"{self.base_url}/iserver/secdef/search"
        params = {"symbol": symbol}
        response = self.session.get(url, params=params)
        return response.json()

    def get_contract_details(self, conid=796056051):
        """Get detailed contract information"""
        url = f"{self.base_url}/iserver/secdef/info"
        params = {
            "conid": conid,
            "sectype": "OPT",
            "exchange": "FORECASTX"
        }
        response = self.session.get(url, params=params)
        return response.json()

    def get_market_snapshot(self, conid=796056051):
        """Get real-time market data snapshot"""
        url = f"{self.base_url}/iserver/marketdata/snapshot"
        params = {
            "conids": conid,
            "fields": "31,84,85,86,88,7059"  # Last, Bid, Ask Size, Ask, Bid Size, Last Size
        }
        response = self.session.get(url, params=params)
        return response.json()

    def get_historical_data(self, conid=796056051, period="1d", bar="1h"):
        """Get historical market data"""
        url = f"{self.base_url}/iserver/marketdata/history"
        params = {
            "conid": conid,
            "period": period,
            "bar": bar,
            "startTime": datetime.now().strftime("%Y%m%d-%H:%M:%S")
        }
        response = self.session.get(url, params=params)
        return response.json()

    def get_nyc_mayor_election_data(self):
        """Complete workflow to get NYC Mayor election contract data"""
        try:
            # 1. Check authentication
            auth_status = self.check_auth_status()
            print(f"Auth Status: {auth_status}")

            if not auth_status.get('authenticated', False):
                print("Initializing brokerage session...")
                self.initialize_session()
                time.sleep(2)  # Wait for session initialization

            # 2. Search for MNYCG contract
            print("\nSearching for MNYCG contract...")
            search_results = self.search_contract("MNYCG")
            print(f"Search Results: {json.dumps(search_results, indent=2)}")

            # 3. Get contract details
            print("\nGetting contract details...")
            contract_details = self.get_contract_details(796056051)
            print(f"Contract Details: {json.dumps(contract_details, indent=2)}")

            # 4. Get current market data
            print("\nGetting market snapshot...")
            market_data = self.get_market_snapshot(796056051)
            print(f"Market Data: {json.dumps(market_data, indent=2)}")

            # 5. Parse and display key information
            if market_data and len(market_data) > 0:
                data = market_data[0]
                print("\n" + "="*50)
                print("NYC MAYOR ELECTION CONTRACT (MNYCG)")
                print("="*50)
                print(f"Contract ID: {data.get('conid', 'N/A')}")
                print(f"Last Price: ${data.get('31', 'N/A')}")
                print(f"Bid: ${data.get('84', 'N/A')} (Size: {data.get('88', 'N/A')})")
                print(f"Ask: ${data.get('86', 'N/A')} (Size: {data.get('85', 'N/A')})")
                print(f"Last Size: {data.get('7059', 'N/A')}")
                print(f"Updated: {datetime.fromtimestamp(data.get('_updated', 0)/1000)}")
                print("="*50)

            # 6. Get historical data if available
            print("\nGetting historical data...")
            historical_data = self.get_historical_data(796056051)
            print(f"Historical Data: {json.dumps(historical_data, indent=2)}")

            return {
                "search_results": search_results,
                "contract_details": contract_details,
                "market_data": market_data,
                "historical_data": historical_data
            }

        except Exception as e:
            print(f"Error: {str(e)}")
            return None

# Usage example
if __name__ == "__main__":
    # Initialize API client
    api = IBKRForecastAPI()

    # Get NYC Mayor election data
    result = api.get_nyc_mayor_election_data()

    if result:
        print("\nData retrieval completed successfully!")
    else:
        print("\nData retrieval failed. Check authentication and permissions.")

"""
Expected Market Data Fields for ForecastEx Contracts:
- Field 31: Last Price (current contract price)
- Field 84: Bid Price
- Field 85: Ask Size  
- Field 86: Ask Price
- Field 88: Bid Size
- Field 7059: Last Size

For the NYC Mayor election example, you would see data like:
{
  "conid": 796056051,
  "31": "0.71",      # Last price ($0.71 = 71% probability)
  "84": "0.70",      # Bid price  
  "85": "15",        # Ask size
  "86": "0.72",      # Ask price
  "88": "20",        # Bid size
  "7059": "5",       # Last trade size
  "_updated": 1721590600000  # Timestamp
}

Notes:
1. Prices are in USD and represent probability (e.g., $0.71 = 71% chance)
2. Contract pays $1.00 if prediction is correct, $0.00 if incorrect
3. Market data updates in real-time during trading hours
4. After hours, you get the last available prices from the trading session
5. Historical data is only available while the contract is actively trading
"""
