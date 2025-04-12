from strategies import base
import numpy as np

class MovingAverageStrategy(base.Strategy):
    def generate_signals(self):
        self.calculate_sma(50)
        self.calculate_sma(200)
        self.signals['position'] = np.where(
            self.data['sma_50'] > self.data['sma_200'], 1, -1
        )