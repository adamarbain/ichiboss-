import pandas as pd
from typing import Dict, Any
from data.loader import DataLoader
from data.preprocessor import DataPreprocessor
from strategies.base import Strategy
from execution.order_manager import OrderManager
from analysis.metrics import PerformanceMetrics

class BacktestingEngine:
    def __init__(self, data_path: str, initial_capital: float = 100000):
        self.data_loader = DataLoader(data_path)
        self.preprocessor = DataPreprocessor()
        self.order_manager = OrderManager()
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        
    def run_backtest(self, strategy: Strategy, 
                    start_date: str = None,
                    end_date: str = None) -> Dict[str, Any]:
        """Run a backtest with the given strategy"""
        # Load and prepare data
        data = self.data_loader.load_all_data()
        market_data = data['market']
        network_data = data['network']
        miner_data = data['miner']
        
        # Preprocess data
        features = self.preprocessor.create_features(
            market_data, network_data, miner_data
        )
        
        # Filter by date range if specified
        if start_date:
            features = features[features.index >= start_date]
        if end_date:
            features = features[features.index <= end_date]
            
        # Generate signals
        signals = strategy.generate_signals(features)
        
        # Execute trades based on signals
        for date, row in signals.iterrows():
            if row['signal'] != 0:
                # Calculate position size
                position = strategy.calculate_position_size(
                    pd.DataFrame([row]), self.current_capital
                )
                
                # Create and execute order
                order = self.order_manager.create_order(
                    symbol='BTC',
                    order_type='buy' if row['signal'] > 0 else 'sell',
                    quantity=abs(position['position'].iloc[0] / features.loc[date, 'price']),
                    price=features.loc[date, 'price']
                )
                
                self.order_manager.execute_order(order, features.loc[date, 'price'])
                
                # Update capital
                if row['signal'] > 0:  # buy
                    self.current_capital -= order.quantity * features.loc[date, 'price']
                else:  # sell
                    self.current_capital += order.quantity * features.loc[date, 'price']
        
        # Calculate performance metrics
        metrics = PerformanceMetrics(
            self.order_manager.get_trade_history(),
            market_data,
            self.initial_capital
        )
        
        return {
            'metrics': metrics.calculate_metrics(),
            'report': metrics.generate_report(),
            'trade_history': self.order_manager.get_trade_history(),
            'final_capital': self.current_capital
        } 