import pandas as pd

class MSNR:
    def __init__(self, df, breakout_min_excess_pct=0.0005):
        self.df = df.copy().reset_index(drop=True)
        self.min_excess = breakout_min_excess_pct
        self.levels = []

    def run(self):
        for i in range(1, len(self.df)):
            prev, curr = self.df.iloc[i-1], self.df.iloc[i]
            if prev['close'] > prev['open'] and curr['close'] < curr['open']:
                self.levels.append({'type': 'resistance', 'price': (prev['close']+curr['close'])/2, 'fresh': True})
            elif prev['close'] < prev['open'] and curr['close'] > curr['open']:
                self.levels.append({'type': 'support', 'price': (prev['close']+curr['close'])/2, 'fresh': True})
        return self.levels
