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
        
        price_df = pd.read_csv(price_file)
        volume_df = pd.read_csv(volume_file)
        
        # Merge price and volume data
        market_data = pd.merge(price_df, volume_df, on='date', how='inner')
        market_data['date'] = pd.to_datetime(market_data['date'])
        market_data.set_index('date', inplace=True)
        
        return market_data
    
    def load_network_data(self, symbol: str = 'BTC') -> Dict[str, pd.DataFrame]:
        """Load all network-related metrics"""
        network_files = self.data_path.glob(f"{symbol}-NetworkData-*.csv")
        network_data = {}
        
        for file in network_files:
            metric_name = file.stem.split('-')[-1]
            df = pd.read_csv(file)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            network_data[metric_name] = df
            
        return network_data
    
    def load_miner_data(self, symbol: str = 'BTC') -> Dict[str, pd.DataFrame]:
        """Load all miner-related metrics"""
        miner_files = self.data_path.glob(f"{symbol}-Miner-*.csv")
        miner_data = {}
        
        for file in miner_files:
            metric_name = file.stem.split('-')[-1]
            df = pd.read_csv(file)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            miner_data[metric_name] = df
            
        return miner_data
    
    def load_all_data(self, symbol: str = 'BTC') -> Dict[str, Union[pd.DataFrame, Dict[str, pd.DataFrame]]]:
        """Load all available data for a symbol"""
        return {
            'market': self.load_market_data(symbol),
            'network': self.load_network_data(symbol),
            'miner': self.load_miner_data(symbol)
        } 