import json
import requests
import csv
from urllib.parse import urlencode
from api.exchange_flows import reserve

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
        with open('BTC-ExchangeFlows-Reserve.csv', 'a', newline='') as csvfile:
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
                
        print("Data has been written to BTC-ExchangeFlows-Reserve.csv")
    except Exception as e:
        print(f"Error processing data: {e}")
        return

if __name__ == "__main__":
    main() 