import pandas as pd
import numpy as np
from typing import Dict, Union, List

class DataPreprocessor:
    def __init__(self):
        self._feature_cache = {}
        
    def clean_market_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare market data"""
        # Remove any rows with NaN values
        df = df.dropna()
        
        # Ensure numeric columns are float type
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].astype(float)
        
        return df
    
    def create_features(self, market_data: pd.DataFrame, 
                       network_data: Dict[str, pd.DataFrame],
                       miner_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Create technical and fundamental features"""
        features = market_data.copy()
        
        # Add technical indicators
        features['returns'] = features['price'].pct_change()
        features['log_returns'] = np.log(features['price']).diff()
        features['volatility'] = features['returns'].rolling(window=20).std()
        
        # Add network features if available
        if 'AddressesCount' in network_data:
            features['active_addresses'] = network_data['AddressesCount']['value']
            features['address_growth'] = features['active_addresses'].pct_change()
            
        if 'Velocity' in network_data:
            features['network_velocity'] = network_data['Velocity']['value']
            
        # Add miner features if available
        if 'HashRate' in miner_data:
            features['hash_rate'] = miner_data['HashRate']['value']
            features['hash_rate_growth'] = features['hash_rate'].pct_change()
            
        if 'Fees' in miner_data:
            features['miner_fees'] = miner_data['Fees']['value']
            features['fee_ratio'] = features['miner_fees'] / features['volume']
            
        # Remove any rows with NaN values after feature creation
        features = features.dropna()
        
        return features
    
    def align_data(self, *dfs: pd.DataFrame) -> List[pd.DataFrame]:
        """Align multiple dataframes to the same index"""
        # Get the intersection of all indices
        common_index = dfs[0].index
        for df in dfs[1:]:
            common_index = common_index.intersection(df.index)
            
        # Align all dataframes to the common index
        aligned_dfs = [df.loc[common_index] for df in dfs]
        return aligned_dfs 