import pandas as pd
import numpy as np
from typing import Dict, List

class PerformanceMetrics:
    def __init__(self, trade_history: pd.DataFrame, 
                 market_data: pd.DataFrame,
                 initial_capital: float):
        self.trade_history = trade_history
        self.market_data = market_data.copy()  # Create a copy to avoid modifying original
        self.initial_capital = initial_capital
        
        # Ensure market data index is in the correct format
        if not isinstance(self.market_data.index, pd.DatetimeIndex):
            self.market_data.index = pd.to_datetime(self.market_data.index, unit='ms')
        
    def calculate_returns(self) -> pd.Series:
        """Calculate portfolio returns"""
        if len(self.trade_history) == 0:
            return pd.Series(0, index=self.market_data.index)
            
        # Sort trade history by timestamp and convert timestamps
        self.trade_history = self.trade_history.sort_values('timestamp')
        trade_dates = pd.to_datetime(self.trade_history['timestamp'], unit='ms')
        
        # Initialize portfolio tracking
        portfolio_value = self.initial_capital
        portfolio_holdings = 0
        daily_values = []
        dates = []
        
        # Create a date range for all trading days
        date_range = pd.date_range(
            start=self.market_data.index.min(),
            end=self.market_data.index.max(),
            freq='D'
        )
        
        for date in date_range:
            # Get trades for this date
            daily_trades = self.trade_history[
                trade_dates.dt.date == date.date()
            ]
            
            # Process trades for the day
            for _, trade in daily_trades.iterrows():
                if trade['type'] == 'buy':
                    cost = trade['quantity'] * trade['price']
                    if portfolio_value >= cost:
                        portfolio_value -= cost
                        portfolio_holdings += trade['quantity']
                    else:
                        # Not enough cash to buy - skip or partial buy
                        pass
                else:  # sell
                    if portfolio_holdings >= trade['quantity']:
                        portfolio_value += trade['quantity'] * trade['price']
                        portfolio_holdings -= trade['quantity']
                    else:
                        # Not enough holdings to sell - skip or partial sell
                        pass
                    
            # After handling trades
            # Find the closest market data point for this date
            try:
                closest_date = self.market_data.index[
                    self.market_data.index.get_indexer([date], method='nearest')
                ][0]
                current_price = self.market_data.loc[closest_date]['price_usd_close']
                
                # Calculate end-of-day portfolio value including holdings
                total_value = portfolio_value + (portfolio_holdings * current_price)
                
                daily_values.append(total_value)
                dates.append(date)
                
            except (KeyError, IndexError):
                continue  # Skip dates where we don't have market data
            
        # Calculate daily returns
        if not daily_values:  # If no valid data points
            return pd.Series(0, index=date_range)
            
        values_series = pd.Series(daily_values, index=dates)
        returns = values_series.pct_change().fillna(0)
        
        return returns
    
    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        returns = self.calculate_returns()
        if len(returns) < 2 or returns.std() == 0:
            return 0.0
            
        excess_returns = returns - risk_free_rate/252  # Daily risk-free rate
        sharpe = np.sqrt(252) * excess_returns.mean() / returns.std()
        return float(sharpe)
    
    def calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown"""
        returns = self.calculate_returns()
        if len(returns) == 0:
            return 0.0
            
        # Calculate cumulative returns
        cumulative_returns = (1 + returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdowns = cumulative_returns - rolling_max
        max_drawdown = (drawdowns / rolling_max).min()
        
        return float(max_drawdown) if not np.isnan(max_drawdown) else 0.0
    
    def calculate_win_rate(self) -> float:
        """Calculate win rate of trades"""
        if len(self.trade_history) == 0:
            return 0.0
            
        # Consider a trade winning if selling price > buying price
        trades = self.trade_history.copy()
        trades['pnl'] = trades.apply(
            lambda x: x['quantity'] * x['price'] * (1 if x['type'] == 'sell' else -1),
            axis=1
        )
        
        winning_trades = len(trades[trades['pnl'] > 0])
        return winning_trades / len(trades)
    
    def calculate_average_trade_return(self) -> float:
        """Calculate the average return per trade"""
        if len(self.trade_history) == 0:
            return 0.0
            
        # Pair buy and sell trades to calculate profit per round-trip trade
        buys = self.trade_history[self.trade_history['type'] == 'buy']
        sells = self.trade_history[self.trade_history['type'] == 'sell']
        
        if len(buys) == 0 or len(sells) == 0:
            return 0.0
            
        # Calculate total cost and proceeds
        total_buy_cost = (buys['quantity'] * buys['price']).sum()
        total_sell_proceeds = (sells['quantity'] * sells['price']).sum()
        
        # Total profit across all trades
        total_profit = total_sell_proceeds - total_buy_cost
        
        # Number of complete trades (buy+sell pairs)
        # In a simple strategy, this is typically the number of sells
        num_complete_trades = len(sells)
        
        if num_complete_trades > 0:
            return total_profit / num_complete_trades
        else:
            return 0.0
    
    def calculate_metrics(self) -> Dict[str, float]:
        """Calculate all performance metrics"""
        returns = self.calculate_returns()
        total_return = float((1 + returns).prod() - 1) if len(returns) > 0 else 0.0
        
        # Calculate average trade return correctly
        avg_trade_return = self.calculate_average_trade_return()

        metrics = {
            'total_return': total_return,
            'sharpe_ratio': self.calculate_sharpe_ratio(),
            'max_drawdown': self.calculate_max_drawdown(),
            'win_rate': self.calculate_win_rate(),
            'total_trades': len(self.trade_history),
            'avg_trade_return': avg_trade_return  # Fixed calculation
        }
        
        # Ensure all values are finite
        for key in metrics:
            if not np.isfinite(metrics[key]):
                metrics[key] = 0.0
                
        return metrics
    
    def generate_report(self) -> str:
        """Generate a performance report"""
        metrics = self.calculate_metrics()
        
        report = f"""
Performance Report
-----------------
Initial Capital: ${self.initial_capital:,.2f}
Total Return: {metrics['total_return']:.2%}
Sharpe Ratio: {metrics['sharpe_ratio']:.2f}
Max Drawdown: {metrics['max_drawdown']:.2%}
Win Rate: {metrics['win_rate']:.2%}
Total Trades: {metrics['total_trades']}
Average Trade Return: ${metrics['avg_trade_return']:,.2f}
"""
        return report