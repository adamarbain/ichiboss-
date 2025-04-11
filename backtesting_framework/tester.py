import pandas as pd
import numpy as np
from data.preprocessor import DataPreprocessor
from strategies import moving_average
from main import VectorBacktester
from analysis.metrics import AdvancedAnalyzer

preprocessor = DataPreprocessor()
temp = pd.read_csv('DOGE.csv')

clean_temp = preprocessor.clean_market_data(temp)
added_temp = preprocessor.add_returns(clean_temp)
print(added_temp)


strategy = moving_average.MovingAverageStrategy(added_temp)
strategy.generate_signals()

backtester = VectorBacktester(strategy=strategy)
backtester.run_backtest()

results = backtester.results

analysis = AdvancedAnalyzer(results)
print(f"Sharp: {analysis.sharpe_ratio()}")
print(f"MDD: {analysis.max_drawdown()}")
print(f"Donno this one: \n{analysis.plot_waterfall()}")



