import pandas as pd
import numpy as np
from typing import Dict, List
import matplotlib.pyplot as plt

# class PerformanceMetrics:
#     def __init__(self, trade_history: pd.DataFrame, 
#                  market_data: pd.DataFrame,
#                  initial_capital: float):
#         self.trade_history = trade_history
#         self.market_data = market_data
#         self.initial_capital = initial_capital
        
#     def calculate_returns(self) -> pd.Series:
#         """Calculate portfolio returns"""
#         # Calculate daily portfolio value
#         portfolio_value = self.initial_capital
#         daily_values = []
        
#         for date in self.market_data.index:
#             # Get trades for this date
#             daily_trades = self.trade_history[self.trade_history['timestamp'].dt.date == date.date()]
            
#             # Calculate P&L from trades
#             trade_pnl = 0
#             for _, trade in daily_trades.iterrows():
#                 if trade['type'] == 'buy':
#                     trade_pnl -= trade['value']
#                 else:  # sell
#                     trade_pnl += trade['value']
            
#             portfolio_value += trade_pnl
#             daily_values.append(portfolio_value)
            
#         # Calculate returns
#         returns = pd.Series(daily_values, index=self.market_data.index).pct_change()
#         return returns
    
#     def calculate_sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
#         """Calculate Sharpe ratio"""
#         returns = self.calculate_returns()
#         excess_returns = returns - risk_free_rate/252  # Daily risk-free rate
#         return np.sqrt(252) * excess_returns.mean() / excess_returns.std()
    
#     def calculate_max_drawdown(self) -> float:
#         """Calculate maximum drawdown"""
#         returns = self.calculate_returns()
#         cumulative_returns = (1 + returns).cumprod()
#         rolling_max = cumulative_returns.expanding().max()
#         drawdowns = (cumulative_returns - rolling_max) / rolling_max
#         return drawdowns.min()
    
#     def calculate_win_rate(self) -> float:
#         """Calculate win rate of trades"""
#         if len(self.trade_history) == 0:
#             return 0.0
            
#         winning_trades = self.trade_history[
#             (self.trade_history['type'] == 'sell') & 
#             (self.trade_history['value'] > 0)
#         ]
#         return len(winning_trades) / len(self.trade_history)
    
#     def calculate_metrics(self) -> Dict[str, float]:
#         """Calculate all performance metrics"""
#         return {
#             'total_return': (1 + self.calculate_returns()).prod() - 1,
#             'sharpe_ratio': self.calculate_sharpe_ratio(),
#             'max_drawdown': self.calculate_max_drawdown(),
#             'win_rate': self.calculate_win_rate(),
#             'total_trades': len(self.trade_history),
#             'avg_trade_return': self.trade_history['value'].mean() if len(self.trade_history) > 0 else 0
#         }
    
#     def generate_report(self) -> str:
#         """Generate a performance report"""
#         metrics = self.calculate_metrics()
        
#         report = f"""
# Performance Report
# -----------------
# Initial Capital: ${self.initial_capital:,.2f}
# Total Return: {metrics['total_return']:.2%}
# Sharpe Ratio: {metrics['sharpe_ratio']:.2f}
# Max Drawdown: {metrics['max_drawdown']:.2%}
# Win Rate: {metrics['win_rate']:.2%}
# Total Trades: {metrics['total_trades']}
# Average Trade Return: ${metrics['avg_trade_return']:,.2f}
# """
#         return report 
    
class AdvancedAnalyzer:
    def __init__(self, results):
        self.equity = results['equity']
        self.returns = results['returns']
    
    def sharpe_ratio(self, risk_free_rate=0.02):
        excess_returns = self.returns - risk_free_rate/252
        return np.sqrt(252) * excess_returns.mean() / excess_returns.std()
    
    def max_drawdown(self):
        cumulative_max = self.equity.cummax()
        drawdown = (self.equity - cumulative_max) / cumulative_max
        return drawdown.min()
    
    def plot_waterfall(self):
        plt.figure(figsize=(10,6))
        plt.fill_between(self.equity.index, self.equity, 
                        where=self.equity >= self.equity.shift(1),
                        color='green', alpha=0.3)
        plt.fill_between(self.equity.index, self.equity,
                        where=self.equity < self.equity.shift(1),
                        color='red', alpha=0.3)
        plt.title("Equity Waterfall Chart")
