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
                    end_timestamp: int = None,
                    max_position_pct: float = 1.0,  # Max position size as percentage of capital
                    commission_pct: float = 0.002) -> Dict[str, Any]:  # 0.2% commission
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
        
        # Initialize trade history tracking
        trade_log = []
        
        # Execute trades based on signals
        for timestamp, row in signals.iterrows():
            if row['signal'] != 0:
                try:
                    print(f"\nTimestamp: {timestamp}")
                    print(f"Signal: {row['signal']}")
                    print(f"Current Capital: ${self.current_capital:,.2f}")
                    print(f"Current Position: {self.current_position} BTC")
                    
                    price = features.loc[timestamp, 'price_usd_close']
                    
                    if row['signal'] > 0 and self.current_position == 0:  # Buy signal and no position
                        # Calculate position size based on available capital
                        suggested_position = strategy.calculate_position_size(
                            pd.DataFrame([row]), self.current_capital
                        )
                        
                        # Safety check: limit position size
                        max_capital_to_use = self.current_capital * max_position_pct
                        suggested_quantity = abs(suggested_position['position'].iloc[0])
                        max_affordable_quantity = max_capital_to_use / price
                        quantity = min(suggested_quantity, max_affordable_quantity)
                        
                        # Apply commission to get actual cost
                        total_cost = quantity * price
                        commission = total_cost * commission_pct
                        total_cost_with_commission = total_cost + commission
                        
                        # Final check to ensure we don't exceed available capital
                        if total_cost_with_commission > self.current_capital:
                            quantity = (self.current_capital / (price * (1 + commission_pct)))
                            total_cost = quantity * price
                            commission = total_cost * commission_pct
                            total_cost_with_commission = total_cost + commission
                        
                        if quantity > 0:
                            order = self.order_manager.create_order(
                                symbol='BTC',
                                order_type='buy',
                                quantity=quantity,
                                price=price,
                                timestamp=timestamp
                            )
                            
                    elif row['signal'] < 0 and self.current_position > 0:  # Sell signal with existing position
                        # Sell entire position
                        quantity = self.current_position
                        
                        # Calculate commission
                        total_value = quantity * price
                        commission = total_value * commission_pct
                        
                        if quantity > 0:
                            order = self.order_manager.create_order(
                                symbol='BTC',
                                order_type='sell',
                                quantity=quantity,
                                price=price,
                                timestamp=timestamp
                            )
                    else:
                        # No valid action to take
                        continue
                    
                    if quantity > 0:
                        print(f"Order Type: {order.order_type}")
                        print(f"Order Quantity: {quantity}")
                        print(f"Order Price: ${price:,.2f}")
                        
                        self.order_manager.execute_order(order, price)
                        
                        # Update capital and position
                        if order.order_type == 'buy':
                            # Include commission in the cost
                            self.current_capital -= (quantity * price) * (1 + commission_pct)
                            self.current_position += quantity
                        else:  # sell
                            # Deduct commission from the proceeds
                            self.current_capital += (quantity * price) * (1 - commission_pct)
                            self.current_position = 0  # Completely exit position
                        
                        # Ensure capital doesn't go negative due to rounding errors
                        self.current_capital = max(0, self.current_capital)
                            
                        print(f"Updated Capital: ${self.current_capital:,.2f}")
                        print(f"Updated Position: {self.current_position} BTC")
                        
                        # Log trade for analysis
                        trade_log.append({
                            'timestamp': timestamp,
                            'type': order.order_type,
                            'price': price,
                            'quantity': quantity,
                            'capital_after': self.current_capital,
                            'position_after': self.current_position
                        })
                    
                except KeyError as e:
                    print(f"Warning: Missing data for timestamp {timestamp}: {e}")
                    continue
                except Exception as e:
                    print(f"Error executing order at {timestamp}: {e}")
                    continue
        
        # Close any remaining position at the end of the backtest
        if self.current_position > 0:
            final_price = features['price_usd_close'].iloc[-1]
            commission = (self.current_position * final_price) * commission_pct
            self.current_capital += (self.current_position * final_price) - commission
            self.current_position = 0
            
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
            'final_capital': self.current_capital,
            'trade_log': trade_log
        }