import requests
import json
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def miner_volume():
    url = "https://api.datasource.cybotrade.rs/glassnode/mining/volume_mined_sum"
    
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
    
def miner_fees():
    url = "https://api.datasource.cybotrade.rs/glassnode/mining/revenue_from_fees"
    
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
    
def miner_total():
    url = "https://api.datasource.cybotrade.rs/glassnode/mining/revenue_sum"
    
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
if __name__ == "__main__":
    result = miner_total()
    if result:
        print(json.dumps(result, indent=2)) 