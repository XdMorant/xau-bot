import pandas as pd

class MarketStructure:
    def __init__(self, df, swing_length=3):
        self.df = df.copy().reset_index(drop=True)
        self.sl = swing_length
        self.swings = []

    def run(self):
        for i in range(self.sl, len(self.df) - self.sl):
            if all(self.df.iloc[i]['high'] > self.df.iloc[i+j]['high'] and self.df.iloc[i]['high'] > self.df.iloc[i-j]['high'] for j in range(1, self.sl+1)):
                self.swings.append({'index': i, 'price': self.df.iloc[i]['high'], 'type': 'high'})
            if all(self.df.iloc[i]['low'] < self.df.iloc[i+j]['low'] and self.df.iloc[i]['low'] < self.df.iloc[i-j]['low'] for j in range(1, self.sl+1)):
                self.swings.append({'index': i, 'price': self.df.iloc[i]['low'], 'type': 'low'})
        
        trend = "BEARISH" if self.swings and self.swings[-1]['type'] == 'low' else "BULLISH"
        return {"current_trend": trend}
