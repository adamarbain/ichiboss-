import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, Dict, List

class DataLoader:
    def __init__(self, data_path: Union[str, Path]):
        self.data_path = Path(data_path)
        self._data_cache = {}
        
    def load_market_data(self, symbol: str = 'BTC') -> pd.DataFrame:
        """Load OHLCV market data"""
        price_file = self.data_path / f"{symbol}-FundData-MarketPriceUSD.csv"
        volume_file = self.data_path / f"{symbol}-FundData-MarketVolume.csv"
        
        try:
            price_df = pd.read_csv(price_file)
        except FileNotFoundError:
            print(f"Error: Price data file not found at {price_file}")
            raise
        except Exception as e:
            print(f"Error loading price data: {str(e)}")
            raise
            
        try:
            volume_df = pd.read_csv(volume_file)
        except FileNotFoundError:
            print(f"Error: Volume data file not found at {volume_file}")
            raise
        except Exception as e:
            print(f"Error loading volume data: {str(e)}")
            raise
        
        try:
            # Merge price and volume data using start_time
            market_data = pd.merge(price_df, volume_df, on='start_time', how='inner')
            market_data['start_time'] = pd.to_numeric(market_data['start_time'])
            market_data.set_index('start_time', inplace=True)
        except Exception as e:
            print(f"Error processing market data: {str(e)}")
            raise
            
        # Display general information about the market data
        # print("\nMarket Data Info:")
        # print(market_data.info())
        # print("\nMarket Data Description:")
        # print(market_data.describe())
            
        # print(market_data.head())    
        return market_data
    
    def load_network_data(self, symbol: str = 'BTC') -> Dict[str, pd.DataFrame]:
        """Load all network-related metrics"""
        network_files = self.data_path.glob(f"{symbol}-NetworkData-*.csv")
        network_data = {}
        
        for file in network_files:
            try:
                metric_name = file.stem.split('-')[-1]
                df = pd.read_csv(file)
                df['start_time'] = pd.to_numeric(df['start_time'])
                df.set_index('start_time', inplace=True)
                network_data[metric_name] = df
            except FileNotFoundError:
                print(f"Error: Network data file not found at {file}")
                raise
            except Exception as e:
                print(f"Error loading network data from {file}: {str(e)}")
                raise
            
        # Display general information about the network data
        # print("\nNetwork Data Info:")
        # for metric, df in network_data.items():
        #     print(f"\n{metric} Data Info:")
        #     print(df.info())
        #     print(f"\n{metric} Data Description:")
        #     print(df.describe())
        #     print(f"\n{metric} Data Head:")
        #     print(df.head())
            
        return network_data
    
    def load_miner_data(self, symbol: str = 'BTC') -> Dict[str, pd.DataFrame]:
        """Load all miner-related metrics"""
        miner_files = self.data_path.glob(f"{symbol}-Miner-*.csv")
        miner_data = {}
        
        for file in miner_files:
            try:
                metric_name = file.stem.split('-')[-1]
                df = pd.read_csv(file)
                df['start_time'] = pd.to_numeric(df['start_time'])
                df.set_index('start_time', inplace=True)
                miner_data[metric_name] = df
            except FileNotFoundError:
                print(f"Error: Miner data file not found at {file}")
                raise
            except Exception as e:
                print(f"Error loading miner data from {file}: {str(e)}")
                raise
            
        # Display general information about the miner data
        # print("\nMiner Data Info:")
        # for metric, df in miner_data.items():
        #     print(f"\n{metric} Data Info:")
        #     print(df.info())
        #     print(f"\n{metric} Data Description:")
        #     print(df.describe())
        #     print(f"\n{metric} Data Head:")
        #     print(df.head())
            
        return miner_data
    
    def load_all_data(self, symbol: str = 'BTC') -> Dict[str, Union[pd.DataFrame, Dict[str, pd.DataFrame]]]:
        """Load all available data for a symbol"""

        # Handle duplicate dates by keeping the last value
        market_data = self.load_market_data(symbol).groupby('start_time').last()
        network_data = self.load_network_data(symbol)
        miner_data = self.load_miner_data(symbol)

        # return {
        #     'market': self.load_market_data(symbol),
        #     'network': self.load_network_data(symbol),
        #     'miner': self.load_miner_data(symbol)
        # } 

        return {
            'market': market_data,
            'network': network_data,
            'miner': miner_data
        }