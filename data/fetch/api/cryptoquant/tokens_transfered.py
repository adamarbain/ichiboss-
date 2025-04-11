import requests
import json
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def addresses_count():
    url = "https://api.datasource.cybotrade.rs/cryptoquant/btc/network-data/tokens-transferred"
    
    headers = {
        "accept": "application/json",
        "X-API-KEY": os.getenv("API_KEY")
    }
    
    query_params = {
        "window": "day",
        "start_time": "1199145600000", # 2008 01 01
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
    result = addresses_count()
    if result:
        print(json.dumps(result, indent=2)) 