import json
import requests
import csv
from urllib.parse import urlencode
from api.exchange_flows import reserve

def ping():
    url = "https://api.datasource.cybotrade.rs/cryptoquant/btc/status/entity-list"
    
    headers = {
        "accept": "application/json",
        "X-API-KEY": "iheM86n8mn8vC3vjOE444vlVTP5sTuBb71FJuVKQc5UqdIBn"
    }
    
    query_params = {
        "type": "exchange",
        "start_time": 1735689600,
        "end_time": 1738368000,
        "limit": 1
    }
    
    # Build the URL with query parameters
    full_url = f"{url}?{urlencode(query_params)}"
    
    try:
        # Make the GET request
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Print the response
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

def main():
    # Call the ping function
    # ping()
    
    # Get data from reserve function
    test = reserve()
    if not test:
        print("Failed to get reserve data")
        return
    
    try:
        # The response is already a dictionary
        data = test
        
        # Write to CSV file
        with open('data.csv', 'a', newline='') as csvfile:
            # Get the fieldnames from the first item in the data
            if isinstance(data, dict) and 'data' in data and data['data']:
                fieldnames = data['data'][0].keys()
            else:
                fieldnames = data.keys() if isinstance(data, dict) else []
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header only if file is empty
            if csvfile.tell() == 0:
                writer.writeheader()
            
            # Write the data
            if isinstance(data, dict) and 'data' in data:
                writer.writerows(data['data'])
            else:
                writer.writerow(data)
                
        print("Data has been written to data.csv")
    except Exception as e:
        print(f"Error processing data: {e}")
        return

if __name__ == "__main__":
    main() 