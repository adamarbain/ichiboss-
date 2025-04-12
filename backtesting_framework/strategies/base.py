from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any

class Strategy(ABC):
    def __init__(self, data):
        self.data = data  # Historical OHLCV data (Pandas DataFrame)
        self.signals = pd.DataFrame(index=data.index)  # Stores decisions
        self._validate_data()

    def _validate_data(self):
        """Like input sanitization - prevents garbage in/garbage out"""
        if self.data.isnull().values.any():
            raise ValueError("Missing data detected! Run clean_data() first.")
        
        # FROM BACKTESTING.py
        # self._indicators = []
        # self._broker: _Broker = broker
        # self._data: _Data = data
        # self._params = self._check_params(params)

    def calculate_sma(self, window=20):
        """Average of last 'window' prices - smoothens noise"""
        self.data[f'sma_{window}'] = (
            self.data['close'].rolling(window).mean()
        )

    def calculate_rsi(self, window=14):
        """Measures speed of price changes (0-100 scale)"""
        delta = self.data['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window).mean()
        loss = -delta.where(delta < 0, 0).rolling(window).mean()
        rs = gain / loss
        self.data['rsi'] = 100 - (100 / (1 + rs))

    def generate_signals(self):
        """Override this in child classes"""
        raise NotImplementedError("Implement strategy logic here!")
    
    # @abstractmethod
    # def init():
    #     pass

    # @abstractmethod
    # def next(self):
    #     pass
        
    # @abstractmethod
    # def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
    #     """Generate trading signals based on the strategy logic"""
    #     pass
    
    # def calculate_position_size(self, signals: pd.DataFrame, 
    #                           portfolio_value: float) -> pd.DataFrame:
    #     """Calculate position sizes based on signals and portfolio value"""
    #     positions = signals.copy()
    #     positions['position'] = positions['signal'] * portfolio_value
    #     return positions
    
    # def update_positions(self, new_positions: pd.DataFrame):
    #     """Update the current positions"""
    #     self.positions = new_positions
        
    # def get_current_positions(self) -> pd.DataFrame:
    #     """Get the current positions"""
    #     return self.positions 