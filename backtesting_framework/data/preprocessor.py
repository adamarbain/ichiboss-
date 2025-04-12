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
        features['returns'] = features['price_usd_close'].pct_change()
        features['log_returns'] = np.log(features['price_usd_close']).diff()
        features['volatility'] = features['returns'].rolling(window=20).std()
        
        
        # Add network features if available
        if 'AddressesCount' in network_data:
            if 'tokens_transferred_total' in network_data['AddressesCount'].columns:
                features['active_addresses'] = network_data['AddressesCount']['tokens_transferred_total']
                features['address_growth'] = features['active_addresses'].pct_change()
            else:
                print("Warning: 'tokens_transferred_total' not found in AddressesCount data.")
            
        if 'Velocity' in network_data:
            if 'velocity_supply_total' in network_data['Velocity'].columns:
                features['network_velocity'] = network_data['Velocity']['velocity_supply_total']
            else:
                print("Warning: 'velocity_supply_total' not found in Velocity data.")
        
        # Add miner features if available
        if 'HashRate' in miner_data:
            if 'v' in miner_data['HashRate'].columns:
                features['hash_rate'] = miner_data['HashRate']['v']
                features['hash_rate_growth'] = features['hash_rate'].pct_change()
            else:
                print("Warning: 'v' not found in HashRate data.")
            
        # if 'Fees' in miner_data:
        #     if 'v' in miner_data['Fees'].columns:
        #         features['miner_fees'] = miner_data['Fees']['v']
        #         if 'volume' in features.columns:
        #             features['fee_ratio'] = features['miner_fees'] / features['volume']
        #         else:
        #             print("Warning: 'volume' column not found in market data for fee_ratio calculation.")
        #     else:
        #         print("Warning: 'v' not found in Fees data.")
            
        # Remove any rows with NaN values after feature creation
        # features = features.dropna()

        # convert features into csv file 
        features.to_csv('features.csv', index=True)

        # fill emppty values with mean of the column except "start_time" and "date"
        for col in features.columns:
            if col not in ['start_time', 'date_x', 'date_y']:
                features[col].fillna(features[col].mean(), inplace=True)

        # Check features length
        if len(features) == 0:
            print("Warning: No features available after cleaning. Check input data.")
        
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