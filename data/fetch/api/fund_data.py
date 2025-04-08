import requests
import json
from urllib.parse import urlencode

def market_price_usd():
    url = "https://api.datasource.cybotrade.rs/cryptoquant/btc/fund-data/market-price-usd"
    
    headers = {
        "accept": "application/json",
        "X-API-KEY": "iheM86n8mn8vC3vjOE444vlVTP5sTuBb71FJuVKQc5UqdIBn"
    }
    
    query_params = {
        "symbol": "gbtc",
        "window": "hour",
        "limit": 10000
    }
    
    # Build the URL with query parameters
    full_url = f"{url}?{urlencode(query_params)}"
    
    try:
        # Make the GET request
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response and return the dictionary
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None

def market_volume_usd():
    url = "https://api.datasource.cybotrade.rs/cryptoquant/btc/fund-data/market-volume"
    
    headers = {
        "accept": "application/json",
        "X-API-KEY": "iheM86n8mn8vC3vjOE444vlVTP5sTuBb71FJuVKQc5UqdIBn"
    }

    query_params = {
        "symbol": "gbtc",
        "window": "day",
        "limit": 10000
    }

    # Build the URL with query parameters
    full_url = f"{url}?{urlencode(query_params)}"
    
    try:
        # Make the GET request
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the JSON response and return the dictionary
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None
    
    

if __name__ == "__main__":
    result = market_price_usd()
    if result:
        print(json.dumps(result, indent=2)) 