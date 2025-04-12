import pandas as pd
import numpy as np
import math

class Ichiboss:
    def z_score(data, window):
        roll = data.rolling(window, min_periods=1)
        mean = roll.mean()
        std = roll.std()

        return (mean - data)/ std

    def generate_position(data, threshold):
        z = data.z_score
        positions = [0]

        # high netflow volume = sell
        for score in z:
            if math.isnan(score):
                continue
            
            if score > threshold:
                position = -1
            else:
                position = 1
                
            positions.append(position)
            
        positions_series = pd.Series(positions)
        data['positions'] = positions_series  

        data['trades'] = abs(data.positions - data.positions.shift(1))

        return data

    def calc_metrics(data, fees, window):

        p_change = data.price_change
        position = data.positions.shift(1)
        trade = data.trades

        pnl = p_change*position-trade*fees
        data['pnl']= pnl

        data['equity'] = pnl.cumsum()

        avg_pnl = pnl.sum()/pnl.count()
        sharp_ratio = avg_pnl/pnl.std() * math.sqrt(365)
        
        trade_per_interval = data.trades.sum()/ data.trades.count()

        # drawdown = 
        
        currmax = data.equity.cummax()
        daily_drawdown = data.equity - currmax 

        data['drawdown'] = daily_drawdown
        MDD = daily_drawdown.min()

        print(MDD)
        return data, sharp_ratio, trade_per_interval, MDD