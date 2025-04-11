from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any

class Strategy(ABC):
    def __init__(self, params: Dict[str, Any] = None):
        self.params = params or {}
        self.positions = pd.DataFrame()
        self.signals = pd.DataFrame()


    def next(self):
        pass
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on the strategy logic"""
        pass
    
    def calculate_position_size(self, signals: pd.DataFrame, 
                              portfolio_value: float) -> pd.DataFrame:
        """Calculate position sizes based on signals and portfolio value"""
        positions = signals.copy()
        positions['position'] = positions['signal'] * portfolio_value
        return positions
    
    def update_positions(self, new_positions: pd.DataFrame):
        """Update the current positions"""
        self.positions = new_positions
        
    def get_current_positions(self) -> pd.DataFrame:
        """Get the current positions"""
        return self.positions 