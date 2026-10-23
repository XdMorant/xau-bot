import os
import requests
import pandas as pd

def get_gold_candles(timeframe="H1", count=200):
    # Defaults to Binance PAXG. To use OANDA, set env vars:
    # export OANDA_API_KEY="your_key"
    oanda_key = os.getenv("OANDA_API_KEY")
    
    if oanda_key:
        return _fetch_oanda(timeframe, count, oanda_key)
    else:
        return _fetch_binance(timeframe, count)

def _fetch_binance(timeframe, count):
    print(f"🔄 Fetching XAU proxy ({timeframe}) from Binance PAXG...")
    tf_map = {"M": "1M", "W": "1w", "D": "1d", "H4": "4h", "H1": "1h", "M15": "15m", "M5": "5m"}
    url = f"https://api.binance.com/api/v3/klines?symbol=PAXGUSDT&interval={tf_map.get(timeframe, '1h')}&limit={count}"
    try:
        res = requests.get(url, timeout=10).json()
        df = pd.DataFrame([{
            "time": pd.to_datetime(c[0], unit='ms'),
            "open": float(c[1]), "high": float(c[2]),
            "low": float(c[3]), "close": float(c[4])
        } for c in res])
        return df
    except Exception as e:
        print(f"❌ Binance Error: {e}")
        return None

def _fetch_oanda(timeframe, count, api_key):
    print(f"🔄 Fetching XAU/USD ({timeframe}) from OANDA...")
    tf_map = {"M": "M", "W": "W", "D": "D", "H4": "H4", "H1": "H1", "M15": "M15", "M5": "M5"}
    url = f"https://api-fxpractice.oanda.com/v3/instruments/XAU_USD/candles"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"granularity": tf_map.get(timeframe, "H1"), "count": count, "price": "M"}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=10).json()
        df = pd.DataFrame([{
            "time": pd.to_datetime(c["time"]),
            "open": float(c["mid"]["o"]), "high": float(c["mid"]["h"]),
            "low": float(c["mid"]["l"]), "close": float(c["mid"]["c"])
        } for c in res["candles"] if c["complete"]])
        return df
    except Exception as e:
        print(f"❌ OANDA Error: {e}")
        return _fetch_binance(timeframe, count) # Fallback to Binance
