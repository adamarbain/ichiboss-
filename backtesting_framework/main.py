import pandas as pd
from typing import Dict, Any
from backtesting_framework.data.loader import DataLoader
from backtesting_framework.data.preprocessor import DataPreprocessor
from backtesting_framework.strategies.base import Strategy
from backtesting_framework.execution.order_manager import OrderManager
from backtesting_framework.analysis.metrics import PerformanceMetrics

class BacktestingEngine:
    def __init__(self, data_path: str, initial_capital: float = 100000):
        self.data_loader = DataLoader(data_path)
        self.preprocessor = DataPreprocessor()
        self.order_manager = OrderManager()
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.current_position = 0  # Track current position in BTC
        
    def run_backtest(self, strategy: Strategy, 
                    start_timestamp: int = None,
                    end_timestamp: int = None) -> Dict[str, Any]:
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
        
        # Filter by timestamp range if specified
        if start_timestamp:
            features = features[features.index >= start_timestamp]
        if end_timestamp:
            features = features[features.index <= end_timestamp]
            
        if len(features) == 0:
            raise ValueError("No data available for the specified timestamp range")
            
        # Generate signals
        signals = strategy.generate_signals(features)
        
        # Execute trades based on signals
        for timestamp, row in signals.iterrows():
            if row['signal'] != 0:
                try:
                    print(f"\nTimestamp: {timestamp}")
                    print(f"Signal: {row['signal']}")
                    print(f"Current Capital: ${self.current_capital:,.2f}")
                    print(f"Current Position: {self.current_position} BTC")
                    
                    price = features.loc[timestamp, 'price_usd_close']
                    
                    if row['signal'] > 0:  # Buy signal
                        # Calculate position size based on available capital
                        position = strategy.calculate_position_size(
                            pd.DataFrame([row]), self.current_capital
                        )
                        quantity = abs(position['position'].iloc[0])
                        
                        if quantity > 0:
                            order = self.order_manager.create_order(
                                symbol='BTC',
                                order_type='buy',
                                quantity=quantity,
                                price=price,
                                timestamp=timestamp
                            )
                            
                    else:  # Sell signal
                        # Sell from existing position
                        quantity = self.current_position  # Sell entire position
                        
                        if quantity > 0:
                            order = self.order_manager.create_order(
                                symbol='BTC',
                                order_type='sell',
                                quantity=quantity,
                                price=price,
                                timestamp=timestamp
                            )
                    
                    if quantity > 0:
                        print(f"Order Type: {order.order_type}")
                        print(f"Order Quantity: {order.quantity}")
                        print(f"Order Price: ${price:,.2f}")
                        
                        self.order_manager.execute_order(order, price)
                        
                        # Update capital and position
                        if order.order_type == 'buy':
                            self.current_capital -= order.quantity * price
                            self.current_position += order.quantity
                        else:  # sell
                            self.current_capital += order.quantity * price
                            self.current_position -= order.quantity
                            
                        print(f"Updated Capital: ${self.current_capital:,.2f}")
                        print(f"Updated Position: {self.current_position} BTC")
                    
                except KeyError as e:
                    print(f"Warning: Missing data for timestamp {timestamp}: {e}")
                    continue
        
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