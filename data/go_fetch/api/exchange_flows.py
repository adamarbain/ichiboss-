import requests
import json
from urllib.parse import urlencode

def reserve():
    url = "https://api.datasource.cybotrade.rs/cryptoquant/btc/exchange-flows/reserve"
    
    headers = {
        "accept": "application/json",
        "X-API-KEY": "iheM86n8mn8vC3vjOE444vlVTP5sTuBb71FJuVKQc5UqdIBn"
    }
    
    query_params = {
        "exchange": "all_exchange",
        "window": "day",
        "limit": 20
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
    result = reserve()
    if result:
        print(json.dumps(result, indent=2)) 