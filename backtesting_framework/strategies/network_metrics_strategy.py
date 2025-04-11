import pandas as pd
import numpy as np
from typing import Dict, Any
from .base import Strategy

class NetworkMetricsStrategy(Strategy):
    def __init__(self, params: Dict[str, Any] = None):
        default_params = {
            'address_threshold': 0.05,  # 5% growth threshold
            'velocity_threshold': 0.1,  # 10% velocity threshold
            'hash_rate_threshold': 0.1,  # 10% hash rate growth threshold
            'position_size': 0.1  # 10% of portfolio per position
        }
        super().__init__(params or default_params)
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on network metrics"""
        signals = pd.DataFrame(index=data.index)
        
        # Initialize signal column
        signals['signal'] = 0
        
        # Generate buy signals based on network metrics
        buy_conditions = (
            (data['address_growth'] > self.params['address_threshold']) &
            (data['network_velocity'] > self.params['velocity_threshold']) &
            (data['hash_rate_growth'] > self.params['hash_rate_threshold'])
        )
        
        # Generate sell signals based on network metrics
        sell_conditions = (
            (data['address_growth'] < -self.params['address_threshold']) |
            (data['network_velocity'] < -self.params['velocity_threshold']) |
            (data['hash_rate_growth'] < -self.params['hash_rate_threshold'])
        )
        
        # Set signals
        signals.loc[buy_conditions, 'signal'] = 1
        signals.loc[sell_conditions, 'signal'] = -1
        
        # Store signals
        self.signals = signals
        
        return signals
    
    def calculate_position_size(self, signals: pd.DataFrame, 
                              portfolio_value: float) -> pd.DataFrame:
        """Calculate position sizes with network metrics strategy"""
        positions = signals.copy()
        positions['position'] = positions['signal'] * portfolio_value * self.params['position_size']
        return positions 