import requests
import pandas as pd

def get_gold_candles(timeframe="H1", count=200):
    # Coinbase PAXG-USD (Works on Vercel US servers)
    tf_map = {"M": "1M", "W": "1W", "D": "1D", "H4": "6H", "H1": "1H", "M15": "15M", "M5": "5M"}
    cb_tf = tf_map.get(timeframe, "1H")
    
    # Coinbase API granularity is in seconds
    granularity_map = {"1M": 2592000, "1W": 604800, "1D": 86400, "6H": 21600, "1H": 3600, "15M": 900, "5M": 300}
    gran = granularity_map.get(cb_tf, 3600)
    
    url = f"https://api.exchange.coinbase.com/products/PAXG-USD/candles?granularity={gran}"
    
    try:
        # Coinbase requires a User-Agent header
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10).json()
        
        # Coinbase returns data as: [time, low, high, open, close, volume]
        # We need to reverse it to be oldest to newest
        res.reverse()
        
        df = pd.DataFrame([{
            "time": pd.to_datetime(c[0], unit='s'),
            "open": float(c[3]),
            "high": float(c[2]),
            "low": float(c[1]),
            "close": float(c[4])
        } for c in res])
        
        return df.tail(count).reset_index(drop=True)
    except Exception as e:
        print(f"❌ Coinbase Error: {e}")
        return None
