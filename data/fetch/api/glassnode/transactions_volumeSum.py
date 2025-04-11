import requests
import json
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
def transaction_volume():
    url = "https://api.datasource.cybotrade.rs/glassnode/transactions/transfers_volume_adjusted_sum"
    
    headers = {
        "accept": "application/json",
        "X-API-KEY": os.getenv("API_KEY")
    }
    query_params = {
        "a": "BTC",
        "i": "1h",
        "start_time": 1270815381000,
        "limit": 2000   
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

def transaction_transfer_volume_exchanges_net():
    url = "https://api.datasource.cybotrade.rs/glassnode/transactions/transfers_volume_exchanges_net"
    
    headers = {
        "accept": "application/json",
        "X-API-KEY": os.getenv("API_KEY")
    }
    query_params = {
        "a": "BTC",
        "i": "24h",
        "start_time": 1270815381000,
        "limit": 2000   
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


def transaction_Exchange_Withdrawal():
    url = "https://api.datasource.cybotrade.rs/glassnode/transactions/transfers_from_exchanges_count"
    
    headers = {
        "accept": "application/json",
        "X-API-KEY": os.getenv("API_KEY")
    }
    query_params = {
        "a": "BTC",
        "i": "24h",
        "start_time": 1270815381000,
        "limit": 2000   
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
    
def transaction_Exchange_Inflow_Volume():
    url = "https://api.datasource.cybotrade.rs/glassnode/transactions/transfers_volume_to_exchanges_mean"
    
    headers = {
        "accept": "application/json",
        "X-API-KEY": os.getenv("API_KEY")
    }
    query_params = {
        "a": "BTC",
        "i": "24h",
        "start_time": 1270815381000,
        "limit": 2000   
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
    result = transaction_Exchange_Inflow_Volume()
    if result:
        print(json.dumps(result, indent=2)) 