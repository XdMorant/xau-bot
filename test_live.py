from data_feed import get_gold_candles
from indicators.structure import MarketStructure
from indicators.msnr import MSNR
from grader import SetupGrader

def run():
    df = get_gold_candles("H1", 200)
    if df is None: return
    
    price = df.iloc[-1]['close']
    print(f"\n💰 Current Price: {price:.2f}")

    # Structure
    ms = MarketStructure(df)
    trend = ms.run()['current_trend']
    
    # MSNR
    msnr = MSNR(df)
    levels = msnr.run()

    # Grade
    grader = SetupGrader(price, trend, levels)
    result = grader.grade()

    print(f"\n📈 Trend: {trend}")
    print(f"🏆 Grade: {result['grade']} (Score: {result['score']})")
    for r in result['reasons']:
        print(f"  {r}")

if __name__ == "__main__":
    run()
